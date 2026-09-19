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
