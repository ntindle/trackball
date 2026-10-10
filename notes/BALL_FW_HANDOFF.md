# BALL_FW_HANDOFF.md — ball firmware notes (nRF52810, ball side)

Owner-approved pin changes the firmware MUST honor (2026-10-10):

1. CHRG↔FAULT remap (Q13a): P0.05 reads FAULT (was CHRG), P0.06 reads
   CHRG (was FAULT). Both are charger open-drain status inputs with 10k
   pull-up to +3V0 (ELEC-018, CHG-006/007). Invert/handling unchanged —
   only the pin assignment moved. TP9=CHRG, TP10=FAULT unchanged.
2. NRESET open + TP7 DNP (Q10a): no firmware RESET control; rely on
   internal pull-up, MCUBoot DFU (listens briefly every reset), and dock
   power-cycle for bricked-bootloader recovery.
3. `RING_SCROLL_ENABLE` kept (Method B gated on ELEC-002 coupon; do NOT
   assume it passes — SCROLL_UX_DESIGN.md).
4. DFU: MCUBoot + SMP-over-BLE; base sends "enter DFU" over ESB and may
   relay images (FW-010 ball side). Bad-image rejection required on the
   screwed-shut ball.
5. ESB protocol + BASE_STATUS reservation: see notes/BALL_ESB.md and
   base notes/FW_HANDOFF_S2MOT.md (register 0x02 bit 7 is the base
   firmware job's problem; ball side reserves the channel).
