# BASE PCB Layout Review — trackball-base

**Branch:** `job/trackball-base-layout` · **Checkpoint:** drc127 (unc26/0err/0parity; TP305/306 ECO + U2 closed; was drc126 unc27) + §9 stage-1 Blender-manual review
**Date:** 2026-10-01, resumed 2026-10-03 (owner Q1–Q4 approved) · **Tools:** KiCad 10.0.6, Blender 5.2.2 LTS, Python 3.12.3, freerouting 2.4.1 (headless, JRE 25)
**Status:** BLOCKED Q5/Q6 (schematic-ECO 4 pads + placement-ECO decision) — see `notes/QUESTIONS.md`
**Spec:** `docs/FINAL_SPEC.md` Rev 3.1 · **Rules:** `trackball-drc/RULES.md` (normative)

> Every DRC-governed choice cites a rule ID. Unmeasured electrical/performance
> values are flagged PROVISIONAL — never stated as fact.

---

## 1. Overview

2-layer 1.6 mm FR-4 BASE board for a custom capacitive-trackball mouse,
laid out forward from schematic branch `job/trackball-base-schematic`
(`bd54638`) without schematic changes (ECO E13.2 excepted, §6).

| Item | Value |
|---|---|
| Footprints placed | 155 |
| Courtyard violations | 0 (after ECOs, §6) |
| ERC | 1 benign `pin_to_pin` (documented in SCHEMATIC_REVIEW) |
| DRC (drc127, `--schematic-parity`) | **0 errors**, 0 parity |
| Unconnected | 26 (documented blockers, §7; was 27 at drc126, 57 at drc143) |
| Stackup | 2L FR-4 1.6 mm, TOP signals + power, BB signals + power |
| GND | 0 zones in file (F9-1 §9); GND = track stitching only (pour = intent, KICAD-019) |
| Assembly | JLCPCB SMT except 2× PMW3360 (hand-solder) |

**Routing status is PARTIAL.** §7 lists every open net with root cause.
The board is electrically incomplete but DRC-clean on all placed copper.

---

## 2. Placement

### 2.1 Sensors — 2× PMW3360DM-T2QU (SENSOR_SELECTION.md)

Custom DIP footprint (`trackball.pretty`), polar 110°, rotation 80–100°
(target 90°) per MECH layout plan. Both sensors on TOP, lens apertures
facing the ball socket keepout. Sensors are the ONLY hand-solder parts;
all other SMT is JLCPCB-placeable standard packages (no fantasy parts).

- U301 (S1) + U302 (S2): PTH pads double as BB access (no via needed).
- Decoupling: C301/C302 (S1 VDDPIX), C308/C309 (S2 VDDPIX) adjacent.
- Crystal pocket: Y201 + C201/C202 + R201/R202 + TP206 placed clear of
  J202 courtyard after ECO-CRYSTAL (§6).

### 2.2 Buttons — 3× D2FC (MECH-049, SCROLL_UX_DESIGN.md)

L/R + front-center scroll (D2FC plunger-side assumed — PROVISIONAL,
flagged for MECH review). SW401 (GND PTH) + SW40x signal routing open (§7).

### 2.3 USB-C — J201 + U202 ESD (ELEC-004/005/006)

J201 hybrid shell footprint (NOT mid-mount — deviation vs MECH-006, §6).
U202 TVS array <5 mm from connector shell (ELEC-006).
USB90: D+/D− 0.25/0.20 mm provisional GCPW (KICAD-019/020 — PROVISIONAL,
bench TBD). CC1/CC2, SBU, VBUS fanout placed; VBUS tree partial (§7).

### 2.4 RF — E73-2G4M08S1C + antenna keepout (REAR)

E73 module on REAR (opposite USB-C FRONT); antenna-edge strip
measured clear on both layers (planar census §9.6 — first actual
measurement; prior "verified by script" had no supporting evidence).
No zones exist (F9-1), so "poured clear" was intent, not copper.

### 2.5 Wireless TX — LTC4125 (U501) + annular coil interface

U501 QFN-20 0.5 mm pitch (E-side). Coil interface L501 (PTH 3×3 mm ×2)
+ D501/D502 + R512 + C50x/R50x passives. COILFAN nets (E26): SW1_LTX,
SW2, FTH, DTH — 0.3 mm floor, trunks 1.0 mm via AUTO_W. TX zone is
densely caged; U501 fanout is the #1 routing blocker (§7).

### 2.6 Power tree — U101/U104/U105/U106/U107 + Q101

- U101 AP2112K-3.3 (SOT-23-5): VBUS→+3V3. EN (pin 3) tied to VIN (pin 1)
  externally — OPEN, caged (§7). PROVISIONAL startup assumption.
- U104: VSEN_1V9 LDO. U105: TX_5V_SW. U106/U107: comparators (UV/OV).
- Q101: TX_ON switch. R101/R102: VBUS_SENSE divider.
- C115 (VBUS cap for U107): placed at (59.0, 109.5) rot180 via
  keepout-surveyed ECO-C115 v4 (courtyard + copper scan, 393 free sites;
  nearest 4.6 mm from U107.6). U107 NOT moved per owner Q2. C115.1/C115.2
  stubs routed by freerouting (§3).
- U101 EN (pin 3) tied to VIN (pin 1) externally per AP2112K standard use:
  GND via moved (66.12,124.5)→(65.0,124.5) + N@67.0 w0.5 wire (ECO-U101-VIA,
  deviation E51 §6; layout-only, NO schematic change per owner Q3).

### 2.7 ECO moves (all DRC-verified post-move)

| ECO | Move | Reason |
|---|---|---|
| ECO-CRYSTAL | Y201/C201/C202/R201/R202/TP206 row y=24.6, C201 rot90, R201 (13.9,27.3) | Clear J202 courtyard + crystal shorts |
| ECO-VBUS2 | R203→(40.0,120.0), TP101→(50.0,127.3) | Open CC1/VBUS corridor |
| ECO-C115 v1/v2/v3 | Attempted (58.5,115.0) → (63.5,112.0) → (61.7,116.0); PARKED (46.0,108.0) | Collided U107/Q101/R109; no site |
| ECO-TP204 | TP204→(10.8,14.0) | Open J202-Pin_2 east corridor |
| ECO-C115 v4 | C115→(59.0,109.5) (was parked 46.0,108.0) | Keepout-surveyed site (Q2) |
| ECO-U101-VIA | GND via (66.12,124.5)→(65.0,124.5) | Open U101 EN tie corridor (Q3, E51) |
| ECO-R207 | R207 (37,17.3)→(38,17.3) + S2_SCK stub extend + GND via→(36.4,16.26) | U201-E spread (Q1) |
| ECO-C509 | C509 (66,18)→(63,18), D501-A stub ripped | TX-S spread, SW2 gap 10.3→7.3 (Q1) |
| RIP-U501S | VIN south bus + west box + east staircase, IS+ staircase ripped | U501-S copper spread for autorouter (Q1) |

Silk: Values hidden, chip/H/FID refdes hidden, `zone_connect 2` on power
parts (KICAD-022 recipe, CLR_PAD 0.2, gap/spoke 0.2).

---

## 3. Routing

Router: scripted TOP-first + BB (`/tmp/route.py` E23–E49, `/tmp/heal*.py`,
`/tmp/astar.py`, `/tmp/hand.py`, `/tmp/raw.py`). Order USB→SPI→wide→
signals (E35); phased phase-1 USB+SPI (E37). Alternate layer-first (E23).

| Class | Width / clearance | Rule |
|---|---|---|
| USB90 D+/D− | 0.25/0.20 mm GCPW (PROVISIONAL) | KICAD-019/020 |
| POWER (VBUS/VIN/+3V3) | 0.5 mm | ELEC-027 exempt U501 |
| VIN→VINPWR | 0.3 mm floor | E19 |
| COILFAN (SW1_LTX/SW2/FTH/DTH) | 0.3 mm floor, trunks 1.0 | E26 |
| SPI intra (Track-vs-Track only) | 0.6 mm | E43 |
| SPI-to-coil | 5.0 mm | ELEC-029 |
| U201 keepout | 20 mm | — |
| Edge-to-coil | 3.0 mm | ELEC-029 |
| Base CLR (vias/pads/signals) | 0.2 mm | — |
| VBUS intra-connector + VINPWR | exempt | vbus_clearance 0.25 |

- Same-net via/track merge exempt; via-via hole_to_hole only (E27).
- Same-net pad touch = merge (E28).
- DRC length = track total + 1.6 mm/via (verified on 3 nets).
- P0.13/NCS channel swap: NCS ripped + rerouted west-BB after NCS@12.0
  sealed U201-33 (0.6 track-track); P0.13 took FT channel.
- S1_MOSI 200 mm → 99 mm, S2_NCS 175 mm → ~140 mm after rip-up +
  tighten (ELEC-012 150 mm budget — PROVISIONAL, length TBD on closers).

GND: 0 zones in file (F9-1 §9) — track stitching only; pour is
post-Q5/Q6 route-close work.
VBUS: power tree + U101-EN tied (E51).

### 3.1 Autorouter (freerouting.org, owner Q1)

Remaining singles/pours routed with freerouting 2.4.1 headless
(`--gui.enabled=false -mp 50 -mt 7`) via `pcbnew.ExportSpecctraDSN` /
`ImportSpecctraSES` (KiCad 10 `kicad-cli` has no Specctra path; needs
JRE 25 — Temurin used). Pre-route prep: ECO batch 1 (above) + copper
cleanup (zero-length + exact-duplicate removal, DRC-verified unchanged).
Hand-placed critical copper (USB90, SPI, coil, power trunks) exported as
fixed wiring and preserved. Post-import: full `--schematic-parity` DRC +
hand-fix of any DRU delta (freerouting honors DSN netclass width/clear
only, not `trackball.kicad_dru` custom rules) — deviation E52 §6.

---

## 4. Scripted measurements

> Run BEFORE final sign-off. Record actuals here; flag PROVISIONAL.

| # | Check | Method | Result |
|---|---|---|---|
| M1 | USB D+/D− skew <0.5 mm | `usb_tune.py` post-route audit | OPEN — split per E14, audit pending close |
| M2 | USB90 width/gap | caliper on Gerber | PROVISIONAL stackup (KICAD-019/020) |
| M3 | SPI lengths ≤150 mm | DRC length + 1.6/via | S1_MOSI 99, S2_NCS ~140 (PROVISIONAL) |
| M4 | Antenna keepout clear | `check_antenna_keepout.py` (MISSING — §9.6 manual planar census instead) | MANUAL-PLANAR-ONLY (RF-022 volumetric needs enclosure CAD) |
| M5 | Coil keepouts (5 mm / 0.8 mm) | `check_coil_keepouts.py` (MISSING — §9.5 manual partial) | MANUAL-PARTIAL (coil geometry PROVISIONAL/off-board) |
| M6 | Sensor geometry 80–100° | `check_sensor_geometry.py` (MISSING — §9.2 manual XY only) | MANUAL-XY-ONLY (angle/Z need ball datum) |
| M7 | Ball socket / base stability | `check_ball_socket.py`, `check_base_stability.py` (MISSING) | NOT RUNNABLE (enclosure CAD absent) |
| M8 | Buttons + USB placement | `check_buttons_usb.py` (MISSING — §9.3/9.4 manual partial) | MANUAL-PARTIAL (ELEC-006 3.99 ✓; enclosure items open) |
| M9 | Courtyards 0 overlap | DRC `courtyards_overlap` | 0 (drc126) |
| M10 | Holes 0 violation | DRC `hole_*` | 0 (drc126; drc125 hole_to_hole FIXED P130) |
| M11 | ERC clean | `kicad-cli sch erc` | 1 benign pin_to_pin |
| M12 | Schematic parity | `pcb drc --schematic-parity` | 0 (drc126) |

---

## 5. DRC evidence (drc127)

```
viol: lib_footprint_mismatch 123, track_dangling 49, via_dangling 3,
      holes_co_located 2, silk_edge_clearance 2
unc: 26 (+3V3 2, GND 5, MCU_RST 2, VBUS 3, VSEN_1V9 1, TX_IMON 1,
      VIN 3, FTH 1, D501-A 1, MCU_TX_EN 1, VBUS_SENSE 1,
      SENSOR_EN 1, CTD 1, J202-Pin_2 1, P0.12 1, S2_MOT 1)
real violations: 0    parity: 0
```

