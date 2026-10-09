# trackball-base fab outputs (WaveZ, 2026-10-09, branch job/trackball-base-layout)

Board: 110.10 × 140.10 mm, 4-layer 1.6 mm FR-4.
Stackup: F.Cu (signal) / In1.Cu (GND plane, poured) / In2.Cu (signal+power
escape) / B.Cu (signal). Design state: ERC 0 errors + 1 benign warning;
DRC drc246 1 unconnected (VIN-pad3 documented accept) / 0 errors.

## Files
- Gerbers (X2, precision 5, soldermask-subtracted): F_Cu, In1_Cu (.g1),
  In2_Cu (.g2), B_Cu, F/B Mask, F/B Silkscreen, F/B Paste, Edge_Cuts,
  F/B Fab + job file (.gbrjob).
- Drill: Excellon, mm units (.drl).
- Assembly: component positions both sides, mm (trackball-base-pos.csv);
  3D STEP (trackball-base.step, 36 solids).
- Generic BOM: trackball-base-bom.csv (fields export; no LCSC numbers
  claimed — assign at ordering).

## Order notes (JLCPCB 4L SMT, both sensors hand-placed per project rule)
- U501 uses a project-local footprint variant (pad 10 removed, DNC by
  schematic+layout; 19/20 perimeter pads + EP remain). Stock library
  untouched; fab uses board copper as plotted.
- Assembly watch (non-blocking): FTH divider via (60.60,31.75) hole edge
  0.12 mm from R505-2 pad edge, same net — no short risk; mask sliver may
  not resolve, minor wicking watch on one 0402 joint.
- Firmware-owned: S2_MOT removed (Q6-A); firmware polls S2 Motion 0x02b7 —
  see notes/FW_HANDOFF_S2MOT.md. Provisional part values in
  SCHEMATIC_REVIEW §7 need bench validation (pre-existing).
