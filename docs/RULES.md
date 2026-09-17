# Trackball DRC Rule Library

Revision 2.3 — 2026-09-17: INT cross-subsystem integration category (30 rules, R287–R298); Revision 2.2 — 2026-09-17: qualified manufacturing processes for the ball — 0.2 mm-nozzle FDM as a V1 option (MFG-037/038) and outsourced resin printing on the V2 path (MFG-039/040/041); +5 rules from adversarial rounds R276–R285. Revision 2.1 — 2026-09-17: donor ball removed — fully custom ball with frozen nominals (see Ball specification), +8 rules from adversarial rounds R263–R275. Base: Revision 2.0 nine-domain integration (MECH, ELEC, RF, PWR, CHG, FW, HID, TOUCH, MFG, KICAD). Merge base: the original 52 + the direct HID expansion (HID-005…HID-031, R146–R160). Staged: R31–R55, R56–R75, R81–R95, R96–R115, R116–R145, R166–R176, R186–R195, R206–R220. Global dedupe: DEDUPE.md (R221–R262: 8 merged, 5 amended). Round log: ROUND_LOG.md.

## Rule counts (category × severity)

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
| KiCad DRC catalog (KICAD) | 9 | 28 | 2 | 39 |
| Integration (INT) | 5 | 23 | 2 | 30 |
| Scroll UX (UX) | 2 | 9 | 2 | 13 |
| **Total** | **69** | **276** | **58** | **403** |

## Ball specification — frozen nominals (Rev 2.2, 2026-09-17)

The Kensington donor is dead: no salvaged parts. The ball is fully custom;
the values below are CHOSEN and frozen, not estimates awaiting a donor
measurement. Every rule that carried "PROVISIONAL (needs ball diameter)"
now verifies against this spec as a first-article rule.

Rev 2.2 adds qualified manufacturing processes as options — a process is
not a free choice until its qualification rules pass (MFG-037/038 for the
0.2 mm nozzle; MFG-039/040/041 for outsourced resin).

| Parameter | V1 (rough FDM print) | V2 path |
|---|---|---|
| Diameter | **Ø40.0 mm** | Ø40.0 mm |
| Diametral tolerance | ±0.3 mm | ±0.1 mm |
| Radial runout (total) | ≤0.15 mm | ≤0.10 mm |
| Shell wall | 1.2 mm | 1.0 mm |
| Wall tolerance | ±0.15 mm | ±0.05 mm |
| Shell material | FDM PETG, black — 0.4 mm **or** 0.2 mm nozzle, each a separately qualified process (MFG-037/038) | Outsourced resin print (supplier-qualified per MFG-039/040/041, tough/ABS-like class), SLA tough resin, or injection-molded PC/ABS |
| Touch-ring band infill | solid (100%) or ≥4 perimeters | molded solid (resin: solid by process) |

**Justifications.**
- **Ø40.0:** preserves the entire validated geometry stack — sensor patches
  at polar 110° (MECH-003), 24-electrode ring at 5.24 mm pitch / 16-electrode
  minimum at 7.85 mm pitch (TOUCH-001), 19 mm RX coil at the charging pole
  (MECH-010/CHG-001), and the socket/kinematic-cradle geometry (MECH-015).
  It is also the ergonomic standard for thumb trackballs; circumference
  125.66 mm.
- **PETG, black:** lowest warp of the common FDM materials (dimensional
  stability for a sphere without an enclosure), tough (drop survival per
  MECH-039), stable εr ≈ 3.0 for the touch stack, and black for IR opacity
  (MECH-001). PLA rejected (brittle; creeps under the MECH-016 retention
  lip); ASA rejected for V1 (needs enclosure, warps worse).
- **±0.3 mm V1:** achievable on calibrated FDM with per-spool shrinkage
  compensation (MECH-023); sensor Z is protected by the datum strategy
  (MECH-022) plus per-unit calibration (ELEC-007), and MECH-045 budgets the
  radius tolerance into the Z stack.
- **Runout ≤0.15 mm V1:** fits the socket clearance budget
  (0.4 mm clearance ≥ 0.15 runout + 0.2 print tol); 0.10 mm reserved for V2.
- **Wall 1.2 ±0.15 mm:** the ELEC-002/TOUCH-004 coupon gate qualifies this
  exact stack; TOUCH-009 tests ±0.2 mm as margin.

Derived constants used across rules and Blender PARAMS: ball radius 20.0 mm,
ball center height 20.0 mm above socket datum, ring circumference 125.66 mm,
shell inner circumference (ring band) π×37.6 ≈ 118.1 mm.

## Mechanical (47)

### MECH-001 — blocker — PROVISIONAL (needs sensor λ)
**Statement:** Ball shell material shall transmit <1% at the optical
sensor's illumination wavelength λ_sensor through a production-thickness
sample.
**Rationale:** Dye-black resins are often IR-transparent; a translucent
shell lets the sensor see the copper ring/coil moving underneath and
destroys the correlation peak. No finish fixes translucency (R3).
**Validation:** Bench transmission test — 850 nm source (TV remote) through
2 mm shell sample, photodiode or phone camera; PASS <1% transmission.
Gates ball fabrication. Provisional: λ depends on sensor part (630 nm red
vs 850 nm IR).
**Provenance:** R3.

### MECH-002 — blocker
**Statement:** Each sensor's lens reference plane shall sit Z = 2.4 ±0.1 mm
from the ball surface, both sensors.
**Rationale:** Off-focus changes magnification (CPI drift); beyond ~±0.5 mm
[est.] SQUAL collapses. Two sensors at different Z get different CPI → a
constant systematic error in fused ω (R2).
**Validation:** `blender/check_sensor_geometry.py` (Z check per sensor) +
bench Z-shim ladder 2.0–3.0 mm in 0.1 mm steps: PASS = SQUAL above floor
and CPI within ±3% of nominal for Z ∈ [2.3, 2.5] mm.
**Provenance:** R2.

### MECH-003 — blocker
**Statement:** The angle between the two sensors' optical axes (through the
ball center) shall be 80–100° (target 90°); sensors shall never be
co-located or antipodal.
**Rationale:** "90° apart" as mount azimuth does not guarantee 90° optical
axes (75.5° at polar 120°). Rank(A)=3 fails only at 0°/180°, but
conditioning degrades toward those extremes (R1).
**Validation:** `blender/check_sensor_geometry.py` computes the axis angle
from CAD patch coordinates; PASS in [80, 100]°.
**Provenance:** R1.

### MECH-004 — major
**Statement:** Ball total radial runout ≤0.15 mm (V1 rough print) /
≤0.10 mm (V2 molded); fused |ω| ripple <2% peak-to-peak per revolution;
SQUAL ripple <20% of mean.
**Rationale:** Lobing (±0.5% speed error at ±0.1 mm) integrates into cursor
drift and poisons single-patch CPI calibration. Fine uniform texture is
good sensor food; low-frequency lobing is the enemy (R6).
**Validation:** Dial indicator on V-block (runout) + mandrel spin at
constant ω logging fused |ω| vs ball angle. `blender/check_ball_socket.py`
budgets runout into socket clearance (runout_max = 0.15 V1 / 0.10 V2).
**Provenance:** R6; Rev 2.1 split V1/V2 (0.15 mm achievable on calibrated
FDM; 0.10 mm reserved for molded V2).

### MECH-005 — major
**Statement:** Both optical sensors shall mount on one rigid PCB, screwed to
the socket. No flex, no separate stalks, between the sensors.
**Rationale:** Differential shake between two sensor boards injects fake
differential velocity = phantom rotation, worst when clicking (R10).
**Validation:** Tap/click test with ball parked: zero-motion RMS <1 count
at 1 kHz; ≤2 counts displacement per click event (see FW-004).
**Provenance:** R10.

### MECH-006 — major
**Statement:** USB-C receptacle shall be mid-mount (hybrid) with ≥4
through-hole shield legs (no thermal relief on shield legs) + 2 locating
pegs; enclosure shall capture the cable jacket in a boss before the
receptacle; total base mass ≥200 g [est.] via steel weight insert.
D+/D− routed as 90 Ω differential pair, length match <0.5 mm [est.].
**Rationale:** #1 field-return driver on USB-C peripherals is pad lift;
a light base drags instead of unmating, converting a yank into a drop
(R22, severity challenged and upheld).
**Validation:** `blender/check_buttons_usb.py` (retention envelope:
strain boss ≤12 mm behind connector, exit-zone height check, mass calc) +
force-gauge pull 30 N axial / 20 N lateral × 5 cycles (PASS: no pad lift,
continuity, extraction still 6–20 N) + 1 m drop (PASS: mates + enumerates).
**Provenance:** R22.

### MECH-008 — major
**Statement:** Button top surfaces below the ball equator plane and ≥8 mm
[est.] lateral clearance from the ball surface; primary switches Omron
D2FC-F-7N class (or Kailh GM 8.0), actuation force 0.6–0.9 N [est.].
**Rationale:** Prevents accidental actuation while rolling; 0.74 N click vs
~0.05–0.2 N [est.] rolling force gives 4–10× separation. SMT tactile domes
rejected for primary clicks (life/feel vs the $300 benchmark).
**Validation:** `blender/check_buttons_usb.py` (equator + lateral
clearance) + force gauge + 5-user roll test, 2 min each: zero unintended
clicks logged.
**Provenance:** R10 (button placement), worker-D §5.

### MECH-009 — minor
**Statement:** Touch-ring flex bend radius ≥10× flex thickness; no 90°
trace bends at the bend apex (teardrops/curved routing); copper kept off
the neutral-axis extremes where possible.
**Rationale:** Fatigue cracks at bend apexes → open (dead sector) or
hairline-intermittent (phantom taps masquerading as firmware bugs).
**Validation:** 1,000-cycle thermal shock (−20/+60 °C [est.]) + 50× 1 m
drops: PASS if all electrode baselines stay within ±10% [est.] and no
channel rails; firmware continuity self-test (FW-012) catches field
failures.
**Provenance:** Worker-B F14.

### MECH-010 — minor
**Statement:** RX coil face ≤1 mm from the ball inner shell surface at the
charging pole; socket shall locate the parked ball repeatably (dot-up
parking within the CHG-002 envelope).
**Rationale:** Minimizes coil-to-coil gap; repeatable seating makes the
charging envelope testable (R18/R21).
**Validation:** `blender/check_coil_keepouts.py` (RX coil placement) +
gap/offset jig sweep (CHG-002).
**Provenance:** R18, worker-C FM-2.

---

### MECH-011 — major
**Statement:** Ball center-of-mass offset from geometric center ≤0.5 mm
[est.]; heavy components (cell, RX coil) placed symmetric about the
dot–pole axis.
**Rationale:** An imbalanced 40 mm ball wobbles when spun at 2–5 rev/s and
rolls to CG-lowest when parked — which may or may not be dot-up. A
CG-lowest bias toward the charging pole is acceptable (even helpful for
parking); an arbitrary bias is not (R31).
**Validation:** Static-balance test (ball on a level air/needle fixture:
no preferred rest orientation beyond the designed pole bias) + mandrel
spin at 3 rev/s: no visible wobble, |ω| ripple within MECH-004 limits.
**Provenance:** R31.

### MECH-012 — major
**Statement:** Ball exterior texture shall be fine and uniform: SQUAL
variance ≤20% [est.] of mean across ball angle at constant ω on a mandrel.
If the as-printed surface fails, apply bead-blast or vapor-hone as a
specified process step — never hand-sanding to an undefined finish.
**Rationale:** 0.2 mm layer ridges create a periodic correlation feature
at the layer frequency: SQUAL looks healthy while the correlation peak
jitters. MECH-004's runout bound does not catch corrugation (R32).
**Validation:** Mandrel spin at constant ω logging SQUAL vs ball angle per
sensor; PASS = variance ≤20% of mean on both sensors.
**Provenance:** R32.

### MECH-013 — major
**Statement:** Ball shell split-line seam step ≤0.15 mm [est.]; halves keyed
with ≥2 alignment pins; seam plane documented in CAD.
**Rationale:** The ball spins, so the seam sweeps through both sensor
patches every revolution — a 0.1–0.2 mm step reads as a giant correlation
feature (per-rev count jump) plus a dielectric step under the touch ring
(R33).
**Validation:** `blender/check_ball_socket.py` (seam step + pin count) +
feeler/indicator measurement of the seam on first article; mandrel spin
shows no per-rev count discontinuity attributable to the seam.
**Provenance:** R33.

### MECH-014 — major
**Statement:** Touch-ring flex-to-shell gap ≤0.3 mm [est.] maximum anywhere
on the ring, held by a retaining lip/cradle molded/printed into the shell
— not by adhesive alone.
**Rationale:** Uncontrolled electrode lift-off (0–1 mm around the ring on a
20 mm-radius sphere) varies per-electrode touch delta ~3:1 → dead and hot
sectors that masquerade as firmware bugs (cf. MECH-009, R34).
**Validation:** Per-electrode touch-delta variance ≤20% [est.] across the
ring on the assembled ball (same coupon method as ELEC-002, on the
finished assembly).
**Provenance:** R34.

### MECH-015 — blocker
**Statement:** The socket shall locate the parked ball kinematically:
≥3 contact points (tri-lobed cradle), parked lateral repeatability
≤0.5 mm [est.].
**Rationale:** A smooth spherical socket under-constrains the ball; parking
offset becomes luck, and CHG-002's 3 mm envelope cannot be relied on. The
kinematic cradle makes the charging envelope testable (R35).
**Validation:** `blender/check_ball_socket.py` (contact geometry vs
repeatability budget) + 20 park cycles from random orientations: lateral
offset of the parked ball ≤0.5 mm, 20/20.
**Provenance:** R35.

