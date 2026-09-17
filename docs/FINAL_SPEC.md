# Ultimate Mouse — Final Engineering Specification
**Revision 3.1 — 2026-09-17.** Authoritative source: `~/workspace/trackball-drc/` (RULES.md Rev 2.3, 403 rules, 297 adversarial rounds). Supersedes the Rev 0.2 build-spec PDF wherever they conflict (see Appendix A). **The PDF (Rev 3.0) is stale — re-render pending.**

Values marked **[est.]** are engineering estimates, not measured. Values marked **PROVISIONAL** require a pending test/selection before fabrication money is spent. Frozen nominals are CHOSEN design values — they do not move without a recorded round in the DRC round log.

---

## 1. Architecture (final, settled)

**No donor parts anywhere.** The Kensington Orbit is dead as a parts source (decision 2026-09-16/17). Ball and base are fully custom.

### 1.1 The ball — free-spinning, active

- **Ø40.0 mm** sphere, fully custom shell (see §2 for frozen nominals). Spins freely in a socket; nothing tethers it.
- **Capacitive touch ring**: ≥16 independent self-capacitance electrodes covering the full 360° azimuth, each on its own controller channel (TOUCH-001, ELEC-002). *Not* the old 9×8 spherical gore array — that design is dead.
- **MCU/radio**: nRF52810-class, inside the ball. Talks to the base over 2.4 GHz proprietary (ESB-class) link; BLE is used only for DFU.
- **Battery**: small LiPo, ~120 mAh [est.], with two-level protection (CHG-005 — never waivable).
- **Charging RX**: 19 mm [est.] planar coil at a designated charging pole + ferrite + LTC4120-class receiver path. Electrode and antenna keep-outs around the charging structure.
- **Docking ritual**: orientation dot marks the pole opposite the charging pole. Park the ball dot-up; a status LED immediately below the shell at the dot confirms coupling within ~1–2 s [est.] (CHG-007). No light = not charging, never a false green.
- **No IMU for pointer tracking.** Any inertial sensing is auxiliary only. Pointer motion comes exclusively from the base's optical sensors.

### 1.2 The base — fully custom

- **Two standard optical mouse sensors**, optical axes 80–100° apart (target 90°) through the ball center, patches at polar 110° (MECH-003). Both read the ball surface; firmware fuses them (FW-001).
- **Controller**: nRF52840-class MCU with native USB.
- **Buttons**: left/right microswitches (Omron D2FC-F-7N class or Kailh GM 8.0, 0.6–0.9 N actuation [est.]) placed below the ball equator plane with ≥8 mm lateral clearance from the ball (MECH-008). Third button = **scroll button**, front-center: Ø12–14 mm [est.] concave-dish cap, 0.5 mm [est.] recessed below L/R caps, inside the thumb reach arc — holdable with the thumb while fingers roll the ball (MECH-049).
- **Scroll**: **modal, no wheel** (wheel killed by user direction 2026-09-17; MECH-007/MECH-029/FW-049 dead). Two methods: (A) ball motion in-plane while the scroll button is held → scroll vectors, cursor frozen (always available); (B) two-finger slide on the capacitive touch ring → scroll (gated on the ELEC-002 coupon proving 2-finger disambiguation; firmware flag `RING_SCROLL_ENABLE`, otherwise Method A is the complete UX). Full contract: UX-001…UX-013; design doc `~/workspace/trackball-build/scroll-ux/SCROLL_UX_DESIGN.md`.
- **USB-C**: mid-mount hybrid receptacle, ≥4 through-hole shield legs, cable-jacket strain boss in the enclosure, base mass ≥200 g [est.] via steel insert (MECH-006). Carries two interfaces (§3.4).
- **Charging TX**: LTC4125-class autoresonant transmitter driving an annular TX coil around the sensor region (CHG-001).

### 1.3 Interfaces and firmware update

