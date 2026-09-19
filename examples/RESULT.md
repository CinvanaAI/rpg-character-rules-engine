# Recorded first use

This output was produced by the included example with network connections disabled. Synthetic provider or worker replies are identified by the example; no real model quality or billing is implied.

From the installed checkout:

```sh
python -m examples.offline_demo
```

[Complete recorded output](result.json)

```text
{
  "mode": "Synthetic character; actual rules and revisioned persistence",
  "name": "Mira Vale",
  "abilities": {
    "STR": "15",
    "DEX": "15",
    "CON": "15",
    "INT": "8",
    "WIS": "8",
    "CHA": "8"
  },
  "class": "Fighter 1",
  "revision": 4,
  "required_profile_issues": [],
  "invalid_ability_rejected": "STR must be between 8 and 15.",
  "stale_edit_rejected": "Stale sheet revision: expected 1, current 4.",
  "other_blank_fields": 119
}
```

Generated timestamps and synthetic identifiers can change between runs. The demonstrated behavior and input fixture remain inspectable in the adjacent example files.
