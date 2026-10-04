# BLOCKED Questions — trackball-base layout (job/trackball-base-layout)

**Date:** 2026-10-03 (triage) · **DRC:** drc128 (0 errors, 0 parity,
26 unconnected — item-for-item identical to drc127; board unchanged)
**Prior:** Q1–Q4 owner-approved 2026-10-02 (placement ECOs, freerouting.org,
via/placement micro-moves, Blender-manual). This file asks ONLY what exceeds
that authority: schematic-intent + destructive placement rework.
**Resolved:** TP305/TP306 micro-move DONE drc127 (ECO4 + P131, U2 closed —
see below). Q5 APPROVED + EXECUTED (Q5 ECO, SCHEMATIC_REVIEW §11). Q6
APPROVED — destructive re-place IN PROGRESS (no accepted opens).

## Q5 — Schematic ECO: alternate taps for 4 unroutable pads (APPROVED + EXECUTED 2026-10-04)

4 nets are unroutable because BOTH endpoints are caged by fixed adjacent
pads/traces no layout move can clear (verified by survey + ripup-attempt +
independent freerouting.org run stuck with no progress):

| # | Net | Pad A (cage) | Pad B (cage) | Why unroutable |
|---|---|---|---|---|
| 1 | `/tx/Net-(U501-CTD)` | U501.14 (U501 0.5-pitch QFN: U501.13-FB 0.5 N, U501.15-EN 0.5 S — 0.25 track + 2×0.2 clr = 0.65 > 0.5 gap, unthreadable) | C507.1 (C507.2-GND 0.96 W: below-row 0.065 clr SHORT, on-row OVERLAP, above-row 0.065 SHORT — 3-sided cage) | Both ends pad-caged. Ripup of TX_STAT/SW2/FB corridor attempted (rb36/P109): CTD placed then SHORTED vs C507.2 (0.065), TX_STAT-via (OVERLAP), D501-A-x=66.2 (crossing). Reverted (rb39/P112). Moving C507 N fails (W-end still caged by U501.13). Moving U501 breaks 20 routed nets. |
| 2 | `VBUS_SENSE` | U201.3 (U201 QFN row: adjacent-pin cage, no fanout) | R-triple + B-E-W-y=122.9 (ends mid-board, 115 mm gap across USB/SPI/GND maze) | 115 mm pad-to-stub gap across routed maze; both ends caged. |
| 3 | `SENSOR_EN` | U201.42 (U201 QFN row: TX_STAT-x=25.4 W-cage (0.4 clr), U201.40-TX_STAT N-cage (OVERLAP)) | R103.1 (R103.2-GND E-cage (OVERLAP)), U104.3 (GND-cage (N-S-x=28.363 crossing, E-W-y=87.0 OVERLAP)) | All 3 sensor-end taps caged; MCU-end caged. N-stub attempt SHORTED vs BTN1/R401.2 (ripped). |
| 4 | `MCU_TX_EN` | U201.28 (U201 QFN row cage) | R111.2 (mid-board, 104 mm gap across routed maze) | 104 mm pad-to-pad gap across routed maze; both ends caged. |

**Owner decision 2026-10-04:** option (b) — Q5 schematic ECO APPROVED
(no accepted opens). EXECUTED: R113 (VBUS_SENSE), R114 (SENSOR_EN),
R115 (MCU_TX_EN) 0R branch jumpers on power sheet; R515 (CTD) 0R in-line
on TX sheet (CTD split into `/tx/CTD_U501` + `/tx/Net-(U501-CTD)`).
ERC 0 errors + 1 benign warning; netlist diff verified minimal (§4-net
only). See SCHEMATIC_REVIEW §11 + LAYOUT_REVIEW E53.

## Q6 — Destructive placement ECO: re-place U501/C106/U201/R202/C203/C507/D501/D502 (APPROVED 2026-10-04 — IN PROGRESS)

22 remaining nets (Q6-remainder; TP305/TP306 U2 FIXED drc127) are
unroutable due to FIXED-pad cages a placement ECO could clear, but every
candidate move breaks already-routed nets (ripup verified necessary, not
attempted — destructive):

| Cage | Nets blocked | Move needed | Breaks |
|---|---|---|---|
| U501 QFN 0.5-pitch (U501.2-CTS/U501.3-VIN/U501.13-FB) | VIN U15/U16 (IS+/U501.2), FTH U18 (maze incl U501.9) | Move U501 ≥1 mm | 20 routed nets (FB/SW2/EN/CTD/GND/VIN/FTH/NTC/DTH/…) |
| C106.1/C106.2 (0.9 gap, w0.5 needs 1.0) | VBUS U12 (C118.1↔N-S-x=59.3) | Move C106 ≥0.5 mm | VBUS/GND/+3V3 mesh (U7/U8/U9/U11 cluster) |
| U201 QFN row (S2_MOSI/U201.28/GND-x=23.9) | +3V3 U0/U1, VBUS U10, P0.12 U28, S2_MOT U29 | Move U201 ≥1 mm | SPI/USB/GND maze (S1_MOSI/S1_NCS/AIN5/D±) |
| R202.1-+3V3 (S-edge 20.725) | MCU_RST U8 (0.0 clr vs E-W-y=20.6) | Move R202 ≥0.5 mm | +3V3/RST/P1.11 maze |
| C203.2-GND (W-edge 24.2) | +3V3 U0-N (OVERLAP) | Move C203 ≥0.5 mm | +3V3/GND mesh |
| C507.2-GND | GND U7 (TX_EN-cage), CTD (see Q5) | Move C507 (attempted N: fails W-end) | GND/TX_EN mesh |
| D501.1-FB_PK, D502.1-VIN | D501-A U19 (crossing/OVERLAP) | Move D501/D502 | TX coil-fan mesh |
| TP305/TP306 (testpoints) | +3V3 U2 | **DONE drc127** (ECO4: TP305→(44.0,43.5), TP306→(44.0,47.2), stubs kept; P131 east loop closed U2; probe showed pads F-only, true cages were S2_SCK-diag + S2_SCK-y=42.8) | Nothing (testpoints) |

**Owner decision 2026-10-04:** option (c) — Q6 destructive re-place
APPROVED (no accepted opens; cheap partial moves first, fully destructive
only where partial provably fails). IN PROGRESS on this branch; checkpoint
committed before any ripup. (TP305/TP306 micro-move already DONE drc127.)

## Corroboration

- Hand/survey routing: 126 DRC passes, P6–P130, every cage verified by
  TRUE pcbnew corridor surveys with 0.5 mm margin + ripup attempts.
- Independent oracle: freerouting.org 2.4.1 headless (Java 25, 50-pass
  budget) stuck at 73 unrouted with ZERO progress across passes 2–4
  (score frozen 716.45) before timeout — autorouter agrees cages hold.
- DRC127: 0 errors, 0 parity, 26 unconnected, 179 warnings
  (123 lib_footprint_mismatch expected per KICAD-013).
- DRC128 triage: identical (board unchanged) — see
  `notes/stage1/drc128-triage.json` + `kicad-render128-top/bottom.png`.

OWNER DECIDED 2026-10-04 (do it right, not easy — no accepted opens):
Q5 EXECUTED (R113/114/115/515, ERC clean, netlist verified); Q6 APPROVED —
re-place in progress, checkpoint before ripup, partial moves first.
