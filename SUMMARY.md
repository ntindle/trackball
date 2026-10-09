# trackball-base layout — SUMMARY (DONE 2026-10-09, branch job/trackball-base-layout)

## Deliverables (all committed on branch)
- Board: `trackball-base/trackball-base.kicad_pcb` — 4L 1.6mm FR-4
  (F / In1-GND-plane / In2-sig+power / B), 110.10×140.10mm.
- Project files: `.kicad_pro`, `fp-lib-table` (project-local NoP10 QFN
  variant for U501, pad 10 removed, DNC-verified).
- Reviews: `notes/LAYOUT_REVIEW.md` (§7 through §7.10.46),
  `notes/SCHEMATIC_REVIEW.md` (§11 Q5 ECO, §12 Q6-A removal),
  `notes/PINMAP.md`, `notes/FW_HANDOFF_S2MOT.md`, `notes/wavez/` renders.
- Evidence: ERC 0 errors + 1 benign warning; DRC drc246 1 unconnected
  (VIN-pad3 documented accept) / 0 errors / warnings identical to baseline.
- Fab: `trackball-base/fab/` regenerated 4L — 13 gerbers + job file,
  Excellon drill, both-side positions, STEP (36 solids), generic BOM
  (150 refs), README with stackup/order/assembly notes.

## How the opens closed
- +3V3-gap-a: L2 hop (drc240). VIN-pad3: documented ACCEPT last resort
  (§7.10.35, rigid-body invariant; 3/4 VIN pins connected).
- FTH: NoP10 variant + west-via/In2-dogleg/divider-via (drc244, §7.10.44);
  4 relief attempts aborted pre-placement with measured proof (§7.10.40-43).
- S2_MOT: Q6-A owner-approved removal to firmware polling (ERC 0/1,
  drc245, §7.10.45, FW handoff). 15trk/3via purged, pads cleared.

## Remaining / owned elsewhere
- VIN-pad3 accept (documented, §7.10.35). S2_MOT firmware poll plan
  (firmware-owned). Provisional values bench validation (§7). No enclosure
  CAD (pre-existing). Full Blender-manual pass deferred to GUI session.
