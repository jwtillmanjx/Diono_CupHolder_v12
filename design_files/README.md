# Diono Car-Seat Cup Holder (current version: v13)

A 3D-printed replacement cup holder for a Diono child car seat. It clips onto the seat with the original v6 snap rod. v13 adds a **brace** near the bottom of the cup on the arm side. When the cup is pushed toward the seat, the brace's flat pad presses on the seat, so the load no longer bends the **Arm Elbow**, the joint between the snap rod and the sloped support wedge, which kept breaking. v13 also replaces the arm's thin gusset post with a smooth arch, and joins the whole arm to the cup with smooth 8 mm arches. The inside of the cup, the 0.75 mm snap bumps and the snap disc are unchanged from v12.

Full design history and decisions: `../Diono_CupHolder_Session_Context.md`. Simple printing steps: `../PRINT_INSTRUCTIONS.md`.

## Files

The main folder holds only what is needed to print: `Diono_CupHolder_v13_Cup_and_SnapDisc.3mf` and `PRINT_INSTRUCTIONS.md`. Everything below lives in `design_files/`. Older v12 deliverables were deleted on 2026-10-05 at James's request so there's only one file to pick. The v12 cup is kept here as `v12_base_for_generator.3mf` because the generator builds v13 from it.

| File | Purpose |
|---|---|
| `../Diono_CupHolder_v13_Cup_and_SnapDisc.3mf` | **Open this in Bambu Studio.** A ready-to-print project with the cup + disc, all print settings and the snap-rod support blocker (written to the main folder by `Diono_CupHolder_v13_bambu_project.py`) |
| `v12_base_for_generator.3mf` | The delivered v12 cup + disc; the generator's input |
| `Diono_CupHolder_v13_Cup.stl` | Cup only, already in print orientation (rim down), for use without the project |
| `Diono_CupHolder_v13_SnapDisc.stl` | Snap disc (same as v12) |
| `print_orientation.png` | How the cup sits on the plate: bed contact and supported areas |
| `Diono_CupHolder_v13_views.png` | Six views of the finished part |

| `Diono_CupHolder_v13.py` | Parametric generator: builds v13 from the v12 3MF; edit the constants at the top and rerun |
| `Diono_CupHolder_v13_verify.py` → `Diono_CupHolder_v13_verification.png` | 15 automatic checks + v12-vs-v13 cross-sections |
| `Diono_CupHolder_v13_bambu_project.py` → `Diono_CupHolder_v13_slice_check.png` | Builds the Bambu project with Bambu Studio's command-line slicer, adds the support blocker, slices it, and checks the G-code |
| `Diono_CupHolder_v13_images.py` | Makes the views and print-orientation images |
| `Diono_CupHolder_v13_geometry.3mf` | Plain geometry (no settings), used by the verify script |

Rebuild everything: `python Diono_CupHolder_v13.py`, then `python Diono_CupHolder_v13_verify.py`, `python Diono_CupHolder_v13_bambu_project.py` and `python Diono_CupHolder_v13_images.py`. They need `trimesh manifold3d shapely scipy scikit-image numpy matplotlib`, plus Bambu Studio for the project step.

## How this model was made

- **Base:** the delivered and printed v12 cup (kept as `v12_base_for_generator.3mf`). Its arm and snap rod are the original v6 geometry, and its 0.75 mm snap bumps were confirmed by James's fit test. Every v13 change is a boolean addition to v12, except the gusset post (removed and replaced by an arch, at James's request).
- **James's instructions:** brace 4 mm from the bottom, 10 mm thick, 25 mm out from the cup, 55 mm wide; remove the wrap band; smooth arched supports, full width; replace the gusset post with a smooth arch; join the mounting arm to the cup with smooth curved arches; 100% infill everywhere.
- **Not changed:** the inside of the cup (lower and upper bore, snap bumps, disc seat), the snap rod, the cup's outside away from the arm, and the disc. The verify script proves each of these with 0.000 mm³ difference from v12.

### Auto-selected sizes

James gave the brace's position and size; Claude chose these blending sizes. All of them were shown on the concept sheet before building.

