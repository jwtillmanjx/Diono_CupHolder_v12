# Context Handoff — Diono Car-Seat Cup Holder Redesign (v6 → v12)

> **For the new Claude session:** Read this whole file first. It summarizes a long design session. The user is **James**. He prints on a **Bambu Lab P2S** with an **AMS**, slicing in **Bambu Studio**. **Current state (2026-10-06): v13 REBUILT after the failed first print (Section 9, items 0a–0d). Settings are locked per object, the disc no longer rattles (bumps lowered 0.45 mm), and the brace arch is steep enough to need NO supports. Ready to print; awaiting James's print result.** (Earlier, 2026-10-05: v13 built, verified and delivered.) v13 = v12 + a brace that protects the Arm Elbow + smooth arm-to-cup arches (concept rev 7) + 100% infill everywhere. The folder was cleaned at James's request so there's only one file to pick. **Main folder:** `Diono_CupHolder_v13_Cup_and_SnapDisc.3mf` (a Bambu Studio project with settings and a snap-rod support blocker), `PRINT_INSTRUCTIONS.md` (James asked for SIMPLE and CLEAR; keep it that way), this file, and CLAUDE.md. **Everything else is in `design_files/`**: the generator, verify, Bambu-project and image scripts, STLs, README.md, check images, and `v12_base_for_generator.3mf` (the v12 cup, kept as the generator's input). Old v12 deliverables were deleted. We're waiting for James to print v13 and report back. To rebuild v13, see Section 9, item 0 ("Rebuild"). Section 11 still holds the v6 → v12 script (needs the v6 file, which is not in this folder).

---

## 1. Project summary

James has a 3D-printed replacement cup holder for a **Diono child car seat**. The cup clips onto the seat with an angled **arm/peg** that snaps into the seat. His original design is **v6**, which came as two files:

- `Diono_CupHolder_v6_Solid_UpsideDown.3mf` is the cup. It prints upside down, with the rim on the bed.
- `Diono_CupHolder_v6_FloorDisc.3mf` is a separate floor disc. It drops into the bottom of the cup.

### Original requests (all completed)
1. Redesign the cup and disc so the disc **snaps in and stays in place**.
2. Make the **wider upper section taller** for tall bottles. James required approval before this change; he **approved +0.5" (12.7 mm)**.
3. Increase the **entire cup diameter by 2 mm**, top to bottom. The disc grows to match.
4. Produce a **multi-angle image** of the cup.
5. Deliver **one 3MF containing both parts**, ready for Bambu Studio and the P2S.

