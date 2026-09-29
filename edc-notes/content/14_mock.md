# Chapter 21: Full mock exam with worked solutions

::: kid How to use this
Set a timer for **90 minutes**. Answer everything on paper first. **Only then** open the solutions. Part A tests definitions (quick marks), Part B the numericals (where the class-style questions live), Part C the derivations and long answers. Each part has its questions in a purple box and its full step-by-step solutions in a separate green box below it.
:::

## Part A: short answers (2 marks each)

::: try Part A questions
1. Define the depletion region and explain why it widens under reverse bias.
2. Write the diode current equation and state $\eta$ for Ge and for Si.
3. Distinguish avalanche breakdown from Zener breakdown (two points).
4. Explain why a tunnel diode shows negative resistance.
5. Define the intrinsic stand-off ratio of a UJT and give its usual range.
6. What is the peak inverse voltage (PIV) of a centre-tap and of a bridge rectifier?
7. Why is a TRIAC preferred over an SCR for ac power control?
8. State the mass-action law and use it for N-type material.
9. Why is a bypass capacitor connected across $R_E$ in a CE amplifier?
10. What is the Early voltage and what does it determine?
:::

::: soln Part A solutions
<details markdown="1"><summary>Solution A1</summary>

**Definition:** the region on both sides of a PN junction emptied of mobile carriers; it contains only fixed ionised donors and acceptors.
**Why it widens:** reverse bias pulls electrons and holes away from the junction, uncovering more fixed ions, so the region widens. ($W\propto\sqrt{V_0+V_R}$.)
</details>

<details markdown="1"><summary>Solution A2</summary>

$I=I_0\left(e^{V/\eta V_T}-1\right)$ with $V_T=T/11600$; $\eta=1$ for germanium, $\eta=2$ for silicon.
</details>

<details markdown="1"><summary>Solution A3</summary>

* **Avalanche:** lightly doped, wide depletion layer, carriers gain energy and knock out more carriers (multiplication), occurs above about 6 V.
* **Zener:** heavily doped, very thin layer, the strong field directly breaks bonds, occurs below about 6 V.
</details>

<details markdown="1"><summary>Solution A4</summary>

**Step 1.** In the very heavily doped junction, electrons tunnel through the thin barrier when electron and hole states line up.
**Step 2.** Beyond the peak voltage the states move out of alignment, so tunnelling (and current) **fall** while the voltage rises.
**Step 3.** $\Delta I/\Delta V<0$ is negative resistance.
</details>

<details markdown="1"><summary>Solution A5</summary>

$\eta=\dfrac{R_{B1}}{R_{B1}+R_{B2}}$: the fraction of $V_{BB}$ that appears between the emitter joint and $B_1$ with the emitter open. Usually **0.4 to 0.85**.
</details>

<details markdown="1"><summary>Solution A6</summary>

Centre-tap: $2V_{Smax}$ (half-winding peak $V_{Smax}$). Bridge: $V_{Smax}$ (whole-winding peak).
</details>

<details markdown="1"><summary>Solution A7</summary>

A TRIAC conducts both ways, so it controls both half-cycles; either gate polarity can trigger it; one heat sink and one fuse suffice.
</details>

<details markdown="1"><summary>Solution A8</summary>

$np=n_i^2$. For N-type, $n\approx N_D$, so $p=n_i^2/N_D$.
</details>

<details markdown="1"><summary>Solution A9</summary>

It shorts $R_E$ for the ac signal, so the gain is $-R_C/r_e$ (large) instead of $-R_C/R_E$ (small), while $R_E$ still stabilises the dc bias.
</details>

<details markdown="1"><summary>Solution A10</summary>

$V_A$ is the voltage at which the extended output characteristics meet the $V_{CE}$-axis (at $-V_A$). It sets the output resistance $r_o\approx V_A/I_{CQ}$.
</details>
:::

## Part B: numericals (5 marks each)

::: try Part B questions
**B1.** A silicon diode has $I_0=10$ nA at 25 °C. Find $I_0$ at 85 °C. Then find the forward current at 300 K when $V_D=0.55$ V ($\eta=2$, take $I_0=10$ nA).

**B2.** Design a Zener regulator for a 6.2 V supply from an unregulated input that varies between 16 V and 20 V. The load current varies from 0 to 20 mA and the minimum Zener current is 5 mA. Find $R_S$ (preferred value) and the Zener power rating needed.

**B3.** A silicon PN junction has $N_A=5\times10^{16}$ and $N_D=10^{15}\ \text{cm}^{-3}$, $n_i=1.5\times10^{10}\ \text{cm}^{-3}$, $\varepsilon_r=12$ at 300 K ($V_T=25.85$ mV). Find $V_0$ and the depletion width at zero bias and at 10 V reverse bias.

