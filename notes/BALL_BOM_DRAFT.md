# BALL_BOM_DRAFT.md — ball electronics BOM (DRAFT, DO-NOT-ORDER)

No fantasy parts: real part + real datasheet, or a gap note. LCSC/JLCPCB placeability still to verify at order time — **the ball has no hand-solder exception; anything not JLCPCB-placeable is flagged FAIL and must be replaced before fab** (see Flags).

| Ref | Part (real MPN) | Datasheet | Notes | Placeability |
|-----|-----------------|-----------|-------|--------------|
| U1/U2 | Infineon CY8CMBR3116-LQXI, QFN-24 | Infineon MBR3 datasheet | 24ch (A) + 16ch (B); 0x37/0x38, EZ-Click SAVE for 0x38 | VERIFY |
| U3 | Nordic nRF52810-QCAA | Nordic PS | Pinout AUDIT required (see REVIEW) | VERIFY |
| U4 | ADI LTC4120EUD-4.2, QFN-16 | ADI LTC4120 datasheet | RX path; RPROG 20k→60 mA | VERIFY |
| U5 | TI BQ29700DSER, WSON-6 | TI datasheet | Protection, EP=CELL_N | VERIFY |
| Q1 | Diodes Inc DMG6968U, SOT-26 | Diodes datasheet | Dual N-FET; SOT-26 pinout AUDIT | VERIFY |
| U6 | Torex XC6206P302MR, SOT-23 | Torex datasheet | 3.0 V LDO; pinout AUDIT | VERIFY |
| Y1 | Abracon ABM8-32.000MHZ (12 pF trim TBD) | Abracon datasheet | Pads 1/3 vs 2/4 AUDIT | VERIFY |
| J1 | Hirose FH28D-28S-0.5SH | Hirose CL586-1835-4 | 28-pos FPC; footprint AUDIT | VERIFY |
| J2/J3 | JST PH-3 / PH-2 TH | JST datasheet | Coil + cell (pre-wired leads) | VERIFY (TH) |
| L1 | TDK SLF6028T-470MR (47 µH buck) | TDK datasheet | Charger buck | VERIFY |
| C11–C15, R17–R40 | 0402 R/C, Samsung/Yageo-class | vendor datasheets | 560R Cx per ELEC-004 | VERIFY |
| C16–C23, R10–R16 | 0402/0603 R/C as sch | vendor datasheets | C22/RUN/RPROG per REVIEW | VERIFY |
| D1 (coil) | Zener 12 V SOD-123 (Vr TBD gate 2.5) | at order time | PROVISIONAL value | VERIFY |
| D2/D3 | Amber/green 0603 LEDs (MPN TBD) | at order time | Gap note: exact MPN at order | VERIFY |
| Cell | 401230 LiPo ~120 mAh [est.] + 10k NTC flying | cell vendor datasheet | TWO-LEVEL protection via U5+Q1 (CHG-005) | N/A (mech fit) |
| Ferrite | RX disc r10.5 + TX per base pick | at order time | Gap note: MPN pending gate 2.4 | N/A |
| Flex | 2L flex, ENIG fingers, coverlay, stiffener | fab drawing at order | Geometry frozen on coupon winner | flex house |

**Flags:** every SMT line is VERIFY (LCSC stock + JLCPCB basic/preferred at order time). No line is authorized for hand-solder. Nothing is ordered by this job.
