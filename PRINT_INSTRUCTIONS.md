# How to print the Diono Cup Holder (v13)

**File to open:** `Diono_CupHolder_v13_Cup_and_SnapDisc.3mf`. All settings are already inside it.

**New (2026-10-07): the snap rod now has a hole down its centre for a steel screw.** If you haven't rebuilt the project since then, do this first on your PC: `git pull`, then `cd design_files`, then `python Diono_CupHolder_v13_bambu_project.py`.

## Steps

1. Put the **Textured PEI plate** on the printer. **Wash it with dish soap and warm water**, rinse, and dry it. Don't touch the surface afterward. (Finger oils make PETG come loose.)
2. In Bambu Studio: **File → Open Project** → choose `Diono_CupHolder_v13_Cup_and_SnapDisc.3mf`.
   If it asks about loading settings, say **yes**.
3. Pick your **PETG** spool in the filament box.
4. **Don't move or rotate anything.** The cup is meant to be upside down.
5. Click **Slice plate**. **Before printing, check the preview:**
   - a thin **brim** ring around the rim on the plate
   - **no supports** (the cup doesn't need any)
   - about **152 g** of filament, about **4 hours**

   If the brim is missing or the weight is far off, **don't print**. Close the project without saving and open it again.
   Bambu may show **"floating regions"**. That's normal: it's the tiny ridge on the clip rod, which prints fine. Print anyway.
6. Click **Print plate**. Keep the printer door **closed**.
7. Let the plate **cool down**, then take the parts off and peel off the thin brim.

## Putting it together

- **Disc:** tilt it into the cup, hook one edge under a bump, press down until it clicks. It should sit snug with no rattle.
  To take it out, push up from underneath.
- **Steel screw (makes the arm much harder to break):** use an **M5 × 60 mm stainless set screw** (no head). Screw it into the hole in the **tip of the snap rod** with a 2.5 mm hex key until it's flush with the tip.
  It cuts its own thread, so go slowly: a drop of dish soap helps, and back it out half a turn every few turns. If it gets too hard to turn, run a 4.5 mm drill bit through the hole by hand, then try again.
  (An M5 × 50 button-head screw also fits, but its head sticks out of the rod tip. Test that it still clips into the seat.)
- **In the car:** clip it onto the seat like before. The flat face of the shelf faces the seat.

## Good to know

- Don't leave a full, heavy bottle in it while the car is parked in hot sun.
- Design files and details are in the `design_files` folder. You don't need them to print.
