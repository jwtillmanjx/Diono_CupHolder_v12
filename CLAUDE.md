# Diono Car-Seat Cup Holder — Project Instructions

## At the start of every session
Read `Diono_CupHolder_Session_Context.md` (in the repo root, next to this file) in full before doing anything else.

It holds the full design history, hard constraints, current geometry, print settings, open items, and the rebuild script. Treat it as the source of truth for where the project stands.

## Cloud sessions (Claude Code on the web)
Bambu Studio is only installed on James's Windows PC, so a cloud session can't run `Diono_CupHolder_v13_bambu_project.py`.
- In the cloud, run the generator, verify and images scripts as usual, but **skip the Bambu project step**.
- The print project `Diono_CupHolder_v13_Cup_and_SnapDisc.3mf` will then be missing or out of date. If an out-of-date copy is in the repo, delete it (see the one-design rule below). Say so clearly in the final message and in the context file, and tell James to run `python Diono_CupHolder_v13_bambu_project.py` in the project root on his PC (after `git pull`) before printing.
- Don't hand-edit the print project 3MF to work around this.

## One design only, in the project root (James, 2026-10-07)
- The repo must never hold more than one design of the cup. When the design changes, delete the files of the old design in the same commit. Don't keep old versions, copies or stale outputs "just in case"; git history has them.
- The current design lives in the **project root**, not in a subfolder. Don't recreate `design_files/`.
- The only exception is `generator_input/v12_base_for_generator.3mf`. It is not a design to print: it is the input the generator and the verify script read. Don't add anything else to that folder.
- Don't leave finished work on a side branch. Merge it to `main` and delete the branch.

## Keep the context file current
Whenever the design changes, update `Diono_CupHolder_Session_Context.md` **in the same session, before finishing the task**, so the next session can pick up exactly where this one left off. Changes that count include:
- geometry or dimensions (cup, disc, bumps, fillets, arm handling)
- a new version (v13, ...)
- print settings or material/color decisions
- new or superseded deliverable files
- fit-test results or other feedback from the user
- resolved or new open items
- changes to the rebuild script

When updating:
- Edit the relevant sections in place (current design table, version history, print settings, files delivered, open items). Don't just append notes at the end.
- Add each new version as a row in the Version History table, with what changed and why.
- Mark superseded files as superseded in the Files section.
- If the rebuild script changes, replace the script in Section 11 with the new, tested version and update its expected cup volume.
- Update the "Current state" line at the top of the file.
- Keep the hard constraints in Section 2. Change them only when the user explicitly changes a constraint.
