# SUMMARY — trackball ball electronics (delegate status, 2026-10-10Z)

**Design work advanced; nothing ordered (DO-NOT-ORDER: gated on Phase 1 exit + owner purchase approval). No shell on this box — all tool runs are human-side.**

## CLOSED (file-verified this job)

- **Main PCB touch + control**: Geometry A (U2 0x37) + Geometry B (U3 0x38), all control (HI/XRES/I2C/LED/SWD/SPARE/DEC1-2-4/XC/VBAT_SNS/CHRG/FAULT), U3-I2C, DEC3, DHC, VBAT-loop, +3V0-island (U2/U3-VDD, pullups), INTVCC, BOOST/SW/VIN. 13 live-short defects found+fixed (#1–#11, #13; #5/#7–#11 EP-class, #12/#14 filed or disproven — see below).
- **Owner verdicts executed**: Q10a NRESET accept-open, Q13a CHRG↔FAULT swap, Q14d(ii) C18-mirror, Q15a power cascade, Q11(A) U1.13-XRES2-open RATIFIED (accept-open, Q10a precedent; firmware P0.16-disabled, U3 on SW-reset).
- **Coil v0.2 + J1-edge fix**: 14.8mm spiral, separated nets, all feeds verified; J1 moved south 0.2 (J1.3-copper was 0.04 over r11). DONE pending human DRC/exports.
- **Flex v0.1** (geometry A, FAB-HOLD), **Stage 1** coupons/test-plans/bench-handoff/DO-NOT-ORDER BOM, **CAD** (frozen-nominal parametric), **ESB** protocol doc, firmware handoff notes.

## Owner-BLOCKED (exact questions, in QUESTIONS.md Q11)

1. **East-field cascade arbitration** (ANT net6 + DEFECT #12, parked, do NOT route): (i) 6-net cascade (t490/t491/t788 delete + SWDIO-t572/573/574 move + R9 restitch + ANT route — NOT recommended blind); (ii) schematic ANT-to-GPIO move (almost certainly INVALID, RF-pin class — same error as DEC3); (iii) no-RF V1 (NOT recommended, kills radio link). DEFECT #12 (live SWDIO-t573-via ↔ DEC2-t594 short, 0.25×0.6, debug-into-regulator) rides this verdict — owner-urgent, no verified standalone fix. R9-displacement was STOPPED per owner fallback with three independent file-proofs.

## Parked with proof (delegate scope, no verified route yet)

U1.25/U1.32-VDD (redundant pins; rail LIVE via pad9 — pinout audit to confirm), C6.1/C11.1, C23.2-CELL_N + TP12, RUN divider + U4.16, PROG/NTC/CHGSNS, VIN-west (R12.1/C20.1), J2.2-GND + C8.2-GND (GND pours verified present (B.Cu + In1.Cu whole-board, 0.3 clr + thermals): J2.2-GND + C8.2-GND + R16.2-GND closed pour-fed; U5_VM (U5.6→R16.1) parked NEW with proof + CHG-005 protection-degraded flag for human datasheet audit), J3.1/C21.1 landlocked. U1-VDD rail live; no floating-rail accept-opens outstanding.

## Human TOOL-RUN-TBD (branch job/trackball-ball-electronics, no shell for delegate)

`kicad-cli sch erc` + `pcb drc` (expect: parked-net unconnecteds + RATIFIED XRES2-open + ONE live short #12 + 0.2-exact inventory + U4-EP 0.1-footprint flags; 0 clearance violations elsewhere), fab exports (Gerbers/STEP), KiKit, Blender/FreeCAD STEP, pinout + lib audits (incl U4-EP 1.7×1.7 oversize flag, C8 descr, nRF52 RESET pull-up confirm, U1-VDD redundancy), `git add/commit/push`, bench gates 2.1–2.6.
