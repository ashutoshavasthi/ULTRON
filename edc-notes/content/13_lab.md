# Chapter 19: The lab: BJT characteristics (your circuit photos)

*Sources: your three circuit photos (two BC547 set-ups and a hand-drawn "self-bias with bypass capacitor")*

::: words
| Word / symbol | Plain meaning |
|---|---|
| BC547 | a small silicon NPN transistor in a 3-legged plastic (TO-92) case |
| Characteristic | a graph showing how one quantity depends on another |
| Input characteristic | $I_B$ against $V_{BE}$ at fixed $V_{CE}$ |
| Output characteristic | $I_C$ against $V_{CE}$ at fixed $I_B$ |
| $V_{BB}$, $V_{CC}$ | variable supplies for the base and collector circuits |
| $R_B$ | resistor in the base circuit (100 kΩ) that limits base current |
| $R_C$ | resistor in the collector circuit (1 kΩ) |
| µA meter, mA meter | ammeters for the (small) base and (larger) collector currents |
| $V_{BE}$, $V_{CE}$ | voltmeters across base–emitter and collector–emitter |
| $\beta_{dc}$, $\beta_{ac}$ | $I_C/I_B$ at a point; $\Delta I_C/\Delta I_B$ between two curves |
| $r_i$, $r_o$ | dynamic input and output resistance from the slopes |
:::

::: kid What are we actually doing?
In lectures the transistor is a symbol and some equations. In the lab we **measure** it. We turn two knobs (an input voltage and an output voltage), read three or four meters, and draw two graphs showing how the transistor really behaves. These are the same curves used for the load lines in Chapters 16–17.
:::

## 19.1 The transistor: BC547

The BC547 is a small-signal **NPN silicon** transistor. <span class="tag">extra</span> Typical data (check your data sheet): $V_{CEO}\approx45$ V, $I_{C,max}\approx100$ mA, power about 500 mW, $h_{FE}$ from about 110 to 800 depending on the suffix letter. With the flat face towards you and the legs down, the pins are usually **C – B – E** from left to right. **Always confirm the pin-out on the data sheet before wiring.**

## 19.2 Circuit 1 (photo 1): output characteristic with a fixed base current

{{fig c_lab_bc547|Photo 2 redrawn: the standard CE characteristics test bench with four meters (µA, $V_{BE}$, mA, $V_{CE}$). Both $V_{BB}$ and $V_{CC}$ are variable supplies.|92}}

Photo 1 is the simplest version of the same experiment: a **fixed 5 V source $V_1$** feeds the base through **$R_1$ (470 kΩ or 1 MΩ)**, and a **variable 0–15 V supply $V_2$** feeds the collector through **$R_2=1\ \text{k}\Omega$**, with an **mA meter** in the collector path and a **voltmeter** across the transistor.

::: ex Example 19.1: The base current in photo 1
**Given:** $V_1=5$ V, $V_{BE}=0.7$ V, $R_1=470\ \text{k}\Omega$ or $1\ \text{M}\Omega$.

**Formula:** $I_B=\dfrac{V_1-V_{BE}}{R_1}$.

**Step 1:** voltage across $R_1$: $5-0.7=4.3$ V.
**Step 2 ($R_1=470\ \text{k}\Omega$):** $I_B=\dfrac{4.3}{470\,000}=9.15\ \mu$A.
**Step 3 ($R_1=1\ \text{M}\Omega$):** $I_B=\dfrac{4.3}{1\,000\,000}=4.3\ \mu$A.
**Step 4: expected collector current** (say $\beta=200$): $9.15\ \mu\text{A}\times200=1.83$ mA and $4.3\ \mu\text{A}\times200=0.86$ mA.

**Answer:** $I_B=9.15\ \mu$A and $4.3\ \mu$A: two curves of the output family.
:::

