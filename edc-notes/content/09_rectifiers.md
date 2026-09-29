# Chapter 14: Rectifiers

*Class notes pp. 29–32 · slides: Rectifiers, half-wave rectifier*

::: words
| Word / symbol | Plain meaning |
|---|---|
| Rectifier | circuit that turns ac into (pulsating) dc using diodes |
| Half-wave (HWR) / full-wave (FWR) | uses one half / both halves of the ac wave |
| Centre-tap | a transformer secondary with a wire from its middle (0 V reference) |
| Bridge | four diodes arranged in a diamond |
| Transformer secondary | the output winding of the transformer that feeds the rectifier |
| $V_m$, $V_{Smax}$ | **peak** value of the secondary voltage |
| $I_{max}$ or $I_m$ | **peak** load current |
| $R_L$ | load resistance |
| $R_f$ | forward resistance of one diode |
| $I_{dc}$, $V_{dc}$ | **average** (dc) load current and voltage |
| $I_{rms}$ | **root-mean-square** current (the "effective" value) |
| $P_{dc}$ | dc power delivered to the load |
| $P_{ac}$ | total ac power supplied to the circuit (load + diode) |
| $\eta$ | rectification **efficiency** $=P_{dc}/P_{ac}$ |
| Ripple | the unwanted ac left in the output |
| $\gamma$ | **ripple factor**: rms of the ac part ÷ dc value |
| $K_f$ | **form factor** $=I_{rms}/I_{dc}$ |
| PIV | peak inverse voltage across a non-conducting diode |
| TUF | transformer utilisation factor |
| $\omega t$ | angle of the ac wave (radians): one full cycle is $2\pi$ |
| Regulation | percentage fall of the dc output voltage from no-load to full-load |
:::

::: kid Turning a see-saw into a river
The mains socket gives **alternating current (AC)**: electricity flows one way, then the other, 50 times a second, like a see-saw. Your phone charger needs **direct current (DC)**: flowing one way only, like a river. A **rectifier** is a set of one-way doors (diodes) that catches the backward half of the see-saw and flips it (or throws it away), so everything flows the same way. The result is bumpy, like waves on a river, so a **filter** (Chapter 15) smooths it.
:::

## 14.1 Rectification

*Rectification* means converting AC to DC using the fact that a diode has **low resistance in forward bias and high resistance in reverse bias**. Types: **half-wave** (uses one half-cycle) and **full-wave** (uses both). Full-wave has two forms: **centre-tap** and **bridge**.

{{fig p_rect_waves|Input, half-wave output and full-wave output. The dashed red line is the average (dc) value.|85}}

## 14.2 Half-wave rectifier (HWR)

{{fig c_hwr|Half-wave rectifier: source (transformer secondary), one diode, load $R_L$.|72}}

**Circuit:** a step-down transformer, one diode in series with the secondary, and the load $R_L$.

* **Positive half-cycle:** the diode is forward biased and conducts (above the knee voltage). Current flows through $R_L$: the positive half-cycle appears across the load.
* **Negative half-cycle:** the diode is reverse biased and blocks: no load current or voltage.
* Output: **pulsating dc** (positive half-cycles only) containing a large ac "ripple".

### Analysis, step by step

The secondary voltage is $v_s=V_{Smax}\sin\omega t$. The diode has forward resistance $R_f$. Then
$$i=I_{max}\sin\omega t\ (0\le\omega t\le\pi),\qquad i=0\ (\pi\le\omega t\le2\pi),\qquad I_{max}=\frac{V_{Smax}}{R_f+R_L}.$$

**1. PIV.** In the negative half-cycle there is no current, so no voltage drop across $R_L$, and the *whole* secondary peak appears across the diode:
$$\boxed{PIV=V_{Smax}}.$$

**2. Average (dc) current.** The average of the wave over one full cycle is
$$I_{dc}=\frac1{2\pi}\int_0^{2\pi}i\,d(\omega t)=\frac{I_{max}}{2\pi}\int_0^{\pi}\sin\omega t\,d(\omega t)=\frac{I_{max}}{2\pi}\Big[-\cos\omega t\Big]_0^{\pi}=\frac{I_{max}}{2\pi}(1+1)=\boxed{\frac{I_{max}}{\pi}}\ (=0.318I_{max}).$$

