# Validation Plan — "Prove We Built It Right"

Every rule in RULES.md maps to exactly one primary validation tool.
Run order: fast software checks first, bench tests last. A stage's exit
gates must pass before the next stage's money gets spent (flex orders,
PCB fabs, tooling).

## Frozen nominals + first-article gates — clear these before Stage 1

The donor ball is dead (Rev 2.1): nothing is measured off a salvaged part.
Instead, the ball spec is FROZEN (RULES.md "Ball specification", Rev 2.2:
Ø40.0 mm, ±0.3 mm V1, runout ≤0.15 mm V1, wall 1.2 ±0.15 mm, FDM PETG
black). Rev 2.2 adds qualified manufacturing processes as options — a
process is not usable until its qualification rules pass:

0. **Process qualification gates** — clear before any ball from that
   process enters Stage 3:
   - 0.2 mm-nozzle FDM: MFG-037 (full first-article suite per nozzle
     serial, incl. SQUAL mean floor vs the 0.4 baseline) + MFG-038
     (mass window, flow-recal interval, thermal log) pass.
   - Outsourced resin: MFG-039 (supplier sample-lot dimensions,
     post-cure stability, tough-class resin, drop test) + MFG-040
     (formulation lock) pass; MFG-041 dual-source/fallback retired
     before production.
   What gates downstream work is first-article verification of OUR
   ball against that spec, per qualified process (MFG-001):

1. **Custom-ball first article** — diameter, radial runout (V-block),
   wall thickness at ≥6 points, weight; print traveler per MFG-036
   (spool lot, MECH-023 shrinkage factors). Gates MECH-002, MECH-004,
   MECH-011, MECH-012, MECH-034, MECH-045, TOUCH-003, TOUCH-009,
   TOUCH-010, TOUCH-032, CHG-002, CHG-036, RF-005, RF-006. Every Blender
   PARAMS value is frozen at the chosen nominal, not provisional.
2. **Sensor selection** — part number, sensing wavelength λ, lens
   geometry, SQUAL/CPI behavior. Gates MECH-001 (shell transmission is
   measured *at λ_sensor*), MECH-002 (Z-shim ladder), ELEC-007,
   FW-001…FW-005. MECH-045 requires the Z-shim ladder repeated on
   min/max-diameter first articles.
3. **Coil LCR + tank voltage** — TX/RX inductance, coupling k, tank Vpk
   at full drive. Gates CHG-001, CHG-009, ELEC-027 (creepage scales with
   measured Vpk), ELEC-029 (SPI keepaway is provisional pending the
   coil-current measurement).

## Stage 1 — Static / software (minutes, $0)

Run on every CAD/schematic change.

| Tool | Command | Rules covered |
|------|---------|---------------|
| Blender sensor geometry | `blender --background --python blender/check_sensor_geometry.py` | MECH-002, MECH-003 |
| Blender ball/socket | `blender --background --python blender/check_ball_socket.py` | MECH-004 (clearance budget) |
| Blender buttons/USB | `blender --background --python blender/check_buttons_usb.py` | MECH-006, MECH-008, MECH-027, MECH-049 (scroll button reach/recess) |
| Blender coil keep-outs | `blender --background --python blender/check_coil_keepouts.py` | CHG-001 (geometry), ELEC-003, ELEC-008, RF-001, RF-002 |
| Blender antenna keep-out (volumetric) | `blender --background --python blender/check_antenna_keepout.py` | RF-022 (8 mm sphere; complements the planar .dru proxy) |
| KiCad ERC | `kicad-cli sch erc` (spark-vm, KiCad 10.0.6) | KICAD-001…KICAD-006: netclass assignments, ERC errors |
| KiCad native DRC | `kicad-cli pcb drc --schematic-parity -f <board>.kicad_pcb` (spark-vm) | KICAD-007…KICAD-025: track width (PWR-001), USB diff-pair gap/skew/length (HID-002), clearances, annular rings, solder mask, silkscreen, edge, courtyard |
| KiCad custom DRC | same command with `trackball.kicad_dru` loaded (spark-vm) | KICAD-027…KICAD-039: the 10 conditional rules — RX/touch keepout (ELEC-003/CHG), ball antenna vs touch (RF-001), base antenna vs TX coil / USB shell (RF-002), USB-C shield annular (MECH-006), TX/USB clearance (ELEC-005), TX creepage (ELEC-027), SPI keepaway (ELEC-029), TX edge keep-back (PWR), antenna vs RX coil (RF-022) |