### Later requests (all completed)
- Account for **PETG**. James is printing in PETG.
- Make the cup **sturdy**. Smooth the edges and the **arm-to-cup transitions**, but **the arm itself must not change**, because it snaps into the car seat. Changes may only strengthen the design and reduce stress points.
- Design for **high heat in a car**.
- Give a color recommendation, backed by research, among **black (James's preference), blue, green, and transparent**.
- Provide clear **Bambu Studio print settings**, delivered as a file.
- **No visible changes to the cup exterior.** No slots.
- The cup must be **smooth and easy to clean**.
- **No spring arms** on the disc.
- Use **3 small, smooth bumps** inside the cup for the snap.
- James printed v11 and reported a **loose snap** (only one faint click). The fix, now v12: **bigger and wider bumps, plus fit-test rings**.

---

## 2. Hard constraints / James's preferences (keep honoring these)

- **The arm/peg geometry must not change.** It is extracted from v6 and only translated (+1 mm radially, +12.7 mm in print Z). Arm surfaces more than 3.5 mm from the cup wall were verified to deviate by less than 0.002 mm.
- **The cup exterior must stay smooth**: no slots, holes, or visible snap features. The snap must work entirely from the inside.
- **The disc must be a plain solid disc**: no slits, no spring arms.
- **Snap = 3 smooth internal bumps** at 120° spacing, positioned at 60°, 180°, and 300°, so none sits at the arm (0°).
- **Approval gates:** when James says a recommendation needs his approval, present it and wait. For design questions, recommend one option with reasoning, then ask before building.
- **Deliverables each round:** one 3MF with the cup and disc laid out on the plate, a multi-angle PNG, and a print-instructions `.md` file.
- **STANDING RULE (James, 2026-10-06): the `_views` image must ALWAYS label every element of the cup design** (rim, bottle opening, upper/lower sections, shoulder, bottom edge, sloped support wedge, arm-to-cup arches, arm block, arch under the arm block, Arm Elbow, snap rod, rod ridge, rod tip, brace arch, brace side fillets, fillet under the brace, flat pad face, brace underside, snap bumps, snap disc). `design_files/Diono_CupHolder_v13_images.py` does this with surface-snapped label anchors. Update the labels whenever the design changes, and check the rendered image for misplaced labels.
- **Final filament: light blue PETG Matte** (James, 2026-10-06). The project uses the `Bambu PETG Matte @BBL P2S 0.4 nozzle` preset; renders use light blue.
- **Material: PETG.** The cup lives in a hot car on a child's seat, so heat, sturdiness, and stress reduction matter.
- **Formatting James responds well to:** clear recommendations, plain explanations, and step-by-step print settings.

---

## 3. Geometry of the original v6 (as measured)

All units are mm. **Print coordinates**: z = 0 is the cup rim on the bed (the cup prints upside down); the cup axis is at x = 106.42, y = 128.0. **Use coordinates**: h = height above the cup bottom when installed.

| Feature | v6 |
|---|---|
| Overall height | 76.2 |
| Upper (wide) section | OD 82.56 / ID 77.74. Straight wall z 0–26.18, then a ~50° shoulder to z 30.2 |
| Lower (narrow) section | OD 76.0 / ID 71.2 |
| Wall thickness | 2.4 horizontal. The shoulder cone was only about 1.86–1.9 normal, the weakest spot |
| Bottom | Open bottom with a 45° inward conical seat lip, ID 71.2 tapering to 65.4 over about 3 mm |
| v6 disc | 3 mm thick, 45° conical edge (r 32.45 to 35.45). It sat on the lip, held by gravity only |
| Arm/peg | At +x (0°). A sloped support wedge runs along the upper section down to the rim, a narrower block near the shoulder, a thin gusset post along the lower wall, and an angled rod about 10.3 mm wide that snaps into the seat, extending to x = 190.85 |
| Mesh issue | The v6 cup mesh is non-manifold: 48 two-face sliver shells sit at the rod/block joint. Dropping components with 10 or fewer faces and merging vertices (4 decimal places) yields a clean manifold |

---

## 4. Current design: v12 (latest)

| Feature | v12 |
|---|---|
| Overall height | **88.9 mm** (3.5") |
| Upper section | ID **79.9** / OD **84.6**. Grip depth about 39 mm, up from about 26.5 |
| Lower section | ID **73.2** / OD **78.0** |
| Wall | 2.4 mm everywhere. The outer shoulder was moved 1 mm toward the bottom, raising the shoulder wall from 1.9 to 2.4 |
| Rounding | Shoulder fillets: outer convex 3 mm, outer concave 4 mm, inner convex 2 mm, inner concave 3 mm. Rim chamfers: 0.6 mm outer, 1.0 mm inner, both 45° so they print safely on the bed. Bottom outer edge: 1.5 mm round |
| Arm | Unchanged from v6, translated only. **3 mm fillets where it meets the cup**, made with a voxel SDF smooth union; the fillet stands off at most about 0.85 mm |
| Snap bumps | **3 bumps** at 60°, 180°, and 300°. Height **0.75 mm (confirmed final by fit test, 2026-10-05)** (tip at r 35.85 against a 36.6 bore). Width about **13 mm**, with 7.5 mm at full height and cosine-blended ends. **Catch face 30° from horizontal**; lead-in ramp 30° from vertical. Located at h about 4.35–6.4 |
| Disc | **Solid**, 4.6 mm thick. Profile in (r, h): (0,0), (33.4,0), (36.4,3.0), (36.4,4.1), (35.9,4.6), (0,4.6). It has 0.2 mm radial clearance to the bore and the seat, and a smaller top-edge chamfer so the flatter catch can grip |
| Fit check (in the model) | Seated disc: zero interference. It catches after about 0.2 mm of lift. With a 0.2 mm side shift in any direction it still catches |
| Volume / mass | Cup about 65.8 cm³ (~83 g of PETG at 100% infill). Disc about 18.1 cm³ (~23 g) |
| Exterior | Smooth: no slots, no features |
| Fit-test rings | The bottom 18 mm of the cup, printed upside down like the real cup, with bumps of **0.65 / 0.75 / 0.85 mm**. They are marked by **1 / 2 / 3 notches** on the outside at the bed. The file includes one v12 disc. About 65 g total. **A short ring flexes more than the full cup**, so the full cup will feel slightly firmer; if two sizes feel good, pick the smaller |

### Named regions (agreed names James uses to reference parts)
- **Arm Elbow**: the junction where the **angled snap rod (peg)** comes out of the bottom of the **sloped support wedge**. In use coordinates (cup axis at origin, arm along +x, h = height above cup bottom) it spans about **h 40–52, x 55–70**. Here the rod cross-section (about ±5.2 mm wide, h < 40) widens through a short ±6.5 mm step (h ≈ 44–50) into the ±10 mm wedge (h > 51). It is part of the v6 arm, so it falls under the "arm must not change" constraint unless James says otherwise. (It was highlighted in the v12 parts-identified image, which was deleted in the 2026-10-05 cleanup; `design_files/Diono_CupHolder_v13_Brace_Concept.png` labels it too.) Exceptions James approved in v13: the gusset post was replaced by an arch, and the arm-to-cup joints were enlarged into 8 mm arches. The snap rod itself is still unchanged.
- Other labels used in that image: rim, bottle opening, upper (wide) section, shoulder, lower (narrow) section, bottom edge, mounting arm, sloped support wedge, arm block at shoulder, gusset post, angled snap rod (peg), small ridge on rod, rod tip, arm-to-cup fillets, snap bumps, 45° seat lip, bottom opening, floor disc.

### Snap mechanics notes
- Without wall slots, the **cup wall itself ovalizes** to let the disc pass the bumps. For n equal radial loads on a ring, deflection scales as (PR³/EI)·k(n), where k(2) ≈ 0.074 and k(3) ≈ 0.016. Three bumps are therefore about 4.7× stiffer than two, so the bumps are kept small and wide.
- Holding force rises sharply as the catch face flattens. With friction μ ≈ 0.3, the ratio of axial to radial force is about 1.86 at 45° and about 4.2 at 30°. The design is still not self-locking, so the disc remains removable.
- **Install:** tilt the disc, hook one edge under a bump, then press the opposite edge down until it clicks. **Remove:** push up through the bottom opening.
- **Tuning knob:** bump height, in 0.1 mm steps. Width (SPAN/TAPER) is a second option.

---

## 5. Version history (what was tried and why it changed)

| Ver | Snap approach | Outcome / reason for change |
|---|---|---|
| v6 | Disc rests on the 45° lip under gravity | Falls out when the cup is tipped |
| v7 | 3 flex tabs cut through the cup wall (U-slots), with inward nubs. Also added +0.5" height and +2 mm diameter | James disliked the slots visible on the exterior |
| v8 | Same tabs plus keyhole stress reliefs. Added the arm fillets, a thicker rounded shoulder, and rim/edge rounding (PETG and heat focus) | Exterior slots still present |
| v9 | Solid cup; snap moved onto the disc as **3 in-plane spring arms**, with a hidden groove in the cup | James: **no spring arms** |
| v10 | Solid disc; **2** internal bumps (0.6 mm) at 90° and 270° | James wanted **3** bumps |
| v11 | 3 internal bumps, 0.5 mm, about 7.6 mm wide, 45° catch | **Printed: loose snap, only one faint click** |
| **v12** | 3 bumps, **0.75 mm**, about **13 mm** wide, **30° catch**; new disc edge; **plus fit-test rings** | **Current. Fit test passed: 0.75 mm confirmed final by James (2026-10-05)** |
| **v13** | v12 + **brace** (55 × 10 mm, h 4–14, pad face 25 mm from the wall) so pushing the cup inward loads the seat instead of breaking the **Arm Elbow**; gusset post → smooth arch; arm joins the cup with 8 mm arches; 100% infill | **Current. Delivered 2026-10-05** after 7 concept revisions. Verified (15 geometry checks) and sliced by Bambu Studio's command-line slicer (no warnings). **Awaiting James's print feedback** |

---

## 6. Research findings used (heat and color)

- **Bambu PETG HF:** Tg 66 °C. HDT 69 °C at 0.45 MPa. Vicat 70 °C. Recommended chamber temperature 35–50 °C. (Bambu technical data sheet)
- **Bambu PETG Basic:** Tg 68 °C. HDT 69 °C. Vicat 78 °C. Slightly better for heat than HF.
- **Bambu ASA:** HDT about 100 °C and UV-resistant. This is the real upgrade if heat becomes a problem; the P2S is enclosed and can print it.
- **Car interior temperatures** (Arizona State University study, cars parked in the sun for 1 hour): dashboard averaged about 157 °F (69 °C), steering wheel about 127 °F, **seat about 123 °F (51 °C)**, cabin air about 116 °F.
- **Black absorbs about 95% of sunlight.** Lawrence Berkeley National Laboratory work, as reported, found black car roofs up to about 25 °C hotter than white or silver ones.
- **UV:** carbon black is a very effective UV stabilizer, which is black's one advantage. Car side windows block on average about 71% of UVA (range 44–96%); windshields block about 96% (Boxer Wachler, *JAMA Ophthalmology*, 2016).
- **Color recommendation given: transparent** runs coolest because it absorbs the least sunlight. Blue or green are acceptable, with lighter shades better. Black was not recommended because it heats the most and the hot-car temperature range overlaps PETG's HDT. Caveat: clear PETG lacks carbon-black UV protection and may yellow slowly over the years. James had not confirmed his final color choice.
- **Usage advice given:** don't leave a full, heavy bottle in the holder while the car is parked in strong sun, since sustained load plus heat causes PETG to creep. An empty cup puts very little load on the arm.

### Bottle-fit notes
- **Hydro Flask 24 oz** (2.87" ≈ 72.9 mm diameter, 10.8" tall): fits the 73.2 mm lower bore with about 0.3 mm of clearance. Very snug; it may not fit if PETG holes print slightly undersized.
- **Owala FreeSip 24 oz** (3.12" ≈ 79.2 mm base, 10.68" tall): sits in the 79.9 mm upper section with about 0.7 mm of clearance. Tight.
- **Owala 32 oz** (3.43"): does not fit.
- The bumps protrude into the bore only at the floor corner, where most bottles' rounded heels clear them.

---

## 7. Print settings (Bambu Studio, P2S) — current (v13; all built into the project 3MF)

0. **v13 changes vs v12:** supports are now **ON** (tree(auto), build plate only) because the brace overhangs at print z ≈ 61–75. There is a **support-blocker part** around the snap rod (print-coordinate box x 116.4–145.4, y 114–142, z 0–89.9). Without it, the slicer grows a support column onto the rod's small ridge (use coords about (71, ±1, 42.5)); v12 printed that ridge fine unsupported. **100% infill requires the Rectilinear pattern** (internal name `zig-zag`); the P2S default Grid is rejected at 100% (the CLI fails with "Invalid parameter value(s)"; the GUI offers to switch). **There is no "0.16mm Optimal" preset for the P2S**: use `0.16mm Standard @BBL P2S`. Verified slice: 3 h 25 min, 132 g, supports only under the brace, nearest support to the rod 4.4 mm, no warnings.
1. **Printer:** Bambu Lab P2S, 0.4 mm nozzle. **Plate:** Textured PEI. Clean it with IPA.
2. **Filament:** PETG, selected from the AMS slot. Dry it if the spool has been open; Bambu lists 65 °C for PETG HF.
3. **Process:** **0.16mm Standard @BBL P2S** (v12 docs said "0.16 mm Optimal", which does not exist for the P2S).
4. **Strength:** Wall loops **6**. Top shell layers **5**. Bottom shell layers **4**. Sparse infill **100%**, **Rectilinear**.
5. **Support (v13):** **On**, tree(auto), **on build plate only**, plus the snap-rod support blocker. (v12 used no supports.)
6. **Others:** Brim **Outer brim only, 5 mm**.
7. **Quality:** Seam **Aligned**.
8. Leave speed, cooling, and temperatures at the filament defaults. Keep the **door closed**.
9. If Bambu Studio says the file is not a Bambu project and only geometry will load, click OK. **Don't rotate the parts**: the cup prints rim-down and the disc prints flat.
10. **Preview checks:** no supports; smooth exterior; 3 bumps (about 13 mm wide) on the inside near the top of the cup as printed.
11. Let the plate cool before removing parts. Peel the brim and deburr the rim.
12. Optional **Step 0:** print the fit-test rings first with the same settings, then pick a bump size.

---

## 8. Files delivered in this session (in James's outputs folder)

**Folder layout since 2026-10-05.** James asked to "delete old versions so I'm not confused on which one to pick".

| File | What |
|---|---|
| `Diono_CupHolder_v13_Cup_and_SnapDisc.3mf` (main folder) | **CURRENT, the only file to print.** A Bambu Studio 02.08.02.61 project: cup + disc on the plate, process/filament/printer settings embedded, snap-rod support blocker part |
| `PRINT_INSTRUCTIONS.md` (main folder) | **CURRENT.** Short, simple steps (James asked for SIMPLE and CLEAR). Keep any future edits short |
| `design_files/Diono_CupHolder_v13.py` | Generator: builds v13 from `v12_base_for_generator.3mf`, with asserts; writes the cup/disc STLs and `Diono_CupHolder_v13_geometry.3mf` |
| `design_files/Diono_CupHolder_v13_verify.py` | 15 checks (bores and bumps unchanged, rod unchanged, pad 55 × 10, gap to rod, area scan, bed contact …) → `..._verification.png` |
| `design_files/Diono_CupHolder_v13_bambu_project.py` | Flattens the P2S/0.16/PETG HF system presets and applies our settings; uses the Bambu Studio CLI to export the project; adds the support blocker; slices it and checks the G-code (no warnings, supports on the plate, ≥ 1 mm from the rod) → main-folder 3MF + `..._slice_check.png` |
| `design_files/Diono_CupHolder_v13_images.py` | `..._views.png` (6 views) and `print_orientation.png` |
| `design_files/README.md` | Skill-format README: files, sources, auto-selected sizes, Bambu Studio click-paths, tuning constants |
| `design_files/Diono_CupHolder_v13_Cup.stl`, `..._SnapDisc.stl`, `..._geometry.3mf` | Plain geometry (STL route needs the blocker added by hand: a 29 × 28 × 90 mm box from 2 mm past the pad face outward) |
| `design_files/Diono_CupHolder_v13_Brace_Concept.png` | Rev 7 labeled concept sheet (part numbers 1–11) |
| `design_files/v12_base_for_generator.3mf` | The delivered v12 cup + disc (renamed); the generator's input. **Do not delete** |
| **Deleted 2026-10-05** | v12 fit-test rings 3MF, v12 views PNG, v12 print instructions, v12 parts-identified PNG, the earlier long v13 instructions. (v7–v11 files were never in this folder) |

**Plate layout used in the 3MFs** (P2S bed is 256 × 256):
- Main file: cup translated x −56, so its footprint is about x 8–136 and y 86–170. Disc centered at (200, 60).
- Test file: rings centered at (55, 55), (150, 55), and (55, 160). Disc at (160, 165).

---

## 9. Open items / next steps

0a. **2026-10-06 FIRST v13 PRINT FAILED (spaghetti under the brace; the cup was also loose on the bed; no brim).** Photos: `C:\Users\James\Downloads\20261006_001110.jpg`, `..._001130.jpg`. **Root cause, proven from the actual G-code** (Bambu's session backup `%LOCALAPPDATA%\Temp\bamboo_model\Mon_Oct_05\21_04_01#29328#91\Metadata\.29328.0.gcode`): the job was sliced with the **stock "0.16mm Standard @BBL P2S"** (2 walls, 15% grid, **supports off**, auto brim, 85 g) instead of the project's "…- Diono v13" preset. The project had loaded correctly (its snapshot `_temp_3.config` shows Diono v13: 6 walls, 100%, supports on), but within about a minute the Process had become the stock preset. It is unknown whether James switched it by hand or Bambu switched it (filament also changed to PETG Matte via the AMS). **Fixes done:** (1) the project builder now writes **per-object settings** on the cup (walls 6, top 5, bottom 4, 100% zig-zag, tree supports, build plate only, outer brim 5 mm) and on the disc (same minus supports). Per-object settings survive a Process preset switch. (2) **Regression test** in the builder: it re-slices with the stock preset forced and asserts the same weight (±3%) and the same supports. Before the fix: 80 g, no supports (FAIL); after: 132 g, supports (PASS). (3) PRINT_INSTRUCTIONS: wash the plate with dish soap; check the preview for supports, brim and ~132 g before printing.
0b. **2026-10-06 disc rattle fix (James: "snaps in place … but it does still rattle").** Measured: about **0.35 mm vertical play** at each bump (the disc sinks 0.20 mm onto the 45° seat because of the 0.2 mm clearance, then can lift 0.15 mm to the catch face), plus about 0.2 mm radial play. **Fix: the 3 bumps are lowered by `BUMP_DROP = 0.45` mm** (same 0.75 mm shape and volume; they now start at h 3.90 instead of 4.35), leaving about **0.10 mm preload** (measured 0.096–0.102 at 60/180/300°). The catch faces now press the disc onto the seat and centre it. The disc itself is unchanged. Tuning: still rattles → larger; too hard to press in → smaller (0.35 = zero play). The verify script has 3 disc-fit checks (preload must be 0.05–0.20 mm) and now compares against "v12 with lowered bumps". **The main-folder 3MF was rebuilt with both fixes (2026-10-06); images not yet regenerated** (the bump change isn't visible in them).
0g. **2026-10-06 (latest) — James printed rev 0f: "the disc does still rattle a little but it is much better … make just a slight adjustment".** `BUMP_DROP` 0.45 → **0.50** mm (the tuning step); measured preload is now **0.146–0.152 mm** (was ~0.10). Within the verify range 0.05–0.20. If it still rattles, try 0.55; if it gets too hard to press in, go back to 0.45. Verified build with the PETG Matte preset: Bambu slice 3 h 51 min, 152 g (Matte prints slower and heavier than the HF estimate), no supports, preset-switch test OK. (One verify slice hung once while images rendered at the same time; run the scripts one after another.) Also: the project filament preset is now PETG Matte (James's light blue), and the `_views` image is now fully labeled (see the standing rule in Section 2).
0f. **2026-10-06 — James: "make the arch curve more and reduce the pad thickness to 7mm".** The brace is now **h 4–11** (H1 = 11; the pad face is 55 × 7 mm, bottom still 4 mm from the cup bottom). Arch: **ARCH_PHI1 = 28°** (was 35°), ARCH_Q = 1.0 (the corners keep 28°), arc to vertical at the wall. R ≈ 47 mm (was 59), height ≈ 42 mm (wall top about h 53 at the centre); clearly rounder. **28° is about the practical limit:** Bambu adds supports below 25°, so a rounder arch would bring supports back under the arch's lower edge. Tell James that if he asks for even more curve. Verify: overhang check is now "flatter than 25.5°" (0.00 mm²); pad check 55 × 7; rod-to-pad gap 15.3 mm at h 11. Supports-on diagnostic: the only support is the rod-ridge tree, none under the arch. Build: **3 h 23 min, 142 g**, no supports, preset-switch test OK, all checks pass.
0e. *(Superseded by 0f.)* **2026-10-06 — TRUE ARCH (James was angry about 0d: "Create more of a arch, you did a straight line which was EXACTLY WHAT I SAID NOT TO DO").** Lesson: a ≥45° minimum slope with only about 31 mm of height can't bend visibly (2.9 mm sag ≈ straight). **Don't trade the arch shape away for printability margin without asking.** The arch #9 profile is now a **circular arc from ARCH_PHI1 = 35° at the pad edge to 90° (tangent to the wall)**, height ARCH_HC = 25·Δcos/Δsin ≈ 48 mm at the centre, Hm scaled by (span/25)^0.5 (ARCH_Q). That gives **6.6 mm of visible curve** (12% of the chord, vs 7% before). In the middle the arch merges into the arm underside (leaving an open tunnel under the arm block, not a sealed void: one shell); at the sides it meets the wall at about h 46–48. Minimum slope is about 32° (more than Bambu's 25° threshold). The verify check is now "no brace/arch overhang flatter than 30°" (0.00 mm²). **Diagnostic slice with supports ON:** Bambu puts support ONLY under the v6 rod ridge (use h 42.6), nothing under the arch. The delivered project keeps supports OFF. Result: 3 h 32 min, 151 g, preset-switch test OK, all checks pass. The 0d constants `ARCH_A/ARCH_N/ARCH_HC` were replaced by `ARCH_PHI1/ARCH_PHI2/ARCH_Q`.
0d. *(Superseded by 0e: James rejected it as straight.)* **2026-10-06 — STEEP SELF-SUPPORTING ARCH, NO SUPPORTS.** James: "I do not want a straight 45 degree slope. Maintain an arch. Increase the slope of the arch as much as you can without making it appear straight and to not require support", then "create the design file and delete old versions, I have to print ASAP". Arch #9 is now a heightfield from the pad's top edge (x 64, h 14) to the wall: `h = 14 + Hm(y)·(0.8t + 0.2t⁴)`, with t = 0 at the pad and 1 at the wall (t = b/(a+b): b = distance to the pad plane, a = distance to the wall). Hm = 33·(pad-to-wall span / 25), so the outer corners keep the slope. Constants `ARCH_A/ARCH_N/ARCH_HC` = 0.8/4/33. The arch meets the wall at about h 45.5 in the middle and up to about 53.7 at the corners, where it merges into the shoulder. It is cut out of the bore (r < 40 above h 45.5). A 5 mm rolling-ball blend (`ARCH_BLEND`) joins it to the wall. Result: the minimum slope is **45.6°**, with about 3 mm of visible curve, steepening to about 65° at the wall. The verify script checks **0.00 mm² of brace overhang flatter than 45°**. **Supports are now OFF** (globally and per object); the support blocker was removed. Bambu's slice: 3 h 33 min, **153 g**, no supports. The preset-switch test passes (same 153 g). Bambu warns **"floating regions"**: this is the v6 snap-rod ridge (a 0.31 mm² island at use (71.1, 0, 42.6)), and **v12 has the identical island and printed fine**. The verify script asserts it is the only island, and the builder allows only that warning. The cup is now ~107.5 cm³ (~136 g). The 18 + 2 checks pass. The rev 7 concept PNG was deleted (outdated); the views/orientation/slice-check images were regenerated. PRINT_INSTRUCTIONS was updated (no supports, 153 g, ignore "floating regions").
0c. *(Superseded by 0d.)* **Question from James: "would it help to increase the arch support to reach until the end of the pad so that it would not need Tree support?"** My answer: yes, but not as a longer concave arch (its end would flatten out to horizontal and still need support). Recommended a **45° straight slope** from the pad's top edge (x 64, h 14) up to the wall (h ≈ 39), full brace width, with a smooth concave blend into the wall. Every surface would then be ≥45° in print orientation, so **no supports and no blocker are needed** (like v12). It would survive even a full settings reset, but adds about 15–20 g. **Waiting for James's approval before building.**
0. **v13: DELIVERED 2026-10-05. Next: James prints it and reports back** (Does the pad reach the seat? Does it still clip in? Any print problems?). Tuning knobs in `design_files/Diono_CupHolder_v13.py`: `REACH` (25), `H0`/`H1` (4/14), `HALF_W` (27.5), `GL`/`R_FLARE`/`R_ARM`/`RP`. **Rebuild:** `cd design_files` then run `python Diono_CupHolder_v13.py`, `python Diono_CupHolder_v13_verify.py` (must print ALL CHECKS PASSED), `python Diono_CupHolder_v13_bambu_project.py` (needs Bambu Studio; must print "slice OK"; writes the main-folder 3MF), and `python Diono_CupHolder_v13_images.py`. Build notes: mesh `simplify()` is deliberately NOT used (even 0.01 mm drift pushed about 1.9 mm³ into the bore); the arm-arch exclusion zone under the arm block is |y| < 5 (narrowed from 9.5, which left a ragged lip). Bambu CLI quirks: presets must be saved with `"from": "User"` + `inherits` (otherwise the 3MF export fails, code −13), `curr_bed_type` must be set (code −61), and 100% infill needs `zig-zag` (code −18).
   - **Design history of v13 (brace extension):** James's request: the cup breaks at the **Arm Elbow**. Add an extension on the arm side that pushes against the seat. His spec: **20 mm from the bottom, 10 mm thick, wraps around the cup exterior, well connected with smooth supporting ramps, longest length 60 mm out to the seat (the seat is 60 mm away)**. He wants **images first; STL/3MF only when he asks**.
   - **Key finding:** at h 20–30 the angled snap rod sits 26–44 mm out from the lower wall (x 65–83 in use coords, |y| ≤ 5.2). A straight extension toward the seat would run through the rod. James questioned this; it was explained with a clash overlay.
   - "Longest side 60 mm" is NOT measured from the cup center. I measured it from the outer wall (r 39) to the seat (x = 99). James's exact meaning of "longest side" is still unconfirmed.
   - **INFILL DECISION (2026-10-05; James: "Make the snap rod have 100% infill so that it is as strong as possible. The new pad extension could have 40% infill"):** this is a print setting, not a geometry change. **Snap rod and everything else: 100% sparse infill** (already the v12 default). **Brace region: 40% infill**, via a Bambu Studio **modifier box**. In use coordinates (cup axis at origin, arm +x, h up) the box is **x 39.5–64.5, |y| ≤ 36, h 0–29**; it covers the 55 mm brace (pad face at x = 64), its 8 mm plan fillets, the 3 mm under-fillet, and the full-width 14 mm arch #9 (top at h ≈ 28). It clears the snap rod: the closest the rod comes in that height range is x ≈ 65.6 at h 29 (66.3 at h 28, ≥ 72 at h ≤ 20), so there is ≥ 1.1 mm of clearance. **Do not extend the box past x ≈ 65.** Convert to print coordinates (z = 88.9 − h, so the box spans z 59.9–88.9 above the bed) and to plate placement when writing the 3MF. **When building the v13 deliverables:** try to embed the modifier in the 3MF as a Bambu-format part (subtype modifier_part, sparse_infill_density = 40%, in Metadata/model_settings.config). Always also give manual steps in the print-instructions .md as a fallback (right-click cup → Add Modifier → Box, set size and position, set Sparse infill density to 40%), and say in the preview checks to confirm the rod shows 100%. With 6 wall loops, about 2.5 mm of every brace surface is solid wall anyway; 40% only affects the core.
   - **REV 7 (geometry current; James: "The Mounting arm should connect to the cup using smooth curved arches. Increase brace width from 40 mm wide to 55 mm wide"):**
     - **Brace width 55 mm** (|y| ≤ 27.5). Everything else on the brace is as in rev 6 (h 4–14, 25 mm reach, pad face x = 64, 8 mm plan fillets into the wall, 3 mm fillet under it, 14 mm full-width arch #9).
     - **NEW #11, arm-to-cup arches:** a deliberate **exception to "arm must not change", requested by James.** Wherever the mounting arm meets the cup wall (both sides of the sloped wedge, the arm block, up to the rim), the v12 3 mm fillets are enlarged into **8 mm concave arches**. Method: a rolling-ball morphological closing with an 8 mm ball on a 0.25 mm voxel grid over (arm ∪ cup body). Only material the ball adds in free space is kept (with 0.5 mm overlap into the solid, Gaussian-smoothed, specks < 20 mm³ dropped), and only where it is within 8.5 mm of both arm and wall. It is excluded under the arm block (x < 56, |y| < 9.5, h < 44) because arch #10 already fills that space. It is clipped below the rim (h ≤ 88.3) and kept out of the bore. The arm needs to be separated from the cup with the v12 body profile **grown by 0.12 mm**; otherwise a thin skin of cup surface stays attached to the arm. Because the v12 3 mm fillets already filled most of each corner, the 8 mm arches add only a thin crescent (about 1–2 mm thick at most).
     - **Things that did NOT work (don't repeat):** (1) the circular smooth-min SDF blend at r = 8 inflated thin parts of the arm (the wedge near the rim by about 1.4 mm). (2) Gating that blend by the angle between gradients produced jagged, notched fillets. (3) Eroding the free-space region thinned the arches by half.
     - Checks: one connected solid, nothing in the bottle space, **zero change more than 12 mm from the wall (snap rod untouched)**. v13 volume is about 84.8 cm³ vs v12's 65.8, i.e. about **+19 cm³ (~24 g)**.
     - Known cosmetic issue to tidy when building the STL: a small ragged lip where the #11 arches meet the top of the #10 arch (h ≈ 44, beside the arm block).
     - Rendering note: the image colors one merged solid by triangle origin (manifold3d `as_original` / `run_original_id`): gray = v12 surface, orange = new or changed. scikit-image was installed on James's machine for this.
   - *Rev 6 (superseded by rev 7 except where noted):* **James: "remove the outer band that wraps all the way around the cup, extend the width of the flat pad face to 40 mm, reduce the brace from 30 mm to 25 mm, and move the entire brace to 4 mm from the bottom"):**
     - **Wrap band (#1) and its ramps/chamfer (#2, #3) are REMOVED.** The cup exterior away from the brace is back to v12, including the 1.5 mm bottom-edge round.
     - **Brace (#4):** h **4–14** (10 mm thick), reaches **25 mm** from the wall (pad face at x = 64), **40 mm wide** (|y| ≤ 20). The pad face (#8) is 40 × 10 mm with 1.5 mm rounded corners.
     - **Wall blend (#5):** with no band, the brace sides blend straight into the curved cup wall through **8 mm plan-view concave fillets**, which touch the wall at about |y| 22.6. The brace is embedded 1.2 mm into the wall (to r 37.8).
     - **NEW #2: a small 3 mm concave fillet under the brace** where it meets the wall (radial cove, h 1–4, limited to the brace outline). I added it so there is no sharp inside corner once the band is gone; it is labeled so James can remove it.
     - **Arch (#9)** is unchanged in design (14 mm radius, full width, now across the 40 mm brace plus fillets), running from the brace top at h 14 up to the wall at h 28. **Post arch (#10)** is unchanged from rev 5.
     - Snap rod clearance: at h 14 the rod starts at x 76.3, so there is about a 12 mm gap to the pad.
     - Checks: one connected solid, nothing in the bottle space. Net added material is about 12.5 cm³ (~16 g). The brace still needs supports when printed rim-down.
   - *Rev 5 (superseded by rev 6; #10 post arch still current):* **Two James requests:**
     - **(a) "Replace the Gusset Post (along lower wall) with the same type of smooth arch design."** This is a **deliberate exception to the "arm must not change" constraint, made at James's explicit request; it applies to the gusset post only.** The v6 post was a triangular wedge under the arm block (x 39–48, h 29–45.7, |y| ≤ 4.4, straight sloped face up to the block underside at (48, 45.7)). It is cut away outside the wall (r > 39.03, |y| ≤ 7.5, h 27 to min(45.2, block underside − 0.3); 486 mm³ removed). In its place is a **concave 10 mm-radius arch, 8.8 mm wide**, tangent to the wall at h 34.3 and tangent to the arm-block underside line (48, 45.7)→(58, 41.3) at (53.0, 43.5). A small filler block (x 37–47.5, h 44.5–50, |y| ≤ 4.4) closes a crevice between the wall and the arm block and stays inside the block's outline. Material above h 46 changed by +28.7 mm³ added, 0 removed (junction fill only). The snap rod and the rest of the arm are unchanged. A tiny pre-existing v12 sliver at about x 44, h 50–52, y ≈ 3.5 remains.
     - **(b) "Move the brace down to 2 mm from the bottom and extend the flat pad face to 30 mm."** Interpreted as **brace/band at h 2–12** (still 10 mm thick) and **pad face 30 mm from the cup wall (x = 69)**; the pad face stays 31 × 10 mm. **The "30 mm = distance from the wall" reading is unconfirmed.** Because the band bottom is at h 2, its lower ramp is now a **45° chamfer from (r 41.5, h 2) down to (r 39.5, h 0)**, which covers the old 1.5 mm bottom-edge round. The brace arch (#9, 14 mm radius) now runs from the brace top at h 12 to the wall at h 26. Snap rod clearance: at h 12 the rod starts at x 78.3, so there is about a 9 mm gap to the pad; there is no rod below h 10.
     - Checks: one connected solid, nothing in the bottle space. Net added material is about 20 cm³ (~25 g).
   - *Rev 4 (superseded by rev 5):* **James: "extend the arch support to be continuous of the width of the part that extends from brace"):** the two narrow arches are replaced by **one continuous arched support (#9) across the full width of the brace footprint, flares included**. It is a radial concave cove: 14 mm radius measured from the curved cup wall (revolved profile intersected with the brace plan shape), flat along the brace top at h 18 and vertical where it meets the wall at h ≈ 32. **James also asked to double the arch size, then cancelled that ("ignore doubling the size"). Keep the 14 mm radius.** (For reference, a 28 mm radius would overrun the 20 mm brace and merge about 67 mm³ into the arm's gusset post.) Checks: one connected solid, zero overlap with the arm, zero intrusion into the bottle space. Added material is about 17.0 cm³ (~22 g).
   - *Rev 3 (superseded by rev 4):* **James: "replace the upper gusset support design with smooth arch":** the two triangular 45° gussets (#9) are replaced by **two smooth arched supports**. Each is a concave quarter-circle (14 mm radius), 5 mm thick, at |y| ≈ 11.7. The curve runs flat along the brace top (h 18) and meets the cup wall vertically at about h 32, and the arch tips are softened by 0.4 mm. **Fix included:** the supports are now measured from the curved wall surface (x = √(39² − y²)) and embedded to r 36.9. The rev-1/2 gussets were measured from a flat x = 39 plane and floated about 1.4 mm off the wall. Checks: cup + brace is one connected solid, zero overlap with the arm, zero intrusion into the bore. Added material is about 15.7 cm³ (~20 g). Everything else is as in rev 2.
   - *Rev 2 (gussets superseded by rev 3):* **James's correction:** brace moved to 8 mm from the bottom (h 8–18, still 10 mm thick) and extends only 20 mm from the cup wall (pad face at x = 59).** Because the snap rod at h ≤ 18 is at x ≥ 72.7, the brace ends about 14 mm short of the rod, so **the fork (#6) and notch (#7) were removed**. The brace is now one solid piece: 31.4 mm wide (|y| ≤ 15.7) with curved flares into the band (#5), a flat 31 × 10 mm pad face toward the seat (#8), and two 45° upper gussets (#9), 5 mm thick at |y| ≈ 11.7, 14 mm legs, up to about h 33. The 360° wrap band (#1) is now at h 8–18, r 41.5, with ramps (#2, #3) from h ≈ 5 to h ≈ 21. Checks: zero overlap with the arm, zero intrusion into the bore. It adds about 16.6 cm³ (~21 g). Still needs supports when printed rim-down. It is assumed the seat is about 20 mm from the cup at that height (unconfirmed). Image updated; awaiting James's review.
   - *Rev 1 (superseded):* **Concept drawn (numbered assumptions for James to correct):** (1) a full 360° wrap band at h 20–30, 2.5 mm proud (r 41.5); (2, 3) 45° ramps blending it into the wall; (4) a solid root web; (5) curved plan-view flares; (6) two fork prongs, 8 mm wide × 10 mm thick, at |y| 7.7–15.7, straddling the rod; (7) a notch with 2.5 mm rod clearance (notch bottom at x 62.5); (8) flat seat pads at x = 99; (9) 45° upper gussets, 5 mm thick, h 30–45, at |y| ≈ 11.7. It adds about 24 cm³ (~30 g). The band's upper ramp just touches the bottom tip of the arm's gusset post (3 mm³ overlap). Nothing enters the bore. The prongs need print supports when printed rim-down.
   - The concept was built with manifold3d + shapely in scratch scripts (not kept). Rebuild from the parameters above.

1. **RESOLVED (2026-10-05): fit test done. 0.75 mm bumps are correct.** James confirmed that the bump size in `Diono_CupHolder_v12_Cup_and_SnapDisc.3mf` is right and should be used going forward. That file was measured: all 3 bumps are 0.75 mm (tip r ≈ 35.85 vs 36.6 bore). **Use `BUMP = 0.75` in all future versions, including v13.** No more fit-test rings are needed unless the snap design changes.
2. **RESOLVED 2026-10-06: final filament color is light blue PETG Matte.** (A light color is good for heat; transparent had been recommended and black was the original plan.)
3. Possible extra: a PDF version of the instructions (offered, not yet requested).

---

## 10. Build pipeline overview (how the geometry is made)

- **Libraries:** Python with `trimesh`, `manifold3d` (booleans, revolve, warp), `shapely`, `scikit-image` (polygon rasterizing, marching cubes), `scipy` (EDT), and `numpy`. For renders, a custom numpy z-buffer rasterizer drives matplotlib panels. That code is not included; any renderer works.
- **Steps:**
  1. Repair the v6 mesh.
  2. Extract the arm: subtract the v6 outer envelope offset by 0.03 mm from the repaired cup, then extend the arm root 1.6 mm inward so it embeds in the new wall.
  3. Translate the arm by (+1, 0, +12.7).
  4. Add a convex-hull wedge that continues the arm's sloped support face down toward the new rim.
  5. Revolve the filleted wall profile.
  6. Add the 3 bumps: a revolved profile cut to a wedge, then warped radially with a cosine taper.
  7. Union the body with the arm and a 3 mm voxel-SDF fillet. The circular smooth-min uses a 0.25 mm grid, is masked to the genuine junction, and its pieces are filtered by size.
  8. Simplify the mesh with tolerance 0.01 and write a plain core-spec 3MF.
- **Verification habits used:**
  - Disc-versus-cup interference at lift 0 / 0.2 / 0.3 mm and with ±0.2 mm side shifts, with the cup mirrored to use orientation.
  - Wall thickness checked via shapely negative buffer.
  - Arm-unchanged check using surface samples more than 3.5 mm from the wall.
  - Exterior compared against the previous version by slice radii.

---

## 11. Rebuild script (tested — reproduces v12 exactly; cup volume 65,804.8 mm³)

Save it as `rebuild_v12.py`. Run it with the original v6 cup file:

```bash
pip install trimesh manifold3d shapely scikit-image scipy numpy
python rebuild_v12.py Diono_CupHolder_v6_Solid_UpsideDown.3mf out
```

Keep `BUMP = 0.75`: the fit test confirmed it. The test rings (0.65 / 0.75 / 0.85) are no longer needed.

```python
#!/usr/bin/env python3
"""Rebuild Diono Cup Holder v12 from the original v6 3MF.
Usage: python rebuild_v12.py <path/to/Diono_CupHolder_v6_Solid_UpsideDown.3mf> [outdir]
Needs: pip install trimesh manifold3d shapely scikit-image scipy numpy
"""
import sys, os, re, zipfile, numpy as np, trimesh, manifold3d as mf
from skimage.draw import polygon as dpoly
from skimage.measure import marching_cubes
from scipy.ndimage import distance_transform_edt as edt, label, binary_dilation

SRC = sys.argv[1] if len(sys.argv) > 1 else "Diono_CupHolder_v6_Solid_UpsideDown.3mf"
OUT = sys.argv[2] if len(sys.argv) > 2 else "out"
os.makedirs(OUT, exist_ok=True)

# ---------------- helpers ----------------
C = np.array([106.42, 128.0])          # cup axis (x,y) in the v6 file
def to_mf(t): return mf.Manifold(mf.Mesh(vert_properties=np.asarray(t.vertices, np.float32), tri_verts=np.asarray(t.faces, np.uint32)))
def to_tm(M):
    m = M.to_mesh(); return trimesh.Trimesh(np.array(m.vert_properties)[:, :3], np.array(m.tri_verts), process=False)
def ccw(P):
    P = np.asarray(P, float); sa = 0.5*np.sum(P[:, 0]*np.roll(P[:, 1], -1)-np.roll(P[:, 0], -1)*P[:, 1])
    return P if sa > 0 else P[::-1]
def rev(P, seg=360, ctr=True):
    M = mf.Manifold.revolve(mf.CrossSection([ccw(P)]), seg)   # profile (r,z) revolved about z
    return M.translate([C[0], C[1], 0]) if ctr else M
def fillet_poly(pts, radii, n=16):
    P = np.array(pts, float); N = len(P); out = []
    for i in range(N):
        p0, p1, p2 = P[i-1], P[i], P[(i+1) % N]; r = radii[i]
        if r <= 0: out.append(p1); continue
        u = (p0-p1)/np.linalg.norm(p0-p1); v = (p2-p1)/np.linalg.norm(p2-p1)
        ang = np.arccos(np.clip(u@v, -1, 1)); t = r/np.tan(ang/2)
        t = min(t, 0.49*np.linalg.norm(p0-p1), 0.49*np.linalg.norm(p2-p1)); rr = t*np.tan(ang/2)
        a = p1+u*t; b = p1+v*t; bis = (u+v)/np.linalg.norm(u+v); c = p1+bis*(rr/np.sin(ang/2))
        a0 = np.arctan2(*(a-c)[::-1]); a1 = np.arctan2(*(b-c)[::-1]); d = (a1-a0+np.pi) % (2*np.pi)-np.pi
        for k in range(n+1):
            th = a0+d*k/n; out.append(c+rr*np.array([np.cos(th), np.sin(th)]))
    return np.array(out)

# ---------------- 1. load + repair v6 (it has 48 two-face sliver shells at the arm joint) ----------------
x = zipfile.ZipFile(SRC).read('3D/3dmodel.model').decode()
v = np.array(re.findall(r'<vertex x="([^"]+)" y="([^"]+)" z="([^"]+)"', x), float)
t = np.array(re.findall(r'<triangle v1="(\d+)" v2="(\d+)" v3="(\d+)"', x), int)
m = trimesh.Trimesh(v, t, process=True)
parts = [p for p in m.split(only_watertight=False) if len(p.faces) > 10]
O = trimesh.util.concatenate(parts); O.merge_vertices(digits_vertex=4)
O = to_mf(O); assert O.status() == mf.Error.NoError

# ---------------- 2. extract the arm (unchanged), move it with the resized/taller cup ----------------
EXT, DR = 12.7, 1.0              # +0.5" upper section, +1 mm radius (+2 mm diameter)
H = 76.2+EXT                     # 88.9 mm overall
def env(off, zlo=-1, zhi=77):    # v6 outer envelope (print coords: z=0 is the rim on the bed)
    return rev([(0, zlo), (41.28+off, zlo), (41.28+off, 26.18), (38+off, 30.2), (38+off, zhi), (0, zhi)])
peg = O - env(0.03)
root = peg ^ (env(0.6)-env(0.0))
for d in (0.4, 0.8, 1.2, 1.6): peg = peg + root.translate([-d, 0, 0])   # embed root into new wall
peg = peg.translate([DR, 0, EXT])
yA, yB = 118.0, 138.0; xo = 154.1+0.63*0.5      # extend the sloped support wedge down toward new rim
pts = np.array([[146.9, yA, 13.2], [146.9, yB, 13.2], [xo, yA, 13.2], [xo, yB, 13.2],
                [146.9, yA, 2.2], [146.9, yB, 2.2], [147.4, yA, 2.2], [147.4, yB, 2.2]])
peg = peg + to_mf(trimesh.convex.convex_hull(pts))

# ---------------- 3. cup wall profile (print coords), fillets, 3 snap bumps ----------------
def z(h): return H-h             # h = height above cup bottom in USE orientation
Rw_o, Rn_o = 41.28+DR, 38.0+DR; Rw_i, Rn_i = 38.88+DR, 35.6+DR
zs0, zs1 = 26.18+EXT, 30.2+EXT; SH = 1.0         # outer shoulder moved 1 mm -> shoulder wall 2.4 mm
wall = [(Rw_i+1.0, 0.0), (Rw_o-0.6, 0.0), (Rw_o, 0.6), (Rw_o, zs0+SH), (Rn_o, zs1+SH), (Rn_o, H),
        (Rn_i-3.0, H), (Rn_i, z(3.0)), (Rn_i, zs1), (Rw_i, zs0), (Rw_i, 1.0)]
rad = [0, 0, 0, 3.0, 4.0, 1.5, 0.4, 0, 2.0, 3.0, 0]
W = fillet_poly(wall, rad)

BORE, RB, H0, CATCH, LEAD, FLAT = 36.6, 37.0, 4.35, 30.0, 30.0, 0.2
SPAN, TAPER, ANG = 20.6, 4.35, (60, 180, 300)     # arm is at 0 deg (+x)
BUMP = 0.75                                       # bump height (tunable; test rings 0.65/0.75/0.85)
def bump_profile(p):
    tip = BORE-p; h1 = H0+p*np.tan(np.radians(CATCH)); h2 = h1+FLAT; h3 = h2+p/np.tan(np.radians(LEAD))
    return [(RB, H0), (BORE, H0), (tip, h1), (tip, h2), (BORE, h3), (RB, h3)]
def wedge(a0, a1, r=45, zl=-1, zh=H+2):
    a = np.radians(np.linspace(a0, a1, 64)); P = [(0, 0)]+[(r*np.cos(q), r*np.sin(q)) for q in a]
    return mf.Manifold.extrude(mf.CrossSection([ccw(P)]), zh-zl).translate([0, 0, zl])
def bumps(p):
    ring = mf.Manifold.revolve(mf.CrossSection([ccw([(r, z(h)) for r, h in bump_profile(p)])]), 1440)
    out = None
    for c in ANG:
        seg = ring ^ wedge(c-SPAN/2, c+SPAN/2)
        def wf(vv, c=c):
            xx, yy, zz = vv; r = np.hypot(xx, yy); th = np.degrees(np.arctan2(yy, xx)); d = abs(((th-c)+180) % 360-180)
            e = SPAN/2-d; f = 1.0 if e >= TAPER else max(0.0, 0.5-0.5*np.cos(np.pi*e/TAPER))
            s = (RB-(RB-r)*f)/r if r > 0 else 1
            return (xx*s, yy*s, zz)
        seg = seg.warp(wf); out = seg if out is None else out+seg
    return out.translate([C[0], C[1], 0])
def body(p): return rev(W)+bumps(p)

DISC_RH = [(0, 0), (33.4, 0), (36.4, 3.0), (36.4, 4.1), (35.9, 4.6), (0, 4.6)]   # solid disc, printed flat
disc = rev(DISC_RH, ctr=False)

# ---------------- 4. 3 mm fillet where arm meets cup (voxel SDF smooth-union, arm surfaces >3.5 mm away untouched) ----------------
def voxelize(M, x0, y0, z0, nx, ny, nz, p):
    V = np.zeros((nx, ny, nz), bool)
    for k in range(nz):
        for P in M.slice(z0+(k+0.5)*p).to_polygons():
            P = np.asarray(P); rr, cc = dpoly((P[:, 0]-x0)/p-0.5, (P[:, 1]-y0)/p-0.5, shape=(nx, ny)); V[rr, cc, k] ^= True
    return V
def fillet_union(bodyM, armM, box=((138, 108, 0), (196, 148, 84)), r=3.0, p=0.25):
    (x0, y0, z0), (x1, y1, z1) = box; nx, ny, nz = int((x1-x0)/p), int((y1-y0)/p), int((z1-z0)/p)
    a = voxelize(armM, x0, y0, z0, nx, ny, nz, p); b = voxelize(bodyM, x0, y0, z0, nx, ny, nz, p)
    a = (edt(~a)-edt(a))*p; b = (edt(~b)-edt(b))*p; mm = np.minimum(a, b)
    sm = np.maximum(r, mm)-np.sqrt(np.maximum(r-a, 0)**2+np.maximum(r-b, 0)**2)      # circular smooth-min
    core = (sm < 0) & (mm > 0.15) & (a < r+0.3) & (b < r+0.3)
    lab, n = label(core); sizes = np.bincount(lab.ravel())*p**3
    mask = binary_dilation(np.isin(lab, [i for i in range(1, n+1) if sizes[i] >= 5.0]), iterations=3)
    add = np.where(mask, np.maximum.reduce([sm, -mm-0.4, a-(r+0.3), b-(r+0.3)]), 10.0)
    vv, ff, _, _ = marching_cubes(np.pad(add, 1, constant_values=10), 0.0, spacing=(p, p, p))
    tm = trimesh.Trimesh(vv+np.array([x0, y0, z0])-p/2, ff[:, ::-1], process=True)
    if tm.volume < 0: tm.invert()
    return to_mf(tm)

b = body(BUMP)
cup = sorted((b+peg+fillet_union(b, peg)).decompose(), key=lambda q: -q.volume())[0].simplify(0.01)
print("cup volume mm3:", round(cup.volume(), 1), "(expected ~65805)")

# ---------------- 5. write 3MFs ----------------
def obj(i, name, M):
    mm_ = M.to_mesh(); V = np.array(mm_.vert_properties)[:, :3]; F = np.array(mm_.tri_verts)
    vs = ''.join(f'<vertex x="{a:.4f}" y="{b_:.4f}" z="{c:.4f}"/>' for a, b_, c in V)
    ts = ''.join(f'<triangle v1="{a}" v2="{b_}" v3="{c}"/>' for a, b_, c in F)
    return f'<object id="{i}" name="{name}" type="model"><mesh><vertices>{vs}</vertices><triangles>{ts}</triangles></mesh></object>'
def write3mf(path, title, objs):
    res = ''.join(obj(i+1, n, M) for i, (n, M) in enumerate(objs)); items = ''.join(f'<item objectid="{i+1}"/>' for i in range(len(objs)))
    model = ('<?xml version="1.0" encoding="UTF-8"?>\n<model unit="millimeter" xml:lang="en-US" '
             'xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02">'
             f'<metadata name="Title">{title}</metadata><resources>{res}</resources><build>{items}</build></model>')
    ct = ('<?xml version="1.0" encoding="UTF-8"?>\n<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
          '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
          '<Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
    rels = ('<?xml version="1.0" encoding="UTF-8"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
    with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', ct); zf.writestr('_rels/.rels', rels); zf.writestr('3D/3dmodel.model', model)

write3mf(f"{OUT}/Diono_CupHolder_v12_Cup_and_SnapDisc.3mf", "Diono cup holder v12",
         [("Cup v12 (prints upside down)", cup.translate([-56, 0, 0])), ("Snap disc v12", disc.translate([200, 60, 0]))])

RH = 18.0; pos = {0.65: (55, 55), 0.75: (150, 55), 0.85: (55, 160)}; objs = []
for k, p in enumerate((0.65, 0.75, 0.85), start=1):
    r = (body(p) ^ mf.Manifold.cube([200, 200, RH]).translate([C[0]-100, C[1]-100, H-RH])).translate([-C[0], -C[1], -(H-RH)])
    for j in range(k):   # 1/2/3 marker notches on the outside at the bed
        a = np.radians(-90+(j-(k-1)/2)*4.0)
        r = r - mf.Manifold.cube([1.2, 1.0, 4.0]).translate([-0.6, -0.5, -1]).rotate([0, 0, np.degrees(a)-90]).translate([39*np.cos(a), 39*np.sin(a), 0])
    objs.append((f"Test ring {p:.2f} mm bumps ({k} notch{'es' if k > 1 else ''})", r.translate([*pos[p], 0])))
objs.append(("Snap disc v12", disc.translate([160, 165, 0])))
write3mf(f"{OUT}/Diono_CupHolder_v12_FitTest_Rings.3mf", "Diono v12 snap fit test rings", objs)
print("done ->", OUT)

```
