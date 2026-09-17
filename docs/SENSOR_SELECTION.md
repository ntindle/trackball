# Phase 1 — Optical Sensor Selection

**Date:** 2026-09-17
**Spec basis:** `~/workspace/trackball-final-spec/FINAL_SPEC.md` Rev 3.0 · DRC `~/workspace/trackball-drc/RULES.md` (358 rules, 286 adversarial rounds)
**Status:** Selection made with two explicit constraint deviations (see §8). No LCSC live stock could be verified on 2026-09-17 (see §9).

## Verdict (read this first)

- **Primary:** **PixArt PMW3360DM-T2QU** — best-documented protocol fit (SPI + SQUAL @ 0x07 + Motion_Burst @ 0x50), integrated IR LED, documented lens (LM19-LSI).
- **Fallback:** **PixArt PMW3389DM-T3QU** — same sensor family, newer; register-map compatibility assumed from family lineage, **must be verified against its datasheet before PCB layout**.
- **Hard finding:** every optical mouse sensor with a verified SPI + readable-SQUAL register map is a **through-hole DIP module** (industry-wide packaging convention — the molded DIP body carries the lens-alignment features and integrated LED). JLCPCB PCBA is SMT-only, so **no verified candidate can be JLCPCB-placed**. The build-kit "JLCPCB must place the sensor" constraint, taken literally, has zero satisfiable candidates. Recommended resolution in §8: hand-solder 2 units for V1 (10-minute job) and get the rest of the board from JLCPCB PCBA; or run full turnkey through PCBWay, which does place through-hole parts.
- **3.3 V finding:** only PAW3205DB-TJ3T (2.1–3.6 V) runs directly from 3.3 V among verified candidates. The PixArt gaming line (PMW3360/3389/3325) needs a dedicated ~1.9 V rail with I/O-voltage review. ADNS-3050 (2.8–3.0 V) needs an LDO from 3.3 V.

## 1. Primary: PMW3360DM-T2QU

| Item | Value (verified from LCSC-hosted datasheet) |
|---|---|
| Function | Optical gaming navigation sensor, IR LED integrated |
| Interface | 4-wire SPI (SCLK, MOSI, MISO, NCS) + MOTION interrupt |
| SQUAL | Register **0x07**, 8-bit unsigned image-quality metric — satisfies FW-001 |
| Motion burst | Register **0x50**, burst read of up to 12 register bytes — satisfies FW-003 (≥1 kHz) |
| Resolution | Up to 12,000 CPI (programmable) |
| Frame rate / speed | Up to 12,000 fps; 250 ips |
| Lift settings | 2 mm / 3 mm configurable |
| Supply | **1.8–2.1 V** (dedicated rail required; see §8) |
| Package | 16-pin molded lead-frame DIP, through-hole — **hand-solder or PCBWay THT** |
| Required lens | **LM19-LSI** (PixArt-specified) |
| SROM | Required — firmware must load SROM blob at init (store in base MCU flash) |
| LCSC product code | **C20612443** (code confirmed via LCSC-hosted datasheet URL; **stock NOT verified**, §9) |

Why it wins: it is the only candidate with *all three* firmware-critical features independently confirmed in a public register map — SPI, readable SQUAL, and a true motion-burst register. It is also the most widely cloned/community-supported sensor in the DIY trackball/mouse world (Ploopy and others), which de-risks bring-up.

## 2. Fallback: PMW3389DM-T3QU

Newer member of the same PixArt gaming family (16,000-CPI class). Same 16-pin DIP module format, integrated IR LED, SPI + SQUAL + motion-burst architecture by family lineage.

**Caveat:** its register map was **not** independently verified in this pass (no public full datasheet excerpt confirmed 0x07/0x50 on the 3389 specifically). Do not lay out a PCB for the 3389 until its datasheet's register map is checked against the 3360's. If it matches, it is a drop-in upgrade path (higher CPI headroom, same lens family).

## 3. Alternatives (evaluated)

### 3a. PMW3325DB-TWV1 — budget alternative
8-pin staggered DIP, 3-wire SPI, 1.8–2.1 V, 5,000 CPI, 100 ips / 20 g, IR LED integrated, 9.90 × 12.85 × 6.1 mm. Same PixArt register-map family (SQUAL/burst presumed, **not** independently verified). Pick if unit cost dominates and 5k CPI is acceptable for a Ø40 mm ball. Same DIP/voltage deviations as the primary.

