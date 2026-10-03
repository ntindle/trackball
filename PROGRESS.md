2026-09-30T17:50Z layout-place: pin-map audit clean (SOTs correct, HRO opening +Y, D2FC COM/NO ok); geometry resolved from FINAL_SPEC (MECH-008 ball-lateral, MECH-049 thumb<=45, TX annular r24-30 prov, no routed D44). Writing placement script next.
2026-09-30T19:05Z layout-place: topology fully decoded (power/SPI/USB/TX/BTN/SWD); routability proven for all critical nets (USB via-joins, SPI radial coil crossing, E73 fanout); writing board build script.
2026-09-30T20:10Z layout-build: placement table complete (155 fps); E73 fanout ECO (edge pads 0.8->0.5) + L501 courtyard shrink applied; running board build.
2026-09-30T20:45Z layout-build: placement CLEAN (155 fps, 0 courtyard clashes, 0 missing); running DRC+parity.
2026-09-30T22:10Z layout-drc: annotation fixed (dup FIDs), live netlist (155/88), FPID+fields+pro+dru ECOs, silk strategy set; rebuilding.

## P6-DRC18 (02:30Z)
P6 placed 20 jobs (U0/U1/U15/U18/VIN/U20/U23/U24/U26via) + C507-ECO + E0-viamove, audit 46/46 OK. DRC18: 20 unc (was 30) + 43 errors (was 17). P6 closed U0/U1/U18/U20/U24/U26 + stale U25/U9/U11/E15 cleared. New P6-errors: SW2/SW1_LTX coilfan width (10), +3V3-vs-S1_MOSI/MISO/AIN5 shorts (E31-34/36-38, survey-miss), E13 hole (+3V3 vias), E14b hole (GND vias), E20 TX_EN-short (missed via), E21/22 U15-vs-CTS, U23-UNROUTABLE (C507/FB/CTD triangle: E0/E15/E18/E39/E40), E16/E26-30 GND-vs-VBUS top (P5), E19 VDDPIX-via, E1/E2/E25/E41/42 GND-via (57.2,128.9). U3-E0-orphan (new UNC). P7: fix-all + U27/U28/U2/U3/U11/U15post/EAST/NORTH routes. P8-defer: U4/E11/E14/E16/E24 (U202-cage), U25/E1/E2 (VBUS-top), U15/CTS, U13, E17, E23/E35.

## P7-DRC19 (03:15Z)
P7 placed 26 jobs (SW2/SW1_LTX-w0.3, EAST, U27/U28/U2/U3/U11/U15post/U19/E20/E14b/E0orphan), audit 81/81 OK. DRC19: 20 unc + 77 errors (REGRESSION +34). Root causes: svbatch MISSES tracks (S1_MOSI-x=24.4, BTN1-x=19.6, NTC-B, CTS-B, VIN-B, BTN3-B, VSEN-x=18.57, R202, R507.2-stub, D501-A-x=66.2, C504.1-body, U201.39-corner) + my endpoint-vs-body mistakes (FB-via, TX_STAT-via, C504.1, GND-y=11.0). U27-UNROUTABLE (escalate), U11-HOLD (FB/EN), U28-E-HOLD (VIN/NTC/L501.1), U19-REDUX-2, U18-REDUX, EAST-REDUX-2, NORTH-REDUX-2+U2-W-FIX, U17-fix, U4-FINAL-2 ready P8. P8-block grows: U1/U2/U3/U4/U5/U7/U8/U9/U10/U12/U14/U15/U16/U18 + holds.

## P8-DRC20 (04:00Z)
P8 placed 18 jobs (restores + U19-REDUX-2/U18-REDUX/EAST-REDUX-2/NORTH-REDUX-2/U2-W-FIX/U2-E-FIX/U17/U4), audit 45/45 OK. DRC20: 24 unc + 41 errors (-36 ✓). New fails: U19-B (spi/NCS/BTN3/P0.12-maze) HOLD, U18-N (TX_EN/FB_PK) REVERT-y=6.1+TX_EN-viamove, EAST (AIN5/S1_MOSI-x2) HOLD, U4-N (BTN2/+3V3/R201.2/P1.11) HOLD, E3/E13/E38/E40-unexplained (probe), U15-VIN-netcode? (probe). U1-FIX, U28-S-FIX-2, U2-FIX, U18-REVERT ready P9. P9-block: U3-U19 + holds (U27/U23/U19/U28-E/U11/U15/U13/U4/EAST).

## 2026-10-03 — DRC18→DRC126: 57→27 unconnected, 0 errors, 0 parity — BLOCKED Q5/Q6

Hand/survey routing P6–P130 + rb6–rb43 + q1–q27 + sv3a–sv35f. Every
placement verified by TRUE pcbnew corridor survey (0.5 mm margin) +
file audit; every DRC choice cites rule ID (CLR/Power/vbus_clearance/
vbus_min_width/COILFAN/KICAD-013; trackball-drc/RULES.md normative file
NOT present in worktree — cites use LAYOUT_REVIEW §8 E-series).

Closed −30: T-junction workarounds (P37/P99/P100: split + endpoint-
endpoint re-add — KiCad ratsnest misses MID-touch T-junctions),
via stitches (P129/P130), U2 (P101/P102), U7-GND (P106), U10-RST
(P107), U12-RST (P101/P104), U26-D501-A-B (P108), VBUS/GND crawls
(H3.1 P78, GND-S P91, U7-U8 P44, U15-U17 P31, U14 P32, U5 P33).