**Procedure:** sweep $V_2$ from 0 to 15 V and record $I_C$ (mA) and $V_{CE}$ (V). $I_C$ rises steeply for $V_{CE}$ below about 0.3 V (saturation) then flattens in the active region at $I_C\approx\beta I_B$. The load line of the 1 kΩ resistor is $V_{CE}=V_2-I_C\times1\ \text{k}\Omega$.

## 19.3 Circuit 2 (photo 2): full input and output characteristics

Components: $R_B=100\ \text{k}\Omega$ (protects the base), $R_C=1\ \text{k}\Omega$, a **µA meter** in the base circuit, an **mA meter** in the collector circuit, voltmeters for $V_{BE}$ and $V_{CE}$, and two variable supplies $V_{BB}$ and $V_{CC}$.

### A. Input characteristic ($I_B$ against $V_{BE}$ at constant $V_{CE}$)
1. Set $V_{CC}$ so that $V_{CE}$ has a fixed value (say 0 V first, then 5 V). Keep readjusting $V_{CC}$ so $V_{CE}$ stays fixed (the meter reads $V_{CE}$ **at the transistor**, not the supply).
2. Increase $V_{BB}$ in steps; note $V_{BE}$ (V) and $I_B$ (µA) each time.
3. Plot $I_B$ (y) against $V_{BE}$ (x): a diode-like curve with a knee at 0.6–0.7 V.
4. **Dynamic input resistance:** $r_i=\dfrac{\Delta V_{BE}}{\Delta I_B}$ at constant $V_{CE}$ (from the steep part).

### B. Output characteristic ($I_C$ against $V_{CE}$ at constant $I_B$)
1. Set $V_{BB}$ to give a chosen $I_B$ (say 20 µA); keep $I_B$ constant.
2. Vary $V_{CC}$ (0 → 12 V); note $V_{CE}$ and $I_C$.
3. Repeat for $I_B=40,60,80\ \mu$A.
4. Plot $I_C$ (y) against $V_{CE}$ (x): a family of curves like the figure in Chapter 16.
5. **Output resistance:** $r_o=\dfrac{\Delta V_{CE}}{\Delta I_C}$ at constant $I_B$ (reciprocal of the slope; large). **AC current gain:** $\beta_{ac}=\dfrac{\Delta I_C}{\Delta I_B}$ at constant $V_{CE}$. **DC gain:** $\beta_{dc}=I_C/I_B$.

::: ex Example 19.2: Calculating $\beta$ and $r_o$ from readings
**Given (hypothetical readings):** at $V_{CE}=5$ V: $I_B=20\ \mu$A gives $I_C=4.0$ mA and $I_B=40\ \mu$A gives $I_C=8.2$ mA. On the $I_B=20\ \mu$A curve, $V_{CE}=4$ V gives $I_C=3.95$ mA and $V_{CE}=10$ V gives $I_C=4.10$ mA.

**Step 1: $\beta_{dc}$ at $I_B=20\ \mu$A.** $\dfrac{4.0\ \text{mA}}{20\ \mu\text{A}}=200$.
**Step 2: $\beta_{ac}$.** $\dfrac{\Delta I_C}{\Delta I_B}=\dfrac{8.2-4.0\ \text{mA}}{40-20\ \mu\text{A}}=\dfrac{4.2\ \text{mA}}{20\ \mu\text{A}}=210$.
**Step 3: $r_o$.** $\dfrac{\Delta V_{CE}}{\Delta I_C}=\dfrac{10-4\ \text{V}}{4.10-3.95\ \text{mA}}=\dfrac{6}{0.15\ \text{mA}}=40\ \text{k}\Omega$.

**Answer:** $\beta_{dc}=200$, $\beta_{ac}=210$, $r_o=40\ \text{k}\Omega$.
:::

### Points to remember
* **Never** connect the base to a supply without $R_B$ (the base current would destroy the transistor).
* Keep $I_C$ below the rated maximum; watch the power $V_{CE}I_C$.
* Meters have their own resistance: use the µA meter in the base circuit only.