### 3b. ADNS-3050 — closest-to-3.3 V alternative
8-pin staggered DIP, 4-wire serial (MISO/MOSI/SCLK/NCS). Verified register map: PROD_ID 0x00 = 0x09, MOTION 0x02, DELTA_X 0x03, DELTA_Y 0x04, **SQUAL 0x05** (named Image_Quality), configurable SQUAL threshold 0x1D. Supply **2.8–3.0 V** (single LDO from 3.3 V). Up to 2,000 CPI, 60 ips / 20 g.
**Deviations:** (1) no Motion_Burst register in its map (ends at 0x45) — FW-003's burst reads cannot be used; firmware would read Motion/Delta_X/Delta_Y/SQUAL as individual SPI transactions (4× bus cost per sensor per poll; still feasible at 1 kHz with EasyDMA, but margin is thinner). (2) External optics required: **ADNS-5110-001 lens** or ADNS-5120-002 trim lens + LED clip + **HLMP-EG3E** red LED (not integrated). (3) DIP through-hole.

### 3c. PAW3205DB-TJ3T — only verified 3.3 V-native sensor
Staggered DIP-8, serial interface (SDIO/SCLK). Verified: **Image_Quality (= SQUAL) @ 0x07**, Motion_Status 0x02, Delta_X/Y 0x03/0x04, **Quick-Burst (QB)** for fast motion readout. Supply **2.1–3.6 V** — runs directly from the 3.3 V rail, no extra regulator. 600/800/1000/1300/1600 CPI, 2,400 fps, 30 ips. Lens: PNLR-012RSI red-LED lens bundle.
**Deviations:** lowest performance envelope (30 ips / 2,400 fps may limit fast flicks on a 40 mm ball — validate against expected peak surface speed in Phase 2); DIP through-hole. Choose only if the dedicated 1.9 V rail is deemed unacceptable.

### 3d. ADNS-9800 — evaluated and REJECTED
Laser (VCSEL 832–865 nm) in a 16-pin chip-on-board package. Rejected: (a) listed **Obsolete** at Mouser; (b) laser adds IEC/EN 60825-1 eye-safety documentation burden for a device whose ball well is user-accessible; (c) COB is not JLCPCB-placeable either. Not a fallback.

### 3e. PMW3330DM-TZQU / PMW3310DH-AWQT — not verified, not recommended
Appear in distributor listings in the same family, but no register map, voltage, or lens data was confirmed in this pass. Do not select without the same verification applied above.

## 4. Datasheet links

```text
PMW3360DM-T2QU (LCSC-hosted, product code C20612443):
https://datasheet.lcsc.com/datasheet/pdf/c018c3e1d470821feefadd37e2f785d5.pdf?productCode=C20612443

ADNS-3050 (EPSGlobal-hosted PixArt datasheet):
https://www.epsglobal.com/Media-Library/EPSGlobal/Products/files/pixart/ADNS-3050.pdf?ext=.pdf

PAW3205DB-TJ3T (EPSGlobal-hosted PixArt datasheet):
https://www.epsglobal.com/Media-Library/EPSGlobal/Products/files/pixart/PAW3205DB-TJ3T.pdf

PMW3325DB-TWV1 (distributor product page; full datasheet via alldatasheet listing):
https://www.epsglobal.com/products/semiconductors/sensing-and-haptics/optical-navigation/gaming-navigation-chip-suitable-for-wired-wireless

PixArt official product list (package/variant cross-reference):
https://www.pixart.com/products-detail/tw/131/PAW3311DB-T2MU
```

## 5. Register maps (firmware-relevant)

### PMW3360DM-T2QU (verified)
| Addr | Name | Notes |
|---|---|---|
| 0x00 | Product_ID | expect 0x42 |
| 0x02 | Motion | bit 7 = MOT |
| 0x03 / 0x04 | Delta_X_L / Delta_X_H | 12-bit 2's complement |
| 0x05 / 0x06 | Delta_Y_L / Delta_Y_H | 12-bit 2's complement |
| **0x07** | **SQUAL** | 8-bit image quality — FW-001 weight source |
| 0x50 | Motion_Burst | up to 12 bytes: Motion, Observation, Delta_X_L/H, Delta_Y_L/H, SQUAL, RawData_Sum, Maximum_RawData, Minimum_RawData, Shutter_Upper/Lower |

FW-003 implementation: assert NCS, write 0x50, clock out 12 bytes, deassert NCS — one transaction per sensor per poll. At 1 kHz × 2 sensors with independent NCS lines and separate timer timestamps (FW-003).

### ADNS-3050 (verified)
| Addr | Name | Notes |
|---|---|---|
| 0x00 | Product_ID | 0x09 |
| 0x02 | Motion_Status | |
| 0x03 / 0x04 | Delta_X / Delta_Y | 8-bit 2's complement |
| **0x05** | **SQUAL** | named Image_Quality |
| 0x1D | SQUAL threshold | configurable floor — FW-001 zero-weight threshold |

