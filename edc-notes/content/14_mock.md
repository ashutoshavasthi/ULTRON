# Chapter 21: Full mock exam with worked solutions

::: kid How to use this
Set a timer for **90 minutes**. Answer everything on paper first. *Then* open the answers. Part A tests definitions (the quick marks), Part B the numericals (where the class-style questions live), Part C the derivations and long answers.
:::

## Part A: short answers (2 marks each)

::: try Part A: 10 questions
1. Define the depletion region and explain why it widens under reverse bias.
2. Write the diode current equation and state the values of $\eta$ for Ge and Si.
3. Distinguish avalanche breakdown from Zener breakdown (two points).
4. Explain why a tunnel diode shows negative resistance.
5. Define the intrinsic stand-off ratio of a UJT and give its usual range.
6. What is the peak inverse voltage (PIV) of a centre-tap and of a bridge rectifier?
7. Why is a TRIAC preferred over an SCR for ac power control?
8. State the mass-action law and give its use for N-type material.
9. Why is a bypass capacitor connected across $R_E$ in a CE amplifier?
10. What is the Early voltage and what does it determine?

<details markdown="1"><summary>Answers</summary>

1. The region on both sides of the junction that has been emptied of mobile carriers, containing only fixed ionised donors and acceptors. Reverse bias pulls electrons and holes away from the junction, uncovering more fixed ions, so the region widens (and $W\propto\sqrt{V_0+V_R}$).
2. $I=I_0(e^{V/\eta V_T}-1)$, $V_T=T/11600$; $\eta=1$ (Ge), $2$ (Si).
3. Avalanche: lightly doped, wide depletion layer, carrier multiplication by impact ionisation, above about 6 V. Zener: heavily doped, thin layer, field directly breaks covalent bonds, below about 6 V.
4. In the heavily doped junction electrons tunnel through the thin barrier; beyond the peak voltage the electron and hole states move out of alignment so tunnelling (hence current) *falls* while voltage rises: $dI/dV<0$.
5. $\eta=R_{B1}/(R_{B1}+R_{B2})$; 0.4 to 0.85.
6. Centre-tap: $2V_{Smax}$; bridge: $V_{Smax}$.
7. It conducts in both directions (both half-cycles), is triggered by either gate polarity, needs one heat sink and fuse.
8. $np=n_i^2$. For N-type $n\approx N_D$ so $p=n_i^2/N_D$.
9. It shorts $R_E$ for ac so the gain is $-R_C/r_e$ (large) instead of $-R_C/R_E$, while $R_E$ still stabilises the dc bias.
10. $V_A$ is the voltage where the extended output characteristics meet the $V_{CE}$ axis (at $-V_A$); it sets $r_o\approx V_A/I_{CQ}$ (the slope of the output curves).
</details>
:::

## Part B: numericals (5 marks each)

::: try Part B: 6 problems
**B1.** A silicon diode has $I_0=10$ nA at 25 °C. Find $I_0$ at 85 °C. Then find the forward current at 300 K when $V_D=0.55$ V ($\eta=2$, take $I_0=10$ nA).

**B2.** Design a Zener regulator for a 6.2 V supply from an unregulated input that varies between 16 V and 20 V. The load current varies from 0 to 20 mA and the minimum Zener current is 5 mA. Find $R_S$ (preferred value) and the Zener power rating needed.

**B3.** A silicon PN junction has $N_A=5\times10^{16}$ and $N_D=10^{15}\ \text{cm}^{-3}$, $n_i=1.5\times10^{10}\ \text{cm}^{-3}$, $\varepsilon_r=12$ at 300 K ($V_T=25.85$ mV). Find $V_0$ and the depletion width at zero bias, and at 10 V reverse bias.

**B4.** A bridge rectifier is fed from a 230 V rms mains through a 230 V : 12 V rms transformer. Silicon diodes, $R_L=47\ \Omega$. Find $V_{dc}$, $I_{dc}$, PIV. If a 2200 µF capacitor is added (50 Hz), find the ripple factor.

**B5.** A UJT relaxation oscillator has $\eta=0.7$, $V_{BB}=15$ V, $R_E=68$ kΩ, $C_E=0.022\ \mu$F. Find $V_P$, the period and the frequency.