## 19.4 The hand-drawn circuit (photo 3): self-bias with bypass capacitor

The sketch shows an NPN transistor with **$R_B$ from $V_{CC}$ to the base**, **$R_C$ in the collector**, an **input coupling capacitor $C_b$**, an **output coupling capacitor $C_c$** and **$R_E$ in parallel with a bypass capacitor $C_e$**. It is exactly the circuit of §17.2 (dc) and §18.4 Case 1 (ac, bypassed). Your labels "N P N" and "c, b, e" mark the layers and terminals.

* **DC:** capacitors are open, so $I_B=\dfrac{V_{CC}-V_{BE}}{R_B+(\beta+1)R_E}$ and $V_{CE}=V_{CC}-I_C(R_C+R_E)$.
* **AC:** $C_e$ shorts $R_E$, so $Z_i=R_B\parallel\beta r_e$, $Z_o\approx R_C$, $A_v=-R_C/r_e$.

## 19.5 Viva questions

::: try Questions for Chapter 19
1. Why do we use $R_B=100\ \text{k}\Omega$ in the base circuit?
2. Why is $V_{BE}$ about 0.6–0.7 V?
3. What does the nearly flat part of the output curves tell you?
4. How is $\beta$ obtained from the curves?
5. Why must $V_{CE}$ be kept constant while plotting the input characteristic?
6. In photo 1, $R_1=680\ \text{k}\Omega$. What is $I_B$?
:::

::: soln Answers and full solutions
<details markdown="1"><summary>Solution 1</summary>

The base–emitter junction is a forward-biased diode: without a series resistor, a small change in $V_{BB}$ causes a huge $I_B$. $R_B$ limits $I_B$ and lets a coarse voltage source set a fine current.
</details>

<details markdown="1"><summary>Solution 2</summary>

It is the forward voltage of the silicon base–emitter diode (the knee of its characteristic).
</details>

<details markdown="1"><summary>Solution 3</summary>

In the active region $I_C\approx\beta I_B$ almost independently of $V_{CE}$: the transistor acts as a current source controlled by $I_B$. The small slope is the Early effect ($1/r_o$).
</details>

<details markdown="1"><summary>Solution 4</summary>

$\beta_{dc}=I_C/I_B$ at a point, or $\beta_{ac}=\Delta I_C/\Delta I_B$ between two neighbouring curves at fixed $V_{CE}$ (see Example 19.2).
</details>

<details markdown="1"><summary>Solution 5</summary>

$I_B$ depends slightly on $V_{CE}$. Fixing $V_{CE}$ isolates the $I_B$–$V_{BE}$ relationship.
</details>

<details markdown="1"><summary>Solution 6</summary>

**Step 1.** $I_B=\dfrac{V_1-V_{BE}}{R_1}=\dfrac{5-0.7}{680\,000}=\dfrac{4.3}{680\,000}=6.32\times10^{-6}$ A.
**Answer:** **6.3 µA**.
</details>
:::

# Chapter 20: One-page formula sheet {.chap}

::: words
Every symbol here is explained in Chapter 0 and at the top of its own chapter. Quick reminders: $I_m$ or $I_{max}$ = **peak** current; $V_m$ = **peak** voltage; "dc" = **average**; $\eta$ has three meanings (diode: 1 or 2; UJT: stand-off ratio; rectifier: efficiency); $\gamma$ = ripple factor; $\parallel$ = in parallel with.
:::

