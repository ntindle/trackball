# BOM draft — trackball base (BAL-BASE-001), Rev 0.1

145 components in `trackball-base.net` (0 duplicate refs). Positions marked
LCSC:TBD were selected as real MPNs but their LCSC codes/stock could NOT be
verified from this environment (LCSC product pages are unreachable here —
same limitation as documented in `docs/SENSOR_SELECTION.md` §9).
**Before any PCB order:** confirm every code + JLCPCB PCBA eligibility from
a live browser session. "JLC basic" = pick any in-stock basic-part
equivalent at order time; the spec column is normative.

## ICs, modules, sensors

| Refs | Value / MPN | Mfr | Footprint | LCSC | JLC | Notes |
| U201 | E73-2G4M08S1C | Ebyte | (custom, layout job) | TBD | confirm | nRF52840 module, castellated SMT; confirm PCBA eligibility |
| U301, U302 | PMW3360DM-T2QU | PixArt | (custom DIP, layout job) | C20612443 (code exists; stock NOT verified) | NO — hand-solder V1 | THT sensor modules; lens LM19-LSI separate, no LCSC code, confirm orderable |
| U501 | LTC4125EUFD | ADI | QFN-20-1EP_4x4_P0.5_EP2.5_ThermalVias | TBD | confirm | Verify EP size vs datasheet at layout; confirm part active/stocked |
| U101 | AP2112K-3.3TRG1 | Diodes Inc | SOT-23-5 | TBD | yes | 3.3 V LDO |
| U102 | APX809-29SAG-7 | Diodes Inc | SOT-23 | TBD | yes | 2.9 V reset supervisor, push-pull |
| U103 | XC6206P192MR | Torex | SOT-23 | TBD | yes | 1.9 V LDO |
| U104, U105 | TPS22918DBVR | TI | SOT-23-6 | TBD | yes | load switches, SENSOR_EN / TX_ON |
| U106, U107 | TLV3011AIDBVR | TI | SOT-23-6 | TBD | yes | UVLO / OV comparators, open-drain |
| U202 | TPD2E1B06DRLR | TI | SOT-563 | TBD | yes | USB ESD; confirm exact variant at order |
| Q101 | 2N7002 | generic | SOT-23 | JLC basic | yes | OV pulldown NFET |
| Y201 | ABS07-32.768KHZ-9-T | Abracon | 3215 2-pin | TBD | yes | CL=9 pF; caps PROV, trim at bench |

## Connectors, switches, magnetics, protection

| Refs | Value / MPN | Mfr | Footprint | LCSC | JLC | Notes |
| J201 | TYPE-C-31-M-12 | HRO | USB_C_Receptacle_HRO_TYPE-C-31-M-12 | TBD | yes | USB-C receptacle, SMT |
| J202 | 2×05 1.27 mm SMD header | generic | PinHeader_2x05_P1.27mm_Vertical_SMD | JLC basic | opt | dev debug; DNI-optional (pogo TP203–206 covers factory) |
| SW201, SW202 | 6 mm tact SMD | generic | SW_SPST_B3S-1000 | JLC basic | yes | RESET / BOOT |
| SW401–403 | D2FC-F-7N | Omron | (custom THT, layout job) | TBD | NO — hand-solder | THT for mechanical strength, DNI from JLC |
| L501 | 24 µH TX coil, Wurth 760308100110 ref | custom | (none — off-board) | — | NO — custom | PROVISIONAL geometry per MECH; inductance + Vpk bench items |
| TH501 | 100 k NTC 0603 | generic | R_0603 | JLC basic | yes | B-value per LTC4125 Fig 7 intent, TBD; place AT coil (remote) |
| FB301, FB302 | 600 Ω@100 MHz ferrite 0603 | generic | L_0603 | JLC basic | yes | ≥500 mA rated; e.g. BLM18PG601SN1D class |
| F101 | MF-MSMF050-2 | Bourns | Fuse_1812 | TBD | yes | PTC, 500 mA hold |
| D501 | BAS521-7 | Diodes Inc | SOD-523 | TBD | yes | high-voltage FB diode |
| D502 | CDBQR70 (alt BAT54) | — | D_0402 | TBD | yes | FB clamp; VERIFY package at order, alt BAT54 (SOT-23, needs fp swap) |

