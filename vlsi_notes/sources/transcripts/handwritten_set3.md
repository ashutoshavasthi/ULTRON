# Transcript: handwritten notes, set 3 (sent 2026-11-18)

## `class_notes/Vlsi-MOS29-09.pdf` (14 pages)
Pages 1–7 repeat set B pages 1–7 (MOS capacitor, MOSFET structure, types, biasing, I = Q·v), with small additions:
- **p.6:** cut-off mode adds I_D = 0 A. VDS shown +ve. "(Enhancement) For operating nMOS: VDS → +ve, VGS → +ve. For operating pMOS: VGS → −ve, VDS → −ve."
- **p.7:** adds "VDS↑ at a fixed VGS, VDS,sat = VGS − Vth".

**p.8:** I_D derivation as in B8, boxed as Eq.① I_D = μn Cox (W/L)[(VGS − Vth)VDS − VDS²/2]. *Effect of VDS:* as VDS↑, VDS,sat = VGS − Vth (saturation voltage) ⇒ I_D = I_D,max = constant, independent of VDS.

**p.9:** For I_D,max: dI_D/dVDS = 0 (sketch: I_D rises to I_D,max at VDS,sat for fixed VGS). Substituting VDS,sat into I_D gives **I_D,max = μn Cox (W/L) · ½ (VGS − Vth)²**. *Effect of VGS:* curves for VGS = 2 V and 4 V; higher VGS gives a higher plateau. **Regions-of-operation table** (Region | biasing | channel | drain current | physical meaning):
1. Cut-off: VGS < Vth | no channel | I_D = 0 | MOSFET off.
2. Sub-threshold: VGS ≤ Vth | weak inversion | I_D ∝ exp((VGS − Vth)/(n VT)), n = ideality factor | very small current flows.

**p.10:** Family of I_D–VDS curves (VGS2 > VGS1) with VDS,sat marked. Regions on one curve: ① deep-triode, ② linear, ③ non-linear, ④ saturation. *In deep-triode & linear:* VDS small ⇒ VDS²/2 negligible ⇒ **I_D = μn Cox (W/L)(VGS − Vth)·VDS** (Eq.②) ⇒ **R_on = VDS/I_D = 1/[μn Cox (W/L)(VGS − Vth)]**: on-resistance, a voltage-variable resistor (changed via VGS).

**p.11:** table continued.
3. Deep-triode / linear: VGS > Vth, VDS < VGS − Vth | strong inversion, channel formed | Eq.② | voltage-variable resistor.
4. Non-linear: VGS > Vth, VDS < VGS − Vth | strong inversion | I_D = μn Cox (W/L)[(VGS − Vth)VDS − VDS²/2] | non-linear.
5. Saturation: VGS > Vth, VDS ≥ VGS − Vth | strong inversion, pinch-off of channel | I_D = I_D,max | ideal current source.

Sketch: Ex along the channel (longitudinal), Ey into the substrate (transverse). For long-channel devices **Ex ≪ Ey**; Ex ∝ VDS/L, Ey ∝ VGS/tox.

**p.12:** **Device scaling.**
1. Constant electric field: Ex = VDS/L → (VDS/2)/(L/2); Ey = VGS/tox → (VGS/3)/(tox/3). Scale voltages and dimensions by the same factor so E stays constant.
2. Constant voltage scaling (generally used).

**Short-channel / second-order effects:**
1. **Body effect:** sketch of S, G, D, p-substrate, B. nMOS: body → most −ve potential; pMOS: body → most +ve potential. As V_B (source-to-body reverse bias) ↑, Vth ↑: the body effect.

**p.13:**
2. **Channel-length modulation (CLM):** as you decrease the channel length, Ex increases (Ex = VDS/L) and I_D ∝ 1/L. In saturation the curve slopes up: **I_D = μn Cox (W/L) ½ (VGS − Vth)² (1 + λ VDS)**, λ = CLM parameter, **V_A = 1/λ**.
3. **Velocity saturation:** Vd vs E saturates at Vd,sat. In short-channel devices E is very high, so saturation happens much earlier than in long-channel devices (sketch: long- vs short-channel Vd–E). Long-channel: VDS,sat = VGS − Vth, Vd = μE.

**p.14:** Short-channel: **Vd = μE/(1 + E/Ec)** for E < Ec (Ec = critical field where velocity saturates); Vd = Vd,sat for E > Ec. Long-channel: I_D = μn Cox (W/L){(VGS − Vth)VDS − VDS²/2}. Short-channel: **I_D = μn Cox (W/L){(VGS − Vth)VDS − VDS²/2} × 1/(1 + VDS/(Ec L))** (the notes write VDS/Ec; with E = VDS/L the dimensionally correct form is VDS/(Ec·L)).
4. **Punch-through:** source and drain depletion regions overlap ⇒ I ≠ 0 even when the device should be off.
5. **Drain-induced barrier lowering (DIBL):** as VDS↑, Vth↓.

## `class_notes/VLSI-1-10-26.pdf` (2 pages, dated 1-10-26) and the two photos
**CMOS inverter.** Pull-up network → pMOS, pull-down network → nMOS. Structure: M2 = pMOS (S to Vdd), M1 = nMOS (S to GND); gates tied to Vin, drains tied to Vout; C_load at Vout. nMOS enhancement: VGS +ve, VGS > Vth. pMOS enhancement: VGS −ve (p+ S/D in n-sub).
- Case 1: Vin = 0 V → M2 ON, M1 OFF → Vout = VDD (logic 1).
- Case 2: Vin = VDD → M1 ON, M2 OFF → Vout = 0. "Static CMOS technology."
- **Switch model:** (i) Vin = 0: pMOS = resistor Rp from VDD to Vout charging C_L, nMOS open. (ii) Vin = VDD: pMOS open, nMOS = resistor Rn discharging C_L. "You can calculate the time-constant" (τ = Rp·C_L or Rn·C_L).
- **Static behaviour:** (i) zero static power dissipation, (ii) high input impedance, (iii) low output impedance.
- **VTC:** plot of Vout vs Vin, from VDD down to 0; it crosses the Vout = Vin line at **Vm, the switching threshold**.
- (Photo only) Gain Av = dVout/dVin = 100; for ΔVin = 10⁻³ V, ΔVout = 100 × 10⁻³ = 0.1 V.
