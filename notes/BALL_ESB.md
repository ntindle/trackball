# Ball ↔ base ESB link design (ball side)

Matches the base-side contract (`notes/FW_HANDOFF_S2MOT.md`, `notes/PINMAP.md` on this branch): nRF52810 ball ↔ nRF52840 base, 2.4 GHz proprietary ESB-class, BLE reserved strictly for DFU. Base S2_MOT optical polling (PMW3360 reg 0x02 bit 7) is the base firmware job's problem — this design reserves the channel it needs (BASE_STATUS byte) and never touches pointer data (no IMU for pointer, per frozen spec).

## PHY/MAC

- nrf_esb-class: 2 Mbps, 32-byte fixed payloads, 5-byte address, 2-byte CRC16, auto-ACK + up to 3 retransmits, TX power 0 dBm (bench-TBD range check in-ball).
- Channels: data 2.440 GHz, fallback 2.480 GHz after 8 consecutive ACK losses; base commands the hop (ball obeys within 50 ms).
- Timing: 8 ms touch-report cadence while contact detected; 500 ms heartbeat otherwise (VBAT + flags only). Radio off between events (DCC-open deep-sleep budget, ELEC-023).

## Packet format (32 B, little-endian)

| Offset | Field | Notes |
|--------|-------|-------|
| 0 | `PKT_TYPE` | 0x01 TOUCH, 0x02 STATUS, 0x03 DFU_CTRL, 0x04 DFU_CHUNK, 0x7E ACK |
| 1 | `SEQ` | wraps; ACK echoes SEQ |
| 2–3 | `BASE_STATUS` | reserved for the S2_MOT/base-firmware channel (this job: keep zero, do not repurpose) |
| 4 | `FLAGS` | bit0 contact, bit1 two-finger (valid only if ELEC-002 passed → else forced 0), bit2 RING_SCROLL_ENABLE echo, bit3 CHRG, bit4 FAULT, bit5 DFU_ARMED |
| 5 | `VBAT_50MV` | cell voltage / 50 mV (ADC via 1M/330k divider, ELEC-023) |
| 6–7 | `TEMP_C16` | NTC-derived, 1/16 °C (provisional curve — bench-TBD) |
| 8–31 | payload | TOUCH: 24× 8-bit deltas T00–T23 (geometry A) or 16× T + pad (geometry B); DFU_CHUNK: 24 B image data + offset in bytes 8–11 |

## DFU relay (FW-010 ball side)

1. Base sends DFU_CTRL ENTER_DFU (with image size + CRC32). Ball ACKs, reboots into MCUBoot, listens BLE briefly on every reset per frozen spec.
2. Base relays the image as DFU_CHUNKs over ESB (24 B each); ball writes to the secondary slot, verifies CRC32, sets test-flag, reboots.
3. Ball reports DFU status in STATUS FLAGS bit5 + VBAT field reused as error code on failure; bad image → MCUBoot rejects → old image runs (screwed-shut ball never bricks: bootloader-on-every-reset is the recovery path).
4. Direct BLE DFU (phone/laptop) also honored; ESB relay and BLE DFU are mutually exclusive per boot (first claimant wins).

## Scroll gating

`RING_SCROLL_ENABLE` (bit2) is a base-commanded flag stored in ball NVS: ball computes two-finger state only when ELEC-002 passed AND the flag is set; otherwise byte 4 bit1 reads 0 and the payload carries single-contact data (SCROLL_UX Method B stays dark until the coupon says otherwise).
