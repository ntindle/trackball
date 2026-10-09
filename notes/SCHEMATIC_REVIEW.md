# Schematic review — trackball base (BAL-BASE-001), Rev 0.1

Hierarchical KiCad 10 project: root (`trackball-base.kicad_sch`) + 5 sheets
(power, mcu, sensors, buttons, tx). Inter-sheet connection is by global label
+ power net; there are no hierarchical sheet pins (map is printed on the root
sheet). Full-project ERC: **0 errors, 1 warning** (benign, documented §8).
Netlist `trackball-base.net`: 145 components, 0 duplicate refs, every
control/signal net continuity-checked (§9).

## 1. Power architecture

```
USB-C VBUS ─┬─ F101 PTC (500 mA hold) ─ VBUS_TX ─ U105 TPS22918 (TX_ON) ─ TX_5V_SW ──► TX sheet
            ├─ U101 AP2112K-3.3 ─ +3V3 ─┬─ MCU, buttons PU, ESD, NCS PU, STAT PU
            │                           ├─ U103 XC6206 1.9 V ─ V1V9_LDO ─ U104 TPS22918 (SENSOR_EN) ─ VSEN_1V9 ──► sensors VDD + IR LED
            │                           └─ FB301/FB302 ferrite ─ VDDIO_S1/S2 ──► sensors VDDIO
            ├─ R101/R102 ─ VBUS_SENSE (÷2 → MCU ADC)
            └─ U106 UVLO + U107 OV ─ TX_ON gate (= MCU_TX_EN AND VBUS-ok)
U102 APX809 (2.9 V) ─ MCU_RST ─ MCU + both sensors + SWD-10 + tact + TP
```

### 1.1 Why an LDO for 1.9 V, not a buck (PWR-002)
Sensor VDD current is small (PMW3360 run ≈ 10–20 mA typ incl. LED pulse
average; two sensors + margin < 100 mA). LDO loss at (3.3−1.9)×100 mA ≈
140 mW worst-case is thermally trivial in SOT-23, while a buck would inject
switching ripple into the rail PixArt specs at <100 mVpp in 10 kHz–50 MHz
(PWR-002) — exactly the band where TX harmonics already threaten SQUAL
breathing. LDO = no switching source on the sensor rail by construction.
XC6206P192MR: fixed 1.9 V, SOT-23, stable with ceramic 1–10 µF (C108 10 µF
+ C109 100 nF at output, C106 10 µF + C107 100 nF at input).
Tradeoff accepted: ~42% efficiency on this rail vs a buck's ~85%; the
absolute waste (<150 mW) is noise-floor inside the 500 mA USB budget
(PWR-001) and buys the PWR-002 noise margin.

### 1.2 Sequencing (INT-008) and inrush (INT-007, PWR-004)
Boot order is hardware + firmware: VBUS → +3V3 → MCU boots → enumerates
(500 mA descriptor, SET_CONFIGURATION) → FW asserts SENSOR_EN (U104,
controlled slew via CT cap C111 4.7 nF) → sensors run their power-up sequence →
FW asserts MCU_TX_EN → TX_ON only if UVLO+OV agree → U105 soft-starts the
TX 5 V feed → FW pulls TX_EN low to start the LTC4125 driver.
TX + sensor rails are off until SET_CONFIGURATION (PWR-004): pre-enum load
is MCU + LDO quiescent only, inside the 100 mA budget. TX soft-start comes
from U105's controlled rise (CT cap C116 4.7 nF)
plus the LTC4125's own search soft-start; bulk ≥100 µF at the TX input
(C504/505/506 3×47 µF, PWR-001) holds the rail during search pulses.
Failsafes for MCU-in-reset (Hi-Z outputs): R112 100 k PD holds TX_ON low;
R103 100 k PD holds SENSOR_EN low; R508 100 k PU to VIN holds LTC4125 EN
high = driver DISABLED (EN is active-low for run... see §4.3).

### 1.3 Suspend (PWR-009)
Suspend = TX rail off (MCU_TX_EN low), sensors in SPI shutdown (rail may
stay on; FW decides), MCU sleep. Budget: ≤2.5 mA total, no remote wakeup
from the charger function, no ping cadence. TX_STAT/TX_IMON stay readable
so FW can confirm the field is really off.