- **USB Interface 0**: 100% vanilla boot-protocol HID mouse — works in BIOS/UEFI with zero software (HID-001).
- **USB Interface 1**: vendor HID interface, usage page 0xFF00, interrupt IN ≤64 bytes @ 1000 Hz — exposes raw sensor deltas, SQUAL, and touch telemetry for the custom 3D-manipulation driver. Stays inside the HID class (no WinUSB). Host software binds by VID/PID + usage page, never interface index (HID-002, HID-003).
- **Ball DFU**: MCUBoot + SMP-over-BLE; bootloader listens briefly on every reset. Base sends "enter DFU" over ESB and may relay images (FW-010).
- **Base DFU**: USB DFU, dual image slots, signed images (ECDSA-P256), hardware force-bootloader button. SWD pogo pads on both PCBs. V1 ball shell is screwed/serviceable, never glued.

---

## 2. Frozen ball spec (Rev 2.2, 2026-09-17)

Chosen and frozen — not estimates awaiting measurement. First-article rules verify *against* these.

| Parameter | V1 (rough print) | V2 path |
|---|---|---|
| Diameter | **Ø40.0 mm** | Ø40.0 mm |
| Diametral tolerance | ±0.3 mm | ±0.1 mm |
| Radial runout (total) | ≤0.15 mm | ≤0.10 mm |
| Shell wall | 1.2 mm ±0.15 | 1.0 mm ±0.05 |
| Shell material | FDM PETG, black — **0.4 mm or 0.2 mm nozzle, each a separately qualified process** (MFG-037/038) | Outsourced resin (supplier-qualified per MFG-039/040/041, tough/ABS-like class), SLA tough resin, or molded PC/ABS |
| Touch-ring band infill | solid (100%) or ≥4 perimeters | molded solid |

**Justifications.** Ø40.0 preserves the validated geometry stack (sensor patches at polar 110°, 24-electrode ring at 5.24 mm pitch / 16-electrode minimum at 7.85 mm, 19 mm RX coil, kinematic cradle) and is the ergonomic thumb-trackball standard (circumference 125.66 mm). PETG black: lowest-warp FDM material (sphere holds shape unenclosed), drop-tough (MECH-039), stable εr ≈ 3.0 for the touch stack, IR-opaque (MECH-001). PLA rejected (brittle, creeps under the retention lip); ASA rejected for V1 (needs enclosure, warps worse). ±0.3 mm achievable on calibrated FDM with per-spool shrinkage compensation (MECH-023); sensor Z protected by the datum strategy (MECH-022) + per-unit calibration (ELEC-007), with MECH-045 budgeting radius tolerance into the Z stack. Runout 0.15 mm fits the socket clearance budget (0.40 ≥ 0.15 + 0.20).

**Derived constants** (used across rules and Blender PARAMS): ball radius 20.0 mm; ball center 20.0 mm above socket datum; ring circumference 125.66 mm; shell inner circumference at ring band ≈ 118.1 mm.

**Qualified manufacturing processes** (a process is not usable until its qualification passes):
- **0.4 mm nozzle FDM**: the V1 baseline. Per-spool shrinkage calibration (MECH-023); per-ball print traveler with spool lot (MFG-036).
- **0.2 mm nozzle FDM** (MFG-037/038): separately qualified per nozzle serial — full first-article suite (Ø40.0 ±0.3, runout ≤0.15, wall at ≥6 pts, mass window), mandrel SQUAL mean ≥ 0.4-baseline floor AND variance ≤20% (MECH-012), Z-seam ≤0.05 mm (MECH-046). Re-qualification on nozzle change or any clog event. Finer ≠ better: if the texture is too fine for the sensor, fall back to controlled microtexture, not hope.
- **Outsourced resin** (MFG-039/040/041): supplier qualification (sample lot: dimensions Ø40.0 ±0.1, runout ≤0.10, TOUCH-004/007 on production resin, MECH-039 drop, tack-free cure) + per-lot incoming inspection with **two-pass post-cure stability** (measure at receiving, re-measure after 72 h settle at 23 °C + one −10/+50 °C cycle). Formulation locked (any resin change = new batch = full TOUCH-010 re-qualification, COA per lot). Tough/ABS-like class only. Dual-source or qualified in-house fallback retired before production (MFG-041).

---

## 3. Base design requirements

### 3.1 Sensor geometry and fusion