## Diodes
| Quantity | Formula |
|---|---|
| Thermal voltage | $V_T=T/11600\approx26$ mV (300 K) |
| Diode equation | $I=I_0(e^{V/\eta V_T}-1)$; Ge $\eta=1$, Si $\eta=2$ |
| Temperature | $I_{02}=I_{01}2^{(T_2-T_1)/10}$; cut-in voltage falls as $T$ rises |
| Static / dynamic resistance | $R_{dc}=V/I$; $r_{ac}=\Delta V/\Delta I=\eta V_T/I$ |
| Transition capacitance | $C_T=K/(V_B-V)^n$ |
| Diffusion capacitance | $C_D=\tau I/(\eta V_T)$ |
| Zener | $P=V_ZI_Z$; $I_{ZM}=P_{ZM}/V_Z$; $r_Z=\Delta V_Z/\Delta I_Z$; $V_Z'=V_Z+I_Zr_Z$; $R_S=\dfrac{V_{in,min}-V_Z}{I_{Z,min}+I_{L,max}}$ |
| Tunnel diode | $R_n=-\Delta V/\Delta I$ (10–200 Ω); $I_P/I_V$: Ge ≈ 6, GaAs ≈ 10 |
| LED | $R_S=(V_S-V_F)/I_F$; $E=1240/\lambda$ (eV; $\lambda$ in nm) |

## Special devices
| | |
|---|---|
| SCR | 4 layers PNPN; states: forward blocking, forward conducting, reverse blocking; off when $I<I_H$; $V_{dc}=\frac{V_m}{2\pi}(1+\cos\alpha)$ |
| TRIAC | 5 layers; two SCRs in inverse-parallel; 4 trigger modes; $V_{DRM},I_{DRM},V_{RRM},I_{RRM},V_{TM},I_H$ |
| DIAC | 2-terminal; breakover about 30 V; triggers TRIAC |
| UJT | $\eta=\dfrac{R_{B1}}{R_{B1}+R_{B2}}$ (0.4–0.85); $V_P=\eta V_{BB}(+V_D)$; $T=R_EC_E\ln\dfrac{1}{1-\eta}$; $f=1/T$ |
| Photodiode | reverse-biased, $I\propto$ light; $\lambda_c\approx1240/E_g$; $R=\eta_q\lambda(\mu\text{m})/1.24$ |

## Semiconductor physics
| | |
|---|---|
| Conductivity | $\sigma=(n\mu_n+p\mu_p)q$; $\rho=1/\sigma$; intrinsic $\sigma_i=qn_i(\mu_n+\mu_p)$ |
| Mass action | $np=n_i^2$; N: $n\approx N_D$, $p=n_i^2/N_D$; P: $p\approx N_A$, $n=n_i^2/N_A$ |
| Carriers | $n=N_ce^{-(E_c-E_F)/kT}$; $p=N_ve^{-(E_F-E_v)/kT}$ |
| Fermi level | intrinsic $\frac{E_c+E_v}{2}-\frac{kT}{2}\ln\frac{N_c}{N_v}$; N: $E_c-kT\ln\frac{N_c}{N_D}$; P: $E_v+kT\ln\frac{N_v}{N_A}$ |
| $n_i$ against $T$ | $n_i^2=A_0T^3e^{-E_{G0}/kT}$ |
| Drift / diffusion | $J_n=qn\mu_nE$; $J_p=qp\mu_pE$; $J_p=-qD_p\,dp/dx$; $J_n=qD_n\,dn/dx$ |
| Einstein; diffusion length | $D/\mu=kT/q=V_T$; $L=\sqrt{D\tau}$ |
| Junction | $V_0=V_T\ln\frac{N_AN_D}{n_i^2}$; $W=\left[\frac{2\varepsilon V_0}{q}\frac{N_A+N_D}{N_AN_D}\right]^{1/2}$; $N_A|x_1|=N_Dx_2$; $W\propto\sqrt{V_0+V_R}$ |

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