**3. DC output voltage.** $V_{dc}=I_{dc}R_L=\dfrac{I_{max}R_L}{\pi}=\dfrac{V_{Smax}}{\pi}\cdot\dfrac{R_L}{R_f+R_L}$. If $R_L\gg R_f$:
$$\boxed{V_{dc}=\frac{V_{Smax}}{\pi}}.$$

**4. RMS current.** Square, average, then take the square root:
$$I_{rms}^2=\frac1{2\pi}\int_0^{\pi}I_{max}^2\sin^2\omega t\,d(\omega t)=\frac{I_{max}^2}{2\pi}\cdot\frac{\pi}{2}=\frac{I_{max}^2}{4}\ \Rightarrow\ \boxed{I_{rms}=\frac{I_{max}}{2}}.$$
(Because $\int_0^\pi\sin^2\theta\,d\theta=\pi/2$.) The rms load voltage is $V_{L,rms}=I_{rms}R_L\to V_{Smax}/2$ for $R_L\gg R_f$.

**5. Efficiency** $\eta=P_{dc}/P_{ac}$:
* $P_{dc}=I_{dc}^2R_L=\dfrac{I_{max}^2}{\pi^2}R_L$.
* $P_{ac}$ = power in diode + load $=I_{rms}^2R_f+I_{rms}^2R_L=\dfrac{I_{max}^2}{4}(R_f+R_L)$.
$$\eta=\frac{I_{max}^2R_L/\pi^2}{I_{max}^2(R_f+R_L)/4}=\frac{4}{\pi^2}\frac{R_L}{R_f+R_L}=\frac{0.406}{1+R_f/R_L}\ \xrightarrow{R_f\to0}\ \boxed{\eta_{max}=40.6\%}.$$

**6. Ripple factor.** $\gamma=I_{ac}/I_{dc}$, the rms of the ac component divided by the dc value. Since $I_{rms}^2=I_{dc}^2+I_{ac}^2$:
$$\gamma=\frac{\sqrt{I_{rms}^2-I_{dc}^2}}{I_{dc}}=\sqrt{K_f^2-1},\qquad K_f=\frac{I_{rms}}{I_{dc}}=\frac{I_{max}/2}{I_{max}/\pi}=\frac{\pi}{2}=1.57\ \Rightarrow\ \gamma=\sqrt{1.57^2-1}=\boxed{1.21}.$$

::: flag 40.5 % or 40.6 %?
Exactly $4/\pi^2=0.4053$ (40.5 %). Your slides round it to **40.6 %**; the class solution uses **40.5**. Both are accepted; use the one your question's method gives.
:::

**Disadvantages of the HWR (slides):**
1. The output has an ac component at the **input frequency**, so ripple is large and heavy filtering is needed.
2. **Low efficiency** (only one half-cycle is used).
3. **Low transformer utilisation factor.**
4. **dc saturation of the transformer core** (magnetising current, hysteresis loss, harmonics).

## 14.3 Centre-tap full-wave rectifier

{{fig c_ct_fwr|Centre-tap full-wave rectifier: two diodes and a centre-tapped transformer. Each diode conducts in alternate half-cycles and both send current the same way through $R_L$.|78}}

* **Two diodes** join the two ends of a **centre-tapped secondary**; the centre tap is the ground (0 V) reference.
* **Positive half-cycle** (top end positive): $D_1$ is forward biased and $D_2$ is reverse biased. Current path: top end → $D_1$ → $R_L$ → centre tap.
* **Negative half-cycle** (bottom end positive): $D_2$ conducts and $D_1$ is off. Path: bottom end → $D_2$ → $R_L$ → centre tap.
* The current through $R_L$ has the **same direction in both half-cycles**. The output frequency is **twice** the input frequency.

**Analysis** (each half of the secondary gives peak $V_{Smax}$; one diode conducts at a time, so $I_{max}=V_{Smax}/(R_f+R_L)$):