**B6.** Voltage-divider bias: $V_{CC}=15$ V, $R_1=56$ kΩ, $R_2=12$ kΩ, $R_C=3.3$ kΩ, $R_E=1$ kΩ, $\beta=120$. (a) Test the approximation and find $I_C$, $V_{CE}$ (approximate and exact). (b) With $C_E$ present find $r_e$, $Z_i$, $A_v$. (c) Without $C_E$ find $Z_i$, $A_v$.

<details markdown="1"><summary>Answers</summary>

**B1.** $\Delta T=60$ °C → 6 doublings: $I_0=10\times2^6=\mathbf{640\ nA}$. Forward current at 300 K: $\eta V_T=2\times0.02586=0.05172$; $0.55/0.05172=10.63$; $e^{10.63}=4.14\times10^4$; $I=10\text{ nA}\times4.14\times10^4=\mathbf{0.41\ mA}$.

**B2.** $R_S=\dfrac{V_{in,min}-V_Z}{I_{L,max}+I_{Z,min}}=\dfrac{16-6.2}{20+5\text{ mA}}=392\ \Omega\to$ **390 Ω**. Worst-case Zener current is at $V_{in}=20$ V, no load: $I_Z=(20-6.2)/390=35.4$ mA, so $P_Z=6.2\times35.4=\mathbf{219\ mW}$ ⇒ choose a **500 mW** Zener. Check minimum: at 16 V and 20 mA load, $I_S=25.1$ mA ⇒ $I_Z=5.1$ mA ✓.

**B3.** $V_0=V_T\ln\dfrac{N_AN_D}{n_i^2}=0.02585\ln\dfrac{5\times10^{31}}{2.25\times10^{20}}=0.02585\times26.13=\mathbf{0.675\ V}$. $W=\left[\dfrac{2\varepsilon V}{q}\dfrac{N_A+N_D}{N_AN_D}\right]^{1/2}$ with $\varepsilon=12\times8.85\times10^{-14}$ F/cm: at zero bias $W=\left[\dfrac{2(1.062\times10^{-12})(0.675)}{1.6\times10^{-19}}\times\dfrac{5.1\times10^{16}}{5\times10^{31}}\right]^{1/2}=\mathbf{0.96\ \mu m}$ (mostly on the lightly-doped N side: $x_n=0.94\ \mu$m, $x_p=0.02\ \mu$m). At 10 V reverse: $V=10.675$: $W=0.96\sqrt{10.675/0.675}=\mathbf{3.8\ \mu m}$.

**B4.** Secondary 12 V rms ⇒ $V_m=12\sqrt2=16.97$ V; minus two diode drops $=15.57$ V. $V_{dc}=\dfrac{2\times15.57}{\pi}=\mathbf{9.91\ V}$; $I_{dc}=9.91/47=\mathbf{211\ mA}$; PIV $=V_{Smax}=\mathbf{17.0\ V}$ (choose ≥ 50 V diodes). With the C filter: $\gamma=\dfrac{1}{4\sqrt3fCR_L}=\dfrac{1}{4\sqrt3\times50\times2200\times10^{-6}\times47}=\mathbf{0.028}$ (2.8 %).

**B5.** $V_P=\eta V_{BB}=0.7\times15=\mathbf{10.5\ V}$ (11.2 V if $V_D=0.7$ V is included). $T=R_EC_E\ln\dfrac1{1-\eta}=68\text{k}\times22\text{n}\times\ln\dfrac1{0.3}=1.496\text{ ms}\times1.204=\mathbf{1.80\ ms}$; $f=\mathbf{555\ Hz}$.