**Trap (KICAD-013):** `kicad-cli pcb drc` silently ignores
`missing_courtyard` unless its severity is warning/error in `.kicad_pro`.
Audit that setting on every run and confirm it is absent from "Ignored
checks."

Note: the Blender scripts already caught three real violations during
development (strain-boss distance; ball-antenna/RF-001 conflict that forced
the antenna off the ring plane; trace routing inside the RF-022 sphere).
They bite.

## Stage 2 — Coupons / material gates (before ANY flex or PCB order)

| # | Test | Rules | Pass |
|---|------|-------|------|
| 2.1 | Shell transmission at λ_sensor through 2 mm production sample | MECH-001 | <1% transmission |
| 2.2 | Flat touch coupon: production shell 1.2 mm + candidate electrode geometry, per-electrode delta vs noise at 20 °C and 45 °C | ELEC-002, TOUCH-001…TOUCH-004 | delta ≥5× noise; baselines 20–80% ATI range |
| 2.3 | IQS register-map confirm (ATI target, raw-count streaming, report-rate vs touch count) | ELEC-002, FW-006 | documented, matches firmware assumptions |
| 2.4 | Annular TX vs disk reference on LCR jig: k, TX input power at 60 mA charge | CHG-001 | k ≥70% of disk [est.]; ≤0.8 W in |
| 2.5 | Tank tuning in final mechanical mockup; scope tank Vpk at full drive | CHG-009, ELEC-027 | \|f0_TX − f0_RX\| <3% [est.]; Vpk logged, creepage re-checked |
| 2.6 | Sensor coupon: SQUAL floor and CPI vs Z on the Z-shim ladder | MECH-002, FW-001 | SQUAL above floor, CPI ±3% in [2.3, 2.5] mm |

**Gate:** 2.1–2.6 pass before flex/PCB fab. 2.2 failing kills the
touch-ring approach before it costs a flex spin. 2.5 failing (tank won't
tune in the real stack) kills the coil geometry before fab.

## Stage 3 — Mechanical first articles

| # | Test | Rules | Pass |
|---|------|-------|------|
| 3.0 | Ball first-article verification, per qualified process: diameter, runout, wall ×6 pts, weight, traveler | MFG-001, MFG-036, MFG-037/038 (0.2 nozzle), MFG-039 (resin), MECH-004 | Ø40.0 ±0.3 (V1) / ±0.1 (resin); runout ≤0.15 (V1) / ≤0.10 (resin); wall 1.2 ±0.15; traveler complete |
| 3.1 | Dial indicator on V-block, ball runout | MECH-004 | ≤0.15 mm (V1) |
| 3.1b | Z-shim ladder on min- and max-diameter first articles | MECH-045, MECH-002 | SQUAL/CPI criteria hold on both |
| 3.2 | Z-shim ladder 2.0–3.0 mm × 0.1 mm, SQUAL + CPI per sensor | MECH-002 | SQUAL above floor, CPI ±3% in [2.3, 2.5] mm |
| 3.3 | Force gauge: button actuation | MECH-008 | 0.6–0.9 N |
| 3.4 | 5-user roll test, 2 min each, click log | MECH-008 | zero unintended clicks |
| 3.5 | USB-C pull 30 N axial / 20 N lateral × 5; 1 m drop | MECH-006 | no pad lift, continuity, extraction 6–20 N; mates + enumerates |
| 3.6 | Base mass on scale | MECH-006 | ≥200 g |
| 3.7 | Threaded-insert pull test (heat-set, production boss geometry) | MECH-025 | pull-out ≥ design load × 2 |
| 3.8 | Flex bend-cycle coupon to the minimum bend radius | MECH-042 (via ELEC-036) | no trace cracking at 10 k cycles |