| Quantity | Working | Result |
|---|---|---|
| **PIV** | when $D_1$ conducts (ideal, zero drop) its cathode is at $+V_{Smax}$ while the other end of the winding is at $-V_{Smax}$: $D_2$ sees the difference | $\boxed{PIV=2V_{Smax}}$ |
| $I_{dc}$ | average over $0$ to $\pi$: $\dfrac1\pi\int_0^\pi I_{max}\sin\omega t\,d(\omega t)=\dfrac{I_{max}}{\pi}\cdot2$ | $\dfrac{2I_{max}}{\pi}=0.636I_{max}$ |
| $V_{dc}$ | $I_{dc}R_L$ | $\dfrac{2V_{Smax}}{\pi}$ ($R_L\gg R_f$) |
| $I_{rms}$ | $\sqrt{\dfrac1\pi\int_0^\pi I_{max}^2\sin^2\omega t\,d(\omega t)}=\sqrt{\dfrac{I_{max}^2}{\pi}\cdot\dfrac\pi2}$ | $\dfrac{I_{max}}{\sqrt2}$ |
| $P_{dc}$ | $I_{dc}^2R_L$ | $\dfrac{4}{\pi^2}I_{max}^2R_L$ |
| $P_{ac}$ | $I_{rms}^2(R_f+R_L)$ | $\dfrac{I_{max}^2}{2}(R_f+R_L)$ |
| Efficiency | $\dfrac{4I_{max}^2R_L/\pi^2}{I_{max}^2(R_f+R_L)/2}$ | $\dfrac{8}{\pi^2}\dfrac{R_L}{R_f+R_L}=\dfrac{0.812}{1+R_f/R_L}\to$ **81.2 %** |
| Form factor | $\dfrac{I_{max}/\sqrt2}{2I_{max}/\pi}$ | $\dfrac{\pi}{2\sqrt2}=1.11$ |
| Ripple factor | $\sqrt{K_f^2-1}=\sqrt{1.11^2-1}$ | **0.482** |

Your class notes also derive $V_{dc}$ and $V_{rms}$ for a full-wave sine directly: $V_{dc}=\dfrac1\pi\int_0^\pi V_m\sin\theta\,d\theta=\dfrac{2V_m}{\pi}$ and $V_{rms}=\dfrac{V_m}{\sqrt2}$, and quote $\gamma=I_{ac}/I_{dc}=0.481$.

## 14.4 Full-wave bridge rectifier

{{fig c_bridge|Bridge rectifier: four diodes. The load is connected across the other diagonal of the AC source.|65}}

* **Four diodes** in a bridge. The AC source connects to two opposite corners; the load $R_L$ to the other two.
* **Positive half-cycle:** one diagonal pair conducts ($D_1$ and $D_4$ in the drawing). **Negative half-cycle:** the other pair ($D_2$ and $D_3$). Current flows through $R_L$ in the **same direction** both times.
* It works with or without a transformer; if one is used, any ordinary secondary will do (**no centre tap**).

The analysis is the same as the centre-tap one, with three differences:
* **Two diodes conduct in each half-cycle**, so the total diode resistance is $2R_f$: $I_{max}=\dfrac{V_{Smax}}{2R_f+R_L}$ and $\eta=\dfrac{0.812}{1+2R_f/R_L}$.
* $V_{Smax}$ is now the peak of the **whole** secondary (in the centre-tap circuit it is the peak of **half** the secondary).
* $\boxed{PIV=V_{Smax}}$: the two conducting diodes short the source across the two OFF diodes, which therefore see only $V_{Smax}$.

The output waveform is the same as for the centre-tap circuit (see the figure in §14.1).

## 14.5 Comparison

| | Half-wave | Centre-tap FWR | Bridge FWR |
|---|---|---|---|
| Diodes | 1 | 2 | 4 |
| Transformer | ordinary | **centre-tapped** | ordinary (or none) |
| $I_{dc}$ | $I_{max}/\pi$ | $2I_{max}/\pi$ | $2I_{max}/\pi$ |
| $V_{dc}$ (ideal) | $V_{Smax}/\pi$ | $2V_{Smax}/\pi$ | $2V_{Smax}/\pi$ |
| $I_{rms}$ | $I_{max}/2$ | $I_{max}/\sqrt2$ | $I_{max}/\sqrt2$ |
| **PIV** | $V_{Smax}$ | $2V_{Smax}$ | $V_{Smax}$ |
| Ripple frequency | $f$ | $2f$ | $2f$ |
| Form factor $K_f$ | 1.57 | 1.11 | 1.11 |
| **Ripple factor** | **1.21** | **0.482** | **0.482** |
| Max efficiency | 40.6 % | 81.2 % | 81.2 % |
| Efficiency with $R_f$ | $\dfrac{0.406}{1+R_f/R_L}$ | $\dfrac{0.812}{1+R_f/R_L}$ | $\dfrac{0.812}{1+2R_f/R_L}$ |
| TUF <span class="tag">extra</span> | 0.287 | 0.693 | 0.812 |