**B4.** A bridge rectifier is fed from a 230 V rms mains through a 230 V : 12 V rms transformer. Silicon diodes, $R_L=47\ \Omega$. Find $V_{dc}$, $I_{dc}$ and PIV. If a 2200 µF capacitor is added (50 Hz), find the ripple factor.

**B5.** A UJT relaxation oscillator has $\eta=0.7$, $V_{BB}=15$ V, $R_E=68\ \text{k}\Omega$, $C_E=0.022\ \mu$F. Find $V_P$, the period and the frequency.

**B6.** Voltage-divider bias: $V_{CC}=15$ V, $R_1=56\ \text{k}\Omega$, $R_2=12\ \text{k}\Omega$, $R_C=3.3\ \text{k}\Omega$, $R_E=1\ \text{k}\Omega$, $\beta=120$. (a) Test the approximation and find $I_C$, $V_{CE}$ (approximate and exact). (b) With $C_E$ present find $r_e$, $Z_i$, $A_v$. (c) Without $C_E$ find $Z_i$, $A_v$.
:::

::: soln Part B solutions
<details markdown="1"><summary>Solution B1</summary>

**Part 1: leakage at 85 °C.**
**Step 1.** Rise: $85-25=60$ °C.
**Step 2.** Doublings: $60/10=6$; factor $2^6=64$.
**Step 3.** $I_0=10\ \text{nA}\times64=640$ nA.

**Part 2: forward current.**
**Step 4.** $\eta V_T=2\times\dfrac{300}{11600}=2\times0.02586=0.05172$ V.
**Step 5.** Exponent: $\dfrac{0.55}{0.05172}=10.63$.
**Step 6.** $e^{10.63}=4.14\times10^{4}$.
**Step 7.** $I=10^{-8}\times(4.14\times10^{4}-1)=4.14\times10^{-4}$ A.

**Answer:** $I_0(85^\circ\text{C})=\mathbf{640\ nA}$; $I_D=\mathbf{0.41\ mA}$.
</details>

<details markdown="1"><summary>Solution B2</summary>

**Given:** $V_Z=6.2$ V; $V_{in}$ from 16 V to 20 V; $I_L$ from 0 to 20 mA; $I_{Z,min}=5$ mA.

**Step 1: worst case for the minimum Zener current** is the lowest input (16 V) and the heaviest load (20 mA). The Zener must still carry 5 mA, so $I_S=I_Z+I_L=5+20=25$ mA.
**Step 2:** $R_S=\dfrac{V_{in,min}-V_Z}{I_S}=\dfrac{16-6.2}{0.025}=\dfrac{9.8}{0.025}=392\ \Omega$. Preferred value: **390 Ω**.
**Step 3: worst case for power** is the highest input (20 V) with no load (all $I_S$ through the Zener): $I_S=\dfrac{20-6.2}{390}=35.4$ mA.
**Step 4:** $P_Z=V_ZI_Z=6.2\times35.4\ \text{mA}=219$ mW.
**Step 5: check the minimum.** At 16 V with 20 mA load: $I_S=9.8/390=25.1$ mA, $I_Z=5.1$ mA $\ge5$ mA ✓.

**Answer:** $R_S=\mathbf{390\ \Omega}$; use a **500 mW** Zener (needs at least 219 mW).
</details>

<details markdown="1"><summary>Solution B3</summary>

**Step 1: contact potential.** $V_0=V_T\ln\dfrac{N_AN_D}{n_i^2}$. $N_AN_D=5\times10^{16}\times10^{15}=5\times10^{31}$. $n_i^2=2.25\times10^{20}$. Ratio $=2.22\times10^{11}$. $\ln(2.22\times10^{11})=\ln2.22+11\ln10=0.798+25.328=26.13$. $V_0=0.02585\times26.13=0.675$ V.
**Step 2: constants (in cm units).** $\varepsilon=12\times8.85\times10^{-14}=1.062\times10^{-12}$ F/cm.
**Step 3: doping factor.** $\dfrac{N_A+N_D}{N_AN_D}=\dfrac{5.1\times10^{16}}{5\times10^{31}}=1.02\times10^{-15}$.
**Step 4: zero-bias width.** $W=\left[\dfrac{2\varepsilon V_0}{q}\times1.02\times10^{-15}\right]^{1/2}$. $\dfrac{2\times1.062\times10^{-12}\times0.675}{1.6\times10^{-19}}=8.96\times10^{6}$. Multiply: $8.96\times10^{6}\times1.02\times10^{-15}=9.14\times10^{-9}$. $W=\sqrt{9.14\times10^{-9}}=9.56\times10^{-5}$ cm $=0.956\ \mu$m.
**Step 5: split.** $x_n=W\dfrac{N_A}{N_A+N_D}=0.956\times0.98=0.937\ \mu$m; $x_p=0.019\ \mu$m.
**Step 6: at 10 V reverse.** $V_0+V_R=10.675$ V. $W\propto\sqrt{V}$, so $W=0.956\times\sqrt{10.675/0.675}=0.956\times3.977=3.80\ \mu$m.

