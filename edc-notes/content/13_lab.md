# Chapter 19: The lab: BJT characteristics (your circuit photos)

*Sources: your three circuit photos (BC547 set-ups and the hand-drawn “self-bias with bypass capacitor”)*

::: kid What are we actually doing?
In lectures the transistor is a symbol and some equations. In the lab we **measure** it. We turn two knobs (an input voltage and an output voltage), read three or four meters, and draw two graphs that show how the transistor really behaves: the **input characteristic** (how much base current flows for a given base voltage) and the **output characteristic** (how much collector current flows for a given collector voltage). These are exactly the curves used in the load-line pictures of Chapters 16–17.
:::

## 19.1 The transistor: BC547

The BC547 is a small-signal **NPN silicon** transistor in a TO-92 plastic case. <span class="tag">extra</span> Typical data (check your data sheet): $V_{CEO}\approx45$ V, $I_{C,max}\approx100$ mA, $P_{D}\approx500$ mW, $h_{FE}$ roughly 110–800 depending on the letter suffix (A/B/C). With the flat face towards you and the legs down the pins are usually **C – B – E** from left to right. **Always confirm the pin-out on the data sheet before wiring.**

## 19.2 Circuit 1 (photo 1): output characteristic with a fixed base current

{{fig c_lab_bc547|Photo 2 redrawn: the standard CE characteristics test bench with four meters (µA, V$_{BE}$, mA, V$_{CE}$). Both $V_{BB}$ and $V_{CC}$ are variable supplies.|92}}

Photo 1 is the simplest version of the same experiment: a **fixed 5 V source $V_1$** feeds the base through **$R_1$ (470 kΩ or 1 MΩ)**, and a **variable 0–15 V supply $V_2$** feeds the collector through **$R_2=1\ \text{k}\Omega$**, with an **mA meter** in the collector path and a **voltmeter** across the transistor.

* **Fixed base current:** $I_B=\dfrac{V_1-V_{BE}}{R_1}$.
  * $R_1=470\ \text{k}\Omega$: $I_B=\dfrac{5-0.7}{470\text{k}}=\mathbf{9.15\ \mu A}$
  * $R_1=1\ \text{M}\Omega$: $I_B=\dfrac{5-0.7}{1\text{M}}=\mathbf{4.3\ \mu A}$
* Sweep $V_2$ from 0 to 15 V, record $I_C$ (mA) and $V_{CE}$ (V). The two runs give **two curves of the output family**: $I_C$ rises steeply for $V_{CE}$ below about 0.3 V (saturation), then flattens (active region) at $I_C\approx\beta I_B$.
* Sanity check: with $\beta=200$, $I_B=9.15\ \mu$A ⇒ $I_C\approx1.8$ mA in the flat part; for $I_B=4.3\ \mu$A ⇒ about 0.86 mA.
* The load line of the 1 kΩ resistor: $V_{CE}=V_2-I_C(1\text{k})$.

## 19.3 Circuit 2 (photo 2): full input and output characteristics

Components: $R_B=100\ \text{k}\Omega$ (protects the base), $R_C=1\ \text{k}\Omega$, **µA meter** in the base circuit, **mA meter** in the collector circuit, voltmeters for $V_{BE}$ and $V_{CE}$, two variable supplies $V_{BB}$ and $V_{CC}$.

### A. Input characteristic ($I_B$ vs $V_{BE}$ at constant $V_{CE}$)
1. Set $V_{CC}$ so that $V_{CE}$ = a fixed value (e.g., 0 V first, then 5 V). Keep readjusting $V_{CC}$ so $V_{CE}$ stays fixed (the meter reads $V_{CE}$ **at the transistor**, not the supply).
2. Increase $V_{BB}$ in steps; note $V_{BE}$ (V) and $I_B$ (µA) each time.
3. Plot $I_B$ (y) against $V_{BE}$ (x). Expect a diode-like curve with a knee near 0.6–0.7 V.
4. **Dynamic input resistance:** $r_i=\dfrac{\Delta V_{BE}}{\Delta I_B}\Big|_{V_{CE}}$ (from the steep part).

