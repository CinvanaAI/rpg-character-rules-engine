import json
import pytest
from rpg_character_rules.rules import RulesEngine


@pytest.mark.parametrize("section", [None, [], "invalid", 5])
def test_malformed_sections_use_documented_defaults(section):
    rules = RulesEngine()
    config = json.dumps({"ability_generation": section, "derived": section})
    assert rules.validate_point_buy(dict(zip(("STR","DEX","CON","INT","WIS","CHA"), (15,15,15,8,8,8))), config) == (True, None)
    assert rules.validate_standard_array(dict(zip(("STR","DEX","CON","INT","WIS","CHA"), (15,14,13,12,10,8))), config) == (True, None)
    assert rules.compute_ability_mod(15, config) == "+2"


def test_missing_stats_and_non_integer_scores_fail():
    rules = RulesEngine()
    assert rules.validate_point_buy({"STR": 15, "DEX": 15, "CON": 15}, "{}")[0] is False
    assignment = dict(zip(("STR","DEX","CON","INT","WIS","CHA"), (15,14,13,12,10,8)))
    assignment["STR"] = 15.0
    assert rules.validate_standard_array(assignment, "{}")[0] is False