::: flag Your class page and the efficiency formula
Class page 32 writes $\eta=\dfrac{0.812}{1+2R_f/R_L}$ immediately after $P_{ac}=\dfrac{I_{max}^2}{2}(R_f+R_L)$ (the centre-tap expression). With that $P_{ac}$ the result is $\dfrac{0.812}{1+R_f/R_L}$; the "$2R_f$" version belongs to the **bridge**. Know both and label them correctly. Also $8/\pi^2=0.8106$, which the slides round to 0.812.
:::

**Merits of full-wave over half-wave (slides):** double the efficiency (both half-cycles used); very low residual ripple (a simple filter suffices); higher transformer utilisation factor and output power. **Demerit:** more components, costlier.

**Bridge over centre-tap.** *Merits:* no special (centre-tapped, costly) transformer; can be built with or without a transformer; suits **high-voltage** uses (its PIV is half that of the centre-tap for the same output); higher TUF. *Demerits:* **four diodes**; two conduct at once, so the voltage drop across diodes is **double** (2 × 0.7 V), which matters at low voltages.

::: kid Which rectifier would you pick?
* Tiny cheap gadget, ripple does not matter: **half-wave**.
* Low-voltage supply, transformer already has a centre tap: **centre-tap** (only one diode drop).
* High voltage, or no centre-tapped transformer: **bridge**.
:::

## 14.6 Solved problems

::: ex Example 14.1: Your class half-wave problem, worked both ways
*A half-wave rectifier uses a diode with internal resistance 20 Ω and load $R_L=1\ \text{k}\Omega$. A 4:1 transformer is used and the primary voltage is 220 V rms at 50 Hz. Calculate dc output current and voltage, ac output current and voltage, PIV, efficiency and regulation.*

**Given:** $R_f=20\ \Omega$, $R_L=1000\ \Omega$, primary 220 V rms, turns ratio 4:1.

**Step 1: secondary rms voltage.** $220/4=55$ V rms.
**Step 2: the peak voltage $V_m$.** The class solution writes $V_m/2=V_{rms}=55$, so $V_m=110$ V. Strictly, a 55 V rms sine has peak $55\sqrt2=77.8$ V. Both are worked below.
**Step 3: total resistance.** $R_f+R_L=1020\ \Omega$.
**Step 4: peak current.** $I_{max}=V_m/1020$.
**Step 5: the rest, using the boxed formulas** $I_{dc}=I_{max}/\pi$, $V_{dc}=I_{dc}R_L$, $I_{rms}=I_{max}/2$, $I_{ac}=\gamma I_{dc}$ with $\gamma=1.21$, $PIV=V_m$.

| Quantity | **Class page** ($V_m=110$ V) | **Strict** ($V_m=77.8$ V) |
|---|---|---|
| $I_{max}=V_m/1020$ | 0.1078 A | 0.0763 A |
| $I_{dc}=I_{max}/\pi$ | **0.0343 A** (page: 0.034) | **0.0243 A** |
| $V_{dc}=I_{dc}R_L$ | 34.3 V (page: 35.01, then 32) | **24.3 V** |
| $I_{rms}=I_{max}/2$ | 0.0539 A (page: 0.05) | 0.0381 A |
| $V_{rms}$ across load | 53.9 V | 38.1 V |
| $I_{ac}=1.21\,I_{dc}$ | 0.0415 A (page 0.0411) | 0.0294 A |
| $P_{dc}=I_{dc}^2R_L$ | 1.18 W (page 1.01) | 0.589 W |
| **PIV** $=V_m$ | **110 V** | **77.8 V** |
| **Efficiency** $\eta=40.5\%\times\dfrac{R_L}{R_L+R_f}=40.5\times\dfrac{1000}{1020}$ | **39.7 %** | **39.7 %** |
| **Regulation** $=\dfrac{R_f}{R_L}\times100=\dfrac{20}{1000}\times100$ | **2 %** | **2 %** |