## Passives (all JLC basic unless noted; LCSC TBD, select at order)

Resistors 1% thick-film; capacitors as specced (dielectric matters — do not
sub X7R→Y5V etc.).

| Refs | Value | Spec | Footprint |
| R501 | 100 mΩ | current sense, 1%, ≥0.25 W | R_1206 |
| R502 | 10 k | 1% | R_0402 |
| R509 | 267 k | 1% (E96) | R_0402 |
| R503, R505, R508 | 100 k | 1% | R_0402 |
| R101, R102, R103, R104, R107, R110, R112 | 100 k | 1% | R_0603 |
| R512 | 100 k 100 V | HIGH-VOLTAGE rated ≥100 V | R_1206 |
| R511, R510 | 10 k | 1% | R_0402 |
| R111, R201, R202, R301, R303, R402, R404, R406 | 10 k | 1% | R_0603 |
| R504 | 7.87 k | 1% (E96) | R_0402 |
| R506 | 59.0 k | 1% (E96) | R_0402 |
| R513 | 5.23 k | 1% (E96) | R_0402 |
| R105 | 37.4 k | 1% (E96) | R_0603 |
| R108 | 27.4 k | 1% (E96) | R_0603 |
| R106, R205 | 1 M | 1% | R_0603 |
| R109 | 6.8 M | 1% | R_0603 |
| R507, R514 | 1 k | 1% | R_0402 |
| R401, R403, R405 | 1 k | 1% | R_0603 |
| R203, R204 | 5.1 k | 5% OK (CC termination) | R_0603 |
| R302, R304 | 39 Ω | 5% OK (LED feed; tune point) | R_0603 |
| R206, R207 | 33 Ω | 5% OK (SCK termination) | R_0603 |
| C509 | 100 nF 100 V | C0G/NP0, ≥100 V — PROVISIONAL, re-rate per measured Vpk | C_1206 |
| C504, C505, C506 | 47 µF | X5R/X7R, ≥10 V | C_1206 |
| C101, C103, C106, C108, C112, C114 | 10 µF/16 V | X5R/X7R, ≥10 V | C_0805 |
| C207 | 10 µF/10 V | X5R/X7R, ≥6.3 V | C_0805 |
| C301, C304, C306, C308, C311, C313 | 1 µF | X7R, ≥10 V | C_0603 |
| C501 | 1 µF | X7R, ≥10 V | C_0402 |
| C205 | 1 µF/16 V | X7R, ≥10 V | C_0603 |
| C303, C310 | 4.7 µF | X5R, ≥6.3 V | C_0603 |
| C102, C104, C105, C107, C109, C110, C113, C115, C117, C118, C206, C302, C305, C307, C309, C312, C314, C401, C402, C403 | 100 nF | X7R, ≥10 V (22× incl C203/C204 0402) | C_0603 (C203, C204: C_0402) |
| C510, C511 | 0.1 µF | X7R, ≥10 V | C_0402 |
| C502, C503 | 10 nF | X7R/C0G, ≥10 V | C_0402 |
| C111, C116, C208 | 4.7 nF | X7R, ≥10 V | C_0603 |
| C508 | 4.7 nF | C0G, ≥10 V | C_0402 |
| C507 | 470 pF | C0G, ≥10 V | C_0402 |
| C201, C202 | 12 pF | C0G/NP0 — PROVISIONAL, trim at bench | C_0603 |

## Test points (pads only, no parts — 20× D1.5 mm)

TP101 VBUS, TP102 +3V3, TP103 VBUS_SENSE, TP104 VSEN_1V9, TP105 TX_5V_SW,
TP201 UART_TXD, TP202 UART_RXD, TP203 SWDIO, TP204 SWDCLK, TP205 nRESET,
TP206 GND, TP301–TP304 S1 SPI, TP305–TP308 S2 SPI, TP501 coil tap.

## Not JLCPCB-placeable (besides the two sensors)

1. SW401–403 D2FC-F-7N: THT, hand-solder (mechanical strength).
2. L501 TX coil: custom/off-board assembly with ferrite (MECH).
3. JLC-eligibility to CONFIRM (placeable in principle): E73 module, LTC4125,
   PMW3360 codes, TPD2E1B06/ABS07 exact variants, D502 package.
4. J202: DNI-optional (pogo alternative fitted).
