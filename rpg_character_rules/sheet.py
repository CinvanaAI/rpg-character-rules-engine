"""Schema-driven character sheets with revision guards and rules validation."""

from __future__ import annotations

import uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any

from .rules import STAT_KEYS, RulesEngine
from .schema import CharacterFieldIndex


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


@dataclass(frozen=True, slots=True)
class ValidationIssue:
    code: str
    field_key: str
    message: str


@dataclass(slots=True)
class CharacterSheet:
    sheet_id: str
    name: str
    created_at: str
    updated_at: str
    revision: int
    fields: dict[str, str]

    @classmethod
    def create(cls, name: str, schema: CharacterFieldIndex | None = None) -> "CharacterSheet":
        compact = " ".join(name.split())
        if not compact or len(compact) > 120:
            raise ValueError("Character name must contain between 1 and 120 characters.")
        index = schema or CharacterFieldIndex()
        fields = {field.field_key: field.default_value for field in index.build_template()}
        fields["identity.character_name"] = compact
        timestamp = _now()
        return cls(
            sheet_id="sheet-" + uuid.uuid4().hex[:12],
            name=compact,
            created_at=timestamp,
            updated_at=timestamp,
            revision=1,
            fields=fields,
        )

    def update(self, field_key: str, value: str, *, expected_revision: int) -> None:
        if expected_revision != self.revision:
            raise RuntimeError(f"Stale sheet revision: expected {expected_revision}, current {self.revision}.")
        if field_key not in self.fields:
            raise KeyError(f"Unknown character field: {field_key}")
        if not isinstance(value, str) or len(value) > 5_000:
            raise ValueError("Character field values must be strings no longer than 5,000 characters.")
        self.fields[field_key] = value
        if field_key == "identity.character_name" and value.strip():
            self.name = " ".join(value.split())[:120]
        self.revision += 1
        self.updated_at = _now()

    def apply_abilities(
        self,
        assignment: dict[str, int],
        *,
        mode: str,
        rules_json: str = "{}",
        expected_revision: int,
    ) -> None:
        if expected_revision != self.revision:
            raise RuntimeError(f"Stale sheet revision: expected {expected_revision}, current {self.revision}.")
        engine = RulesEngine()
        if mode == "point_buy":
            valid, error = engine.validate_point_buy(assignment, rules_json)
        elif mode == "standard_array":
            valid, error = engine.validate_standard_array(assignment, rules_json)
        else:
            raise ValueError("mode must be point_buy or standard_array")
        if not valid:
            raise ValueError(error or "Ability assignment is invalid.")
        for stat in STAT_KEYS:
            score = assignment[stat]
            key = stat.casefold()
            self.fields[f"ability.{key}"] = str(score)
            self.fields[f"ability.{key}_mod"] = engine.compute_ability_mod(score, rules_json)
        self.revision += 1
        self.updated_at = _now()

    def verify(self, required_fields: tuple[str, ...] | None = None) -> tuple[ValidationIssue, ...]:
        required = required_fields or (
            "identity.character_name",
            "identity.race_species",
            "identity.class_level",
            "ability.str",
            "ability.dex",
            "ability.con",
            "ability.int",
            "ability.wis",
            "ability.cha",
        )
        issues: list[ValidationIssue] = []
        for key in required:
            if key not in self.fields:
                issues.append(ValidationIssue("unknown-required-field", key, "Required field is not in the schema."))
            elif not self.fields[key].strip():
                issues.append(ValidationIssue("missing-value", key, "Required field is empty."))
        for stat in STAT_KEYS:
            key = f"ability.{stat.casefold()}"
            value = self.fields.get(key, "")
            if value:
                try:
                    parsed = int(value)
                except ValueError:
                    issues.append(ValidationIssue("invalid-ability", key, "Ability score must be an integer."))
                    continue
                if not 1 <= parsed <= 30:
                    issues.append(ValidationIssue("ability-range", key, "Ability score must be between 1 and 30."))
        return tuple(issues)

    def to_payload(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_payload(cls, payload: dict[str, Any], schema: CharacterFieldIndex | None = None) -> "CharacterSheet":
        if not isinstance(payload, dict) or not isinstance(payload.get("fields"), dict):
            raise ValueError("Invalid character-sheet payload.")
        index = schema or CharacterFieldIndex()
        allowed = index.by_key()
        fields = {str(key): str(value) for key, value in payload["fields"].items()}
        unknown = sorted(set(fields) - set(allowed))
        if unknown:
            raise ValueError(f"Unknown character fields: {', '.join(unknown[:5])}")
        complete_fields = {key: fields.get(key, field.default_value) for key, field in allowed.items()}
        return cls(
            sheet_id=str(payload.get("sheet_id") or ""),
            name=str(payload.get("name") or ""),
            created_at=str(payload.get("created_at") or ""),
            updated_at=str(payload.get("updated_at") or ""),
            revision=int(payload.get("revision") or 0),
            fields=complete_fields,
        )
