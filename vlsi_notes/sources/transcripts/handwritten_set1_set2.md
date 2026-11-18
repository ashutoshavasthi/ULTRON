# Transcript: handwritten notes, sets 1 and 2

Made on 2026-09-29 while reading the original scans page by page. The scans themselves are no longer on disk (see `../../SOURCES_AND_INTENT.md` §3a), so this transcript is the record of their content.

- **A** = `vlsi_notes_till_engineers_day_2026.pdf` (36 pages)
- **B** = `vlsi_notes_after_engineers_day_till_24926.pdf` (8 pages)

Notation: `^` is a power, `_` a subscript.

## Set A

- **A1:** Header: VLSI. Discrete & integrated circuit; SSI, MSI, LSI, VLSI; process. Unit-1: intro to semiconductor materials, crystal structure, types of semiconductor, doping & carrier concentration | PN junction diode, BJT, MOSFETs. Semiconductor: conductivity can be tuned by many orders of magnitude. Applications: switch, amplifier, logic device, LED/solar cells/photodetectors, electronics industry. Elemental SC (Si, Ge). Compound SC (GaAs, GaN).
- **A2:** Energy bands: VB, CB, bandgap. Metals (VB/CB overlap), insulators (Eg very large), semiconductors (Eg smaller). Formation of bands: carbon atom Z=6, 1s2 2s2 2p2 (1s: 2 states, 2s: 2 states, 2p: 6 states). Discrete levels → band of energies.
- **A3:** N atoms of C: 6N states (2p) with 2N e; 2N states (2s) with 2N e; total 8N states, 4N electrons. E-vs-r diagram: 2s and 2p bands split, merge, re-split; lower band 4N states / 4N e (VB), upper 4N states empty (CB). Bandgaps: Si 1.1 eV, Ge 0.7, GaAs 1.34, GaN 3.4. Thermal energy kBT, kB = 1.38e-23 J/K; at 300 K E = 300×1.38e-23/1.6e-19 = 25.87 meV.
- **A4:** E–k diagram. time →(FT)→ frequency; real space (cm) →(FT)→ reciprocal space (cm^-1); λ → k = 2π/λ (wave vector). ħk = ħ·2π/λ = h/λ = p. KE = ½mv² = p²/2m ⇒ E = ħ²k²/2m.
- **A5:** Parabola for a free electron. Crystal lattice: gaps at k = ±π/a, ±2π/a. E = ħ²k²/2m*, m* effective mass. dE/dk = ħ²k/m*; d²E/dk² = ħ²/m*; m* = ħ²/(d²E/dk²): incorporates band-structure information; curvature of the E–k diagram.
- **A6:** Q: semiconductor 1 (m* = 0.2 m0) vs semiconductor 2 (m* = 0.06 m0), values struck out; plot 1 drawn with higher curvature. "Which has higher current density?" → (1) higher curvature, lower m*, higher mobility, higher current density; (2) lower curvature, higher m*, lower mobility. Hole: absence of an electron, modelled as a +ve charged particle, always moves in the VB; mh*, me* effective masses. Eg = lowest CB level − highest VB level. Direct-bandgap sketch.
- **A7:** Direct: GaAs, GaN. Indirect: Si, Ge (CB minimum not at k=0; exciting e from VB to CB needs a momentum change; phonons = atomic vibrations (heat)). Fermi–Dirac f(E) = 1/(1+exp((E−Ef)/kBT)); Ef = Fermi level (imaginary construct), 50% occupation. 1−f(E) = hole probability. At T=0 K: E=Ef → ½; E<Ef → 1; E>Ef → 0. Plot at T=0 and T>0.
- **A8:** T=0 K: all states below Ef filled, above empty. Density of states g(E): number of states per unit energy per unit volume. n = ∫_Ec^∞ g(E) f(E) dE. Gap 1.1 eV vs thermal 26 meV. Ef positions: intrinsic mid-gap (n=p), n-type near Ec (n>p), p-type near Ev (p>n).
- **A9:** More doping: Ef moves toward CB (n-type) / VB (p-type). Doping: n-type = pentavalent (P); p-type = trivalent. Dopant concentration in atoms/cm³. Donor → +ve immobile ion. Ed just below Ec; Ea just above Ev. Slope in Ef ⇒ current flowing. Slope in Ec, Ev ⇒ electric field exists.
- **A10:** Intrinsic n=p; n-type n>p, ND+; p-type p>n, NA−. Mass-action law: at equilibrium np = ni², constant at given T, independent of doping. Charge neutrality p + ND+ = n + NA− ⇒ n² + n(NA−ND) − ni² = 0 ⇒ n = [−(NA−ND) ± √((NA−ND)² + 4ni²)]/2.
- **A11:** Strongly n-type: n ≈ ND, p = ni²/ND. Strongly p-type: p ≈ NA, n = ni²/NA. **Q1:** T=300 K, occupation probability at E = Ef ± 0.1 eV → 1/(1+46.81) = 2.09%; 1/(1+0.0213) = 97.9%.
- **A12:** **Q2:** plot f(E) at T = 0, 200, 300 K. Charge transport, case 1 (no excitation): random thermal velocity, collisions with (i) lattice (phonons), (ii) impurity ions (Coulomb); net current 0.
- **A13:** Case 2 (E field): drift current. v = a·τ, a = qE/m*, τ = mean time between collisions ⇒ Vd = (qτ/m*)E, slope μ. mh* > me* ⇒ μn > μp.
- **A14:** Mobility vs T: phonon μ falls with T; ionised-impurity μ rises with T; 1/μ_total = 1/μ_phonon + 1/μ_II; μ_total is bell-shaped.
- **A15:** J_drift = (nqμn + pqμp)E = σE (A/cm²). Vd vs E: linear (low E), saturates at v_sat (high E; acceleration up but scattering up). Diffusion: current due to concentration gradient; for decreasing p(x), holes and hole current go +x; for decreasing n(x), electrons go +x and electron current −x.
- **A16:** Jn = qDn dn/dx; Jp = −qDp dp/dx. Einstein: Dn/μn = Dp/μp = kT/q = VT ≈ 25.9 mV. Recombination via trap states (e capture / e emission); SRH U = (1/τ)(pn − ni²)/(p + n + 2ni).
- **A17:** Equilibrium: np = ni², U=0. Non-equilibrium: p = p0 + Δp, n = n0 + Δn. n-type U = Δp/τ, p-type U = Δn/τ (minority lifetime should be high). **Q:** n(x) = n0 + Ax, A = −5e15 cm^-4, μn = 1200 → Jn = 1.6e-19 × 25.9e-3 × 1200 × (−5e15) = −248.64e-4 A/cm². **Q:** p-type Si p = 5e15, ni = 1e10, μp = 450, μn = 1350 → conductivity.
- **A18:** σ = q(nμn + pμp), n = 2e4 → σ ≈ 0.36 S/cm. **Q3:** n-Si bar 2 μm, 1 V, ND = 1e16, μn = 1350: (a) Vd = 6.75e6 cm/s, (b) t = 2.96e-11 s, (c) J = 1.08e4 A/cm², (d) resistance and current for 0.25 μm² (I ≈ 27 μA, R ≈ 37 kΩ).
- **A19:** P–N junction diode: anode–[P|N]–cathode, metal contacts. Open circuit: holes + immobile acceptors (−) on p, electrons + immobile donors (+) on n. Diffusion current: holes p→n, electrons n→p; diffusion current direction p→n.
- **A20:** Depletion region (no free carriers), Q− on p, Q+ on n, field n→p, barrier potential. Drift current due to minority carriers, direction n→p = Is. Equilibrium: I_diffusion = I_drift = Is.
- **A21:** V0 = VT ln(NA ND/ni²). W = xn + xp; |Q+| = |Q−|; if NA > ND then xp < xn.
- **A22:** |Q+| = qA xn ND, |Q−| = qA xp NA ⇒ xn/xp = NA/ND. W = √((2εs/q)(1/NA + 1/ND)V0), εs(Si) = 1.04e-12 F/cm. xp = W ND/(NA+ND), xn = W NA/(NA+ND).
- **A23:** QJ = Aq(NA ND/(NA+ND))W = A√(2εs q (NA ND/(NA+ND)) V0). Band diagram: flat Ef, bands bend. E = −dV/dx, Ec = −qV ⇒ E = (1/q) dEc/dx.
- **A24:** Bias: reverse (W↑), forward (W↓) sketches with Is and ID arrows.
- **A25:** Barrier V0+VR (reverse, I_drift > I_diff), V0−VF (forward, I_diff > I_drift). W and QJ with (V0+VR). I–V derivation: barrier ↓, majority diffusion, minority injection; np = np0 + Δn(x).
- **A26:** pn = pn0 + Δp(x). pn(xn) = pn0 e^{V/VT}; excess pn0(e^{V/VT} − 1); np(−xp) = np0 e^{V/VT}. Diffusion lengths Ln, Lp. pn(x) = pn0 + pn0(e^{V/VT}−1) e^{−(x−xn)/Lp}; similarly for np(x).
- **A27:** Jp(xn) = q(Dp/Lp)pn0(e^{V/VT}−1); Jn(−xp) = q(Dn/Ln)np0(e^{V/VT}−1). I = Aq ni²(Dp/(Lp ND) + Dn/(Ln NA))(e^{V/VT}−1) = Is(e^{V/VT}−1). Drift carries the current in the quasi-neutral regions.
- **A28:** I–V curve: V=0 → 0; reverse → −Is; forward exponential. Breakdown: Zener (strong field breaks bonds, VBR < 5 V), avalanche (high-KE collisions, VBR > 8 V). **Q:** NA = 1e18, ND = 1e16, A = 1e-4 cm², ni = 1.5e10, Lp = 5 μm, Ln = 10 μm, Dp = 10, Dn = 18, ID = 0.1 mA: find Is, V, hole and electron components.
- **A29:** Is = 7.26e-15 A; V = 0.605 V; Ip/In = (Dp/Dn)(Ln/Lp)(NA/ND) = 111 ⇒ Ip = 0.0991 mA, In = 0.0009 mA.
- **A30:** **Assignment:** Si vs Ge diode, which needs a higher voltage for 20 mA? ni ∝ e^{−Eg/2kT}; Eg,Si > Eg,Ge ⇒ ni,Si < ni,Ge ⇒ VSi > VGe.
- **A31:** Ef constant ⇒ no current; slope in Ec, Ev ⇒ field. Transistor applications: switch, logic gates, memory, amplifiers. FET (field at C controls A–B current: MOSFET, MESFET, MISFET) vs junction transistor (current injected at C: BJT, HBT). BJT pnp drawing with EBJ, CBJ.
- **A32:** npn band diagram at equilibrium. Modes: FB/RB active, FB/FB saturation, RB/RB cut-off. Configurations CE (in B–E, out C–E), CB (E–B, C–B), CC (B–C, E–C).
- **A33:** Base current replaces holes lost to recombination (IB,rec). Input char. (output V constant), output char. (input I constant). Table: CE IB–VBE (VCE), IC–VCE (IB); CB IE–VEB (VCB), IC–VCB (IE); CC IB–VBC (VEC), IE–VEC (IB). Active npn: IEn ①, IEp ② (not useful), IE = IEn + IEp, IB,rec ③, ICn ④, IBC,rev ⑤ (neglected).
- **A34:** Base transport factor B = ICn/IEn ≈ 1; emitter injection efficiency γ = IEn/(IEn+IEp) ≈ 1; α = ICn/IE = B·γE; β = IC/IB.
- **A35:** β = α/(1−α). Base width as small as possible; IEn ∝ (Dn/Ln)(ni²/NA), IEp ∝ (Dp/Lp)(ni²/ND) ⇒ base lightly doped, emitter heavily doped. Metallurgical base width (initial) vs neutral base width (where recombination happens).
- **A36:** Base-width modulation & Early voltage: ideal flat IC–VCB; practical lines slope up and extrapolate to −VA.

