"""Rules-input regressions for the standard-library unittest CI runner."""
import json
import unittest

from rpg_character_rules.rules import RulesEngine


class RulesInputBoundaryTests(unittest.TestCase):
    def _assert_documented_defaults(self, section):
        rules = RulesEngine()
        config = json.dumps({"ability_generation": section, "derived": section})
        stats = ("STR", "DEX", "CON", "INT", "WIS", "CHA")
        point_buy = dict(zip(stats, (15, 15, 15, 8, 8, 8)))
        standard_array = dict(zip(stats, (15, 14, 13, 12, 10, 8)))
        self.assertEqual(rules.validate_point_buy(point_buy, config), (True, None))
        self.assertEqual(rules.validate_standard_array(standard_array, config), (True, None))
        self.assertEqual(rules.compute_ability_mod(15, config), "+2")

    def test_null_sections_use_documented_defaults(self):
        self._assert_documented_defaults(None)

    def test_list_sections_use_documented_defaults(self):
        self._assert_documented_defaults([])

    def test_string_sections_use_documented_defaults(self):
        self._assert_documented_defaults("invalid")

    def test_integer_sections_use_documented_defaults(self):
        self._assert_documented_defaults(5)

    def test_missing_stats_and_non_integer_scores_fail(self):
        rules = RulesEngine()
        self.assertIs(
            rules.validate_point_buy({"STR": 15, "DEX": 15, "CON": 15}, "{}")[0],
            False,
        )
        assignment = dict(zip(
            ("STR", "DEX", "CON", "INT", "WIS", "CHA"),
            (15, 14, 13, 12, 10, 8),
        ))
        assignment["STR"] = 15.0
        self.assertIs(rules.validate_standard_array(assignment, "{}")[0], False)


if __name__ == "__main__":
    unittest.main()
