# BALL_REVIEW.md — ball electronics review notes (v0.1)

Working-method note: layout-level judgment calls applied under standing authority without asking. Skills named per choice (`kicad-schematic`, `kicad-symbol`, `kicad-footprint`, `kicad-layout`, `kicad-pcb`, `kicad-bom`, `kicad-export` for the TOOL-RUN-TBD exports). LAYOUT_REVIEW §7.10.x rigor: measured proof or explicit bench-TBD, never hand-waving. Shell broken on this box (bwrap loopback denied) — every `kicad-cli`/KiKit/Blender/git step is TOOL-RUN-TBD for the human (exact commands below).

## Architecture (locked)

3 boards: main Ø28 4L (`trackball-ball/`), coil Ø22 2L (`trackball-ball-coil/`), flex ring/tail/antenna-tab (`trackball-ball-flex/`). One sheet, labels-only wiring throughout (`kicad-schematic`). 2× CY8CMBR3116-LQXI @ 0x37/0x38: U1 geometry A (24 ch), U2 geometry B (16 ch) — both footprints on the board so the coupon winner needs no re-spin (TOUCH-001, ELEC-002). nRF52810-QCAA (U3). LTC4120-4.2 (U4). BQ29700 (U5) + DMG6968U (Q1) two-level protection (CHG-005, never waivable). XC6206P302 LDO 3.0 V (U6 — dropout headroom to VBAT≈3.3 V). Single FH28D-28S FPC (J1): 24 touch + ANT feed + 3 GND. Coil interface J2 (VIN/BGND/DHC). 401230 cell horizontal centered + NTC flying leads. 2× LEDs at the dot (CHG-007: amber CHG, green PWR — no light = not charging, never false green).

## Decisions with rule citations