### 1.4 Supervisors (PWR-006 PROVISIONAL thresholds)
- U106 TLV3011 UVLO: trip 4.39 V fall / 4.69 V rise (R104/R105 + R106 1 M
  hysteresis FB). Open-drain OUT pulls TX_ON low directly.
- U107 TLV3011 OV: assert 5.99 V rise / release 5.71 V fall (R107/R108 +
  R109 6.8 M FB). OUT drives Q101 2N7002 gate (R110 100 k PU, local TX_ON
  flag); Q101 pulls TX_ON low.
- Band 4.4–5.5 V normal per PWR-001/PWR-006; disconnect band 5.75–6.0 V
  [est.] (R107/R108 ratio — recompute at layout review if PWR-006
  thresholds move after measurement).
- MCU ADC cross-checks: VBUS_SENSE (÷2, FW asserts TX disable if
  VBUS < 4.4 V, PWR-001) and VSEN_1V9 rail-good.
- INT-027 (cell/charger fault chain) is N/A to the base schematic: the
  base has no cell. The base-side hook is TX_STAT + TX_IMON + TX_EN, which
  FW uses to halt TX within 1 s of an ESB fault frame from the ball.

## 2. 1.9 V sensor rail design (detail)

VSEN_1V9 net (16 nodes, netlist-verified): U104.5/6 → C112/C113 bulk →
U301.4/U302.4 (VDD) → R302/R304 39 Ω → U301.6/U302.6 (LED_P) →
C303–C305/C310–C312 (4.7 µF + 1 µF + 100 nF per sensor, at the pins) →
TP104 + U201.7 (P0.02/AIN0 rail-good ADC).
- VDD 1.9 V is the PMW3360 recommended operating point (datasheet Table 3:
  1.80–2.10 V, typ 1.9 V).
- IR LED is integrated in the module; LED_P (anode) fed from VSEN_1V9 via
  39 Ω (typ 3.3 V designs use ~39–47 Ω from a higher rail; from 1.9 V the
  LED current is lower — bench-check brightness/SQUAL floor per ELEC-007;
  R302/R304 are the tune points).
- VDDPIX (pin 3) is the sensor's internal-LDO OUTPUT: bypass caps only
  (C302/C309 1 µF + C305... shared per-sensor set), never a rail.
- NCS has no internal PU: external 10 k (R301/R303). MOTION/MISO are
  push-pull: no PU fitted. NRESET: APX809 push-pull + internal weak PU, no
  external PU.
- Per-sensor VDDIO ferrite (FB301/FB302 600 Ω @100 MHz, PWR-002): the 3V3
  VDDIO feed is filtered per sensor; bead output has its own local net
  (VDDIO_S1/S2) with 1 µF + 100 nF at the pin. The bead blocks the ERC
  power drive, hence the local PWR_FLAGs (PWR-002).

### 2.1 No level shifters — VDDIO = 3.3 V (datasheet-grounded)
PMW3360 VDDIO recommended operating range is 1.80–3.60 V (datasheet Table 3;
absmax 3.60 V), so VDDIO is powered from +3V3 and talks directly to the
nRF52840's 3.3 V SPI. Margins at VDDIO = 3.3 V:
- Sensor VIH = 0.7×VDDIO = 2.31 V; nRF VOH ≈ 3.0 V min → OK.
- Sensor VOH = VDDIO−0.45 = 2.85 V min (@−1 mA); nRF VIH ≈ 0.7×VDD = 2.31 V
  → ~540 mV margin → OK.
- Assumes +3V3 within ±5% (AP2112K regulation + IR drop); layout keeps the
  SPI stubs short with 33 Ω source termination on SCK (ELEC-012, R206/R207).
  The series R splits each SCK net in two (MCU-side anonymous stub,
  sensor-side named net) — this is intentional, not an ERC artifact.