## Set B

- **B1:** MOS → MOSFETs → CMOS (complementary MOSFETs). MOS capacitor: MIM C = ε0A/d constant; MIS: C depends on VG. ① VG −ve: metal −Qm, holes accumulate (+Qs) in the p-type SC → accumulation.
- **B2:** ② VG small +ve: depletion of immobile ions, Qs = −qNA w; Cox and Cdep. ③ VG large +ve: minority electrons (mobile) + depletion ions (qNA wm) → inversion (p to n).
- **B3:** w depletion width, wm maximum. Cox = εox/tox (bias independent); Cs = εs/w (bias dependent); 1/C = 1/Cox + 1/Cs. C/Cox = 1 in accumulation, falls to Cmin at w = wm (VG = Vth), then frequency-dependent rise.
- **B4:** nMOS: electron current; pMOS: hole current; unipolar. MOSFET as a switch: very high speed, low power. Terminals S, D, G, B. Questions: turn-on VG? RON? speed τ = RC? Structures: nMOS on p-sub with n+ S/D; pMOS with p+ S/D.
- **B5:** n-well process. Types: nMOS/pMOS; enhancement (normally OFF, no channel) vs depletion (normally ON, channel exists). Four combinations listed.
- **B6:** Biasing: nMOS source GND, VGS, VDS +ve, substrate GND or −ve; pMOS VGS, VDS −ve, substrate to highest potential. Operation: VGS ≤ 0 → cutoff; VGS = VTH → channel (onset of inversion). Vertical E = V/tox.
- **B7:** I = Q·v. W/L aspect ratio. Overdrive VGS − VTH. Q′ = W Cox(VGS − VTH). With VDS: (VGS − Vth − V(x)). Pinch-off: thinning of inversion charge due to V(x) and encroachment of depletion layer.
- **B8:** Q = W Cox(VGS − Vth − V(x)); Vd = −μ dV/dx; integrate 0→L, 0→VDS ⇒ ID = μn Cox (W/L)[(VGS − Vth)VDS − VDS²/2]. (End of set B.)