### PAW3205DB-TJ3T (verified)
| Addr | Name | Notes |
|---|---|---|
| 0x00/0x01 | Product_ID1/2 | 0x30 |
| 0x02 | Motion_Status | |
| 0x03 / 0x04 | Delta_X / Delta_Y | |
| **0x07** | **Image_Quality** | = SQUAL |
| 0x0D/0x0E | Image_Threshold / Image_Recognition | |

## 6. Lens, standoff, and the MECH-002 reconciliation

- **Primary stack:** LM19-LSI lens mated to the PMW3360 DIP module. The DIP package's molded alignment features register the lens to the sensor — this is the industry-standard assembly and the reason the DIP form factor exists.
- **MECH-002 provisional target** (lens reference plane 2.4 ± 0.1 mm from ball surface) was written against a provisional lens. It must be **reconciled with the LM19-LSI's actual optical geometry**, not imposed blindly: the LM19-LSI defines its own sensor-to-surface distance for best focus. Procedure: (1) read the LM19-LSI mechanical drawing for its nominal object distance; (2) set the CAD nominal to that distance; (3) run the MECH-002 Z-shim ladder (2.0–3.0 mm in 0.1 mm steps) around it and verify SQUAL stays above floor and CPI stays within ±3% across the ±0.1 mm window; (4) if the LM19-LSI nominal differs from 2.4 mm, update MECH-002's target to the measured optimum and record the deviation.
- **MECH-022 datum chain** (ball center → sensor PCB → lens plane, ≤0.25 mm worst-case): the DIP's molded body + lens alignment features shorten this chain — sensor PCB top face → DIP shoulder → lens reference plane is a manufacturer-controlled stack. Document it from the PMW3360/LM19-LSI drawings in Phase 2 CAD.
- **MECH-021** (sensor-well axis tilt ≤1.5°): the through-hole DIP solders perpendicular to the PCB by construction; well tilt is controlled by the PCB mounting, not the sensor.
- **MECH-003** (optical axes 80–100°, target 90°): satisfied by base CAD placement of the two modules — sensor choice is agnostic. Each DIP's 16-pin footprint is large (~10.9 × 16.2 mm); verify both wells clear the Ø40 mm ball cradle in CAD.

## 7. DRC mapping

| Rule | How the selection satisfies it |
|---|---|
| MECH-001 (shell <1% transmission at illumination λ) | PMW3360 uses integrated **IR LED** — wavelength stays provisional until the datasheet's LED λ is read; shell dye must then be qualified at that λ. (PAW3205/ADNS-3050 alternatives use red LED — different λ, re-qualify.) |
| MECH-002 (Z target + shim ladder) | See §6 — reconcile 2.4 mm provisional target with LM19-LSI geometry; ladder test gates selection |
| MECH-003 (80–100° axes) | CAD placement; sensor-agnostic |
| MECH-004 (runout ≤0.15 mm; ripple <2% fused / SQUAL ripple <20%) | 12,000 fps + SQUAL-gated fusion (FW-001) gives headroom; validate on fixture |
| MECH-021 (well tilt ≤1.5°) | DIP through-hole solders square to PCB by construction |
| MECH-022 (datum chain ≤0.25 mm) | Manufacturer-controlled DIP-shoulder → lens stack; document from drawings |
| ELEC-007 (3-axis spin calibration) | See §10 |
| FW-001 (SQUAL-weighted fusion) | SQUAL @ 0x07 readable every burst — satisfied |
| FW-003 (≥1 kHz burst, separate timestamps) | Motion_Burst @ 0x50, one transaction/sensor/poll — satisfied |

New rules worth adding to the DRC library: (1) sensor supply rail rule — no sensor powered outside its datasheet VDD range (blocks the "just run the 3360 at 3.3 V" shortcut); (2) SROM rule — gaming sensors requiring SROM must have the blob stored in base-MCU flash with a version check at boot; (3) lens-bundle rule — sensor selection is invalid unless its manufacturer-specified lens is identified in the same selection pass.

## 8. Constraint deviations and power design

Two hard-constraint deviations are unavoidable with any verified SQUAL-capable sensor. Both are documented here rather than hidden.

### Deviation 1 — JLCPCB cannot place the sensor (build-kit constraint conflict)
All verified candidates are through-hole DIP modules; JLCPCB PCBA places SMT only. There is no verified QFN/SMD optical mouse sensor with a readable SQUAL register. **Resolution options:**
- **(a) Recommended for V1:** JLCPCB PCBA places everything except the two sensor modules + lenses; the builder hand-solders 2× 16-pin DIP + 2× LM19-LSI (a ~10-minute job, no hot air needed). The build kit's JLCPCB quote covers the rest of the board.
- **(b)** Full turnkey through **PCBWay**, which does place through-hole parts in mixed SMT+THT assembly — get the competing quote the build kit already requires and compare.
- **Do not** "solve" this by picking a sensor without verified SQUAL (breaks FW-001) or by assuming an SMD variant exists (none verified).

