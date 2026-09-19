# Origin

This repository is extracted from the February 2026 Persistent Discord RPG character subsystem.

The historical product represented every editable character field as a stable key that could map to a Discord message, persisted character pages and field bindings, and validated point-buy/standard-array ability generation through configurable rules JSON.

The public extraction retains the authored field taxonomy and numeric rules engine while removing Discord adapters, guild/channel/message identifiers, live SQLite state, credentials, campaign membership, and private characters. It adds platform-neutral sheets, strict schema loading, optimistic revisions, atomic JSON storage, synthetic examples, and independent tests.
