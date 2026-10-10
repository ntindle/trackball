# SUMMARY — trackball ball electronics (Stage 1 + Stage 2 design)

**Design work complete. Nothing ordered (gated on Phase 1 exit + owner purchase approval).**

## Deliverables (all under `work/` — job-dir writes were sandbox-denied, human to move: PROGRESS/QUESTIONS/SUMMARY/notes)

1. **Main ball PCB v0.2-routing-in-progress** (`trackball-ball/`): pro/sym/sch/dru + 16 footprints in `.pretty` + placed `.kicad_pcb` (Ø27.5, 4L, pours, keepouts, outline). ROUTED & CLOSED by hand-math (0.25mm/0.6-0.3 vias/0.2 clr, no via-in-pad): Geometry A (U2 0x37: T00-T11 + CS0-CS11 + CMOD, t001-t185), Geometry B (U3 0x38: T12-T23 + CS0-CS11 + CMOD, t186-t399), control (HI1/HI2/XRES1/XRES2/I2C-west/LED/SWD/SPARE/DEC1-2-4/XC/VBAT_SNS/CHRG/FAULT/U6 + GND stitches, t400-t703). ERC-directed by construction; DRC/exports/STEP/commit all TOOL-RUN-TBD (no shell — bwrap denied). CLOSED since: Q9 (U3-I2C t709-t723, no moves), Q12 (ANT t724-t732, SWD untouched), Q15-partial (U5_BAT t738-t742, p20/C6.2 GND; U2.7/U2.6 parked sealed), coil v0.2 above. BLOCKED only on owner-only Q10 (NRESET accept-open), Q11c (DEC3↔SPARE swap), Q13 (CHRG↔FAULT swap), Q14d (U4-rotation/INTVCC direction) before the Q14d-gated power tails (BOOST/SW/DHC/VIN/CHRG/INTVCC) + bulk power + J2/J3/L1 landings.
2. **Flex v0.1** (`trackball-ball-flex/`): 24-electrode geometry-A ring + tail + antenna tab + π-match, FAB-HOLD silk pending coupon winner.
3. **Coil board v0.2** (`trackball-ball-coil/`): sch nets separated (RX_A/VIN_RX/GND); 14.8mm square 5.7-turn spiral fits r11 (0.39 edge; documented deviation from 19mm est, bench re-tune CHG-009); all 3 nets routed (RX_A lead/lane/stub, VIN lane + B.Cu J1.1 feed, GND B.Cu + y109 F.Cu bus); net-tie NT1 at center hole (syntax for human DRC, 0R fallback); net0 pours removed (eddy); C1→(96,108.3), D1→(105,108.5); provisional tank/zener values kept; ferrite note kept.
4. **Stage 1** (`notes/STAGE1_COUPONS.md`): coupon T-A/T-B/C/M fab specs, gates 2.1–2.6 with explicit PASS criteria, bench handoff (equipment/procedure/sheet), DO-NOT-ORDER BOM.
5. **CAD** (`cad/ball_cad.py` + `notes/BALL_CAD.md`): parametric frozen-nominal model, STL now, STEP via FreeCAD.
6. **ESB** (`notes/BALL_ESB.md`): 32 B packets, channels, DFU relay (FW-010), BASE_STATUS reserved, RING_SCROLL_ENABLE gating.
7. **Review/BOM** (`notes/BALL_REVIEW.md`, `notes/BALL_BOM_DRAFT.md`): every governed choice rule-cited, provisional list, 3 explicit deviations, real-parts BOM with VERIFY flags.
8. **QUESTIONS.md**: 15 items — Q1-Q8 (pinout audits, TX-MPN/λ_sensor gaps, no-shell caveat) + Q9-Q15 (routing contact points with audited options; In2-hops REJECTED after full In2 occupancy audit found no east-west corridor).

## Key judgments

MBR3 over IQS (channel count); both geometries on-board (no re-spin); single-net coil spiral v0.1 with v0.2 net-tie TODO; J1.3=DHC_SNS=RX_A provisional; LDO 3.0 V; bottom-side mirrored-X; H1/J1/coil placements fixed after collision analysis.

## Human runbook (shell was broken — bwrap denied)

`kicad-cli sch erc` + `pcb drc` all three projects → route v0.2 → `kicad-cli` fab exports + KiKit + Blender/FreeCAD → `git commit`. Pinout audits before any fab. Then bench gates 2.1–2.6.
