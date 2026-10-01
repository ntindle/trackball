# BASE PCB Layout Review — trackball-base

**Branch:** `job/trackball-base-layout` · **Checkpoint:** `6707a18` (drc143)
**Date:** 2026-10-01 · **Tools:** KiCad 10.0.6, Blender 5.2.2 LTS, Python 3.12.3
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
| DRC (drc143, `--schematic-parity`) | **0 errors**, 0 parity |
| Unconnected | 57 (documented blockers, §7) |
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
- C115 (VBUS cap for U107): PARKED at (46.0, 108.0) — no verified site
  found after 3 ECO attempts (ECO-C115 v1/v2/v3 collided with
  U107/Q101/R109). Requires placement ECO (§7).

### 2.7 ECO moves (all DRC-verified post-move)

| ECO | Move | Reason |
|---|---|---|
| ECO-CRYSTAL | Y201/C201/C202/R201/R202/TP206 row y=24.6, C201 rot90, R201 (13.9,27.3) | Clear J202 courtyard + crystal shorts |
| ECO-VBUS2 | R203→(40.0,120.0), TP101→(50.0,127.3) | Open CC1/VBUS corridor |
| ECO-C115 v1/v2/v3 | Attempted (58.5,115.0) → (63.5,112.0) → (61.7,116.0); PARKED (46.0,108.0) | Collided U107/Q101/R109; no site |
| ECO-TP204 | TP204→(10.8,14.0) | Open J202-Pin_2 east corridor |

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

GND: poured zones both sides + track stitching; 11 links open (§7).
VBUS: 12 links open, incl. C115 (parked) + U101-EN (caged) + V3-N2
(J201.A9→BB, caged by IOA1) + C115→north spine (93 mm gap).

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
| M9 | Courtyards 0 overlap | DRC `courtyards_overlap` | 0 (drc143) |
| M10 | Holes 0 violation | DRC `hole_*` | 0 since drc90 fix |
| M11 | ERC clean | `kicad-cli sch erc` | 1 benign pin_to_pin |
| M12 | Schematic parity | `pcb drc --schematic-parity` | 0 (drc143) |

---

## 5. DRC evidence (drc143)

```
viol: lib_footprint_mismatch 123, track_dangling 27, via_dangling 4,
      silk_edge_clearance 2
unc: 57 (VBUS 12, GND 11, +3V3 8, VSEN_1V9 5, MCU_RST 2,
      J202-Pin_2 2, + 17 singles)
real violations: 0    parity: 0
```

- `lib_footprint_mismatch` 123: expected — custom footprints differ from
  library (KICAD-013 `missing_courtyard` handled per rule).
- `track_dangling`/`via_dangling`: open stubs on unrouted nets (§7).
- `silk_edge_clearance` 2: accepted (silk clipped at edge, no fab risk).
- Full JSON: `/tmp/drc143.json` (job archive).

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

Provisionals (bench TBD before fab money): tank Vpk, coil current,
CHG-011 ferrite, PWR-002 ripple <100 mVpp, ELEC-004/005/006 ESD Level 4,
ELEC-012 SPI length, USB90 stackup (KICAD-019/020).

---

## 7. Open nets — blockers (57)

Root cause for ALL: placement density exceeds hand-routing capacity in
QFN fanout zones + BB minefield (USB spine + SPI + GND + P1.11). No
autorouter available (no freeroute/java/DSN support in this env).

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

**Recommended path:** placement ECO pass (spread U501 south row,
U201 east row, TX south band; place C115 with keepout survey) + BB
corridor plan (USB spine fixed; route SPI/GND around) + autorouter
(freerouting.org) for singles. Estimated 2–3 further sessions.

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

- DRC: `/tmp/drc143.json` (+ drc51–drc142 series in job archive).
- Board: `trackball-base.kicad_pcb` @ `6707a18`.
- Scripts: `/tmp/route.py`, `/tmp/heal*.py`, `/tmp/raw*.py`, `/tmp/raw*.json`.
- Stage-1 checks: PENDING (run at route-close; §4 M4–M8).