## Stage 4 — Electrical / charging bench

| # | Test | Rules | Pass |
|---|------|-------|------|
| 4.1 | Gap 2–7 mm × offset 0–5 mm jig: VIN(RX), ICHG, TX freq, STAT | CHG-002, CHG-003, CHG-007 | ICHG ≥50 mA in envelope; FTH = max+5%; zero false-green |
| 4.2 | FO matrix (steel disc, coin, paperclip, Al foil) + thermal cam, 15 min each | CHG-010 | fault/retry; no FO >60 °C |
| 4.3 | Full 0→100% charge, in-ball thermocouple + NTC pause/resume + detach simulation | CHG-004, CHG-006 | ΔT ≤15 °C, peak <45 °C; pause outside 0–40 °C; "complete" = sleep entry |
| 4.4 | Scope sensor VDD pins during charging, 10 kHz–50 MHz | PWR-002 | <100 mVpp |
| 4.5 | Static ball, TX on vs off: 60 s count log + SQUAL | CHG-008 | zero net counts; SQUAL −<10% |
| 4.6 | Worst-case cable + load steps, scope VBUS/3.3 V; 24 h charge cycling | PWR-001 | VBUS ≥4.4 V; 3.3 V ±3%; zero resets |
| 4.7 | Single-fault: charger forced 4.3 V; 200-cycle swell check | CHG-005 | secondary trips every time; no deformation |
| 4.8 | IEC 61000-4-2 gun: ball ±4 kV/±8 kV; base Level 4 | ELEC-004, ELEC-005, ELEC-006 | ball recovers ≤2 s via NRST; base criterion B; sensor re-init ≤100 ms |
| 4.9 | TX frequency across 4 states + steel-disc trip | CHG-003 | no false FOD; trip within one search interval |
| 4.10 | Radiated/conducted pre-scan against the module grant conditions | RF-004, RF-005…RF-009 | no new intentional radiator; antenna area unmodified |

## Stage 5 — Firmware / HID / RF

| # | Test | Rules | Pass |
|---|------|-------|------|
| 5.1 | Half-masked ball at fixed ω, SQUAL streams + fused error | FW-001 | ±5% of clean baseline; no >2-count steps |
| 5.2 | Tape-over-lens jig, rotations about each axis | FW-002 | dead-normal axis ±5%; live-normal axis flagged ≤50 ms |
| 5.3 | Motor accel ramp vs shaft encoder | FW-003 | lag <1 ms; axis error <2° |
| 5.4 | Parked ball: tap case + click buttons, fused log | FW-004 | RMS <1 count; ≤2 counts/click |
| 5.5 | Fixed-ball slide vs fixed-finger rotation, 50 trials each; yaw-spin | FW-005 | ≥95% classification; flag ≤100 ms; zero inversions |
| 5.6 | Solenoid 1/2/3-finger taps, 0–60 ms delays | FW-006, TOUCH-005…TOUCH-012 | ≥99% type accuracy; ≤80 ms; zero wrong clicks |
| 5.7 | RF-attenuated dropout injection, press/drag/idle × 20 | FW-007 | zero phantoms; zero stuck; converge ≤200 ms |
| 5.8 | 100 k-click solenoid life test | FW-008 | no double/missed in 1 kHz log |
| 5.9 | Ball removed, 60 s log | FW-009 | zero net motion |
| 5.10 | 3/3 ball DFU incl. bad image; 20-cycle base DFU incl. power cut | FW-010 | always recovers bootable |
| 5.11 | Grab test (≥4 contacts) | FW-011, TOUCH-013…TOUCH-018 | zero gestures |
| 5.12 | Disconnect one electrode on test flex | FW-012 | health report names channel ≤5 s |
| 5.13 | Full charge: touch raw counts + ESB PER | FW-013 | zero touch events; baseline <2 s; PER −<1 pp |
| 5.14 | Tri-OS plug test + UEFI cursor + hidapi open + 1000 Hz × 60 s | HID-001, HID-002 | cursor <5 s; >99.9% sequence integrity |
| 5.15 | 20 Windows plug/reboot cycles, app bind | HID-003 | 20/20 by VID/PID + usage page |
| 5.16 | Two paired units side by side; 20 pair cycles; PER/RSSI | RF-003 | zero foreign packets; 20/20; PER <1% |
| 5.17 | Scroll UX matrix: tap/hold/brush-press/drag classification 200 trials; ring slide-vs-roll confusion matrix 200 trials; precedence (button+ring) 50 trials; mode enter/exit cursor-freeze 100 cycles | UX-001…UX-012, FW-056, FW-057, MECH-049 | 100% classification; ≥99% slide/roll; ring vector →0 in 1 tick; zero cursor deltas in SCROLL, zero burst after exit |
| 5.17b | Scroll fallback: full UX matrix with RING_SCROLL_ENABLE=0; binary audit | UX-007 | matrix passes flag-off; no ring-scroll code path in binary |
| 5.17c | Scroll latch: 5-user one-handed task; escape-hatch 20/20 | UX-008 | 5/5 completion; latch exits on L/R press 20/20 |
| 5.17d | HID scroll reports: clean-OS scroll (no driver); Resolution Multiplier in descriptor; IF1 vectors/flags vs firmware state | HID-032, HID-033, UX-009 | scroll works Win/macOS/Ubuntu; flags match 100% |
| 5.18 | Straightedge roll per axis after A-matrix cal; repeat after reassembly | ELEC-007 | off-axis <2% |
| 5.19 | Touch latency budget: finger-down to HID report, 100 trials | TOUCH-019…TOUCH-024, FW-006 | p99 ≤ budget; no dropped taps |
| 5.20 | Moisture film + spray on shell; nitrile-glove taps | TOUCH-025…TOUCH-030 | zero false clicks; baseline reconverges ≤10 s; ≥95% nitrile registration |