**Answer:** efficiency **39.7 %**, regulation **2 %**, ripple factor **1.21** (these do not depend on $V_m$); PIV = **110 V** (class) or 77.8 V (strict).

::: flag Why two columns?
The class solution applies the HWR *output* relation $V_{rms}=V_m/2$ to the 55 V transformer secondary. For a sinusoid $V_m=\sqrt2\,V_{rms}$. Efficiency, ripple factor and regulation come out the same either way. If your teacher's key uses 110 V, write that method; mention the $\sqrt2$ version if the question says "55 V rms". Also, the class page's $V_{dc}=32$ V does not match its own $I_{dc}R_L=34.3$ V or $V_m/\pi=35.0$ V.
:::

**Regulation** here means the fall in dc output voltage between no load and full load: $\%\text{reg}=\dfrac{V_{NL}-V_{FL}}{V_{FL}}\times100$. With $V_{NL}=V_m/\pi$ and $V_{FL}=V_m/\pi-I_{dc}R_f$: $\%\text{reg}=\dfrac{I_{dc}R_f}{V_{FL}}=\dfrac{R_f}{R_L}=2\%$.
:::

::: ex Example 14.2: A bridge rectifier from the mains
**Given:** 230 V rms mains, a 10:1 step-down transformer, a silicon bridge (0.7 V per diode), $R_L=100\ \Omega$.

**Find:** $V_{dc}$, $I_{dc}$, PIV, ripple frequency.