### B. Output characteristic ($I_C$ vs $V_{CE}$ at constant $I_B$)
1. Set $V_{BB}$ to give a chosen $I_B$ (e.g., 20 µA); keep $I_B$ constant.
2. Vary $V_{CC}$ (0 → 12 V); note $V_{CE}$ and $I_C$.
3. Repeat for $I_B=40,60,80\ \mu$A.
4. Plot $I_C$ (y) vs $V_{CE}$ (x): a family of curves like the figure in Chapter 16.
5. **Output resistance:** $r_o=\dfrac{\Delta V_{CE}}{\Delta I_C}\Big|_{I_B}$ (the slope’s reciprocal; large). **AC current gain:** $\beta_{ac}=\dfrac{\Delta I_C}{\Delta I_B}\Big|_{V_{CE}}$. **DC gain:** $\beta_{dc}=I_C/I_B$.

| $I_B$ (µA) | $V_{CE}$ (V) | $I_C$ (mA) | $\beta=I_C/I_B$ |
|---|---|---|---|
| 20 | 0.2, 0.5, 1, 2, 5, 8, 10 | ... | ... |

### Points to remember
* **Never** connect the base to a supply without $R_B$ (or the base current will destroy the transistor).
* Keep $I_C<$ the rated maximum; watch power $V_{CE}I_C$.
* Meters have their own resistance: use the µA meter in series with the base only.

## 19.4 The hand-drawn circuit (photo 3): self-bias with bypass capacitor

The sketch shows an NPN transistor with **$R_B$ from $V_{CC}$ to the base**, **$R_C$ in the collector**, an **input coupling capacitor $C_b$**, an **output coupling capacitor $C_c$**, and **$R_E$ in parallel with a bypass capacitor $C_e$** at the emitter. It is exactly the circuit of §17.2 (dc) and §18.4 Case 1 (ac, bypassed). Your annotations “N P N” and “c, b, e” label the layers and terminals.

* **DC:** capacitors open ⇒ $I_B=\dfrac{V_{CC}-V_{BE}}{R_B+(\beta+1)R_E}$, $V_{CE}=V_{CC}-I_C(R_C+R_E)$.
* **AC:** $C_e$ shorts $R_E$ ⇒ $Z_i=R_B\parallel\beta r_e$, $Z_o\approx R_C$, $A_v=-R_C/r_e$.

## 19.5 Viva questions

::: try Chapter 19 questions
1. Why do we use $R_B=100$ kΩ in the base circuit?
2. Why is $V_{BE}$ about 0.6–0.7 V?
3. What does the horizontal-ish part of the output curves tell you?
4. How is $\beta$ obtained from the curves?
5. Why must $V_{CE}$ be kept constant while plotting the input characteristic?

<details markdown="1"><summary>Answers</summary>

1. To limit the base current (the base–emitter junction is a forward-biased diode) and to allow fine control of $I_B$ with a coarse voltage source.
2. It is the forward voltage of the silicon base–emitter diode (knee at 0.6–0.7 V).
3. In the active region $I_C\approx\beta I_B$ almost independent of $V_{CE}$: the transistor acts as a current source controlled by $I_B$; the small slope is the Early effect ($r_o$).
4. $\beta_{dc}=I_C/I_B$ at a point, or $\beta_{ac}=\Delta I_C/\Delta I_B$ between two adjacent curves at fixed $V_{CE}$.
5. $I_B$ depends (slightly) on $V_{CE}$; fixing it isolates the $V_{BE}$–$I_B$ relation.
</details>
:::

# Chapter 20: One-page formula sheet {.chap}