## Stage 6 — Manufacturing / system ritual

| # | Test | Rules | Pass |
|---|------|-------|------|
| 6.1 | Bed-of-nails / pogo ICT: shorts/opens, programming, touch-baseline capture per unit | MFG-001…MFG-010 | 100% pass; baseline stored per serial |
| 6.2 | Pairing + RF check on the line (golden unit) | MFG-011…MFG-015, RF-003 | PER <1%; address unique per FICR |
| 6.3 | 20 trials from random orientations: roll dot-up, park | CHG-007 | LED ≤2 s [est.] in ≥18/20; zero false-green dot-down |
| 6.4 | ±3 mm lateral nudge while parked dot-up | CHG-002 | still charges (LED on) |
| 6.5 | Pack-out SoC audit: 10 units off the line | CHG-020, MFG-031 | 30–50% SoC by OCV window |
| 6.6 | ESS / burn-in: 24 h charge cycling + thermal soak, sample lot | MFG-016…MFG-025 | zero failures; drift within calibration limits |
| 6.7 | Final QA ritual: full HID + touch + motion + charge smoke test per unit | MFG-026…MFG-041 | 100% pass before box |

## Integration review process (standing)

No subsystem is reviewed alone at a phase gate. Every build-phase exit
requires an integration review in which the authors of the touching
subsystems review the interface between them — plus one reviewer who
authored neither side, sitting in the standing attacker seat, whose job
is to break the interface.

**Sign-off artifact:** `integration-review-<phase>.md` checked into the
repo: reviewers, INT rules checked with evidence links, open items with
named owners. The next phase does not start until the sign-off is
merged. **Regression rule:** any change to an INT rule, or to a
subsystem interface an INT rule governs, re-opens the affected phase
reviews.