### 2.2 DEVIATION — VDD/VDDIO power timing (documented, needs bench proof)
Datasheet §power-up: VDD and VDDIO in any order with ≤100 ms between
supplies. This design violates the letter of that spec at every plug-in:
VDDIO (3V3) is up from USB attach while VDD (VSEN_1V9) stays off until FW
asserts SENSOR_EN after enumeration (hundreds of ms later).
Justification for accepting the deviation:
- No forward-bias path: all MCU-driven sensor inputs idle at levels clamped
  to the powered VDDIO rail (NCS high = 3.3 V; SCK/MOSI low). FW holds SPI
  idle and ignores MISO/MOTION (floating while VDD = 0; FW enables MCU
  pulldowns on MOT until rail-good) until VSEN_1V9 is stable.
- FW runs the full datasheet power-up sequence (NCS toggle, register init)
  AFTER enabling the rail, so the sensor always boots from a clean state.
Bench validation required (ELEC-007): measure VSEN_1V9 pre-enable leakage
(backpower through the sensor must not float the rail or backdrive U104),
sensor inrush at enable, and first-motion reliability over 20 plug cycles.
Fallback if it fails: gate VDDIO per sensor (respins FB301/302 as load
switches) or move VDDIO to VSEN_1V9 + level shifters.

## 3. MCU + USB + ESD + debug

E73-2G4M08S1C (nRF52840 module, integrated antenna — see §5).
- Normal-voltage mode: VDD = VDDH = +3V3; DCCH floats (LDO mode, no DCDC
  inductor — one less switching source near the sensors).
- Decoupling (ELEC-010): 10 µF bulk on the 3V3 lane at the E73 VDD entry
  (C207) + 100 nF 0402 at VDD/VDDH (C203/C204) + VBUS 1 µF (C205).
- USB-C J201 (HRO TYPE-C-31-M-12): CC1/CC2 5.1 k to GND (R203/R204, UFP
  500 mA advertise); D+/D− A/B pins shorted at the connector, routed
  through U202 TPD2E1B06 (netlist-verified: J201.A6/B6→IOB1→IOB2→D+,
  A7/B7→IOA1→IOA2→D−); VBUS A4/B4 + A9/B9 joined.
- Shield → CHASSIS net → GND via 1 M || 4.7 nF (R205/C208, ELEC-038): ESD
  bleed + RF short, no DC ground loop. No hard shield-to-GND short.
- Reset: U102 APX809-29SAG push-pull → MCU_RST net shared with P0.18
  (UICR PSELRESET, FW), tact SW201, SWD-10 pin 10, both sensor NRESET, TP205,
  R202 10 k PU + C206 100 nF (netlist: 9 nodes).
- 32.768 kHz XTAL Y201 (ABS07, CL = 9 pF) + 12 pF load caps C201/C202
  PROVISIONAL, trim at bench (§7).
- SWD: J202 Cortex-10 (1.27 mm SMD, dev use) + pogo pads TP203 SWDIO /
  TP204 SWDCLK / TP205 nRESET / TP206 GND (ELEC-018; factory programming +
  physical recovery without the header populated). J202 VTref = +3V3.
- DFU hooks (no firmware written, nothing blocked): native USB D+/D−;
  BOOT tact SW202 → P1.11 with 10 k PU (hold BOOT + tap RESET enters
  UF2/MCUBoot serial recovery; double-tap RESET also enters bootloader);
  UART TXD/RXD pogo pads TP201/TP202 (P0.28 TXD, P0.29 RXD)
  for debug console; all unused GPIOs left NC with FW input-with-pull note
  (ELEC-020; NFC pins P0.09/P0.10 need UICR to be GPIO — left NC).

