# Scroll + Gesture UX Design — Ultimate Mouse Trackball
**Rev 1.1 — 2026-09-17.** Status: user-approved contract (no scroll wheel, dead by user direction 2026-09-17). This document is the normative UX definition; DRC rules UX-001…UX-013 enforce it.

## 0. Contract (normative)

Scroll is **modal**, with exactly two methods. There is no scroll wheel, no scroll ring, no capacitive strip.

- **Method A — button-held scroll (primary, always available).** Hold the scroll button → ball motion maps to scroll vectors, cursor frozen. Works with zero touch-ring capability.
- **Method B — two-finger ring scroll (secondary, gated).** Two fingers sliding on the capacitive touch ring → scroll/zoom. Available only if the ELEC-002 coupon proves reliable 2-finger disambiguation; otherwise firmware-disabled and Method A is the complete UX.

## 1. Physical controls

Three physical buttons, no wheel:

| Button | Position | Tap | Hold |
|---|---|---|---|
| Left | below ball equator, thumb/index side | left click | left drag |
| Right | below ball equator, opposite side | right click | right drag (context) |
| **Scroll** | front-center, between L/R | **middle click** | **scroll mode** |

The scroll button is the mode key for Method A. Its cap is tactilely distinct (concave dish vs convex L/R) so it is identifiable blind.

## 2. State machine (firmware, base MCU)

### 2.1 States

- **POINT** (default): ball rotation → cursor deltas (FW-001 fusion). Touch ring → tap clicks per FW-006.
- **SCROLL_BTN**: entered on scroll-button press edge (FW-008 debounce). Cursor deltas forced to zero. Ball rotation → scroll vector accumulator.
- **SCROLL_RING**: entered when two ring contacts exhibit ball-frame slide (see §3). Cursor frozen. Slide velocity → scroll vector.
- **SCROLL_LATCH**: opt-in sticky variant of SCROLL_BTN (see §5). Entered/exited by tap toggle.

Transitions out of any SCROLL state: the engaging condition releases (button up / fingers lift or stop), or a 150 ms [est.] link-dropout forces all-up (FW-007). **Mode engagement is strictly level-triggered** — firmware never latches scroll on except in the explicitly configured SCROLL_LATCH mode. On boot/reset, state = POINT, all buttons up (FW-034).

### 2.2 Tap-vs-hold disambiguation (scroll button)

On scroll-button press edge: enter SCROLL_BTN **immediately** (cursor freezes at once — no cursor jump later). Start a decision window:

- If released with press duration < 200 ms [est.] **and** total ball motion during the press < 8 counts [est.] → emit **middle click** (press+release), no scroll vectors emitted.
- Otherwise → it was a scroll session: emit accumulated scroll vectors, **no click**.
- Left/right clicks during SCROLL_BTN pass through as clicks (cursor stays frozen). This preserves chords (e.g. Ctrl+click style combos) without leaving scroll mode.

Rationale: freezing the cursor at press time (rather than at hold-timeout) eliminates the "cursor jumped then froze" artifact and makes tap-vs-scroll a pure post-hoc classification, exactly like tap-to-click vs drag on a touchpad.

### 2.3 Scroll vector mapping (Method A)

- Ball X-axis rotation → horizontal scroll; ball Y-axis rotation → vertical scroll (natural-scroll direction configurable; default follows OS convention).
- Gain: scroll units per ball count, default 1:1 with the fused CPI [est.], acceleration curve configurable via the gesture map (FW-033). Vectors accumulate at the 1 kHz report cadence and are emitted as HID wheel + AC Pan reports on IF0 and as raw int16 vectors on IF1.
- On exiting SCROLL_BTN: the accumulator is **cleared, never flushed** — no catch-up scroll burst after release.

### 2.4 Timing constants (all [est.], tunable via gesture map)

| Constant | Value | Purpose |
|---|---|---|
| `SCROLL_TAP_MS` | 200 ms | tap = middle click below this |
| `SCROLL_TAP_COUNTS` | 8 counts | tap motion budget |
| `RING_SLIDE_MIN` | 10°/s ball-frame | slide detection floor |
| `RING_SCROLL_IDLE_MS` | 120 ms | fingers stopped → exit SCROLL_RING |
| `LATCH_IDLE_MS` | 15 s | latch exits on idle (Auto Scroll pattern) |
| `MODE_INDICATE` | host cursor | mode feedback channel |

## 3. Two-finger ring scroll (Method B) — ball-frame vs world-frame