## Diodes
| Quantity | Formula |
|---|---|
| Thermal voltage | $V_T=T/11600\approx26$ mV (300 K) |
| Diode equation | $I=I_0(e^{V/\eta V_T}-1)$; Ge $\eta=1$, Si $\eta=2$ |
| Temperature | $I_{02}=I_{01}2^{(T_2-T_1)/10}$; cut-in voltage ↓ with $T$ |
| Static / dynamic resistance | $R_{dc}=V/I$; $r_{ac}=\Delta V/\Delta I=\eta V_T/I$ |
| Transition capacitance | $C_T=K/(V_B-V)^n$ |
| Diffusion capacitance | $C_D=\tau I/(\eta V_T)$ |
| Zener | $P_{DZ}=V_ZI_Z$, $I_{ZM}=P_{ZM}/V_Z$, $r_Z=\Delta V_Z/\Delta I_Z$, $V_Z'=V_Z+I_Zr_Z$; $R_S=\dfrac{V_{in}-V_Z}{I_Z+I_L}$ |
| Tunnel diode | $R_n=-\Delta V/\Delta I$ (10–200 Ω); $I_P/I_V$: Ge ≈ 6, GaAs ≈ 10 |
| LED | $R_S=(V_S-V_F)/I_F$; $E=1240/\lambda$ (eV, nm) |

## Special devices
| | |
|---|---|
| SCR | 4 layers PNPN; states: forward blocking, forward conducting, reverse blocking; turns off when $I<I_H$ |
| TRIAC | 5 layers; two SCRs in inverse parallel; 4 modes; $V_{DRM},I_{DRM},V_{RRM},I_{RRM},V_{TM},I_H$ |
| DIAC | 2-terminal; breakover ≈ 30 V; triggers TRIAC |
| UJT | $\eta=\dfrac{R_{B1}}{R_{B1}+R_{B2}}$ (0.4–0.85); $V_P=\eta V_{BB}(+V_D)$; $T=R_EC_E\ln\dfrac1{1-\eta}$, $f=1/T$ |
| Photodiode | reverse-biased, $I\propto$ light; $\lambda_c\approx1240/E_g$ |

## Semiconductor physics
| | |
|---|---|
| Conductivity | $\sigma=(n\mu_n+p\mu_p)q$, $\rho=1/\sigma$; intrinsic $\sigma_i=qn_i(\mu_n+\mu_p)$ |
| Mass action | $np=n_i^2$; N: $n\approx N_D$, $p=n_i^2/N_D$; P: $p\approx N_A$, $n=n_i^2/N_A$ |
| Carriers | $n=N_ce^{-(E_c-E_F)/kT}$, $p=N_ve^{-(E_F-E_v)/kT}$ |
| Fermi level | intrinsic $\frac{E_c+E_v}2-\frac{kT}2\ln\frac{N_c}{N_v}$; N: $E_c-kT\ln\frac{N_c}{N_D}$; P: $E_v+kT\ln\frac{N_v}{N_A}$ |
| $n_i$ vs $T$ | $n_i^2=A_0T^3e^{-E_{G0}/kT}$ |
| Drift / diffusion | $J_n=qn\mu_nE$, $J_p=qp\mu_pE$; $J_p=-qD_pdp/dx$, $J_n=qD_ndn/dx$ |
| Einstein | $D/\mu=kT/q=V_T$; $L=\sqrt{D\tau}$ |
| Junction | $V_0=V_T\ln\frac{N_AN_D}{n_i^2}$; $W=\left[\frac{2\varepsilon V_0}q\frac{N_A+N_D}{N_AN_D}\right]^{1/2}$; $N_Ax_1=N_Dx_2$; $W\propto\sqrt{V_0+V_R}$ |

## Rectifiers
| | HWR | CT FWR | Bridge |
|---|---|---|---|
| $I_{dc}$ | $I_m/\pi$ | $2I_m/\pi$ | $2I_m/\pi$ |
| $V_{dc}$ | $V_m/\pi$ | $2V_m/\pi$ | $2V_m/\pi$ |
| $I_{rms}$ | $I_m/2$ | $I_m/\sqrt2$ | $I_m/\sqrt2$ |
| PIV | $V_m$ | $2V_m$ | $V_m$ |
| $\eta_{max}$ | 40.6 % | 81.2 % | 81.2 % |
| $\gamma=\sqrt{K_f^2-1}$ | 1.21 | 0.482 | 0.482 |
| $I_m$ | $\frac{V_m}{R_f+R_L}$ | $\frac{V_m}{R_f+R_L}$ | $\frac{V_m}{2R_f+R_L}$ |

