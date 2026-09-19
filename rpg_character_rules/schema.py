"""Stable, platform-neutral character-field template definitions."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CharacterField:
    """One editable field in a deterministic character-sheet schema."""

    field_key: str
    label: str
    default_value: str
    section: str
    sort_index: int


class CharacterFieldIndex:
    """Builds a stable, ordered field template for character sheets."""

    def build_template(self) -> list[CharacterField]:
        """Return all editable fields in deterministic creation order."""
        raw_fields: list[tuple[str, str, str]] = [
            ("identity", "identity.player", "Player"),
            ("identity", "identity.character_name", "Character Name"),
            ("identity", "identity.pronouns", "Pronouns"),
            ("identity", "identity.race_species", "Race/Species"),
            ("identity", "identity.class_level", "Class & Level"),
            ("identity", "identity.background", "Background"),
            ("identity", "identity.alignment", "Alignment"),
            ("identity", "identity.xp_milestone", "XP / Milestone"),
            ("ability", "ability.str", "STR"),
            ("ability", "ability.str_mod", "STR Mod"),
            ("ability", "ability.dex", "DEX"),
            ("ability", "ability.dex_mod", "DEX Mod"),
            ("ability", "ability.con", "CON"),
            ("ability", "ability.con_mod", "CON Mod"),
            ("ability", "ability.int", "INT"),
            ("ability", "ability.int_mod", "INT Mod"),
            ("ability", "ability.wis", "WIS"),
            ("ability", "ability.wis_mod", "WIS Mod"),
            ("ability", "ability.cha", "CHA"),
            ("ability", "ability.cha_mod", "CHA Mod"),
            ("core", "core.proficiency_bonus", "Proficiency Bonus"),
            ("core", "core.initiative", "Initiative"),
            ("core", "core.speed", "Speed"),
            ("core", "core.passive_perception", "Passive Perception"),
            ("core", "core.passive_insight", "Passive Insight"),
            ("core", "core.passive_investigation", "Passive Investigation"),
            ("saves", "saves.str_prof", "STR Save Proficient"),
            ("saves", "saves.str_notes", "STR Save Notes"),
            ("saves", "saves.dex_prof", "DEX Save Proficient"),
            ("saves", "saves.dex_notes", "DEX Save Notes"),
            ("saves", "saves.con_prof", "CON Save Proficient"),
            ("saves", "saves.con_notes", "CON Save Notes"),
            ("saves", "saves.int_prof", "INT Save Proficient"),
            ("saves", "saves.int_notes", "INT Save Notes"),
            ("saves", "saves.wis_prof", "WIS Save Proficient"),
            ("saves", "saves.wis_notes", "WIS Save Notes"),
            ("saves", "saves.cha_prof", "CHA Save Proficient"),
            ("saves", "saves.cha_notes", "CHA Save Notes"),
            ("skills", "skills.acrobatics", "Acrobatics (DEX)"),
            ("skills", "skills.animal_handling", "Animal Handling (WIS)"),
            ("skills", "skills.arcana", "Arcana (INT)"),
            ("skills", "skills.athletics", "Athletics (STR)"),
            ("skills", "skills.deception", "Deception (CHA)"),
            ("skills", "skills.history", "History (INT)"),
            ("skills", "skills.insight", "Insight (WIS)"),
            ("skills", "skills.intimidation", "Intimidation (CHA)"),
            ("skills", "skills.investigation", "Investigation (INT)"),
            ("skills", "skills.medicine", "Medicine (WIS)"),
            ("skills", "skills.nature", "Nature (INT)"),
            ("skills", "skills.perception", "Perception (WIS)"),
            ("skills", "skills.performance", "Performance (CHA)"),
            ("skills", "skills.persuasion", "Persuasion (CHA)"),
            ("skills", "skills.religion", "Religion (INT)"),
            ("skills", "skills.sleight_of_hand", "Sleight of Hand (DEX)"),
            ("skills", "skills.stealth", "Stealth (DEX)"),
            ("skills", "skills.survival", "Survival (WIS)"),
            ("combat", "combat.ac", "Armor Class (AC)"),
            ("combat", "combat.hp_max", "Hit Points (Max)"),
            ("combat", "combat.hp_current", "Hit Points (Current)"),
            ("combat", "combat.temp_hp", "Temp HP"),
            ("combat", "combat.hit_dice", "Hit Dice"),
            ("combat", "combat.death_saves_success", "Death Saves Success"),
            ("combat", "combat.death_saves_fail", "Death Saves Fail"),
            ("combat", "combat.conditions_status", "Conditions / Status"),
            ("attacks", "attacks.attack_1_name", "Attack 1 Name"),
            ("attacks", "attacks.attack_1_bonus", "Attack 1 Bonus"),
            ("attacks", "attacks.attack_1_damage_type", "Attack 1 Damage/Type"),
            ("attacks", "attacks.attack_1_notes", "Attack 1 Notes"),
            ("attacks", "attacks.attack_2_name", "Attack 2 Name"),
            ("attacks", "attacks.attack_2_bonus", "Attack 2 Bonus"),
            ("attacks", "attacks.attack_2_damage_type", "Attack 2 Damage/Type"),
            ("attacks", "attacks.attack_2_notes", "Attack 2 Notes"),
            ("attacks", "attacks.attack_3_name", "Attack 3 Name"),
            ("attacks", "attacks.attack_3_bonus", "Attack 3 Bonus"),
            ("attacks", "attacks.attack_3_damage_type", "Attack 3 Damage/Type"),
            ("attacks", "attacks.attack_3_notes", "Attack 3 Notes"),
            (
                "attacks",
                "attacks.common_actions_bonus_reactions",
                "Common Actions / Bonus Actions / Reactions",
            ),
            ("equipment", "equipment.armor", "Armor"),
            ("equipment", "equipment.weapons", "Weapons"),
            ("equipment", "equipment.tools", "Tools"),
            ("equipment", "equipment.gear", "Gear"),
            ("equipment", "equipment.consumables", "Consumables"),
            ("equipment", "equipment.containers", "Containers (packs/bags)"),
            ("wealth", "wealth.cp", "CP"),
            ("wealth", "wealth.sp", "SP"),
            ("wealth", "wealth.ep", "EP"),
            ("wealth", "wealth.gp", "GP"),
            ("wealth", "wealth.pp", "PP"),
            ("wealth", "wealth.valuables_treasure", "Valuables / Treasure"),
            ("features", "features.racial_species_traits", "Racial / Species Traits"),
            ("features", "features.class_features", "Class Features"),
            ("features", "features.feats", "Feats"),
            ("features", "features.special_abilities", "Special Abilities"),
            ("proficiencies", "proficiencies.armor", "Armor Proficiency"),
            ("proficiencies", "proficiencies.weapons", "Weapons Proficiency"),
            ("proficiencies", "proficiencies.tools", "Tools Proficiency"),
            ("proficiencies", "proficiencies.languages", "Languages"),
            ("personality", "personality.traits", "Personality Traits"),
            ("personality", "personality.ideals", "Ideals"),
            ("personality", "personality.bonds", "Bonds"),
            ("personality", "personality.flaws", "Flaws"),
            ("personality", "personality.fears_triggers", "Fears / Triggers"),
            ("personality", "personality.motivations", "Motivations"),
            ("backstory", "backstory.origin", "Origin"),
            ("backstory", "backstory.key_events", "Key Events"),
            ("backstory", "backstory.secrets", "Secrets"),
            ("backstory", "backstory.important_people", "Important People"),
            ("backstory", "backstory.personal_goals", "Personal Goals"),
            ("appearance", "appearance.age", "Age"),
            ("appearance", "appearance.height", "Height"),
            ("appearance", "appearance.weight", "Weight"),
            ("appearance", "appearance.eyes", "Eyes"),
            ("appearance", "appearance.skin", "Skin"),
            ("appearance", "appearance.hair", "Hair"),
            ("appearance", "appearance.style_markings", "Style / Markings"),
            ("appearance", "appearance.vibe_presence", "Vibe / Presence"),
            ("allies", "allies.allies", "Allies"),
            ("allies", "allies.enemies", "Enemies"),
            ("allies", "allies.factions_guilds", "Factions / Guilds"),
            ("allies", "allies.patrons", "Patrons"),
            ("allies", "allies.symbols_tokens", "Symbols / Tokens"),
            ("spellcasting", "spellcasting.class", "Spellcasting Class"),
            ("spellcasting", "spellcasting.ability", "Spellcasting Ability"),
            ("spellcasting", "spellcasting.save_dc", "Spell Save DC"),
            ("spellcasting", "spellcasting.attack_bonus", "Spell Attack Bonus"),
            (
                "spellcasting",
                "spellcasting.prepared_known_notes",
                "Prepared / Known Rules Notes",
            ),
            ("resources", "resources.spell_slots_l1_l9", "Spell Slots (L1-L9)"),
            (
                "resources",
                "resources.class_resources",
                "Class Resources (Ki/Sorcery/etc)",
            ),
            ("resources", "resources.limited_use_features", "Limited-Use Features"),
            ("notes", "notes.session_log", "Session Log"),
            ("notes", "notes.quest_threads", "Quest Threads"),
            ("notes", "notes.important_clues", "Important Clues"),
            ("notes", "notes.npc_names", "NPC Names"),
            ("notes", "notes.loot_changes", "Loot / Changes"),
        ]

        return [
            CharacterField(
                field_key=field_key,
                label=label,
                default_value="",
                section=section,
                sort_index=index,
            )
            for index, (section, field_key, label) in enumerate(raw_fields, start=1)
        ]

    def by_key(self) -> dict[str, CharacterField]:
        fields = self.build_template()
        result = {field.field_key: field for field in fields}
        if len(result) != len(fields):
            raise ValueError("Character schema contains duplicate field keys.")
        return result

    def sections(self) -> tuple[str, ...]:
        return tuple(dict.fromkeys(field.section for field in self.build_template()))
