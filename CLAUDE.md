# Diono Car-Seat Cup Holder — Project Instructions

## At the start of every session
Read `Diono_CupHolder_Session_Context.md` (in this folder) in full before doing anything else:
C:\code\poc\Bambu\Diono_CupHolder_v12\Diono_CupHolder_Session_Context.md

It holds the full design history, hard constraints, current geometry, print settings, open items, and the rebuild script. Treat it as the source of truth for where the project stands.

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
