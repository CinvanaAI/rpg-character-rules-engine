"""Atomic JSON persistence with optimistic revision checks."""

from __future__ import annotations

import json
import os
import re
import tempfile
from pathlib import Path

from .sheet import CharacterSheet


SHEET_ID = re.compile(r"^sheet-[a-f0-9]{12}$")


def _atomic(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary_name = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(handle, "wb") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary_name, path)
    except Exception:
        try:
            os.unlink(temporary_name)
        except FileNotFoundError:
            pass
        raise


class CharacterStore:
    def __init__(self, root: Path) -> None:
        self.root = root.resolve()
        self.root.mkdir(parents=True, exist_ok=True)

    def _path(self, sheet_id: str) -> Path:
        if not SHEET_ID.fullmatch(sheet_id):
            raise ValueError("Invalid sheet id.")
        path = (self.root / f"{sheet_id}.json").resolve()
        if path.parent != self.root:
            raise ValueError("Sheet path escaped the store root.")
        return path

    def create(self, name: str) -> CharacterSheet:
        sheet = CharacterSheet.create(name)
        self.save(sheet, expected_previous_revision=None)
        return sheet

    def load(self, sheet_id: str) -> CharacterSheet:
        payload = json.loads(self._path(sheet_id).read_text(encoding="utf-8"))
        sheet = CharacterSheet.from_payload(payload)
        if sheet.sheet_id != sheet_id:
            raise ValueError("Sheet identity does not match its file name.")
        return sheet

    def save(self, sheet: CharacterSheet, *, expected_previous_revision: int | None) -> Path:
        path = self._path(sheet.sheet_id)
        if path.exists():
            if expected_previous_revision is None:
                raise FileExistsError(sheet.sheet_id)
            current = self.load(sheet.sheet_id)
            if current.revision != expected_previous_revision:
                raise RuntimeError(
                    f"Stored revision changed: expected {expected_previous_revision}, current {current.revision}."
                )
            if sheet.revision <= current.revision:
                raise ValueError("Saved sheet revision must advance.")
        elif expected_previous_revision is not None:
            raise FileNotFoundError(sheet.sheet_id)
        payload = json.dumps(sheet.to_payload(), indent=2, ensure_ascii=False, sort_keys=True).encode("utf-8") + b"\n"
        if len(payload) > 2_000_000:
            raise ValueError("Sheet payload exceeds the two-megabyte bound.")
        _atomic(path, payload)
        return path

    def update_field(self, sheet_id: str, field_key: str, value: str, *, expected_revision: int) -> CharacterSheet:
        sheet = self.load(sheet_id)
        sheet.update(field_key, value, expected_revision=expected_revision)
        self.save(sheet, expected_previous_revision=expected_revision)
        return sheet

    def list(self) -> tuple[CharacterSheet, ...]:
        sheets: list[CharacterSheet] = []
        for path in sorted(self.root.glob("sheet-*.json")):
            try:
                sheets.append(self.load(path.stem))
            except (ValueError, json.JSONDecodeError, OSError):
                continue
        return tuple(sheets)