**The load-bearing definition.** The touch ring rotates *with* the ball. Two fingers rolling the ball normally keep their contacts fixed in the ball frame while the ball frame itself rotates — this is **not** scroll. Two fingers *sliding across the ring surface* change their contact azimuth in the ball frame — this **is** scroll.

- The ball MCU reports per-contact centroids in **ball frame** (azimuth, contact size) at the touch report rate.
- The base computes ball angular velocity (from FW-001 fusion) and derives each contact's **slide velocity** = contact velocity in world frame − ball surface velocity at the contact point. Equivalently: `d(azimuth_ballframe)/dt`.
- `|slide| > RING_SLIDE_MIN` coherently for both contacts (same tangential direction within 30° [est.]) for > 40 ms [est.] → enter SCROLL_RING. Slide direction maps to scroll direction (tangential slide ≈ vertical scroll; this is a 1D ring — see §4).
- Exit: either contact lifts, slide drops below floor for `RING_SCROLL_IDLE_MS`, or coherence breaks.
- **Two-finger tap** (contacts appear and release with < `RING_SLIDE_MIN` motion and < `SCROLL_TAP_MS` duration) = **right click** — consistent with FW-006's settled-count rule.
- **One finger sliding on the ring = explicit no-op.** Single-finger slides happen constantly during normal rolling; they must never scroll and never click.
- **Precedence:** while the scroll button is held (SCROLL_BTN active), ring-slide detection is **suppressed** — Method A wins deterministically. No double-scroll, no mode fight.

## 4. Pinch / zoom

Two contacts whose **angular separation changes** while each contact's individual slide stays below floor = pinch gesture. Separation velocity → zoom vector (emitted on IF1 as raw zoom; on IF0 as Ctrl+wheel, configurable). Secondary gesture; disabled under the same ELEC-002 gate as Method B.

## 5. Scroll latch (sticky) mode — accessibility / one-handed use

Opt-in via the gesture map (FW-033), default off. When enabled:

- Tap scroll button = toggle SCROLL_LATCH on/off (no hold required).
- Middle click moves to left+right chord (configurable).
- **Exit paths (any of):** scroll-button tap, left/right press, 15 s idle countdown from last ball movement (Auto Scroll pattern), USB suspend, vendor-OUT "drop mode".
- The vendor IF exposes latch state; the host driver shows persistent mode indication.
- Rationale: hold-while-rolling needs two digits of one hand; latch mode makes scroll fully one-finger operable and covers limited-dexterity users. Kensington's stuck-modal history is why the exit paths are enumerated, not single.

## 6. Mode indication (anti-confusion)

Mode confusion ("why is my cursor dead") is the #1 UX risk of modal scroll. Three layers:

1. **Host cursor**: the driver switches to a scroll cursor (all-scroll / directional) whenever any SCROLL state is active, driven by the IF1 mode-flags byte. This is the primary channel.
2. **Vendor IF telemetry**: mode flags on every IF1 report (bit0 = SCROLL_BTN, bit1 = SCROLL_RING, bit2 = SCROLL_LATCH) — scriptable, OSD-able.
3. **No-cursor-jump guarantee**: cursor freezes at mode entry and resumes exactly where it was; scroll vectors never leak into cursor deltas (UX-010).

## 7. Host software contract

### 7.1 Interface 0 (boot HID mouse) — compatibility path

Report descriptor declares **Wheel + AC Pan** (in addition to buttons/X/Y). Scroll vectors → standard wheel units:

- Vertical: HID `Wheel` usage with **Resolution Multiplier** (Windows 10+ honors hi-res wheel; descriptor declares it).
- Horizontal: `AC Pan`.
- Scaling default: 120 units (one WHEEL_DELTA) per `SCROLL_NOTCH_COUNTS` ball counts [est., tunable]. No driver needed on any OS.

### 7.2 Interface 1 (vendor 0xFF00) — precision path

- Raw scroll vector: int16 LE X/Y per 1 ms report, plus int16 zoom.
- Mode-flags byte (§6).
- The reference host daemon (HID-004) maps these to: virtual 6-DOF/space-mouse-style output, OSC/WebSocket for Blender/CAD, and per-application profiles (SpaceMouse-style app-specific mappings live here, not in firmware).

### 7.3 OS notes

- **Windows**: WHEEL_DELTA = 120 per notch; hi-res wheel via Resolution Multiplier descriptor item; "scroll inactive windows" works with standard wheel reports.
- **macOS**: "Natural" vs traditional scroll direction is an OS-level inversion applied to wheel reports — respected automatically; the gesture map also offers an explicit invert for the vendor path.
- **Linux**: libinput consumes REL_WHEEL / REL_WHEEL_HI_RES; no special handling.