- `lib_footprint_mismatch` 123: expected — custom footprints differ from
  library (KICAD-013 `missing_courtyard` handled per rule).
- `track_dangling` 49 / `via_dangling` 3: open stubs on unrouted nets (§7).
- `holes_co_located` 2: accepted (intentional stacked vias, no fab risk).
- `silk_edge_clearance` 2: accepted (silk clipped at edge, no fab risk).
- Full JSON: `/tmp/resume_drc127.json` (job archive).
- Progress drc143→drc127: 57→26 unconnected (−31) via P6–P131
  (survey-verified hand routes + T-junction workarounds + ripup-reverts
  + TP305/306 ECO4 + U2 east loop).
- Independent corroboration: freerouting.org 2.4.1 headless (JRE 25,
  50-pass budget) stuck at 73 unrouted, score frozen 716.45 across
  passes 2–4 — autorouter agrees remaining cages hold.

---

## 6. Deviations requiring sign-off

| ID | Deviation | Rationale |
|---|---|---|
| E13.2 | Verbatim netlabels (`/mcu/`, `/tx/`, `{slash}`) | Net-aware DRC |
| E14 | USB skew split (audit post-route) | Tuning profiles carry delay |
| E19 | VIN→VINPWR 0.3 mm floor | U501 0.5 mm pitch fanout |
| E26 | COILFAN 0.3 mm floor, trunks 1.0 | Coil current (PROVISIONAL bench) |
| E27/E28 | Same-net merge exempts | Standard practice |
| E29–E49 | Router candidate upgrades (see devlog) | Convergence (E43–E49 DRU-relevant) |
| MECH-006 | J201 not mid-mount | Footprint availability |
| KICAD-011 | Annular 0.2 mm | Density |
| U202 | 0.15 mm geometry | Package |
| ELEC-006 | No SPI TVS | Gap — ESD L4 PROVISIONAL |
| CLR 0.2 | Base clearance spans | Density |
| E51 | U101 EN tie via GND-via micro-move (layout-only) | See DEVIATION E51 below |
| E52 | freerouting autorouter for singles/pours | See DEVIATION E52 below |
| E53 | Q5 schematic ECO: 4× 0R jumpers (R113/114/115/515) on pad-caged nets | Owner-approved 2026-10-04; see SCHEMATIC_REVIEW §11 |

### 6.1 DEVIATION E51 — U101 EN tie via GND-via micro-move (documented, owner Q3)

AP2112K-3.3 EN (U101.3) must be tied to VIN (U101.1) for always-on use.
The as-placed corridor was caged (U101.2 GND pad + GND via at
(66.12,124.5)): no 0.5 mm path passed DRC.
Justification for accepting the deviation:
- Layout-only change: GND via moved (66.12,124.5)→(65.0,124.5), GND web
  reconnected (FT L + BB-E), EN tied via N@67.0 w0.5 + W stubs.
  NO schematic change (owner Q3 explicitly forbids it).
- DRC-verified: 0 errors, U101.1↔U101.3 closed, GND whole (C101.2 link
  restored around C101.1).
- Electrical intent unchanged: same two-pin tie the schematic specifies.

### 6.2 DEVIATION E52 — freerouting autorouter for remaining copper (documented, owner Q1)

Hand/scripted routing stalled at 57 unconnected (QFN fanout + dense BB,
documented §7 of prior rev). Owner approved freerouting.org.
Justification for accepting the deviation:
- Critical hand copper (USB90, SPI lengths, coil, power trunks) kept as
  fixed wiring; autorouter closes only the remainder.
- Freerouting honors DSN netclass width/clearance, NOT custom DRU rules
  (E43 SPI-intra, E19/E26 floors, vbus_clearance): every SES import is
  followed by full `--schematic-parity` DRC and hand-fix of deltas.
- Net lengths re-audited post-import (ELEC-012); USB skew audit per E14.

Provisionals (bench TBD before fab money): tank Vpk, coil current,
CHG-011 ferrite, PWR-002 ripple <100 mVpp, ELEC-004/005/006 ESD Level 4,
ELEC-012 SPI length, USB90 stackup (KICAD-019/020).

---

## 7. Open nets — blockers (26 at drc127; BLOCKED Q5/Q6 — was 27 at drc126, 57 at drc143)

Root cause: placement density exceeds hand-routing capacity in QFN
fanout zones + BB minefield (USB spine + SPI + GND + P1.11). Resolution
per owner: ECO batch 1 (§2.7; Q2 C115 placed, Q3 U101 EN tied — both
CLOSED) + freerouting.org autorouter (§3.1) for the remainder. Prior-rev
per-net table retained below as the router work list; rows marked CLOSED
verified by parity DRC.

### 7.1 VBUS (12)

| Gap | Endpoints | Blocker |
|---|---|---|
| 1.90 | U101.3↔U101.1 (EN↔VIN) | Caged (U101.2 GND + GND via); AP2112K EN needs ext tie |
| 2.95 | R101.1↔BB | CLOSED drc141 (via 60.3,126.0) — verify |
| 4.13 | BB↔BB (63.4↔67.5 @112.3) | BB corridor survey needed |
| 4.60 | V3-N2 J201.A9→BB | Caged by IOA1-N@57.0 |
| 4.86 | U107.6↔BB | CLOSED drc136 (E@113.9 w0.5) — verify |
| 5.11 | C101.1↔U101.3 | D203→C101 east link open |
| 6.33 | R107.1↔C115.1 | C115 PARKED (46.0,108.0) — needs placement ECO |
| 6.36 | FT↔U106.6 | CLOSED drc140 — verify |
| 6.63 | E@134.0↔C101.1 | D203→C101 east link open |
| 7.79 | C118.1↔BB | East-exit corridor survey needed |
| 9.60 | West spine↔TP101 | A4–A9 west link open |
| 93.56 | C115.1↔north spine | C115 PARKED — needs placement ECO |

### 7.2 GND (11)

U107.2↔BB-112 (U107 cage), C118.2↔C107.2 (C104.1 cage), U501.21
(IS+ staircase cage), U202.3↔BB + U202↔BB (U202/USB cage), Q101.2
(VBUS-BB cage), EAST↔SOUTH-BB (C107.1 cage), U201.21 (3V3-box cage),
C204.1↔C205.2 (R207.2 cage), SW401.1 (3V3 cage), C115.2 (C115 parked).

### 7.3 +3V3 (8), VSEN_1V9 (5)

J202.1→R202.1 (P1.11-BB cage), R202.1→BOX (BTN2-BB cage), BOX→C204.2
(USB-BB + S2_NCS cage), BB→R511.2 (24 mm, TX corridor), + fragments.
VSEN: SOUTH↔NORTH (U301 cage), U302.4↔cluster (U302-row cage),
cluster→U201.7 (51 mm SW run), + 2 stubs.

### 7.4 Singles (19)

MCU_RST 2 (Pin_4 + BTN2-BB cage), J202-Pin_2 2 (GND+Pin_4+P1.11 cage),
P0.12 (S1_SCK adjacency), S2_NCS (S2_MISO + U201 cage), SW1_LTX/CTS/
IS+/D501-A/SW2/CTD/FTH (U501-QFN + TX cage), BTN3/SENSOR_EN/MCU_TX_EN/
VBUS_SENSE (cross-board runs), VDDPIX×2/LED_P (sensor-zone cage),
TX_IMON (29 mm).

**Recommended path (drc143-era, superseded — see §7.5):** placement ECO
pass (spread U501 south row, U201 east row, TX south band; place C115
with keepout survey) + BB corridor plan (USB spine fixed; route SPI/GND
around) + autorouter (freerouting.org) for singles.

### 7.5 drc127 — 26 opens (BLOCKED Q5/Q6; every row survey-verified)

Root cause: fixed-pad cages (0.5 mm-pitch QFN rows, adjacent-pad pairs,
testpoint overlaps) + routed mazes no ripup clears without breaking
placed copper. Q-ref = `notes/QUESTIONS.md`.

**+3V3 (2):** U0 (24.67,20.09)↔(22.66,19.0): GND-x=23.9 crossing (CLR 0.2)
— Q6 (move U201). U1 (33.48,26.6)↔(26.5,23.6): S2_MOSI-x=28.9 crossing —
Q6 (move U201). U2 CLOSED drc127 (ECO4 TP305→(44.0,43.5),
TP306→(44.0,47.2) + P131 east loop: B-y=45.0/F-hop/B-x=78.8/B-y=42.0
around S2_SCK corner (78.0,42.8); probe showed TP pads are F-only so the
true cages were S2_SCK-diag (path A) and S2_SCK-y=42.8 (path B direct)).

**GND (5):** U3 diag↔E-W-y=14.2-W-end: via (46.9,14.2) vs MCU_RST-x=46.43
SHORT (0.47) — Q6 (ripup MCU_RST zone). U4 (56.88,116.7)↔(56.52,115.0):
via-B N-S crosses +3V3-y=115.875 (X) — accept. U5 mesh↔rect-S: N-end
caged (VBUS-via 0.125 (vbus_clearance 0.25), +3V3-x=61.225 SHORT,
C106.2 0.1) — accept. U6 N-S-x=59.95↔N-S-x=60.45: via (59.95,117.0) vs
VBUS-x=59.3 SHORT (0.0, vbus_clearance) — accept. U7 frag
(74.985,15.0)↔N-S-x=71.8: TX_EN-x=74.51 (X); y=15.3 vs TX_EN-y=15.0
0.05 clr — Q6 (C507 move fails, see Q5-1).

**MCU_RST (2), VBUS (3):** U8 (12.475,20.75)↔(13.025,19.705):
R202.1-S-edge vs E-W-y=20.6 0.0 clr (Power 0.2) — Q6 (move R202).
U9 TP205↔maze: N-S-x=12.7 attempt crossed 6 items (P1.11/GND/+3V3/vias,
12 DRC errors, reverted) — accept/ripup P1.11 zone. U10 crawls↔U201.27:
3-sided cage (S2_MOSI N, U201.28 W, MCU_RST N) — Q6 (move U201).
U11 N-S-x=49.5↔N-S-x=43.8: IOB1-via F (OVERLAP), D+-y=124.7 B (X) —
accept. U12 C118.1↔N-S-x=59.3: C106 gap 0.9 < 1.0 needed
(w0.5 + 2×0.25 vbus_clearance); neck w0.25 REJECTED (vbus_min_width)
— Q6 (move C106).

**Power/sense:** U13 VSEN 34 mm: F GND-x=51.725 (X) + VDDIO_S1
(OVERLAP); B TX_5V_SW-x=50.99 (X) + S2_MISO-diag (X) — accept.
U14 TX_IMON 29 mm maze (10+ nets) — accept. U15/U16 VIN: U501.2-CTS
pad between U501.1/U501.3 (OVERLAP); IS+-x=50.48 (0.12 clr) —
Q6 (move U501: breaks 20). U17 VIN-E N-end: BTN3-diag cage (X, 0.0747
clr); W/E also cross BTN3 — accept. U18 FTH 14.7 mm maze — accept.
U19 D501-A: F FB_PK-diag (X) + D501.1-pad (OVERLAP); B TX_EN-x=61.9
(X) + FB_PK-x=64.55 (X) — Q6 (move D501/D502).

**Cross-board + TX (schematic-ECO or accept):** U20 MCU_TX_EN 104 mm
pad-pad, both QFN-caged — **Q5-4**. U21 VBUS_SENSE 115 mm — **Q5-2**.
U22→23 SENSOR_EN 79.5 mm: U201.42 (TX_STAT W, U201.40 N), R103.1
(R103.2 OVERLAP), U104.3 (GND-cage) — **Q5-3**. U26 CTD: U501
0.5-pitch unthreadable (0.65 > 0.5) + C507.2 3-sided cage; ripup
attempted & reverted (10 DRC errors) — **Q5-1**. U27 Pin_2: F Pin_4
(X) + MCU_RST-x=9.725 (SHORT); B Pin_4 (0.182) + MCU_RST (SHORT) —
accept/ripup J202 zone. U28 P0.12: F S2_MOSI + MCU_RST-x=29.77 (X);
B S1_MOSI-x=24.4 (X) + AIN5-x=23.34 (X) — accept. U29 S2_MOT: F-W
S1_SCK-x=40.0 (X) + BTN3-x=40.793 (X); S GND-via (0.05) +
C504.1-N-edge (SHORT) + GND-diag (X) — accept.