**B6.** (a) $\beta R_E=120$ k vs $10R_2=120$ k: borderline (satisfied with equality). *Approximate:* $V_B=\dfrac{12\times15}{68}=2.65$ V; $V_E=1.95$ V; $I_C\approx I_E=\mathbf{1.95\ mA}$; $V_{CE}=15-1.95(4.3)=\mathbf{6.63\ V}$. *Exact:* $R_{Th}=9.88$ k, $E_{Th}=2.65$ V, $I_B=\dfrac{1.95}{9.88\text{k}+121\text{k}}=14.9\ \mu$A, $I_C=\mathbf{1.79\ mA}$, $V_{CE}=\mathbf{7.32\ V}$ (10 % apart because the condition is only just met).
(b) With $C_E$ (use $I_E=1.95$ mA): $r_e=26/1.95=\mathbf{13.4\ \Omega}$; $Z_i=9.88\text{k}\parallel(120\times13.4)=9.88\text{k}\parallel1.60\text{k}=\mathbf{1.38\ k\Omega}$; $A_v=-3300/13.4=\mathbf{-247}$.
(c) Without $C_E$: $Z_b=120(13.4+1000)=121.6$ k; $Z_i=9.88\text{k}\parallel121.6\text{k}=\mathbf{9.14\ k\Omega}$; $A_v=-\dfrac{3300}{13.4+1000}=\mathbf{-3.26}$.
</details>
:::

## Part C: derivations and long answers (10 marks each)

::: try Part C: 5 questions
**C1.** Derive the ripple factor and efficiency of a half-wave rectifier.

**C2.** Derive an expression for the depletion width $W$ of an abrupt PN junction using Poisson’s equation, and the expression for the contact potential.

**C3.** Explain the working of a UJT relaxation oscillator with waveforms, and derive its frequency.

**C4.** Explain the construction, working and V–I characteristic of an SCR, with the two-transistor analogy.

**C5.** For the CE amplifier with self-bias (emitter-bias), derive $Z_i$, $Z_o$, $A_v$ with and without the bypass capacitor using the $r_e$ model.

<details markdown="1"><summary>Answer outlines (marks in brackets)</summary>

**C1.** [2] Circuit and operation. [2] $I_{dc}=I_m/\pi$, $I_{rms}=I_m/2$. [2] $P_{dc}=(I_m/\pi)^2R_L$, $P_{ac}=\frac{I_m^2}{4}(R_f+R_L)$, $\eta=\frac{4}{\pi^2}\frac{R_L}{R_f+R_L}\to40.6\%$. [3] $K_f=\pi/2$, $\gamma=\sqrt{K_f^2-1}=1.21$. [1] Conclusion (poor).

**C2.** [2] Charge distribution and figure ($\rho=-qN_A$, $+qN_D$). [3] Poisson, integrate twice, boundary conditions ⇒ $V_1=-\frac{qN_A}{2\varepsilon}x_1^2$, $V_2=\frac{qN_D}{2\varepsilon}x_2^2$. [2] $V_0=V_2-V_1$, neutrality $N_Ax_1=-N_Dx_2$. [2] $W=\left[\frac{2\varepsilon V_0}{q}\frac{N_A+N_D}{N_AN_D}\right]^{1/2}$. [1] $V_0=V_T\ln(N_AN_D/n_i^2)$ from the bands.

**C3.** [2] Circuit and UJT working ($V_P=\eta V_{BB}$). [3] Cycle: charge, fire, discharge, cut-off; waveforms at $E$, $B_1$, $B_2$. [4] $v_C=V_{BB}(1-e^{-t/RC})$, set $v_C=\eta V_{BB}$ ⇒ $T=R_EC_E\ln\frac1{1-\eta}$, $f=1/T$. [1] Applications.

**C4.** [2] Structure, symbol, junctions. [3] Two-transistor analogy, regenerative action. [3] Gate open/gate positive operation; three states. [2] V–I curve with $V_{BO}$, $I_H$; turn-off.

**C5.** [2] AC equivalent rules. [3] With $C_E$: $Z_i=R_B\|\beta r_e$, $Z_o=R_C$, $A_v=-R_C/r_e$. [4] Without: $V_i=I_b\beta r_e+(\beta+1)I_bR_E$ ⇒ $Z_b=\beta(r_e+R_E)$; $Z_i=R_B\|Z_b$; $Z_o=R_C$; $A_v=-\beta R_C/Z_b\approx-R_C/(r_e+R_E)\approx-R_C/R_E$. [1] Comment on the effect of $C_E$.
</details>
:::