## Filters (full wave, $f=50$ Hz)
| | |
|---|---|
| L | $\gamma=\dfrac{2}{3\sqrt2}\dfrac{R_L}{\sqrt{R_L^2+4\omega^2L^2}}\to\dfrac{R_L}{3\sqrt2\omega L}$ |
| C | $\gamma=\dfrac1{4\sqrt3fCR_L}=\dfrac{2890}{CR_L}$ (C in µF) |
| LC | $\gamma=\dfrac{\sqrt2}{3}\dfrac1{4\omega^2LC}=\dfrac{1.194}{LC}$ (L in H, C in µF) |
| π | $\gamma=\sqrt2\dfrac{X_{C1}X_{C2}}{R_L(X_L+X_{C2})}\to\dfrac{\sqrt2}{8\omega^3LC_1C_2R_L}$; $V_{dc}=V_m-\frac{I_{dc}}{4fC_1}-I_{dc}(R_S+R_f+R_{ch})$ |
| Regulation | $\%=\dfrac{R_{series}}{R_L}\times100$ |

## BJT DC
| | |
|---|---|
| Basics | $I_C=\beta I_B$, $I_E=(\beta+1)I_B$, $V_{BE}=0.7$ V; $\alpha=\beta/(\beta+1)$ |
| Fixed | $I_B=\frac{V_{CC}-V_{BE}}{R_B}$, $V_{CE}=V_{CC}-I_CR_C$, $I_{C,sat}=V_{CC}/R_C$ |
| Emitter | $I_B=\frac{V_{CC}-V_{BE}}{R_B+(\beta+1)R_E}$, $V_{CE}=V_{CC}-I_C(R_C+R_E)$ |
| Divider exact | $R_{Th}=R_1\|R_2$, $E_{Th}=\frac{R_2V_{CC}}{R_1+R_2}$, $I_B=\frac{E_{Th}-V_{BE}}{R_{Th}+(\beta+1)R_E}$ |
| Divider approx ($\beta R_E\ge10R_2$) | $V_B=\frac{R_2V_{CC}}{R_1+R_2}$, $V_E=V_B-0.7$, $I_E=V_E/R_E$ |
| Collector feedback | $I_B=\frac{V_{CC}-V_{BE}}{R_F+\beta(R_C+R_E)}$ |
| Follower | $I_B=\frac{V_{EE}-V_{BE}}{R_B+(\beta+1)R_E}$, $V_{CE}=V_{EE}-I_ER_E$ |
| CB | $I_E=\frac{V_{EE}-V_{BE}}{R_E}$, $V_{CE}=V_{EE}+V_{CC}-I_E(R_C+R_E)$, $V_{CB}=V_{CC}-I_CR_C$ |

## BJT AC
| | |
|---|---|
| $r_e=26\text{ mV}/I_E$; $r_o=V_A/I_{CQ}$ | $h_{ie}=\beta r_e$, $h_{fe}=\beta$, $h_{oe}=1/r_o$ |
| Fixed / bypassed | $Z_i=R_B\|\beta r_e$, $Z_o=R_C\|r_o$, $A_v=-R_C/r_e$, $A_i=\beta$ |
| Unbypassed | $Z_b=\beta(r_e+R_E)$, $Z_i=R_B\|Z_b$, $Z_o=R_C$, $A_v=-\frac{R_C}{r_e+R_E}\approx-\frac{R_C}{R_E}$ |
| Follower | $Z_i=R_B\|Z_b$, $Z_o=R_E\|r_e\approx r_e$, $A_v=\frac{R_E}{R_E+r_e}\approx1$ |
| Collector feedback | $Z_i=R_{F1}\|\beta r_e$, $Z_o=R_C\|R_{F2}$, $A_v=-\frac{R_{F2}\|R_C}{r_e}$ |
| Hybrid fixed | $Z_i=R_B\|h_{ie}$, $Z_o=R_C$, $A_v=-\frac{h_{fe}R_C}{h_{ie}}$, $A_i=h_{fe}$ |