**Answer:** $V_0=\mathbf{0.675\ V}$; $W(0)=\mathbf{0.96\ \mu m}$ (almost all in the lightly-doped N side); $W(10\ \text{V})=\mathbf{3.8\ \mu m}$.
</details>

<details markdown="1"><summary>Solution B4</summary>

**Step 1: secondary rms.** 12 V.
**Step 2: peak.** $V_m=12\sqrt2=16.97$ V.
**Step 3: two diode drops.** $16.97-2\times0.7=15.57$ V.
**Step 4: $V_{dc}$.** $\dfrac{2\times15.57}{\pi}=\dfrac{31.14}{3.1416}=9.91$ V.
**Step 5: $I_{dc}$.** $\dfrac{9.91}{47}=0.211$ A.
**Step 6: PIV.** $V_{Smax}=16.97$ V; choose diodes rated at least 50 V.
**Step 7: ripple with the capacitor.** $\gamma=\dfrac{1}{4\sqrt3fCR_L}$; $fCR_L=50\times2200\times10^{-6}\times47=5.17$; $4\sqrt3=6.928$; $\gamma=\dfrac{1}{6.928\times5.17}=0.0279$.

**Answer:** $V_{dc}=\mathbf{9.91\ V}$, $I_{dc}=\mathbf{211\ mA}$, PIV $=\mathbf{17\ V}$, ripple factor $=\mathbf{0.028}$ (2.8 %).
</details>

<details markdown="1"><summary>Solution B5</summary>

**Step 1:** $V_P=\eta V_{BB}=0.7\times15=10.5$ V (11.2 V if the 0.7 V diode drop is added).
**Step 2: time constant.** $R_EC_E=68\times10^{3}\times22\times10^{-9}=1.496\times10^{-3}$ s.
**Step 3:** $\ln\dfrac{1}{1-\eta}=\ln\dfrac1{0.3}=1.204$.
**Step 4:** $T=1.496\ \text{ms}\times1.204=1.80$ ms.
**Step 5:** $f=1/T=1/1.80\ \text{ms}=555$ Hz.

**Answer:** $V_P=\mathbf{10.5\ V}$, $T=\mathbf{1.80\ ms}$, $f=\mathbf{555\ Hz}$.
</details>

<details markdown="1"><summary>Solution B6</summary>

**(a) DC.**
**Step 1: test.** $\beta R_E=120\ \text{k}$; $10R_2=120\ \text{k}$: equal, so the condition is only just satisfied.
**Approximate:** $V_B=\dfrac{12}{68}\times15=2.65$ V; $V_E=2.65-0.7=1.95$ V; $I_C\approx I_E=\dfrac{1.95}{1\ \text{k}}=1.95$ mA; $V_{CE}=15-1.95\times(3.3+1)=15-8.39=6.63$ V.
**Exact:** $R_{Th}=\dfrac{56\times12}{68}=9.88\ \text{k}$; $E_{Th}=2.65$ V; $I_B=\dfrac{2.65-0.7}{9.88\ \text{k}+121\times1\ \text{k}}=\dfrac{1.95}{130.88\ \text{k}}=14.9\ \mu$A; $I_C=120\times14.9\ \mu\text{A}=1.79$ mA; $V_{CE}=15-1.79\times4.3=7.32$ V.
(They differ by about 10 % because the condition holds only marginally.)

**(b) AC with $C_E$** (use the exact $I_E=121\times14.9\ \mu\text{A}=1.80$ mA):
**Step 2:** $r_e=\dfrac{26}{1.80}=14.4\ \Omega$ (or 13.4 Ω using the approximate $I_E=1.95$ mA; use one consistently).
Using $r_e=13.4\ \Omega$: $\beta r_e=120\times13.4=1.61\ \text{k}\Omega$; $Z_i=R_{Th}\parallel\beta r_e=9.88\ \text{k}\parallel1.61\ \text{k}=\dfrac{9.88\times1.61}{11.49}=1.38\ \text{k}\Omega$; $A_v=-\dfrac{R_C}{r_e}=-\dfrac{3300}{13.4}=-247$.

**(c) Without $C_E$:**
**Step 3:** $Z_b=\beta(r_e+R_E)=120\times(13.4+1000)=121.6\ \text{k}\Omega$.
**Step 4:** $Z_i=9.88\ \text{k}\parallel121.6\ \text{k}=\dfrac{9.88\times121.6}{131.5}=9.14\ \text{k}\Omega$.
**Step 5:** $A_v=-\dfrac{R_C}{r_e+R_E}=-\dfrac{3300}{1013.4}=-3.26$.