## Filters (full-wave; $\omega=2\pi f$)
| | |
|---|---|
| L | $\gamma=\dfrac{2}{3\sqrt2}\dfrac{R_L}{\sqrt{R_L^2+4\omega^2L^2}}\to\dfrac{R_L}{3\sqrt2\,\omega L}$ |
| C | $\gamma=\dfrac{1}{4\sqrt3fCR_L}=\dfrac{2890}{CR_L}$ (50 Hz; $C$ in µF) |
| LC | $\gamma=\dfrac{\sqrt2}{3}\dfrac{1}{4\omega^2LC}=\dfrac{1.194}{LC}$ (50 Hz; $L$ in H, $C$ in µF) |
| π | $\gamma=\sqrt2\dfrac{X_{C1}X_{C2}}{R_L(X_L+X_{C2})}\to\dfrac{\sqrt2}{8\omega^3LC_1C_2R_L}$; $V_{dc}=V_m-\frac{I_{dc}}{4fC_1}-I_{dc}(R_S+R_f+R_{ch})$ |
| Regulation | $\%=\dfrac{R_{series}}{R_L}\times100$ |
| Reactances | $X_L=\omega L$; $X_C=\dfrac{1}{\omega C}$ (at the ripple frequency use $2\omega$) |

## BJT DC
| | |
|---|---|
| Basics | $I_C=\beta I_B$; $I_E=(\beta+1)I_B$; $V_{BE}=0.7$ V; $\alpha=\beta/(\beta+1)$ |
| Fixed | $I_B=\frac{V_{CC}-V_{BE}}{R_B}$; $V_{CE}=V_{CC}-I_CR_C$; $I_{C,sat}=V_{CC}/R_C$ |
| Emitter | $I_B=\frac{V_{CC}-V_{BE}}{R_B+(\beta+1)R_E}$; $V_{CE}=V_{CC}-I_C(R_C+R_E)$ |
| Divider exact | $R_{Th}=R_1\parallel R_2$; $E_{Th}=\frac{R_2V_{CC}}{R_1+R_2}$; $I_B=\frac{E_{Th}-V_{BE}}{R_{Th}+(\beta+1)R_E}$ |
| Divider approx ($\beta R_E\ge10R_2$) | $V_B=\frac{R_2V_{CC}}{R_1+R_2}$; $V_E=V_B-0.7$; $I_E=V_E/R_E$ |
| Collector feedback | $I_B=\frac{V_{CC}-V_{BE}}{R_F+\beta(R_C+R_E)}$ |
| Follower | $I_B=\frac{V_{EE}-V_{BE}}{R_B+(\beta+1)R_E}$; $V_{CE}=V_{EE}-I_ER_E$ |
| CB | $I_E=\frac{V_{EE}-V_{BE}}{R_E}$; $V_{CE}=V_{EE}+V_{CC}-I_E(R_C+R_E)$; $V_{CB}=V_{CC}-I_CR_C$ |

## BJT AC
| | |
|---|---|
| Parameters | $r_e=26\text{ mV}/I_E$; $r_o=V_A/I_{CQ}$; $h_{ie}=\beta r_e$; $h_{fe}=\beta$; $h_{oe}=1/r_o$ |
| Fixed / bypassed | $Z_i=R_B\parallel\beta r_e$; $Z_o=R_C\parallel r_o$; $A_v=-R_C/r_e$; $A_i=\beta$ |
| Unbypassed | $Z_b=\beta(r_e+R_E)$; $Z_i=R_B\parallel Z_b$; $Z_o=R_C$; $A_v=-\frac{R_C}{r_e+R_E}\approx-\frac{R_C}{R_E}$ |
| Follower | $Z_i=R_B\parallel Z_b$; $Z_o=R_E\parallel r_e\approx r_e$; $A_v=\frac{R_E}{R_E+r_e}\approx1$ |
| Collector feedback | $Z_i=R_{F1}\parallel\beta r_e$; $Z_o=R_C\parallel R_{F2}$; $A_v=-\frac{R_{F2}\parallel R_C}{r_e}$ |
| Hybrid fixed | $Z_i=R_B\parallel h_{ie}$; $Z_o=R_C$; $A_v=-\frac{h_{fe}R_C}{h_{ie}}$; $A_i=h_{fe}$ |