**Closed drc143→drc127 (−31):** T-junction workarounds (P37/P99/P100),
via stitches (P129/P130), U2 (P101/P102), U7-GND (P106), U10-RST (P107),
U12-RST (P101/P104), U26-D501-A-B (P108), VBUS/GND crawls (H3.1 P78,
GND-S P91, U7-U8 P44, U15-U17 P31, U14 P32, U5 P33), U2 east loop
(ECO4 TP305/306 + P131).
**Ripup attempted & reverted:** TX-zone (rb36/P109, 10 errors),
RST-maze (P103, 12 errors), SEN-N (rb23), U8N (rb25), C505N
(rb28/rb29). **Path:** owner answers Q5 (4 alt-taps) + Q6 (TP move +
accept-or-ripup on 23); 2–3 sessions after ECOs.

### 7.6 Known-opens for respin (drc128 triage — all 26 items)

Board unchanged since drc127 (drc128: 179 warn / 26 unc / 0 err /
0 parity, item-for-item identical). Every row below was verified by
TRUE pcbnew corridor surveys (0.5 mm margin) + file audit; ripups
attempted & reverted: TX-zone rb36/P109 (10 errors), RST-maze P103
(12 errors), SEN-N rb23, U8N rb25, C505N rb28/rb29, C203N rb32,
C101N, J201N/E, VIN-N rb42/P128. Independent oracle: freerouting.org
2.4.1 headless (JRE 25, 50-pass) stuck at 73 unconnected, score frozen
716.45 across passes 2–4 — autorouter agrees the cages hold.

**Q5 — schematic-ECO group (4 nets, both endpoints pad-caged):**

| ID | Net | Caged endpoints | What was tried |
|---|---|---|---|
| U20 | MCU_TX_EN | U201.28 (QFN row) ↔ R111.2, 104 mm across maze | Corridor surveys both ends caged; no ripup (cross-board, pad-caged) |
| U21 | VBUS_SENSE | U201.3 (adj-pin cage) ↔ R-triple / B-E-W-y=122.9 stub, 115 mm | Corridor surveys both ends caged; no ripup |
| U22/23 | SENSOR_EN | U201.42 (TX_STAT W 0.4clr + U201.40 N OVERLAP) ↔ R103.1 (R103.2 OVERLAP) / U104.3 (GND cage), 79.5 mm | All taps surveyed caged; N-stub SHORTED vs BTN1/R401.2, ripped |
| U26 | CTD (`/tx/Net-(U501-CTD)`) | U501.14 (0.5-pitch: 0.65 > 0.5 gap, unthreadable) ↔ C507.1 (C507.2 3-sided cage) | Surveys fail all rows; rb36/P109 ripup placed then SHORTED (C507.2 0.065, TX_STAT-via OVERLAP, D501-A crossing, 10 errors), reverted rb39/P112; C507-N move fails W-end; U501 move breaks 20 |

**Q6-remainder — placement group (22 nets; TP305/TP306 U2 FIXED drc127
via ECO4 + P131, noted — not in this table):**

| ID | Net | Caged endpoints | What was tried |
|---|---|---|---|
| U0 | +3V3 | (24.67,20.09)↔(22.66,19.0): GND-x=23.9 crossing (CLR 0.2) | Surveys; needs U201 move |
| U1 | +3V3 | (33.48,26.6)↔(26.5,23.6): S2_MOSI-x=28.9 crossing | Surveys; needs U201 move |
| U3 | GND | diag↔E-W-y=14.2-W-end: via (46.9,14.2) vs MCU_RST-x=46.43 SHORT (0.47) | Surveys; needs MCU_RST-zone ripup |
| U4 | GND | (56.88,116.7)↔(56.52,115.0): via-B crosses +3V3-y=115.875 | Surveys; accept |
| U5 | GND | mesh↔rect-S: VBUS-via 0.125 (vbus_clearance 0.25), +3V3-x=61.225 SHORT, C106.2 0.1 | Surveys; accept |
| U6 | GND | N-S-x=59.95↔60.45: via (59.95,117.0) vs VBUS-x=59.3 SHORT | Surveys; accept |
| U7 | GND | (74.985,15.0)↔N-S-x=71.8: TX_EN-x=74.51 X; 0.05 clr | Surveys; C507 move fails (Q5-1); accept-or-move |
| U8 | MCU_RST | (12.475,20.75)↔(13.025,19.705): R202.1-S-edge vs E-W-y=20.6, 0.0 clr (Power 0.2) | Surveys; needs R202 move |
| U9 | MCU_RST | TP205↔maze: N-S-x=12.7 crossed 6 items, 12 DRC errors (P103) | P103 ripup reverted (rb35/P104/P105); accept-or-ripup P1.11 zone |
| U10 | VBUS | crawls↔U201.27: 3-sided cage (S2_MOSI N, U201.28 W, MCU_RST N) | Surveys; needs U201 move |
| U11 | VBUS | N-S-x=49.5↔43.8: IOB1-via F OVERLAP, D+-y=124.7 B X | Surveys; accept |
| U12 | VBUS | C118.1↔N-S-x=59.3: C106 gap 0.9 < 1.0 (w0.5 + 2×0.25); neck w0.25 REJECTED (vbus_min_width) | Surveys; needs C106 move |
| U13 | VSEN_1V9 | 34 mm: F GND-x=51.725 X + VDDIO_S1 OVERLAP; B TX_5V_SW-x=50.99 X + S2_MISO-diag X | Surveys + SEN-N rb23 ripup reverted; accept |
| U14 | TX_IMON | U201.15↔stub, 29 mm maze (10+ nets) | Surveys; accept |
| U15 | VIN | U501.2-CTS pad between U501.1/U501.3 OVERLAP | Surveys; needs U501 move (breaks 20) |
| U16 | VIN | IS+-x=50.48, 0.12 clr | Surveys; needs U501 move (breaks 20) |
| U17 | VIN-E | N-end BTN3-diag cage (X, 0.0747 clr); W/E cross BTN3 | Surveys + VIN-N rb42/P128 ripup reverted; accept |
| U18 | FTH | U501.9↔stub, 14.7 mm maze | Surveys; accept |
| U19 | D501-A | F FB_PK-diag X + D501.1-pad OVERLAP; B TX_EN-x=61.9 X + FB_PK-x=64.55 X | Surveys; needs D501/D502 move |
| U27 | J202-Pin_2 | F Pin_4 X + MCU_RST-x=9.725 SHORT; B Pin_4 (0.182) + MCU_RST SHORT | Surveys; accept-or-ripup J202 zone |
| U28 | P0.12 | F S2_MOSI + MCU_RST-x=29.77 X; B S1_MOSI-x=24.4 X + AIN5-x=23.34 X | Surveys; accept (Q6 table lists U201-move alt) |
| U29 | S2_MOT | F-W S1_SCK-x=40.0 X + BTN3-x=40.793 X; S GND-via 0.05 + C504.1-N-edge SHORT + GND-diag X | Surveys; accept (Q6 table lists U201-move alt) |

---

## 8. Rule citations (index)

ELEC-002/004/005/006/012/027/029, CHG-001/009/011, PWR-002,
MECH-002/003/006/008/022/049, RF-002/022, TOUCH-001,
KICAD-011/013/019/020/022, SENSOR_SELECTION, SCROLL_UX_DESIGN,
FINAL_SPEC Rev 3.1, RULES.md (normative). E-series deviations E13.2–E49
per devlog (`/tmp/devlog.md`, merged above).

---

## 9. Stage-1 Blender-manual geometry review (Q4, drc127)

Scope: owner Q4 (2026-10-02) authorized the Blender-manual path. The six
automated `blender/check_*.py` scripts (§4 M4–M8) are NOT runnable here:
absent from this repo, and `~/workspace/trackball-drc/` does not exist on
this box — stated per prompt §Validation, no script invented. This section
records the manual equivalents: fresh STEP/GLB exports, 4 Blender review
renders with deterministic fallback bodies, KiCad top/bottom cross-check
renders, and pcbnew measurements. Coordinates in mm, file origin, +y
south (toward the USB edge).

DRC at review time: `notes/stage1/drc-stage1.json` — 179 warnings (123
`lib_footprint_mismatch` per KICAD-013, 49 `track_dangling`, 3
`via_dangling`, 2 `holes_co_located`, 2 `silk_edge`) + 26 unconnected,
0 errors, 0 parity — same scope as drc127 §5. Review proceeds under the
explicit task authorization; opens stay documented in §7, BLOCKED Q5/Q6
stands.

### 9.1 Board outline, stackup, mounting

- Outline: rect 110.1 × 140.1 (x −0.05…110.05, y −0.05…140.05),
  4 straight segments, SHARP corners (no arcs). kicad-pcb practice
  prefers rounded/chamfered corners — flagged for MECH confirm, not a
  rule violation. Renders confirm all holes cut through.
- Stackup: 2L FR-4, `(thickness 1.6)` from file; GLB board-top z =
  1.595 mm (Blender GLB→world calibration residual 0.0000 mm on
  U501/U202/SW201/SW202).
- Mounting: H1–H6, 3.2 mm drill, corners (5,5) (105,5) (5,135)
  (105,135) + mid-sides (5,70) (105,70); symmetric about x = 55.
  (MECH-006 steel-insert mounting is enclosure scope.)

### 9.2 Sensors (MECH-002/003/022; M6)

- U301 (41.66,71.59) rot0 F, U302 (68.34,71.59) rot0 F, custom
  PMW3360DM-T2QU DIP; center distance 26.68. Both rot0 = parallel
  packages: consistent — MECH-003's 80–100° is the angle between
  ball-center→patch vectors (enclosure datum), not a footprint rotation.
- PTH census: 16 pins × 0.7 mm drill each ✓ (16-pin DIP per
  SENSOR_SELECTION §1).
- NOT verifiable at PCB stage: MECH-003 axis angle (needs ball-center XY
  + patch coords from enclosure CAD), MECH-002 Z = 2.4±0.1 (needs DIP
  shoulder + LM19-LSI stack + ball surface datum), MECH-022 ≤0.25 stack.
  Sensor XY above is the PCB-side input; enclosure CAD plus the missing
  `check_sensor_geometry.py` own the verdict. M6 → MANUAL-XY-ONLY.

### 9.3 Buttons (MECH-008/049; M8-partial)

- SW401 (35,100), SW402 (75,100), SW403 (55,93), all rot0 F, D2FC-F-7N.
  L/R spread 40 mm about x = 55; scroll 7 mm south of the L/R row,
  centered.
- MECH-008 (below equator, ≥8 mm from ball) and MECH-049 (thumb reach
  ≤45 mm) need the ball-center/enclosure datum — not verifiable at PCB
  stage. D2FC plunger-side orientation still PROVISIONAL (App A.1):
  fallback plunger modeled at local x −5.2 per project .wrl.

### 9.4 USB-C (MECH-006, ELEC-004/005/006; M8-partial)

- J201 (55,134) rot0 F, USB_C_Receptacle_HRO_TYPE-C-31-M-12; 6 TH legs
  (slot drills 0.6×1.2, 0.6×1.7 + 0.65 round) + 16 SMD → MECH-006 "≥4 TH
  shield legs" SATISFIED by count; the mid-mount deviation stands (§6).
- Placement: center 6.05 from the south edge; courtyard y 128.71…138.18
  (1.875 inside the outline) ✓ seated, no overhang.
- U202 (55,124) SOT-563 rot−90: min U202-pad → J201-courtyard-edge =
  3.99 (pad-bbox top 124.713 vs courtyard ymin 128.705, x-ranges
  overlap) → ELEC-005/006 "<5 mm from connector" SATISFIED vs the shell
  courtyard (pad-to-pad 5.248 recorded for the file). §2.3 claim holds.

### 9.5 TX coil interface (CHG-001, ELEC-029; M5-partial)

- L501 (55,10) rot0 F, TX_COIL_IF_2P508: 2×PTH 1.6 mm drill ✓ (§2.5);
  courtyard 7.04×6.06. U501 QFN-20 at (55,16), 6.0 south of L501 center.
- Coil is off-board/custom per BOM (Wurth 760308100110 ref geometry,
  PROVISIONAL): ELEC-029 SPI-to-coil 5 mm / edge-to-coil 3 mm cannot be
  verified until coil geometry lands. Interface position + PTH recorded.

### 9.6 RF module + antenna keepout (RF-002/022; M4-manual)

- U201 = E73-2G4M08S1C module at (22,10) rot180 F; courtyard x
  14.38…29.62, y 0.68…20.12 (0.73 from the south edge). Module long axis
  N–S; shield/antenna end faces the south board edge per project .wrl
  massing (local +y → board −y under rot180).