### GPIO map (netlist-verified)
| Pin | GPIO | Net | Dir | Notes |
| 1 | P1.11 | BOOT btn + 10 k PU | in | DFU hold at reset |
| 2 | P1.10 | NC | — | FW input-with-pull |
| 3 | P0.03/AIN1 | VBUS_SENSE | ADC in | ÷2 divider + TP103 |
| 4 | P0.28/AIN4 | UART_TXD | out | TP201 |
| 6 | P1.13 | BTN3 | in | MIDDLE / scroll-hold |
| 7 | P0.02/AIN0 | VSEN_1V9 | ADC in | rail-good |
| 8 | P0.29/AIN5 | UART_RXD | in | TP202 |
| 9 | P0.31/AIN7 | BTN1 | in | LEFT |
| 10 | P0.30/AIN6 | BTN2 | in | RIGHT |
| 11/13 | P0.00/XL1, P0.01/XL2 | Y201 | xtal | 12 pF PROV |
| 12/14/16 | P0.26, P0.06, P0.08 | NC | — | FW input-with-pull |
| 15 | P0.05/AIN3 | TX_IMON | ADC in | TACQ ≥ 10 µs (267 k source) |
| 17 | P1.09 | S2_MISO | in | |
| 18 | P0.04/AIN2 | S2_NCS | out | 10 k PU at sensor |
| 20 | P0.12 | S2_SCK | out | via R207 33 Ω |
| 22 | P0.07 | S2_MOSI | out | |
| 26 | P0.18 | MCU_RST | in | UICR PSELRESET |
| 27 | VBUS | VBUS | pwr | USB detect |
| 28 | P0.15 | MCU_TX_EN | out | → TX_ON gate |
| 29/31 | D−/D+ | USB | bidi | via U202 ESD |
| 30 | P0.17 | TX_EN | out | → LTC4125 EN (via 1 k) |
| 32 | P0.20 | S1_NCS | out | 10 k PU at sensor |
| 33 | P0.13 | S1_SCK | out | via R206 33 Ω |
| 34 | P0.22 | S1_MOSI | out | |
| 35 | P0.24 | S1_MISO | in | |
| 36 | P1.00 | S1_MOT | in | FW pulldown until sensors up |
| 37/39 | SWDIO/SWDCLK | TP203/TP204 + J202 | dbg | |
| 38 | P1.02 | S2_MOT | in | FW pulldown until sensors up |
| 40 | P1.04 | TX_STAT | in | OD + 10 k PU |
| 41/43 | P0.09/P0.10 NFC | NC | — | need UICR for GPIO |
| 42 | P1.06 | SENSOR_EN | out | 100 k PD failsafe |

## 4. Wireless TX (LTC4125, datasheet 4125f Fig 7 reference)

U501 LTC4125EUFD per Typical Application Fig 7, tuned to PWR-001 1 W:
RIS = 100 mΩ (R501), RIN = 10 kΩ (R502), RIMON = 267 kΩ (R509) →
ITH = 300 mA / ILIM = 450 mA; bulk 3×47 µF (C504/505/506) ≥ 100 µF.
- Current loop: IN (pin 1) / IS− (3) / IS+ (4) / IMON (5) / RIN / RIMON /
  CIMON (C503 10 nF) / CIF (C502 10 nF), exactly Fig 7.
- DTH 100 k/7.87 k (R503/R504), FTH 100 k/59.0 k (R505/R506, ≈119 kHz
  search ceiling); DTH step size for 1 W is bench-tune (§7).
- PTHM = GND (min pulse 1/32 period); PTH1/PTH2 OPEN per Fig 7 (NC)
  (netlist confirms single-pin unconnected nets — intentional).
- CTD 470 pF (C507), CTS 4.7 nF (C508).
- EN (pin 15, active-low RUN): MCU TX_EN → R507 1 k → EN; R508 100 k PU to
  VIN holds the driver OFF by default (PWR-001: TX off until enum).
  FW drives low to run (after enum + rail on), high/Hi-Z to stop; FW stops
  TX if VBUS < 4.4 V (PWR-001).
- STAT (pin 8, open-drain) → R511 10 k PU → TX_STAT → MCU P1.04.
  Fig-7 DSTAT LED omitted (no user-visible LED requirement; status goes to
  FW/host).
- TX_IMON → MCU ADC P0.05; FW TACQ ≥ 10 µs (267 k source impedance).
- NTC 10 k (R510) + 100 k TH501 thermistor AT THE COIL (remote): ≈41.5 °C
  coil limit per Fig 7.