- DCC open (LDO mode) to save deep-sleep Iq; 1M/330k VBAT divider (ELEC-023); 560R per Cx (ELEC-004); 0.42 pF-class TVS only on I2C lines (`kicad-schematic`).
- RPROG 20k → 60 mA via hPROG=988 (CHG-005, ELEC-024); RUN divider 150k/100k ≈ 6.1/5.6 V thresholds (CHG-002).
- BOR highest threshold (ELEC-031). FREQ=GND, EP grounded with 4× thermal vias (ELEC-004).
- Antenna + π-match on flex tab with stiffener (ELEC-028); keepout on main F.Cu around ANT feed (RF-001/022 volumetric keepouts honored in 3D stack: no copper/ferrite/battery near the tab).
- U3 crystal 32 MHz + 12 pF load-trim caps (provisional trim — bench-TBD); HI assumed OD-capable (provisional).
- Bottom-side parts mirrored-X in-file (U4/U5/U6/Q1 + all bottom passives); TH connectors unmirrored (`kicad-layout`, `kicad-footprint`).
- Mounting H1 moved to (104.5, 89.5) after TP3 collision analysis; H3 (88.5, 99.5) clears C18/R12; all holes ≥0.25 from copper edge (`kicad-layout` micro-move authority).
- Coil v0.2 (`kicad-layout`): nets separated in sch (1-line label fix: L1.2→GND; RX_A={L1.1,C1.1,J1.3/DHC-tap}, VIN_RX={C1.2,D1.2,J1.1}, GND={L1.2,D1.1,J1.2}); 14.8mm square 5.7-turn spiral fits r11 (0.39 edge, 0.3/0.3 cu/gap); all three nets routed; net-tie NT1 (`net_tie_pad_groups "1,2"`) at center hole joins RX_A→GND as coil inner terminal (L1 has no footprint — hand tracks can't join nets otherwise; syntax MUST be confirmed by human DRC, fallback = discrete 0R); net0 pours removed (no copper pour under coil — eddy); C1→(96,108.3), D1→(105,108.5) (D1 edge 0.24, noted); J1.1 fed on B.Cu (F.Cu blocked by RX_A lane). Self-caught during authoring: GND stub started on RX_A spiral end (would-be short) — repaired via center net-tie. Prior SPARE-U4 quad-short catch (main board t580 cut U4.1-4 pads) fixed same session.
- Main routing v0.2 (`kicad-layout`, all hand-math 0.25/0.6-0.3/0.2, no via-in-pad): touch+CS (48 nets) + control + I2C-U3 (t709-t723, no moves) + ANT (t724-t732, SWD untouched, self-moved VBAT lane) + U5_BAT (t738-t742) + p20/C6.2 GND stitches CLOSED. Parked with clearance-proof: DEC3, NRESET, FAULT-U1.6, BOOST/SW/INTVCC/DHC/VIN (Q14d), U2.7/U2.6 cluster. Borderline inventory (all 0.2-exact, accepted precedent, human DRC to confirm): CS10/CS11 threading ×2, SDA/SCL jog stagger, ANT/T17 lane + ANT/U2-west-pads, VBAT/U5.4, VIN-lane/RX_A ×2, J1.1-stub/RX_A-lane; coil: VIN-lane/RX_A ×2. Tented-via assumption throughout (plotparams viasonmask=false).
- Coil WIRE pads moved to top edge SMD (J1 footprint exceeded Ø22 outline — caught before fab).
- Flex = geometry A with explicit FAB-HOLD (coupon winner freezes geometry; silkscreen says so).
- CAD STEP via FreeCAD (Blender has no STEP exporter) — tool-chain deviation only.

## Provisional values (bench-TBD, never stated as facts)

C22 DHC value/topology; tank L/C + coil current + Vpk/SNR; Y1 12 pF trim; HI OD assumption; LED exact MPNs; TX annular-vs-disk k/Q thresholds (§6 2.4 numbers); NTC curve; ESB TX-power/range; antenna π values (VNA). NEW v0.2: coil 14.8mm (was 19mm est) → L/k/Q re-tune + gate-2.4 thresholds re-validate (CHG-009); ANT feed 0.25mm microstrip impedance + T17-parallel crosstalk (RF/ELEC bench); net_tie_pad_groups syntax confirm via human DRC; borderline inventory above re-measured in DRC; tented-via wicking spot-check (JLCPCB); U3 0x38 SAVE_CHECK_CRC still required; all Q10/Q11c/Q13/Q14d-gated nets (NRESET/DEC3/FAULT/BOOST/SW/INTVCC/DHC/VIN/U2.7/U2.6) unresolved by construction.

## Deviations from frozen spec (explicit, with rationale)

1. IQS → CY8CMBR3116 (IQS266x-class cannot reach 24 ch off-the-shelf; SmartSense replaces ATI per ELEC-002; XRES documented vs ELEC-004 IQS-NRST).
2. LDO 3.0 V (not 3.3 V) for dropout (above).
3. U3 second address 0x38 requires production EZ-Click SAVE_CHECK_CRC step (gate 2.3).

## TOOL-RUN-TBD (human, exact commands)

- `kicad-cli sch erc trackball-ball/trackball-ball.kicad_sch` (+ flex, coil) → expect 0 errors; document warnings.
- `kicad-cli pcb drc --schematic ... trackball-ball/trackball-ball.kicad_pcb` → v0.1 WILL show unconnected (no routing yet) + must show 0 clearance/short violations; routing pass is the scheduled follow-up (freerouting.org singles/pours per standing authority).
- `kicad-cli sch export pdf / pcb export gerbers / pcb export step` per `kicad-export`; KiKit panelize (coupons); Blender + FreeCAD per BALL_CAD.md; `git add/commit` (no commits by this job — no shell).
- Pinout audits before ANY fab: nRF52810-QCAA (Nordic PS), LTC4120EUD, MBR3 pin 6, DMG6968U SOT-26, FH28D-28S vs Hirose CL586-1835-4, XC6206 SOT-23, ABM8 pads, WSON-6 EP, C19 BOOST-SW, NTC bias, TVS package. See QUESTIONS.md.