- Planar census (first actual measurement; §2.4 "verified by script" had
  no supporting evidence — corrected): 0 tracks/vias in the strip
  x∈[10,34], y<2.0 south of the module on EITHER layer ✓; nearest other
  pad to the module courtyard R202.2 @ 1.08. The 163 in-courtyard copper
  hits are predominantly U201's own pin fanout (SPI/GPIO/USB/BTN stubs)
  plus crossing stubs of open nets — all under the module body, not a
  keepout verdict either way.
- RF-022 volumetric 8 mm keepout needs enclosure CAD + module datasheet
  antenna geometry — not verifiable at PCB stage. M4 → MANUAL-PLANAR-ONLY.

### 9.7 FINDING F9-1 — no zones in file (KICAD-019)

- Measured: 0 `(zone` entries (file grep + pcbnew `board.Zones()`),
  2318 tracks. §1 "GND poured zones both sides", §2.4 "keepout poured
  clear", §3 "poured zones" were INTENT, not embodied copper — corrected
  in place. GND today = track stitching only; keepout claims reduce to
  "clear by absence" (verified §9.6 for the antenna strip). Zones must be
  placed + refilled before fab (route-close work, after Q5/Q6 unblock).
  GLB `--include-zones` exported nothing.

### 9.8 FINDING F9-2 — 3D massing models unusable in KiCad 10 (MECH review aid)

- Project .wrl (PMW3360/D2FC/E73, plausible-mm dims): KiCad 10 export
  reports "No model for filename" (6×) for GLB and refuses VRML for
  STEP; `pcb render` loads them at wrong scale (giant grey/white blocks
  in `kicad-render-top.png`). Root cause not chased (loader/unit issue);
  footprints need a `(model (scale …))` fix or STEP replacements before
  MECH sign-off.