- Shell transmits <1% at the sensor illumination wavelength λ through a production-thickness sample — **PROVISIONAL on sensor selection** (630 nm red vs 850 nm IR); measured with an 850 nm source until λ is known (MECH-001).
- Lens reference plane Z = 2.4 ±0.1 mm from the ball surface, both sensors; bench Z-shim ladder 2.0–3.0 mm must hold SQUAL above floor and CPI within ±3% over [2.3, 2.5] mm (MECH-002).
- Optical-axis angle 80–100° (target 90°) through the ball center; never co-located or antipodal (MECH-003). Checked by `blender/check_sensor_geometry.py`.
- Sensor wells: labyrinth + gravity shed + cleaning port (MECH-019); bores printed support-free or reamed, bore-axis tilt ≤1.5° from design (MECH-020/021); single documented datum chain, worst-case stack to lens plane ≤0.25 mm (MECH-022).
- **Fusion (FW-001, blocker):** fuse timestamped *velocities* (1 µs timer per SPI read) via SQUAL-weighted least squares; weight 0 below SQUAL floor 16, ∝ SQUAL² above [est.]; 3σ cross-sensor gate rejects the outlier; on clean disagreement **trust the larger motion vector** (sensors miss counts, never over-count).
- Dead-sensor handling ≤50 ms flag on the dead-normal axis; fused output must not step >2 counts across the weighting threshold (FW-002, validation 5.1/5.2).

### 3.2 Buttons, scroll, socket

- L/R switches below ball equator, ≥8 mm lateral clearance, 0.6–0.9 N [est.]; 5-user roll test with zero unintended clicks (MECH-008).
- Scroll button: front-center third button per MECH-049 (Ø12–14 mm concave cap, 0.5 mm recess, thumb reach ≤45 mm); tap = middle click, hold = scroll mode; 5-user hold-while-rolling test with zero unintended actuations.
- Scroll contract (UX-001…UX-013): Method A (button-held ball motion → scroll vectors, cursor frozen) always available; Method B (two-finger ring slide → scroll) gated on ELEC-002; ball-frame vs world-frame disambiguation (UX-004, blocker); button suppresses ring (UX-006); single-finger ring slide = no-op (UX-012); opt-in sticky latch mode (UX-008); three-layer mode indication incl. no-driver LED pulse (UX-009).
- Socket: kinematic tri-lobed cradle, ≥3 contact points, parked lateral repeatability ≤0.5 mm (MECH-015); replaceable PTFE wear pads at the contacts, 10k-rotation wear test with ≤0.1 mm clearance growth (MECH-018); breakaway torque ≤0.5 mN·m after 24 h dwell, resin-on-resin contact forbidden (MECH-017); extraction force 2–8 N, ball retained at 90° base tilt, re-verified after 50 °C hot soak per qualified shell process (MECH-016).
- Ball CG offset from geometric center ≤0.5 mm [est.]; heavy parts symmetric about the dot–pole axis (MECH-011).

### 3.3 Power, ESD, RF (base)

- USB-C per MECH-006 (§1.2); D+/D− 90 Ω diff pair, length match <0.5 mm [est.]; TVS arrays <5 mm from connector (ELEC-005).
- VBUS ≥4.4 V under worst-case cable + load steps; 3.3 V ±3%; 24 h charge cycling with zero resets (PWR-001).
- Sensor VDD ripple <100 mVpp with TX charging active, 10 kHz–50 MHz (PWR-002); sensor 3.3 V LC filters at the pins, TX 5 V feed separate.
- ESD: ball ±4 kV contact / ±8 kV air with recovery ≤2 s via NRST; base IEC 61000-4-2 Level 4, criterion B, sensor re-init ≤100 ms (ELEC-004/005/006).
- Base antenna keep-out per module datasheet; no copper/components/metal in keep-out (RF-002); radiated/conducted pre-scan against module grant conditions (RF-004…009); two units side-by-side: zero foreign packets, 20/20 pair cycles, PER <1% (RF-003).

### 3.4 USB/HID contract

