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

## 2026-10-03 15:50 -0600 — BLOCKED triage: §7.6 known-opens (26) + drc128 snapshot committed, Q5/Q6 OWNER-DECISION PENDING
- No routing, no schematic ECO, no destructive re-place (all exceed standing directives). drc128 identical to drc127 (179 warn/26 unc/0 err/0 parity).
- LAYOUT_REVIEW §7.6: all 26 opens tabulated (Q5: U20/U21/U22-23/U26; Q6-remainder: 22 rows, TP fixed noted) with caged endpoints + tried (surveys/ripups/freerouting oracle).
- Snapshot: notes/stage1/drc128-triage.json + kicad-render128-top/bottom.png; QUESTIONS.md options (a) accept opens (b) Q5 ECO (c) Q6 re-place. Idle awaiting owner.

## 2026-10-04 02:50 -0600 — Q5 ECO EXECUTED: R113/114/115/515 placed, ERC clean, drc129 33unc/0err/0parity (pre-ripup checkpoint)
- Schematic: 3x 0R branch jumpers on power (R113 VBUS_SENSE, R114 SENSOR_EN, R115 MCU_TX_EN) + R515 CTD in-line on tx (split /tx/CTD_U501 + /tx/Net-(U501-CTD)). Fixed 2 file-format issues found by ERC: 3-pt polylines unsupported (split to 2-pt + junctions), CTD auto-split renamed (verbatim CTD_U501 label).
- ERC 0 errors + 1 known benign pin_to_pin; netlist diff proves only the 4 nets changed (+4 refs, 89->90 nets); all 4 sites visually verified in PDF crops.
- PCB: 4x 0603 staged at x=92 open column, nets assigned, U501.14 moved to CTD_U501. drc129: 179 warn (same breakdown, no courtyard hits), 0 errors, 0 parity, 33 unc (+7 new jumper nodes as expected).
- Docs: SCHEMATIC_REVIEW §11 deviation, BOM row, LAYOUT_REVIEW E53, QUESTIONS Q5-executed/Q6-in-progress. Next: Q6 partial moves first (U201/R202/C106/C203/C507/D501/D502), then route-close to 0.

## 2026-10-04 03:10 -0600 — Q6 started: SENSOR_EN plan (R114 micro-tap + Pin_4 via shift), B-side ruled out
- Micro-exit surveys (svbatch, 0.5 margin): U201.3 E-exit at y=7.8 (0.45 past TX_EN); U201.42 S-exit blocked by TX_STAT+TQs; U201.42 E-exit threads between U201.41/43 (0.77 gap, 0.65 needed) but J202-Pin_4 via (30.4,6.1) overlaps by 0.03; U201.28 sealed on F (all 4 dirs copper); U501.14 east blocked by FB/TX_STAT/SW2; B-layer TX zone sealed (EN floor + SW2/TX_STAT walls).
- Key constraints found: courtyards_overlap=ERROR forbids U201-adjacent jumpers (R114 must clear x=29.62 cyd -> site (31.3,5.605)); B-side footprints = 0 (F-only assembly, no B-side parts without owner process approval).
- SENSOR_EN plan: shift Pin_4 via (30.4,6.1)->(30.4,6.8) + extend B vertical, place R114 (31.3,5.605), stub U201.42->R114.1. CTD will need TX zone rewrite (rip U501 fanout, re-route CTD-first, no U501 move yet).

## 2026-10-04 03:45 -0600 — SENSOR_EN: N-S corridors walled on F (middle + east); trying B-side highway
- drc130 holds (32unc/0err/0parity). N-S survey x[32.5,35]: F = wall of ~15 E-W crossings (SPI/PWR/RST); B = spines (S1_MISO/MOSI/NCS, D+/D-) + ~10 E-W crossings. Threading needs 9+ ripups incl. 3 SPI (M2 risk) — rejected for now.
- B-highway plan: R114.2 -> via (33.0,4.5) -> B east y=4.5 (channel between P1.11 4.095 and TX_EN 5.1) -> B north x~82 -> B west y~88 -> via up at cluster. Only 2 vias, no SPI touched. Surveying B south/east/north now.
## 2026-10-04 03:05 UTC — Q6 SENSOR_EN highway FAILED + recovered (drc131c 32unc/0err/0parity, committed)
- P134 placed 5 B-jogs (TX_EN/Pin_4/S1_NCS/BTN3/P1.11 @x~29-31) + SENSOR_EN via (33.2,4.7)+F-stub+B-west+N-S x=29.9 to north. Audit 30/30.
- DRC131 (misread flags: no --severity-all, wrong unconn key) showed 197 "errors" incl 123 lib_footprint_mismatch WARNINGS (env/library drift, pre-existing) — real errors were mine:
  1) N-S x=29.9 crossed UNSURVEYED B copper: MCU_RST nest (y16-30), GND (25.97), P0.29 (32.86), S1_MOSI (44) — 9 shorts + 7 crossings. Root cause: corridor "clear" claim from ~8 known segs, never a full-strip survey. N-S concept at x=29.9 DEAD.
  2) B-west @4.7 crossed TX_EN jog east leg (30.6) — unchecked own-geometry crossing.
  3) Via (33.2,4.7) annular vs TX_EN 5.3-seg: 0.075 gap — d0.8 via doesn't fit P1.11/5.3-seg channel (needs d0.6 or relocate).