- Tank: L501 24 µH nominal (Würth 760308100110 ref) + C509 100 nF C0G
  100 V → f0 ≈ 103 kHz. Coil geometry is PROVISIONAL per MECH (annular
  around sensor area + ferrite — see job docs); inductance AND tank-cap
  voltage rating are bench-validation items (§7).
- FB network: D501 BAS521-7 (high-voltage), RFB1 100 k 100 V 1206 (R512),
  C510 0.1 µF, R513 5.23 k + C511 0.1 µF; DC1 D502 clamps the FB node to
  VIN (CDBQR70 — package TBD at BOM, alt BAT54).
- Tank peaks are HIGH VOLTAGE: CTX 100 V C0G, RFB1 100 V part, DFB
  high-voltage diode. Layout must minimize/isolate the red high-voltage
  nodes per datasheet Fig 18 (layout job).
- EP (pin 21) = GND with thermal vias to the GND plane (layout); θJA
  43 °C/W → ≈1.25 W @ 2.5 A RMS ≈ +55 °C — needs the vias + copper.
- Layout-critical (from datasheet pp. 24–25, for the layout job): Kelvin
  RIS sense back to the resistor terminals, minimal sense loop area, away
  from the coil; CIN/CIN1/CIN2 tight to IN/GND pins; hot loops
  CIN1→IN1→SW1→GND and CIN2→IN2→SW2→GND minimum area; short fat traces
  SW→coil (resistance matters, inductance doesn't); Demo board DC2330A as
  reference.
- TX-bus interface to power sheet: TX_5V_SW feed (netlist 5 nodes) +
  TX_EN/TX_STAT/TX_IMON to MCU. Coil tap: TP501 via R514 1 k for bench
  probing of the tank midpoint.
- FOD intent (FTH ceiling ≈119 kHz) + INT-009: FW validates motion-burst
  status/CRC and discards — never fuses — corrupt samples; scope-triggered
  TX-edge-vs-SPI test at integration.

## 5. Antenna choice + keepout

Choice: **E73 module's integrated antenna** (no external chip/PCB antenna).
Justification: the E73-2G4M08S1C is a pre-certified nRF52840 module; using
its integrated antenna removes 2.4 GHz matching/network design risk from
V1 and keeps the ESB link to the ball a firmware/integration concern
(FW-001) rather than an RF design concern. A discrete antenna can be
revisited if range tests fail, at the cost of a matching network + anechoic
validation.
Keepout (volumetric, 3D — layout job, noted on the MCU sheet): no copper,
no ferrite, no battery under/near the E73 antenna end; keep the TX coil +
ferrite out of the antenna near field per the ELEC-002-adjacent touch/RF
keepout rules; plain bounding-box keepout documented on schematic, exact
volumes per MECH at layout.

## 6. Buttons

3× D2FC-F-7N SPST-NO (THT for mechanical strength — hand-solder, DNI from
JLC; see BOM). Each channel: 10 k PU (R402/404/406) + 100 nF to GND
(C401/402/403) + 1 k series (R401/403/405) → BTN glabel.
- RC time: press ≈100 µs (1 k), release ≈1 ms (10 k); FW debounces 5–20 ms
  on top. RC is FITTED (not DNP option) — cheap insurance against a FW
  schedule slip.
- 1 k limits ESD strike current into the MCU clamp diodes.
- BTN3 = MIDDLE = scroll-hold (P1.13); hold + ball motion = scroll per
  SCROLL_UX_DESIGN (no scroll wheel). Placement must support
  hold-while-rolling (layout + MECH concern; nets are clean for the handoff).

## 7. Provisional values (bench validation required)

| # | Value | Current | Validation |
| 1 | C509 voltage rating | 100 nF C0G 100 V 1206 | Scope tank Vpk at full TX; re-rate per measured peak + margin |
| 2 | L501 inductance | 24 µH nom (760308100110 ref) | Measure final annular geometry; re-tune f0 ≈ 103 kHz with C509 |
| 3 | Coil geometry | annular + ferrite, off-board/custom | MECH-controlled; keepout vs antenna near field |
| 4 | Y201 load caps | 12 pF (CL = 9 pF XO) | Trim at bench for ±20 ppm |
| 5 | DTH step / 1 W tune | R503/R504 Fig-7 values | Bench-tune if search stalls; TX burst rail dip ≤ 5% |
| 6 | R302/R304 LED feed | 39 Ω from 1.9 V | SQUAL floor / brightness per ELEC-007 |
| 7 | VSEN_1V9 pre-enable | 0 V expected | Measure backpower leakage (§2.2 deviation proof) |
| 8 | PWR-006 thresholds | UV 4.39/4.69 V, OV 5.99/5.71 V | Lab-supply ramp per rule validation; [est.] until measured |
| 9 | U501 EP size | 2.5×2.5 mm footprint | Verify against LTC4125 UF drawing at layout |
| 10 | LCSC PNs / stock | MPNs only (§BOM) | Confirm all codes + JLCPCB PCBA eligibility from live browser |
| 11 | Lens LM19-LSI | per SENSOR_SELECTION | Confirm orderable — likeliest procurement failure |
| 12 | TPD2E1B06/ABS07 variants | DRLR / -9-T | Confirm exact LCSC variants at order |
| 13 | D502 | CDBQR70 (0402) | Verify package; alt BAT54 |

## 8. ERC status

`kicad-cli sch erc --format json --severity-all` on the full project:
**0 errors, 1 warning.**
- Warning `pin_to_pin`: U201.7 (P0.02/AIN0, Bidirectional) ↔ U104.6
  (VOUT, Power output) on VSEN_1V9. BENIGN BY DESIGN: an ADC input sensing
  a driven rail. FW configures P0.02 as ADC input only; it never drives
  against the load switch. (Same class of warning would apply to any
  rail-sense ADC pin; VBUS_SENSE avoids it only because a divider sits
  between.)
- Standalone per-sheet ERC shows expected errors in isolation
  (power_pin_not_driven, isolated labels) because rail drivers live on the
  power sheet and join by name at the project level. These clear at
  full-project ERC and are not defects.
- `footprint_link_issues` for the 7 footprintless customs (U201, U301,
  U302, SW401–403, L501) is benign at schematic stage — footprints are the
  layout job's deliverable (§10). The `trackball-lib` CLI warning is benign
  (project-local symbol lib).

## 9. Netlist verification log

Full-project `trackball-base.net` checked programmatically (not just ERC):
VSEN_1V9 16 nodes; MCU_RST 9 nodes (APX809 + tact + SWD-10 + TP205 + MCU +
both sensors); TX_5V_SW power→TX; VBUS continuity (connector + PTC + LDO +
supervisors + E73); +3V3/GND fanout; USB D+/D− path through U202 both legs;
S1/S2 SPI (NCS/MOSI/MISO direct, SCK via 33 Ω with intentional net split,
MOT direct); BTN1→P0.31, BTN2→P0.30, BTN3→P1.13 with full RC per channel;
TX_EN (MCU→1 k→EN, PU to VIN), TX_STAT (OD+PU), TX_IMON (R+C+ADC);
SENSOR_EN (MCU + PD failsafe), MCU_TX_EN → TX_ON gate (UVLO OD + OV Q101 +
PD failsafe); V1V9_LDO LDO→switch; VBUS_TX PTC→switch; VIN bulk + sense +
dividers; PTH1/PTH2 confirmed open; FB network; CHASSIS (shield + 1 M +
4.7 nF); VDDIO_S1/S2 (bead + caps + pin each); all 8 SPI TPs, 4 SWD TPs,
TP501 coil tap, rail TPs; U501 EP + PTHM on GND. No duplicate refs.

## 10. Layout handoff (footprints + notes)

- Assigned standard footprints for all SMT passives, SOTs, USB-C, SWD-10,
  tacts (B3S-1000), crystal, PTC, U501 (QFN-20-1EP 4×4, EP VERIFY per §7.9).
- Custom footprints for the layout job: E73-2G4M08S1C module (NOT the
  stock E73-2G4M04S — different module/pinout), PMW3360 ×2 (lens-aligned,
  Z = 2.4+0.1 mm per MECH-002), D2FC ×3 (THT), L501 + TH501-at-coil
  (off-board/remote).
- ELEC-010: 4.7–10 µF within 10 mm of every IC rail entry.
- Antenna volumetric keepout (§5); TX hot loops + Kelvin + EP vias (§4);
  TX coil/ferrite out of antenna near field; PWR_FLAGs at rail entries.
- Factory pogo: TP203/204/205/206 (SWD + GND) must be bottom-accessible
  probes; TP501/TP101–105 bench access.

## 11. DEVIATION — Q5 layout-jumper ECO (layout job, owner-approved 2026-10-04)

Four nets were unroutable because both endpoints are pad-caged by fixed
adjacent pads/traces no layout move can clear (LAYOUT_REVIEW §7.5 U20/U21/
U22–23/U26 + QUESTIONS.md Q5: survey-verified, ripup-attempted, freerouting
oracle corroborates). Owner approved a schematic ECO (no accepted opens).
Change: 4× 0 Ω series/branch jumpers (0603, JLC basic) added as alternate
taps — R113 (VBUS_SENSE), R114 (SENSOR_EN), R115 (MCU_TX_EN) on the power
sheet as same-net branches (both pins labeled to the existing global net),
R515 (CTD) on the TX sheet in-line (deleted 1 wire segment U501.14–C507.1,
R515 bridges it; U501-side sub-net explicitly labeled `/tx/CTD_U501`, C507
side keeps `/tx/Net-(U501-CTD)`).
Netlist delta (verified by pre/post diff): +4 refs (155→159 by netlist ref
count), nets 89→90 (CTD split); ONLY the 4 target nets changed. ERC after
ECO: 0 errors + the same 1 benign `pin_to_pin` warning (§8).
Justification for accepting the deviation:
- Zero electrical change: 0 Ω jumpers add no resistance, no drive level
  shift, no timing change on control/ADC-sense nets; CTD keeps its 470 pF
  timing cap on the same copper path through R515 (trace + 0 Ω is
  negligible for a timing node, not a hot loop).
- Standard JLC-placeable 0603 parts (BOM passives row); +4 placements, no
  cost driver, no new rails or modes.
- The alternative (accept 4 opens) was explicitly rejected by owner
  directive 2026-10-04 ("do it right, not easy").
Layout must route each net THROUGH its jumper pads (R515.1↔U501.14 and
R515.2↔C507.1 as separate closable sub-nets; R113/114/115 similarly) —
parity DRC enforces the new nodes. No bench validation required (passive
jumpers); validation is ERC + netlist diff (done) + route-close with
`--schematic-parity` DRC (layout job).

## 12. DEVIATION — Q6-A S2_MOT removal (layout job, owner-approved 2026-10-09)
Owner decision Q6 Option A: drop S2_MOT from the schematic; firmware polls
sensor-2 Motion register (0x02, bit 7 = MOT, per docs/SENSOR_SELECTION.md §5)
over SPI; S1_MOT remains the shared wake interrupt. Rationale (owner):
layout exhaustion proven six ways (§7.10.37 ECO matrix, 5 independent walls,
0.60mm needed vs 0.42mm gap); USB-C powered so idle-polling tradeoff moot;
latency bounded by poll interval; SPI arbitration is the firmware design
point. Functional relocation to firmware, not a dead open.
Change (this branch): mcu.kicad_sch — deleted wire (207.01,203.20)→
(231.14,203.20) + `S2_MOT` global_label (input); placed no-connect on U201
pin 38 at (207.01,203.20). sensors.kicad_sch — deleted wire
(292.10,146.05)→(307.34,146.05) + `S2_MOT` global_label (output); placed
no-connect on U302 pin 9 at (292.10,146.05). S1_MOT untouched. grep S2_MOT
over *.kicad_sch: zero hits.
Verification: `kicad-cli sch erc` 0 errors + the same 1 benign `pin_to_pin`
warning (§8). Layout follow-up (same branch): purged 15 S2_MOT tracks + 3
vias + cleared U201-38/U302-9 pad nets; DRC drc245 1unc (VIN-pad3 accept) /
0err. Fully reversible: re-add two labels + wire to restore.