| Phase (per FINAL_SPEC §6) | Artifact under review | Reviewers (authors + attacker seat) | INT rules gated |
|---|---|---|---|
| 0 — Sensor selection + first ball print | Sensor choice doc, first-article ball | FW + MECH + ELEC authors; attacker: charging | INT-006 (tick budget feasibility), INT-012 (RSSI), INT-025 (diameter→CPI plan) |
| 1 — Coupons (gates ALL fab) | Coupon results 2.1–2.6 | Touch/ELEC + FW + charging authors; attacker: host-driver | INT-010 (frequency plan), INT-002 (state-matrix test plan), INT-015 (descriptor draft) |
| 2 — Ball electronics | Ball schematic/PCB, flex, assembled ball | Ball-FW + schematic + RF + charging authors; attacker: base-FW | INT-001 (harness vs ball output), INT-002, INT-003, INT-004, INT-010, INT-011, INT-013 (rungs 1–2), INT-027/028 (threshold coordination), INT-012 |
| 3 — Base schematic + PCB | Base schematic/PCB | Base-FW + schematic + power authors; attacker: ball-FW | INT-006, INT-007, INT-008, INT-009, INT-015, INT-019, INT-020, INT-022 |
| 4 — Firmware bring-up | Ball FW, base FW, harness results | Ball-FW + base-FW + host-driver authors; attacker: MFG/QA | INT-001, INT-004, INT-005, INT-006, INT-014, INT-017, INT-021, INT-029, INT-030 |
| 5 — Charging integration | TX jig + full-charge logs | Charging + ball-FW + base-FW authors; attacker: safety reviewer | INT-002, INT-003, INT-007, INT-008, INT-009, INT-010, INT-011, INT-020, INT-027, INT-028 |
| 6 — System + V1 exit | Whole system, production-representative units | All authors; attacker: external (fresh eyes) | INT-016, INT-017, INT-018, INT-023, INT-024, INT-025, INT-026 (golden matrix), all INT blockers re-verified |

## What "proved we built it right" means for V1

**Exit criteria (all must hold):**
1. All 67 **blocker** rules PASS with logged evidence (no waivers) —
   including the 5 INT blockers (INT-001, INT-006, INT-007, INT-015,
   INT-027), each validated across its interface, not on one side.
2. All 265 **major** rules PASS; any waiver needs a written rationale +
   a V2 tracking issue, and no waived major may be safety-related
   (CHG-004/005/008/010, ELEC-004/005/006 are never waivable).
3. All 56 **minor** rules PASS or waived with rationale.
4. Stage 1 checks run green on the final CAD/schematic revision
   (checked into the repo alongside the fab outputs).
5. Every build phase (0–6) has a merged `integration-review-<phase>.md`
   sign-off; no phase started before the previous sign-off merged.
6. The killed rules stay dead: no blanket <50 ms click target
   reappears in docs, and no unvalidatable "premium feel" rule is
   smuggled back in — its measurable proxies (6.3, 6.4) are the contract.
   The R287 monorepo/lockstep mandate and the R290 hardware interlock
   line stay dead with them.
7. Frozen nominals + first-article gates (custom-ball first article,
   sensor selection, coil LCR/tank voltage) are recorded in the build log;
   every PROVISIONAL flag in RULES.md is either cleared or carried
   explicitly into V2. The "measure the donor ball" gate is gone — the
   ball spec is chosen, and MFG-001/MFG-036 verify we built it.

## Layout-review checklist (human, per PCB revision)

- [ ] Netclasses COIL_RX/COIL_TX/TOUCH/ANT/USB90/SPI/CHASSIS assigned;
      native + custom DRC run clean (Stage 1).
- [ ] `missing_courtyard` severity is warning/error in `.kicad_pro` and
      absent from "Ignored checks" (KICAD-013 trap).
- [ ] TVS arrays <5 mm from USB-C connector, straight traces, short/wide
      ground return (ELEC-005 — not expressible in .dru).
- [ ] TX tank creepage re-checked against measured Vpk (ELEC-027); SPI
      keepaway re-checked against measured coil current (ELEC-029).
- [ ] Antenna keep-out per module datasheet; no copper/components/metal
      in the keep-out (RF-002/RF-004); "do not modify antenna area" on
      the fab drawing.
- [ ] Ring feed traces routed around the RF-022 8 mm sphere
      (blender/check_antenna_keepout.py NOTE).
- [ ] Sensor 3.3 V LC filters at the sensor pins; TX 5 V feed separate
      (PWR-002).
- [ ] NTC bonded to cell pouch, not just the PCB (CHG-004).
- [ ] Electrode geometry frozen before FTH calibration (ELEC-003/CHG-003).
