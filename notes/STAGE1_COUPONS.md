# Stage 1 — Phase 1 coupons: designs + test plans + bench handoff + ordering BOM

**Status: design complete, bench human-side. DO-NOT-ORDER until Phase 1 exits AND owner purchase approval.**
**Skills used:** `kicad-schematic`, `kicad-pcb`, `kicad-layout`, `kicad-bom` (coupon T-A/T-B laid out in the flex project pattern; TX jig per base TX interface).

## 0. Rule basis

FINAL_SPEC §6 gates ALL fab orders on Phase 1. Governed choices cite TOUCH-001…004, ELEC-002, MECH-001/002, CHG-001/009/011, FW-001, MFG-037/038. Controller pick deviation: Azoteq IQS rejected (IQS269A = 8 ch × 2 addresses = 16 max; IQS7222A ≈ 8–10 self-cap per chip — neither reaches 24 channels off-the-shelf). Pick: **2× Infineon CY8CMBR3116-LQXI** (SmartSense auto-tuning, EZ-Click config, I2C 0x37/0x38). Register-map confirmation (was: IQS map) is now **MBR3 map + address + EZ-Click SAVE_CHECK_CRC** — gate 2.3. RING_SCROLL_ENABLE kept; ELEC-002 2-finger result NOT assumed (SCROLL_UX Method B stays flagged).

## 1. Coupon designs (fab-ready specs)

### Coupon T-A — touch geometry A (24-ring finalist), flat
- 2L FR4 test PCB, 80 × 40 mm: **12 parallel electrodes, 4.5 mm wide, 5.24 mm pitch** (covers half the 24-ring circumference unrolled: 12 × 5.24 = 62.9 mm), F.Cu electrodes under coverlay, B.Cu solid GND shield, 0.1"-header breakout (12 sig + GND + shield) to the MBR3 EVM.
- Overlay: **production-shell sample panel** — FDM PETG black, **1.2 mm ±0.15 thick**, printed with the **0.4 mm nozzle process** (MFG-037), 100 × 60 mm, laid directly on electrodes (no adhesive — weight only).
- Partner instrument: **CY3280-MBR3 EVM** (real kit, Infineon) + EZ-Click; 12 of its 16 channels used.

### Coupon T-B — touch geometry B (16-ring finalist), flat
- Identical PCB/overlay/EVM, electrodes **7.0 mm wide, 7.85 mm pitch** (16-ring equivalent: 16 × 7.85 = 125.6 mm). Same header pinout so the EVM cable swaps straight over.

### Coupon C — charging link jig (CHG-001/009/011)
- **RX side = the coil-board project as drawn** (`trackball-ball-coil/`, 6-turn square spiral Ø19 + C_TANK + Zener + wire pads) + **ferrite disc r10.5** behind it + 1.2 mm PETG disc (charging-pole wall sample) in front.
- **TX side (annular finalist):** annular PCB coil coupon, Ø40 outer / Ø22 inner single-layer spiral on 2L FR4 + series cap pads (value TBD on bench) + wire pads — driven by the base LTC4125 TX EVM/jig from the base job.
- **TX side (disk alternative):** 1× ferrite-backed disk/puck coil sample (gap note: exact MPN pending base TX choice — see QUESTIONS.md) for the annular-vs-disk LCR comparison.
- LCR jig: 4-wire Kelvin clips + printed spacer ladder (0.5/1.0/1.5/2.0/3.0 mm PETG shims) setting TX–RX gap.

### Coupon M — mechanical/optical samples (MECH-001/002)
- **Transmission discs:** 3× Ø25 × 1.2 mm PETG black discs (0.4 mm nozzle) + 3× (0.2 mm nozzle, MFG-038) — one of each kept unprinted-clean as reference; λ_sensor = the base PMW3360 illumination band (red/IR per base job — gap: confirm wavelength with base team before the transmission run).
- **Z-shim ladder:** 0.1/0.2/0.3/0.5 mm PETG shims for the base optical-sensor EVM stack (FW-001 input owner: base firmware job; ball side supplies surface-finish samples only).

## 2. Test plans + explicit PASS criteria (gates 2.1–2.6)

General: log ambient T/H, instrument IDs, sample IDs; every gate records raw numbers in the bench sheet (§4). n=3 repeats minimum.