### MECH-016 — major
**Statement:** Ball extraction force 2–8 N [est.] via a retention lip:
the ball shall not fall out at 90° base tilt, and shall be removable by
hand with no tools.
**Rationale:** A removable-for-cleaning ball that escapes when the base is
tilted is an unplanned drop test of the most expensive subassembly. The
force window matters both ways: too loose = escape, too tight = cleaning
becomes a service event (R36).
**Validation:** Tilt table to 90° (ball stays) + pull gauge (2–8 N
extraction), 20 cycles; then 50 °C [est.] 24 h soak and re-test: PASS =
still 2–8 N and ball retained at 90° tilt. Re-run for EACH qualified
ball process (0.4 PETG, 0.2 PETG, outsourced resin) — resin's lower
heat-deflection temperature makes the soak strictly harder for it than
for PETG (R283).
**Provenance:** R36; Rev 2.1 added hot-soak re-test (custom PETG ball
creeps where a donor ball didn't); Rev 2.2: per-process re-run.

### MECH-017 — major
**Statement:** Breakaway torque to start the ball rolling ≤0.5 mN·m [est.]
after 24 h static dwell at 25 °C. Socket contact surfaces shall be PTFE
(MECH-018 pads) against the polished ball — never resin-on-resin.
**Rationale:** Resin-on-resin stiction after overnight parking makes the
first roll of the day need a yank; the cursor jump reads as a sensor
fault (R37).
**Validation:** Torque watch: park ball 24 h, measure breakaway torque;
PASS ≤0.5 mN·m, and steady rolling torque within MECH-044.
**Provenance:** R37.

### MECH-018 — major
**Statement:** Socket contact points shall be replaceable PTFE wear pads
(at the MECH-015 kinematic contacts), not printed resin. After a 10k-rotation
wear test: clearance growth ≤0.1 mm [est.] and MECH-015 parking
repeatability re-verified.
**Rationale:** Ball-on-resin wears grooves → clearance grows → parking
repeatability dies → CHG-002 fails at month six looking like a charging
regression (R38).
**Validation:** 10k-rotation wear rig (motor-driven ball), measure socket
clearance before/after (≤0.1 mm growth), re-run the 20-cycle park test.
Pads replaceable with the shell opened (ties to MECH-037).
**Provenance:** R38.

### MECH-019 — major
**Statement:** Sensor cavities shall be protected by labyrinth + gravity
shed: well placement and lip geometry such that debris falls away from the
optical path, plus a cleaning port accessible without full disassembly.
**Rationale:** The ball sheds debris into the socket; wells below collect
it and SQUAL decays over weeks until someone disassembles the product
(R39).
**Validation:** Talc dust test: 1 g talc cycled through the socket with
the ball rolling, then SQUAL re-measured; PASS = degradation <15% [est.]
vs pre-dust on both sensors.
**Provenance:** R39.

### MECH-020 — major
**Statement:** Sensor well bores shall be printed support-free (bore axis
within 45° of vertical, or soluble supports) or post-print reamed to size;
no support-material contact allowed inside the bore.
**Rationale:** Support scars and wisps in the bore shadow the illumination
field → asymmetric SQUAL that ELEC-007's calibration then bakes in as a
permanent scale error (R40).
**Validation:** Bore gauge (go/no-go) + 10× visual inspection of every
first-article well; SQUAL symmetry check between the two sensors before
calibration.
**Provenance:** R40.

### MECH-021 — blocker
**Statement:** As-built sensor well-bore axis tilt ≤1.5° [est.] from the
design optical axis, both wells.
**Rationale:** On a rough print the bore follows the layer normal, not the
CAD axis. A 2° tilt silently moves the true optical axis outside MECH-003's
validated window while the CAD check still passes (R41).
**Validation:** `blender/check_sensor_geometry.py` (well-tilt check, tilt
carried as a measured parameter) + indicator sweep of each well bore on
first article.
**Provenance:** R41.

### MECH-022 — major
**Statement:** A single datum chain shall be documented: datum A = ball
center as realized by the socket bore; datum B = sensor-PCB locating
features cut directly into the socket part (never the base shell); no
datum through a compliant feature. Worst-case stack to the lens plane
≤0.25 mm [est.].
**Rationale:** Six printed features chain into MECH-002's ±0.1 mm Z;
without a datum strategy the worst-case stack (±0.3 mm+) makes the rule
unbuildable (R42).
**Validation:** Datum diagram in CAD + stack-up sheet: worst-case sum
≤0.25 mm; residual absorbed by ELEC-007 per-unit calibration (verified by
the calibration's scale-spread check).
**Provenance:** R42.

### MECH-023 — blocker
**Statement:** Per-spool shrinkage calibration: print a calibration coupon,
measure XY/Z scale factors, apply them to the socket bore and all mating
features; as-printed socket bore within ±0.15 mm [est.] of nominal before
any assembly.
**Rationale:** Uncompensated FDM shrinkage (0.5–1% XY) turns a 40 mm bore
into 39.6 mm → the ball binds and MECH-004's clearance budget is blown
before assembly starts (R43).
**Validation:** Coupon measurement log per spool + caliper/CMM of the
socket bore; PASS = bore within ±0.15 mm of nominal. Gates shell
fabrication.
**Provenance:** R43.

### MECH-024 — major
**Statement:** The sensor PCB shall mount with slotted holes: slot length ≥
computed resin-vs-FR4 differential growth over the operating range + 0.2 mm
[est.] margin; screws with shoulder clearance, torqued to spec.
**Rationale:** Resin CTE ≈ 70 ppm/°C vs FR-4 ≈ 14 ppm/°C → ~0.13 mm
differential over 40 °C × 60 mm. Screwed tight, the PCB bows or screws
bind, and MECH-002's Z walks with temperature looking like sensor drift
(R44).
**Validation:** Thermal cycle −10/+50 °C [est.] × 10: no screw loosening
(torque re-check), lens Z re-verified within MECH-002 after cycling.
**Provenance:** R44.

### MECH-025 — blocker
**Statement:** Heat-set brass inserts (M2.5 class) at every screw seeing
repeated load or vibration (sensor PCB, socket, shell halves); boss OD ≥
2.2× insert OD [est.], boss depth ≥ insert length. No self-tapped screws
in resin for structural joints.
**Rationale:** Self-tapped screws in resin strip at 20–40 N and loosen
under click vibration; when the sensor-PCB screws loosen, MECH-005's
rigid mount becomes a rattle injecting phantom rotation (R45).
**Validation:** Pullout test ≥80 N [est.] per boss + 10k-cycle vibration
table with torque re-check (no loosening). Gates assembly and the shell tooling/DfM release (former MFG-019, R191).
**Provenance:** R45 + R191; merged per R225 (DEDUPE.md).

### MECH-026 — major
**Statement:** No sustained structural load shall bear on bare printed
plastic: inserts + washers under every preload, bearing-stress limits
noted in CAD. Validation: 1000 h constant-load boss deflection at 40 °C
[est.]: deflection ≤0.1 mm [est.], preload loss ≤20% [est.].
**Rationale:** Resin creeps under constant screw preload and spring force →
months-later rattles, Z drift, and button-feel change. A "retorque every
6 months" maintenance rule was killed as unvalidatable; the creep must be
designed out (R46).
**Validation:** Dead-weight boss creep rig at 40 °C, 1000 h: deflection
and preload loss within limits.
**Provenance:** R46.

### MECH-027 — major
**Statement:** Button overtravel stack: ≥0.15 mm [est.] of switch
overtravel shall remain when the button cap reaches its shell stop (the
cap shall never bottom out before the switch's overtravel is consumed).
**Rationale:** Cap-bottoming first = dead-feeling clicks, impact load into
the shell at every press, and eventual aperture cracking (R47).
**Validation:** `blender/check_buttons_usb.py` (overtravel stack check) +
stack measurement on first article (shim/indicator).
**Provenance:** R47.

### MECH-028 — minor
**Statement:** Radial gap around button caps ≤0.25 mm [est.]; caps removable
for cleaning without tools beyond the service driver.
**Rationale:** The cap gap admits crumbs and debris → jamming and feel
degradation. Small enough to block most debris, large enough to never bind
(R48).
**Validation:** Feeler gauge on first article + crumb test (0.5 mm
granules): no jam after 100 press cycles; caps removable per MECH-037.
**Provenance:** R48.

### MECH-030 — major
**Statement:** USB-C enclosure aperture shall clear a 15×9 mm [est.]
plug-body envelope with ≥0.5 mm clearance per side.
**Rationale:** Premium braided cables carry 12–14 mm plug housings; a tight
aperture turns "doesn't fit my cable" into a return (R50).
**Validation:** `blender/check_buttons_usb.py` (aperture envelope check) +
gauge-plug fit test with a 15×9 mm reference plug body.
**Provenance:** R50.

### MECH-031 — major
**Statement:** Internal USB cable service loop ≥25 mm [est.]; cable bend
radius ≥4× cable OD everywhere inside the enclosure.
**Rationale:** No slack means the USB-C connector takes full assembly
strain and every tug transmits into MECH-006's solder joints (R51).
**Validation:** `blender/check_buttons_usb.py` (service-loop + bend-radius
check) + assembly trial: connector mates with zero cable tension.
**Provenance:** R51.

### MECH-032 — major
**Statement:** Tip-over angle ≥30° [est.] in any direction with the ball
parked; CG projection within the central 30% of the footprint.
**Rationale:** MECH-006 made the connector survive a yank, but a 200 g
base still tips instead of unmating — the drop MECH-006 warned about,
unaddressed (R51).
**Validation:** `blender/check_base_stability.py` (tip angle from CG height
+ footprint) + tilt table per direction, cable attached and snagged.
**Provenance:** R51.

### MECH-033 — minor
**Statement:** Feet friction μ ≥0.45 [est.] on glass and matte laminate;
slide force ≥1.5× peak rolling force on both surfaces.
**Rationale:** Hard printed feet on glass = hockey puck; MECH-008's
0.05–0.2 N rolling force slides the base instead of the ball (R52).
**Validation:** `blender/check_base_stability.py` (slide-force calc) +
push-gauge slide test on glass and laminate.
**Provenance:** R52.

### MECH-034 — major
**Statement:** A mechanical Interface Control Document shall freeze, across
all shell iterations (V1 rough print → V2): datum features, screw/insert
positions, sensor well geometry, socket bore diameter, and connector
cutouts. V2 shell changes go through the ICD.
**Rationale:** "We iterate" without a contract means every shell re-spin
silently breaks sensor alignment, screw positions, and ball fit (R52).
**Validation:** ICD checklist sign-off per shell revision; V2 shell
assembles to V1 internals with zero rework (assembly trial).
**Provenance:** R52.

### MECH-035 — major
**Statement:** A documented assembly sequence with interference-free order
(RX coil before touch-flex fold, dot verification before halves close)
shall exist and shall be proven by a trial build with zero rework steps.
**Rationale:** Assembly order is a design constraint, not tribal knowledge:
the coil cannot be installed after the flex is folded, and the dot cannot
be verified after the halves close (R53).
**Validation:** Written sequence + trial build log: zero rework steps,
zero forced fits.
**Provenance:** R53.

### MECH-036 — major
**Statement:** Orientation dot antipodal to the charging pole within ≤3°
[est.], measured at assembly with a pole/dot jig.
**Rationale:** The dot is the ball's only absolute angular reference. 10°
of misalignment parks the ball ~3.5 mm off the coil center — outside
CHG-002's envelope — with zero indication (R53).
**Validation:** `blender/check_ball_socket.py` (dot-angle parameter) +
pole/dot jig measurement at assembly; reject >3°.
**Provenance:** R53.

### MECH-037 — major
**Statement:** Full disassembly with ≤6 fasteners of a single drive type;
sensor PCB removable without desoldering; ball opens with no tools beyond
the service driver; wear pads (MECH-018) replaceable in the same
operation.
**Rationale:** A screwed-shut product that needs desoldering to service is
e-waste with extra steps; FW-010's SWD pogo pads are useless if reaching
them destroys the assembly. (Single-drive-type screws merged here, R54.)
**Validation:** Timed teardown/reassembly by a technician unfamiliar with
the build: ≤10 min [est.], no solder iron, all fasteners captured or
counted.
**Provenance:** R54.

### MECH-038 — major
**Statement:** The TX coil compartment shall have baffled vents (baffled so
they are not a dust path into the sensor cavities per MECH-019);
compartment ΔT ≤15 °C [est.] above ambient at full charge current.
**Rationale:** Up to 0.8 W (CHG-001) heat-soaks a sealed resin base:
sensor-PCB drift plus softened resin around standoffs feeding MECH-026
creep (R54).
**Validation:** Thermocouple in the TX compartment during a full charge at
25 °C ambient: ΔT ≤15 °C; dust test (MECH-019) re-run to confirm the
baffles don't admit dust.
**Provenance:** R54.

### MECH-039 — major
**Statement:** Ball 1.2 m drop onto hardwood, 6 orientations: halves stay
mated, no rattle, LED/dot legible, all electrode baselines within ±10%
(ELEC-002 criteria).
**Rationale:** The 40 mm ball *will* hit the floor; MECH-009's drops
validate the flex, not the shell joint (R55).
**Validation:** Drop rig, 6 orientations × 3 drops; PASS criteria as
stated; electrode health via FW-012 self-test after.
**Provenance:** R55.

### MECH-040 — major
**Statement:** Sensor PCB clamped flatness over the sensor region ≤0.1 mm
[est.] under full screw preload.
**Rationale:** A PCB bowed by its own standoff screws carries a Z error
straight into MECH-002 — per-sensor, so ELEC-007 sees it as a scale
spread (R55).
**Validation:** Indicator sweep of the clamped PCB on first article;
standoff height matched within 0.05 mm [est.] (shim if needed).
**Provenance:** R55.

### MECH-041 — major
**Statement:** Cable exit edge break ≥0.5 mm radius [est.] or a fitted
grommet; 10k flex cycles with no jacket damage.
**Rationale:** Even with MECH-006's strain boss, the exit edge saws the
jacket over thousands of desk micro-movements; jacket failure precedes
conductor fatigue (R50).
**Validation:** `blender/check_buttons_usb.py` (exit chamfer check) +
10k-cycle flex rig, jacket inspected under 10×: no damage.
**Provenance:** R50.

### MECH-042 — major
**Statement:** Base 1.2 m drop matrix, 6 orientations: weight insert, buttons,
sensor PCB, and connectors stay retained — no rattle, insert shift
≤0.2 mm [est.], sensors re-pass the MECH-002 Z-shim check after.
**Rationale:** MECH-006's drop test has USB-specific pass criteria; the
internal retention of insert/buttons/sensors needs its own (R55).
**Validation:** Drop rig 6 orientations; rattle test, insert position
remeasure, Z-shim ladder re-run.
**Provenance:** R55.

### MECH-043 — major — PROVISIONAL (weight insert geometry TBD)
**Statement:** The steel weight insert shall be captured by ≥2 screws (steel weight insert — not the MECH-025 threaded insert)
never glue alone (glue creeps per MECH-026 and kills MECH-037
serviceability).
**Rationale:** MECH-006 requires the 200 g mass but never said how it
stays put; a glued insert is a drop-test failure and a serviceability
failure waiting to happen (R55).
**Validation:** `blender/check_base_stability.py` (screw count + pocket
clearance) + MECH-042 drop matrix: insert shift ≤0.2 mm.
**Provenance:** R55.

### MECH-044 — major
**Statement:** Steady-state ball rolling torque ≤2 mN·m [est.]; spin-down
from 2 rev/s ≥8 s [est.] on the finished socket with PTFE pads.
**Rationale:** The ball should spin like a premium trackball, not a sticky
knob; rolling effort is the primary feel metric and it is currently
unspecified (R55).
**Validation:** `blender/check_ball_socket.py` (torque budget parameter) +
torque-watch spin test and spin-down timing on the finished assembly.
**Provenance:** R55.

### MECH-045 — major
**Statement:** Ball radius tolerance (±0.15 mm V1) shall be carried through
the cradle geometry into the MECH-002 sensor-Z stack-up: for the 3-point
kinematic cradle (contact circle rc), center-height shift ≈ Δr ×
r/√(r²−rc²) (≈1.4×Δr at r=20, rc=14), projected onto each sensor's optical
axis. Worst-case Z shift plus the MECH-022 datum stack shall fit inside
MECH-002's ±0.1 mm; any residual is absorbed by ELEC-007 per-unit
calibration, verified by the calibration's scale-spread check.
**Rationale:** A small ball sits deeper in the cradle; ±0.15 mm radius
moves the center ≈±0.21 mm vertically, ≈±0.07 mm along the sensor optical
axis — 70% of the Z budget before print tolerance is counted (R264).
Without this rule the tolerance we chose for the ball silently eats the
tolerance we chose for the sensors.
**Validation:** Stack-up sheet with the cradle projection math +
Z-shim ladder (MECH-002 validation) repeated on min-diameter and
max-diameter first articles; PASS = SQUAL/CPI criteria hold on both.
**Provenance:** R264.

### MECH-046 — major
**Statement:** FDM Z-seam (layer start/stop ridge) height ≤0.05 mm [est.]
via scarf or distributed seam placement; the seam azimuth shall be
documented in the print profile. No per-revolution count discontinuity
>2 counts [est.] attributable to seam azimuth on mandrel spin.
**Rationale:** The Z-seam is a vertical ridge spanning all latitudes — it
sweeps both sensor patches once per rev. MECH-013 covers the shell
split-line; this covers the print artifact, which exists on every layer
(R265).
**Validation:** Print profile audit (seam mode = scarf/distributed) +
mandrel spin at constant ω: fused-count trace vs ball angle shows no
>2-count step repeating at 1/rev.
**Provenance:** R265.

### MECH-047 — major
**Statement:** The ball shell split plane shall contain the dot–pole axis
(polar split), never equatorial: the seam shall avoid the touch-ring band
(polar 75–105°) and both sensor read patches (polar ~110°) by ≥10°
[est.] of latitude at every azimuth.
**Rationale:** An equatorial split puts the MECH-013 seam step directly
under the touch ring (dielectric step → touch artifact) and through both
sensor patches (correlation step → count jump) — the worst placement on
the sphere (R266). A polar split keeps the seam in the socket-shadowed
region between the read patches.
**Validation:** CAD review (split plane documented, latitude clearance
checked) + `blender/check_ball_socket.py` seam-plane check; MECH-013's
mandrel-spin test must show no per-rev discontinuity at seam azimuth.
**Provenance:** R266.

### MECH-048 — major
**Statement:** In the ball/PTFE-pad wear couple, the replaceable pad shall
be the wear element: after the 10k-rotation wear test, ball diameter loss
≤0.05 mm [est.] at the contact latitudes.
**Rationale:** If the PETG ball wears instead of the PTFE pad, the
expensive subassembly becomes the consumable and MECH-004's runout budget
is eaten from the wrong side (R267). PTFE-on-PETG usually favors pad
wear, but filled/abrasive filaments invert it — the rule measures rather
than assumes.
**Validation:** Micrometer diameter at 3 contact latitudes before/after
the 10k-rotation rig (same rig as MECH-018); PASS ≤0.05 mm loss.
Re-verify MECH-015 parking repeatability after. Re-run for EACH
qualified ball process — the PETG result does not transfer to resin,
which is harder and more abrasive (R284).
**Provenance:** R267; Rev 2.2: per-process re-run.

### MECH-049 — major
**Statement:** The scroll button (third button, front-center) shall be holdable with the thumb while the index/middle fingers roll the ball: cap diameter Ø12–14 mm [est.], top surface 0.5 mm [est.] recessed below the L/R caps, concave-dish cap profile tactilely distinct from the convex L/R caps, and the cap center inside the thumb reach arc (≤45 mm [est.] from the ball center at the equator plane) with MECH-008's ≥8 mm lateral ball clearance maintained.
**Rationale:** Hold-while-rolling is the primary scroll method — the button is a sustained-hold control, not a tap target. A small/flush cap fatigues the thumb; a proud cap gets brush-pressed during aggressive rolls (R289); an indistinguishable cap can't be found blind. Hold fatigue is managed by cap size, never by a stiffer switch (click-feel consistency vs the $300 benchmark).
**Validation:** `blender/check_buttons_usb.py` (reach envelope + recess + clearance checks) + 5-user hold-while-rolling test, 2 min each: zero unintended actuations logged, and users locate the scroll button blind 10/10.
**Provenance:** R287–R289 (scroll-UX rounds).

## Electrical (38)

### ELEC-001 — major — PROVISIONAL (part not selected)
**Statement:** Prefer 16-bit-delta, SPI-burst, programmable-lift-cutoff
sensors (PMW3360/PAW3395 class). If an 8-bit part is used, polling shall be
fast enough that ±127 counts/read cannot saturate at max surface speed,
and saturation events shall be logged, never silently clipped.
**Rationale:** 8-bit saturation at ±127 counts (2.0 mm/poll at 1600 CPI)
corrupts the fused axis on fast flicks (R9).
**Validation:** Max-flick test: no saturation events in log at ~2 m/s [est.]
surface speed; lift-cutoff register doubles as a health signal.
**Provenance:** R9.

### ELEC-002 — blocker — PROVISIONAL (needs coupon test)
**Statement:** Touch ring ≥16 electrodes; electrode arc width ≈ 2× overlay
thickness (≈2.5–3 mm at 1.2 mm shell); per-electrode touch delta ≥5× the
channel's peak-to-peak noise floor; raw baselines 20–80% [est.] of the ATI
target range at both 20 °C and 45 °C shell temperature. A flat coupon in
production shell material/thickness shall pass these criteria BEFORE the
ring flex is ordered.
**Rationale:** The 95%-parasitic problem: too-small electrodes drown in
noise, too-large rail the ATI with no temperature headroom. The coupon
gates the entire input device (R12).
**Validation:** Bench coupon measurement per electrode; PASS criteria as
stated. Flex order is blocked on this test.
**Provenance:** R12.

### ELEC-003 — blocker
**Statement:** No electrode copper within 5 mm [est.] of the RX coil edge;
no electrode traces routed over the coil footprint; electrode geometry
frozen before FTH calibration.
**Rationale:** Eddy-current loading from copper near the coil moves the
FOD frequency baseline; a late reroute silently eats the FOD margin either
toward false trips or toward a safety hole (R17).
**Validation:** `trackball.kicad_dru` rule `chg_rx_coil_to_touch_keepout`
(5 mm clearance, netclasses COIL_RX vs TOUCH) + bench Δf <2% [est.]
bare-coil vs fully assembled ball (worker-C FM-5).
**Provenance:** R17.

### ELEC-004 — major
**Statement:** Ball ESD: 560 Ω series resistor at each Cx pin; ≤1 pF
low-capacitance TVS (SP3001-class, not generic 5–50 pF) on exposed lines;
in-ball MCU shall detect IQS I2C non-response and pulse NRST to force
autocalibration.
**Rationale:** Handled ball = kV-level events 1.2 mm from the electrodes;
a latched IQS in a sealed ball is a brick without a recovery path (R28).
**Validation:** IEC 61000-4-2 contact ±4 kV / air ±8 kV at 8 shell points,
10 strikes each: PASS = no hard failure, function recovers ≤2 s [est.] via
NRST without power cycle, F4-equivalent SNR still passes after.
**Provenance:** R28.

### ELEC-005 — blocker
**Statement:** Base ESD: IEC 61000-4-2 Level 4 (±8 kV contact / ±15 kV air),
performance criterion B (self-recovery, no latch-up/damage/FW corruption).
USB-C shell tied to the CHASSIS net via the through-hole shield legs (mechanical retention is MECH-006); CHASSIS → signal ground through 1 MΩ ∥ 4.7 nF per ELEC-038 — the hard short is explicitly rejected (R230, DEDUPE.md);
D+/D− TVS array <5 mm from the connector, C < 4 pF, Vrwm ≥ 3.3 V,
IEC-rated ≥ ±8 kV contact (TPD2E1B06-class); VBUS TVS; CC-line protection;
grounded guard pour around button apertures; enclosure seam gaps <1 mm
[est.] with overlapping lips; no floating metal.
**Rationale:** The USB shell is the first thing a discharge hits; the TVS
ground return must be short/wide or the protection is fiction (R28).
**Validation:** IEC gun at Level 4, 10 discharges per polarity per point
(shell, buttons, plug shield, seams, socket): PASS = criterion B or
better, automatic USB re-enumeration if a reset occurs.
**Provenance:** R28.

### ELEC-006 — major
**Statement:** Sensor SPI lines: TVS array + 22–47 Ω [est.] series
resistors; firmware shall watchdog SQUAL and product-ID registers and
re-initialize a sensor returning garbage within 100 ms.
**Rationale:** A latched sensor feeds one insane row into the fusion
matrix → fused ω garbage on a dry winter day (R28, worker-A mode 8).
**Validation:** Included in the ELEC-005 gun test: PASS = no spurious
motion >5 counts per event; upset sensor re-inits ≤100 ms.
**Provenance:** R28.

### ELEC-007 — minor
**Statement:** Per-unit calibration: fixture-spin the ball about three
known orthogonal axes; solve the full 4×3 fusion matrix A and per-sensor
scale s_i by least squares; store in flash. Reject any assembly whose
calibrated s_i differ by >5% [est.]. Re-run after any disassembly.
**Rationale:** Lens tilt, die rotation, and PCB skew make the CAD A-matrix
a fiction; a 2° basis error injects ~3.5% cross-axis error — a permanent
invisible curve in the pointer (R2, worker-A mode 10).
**Validation:** Straightedge roll per axis after calibration: off-axis
residual <2% of on-axis counts; repeat after disassembly/reassembly.
**Provenance:** R2.

### ELEC-008 — minor
**Statement:** Status-LED light-pipe aperture: ≥3 mm [est.] copper
keep-out radius; no LED drive traces under electrodes; LED driven DC or
PWM >20 kHz [est.] (no beating with the cap-scan).
**Rationale:** Dielectric discontinuity at the dot plus switching noise
next to the one absolute angular reference (R16/R13 of worker-B).
**Validation:** F4-equivalent SNR on the two electrodes flanking the dot
with LED at full brightness and PWM extremes: noise floor unchanged vs
LED off; centroid interpolation across the gap monotonic.
**Provenance:** Worker-B F16.

---

### ELEC-009 — major — PROVISIONAL
**Statement:** Each nRF52840 (base) / nRF52810-class (ball) VDD and VDDH supply pin gets one 100 nF X7R 0402 capacitor; capacitor pad to MCU pad trace length ≤2 mm (PROVISIONAL), with a direct via to the GND plane at the capacitor's ground pad. **Rationale:** HF bypass loop inductance dominates RF spur and RX desense on the 2.4 GHz SoC; distance is the control variable. **Validation:** layout review — KiCad measure tool pad-edge to pad-edge ≤2 mm, recorded in review checklist; `kicad-cli pcb drc --output drc.json` clean on connectivity. **Provenance:** R56.

### ELEC-010 — major
**Statement:** Bulk ceramic capacitance 4.7–10 µF (X7R/X5R, ≥10 V) within 10 mm of each IC rail entry: base MCU 3V3 input, sensor LDO input, LTC4125 VIN (complements PWR-001's ≥100 µF TX-input reservoir — R234). **Rationale:** transient charge reservoir for TX coil switching bursts and radio TX pulses; distinct from per-pin HF bypass. **Validation:** schematic BOM value check + layout review bounding-box measure ≤10 mm; bench: TX burst load step, rail dip ≤5%. **Provenance:** R56.

### ELEC-011 — major
**Statement:** One continuous GND plane on each board; no splits, moats, or necked regions under high-speed nets. Analog sensor filtering is done with local ferrite bead + capacitors, never with a plane split. The TX coil return runs as a dedicated ≥1 mm trace to the LTC4125 GND pad before joining the plane. **Rationale:** splits become slot antennas at 2.4 GHz and return-path discontinuities for 12 MHz SPI; the TX return star contains 50–250 kHz switching current. **Validation:** `kicad-cli pcb drc` — zero "unconnected items" on GND; zone-fill review confirming single plane. **Provenance:** R57 (star-ground candidate MERGED in).

### ELEC-012 — major — PROVISIONAL
**Statement:** Sensor SPI bus (netclass SPI): SCLK ≤ device f_max (PMW3360: 2.0 MHz per datasheet §2.2; PAW3395-class: ≤12 MHz design target, confirm in datasheet); SCLK source series termination 22–47 Ω at the MCU; total routed length ≤150 mm (PROVISIONAL); intra-bus length match within ±10% of SCLK. **Rationale:** dual-sensor shared bus in a 50–250 kHz high-current switching environment; termination damps ringing, length cap bounds skew and antenna pickup. **Validation:** KICAD-028 length constraint + `kicad-cli pcb drc`; BOM check of series R; bench (when SCLK ≥8 MHz): scope SCLK at sensor pin, overshoot ≤10% of VDDIO. **Provenance:** R58.

### ELEC-013 — major — PROVISIONAL
**Statement:** Sensor rails stable ≥10 ms (PROVISIONAL) before the first SPI transaction; VDDIO ≥ VDD at all times (PMW3360 datasheet §2.2). Guaranteed by a schematic-present element (supervisor, sequencer, or load-switch with power-good) or by a documented firmware gate proven with a power-cycle + logic-analyzer capture. **Rationale:** brownout-mid-init bricks the sensor into undefined state; VDDIO < VDD violates absolute maximum. **Validation:** `kicad-cli sch export netlist` + script checking for guarantee element on sensor rails, or LA capture showing ≥10 ms stable rail before first SCLK edge. **Provenance:** R59.

### ELEC-014 — minor
**Statement:** Each optical sensor NCS has a 10 kΩ (±20%) pull-up to VDDIO; NCS is never left floating through MCU reset/boot. **Rationale:** prevents bus contention and phantom-powering of the sensor while the MCU pins are Hi-Z. **Validation:** netlist scan — every net matching `*NCS*`/`*CS_*SENSOR*` has a 8–12 kΩ resistor to VDDIO. **Provenance:** R59.

### ELEC-015 — minor
**Statement:** Every mechanical switch input has a defined idle level (pull-up/down resistor or documented internal pull + schematic note) and a debounce mechanism: RC τ 1–10 ms or firmware counter ≥5 ms, documented in the schematic note or firmware spec. **Rationale:** floating inputs + contact bounce = phantom clicks and wake storms; base is USB-powered so firmware debounce is acceptable, but it must be explicit. **Validation:** `kicad-cli sch erc` (no unconnected input pins) + design-note audit. **Provenance:** R60.

### ELEC-016 — major
**Statement:** USB D+/D− TVS array at the Type-C receptacle: junction capacitance ≤3 pF per line (≤1 pF preferred), placed ≤5 mm from the connector pins, ground pad stitched with ≥2 vias to the plane, TVS physically between connector and MCU. **Rationale:** keeps the USB90 differential impedance intact while surviving ESD; placement controls clamp loop inductance. **Validation:** BOM Cj check + layout measure ≤5 mm + via count; `kicad-cli pcb drc` clean. **Provenance:** R61.

### ELEC-017 — blocker
**Statement:** USB-C CC1/CC2 each terminated with 5.1 kΩ ±10% to GND (UFP, no PD); SBU1/SBU2 unconnected (DNI); VCONN not sourced. **Rationale:** wrong CC termination = no enumeration or false 3 A advertisement into a 500 mA path — a single-resistor brick. **Validation:** netlist scan — CC1/CC2 nets each have one 4.59–5.61 kΩ resistor to GND. **Provenance:** R61.

### ELEC-018 — minor
**Statement:** Test points on: every power rail (VBUS, 3V3, VSENSOR, VDDH), SWDIO/SWDCLK/nRESET, one full SPI bus per sensor (SCLK/MOSI/MISO/NCS), TX coil tap through a 1 kΩ series resistor, and (ball) VBAT plus charger status. **Rationale:** bring-up of a dual-sensor + wireless-power + RF board without observability is a debug blocker; the 1 kΩ coil tap allows safe autoresonant-frequency verification. **Validation:** script over `.kicad_pcb` — footprint `TestPoint*` present on each required net. **Provenance:** R62.

### ELEC-019 — minor
**Statement:** Every net is assigned to an explicit netclass (no high-speed net left in Default except allowlisted passives); net naming matches netclass intent (`SPI_*`, `USB_*`, `COIL_*`, `TOUCH_*`); a dedicated SPI netclass exists. **Rationale:** mis-netted nets silently escape the netclass-pair clearance rules — discipline is what makes them fire. **Validation:** Python scan of `.kicad_pcb`: all nets have non-Default netclass or are on the allowlist. **Provenance:** R63.

### ELEC-020 — minor
**Statement:** `kicad-cli sch erc` reports zero errors as a gate; every unused CMOS input is terminated (pull-up/down or driven output); unused nRF GPIOs are firmware-configured input-with-pull with a schematic note; NC pins are explicitly marked NC. Unused pins are never hard-tied directly to GND. **Rationale:** ERC pin-type conflicts are real contention faults; hard-tied pins become shorts if firmware reconfigures them as outputs. **Validation:** `kicad-cli sch erc --output erc.json` — zero errors; symbol pin audit. **Provenance:** R64.

### ELEC-021 — major — PROVISIONAL
**Statement:** Base nRF52840 nRESET is driven by a reset supervisor (threshold ≥2.7 V PROVISIONAL, reset pulse ≥140 ms), or the internal BOR is enabled at its highest threshold with a bulk-capacitance sizing calculation in the schematic note. Bench: ramp supply 0→3.6 V, record release threshold, pass ≥2.7 V. **Rationale:** 5 W autoresonant TX load-steps droop the shared rail; the default BOR threshold may sit below sensor dropout, causing partial-reset lockups. **Validation:** netlist scan for supervisor on nRESET or BOR-enable documentation + bench ramp test. **Provenance:** R65.

### ELEC-022 — major — PROVISIONAL
**Statement:** 32 MHz and 32.768 kHz crystals use C0G load capacitors with value = 2×(CL − Cstray), CL from the crystal datasheet, Cstray = 2–5 pF (PROVISIONAL), calculation recorded in a schematic note; caps ≤5 mm (PROVISIONAL) from the XI pins. **Rationale:** wrong CL = ppm offset = BLE link failures misdiagnosed as firmware bugs. **Validation:** BOM cross-check script (cap value vs crystal CL) + layout measure. **Provenance:** R66.

### ELEC-023 — blocker
**Statement:** Ball VBAT ADC sense divider totals ≥1 MΩ, or is FET-switched (enabled only during sampling); leakage budget calculation in the schematic note (4.2 V / 1 MΩ = 4.2 µA against the 120 mAh budget). **Rationale:** a 100 kΩ divider burns 42 µA continuously ≈ 120 days of standby alone — a silent quarter of the battery budget gone to a resistor. **Validation:** BOM resistor-value sum on the VBAT divider nets ≥1 MΩ, or FET gate-drive net present. **Provenance:** R67.

### ELEC-024 — major
**Statement:** Charger PROG (charge-current program) resistor is 1% tolerance or better. **Rationale:** charge-current error into a 120 mAh LiPo pouch is safety-adjacent; the check is exact and free. **Validation:** BOM tolerance field on the PROG resistor = 1% or 0.5%. **Provenance:** R67.

### ELEC-025 — major
**Statement:** Status/orientation LED drive: series resistor sized for ≤5 mA; LED current return star-connected at the MCU GND pad (no shared return with touch electrodes or SPI); no LED drive copper under the ball touch ring. Bench: capacitive touch delta with LED PWM on vs off, pass = change <1× noise floor. **Rationale:** ELEC-008 covers optical keep-out and PWM frequency; this covers conducted switching noise into the capacitive front-end — a different coupling path. **Validation:** layout review of LED return routing + BOM current calc + bench touch-delta test. **Provenance:** R68.

### ELEC-026 — major — PROVISIONAL
**Statement:** nRF52840 DCDC inductor is 10 µH ±20% or better (Nordic specification; a 2.2 µH "because the switcher runs at 8 MHz" is explicitly non-compliant — loop compensation assumes 10 µH), Isat ≥2× peak DCDC current (PROVISIONAL margin); DCDC input capacitor ≤3 mm (PROVISIONAL) from VDDH. If DCDC is unused, DEC4/DCC pins follow the Nordic configuration note. **Rationale:** wrong L breaks regulator stability and increases ripple into the radio supply. **Validation:** BOM (10 µH, tolerance, Isat) + layout measure. **Provenance:** R68.

### ELEC-027 — major — PROVISIONAL
**Statement:** COIL_TX copper to any other net ≥0.8 mm clearance (PROVISIONAL, pending measured tank ring voltage; IPC-2221B extrapolation for ≈50 V peak). **Rationale:** autoresonant TX tank nodes ring to tens of volts; creepage is a safety and carbon-tracking rule, not just DRC tidiness. **Validation:** custom .dru pair rule + `kicad-cli pcb drc`; de-provisionalize after scoping tank nodes at full load. **Provenance:** R69.

### ELEC-028 — major — PROVISIONAL (stackup freeze; first-article antenna measurements)

**Statement:** The ANT feed is 50 Ω controlled impedance (track width set per the stackup calculation, ANT netclass), total length ≤20 mm (PROVISIONAL — freeze at the stackup review), with no stubs or test points on the feed; use ground-stitched coplanar waveguide if microstrip impedance is unachievable. On the ball flex the feed is further constrained: length ≤15 mm [est.] from the nRF to the matching network, no vias in the feed, and the feed is kept off the flex bend radius (former RF-023, R84).

**Rationale:** A 2.4 GHz feed that is not 50 Ω (or that carries stubs/vias) reflects power and detunes the ball antenna — the failure is silent on the schematic and fatal to BLE range. The ball's curved-flex routing gets the stricter length/via rules because the feed cannot be re-tuned after the flex is folded (see RF-008 for the matching network, which stays separate).

**Validation:** Stackup impedance calc + antenna feed coupon VNA (S11 at the matching-network input); KICAD-027 (ANT netclass width) and the custom `.kicad_dru` complement; RF-020 conducted-power bench closes the loop.

**Provenance:** R69 + R84; merged per R222 (DEDUPE.md).

### ELEC-029 — major — PROVISIONAL
**Statement:** SPI netclass to COIL_TX clearance ≥5 mm (PROVISIONAL, pending near-field probe measurement); intra-bus spacing ≥3W (W = SPI track width); SPI routed on a layer with solid GND reference, never over the TX coil keepout. **Rationale:** inductive crosstalk from 50–250 kHz fundamental plus harmonics into the sensor bus — distinct physics from ELEC-027's voltage creepage. **Validation:** custom .dru pair rule + `kicad-cli pcb drc`. **Provenance:** R70.

### ELEC-030 — major
**Statement:** SCLK and USB D+/D− have unbroken GND reference on the adjacent layer for their full routed length: no plane crossings, no routing over splits or keepouts. **Rationale:** a return-path discontinuity is an impedance step and an EMI slot at exactly the nets that must be clean. **Validation:** layout-review procedure — layer-stack checklist per high-speed net + native keepout zones; `kicad-cli pcb drc` clean. **Provenance:** R70.

### ELEC-031 — major
**Statement:** Ball LDO input bulk ≥10 µF; nRF52810-class BOR enabled at highest threshold. Bench: step charger 0→programmed max current, record VDD dip, pass = no reset and dip ≤10%. **Rationale:** charger load-steps on the ball are a different brownout mechanism on a different board than ELEC-021's base supervisor. **Validation:** BOM bulk value + bench load-step capture. **Provenance:** R71.

### ELEC-032 — major — PROVISIONAL
**Statement:** TVS ground pad → GND plane with ≥2 vias within 3 mm (PROVISIONAL) of the pad; minimal ground loop area; USB-C shield fingers to CHASSIS at ≥2 points; TVS placed between connector and protected IC. **Rationale:** ELEC-005 states the outcome (Level 4, criterion B); this is the layout construction that achieves it. **Validation:** layout review (via count, distance measure, loop-area check) + ESD bench per ELEC-005. **Provenance:** R72.

### ELEC-033 — major
**Statement:** VBUS gets a unidirectional TVS (VRWM 5 V, standoff >5.25 V) placed ≤5 mm from the receptacle VBUS pins; VBUS bulk capacitance rated ≥10 V. **Rationale:** the mouse must survive EFT/surge from the host side (hubs, chargers) — host protection does not cover the device. **Validation:** BOM (VRWM, direction, direction, voltage rating) + layout measure. **Provenance:** R73.

### ELEC-034 — minor
**Statement:** SWDIO/SWDCLK have 1 kΩ series resistors (ESD isolation) and SWDIO has a 10–100 kΩ pull-up; debug access is via pogo/tag-connect footprint — no loose header on production boards. **Rationale:** unprotected SWD is an ESD entry point and a bricked-bring-up risk; the footprint is an electrical interface. **Validation:** netlist/schematic check of series R + pull-up + footprint. **Provenance:** R73.

### ELEC-035 — minor

**Statement:** Programming/test pogo pads: SMD annular pads ≥1.6 mm [est.] diameter (the stricter of the old ELEC-037 and former MFG-010 requirements — ≥1.6 mm satisfies both), ≥2 tooling/alignment holes [est.], 3 mm [est.] keepout from tall components [est.], ENIG finish (hard gold acceptable) called out on the fab drawing. SWD pogo pads on both PCBs (FW-010) use the same construction. Probe-cycle life qualified once per fab: 200 cycles [est.] with contact resistance <100 mΩ [est.] (former MFG-010, R191).

**Rationale:** The pogo interface is the factory's only electrical access to the boards; undersized pads or soft finish cause contact failures that are misdiagnosed as firmware bugs. One geometry/finish/life spec, owned by the test-interface construction.

**Validation:** Footprint spec review + KICAD-029 annular checks; incoming measurement at COC (MFG-004); per-fab probe-life qualification.

**Provenance:** R74 + R191; merged per R224 (DEDUPE.md).

### ELEC-036 — minor

**Statement:** Ball flex-to-rigid connection: positive-lock ZIF (or equivalent locking, Hirose FH-class) rated ≥50 mating cycles [est.], gold-plated contacts [est.], strain relief at the connector [est.], retention ≥5 N [est.], ≥3 mm [est.] service loop at each connection [est.] (merged from former MECH-042, R47).

**Rationale:** An intermittent flex contact produces touch dropouts and sensor tears that are misdiagnosed as firmware — the contact spec is electrical reliability, not mechanical convenience. Retention + service loop keep the latch from walking under drop shock.

**Validation:** BOM/flex-cycle bench (≥50 cycles, contact resistance logged); 50× 1 m ball drops with continuity logged: zero disconnects [est.].

**Provenance:** R74 + R47; merged per R226 (DEDUPE.md).

### ELEC-037 — major
**Statement:** Base 5 V TX rail has a PTC/polyfuse (or equivalent current-limited source) between the USB input and the LTC4125; a shorted coil or harness must not dump the full USB rail current. **Rationale:** the LTC4125's programmable current limit protects the IC, not the harness — defense in depth. **Validation:** schematic check for PTC/fuse on the TX 5 V rail with hold current ≥ max TX input current. **Provenance:** R75.

### ELEC-038 — major
**Statement:** USB-C shield → CHASSIS through 1 MΩ in parallel with 4.7 nF, not a hard short. **Rationale:** hard short couples chassis ESD strikes into signal ground and creates a DC ground loop with the host; the RC bleeds ESD while blocking loop current — standard USB-IF practice. **Validation:** netlist scan — shield net to CHASSIS through 0.8–1.2 MΩ ∥ 1–4.7 nF, no direct copper short. **Provenance:** R75.

## RF / radio (23)

### RF-001 — blocker
**Statement:** Ball 2.4 GHz antenna: no copper (electrodes, traces, pours)
within 8 mm [est.]; antenna in the upper hemisphere opposite the charging
pole, OFF the ring plane (the 8 mm keep-out does not fit between adjacent
ring electrodes at ~5.2 mm pitch — place at polar ~60°, ≈10 mm from the
nearest electrode); chip antenna oriented with its null toward the
electrode ring where possible.
**Rationale:** The electrode ring capacitively loads and detunes the
antenna (range collapse) and couples RF noise into cap-sense channels
(worker-B F6).
**Validation:** RSSI vs distance, electrodes populated vs removed: PASS
<3 dB [est.] penalty at 3 m through the shell; streaming noise-floor test
(ELEC-002 criteria) passes with radio at max TX duty.
**Provenance:** Worker-B F6; refined by the Blender keep-out check, which
proved the equatorial placement incompatible with the 8 mm keep-out.

### RF-002 — major
**Statement:** Base: use a pre-certified nRF52840 module; follow its
antenna keep-out exactly (no copper/components/metal in the keep-out).
Antenna ≥15 mm [est.] from the USB-C shell metal, ≥20 mm [est.] from the
TX coil outer edge; antenna at the rear PCB edge, USB-C at the front.
**Rationale:** USB-C shell is a large ground-adjacent mass; the TX coil is
a big driven metal loop; both detune. Module grant is void if the
antenna area is modified (R30).
**Validation:** `trackball.kicad_dru` rules `rf_base_ant_to_tx_coil`
(20 mm) and `rf_base_ant_to_usb_shell` (15 mm) + assembled PER/RSSI test
(RF-003 validation covers the link).
**Provenance:** R30, worker-D §8.

### RF-003 — major
**Statement:** ESB: factory-unique 5-byte address derived from FICR
DEVICEID; 30 s [est.] learn-mode pairing; every packet carries magic +
version + monotonic sequence/nonce, AES-128-CCM with the paired key; base
ignores all packets failing any check. Fixed channel documented (e.g.
2480 MHz [est.]); 3-channel hop list if Wi-Fi coexistence tests fail.
**Rationale:** Two default units on one bench will otherwise cross-talk —
ball A's touch stream driving base B (R25).
**Validation:** Two paired units side by side streaming: zero accepted
foreign packets (rejections logged); 20/20 pair cycles; unpaired ball
never accepted; PER <1% [est.] at operating distance + 1 m [est.] with
hand on ball; RSSI ≥ −70 dBm [est.] at 30 cm.
**Provenance:** R25.

### RF-004 — minor
**Statement:** Regulatory: keep the module grant intact (certified antenna
unmodified, keep-outs per grant conditions); the finished product gets a
Supplier's Declaration of Conformity for unintentional radiation; the
LTC4125 TX subsystem gets a radiated-emissions lab scan with the charger
active, early (Part 15 Subpart C / Part 18 determination by the lab).
**Rationale:** The module grant covers the radio only — not MCU clocks,
USB 12 MHz, or the wireless-power TX, which is itself an intentional
radiator (R30).
**Validation:** Lab scan report; "do not modify antenna area" as a layout
review checklist item.
**Provenance:** R30.

---

### RF-005 — blocker — PROVISIONAL (first-article antenna measurements)
**Statement:** The ESB link budget shall close at 3 m [est.] with ≥15 dB
[est.] fade margin under worst-case assumptions: ball TX 0 dBm [est.],
ball antenna −3 dBi [est.] loaded (hand + shell), base module antenna
+2 dBi [est.], FSPL 50 dB [est.] @ 3 m / 30 dB [est.] @ 30 cm @ 2480 MHz,
polarization/orientation loss 6 dB [est.], implementation loss 3 dB
[est.], RX sensitivity −93 dBm [est.] @ 2 Mbps. Budget spreadsheet checked
into the design record; re-close with measured antenna gains before ball
PCB fab.
**Rationale:** Every downstream RF rule (orientation, hand, coexistence)
spends from this margin; an unbudgeted link collapses silently at range.
**Validation:** Link-budget worksheet (FSPL + gains + losses +
sensitivity) reviewed per PCB rev; RSSI-vs-distance PER test (RF-003
validation) must show ≥15 dB [est.] margin above the PER knee at 3 m;
re-run with first-article measured gains.
**Provenance:** R81. Unverified values provisional.

### RF-006 — blocker — PROVISIONAL (hand phantom / first-article ball)
**Statement:** With a saline hand phantom gripping the ball in the defined
worst-case grip, the ball antenna shall show |S11| ≤ −6 dB [est.] over
2440–2520 MHz [est.] and resonant-frequency shift <40 MHz [est.] vs free
space.
**Rationale:** Hand tissue at 1.2 mm detunes and absorbs; an antenna tuned
only in free space can be 10+ dB down in the hand — the dominant
link-budget uncertainty.
**Validation:** VNA on first-article ball antenna: free-space vs phantom-grip S11;
PASS criteria as stated. Gates ball antenna design sign-off.
**Provenance:** R82. Unverified values provisional.

### RF-007 — major — PROVISIONAL (shell material)
**Statement:** The ball antenna matching shall be tuned for the *loaded*
case (inside the 1.2 mm production shell): in-shell |S11| ≤ −10 dB [est.]
at 2480 MHz, f_res shift vs bare <40 MHz [est.]. The shell's RF effect
(dielectric loading; loss-tangent proxy folded into the measured delta)
is characterized once per resin via VNA in-shell vs bare on the first-article custom
ball; re-characterize if the resin changes.
**Rationale:** The shell is a dielectric radome; tuning for bare air and
hoping is the classic chip-antenna failure.
**Validation:** VNA S11 bare vs in-shell on the first-article custom ball; PASS = in-shell
return loss ≤ −10 dB at 2480 MHz.
**Provenance:** R83. Unverified values provisional.

### RF-008 — major
**Statement:** Ball antenna matching: π-network, 1% NP0/C0G parts, values
from the VNA-tuned prototype (E24); tolerance-stack analysis (Monte Carlo
[est.] over part tolerance + −20…+60 °C [est.]) shall keep |S11| ≤ −10 dB
[est.] at 2480 MHz across corners.
**Rationale:** 5% parts + tempco can walk a narrow chip-antenna match off
frequency in production.
**Validation:** Tolerance simulation in the design record + first-article
VNA on 3 units: |S11| ≤ −10 dB at 2480 MHz on all three.
**Provenance:** R84.

### RF-009 — major — PROVISIONAL (antenna datasheet)
**Statement:** The ball PCB shall provide a contiguous ground counterpoise
≥20×12 mm [est.] (per the chip-antenna datasheet minimum) under/behind
the antenna; no slots, cutouts, or flex-connector keep-outs fragmenting
the counterpoise; counterpoise tied to radio ground with ≥3 vias [est.].
**Rationale:** The PCB pour is the antenna's counterpoise; a slotted pour
shrinks it exactly like a too-small ground plane — efficiency collapse
with no DRC violation.
**Validation:** Layout-review checklist item (pour continuity under
antenna) + VNA efficiency comparison coupon (slotted vs solid
counterpoise).
**Provenance:** R85. Unverified values provisional.
**KiCad built-in?** No — pour continuity isn't expressible; checklist.

### RF-010 — major
**Statement:** The ESB link shall hold PER <1% [est.] at 1 m [est.] in ≥8
ball orientations (45° steps on a turntable) plus continuous hand-rotation
while streaming; no orientation with PER >5% [est.].
**Rationale:** The ball spins freely; a pattern null sweeping across the
base is a guaranteed field event. This is the test that catches RF-001
placement errors.
**Validation:** PER matrix on turntable + rotating-ball streaming test;
PASS criteria as stated.
**Provenance:** R86.

### RF-011 — major
**Statement:** ESB PER degradation during active wireless charging shall be
≤1 pp [est.] vs charger off, at 30 cm and 1 m [est.]; conducted noise at
the ball antenna port (radio off, charger on) ≤ −90 dBm/MHz [est.] in
2400–2500 MHz.
**Rationale:** Bridge switching noise (ns edges, ringing into the hundreds
of MHz) conducted into the ball, near-field magnetic coupling at 5–15 mm,
and rectified ripple on the rail — not the 24,000th harmonic — is the
desense path; the link must carry charge telemetry during charge.
**Validation:** PER matrix charger on/off + spectrum snapshot at the
antenna port; PASS criteria as stated.
**Provenance:** R88. Unverified values provisional.

### RF-012 — major
**Statement:** Coexistence acceptance: Wi-Fi AP on channel 13 (2472 MHz) at
maximum legal EIRP blasting bulk traffic + ≥3 BLE advertisers nearby; ESB
on 2480 MHz shall hold PER <2% [est.]; if not, the documented 3-channel hop
list engages per its documented PER/time trigger and re-passes the same
test. Hop channels and trigger are documented in the design record.
**Rationale:** 2480 MHz sits inside Wi-Fi ch13's skirt; RF-003's "hop if
tests fail" is undefined without the trigger and the test.
**Validation:** Bench coexistence test as stated; hop trigger logged and
verified.
**Provenance:** R89.

### RF-013 — major
**Statement:** Two paired pairs on one bench streaming simultaneously:
zero accepted foreign packets (rejections logged) over 10 min [est.];
under a −20 dBm [est.] CW jammer at 2480 MHz the link degrades to announced
link-loss (per FW-007) but never cross-controls; recovery is re-pair,
documented in the user guide.
**Rationale:** RF-003's crypto prevents acceptance, but the immunity test
and the defined degraded behavior exist nowhere else; silent
cross-control is the catastrophic case.
**Validation:** Two-pair bench test + CW jammer test; PASS criteria as
stated.
**Provenance:** R90. Unverified values provisional.

### RF-014 — minor
**Statement:** Base on a 300 mm [est.] steel plate vs wood/plastic bench:
PER <1% [est.] at 1 m [est.] on both; the rear-edge antenna placement
keeps the desk a second-order effect.
**Rationale:** Module-antenna placement must be validated against the
bracketing desk cases, not assumed.
**Validation:** Two-case PER matrix; PASS criteria as stated.
**Provenance:** R91. Unverified values provisional.

### RF-015 — major — PROVISIONAL (golden unit)
**Statement:** Production RF fixture: golden-unit RSSI at 1 m [est.]
recorded; every unit shall read within ±3 dB [est.] of golden; fail =
antenna/matching rework, not firmware. RSSI logged per unit (feeds the
telemetry low-water field).
**Rationale:** The only production screen for RF regressions (bad
matching-cap reel, shell resin lot change); without it RF dies silently in
manufacturing.
**Validation:** Fixture procedure + golden-unit record in the DHR; 100%
units tested.
**Provenance:** R92. Unverified values provisional.

### RF-016 — major
**Statement:** ESB retransmit policy: ≤3 retransmits [est.] per motion
frame inside a 4 ms [est.] deadline; oldest-frame-drop on deadline expiry;
ball-event → USB HID report latency p99 ≤8 ms [est.].
**Rationale:** Unbounded retransmits trade latency for PER and produce
cursor lag spikes; the policy makes the trade explicit and testable.
**Validation:** USB protocol-analyzer capture during RF-attenuated dropout
injection: p99 latency ≤8 ms [est.], zero stuck frames.
**Provenance:** R93. Unverified values provisional.

### RF-017 — minor
**Statement:** While the ball's BLE advertiser runs (DFU), ESB streaming is
suspended — the single radio is never time-shared between ESB TX bursts
and BLE advertising.
**Rationale:** Self-jamming the DFU path on a sealed ball bricks updates;
FW-010 covers recovery, not this coexistence.
**Validation:** Sniffer capture during DFU entry: zero ESB packets on air
while advertising; DFU completes 3/3.
**Provenance:** R94.

### RF-018 — major
**Statement:** Regulatory change-control: any of the following triggers
re-evaluation before ship — antenna-area copper/component/metal change,
antenna part change, conducted TX power increase above the grant,
enclosure material change near the antenna, TX-coil frequency/drive/
topology change. Trigger list signed off at every PCB revision in the
layout-review checklist.
**Rationale:** The module grant is void on antenna-area modification
(RF-004/R30); without a trigger list the voiding happens silently at some
rev.
**Validation:** Change-control log + signed checklist per PCB rev; "do not
modify antenna area" already on the fab drawing (RF-004).
**Provenance:** R95.

### RF-019 — minor — PROVISIONAL (final TX power)
**Statement:** SAR evaluation exclusion documented: at ≤+4 dBm [est.]
conducted, the ball is below the KDB 447498 1-g SAR exclusion threshold
for the hand-held separation distance; exclusion calculation worksheet
filed in the DHF. If conducted power rises above the exclusion threshold,
a SAR evaluation is triggered (see RF-018).
**Rationale:** Without the worksheet a test house quotes a SAR evaluation
you don't need — or you ship without one you do.
**Validation:** Conducted TX power measurement (RF-020) + signed exclusion
worksheet.
**Provenance:** R95. Unverified values provisional.

### RF-020 — major
**Statement:** Per-unit conducted TX power: 0 dBm ±2 dB [est.] at 25 °C,
within ±3 dB [est.] over 0–40 °C [est.]; 100% units on the production
fixture (conducted tap/pogo at the antenna port).
**Rationale:** Absolute power is the regulatory-traceable number (grant,
SAR exclusion RF-019); RSSI (RF-015) is relative and can't substitute.
**Validation:** Fixture procedure; temp-corner sampling per lot.
**Provenance:** R92. Unverified values provisional.

### RF-021 — minor
**Statement:** Pre-lab gate before booking the radiated lab visit:
first-article conducted spurious/harmonics on both radios (to 12.75 GHz
[est.]) + near-field-probe quick-look of the TX coil; PASS criteria written
before the bench run; the bench report ships with the RF-004 lab request.
**Rationale:** The first paid lab visit must not be the first time the
spectrum is seen.
**Validation:** Bench report attached to the lab booking; no booking
without it.
**Provenance:** R95. Unverified values provisional.

### RF-022 — major
**Statement:** The RF-001 8 mm keep-out is volumetric: no copper
(electrodes, traces, pours, RX coil) inside an 8 mm [est.] sphere around
the chip antenna — the electrode ring wraps the sphere in 3D, so the planar
.dru rule alone is insufficient. Planar complement in the custom .dru:
ANT vs COIL_RX clearance 8 mm [est.] (guards a bad reroute of the feed
near the coil).
**Rationale:** KiCad clearances are 2D per-layer; the ball's antenna sits
in 3D space surrounded by wrap-around electrodes — a planar pass can still
fail in 3D.
**Validation:** `blender/check_antenna_keepout.py` (8 mm sphere vs
electrode/coil geometry) + `trackball.kicad_dru` rule
`rf_ball_ant_to_rx_coil` (8 mm, ANT vs COIL_RX) + VNA.
**Provenance:** R86.
**KiCad built-in?** Partial — built-in clearance suffices for the planar
ANT-vs-COIL_RX complement (add to .dru); the 3D sphere needs the custom
Blender check (built-ins can't do volumes).

### RF-023 — major
**Statement:** ESB airtime budget: ≤32-byte [est.] payloads, 2 Mbps PHY,
250 Hz [est.] motion+touch cadence; total channel airtime ≤20% [est.] per
deadline window, reserving ≥3 retransmit slots inside RF-016's 4 ms
deadline.
**Rationale:** The budget that makes RF-016's retransmit policy physically
possible — policy without airtime headroom is a wish.
**Validation:** nRF Sniffer airtime measurement on first article;
re-verify if payload or cadence changes.
**Provenance:** R93. Unverified values provisional.

---

## Power (15)

### PWR-001 — blocker
**Statement:** USB 5 V budget: enumerate at 500 mA; LTC4125 ITH = 300 mA /
ILIM = 450 mA (RIS = 100 mΩ, RIN = 10 kΩ, RIMON = 267 kΩ); bulk ≥100 µF on
5 V at the TX input; TX driver held OFF (EN) until USB enumeration
completes; MCU ADC asserts TX disable if VBUS < 4.4 V [est.].
**Rationale:** Search pulses across cable resistance dip VBUS; LDO dropout
resets the MCU mid-charge — flaky charging masquerading as firmware (R24).
**Validation:** Worst-case cable (long/thin) + 0→450 mA load steps,
scope VBUS and 3.3 V during search pulses and full charge: PASS VBUS
≥ 4.4 V, 3.3 V within ±3% [est.], zero MCU resets over 24 h charge
cycling.
**Provenance:** R24, worker-C FM-14.

### PWR-002 — major
**Statement:** Sensor 3.3 V rail separate from the TX 5 V feed, with its
own LC/ferrite filter per sensor; <100 mVpp at each sensor's VDD pins in
the 10 kHz–50 MHz band during active charging (PixArt supply-noise spec).
**Rationale:** TX switching harmonics beat with sensor exposure timing →
SQUAL breathing and correlated count noise; charging happens exactly when
the user expects a perfectly still cursor (R24, worker-A mode 9).
**Validation:** Scope VDD at each sensor's pins during charging: PASS
<100 mVpp; functional: SQUAL degradation <10%, zero-motion RMS unchanged
vs TX off.
**Provenance:** R24.

### PWR-003 — minor
**Statement:** nRF52840: 32 MHz HFXO ±40 ppm [est.] with load caps per
C = 2×CL − Cstray (Cstray ≈ 3–5 pF [est.]); 32.768 kHz LF crystal
populated (internal RC ±500 ppm [est.] is marginal for radio slot timing).
USBD runs from HFINT calibrated against USB SOF — no 48 MHz crystal.
**Rationale:** Radio needs the HFXO; USB does not need an external
48 MHz crystal on this part (worker-D §7).
**Validation:** ERC + crystal-frequency check on first article; radio
PER test (RF-003) passes.
**Provenance:** Worker-D §7.

---

### PWR-004 — major
**Statement:** TX EN asserted only after USB enumeration completes
(SET_CONFIGURATION, 500 mA descriptor); plug-in inrush held inside the
100 mA pre-enumeration budget by soft-start/load switch. A non-enumerating
5 V source (dumb charger) shall never enable TX.
**Rationale:** Inrush into ≥100 µF bulk plus the first TX search pulse can
brown out a marginal port before the current budget is granted; TX on a
dumb charger draws 450 mA the source never agreed to (R96).
**Validation:** USB protocol analyzer + current probe, 10 plug cycles on
a hub port and a direct port: PASS = peak pre-enumeration current
≤ 100 mA, EN low until SET_CONFIGURATION, TX never starts on a dumb
charger, zero host-port resets.
**Provenance:** R96.

### PWR-005 — major — PROVISIONAL (cable spec unmeasured)
**Statement:** With the worst-case specified cable (max R loop) and max TX
load (450 mA), VBUS at the TX input shall be ≥ UVLO threshold + 100 mV
margin [est.]. If the arithmetic fails, the shipped cable is specified
shorter/thicker or the UVLO moves per PWR-014 — the conflict is resolved
in the design, not waived.
**Rationale:** A 2 m 28 AWG cable drops ~0.38 V at 450 mA; a 4.75 V host
then delivers 4.37 V — below the 4.4 V UVLO. The design as specified
fails its own threshold with a legal cable (R97).
**Validation:** Four-wire measurement of the longest/thinnest shippable
cable; programmable load stepping 0→450 mA; scope VBUS at the TX input:
PASS = ≥ 4.5 V [est.] sustained, zero UVLO chatter events over 1 h.
**Provenance:** R97.

### PWR-006 — blocker — PROVISIONAL (thresholds unmeasured)
**Statement:** VBUS overvoltage: disconnect the TX stage at 5.75–6.0 V
[est.], survive 6.5 V indefinitely without damage, auto-recover when VBUS
returns to 4.4–5.5 V. No single VBUS fault shall expose the bridge FETs
or bulk caps beyond their ratings.
**Rationale:** A 20 V PD source with a damaged CC line or a miswired dock
hub can put >6 V on VBUS; the TX bridge is the first victim (R98).
**Validation:** Lab supply ramp 5→6.5 V at 100 mV/s and 5 V step to
6.5 V: PASS = disconnect within the 5.75–6.0 V band, zero component
damage at 6.5 V / 1 h, auto-recovery, FET Vds never exceeds 80% of rating
during the event.
**Provenance:** R98.

### PWR-007 — major — PROVISIONAL (limit unmeasured)
**Statement:** Hot-plug inrush into the discharged bulk capacitance shall
peak ≤ 1 A [est.] and deliver within USB 2.0 inrush discipline; the host
port shall not reset or drop enumeration across 10 insertion cycles on a
hub port.
**Rationale:** Discharged ≥100 µF bulk rings multi-ampere spikes on stiff
hosts; marginal hosts brown out and the base enumerates as a ghost (R98).
**Validation:** Current probe on VBUS, 10 hot-plugs on a bus-powered hub
port + 10 on a root port: PASS = peak ≤ 1 A every cycle, enumeration
succeeds every cycle, no host-side overcurrent trip.
**Provenance:** R98.

### PWR-008 — minor

**Statement:** No-ball TX search: average TX-side power ≤150 mW [est.] over a rolling 60 s window [est.]. USB-suspend current is owned by HID-010 (this rule's former suspend-current clause was struck as a duplicate — R228, DEDUPE.md); this rule covers only the charger-side TX-search budget.

**Rationale:** A lost-ball search that runs the bridge at full duty would cook the base and waste the USB budget; the search policy needs its own power envelope independent of the USB-suspend contract.

**Validation:** ≤150 mW TX-search average over 60 s rolling windows [est.]; worst-case search cadence × per-burst energy; suspend current validated under HID-010.

**Provenance:** R97; amended per R228 (DEDUPE.md).

### PWR-009 — major
**Statement:** The base shall enter USB suspend on host request, draw
≤ 2.5 mA, assert no remote wakeup from the charger function, and never
prevent the host from sleeping (no periodic traffic, no ping cadence that
re-triggers activity timers).
**Rationale:** A charger that keeps the host awake is a ship-blocker
class bug — the user's laptop never sleeps because the mouse dock is
plugged in (R112).
**Validation:** Host powercfg/pmset sleep test with the base attached,
no ball and ball-charging: PASS = host sleeps on schedule both ways,
base current ≤ 2.5 mA in suspend, resume re-enumerates without replug.
**Provenance:** R112.

### PWR-010 — major
**Statement:** USB-C sink behavior: 5.1 kΩ Rd on both CC pins; full
function in both plug orientations; works with e-marked and legacy
cables, dead-battery providers, and 4.75–5.5 V sources; the base shall
never source VBUS under any CC fault (open/short on either CC).
**Rationale:** "Rd and done" still needs the matrix — a CC misconfig that
backfeeds 5 V into a dead-battery laptop port is a hardware-kill bug;
orientation-dependent charging is a support nightmare (R98, R113).
**Validation:** Cable/orientation matrix (both flips × legacy/e-marked/
thin-long cable × dead-battery provider): PASS = enumerates and charges
in all, VBUS sourcing = 0 mA with either CC open/shorted.
**Provenance:** R98, R113.

### PWR-011 — minor — PROVISIONAL (budget unmeasured)
**Statement:** TX search behavior with no RX present: bounded ping
interval and duty such that the 60 s average TX input power meets
PWR-008; ping burst peak current ≤ ILIM (450 mA); search shall not
masquerade as charging on any indicator (ties CHG-007).
**Rationale:** PWR-008 is the budget; this is the TX behavior that must
fit inside it — unbounded search duty is how "standby" becomes 0.5 W
(R113).
**Validation:** 60 s power integration with no ball, plus single-ping
capture: PASS = average ≤ 150 mW [est.], peak ≤ 450 mA, base LED shows
"searching" (distinct from "charging") per CHG-007.
**Provenance:** R113.

### PWR-012 — major — PROVISIONAL (timings unmeasured)
**Statement:** TX full-bridge: gate-drive loop inductance minimized
(short, wide return), FETs selected so Miller charge cannot defeat the
LTC4125 non-overlap; scope-verified non-overlap ≥ 20 ns [est.] and zero
shoot-through current spike at max VBUS (5.5 V) and full TX load;
bridge FET case ΔT ≤ 25 K [est.] at full load, 25 °C ambient.
**Rationale:** The controller's non-overlap does not survive bad gate
loops — Miller turn-on cross-conducts at 103 kHz despite the silicon's
best efforts, and the failure looks like "the dock runs warm" until a
FET shorts (R99).
**Validation:** Differential probes on both gate drives + Vds, max VBUS,
full load: PASS = ≥ 20 ns non-overlap, no cross-conduction spike,
ringing < 80% of FET Vds rating; thermal cam on FETs at 30 min.
**Provenance:** R99.

### PWR-013 — minor — PROVISIONAL (current unmeasured)
**Statement:** Dock/ball indicator LEDs driven at 2–10 mA [est.], within
the LED absolute-maximum under all firmware states (including PWM
dimming faults at 100% duty); LED current set by hardware (resistor/CC
source), not by firmware alone.
**Rationale:** The entire dock ritual (CHG-007/029) depends on the LED;
a wrong resistor or a PWM-stuck-high bug toasts the one indicator the
user trusts (R112).
**Validation:** Measure LED current in every indicator state including
fault-injected 100% PWM: PASS = within 2–10 mA [est.] and below LED
AbsMax in all states; 168 h continuous-on soak, no degradation.
**Provenance:** R112.

### PWR-014 — major — PROVISIONAL (hysteresis unmeasured)
**Statement:** VBUS UVLO: TX disable asserted below 4.4 V, released at
≥ 4.6 V (200 mV hysteresis [est.]); the comparator/filter shall not
chatter or oscillate with VBUS held anywhere in the 4.3–4.7 V band for
60 s.
**Rationale:** UVLO without hysteresis chatters at the threshold and
power-cycles the MCU mid-charge — PWR-001's exact failure mode, moved
into the supervisor where it belongs (R113).
**Validation:** Lab supply swept/held across 4.3–4.7 V, scope on EN and
the 3.3 V rail: PASS = single clean transitions, zero MCU resets, zero
TX restarts during a 60 s threshold dwell.
**Provenance:** R113.

### PWR-015 — minor — PROVISIONAL (limit unmeasured)
**Statement:** TX load-transient droop at the TX input: < 200 mV [est.]
on ping leading/trailing edges at full TX load (validates PWR-001's
≥100 µF bulk as an observable, not a parts-list entry).
**Rationale:** Bulk capacitance on the schematic is not bulk capacitance
at the load — ESR, ESL, and placement decide; the droop number is what
the MCU actually feels (R115).
**Validation:** Scope VBUS at the TX input pins during search ping edges
and full-charge load steps: PASS = droop < 200 mV [est.], no ringing
above 5.5 V, PWR-002's sensor rail stays in spec simultaneously.
**Provenance:** R115.

## Charging (36)

### CHG-001 — blocker — PROVISIONAL (coil geometry unmeasured)
**Statement:** Annular TX: RX disk shall overlap the winding band (inner
radius ≤7 mm, outer ≥12 mm [est.]); wind TX to 24 µH ±10% (≈103 kHz with
100 nF, inside the 50–250 kHz LTC4125 window); ferrite plate behind TX
with a center cutout for the optical sensors. k_annular ≥70% [est.] of a
24 µH disk reference; TX input ≤0.8 W at full charge current.
**Rationale:** The annulus null at center can park the system in a dead
zone: enough load to avoid FOD fault, not enough to exit charger UVLO —
STAT "delivering" while the battery stays flat (R18).
**Validation:** LCR jig: k from series-aiding/opposing
(k = (L_aid − L_opp)/(4√(Lp·Ls))); TX input power at 60 mA charge
current, annulus vs disk. Bench before freezing mechanics.
**Provenance:** R18.

### CHG-002 — major — PROVISIONAL (gap stack unmeasured)
**Statement:** Charging envelope: ICHG ≥50 mA at coil-to-coil gap ≤5 mm
and lateral offset ≤3 mm; LTC4120 RUN divider set for VIN(enable) ≈6 V
with hysteresis (not the 11.2 V ADI example). Below the envelope the ball
reports not-charging — never a false "charging."
**Rationale:** Worst-case gap + parking error must still charge, or fail
honestly (R21, worker-C FM-2/3).
**Validation:** Gap 2–7 mm × offset 0–5 mm jig sweep logging VIN(RX),
ICHG, CHRG: PASS = ICHG ≥50 mA inside the envelope; monotonic current
vs offset with a defined cutoff; no offset where STAT is low but ICHG=0.
**Provenance:** R21, worker-C FM-2.

### CHG-003 — blocker
**Statement:** Resonant caps 1–2% C0G/film; measure TX frequency across
four states (no ball / charging / DHC detune / fully assembled ball with
electrodes); set FTH ≥ max observed + 5% [est.]; confirm a 25 mm steel
disc [est.] still trips FOD within one search interval.
**Rationale:** DHC detune + LC tolerance + copper loading all raise TX
frequency legitimately; FTH must clear them all and still catch a coin
(R19). ADI's own LTC4125+LTC4120 design used +15.5%.
**Validation:** Frequency counter on the SW node across all states, then
FO trip test: PASS = no FOD trip in any legitimate state; trip on steel
disc within one search interval.
**Provenance:** R19.

### CHG-004 — major
**Statement:** NTC thermistor bonded to the cell pouch (thermally
conductive, electrically insulating adhesive); cell ΔT ≤15 °C [est.],
peak <45 °C during 0→100% charge at 25 °C ambient; independent NTC on the
TX coil into the LTC4125 (41.5 °C surface-limit class per ADI reference);
NTC detach simulated → charge pauses (open = cold fault).
**Rationale:** Resin is an insulator; the NTC must read cell temperature,
not PCB temperature, or the 40 °C cutoff is fiction. Single NTC = single
point of sensing (R20, worker-C FM-6/17).
**Validation:** In-ball thermocouple during full charge; heat-gun pause/
resume at ~40 °C/0 °C; detached-NTC simulation; thermal chamber −5…+45 °C:
current = 0 outside window, FAULT asserted and reported over ESB.
**Provenance:** R20.

### CHG-005 — blocker
**Statement:** Two-level LiPo protection: LTC4120-4.2 (fixed 4.2 V, ±1%)
primary + dedicated protector (BQ29700-class: overcharge 4.25–4.30 V,
overdischarge, overcurrent) with its own FET secondary; ≥10% [est.] free
thickness around the pouch — never potted rigidly (compliant foam/film
retention); UL1642 / IEC 62133-2 certified cell from a traceable vendor;
charge current 0.5 C (60 mA → R_PROG = 20.0 kΩ 1%).
**Rationale:** A pouch in a rigid resin sphere is a pressure vessel;
single-fault overcharge must trip the secondary before the pouch is
stressed. Highest-severity failure in the analysis (R20).
**Validation:** 200+ cycle swell check (pouch thickness, internal
clearance); single-fault injection (charger forced to 4.3 V [est.]):
secondary trips every time; no shell deformation.
**Provenance:** R20.

### CHG-006 — major
**Statement:** "Charge complete" = charger sleep-mode entry, or VBAT
≥4.18 V AND ICHG < C/10 sustained >10 min [est.]. CHRG pin alone is NOT
"done" (top-off continues ~2 h after C/10). FAULT (bad-battery,
precondition timeout) surfaced distinctly (red blink) and logged over ESB
as battery-health telemetry.
**Rationale:** CHG-007's LED logic and the user's "is it full?" question
need a true definition of done (worker-C FM-7).
**Validation:** Full charge logging VBAT/ICHG/CHRG/FAULT/sleep: reported
"complete" aligns with sleep entry ±10 min [est.]; a 2.5 V-preconditioned
cell recovers or cleanly FAULTs.
**Provenance:** Worker-C FM-7.

### CHG-007 — blocker
**Statement:** Ball LED logic from *measured* charge state only: green iff
ICHG > 10 mA [est.] (or VBAT rising >1 mV/min [est.]) sustained; off if
field absent >200 ms [est.]; blink on FAULT. Zero false-green across the
full mis-seat matrix. LED-on ≤2 s [est.] after placement (CTD ≤1 s or
search already running). Base LED (if any) shows "field active/searching"
from STAT, visually distinct from "charging."
**Rationale:** STAT lies in the marginal-coupling dead zone; mis-seated
must read as not-charging, never as charging (R21).
**Validation:** Mis-seat matrix (offsets/gaps per CHG-002): record LED
state vs measured ICHG — zero cases of green with ICHG <10 mA; LED
latency timing.
**Provenance:** R21.

### CHG-008 — major
**Statement:** With the ball static and TX at full power: zero net sensor
counts over 60 s; SQUAL degradation <10% vs TX off; zero-motion RMS
unchanged within measurement noise.
**Rationale:** TX switching noise inside the annulus hole couples into
sensor rails/front-ends; charging happens exactly when the cursor must
be perfectly still (R24, worker-C FM-10).
**Validation:** Static-ball count log, TX on vs EN-disabled; scope per
PWR-002.
**Provenance:** R24.

### CHG-009 — major — PROVISIONAL (coils unmeasured)
**Statement:** |f0_TX − f0_RX| <3% [est.] in the final mechanical assembly;
drift <1% from 0–40 °C [est.]. Select CRX = 1/(4π²·f0²·L_RX,meas) from
*measured* inductances using 1–2% caps (e.g. 2×47 nF trimmed); re-verify
after ferrite and enclosure are fitted (ferrite raises L).
**Rationale:** A mistuned RX tank looks exactly like weak coupling —
silent undercharge (worker-C FM-16).
**Validation:** LCR/network sweep of both tanks in final assembly.
**Provenance:** Worker-C FM-16.

### CHG-010 — minor
**Statement:** Foreign-object matrix: 25 mm steel disc, coin, paperclip,
50 mm Al foil [est.], centered and offset, with and without the ball:
TX enters fault/retry (STAT high-Z), no FO surface exceeds 60 °C [est.];
a paperclip at the coil edge does not break ball charging.
**Rationale:** The analog FOD stack (FTH/PTH/ITH/NTC) is the entire safety
case for a dumb non-Qi desk charger (worker-C FM-9).
**Validation:** Thermal camera, 15 min per FO placement.
**Provenance:** Worker-C FM-9.

---

### CHG-011 — blocker — PROVISIONAL (tank voltage unmeasured)
**Statement:** Resonant capacitors (TX and RX tanks) rated ≥ 2× the
measured tank peak voltage, C0G/film dielectric; the 100 V default floor
[est.] stands until the tank Vpk is measured with a HV differential
probe at full drive; re-measure after any coil, ferrite, or gap-stack
change. BOM check: C0G/NP0 only — X7R/X5R prohibited in the tank (absorbed from former ELEC-028, R69).
**Rationale:** Tank Q multiplies the ~5 V drive onto the caps — a Q≈30
tank parks 150+ Vpk on a 50 V cap → shorted tank → bridge into a short
→ dock fire. The most violent passive failure in the link (R100).
**Validation:** HV differential probe across each tank cap, full TX
drive, ball present and absent: PASS = rating ≥ 2× max observed Vpk;
LCR confirms 1–2% tolerance (ties CHG-009); post-thermal-soak re-check.
**Provenance:** R100 + R69; merged per R223 (DEDUPE.md).

### CHG-012 — major — PROVISIONAL (limit unmeasured)
**Statement:** TX coil self-heating: ΔT ≤ 20 K [est.] at 25 °C ambient
after 30 min at full TX load (max charge current, worst accepted seat
per CHG-015); no surface the user touches exceeds 45 °C.
**Rationale:** I²R plus proximity-effect loss in a compact annular coil
is the dock's dominant heat source; "warm dock" is also the symptom that
masks FET (PWR-012) and FO (CHG-010/014) heating (R101).
**Validation:** Thermal camera, still air, 30 min full-load soak, ball at
worst accepted seat: PASS = coil ΔT ≤ 20 K [est.], touch surfaces
≤ 45 °C, NTC-on-coil (CHG-004) never trips in normal operation.
**Provenance:** R101.

### CHG-013 — major — PROVISIONAL (ferrite unmeasured)
**Statement:** Ferrite margin: Bpk ≤ 70% of Bsat at max TX current,
computed from measured L and Ipk (Bpk = L·Ipk/(N·Ae)) with Bsat derated
to the max operating temperature; re-check if the ferrite grade or the
sensor cutout geometry changes.
**Rationale:** Saturation collapses L, detunes the tank (fights CHG-009),
spikes TX current, and heats the core — all while looking like "weak
coupling." A cheap ungapped ferrite at 45 °C ambient is where it bites
(R101).
**Validation:** Calculation from LCR-measured L, scoped Ipk at full
load, core datasheet Bsat(T): PASS = Bpk ≤ 0.7 × Bsat@Tmax; thermal cam
shows no core-localized hotspot beyond coil ΔT (CHG-012).
**Provenance:** R101.

### CHG-014 — major — PROVISIONAL (thermal gate per CHG-010)
**Statement:** Extended foreign-object set — steel coin, crumpled Al foil
disc, keyring/keys, magnetic watch band — each tested centered, offset,
and at the coil edge, with and without the ball: TX enters fault/retry,
no FO surface exceeds 60 °C [est.], and no placement produces ΔT > 15 K
[est.] *without* tripping FOD (the non-tripping warm state is the fail).
**Rationale:** CHG-010's four items miss the realistic desk set; foil in
the annulus null is the adversarial case — light, mobile, and parked
where coupling is weakest and heating stealthiest (R102).
**Validation:** Thermal camera, 15 min per FO placement per CHG-010
method: PASS = fault/retry asserted, 60 °C gate held, zero non-tripping
warm placements; ball charging unaffected by a paperclip at the coil
edge (CHG-010 compatibility).
**Provenance:** R102.

### CHG-015 — major — PROVISIONAL (efficiency floor unmeasured)
**Statement:** Degraded-seat contract: at the worst accepted seat (dot
±20° per CHG-029, 1 mm lift), either ICHG ≥ 50 mA at end-to-end
efficiency ≥ 25% [est.], or the LED refuses green per CHG-007. No state
in which the dock burns full TX input power for trickle charge current.
**Rationale:** The marginal-coupling dead zone (CHG-001) has a second
face: enough coupling to stay out of FOD fault, too little to charge —
0.8 W in, 10 mA out, forever (R103).
**Validation:** Jig sweep (gap/offset/rotation) logging TX input power
vs ICHG vs LED state: PASS = every accepted seat meets current +
efficiency, every rejected seat shows no-green; no point with TX input
> 0.4 W [est.] and ICHG < 10 mA.
**Provenance:** R103.

### CHG-016 — blocker — PROVISIONAL (system tolerances unmeasured)
**Statement:** System-level termination: Vterm = 4.20 V ± 1% measured at
the cell tabs (not the IC pins), Iterm ≤ C/10 (12 mA), 2 h safety timer
[est.]; under any single fault (ties CHG-026) the tabs shall never exceed
4.25 V.
**Rationale:** The datasheet ±1% is at the IC pins; cell IR, tab/contact
drop, and NTC-window compromises move the system number — overcharge is
the highest-severity cell failure (R104, CHG-005).
**Validation:** Full charge logged on a calibrated DMM at the tabs:
PASS = termination within 4.158–4.242 V, Iterm ≤ 12 mA, timer ends
charge ≤ 2 h past C/10 [est.]; fault-injection (charger forced high)
trips the secondary before 4.25 V at the tabs, every time.
**Provenance:** R104.

### CHG-017 — major — PROVISIONAL (thresholds unmeasured)
**Statement:** Precondition: Vbat < 2.9 V [est.] → charge at ≤ C/10
(12 mA) until 2.9 V; 30-min precondition timeout [est.] → FAULT with red
blink and ESB log (per CHG-006); LED shows "recovering," never
"charging" (per CHG-007).
**Rationale:** A deeply discharged cell takes hours at trickle; without
an observable contract the timeout FAULT ships as a mystery brick, and
without the LED distinction the user "charges" a dead cell all day
(R105).
**Validation:** 2.5 V-preconditioned cell on the dock: PASS = trickle ≤
12 mA, transitions to full current at 2.9 V [est.], timeout FAULT with
correct LED + ESB log on a cell held below 2.9 V by load.
**Provenance:** R105.

### CHG-018 — minor — PROVISIONAL (cell unmeasured)
**Statement:** Cycle life: ≥ 300 cycles to ≥ 80% of initial capacity at
0.5 C charge / 0.5 C discharge, 25 °C, on the actual selected cell, 3
samples; capacity measured at C/5 reference cycles every 50 cycles.
**Rationale:** The vendor's cycle claim is for the vendor's fixture; the
rule forces it onto the actual cell, the actual 0.5 C rate (CHG-005),
and the actual thermal environment (resin sphere, CHG-004) (R106).
**Validation:** 3 cells cycled per protocol: PASS = all ≥ 80% at cycle
300; pouch thickness logged (feeds CHG-034); any sample < 80% before
cycle 200 fails the cell selection.
**Provenance:** R106.

### CHG-019 — minor — PROVISIONAL (proxy unvalidated)
**Statement:** Calendar aging: 45 °C / 90 days at 40% SoC (≈ 1 yr @ 25 °C
by Arrhenius ~2×/10 K) → retained capacity ≥ 85% [est.] and ΔIR ≤ 50%
[est.], 3 samples; storage SoC per CHG-020.
**Rationale:** The ball sits on desks for years; cycle life without
calendar life is half the aging story. The accelerated proxy is
falsifiable where a 1-year test is not shippable (R106).
**Validation:** 3 cells stored per protocol, reference C/5 capacity
before/after: PASS = ≥ 85% retained [est.] all samples; if the proxy is
disputed, the rule requires the vendor's calendar data instead of a
waiver.
**Provenance:** R106.

### CHG-020 — major
**Statement:** Shipping/storage SoC: 30–50% at pack-out, verified by OCV
3.75–3.85 V on a 10-unit sample per lot; units stored > 6 months get an
SoC re-check before sale.
**Rationale:** Full cells in transport are the regulatory and safety
worst case; empty cells die in the warehouse and become CHG-021 cases.
30–50% is the industry compromise (R107).
**Validation:** Pack-out sampling with calibrated DMM: PASS = 10/10
units within OCV band; 6-month storage audit on retained samples.
**Provenance:** R107.

### CHG-021 — blocker
**Statement:** Deep-discharge recovery: a cell found < 2.0 V (or 0 V) is
quarantined — never trickle-charged on the dock, never shipped;
2.0–2.9 V gets precondition only per CHG-017. The dock shall refuse
charge (FAULT, red blink) on a cell below 2.0 V.
**Rationale:** Below ~2 V copper dissolves into the electrolyte; the
"recovered" cell grows dendrites and fails *later* — in the user's hand.
The protector blocks; this rule governs what people do (R107).
**Validation:** Procedure + injected-cell test: 0 V and 1.5 V cells on
the dock → PASS = zero charge current, FAULT asserted ≤ 10 s [est.],
quarantine tag in the factory flow; 2.5 V cell → precondition per
CHG-017.
**Provenance:** R107.

### CHG-022 — blocker — PROVISIONAL (timing unmeasured)
**Statement:** NTC open (including detach — the CHG-004 case): charge
inhibited ≤ 10 s [est.], FAULT asserted and reported over ESB; charging
shall not resume until the NTC reads back inside the valid window.
**Rationale:** Open reads as extreme cold → a naive JEITA table *permits*
charge; without the inhibit, a detached NTC is a license to cook the
cell blind (R108).
**Validation:** Disconnect the cell NTC mid-charge and pre-charge: PASS
= ICHG = 0 within 10 s [est.] both cases, FAULT + ESB report, no
auto-resume until reconnected and in-window.
**Provenance:** R108.

### CHG-023 — blocker — PROVISIONAL (timing unmeasured)
**Statement:** NTC short: charge inhibited ≤ 10 s [est.], FAULT asserted
and reported over ESB; a shorted NTC shall never be interpreted as
"cell is hot, keep charging at reduced current" — short = no valid
temperature = no charge.
**Rationale:** Short reads as extreme hot; some charger logic
"derates" instead of stopping — derating against a lying sensor is still
blind charging (R108).
**Validation:** Short the cell NTC mid-charge and pre-charge: PASS =
ICHG = 0 within 10 s [est.], FAULT + ESB report; firmware review shows
no derate-instead-of-stop path for the short signature.
**Provenance:** R108.

### CHG-024 — major — PROVISIONAL (tolerances unmeasured)
**Statement:** NTC drift: with worst-case component tolerance (±5% R
[est.]) plus ADC error stacked against the design, the effective charge
window shall remain within 0–45 °C actual cell temperature; the window
edges are validated by precision-resistor substitution, not by trusting
the thermistor.
**Rationale:** Open/short are caught; drift is not — a ±5% NTC silently
shifts the window and permits charging a genuinely hot cell while the
firmware believes 38 °C (R108).
**Validation:** Substitute precision resistors for the NTC at the
computed window edges under worst-case tolerance stack: PASS = charge
permitted only when actual (resistor-equivalent) temperature is within
0–45 °C; guardband documented in the schematic notes.
**Provenance:** R108.

### CHG-025 — blocker — PROVISIONAL (limit unmeasured)
**Statement:** Secondary protector single-fault: with one BQ29700-class
FET shorted on a sacrificial board and the charger forced toward
overcharge, the protector shall still interrupt (remaining FET), cell ΔT
≤ 5 K [est.], no vent, no pouch deformation.
**Rationale:** CHG-005 installs the second level; this rule *tests* it.
A protector whose FETs fail short together is one level wearing a
costume (R109).
**Validation:** Injected FET short + charger forced to 4.35 V [est.]:
PASS = interruption every one of 5 trials, cell ΔT ≤ 5 K [est.],
post-test pouch thickness unchanged (ties CHG-034).
**Provenance:** R109.

### CHG-026 — blocker
**Statement:** Single-fault cascade FMEA: ≥ 15 single faults enumerated
(NTC open/short/drift, protector FET short, charger stuck-high, coil
open/short, tank cap short, TX bridge FET short, FW watchdog loss, ESB
link loss, cell tab short, …), each mapped to a safe state (no charge /
no heat / FAULT indicated); 5 faults injected on the bench, all reach
their mapped safe state; the table is a living document, updated per
design change.
**Rationale:** Component rules verify components; only a fault tree
verifies the *system* — cascades (NTC drifts AND charger runs hot) are
where real products fail (R109).
**Validation:** FMEA table review + 5 injected faults: PASS = every
injected fault reaches its documented safe state ≤ 10 s [est.] with no
unmapped behavior; any design change re-opens the affected rows.
**Provenance:** R109.

### CHG-027 — blocker — PROVISIONAL (no abuse data yet)
**Statement:** Thermal-runaway containment: nail-penetration at 100% SoC
on a sacrificial sphere → no sustained flame > 5 s [est.], sphere
exterior < 120 °C at 10 s [est.], vent path (CHG-028) functions; the
sphere shall not rupture or eject fragments.
**Rationale:** A pouch in a rigid resin sphere is a pressure vessel; the
safety case is containment + venting, and analysis alone is not a safety
case for the highest-severity event (R110).
**Validation:** 3 abuse tests with thermocouples + video: PASS = all
within flame/temperature/fragment limits; test repeated after any
resin, wall-thickness, or cell change.
**Provenance:** R110.

### CHG-028 — blocker — PROVISIONAL (area unmeasured)
**Statement:** Vent path: the sphere assembly shall have ≥ 8 mm² [est.]
effective vent area (not sealable by normal handling — pocket lint,
palm grease), verified geometrically and by pressure-decay test of the
empty assembly; the vent shall not compromise the dock ritual alignment
(CHG-029) or admit water in normal use beyond the product's rating.
**Rationale:** CHG-027's containment assumes pressure can leave; a
sealed sphere turns a 0.44 Wh vent into a rupture. Venting is the other
half of the pressure-vessel answer (R110).
**Validation:** Blender geometric check of vent channels + pressure
decay (pressurize empty sphere to 10 kPa [est.], measure leak-down):
PASS = effective area ≥ 8 mm² [est.] and decay within the vented
reference band — not the sealed band.
**Provenance:** R110.

### CHG-029 — major — PROVISIONAL (angles unmeasured)
**Statement:** Dock ritual tolerance: with the orientation dot parked
±20° [est.] off the charging pole, the ball shall couple inside the
CHG-002 envelope (ICHG ≥ 50 mA) and the LED shall read green truthfully
per CHG-007; beyond 30° [est.] the LED shall not read green
(never false-green). The dock geometry (cradle depth, pole mark) is
dimensioned to make ±20° the *nominal* user outcome, not the edge.
**Rationale:** "User rolls ball dot-up" is a wish until it's a
dimensioned tolerance; CHG-007 is the LED's honesty, this is the
mechanics that keep the LED honest (R111).
**Validation:** Rotation-indexed jig logging ICHG + LED vs angle, 5°
steps, 3 balls: PASS = green + ≥ 50 mA throughout ±20° [est.], zero
green beyond 30° [est.], monotonic current falloff with no dead-zone
flicker.
**Provenance:** R111.

### CHG-030 — minor — PROVISIONAL (limit unmeasured)
**Statement:** Acoustic: no tonal peak > 10 dB above the noise floor in
20 Hz–20 kHz at 10 cm from the dock, in search and in full charge;
sweep the ping interval across its tolerance band — the whine often
hides at one interval setting.
**Rationale:** 103 kHz is ultrasonic; the search-ping *envelope* AM is
not — magnetostriction sings at the repetition rate, and a desk charger
that whines gets returned (R114).
**Validation:** Calibrated mic + FFT in a quiet room, search + charge,
ping interval swept: PASS = no tone > 10 dB above floor [est.]; a
failed unit gets ping-spectrum shaping, not a waiver.
**Provenance:** R114.

### CHG-031 — minor — PROVISIONAL (tolerance unmeasured)
**Statement:** Charge-efficiency reporting: the energy the system reports
as delivered shall match VBUS-integrated input energy within ±10%
[est.] over a full 0→100% charge; the number is reported over ESB per
charge session.
**Rationale:** Efficiency is the observable that catches silent
degradation — detuned tanks (CHG-009), weakened coupling, tired cells —
before the user notices "it charges slower now" (R114).
**Validation:** 3 full charges, independent VBUS power integration vs
reported energy: PASS = within ±10% [est.] every session; a unit
drifting beyond gets flagged, not averaged away.
**Provenance:** R114.

### CHG-032 — minor — PROVISIONAL (tolerance unmeasured)
**Statement:** Battery-health telemetry over ESB: the ball reports cycle
count and a full-charge-capacity estimate; after 50 reference cycles the
reported FCC shall be within 10% [est.] of the measured C/5 capacity;
cycle count increments once per completed 0→100% equivalent.
**Rationale:** CHG-006 promises FAULT logging as health telemetry; this
is the rest of the promise — the data the app needs to say "your
battery is at 82%" truthfully (R114).
**Validation:** 50-cycle run with reference capacity checks: PASS = FCC
within 10% [est.] of measured, cycle count exact, telemetry present in
every ESB session log.
**Provenance:** R114.

### CHG-033 — major — PROVISIONAL (limit unmeasured)
**Statement:** RX coil heating in the ball: ball surface over the RX coil
ΔT ≤ 15 K [est.] at 25 °C ambient during full-rate charge; the cell
ΔT ≤ 15 °C per CHG-004 is measured independently — coil heat shall not
be laundered through the cell NTC.
**Rationale:** The ball sits in a hand; a hot spot under the palm is a
comfort failure and a support ticket even when the cell is fine (R115).
**Validation:** Thermal camera on the ball exterior during a full
0→100% charge at max ICHG: PASS = surface ΔT ≤ 15 K [est.] everywhere,
cell NTC track matches CHG-004 independently.
**Provenance:** R115.

### CHG-034 — major — PROVISIONAL (swell unmeasured)
**Statement:** Pouch free thickness: ≥ 10% [est.] free thickness around
the pouch retained at end-of-life swell — verified after the CHG-018
cycle run (measure aged pouch thickness) or against the cell vendor's
swell model, whichever is worse; the retention (foam/film, never rigid
potting per CHG-005) shall not take a compression set that consumes the
margin.
**Rationale:** CHG-005's ≥10% is a day-one number; swell is an EOL
number. A sphere that fits the pouch on day one and crushes it at cycle
300 is a pressure vessel with a timer (R115, ties CHG-027).
**Validation:** Caliper/Blender stackup on post-cycle-test cells:
PASS = ≥ 10% [est.] free thickness remaining at measured EOL swell;
retention foam compression set < 20% [est.] after the cycle run.
**Provenance:** R115.

### CHG-035 — minor — PROVISIONAL (ratio unmeasured)
**Statement:** Ferrite sensor-cutout field uniformity: no local B-field
hotspot > 1.3× [est.] the winding-band average at the cutout edge, at
full TX drive; the cutout the architecture mandates (CHG-001) is also a
flux concentrator and a stealth heater.
**Rationale:** The cutout edge concentrates flux → localized core loss →
a hot spot the coil NTC (CHG-004) may not see, detuning the tank
asymmetrically (R115).
**Validation:** Field probe scan or high-resolution thermal cam of the
ferrite at full drive: PASS = cutout-edge field ≤ 1.3× [est.] average;
if exceeded, chamfer/grade change, not a waiver.
**Provenance:** R115.

### CHG-036 — major
**Statement:** The CHG-002 gap/offset charging-envelope jig test shall be
run on the maximum-runout first article (MECH-004 limit, worst-case
orientation), not only on the nominal ball.
**Rationale:** An out-of-round custom ball rocks in the MECH-015 kinematic
cradle; the coil-to-coil gap varies through the rock. Qualifying charging
on a perfect sphere ships a regression that only appears on real print
variation (R270).
**Validation:** Repeat the CHG-002 jig sweep (gap 2–7 mm × offset 0–5 mm)
with the max-runout article rotated to its worst orientation; PASS =
ICHG ≥50 mA across the full CHG-002 envelope.
**Provenance:** R270.

---

## Firmware (56)

### FW-001 — blocker
**Statement:** Fuse timestamped *velocities* (1 µs hardware timer per SPI
read, v_i = Δcounts/Δt_i) via SQUAL-weighted least squares
ω = (AᵀWA)⁻¹AᵀW·m; weight 0 below SQUAL floor 16, ∝ SQUAL² above [est.];
3σ cross-sensor consistency gate rejects the outlier; on clean
disagreement trust the larger motion vector (sensors miss counts, never
over-count).
**Rationale:** Unweighted fusion corrupts ω whenever the sensors disagree;
this is the load-bearing math of the dual-sensor concept (R4).
**Validation:** Half-masked ball (matte vs glossy tape) at fixed ω: fused
error within ±5% of both-clean baseline; no step discontinuities >2
counts across the weighting threshold.
**Provenance:** R4.

### FW-002 — major
**Statement:** On single-sensor blindness (SQUAL at floor): drop the dead
sensor's rows from A (rank-2 fit + constant-velocity predictor for brief
dropouts); expose per-axis confidence = diagonal of (AᵀWA)⁻¹ to the
HID/3D-driver layer; flag low-confidence within 50 ms. Never zero-fill.
**Rationale:** Silent zero-fill makes a rotation axis vanish with no
indication; announced degradation lets the host freeze the axis (R5).
**Validation:** Opaque tape over one lens, jig rotations about each
principal axis: rotation about the dead sensor's normal tracks within
±5%; rotation about the live sensor's normal is flagged low-confidence
≤50 ms, never silently zeroed.
**Provenance:** R5.

### FW-003 — major
**Statement:** Poll both sensors at ≥1 kHz via motion-burst reads in an
EasyDMA SPI timer/PPI chain; timestamp every read; per-sensor Δt from its
own timestamps; log delta-saturation events; USB IN servicing shall never
jitter the sampling.
**Rationale:** Unsynchronized free-running sensors skew integration
windows up to a poll interval — fused-axis tilt proportional to angular
acceleration, worst in fast flicks (R8).
**Validation:** Motor-driven accelerating profile vs shaft encoder: phase
lag <1 ms at 1 kHz polling; axis-direction error <2° during a 10 rev/s²
ramp [est.].
**Provenance:** R8.

### FW-004 — major
**Statement:** Rest-gate: when both sensors' high-frequency energy exceeds
fused-ω energy by ratio (vibration signature ≠ coherent rotation), hold
the cursor. Click events shall displace the cursor ≤2 counts [est.].
**Rationale:** Click-induced shake is the classic trackball complaint;
with two sensors differential shake is worse (R10).
**Validation:** Ball parked, tap case + click buttons while logging fused
output: zero-motion RMS <1 count at 1 kHz; ≤2 counts per click event.
**Provenance:** R10.

### FW-005 — major
**Statement:** The touch ring is a contact-*state* sensor (touch count +
centroid arc), never a motion sensor. Finger velocity = contact arc
velocity − ball angular velocity (from FW-001). Ring-motion gestures are
relative and gated on the optical measurement. Yaw-spin ambiguity zone
(optical magnitude below threshold while arc-velocity high): inhibit
motion-correlated gestures and report "ambiguous" to the 3D driver —
never guess a direction.
**Rationale:** Ring scans cannot distinguish finger slide from ball
rotation under a stationary finger; yaw-spin about the vertical is
singular for the correlator, and a wrong guess inverts scroll/drag (R11,
R13).
**Validation:** (a) Fixed ball, 90° finger slide vs fixed finger, 90°
ball rotation: ≥95% correct classification over 50 trials each.
(b) Yaw-spin under a stationary top contact: ambiguity flag asserts
≤100 ms after spin onset; zero sign-inverted scroll/drag events.
**Provenance:** R11, R13.

### FW-006 — major
**Statement:** Click-commitment window 30–50 ms [est.] (≈4–7 frames at
135 Hz): on first touch, hold click dispatch until the finger count
settles; fire for the settled count. Latency targets (separated):
detection-to-decision <50 ms; tap click ≤150 ms including
disambiguation; single-finger press-down <50 ms. Adaptive: shorten the
window after the user's first stable single-finger press.
*Replaces the killed blanket "<50 ms touch-to-click" rule (R14).*
**Rationale:** Fire-on-first-contact manufactures phantom left-clicks
before two-finger right-clicks; the blanket target was unsatisfiable.
**Validation:** Solenoid rig, 1/2/3-finger taps at 0–60 ms inter-finger
delays: click-type accuracy ≥99%; USB HID click latency ≤80 ms [est.];
zero cases of a 1-finger tap emitting right/middle click.
**Provenance:** R14.

### FW-007 — major
**Statement:** Sequence-number every touch frame from the ball MCU. After
link re-establishment, require ≥3 consecutive consistent frames [est.]
before accepting contact-state changes; force all buttons released in HID
if no valid frame within 150 ms [est.] of cadence; never dispatch a click
whose press frame predates the dropout; synthesized all-up states never
feed tap eligibility.
**Rationale:** Dropout → resync → reappearing finger reads as a new short
contact = phantom click; dropout mid-drag = stuck drag (R15).
**Validation:** RF-attenuated dropout injection during press/drag/idle,
≥20 trials each: zero phantom clicks, zero stuck buttons, button state
converges to ground truth within 200 ms [est.] of link return.
**Provenance:** R15.

### FW-008 — major
**Statement:** Button debounce: 5 ms stable-time [est.] state machine on
press and release, sampled ≥1 kHz; timestamp the edge at detection and
report on the next 1 ms poll (debounce never delays the HID report);
reject pulses <2 ms [est.] as chatter/ESD.
**Rationale:** Crisp premium click feel with no double-click; coupled
noise must not become clicks (worker-D §5).
**Validation:** 100 k-click solenoid life test [est.]: no double/missed
click in a 1 kHz log; actuation force 0.6–0.9 N [est.].
**Provenance:** Worker-D §5.

### FW-009 — major
**Statement:** Gate all motion reports on ball presence (proximity /
capacitive detect); send zero deltas when the ball is absent.
**Rationale:** Sensors staring at an empty socket report garbage →
cursor drift on the bench (R27).
**Validation:** Remove ball, log 60 s: zero net motion reports.
**Provenance:** R27.

### FW-010 — major
**Statement:** Ball: MCUBoot + SMP-over-BLE; bootloader listens briefly on
every reset (not wake-from-sleep); base sends "enter DFU" over ESB and
may relay images. Base: USB DFU, dual image slots (swap mode), signed
images (ECDSA-P256), hardware force-bootloader (button held at power-on),
never software-entry-only. SWD pogo pads on both PCBs.
**Rationale:** A DFU path whose only entry is a working app bricks on the
first bad flash; V1's screwed shell keeps SWD reachable but the rule must
not depend on opening it (R29).
**Validation:** 3/3 ball DFU on a screwed-shut ball incl. bad-image
rejection (bootloader still advertises); 20-cycle base DFU incl.
power-cut-during-swap: always recovers to a bootable image.
**Provenance:** R29.

### FW-011 — minor
**Statement:** Grab rejection: ≥4 simultaneous contacts or total contact
area above threshold → suppress all gestures (use the controller's palm
rejection).
**Rationale:** 4–5 contacts are otherwise undefined while 3 = middle
click; a full grab must not click (worker-B, prior review m6).
**Validation:** Grab test: zero gesture/click output during ≥4-contact
holds.
**Provenance:** Prior review m6.

### FW-012 — minor
**Statement:** Per-electrode continuity self-test in ball firmware: a
railed-low baseline channel = broken electrode; report channel health
over ESB.
**Rationale:** Flex cracks (MECH-009) present as firmware bugs; the
firmware should name the broken channel instead (worker-B F14).
**Validation:** Bench: disconnect one electrode on a test flex; health
report names the channel within 5 s [est.].
**Provenance:** Worker-B F14.

### FW-013 — minor
**Statement:** Suspend touch acquisition while the charging field is
present; force baseline recalibration on field-loss; baseline recovery
<2 s [est.] after field removal.
**Rationale:** WPT field at ~100–200 kHz overlaps cap-scan frequencies;
a latched post-charge offset is a broken mouse (R16).
**Validation:** Raw-count logs field on/off over a full charge: zero
touch events during charge; baseline recovery <2 s after; ESB PER
degradation <1 pp [est.] during charge (worker-C FM-11).
**Provenance:** R16.

---

### FW-014 — major
**Statement:** All fusion-path math (SQUAL weights, AᵀWA assembly, 3×3 inverse, ω solve) shall be IEEE-754 single-precision; no double-precision operations and no iterative solvers in the 1 kHz fusion task; the 3×3 inverse shall use the closed-form adjugate/determinant.
**Rationale:** Cortex-M4F executes single in hardware; doubles trap to software emulation (~10–20× slower [est.]) and iterative solvers have data-dependent iteration counts — either can push the fusion tick past the 1 kHz deadline, silently and only under load (R116).
**Validation:** Build with -Wdouble-promotion -Werror on the fusion translation unit; binary scan (no `__aeabi_d*` symbols) in the fusion object; cycle-counter measurement of the fusion tick ≤40 µs [est.] on nRF52840 @ 64 MHz; determinant-floor fault injection takes the FW-015 path, never stalls.
**Provenance:** R116.

### FW-015 — major
**Statement:** Firmware shall compute det(AᵀWA) every fusion tick (it falls out of the adjugate); if det < D_floor (calibrated so cond(AᵀWA) ≲ 100 [est.]), drop the lower-weight sensor's rows and take the rank-2 + constant-velocity predictor path (FW-002) instead of inverting; set the conditioning flag in telemetry. Never invert below the floor.
**Rationale:** Near-singular inversion amplifies sensor noise into cursor teleports; the 3σ gate (FW-001) checks inter-sensor agreement, not conditioning (R117).
**Validation:** Bench with synthetic weight profiles sweeping cond 10→10⁴: fused |ω| stays within ±10% of the both-clean reference and no tick emits a >50-count jump; conditioning flag asserts in telemetry.
**Provenance:** R117.

### FW-016 — blocker
**Statement:** Every division in the sensor→fusion→HID path shall be guarded: Δt ≤ 0 → the sample is discarded, never fused; sum-of-weights = 0 → emit zero motion, not NaN; an isfinite() canary on fused ω before HID encode — non-finite ω forces a zero-motion report and increments the error counter (FW-040).
**Rationale:** Duplicate timestamps give Δ/0 = inf; double-floor SQUAL gives 0/0 = NaN — a NaN cursor or a HardFault from one bad tick (R118).
**Validation:** Fault injection at 1 kHz for 60 s: forced duplicate timestamps and forced both-sensors-at-floor; host log asserts every fused ω finite, zero HardFaults; code-review checklist enumerates every division site.
**Provenance:** R118.

### FW-017 — major
**Statement:** SQUAL weight engagement uses hysteresis: weight transitions 0 → ∝SQUAL² at SQUAL ≥ 20 [est.], and back to 0 at SQUAL ≤ 12 [est.] (floor 16 ± 4); per-tick weight changes slew-limited to ≤2× [est.].
**Rationale:** A hard threshold flaps 0 ↔ ∝289 every ms when SQUAL breathes across 16 → cursor stutter at the handoff (R119).
**Validation:** Motor rig with SQUAL ramped 8→24→8 both directions: zero weight toggles while SQUAL is inside (12, 20); fused-velocity step discontinuities <2 counts across crossings.
**Provenance:** R119.

### FW-018 — major
**Statement:** All timestamp deltas shall be computed as unsigned modular differences (Δt = now − last, uint32); Δt sanity-clamped to (0, 2× expected poll]; firmware shall survive the 1 µs timer's ~71.6 min overflow with no Δt anomaly.
**Rationale:** One signed subtraction or 64-bit promotion in the chain breaks at wrap → sign-flipped velocity or a div-guard skipping every sample for a tick — a once-per-hour cursor freeze no short test catches (R120).
**Validation:** Test build preloads the timer near 0xFFFFFFFF and runs 5 min across the wrap: host log asserts no negative/clamped Δt events and velocity continuity; 72 h soak as the production-path check.
**Provenance:** R120.

### FW-019 — major
**Statement:** SPI burst reads: CRC/parity-checked; ≤2 retries inside the poll slot; per-sensor consecutive-failure counter; ≥8 [est.] consecutive failures → full sensor re-init (≤100 ms) with fusion degraded per FW-002; the poll loop and USB reporting never block on SPI; samples are sequence-tagged and stale samples are never re-fused.
**Rationale:** Unbounded retry stalls the 1 kHz loop; silent reuse of the last good sample fuses phantom constant velocity (R121).
**Validation:** Glitch injection on SCK/MISO (100 faults): recovery ≤100 ms every time, poll jitter within the FW-022 budget, zero fused samples carrying stale sequence tags.
**Provenance:** R121.

### FW-020 — major
**Statement:** Sensor init is an ordered, verified sequence: power settle ≥10 ms [est.] → SROM download + checksum verify → product-ID readback → config write + readback-verify → rest SQUAL sanity (>floor on a matte reference); any step failure sets init-failed, increments the counter (FW-040), and announces degraded mode; retries bounded with backoff.
**Rationale:** Init before the oscillator/SROM is ready yields wrong CPI or unloaded SROM — a wrong-speed cursor that passes smoke tests; ignored init failure streams zeros that masquerade as FW-002 blindness without ever flagging (R122).
**Validation:** 100 power-cycle init log, 100% pass; SROM-corruption injection → init-failed asserted, driver never reports "initialized" with zeroed data.
**Provenance:** R122.

### FW-021 — major
**Statement:** Per-axis confidence is reported on vendor page 0xFF00 as three uint8 fields: conf_axis = round(255·clamp(σ_ref²/σ_axis², 0, 1)), where σ_axis² is the axis variance (diagonal of (AᵀWA)⁻¹) and σ_ref² the both-clean reference variance (factory calibration constant); 0 = unobservable, 255 = reference-clean; refreshed ≤50 ms after a change. Semantics fixed in the interface spec.
**Rationale:** FW-002's raw variance diagonal is unbounded and unit-dependent — hosts cannot interpret it and revisions would disagree (R123).
**Validation:** Half-masked ball per FW-002: host parses telemetry against the spec and asserts the dead axis reports 0 within 50 ms and live axes stay >200 [est.].
**Provenance:** R123.

### FW-022 — major
**Statement:** Report pacing is decoupled from sensor polling via a timestamped sample FIFO: the 1 kHz sampler never waits for USB; the reporter emits on a 1 ms SOF-aligned cadence using the newest sample ≤1 poll old, interpolating position between the two bracketing samples; report-interval jitter ≤±100 µs p99 [est.]; sampler jitter ≤±50 µs [est.] during USB IN floods.
**Rationale:** Pace-by-completion couples USB stalls into pointer wobble; pace-by-ISR couples USB into sampling — FW-003's mirror image (R124).
**Validation:** USB protocol analyzer, 60 s: histograms of SOF→report intervals and poll intervals; PASS on both jitter budgets.
**Provenance:** R124.

### FW-023 — major
**Statement:** Under the defined worst-case load (1 kHz fusion + ESB RX storm at max rate + touch processing + 1000 Hz telemetry encode), the base shall emit every 1 ms HID report with zero missed intervals over 60 s; a missed-interval counter is exposed via vendor GET (FW-040).
**Rationale:** No load budget exists; a 500 Hz-effective cadence under load reads as smoothing lag and is invisible in idle testing (R125).
**Validation:** Synthetic load rig + USB capture: 60,000/60,000 reports, missed-interval counter reads 0.
**Provenance:** R125.

### FW-024 — major
**Statement:** On USB suspend: halt sensor polling and touch acquisition (or lowest-power retention), discard the sample FIFO, assert ≤2.5 mA [est.] suspend current; on resume: fast sensor re-init ≤10 ms [est.], discard the first 4 samples [est.], resume full rate; remote wakeup only on button/motion and only if host-enabled.
**Rationale:** Polling through suspend violates USB current limits; a stale FIFO dumped on resume becomes a cursor jump; undefined wakeup is a compliance and UX hole (R126).
**Validation:** Bus suspend + current measurement ≤2.5 mA; USB capture of resume: first valid report ≤10 ms, zero motion burst; wakeup-source matrix tested enabled/disabled.
**Provenance:** R126.

### FW-025 — major
**Statement:** Touch baseline: slow-track ≤1 count/s [est.] only while the channel is untouched; baseline frozen for touched channels; total excursion capped at ±15% [est.] of factory baseline; on release the channel must return within window within 2 s or trigger forced recal (FW-026).
**Rationale:** A leaky baseline tracks into a held finger until the hold "disappears" → dropped drags; uncompensated drift → overnight false touches (R127).
**Validation:** 60 s hold: contact persists the entire hold with no dropout; 24 h idle soak: zero false touches.
**Provenance:** R127.

### FW-026 — major
**Statement:** ATI/baseline recal triggers are enumerated: baseline outside ±X window, channel railed high/low for >64 frames [est.], temperature Δ >5 °C [est.] since last cal; rate-limited to ≤1 recal per 30 s [est.]; always deferred until all-contacts-up; every recal logged (counter + telemetry event, FW-040/HID-017).
**Rationale:** Mid-gesture recal corrupts the gesture; never-recal leaves railed channels stuck (R128).
**Validation:** Temperature chamber ramp + forced channel rail: zero recals during an active gesture; recal fires within 30 s of rail onset at idle; log shows the event.
**Provenance:** R128.

### FW-027 — minor
**Statement:** Per-channel temperature coefficient table in flash (factory 2-point calibration [est.]); baseline compensated continuously between recals (FW-026).
**Rationale:** Discrete recal leaves drift (temperature, humidity) uncompensated between events; continuous compensation narrows the window (R129).
**Validation:** Chamber sweep −10…+50 °C [est.] at idle: raw-count excursion within ±5% [est.] with compensation enabled vs uncompensated baseline run.
**Provenance:** R129.

### FW-028 — major
**Statement:** Contact IDs persist across frames via nearest-centroid matching within a max-jump radius (8 mm [est.] per frame); a new ID is issued only after K=3 [est.] consecutive absent frames; the ID table is included in touch debug telemetry.
**Rationale:** Index-based matching swaps IDs when fingers cross → taps misassigned to the wrong finger → wrong clicks (R130).
**Validation:** Two-finger crossing/swap solenoid rig, 50 trials: ID continuity ≥99%, zero cross-assigned taps.
**Provenance:** R130.

### FW-029 — major
**Statement:** Explicit time thresholds: tap = contact <200 ms [est.]; hold = contact ≥400 ms [est.] without release; 200–400 ms resolves as press (no hold action until 400 ms elapses; release before → tap); long-press actions default OFF except drag (FW-030); thresholds reconfigurable via vendor IF (FW-033).
**Rationale:** Without thresholds a 300 ms contact is ambiguously tap/hold, and long-press-for-right-click collides with hold-to-drag (R131).
**Validation:** Solenoid confusion matrix over 50–800 ms contacts: classification accuracy ≥99%.
**Provenance:** R131.

### FW-030 — major
**Statement:** Drag-lock is an explicit latched mode: entry = double-tap-hold or vendor-configured gesture; contact gaps ≤80 ms [est.] are bridged; exit = single tap, 10 s [est.] idle timeout, link dropout, or ball-absent; exit always emits HID all-up; lock state visible in telemetry.
**Rationale:** A 40 ms micro-lift reads as release → dropped drag; a logic-latched drag with no exit path survives dropouts (FW-007 covers the link, not the latch) → stuck drag (R132).
**Validation:** Scripted micro-lift drags (20–120 ms gaps): ≥95% survive gaps ≤80 ms; every forced exit path emits all-up on USB capture.
**Provenance:** R132.

### FW-031 — major
**Statement:** Default chord map: 1 finger = left, 2 = right, 3 = middle (tap, per FW-029 thresholds); simultaneous multi-finger contacts resolve through the click-commitment window (FW-006); map reconfigurable via vendor IF (FW-033); mixed physical+touch chords arbitrated per FW-048.
**Rationale:** FW-006 settles the finger count but never defines what counts mean; mixed chords are otherwise undefined (R133).
**Validation:** Inter-finger delay sweeps 0–60 ms, 1/2/3 fingers: click-type accuracy ≥99%; zero cases of a 1-finger tap emitting right/middle click.
**Provenance:** R133.

### FW-032 — major
**Statement:** Contacts with major-axis >18 mm [est.] or area >250 mm² [est.] are excluded from finger count and gestures (tracked only for rejection); finger-count transitions during an active gesture require all-contacts-up or a new commitment window — a growing contact mid-drag never morphs a 1→2 finger chord.
**Rationale:** A palm heel at the ring edge reads as one large "finger"; a rolling palm growing mid-drag morphs chords → spurious right-click mid-drag (R134).
**Validation:** Palm sweep/roll fixture, 50 rolls: zero gesture output, zero chord morphs.
**Provenance:** R134.

### FW-033 — major
**Statement:** Gesture map exposed on vendor page 0xFF00: GET/SET with schema version; factory-reset command; invalid SETs NACKed and never partially applied; persisted to flash within the FW-053 wear budget.
**Rationale:** Hardcoded gestures strand left-handed/3D-driver users; an unconstrained config protocol with no reset path bricks UX (R135).
**Validation:** Host script round-trip (set → power cycle → get = set); fuzz 200 invalid SETs: all NACKed, stored map unchanged.
**Provenance:** R135.

### FW-034 — blocker
**Statement:** On any reset, button/switch state initializes to released in both RAM shadow and GPIO latch; the first HID report after boot is all-buttons-up + zero deltas; reset cause is logged to the non-volatile error log (FW-040); boot self-check flags GPIO-read vs shadow mismatch.
**Rationale:** Watchdog firing mid-click → reboot restoring "pressed" = permanently stuck button until power cycle (R136).
**Validation:** Test build with injected infinite loop (forced watchdog) during an active click: USB capture asserts clean boot, zero stuck-button reports, reset cause logged.
**Provenance:** R136.

### FW-035 — blocker
**Statement:** BOD threshold configured (2.7 V [est.]); calibration/config writes are atomic (dual-slot + CRC + sequence counter); on brownout reset: full sensor re-init, touch re-baseline, gesture state discarded; never resume a mid-gesture or mid-click state.
**Rationale:** Slow VBUS droop mid-write tears calibration → corrupt A-matrix → garbage fusion; resuming fiction is worse than resuming clean (R137).
**Validation:** Programmable supply droop 3.3→2.0 V sweeps + torn-write injection: always boots to clean idle; calibration CRC-valid or factory-default-flagged, never half-valid.
**Provenance:** R137.

### FW-036 — major
**Statement:** Bootloader listen window ≤1 s [est.] after reset, then forced application boot; reset-storm guard (≥3 resets within 10 s [est.] → skip listen, boot app immediately); DFU entry only via explicit ESB/USB command or hardware force.
**Rationale:** Unbounded "briefly" (FW-010) = unresponsive ball after every reset; reset spam = denial of input (R138).
**Validation:** Reset→app-report time ≤1.5 s [est.] measured; 10× rapid resets: app boots every time, bootloader never holds the device.
**Provenance:** R138.

### FW-037 — blocker
**Statement:** Ball (MCUBoot) and base both verify ECDSA-P256 signatures against the production key in protected storage (UICR/OTP) before any swap; test keys cannot validate production images; failed verification boots the previous image and increments the DFU-reject counter (FW-040); no unsigned-image override exists in production builds.
**Rationale:** FW-010 mandates "signed images" but never the verification policy or key custody — a shipped test key lets anyone sign malware for every unit (R139).
**Validation:** Test-key-signed image → rejected, app still boots; bit-flipped image → rejected; DFU-reject counter increments; production image signed by production key → accepted.
**Provenance:** R139.

### FW-038 — major
**Statement:** Monotonic anti-rollback version counter in protected flash; bootloader rejects any image with version < counter; downgrade attempts logged (FW-040); factory override requires physical access (SWD/hardware strap), never a software command.
**Rationale:** Signed images without monotonicity let an attacker DFU a known-vulnerable old signed image and exploit it (R140).
**Validation:** Attempt N−1 install → rejected + logged; counter survives power cycle; physical-override path demonstrated on bench.
**Provenance:** R140.

### FW-039 — major
**Statement:** ESB application packets: version byte (major.minor), length, type, 16-bit seq, payload, CRC16; receiver rejects unknown major versions and skips unknown minor fields by length; version mismatch raises a telemetry event (HID-017); ball/base each report their ESB app version in the factory passport (FW-041).
**Rationale:** Skewed ball/base firmware misparses touch frames → phantom clicks; no version negotiation exists today (R141).
**Validation:** Version-skew bench (new ball + old base): mismatch flagged, zero misparsed frames; fuzz unknown major/minor versions → rejected/skipped correctly.
**Provenance:** R141.

### FW-040 — minor
**Statement:** Defined saturating 16-bit error counters: SPI retries, SPI re-inits, ESB drops, ESB CRC fails, SQUAL-floor entries, dropout resyncs, init failures, watchdog resets, brownouts, DFU rejects, recal events, missed HID intervals; persisted across resets; readable via vendor GET; cleared only by explicit vendor SET.
**Rationale:** Field failures are invisible without counters; RAM counters die on reset — exactly when they are needed (R143).
**Validation:** Each fault injected → matching counter increments; power cycle → counters retained; unauthorized clear attempt → rejected.
**Provenance:** R143.

### FW-041 — major
**Statement:** Factory test mode entered only via hardware fixture signal (pogo strap), never by host traffic: runs sensor SQUAL-vs-reference check, per-electrode continuity, button actuation count, ESB PER test; reports per-test pass/fail over vendor IF; writes a unit passport (versions, calibration hash, test results) to flash; exits on reset.
**Rationale:** FW-012's self-test exists but nothing runs it at the factory or records the result — dead electrodes and weak sensors ship (R144).
**Validation:** Fixture on 5 units including one with a disconnected electrode: mode entered, fault named, passport written; host traffic alone never enters the mode.
**Provenance:** R144. KICAD/ELEC handoff: fixture strap pad + test points on both PCBs.

### FW-042 — blocker
**Statement:** Production firmware enables APPROTECT (SWD disabled); SWD pogo pads remain for pre-lockdown factory use; post-lockdown recovery is ERASEALL-only (destroys keys/calibration).
**Rationale:** Open SWD in production = readout of signing keys and calibration; the pads must exist but be inert in the field (R145).
**Validation:** Production image on bench: debug probe attach/readout fails; ERASEALL succeeds (unit returns to blank).
**Provenance:** R145. KICAD/ELEC handoff: SWD pogo pads on both PCBs per FW-010.

### FW-043 — major
**Statement:** Ball sleeps after 5 s [est.] of no motion + no touch: sensors to low-power, touch controller to wake-on-touch, ESB to sniff; wake on motion IRQ or touch with ≤15 ms [est.] wake latency; samples spanning the wake transition are buffered, never fused across the sleep Δt.
**Rationale:** An unslept ball drains between charges; naive wake fuses a huge Δt → cursor jump (R126).
**Validation:** Motion-triggered wake: USB capture shows first motion report ≤15 ms after solenoid tap, zero jump; sleep current measured on the ball supply.
**Provenance:** R126.

### FW-044 — minor
**Statement:** Water-droplet rejection: small (<6 mm [est.]), low-ΔC, stationary contacts appearing without a preceding approach transient are classified as moisture, excluded from finger count, and never start gestures; a droplet + real finger still tracks the finger.
**Rationale:** Condensation/sweat droplets otherwise become phantom "fingers" → phantom taps (R127).
**Validation:** Misting fixture: zero gesture output from droplets alone; droplet + solenoid tap: tap classified ≥95%.
**Provenance:** R127.

### FW-045 — major
**Statement:** End-to-end latency budgets: motion→USB-report <8 ms [est.] p99 (poll 1 ms + fusion ≤1 ms + USB ≤2 ms; host stack excluded), touch→click ≤150 ms per FW-006, touch→photon measured on an LED-synchronized photodiode rig; any stage exceeding budget fails the build's latency gate.
**Rationale:** Per-stage targets without an end-to-end budget let integration eat the margin (R124).
**Validation:** Photodiode rig: p99 touch→photon within budget; USB capture asserts motion→report <8 ms p99 over 60 s.
**Provenance:** R124.

### FW-046 — major
**Statement:** No heap allocation in the 1 kHz sampler, fusion task, SPI/PPI/EasyDMA ISRs, or ESB radio ISR: static pools sized at compile time; build asserts no heap references from those translation units; worst-case stack depth analyzed per ISR with ≥25% margin [est.]; stack canaries verified in soak.
**Rationale:** Heap in hot paths = nondeterministic latency + fragmentation death over days (R125).
**Validation:** Build-time link check (no `_sbrk`/heap symbols in hot-path objects); 72 h soak with canary verification, zero overruns.
**Provenance:** R125.

### FW-047 — major
**Statement:** Interrupt priority map documented and enforced: 1 kHz sampler (highest), SPI DMA completion, USB, ESB radio (lowest of the time-critical set); no ISR blocks waiting on a lower-priority task (no priority inversion); ESB floods must not push the sampler outside the FW-022 jitter budget.
**Rationale:** A mis-prioritized radio ISR starves the sampler under RF load — FW-003's guarantee dies by a different perpetrator (R121).
**Validation:** ESB flood at max rate + USB IN flood: sampler jitter within ±50 µs; priority map asserted in the code-review checklist.
**Provenance:** R121.

### FW-048 — major
**Statement:** Click arbitration: a physical button edge and a touch tap within the same 50 ms [est.] window dispatch exactly one click — physical wins, touch suppressed; a physical press cancels a pending touch commitment window (FW-006); simultaneous physical-left + 2-finger touch never emits left+right.
**Rationale:** Shell-squeezers who also tap the ring otherwise double-fire (R131).
**Validation:** Solenoid rig pressing the physical button + tapping the ring with 0–50 ms offsets, 100 trials: exactly one click per trial, physical wins.
**Provenance:** R131.

### FW-050 — minor
**Statement:** CPI/DPI scaling from sensor counts to HID units uses an integer remainder accumulator: fractional counts accumulate across 1 ms ticks and only whole HID units are emitted; rounding is convergent (no systematic drift); DPI settable via vendor IF (200–3200 [est.]).
**Rationale:** Per-tick truncation loses ~0.5 count/tick → slow drift at rest-adjacent speeds (R124).
**Validation:** Constant-velocity motor rig: total HID displacement matches the shaft encoder within ±0.5% over 60 s at multiple DPI settings.
**Provenance:** R124.

### FW-051 — major
**Statement:** Click-commitment and gesture windows are computed on base-side arrival timestamps only; ball-frame timestamps are relative (ball boot clock) and carried for sequencing (FW-007), never mixed into base time math; ESB latency (≤5 ms [est.] typical) is absorbed by measuring the window from first-frame arrival; clock drift between ball and base is irrelevant by construction.
**Rationale:** Mixing ball-clock timestamps into base-side window math silently breaks FW-006 whenever clocks drift or ESB latency spikes (R130).
**Validation:** ESB latency injection 0–20 ms: click-type accuracy unchanged at ≥99%; code review asserts no ball-timestamp use in window comparisons.
**Provenance:** R130.

### FW-052 — major
**Statement:** ESB touch frames: bounded retransmit (≤3 tries [est.], ≤10 ms [est.] total) then drop; receiver discards frames with seq ≤ last-accepted (stale retransmits never re-fuse); latency beats reliability — a newer frame always supersedes an in-flight retry.
**Rationale:** Unbounded retry head-of-line-blocks fresh contact state; a stale retransmit replays a lifted finger → phantom click (R141).
**Validation:** Lossy-link bench (20% loss): click accuracy ≥99%, USB capture shows zero stale-frame dispatches.
**Provenance:** R141.

### FW-053 — major
**Statement:** Calibration/config flash writes: write-only-on-change (byte-compare before erase), dual-slot + CRC + sequence (atomicity per FW-035); lifetime writes budgeted <10% of the 10k-cycle [est.] rating at 1 cal/day × 10 years; flash-write counter exposed (FW-040).
**Rationale:** Per-boot calibration rewrites wear out nRF flash in the field (R137).
**Validation:** Write-cycle accounting test: 1000 simulated cal cycles → counter reads 1000, projected lifetime within budget; torn-write injection → old slot intact, CRC-valid.
**Provenance:** R137.

### FW-054 — major
**Statement:** Independent watchdog, windowed: serviced only from the main loop after all tasks check in alive (sampler, fusion, reporter, ESB); timeout 500 ms [est.], window lower bound 50 ms [est.] (early service = fault); watchdog config locked after init.
**Rationale:** A watchdog any ISR can pet never catches a wedged fusion task — only total lockup (R136).
**Validation:** Wedge each task in turn (test build): watchdog fires ≤500 ms every time; early-pet injection → fault flagged, not serviced.
**Provenance:** R136.

### FW-055 — minor
**Statement:** Firmware version (semantic + git hash + dirty flag) reported in the USB string descriptor, vendor GET, ESB passport, and embedded in the signed image metadata; all four must agree; host tools refuse to parse telemetry from an unknown version.
**Rationale:** Four disagreeing version identities make field diagnosis impossible (R139).
**Validation:** Build asserts the hash is injected at link time; host script checks all four agree across 3 builds; unknown-version telemetry → host refuses with a clear error.
**Provenance:** R139.

### FW-056 — major
**Statement:** The base firmware shall implement the scroll state machine (POINT / SCROLL_BTN / SCROLL_RING / SCROLL_LATCH) exactly per UX-002…UX-010: engagement strictly level-triggered (no firmware latch outside the configured SCROLL_LATCH mode); boot/reset state = POINT with all buttons up (FW-034); USB suspend forces POINT and clears the accumulator (no resume-into-scroll); a stuck-switch watchdog raises a vendor-IF diagnostic flag if any button is continuously asserted >60 s [est.] with zero ball motion and zero other input; timing constants (`SCROLL_TAP_MS` 200 ms, `SCROLL_TAP_COUNTS` 8, `RING_SCROLL_IDLE_MS` 120 ms [est.]) live in the gesture map (FW-033), never hardcoded.
**Rationale:** A latched-by-software scroll state is the stuck-mode failure (R288); hardcoded timing strands left-handed/accessibility users (R291).
**Validation:** State-machine model test: scripted press/hold/release/slide sequences, 200 trials — every transition matches the UX-002…010 contract; watchdog injection (60 s asserted, no motion) raises the flag exactly once; constants round-trip via gesture-map GET/SET.
**Provenance:** R287–R289, R291 (scroll-UX rounds).

### FW-057 — major
**Statement:** For ring scroll, the base shall compute per-contact slide velocity = contact world-frame velocity − ball surface velocity at the contact (from FW-001 fusion), using ball touch frames correlated to fusion ticks by frame sequence number (FW-007), never wall-clock; contacts within 12° [est.] azimuth merge to one before the gesture machine; slide floor 10°/s [est.] with 40 ms [est.] coherence for two contacts within 30° [est.] of tangential agreement.
**Rationale:** Timestamp-skew false-triggering is the implementation trap (R292); the merge threshold kills fat-finger phantoms (R290).
**Validation:** Bench rig with independently known slide vs roll (motorized ball + scripted finger slide): confusion matrix ≥99% correct classification over 200 trials; injected ±5 ms frame jitter produces zero false scroll entries.
**Provenance:** R290, R292 (scroll-UX rounds).

---

## HID / driver (33)

### HID-001 — blocker
**Statement:** USB Interface 0: 100% vanilla boot-protocol HID mouse
(buttons, X/Y 16-bit, wheel). It shall move the cursor in BIOS/UEFI with
zero software installed.
**Rationale:** The standard mouse interface is the fallback that makes the
product sellable with no driver; a broken composite descriptor kills it
(R23).
**Validation:** Plug into clean Windows 11 / macOS / Ubuntu + a UEFI
screen: cursor works <5 s, no prompts; descriptor parses clean under
USBView/hidrd with no warnings.
**Provenance:** R23.

### HID-002 — major
**Statement:** USB Interface 1: separate HID interface, vendor usage page
0xFF00, own report descriptor (<200 bytes [est.]), report IDs (e.g. RID 2
telemetry IN, RID 3 host→device OUT), single top-level application
collection, fixed-length interrupt IN ≤64 bytes @ 1000 Hz (bInterval 1),
`protocol_version` byte as stable ABI. Stay inside the HID class — never
WinUSB/bulk.
**Rationale:** Inbox drivers bind HID vendor pages on all three OSes with
no install; WinUSB would reintroduce the driver chicken-and-egg (R23).
**Validation:** Interface opens via hidapi on all three OSes; sustained
1000 reports/s, >99.9% [est.] sequence integrity over 60 s of motion.
**Provenance:** R23.

### HID-003 — major
**Statement:** Host software shall bind by VID/PID + usage page, never by
interface index or device-instance order.
**Rationale:** Windows enumerates composite HID interfaces in
nondeterministic order; index binding breaks across reboots (worker-D
§10.4).
**Validation:** 20 plug/reboot cycles on Windows: app finds the vendor
interface every time.
**Provenance:** Worker-D §10.4.

### HID-004 — minor
**Statement:** Ship a reference host daemon (hidapi, ~300 lines) plus a
permissive-license parser library on day one: raw deltas → (a) virtual
6-DOF joystick/spacemouse-style output, (b) OSC / local WebSocket stream
for Blender/CAD plugins. Optionally expose a third interface as a
standard HID multi-axis controller (Generic Desktop X/Y/Z/Rx/Ry/Rz) for
spacemouse-compatible apps.
**Rationale:** Defuses the hardware/app chicken-and-egg; the standard
mouse interface remains the no-driver fallback (R23, worker-D §3).
**Validation:** Clean-OS install test: vendor interface opens in the
sample app; Blender test build registers 6-DOF input if the multi-axis
interface is implemented.
**Provenance:** Worker-D §3.

### HID-005 — blocker
**Statement:** Interface 0's report descriptor shall declare zero Report ID
items (implicit ID 0). Interface 0 shall default to boot protocol on USB
reset/power-on and shall honor SET_PROTOCOL (0/1) and GET_PROTOCOL. In
boot protocol it shall emit exactly the 3-byte boot mouse format (buttons,
X/Y 8-bit signed, no wheel, no ID byte); in report protocol, the
descriptor-defined format, still with no ID byte.
**Rationale:** Boot-protocol reports have no ID byte by definition; a
0x85 item in the iface-0 descriptor makes BIOS/UEFI stacks misparse input.
Some UEFI implementations never issue SET_PROTOCOL, so the reset default
must be boot (R146).
**Validation:** hidrd parse of the iface-0 descriptor shows no Report ID
item; USB analyzer script: GET_PROTOCOL after reset returns 0;
SET_PROTOCOL(1) → descriptor-format reports; SET_PROTOCOL(0) → 3-byte boot
reports; cursor works in a UEFI shell on 2 boards.
**Provenance:** R146.

### HID-006 — major
**Statement:** Interface 0 shall be bInterfaceClass 3 (HID),
bInterfaceSubClass 1 (Boot), bInterfaceProtocol 2 (Mouse) — exactly.
**Rationale:** This triple is what binds the inbox boot-mouse driver on
every OS (mouhid/usbhid/IOHID); any other combination silently drops the
zero-software fallback (R160).
**Validation:** USBView/lsusb descriptor dump asserts the triple;
Device Manager shows mouhid.sys bound on Windows; dmesg shows usbhid on
Linux; IOHIDFamily on macOS.
**Provenance:** R160.

### HID-007 — major
**Statement:** Every field in the Interface 1 (vendor 0xFF00) report
descriptor shall declare Logical Minimum/Maximum covering firmware's real
emission range, an explicit Unit page + Unit Exponent, and little-endian
packing. ω axes: int32 LE, millidegrees/second, logical ±3,600,000.
Padding bits shall be declared Constant and firmware shall emit them as
zero. No float HID items.
**Rationale:** OS parsers clamp to logical range; float items are
mishandled by real HID stacks; undeclared padding leaks stack garbage to
the host (R147).
**Validation:** hidrd/USBView parse with zero warnings; firmware unit test
+ analyzer capture under extreme inputs: every emitted value within
logical range, all padding bits zero, byte-exact LE layout.
**Provenance:** R147.

### HID-008 — major
**Statement:** iSerialNumber shall be a 16-char uppercase hex string from
nRF FICR DEVICEID[1]:DEVICEID[0] (64-bit silicon ID); unique per unit;
stable across DFU. LANGID 0x0409 present; iManufacturer/iProduct non-empty
ASCII; all strings ≤126 UTF-16 chars.
**Rationale:** Windows builds the device-instance ID from the serial;
absent/unstable serials break rebinding (HID-003), multi-instance
disambiguation (HID-023), and post-reset daemon recovery (HID-012) (R148).
**Validation:** Enumerate 10 units: all serials distinct, 16 hex chars;
DFU one unit, re-read serial — identical; USBView shows strings clean.
**Provenance:** R148.

### HID-009 — major
**Statement:** bMaxPower shall be 0xFA (500 mA). Measured VBUS draw in the
worst case (1000 Hz streaming + max touch scan + LEDs max) shall stay
under the declared value with margin (target ≤450 mA [est.]).
**Rationale:** Under-declaring bMaxPower to "look efficient" risks host
overcurrent trips; the descriptor is a contract (R149).
**Validation:** USB power meter profile: streaming worst case, idle,
charger-active; PASS if peak < 500 mA declared and suspend (below) holds.
**Provenance:** R149.

### HID-010 — major
**Statement:** After 3 ms of bus idle the device shall enter USB suspend:
gate sensor clocks and touch scan, keeping only wake sources (button GPIO
+ ball proximity). Suspend current ≤2.5 mA. On resume, first valid report
≤10 ms [est.] with no state loss (RID-3 config retained).
**Rationale:** The 2.5 mA USB-2.0 suspend limit is measured by real
laptops; a 1 kHz sensor rig left running in suspend blows it 100× (R149).
**Validation:** Analyzer suspend/resume sequence + current measurement;
functional check post-resume on Windows/macOS/Linux; 20 suspend cycles,
zero state loss.
**Provenance:** R149.

### HID-011 — major
**Statement:** bmAttributes bit 5 (REMOTE_WAKEUP) shall be set. Firmware
shall signal resume only if the host armed it via
SET_FEATURE(DEVICE_REMOTE_WAKEUP); never otherwise. Button press wakes the
host <2 s when armed (wake sources configurable via RID 3; default
buttons + ball motion).
**Rationale:** Unarmed wakeup signaling is a USB-IF Chapter 9 failure and
wakes sleeping laptops in bags (R150).
**Validation:** Sleep host to S3 on each OS: armed → click wakes <2 s;
OS wake-disabled → analyzer shows no resume signaling on click; Chapter 9
compliance script passes.
**Provenance:** R150.

### HID-012 — major
**Statement:** After a USB reset the device shall re-enumerate <2 s into a
known default state (boot protocol on iface 0, default RID-3 config). The
host daemon shall detect re-enumeration by VID/PID + usage page + serial,
reopen, and re-send the last RID-3 host→device config within 1 s.
**Rationale:** Resets happen on every KVM flip and hub power-cycle; without
daemon re-send, vendor features silently revert to defaults (R151).
**Validation:** 20 hub-port power cycles: cursor works, vendor stream
resumes with config intact (assert a non-default RID-3 setting survives);
KVM flip test per HID-024.
**Provenance:** R151.

### HID-013 — major
**Statement:** Interface 1 interrupt IN: bInterval 1 (1 ms on full-speed);
firmware shall pace reports to SOF with at most one report per 1 ms frame
per endpoint. Mean inter-report interval 1.000 ms ±50 µs [est.]; jitter
(stddev) ≤100 µs [est.]. Never burst to catch up — coalesce to latest
state instead.
**Rationale:** FS interrupt allows one transaction/frame/endpoint; a
faster firmware timer cannot push more reports through, it only adds
jitter (R152).
**Validation:** 60 s USB analyzer capture: histogram of IN-token spacing
per endpoint; PASS on mean/jitter bounds; zero frames with >1 report.
**Provenance:** R152.

### HID-014 — major
**Statement:** Interrupt endpoints shall never STALL in normal operation
(empty → hardware NAK). STALL is for the control endpoint on unsupported
requests only.
**Rationale:** A STALLed interrupt endpoint wedges the host driver's queue
until clear; NAK-when-empty is the designed idle state (R152).
**Validation:** 60 s analyzer soak across all OSes: zero STALL PIDs on
interrupt endpoints; IN-token response within FS timing.
**Provenance:** R152.

### HID-015 — major
**Statement:** Class control requests: honor SET_IDLE/GET_IDLE per report
ID (boot iface included); GET_REPORT (Input) shall return the most recent
report bytes, never STALL; SET_PROTOCOL on iface 0 per HID-005; control
SET_REPORT routes to the RID-3 handler; any other class request shall
STALL cleanly in <50 ms. No request may ever time out.
**Rationale:** Some UEFI stacks hang on a GET_REPORT STALL; Windows
expects SET_IDLE honored; a 5 s control timeout bricks enumeration (R153).
**Validation:** Control-transfer fuzzer: all HID bRequests 0x01–0x0C ×
report types/IDs — every request completes (data or STALL) in <100 ms;
enumeration captures on 3 OSes show zero failed control transfers.
**Provenance:** R153.

### HID-016 — major
**Statement:** RID 3 host→device uses the interrupt OUT endpoint
(wMaxPacketSize ≥64); first byte is the report ID. The device shall apply
settings atomically, echo protocol_version, acknowledge via status flags
in the next RID 2, and ignore unknown trailing bytes/fields.
**Rationale:** Forward-compatible host→device channel: old firmware must
not choke on a newer daemon's longer config (R155).
**Validation:** Send RID 3 with random trailing bytes (fuzz): applied, no
STALL, status flags acknowledge; config round-trip test daemon→device.
**Provenance:** R155.

### HID-017 — major

**Statement:** RID 2 telemetry IN is fixed 64 B on the wire (1 B report ID + 63 B payload): u8 report_id = 2; u16 magic; u8 protocol_version (≠0); u16 seq (monotonic per session — 16-bit wrap disambiguated by host-side 32-bit extension); u32 timestamp_us (1 MHz device timer, HID-019); i32 ωx, ωy, ωz; u8 confidence[3]; u32 touch_timestamp_us; u8 touch_state; u8 status_flags; u16 crc16; zero-padded to 64 B. The magic/type/length/CRC16 framing discipline is folded in from former FW-040 (R142). Version ≠0 and length = 64 are the ABI contract (HID-016); any change to the layout bumps protocol_version and adds a new PID only per HID-015.

**Rationale:** The daemon parses this frame at 1000 Hz in a hot loop; a length change or a field reorder silently corrupts ω/touch on every OS. The framing header (magic, seq, CRC16) gives the host gap/corruption detection that a bare fixed layout lacks — one frame, one spec.

**Validation:** 60 s capture at 1000 Hz: host asserts monotonic seq (with 32-bit wrap extension), CRC16 passes on every frame, version == expected, length == 64 always.

**Provenance:** R154 + R142; merged per R227 (DEDUPE.md).

### HID-018 — major
**Statement:** protocol_version byte carries the ABI (e.g. 0x10 = v1.0).
Minor revisions are append-only before the zero padding; the host parser
shall accept reports with length ≥ the v1.0 minimum and ignore unknown
trailing bytes. Field removal/reorder requires a major bump + documented
migration. Old daemon + new firmware must still parse.
**Rationale:** PID-bumping per ABI change would nuke driver bindings and
daemon config; append-only + ignore-trailing is the compatible path
(R155).
**Validation:** Fuzz: random trailing bytes appended to RID 2 — parser
never rejects; cross-version smoke matrix (daemon v1.0 × firmware v1.1)
parses clean; parser unit tests pin the minimum-length rule.
**Provenance:** R155.

### HID-019 — major
**Statement:** The sensor timestamp and touch timestamp in RID 2 shall
derive from a single 1 MHz hardware timer (1 µs ticks); the host may
subtract them directly. 32-bit wrap (~71 min) is documented; host uses
modular arithmetic.
**Rationale:** Two free-running clock domains drift (crystal/RC ppm);
host-side "alignment" of independent clocks is guesswork (R154).
**Validation:** Synchronized stimulus rig (solenoid tap + motor flick at
the same instant): |touch_ts − sensor_ts| ≤1 ms [est.] in reported frames
across a 10-minute run spanning no wrap; wrap-handling unit test.
**Provenance:** R154.

### HID-020 — major
**Statement:** Per-axis confidence u8: 0 = axis unobservable (sensor
dropped from fusion), 255 = full weight. Confidence shall fall 255→0
within 50 ms of sensor loss (links FW-002). Host daemon: confidence <64
[est.] → freeze the axis (hold last value); never extrapolate across a
confidence drop.
**Rationale:** Silent zero-fill reads as a dead axis; announced
low-confidence lets the host freeze instead of drifting (R154, R5).
**Validation:** Tape-over-lens jig: confidence hits 0 ≤50 ms, host
freezes the axis, no cursor jump on recovery; host policy unit-tested.
**Provenance:** R154.

### HID-021 — major
**Statement:** Touch→photon latency budget: touch scan ≤2 ms + fusion ≤1 ms
+ USB frame ≤1 ms + host daemon ≤2 ms + app/compositor ≤8 ms [est.] =
total <20 ms [est.] (p99). Host inter-arrival jitter (stddev) ≤0.5 ms
[est.].
**Rationale:** "USB is fast" ships 60 ms mice; only an itemized, measured
budget keeps the 1 kHz path honest end to end (R156).
**Validation:** Firmware LED-on-touch test mode + photodiode on display +
scope: 100 taps, p99 LED→screen-flash <20 ms; daemon logs inter-arrival
histogram for the jitter bound.
**Provenance:** R156.

### HID-022 — major
**Statement:** Every RID 2 carries the u16 monotonic seq (HID-017); it
shall never repeat (wrap documented). The daemon shall keep a per-device
drop counter and expose it via API/status. Direct-attach 60 s @1000 Hz
soak: zero gaps expected. On a detected gap the daemon freezes; it never
extrapolates motion.
**Rationale:** Link-level retry doesn't cover host scheduling gaps, KVM
re-emulation, or hub TT quirks; without a seq, loss is a mystery jump
(R157).
**Validation:** 60 s soak asserts gaps == 0; fault-injection (firmware
test mode skips seq values): daemon counter increments, cursor freezes,
no jump.
**Provenance:** R157.

### HID-023 — major
**Statement:** The daemon shall key devices by serial (HID-008), hold zero
global/static per-device state, and stream N devices independently.
Unplugging one device shall not disturb the others or crash the daemon.
**Rationale:** Two-ball setups (dev + daily driver, A/B testing) are a
first-class use; global state turns the second plug-in into a heisenbug
(R158).
**Validation:** Two units streaming: assert independent seq streams and
per-device drop counters; unplug/replug one mid-stream — the other is
unaffected, daemon stays up, replugged unit rebinds by serial.
**Provenance:** R158.

### HID-024 — major
**Statement:** The device shall enumerate and sustain 1000 Hz through ≥2
cascaded USB 2.0 hubs. Through a KVM switch: Interface 0 (boot mouse)
must work via the KVM's HID ports; Interface 1 vendor features shall be
tested on 2 KVM models and traverse/fail documented per model (KVM HID
ports emulate a boot mouse; hub ports on the KVM may pass the full
device).
**Rationale:** KVMs emulate standard HID on their HID ports — vendor
interfaces are model-dependent, not guaranteed (R158).
**Validation:** 2-deep hub chain soak; 2-KVM test matrix (HID ports vs
hub ports × iface 0/1) published in docs; KVM flip triggers HID-012
recovery.
**Provenance:** R158.

### HID-025 — major
**Statement:** 5.1 kΩ Rd pull-downs on BOTH CC1 and CC2 (±10%). The device
shall enumerate and run full function (1000 Hz both interfaces) in both
USB-C plug orientations.
**Rationale:** Attach is detected on whichever CC the plug mates; a single
Rd enumerates in one orientation only — a classic field return (R159).
D+/D− diff-pair routing and TVS placement at the connector are
KICAD-domain: handoff to trackball.kicad_dru / layout checks, no custom
.dru here.
**Validation:** DMM: Rd on CC1/CC2 = 5.1 kΩ ±10% unpowered; 10 flips per
orientation: enumerate <2 s every time; 60 s 1000 Hz soak per orientation.
**Provenance:** R159.

### HID-026 — minor
**Statement:** Ship 99-trackball.rules matching the device by VID/PID with
TAG+="uaccess" (MODE 0660). A non-root user shall open the vendor
interface via hidapi on a fresh Ubuntu/Fedora install with no sudo.
**Rationale:** Linux hidraw nodes are root-only by default; without the
udev rule the reference daemon fails for every non-root user (R160).
**Validation:** Fresh-install test: non-root hidapi open succeeds;
dmesg shows no hid-core warnings ("unhandled", parse errors) on plug.
**Provenance:** R160.

### HID-027 — minor
**Statement:** Exactly one top-level application collection per interface;
macOS shall show exactly one IOHIDDevice service per interface in ioreg,
with vendor-page input reports delivered via IOHIDManager matching on
usage page 0xFF00 and no IOHIDFamily parse errors in Console.
**Rationale:** Locks in HID-002's single-TLC choice against the macOS
behavior of surfacing one service per top-level collection (R160).
**Validation:** ioreg -l | grep IOHIDDevice count == interface count;
sample IOHIDManager client with the 0xFF00 matching dictionary receives
RID 2 at 1000 Hz; Console clean during plug/unplug.
**Provenance:** R160.

### HID-028 — minor
**Statement:** Windows binds inbox drivers only: "HID-compliant mouse"
(mouhid) on iface 0, "HID-compliant vendor-defined device" (hidusb) on
iface 1, driver provider Microsoft, no yellow bangs. No .inf/.cat shall be
shipped. The device shall expose no MS OS 2.0 / WCID descriptor
advertising WinUSB.
**Rationale:** Inbox-only is the architecture; a WCID/WinUSB advertisement
or a shipped .inf reintroduces the driver chicken-and-egg HID-002 was
designed to kill (R160).
**Validation:** Clean Windows 11 install: no prompts, correct Device
Manager entries <5 s after plug (extends HID-001); USBView/descriptor dump
asserts no MS OS 2.0 descriptor; assert no WinUSB binding in setupapi log.
**Provenance:** R160.

### HID-029 — minor — PROVISIONAL (bonus platform coverage)
**Statement:** ChromeOS: WebHID shall be able to open the Interface 1
collection (vendor page 0xFF00 is outside the protected-usage list).
Android (host/OTG mode): the boot-mouse interface shall work as a
pointer; the vendor interface shall be reachable via UsbDeviceConnection
after the standard user permission dialog. Document both flows; not gating
V1.
**Rationale:** Bonus coverage; documents expectations instead of
discovering them from user bug reports (R160).
**Validation:** Chromebook: WebHID sample page opens iface 1 and reads
RID 2; Android: permission-flow doc + test on 1 device, mouse moves
cursor.
**Provenance:** R160.

### HID-030 — minor
**Statement:** Firmware shall implement no sticky-key, key-latching, or
modifier-emulation behavior. Sticky Keys, Filter Keys, and Mouse Keys are
OS-owned: with each enabled on Windows and macOS, click/drag/double-click
behavior shall be identical to a reference mouse. Document these
expectations in the user docs.
**Rationale:** Firmware-side latching fights the OS accessibility stack
and produces double-latch bugs; the device is a standard mouse to the OS
(R160).
**Validation:** Enable each feature on Win11/macOS: scripted click,
drag, and double-click-timing tests match reference-mouse results;
docs contain the expectations matrix.
**Provenance:** R160.

### HID-031 — minor
**Statement:** The daemon's outputs — OSC address schema, WebSocket JSON
schema, and virtual 6-DOF joystick mapping — shall be versioned with
semver, expose a /version endpoint, and carry migration notes on any major
bump. Breaking changes require a major version bump.
**Rationale:** The daemon is the ABI users build on (Blender/CAD plugins);
silent schema drift breaks plugins with no diagnostic (R160).
**Validation:** Schema conformance tests in CI; golden-transcript test:
recorded RID-2 stream → expected OSC/WS output, byte-compared.
**Provenance:** R160.

### HID-032 — major
**Statement:** Interface 0's report descriptor shall declare Wheel + AC Pan (+ Resolution Multiplier for hi-res wheel). Scroll vectors map to wheel units at 120 units per `SCROLL_NOTCH_COUNTS` ball counts [est., gesture-map tunable]; horizontal vector → AC Pan. Direction: default follows OS convention; macOS "natural" inversion applies automatically to wheel reports, and the gesture map offers an explicit invert for the vendor path. No driver required on Windows/macOS/Linux.
**Rationale:** The no-driver compatibility path must scroll out of the box; hi-res wheel keeps smooth-scroll feeling premium, not steppy (R287 context; SpaceMouse research: detented feel in CAD, smooth + inertia in documents).
**Validation:** Clean-OS plug test (Win/macOS/Ubuntu): scroll works in a browser and a text editor with no driver; USB capture shows Resolution Multiplier in the descriptor; direction-invert round-trips via gesture map.
**Provenance:** R287–R294 (scroll-UX rounds).

### HID-033 — major
**Statement:** Interface 1 (vendor 0xFF00) shall carry per-1 ms-report: raw scroll vector int16 LE X/Y, int16 zoom, and a mode-flags byte (bit0 = SCROLL_BTN, bit1 = SCROLL_RING, bit2 = SCROLL_LATCH); layout frozen under the `protocol_version` ABI (HID-002). The reference daemon maps these to virtual 6-DOF output, OSC/WebSocket, and per-application profiles (SpaceMouse-style auto-switching; never silently overwrites user customizations).
**Rationale:** Raw vectors + mode flags are what make the custom 3D-manipulation driver possible; app profiles are where CAD-vs-document scroll feel (detented vs smooth+inertia) lives.
**Validation:** hidapi capture during scripted scroll sessions: vectors track ball motion within one report tick, flags match the firmware state machine 100%; daemon app-profile switch test (two apps, 20 switches, zero lost customizations).
**Provenance:** R287–R294 (scroll-UX rounds).

---

## Scroll UX (13)

Normative UX definition: `~/workspace/trackball-build/scroll-ux/SCROLL_UX_DESIGN.md` Rev 1.0. Scroll is modal — two methods, no wheel (killed by user direction 2026-09-17; MECH-007/MECH-029/FW-049 dead).

### UX-001 — blocker
**Statement:** Scroll is modal with exactly two methods and no wheel: (A) button-held scroll — holding the scroll (third) button maps ball motion to scroll vectors with the cursor frozen, always available; (B) two-finger ring scroll — two fingers sliding on the capacitive touch ring map to scroll, available only when the ELEC-002 coupon proves reliable 2-finger disambiguation. No scroll wheel, scroll ring, capacitive strip, or twist-to-scroll shall be designed, tooled, or firmwared.
**Rationale:** The user's contract. Two methods bound the gesture vocabulary so every rule below is testable; a third method smuggled back in reopens mode-confusion (R287–R296).
**Validation:** Design review: no wheel/strip/twist in CAD, BOM, or firmware; firmware build has no scroll-wheel code path.
**Provenance:** User direction 2026-09-17; R287–R296 (scroll-UX rounds).

### UX-002 — major
**Statement:** Scroll-button tap-vs-hold: on press edge enter SCROLL_BTN immediately (cursor frozen at once); on release, if press duration <200 ms [est.] AND total ball motion <8 counts [est.] → emit middle click, no scroll; otherwise emit accumulated scroll vectors, no click. A short press with ball motion above the count budget classifies as scroll (never a phantom middle click — R289). Left/right clicks during SCROLL_BTN pass through as clicks with the cursor frozen. Hold+move behavior is remappable via the gesture map (FW-033): default scroll, optional middle-drag passthrough; the host daemon auto-switches per application profile.
**Rationale:** Freezing at press (not at hold-timeout) eliminates cursor-jump-then-freeze; post-hoc classification mirrors touchpad tap-vs-drag and Kensington's chord rule #1 (unqualified press = normal button); CAD users keep middle-drag pan via remap (R294). Preserving the drag underneath answers the SlimBlade Photoshop bug where scroll cancelled an in-progress drag (TrackballWorks research).
**Validation:** Solenoid + ball-motion rig, 200 trials across tap/hold/brush-press/drag combos: classification matches contract 100%; zero phantom middle clicks; drag preserved across scroll-mode entry/exit 50/50; remap round-trips via gesture map.
**Provenance:** R289, R294 (scroll-UX rounds); TrackballWorks research.

### UX-003 — major
**Statement:** In SCROLL_BTN, ball X-axis rotation → horizontal scroll, ball Y-axis rotation → vertical scroll; gain (scroll units per ball count, default 1:1 with fused CPI [est.]) and acceleration curve configurable via the gesture map (FW-033); the gain range must include a genuine precision floor (≤0.25× default [est.]) and an inertia/coast control — not just a linear multiplier; vectors accumulate at the 1 kHz cadence and emit as HID wheel + AC Pan on IF0 and raw int16 vectors on IF1.
**Rationale:** Multi-axis default (SpaceMouse research: users prefer simultaneous pan+zoom over dominant-axis lock); configurability covers CAD-vs-document feel. The precision floor answers the Orbit reviewers' "slowest setting still too fast" overshoot complaint (TrackballWorks research).
**Validation:** USB + hidapi capture during scripted ball motions: vector direction/gain match config; axis independence verified (diagonal ball motion → both axes); precision floor measured ≤0.25×.
**Provenance:** R287–R294; SpaceMouse research; TrackballWorks research.

### UX-004 — blocker
**Statement:** Ring scroll is defined in the ball frame: the ring rotates with the ball, so contacts fixed in ball frame during ball rotation = normal rolling (never scroll); contacts changing azimuth in ball frame = finger slide = scroll. The base computes per-contact slide velocity = world-frame contact velocity − ball surface velocity (FW-001 fusion), correlating ball touch frames to fusion ticks by frame sequence number (FW-007), never wall-clock.
**Rationale:** This definition is the entire difference between a working two-finger scroll and one that fires on every fast roll; timestamp-skew false-triggering is the implementation trap (R292).
**Validation:** Bench rig with independently known slide vs roll (motorized ball + scripted finger slide): confusion matrix ≥99% correct over 200 trials; ±5 ms injected frame jitter → zero false scroll entries.
**Provenance:** R292 (scroll-UX rounds).

### UX-005 — major
**Statement:** Two-finger tap (contacts appear/release with <10°/s [est.] slide and <200 ms duration) = right click, consistent with FW-006's settled-count rule. Two-finger slide (both contacts >10°/s [est.] ball-frame slide, coherent tangential direction within 30° [est.], sustained >40 ms [est.]) = scroll; detection latency ≤100 ms [est.]. Contacts within 12° [est.] azimuth merge to a single contact before gesture classification.
**Rationale:** The merge threshold kills fat-finger phantoms (R290); the tap/slide split mirrors UX-002's post-hoc classification.
**Validation:** Solenoid two-probe rig: tap→right-click ≥99/100, slide→scroll with latency ≤100 ms on USB capture; 22 mm broad probe (TOUCH-006) never resolves as two contacts.
**Provenance:** R290 (scroll-UX rounds).

### UX-006 — major
**Statement:** While SCROLL_BTN is active, ring-slide detection is suppressed entirely — Method A wins deterministically. The suppression is evaluated before the ring state machine every tick; the two scroll vectors can never sum.
**Rationale:** Eliminates the button+ring race by construction instead of by arbitration timing (R293).
**Validation:** Press scroll button mid-ring-scroll: ring vector drops to zero within one tick, 50/50 trials; no summed vectors on USB capture.
**Provenance:** R293 (scroll-UX rounds).

### UX-007 — major
**Statement:** Firmware build flag `RING_SCROLL_ENABLE`: if the ELEC-002 coupon fails to prove reliable 2-finger disambiguation, the flag is 0 — Method B and pinch compiled out, SCROLL_RING unreachable, ring remains tap-click only (or tap-disabled, configurable). Method A must be a complete scroll UX alone: the full UX validation matrix runs with the flag both on and off. This is a supported configuration, not a degraded mode.
**Rationale:** The coupon is the known weakest assumption; the fallback must be designed, not improvised at the bench (R292).
**Validation:** Full scroll validation matrix executed twice (flag on/off); flag-off build contains no ring-scroll code path (binary audit).
**Provenance:** R292 (scroll-UX rounds).

### UX-008 — major
**Statement:** SCROLL_LATCH (sticky scroll) is an opt-in gesture-map mode: tap scroll button toggles scroll on/off, fully one-finger operable; middle click moves to left+right chord (configurable). Latch exits on ANY of: scroll-button tap, left/right press (escape hatch), 15 s [est.] idle countdown from last ball movement (Auto Scroll pattern — slight motion holds, normal motion scrolls), USB suspend, or vendor-OUT "drop mode". Default off.
**Rationale:** Hold-while-rolling needs two digits of one hand; latch mode covers one-handed and limited-dexterity users as a first-class path (R291); the escape hatch + idle timeout + suspend exit guarantee the user is never trapped by the mode key (R288) — Kensington's own bug history (stuck chords, Auto Scroll surviving app-switch) shows exit paths are where modal designs die.
**Validation:** 5-user one-handed scroll task with latch on: task completion 5/5; latch exits on L/R press 20/20, on 15 s idle 5/5, on suspend 5/5; latch state exposed on vendor IF.
**Provenance:** R288, R291 (scroll-UX rounds); TrackballWorks research (Auto Scroll, chord bug history).

### UX-009 — major
**Statement:** Scroll-mode indication is three-layer: (1) the host driver switches to a scroll cursor whenever any SCROLL state is active, driven by the IF1 mode-flags byte (primary channel); (2) mode flags on every IF1 report (bit0 SCROLL_BTN, bit1 SCROLL_RING, bit2 SCROLL_LATCH) — scriptable/OSD-able; (3) the base status LED slow-pulses while any SCROLL state is active (no-driver fallback, one GPIO).
**Rationale:** "Why is my cursor dead" is the #1 modal-scroll failure (R287); momentary engagement self-resolves, but the user still needs to see the mode.
**Validation:** Scripted scroll sessions: cursor switches within 2 reports of mode entry 50/50; LED pulses during SCROLL with no driver loaded; flags match firmware state 100%.
**Provenance:** R287 (scroll-UX rounds); SpaceMouse research (LED + OSD triad).

### UX-010 — major
**Statement:** In any SCROLL state, cursor deltas are forced to zero; on mode exit the motion accumulator is cleared, never flushed — no catch-up cursor jump, no scroll burst after release. Scroll vectors never leak into cursor deltas.
**Rationale:** Accumulated-motion dumps on mode exit read as sensor faults and break user trust in the pointer (R287).
**Validation:** USB capture across 100 mode enter/exit cycles with ball motion during scroll: zero cursor deltas during SCROLL, zero motion burst within 50 ms after exit.
**Provenance:** R287 (scroll-UX rounds).

### UX-011 — minor
**Statement:** Pinch: two contacts whose angular separation changes while individual slide stays below floor = zoom vector (IF1 raw zoom; IF0 Ctrl+wheel, configurable). Secondary gesture under the same ELEC-002 gate as Method B.
**Rationale:** The 1D ring's only honest second gesture; zoom direction is a first-class user setting (SpaceMouse research: users genuinely disagree).
**Validation:** Scripted separation change: zoom vector sign/magnitude track separation; direction-invert configurable.
**Provenance:** Scroll-UX design; SpaceMouse research.

### UX-012 — major
**Statement:** Single-finger slide on the touch ring is an explicit no-op: it never scrolls and never clicks. The 1D ring's vocabulary is taps (clicks) + two-finger (scroll/pinch) — nothing else.
**Rationale:** Single-finger micro-slides happen constantly during normal rolling; any feature here either false-fires or feels dead, and it breaks the guarantee that rolling stays clean (R295, R296).
**Validation:** Scripted roll-with-one-finger-sliding session: zero scroll vectors, zero clicks on USB capture.
**Provenance:** R295, R296 (scroll-UX rounds).

### UX-013 — minor
**Statement:** Scroll mode shall emit synthesized per-notch tick feedback (host-side audio tick and/or haptic pulse, configurable, default on-soft) aligned to emitted wheel notches — one tick per 120-unit wheel quantum [est.].
**Rationale:** SlimBlade's audible per-tick clicks were specifically praised ("reassuring... easy to get an accurate single click for moving single lines"); a smooth gain curve with no feedback makes single-line scrolling guesswork (TrackballWorks research).
**Validation:** USB-audio capture: tick-to-notch alignment ±10 ms [est.] over 100 notches; user toggle round-trips via gesture map.
**Provenance:** TrackballWorks research (SlimBlade twist reviews).

---

## Touch sensing (32)

### TOUCH-001 — blocker
**Statement:** The touch ring shall provide ≥16 independent
self-capacitance electrodes covering the full 360° azimuth, each routed to
its own controller channel.
**Rationale:** 16 channels at 22.5° pitch give ≥5 samples across a 3-finger
span — the minimum for reliable 1/2/3-finger count + centroid arc sensing.
Fewer electrodes force adjacent-finger merging (R166).
**Validation:** Flat-coupon channel census then in-ball: a 14 mm grounded
steel probe touched at each electrode center must produce a touch delta
≥5× that channel's noise floor on all ≥16 channels. PASS = 16/16.
**Provenance:** R166. Ball Ø40.0 mm frozen nominal (Rev 2.1); ring pitch 5.24 mm at 24 electrodes (7.85 mm at the 16-electrode minimum).

### TOUCH-002 — major
**Statement:** Electrode arc width shall be ≥2× overlay thickness AND the
inter-electrode gap ≤0.3× electrode pitch, so that no azimuth is a dead
zone.
**Rationale:** The 2×-overlay width floor (sensitivity) and the 0.3-pitch
gap ceiling (coverage) jointly force electrode width ≈0.7 pitch on the
provisional geometry; stating only one bound yields an unbuildable ring
(R166 attacker).
**Validation:** Rotary stage, 14 mm grounded probe, 1° azimuth steps full
360°: at every step ≥1 electrode must report delta ≥5× noise. PASS = zero
dead steps. (12 mm probe used for margin check; 8 mm probe covered by
TOUCH-006.)
**Provenance:** R166. Geometry frozen at Ø40.0 mm nominal (Rev 2.1).

### TOUCH-003 — major
**Statement:** Electrode shape (bar vs interdigitated) shall be selected by
A/B measurement on the production-material flat coupon BEFORE the ring
flex is ordered; the winner is the shape with the higher minimum
per-electrode SNR across the coupon.
**Rationale:** Shape superiority claims without coupon data are
unvalidatable (R166 killed C3). The coupon (ELEC-002) is the last cheap
place to decide.
**Validation:** Two coupons, identical stack, both shapes; 14 mm probe,
per-electrode delta/noise on each; PASS = documented winner with ≥10%
SNR margin, decision recorded before flex Gerbers. Gates flex order.
**Provenance:** R166.

### TOUCH-004 — blocker
**Statement:** In the assembled ball (production shell + flex + controller),
every electrode shall show touch delta ≥5× its own noise floor for a
14 mm grounded probe touch, radio idle, 20 °C.
**Rationale:** The system-level SNR floor. ELEC-002 gates the flex on the
coupon (circuit-side); this rule is the in-ball acceptance — curvature,
overlay bond line, and assembly shift all cost signal (R167).
**Validation:** Assembled ball on dielectric stand; per-electrode probe
touch ×5, noise = RMS of 1000 idle samples per channel. PASS = min over
electrodes and trials of (delta/noise) ≥5.
**Provenance:** R167.

### TOUCH-005 — major
**Statement:** With the radio (BT/Wi-Fi) transmitting at max duty cycle,
per-electrode noise floor shall be ≤2× the quiescent floor, and touch
deltas shall still meet TOUCH-004's ≥5× ratio against the elevated floor.
Quiescent = radio idle, motors/coil off, 20 °C. Noise-floor qualification sweeps TX duty 10–100% [est.] (former RF-011, R87); if the criterion fails at any duty, cap-scan and TX bursts are time-multiplexed in firmware (never overlapping) as the designed fallback.
**Rationale:** TX bursts couple into the self-cap front end; a rule that
only passes with the radio quiet is a field failure (R167).
**Validation:** Force max-duty TX (test mode); measure per-channel noise
1000 samples idle vs TX; then probe-touch deltas under TX. PASS = noise
ratio ≤2.0 and delta/noise ≥5 under TX on all channels.
**Provenance:** R167 (absorbed R172 C18) + R87; merged per R221 (DEDUPE.md).

### TOUCH-006 — major
**Statement:** Both an 8 mm probe (child finger [est.]) and an 18 mm probe
(adult finger [est.]) shall be detected as exactly one contact with
correct count ≥95% over 100 trials each, at any azimuth.
**Rationale:** Contact-area variation is the dominant real-world spread;
an 8 mm contact near a gap is the small-signal corner, an 18 mm contact
the merge-risk corner (R167).
**Validation:** Solenoid rig with 8 mm, 14 mm, 18 mm, and 22 mm [est.] grounded probes (22 mm = broad-contact merge case, R290), random
azimuths, 100 trials each. PASS = single-contact declared, count correct
≥95/100 each; centroid within TOUCH-007 bounds; the 22 mm probe never
resolves as two contacts.
**Provenance:** R167. Probe diameters provisional.

### TOUCH-007 — major
**Statement:** Reported touch centroid shall be within ±3° of true probe
azimuth over the full 360°, excluding the seam exception zone.
**Rationale:** Finger velocity = arc velocity − ball ω feeds FW-005's
correlator; ±3° keeps arc-velocity error <10% at 100 Hz report (R168).
**Validation:** Rotary stage, 14 mm probe, 1° steps, 3 dwells per step;
centroid from controller report vs stage encoder. PASS = |error| ≤3° at
≥99% of steps outside the seam zone.
**Provenance:** R168.

### TOUCH-008 — major
**Statement:** The flex gore overlap / seam region shall be ≤1 electrode
pitch wide, and centroid error for touches inside it shall be ≤5°.
**Rationale:** A flex ring needs a seam; bounding its width and error
keeps it a local exception rather than a dead sector (R168).
**Validation:** Ball with production seam; rotary-stage sweep per
TOUCH-007 across the seam ±2 pitches. PASS = error ≤5° inside the
≤1-pitch seam zone, ≤3° outside it.
**Provenance:** R168.

### TOUCH-009 — major
**Statement:** Production shells at 1.0, 1.2, and 1.4 mm overlay (nominal
1.2 ±0.15 mm frozen; test spans ±0.2 mm as margin) shall all meet
TOUCH-004, with max:min per-electrode sensitivity spread ≤2:1 across the
three thicknesses.
**Rationale:** Rough-print thickness variation is a sensitivity spread
mechanism; the rule bounds it instead of hoping the print process is
better than it is (R169).
**Validation:** Three production-material shell coupons (1.0/1.2/1.4 mm)
over the electrode coupon; 14 mm probe delta/noise per electrode.
PASS = all ≥5× and (max delta)/(min delta) ≤2.0.
**Provenance:** R169. Thickness values frozen Rev 2.1 (1.2 ±0.15 mm V1).

### TOUCH-010 — major
**Statement:** The first article of each resin batch shall be re-measured
on the flat coupon; if any electrode's touch delta differs >±25% from the
qualified nominal, the batch triggers touch re-qualification before use.
For outsourced resin, each incoming supplier lot counts as a batch
(formulation locked per MFG-040).
**Rationale:** Batch εr drift is detectable but not controllable — so the
rule detects (R169). Paperwork certificates don't validate sensing.
**Validation:** Coupon delta/noise per electrode vs qualification record.
PASS = within ±25% → batch cleared; else re-run TOUCH-004/007/009
validations on the new batch.
**Provenance:** R169.

### TOUCH-011 — blocker
**Statement:** Every electrode's baseline shall sit within 20–80% of the
controller's ATI (auto-tuning) range at both 20 °C and 45 °C ambient, in
the assembled ball.
**Rationale:** Below 20% a touch saturates the channel; above 80% there is
no headroom for temperature/humidity drift. 45 °C is the realistic
hand-held + self-heating worst case (R170).
**Validation:** Environmental chamber soak 30 min at 20 °C and 45 °C;
read baselines per channel via controller. PASS = all channels in
[20%, 80%] at both temperatures.
**Provenance:** R170.

### TOUCH-012 — major
**Statement:** Over a −10…+50 °C chamber sweep, per-electrode touch delta
shall vary ≤30% vs the 20 °C value, and no false touch shall be declared
during 1 °C/min ramps.
**Rationale:** Baseline trackers lag fast ramps; the ramp test catches
tracker-lag false touches that static soaks miss (R170).
**Validation:** Chamber −10→+50 °C at 1 °C/min and back; continuous touch
logging, probe-touch delta spot checks every 10 °C. PASS = delta within
±30% of 20 °C value, zero false contacts during ramps.
**Provenance:** R170. −10 °C covers cold-soak-then-use; major, not
blocker.

### TOUCH-013 — major
**Statement:** After 24 h at 95% RH, no false touch shall persist >10 s,
baseline drift shall be <15%, and probe-touch deltas shall still meet
TOUCH-004 after the soak.
**Rationale:** Condensation film is a slow common-mode event — the danger
is the baseline tracker eating it and then desensitizing real touches,
so the post-soak touch check is part of the rule (R171).
**Validation:** Humidity chamber 95% RH 24 h, ball powered, touch log
running; then probe-touch per TOUCH-004. PASS = no false contact >10 s,
|baseline drift| <15%, deltas ≥5× noise.
**Provenance:** R171.

### TOUCH-014 — major
**Statement:** A wet adult finger (dipped in water, shaken once, not
dripping) shall be detected as a touch in ≥90% of 50 trials, with no more
than one extra adjacent electrode triggered beyond the true contact.
**Rationale:** Water film spreads the field and risks ghost neighbors;
the rule bounds both miss rate and ghost spread (R171).
**Validation:** 50 solenoid trials, water-dipped 14 mm silicone probe
[est. finger analog], random azimuths. PASS = ≥45/50 detected, ghost
electrodes ≤1 per trial.
**Provenance:** R171. Wetness definition provisional.

### TOUCH-015 — major
**Statement:** Supported glove set: bare finger, nitrile ≤0.15 mm, leather
≤1.0 mm — each shall meet TOUCH-004's ≥5× ratio. Textile/fleece >2 mm is
explicitly NOT supported and shall be documented as such in the user
guide.
**Rationale:** A defined support envelope beats a vague "works with
gloves" claim; the exclusion is part of the rule so support tickets have
an answer (R171).
**Validation:** Calibrated swatch set (nitrile 0.10/0.15 mm, leather 0.6/
1.0 mm shims, fleece 2.5 mm) over 14 mm probe on coupon then ball.
PASS = supported set ≥5× on all electrodes; fleece documented
unsupported (no pass requirement).
**Provenance:** R171.

### TOUCH-016 — major
**Statement:** Touch sensing is suspended during wireless charging
(FW-013); within 2 s of the charger field-off edge, baselines shall be
recalibrated and full sensing resumed, end-to-end including field-loss
detection latency.
**Rationale:** The sensing-side half of FW-013: the user picks the ball up
off the charger and expects it live, not stuck in recal (R172).
**Validation:** Charge-coil rig with field-off edge trigger; log touch
reports; probe-touch immediately at field-off + 2 s. PASS = valid touch
reports (TOUCH-004 deltas) ≤2.0 s after field-off, 20/20 trials.
**Provenance:** R172 (absorbed C18/C39).

### TOUCH-017 — major
**Statement:** After ±8 kV contact / ±15 kV air ESD (IEC 61000-4-2) applied
to the shell, baselines shall recover within 2 s with no stuck contacts
and no corruption of per-ball calibration NVM.
**Rationale:** Hand-held device = ESD target; the pass criterion is
recovery behavior (what we own), not immunity theater (R172).
**Validation:** ESD gun, 10 discharges each level/polarity, ball powered;
log baselines + contact state; read back NVM calibration. PASS = baseline
jump settled ≤2 s every shot, zero stuck contacts, NVM bit-exact.
**Provenance:** R172.

### TOUCH-018 — major
**Statement:** The touch subsystem shall scan a full frame at ≥100 Hz and
report at ≥50 Hz (1 finger) / ≥25 Hz (3 fingers), while drawing ≤15 mW
average [est.] from the ball battery.
**Rationale:** 100 Hz scan keeps arc-velocity quantization error small
for FW-005; the power cap forces the scan-rate/power trade to be measured,
not assumed (R173).
**Validation:** Controller register/frame-sync on scope (frame rate);
report log timestamps under 1- and 3-probe touches (report rate); current
at battery terminals over 60 s (power). PASS = ≥100 Hz scan, ≥50/≥25 Hz
report, ≤15 mW average.
**Provenance:** R173 (absorbed C22). Power budget provisional.

### TOUCH-019 — major
**Statement:** A qualified tap contact is 30–300 ms of continuous touch;
this qualifies the raw contact event and feeds FW-006's 30–50 ms click
commitment window — it does not replace it.
**Rationale:** Separates contact qualification (sensing) from click
arbitration (firmware); the 300 ms upper bound keeps tap distinct from
press/hold gestures owned elsewhere (R173).
**Validation:** Solenoid tap ladder 10–500 ms in 10 ms steps ×20 each;
controller event log. PASS = contacts 30–300 ms flagged tap-qualified,
<30 ms rejected as bounce, >300 ms not tap-qualified, zero misclasses
in the 30/300 ms boundary ±5 ms bands.
**Provenance:** R173.

### TOUCH-020 — major
**Statement:** Lift-off shall use hysteresis: release declared when signal
falls below 60% of the per-electrode touch threshold latched at contact
time (per contact, not global).
**Rationale:** A single threshold flickers on marginal lifts; latching the
release level to the contact-time threshold keeps it correct under
adaptive thresholds (R173).
**Validation:** Solenoid press/release cycling ×200 at threshold-marginal
force; event log. PASS = zero flicker (no re-touch within 100 ms of
release) across all trials.
**Provenance:** R173.

### TOUCH-021 — major
**Statement:** A finger held at ≥8 mm above the shell outer surface for a
2 s dwell shall not be reported as a touch.
**Rationale:** Hover-then-commit is a real gesture pattern; proximity
wake must not pre-fire contact state (R173).
**Validation:** Calibrated 8 mm spacer rig, finger analog hover, 2 s dwell
×30 trials all azimuths. PASS = zero touch reports; proximity channel
(if any) may fire but shall not set contact state.
**Provenance:** R173.

### TOUCH-022 — major
**Statement:** Two simultaneous finger contacts at 20 mm center separation
shall be reported as exactly 2 contacts in ≥95% of 100 trials.
**Rationale:** The baseline two-finger bar — 20 mm ≈ 2.5 pitches should be
easy; failing here means the geometry (TOUCH-001/002) is wrong, not the
algorithm (R174).
**Validation:** Dual-solenoid rig, two 14 mm probes at 20.0±0.5 mm
separation, random azimuths/orientations ×100. PASS = count == 2 in
≥95 trials.
**Provenance:** R174.

### TOUCH-023 — blocker
**Statement:** Two contacts shall be declared only when the inter-peak
valley depth is <60% of the lesser adjacent peak; a single 18 mm probe
shall never be split into two contacts (0/100 false splits), and two
14 mm probes at 18 mm separation shall be split in ≥95/100 trials.
**Rationale:** This is the core promise of a contact-*state* sensor: one
fat finger vs two close fingers. The valley criterion is the algorithm;
both sides of the decision boundary are validated (R174).
**Validation:** Solenoid rig: 18 mm single probe ×100 (PASS = 0 splits);
two 14 mm probes at 18.0±0.5 mm ×100 (PASS = ≥95 splits with valley
<60% of lesser peak at declaration).
**Provenance:** R174. 60% threshold provisional — coupon-tunable.

### TOUCH-024 — major
**Statement:** During 3-finger slow rotation (30°/s), contact tracking IDs
shall swap ≤1 time per 10 s window.
**Rationale:** ID swaps teleport the centroid arc and inject phantom
finger velocity into FW-005's finger-velocity = arc − ω computation
(R174).
**Validation:** Motorized 3-probe carousel at 30°/s, 60 s run; controller
tracking log. PASS = ≤6 swaps total, no swap bursts (>1 per 2 s).
**Provenance:** R174.

### TOUCH-025 — major
**Statement:** ≥4 simultaneous contacts shall each be reported distinctly
(no merging into fewer contacts) so FW-011's grab rejection sees the true
count.
**Rationale:** Sensing-side precondition for FW-011: firmware can't reject
a 4-contact grab it never sees as 4 (R174).
**Validation:** 4-probe solenoid rig (14 mm probes, ≥25 mm pairwise
separation), ×50 trials. PASS = count == 4 in ≥48/50; never reported as
<4.
**Provenance:** R174.

### TOUCH-026 — blocker
**Statement:** Touch delta ≥5× noise floor shall hold BOTH one-handed
(ball floating on a dielectric stand — the touching hand is the only
ground reference) and two-handed (user's other hand on chassis ground),
with the delta ratio between conditions ≤2:1 on every electrode.
**Rationale:** Highest-risk physics in the project: a floating ball whose
ground IS the user. If one-handed sensitivity collapses, the product is
unusable in its primary grip (R175).
**Validation:** Dielectric stand vs grounded-plate rig; 14 mm probe
touched by an isolated vs grounded operator analog; per-electrode
delta/noise both conditions. PASS = ≥5× in both, ratio ≤2.0, all
electrodes.
**Provenance:** R175.

### TOUCH-027 — major
**Statement:** With a probe held stationary on the shell while the ball
rotates 90°, the contact ID shall persist and the reported centroid arc
velocity shall track the ball encoder ω within ±15%.
**Rationale:** Sensing-side requirement for FW-005's correlator: a finger
planted while the ball spins under it must read as arc-velocity ≈ ω
(finger stationary in world frame), not as finger motion (R176/R167).
**Validation:** Motorized ball rig at constant ω with fixed 14 mm probe;
encoder vs reported centroid arc velocity over 90° rotation ×20.
PASS = ID persistence 20/20, |arc_vel − ω|/ω ≤15%.
**Provenance:** R176.

### TOUCH-028 — major
**Statement:** After 10k ball rotations on the wear rig (≈1 year heavy use
[est.]), overlay loss shall be ≤0.1 mm and per-electrode touch delta
degradation ≤20%, with TOUCH-004's ≥5× ratio still met.
**Rationale:** Shell wear thins the overlay unevenly — sensitivity drifts
up where worn, and micro-scratches scatter the field; the rule bounds
lifetime drift (R176).
**Validation:** Wear rig (ball rotated against socket-analog contact
10k rev); overlay thickness gauge before/after; per-electrode probe
delta before/after. PASS = loss ≤0.1 mm, delta loss ≤20%, still ≥5×.
**Provenance:** R176. Lifetime equivalence provisional.

### TOUCH-029 — minor
**Statement:** 50 isopropanol wipe cycles shall shift baselines ≤10% with
no electrode delamination visible at 10× magnification. IPA is the
supported cleaning agent; harsher solvents (acetone etc.) are out of
scope and documented as unsupported.
**Rationale:** Cleaning is a chemical-aging vector distinct from
mechanical wear; scoping the supported agent keeps the rule testable
(R176).
**Validation:** 50× IPA wipe with lint-free cloth, baseline log
before/after, 10× visual inspection. PASS = |shift| ≤10% all channels,
no lifting/edge delamination.
**Provenance:** R176.

### TOUCH-030 — blocker
**Statement:** Every production ball shall store per-electrode baseline +
gain calibration in NVM, written at production test; per-electrode
production touch-test limits with a 14 mm probe are: lower = 5× that
electrode's noise floor, upper = 2× the nominal median delta. Units
outside either limit are rejected (waiver path documented).
**Rationale:** The calibration data IS the sensing model (gain
normalizes the TOUCH-009 thickness spread); the upper limit catches
overlay thin spots and flex damage that would drift out of the ATI
window first (TOUCH-011). Yield concerns don't override a drift
predictor (R176).
**Validation:** Production test fixture: per-electrode noise + delta,
NVM read-back bit-exact; first-article correlation to flat coupon
within ±15%. PASS = limits enforced in fixture software, NVM verified.
Gates shipment.
**Provenance:** R176 (absorbed C36).

### TOUCH-031 — major
**Statement:** The touch-ring band (polar 75–105°) shall be printed solid:
100% infill or ≥4 perimeters [est.] in the band; foaming/lightweight
filaments are banned in the ball shell. The slicer project (profile +
infill settings) is checked into the design record per print lot.
**Rationale:** Infill percentage/pattern variation is local εr and
thickness variation → per-electrode delta spread. TOUCH-004 catches it at
full assembly — the most expensive place to learn the slicer was wrong
(R268). Solid band makes the dielectric deterministic by construction.
**Validation:** Slicer-project audit per lot (infill override in the band
region) + TOUCH-004 per-electrode spread: max:min delta ≤2:1 [est.]
across the ring on the assembled ball.
**Provenance:** R268.

### TOUCH-032 — major
**Statement:** The touch flex ring is a fixed-length band; the shell inner
circumference at the ring band varies with print shrinkage (Ø37.6 ±0.42 mm
→ 118.1 ±1.3 mm). The flex shall close with a compliant overlap joint
accommodating ±1.5 mm [est.] circumference variation, overlap length
≥5 mm [est.] (≈1 electrode pitch, consistent with TOUCH-008's seam
bound), with no buckle (electrode-to-shell gap still ≤0.3 mm per
MECH-014) and no tensile stretch of the flex.
**Rationale:** A fixed flex on a variable shell either buckles (gap >
MECH-014 → dead/hot sectors) or can't close (assembly fails). The donor
ball never had this problem because we didn't print it (R269).
**Validation:** Assemble the production flex on min-circumference and
max-circumference mandrels (116.6 / 119.6 mm [est.]): PASS = closes with
≥5 mm overlap, no visible buckle, per-electrode gap ≤0.3 mm, TOUCH-008
seam error bound holds on both.
**Provenance:** R269.

---

## Manufacturing / test (41)

### MFG-001 — blocker
**Statement:** Each custom-ball print lot, per qualified process: first
article fully verified against the frozen ball spec (diameter Ø40.0 ±0.3
mm V1 / ±0.1 mm resin V2-path, radial runout ≤0.15 mm V1 / ≤0.10 mm
resin, wall 1.2 ±0.15 mm at ≥6 points, weight logged), then n=5 sampled
per lot (100% if lot <10); reject or sort the lot on any out-of-tolerance
ball. The 0.2 mm-nozzle process and the outsourced-resin process each get
their own first-article gate — neither inherits the 0.4 mm gate
(MFG-037/039).
**Rationale:** Ball diameter/sphericity feed MECH-002 (sensor Z), MECH-003,
and the A-matrix (ELEC-007); an out-of-round custom ball silently biases
every downstream calibration — and unlike a donor lot, a bad print lot
is our process failing, so the lot traveler must also record spool lot
and shrinkage-coupon factors (MFG-036) to close the loop.
**Validation:** Caliper + V-block/indicator + ultrasonic/micrometer wall
check per sampled ball; record diameter, max-min roundness, wall
thicknesses, spool lot in the lot traveler. Gate: shell assembly and
first-article calibration blocked on a passing lot.
**Provenance:** R186; rewritten Rev 2.1 (donor-ball lot → custom-ball
print lot).

### MFG-002 — major
**Statement:** Incoming shell lots (printed or molded): critical dims
(sensor window bores, boss IDs, coil seat), LED/dot window clarity, and
finish checked on an AQL sampling plan; reject lot on any critical defect.
**Rationale:** Shell is the datum for sensor Z (MECH-002), coil gap
(MECH-010), and probe-hole alignment (MFG-017); a bad lot poisons
assembly yield.
**Validation:** Caliper/bore-gauge + visual under 5× on sampled shells;
record measurements per lot in traveler. Gate: assembly work order not
released against a rejected lot.
**Provenance:** R186.

### MFG-003 — blocker
**Statement:** LiPo cell lot: vendor UN38.3 test summary on file before
first assembly; capacity spot-check n=3/lot within ±5% [est.] of rated
120 mAh; connector type matches the selected part (see MFG-015).
**Rationale:** Uncertified cells are a ship-blocker and a safety hazard;
capacity drift signals counterfeit or aged stock.
**Validation:** File the UN38.3 summary in the lot traveler; 0.2C
discharge spot check, record mAh. Gate: no cell leaves stores without a
passing lot record.
**Provenance:** R186.

### MFG-004 — major
**Statement:** Incoming PCB/flex lots: fab certificate of conformance
(finish, stackup, UL rating) required; 3-sample dimensional + solderability
(wetting) check per lot.
**Rationale:** COC is the only leverage on an outside fab; solderability
sampling catches shelf-aged ENIG before it becomes an assembly-line
mystery.
**Validation:** File COC in lot traveler; wetting balance or hand-solder
sample, record pass/fail. Gate: kitting blocked on missing COC.
**Provenance:** R186.

### MFG-005 — major
**Statement:** Coupon sequence gates production: (1) flat touch coupon in
production shell material/thickness passes ELEC-002; (2) coil coupon
passes CHG LCR/envelope gates; (3) first article; (4) pilot run. Each
stage's sign-off is required before the next stage's spend.
**Rationale:** Unordered testing lets a fab order race ahead of physics;
the sequence makes each expensive step conditional on the cheap proof
before it.
**Validation:** Stage sign-off sheets in the program traveler with
measured values attached. Gate: PO for the next stage not issued without
the prior sign-off.
**Provenance:** R187.

### MFG-006 — blocker
**Statement:** Program kill criteria are numeric and written before
coupon spend: e.g. 2 consecutive coupon spins failing the ELEC-002
per-electrode floor → halt flex order and trigger design review; coil
coupon missing the CHG envelope twice → halt coil tooling.
**Rationale:** Without pre-committed stops, sunk cost keeps a dead program
walking; the criteria convert "the coupon failed" into an automatic halt
instead of a meeting.
**Validation:** Kill-criteria sheet signed before coupon PO; any halt
event recorded with the failing measurements. Gate: coupon PO not issued
without the signed sheet.
**Provenance:** R187.

### MFG-007 — major
**Statement:** Flex fab drawing shall specify panelization, stiffener
locations/thickness, coverlay windows (pogo pads, test points, bend
regions), and fiducials; fab sign-off required on the drawing revision.
**Rationale:** Stiffeners under the connector/pogo area and coverlay
windows are not inferable by the fab; missing fiducials break automated
flat-test fixturing (MFG-010).
**Validation:** Drawing checklist reviewed at fab release; incoming
3-sample check of stiffener placement and window registration. Gate: fab
release blocked on checklist.
**Provenance:** R188.

### MFG-008 — blocker
**Statement:** Bend regions marked on the flex fab drawing with a
component and via keep-out; no copper features except continuous traces
(with teardrops) inside the bend zone.
**Rationale:** A via or part in the bend apex is a fatigue crack waiting
for the first ball drop; MECH-009's bend-radius rule is unenforceable if
the fab can place features in the bend.
**Validation:** Gerber DRC check for vias/parts inside bend polygons at
fab release + first-article microsection of one bend. Gate: fab release
blocked on clean DRC.
**Provenance:** R188.

### MFG-009 — minor
**Statement:** No impedance control required on the touch flex: stated as a
note on the fab drawing with the justification (all signals <1 MHz
[est.], longest trace <80 mm [est.]); design review sign-off on the note.
**Rationale:** Unstated, a fab may add impedance control (cost, lead
time) or a reviewer may demand it late; a signed negative requirement
closes the question.
**Validation:** Drawing note present + reviewer signature in the release
record. Gate: fab release.
**Provenance:** R188.

### MFG-010 — blocker
**Statement:** Every touch flex is programmed and functionally tested
FLAT before bending (Pixels flow): FW-012 self-test passes, per-electrode
baselines recorded within the ELEC-002 window; the flat-test record
(serial, baselines, FW version) is required before the flex may be bent.
**Rationale:** A dead-on-arrival flex bent into a ball is untestable scrap
inside a $300 device; flat test catches fab defects while rework is still
cheap (replace the flex, not the ball).
**Validation:** Flat-test fixture (pogo bed + FW-012 report capture);
record per serial in traveler. Gate: bend station does not accept a flex
without a passing flat-test record.
**Provenance:** R189.

### MFG-011 — major
**Statement:** Post-bend retest: per-electrode baseline delta ≤10% [est.]
vs the flex's own flat-test record and no railed channels; failing flexes
are scrapped, not re-bent.
**Rationale:** Bending is the highest-stress step in the flex's life;
the delta vs its own flat record isolates bend damage from fab variation.
**Validation:** Same fixture as MFG-010; delta computed automatically,
record stored. Gate: assembly kitting blocked on missing/failed retest.
**Provenance:** R189.

### MFG-012 — major
**Statement:** Flex serialization at flat test: unique serial marked on
the flex (laser or inkjet, outside bend zones) and entered in the test
record; the serial is the traceability root for that ball's touch data.
**Rationale:** Without serialization at the first test, MFG-028
traceability has nothing to anchor to — field failures can't be traced to
a fab lot.
**Validation:** Mark legibility check at flat test; serial uniqueness
enforced in the traveler DB. Gate: flat-test record incomplete without
serial.
**Provenance:** R189.

### MFG-013 — major
**Statement:** Ball assembly order: RX coil → touch flex → main PCB →
battery LAST → shell close; battery installed no earlier than needed and
energized-open time ≤15 min [est.] per unit.
**Rationale:** Battery-last minimizes the time a live cell sits next to
metal tools and probe fixtures; coil-first because the coil seat is
inaccessible once the flex/PCB stack is in.
**Validation:** Assembly traveler with station sign-offs in order;
energized-open time sampled per shift. Gate: QA audit of traveler order.
**Provenance:** R190.

### MFG-014 — major
**Statement:** Cell state of charge 30–70% at assembly; open-circuit
voltage measured and recorded per unit before install.
**Rationale:** Assembling at full charge maximizes stored energy during
the riskiest handling; near-empty risks over-discharge if the unit sits
in WIP. OCV record proves the window was met.
**Validation:** DMM OCV per unit vs the SoC–OCV table for the selected
cell; record in traveler. Gate: unit fails QA without the OCV record.
**Provenance:** R190.

### MFG-015 — major — PROVISIONAL (needs battery connector selection)
**Statement:** Battery connects via its factory-fitted connector only; no
hand soldering or tab welding on cells in V1 assembly or rework.
**Rationale:** Hand heat on LiPo tabs is a latent-damage lottery
(separator shrinkage, seal damage); the connector moves the joint to the
vendor's controlled process.
**Validation:** Assembly drawing shows connector mating, no solder joint
at the cell; QA visual per unit. Gate: first-article approval.
Provisional: connector part not selected.
**Provenance:** R190.

### MFG-016 — blocker
**Statement:** After battery install and before shell close: DMM isolation
check (cell +/− to shell hardware, coil, and flex shield) — no continuity,
leakage <1 µA [est.] at cell voltage; record per unit.
**Rationale:** A pinched flex or stray screw bridging the cell inside a
screwed-shut ball is a thermal event with no user-serviceable fix; this
is the last cheap detection point.
**Validation:** Bed-of-nails or handheld DMM procedure on the line;
pass/fail + leakage value in traveler. Gate: shell-close station blocked
without a passing record.
**Provenance:** R190.

### MFG-017 — blocker
**Statement:** SWD pogo pads reachable with the shell screwed shut via
probe holes: hole Ø ≥1.5 mm [est.], aligned to pads within ±0.3 mm
[est.], depth-limited so pins cannot over-travel; validated with the
production pogo fixture on a screwed-shut ball.
**Rationale:** FW-010 requires SWD pogo on both PCBs and DFU validation
on a screwed-shut ball; without probe holes "serviceable" means
"disassemble first," which breaks the DFU recovery story.
**Validation:** Pogo fixture connects and holds SWD (attach + halt +
resume) on 3/3 screwed-shut first articles; hole/pad alignment measured
on first article. Gate: shell tooling release.
**Provenance:** R191.

### MFG-018 — major — PROVISIONAL (needs boss geometry)
**Statement:** Screw torque spec per boss size on the assembly drawing;
torque drivers (not hand feel) on the line; qualification: ≥10 open/close
cycles without strip or boss cracking on first-article shells.
**Rationale:** Over-torque cracks resin bosses, under-torque rattles;
"snug" is not a spec. The cycle test proves the MECH-025 insert system
delivers the serviceable-shell promise.
**Validation:** Torque values recorded per unit (driver with readout) on
pilot; 10-cycle test on n=3 shells, record torque retention and visual.
Gate: pilot QA. Provisional: torque values need boss/insert geometry.
**Provenance:** R191.

### MFG-019 — major
**Statement:** Adhesive allowlist for serviceable joints: removable only
(silicone RTV, removable acrylic tape); cyanoacrylate and structural
epoxy banned on any joint opened during service; allowlist and ban list
on the assembly drawing; peel compatibility checked on production shell
material.
**Rationale:** Serviceable ≠ permanent is architecture; one CA-glued
joint turns a screwed shell into a destructive teardown.
**Validation:** 90° peel test of allowlisted adhesives on shell-material
coupons (clean removal, no substrate damage); QA visual per unit that no
banned adhesive is present. Gate: first-article approval.
**Provenance:** R191.

### MFG-020 — major
**Statement:** Conformal coat policy: ball main PCB coated (humidity from
handling/condensation cycling); pogo pads, charge contacts, and the
touch-flex connector masked. Base PCB coated except USB-C interior and
sensor apertures. Mask list on the assembly drawing.
**Rationale:** A handled ball sees warm-hand/cool-electronics condensation
cycles; unmasked coat on pogo pads would brick MFG-017 shell-closed SWD.
**Validation:** First-article visual + continuity that masked areas are
coat-free; humidity soak (40 °C/90% RH, 48 h [est.]) on coated vs
uncoated ball PCB coupon, insulation resistance compared. Gate:
first-article approval.
**Provenance:** R192.

### MFG-021 — major
**Statement:** Base uses a pre-certified nRF52840 module; no chip-down RF
in V1.
**Rationale:** Module grant keeps intentional-radiator certification a
labeling exercise (MFG-030) instead of a test campaign; chip-down would
also add RF tuning to every base PCB.
**Validation:** Module part number on BOM; grant ID on file. Gate: BOM
release.
**Provenance:** R192.

### MFG-022 — major
**Statement:** Coil winding uses a turns-count fixture; every wound coil
LCR-checked after winding against the CHG gate limits; per-lot winding
record (turns, L, Q, DCR).
**Rationale:** The CHG LCR gate measures the result; this rule controls
the process that produces it — a drifting winder fails lots instead of
coils.
**Validation:** Fixture turns counter + LCR meter procedure; record per
lot in traveler. Gate: coil lot not released to kitting without the
record.
**Provenance:** R192.

### MFG-023 — major
**Statement:** Optical sensor placement ±0.2 mm / ±1° [est.] via solder
paste + placement fixture (not hand placement); first-article placement
measured per sensor.
**Rationale:** MECH-002's Z tolerance and the fusion geometry assume both
sensors sit where the model says; hand-placed sensors add a per-unit CPI
bias the A-matrix (ELEC-007) then has to absorb.
**Validation:** First-article CMM/vision measurement of sensor position
vs CAD; fixture qualified once, re-checked per shift. Gate:
first-article approval.
**Provenance:** R192.

### MFG-024 — major
**Statement:** A-matrix calibration runs on a spin rig fixture per unit:
procedure + time budget ≤5 min/unit [est.]; calibration file (matrix +
spin log) stored per serial. This is the manufacturing process behind
ELEC-007.
**Rationale:** ELEC-007 states the calibration requirement; without a
fixtured process and a time budget it doesn't happen on a line — it
happens never, or once, by hand.
**Validation:** Rig procedure document; per-unit calibration file present
in traveler; cycle time sampled per shift. Gate: unit ships only with a
calibration file matching its serial.
**Provenance:** R193.

### MFG-025 — major
**Statement:** Touch line limits per unit: per-electrode baseline window
and touch-delta thresholds derived from ELEC-002 recorded at end-of-line
(via FW-012 self-test report); unit fails if any electrode is outside
limits.
**Rationale:** ELEC-002 qualifies the design, FW-012 provides the
mechanism; this rule makes the per-unit pass/fail gate that stops a
damaged flex (MFG-011 escape) from shipping.
**Validation:** End-of-line fixture captures FW-012 report; limits
auto-checked, record per serial. Gate: ship release.
**Provenance:** R193.

### MFG-026 — major
**Statement:** Burn-in before ship: 4 h [est.] thermal cycle plus 2 full
charge cycles per unit; any failure → FA hold, no ship, failure record
linked to serial.
**Rationale:** Screens infant mortality (cold solder, weak cell, flex
microcrack) before the customer finds it; the charge cycles also prove
the CHG path end-to-end on every unit.
**Validation:** Burn-in rack log per serial (temp profile + charge
curves); failure quarantine procedure. Gate: ship release blocked without
a passing burn-in record.
**Provenance:** R193.

### MFG-027 — major
**Statement:** QA sampling: C=0 (zero defects allowed) on blocker-class
defects for pilot lots; production AQL 1.0 major / 2.5 minor [est.];
sampling plan documented per lot size.
**Rationale:** Pilot lots are small, so C=0 on blockers is cheap and buys
a hard gate where design risk is highest; production AQLs scale the
inspection cost with volume.
**Validation:** Lot acceptance records with defect classification counts.
Gate: lot ship release.
**Provenance:** R194.

### MFG-028 — blocker
**Statement:** Traceability: unit serial ↔ MCU FICR ↔ calibration file ↔
flat-test, burn-in, and QA records, linked in the traveler DB; traveler
records retained ≥2 years [est.].
**Rationale:** Without the serial↔FICR↔records chain, every other MFG
record is orphan data — field failures can't reach a fab lot, and the
FA loop (MFG-033) has nothing to analyze.
**Validation:** DB query per sampled serial returns the full chain;
retention verified by audit. Gate: ship release queries the chain.
**Provenance:** R194.

### MFG-029 — major
**Statement:** Packaging: ESD shielding bag, cell SoC 30–50% at pack-out (measured), per CHG-020's OCV definition (3.75–3.85 V [est.]) — amended R231 to resolve the CHG-020 contradiction
(measured), ISTA 1A drop test qualified on the retail pack; pack-out
checklist per unit.
**Rationale:** Storage SoC 40–60% maximizes cell shelf life; the drop
qualification proves the 200 g+ steel-weighted base (architecture) plus
ball survive parcel handling.
**Validation:** SoC recorded at pack-out; ISTA 1A report on file per pack
revision; checklist in traveler. Gate: ship release.
**Provenance:** R195; amended per R231 (DEDUPE.md).

### MFG-030 — major
**Statement:** Labeling: base carries FCC ID (module grant, MFG-021),
serial number, and RoHS mark; ball shell carries revision mark; label
artwork revision-controlled.
**Rationale:** Module-grant labeling is a legal ship requirement, not a
nice-to-have; shell rev marks let service identify the hardware without
opening it.
**Validation:** First-article label inspection vs artwork; per-unit label
presence check at pack-out. Gate: ship release.
**Provenance:** R195.

### MFG-031 — blocker
**Statement:** V1 exit criteria: all blocker rules pass; all major rules
pass or carry a written waiver; waiver = named approver (project lead) +
expiry date + recorded rationale; expired waiver = open defect; minor
rules tracked to closure or waiver.
**Rationale:** Exit criteria as rules make "are we done" auditable
instead of vibes; expiring waivers prevent temporary exceptions from
becoming permanent.
**Validation:** Exit checklist with rule-by-rule disposition, signed;
waiver register reviewed at exit review. Gate: V1 ship decision.
**Provenance:** R195.

### MFG-032 — major
**Statement:** Rework policy: battery never reworked (replace unit-level
assembly); flex/coil replaced, not re-bent/rewound, max one replacement
per unit; inserts re-set max twice per boss; all rework recorded against
the serial and the unit re-passes MFG-011/017/027/028 gates.
**Rationale:** Re-bending a flex re-ages its fatigue life invisibly;
reworked batteries are a safety incident waiting for a customer. The
re-test requirement keeps rework honest.
**Validation:** Rework log per serial; QA verifies gate re-pass records.
Gate: reworked unit ship release.
**Provenance:** R195.

### MFG-033 — minor
**Statement:** Failure-analysis loop: every field return gets an FA record
(root cause, fab lot, serial chain via MFG-028) within 30 days [est.];
recurring root causes produce a rule update or a design change — never
just a replacement shipment.
**Rationale:** Field returns are the only test of the DRC library itself;
without a loop back into the rules, the library fossilizes while the
failure modes evolve.
**Validation:** FA register; quarterly review minutes showing rule
updates or explicit no-change rationale. Gate: none (process), audited
quarterly.
**Provenance:** R195.

### MFG-034 — minor
**Statement:** Version marking: PCBs carry silkscreen revision + date
code; shells carry mold cavity ID (or print batch ID); marks legible
after assembly.
**Rationale:** Cavity/batch IDs isolate tooling-wear defects to a subset
of shells; PCB rev marks let FW (FW-010 DFU) and service identify
hardware rev without a database lookup.
**Validation:** First-article mark inspection; per-lot sample. Gate:
first-article approval.
**Provenance:** R195.

### MFG-035 — minor
**Statement:** Golden units: ≥2 per hardware revision retained, stored at
40–60% SoC, re-baselined (MFG-024/027) at each revision; used as
arbitration reference for line-measurement disputes.
**Rationale:** When the line and the lab disagree, the argument needs a
referee both trust; golden units also give FW regression a stable
hardware target.
**Validation:** Golden-unit log (serials, rev, last baseline date);
annual re-baseline record. Gate: none (process), audited at rev change.
**Provenance:** R195.

### MFG-036 — major
**Statement:** Every ball print lot carries a traveler recording: filament
spool manufacturer + lot, MECH-023 shrinkage-coupon scale factors applied,
first-article CMM (diameter, radial runout, wall thickness at ≥6 points),
and resin/filament batch (feeds TOUCH-010 re-qualification). The traveler
is retained per shipped unit serial.
**Rationale:** With no donor lot to blame, a field failure (drift,
cracking, touch regression) must trace to a print variable — spool,
shrinkage comp, or batch. Without the traveler the failure is
unattributable and the corrective action is guesswork (R271).
**Validation:** Traveler template exists; audit: 100% of shipped-unit
serials link to a complete traveler. Gate: pack-out blocked on missing
traveler.
**Provenance:** R271; amended Rev 2.2 (nozzle ID / supplier-lot + cure
profile fields for the qualified-process options).

### MFG-037 — major
**Statement:** A 0.2 mm nozzle is a separately qualified process — the
0.4 mm qualification does not transfer. Before any ball printed with a
0.2 mm nozzle ships, that nozzle/process shall pass the full first-article
suite: diameter Ø40.0 ±0.3 mm, radial runout ≤0.15 mm, wall 1.2 ±0.15 mm
at ≥6 points, weight within the process mass window (MFG-038), mandrel
SQUAL mean ≥ the 0.4-baseline floor AND variance ≤20% per MECH-012 on the
Z-shim ladder, Z-seam ≤0.05 mm per MECH-046. Nozzle serial tracked in the
traveler; re-qualification required on nozzle change or after any clog
event.
**Rationale:** Same filament ≠ same process: flow rate, retraction,
thermal history, and wear rate all change with nozzle diameter, and finer
layers can resolve defects the 0.4 baseline never showed. Grandfathering
the qualification would certify a process that was never measured (R276).
**Validation:** Qualification record per nozzle serial with all
first-article measurements attached; SQUAL mean compared against the
0.4-baseline floor (fail = texture too fine for the sensor — fall back to
controlled microtexture per MECH-012, not hope). Gate: ship release
blocked for 0.2-printed balls without a passing qualification record.
**Provenance:** R276, R278.

### MFG-038 — major
**Statement:** 0.2 mm-nozzle lot controls: (1) per-ball mass check against
a process mass window (under-extrusion from a partial clog reads as low
mass — the ball can look perfect and be weak); (2) flow recalibration at
a fixed interval (every lot or N print-hours, whichever is first) to
catch nozzle wear; (3) chamber/enclosure temperature logged for the full
print (the 3–4× longer print is a thermal-drift risk for the ±0.3 mm
diametral budget); (4) any clog event scraps the in-progress ball and
forces nozzle re-qualification per MFG-037.
**Rationale:** The 0.2 failure modes are slow and invisible: partial clogs
produce a weak latitude band, wear drifts flow over a lot, and long
prints warp. Mass is the cheapest whole-ball integrity proxy; the
temperature log ties warp failures to a cause instead of a shrug (R277,
R279).
**Validation:** Mass window established at qualification; per-ball mass
recorded in traveler, out-of-window = scrap; flow-cal log per interval;
temp log per print reviewed on any dimensional failure. Gate: lot release.
**Provenance:** R277, R279.

### MFG-039 — major
**Statement:** Outsourced resin balls are a supplier-qualified process:
(1) supplier qualified once — sample lot passes dimensions (Ø40.0 ±0.1 mm
resin target, runout ≤0.10 mm), wall, TOUCH-004/007 on the production
resin, MECH-039 drop on tough-class resin, and tack-free cure check;
(2) every incoming lot inspected — dimensions, runout, wall, plus
post-cure stability: re-measure after 72 h settle at 23 °C and one
−10/+50 °C cycle, dimensional movement within tolerance or the lot is
rejected; (3) supplier's wash/cure profile locked and recorded per lot
on the traveler (MFG-036); (4) resin class restricted to tough/ABS-like —
standard brittle resins are rejected at qualification.
**Rationale:** Post-cure shrink is the signature outsourced-resin failure:
the ball passes inspection at receiving and keeps moving in the box and
in a hot truck. The 72 h re-measure catches the shrinkage the first
measurement misses; the tough-class gate keeps MECH-039's drop test
meaningful (R280, R283).
**Validation:** Supplier qualification record; per-lot incoming report
with both measurement passes; cure profile on traveler; drop test
re-run per process. Gate: kitting blocked on a failing incoming lot.
**Provenance:** R280, R283.

### MFG-040 — major
**Statement:** Resin formulation lock: the qualified resin (manufacturer +
product + formulation revision) is recorded at supplier qualification; no
unannounced formulation or resin-brand change is accepted — any change is
a new batch triggering full TOUCH-010 re-qualification before use. COA or
lot sheet filed per incoming lot.
**Rationale:** A silent resin swap (εr 2.8 → 3.4) shifts every touch
delta ~20% with zero dimensional signal; paperwork is the only upstream
tripwire, and TOUCH-010's coupon check is the downstream one. Both are
required because neither alone is sufficient (R281).
**Validation:** Formulation on file vs lot sheet match per incoming lot;
mismatch = new-batch re-qualification gate before kitting. Gate: kitting
blocked on undocumented formulation.
**Provenance:** R281.

### MFG-041 — minor
**Statement:** Single-supplier risk shall be retired before production:
either a second resin supplier qualified per MFG-039, or the in-house
0.2 mm FDM process held qualified per MFG-037/038 as a documented
fallback with a lead-time and capacity analysis on file.
**Rationale:** A sole supplier going dark halts the program; the fallback
must be qualified *before* it is needed, not improvised during an outage
(R282).
**Validation:** Second qualification record exists, or fallback analysis
document signed with a live qualification record for the fallback
process. Gate: production release.
**Provenance:** R282.

## KiCad DRC catalog (39)

### KICAD-001 — blocker
**Statement:** Global clearance shall be 0.20 mm: zero `Clearance violation`
`[clearance]`.
**Rationale:** The single cheapest net-to-net short guard; 0.20 mm is inside
any 2-layer fab capability and keeps the dense ball-flex routing honest.
**Validation:** DRC report asserts zero `[clearance]`; `.kicad_pro` audit:
`board.design_settings.rules.min_clearance == 0.20` (Board Setup → Design
Rules → Constraints).
**Provenance:** R206.

### KICAD-002 — blocker
**Statement:** Zero `Items shorting two nets` `[shorting_items]`.
**Rationale:** A hard short is a dead board; no threshold, no waiver.
**Validation:** DRC report asserts zero `[shorting_items]`.
**Provenance:** R206.

### KICAD-003 — blocker
**Statement:** Zero `Missing connection between items` `[unconnected_items]`.
**Rationale:** Unconnected items = open nets = dead functions; schematic
parity (`--schematic-parity`) makes this the netlist-truth check.
**Validation:** DRC report asserts zero `[unconnected_items]`.
**Provenance:** R206.

### KICAD-004 — major
**Statement:** Zero `Track has unconnected end` `[track_dangling]`.
**Rationale:** Dangling stubs are antennas and etch traps; every track end
terminates on a pad, via, or explicit test point.
**Validation:** DRC report asserts zero `[track_dangling]`.
**Provenance:** R206.

### KICAD-005 — major
**Statement:** Zero `Via is not connected or connected on only one layer`
`[via_dangling]`.
**Rationale:** A via on one layer is a drilling defect waiting to happen and
breaks return paths.
**Validation:** DRC report asserts zero `[via_dangling]`.
**Provenance:** R206.

### KICAD-006 — major
**Statement:** Global minimum track width 0.20 mm: zero `Track width`
`[track_width]` on Default-netclass copper.
**Rationale:** Etch yield floor for the base PCB; anything narrower is a fab
risk with no electrical need.
**Validation:** DRC report asserts zero `[track_width]` outside netclass
overrides; `.kicad_pro` audit: `rules.min_track_width == 0.20`.
**Provenance:** R206.

### KICAD-007 — blocker
**Statement:** COIL_TX netclass minimum track width 1.0 mm, enforced by
built-in `Track width` `[track_width]` (migrated from custom
`pwr_tx_coil_track_width`).
**Rationale:** Transmit-coil current needs the copper; a netclass minimum
maps exactly onto the built-in check — the custom rule added nothing
(R214).
**Validation:** DRC report asserts zero `[track_width]` on COIL_TX nets;
`.kicad_pro` audit: COIL_TX netclass `track_width >= 1.0`.
**Provenance:** R206, R214.

### KICAD-008 — major
**Statement:** Minimum via diameter 0.60 mm: zero `Via diameter`
`[via_diameter]`.
**Rationale:** Mechanical drill reliability + annular budget (KICAD-010);
smaller vias buy nothing on this 2-layer design.
**Validation:** DRC report asserts zero `[via_diameter]`; `.kicad_pro` audit:
`rules.min_via_diameter == 0.60`.
**Provenance:** R206.

### KICAD-009 — major
**Statement:** Minimum via drill 0.30 mm: zero `Hole size out of range`
`[drill_out_of_range]`. Microvia checks (`[microvia_drill_out_of_range]`,
`[microvia_diameter]`) are explicitly N/A — no HDI/microvias permitted;
their 0.30/0.10 mm reserved defaults stay only as a tripwire (any microvia
appearing fails loudly).
**Rationale:** One drill size = one fab process; the microvia tripwire
catches accidental HDI features from footprint imports.
**Validation:** DRC report asserts zero `[drill_out_of_range]` and zero
microvia IDs; `.kicad_pro` audit: `rules.min_via_drill == 0.30`.
**Provenance:** R206.

### KICAD-010 — major
**Statement:** Minimum via annular width 0.15 mm: zero `Annular width`
`[annular_width]` on vias.
**Rationale:** Drill breakout guard; pairs with KICAD-008 (0.60/0.30 via →
0.15 annular exactly).
**Validation:** DRC report asserts zero `[annular_width]` on vias;
`.kicad_pro` audit: `rules.min_annular_width == 0.15`.
**Provenance:** R206.

### KICAD-011 — blocker
**Statement:** J1 USB-C shield-leg annular width ≥0.50 mm, enforced by the
**custom** `mech_usbc_shield_annular` rule (built-in `[annular_width]`
cannot express a per-reference minimum — R213). Zero built-in
`[annular_width]` violations on J1 shield legs after the custom rule.
**Rationale:** MECH-006: pad lift on the shield legs is the #1 field-return
driver; 0.50 mm annular is the mechanical anchor. A global Board Setup
annular minimum would overconstrain ordinary vias.
**Validation:** Custom DRC run asserts zero `mech_usbc_shield_annular`
hits; `.kicad_pcb` audit: J1 shield-leg pad dimensions.
**Provenance:** R206, R213.

### KICAD-012 — major — PROVISIONAL (needs fab)
**Statement:** Minimum drilled-hole to drilled-hole spacing 0.25 mm: zero
`Drilled hole too close to other hole` `[hole_to_hole]`. (Empirically fired
at 0.50 mm probe setting; project value 0.25 mm proposed.)
**Rationale:** Drill-breakout between adjacent holes; 0.25 mm is the
proposed floor pending fab confirmation.
**Validation:** DRC report asserts zero `[hole_to_hole]`; `.kicad_pro`
audit: `rules.min_hole_to_hole == 0.25`.
**Provenance:** R206.

### KICAD-013 — major — PROVISIONAL (needs fab)
**Statement:** Minimum copper-to-drilled-hole clearance 0.25 mm: zero `Hole
clearance violation` `[hole_clearance]`.
**Rationale:** Mounting holes vs copper pour — breakout into a live pour is
a short. (Empirical note R209: 10.0.6 attribution can pair holes oddly on
synthetic boards; threshold itself verified.)
**Validation:** DRC report asserts zero `[hole_clearance]`; `.kicad_pro`
audit: `rules.min_hole_clearance == 0.25`.
**Provenance:** R206, R209, R212.

### KICAD-014 — major
**Statement:** Minimum copper-to-board-edge clearance 0.25 mm: zero `Board
edge clearance violation` `[copper_edge_clearance]`.
**Rationale:** Rout-bit and v-score keepout; copper at the edge delaminates.
**Validation:** DRC report asserts zero `[copper_edge_clearance]`;
`.kicad_pro` audit: `rules.min_copper_edge_clearance == 0.25`.
**Provenance:** R206.

### KICAD-015 — minor
**Statement:** Minimum silkscreen-to-silkscreen clearance 0.15 mm: zero
`Silkscreen clearance` `[silk_overlap]`.
**Rationale:** Legibility floor for designators; fired empirically between
a footprint reference field and overlapping board text.
**Validation:** DRC report asserts zero `[silk_overlap]`; `.kicad_pro`
audit: `rules.min_silk_clearance` (Board Setup → Constraints → Silk
clearance) `== 0.15`.
**Provenance:** R206.

### KICAD-016 — major
**Statement:** Zero `Silkscreen clipped by solder mask`
`[silk_over_copper]` — no silkscreen over any solder-mask opening.
**Rationale:** Ink on pads poisons solderability. No threshold exists; it is
a zero-tolerance check. (Empirical caveat R207: could not be triggered via
`kicad-cli` 10.0.6 on five geometries although the check exists in
`drc_item.cpp` and fires in the GUI — enforce at severity error and by
construction.)
**Validation:** Board Setup → Violation Severity: `silk_over_copper` =
error; DRC report asserts zero `[silk_over_copper]`; design review keeps
silk off pads.
**Provenance:** R206, R207.

### KICAD-017 — major
**Statement:** Zero `Courtyards overlap` `[courtyards_overlap]`.
**Rationale:** Courtyard overlap = pick-and-place interference; fired
empirically on overlapping synthetic footprints.
**Validation:** DRC report asserts zero `[courtyards_overlap]`; every
placed footprint carries a courtyard (KICAD-018).
**Provenance:** R206.

### KICAD-018 — major
**Statement:** Zero `Footprint has no courtyard defined`
`[missing_courtyard]`, except explicit documented mechanical-only
exemptions (mounting holes, fiducials).
**Rationale:** Supports KICAD-017; a missing courtyard silently opts a part
out of placement checking. **CLI trap (R208):** `kicad-cli pcb drc` lists
this check under "** Ignored checks **" by default — it must be enabled via
Board Setup → Design Rules → Violation Severity (≥ warning), persisted as
`rule_severities.missing_courtyard` in `.kicad_pro`, or validation silently
skips it.
**Validation:** `.kicad_pro` audit: `rule_severities.missing_courtyard` ∈
{warning, error}; DRC report shows the check NOT under "Ignored checks"
and zero `[missing_courtyard]`.
**Provenance:** R206, R208.

### KICAD-019 — blocker — PROVISIONAL (needs stackup)
**Statement:** USB90 differential-pair gap 0.15–0.25 mm, enforced by built-in
`Differential pair gap out of range` `[diff_pair_gap_out_of_range]` via a
KiCad 10 USB90 tuning profile.
**Rationale:** USB 2.0 signal integrity; the gap *maximum* is load-bearing
for impedance and a plain netclass gap is minimum-only (R210) — the tuning
profile carries the range. Fired empirically on a 0.10 mm gap vs 0.20 mm
configured.
**Validation:** `.kicad_pro` audit: USB90 tuning profile gap ∈
[0.15, 0.25]; DRC report asserts zero `[diff_pair_gap_out_of_range]`.
Recompute from frozen stackup before fab.
**Provenance:** R206, R210, R220.

### KICAD-020 — blocker — PROVISIONAL (needs stackup)
**Statement:** USB90 pair track width 0.20–0.30 mm, enforced by built-in
`Track width` `[track_width]` via the KiCad 10 USB90 tuning profile.
**Rationale:** Width and gap jointly set differential impedance; provisional
until the stackup (dielectric, copper weight) is frozen (R220).
**Validation:** `.kicad_pro` audit: USB90 tuning profile width ∈
[0.20, 0.30]; DRC report asserts zero `[track_width]` on USB90 nets.
**Provenance:** R206, R220.

### KICAD-021 — blocker — PROVISIONAL (needs stackup)
**Statement:** USB90 intra-pair skew ≤0.50 mm, enforced by built-in `Skew
between tracks out of range` `[skew_out_of_range]` via the USB90 tuning
profile (migrated from custom `hid_usb_diffpair_skew`).
**Rationale:** MECH-006 already budgets <0.5 mm length match; the built-in
check replaces the custom skew rule once the profile carries the limit.
(Caveat R218: not empirically triggered via CLI; ID from `drc_item.cpp`.)
**Validation:** `.kicad_pro` audit: USB90 tuning profile skew ≤ 0.50;
DRC report asserts zero `[skew_out_of_range]`.
**Provenance:** R206, R218, R220.

### KICAD-022 — minor — PROVISIONAL (needs fab)
**Statement:** Minimum solder-mask dam (bridge) width 0.10 mm: zero `Solder
mask aperture bridges items with different nets` `[solder_mask_bridge]`
(fired empirically 7× on a 0.05 mm-gap probe). Proposed global expansion:
`solder_mask_clearance` 0.05 mm global so fine-pitch areas get automatic
dams.
**Rationale:** A missing dam between nets = solder bridge = short; 0.10 mm
is the fab's minimum dam, provisional until fab freeze (R217).
**Validation:** DRC report asserts zero `[solder_mask_bridge]`; `.kicad_pro`
audit: `solder_mask_min_width == 0.10` (Board Setup → Design Rules → Solder
Mask).
**Provenance:** R206, R217.

### KICAD-023 — major
**Statement:** Zero `Thermal relief connection to zone incomplete`
`[starved_thermal]`; COIL_TX / high-current zones use 4-spoke thermals,
spoke width ≥0.50 mm, gap 0.30 mm. Explicit exception: J1 shield legs are
solid-connect, no thermals (MECH-006).
**Rationale:** Starved thermals on amp-class copper are cold joints;
(Caveat R218: not empirically triggered via CLI; ID from `drc_item.cpp`.)
**Validation:** `.kicad_pcb` audit: zone thermal settings (4 spokes,
≥0.50 mm, 0.30 mm gap); J1 shield pads solid-connect override; DRC report
asserts zero `[starved_thermal]`.
**Provenance:** R206, R218.

### KICAD-024 — major
**Statement:** Zero `Isolated copper fill` `[isolated_copper]` — remove
isolated islands below 0.5 mm² [est.] and require zero remaining
unintended islands.
**Rationale:** Floating copper is an ESD/antenna liability and a fab etch
nonuniformity source. (Caveat R218: not empirically triggered via CLI; ID
from `drc_item.cpp`.)
**Validation:** `.kicad_pcb` audit: zone island-removal settings; DRC
report asserts zero `[isolated_copper]`.
**Provenance:** R206, R218.

### KICAD-025 — blocker
**Statement:** Zero `Items not allowed` `[items_not_allowed]` — no copper
inside keepout areas (ball antenna keepout, touch-ring keepout).
**Rationale:** The built-in side of the RF keepouts; fired empirically when
a track crossed a keepout. Pairwise netclass-vs-keepout distances stay
custom (R215).
**Validation:** DRC report asserts zero `[items_not_allowed]`; `.kicad_pcb`
audit: keepout geometry present over the antenna and touch regions.
**Provenance:** R206, R215.

### KICAD-026 — major
**Statement:** `trackball.kicad_dru` shall contain ONLY constraints requiring
item, reference, or A/B-netclass selectors; everything expressible above
lives in Board Setup / netclasses / tuning profiles / board-local
properties.
**Rationale:** Custom rules are a maintenance liability — each one is a
place where KiCad's built-ins and the project can silently disagree. The
audit below is the enforcement of this rule.
**Validation:** The nine-rule audit: every KEEP-CUSTOM verdict cites the
selector that forces it; re-audit whenever a rule is added.
**Provenance:** R213–R216.

---

### KICAD-027 — major

**Statement:** ANT feed netclass track width is set per the 50 Ω stackup impedance calculation (width value documented with the stackup), enforced by the built-in `[track_width]` DRC on the ANT netclass — the built-in side of ELEC-028 (folded from KICAD-E03).

**Rationale:** A feed that is not 50 Ω reflects power and detunes the antenna; the netclass width is the layout expression of the stackup calc.

**Validation:** `kicad-cli pcb drc --output drc.json`; parse for ANT `[track_width]` violations → zero.

**Provenance:** R75 (KICAD-E03); merged per R247 (DEDUPE.md).

### KICAD-028 — major

**Statement:** SPI netclass track length ≤150 mm (PROVISIONAL) via the built-in track-length DRC constraint on the SPI netclass — the built-in side of ELEC-012 (folded from KICAD-E04).

**Rationale:** Length is the SI lever the layout can actually control; the 150 mm cap is the construction backstop for the ELEC-012 timing budget.

**Validation:** `kicad-cli pcb drc` — zero track-length violations on the SPI netclass.

**Provenance:** R75 (KICAD-E04); merged per R247 (DEDUPE.md).

### KICAD-029 — major

**Statement:** PTH mounting-hole annular ring ≥0.50 mm, enforced by the built-in `[annular_width]` check — the built-in side of ELEC-035 (folded from KICAD-E05). Distinct from KICAD-010 (via annular ≥0.15 mm): mounting holes carry mechanical load.

**Rationale:** A thin annular on a mounting hole cracks under screw torque; the check is cheap and the failure is a field return.

**Validation:** `kicad-cli pcb drc` — zero `[annular_width]` violations on PTH mounting holes.

**Provenance:** R75 (KICAD-E05); merged per R247 (DEDUPE.md).

### KICAD-030 — major

**Statement:** ERC: zero errors before any board order — `kicad-cli sch erc` — the built-in side of ELEC-020 (folded from KICAD-E08).

**Rationale:** ERC catches pin-contention and un-driven-net faults that no layout check can see; zero-errors is the release gate.

**Validation:** `kicad-cli sch erc --output erc.json` → zero errors (warnings reviewed).

**Provenance:** R75 (KICAD-E08); merged per R247 (DEDUPE.md).

### KICAD-031 — major — PROVISIONAL (coil current measurement)

**Statement:** COIL_RX netclass track width ≥0.5 mm [est.] (folded from KICAD-PWR-2) — the RX coil current is smaller than TX but still beyond signal-class widths.

**Rationale:** Undersized RX feed copper heats and drops the tank Q; the netclass width is the layout backstop.

**Validation:** `kicad-cli pcb drc` — zero `[track_width]` violations on COIL_RX.

**Provenance:** R111 (KICAD-PWR-2); merged per R248 (DEDUPE.md).

### KICAD-032 — major

**Statement:** VBUS netclass: track width ≥0.5 mm and clearance to other nets ≥0.25 mm (folded from KICAD-PWR-3) — the built-in side of PWR-007/ELEC-005's creepage concerns.

**Rationale:** VBUS is the highest-energy net on the base; width for inrush, clearance for the connector-adjacent fields.

**Validation:** `kicad-cli pcb drc` — zero width/clearance violations on the VBUS netclass.

**Provenance:** R111 (KICAD-PWR-3); merged per R248 (DEDUPE.md).

### KICAD-033 — major — PROVISIONAL (scripted check; native DRC has no proximity check)

**Statement:** The NTC thermistor footprint is within 4 mm [est.] of the component it protects (cell on the ball, TX coil/bridge on the base) — folded from KICAD-PWR-6, the scripted complement to CHG-004. Native KiCad DRC cannot check component proximity; this is enforced by a scripted layout check (Python parse of `.kicad_pcb` footprint positions).

**Rationale:** An NTC 20 mm from the cell measures the board, not the cell; CHG-004's temperature window is meaningless without the placement proof.

**Validation:** Scripted footprint-distance parse: every NTC centroid → protected-target centroid ≤4 mm [est.] (see VALIDATION_PLAN.md Stage 1).

**Provenance:** R111 (KICAD-PWR-6); merged per R248 (DEDUPE.md).

### KICAD-034 — major — PROVISIONAL (needs board layout)

**Statement:** A keepout zone on the base PCB excludes copper and components under/around the TX coil per the coil datasheet (folded from KICAD-PWR-7), enforced by the native `[items_not_allowed]` check against the zone object — same mechanism as KICAD-025.

**Rationale:** Copper in the TX field becomes a parasitic shorted turn; the zone is the layout expression of the coil's keepout.

**Validation:** `kicad-cli pcb drc` — zero `[items_not_allowed]` violations inside the TX coil zone.

**Provenance:** R111 (KICAD-PWR-7); merged per R248 (DEDUPE.md).

### KICAD-035 — major

**Statement:** TX coil terminal pads: annular ring ≥0.2 mm [est.] (folded from KICAD-PWR-8). The global via annular floor (KICAD-010, 0.15 mm) is via-class; the coil terminals carry TX current and need the wider ring.

**Rationale:** Thermal cycling on a thin annular at the coil terminals is a crack site; the check is free.

**Validation:** `kicad-cli pcb drc` — zero `[annular_width]` violations on the TX coil terminal pads.

**Provenance:** R111 (KICAD-PWR-8); merged per R248 (DEDUPE.md).

### KICAD-036 — major — PROVISIONAL (tank Vpk measurement)

**Statement:** Custom `elec027_coil_tx_creepage` in trackball.kicad_dru: COIL_TX vs every other net ≥0.8 mm (PROVISIONAL — scales with measured tank Vpk; ELEC-027). Custom because built-in clearance is a single blanket value: a conditional pair value for one aggressor net is not natively expressible.

**Rationale:** The TX tank voltage exceeds logic levels by an order of magnitude; a blanket clearance cannot be tightened for one net without punishing the whole board.

**Validation:** `kicad-cli pcb drc` with the project `.dru` loaded → zero violations of this rule.

**Provenance:** Task 4; ELEC-027 (R68).

### KICAD-037 — major — PROVISIONAL (coil current measurement)

**Statement:** Custom `elec030_spi_coil_tx_keepaway` in trackball.kicad_dru: SPI netclass vs COIL_TX ≥5 mm (PROVISIONAL). Implements ELEC-029 (renumbered from ELEC-030 after the ELEC-028 merge — the `.dru` rule name is frozen by Task 4). Custom because a pair-specific keepaway between two netclasses is not a blanket clearance.

**Rationale:** TX-coil switching noise into the sensor SPI is the dominant conducted aggressor on the base; the 5 mm keepaway is the layout backstop.

**Validation:** `kicad-cli pcb drc` with the project `.dru` loaded → zero violations of this rule.

**Provenance:** Task 4; ELEC-029 (R70).

### KICAD-038 — major — PROVISIONAL (needs board layout)

**Statement:** Custom `pwr_coiltx_board_edge` in trackball.kicad_dru: COIL_TX netclass kept ≥3 mm (PROVISIONAL) from the board edge (KICAD-PWR-5). Custom because native copper-to-edge clearance is global-only; a per-netclass keep-back needs a conditional rule. If the installed KiCad version rejects the `edge_clearance` constraint, enforce via the layout-review checklist (documented fallback).

**Rationale:** Field fringing at the TX coil near the board edge couples into the shell and the user's hand; the keep-back is the layout backstop.

**Validation:** `kicad-cli pcb drc` with the project `.dru` loaded → zero violations; fallback: checklist sign-off.

**Provenance:** R111 (KICAD-PWR-5); merged per R248 (DEDUPE.md).

### KICAD-039 — major

**Statement:** Custom `rf_ball_ant_to_rx_coil` in trackball.kicad_dru: ANT vs COIL_RX netclasses ≥8 mm (RF-022; the planar complement of the volumetric `blender/check_antenna_keepout.py` check). Custom because a pair-specific clearance between two netclasses is not a blanket clearance.

**Rationale:** The charging coil detunes the 2.4 GHz ball antenna when they share copper real estate; the planar rule is the fast DRC proxy for the 3D keepout.

**Validation:** `kicad-cli pcb drc` with the project `.dru` loaded → zero violations; Blender volumetric check passes.

**Provenance:** Task 4; RF-022 (R86).

## Integration (30)

Cross-subsystem rules. Each names the two or three subsystems whose
interface it governs; the validation always exercises the interface,
never one side alone. Added Rev 2.3 (R287–R298).

### INT-001 — blocker
**Statement:** The ball↔base ESB packet contract is defined once, in a
versioned interface spec (packet types, field layout, units,
sequence/ACK semantics, protocol version field). The base firmware's
parser is validated against a contract test harness that generates
packets from the spec — never from either implementation — plus
recorded ball output checked for spec conformance.
**Rationale:** Two codebases, one wire format: format drift desyncs the
stream, and each side unit-testing against its own copy of the format
cannot catch it (R287).
**Validation:** Harness generates ≥200 packets (valid, malformed,
fuzzed, version-skewed): parser accepts all valid, rejects all invalid,
and resynchronizes within one packet after garbage; a 60 s recorded
ball stream passes the conformance checker with zero violations.
**Provenance:** R287.

### INT-002 — major
**Statement:** Charging works in every ball power state: active, sleep,
DFU mode, and dead-battery (0 V). Base TX start is gated on analog
field-presence detection (LTC4125 autoresonant start), never on ESB
communication; the ball cold-boots from charger pre-charge. The full
state matrix (ball state × base TX behavior × LED behavior) is
documented.
**Rationale:** Gating TX on ESB creates a chicken-and-egg with a dead
battery: the ball can't announce, so the base never starts, so the
ball never charges (R288).
**Validation:** 0 V ball on the TX jig → MCU boots, LED green within the
CHG-007 latency budget, ESB announce follows; ball forced into DFU mode
still charges; sleeping ball charges without waking the radio (current
probe).
**Provenance:** R288.

### INT-003 — major
**Statement:** LED agreement contract: the ball LED reports measured
charge state only (green iff ICHG > threshold sustained, per CHG-007);
a base LED, if present, reports field-active/searching only — visually
distinct, and never labeled or readable as "charging." The contradiction
matrix (ball LED × base LED × measured ICHG) is tested.
**Rationale:** Marginal coupling makes the two honestly disagree; the
user must never read "charging" from the base while the ball is
honestly dark (R289).
**Validation:** Mis-seat matrix per CHG-002 with both LEDs logged vs
measured ICHG: zero cases of any base indication implying charging
while ICHG < threshold.
**Provenance:** R289.

### INT-004 — major
**Statement:** Base→ball DFU relay contract: the base holds the full
image and verifies its hash before starting; transfer is chunked with
per-chunk CRC and resume from the last good chunk; the ball verifies
the final image hash plus signature before honoring the swap command;
the base tracks the relay as an explicit state machine with
timeout/abort.
**Rationale:** A power cut mid-relay must not brick the ball or leave
the base believing the update succeeded (R290). FW-010 covers each
side's DFU; this rule covers the path between them.
**Validation:** Power-cut injection at 25/50/75% of relay, ×3 each:
ball always boots (old or new image, never partial); base reports
failure honestly; resume completes after power restore.
**Provenance:** R290.

### INT-005 — major
**Statement:** ESB air-time budget: ball transmit cadence at max rate
(touch frames + motion + fault frames) vs base RX servicing — measured
worst-case, the base never drops a packet to RX starvation while the
1 kHz fusion loop runs; packet loss under full load <1% [est.] at
operating distance.
**Rationale:** The radio and the fusion loop share the base MCU; load
on one must not starve the other (R291).
**Validation:** Max-rate ball traffic generator + 1 kHz fusion running
concurrently, 60 s: PER measured; logic analyzer shows the RX path
serviced within its deadline on every packet.
**Provenance:** R291.

### INT-006 — blocker
**Statement:** The base firmware's 1 kHz tick — SPI motion-burst reads
of both sensors + SQUAL-weighted fusion (FW-001) + HID report encode —
completes in ≤800 µs [est.] worst-case on the production clock
configuration, measured with ESB RX traffic at max rate running
concurrently.
**Rationale:** The tick budget is shared; calculation is not proof. An
overrun silently breaks the 1000 Hz HID contract (R291).
**Validation:** GPIO-toggle timing over 60 s worst-case load: PASS =
zero ticks >800 µs, zero dropped HID reports, fusion output verified
against the reference model.
**Provenance:** R291.

### INT-007 — blocker
**Statement:** Base power tree: LTC4125 TX drive + nRF52840 + both
sensors + USB enumeration fit within the USB port current limit
(500 mA for USB 2.0; provisional per the PWR-005 cable decision). TX
enable is sequenced after enumeration completes, with soft-start; the
simultaneous worst case (TX full + radio TX + both sensors + 1000 Hz
USB) is measured at the input.
**Rationale:** TX inrush during enumeration browns out the MCU
mid-handshake — the host sees a flapping device (R292).
**Validation:** Current probe on VBUS through the
enumerate→TX-enable sequence on a 500 mA-limited supply: PASS = VBUS
stays above the PWR-001 floor, zero MCU resets, enumeration completes
on the first attempt.
**Provenance:** R292.

### INT-008 — major
**Statement:** USB plug-in while the ball is docked and charging: the
base staggers power-up (MCU → enumerate → sensors → TX enable with
soft-start); the sequence is tested on a current-limited 500 mA port
with the ball parked dot-up on an already-running TX field.
**Rationale:** Inrush + TX start + MCU boot can blow the port budget
together and reset-loop forever: charge restarts, base resets, repeat
(R292).
**Validation:** 20 plug-in cycles docked-and-charging on a 500 mA
limited port: PASS = 20/20 enumerate cleanly, charging resumes without
a base reset, no USB re-enumeration storms in the host log.
**Provenance:** R292.

### INT-009 — major
**Statement:** LTC4125 switching edges must not corrupt base sensor SPI
transactions: scope-triggered test (TX SW edge vs SPI clock) shows no
bit errors; base firmware validates motion-burst status/CRC bits and
discards — never fuses — a corrupt sample.
**Rationale:** A rail droop too small to reset the MCU can still flip
one SPI bit: one corrupt motion burst reads as a phantom cursor jump,
only while charging (R292).
**Validation:** 10 min TX-on SPI capture: zero accepted corrupt bursts;
fault injection (single flipped SPI bit) → sample discarded, fused
output unaffected.
**Provenance:** R292.

### INT-010 — major
**Statement:** Ball schematic frequency plan: charger switching
frequency, touch-controller scan rate, and ESB channel are documented
with separation margins; any schematic/layout respin re-runs TOUCH-005
(simultaneous RX charging + radio TX at max duty, PER and touch-noise
measured).
**Rationale:** A layout respin can move the coupling that TOUCH-005
passed by luck; the plan makes the re-test mandatory, not optional
(R293).
**Validation:** Frequency-plan document in the repo; after any ball
PCB respin: TOUCH-005 re-run passes (noise ≤2× quiescent, delta/noise
≥5 under TX).
**Provenance:** R293.

### INT-011 — major
**Statement:** Full 0→100% charge with touch-baseline logging and the
radio streaming: no false touches during the thermal ramp, baselines
reconverge within the TOUCH-012 budget after charge completes, ESB PER
within 1 pp of the no-charge baseline.
**Rationale:** TOUCH-011/012 test static soaks; a real charge is a
dynamic 0–40 °C ramp with the charger switching and the radio on —
the combination the static tests miss (R293, ties FW-013).
**Validation:** Instrumented full charge ×3: touch event log vs ground
truth (zero false), baseline drift logged, PER compared charge vs idle.
**Provenance:** R293.

### INT-012 — minor
**Statement:** First-article ball (assembled, production shell + flex +
antenna) RSSI check: RSSI ≥ −70 dBm [est.] at 30 cm with a hand on the
ball, per qualified ball process; links the mechanical tolerance stack
(ball diameter, antenna keepout RF-022) to the RF link budget.
**Rationale:** Diameter tolerance moves the antenna relative to the
keepout boundary; the link budget must be verified on the as-built
article, not the CAD nominal (R293).
**Validation:** RSSI sweep per first article; PASS on all qualified
processes before the article clears Stage 3.
**Provenance:** R293.

### INT-013 — major
**Statement:** Recovery ladder, documented and tested per rung: (1) DFU
via ESB/USB with the shell shut; (2) SWD pogo with the shell opened
(V1 screwed shell — no glue, no destructive entry); bootloader entry
never depends on app code. V2's sealed-shell rung is defined before V2
ships.
**Rationale:** Pogo pads on the PCB are not recovery if the assembled
shell covers them; a DFU path whose entry depends on a working app
bricks on the first bad flash (R294, ties FW-010/FW-042).
**Validation:** Rung 1: 3/3 DFU on a screwed-shut ball with a
deliberately broken app; rung 2: pogo fixture mates and flashes with
the shell opened per the service procedure; bootloader entry
demonstrated with the app region erased.
**Provenance:** R294.

### INT-014 — major
**Statement:** Full host→ball DFU path: host → USB → base → ESB → ball,
with per-stage hash verification; the base never forwards an image it
has not fully received and verified; power-cut at each hop is tested.
**Rationale:** A USB disconnect mid-transfer can leave the base
holding a partial image that it later pushes to the ball — corrupting
a good ball from a good host (R294).
**Validation:** Power-cut/USB-disconnect at each of the four hops ×3:
ball never receives a partial image; base reports the failure stage
honestly; resume completes end-to-end after restore.
**Provenance:** R294.

### INT-015 — blocker
**Statement:** The base's HID report descriptor is the contract with
the host 3D-manipulation driver: the driver parses by descriptor, never
by fixed offsets; the base exposes a descriptor hash; the driver
refuses a mismatched descriptor with an explicit error — never a
silent misparse; any descriptor change bumps the driver interface
version.
**Rationale:** One added usage under offset-based parsing reads garbage
as finger count (R295).
**Validation:** Descriptor fuzzer (field insert/delete/resize ×100
mutations): parser accepts valid, rejects invalid with a clear error;
hash-mismatch test shows explicit refusal, not garbage data.
**Provenance:** R295.

### INT-016 — major
**Statement:** Raw telemetry channel (optical deltas + touch telemetry)
is versioned, with documented units, scaling, and sequence numbers;
the host application ships a conformance test fed by recorded base
output; counter/sequence wraparound is handled explicitly.
**Rationale:** int16 deltas at 1 kHz vs int32 at 500 Hz assumptions
collide at wraparound — the 3D app spins the model backwards once a
minute (R295).
**Validation:** Recorded-stream conformance test passes; wraparound
injection (forced sequence/counter rollover) handled with zero
glitches in the host app.
**Provenance:** R295.

### INT-017 — major
**Statement:** End-to-end latency budget, finger-down to host-driver
callback: partitioned across ball scan → ESB → base fusion → USB →
driver, each partition owned and measured; p99 total within the
TOUCH-019 budget; queueing between stages is measured, not assumed.
**Rationale:** Each team measuring only its slice misses the queues
between slices; the slices never add up on paper (R295).
**Validation:** Solenoid rig + USB capture + driver timestamps, 100
trials: p99 total within budget; per-partition measurements sum to the
observed total within 10%.
**Provenance:** R295.

### INT-018 — minor
**Statement:** Ball and base timestamp domains are defined: touch frames
carry ball-domain timestamps; the base translates to its domain with a
bounded skew (≤1 ms [est.]); skew beyond bound flags the frame
untrusted for velocity use.
**Rationale:** Fusing a touch timestamp from an unsynchronized domain
corrupts finger-velocity estimates (FW-005's correlator) silently
(R295).
**Validation:** Skew injection beyond bound → frames flagged, fusion
falls back to base-domain timing with no accuracy regression.
**Provenance:** R295.

### INT-019 — major
**Statement:** USB-C schematic checklist: CC Rp/Rd correct for the
PWR-005 power decision, SBU pins handled, shield grounded per ELEC-005
with TVS at the connector, and the composite device (HID mouse +
vendor 3D interface) coexists on Windows/macOS/Linux without the
vendor interface hijacking the HID mouse driver binding.
**Rationale:** Wrong CC config starves the TX coil; a composite
descriptor can make Windows bind WinUSB to the whole device and kill
the standard mouse (R296, ties HID-001/HID-003).
**Validation:** Schematic checklist signed + tri-OS plug test: mouse
works with no driver installed on all three OSes; vendor interface
binds only to the 3D driver.
**Provenance:** R296.

### INT-020 — major
**Statement:** Charger STAT (and FAULT) reaches the host: base firmware
routes charger state to the vendor HID interface; the host driver
exposes charging/not-charging/fault; the state agrees with the ball's
measured-state LED per the INT-003 matrix.
**Rationale:** Charging state that exists in silicon but dies in
firmware is a missing feature the premium UX benchmark assumes
present (R296).
**Validation:** Full mis-seat + fault matrix: host-reported state
matches measured ICHG and the ball LED in every case.
**Provenance:** R296.

### INT-021 — major
**Statement:** Click path latency budget: switch → GPIO → debounce →
HID report → USB → driver callback, partitioned and measured; p99
within the HID-021/FW-046 click budget; debounce algorithm choice is
justified against the budget, not by habit.
**Rationale:** 2 ms at the switch becoming 18 ms at the host means the
debounce + USB polling + driver queue ate the budget and nobody owned
it (R296).
**Validation:** Instrumented switch rig + USB capture + driver
timestamps, 200 clicks: p99 within budget; partition table in the
repo.
**Provenance:** R296.

### INT-022 — major
**Statement:** Per-unit calibration data flow (ELEC-007): the firmware
calibration routine writes the A-matrix/CPI scale to NVM atomically
(dual-slot + CRC + sequence, per FW-035) with a calibration version
stamp; boot loads it or falls back to factory-defaults flagged
"uncalibrated" to the host — never a half-valid matrix.
**Rationale:** A torn calibration write is worse than no calibration:
fusion runs on fiction with full confidence (R297).
**Validation:** Torn-write injection during calibration ×20: unit
always boots to CRC-valid calibration or explicit uncalibrated state;
host reads the calibration state correctly.
**Provenance:** R297.

### INT-023 — major
**Statement:** Socket wear triggers recalibration: firmware keeps a
rotation odometer; at the MECH-018 wear threshold the base flags
"recalibration recommended" to the host; CPI drift vs odometer is
characterized on the wear rig.
**Rationale:** PTFE pads wear, sensor Z grows, CPI drifts 4%, and the
user just thinks the mouse got "slow" — nobody re-runs ELEC-007
(R297).
**Validation:** Wear-rig run to threshold: odometer flag fires within
±20% of the characterized wear point; post-recal CPI back within
ELEC-007 limits.
**Provenance:** R297.

### INT-024 — major
**Statement:** SQUAL floor monitor: if either sensor's SQUAL sits at
the MECH-012 floor (texture too smooth, degraded, or contaminated),
fusion degrades explicitly — trust weight floored per FW-001, host
notified "low surface quality" — never silently fusing garbage with
full confidence.
**Rationale:** A 0.2-nozzle ball that's too smooth, or a worn ball,
holds SQUAL at the floor while the correlation peak jitters; silent
fusion turns that into cursor noise (R297).
**Validation:** Floor-SQUAL injection (defocused sensor / smooth test
ball): host notification fires, fused accuracy stays within the
degraded-mode bound, recovery when SQUAL returns.
**Provenance:** R297.

### INT-025 — major
**Statement:** Calibration is validated at the tolerance extremes: the
ELEC-007 procedure passes on min-diameter, nominal, and max-diameter
first articles; per-unit CPI error within limits on all three.
Mechanical tolerance × firmware calibration have a single owner.
**Rationale:** Calibrating on a nominal ball leaves field units at the
±0.3 mm extremes with a systematic CPI error nobody measured (R297,
ties MECH-045 and plan 3.1b).
**Validation:** 3.1b Z-ladder on all three diameter articles: PASS on
each before the calibration procedure is accepted.
**Provenance:** R297.

### INT-026 — major
**Statement:** Golden-unit interop matrix: a golden ball + golden base +
reference host driver must interop; any firmware change to either side
re-runs the full matrix (pairing, motion, touch, charging, DFU,
telemetry) before release.
**Rationale:** Production pairs ball FW v1.2 with base FW v1.1 while
the goldens were qualified on v1.0 — silent interop drift (R297).
**Validation:** Matrix checklist in the repo, re-run log per firmware
release; release blocked on a green matrix.
**Provenance:** R297.

### INT-027 — blocker
**Statement:** Cell/charger fault chain is end-to-end: a protection trip
or charger fault (CHG-005/CHG-026) → ball firmware detects within 1 s
[est.] via voltage/temperature anomaly or the CHG pin → ESB fault
frame → base halts TX and surfaces the fault → host driver shows an
explicit alert; the charging state machine cannot auto-resume.
**Rationale:** A protection FET opening while every layer still
reports "charging" is a silent safety failure (R298). Never waivable.
**Validation:** Injected secondary-protection trip on the bench: fault
visible at the host within 2 s [est.], TX halted, no auto-resume
without user action.
**Provenance:** R298.

### INT-028 — major
**Statement:** Protection vs firmware thresholds are coordinated with
margin: firmware low-battery halt and ship-mode entry sit above the
hardware secondary-protection trip points; ship-mode self-discharge
over 12 months [est.] cannot reach protection lockout; recovery from a
tripped protection state is demonstrated.
**Rationale:** A cell that self-discharges into protection lockout in a
warehouse becomes unrecoverable stock — pre-charge can't wake a pack
the protector has disconnected (R298).
**Validation:** Threshold stack-up document; accelerated
self-discharge test; tripped pack recovers on the charger per the
documented procedure.
**Provenance:** R298.

### INT-029 — major
**Statement:** Triple version handshake: ball firmware, base firmware,
and host driver each report (firmware/protocol/driver-interface)
versions at pair time and at USB connect; an incompatible combination
refuses with a clear host-visible message and a guided update path —
never silent misbehavior.
**Rationale:** Ball v2 + base v1 + driver v3 in the field: the v2
protocol field is misparsed by v1 with no handshake to catch it
(R298).
**Validation:** Version-matrix test (all supported × one-unsupported
combos): supported combos work, unsupported combos show the guided
error, zero silent misparses.
**Provenance:** R298.

### INT-030 — major
**Statement:** Ball error counters (FW-040) are aggregated end-to-end:
ball → ESB fault/counter frames → base → host driver diagnostics page,
with a documented schema; field failures are debuggable from the
host.
**Rationale:** Counters nobody reads are decoration; the first field
failure with no telemetry is a blind debug (R298).
**Validation:** Fault injection (dropout, corrupt SPI, brownout):
each increments the expected counter and is readable at the host
driver within 5 s [est.].
**Provenance:** R298.

## Fabrication gates (build-before-you-order)

- Custom-ball first article verified against the frozen ball spec (Ø40.0, runout, wall): gates MECH-002, MECH-004, MECH-011, MECH-012, MECH-034, MECH-045, TOUCH-003, TOUCH-009, TOUCH-010, TOUCH-032, CHG-002, CHG-036, RF-005, RF-006. First article is per qualified process — 0.2 mm-nozzle balls and outsourced-resin balls each get their own gate (MFG-037/039), never grandfathered from the 0.4 mm gate.
- 0.2 mm-nozzle process qualification (MFG-037/038: full first-article suite incl. SQUAL mean floor, per-ball mass window, flow-recal interval, thermal log) passes before any 0.2-printed ball enters Stage 3.
- Resin supplier qualification (MFG-039/040: sample-lot dimensions + stability + formulation lock) passes before the first outsourced lot is ordered; MFG-041 dual-source/fallback retired before production.
- Sensor part selected: gates MECH-001, ELEC-001, ELEC-012, ELEC-022, ELEC-031, ELEC-032→PWR-002.
- Coil LCR + tank Vpk measured: gates CHG-001, CHG-002, CHG-009, CHG-011, ELEC-027, ELEC-028, ELEC-030→ELEC-029, KICAD-036/037.
- Stackup frozen: gates ELEC-029→ELEC-028, KICAD-019/020/021 (USB90 tuning profile), KICAD-027/028.
- Touch coupon (ELEC-002) before flex tape-out; flex bend coupon before in-ball fold (MFG-005, MFG-011/012→MFG-010/011).
- Fab COC + first-article inspection before volume (MFG-003, MFG-004, KICAD-012/013/022).
- Golden units sealed before production (MFG-035→MFG-033, RF-015→RF-014).

## V1 exit criteria

- Zero unresolved **blocker** rules (67); all **major** rules (265) validated or waived with a dated owner; **minor** rules (56) tracked as known limitations.
- Regulatory pre-scan passed on production-representative units (RF-004); SAR evaluated if TX power requires it (RF-019→RF-018).
- The two killed originals stay dead: the <50 ms-from-first-touch hard gate (superseded by HID-021/FW-046) and the matte-black 'premium feel' mandate (killed R28 — untestable). Expansion kills stand: 51 candidates killed across the ten domains (see DEDUPE.md tally + R287/R290).
- No PROVISIONAL threshold ships without its named measurement (tank Vpk, coil LCR, custom-ball first-article dimensions, sensor part).
- Safety rules are never waivable: CHG-021/022/023/025/026/027/028 (cell + charger single-fault), ELEC-004/005/038 (ESD/shield), FW-016/034/035/037 (firmware safety), INT-027 (fault chain).
