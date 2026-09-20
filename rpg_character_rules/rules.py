"""Rules parsing and validation helpers for platform-neutral character generation."""

from __future__ import annotations

import json
import re
from collections import Counter


STAT_KEYS = ("STR", "DEX", "CON", "INT", "WIS", "CHA")
DEFAULT_POINT_BUY_BUDGET = 27
DEFAULT_POINT_BUY_MIN = 8
DEFAULT_POINT_BUY_MAX = 15
DEFAULT_POINT_BUY_COST_TABLE = {
    8: 0,
    9: 1,
    10: 2,
    11: 3,
    12: 4,
    13: 5,
    14: 7,
    15: 9,
}
DEFAULT_STANDARD_ARRAY = [15, 14, 13, 12, 10, 8]


class RulesEngine:
    """Parses and validates ability generation input from ruleset JSON."""

    def __init__(self) -> None:
        pass

    def parse_ability_assignment(self, text: str) -> tuple[dict[str, int] | None, str | None]:
        """Parse one-line ability assignment text into a stat dictionary."""
        parts = [part.strip() for part in text.split(",") if part.strip()]
        if len(parts) != 6:
            return None, "Provide all six stats exactly once."

        assignment: dict[str, int] = {}
        for part in parts:
            match = re.fullmatch(r"(STR|DEX|CON|INT|WIS|CHA)\s+(-?\d+)", part, re.IGNORECASE)
            if not match:
                return None, f"Invalid segment: '{part}'. Use format like STR 15."
            stat = match.group(1).upper()
            value = int(match.group(2))
            if stat in assignment:
                return None, f"Duplicate stat: {stat}."
            assignment[stat] = value

        missing = [stat for stat in STAT_KEYS if stat not in assignment]
        if missing:
            return None, "Provide all six stats exactly once."

        return assignment, None

    def validate_point_buy(self, assignment: dict[str, int], rules_json: str) -> tuple[bool, str | None]:
        """Validate point-buy assignment against rules JSON with safe fallback."""
        key_error = self._validate_stat_keys(assignment)
        if key_error:
            return False, key_error
        rules = self._load_rules(rules_json)
        ability_rules = rules.get("ability_generation", {})
        if not isinstance(ability_rules, dict):
            ability_rules = {}

        budget = self._int_or_default(ability_rules.get("budget"), DEFAULT_POINT_BUY_BUDGET)
        minimum = self._int_or_default(ability_rules.get("min"), DEFAULT_POINT_BUY_MIN)
        maximum = self._int_or_default(ability_rules.get("max"), DEFAULT_POINT_BUY_MAX)
        raw_cost_table = ability_rules.get("cost_table")
        cost_table = self._parse_cost_table(raw_cost_table)
        if cost_table is None:
            cost_table = DEFAULT_POINT_BUY_COST_TABLE

        total_cost = 0
        for stat, value in assignment.items():
            if value < minimum or value > maximum:
                return False, f"{stat} must be between {minimum} and {maximum}."
            if value not in cost_table:
                return False, f"{stat} score {value} is not allowed by policy."
            total_cost += cost_table[value]

        require_exact = ability_rules.get("require_exact_budget", True) is not False
        if require_exact and total_cost != budget:
            return False, f"Total point-buy cost must equal {budget} (got {total_cost})."
        if not require_exact and total_cost > budget:
            return False, f"Total point-buy cost must not exceed {budget} (got {total_cost})."

        return True, None

    def validate_standard_array(self, assignment: dict[str, int], rules_json: str) -> tuple[bool, str | None]:
        """Validate standard-array assignment against rules JSON with safe fallback."""
        key_error = self._validate_stat_keys(assignment)
        if key_error:
            return False, key_error
        rules = self._load_rules(rules_json)
        ability_rules = rules.get("ability_generation", {})
        if not isinstance(ability_rules, dict):
            ability_rules = {}
        raw_array = ability_rules.get("array")
        if not isinstance(raw_array, list) or len(raw_array) != 6:
            array = DEFAULT_STANDARD_ARRAY
        else:
            try:
                array = [int(v) for v in raw_array]
            except (TypeError, ValueError):
                array = DEFAULT_STANDARD_ARRAY

        if Counter(assignment.values()) != Counter(array):
            return False, f"Values must match standard array exactly: {array}."
        return True, None

    def compute_ability_mod(self, score: int, rules_json: str) -> str:
        """Compute formatted ability modifier from score."""
        rules = self._load_rules(rules_json)
        derived = rules.get("derived", {})
        if not isinstance(derived, dict):
            derived = {}
        mode = derived.get("ability_mod")
        if mode != "5e_standard":
            mode = "5e_standard"

        if mode == "5e_standard":
            value = (score - 10) // 2
        else:
            value = (score - 10) // 2

        return f"{value:+d}"

    def _load_rules(self, rules_json: str) -> dict:
        try:
            data = json.loads(rules_json)
        except (json.JSONDecodeError, TypeError):
            return {}
        if isinstance(data, dict):
            return data
        return {}

    def _parse_cost_table(self, raw: object) -> dict[int, int] | None:
        if not isinstance(raw, dict):
            return None
        parsed: dict[int, int] = {}
        try:
            for key, value in raw.items():
                parsed[int(key)] = int(value)
        except (TypeError, ValueError):
            return None
        return parsed

    def _int_or_default(self, value: object, default: int) -> int:
        try:
            return int(value)
        except (TypeError, ValueError):
            return default

    def _validate_stat_keys(self, assignment: dict[str, int]) -> str | None:
        if set(assignment) != set(STAT_KEYS):
            return "Assignment must contain exactly STR, DEX, CON, INT, WIS, and CHA."
        if any(isinstance(value, bool) or not isinstance(value, int) for value in assignment.values()):
            return "Every ability score must be an integer."
        return None
