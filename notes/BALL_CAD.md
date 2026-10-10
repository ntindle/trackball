# Ball CAD note (frozen nominals Rev 2.2)

Run: `blender --background --python cad/ball_cad.py` (TOOL-RUN-TBD — no shell on this box).
Script builds from frozen nominals only: **Ø40.0 sphere, 1.2 ±0.15 wall** (solidify; tolerance is a manufacturing check, not modeled geometry), equatorial ring band 8 mm (flex home), charging pole at −Z (coil pocket r11.5 for the Ø22 coil PCB + ferrite), orientation dot Ø2.0 at +Z with Ø3.0 LED light pipe below it (CHG-007), 3× M1.6 boss holes matching main-PCB H1/H2/H3, 401230 cell bay witness block (31 × 13 × 5 clearance), screwed/serviceable split at the equator — never glued.

Review gate (standing authority — Blender-manual review): open the generated blend, apply the chassis booleans, verify boss/hole alignment against `trackball-ball.kicad_pcb` H1–H3, verify the dot/pipe/LED stack against D2/D3 placement, then export.

## STEP route (deviation note)

Blender has no native STEP exporter, so the chain is Blender STL → FreeCAD STEP:

1. `freecad -c "import Import, Part; m = Import.open('exports/ball_upper.stl'); ..."` (exact macro TOOL-RUN-TBD, recorded here at conversion time), or GUI: File → Open STL → Part workbench → Create shape from mesh → Convert to solid → Export STEP AP214.
2. Repeat per part (upper, lower, chassis).
3. Record FreeCAD version + macro in this file at conversion time.

This is a documented tool-chain deviation, not a geometry deviation: the frozen Ø40.0/1.2 nominals are untouched.