Ripup attempted & reverted (net-zero or negative): TX-zone (rb36/P109:
CTD placed, 10 DRC errors incl C507.2 SHORT + D501-A crossing; reverted
rb39/P112–P114), RST-maze (P103: 12 DRC errors; reverted rb35/P104/P105),
SEN-N (rb23), U8N (rb25), C505N (rb28/rb29), C203N (rb32), C101N (CC2),
J201N/E (B8/?-pads), VIN-N (BTN3-diag rb42/P128).

Independent oracle: freerouting.org 2.4.1 headless (Temurin JRE 25,
50-pass budget, /tmp/route27.dsn): stuck at 73 unrouted, score frozen
716.45 across passes 2–4 (no progress) before timeout — autorouter
agrees remaining cages hold.

DRC126: unconnected_items=27 parity=[] errors=0 warnings=182
(123 lib_footprint_mismatch per KICAD-013, 49 dangling, 3 via-dangling,
2 holes_co_located, 2 silk_edge). Full pairs in /tmp/resume_drc126.json.

BLOCKED: Q5 schematic-ECO (4 pads: U501.14-CTD, U201.3-VBUS_SENSE,
U201.42-SEN, U201.28-MCU_TX_EN — alternate taps, schematic-intent,
exceeds Q1–Q4) + Q6 placement-ECO decision (TP305/TP306 cheap move +
accept-or-destructive-ripup on 23). See notes/QUESTIONS.md.
Fab outputs NOT refreshed (27 opens — not shippable); LAYOUT_REVIEW
§1/§4/§5/§7/AppB updated to drc126.

## 2026-10-03 — TP305/TP306 micro-move + U2 close: 27→26 unc, 0 errors, 0 parity (DRC127)

Per continuation directive (Q6 cheap move; NO Q5 schematic ECO, NO
destructive re-places). Probe revealed TP305/TP306 pads are F.Cu-only,
no drill — they never blocked B copper; the real U2 cages were
S2_SCK-diag (path A y=41.7, crossing (43.22,41.7)) and S2_SCK-E-W-y=42.8
+ N-S-x=78.0 corner (path B N-S-x=63.51).

ECO4 (standing Q1 craft): TP305 (44.0,42.0)→(44.0,43.5),
TP306 (44.0,46.0)→(44.0,47.2); both stay stub-connected (same-net F
overlap, surveyed tp305n/tp306n clear). P131 (audit 7/7): B-E-W-y=45.0
x[44.9,77.0] (corr45 clear) + via (77.0,45.0) + F-hop x[77.0,78.8]
(fhop EMPTY) + via (78.8,45.0) + B-N-S-x=78.8 y[42.0,45.0] +
B-E-W-y=42.0 x[63.51,78.8] (e41/e45/n78 clear; y=42.0 dodges GND-x=64.1
S-end (0.425) and S2_SCK-y=42.8 (0.425)) + N-S-x=63.51 stub y[41.7,42.0]
(exact endpoint joins, no T-quirk).

DRC127: unconnected_items=26 parity=[] errors=0 warnings=179
(+3V3 left: U0/U1 F-west only (Q6)). See /tmp/resume_drc127.json.

Still BLOCKED: Q5 (4 alt-taps, schematic-intent) + Q6 remainder (23
accept-or-destructive). QUESTIONS.md updated (TPs resolved).

## 2026-10-03 06:55 -0600 — drc127 housekeeping: prl restore verified, tree clean
- Post-commit audit: `git show --stat HEAD` = exactly 4 files (pcb + PROGRESS + LAYOUT_REVIEW + QUESTIONS); no collateral in c9bbc9c.
- `trackball-base.kicad_prl` deleted by pre-commit `rm -f`, restored from HEAD~1 blob (byte-identical; was unmodified pre-rm). All eco_bak/prl tracked + unmodified, `git status` clean.
- Awaiting owner on Q5 (4 opens / schematic ECO) + Q6-remainder (23 opens / destructive re-place). No further executable layout craft.

## 2026-10-03 10:20 -0600 — Q4 stage-1 Blender-manual review done, §9 committed (BLOCKED Q5/Q6 stands)
- Auto check_*.py scripts MISSING (not in repo, ~/workspace/trackball-drc absent) — stated, none invented. Manual equivalents in LAYOUT_REVIEW §9.
- Fresh drc-stage1.json (179 warn/26 unc/0 err/0 parity = drc127 scope), STEP+GLB regen, 4 Blender renders (hero/top/sensor/back, Cycles 64sp, calibration resid 0.0000mm) + kicad top/bottom cross-checks, all inspected.
- Measured: outline 110.1x140.1 sharp corners; H1-H6 3.2mm; U301/U302 26.68 apart rot0; J201 6 TH legs + 6.05 from edge; U202->J201 courtyard 3.99 (ELEC-006 PASS); L501 2xPTH 1.6; antenna strip x[10,34] y<2.0 clear both layers.
- FINDINGS: F9-1 zero zones in file (§1/§2.4/§3 pour claims corrected to intent); F9-2 project .wrl unloadable in KiCad 10 export + wrong-scale in render, J201/F101/D502 stock steps missing — deterministic Blender fallbacks used (J201 h3.5 / L501 h6.0 NOMINAL, App A.7-9).
- MECH-002/003/022, RF-022 volumetric, MECH-008/049, ELEC-029 need enclosure CAD/ball datum/coil geometry — recorded as not-verifiable-at-PCB-stage with PCB-side inputs.
- No schematic ECOs, no re-places. Awaiting owner on Q5 (4 alt-taps) + Q6-remainder (23 accept-or-destructive).
