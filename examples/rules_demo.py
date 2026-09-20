"""Synthetic numeric policies; no character-lore or external rules database."""
import json
from rpg_character_rules.rules import RulesEngine, STAT_KEYS

rules = RulesEngine()
point_buy = dict(zip(STAT_KEYS, [15, 15, 15, 8, 8, 8]))
standard = dict(zip(STAT_KEYS, [15, 14, 13, 12, 10, 8]))
low = dict.fromkeys(STAT_KEYS, 8)
result = {"assignments": {"point_buy": point_buy, "standard": standard, "unspent": low},
    "point_buy_valid": rules.validate_point_buy(point_buy, "{}"),
    "standard_array_valid": rules.validate_standard_array(standard, "{}"),
    "point_buy_as_standard_array": rules.validate_standard_array(point_buy, "{}"),
    "unspent_default": rules.validate_point_buy(low, "{}"),
    "unspent_allowed_explicitly": rules.validate_point_buy(low, '{"ability_generation":{"require_exact_budget":false}}'),
    "malformed_section_fallback": rules.validate_point_buy(point_buy, '{"ability_generation":null}')}
assert result["point_buy_valid"][0] and result["standard_array_valid"][0]
assert not result["point_buy_as_standard_array"][0] and not result["unspent_default"][0]
print(json.dumps(result, indent=2))