## 8. CAD implications (buttons)

- Scroll button front-center, inside the thumb's natural reach arc while index/middle fingers rest on the ball (MECH-049). Larger cap than L/R (Ø12–14 mm [est.]) for comfortable sustained hold; top surface **0.5 mm [est.] recessed** below L/R caps to resist brush-presses during aggressive rolling.
- ≥8 mm lateral clearance from the ball surface maintained (MECH-008 applies to all three buttons).
- Cap force: same switch class as L/R (0.6–0.9 N); hold fatigue is managed by cap size, not by a stiffer switch (a stiffer switch would break click-feel consistency vs the $300 benchmark).
- `blender/check_buttons_usb.py` updated: wheel geometry/check removed; third "scroll" button added with reach-envelope, recess, and clearance checks.

## 9. Fallback (ELEC-002 gate)

If the flat touch coupon fails to prove reliable 2-finger disambiguation:

- Firmware build flag `RING_SCROLL_ENABLE = 0`: Method B and pinch compiled out; SCROLL_RING state unreachable; ring remains tap-click only (or tap-disabled — configurable).
- Method A must be a **complete** scroll UX alone: the full validation matrix (UX-015) runs with the flag both on and off.
- This is not a degraded mode — it is a supported configuration. The decision is recorded at the Phase 1 coupon gate.

## 10. What we stole / avoided (from research)

**Stolen from 3Dconnexion SpaceMouse:**
- Per-application profiles with automatic switching (active profile always displayed) → HID-033 daemon app profiles. Never silently overwrite user customizations (a real SketchUp complaint).
- State legibility triad (hardware LED + on-screen display + audio cues) → UX-009's three-layer indication (host cursor + IF1 flags + base LED pulse).
- Zoom direction as a first-class user setting (users genuinely disagree) → explicit invert in gesture map + OS-level natural-scroll respected.
- Multi-axis default over dominant-axis lock (users prefer simultaneous pan+zoom) → UX-003 default.
- Application-dependent scroll feel (detented in CAD, smooth + inertia in documents, cf. CadMouse Smart Scroll) → lives in daemon app profiles, not firmware.

**Avoided:**
- SlimBlade twist-to-scroll precision complaints → twist stays dead; the user's two-method contract.
- Shapr3D-style exit hysteresis (~1–2 s max-deflection to break a lock made users feel the device was broken) → our mode exit is instantaneous on release (level-triggered); the only hysteresis is the 120 ms ring-idle timeout, disclosed and configurable.
- Hidden modal states with no indication → UX-009.

**Stolen from Kensington / TrackballWorks:**
- evdev Wheel Emulation Timeout model (the community's hold-to-scroll recipe): press = click if released within the timeout, hold = scroll mode, timeout 0 = immediate. Our UX-002 (200 ms / 8 counts) is this model with stated constants.
- Kensington chord rule #1 ("if the chord isn't fully qualified, individual buttons behave normally") → UX-002's post-hoc classification: unqualified press = middle click, never nothing.
- Auto Scroll's 15 s idle countdown (slight motion holds, normal motion changes direction, any button cancels) → UX-008 latch exit paths.
- Omni-directional modal scroll (ball X/Y → wheel axes 6/7 + 4/5) → UX-003 multi-axis mapping.
- Speed + inertia + orientation sliders, per-application profiles → FW-033 gesture map + HID-033 daemon profiles.
- SlimBlade's audible per-tick clicks ("reassuring... easy single-line moves") → UX-013 synthesized tick feedback.

**Avoided (Kensington's bug history is the textbook):**
- Same-surface twist without an explicit mode (SlimBlade's core failure: firmware guesses intent, guesses wrong) → twist stays dead; mode is always explicit (button held).
- Invisible latched modes (SlimBlade Media/Document buttons, old click-to-latch scroll) → UX-008's enumerated exit paths + UX-009 indication.
- Stuck modals: stuck chord keys, missed button-up in debounce, Auto Scroll surviving app-switch → R297: every scroll state has ≥2 exit paths; suspend forces POINT.
- Scroll stealing drag state (SlimBlade Photoshop bug: scroll dropped the in-progress drag) → UX-002 preserves the drag underneath scroll entry.
- Featherweight accidental engagement (classic Orbit ring's light touch → accidental scrolls) → MECH-049 recess + deliberate two-finger gesture (UX-005) + brush-press classification (UX-002).
- Overshoot with no slow end (Orbit "slowest setting still too fast") → UX-003 precision gain floor + inertia control.

**Kensington/TrackballWorks research:** full notes in `trackballworks-research.md` (this directory).
