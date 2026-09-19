import tempfile
import unittest
from pathlib import Path

from rpg_character_rules import CharacterFieldIndex, CharacterSheet, CharacterStore, RulesEngine


POINT_BUY = {"STR": 15, "DEX": 15, "CON": 15, "INT": 8, "WIS": 8, "CHA": 8}
STANDARD = {"STR": 15, "DEX": 14, "CON": 13, "INT": 12, "WIS": 10, "CHA": 8}


class SchemaTests(unittest.TestCase):
    def test_schema_is_large_unique_and_deterministic(self) -> None:
        index = CharacterFieldIndex()
        fields = index.build_template()
        self.assertGreater(len(fields), 100)
        self.assertEqual(len(fields), len(index.by_key()))
        self.assertEqual([field.sort_index for field in fields], list(range(1, len(fields) + 1)))
        self.assertIn("spellcasting", index.sections())


class RulesTests(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = RulesEngine()

    def test_assignment_parser_requires_every_stat_once(self) -> None:
        parsed, error = self.engine.parse_ability_assignment("STR 15, DEX 14, CON 13, INT 12, WIS 10, CHA 8")
        self.assertIsNone(error)
        self.assertEqual(parsed, STANDARD)
        self.assertIsNotNone(self.engine.parse_ability_assignment("STR 10")[1])

    def test_point_buy_accepts_exact_budget(self) -> None:
        self.assertEqual(self.engine.validate_point_buy(POINT_BUY, "{}"), (True, None))

    def test_point_buy_rejects_wrong_shape_and_budget(self) -> None:
        valid, _ = self.engine.validate_point_buy({"STR": 15}, "{}")
        self.assertFalse(valid)
        valid, error = self.engine.validate_point_buy({**POINT_BUY, "CHA": 9}, "{}")
        self.assertFalse(valid)
        self.assertIn("27", error or "")

    def test_optional_unused_points_policy_is_supported(self) -> None:
        rules = '{"ability_generation":{"require_exact_budget":false}}'
        low = {"STR": 8, "DEX": 8, "CON": 8, "INT": 8, "WIS": 8, "CHA": 8}
        self.assertEqual(self.engine.validate_point_buy(low, rules), (True, None))

    def test_standard_array_compares_as_a_multiset(self) -> None:
        self.assertEqual(self.engine.validate_standard_array(STANDARD, "{}"), (True, None))
        invalid = dict(STANDARD)
        invalid["CHA"] = 10
        self.assertFalse(self.engine.validate_standard_array(invalid, "{}")[0])

    def test_modifiers_use_floor_division(self) -> None:
        self.assertEqual(self.engine.compute_ability_mod(9, "{}"), "-1")
        self.assertEqual(self.engine.compute_ability_mod(15, "{}"), "+2")


class SheetTests(unittest.TestCase):
    def test_create_populates_schema_and_name(self) -> None:
        sheet = CharacterSheet.create("  Mira   Vale ")
        self.assertEqual(sheet.name, "Mira Vale")
        self.assertEqual(sheet.fields["identity.character_name"], "Mira Vale")
        self.assertGreater(len(sheet.fields), 100)

    def test_update_is_revision_guarded(self) -> None:
        sheet = CharacterSheet.create("Mira")
        sheet.update("identity.race_species", "Human", expected_revision=1)
        self.assertEqual(sheet.revision, 2)
        with self.assertRaises(RuntimeError):
            sheet.update("identity.class_level", "Fighter", expected_revision=1)
        with self.assertRaises(KeyError):
            sheet.update("unknown", "x", expected_revision=2)

    def test_apply_abilities_sets_scores_and_modifiers_once(self) -> None:
        sheet = CharacterSheet.create("Mira")
        sheet.apply_abilities(POINT_BUY, mode="point_buy", expected_revision=1)
        self.assertEqual(sheet.revision, 2)
        self.assertEqual(sheet.fields["ability.str"], "15")
        self.assertEqual(sheet.fields["ability.str_mod"], "+2")

    def test_verify_reports_missing_and_invalid_values(self) -> None:
        sheet = CharacterSheet.create("Mira")
        self.assertGreater(len(sheet.verify()), 0)
        sheet.fields["ability.str"] = "fifteen"
        self.assertIn("invalid-ability", {issue.code for issue in sheet.verify()})


class StoreTests(unittest.TestCase):
    def test_store_create_load_list_and_update(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            store = CharacterStore(Path(temporary))
            created = store.create("Mira")
            loaded = store.load(created.sheet_id)
            self.assertEqual(loaded.name, "Mira")
            updated = store.update_field(created.sheet_id, "identity.class_level", "Fighter 1", expected_revision=1)
            self.assertEqual(updated.revision, 2)
            self.assertEqual(len(store.list()), 1)

    def test_store_rejects_stale_and_path_shaped_ids(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            store = CharacterStore(Path(temporary))
            sheet = store.create("Mira")
            sheet.update("identity.class_level", "Fighter 1", expected_revision=1)
            with self.assertRaises(RuntimeError):
                store.save(sheet, expected_previous_revision=0)
            with self.assertRaises(ValueError):
                store.load("../escape")


if __name__ == "__main__":
    unittest.main()
