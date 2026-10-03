# BASE PCB Layout Review — trackball-base

**Branch:** `job/trackball-base-layout` · **Checkpoint:** drc127 (unc26/0err/0parity; TP305/306 ECO + U2 closed; was drc126 unc27)
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
| GND | Poured zones both sides + 8 mm stitch intent (KICAD-019) |
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

E73 module on REAR (opposite USB-C FRONT) with antenna keepout poured
clear on both layers. Keepout verified by script (§4).

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

GND: poured zones both sides + track stitching.
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
| M4 | Antenna keepout clear | `check_antenna_keepout.py` | PENDING Stage-1 run |
| M5 | Coil keepouts (5 mm / 0.8 mm) | `check_coil_keepouts.py` | PENDING Stage-1 run |
| M6 | Sensor geometry 80–100° | `check_sensor_geometry.py` | PENDING Stage-1 run |
| M7 | Ball socket / base stability | `check_ball_socket.py`, `check_base_stability.py` | PENDING Stage-1 run |
| M8 | Buttons + USB placement | `check_buttons_usb.py` | PENDING Stage-1 run |
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

---

## 8. Rule citations (index)

ELEC-002/004/005/006/012/027/029, CHG-009/011, PWR-002, MECH-006/049,
TOUCH-001, KICAD-011/013/019/020/022, SENSOR_SELECTION, SCROLL_UX_DESIGN,
FINAL_SPEC Rev 3.1, RULES.md (normative). E-series deviations E13.2–E49
per devlog (`/tmp/devlog.md`, merged above).

---

## Appendix A. Assumptions

1. D2FC plunger-side orientation assumed (MECH to confirm).
2. U101 EN tied to VIN externally (AP2112K standard; route open).
3. D501/D502 package TBD — footprint provisional.
4. USB90 0.25/0.20 GCPW provisional pending stackup sim.
5. All PROVISIONAL values require bench before fab.
6. Partial route accepted for this checkpoint; §7 is the work list.

## Appendix B. Evidence files

- DRC: `/tmp/resume_drc127.json` (+ drc18–drc127 series in job archive).
- Board: `trackball-base.kicad_pcb` @ drc127 (job/trackball-base-layout).
- Scripts: `/tmp/raw.py`, `/tmp/ripbatch.py`, `/tmp/svbatch.py`,
  `/tmp/audit.py`, `/tmp/q*.py`, `/tmp/p*.json`, `/tmp/rb*.json`,
  `/tmp/drc.sh`, `/tmp/freerouting-2.4.1.jar` (+ Temurin JRE 25).
- Stage-1 checks: PARTIAL (M4–M8 need route-close; blocked Q5/Q6).
- Blockers: `notes/QUESTIONS.md` (Q5 schematic-ECO 4 pads, Q6 placement).
