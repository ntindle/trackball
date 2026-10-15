# SUMMARY — trackball ball electronics (delegate status, 2026-10-10Z)

**Design work advanced; nothing ordered (DO-NOT-ORDER: gated on Phase 1 exit + owner purchase approval). No shell on this box — all tool runs are human-side.**

## CLOSED (file-verified this job)

- **Main PCB touch + control**: Geometry A (U2 0x37) + Geometry B (U3 0x38), all control (HI/XRES/I2C/LED/SWD/SPARE/DEC1-2-4/XC/VBAT_SNS/CHRG/FAULT), U3-I2C, DEC3, DHC, VBAT-loop, +3V0-island (U2/U3-VDD, pullups), INTVCC, BOOST/SW/VIN. 13 live-short defects found+fixed (#1–#11, #13; #5/#7–#11 EP-class, #12/#14 filed or disproven — see below).
- **Owner verdicts executed**: Q10a NRESET accept-open, Q13a CHRG↔FAULT swap, Q14d(ii) C18-mirror, Q15a power cascade, Q11(A) U1.13-XRES2-open RATIFIED (accept-open, Q10a precedent; firmware P0.16-disabled, U3 on SW-reset).
- **Coil v0.2 + J1-edge fix**: 14.8mm spiral, separated nets, all feeds verified; J1 moved south 0.2 (J1.3-copper was 0.04 over r11). DONE pending human DRC/exports.
- **Flex v0.1** (geometry A, FAB-HOLD), **Stage 1** coupons/test-plans/bench-handoff/DO-NOT-ORDER BOM, **CAD** (frozen-nominal parametric), **ESB** protocol doc, firmware handoff notes.

## Owner-BLOCKED (exact questions, in QUESTIONS.md Q11)

1. **East-field cascade (i) EXECUTED 2026-10-12** (owner-authorized): ANT CLOSED pad19→J1.2, SWDIO rerouted, R9 moved+refed, U3.7 ext-fed, DEFECT #12 DEAD (t573 removed). Gates 1–4 pass hand-verified (3× 0.2-exact, zero below 0.2); gate 5 tool-DRC QUEUED human (no shell — clean NOT claimed). C5.1 parked per authorization (rail live; degraded-decoupling flag for human review).

## Parked with proof (delegate scope, no verified route yet)

U1.25/U1.32-VDD (redundant pins; rail LIVE via pad9 — pinout audit to confirm), C6.1/C11.1, C23.2-CELL_N + TP12, RUN divider + U4.16, PROG/NTC/CHGSNS, VIN-west (R12.1/C20.1), J2.2-GND + C8.2-GND (GND pours verified present (B.Cu + In1.Cu whole-board, 0.3 clr + thermals): J2.2-GND + C8.2-GND + R16.2-GND closed pour-fed; U5_VM (U5.6→R16.1) parked NEW with proof + CHG-005 protection-degraded flag for human datasheet audit), J3.1/C21.1 landlocked. U1-VDD rail live; no floating-rail accept-opens outstanding.

## Human TOOL-RUN-TBD (branch job/trackball-ball-electronics, no shell for delegate)

`kicad-cli sch erc` + `pcb drc` (expect: parked-net unconnecteds + RATIFIED XRES2-open + ONE live short #12 + 0.2-exact inventory + U4-EP 0.1-footprint flags; 0 clearance violations elsewhere), fab exports (Gerbers/STEP), KiKit, Blender/FreeCAD STEP, pinout + lib audits (incl U4-EP 1.7×1.7 oversize flag, C8 descr, nRF52 RESET pull-up confirm, U1-VDD redundancy), `git add/commit/push`, bench gates 2.1–2.6.

## Driver status 2026-10-15Z

- Q-G nudge program complete: OP1 executed (XRES2 ...837 shortened, tool-verified; clearance 0.1771->0.325, pair absent from DRC report) + 3 no-ops + t836-t544 corner parked for owner rework verdict. Committed c7df811 (driver).
- Post-OP1 tool recount (kicad-cli, sparkvm): ERC 510 flat; DRC 1748/63/92 flat vs gate-9 baselines — no regression.
- Everything remaining (ASK-1/2/3, t836-t544 corner, XRES2-U3_CS3 short, LED_DOT-544-VBAT-893 0.075) is parked for OWNER verdicts. Nothing closable under standing layout authority. Job stands down until verdicts arrive.