**Answer:** (a) approximate $1.95$ mA, $6.63$ V; exact $1.79$ mA, $7.32$ V. (b) $r_e\approx13.4\ \Omega$, $Z_i=1.38\ \text{k}\Omega$, $A_v=-247$. (c) $Z_i=9.14\ \text{k}\Omega$, $A_v=-3.26$.
</details>
:::

## Part C: derivations and long answers (10 marks each)

::: try Part C questions
**C1.** Derive the ripple factor and efficiency of a half-wave rectifier.

**C2.** Derive an expression for the depletion width $W$ of an abrupt PN junction using Poisson's equation, and the expression for the contact potential.

**C3.** Explain the working of a UJT relaxation oscillator with waveforms, and derive its frequency.

**C4.** Explain the construction, working and V–I characteristic of an SCR, with the two-transistor analogy.

**C5.** For the CE amplifier with self-bias (emitter bias), derive $Z_i$, $Z_o$ and $A_v$ with and without the bypass capacitor using the $r_e$ model.
:::

::: soln Part C answer outlines (with mark allocation)
<details markdown="1"><summary>Outline C1 (10 marks)</summary>

* [2] Circuit and operation (diode conducts in the positive half-cycle only).
* [2] $I_{dc}=I_m/\pi$ (integral of $\sin$ from 0 to $\pi$ gives 2, divided by $2\pi$); $I_{rms}=I_m/2$ (integral of $\sin^2$ gives $\pi/2$, divided by $2\pi$, then square root).
* [2] $P_{dc}=(I_m/\pi)^2R_L$; $P_{ac}=\dfrac{I_m^2}{4}(R_f+R_L)$; $\eta=\dfrac{4}{\pi^2}\dfrac{R_L}{R_f+R_L}\to40.6\%$.
* [3] $K_f=I_{rms}/I_{dc}=\pi/2=1.57$; $\gamma=\sqrt{K_f^2-1}=1.21$.
* [1] Conclusion: poor efficiency and large ripple.

See §14.2 for every step.
</details>

<details markdown="1"><summary>Outline C2 (10 marks)</summary>

* [2] Charge distribution $\rho=-qN_A$ (P side), $+qN_D$ (N side); sketch.
* [3] Poisson $d^2V/dx^2=-\rho/\varepsilon$; integrate twice; boundary conditions $V=0$ at $x=0$ and $dV/dx=0$ at $x_1$; get $V_1=-\dfrac{qN_A}{2\varepsilon}x_1^2$ and $V_2=\dfrac{qN_D}{2\varepsilon}x_2^2$.
* [2] $V_0=V_2-V_1$ and neutrality $N_A|x_1|=N_Dx_2$.
* [2] Solve: $W=\left[\dfrac{2\varepsilon V_0}{q}\dfrac{N_A+N_D}{N_AN_D}\right]^{1/2}$.
* [1] $V_0=V_T\ln(N_AN_D/n_i^2)$ from the band diagram.

See §13.3–13.4.
</details>

<details markdown="1"><summary>Outline C3 (10 marks)</summary>

* [2] Circuit and UJT working ($V_P=\eta V_{BB}$).
* [3] The cycle: charge through $R_E$; fire at $V_P$; discharge through $E$–$B_1$; UJT turns off; repeat; waveforms at $E$, $B_1$, $B_2$.
* [4] $v_C=V_{BB}(1-e^{-t/R_EC_E})$; set $v_C=\eta V_{BB}$; $T=R_EC_E\ln\dfrac1{1-\eta}$; $f=1/T$.
* [1] Applications.

See §10.5.
</details>

<details markdown="1"><summary>Outline C4 (10 marks)</summary>

* [2] Structure: four layers $P_1N_1P_2N_2$, three junctions, gate to $P_2$; symbol.
* [3] Two-transistor analogy and regenerative action.
* [3] Gate open (blocks, $J_2$ reverse biased); gate positive (turns on and latches); three states.
* [2] V–I curve with $V_{BO}$, $I_H$; turn-off by reducing current below $I_H$.

See Chapter 8.
</details>

<details markdown="1"><summary>Outline C5 (10 marks)</summary>

* [2] Rules for the ac equivalent (dc sources to zero, capacitors shorted, remove bypassed elements).
* [3] With $C_E$: $Z_i=R_B\parallel\beta r_e$, $Z_o=R_C$, $A_v=-R_C/r_e$.
* [4] Without: $V_i=I_b\beta r_e+(\beta+1)I_bR_E\Rightarrow Z_b=\beta(r_e+R_E)$; $Z_i=R_B\parallel Z_b$; $Z_o=R_C$; $A_v=-\beta R_C/Z_b\approx-R_C/(r_e+R_E)\approx-R_C/R_E$.
* [1] Comment: $C_E$ raises the gain by a large factor.

See §18.4.
</details>
:::