**Step 1: secondary rms.** $230/10=23$ V.
**Step 2: peak.** $V_m=23\sqrt2=32.5$ V.
**Step 3: subtract two diode drops.** In each half-cycle two diodes conduct: $V_m'=32.5-2\times0.7=31.1$ V.
**Step 4: dc voltage.** $V_{dc}=\dfrac{2V_m'}{\pi}=\dfrac{2\times31.1}{3.1416}=19.8$ V.
**Step 5: dc current.** $I_{dc}=V_{dc}/R_L=19.8/100=0.198$ A.
**Step 6: PIV.** $V_{Smax}=32.5$ V; choose diodes rated at least 50 V.
**Step 7: ripple frequency** $=2\times50=100$ Hz.

**Answer:** $V_{dc}=19.8$ V, $I_{dc}=198$ mA, PIV $=32.5$ V, ripple 100 Hz.
:::

::: ex Example 14.3: A centre-tap rectifier
**Given:** a 12-0-12 V secondary (each half is 12 V rms), ideal diodes, $R_L=100\ \Omega$.

**Step 1: peak of each half.** $V_m=12\sqrt2=16.97$ V.
**Step 2: dc output.** $V_{dc}=\dfrac{2V_m}{\pi}=\dfrac{2\times16.97}{3.1416}=10.8$ V.
**Step 3: PIV.** $2V_m=33.9$ V.
**Step 4: dc current.** $I_{dc}=10.8/100=108$ mA; each diode carries on average half of this, 54 mA.

**Answer:** $V_{dc}=10.8$ V, PIV $=33.9$ V.
:::

## 14.7 Practice

::: try Questions for Chapter 14
1. What is a rectifier? Explain how a PN diode acts as a half-wave rectifier and draw the output waveform.
2. Explain the centre-tap full-wave rectifier and calculate its ripple factor.
3. Explain the bridge rectifier with a neat diagram.
4. Define ripple factor and rectification efficiency.
5. A full-wave rectifier delivers $I_{max}=200$ mA to a load $R_L=50\ \Omega$ with ideal diodes. Find $I_{dc}$, $V_{dc}$, $I_{rms}$, $P_{dc}$, $P_{ac}$ and efficiency.
6. Why is PIV $=2V_{Smax}$ for the centre-tap but $V_{Smax}$ for the bridge?
7. A half-wave rectifier has $V_m=20$ V (ideal diode), $R_L=500\ \Omega$. Find $I_{dc}$, $V_{dc}$ and $I_{rms}$.
:::

::: soln Answers and full solutions
<details markdown="1"><summary>Solution 1</summary>

**Definition:** a rectifier converts AC to (pulsating) DC.
**Working:** the diode conducts when its anode is positive (forward bias, positive half-cycle) and blocks when its anode is negative (reverse bias, negative half-cycle). So the load sees only the positive half-cycles. Output: a series of half-sine humps separated by gaps (see Figure in §14.1), with $V_{dc}=V_m/\pi$.
</details>

<details markdown="1"><summary>Solution 2</summary>

**Working:** see §14.3: $D_1$ conducts on the positive half-cycle, $D_2$ on the negative, both through $R_L$ in the same direction.
**Ripple factor:**
**Step 1.** $I_{dc}=2I_{max}/\pi$ and $I_{rms}=I_{max}/\sqrt2$.
**Step 2.** $K_f=I_{rms}/I_{dc}=\dfrac{1/\sqrt2}{2/\pi}=\dfrac{\pi}{2\sqrt2}=1.11$.
**Step 3.** $\gamma=\sqrt{K_f^2-1}=\sqrt{1.2337-1}=\sqrt{0.2337}=0.483$.

**Answer:** **0.482** (your slides round to 0.482).
</details>

<details markdown="1"><summary>Solution 3</summary>

Four diodes in a diamond; the AC source joins two opposite corners, the load the other two. Positive half-cycle: $D_1$ and $D_4$ conduct; negative half-cycle: $D_2$ and $D_3$ conduct; the current through $R_L$ has the same direction both times. Efficiency 81.2 %, ripple 0.482, PIV $=V_{Smax}$. Draw Figure in §14.4.
</details>

<details markdown="1"><summary>Solution 4</summary>

* **Ripple factor** $\gamma=\dfrac{\text{rms value of the ac component}}{\text{dc value}}=\sqrt{K_f^2-1}$. Smaller is better.
* **Efficiency** $\eta=\dfrac{P_{dc}}{P_{ac}}=\dfrac{\text{dc power delivered to the load}}{\text{ac power input}}$.
</details>

<details markdown="1"><summary>Solution 5</summary>

**Given:** $I_{max}=0.2$ A, $R_L=50\ \Omega$, ideal diodes ($R_f=0$).
**Step 1.** $I_{dc}=\dfrac{2I_{max}}{\pi}=\dfrac{0.4}{3.1416}=0.1273$ A.
**Step 2.** $V_{dc}=I_{dc}R_L=0.1273\times50=6.37$ V.
**Step 3.** $I_{rms}=\dfrac{I_{max}}{\sqrt2}=\dfrac{0.2}{1.4142}=0.1414$ A.
**Step 4.** $P_{dc}=I_{dc}^2R_L=0.1273^2\times50=0.810$ W.
**Step 5.** $P_{ac}=I_{rms}^2R_L=0.1414^2\times50=1.00$ W.
**Step 6.** $\eta=P_{dc}/P_{ac}=0.810/1.00=81.0\%$ ($8/\pi^2$).

**Answer:** $I_{dc}=127$ mA, $V_{dc}=6.37$ V, $I_{rms}=141$ mA, $P_{dc}=0.81$ W, $P_{ac}=1.0$ W, $\eta=81\%$.
</details>

<details markdown="1"><summary>Solution 6</summary>

**Centre-tap:** when $D_1$ conducts, its cathode is at $+V_{Smax}$ (the top of the winding). The bottom end of the winding is at $-V_{Smax}$, and $D_2$'s anode is there. So $D_2$ has $V_{Smax}-(-V_{Smax})=2V_{Smax}$ across it in reverse.
**Bridge:** the two conducting diodes connect the source across the two OFF diodes, so each OFF diode sees only $V_{Smax}$.
</details>

<details markdown="1"><summary>Solution 7</summary>

**Step 1.** $I_{max}=V_m/R_L=20/500=0.04$ A.
**Step 2.** $I_{dc}=I_{max}/\pi=0.04/3.1416=0.01273$ A $=12.7$ mA.
**Step 3.** $V_{dc}=I_{dc}R_L=V_m/\pi=6.37$ V.
**Step 4.** $I_{rms}=I_{max}/2=20$ mA.
</details>
:::