- **Interface 0**: boot-protocol mouse, cursor live <5 s on clean Windows 11 / macOS / Ubuntu / UEFI, descriptor parses clean (HID-001).
- **Interface 1**: vendor usage page 0xFF00, own report descriptor <200 bytes [est.], report IDs (e.g. RID 2 telemetry IN, RID 3 host→device OUT), single top-level application collection, fixed-length interrupt IN ≤64 bytes @ 1000 Hz, `protocol_version` byte as stable ABI. Never WinUSB (HID-002).
- Host binds by VID/PID + usage page — 20/20 across Windows plug/reboot cycles (HID-003).
- Ball→base telemetry: raw sensor deltas + SQUAL per sensor, touch ring contacts/count/centroid, battery SoC, charge state. Report IDs and byte layout are frozen by the `protocol_version` ABI.

### 3.5 Charging TX (base side)

- Annular TX coil around the sensor region; on the LCR jig vs disk reference: k ≥70% of disk [est.], TX input ≤0.8 W at 60 mA charge (CHG-001).
- Charging envelope jig (gap 2–7 mm × offset 0–5 mm): ICHG ≥50 mA in-envelope; FOD threshold = max + 5%; **zero false-green** — dot-down parking must never light the LED (CHG-002/003/007).
- Tank tuning in the final mechanical mockup: |f0_TX − f0_RX| <3% [est.]; tank Vpk scoped at full drive, ball present and absent — resonant caps rated ≥2× measured Vpk, C0G/film only (CHG-009, CHG-011).
- TX-on vs TX-off: zero net motion counts, SQUAL degradation <10% (CHG-008). Foreign-object matrix (steel disc, coin, paperclip, Al foil): fault/retry, no object >60 °C (CHG-010).
- Full 0→100% charge: ΔT ≤15 °C, peak <45 °C, NTC pause outside 0–40 °C (CHG-004). NTC bonded to the cell pouch, not just the PCB.
- **CHG-005 (blocker, never waivable):** two-level LiPo protection — LTC4120-4.2 primary + dedicated protector (BQ29700-class) with own FET; ≥10% [est.] free thickness around the pouch, never potted rigid; UL1642 / IEC 62133-2 cell; 0.5 C (60 mA).
- **CHG-026 (blocker):** single-fault cascade FMEA — ≥15 faults enumerated, each mapped to a safe state; 5 injected on the bench, all reach safe state ≤10 s [est.]; living document.

---

## 4. DRC library summary

`~/workspace/trackball-drc/` — **403 rules**, every one with statement, rationale, exact validation method, and round provenance. 297 adversarial rounds logged (54+ candidates killed, 24+ merged/amended); the round log records every kill.

| Category | Blocker | Major | Minor | Total |
|---|---|---|---|---|
| Mechanical (MECH) | 7 | 36 | 4 | 47 |
| Electrical (ELEC) | 5 | 23 | 10 | 38 |
| RF / radio (RF) | 3 | 15 | 5 | 23 |
| Power (PWR) | 2 | 8 | 5 | 15 |
| Charging (CHG) | 13 | 16 | 7 | 36 |
| Firmware (FW) | 6 | 42 | 8 | 56 |
| HID / driver (HID) | 2 | 24 | 7 | 33 |
| Touch sensing (TOUCH) | 6 | 25 | 1 | 32 |
| Manufacturing / test (MFG) | 9 | 27 | 5 | 41 |
| KiCad native catalog (KICAD) | 9 | 28 | 2 | 39 |
| Integration (INT) | 5 | 23 | 2 | 30 |
| Scroll UX (UX) | 2 | 9 | 1 | 12 |
| **Total** | **69** | **276** | **58** | **403** |

### 4.1 Highest-value rules (what the fights produced)

1. **FW-001** — SQUAL-weighted velocity fusion with trust-larger-on-disagreement. The dual-sensor concept is load-bearing on this math.
2. **ELEC-002** — the touch coupon gates the flex order: ≥16 electrodes, touch delta ≥5× noise floor, baselines 20–80% of ATI range at 20 °C and 45 °C, on a flat production-material coupon *before* any flex is ordered. A fail here kills the touch-ring approach while it's still a $5 coupon.
3. **CHG-005** — two-level LiPo protection + expansion allowance. A pouch cell in a resin sphere is a pressure vessel; highest-severity failure in the analysis; never waivable.
4. **RF-022** — volumetric 8 mm antenna keep-out (the planar KiCad check is provably insufficient in 3D). The Blender check already forced the ball antenna off the ring plane during development.
5. **CHG-026** — single-fault cascade FMEA with injected faults; the only rule examining fault *interactions*.
6. **CHG-011** — resonant-cap voltage rating ≥2× *measured* tank Vpk; measurement-first against the most violent passive failure (150+ Vpk on a 5 V drive).

