# RPG Character Rules

Create and validate character-sheet data without running a Discord bot.

## Try it

Python 3.11+. Run from this checkout:

```sh
python -m pip install -e .
python -m examples.offline_demo
```

**Input:** A synthetic character and a 27-point ability assignment.

**Result:** The example saves and reopens the character, changes two identity fields, rejects an invalid ability assignment and reports remaining completeness checks. It uses disposable local files.

See [the captured example](examples/RESULT.md) for the actual output.

## How it works

[Ability rules](rpg_character_rules/rules.py) validate numeric assignments independently of a chat interface. [The character package](rpg_character_rules) combines a blank field schema with revisioned edits and storage, so stale updates can be rejected.

## Use it for your work

Follow `examples/offline_demo.py` to create a `CharacterStore`, apply abilities, and save using the expected prior revision. Start with the identity and six ability fields before exposing the full sheet.

## Scope

This is a character-data and numeric-rules utility, not a complete tabletop ruleset. Valid abilities do not fill every field or prove a finished character. Default point-buy and standard-array profiles can be selected explicitly.

Owned code is available under the [MIT license](LICENSE.md).

## Compare the numeric policies

Run `python -m examples.rules_demo` and inspect [the complete assignments and results](examples/rules-result.json). Three 15s and three 8s spend the default 27-point budget, but are not the standard array. Six 8s fail the default exact-budget policy; `require_exact_budget: false` explicitly permits unspent points. Standard-array validation compares the multiset, so assignments may place its six values in any abilities.

`RulesEngine` falls back to defaults for unreadable rules JSON and malformed nested sections. That makes its default profile usable but is not strict rules-configuration validation: inspect custom policies before relying on them. All six ability keys are required, and scores must be integers rather than booleans or floats. Modifiers use floor division `(score - 10) // 2`.

`CharacterSheet` owns validated field edits and revision advancement; `CharacterStore` persists JSON using an atomic file replacement. Its optimistic checks catch stale sequential edits, but the read/check/replace sequence is not a cross-process lock. Serialize writers externally. `verify()` checks a required profile, not every field or a full game's character legality; the demo intentionally reports 119 remaining blank fields.

[Origin](ORIGIN.md) distinguishes the extraction from [Persistent Discord RPG](https://github.com/CinvanaAI/persistent-discord-rpg). Malformed-section handling and the policy comparison are public continuation work. Class/ancestry progression and a graphical character creator are possible future consumers, not provided behavior.