- Stock .step missing from install: J201 HRO receptacle ("File not
  found"), F101, D502 ("Could not add 3D model"). L501 has no model entry.
- Blender fallbacks used (deterministic, from .wrl numbers-as-mm):
  PMW3360 body 16.2×10.1×2.4 + lens cyl r5 h6.7 + plate 21.15×18.85×1.0;
  D2FC body 12.8×5.8×6.0 + plunger r0.6; E73 13×18×2.2 + shield 10×3×0.8;
  J201 courtyard-box 10.68×9.47 hNOM 3.5; L501 courtyard-box 7.04×6.06
  hNOM 6.0. J201/L501 heights are NOMINAL placeholders (App A.7/8) —
  verify against vendor drawings before MECH sign-off.

### 9.9 Render evidence + observations

- `notes/stage1/blend-hero.png` (1920×1080), `blend-top.png`,
  `blend-sensor.png`, `blend-back.png` (1600²), Cycles CPU 64sp +
  denoise, builder `notes/stage1/build_scene.py` (GLB→world calibration
  residual 0.0000 mm). Cross-checks: `kicad-render-top/bottom.png`.
  Sources: `trackball-base-review.step` + `.glb`, regenerated from the
  drc127 board for this review (`--force --no-dnp --subst-models`,
  tracks/pads/zones/silk/mask, `--cut-vias-in-body` on GLB).
- Observed: outline + all 6 holes + J201 slots present; all 16 fallback
  bodies seated on their pads (sensor stacks over the PTH pin fields,
  D2FC boxes on pin fields, E73/J201/L501 on courtyards); no body-to-body or
  body-to-hole interference visible at review resolution; bottom shows
  sensor PTH stubs + J201 slots + routing.
- Limits: the GLB track mesh sits buried under mask faces (copper
  reviewed via the kicad renders, not Blender); mask color in renders is
  KiCad-default green — NOT a fab color decision (App A.9); F101/D502
  render as bare pads (no model, minor parts).

### 9.10 M-row reconciliation

| M4 antenna | MANUAL-PLANAR-ONLY §9.6 (RF-022 volumetric needs enclosure CAD) |
| M5 coil | MANUAL-PARTIAL §9.5 (coil geometry PROVISIONAL/off-board) |
| M6 sensor | MANUAL-XY-ONLY §9.2 (angle/Z need ball datum + missing script) |
| M7 socket/stability | NOT RUNNABLE — enclosure CAD absent, scripts missing |
| M8 buttons/USB | MANUAL-PARTIAL §9.3/9.4 (ELEC-006 3.99 ✓; enclosure items open) |

---

## Appendix A. Assumptions

1. D2FC plunger-side orientation assumed (MECH to confirm).
2. U101 EN tied to VIN externally (AP2112K standard; route open).
3. D501/D502 package TBD — footprint provisional.
4. USB90 0.25/0.20 GCPW provisional pending stackup sim.
5. All PROVISIONAL values require bench before fab.
6. Partial route accepted for this checkpoint; §7 is the work list.
7. J201 render body height 3.5 NOMINAL (§9.8 render placeholder only).
8. L501 render body height 6.0 NOMINAL (§9.8 render placeholder only).
9. Render mask color (KiCad-default green) is NOT a fab color decision.

## Appendix B. Evidence files

- DRC: `/tmp/resume_drc127.json` (+ drc18–drc127 series in job archive).
- Board: `trackball-base.kicad_pcb` @ drc127 (job/trackball-base-layout).
- Scripts: `/tmp/raw.py`, `/tmp/ripbatch.py`, `/tmp/svbatch.py`,
  `/tmp/audit.py`, `/tmp/q*.py`, `/tmp/p*.json`, `/tmp/rb*.json`,
  `/tmp/drc.sh`, `/tmp/freerouting-2.4.1.jar` (+ Temurin JRE 25).
- Stage-1 checks: MANUAL review §9 (auto scripts missing; M4–M6/M8
  manual-partial, M7 not runnable; route-close + Q5/Q6 still block M1–M3).
- Stage-1 evidence (`notes/stage1/`, drc127 board): `drc-stage1.json`
  (179 warn / 26 unc / 0 err / 0 parity), `trackball-base-review.step`
  + `.glb` (fresh exports), `build_scene.py` (deterministic Blender
  builder), `blend-hero/top/sensor/back.png` (review renders),
  `kicad-render-top/bottom.png` (copper cross-checks).
- Triage snapshot (drc128, board unchanged): `notes/stage1/`
  `drc128-triage.json` + `kicad-render128-top/bottom.png`; known-opens
  tables §7.6; owner options in `notes/QUESTIONS.md`.
- Blockers: `notes/QUESTIONS.md` (Q5 schematic-ECO 4 pads, Q6 placement).

## §7.7 WaveC results (2026-10-04, drc164→drc177, 17→16 unc, 0 err, 0 parity)
- CLOSED: J202-Pin2 (B-route x=13.8 + VSEN-via bypass + vias (12.2,9.45)/(9.95,19.7)).
- →WaveD (micro-route provably sealed, net-zero rips): MCU_RST-north (F-+3V3-maze/B-S1/USB-D+ seals);
  VIN-8/U501.1-3 (CTS-pad sandwich + GND-E-W); P0.12 (U201 pad-forest + TX_EN/D±/S1_NCS);
  S2_MOT (U201-col + SENSOR_EN + TX_STAT-L + FID1-0.6 + B-GND/TX_EN/P1.11);
  MCU_RST-west (GND + P1.11 + +3V3-maze); VSEN_1V9 (F×7 + B-VDDPIX/TX_5V_SW/S2_MOSI-diag);
  VIN-east (TX_STAT/SW2/D501-A + SW2-via + CTD); FTH (U501-8/10/21 cage + GND-B + NTC/TX_STAT-vias).
- WaveD=15, WaveZ=GND-3. Next: Q6-authorized destructive re-place (checkpoint drc177 clean).

## §7.8 WaveD micro-angles exhausted (2026-10-04, board untouched, drc177 16/0/0 stands)
- S2_MOT-B @7.5: sealed (B: BTN3-E-W @7.96/diag/via (38.39,10.0) + S1_NCS-N-S x=39.02/E-W @6.85; south-jog + north-hop both sealed).
- P0.12-B @9.6: sealed (B: J202-E-W @8.81/via + SENSOR_EN-N-S + BTN3-diag/E-W + S1_MOT-diag/via + S1_NCS; F-east sealed by BTN3-E-W @10.00 + S1_SCK-E-Ws).
- MCU_RST-west-B: sealed (B: J202-maze/Pin4-N-S/vias/E-W @20.50 + BTN2/VSEN/BTN1/S2_NCS N-Ss + +3V3-diag/E-W; F sealed per §7.7).
- VIN-8/CTS-reroute-east: sealed (CTS-east blocked by GND-N-S x=54.00 + TX_IMON-N-S + IS+-diag; VIN west bypass independently sealed by GND-via (51.47,15.0)).
- Disposition: micro-routing at its limit for all 15 WaveD nets. Next = Q6 zone-redo:
  (1) south-band y[4,18] x[21,44] rip + coherent bus re-route (P0.12/S2_MOT/TX_IMON-w);
  (2) U501-TX zone rip + re-route (VIN-8/9/FTH); (3) N-S spine corridors
  (MCU_RST-n/VBUS/VSEN/MCU_TX_EN/VBUS_SENSE); (4) WaveZ GND-3 zone-close.

## §7.9 Zone-1 + Zone-2 seals (2026-10-04, drc179 16/0/0 net-zero)
- ZONE-1 south-band SEALED: P0.12-north-dip closed (16->15) but 6 errors — U201-28/U201-27-vbus
  0.125 corridor, SPI-intra-0.6 vs S2_MOSI (P0.12 is SPI-netclass), D--via/VBUS sandwich;
  S2_MOSI-reroute sealed by GND-maze (E-W @17.65 + N-S x=23.9 to y24.6). Ripped net-zero.
- ZONE-2 U501-TX SEALED: FTH needs TX_STAT-E-W @18.94 + FB-N-S x=58.94 (16.5-28.0) double-rip,
  but reroutes re-cross (full-height walls; perpendicular crossings unsolvable without 5-net
  cascade); VIN-9/D502-move west sealed (FB-reroute: D501-A+CTD inverted corridor, SW2-via+D501-A
  inverted corridor; VIN-east @15.0 bus re-feed needs 16mm B-run); VIN-8 needs U501-move
  (GND-rip ripples into VIN/IS+). Rips reverted; drc179 stands.
- NEXT: Zone-3 N-S spines (MCU_RST-n/VBUS/VSEN/MCU_TX_EN/VBUS_SENSE + U501-move assessment).

## §7.10 Zone-3 spine seals + move assessment (2026-10-04, drc179 16/0/0 net-zero)
- VBUS-5: F-column x=28.4 DEATH (20+ crossings + U103 @93.0); B-column x=28.4 DEATH
  (GND/MCU_RST-maze/S1_MOSI/S1_MOT-diag/BTN1-diag/GND-N-S+via/U103). Meander ~45 segs est.
- +3V3-1: F sealed (GND-maze + S2_MOSI-N-S full-height); B sealed (MCU_RST/SENSOR_EN/USB-D±/S1_MISO 5-N-S forest).
- MCU_TX_EN-12: F @118.68 sealed (5 GND-N-S + +3V3-N-S/diag); @117.6 DEATH (9 crossings);
  @116.6 DEATH (10 crossings incl VBUS/TX_ON); @114.6 south-hops sealed (Q101/TX_ON-E-W + TX_ON-diag + GND).
- MOVE ASSESSMENT: U501-move breaks ~15 nets, own-pad sandwiches persist (VIN-8/FTH cages move
  along), new-neighbor risk (D501/C507/C106), ~2 turns uncertain — NOT RECOMMENDED next.
  U201-move breaks ~30 nets, USELESS for own-pad seals (P0.12/S2_MOT) — NOT RECOMMENDED.
- NEXT: freerouting.org ORACLE-as-advisor (standing Q2): run on drc179 copy, inspect oracle
  corridors for the 16 opens, hand-place verified corridors on real board (no blind import).

### 7.10.3 Zone-lock survey (drc182+1, oracle-2 running): 5 opens proven SEALED
Fresh DRC unconnected dump + pad-geometry survey (U501 QFN pins 0.82x0.25, EP x[53.75,56.25] y[14.75,17.25]):
- VIN-#7 (U501-3 pin3 <-> N-S (53.06,13.6-15.0)): PIN-CAGED. F-east sealed by GND-EP (0.275 gap < 0.55 needed); F-west crosses CTS-E-W @15.50/CTS-diag; via-bridge corridor (15.625+0.425 vs 16.375-0.425) INVERTED between CTS-pin2 and IS+-pin4; pin3 north/south escape gaps 0.25 < 0.55. Via-in-pad would violate standing via>=0.6/0.3 rule. NEEDS U501-move (zone-2).
- +3V3-#1 ((22.66,19.0) <-> (24.67,20.09)): south-under sealed by P0.29-E-W @13.88 + TX_EN-E-W @13.16 + TX_EN-via sandwiches; north-over sealed by GND ladder (E-W @24.60/@25.10/@25.60/@26.00); B sealed by P0.29-N-S + S1_MOSI-N-S. NEEDS GND-ladder zone rework.
- GND-#3 ((55.9,124.7) <-> (58.8,124.0)): sealed all 6 sides — north: VBUS-SENSE via-pair + E-W @127.50; south-F: IOA1-E-W @122.00 + VBUS-E-W @122.00; south-B: VBUS-E-W @123.70; east: via-pair; west-around: dies at east wall; F-north: VBUS-N-S x=57.40 + VBUS-E-W @128.50 + VBUS-via. NEEDS U202/VBUS zone rework.
- +3V3-#2 ((25.0,23.6) <-> (33.48,26.6)): F sealed by GND maze (N-S x=32.45/x=31.02, E-W @23.50/@24.50/@25.97/@26.00, vias, S2_MOSI x=28.90, C204); B sealed by 4-spine wall (SENSOR_EN x=30.85, D- x=31.50, D+ x=32.00, S1_MISO x=33.20, all full-span). NEEDS spine-zone rework.
- S2_MOT (oracle @7.53 violates SPI-0.6 on copy; @5.5/@6.0/@6.5 sealed by J202-Pin4-E-W @6.00 + S1_NCS-E-W @6.85 sandwich). Awaiting oracle-2 for SPI-clean corridor.
Board is in ZONE-LOCK: 14 opens need zone rework or deep-oracle corridors. Oracle-2 (-mp 100) running on copy.

### 7.10.4 Zone-lock survey continued: 4 more opens SEALED (9/14 this turn)
- VSEN_1V9 ((49.45,73.7)B <-> (68.66,67.7)F): B-east sealed by S2_MISO-diag + S2_MISO-N-S x=66.88 wall + U302 courtyard (68.34,71.59); F-east sealed by GND maze (x49-57,y64-78) + MCU_RST-N-S x=62.32 + BTN3-N-S x=59.63 full-span + S2_MOSI-diag. NEEDS sensor-field zone rework.
- MCU_RST-w ((12.47,24.0) <-> TP205-1 (20.5,30.0)): F sealed by P0.00-maze + Y201 courtyard (E-W @25.20 violates; @25.60 hits GND-E-W) + P0.01 + +3V3-diag @27.06 + +3V3-E-W @26.50 + +3V3-stub @26.04; B sealed by 5-spine wall (BTN2 x=15.10, VSEN x=18.57, BTN1 x=19.60, S2_NCS x=20.45, S2_MISO x=21.36). NEEDS west-field zone rework.
- VIN-#8 ((53.6-56.0,12.7)B <-> (67.52,9.5-13.0)F): B-north sealed by SW2-via/FB-E-W @13.01 sandwich (corridor inverted); F sealed by SW2-N-S x=61.52 + EN-N-S x=56.94; B-south sealed by TX_EN maze + FB_PK + D501-A + L501/D501/D502. NEEDS U501-TX zone rework.
- P0.12 ((23.27,16.9) <-> (38.83,16.9)): F-north sealed by S2_MOSI wall (N-S x=27.13/x=28.90 + E-W @17.60); F-south sealed by VBUS-E-W @15.12 + S2_MOSI-N-S tip sandwich (corridor 15.72 vs 15.575 INVERTED, vbus_clearance 0.25); B sealed by 7-spine wall. NEEDS south-band zone rework.
Remaining 5 (VBUS, FTH, MCU_TX_ENx2, VBUS_SENSE) sealed in prior waves (WaveC/D). 14/14 opens now zone-locked by survey. Oracle-2 (-mp 100) still running; if it finds no SPI-clean corridors, next step is owner-authorized Q6 destructive zone rework in dependency order (south-band rip + coherent bus re-route, U501-TX zone, N-S spines).

### 7.10.5 Oracle-2 verdict + S1_NCS-relocation failure (drc183) + revert (drc184)
- Oracle-2 (-mp 100, 81 unrouted/88 violations): SES import to copy closes 0/14 opens, adds 40 violations (dangling/edge/drill/clearance). Oracle-as-advisor EXHAUSTED (2 runs). Tag `q6-zone-rework-base` = 9812fdf (drc182 state) before any ripup.
- drc183 FAILED relocation (S1_NCS-E-W @6.85 -> @6.50+@5.65-dip + S2_MOT place): 15unc + 13 real errors. Root causes (all mine): (1) same-layer dip under J202-E-W @6.00 = tracks_crossing (conceptual error — dip must cross the wire); (2) Default clearance is 0.200mm (netclass 'Default'), not 0.125 — all four 0.125-borderlines violated; (3) wrong distance pair (riser-top-point vs via-center-point instead of segment-segment: actual 0.195 vs SPI-0.6); (4) both same-net merges failed open (endpoint assumptions off); (5) spi_max_length 150mm: S1_NCS 150.38mm over budget (relocation must be <=0 length delta); (6) unsurveyed J202-Pin_2 copper @ (24.2,8.6) SHORTED.
- CORRECTION (standing): Default clearance = 0.2mm. Prior SEAL verdicts stand a fortiori (all rested on gaps <0.125 or crossings); TX_IMON/MCU_RST-north placements empirically DRC-clean. Future surveys must use 0.2 (signals), 0.6 (SPI-intra), 0.25 (vbus).
- S1_NCS wall is incrementally immovable (J202-E-W crossing on same layer, length budget, J202-Pin_2 east copper). S2_MOT needs FULL south-band coherent re-route (J202-Pin_4 moves as part of it), not wall-shifts.
- drc184 after `git checkout q6-zone-rework-base`: 14unc/0err/0parity, working tree clean. Net-zero confirmed.

### 7.10.6 S2_MOT partials EXHAUSTED — full south-band rip justified (drc184 base)
U201 pads (F-SMD): 38[S2_MOT] (26.4,8.145) 0.85x0.85, 37[Pin_2] (28.4,8.780), 39[Pin_4] (28.4,7.510) — S2_MOT sits between Pin_2/Pin_4 (1.27 pitch). J202 = CORTEX-DBG-10 2x05 P1.27 SMD @ (8.0,22.0); pins 1:+3V3, 2:Pin_2, 3/5/9:GND, 4:Pin_4, 10:MCU_RST. Board outline 110x140 rect (edge keepout kills y<~0.8 southern path; S1_NCS southern reroute also length-killed: ~148.9+9.9 >> spi_max 150).
- Partial A (S1_NCS-E-W @6.85 -> @6.50+@5.65-dip): FAILED drc183, reverted (§7.10.5).
- Partial B (J202 north 2mm): DEAD — landing zone occupied by own fanout + GND maze + C206 @ (10.5,17.0).
- Partial C (Pin_4 E-W @6.00 -> north lane @13 + N-S x=28.90): DEAD — any via in x[22.91,39.02] y[6.15,7.55] hits S1_NCS-E-W @6.85 (B-annulus, SPI-0.6); N-S x=28.90 cannot reach F-@7.01 across @6.85. S1_NCS-E-W is the KEYSTONE (also length-locked: +1.1mm budget; F-swap blocked by J202-N-S x=33.50).
- Partial D (S2_MOT north-around via @10.40): DEAD — U201-38 caged on B (Pin_2-E-W @8.66/@8.81 + via (24.34,8.66) + BTN3-E-W @7.96 sandwich, all gaps inverted); east @10.40 crosses SENSOR_EN x=30.85 + S1_MOT-diag + S1_MISO x=33.20.
- Partial E (U201-38 F-exits): DEAD — east: SENSOR_EN corner (@8.09-E-W + N-S x=27.16); north: module body; south: J202-@6.00 B-shadow spans full width (via SHORT) + TX_EN @5.30; west: S1_NCS-F-N-S x=22.91.
- Partial F (S1_NCS southern @2.0 / F-swap / @6.50-plain-shift): DEAD — length (+9.9/+1.6 over ~1.1 budget), J202-N-S crossing, N-S tip gaps.
CONCLUSION: S2_MOT + Pin_2 + Pin_4 + S1_NCS-keystone + BTN3 form a TRUE KNOT — no single-net move frees a lane. Q6 FULL south-band rip + coherent simultaneous re-route is the only structural fix (owner-authorized; cheaper partials provably fail per directive).
RIP PLAN (next): zone y[4,18] x[21,44], PRESERVE N-S spines (SENSOR_EN x=30.85, D- x=31.50, D+ x=32.00, S1_MISO x=33.20, S1_MOSI x=24.40, S1_MOT, S1_NCS-north) + TX_IMON corridor + S2_MOT east island + P0.12 east island; RIP E-W band copper + U201/J202 fanouts (S1_NCS-south-leg, Pin_2, Pin_4, BTN3, P0.12-west, S2_MOSI-south, P0.29-south, TX_EN-south?, VBUS-south?, S2_SCK-south?). RE-ROUTE in lane order with spine-hop vias; close S2_MOT-west + P0.12-west in new lane structure. Reversibility: tag q6-zone-rework-base; commit rip as own checkpoint; revert if DRC regresses.

### 7.10.7 RIP CHECKPOINT drc185 (22unc/0err/0parity): surgical rip executed, clean
/tmp/rip.py ripped 65 (S1_NCS-keystone exact-4, Pin_2 all-in-zone, Pin_4 all-in-zone, BTN3-west of x=36, P0.12-west exact-2, S2_MOSI-south-4; BTN3-east + P0.12-via kept as anchors). New opens: S1_NCS, Pin_2 x2, Pin_4 x2, BTN3, S2_MOSI (P0.12 was open, now 2 pairs). Zero real errors, zero parity — rip is DRC-clean. Anchors kept: U201-37/38/39 pads, S2_MOT east island, P0.12 east island (x=38.83), BTN3-east diag (36.15,7.96), S2_MOSI N-S x=28.90, S1_NCS F-N-S x=22.91 + B-N-S x=39.02 stubs, Pin_2/Pin_4 west fanouts, TX_IMON corridor, all spines, power. NEXT: survey emptied band y[5.5,8] x[22,39] (B+F) + anchors, then lane-ordered re-route: (1) S2_MOT-west @6.00-lane, (2) S1_NCS @6.85 re-take, (3) Pin_4, (4) Pin_2, (5) BTN3-west, (6) S2_MOSI-south, (7) P0.12-west.

### 7.10.8 RIP REVERTED drc186 (14unc/0err/0parity): simultaneous-fit impossibility proof
Post-rip band survey (B/F y[5.5,8.5] x[22,39]): only SENSOR_EN feed + TX_IMON-N-S x=37.00 + TX_STAT + S1_NCS-F-N-S x=22.91 + R114 @ (31.30,5.61) + FID1 remain. Lane design proved:
- S2_MOT-razor w0.20 @6.0375 (gaps 0.2025/0.6125) KILLED by R114-courtyard (north ~6.11); R114 IMMOVABLE (SENSOR_EN-series 0R: drops cross TX_IMON-E-W @4.60 full-span); south-@4.85/@5.10 KILLED (TX_IMON-@4.60 + R114 + SENSOR_EN-@5.61 + FID1-0.6); TX_IMON-move cascades into closed nets.
- Pin_4 @7.30-hop KILLED (TX_IMON-N-S x=20.61 + TX_EN-via (19.88,7.10) pincer); @7.60 KILLED (P0.12-N-S tip 0.025); @6.70 kills S2_MOT-razor (mutual exclusion); @13.40 KILLED (TX_IMON-x=16.80 + S1_MOT-diag + S1_MOSI); @14.40 needs 3 hops (TX_IMON+P0.29+S1_MOSI); @6.45-razor FITS S1_NCS-@6.85 (gap 0.20 exact) BUT east-rise x=28.40 CROSSES @6.85 and east-around dies at S2_MOT-island clearance 0.15.
- S1_NCS-high-road @7.325+ LENGTH-KILLED (+1.6 over +1.1 budget); S1_NCS-@6.85-re-take is length-identical (zero-risk) but blocks Pin_4-rise and S2_MOT-lane.
- Band slot accounting y[5.5,7.9]: S2_MOT slot INVERTED 0.035 even with R114 removed (SENSOR_EN-@5.61 vs SPI-0.6); only S1_NCS-alone fits (status quo ante).
CONCLUSION: S1_NCS-@6.85 + Pin_4-east + S2_MOT-lane are pairwise-fittable but TRIPLY MUTUALLY EXCLUSIVE. The rip is reverted net-zero (`git checkout ef13502`, drc186 = drc184 = 14/0/0). S2_MOT stays OPEN by proof (14 lane-proofs). REMAINING CLOSABLE: P0.12-west, Pin_2, BTN3-west, S2_MOSI-south, +3V3s, VINs, VBUS, VSEN, FTH, MCU_TX_ENx2, VBUS_SENSE, MCU_RST-w, GND-3 — each needs its own lane design against the RESTORED band (no commons with the knot except P0.12/S2_MOSI-south, whose lanes were surveyed pre-rip and stand).

### 7.10.9 BLOCKED: all 14 opens proven sealed — schematic pin-reassignment ECO required
P0.12-north final proof (this turn): hop-1 via-slot DEAD (MCU_RST-N-S x=28.70 + S2_MOSI-N-S x=28.90 wall pair, slot inverted); hop-2 DEAD (D+ full-span spine + S1_MISO 0.95-gap sandwich, corridor inverted); S2_MOSI-south IMMOVABLE (MCU_RST-east wall + P0.12-N-S-west wall). P0.12 SEALED.
0R verify: R113/R114/R115 self-pairs by design (no opens); R515 series CTD_U501->Net-(U501-CTD) (CTD closed drc142).
FULL SEAL LEDGER (14/14): S2_MOT (14 lane-proofs §7.10.6/§7.10.8) | P0.12 (WaveC/D + §7.10.4 + §7.10.9) | VIN-#7 pin-cage + VIN-#8 (WaveD + §7.10.3/4) | +3V3x2 (GND-ladder/maze + 4-spine §7.10.3/4) | GND-3 (VBUS-cage §7.10.3) | MCU_RST-w (Y201 + 5-spine §7.10.4) | VBUS (WaveC/D + §7.10) | VSEN (sensor-field §7.10.4) | FTH (U501-cage WaveC/D) | MCU_TX_ENx2 (WaveC/D + §7.10) | VBUS_SENSE (WaveC/D + §7.10).
Q6 destructive re-place assessed: U501/U201 moves do NOT break package-relative cages (VIN-#7 EP/CTS/IS+ cage; U201-37/38/39 pin-order cage move together). Oracle-as-advisor exhausted (0/14). Full south-band rip+revert proved triple mutual exclusion.
ONLY REMAINING LEVERS (all owner-escalation per standing directives): (a) schematic pin-reassignment ECO — move caged nets to free pins with lane access (S2_MOT off U201-38; VIN off U501-3; P0.12/VBUS/FTH/MCU_TX_EN/VBUS_SENSETouching firmware mapping = schematic electrical-intent change); (b) via-in-pad/micro-via process exception (JLCPCB cost/process); (c) stackup change (more layers); (d) accept opens (owner forbade: no accepted opens).
RECOMMENDATION: (a) — schematic job reassigns the pin-caged nets; layout then closes them in the freed lanes. Board held at drc186-equivalent 14unc/0err/0parity (HEAD 4203791), tag q6-zone-rework-base intact.

### 7.10.10 Q7 ECO triage verdict: ZERO pin swaps applicable; TP205/R505 moves dead
- S2_MOT->pin41: riser crosses keystone (SPI); all other free pins die at keystone/spines. P0.12: MCU end connected (mid-route gap) — swap no-op. MCU_TX_EN: 106-mm distance, not cage — swap no-op. VBUS_SENSE: all free-pin lanes die. VIN-#7/VBUS/FTH: power/power-IC pins — unswappable; U501-3 DNC is an electrical current-capacity call, ESCALATED unimplemented. Mid-route gaps: no pad involved.
- TP205-move: attempt SHORTED J202-8 (NC pad) + J202-court (first landing); second landing SHORTED R202-1/J202-4/J202-6 (∅2.0 pad vs pin forest) — both reverted net-zero. Exact-courtyard proof: J202-court-east 12.34 + C201-court-west 12.53 = 0.19 slot < 3.08 needed; R202-court blocks south. TP205 IMMOVABLE. MCU_RST-w stays OPEN (3rd proof). LESSON: dn.py omits pads — all landing surveys now pad+courtyard (procedure fix).
- R505-move (FTH): north KILLED (TX_STAT-E-W @18.94 wall + U501-court); west double-touch (C501/U501 courts); south KILLED (EP). R505 IMMOVABLE. FTH stays OPEN.
- NEXT: R111/MCU_TX_EN-north greenfield (N-S x=20.10, tip-gaps verified) + VIN-#7 electrical answer + PINMAP.md written (null-swap documented).

### 7.10.11 MCU_TX_EN greenfield DEAD — R111 GND-caged, LEG-A walled (5 proofs)
LEG-A N-S x=20.10: EMPTY y[16.9,75] but KILLED north (BTN1-diag crossing @87.27, GND-E-W @103.00 full-span, VBUS-E-W @105.50). N-S x=29.35 dodge needs full-corridor survey; EAST-JOIN at every y dies: @121.90 TX_ON-tip overlap, @122.20 U105, @121.10 TX_5V_SW-N-S, @123.75→south GND-E-W @120.00, R111-2 east-approach crosses GND-N-S x=47.66. LEG-B west exit dies (GND-N-S x=47.66; hop needs via-in-pad on R111-2; north/south arounds hit +3V3-x66.72/TX_ON/GND-@117.50). R111-2 UNREACHABLE (GND double-wall + TX_5V_SW + U105). MCU_TX_EN x2 stays OPEN by proof. Q7 CLOSE-OUT: all 14 triaged — pin swaps 0 applicable, placement moves 0 viable (TP205/R505/R111), power-pin DNCs unimplemented (electrical), remainder sealed by survey. Deliverables: PINMAP.md (null-swap + triage), no .kicad_sch change (nothing valid to change — ERC N/A), board untouched 14/0/0.

### 7.10.12 VIN-#7 electrical verdict: U501-3 DNC REJECTED — stays open
LTC4125 = 5 W monolithic AutoResonant full-bridge TX driver, 20-lead 4x5 QFN. Input current ~1.25 A @5 V (~2 A @3 V) shared by 4 VIN pins (1/3/17/20). Floating one VIN pin forces +33% current through the rest with uneven die heating on a thermally-sensitive resonant loop; no datasheet supports single-VIN-float on a multi-VIN power QFN (all same-named power pins must join). DNC-ing U501-3 is electrically unsound — NOT implemented despite the Q7 reassignment order (that order assumed a swappable pin; U501-3 is power). Re-verified unroutable at all widths (VIN min w0.3: west-bridge still dies at CTS-E-W @15.50; east slot 0.275 < 0.7; via-bridge inverted). VIN-#7 stays OPEN pending via-in-pad / stackup / accept-opens owner call. Direct datasheet fetch failed (timeout); verdict rests on first-principles power-pin practice + the part's 5 W rating — owner/schematic job can override with datasheet evidence.

### 7.10.13 4L stackup live (drc189 14/0/0) + Wave-1 results: VIN-#7 + S2_MOT + P0.12 all OPEN on 4L
Stackup: L1 Top sig / L2 GND plane (solid, WaveZ pour) / L3 sig+power (escape layer, GND-referenced) / L4 Bottom sig; 1.6 mm FR-4 nominal (35 um outer / 17 um inner, fab adjusts PP to thickness; confirm at order; no impedance control — no Z-rules in dru). SetCopperLayerCount(4) via pcbnew; layers verified in file; DRC unchanged.
- VIN-#7 inner: placed (closed net!) but SHORTED TX_IMON-riser/via (52.788,18.0) + pad5 + IS+ (survey missed x[52.7,53.1] y[17,18.5]). Redesigns all dead: via-north (TX_IMON-riser/pad5/EP sandwich, corridor inverted), via-south-east (CTS/EP sandwich inverted), west-at-grade (CTS-E-W spans to 51.54). Ripped net-zero. VIN-#7 OPEN (4L no help — 3D cage).
- S2_MOT inner: west-via DEAD everywhere (BTN3-@7.96 full-span + Pin_2-@8.66 + SEN-@8.09 + diags + S1_NCS-F-N-S + TX_EN-via); F-approach dies (SEN/Pin_2 sandwich); via-in-pad still hits BTN3 B-annulus. BTN3-@7.96 immovable (W-diag crosses S1_NCS-F-N-S). S2_MOT OPEN (15th proof).
- P0.12 inner: placed (closed net!) but hit S2_MOSI-pad (pads invisible to dn.py!), S1_MOSI-B-spine x=24.40 (confused with S2_MOSI-x24.54), GND-N-S x=25.31, MCU_RST-@16.96 (window-edge miss by 0.015), S2_MOSI-N-S span (tip-gap fallacy: E-W @16.60 inside span [15.80,16.90]). West-via dead both sides (S1_NCS/P0.29 + P0.29/S2_MOSI/GND sandwiches). Ripped net-zero, drc193 14/0/0.
PROCEDURE (binding): pad-dump in EVERY window (dn.py blind); margin windows >=0.5; distinguish same-x nets; tip-gap only south of tip; reload-verify every save (caught a null round-trip this turn: VIN tracks vanished between place and rip — cause undetermined, reload-check now mandatory).
REMAINING 4L waves: FTH, VBUS, VSEN, VIN-#8, MCU_TX_ENx2, VBUS_SENSE, MCU_RST-w, +3V3x2, GND-3 (each: pad+courtyard survey, via-slot proof, place, DRC).

### 7.10.14 Wave-2 (4L): FTH + VBUS both OPEN — vbus_clearance 0.25 + pad forest
- FTH: F-exit from U501-9 dies (U501-8/10 pad-row + TX_STAT-E-W @18.94 sandwich, corridor inverted). No placement risked. FTH OPEN.
- VBUS: placed v1 (west feed) closed net but hit U201-28-pad (pad-blind!), vbus_min_width 0.5 (stub w0.3), vbus_clearance 0.25 (S2_MOSI walls), missed S1_MOSI-via (28.0,34.225) + +3V3-vias (window too narrow). Ripped 12. Redesign v2 (direct-pad via + N-S x=30.20 inner, all 11 field vias dodged) died at F-jog: U201-26-pad + S2_MOSI-@15.80 sandwich inverted under vbus_clearance 0.25; direct-pad via blocked by MCU_RST-via (28.70,16.40). Ripped 0 (nothing placed). drc195 14/0/0 net-zero.
- RULES LEARNED (binding): vbus_min_width 0.5, vbus_clearance 0.25 (apply to ALL power routing); survey windows must exceed target span by >=1.0; pad-dump mandatory (U201-28-pad, U201-26-pad both missed by tracks-only surveys).
REMAINING 4L waves: VSEN, VIN-#8, MCU_TX_ENx2, VBUS_SENSE, MCU_RST-w, +3V3x2, GND-3.

### 7.10.15 Wave-3 CLOSED: VSEN_1V9 (drc198 13unc/0err/0parity)
U301-4/U302-4 PTH pads via F-stubs (vias ON stubs, not pads: hole_to_hole 0.25 respected at 0.29+); In2-E-W @63.50 w0.25 dodging GND-via field (49.725/57.748/61.15 @64.24, GND (41.23,63.00)); U301-pin3-VDDPIX PTH avoided (E-W south of it, gap 0.715). Iterations: @66.00 (pin3-short + GND-via), @64.90 (2 GND-vias at window edge) -> @63.50 clean. First 4L close. VSEN = Power netclass (clearance 0.2, w0.25 OK).

### 7.10.16 Wave-4a CLOSED: VBUS_SENSE (drc205 12unc/0err/0parity)
- CORRECTION: the west pad (15.60,7.51) is U201-3 (E73 module SMD 1.8x0.5), not J202; J202 = 2x05 P1.27 SMD header at (3.7-12.3,18.3-27.7). VBUS_SENSE = 6-pt divider net: east cluster (R101/R102/TP103/R113) was ALREADY routed via B-backbone to via (58,122.9) + dangling B-end (32.64,122.90, pre-existing); only the U201-3 west link was open.
- DEAD END: F-staircase west (x8.55-15.95) died on TP203 block, J202-Pin_2 rail @9.45 + via (12.2,9.45), P0.28 rail @8.78, U201-4-pad overrun (8 errors drc203); ripped net-zero.
- CLOSED ROUTE: F-stub east from pad edge (16.50,7.51)->(17.50,7.51) (only clear F exit; north/south/west all pad/rail-caged), via (17.50,7.51), In2-E-W @7.51 ->x16.50, In2-N-S x16.50 south to y100.50, BTN2-via (16.10,101.40,d0.8) bypass jog x17.00 (y100.50-102.30), N-S x16.50 ->y122.90, In2-E-W @122.90 ->via2 (58,122.9)->backbone. Iterations: x17.50 N-S died on P0.29-via (17.60,13.86,d0.8) + TX_IMON-via (17.26,16.12) (drc204 2 shorts); slalom x16.50/x17.00 clean (drc205 0 errors, VBUS_SENSE absent from unconnected list).
- RULES LEARNED (binding): probe VIAS + PTH pads in every inner-layer window (tracks-only probes miss pierce-throughs); after ANY b.Remove loop, the next b.Tracks() call may return non-iterable garbage -> single-pass snapshot scripts only (one list(b.Tracks()) per process); reload-verify counts every save (caught phantom duplication: 4 In2 instead of 2, truncated-iteration reads in between); F-window surveys must cover the FULL corridor, not just via endpoints.
REMAINING waves: VIN-#8, MCU_TX_ENx2, MCU_RST-w, +3V3x2, GND-3, VBUS, VINx2, FTH, P0.12, S2_MOT (12 items / 9 nets).

### 7.10.17 Wave-4b VIN-#8: east link placed-then-ripped (L501-2 overlap); wall proven COMPLETE on In2
- CONTEXT: VIN islands = {A+B: U501 pads 1/17/20 + west network, joined at F (53.60,14.06)} vs {C: east (67.52 F + via (73.49,14.00) + B-backbone @15)} vs {pad3 alone}. U501-3 (53.06,16.00) sealed on F (CTS rail west, GND-thermal east, IS+/CTS pads N/S).
- PLACED: In2 E-W @12.70 jog + N-S x55.60 + E-W @11.05 + riser x73.49 (w0.30, within proven VIN widths). drc206: 11unc (B-C CLOSED!) + 1 SHORT: E-W ran THROUGH L501-2 pad solid copper (box y8.50-11.50; inside-span overlap, not edge gap — LESSON: for pads, test containment (track-rect vs pad-rect overlap), never distance-to-far-edge).
- RIPPED net-zero drc207 12/0/0. WALL PROOFS (In2, w0.30): @11.85+ vs SW2-row inverted; south y<=8.15 mined (TX_STAT/FB_PK/D501-A); basement y<=7.07 vs R512/SW201 inverted; x55-gap slalom dies at TX_STAT-via turn (0.00 exact); x59.50 pocket (FB-via); x60.00 (TX_STAT-via); x61.15 (TX_STAT/SW2 pair inversion); north tiled (U501 thermals + CTD row). F/B previously sealed (ledger §7.10.3/4).
- PLAN: grand tour — In2 west @12.70 from (56.00,12.70) to clear x, south in clear zone, east along bottom edge (y<5), north up riser x73.49 (clear y8-14 verified; y5-8 partially). Needs 3 probes (west span vias/PTH, south corridor, bottom span). Width: prefer w0.50 inner for VIN current if space allows. Pad3: separate micro-wave (CTS re-route or accept-open escalation).
REMAINING: 12 items / 9 nets (VINx2 incl. pad3, MCU_TX_ENx2, MCU_RST-w, +3V3x2, GND-3, VBUS, FTH, P0.12, S2_MOT).

### 7.10.18 Wave-4b CLOSED (2nd attempt): VIN B-C grand tour (drc208 11unc/0err/0parity)
- ROUTE (all In2 w0.30, 6 segs, all verified persisted): E-W @12.70 (56.00->55.00) [SW2-via gap 0.53] + N-S x55.00 (12.70->8.10) [L501 gap 0.89 both sides] + E-W @8.10 (55.00->40.00) [L501-1 bottom gap 0.25, west-under EMPTY] + N-S x40.00 (8.10->4.00) [EMPTY] + E-W @4.00 (40.00->73.49) [bottom vias clear, min gap 0.13 over TX_STAT-via; 4.1 from board edge] + N-S x73.49 (4.00->14.00) [meets existing VIN via barrel; riser-low EMPTY].
- Probed EMPTY (vias+PTH): west-under x35-51 y7-9.5, south-drop x38-42 y3-8.5, riser-low x72.5-74.5 y4-11. Bottom span x40-74 y3-6 holds only 3 vias (TX_EN x2, TX_STAT) threaded @4.00.
- NOTE: VIN inner width w0.30 (DRC-legal, matches existing stubs) but below the w0.50 of F/B power runs — flag for power-integrity review at WaveZ (upgrade to w0.50 if space allows; current path carries VIN across ~150 mm inner).
- VIN REMAINDER: pad3 micro-wave only (F-sealed; CTS re-route or escalation).
REMAINING: 11 items / 9 nets (+3V3x2, GND, MCU_RST, VBUS, VIN-pad3, FTH, MCU_TX_ENx2, P0.12, S2_MOT).

### 7.10.19 Wave-4c MCU_TX_EN (IN PROGRESS): F-escape from U201-28 SOLVED, long link pending
- F-ESCAPE (w0.25, all gaps computed, NOT yet placed): E-W @14.60 (25.98->23.75) [dodges P0.12 diagonal east tip (23.27,16.17) by 0.255; BTN1-@15.13 gap 0.28] + N-S x23.75 (14.60->16.65) [tip dx-gap 0.255; S2_MOSI-x24.54 gap 0.565] + E-W @16.65 (23.75->20.30) [tip dy-gap 0.255] + via d0.6 (20.30,16.65) [B-side clear: P0.29-@13.88 dy 2.77, BTN1-B tip dist 1.67, S2_NCS-via dist 0.82]. KILLED alternatives: direct @14.49 (P0.12 tip, 0.125<0.2); @14.70 (BTN1-F 0.18); @14.90 (BTN1-F overlap); via (20.30,14.40) (B-P0.29 rail 0.095); d0.6 via band between B-P0.29-@13.88/F-BTN1-@15.13 is exactly zero-width (14.505). PENDING: F-pads probe at jog corners (x20-24 y14.5-16.8) before placing.
- LONG LINK (U201-28/R111-2/R115-1, ~100 mm, both pairs open): options: (i) In2 south from (20.30,16.65) to R111-2 (47,118.675) — needs full x20-47 y16-119 via/PTH survey; (ii) bottom-route E-W @4.50 In2 parallel to VIN-@4.00 (gap 0.225) + riser to R115-1/R111 — needs riser probes; (iii) R111-2->R115-1 first (both SE, 45 mm, x47-91 y100-119 survey). R111-2 exits: south blocked (R111-1 TX_ON), west corridor to R112 unprobed.
REMAINING: 11 items / 9 nets.

### 7.10.20 Wave-4c CLOSED: MCU_TX_EN (drc211 9unc/0err/0parity)
- LINK A (U201-28->R111-2): F-escape v3 = E-W @14.20 (25.98->24.60) [S1_MOT-B-diag gap 0.515; pad30/TX_EN-rail clear] + via d0.6 (24.60,14.20)?? NO — v1 via SHORTED S1_MOSI-B-N-S x24.40 (B-rail y10.82-20.68 found only in FULL dump; head-truncated probe missed it — LESSON: never head-limit net dumps). KILLED: west jog (P0.12 tip+pad row), east lane (D- via (30.50,13.86) + VBUS-rail sandwich; B D-/D+ rails tile x30.5-34.2), south lane (pad boxes inverted), via (20.30,14.40)/(20.30,16.65) (B-P0.29 rail / P0.12 tip). FINAL: via-in-pad d0.6 (26.30,14.20) overlapping U201-28 box (S1_MOT-diag gap 0.128; S1_MOSI-via (26.11,34.23) forces N-S back to x24.60) + In2 E-W @14.20 jog (26.30->24.60) + In2 N-S x24.60 (14.20->118.675, min gap 0.495) + In2 E-W @118.675 (24.60->47.00; GND vias clear) + In2 N-S x47.00 stub + F micro-stub + via-in-pad d0.6 (47.00,119.30) [B-GND-rail x47.66 gap 0.235; R111-1 box gap 0.32; d0.5 rejected: annular 0.125 < 0.15 global]. KILLED R111 alternatives: west via (TX_5V_SW-B-rail x46.14 + R112-1 pinch inverted), east via (GND-B-rail x47.66 + R106-2 pinch), south via (R111-1 box overlap).
- LINK B (R111-2->R115-1): In2 E-W @119.10 (47.00->91.175) [VBUS-via (59.30,118.10) dodged by moving off @118.675; all-span gaps >=0.375] + N-S x91.175 (119.10->100.00, EMPTY span) + via-in-pad d0.6 (91.175,100.00) [B-side EMPTY, R115-2 gap 1.245]. drc211: 0 errors incl. no mask-bridge on either via-in-pad.
- FAB NOTE: 2 via-in-pad (26.30,14.20 + 91.175,100.00; 47.00,119.30 is pad-adjacent not in-pad): tent/plug at fab or accept wicking risk — record in fab notes at WaveZ.
REMAINING: 9 items / 8 nets (+3V3x2, GND, MCU_RST, VBUS, VIN-pad3, FTH, P0.12, S2_MOT).

### 7.10.21 Wave-5 +3V3: gap-b CLOSED, gap-a PARKED-SEALED (drc222 8unc/0err/0parity)
- GAP-B CLOSED: F-lead (26.50->27.10 @23.60) + via d0.6 (27.10,23.60) + In2 E-W @23.60 (27.10->35.70) + riser x35.70 + via d0.6 (35.70,26.60) + F-lead (35.00->35.70 @26.60). Iterations: v1 died on S1_MOT-diag/S1_MOSI-x33.20/P0.29-N-S (B-rail endpoint-distance probes miss diagonals — LESSON: point-SEGMENT distance mandatory for diagonal rails); v2 died on S1_NCS-x34.15 (probed riser not via site — LESSON: probe every via site) + hole_to_hole vs existing via (35.00,26.60) (0.10 apart — LESSON: probe existing vias at riser tops).
- GAP-A PARKED-SEALED (maze<->x25.00-spine, 1 open): 5 failed placements (west-F/GND-rail, In2+N-SLALOM, C207-1-via (P0.29-N-S + MCU_RST-F-rail), @12.20-south (TX_EN-via), over-the-top-F (MCU_RST-@30.075 + S1_MOSI-@34.23)). PROVEN SEALED: F (GND-x23.90 solid), B (S1_MOSI-x24.40/24.90 full-height), In2-west (TX_EN-via+spine+jog), In2-north (S1_MOT-diag + MCU_RST-maze + C207-2), In2-south (TX_EN-via + U201-17-pad pinch, bands inverted at all widths). GND-RAIL-REMOVAL ECO experiment: rail is LOAD-BEARING (GND 1->2 opens) — REVERTED byte-exact (w0.25 verified via git diff). LESSONS: never head-limit net dumps (missed S1_MOSI-B-rail); rip-match direction-agnostic (sorted endpoints); record placed endpoints verbatim (33.10 vs 33.60 rip miss); inner-vs-outer layer non-interaction both ways (F/B tracks never block In2 spans; only vias/PTH/holes pierce).
- CLASS: gap-a joins VIN-#7/S2_MOT as ECO-or-escalation (placement ECO of GND-maze/S1_MOSI-spine, or schematic relief). NOT attempted further this wave.
REMAINING: 8 items / 8 nets (+3V3-gap-a, GND, MCU_RST, VBUS, VIN-pad3, FTH, P0.12, S2_MOT).

### 7.10.22 Wave-6 CLOSED: GND (drc225 7unc/0err/0parity)
- CLOSED: In2 E-W @124.70 (55.90->59.27, EMPTY span) + N-S x59.27 stub (124.70->124.00), reusing both existing GND via barrels. 2 segs, first-try clean.
- KILLED: B-south-around (N-S x56.70 crossed VBUS-@123.70 — forgot N-S crosses the rail it avoids; E-W @122.30 died on VBUS_SENSE-via barrel (checked tip copper, forgot barrel — LESSON: via sites = barrel + copper)); B-north-around (VBUS-N-S tip higher than surveyed (129.10 not 128.20 — LESSON: re-verify rail tips from full dumps, not memory; J201-SH PTH 0.195; VBUS-via (58.40,128.50)).
- LESSONS: survey B-rail tips exactly (length/endpoint, not assumed); every via site needs barrel-aware B-check; N-S segments cross E-W rails they parallel-avoid (check both orientations).
REMAINING: 7 items / 7 nets (+3V3-gap-a, MCU_RST, VBUS, VIN-pad3, FTH, P0.12, S2_MOT).

### 7.10.23 Wave-7 FTH PARKED-SEALED (pad-cage class, no board change)
- U501-9 (55.50,17.94) box (55.38-55.62, 17.52-18.35): F-sealed all sides (W: TX_STAT-pad8 gap 0.26; E: empty-pad10 gap 0.26; S: TX_STAT-rail @18.94; N: chip). No d0.6 via fits: between-pad9/10 band 0.26 < 0.5; south-overlap dies on pad10-corner + TX_STAT-N-S x55.03; far island via (60.01,32.00) PROVEN CLEAR (B-empty, F-clear) but unreachable. In2 corridor x54-62 y18-33 probed (6 vias, no PTH). Relief needs schematic: move FTH off pin 9 / move TX_STAT / DNC-pad10 ruling (NOT layout craft — pad10 is a footprint pin).
REMAINING: 7 items / 7 nets (+3V3-gap-a, MCU_RST, VBUS, VIN-pad3, FTH-sealed, P0.12, S2_MOT).

### 7.10.24 Wave-8 CLOSED: MCU_RST (drc230 6unc/0err/0parity)
- PATH: J202-10 → F-west (exists) → B-rail @19.70 (exists) → EXISTING via (13.025,19.705) → In2 N-S x13.025 (19.705->22.10) + E-W @22.10 (13.025->14.90) + N-S x14.90 (22.10->31.00) + E-W @31.00 (14.90->15.70) + via (15.70,31.00) + F-hop (15.70->17.30 @31.30) + via (17.30,31.00) + E-W @31.00 (17.30->22.30) + via (22.40,31.00) + F-N-S x22.30 (30.05->31.00) + F-E-W @31.00 (21.50->22.30) + maze @30.05 (exists) → TP205. 3 iterations (west-via C201-hole + J202-Pin_4-B-rail; hop-vias vs SENSE-spine + endpoint proximity; missing layer transition at x22.30).
- LESSONS: probe-box edges bite (vias 40µm outside missed: +3V3 (13.0414), P1.11 (11.962)); my own full-height spines (VBUS_SENSE x16.50, TX_EN x24.60) are uncrossable walls on In2 — plan hops BEFORE placing (F-jog over, vias ≥0.625 from spine, E-W ends ≥0.45 from spine); verify every layer transition explicitly (F-to-In2 needs a via AT the junction); reusing existing vias/rails beats new copper (their-via (13.025,19.705)); crystal-zone caution (C201/Y201 pads constrain west entry; reset line passes In2 under crystal zone — note for review).
REMAINING: 6 items / 6 nets (+3V3-gap-a, VBUS, VIN-pad3, FTH-sealed, P0.12, S2_MOT).

### 7.10.25 Wave-9 CLOSED: VBUS (drc234 5unc/0err/0parity)
- PATH (all w0.5, vbus 0.5/0.25 rules): via d0.8 (36.23,15.00) [on C205-1 pad + rail tip; B: S1_NCS-tip gap 0.268] + In2 E-W @15.00 (36.23->31.50) + In2 N-S x31.50 (15.00->105.50, with jog (22.70/24.50 via x26.20) around own +3V3-E-W @23.60 tip) + In2 E-W @105.50 (29.50->31.50) + F-E-W @105.50 (29.50->31.50) + via d0.8 (29.50,105.50) [on B-corner] → south B-network. 3 iterations (N-S through +3V3 track same-layer; jog too tight for vbus 0.25; riser 2mm short of transition via — LESSON: trace every junction to a via barrel, endpoint-meets-track across layers does NOT connect).
- LESSONS: vbus_clearance 0.25 (not 0.2) changes all margins (0.75/0.80/0.90 spacings); east band x30.5-32.5 fully EMPTY (90mm clear shot); F x29.5-31.5 @105 EMPTY.
REMAINING: 5 items / 5 nets (+3V3-gap-a, VIN-pad3, FTH-sealed, P0.12, S2_MOT).

### 7.10.26 Wave-10 CLOSED: P0.12 first-try (drc235 4unc/0err/0parity)
- PATH: B-N-S x21.23 bottom (21.23,7.75, exists) + via d0.6 (21.23,7.75) [B: S1_NCS-@6.85 gap 0.375; F: EMPTY] + In2 E-W @7.75 (21.23->39.30) [S1_NCS-via 0.095, SENSOR_EN-via 0.225, J202-Pin_2-via 0.185 — all legal] + In2 N-S x39.30 (7.75->18.50) [BTN3-via 0.285, GND-via 0.95] + In2 E-W @18.50 (39.30->38.80) + via d0.6 (38.80,18.50) [TX_IMON-F-rail 0.125] + F-N-S x38.80 (17.77->18.50, touches R207-2 top) [R207-1 (S2_SCK) gap 0.97]. KEY FINDS: east island terminates at R207-2 (not a stub); B-rails never block In2 spans (only vias/PTH pierce) — the B-route detour analysis was wasted effort, In2-direct was always the answer.
- LESSON: for In2 spans, probe ONLY vias/PTH/holes (never B/F tracks); R-pad terminations (R207-2) hide island ends — always check both islands' far pads.
REMAINING: 4 items / 4 nets (+3V3-gap-a, VIN-pad3, FTH-sealed, S2_MOT).

### 7.10.27 Wave-11 S2_MOT PARKED-SEALED (pad-cage + corridor-mined, no board change)
- Pad38 (26.40,8.14) box (25.98-26.82, 7.72-8.57): N-gap 0.42 (S1_MOT-pad36), S-gap 0.42 (TX_STAT-pad40) both inverted for w0.25; E-lane @8.60 dies on SENSOR_EN-@8.09 (band [8.60..] vs via (27.175,9.00) needs 0.625: 0.51/0.71/0.81/0.91 all fail below 9.00; at 9.00 B-rail check pending but F-lead @8.60/ N-S x27.175 cross SENSOR_EN-rail). E-via (27.175,9.00) planning only.
- Corridor x27-44 y9-37 (In2): N-S x27.175 dies on +3V3-via (27.20,20.45); x28.40 dies on MCU_RST-via (28.70,16.40) (band [28.05,28.075] 25µm); E-W @9.00-9.60 dies on SENSOR_EN-via (33.90,8.60)/BTN3-via (38.39,10.00) inversion; E-W @7.70 dies on S1_MISO-via (33.20,10.05); N-S x32.40-33.90 dies on S1_MISO/SENSOR_EN-via pinch; x29.50-spine dies on 12 stacked vias + own +3V3-E-W @23.60. Consistent with 14 prior 2L proofs; 4L adds no path (vias pierce all layers).
- CLASS: schematic relief (reassign S2_MOT off pin 38, or move SENSOR_EN-rail/BTN3-via — latter is placement ECO with ripple; former is schematic-intent).
REMAINING: 4 items / 4 nets, ALL SEALED class (+3V3-gap-a §7.10.21, VIN-pad3 below, FTH §7.10.23, S2_MOT here).

### 7.10.28 SEALED BATCH — 4 opens need schematic relief (escalation)
1. +3V3-gap-a (maze<->x25.00-spine, 2mm): walled F (GND-x23.90 solid), B (S1_MOSI-x24.40/24.90), In2 (TX_EN-spine/via/jog, U201-17-pad, P0.29/S1_MOSI pinch, S1_MOT-diag). GND-rail ECO rejected (load-bearing). Relief: move GND-x23.90 pair with GND-stitch plan, or schematic tie.
2. VIN-pad3 (U501-3): pad2/pad4/thermal-west/CTS-diagonal seal all via slots (0.26 gap fits nothing). Relief: move VIN off pin 3 (pins 1/17/20 already VIN), or CTS re-route + ripple.
3. FTH (U501-9): pad8/pad10/TX_STAT-rail seal; DNC-pad10 ruling needed. Relief: move FTH off pin 9, move TX_STAT, or DNC-pad10 use ruling.
4. S2_MOT (U201-38): pad-cage + mined corridor (above). Relief: reassign off pin 38, or move SENSOR_EN-rail/BTN3-via.
- VIN inner widths (w0.30 grand tour) + via-in-pad ×3 (26.30,14.20 / 47.00,119.30 / 91.175,100.00 — all DRC-clean, no mask-bridge) flagged for WaveZ review (power-integrity + fab tent/plug notes).

### 7.10.27 Wave-11 S2_MOT PARKED-SEALED (pad-cage + B-mined + via-in-pad dead, no board change)
- Pad38 (26.40,8.14) box (25.98-26.82, 7.72-8.57): N-gap 0.42 (S1_MOT-pad36), S-gap 0.42 (TX_STAT-pad40) both inverted for w0.25 (need 0.65); E-lane @8.57 dies on SENSOR_EN-@8.09 + pad36/S1_MISO 30µm inversion (x27.10-27.30 band); W dies on J202-Pin_2 F-N-S x24.20 crossing.
- B-layer: BTN3-B-E-W @7.96 (23.99-36.15) parallels whole zone (dy=0.18 from any B-copper at pad y); J202-Pin_2 B-maze (@8.66/@8.81) walls east; via-in-pad (26.40,8.14) probed vs ALL pads + B-tracks + vias: BLOCKED by BTN3-B (0.079 < 0.5). North-edge via razors into S1_MOT-pad36.
- West-In2 corridor (x23.65 + P0.29-jog + @37.20) exists but UNREACHABLE: no via slot connects pad38 to any inner/B layer.
- CLASS: schematic relief (reassign S2_MOT off pin 38, or move BTN3-B-rail/SENSOR_EN-rail — placement ECOs with ripple; reassignment is schematic-intent).
REMAINING: 4 items / 4 nets, ALL SEALED class (+3V3-gap-a §7.10.21, VIN-pad3, FTH §7.10.23, S2_MOT here).

### 7.10.29 Wave-12 relief (1) +3V3-gap-a BLOCKED — placement ECO exhausted (no board change)
- Tried: In2-hop @19.80 (via 22.50 + In2-span + via 25.20) PLACED then RIPPED on DRC regression (4 errors: In2-span crossed own TX_EN-In2-spine x24.60 (104mm wall, forgot Wave-8 lesson); east via vs TX_EN 0.175; 2x annular_width — my d0.6/w0.6 nonstandard vs board convention d0.4/w0.8 + d0.3/w0.6). REVERTED via git checkout (tree = drc236). LESSONS: verify script must check In2-vs-In2 tracks (not just vias/PTH); use census via sizes only (d0.4/w0.8, d0.3/w0.6).
- Then proved: GND-rail (x23.90 + @24.60) is the single F-wall; B has two walls (P0.29-x23.34, S1_MOSI-x24.40/24.90 — corner @20.68, NOT full-height as previously recorded); In2 has one wall (TX_EN-x24.60 14.20->118.67). Double-hop needs transition via in P0.29/S1_MOSI pinch band [23.94,23.775] — INVERTED (need 1.225, have 1.06). Relocation slots all pinched: west x21.8-22.0 (S2_MISO-x21.36 vs +3V3-stubs/U201-pad), east x24.8+ (tip/spine/@20.45), x28 (spine-tip/maze inversion), jogs (all cross). South maze is rail-fed ONLY (BFS: 11 nodes isolated without rail; no B/In2-GND, no vias near maze). Every stitch re-feed crosses +3V3's closure (circular). @29.00-east dead (GND-hook + S2_MOSI-F-x28.90 full-height + MCU_RST-maze). North detour (60mm+) rejected on PWR-002 PI grounds.
- FOUND but unusable: +3V3 dead-copper island at y26 (x23.35-N-S to @29.00, @26.0 cluster) — no via, dangling B-end (22.63,26.5) killed by P0.29 (0.11). Usable only with schematic-tie-class rework.
- REMAINING OPTION (not authorized): schematic tie west<->east island, or move S2_MISO-x21.36 rail (outside relief scope). CLASS: schematic-intent. STOPPING on this item per HARD RULE.
REMAINING: 4 opens (+3V3-gap-a BLOCKED, VIN-pad3, FTH, S2_MOT).