### 4.2 How to run the validation

On spark-vm (KiCad 10.0.6, Blender 5.2.2). Order: fast software first, bench last. Stage exit gates must pass before the next stage's money is spent.

- **Stage 1 (minutes, $0)** — per CAD/schematic change:
  - `blender --background --python blender/check_sensor_geometry.py` (MECH-002, MECH-003)
  - `blender --background --python blender/check_ball_socket.py` (clearance budget)
  - `blender --background --python blender/check_buttons_usb.py` (MECH-006/007/008)
  - `blender --background --python blender/check_coil_keepouts.py` (CHG-001, ELEC-003/008, RF-001/002)
  - `blender --background --python blender/check_antenna_keepout.py` (RF-022, volumetric)
  - `blender --background --python blender/check_base_stability.py`
  - `kicad-cli sch erc` (KICAD-001…006)
  - `kicad-cli pcb drc --schematic-parity -f <board>.kicad_pcb` with `trackball.kicad_dru` loaded (KICAD-007…039: the 39 cataloged native checks at our thresholds + 10 custom rules for what KiCad can't express natively). Trap: audit that `missing_courtyard` severity is warning/error in `.kicad_pro` (KICAD-013).
- **Stage 2** — coupons/material gates *before any flex or PCB order*: shell transmission (MECH-001), flat touch coupon (ELEC-002/TOUCH-001…004), IQS register-map confirm, annular-TX LCR jig (CHG-001), tank tuning + Vpk (CHG-009/ELEC-027), sensor Z-shim ladder (MECH-002/FW-001).
- **Stage 3** — mechanical first articles (per qualified process): ball dimensions/runout/wall/weight/traveler, Z-ladder on min/max-diameter articles, button force + 5-user roll test, USB-C pull/drop, base mass, insert pull, flex bend coupon.
- **Stage 4** — electrical/charging bench: envelope jig, FO matrix + thermal cam, full 0→100% charge with thermocouple, VDD ripple, TX-on motion test, cable/load steps, single-fault injection (CHG-005), IEC 61000-4-2 ESD, FOD trip, RF pre-scan.
- **Stage 5** — firmware/HID/RF: fusion accuracy jigs, dead-sensor flag, accel ramp, tap/click arbitration (FW-004/006), dropout injection, 100 k-click life, ball-removed drift, DFU recovery incl. bad image and power cut, grab rejection, electrode health, charge-vs-touch coexistence, tri-OS + UEFI plug, Windows bind cycles, two-unit coexistence, wheel life + blind A/B, straightedge calibration, touch latency budget, moisture + nitrile-glove tests.
- **Stage 6** — manufacturing/system ritual: ICT/pogo per unit, line pairing check, 20-trial dot-up parking ritual, lateral-nudge tolerance, pack-out SoC audit, ESS/burn-in, final QA smoke per unit.

### 4.3 V1 exit criteria ("proved we built it right")

1. All 69 **blocker** rules PASS with logged evidence. No waivers.
2. All 276 **major** rules PASS; any waiver needs a written rationale + a V2 tracking issue. Safety majors (CHG-004/005/008/010, ELEC-004/005/006) are never waivable.
3. All 58 **minor** rules PASS or waived with rationale.
4. Stage 1 checks green on the final CAD/schematic revision, checked in alongside fab outputs.
5. Killed rules stay dead: no blanket <50 ms click target reappears; no unvalidatable "premium feel" rule is smuggled back — its measurable proxies (parking ritual 6.3/6.4, blind A/B 5.17) are the contract.
6. Frozen nominals + first-article gates recorded in the build log; every PROVISIONAL flag either cleared or explicitly carried into V2.

---

## 5. Known weakest assumptions (honest list)

1. **V1 FDM process capability is unmeasured.** Runout ≤0.15 mm, diametral ±0.3 mm, wall ±0.15 mm on a 40 mm PETG sphere are *chosen as achievable* on calibrated FDM — no print has been measured yet. Load-bearing verifications: MECH-023 per-spool shrinkage coupon, MFG-001 first-article gate. If the first article fails, the answer is process work (orientation, perimeters, annealing), not waiving the spec.
2. **The 0.2 mm-nozzle process has zero data.** Print time, thermal envelope, mass window, SQUAL floor vs the 0.4 baseline are all unmeasured until MFG-037's first qualification run. The library blocks any 0.2-printed ball from shipping before that run.
3. **Touch-ring 1/2/3-finger disambiguation rests on the unbuilt ELEC-002 coupon.** ≥16 electrodes is an estimate; electrode geometry is still TBD. If the coupon fails, the fallback is not a tweak — it's rethinking the input contract.
4. **Annular TX coil coupling factor k is unmeasured.** The entire charging envelope stacks on the CHG-001 jig test; tank Vpk is unmeasured (CHG-011's cap rating is measurement-first for a reason).
5. **Outsourced-resin εr stack rests on the unbuilt TOUCH-010 batch coupon** for the first supplier lot.
6. **Sensor part not selected.** λ, SQUAL floor, CPI behavior, and lens geometry are all PROVISIONAL — they gate MECH-001, MECH-002, ELEC-007, and FW-001…005. This is the highest-leverage pending decision in the whole project.

---

## 6. Build sequence

### Phase 0 — Sensor selection + first ball print
- **Do:** pick the optical sensor part (λ, SPI interface, lens, SQUAL/CPI curves from datasheet + vendor EVM). Print the first V1 ball (0.4 mm nozzle PETG) with traveler.
- **Exit:** sensor part frozen; ball first article measured (Ø40.0 ±0.3, runout ≤0.15, wall 1.2 ±0.15 at ≥6 pts, weight) per MFG-001/MFG-036; MECH-023 spool coupon on file. If the print misses, iterate process — do not waive.

### Phase 1 — Coupons (gates ALL fab orders)
- **Do:** shell transmission at λ_sensor (MECH-001); flat touch coupon in production shell 1.2 mm — electrode geometry A/B, delta/noise per channel at 20 °C and 45 °C (ELEC-002, TOUCH-001…004); IQS register-map confirmation; annular TX vs disk LCR jig (CHG-001); tank tuning + Vpk in mechanical mockup (CHG-009, CHG-011); sensor Z-shim ladder on EVM (MECH-002, FW-001 inputs).
- **Exit:** 2.1–2.6 PASS. A fail on the touch coupon kills the ring approach before a flex spin; a fail on tank tuning kills the coil geometry before fab. **No flex or PCB is ordered until this phase exits.**

### Phase 2 — Ball electronics
- **Do:** design/order touch-ring flex (electrode geometry frozen from Phase 1); ball PCB (nRF52810-class, charger, coil, antenna at polar ~60° off the ring plane per RF-001/022); assemble first full ball; in-ball SNR per TOUCH-004; ESB link budget vs assembled ball (RSSI, PER); LED/dot-up charging check on the bench TX jig.
- **Exit:** TOUCH-004/007 pass in the assembled ball; radio link margin documented; ball DFU works on the screwed-shut ball incl. bad-image rejection (FW-010 ball side).

### Phase 3 — Base schematic + PCB
- **Do:** base PCB (nRF52840-class, 2× sensor SPI, buttons incl. the front-center scroll button per MECH-049, USB-C per MECH-006, LTC4125 TX + annular coil). Run the full Stage 1 suite on every revision: Blender geometry checks + `kicad-cli` ERC/DRC with `trackball.kicad_dru`. Human layout-review checklist (§4.2 trap list): netclasses, TVS placement, creepage vs measured Vpk, SPI keepaway vs measured coil current, antenna keep-outs, NTC on the cell pouch.
- **Exit:** Stage 1 green on the final revision; layout checklist signed; then fab.

### Phase 4 — Firmware bring-up
- **Do:** sensor drivers + SQUAL-weighted fusion (FW-001) validated on the half-masked-ball jig; dead-sensor/axis logic (FW-002/003); touch processing + click-commitment window 30–50 ms with separated latency targets (FW-006); HID IF0 (boot mouse) and IF1 (vendor telemetry @ 1000 Hz) with stable `protocol_version` ABI; ESB ball↔base link + DFU relay; base USB DFU dual-slot signed (FW-010).
- **Exit:** Stage 5 firmware/HID rows 5.1–5.16 pass; tri-OS + UEFI plug test; 20/20 Windows bind cycles.

### Phase 5 — Charging integration
- **Do:** full 0→100% charge with in-ball thermocouple; envelope + offset jig; FO matrix; single-fault injection (charger forced 4.3 V — secondary must trip every time); FMEA table (CHG-026) with 5 injected faults to safe state; TX-on motion/SQUAL test; dot-up parking ritual 20 trials (≥18/20 LED ≤2 s [est.], zero false-green dot-down).
- **Exit:** Stage 4 + 6.3/6.4 pass. CHG-005 and CHG-026 evidence logged — these are never waivable.

### Phase 6 — System integration + V1 exit
- **Do:** ICT/pogo per unit; line pairing; ESS/burn-in sample lot; per-unit QA ritual (HID + touch + motion + charge smoke); scroll UX matrix (5.17–5.17d) on golden units.
- **Build kit output** (standing requirement): the build phase delivers everything needed to build one and test it — designs, renders, PCBWay/JLCPCB quotes for boards + pick-and-place + components, and a McMaster order if needed. A complete one-unit build kit, not just design files.
- **Exit:** §4.3 V1 exit criteria — all 69 blockers with logged evidence, majors pass or documented-waived (safety majors never waived), Stage 1 green on final revision, build log with frozen nominals and cleared/carried PROVISIONALs.

---

## Appendix A — Conflicts resolved vs Rev 0.2 build spec

Rev 0.2 (`capacitive-trackball-build-spec.pdf`, 2026-09-16) is superseded. The DRC library is authoritative. Resolved conflicts:

1. **Donor Orbit** — Rev 0.2 preserved the Orbit's optics, scroll ring, buttons, and PCB outline. Dead: base is fully custom, no salvaged parts (user decision 2026-09-16; DRC Rev 2.1).
2. **Touch array** — Rev 0.2 specified a 9×8 / 72-intersection spherical flex-gore mutual-capacitance array. Dead: simplified capacitive touch ring, ≥16 self-capacitance electrodes (user decision 2026-09-16; TOUCH-001, ELEC-002).
3. **"Measure the donor ball"** — Rev 0.2 gated CAD on caliper measurements of the donor. Dead: ball spec is frozen custom nominals (Ø40.0 mm); first-article verification replaces donor measurement (DRC Rev 2.1).
4. **Scroll** — Rev 0.2 kept the Orbit scroll ring / listed scroll mechanism as open; an interim revision settled a mechanical detented wheel (MECH-007). **Both dead by user direction 2026-09-17**: scroll is modal — (A) ball motion in-plane while the scroll button is held, (B) two-finger move on the capacitive touch ring. MECH-007/MECH-029/FW-049 killed; contract in UX-001…UX-013 (R287–R297).
5. **Preserved from Rev 0.2** (no conflict): non-Qi dumb-inductive charging with dot-up ritual (LTC4125/TX + RX coil + ferrite); ~120 mAh LiPo [est.]; nRF52810-class ball / nRF52840-class base; MCUBoot + SMP-over-BLE ball DFU commanded over ESB; SWD pogo pads; screwed V1 shell; ~1.2 mm shell wall; ball DFU and bad-image recovery requirements.

## Appendix B — Key file map

- `~/workspace/trackball-drc/RULES.md` — the 403-rule library (Rev 2.3)
- `~/workspace/trackball-drc/ROUND_LOG.md` — 286 adversarial rounds, all kills/merges
- `~/workspace/trackball-drc/VALIDATION_PLAN.md` — staged validation + V1 exit criteria
- `~/workspace/trackball-drc/trackball.kicad_dru` — 10 custom KiCad DRC rules
- `~/workspace/trackball-drc/blender/` — 6 headless geometry checks (30 checks, all passing)
- `~/workspace/trackball-drc/DEDUPE.md` — integration dedupe record