| Dimension | Value | Source |
|---|---|---|
| Brace-to-wall side fillets | 8 mm radius | Chosen: blends the 55 mm brace into the curved wall without steps |
| Fillet under the brace | 3 mm radius | Chosen: removes the sharp inside corner once the wrap band was removed |
| Arch on top of the brace (#9) | 14 mm radius, full width | Chosen; James approved the size (a 2× version was requested, then cancelled) |
| Arch replacing the gusset post (#10) | 10 mm radius, 8.8 mm wide | Chosen: tangent to the wall and to the arm-block underside; keeps the post's width |
| Arm-to-cup arches (#11) | 8 mm radius | Chosen: larger than the old 3 mm fillets, while still fitting the thin wedge near the rim |
| Pad-face corner rounding | 1.5 mm | Chosen: removes sharp corners |
| Snap-rod support blocker | Box from 2 mm past the pad face outward, 28 mm wide, full height | Chosen: covers the rod and its ridge, but not the brace |
| Process preset | 0.16mm Standard @BBL P2S | The P2S has no "0.16mm Optimal" preset; Standard is the 0.16 mm equivalent |

## Printing on the Bambu Lab P2S (Bambu Studio)

**Easiest:** **File → Open Project** → `Diono_CupHolder_v13_Cup_and_SnapDisc.3mf`, and load its settings when asked. Everything below is already set. Pick your PETG in the AMS, slice, check the preview, print. Simple steps: `../PRINT_INSTRUCTIONS.md`. For the manual STL route, the support blocker is a 29 × 28 × 90 mm box covering the snap rod from 2 mm past the brace pad face outward.

First click **Global** (the toggle next to "Process", not "Objects") so the settings apply to the whole plate.

```
Printer / plate / filament
- Printer: Bambu Lab P2S 0.4 nozzle. Plate type: Textured PEI Plate.
- Filament: your PETG AMS slot (the project uses Bambu PETG HF; PETG Basic is fine and slightly more heat resistant).

Layer height 0.16 mm
- Process preset dropdown at the top of the Process section: "0.16mm Standard @BBL P2S"
  (the project shows it as "0.16mm Standard @BBL P2S - Diono v13").

Walls = 6
- Strength tab → Wall loops → 6.  Top shell layers → 5, Bottom shell layers → 4.

Infill 100% (everything, including the snap rod)
- Strength tab → Sparse infill density → 100%
- Sparse infill pattern → Rectilinear (Bambu Studio offers this switch automatically when you
  type 100% — click Yes; Grid is not allowed at 100%).

Supports (NEW in v13: needed under the brace)
- Support tab → Enable support: checked. Type = tree(auto).
- "On build plate only": checked (keeps supports off the cup and the snap rod).
- Keep the "Snap-rod support blocker" part that the project adds under the cup in the object list.
  Without it, the slicer grows a small support column onto the ridge of the snap rod.

Brim
- Others tab → Brim type = Outer brim only, Brim width = 5.

Seam
- Quality tab → Seam position = Aligned.
```

**Orientation:** the cup prints **upside down, rim on the plate**, and the disc lies flat; both are already placed. If you import the STL instead: never scale it; press **F** (Lay on face) and click the rim face; add the support blocker yourself (see the print instructions); then set the values above. Don't clone or auto-arrange the project, because the blocker is placed relative to the cup.

**Verified by slicing** the finished project with Bambu Studio 02.08.02.61's own slicer (see `Diono_CupHolder_v13_slice_check.png`):
- no warnings
- about 3 h 25 min, about 132 g
- supports start on the plate and sit only under the brace
- nearest support to the snap rod is 4.4 mm
- bed contact is the rim face (207 mm²) plus the 5 mm brim, the same as v12, which printed well

## Fit and tuning

Constants at the top of `Diono_CupHolder_v13.py`:

| If… | Change |
|---|---|
| The pad doesn't reach the seat, or presses too hard | `REACH` (25 mm): longer to reach, shorter to relieve |
| The brace sits at the wrong height on the seat | `H0` / `H1` (4 / 14 mm). Keep 10 mm thick. Below about 3 mm, the under-fillet runs into the bottom edge |
| You want a wider or narrower pad | `HALF_W` (27.5 = 55 mm wide) |
| You want bigger or smaller blends | `GL` (arch on top of the brace), `R_FLARE`, `R_ARM`, `RP` |
| The disc is loose or too tight | Not in v13; the bumps are inherited from v12 (0.75 mm, fit-tested). See the context file for bump tuning |

After any change, rerun all four scripts. The verify and project scripts must report ALL CHECKS PASSED and "slice OK".
