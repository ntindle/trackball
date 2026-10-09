# Firmware handoff: S2_MOT relocation to SPI polling (Q6-A, owner-approved 2026-10-09)

## What changed in hardware
S2_MOT (U201 pin 38 ↔ U302 pin 9) is removed from the schematic and layout.
Both pins carry no-connect flags; no copper remains on the net. S1_MOT is
unchanged and remains the shared wake interrupt for both sensors.

## What firmware must do
Poll sensor-2 (U302, PMW3360) Motion register **0x02, bit 7 = MOT** at the
HID report rate over SPI (register map: docs/SENSOR_SELECTION.md §5).
A set MOT bit means sensor-2 saw motion since its last read; consume it the
same way the S2_MOT edge was consumed.

## Edge case: S2-only motion
Rotation about the S1 axis moves only sensor-2. Detection latency for this
case equals the poll interval (no async edge). S1_MOT still wakes the system
for all other motion. Bound the poll interval to keep this latency acceptable.

## SPI arbitration (design point)
Motion-register polls share the bus with motion-burst reads (0x50, up to 12
bytes per sensor per poll). Schedule the single-byte 0x02 poll of S2 inside
the existing per-report sensor-service transaction; independent NCS lines
per sensor (FW-003). No new hardware modes or rails are involved.

## Reversibility and risk
Fully reversible: re-add the two global labels + wire to restore the net;
zero copper risk (no pads, tracks, or vias reference S2_MOT on the board).
No layout, cost, or BOM impact.
