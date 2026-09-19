# Security and Data Handling

- Character sheets may contain names, backstories, fears, relationships, notes, and other personal material. Treat runtime stores as private user content.
- Sheet IDs and paths are generated or validated and remain under a caller-selected store root.
- Existing records require an expected revision before replacement, and saved revisions must advance.
- Writes use temporary files and atomic replacement.
- Individual values are bounded to 5,000 characters and complete sheets to two megabytes.
- Rules JSON is parsed as data and never evaluated as code.
- This package does not provide authentication, encryption, multi-user authorization, or network synchronization.

Do not commit live character stores merely because the code repository is public.