### Deviation 2 — PMW3360 is not a 3.3 V part
VDD = 1.8–2.1 V. **Power design:** dedicated 1.9 V rail for the two sensors (single low-noise LDO from the 3.3 V rail or USB 5 V; ~10 mA per sensor + IR LED current per datasheet). I/O: verify the PMW3360's SPI input thresholds against the nRF52840's 3.3 V outputs — if the sensor's inputs are not 3.3 V-tolerant, add level translation (or run the SPI bus at the sensor's VDD with a translator). **Do not power the sensor from 3.3 V.** If the extra rail is unacceptable, the fallback is PAW3205DB-TJ3T (§3c, native 3.3 V, lower performance) — a product decision, not a technical equivalence.

## 9. Procurement (LCSC/JLCPCB) — verified 2026-09-17

| Part | LCSC code | Stock 2026-09-17 |
|---|---|---|
| PMW3360DM-T2QU | **C20612443** (confirmed via LCSC-hosted datasheet URL) | **NOT VERIFIED** |
| LM19-LSI lens | — (no LCSC code confirmed) | **NOT VERIFIED** |
| PMW3389DM-T3QU | — | **NOT VERIFIED** |
| PMW3325DB-TWV1 | — | **NOT VERIFIED** |
| ADNS-3050 / ADNS-5110-001 / HLMP-EG3E | — | **NOT VERIFIED** |
| PAW3205DB-TJ3T / PNLR-012RSI | — | **NOT VERIFIED** |

**Explicit statement:** live LCSC stock could not be verified on 2026-09-17. Direct fetches of LCSC product pages fail from this environment (terminal — not retried), and public search does not reliably index LCSC product pages for PixArt sensors. The C20612443 code is proven only to *exist* as an LCSC product-code association (it appears in the LCSC-hosted datasheet URL); that is **not** evidence of stock, pricing, or JLCPCB PCBA-library membership. **Before any PCB order:** confirm C20612443 (sensor) and the LM19-LSI lens as in-stock, PCBA-eligible parts in the JLCPCB parts library from a live browser session, and confirm the lens is actually orderable (lenses are frequently non-stocked mechanicals — the most likely procurement failure point in this stack).

## 10. ELEC-007 calibration plan (fixture spin)

Per the DRC rule, after assembly and after any disassembly:

1. **Fixture:** mount the base in a 3-axis spin fixture that rotates the *ball* about three known orthogonal axes (e.g. precision gimbal or three orthogonal roller rigs) at known angular velocities. Ball surface must be the production-representative finish.
2. **Capture:** for each axis spin, log per-sensor (Δx, Δy, SQUAL) at ≥1 kHz via motion burst with 1 µs timestamps (FW-001/FW-003 path — calibrate through the production read path, not a side channel).
3. **Solve:** least-squares fit of the full **4×3 fusion matrix** (2 sensors × 2 axes → 3 ball angular-velocity components) plus **per-sensor scale factors**. Weight samples by SQUAL² (FW-001); discard below the SQUAL floor.
4. **Store:** matrix + scales + temperature/voltage at calibration → base MCU flash.
5. **Gate:** reject if per-sensor scale mismatch >5% (indicates mis-seating, wrong lens distance, or contaminated optics — reseat and re-run).
6. **Validate:** straightedge roll along one sensor's axis — residual off-axis counts must be <2% of on-axis counts. Also verify MECH-004 ripple: fused angular-velocity ripple <2% p-p/rev, SQUAL ripple <20% of mean.
7. **Re-run** after any disassembly (per rule).

## 11. Open questions for the parent / user

1. **Assembly route:** accept hand-soldered sensors (option a) or require PCBWay THT turnkey (option b)? This gates the build-kit's quote requests.
2. **Power:** accept the dedicated 1.9 V sensor rail, or direct that the design use PAW3205DB-TJ3T (native 3.3 V, lower performance) as primary instead?
3. **Fallback verification:** authorize a datasheet-verification pass on PMW3389DM-T3QU registers before Phase 2 CAD, or drop it as fallback in favor of PMW3325DB-TWV1 (cheaper, same deviations)?
4. **Lens procurement risk:** LM19-LSI availability is the weakest link — if it is not LCSC/JLCPCB-orderable, the selection must be revisited (ADNS-3050's ADNS-5110-001 has the same risk profile).
5. **Spec conflict noticed during this pass:** standing memory (2026-09-17) now says **no mechanical scroll wheel — scroll is modal** (button-held ball motion or two-finger ring gesture), which supersedes FINAL_SPEC §1.2's "mechanical detented scroll wheel." Unrelated to sensor choice, but the base PCB's button/encoder section needs reconciliation before schematic.