- **Gate 2.1 — shell transmission (MECH-001).** Spectrometer or sensor-EVM AGC comparison through each disc vs open air at λ_sensor. **PASS:** transmission loss ≤ 1.0 dB for at least one nozzle process; the passing process is recorded as the V1 shell process and the other is dropped (or both pass → 0.4 mm default per MFG-037 cost).
- **Gate 2.2 — touch delta/noise both geometries (ELEC-002, TOUCH-001…004).** Finger touch per electrode + 2-finger straddle, at **20 °C and 45 °C** (chamber or heat-gun + thermocouple soak 10 min). Record per-channel delta and idle noise RMS. **PASS A/B:** min-channel SNR ≥ 5:1 at both temperatures AND 2-finger straddle resolves two distinct peaks on adjacent channels (ELEC-002 Method-B prerequisite). Winner = higher worst-channel SNR; loser geometry deleted from the flex project. If neither passes → BLOCKED, new geometry required (do not silently keep A).
- **Gate 2.3 — controller confirmation.** I2C scan finds MBR3 at 0x37 (and second EVM/chip strapped 0x38); register map matches datasheet BUTTON_STAT/DIFF/SYSINFO; EZ-Click SAVE_CHECK_CRC persists config across power cycle. **PASS:** all three, both addresses.
- **Gate 2.4 — TX coupling (CHG-001).** LCR (100 kHz/1 MHz TBD on meter): L, Q, k for annular-TX→RX and disk-TX→RX at 1.0/2.0/3.0 mm gaps with ferrite + PETG disc in place. **PASS:** one TX option delivers k ≥ 0.25 at 2.0 mm gap with Q_RX ≥ 40 (provisional thresholds — tighten from measured spread; see provisional list).
- **Gate 2.5 — tank tuning + Vpk (CHG-009/011).** Powered TX jig at the mechanical mockup gap; sweep C_TANK E12 ladder; scope Vpk at RX (open + loaded by LTC4120 EVM or resistive equivalent). **PASS:** C_TANK selected with loaded Vpk inside LTC4120 VIN operating window across 1–3 mm gap AND Zener never conducts in normal operation (conducts only on unload transient — verified by load-dump test).
- **Gate 2.6 — Z-shim ladder (MECH-002 → FW-001).** Ball-surface samples over the base sensor EVM at each shim; record SQUAL/AGC-equivalent vs gap. **PASS:** exists a shim in the ladder with ≥ 20% margin to both rails of the sensor's good-tracking window; shim value handed to base firmware job as FW-001 input.

## 3. Human bench handoff

**Equipment:** LCR meter with Kelvin clips; 2-ch scope ≥100 MHz + 10× probes; CY3280-MBR3 EVM + EZ-Click on a laptop; I2C/USB adapter; calipers; thermocouple + heat source or small chamber; base TX jig (from base job); printed PETG panels/discs/shims (print BEFORE the session); multimeter; lab supply (for EVM, not for the ball — no battery in Phase 1).
**Procedure order:** print first (M panels/discs/shims, both nozzle processes) → 2.1 → 2.2 (room-T first, both geometries, then hot soak) → 2.3 → 2.4 → 2.5 → 2.6. **What "pass" looks like:** each gate's numbers written into §4 sheet; a gate passes only on measured numbers, never on feel. Any gate failing = stop, file QUESTIONS.md entry, do not proceed to fab.
**Safety:** LiPo-free phase (no cell on the bench); TX jig coil currents are bench-TBD — keep fingers clear of the TX coil during 2.5 and follow the base TX jig's own current limit.

## 4. Bench record sheet (copy per run)

`date, operator, T_amb, H_amb | gate | sample ID | instrument | raw readings (3×) | mean | PASS/FAIL | notes`

## 5. Ordering BOM — ⚠️ DO-NOT-ORDER (gated on Phase 1 exit + owner purchase approval)

| # | Part | Qty | Source proviso | Placeability |
|---|------|-----|----------------|--------------|
| 1 | CY3280-MBR3 evaluation kit (Infineon) | 1 (+0 spare — one EVM serves A then B) | Real kit, order from Infineon/distributor | N/A (EVM) |
| 2 | Coupon T-A PCB (80×40 2L per §1) | 5 | JLCPCB 2L (placeability N/A — bare test PCB, hand-assembled header) | hand-solder header |
| 3 | Coupon T-B PCB | 5 | JLCPCB 2L | hand-solder header |
| 4 | Annular TX coil coupon PCB | 5 | JLCPCB 2L | hand-solder |
| 5 | PETG black filament, production lot | 1 spool | Real filament, brand/lot recorded for MFG-037/038 traceability | N/A |
| 6 | Ferrite disc r10.5 (RX) + TX ferrite per base TX choice | 3 + 3 | Gap note: exact MPN pending base TX pick — QUESTIONS.md | N/A |
| 7 | C_TANK E12 ladder kit (1 nF–470 nF X7R) | 1 kit | LCSC brands only (Samsung/SAMWHA/Yageo) | N/A |
| 8 | Zener ladder (9/12/15 V SOD-123) | 10 each | LCSC, SMAJ-series-class real MPNs at order time | N/A |
| 9 | 0.1" headers, Kelvin clips, hookup wire | as needed | bench consumables | N/A |

Nothing here is ordered by this job. No battery, no ball ICs, no flex — all gated behind the coupon winners.