- rb46 ripped SENSOR_EN P134 copper but box ALSO killed pre-existing B-run (30.363,85.142-91.845) -> 33rd unconn. Restored via P135 (w0.25, verified from HEAD sexpr). drc131c: 32unc/0err/0parity = drc130 parity. COMMITTED.
- LESSONS: (a) always drc.sh (proper flags) for DRC reads; (b) FULL-strip survey before any long run; (c) rip boxes must exclude pre-existing copper (compare HEAD sexpr when rip count surprises); (d) same-net branch-0R pads (R113/114/115) self-flag as unconnected pairs — 3 DRC artifacts to disposition (copper short vs document).
- NEXT: full-strip B surveys for SENSOR_EN redesign (candidates x=27 / x=33 / east-around x=62); 5 jogs kept (proven clean, reused if corridor crosses x~30 south band).
## 2026-10-04 03:40 UTC — Plans M/Q/E dead; PLAN F (MCU_RST maze relocation) FORCED for SENSOR_EN (5f0bad7 landed, 32unc/0err)
- q6s6+q6s7 surveys killed 4 more plans: (E) east-around DEAD @TX via cluster x58-62 (TX_EN/TX_STAT vias + P1.11 pinch 0.38<0.65); over-top DEAD (VBUS_SENSE E-W @127.5 + VBUS w0.5 + D-maze); (M) F-long-run DEAD (F-strip x30.7 has TP301-304 row + SPI fanout + VBUS w0.5 + GND/MCU_RST mazes); (Q) east N-S x34.2 DEAD (join crosses USB D-/D+).
- KEY FINDING: USB D-/D+ (B N-S x31.5/32.0, y12.6-125.2) bisects board; maze-east (x30.8, y21-56) + D- leave 0.575 channel — NO x fits y[21,56]. F-feed EAST CONFIRMED CLEAR: R114.2→F-diag→d0.6 via (33.9,4.6)→B-west @4.6 (30.85-33.9, clears P134 jog legs which end x30.6!). Bmaze full map: 25 segs + 3 vias, N-S x30.745 to y56.25.
- PLAN F: relocate MCU_RST maze x-5.5 (to x[23,25.5]) + F-end reroute @16.1 + 2 N-S side-jogs (@S1_MOSI-34.225, @S2_MISO-46); then SENSOR_EN N-S x30.85 (4 east side-jogs legs31.3/32.1 + east feed + north join). ~9 waves. Maze is slow/DC (M2-exempt) — still "partial", no U201/U501 move.
- Endpoints (drc131c): SENSOR_EN closable WEST-side only (U104.3 north endpt confirmed); MCU_TX_EN north (R111.2 @47,118.675) + VBUS_SENSE north (x58-74,y123-127) are EAST-side → need USB-crossing (deferred; SENSOR_EN + CTD first, both USB-free).
- RISK OPEN: route.py len output shows 66 FAIL pairs incl S1_NCS (TP304-U201.32) — M2 length-match vs my S1_NCS jog (+0.6)?? MUST compare HEAD vs WORK S1-bus lengths next turn; revert S1_NCS jog if M2 broken. P134 jogs kept for now (0 errors).
- NEXT: (1) read bundled:git skill (pre-commit rule); (2) S1-bus lengths HEAD vs WORK; (3) PLAN F surveys (B x[22.5,25.5] y[15,31], N-S jog boxes, via F boxes); (4) execute maze move.
## 2026-10-04 04:10 UTC — RESUMED: found+reverted route.py autoroute pollution; clean redo committed fe3c2cc (drc132b = drc131c)
- SMOKING GUN: `route.py len S1_NCS` has NO len subcommand — unknown args hit `else: main()+add_zones()+stitch()+fill+SaveBoard` (route.py:1046-1053). The "length check" background job ran a FULL autoroute: +566 segs/+264 vias+zones. 5f0bad7 DRC: 18unc BUT 473 errors (187 shorts/165 crossings/101 clearance/11 hole-hole/6 length/3 thermal). NEVER run route.py as script again (import-only).
- Reverted pcb to f61c790 (drc-rev = drc129 exactly: 33/0/[]/179), redid rb44F+p133+rb45+p134+rb46+p135+R114-place. drc132b: 32unc/0err/0parity/178warn, per-net counts + SENSOR_EN pairs IDENTICAL to drc131c. Committed fe3c2cc.
- M2 DISPOSITION: S1_NCS 140.896->141.496 (+0.6, +0.4%, as designed); DRC spi_max_length(150mm) passes. route.py's 66 FAILs are pair-analysis gaps (span untouched nets), not violations. Intra-bus ±10%-of-SCLK deviation is pre-existing (f61c790: 140.9 vs 96.0 SCLK), not jog-caused. Jog KEPT.
- Surveys q6s4-q6s7 are CLEAN (all ran before router's save). sexlen.py is now the length tool (pcbnew can't load old-revision files).
- NEXT: PLAN F (MCU_RST maze x-5.5 relocation) surveys, then execute.
## 2026-10-04 04:35 UTC — PLAN F DEAD (home blocked); pivoting to PLAN C (maze compress-in-place)
- FhomeB: maze-new home x[22.7,25.175] pierced by THREE B N-S spines: +3V3 x22.63 (w0.5), P0.29 x23.34, S1_MOSI x24.898. Relocation DEAD. West-center B x[22,25.5] recorded as blocked (matters for later waves).
- PLAN C (compress): keep maze west + south via; rewrite maze-east (x>30.0, ~12 B segs) into x<=30.2; N-S 30.745->30.35; vias (30.4,29.6)->(30.2,29.6)d0.6, (30.745,30.225)->(30.35,30.225), north (30.745,56.25)->(30.35,56.25); F-N-S 30.745->30.6 (dodges S1_NCS-F x30 east 30.125 by 0.35); F E-W extend to 30.6. Corridor x=30.85 gaps 0.4/0.45. ~4 waves. Compress surveys running.
## 2026-10-04 05:15 UTC — PLAN C compress DONE, corridor x=30.85 OPEN (b02cf67, drc134 33unc/0err/0parity)
- rb47 ripped maze-east (26 obj) + N-S + 3 vias + F-N-S/F-E-W; C2a placed snake-straight + GND-via west-jog (x27.2, fixed GND-via short found by drc133) + E-W + F-diags (30.2 via d0.6). Maze-east now <=30.5 (via annular), corridor gap 0.225-0.4.
- North feed: options (E)-all-B (S1_MISO wall @52.5 + USB cross), (F)-east-B (SPI crossings), (G)-F-east (pinches), (18b)-F-x31.5 (C303/S1_NCS) ALL DEAD. North open DEFERRED (+1, documented; Q6-remainder via endpoint-move or SPI-jog). Maze group intact (2 west pre-existing + 1 north).
- SENSOR_EN south RESTRUCTURED: no B-west (TX_EN-leg conflict); via (30.85,4.6)d0.6 + F-diag to R114.2 (FdiagS clear) + N-S x=30.85 + 4 EAST side-jogs (legs 31.5/32.3) + P1.11 straight. NEXT: revert 5 P134 jogs, place P137, close SENSOR_EN.
## 2026-10-04 06:00 UTC — SENSOR_EN CLOSED (drc139 32unc/0err/0parity, committed)
- PLAN S executed: F-feed (south-run T @27.1625 + N-S x=27.1625 (0.2125 gaps) + E-W @8.085 (0.2-exact U201.39/Pin2-via) + N-S x=34.0 + stub) + via (33.9,8.6)d0.6 + B E-W @8.45 + N-S x=30.85 (wide-jog @11.8/@15.1 around D-vias) + join (30.363,85.142). Self-pair (R114 pads) remains by design.
- Killed along the way: side-jog restatements (straddle fallacy x3!), F-east-around @5.3 (FID1 0.6-keepout), N-S x=28.4 (U201.39/41 pads), E-W @8.0 (U201.39 0.115). South band stays STRAIGHT (all 5 jogs reverted, straights restored).
- Open: MCU_RST north deferred (+1). NEXT: CTD TX rewrite, then U0-U19/U27-U29 waves, 0R self-pair shorts (R113/114/115), measurements, fab/, SUMMARY.
## 2026-10-04 06:35 UTC — CTD CLOSED (drc142 30unc/0err, 6547b1d); Wave A hits 2 violations, fixing
- CTD: R515 @ (64.5,15.5) + west FB-hop (vias (58.35,15.3)/(59.65,16.0)d0.6) + east D501-hop ((65.5,15.7)/(67.15,15.85)) + GND-hop ((70.7,15.85)/(72.48,15.85)->C507.1). Fixed: C507.2-short, FB-E-W graze, U501.15-EN corner (0.197).
- Wave A: pairs 8 (MCU_RST west) + 6 (GND east) placed clean; +3V3-0 needs B-detour (S1_MOSI N-S blocks direct hop; E-W @21.2 clear pending); VIN-15 F-strap SHORTED (missed U501.21 EP 2.5x2.5 + CTS pad) -> ripped, B-strap plan; MCU_RST-8 E-W SHORTED (missed R202.1 pad) -> fixed @20.4.
PROGRESS 2026-10-04T12:04:19Z drc148 20unc/0err/0parity: B2c closed VBUS-8,VIN-13,D501-A,R115,R113,VS-east,SEN-R114; VIN-12 deferred WaveD(U501-cage); VIN w>=0.3 rule, via>=0.6/0.3
PROGRESS 2026-10-04T12:20:54Z drc158 17unc/0err/0parity: VBUS-8v4+GND-2v2+GND-4 closed; C106+0.2/C107+0.3; MCU_RST-reroute-west; WaveD=+3V3x2/VIN-12/VIN-14(sealed,doc); GND-3 WaveZ(zone-close); 7 routable remain
PROGRESS 2026-10-04T12:26:53Z drc162 17unc/0err/0parity: VS-south->WaveD(all N-S corridors sealed: x16.6/x13.1/x19.15/x14.5); B-run over-rip restored from 87cd012; WaveD=7(+3V3x2/VINx2/VBUS-S/VS-S); 5 routable(MCU_RST-N/VSEN/TX_IMON/FTH/MCU_TX_ENx2)+4 WaveC remain
PROGRESS 2026-10-04T12:29:58Z drc164 17unc/0err/0parity: TX_IMON+MCU_TX_ENx2->WaveD(all dirs sealed); WaveD=10; 3 routable(MCU_RST-N/VSEN/FTH)+4 WaveC+GND-3Z remain
2026-10-04: Q6 WaveC J202-Pin2 CLOSED (17->16): B-N-S pad-exit + E-W @20.5 + N-S x=13.8 + VSEN-via (14.23,17.51) bypass (x=13.0 legs) + via (12.2,9.45) island-join + via (9.95,19.7) SMD-pad join (19.9->19.7 Pin4-clearance fix). drc168 16unc/0err/0parity. COMMIT.
2026-10-04: Q6 WaveC P0.12 FAILED->WaveD: F-E-W @14.4 closed net (16->15) but hit U201-28 mask-bridge + C205-1 vbus 0.025; dip-jogs hit U201-30 TX_EN SHORT + D--via SPI 0.04; all dips sealed (U201 pad-forest + TX_EN/D-/D+/S1_NCS). Ripped 10 segs, drc171 16unc/0err/0parity. COMMIT.
2026-10-04: Q6 WaveC S2_MOT FAILED->WaveD: F @8.6 SHORTED U201-37/via/E-W (J202-island) + C504-1 + SPI-0.6 (S1_MISO/MOT); deep @5.2 SHORTED R114/U201-42 + FID1-0.6 + TX_STAT; under-TX @2.2 needs B-hop CROSSED by GND/TX_EN/P1.11-E-Ws. Ripped net-zero, drc174 16unc/0err/0parity.
2026-10-04: Q6 WaveC FTH FAILED->WaveD: B-route closed net (16->15) but via-on-U501.9-pad hit TX_STAT/hole + B-spine crossed GND-B; fix via (55.5,17.2) SHORTED U501-21-GND-EP + NTC-via + TX_STAT-via. FTH-pad caged (U501-8/10/21 + TX_STAT-E-W). Ripped net-zero, drc177 16unc/0err/0parity.
2026-10-04: WaveC COMPLETE: J202-Pin2 CLOSED (17->16). 7 nets ->WaveD (MCU_RST-north, VIN-8, P0.12, S2_MOT, MCU_RST-west, VSEN, VIN-east, FTH). WaveD=15 (+3V3x2, MCU_RSTx2, VBUS, VSEN, TX_IMON, VINx2, FTH, MCU_TX_ENx2, VBUS_SENSE, P0.12, S2_MOT) + WaveZ GND-3. Micro-routes provably fail for all 15; destructive re-place authorized (Q6) is next.
2026-10-04: WaveD micro-angles x4 ALL SEALED (board untouched, drc177 16unc/0err/0parity stands): S2_MOT-B @7.5 (BTN3-E-W/diag/via + S1_NCS-N-S/E-W sandwich, N+S jogs both sealed); P0.12-B @9.6 (J202-E-W/via + SENSOR_EN + BTN3-diag/E-W + S1_MOT-diag/via + F-BTN3/S1_SCK); MCU_RST-west-B (J202-maze/Pin4 + BTN2/VSEN/BTN1/S2_NCS N-Ss + +3V3); VIN-8/CTS-reroute (GND-N-S/via + TX_IMON + IS+-diag; west bypass independently sealed by GND-via (51.47,15.0)). NEXT: zone-redo phase (Q6): (1) south-band y[4,18] x[21,44] rip+coherent re-route (P0.12/S2_MOT/TX_IMON-w); (2) U501-TX zone (VIN-8/9/FTH); (3) N-S spines (MCU_RST-n/VBUS/VSEN/MCU_TX_EN/VBUS_SENSE); (4) WaveZ GND-3; then 0R shorts/zones/measure/fab/SUMMARY.
2026-10-04: ZONE-1 south-band SEALED (drc179 16/0/0 net-zero): P0.12-north-dip closed net (16->15) but 6 DRC errors — east-leg sealed (U201-28/U201-27-vbus 0.125 corridor), SPI-intra-0.6 vs S2_MOSI (P0.12 is SPI-netclass!), D--via-dip sealed (via-SPI/VBUS-vbus sandwich); S2_MOSI-reroute (for S2_MOT lane) sealed by GND-maze (E-W @17.65 + N-S x=23.9 spanning to y24.6). Ripped net-zero. ZONE-2 START: TX_STAT-rip+reroute@20.0 opens FTH north lane.
2026-10-04: ZONE-2 U501-TX SEALED (drc179 16/0/0): FTH-double-rip analyzed (TX_STAT-E-W@18.94 + FB-N-S walls full-height; reroutes re-cross; 5-net cascade needed); VIN-9/D502-west sealed (FB: D501-A+CTD inverted + SW2-via+D501-A inverted corridors; VIN-east bus re-feed 16mm); VIN-8 deferred (needs U501-move). §7.9 written. NEXT: Zone-3 N-S spines.
2026-10-04: ZONE-3 partial: VBUS-5 (+3V3-1, MCU_TX_EN-12 sealed w/ evidence (F/B column deaths, N-S forests, Q101/TX_ON/GND/VBUS mazes); U501/U201-move assessed NOT-RECOMMENDED (own-pad cages persist, 15-30 net breaks, ~2 turns uncertain). §7.10 written. NEXT TURN: freerouting oracle-as-advisor on drc179 copy for 16 opens, then hand-place + verify.
2026-10-04: ORACLE launched: /tmp/oracle/board.dsn exported from drc179 copy (pcbnew.ExportSpecctraDSN); freerouting-2.4.1 + Temurin JRE25 running -mp 30 under xvfb (background). Prep: /tmp/ses_diff.py SES->corridor parser validated on fr1 SES (scale /10000 confirmed vs known +3V3). Meanwhile: +3V3-0 B-side sealed (P0.29 full-height wall). Next: parse oracle corridors for 16 opens, survey-verify, hand-place + DRC each.
2026-10-04: ORACLE-1 TX_IMON CLOSED (16->15): hand-placed oracle corridor w/ 3 deviations (via (19.23,7.82)->(18.9,8.0) TX_EN-via touch; via (20.61,4.6)->(20.8,4.6) TX_EN-via touch; N-S x=39.65->39.55 R207.2/S1_SCK corridor) + 6 DRC180 fixes (P0.29-via gap, S1_SCK-N-S x=40.0, U201-11/12 corridor @17.66). drc181 15unc/0err/0parity. COMMIT.
2026-10-04: ORACLE-2 MCU_RST-north CLOSED (15->14): oracle corridor verbatim (F-N-S x=34.97 to via (34.97,40.61) + B-N-S x=36.0 to via (35.82,52.23) + F-diag/N-S x=30.91 + join existing via (34.47,72.6)), 5 surveys all clear, ZERO deviations, first-try clean. drc182 14unc/0err/0parity. COMMIT.

## 2026-10-04 00:00 UTC — Oracle hand-places 2/3: TX_IMON + MCU_RST-north CLOSED (drc182: 14unc/0err/0parity). S2_MOT oracle corridor (@7.53) violates SPI-intra-0.6 on COPY (needs B@7.15/track_width fix per DRC) — alternatives @5.5/@6.0/@6.5 surveyed SEALED (J202-Pin4-E-W @6.00 + S1_NCS-E-W @6.85 sandwich: every drop crosses J202 or R114-1/J202-N-S). Oracle-2 (-mp 100) launched in background on fresh copy. Next: hand-place S2_MOT only if oracle-2 finds SPI-clean corridor; else drill remaining opens (VBUS/VIN/FTH/MCU_TX_EN/VBUS_SENSE/P0.12/+3V3s/MCU_RST-w/VSEN/GND-3) via advisor corridors or new hand surveys.

## 2026-10-04 00:30 UTC — Zone-lock survey: VIN-#7 (pin-caged, EP wall), +3V3-#1 (GND ladder), GND-#3 (VBUS cage, 6 sides), +3V3-#2 (GND maze + 4-spine wall), S2_MOT (SPI-0.6 sandwich) all proven SEALED with measurements. §7.10.3 committed. Oracle-2 (-mp 100) still running in background; will hand-place only SPI-clean verified corridors on wake. If oracle-2 fails: Q6 destructive zone rework (owner-authorized).

## 2026-10-04 01:00 UTC — Zone-lock survey complete: 9/14 opens proven SEALED this turn (VSEN sensor-field, MCU_RST-w Y201+5-spine, VIN-#8 SW2/FB+TX_EN, P0.12 VBUS/S2_MOSI-inverted). Other 5 sealed in prior waves. 14/14 zone-locked. §7.10.4 committed. Oracle-2 still running; on wake: hand-place SPI-clean corridors or begin Q6 destructive zone rework.

## 2026-10-04 02:00 UTC — Oracle-2: 0/14 closed, advisor exhausted. S1_NCS-relocation attempt FAILED drc183 (15unc + SHORT/clearance/crossing/length errors, 6 root causes incl. wrong 0.125 clearance assumption — Default is 0.2mm) and was reverted net-zero to tag q6-zone-rework-base; drc184 confirms 14/0/0. S2_MOT needs full south-band coherent re-route. §7.10.5 committed.

## 2026-10-04 03:00 UTC — S2_MOT partials EXHAUSTED (§7.10.6): J202-north (landing occupied), Pin_4-east (S1_NCS-keystone via-block), north-around (U201-38 B-cage + 3-spine @10.40), U201-38 F-exits (SENSOR_EN corner/module/J202-shadow), S1_NCS-south/F-swap (length+crossing). Keystone S1_NCS-E-W @6.85 fully locked (position+length). FULL south-band rip + coherent re-route justified and planned (preserve spines+TX_IMON+islands; rip E-W band+fanouts). Next turn executes rip checkpoint.

## 2026-10-04 03:30 UTC — RIP CHECKPOINT drc185 22unc/0err/0parity: /tmp/rip.py removed 65 (S1_NCS-keystone, Pin_2, Pin_4, BTN3-west, P0.12-west, S2_MOSI-south); spines/TX_IMON/islands/anchors preserved; zero real errors. §7.10.7 committed. Next: survey emptied band, lane-ordered re-route S2_MOT-west first.

## 2026-10-04 04:00 UTC — RIP REVERTED drc186 14/0/0 (§7.10.8): post-rip lane design proved triple mutual exclusion (S1_NCS-@6.85 + Pin_4-rise + S2_MOT-lane; R114 immovable SENSOR_EN-series; 14 S2_MOT lane-proofs). Reverted net-zero to ef13502. S2_MOT stays OPEN by proof. Next: closable opens each with own lane design (P0.12-west, Pin_2, BTN3-west, S2_MOSI-south first — pre-rip surveys stand).

## 2026-10-04 04:30 UTC — BLOCKED (Q7): P0.12-north final proof (hop-1/hop-2/S2_MOSI-immovable); 0Rs verified (R113/114/115 self-pair, R515 series closed). 14/14 opens sealed (ledger §7.10.9); Q6 moves can't break package-cages; oracle exhausted. Need schematic pin-reassignment ECO (or via-in-pad/stackup/accept-opens decision). Board held 14/0/0. QUESTIONS.md Q7 filed.

## 2026-10-05 05:00 UTC — Q7 ECO START (owner-approved 10-05). Pre-ECO checkpoint = HEAD 00049b9 (14unc/0err/0parity, clean tree). Plan: (1) inventory U201/U501 pins+nets, find free GPIOs; (2) lane-verify candidates; (3) swap table; (4) edit sheets + board pads sync; (5) ERC 0err; (6) SCHEMATIC_REVIEW deviation + PINMAP.md; (7) route freed lanes per wave.

## 2026-10-05 05:30 UTC — Q7 triage verdict (§7.10.10 + PINMAP.md): ZERO pin swaps applicable (mid-route gaps / no better pin / power pins); TP205-move SHORTED twice (J202-8, R202-1/J202-4/6) then proven immovable by exact courtyards (reverted net-zero); R505-move dead (TX_STAT-wall/courts/EP). MCU_RST-w + FTH stay OPEN by proof. NEXT: R111/MCU_TX_EN-north greenfield + VIN-#7 electrical escalation answer.

## 2026-10-05 06:00 UTC — TP205/R505 post-mortem CLOSED: both move attempts reverted net-zero (TP205 SHORTED J202-8 then R202-1/J202-4/6; exact courtyards prove immovable); board restored byte-exact to triage state (tree clean, 14/0/0 by transitivity to drc186). Procedure fix recorded (pad+courtyard surveys). NEXT: R111/MCU_TX_EN-north greenfield + VIN-#7 electrical escalation.

## 2026-10-05 06:30 UTC — MCU_TX_EN greenfield DEAD (§7.10.11): N-S x=20.10 empty to y=75 then BTN1/GND/VBUS walls; every east-join dies (TX_ON-tip/U105/TX_5V_SW/GND-@120/GND-N-S); LEG-B needs via-in-pad. R111 GND-caged. Q7 CLOSE-OUT: 0 swaps + 0 moves viable; VIN-#7 DNC electrical call outstanding. Board untouched 14/0/0.

## 2026-10-05 07:00 UTC — VIN-#7 verdict (§7.10.12): U501-3 DNC REJECTED (5 W bridge, 4 VINs share ~2 A; unroutable at all widths). Q7 outcome filed: 0 swaps/0 moves viable, narrowed ask (via-in-pad/stackup/accept). Fab/SUMMARY held. Board 14/0/0 clean.

## 2026-10-05 08:00 UTC — Q7 RESOLVED: go 4L (owner 10-05). Pre-stackup checkpoint = HEAD 9e35549 (14/0/0 clean). Plan: (1) 4L 1.6mm stackup edit (L1 sig/L2 GND/L3 sig+pwr/L4 sig); (2) DRC on new stackup; (3) inner-escape waves (VIN-#7 + S2_MOT first); (4) fab regen 4L at 0 unc.

## 2026-10-05 08:30 UTC — 4L live drc189 14/0/0; Wave-1: VIN-#7 placed-then-ripped (TX_IMON-riser sandwich), S2_MOT west-via dead everywhere (BTN3-@7.96 immovable), P0.12 placed-then-ripped (S2_MOSI-pad/spine/GND/MCU_RST walls). drc193 14/0/0 net-zero. §7.10.13 + binding survey procedure. Next: remaining 9 waves w/ pad+courtyard discipline.

## 2026-10-05 09:00 UTC — Wave-2 net-zero drc195 14/0/0 (§7.10.14): FTH dead (pad-row/TX_STAT sandwich); VBUS v1 placed-then-ripped (U201-28-pad, vbus_min_width 0.5, vbus_clearance 0.25, narrow windows), v2 dead (U201-26-pad/SEN sandwich). Rules learned: vbus 0.5/0.25, windows+1.0, pad-dump mandatory. Next: VSEN/VIN-#8/MCU_TX_EN/VBUS_SENSE/MCU_RST-w/+3V3s/GND-3.

## 2026-10-05 09:30 UTC — Wave-3 VSEN CLOSED drc198 13/0/0 (§7.10.15): In2 @63.50 U301-4->U302-4 (hole_to_hole + GND-via field dodged, 2 iterations). First 4L close committed. Next: VIN-#8/MCU_TX_EN/VBUS_SENSE/MCU_RST-w/+3V3s/GND-3.

## 2026-10-05 16:00 UTC — Wave-4a VBUS_SENSE CLOSED drc205 12/0/0 (§7.10.16): F-stub east + via (17.50,7.51) + In2 slalom x16.50 w/ BTN2-bypass jog; 2 placed-then-ripped iterations (F-staircase 8err, x17.50 N-S 2 shorts). Committed 2b2be0f. Next: VIN-#8/MCU_TX_EN/MCU_RST-w/+3V3s/GND-3/VBUS/VIN/FTH/P0.12/S2_MOT.

## 2026-10-05 16:40 UTC — Wave-4b VIN-#8 east link placed (11unc drc206) then RIPPED on L501-2 short (containment-lesson §7.10.17); wall complete on In2 (6 proofs), grand-tour plan set; drc207 12/0/0 net-zero, no board commit (byte-identical revert). Next: grand-tour probes, then MCU_TX_EN/MCU_RST-w/+3V3s/GND-3/VBUS/FTH/P0.12/S2_MOT/pad3.

## 2026-10-05 17:10 UTC — Wave-4b VIN B-C CLOSED via grand tour drc208 11/0/0 (§7.10.18): 6-seg In2 x55/x40/@4.00/x73.49, 0 errors, all reload-verified. VIN remainder = pad3 micro-wave. Committed board. Next: MCU_TX_ENx2/MCU_RST-w/+3V3s/GND-3/VBUS/FTH/P0.12/S2_MOT/pad3.

## 2026-10-05 17:40 UTC — Wave-4c MCU_TX_EN surveyed (§7.10.19): F-escape route solved on paper (jog around P0.12 tip, via (20.30,16.65)), long-link options triaged; placement + south surveys next. Tree clean drc208 11/0/0.

## 2026-10-05 18:20 UTC — Wave-4c MCU_TX_EN CLOSED drc211 9/0/0 (§7.10.20): linkA (F-escape v3 + N-S x24.60 + via-in-pad (47.00,119.30)) + linkB (@119.10 + riser x91.175 + via-in-pad R115-1); v1 via shorted S1_MOSI-B-rail (truncated-probe lesson). Committed board. Next: +3V3s/GND/MCU_RST/VBUS/FTH/P0.12/S2_MOT/pad3.

## 2026-10-05 19:30 UTC — Wave-5 +3V3 gap-b CLOSED, gap-a PARKED-SEALED drc222 8/0/0 (§7.10.21): 5 failed placements, GND-rail ECO rejected (load-bearing, reverted byte-exact). Committed board. Next: GND (tiny B-gap) / MCU_RST / VBUS / FTH / P0.12 / S2_MOT / pad3.

## 2026-10-05 20:10 UTC — Wave-6 GND CLOSED drc225 7/0/0 (§7.10.22): In2 direct reusing GND vias; B-arounds dead (VBUS rail tip higher than surveyed + J201-SH). Committed board. Next: MCU_RST/VBUS/FTH/P0.12/S2_MOT/pad3/gap-a.

## 2026-10-05 20:40 UTC — Wave-7 FTH PARKED-SEALED (§7.10.23, no board change): U501-9 pad-caged all sides, no via slot; far-island via clear but unreachable. Next: MCU_RST/VBUS/P0.12/S2_MOT/pad3 surveys.

## 2026-10-05 21:20 UTC — Wave-8 MCU_RST CLOSED drc230 6/0/0 (§7.10.24): existing-via + hop over SENSE-spine + F-step to maze; 3 iterations. Committed board. Next: VBUS/P0.12/S2_MOT/pad3/gap-a.

## 2026-10-05 22:00 UTC — Wave-9 VBUS CLOSED drc234 5/0/0 (§7.10.25): C205-1 via + 90mm In2 N-S x31.50 (+3V3-tip jog) + @105.50 transition; 3 iterations. Committed board. Next: P0.12/S2_MOT surveys, pad3/gap-a/FTH sealed batch.

## 2026-10-05 22:30 UTC — Wave-10 P0.12 CLOSED first-try drc235 4/0/0 (§7.10.26): B-bottom via + In2 @7.75 + x39.30 + R207-2 step. Committed board. Next: S2_MOT survey; sealed batch (gap-a/pad3/FTH) escalation.

## 2026-10-05 22:50 UTC — Wave-11 S2_MOT PARKED-SEALED (§7.10.27); SEALED BATCH §7.10.28 (4 opens need schematic relief: gap-a/pad3/FTH/S2_MOT). No board change. Stopping for owner on schematic-intent per standing orders.

## 2026-10-05 23:05 UTC — Wave-11 S2_MOT PARKED-SEALED (§7.10.27: F-cage + B-mined + via-in-pad killed by BTN3-B). SEALED BATCH = 4 opens (gap-a/pad3/FTH/S2_MOT) needs schematic relief. No board change. STOPPING for owner per standing orders (schematic-intent only).

## 2026-10-06 00:10 UTC — Wave-12 relief (1) +3V3-gap-a BLOCKED (§7.10.29): In2-hop placed-then-ripped (TX_EN-spine crossing + annular convention); exhaustive relocation/re-feed search proves placement ECO has no geometry (pinch bands inverted, south maze rail-fed-only, circular re-feed). Needs schematic tie (unauthorized). No board change. Next: relief (2) VIN-pad3 CTS re-route.

## 2026-10-06 00:35 UTC — Wave-12 relief (2) VIN-pad3 BLOCKED (§7.10.30): 0.26 pad2/pad3 sandwich arithmetically seals all approaches (max w0.1 zero-margin rejected); CTS re-route proven irrelevant (blockers are pad bodies + thermal). Needs VIN-off-pin-3 (unauthorized). No board change. Next: relief (3) FTH TX_STAT move.

## 2026-10-06 01:05 UTC — Wave-12 relief (3) FTH BLOCKED (§7.10.31): TX_STAT rail cannot vacate (pad8 stranded — no via site, DTH/GND pinch inverts all N-S; FTH S-exit walled by rail/hug/pad10; east via clear but needs DNC-pad10). Needs FTH-off-pin-9 or DNC ruling (unauthorized). No board change. Next: relief (4) S2_MOT SENSOR_EN/BTN3 ripple.

## 2026-10-06 01:30 UTC — Wave-12 relief (4) S2_MOT BLOCKED (§7.10.32): SENSOR_EN-rail Y load-bearing (S/maze, N/worse); BTN3-B boxed N+S (inverted bands); BTN3-via move futile (S1_MISO wall behind). All 4 reliefs exhausted at placement level — remaining paths all schematic-intent. No board change. STOPPING for owner.

## 2026-10-06 02:00 UTC — WaveZ fab-prep docs §7.10.33 (copper read-only): 4L stackup record (L2/In1 empty, 9 nets L3; no Z-rules; order notes), via-in-pad tent/plug + R111 wicking note (overlap verified), VIN w0.30 census + widen-later PI note, Q5 jumper-ECO record (ERC re-verified 0/1-benign). Docs only.

## 2026-10-06 03:00 UTC — Wave-13 +3V3-gap-a CLOSED drc240 3/0/0 (§7.10.34): rail-move proven futile (re-feed independent of S2_MISO) + jumper proven unplaceable (no standard footprint straddles); closed via L2/In1 hop (existing west via + In1 segs + east via (27.90,20.45) + F-ext). v1 ripped on same-net hole_to_hole (lesson recorded). Committed board. Next: (2) VIN-pad3 U501 nudge.
