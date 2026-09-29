# Chapter 14: Rectifiers

*Class notes pp. 29–32 · slides: Rectifiers, half-wave rectifier*

::: kid Turning a see-saw into a river
The mains socket gives **alternating current (AC)**: the electricity flows one way, then the other, 50 times per second, like a see-saw. Your phone charger needs **direct current (DC)**: flowing one way only, like a river. A **rectifier** is a set of one-way doors (diodes) that catches the backward half of the see-saw and flips it (or throws it away), so everything flows the same way. The result is bumpy (like waves on a river), so we add a **filter** (Chapter 15) to smooth it.
:::

## 14.1 Rectification

*Rectification* = converting AC to DC using the fact that a diode has **low resistance in forward bias and high resistance in reverse bias**. Types: **half-wave** (uses one half-cycle) and **full-wave** (uses both half-cycles). Full-wave can be built two ways: **centre-tap** and **bridge**.

{{fig p_rect_waves|Input, half-wave output and full-wave output. Dashed red line = the average (dc) value.|85}}

## 14.2 Half-wave rectifier (HWR)

{{fig c_hwr|Half-wave rectifier: source (transformer secondary), one diode, load $R_L$.|72}}

**Circuit:** a step-down transformer, a diode in series with the secondary, and the load $R_L$ on the diode’s cathode side.

* **Positive half-cycle:** the diode is forward biased and conducts (above the knee voltage). Current flows anode → cathode through $R_L$: the positive half-cycle appears across the load.
* **Negative half-cycle:** the diode is reverse biased and does not conduct: no load current and no load voltage.
* Output = **pulsating dc** (positive half-cycles only), with a large ac (“ripple”) component.

### Analysis

Secondary voltage $v_s=V_{Smax}\sin\omega t$. Diode forward resistance $R_f$, ideal reverse resistance. Then
$$i=I_{max}\sin\omega t\ \ (0\le\omega t\le\pi),\qquad i=0\ \ (\pi\le\omega t\le2\pi),\qquad I_{max}=\frac{V_{Smax}}{R_f+R_L}$$

1. **PIV** (peak inverse voltage across the diode): in the negative half-cycle no current flows, so no drop across $R_L$ and the *entire* secondary peak appears across the diode:
$$\boxed{PIV=V_{Smax}}$$
2. **Average (dc) current**
$$I_{dc}=\frac1{2\pi}\int_0^{2\pi}i\,d(\omega t)=\frac{I_{max}}{2\pi}\int_0^\pi\sin\omega t\,d(\omega t)=\frac{I_{max}}{2\pi}\cdot2=\boxed{\frac{I_{max}}{\pi}=0.318\,I_{max}}$$
With $I_{max}=V_{Smax}/(R_f+R_L)$: $I_{dc}=\dfrac{V_{Smax}}{\pi(R_f+R_L)}$; if $R_L\gg R_f$: $I_{dc}=\dfrac{V_{Smax}}{\pi R_L}$.
3. **DC output voltage**
$$V_{dc}=I_{dc}R_L=\frac{I_{max}R_L}{\pi}=\frac{V_{Smax}}{\pi\left(1+\frac{R_f}{R_L}\right)}\ \xrightarrow{R_L\gg R_f}\ \boxed{V_{dc}=\frac{V_{Smax}}{\pi}}$$
4. **RMS current**
$$I_{rms}=\sqrt{\frac1{2\pi}\int_0^{\pi}I_{max}^2\sin^2\omega t\,d(\omega t)}=\sqrt{\frac{I_{max}^2}{4\pi}\cdot\pi}=\boxed{\frac{I_{max}}{2}}=\frac{V_{Smax}}{2(R_f+R_L)}$$
5. **RMS load voltage** $V_{L,rms}=I_{rms}R_L=\dfrac{V_{Smax}R_L}{2(R_f+R_L)}\to\boxed{\dfrac{V_{Smax}}2}$ for $R_L\gg R_f$.
6. **Rectification efficiency** $\eta=\dfrac{P_{dc}}{P_{ac}}$:
   * $P_{dc}=I_{dc}^2R_L=\left(\dfrac{I_{max}}{\pi}\right)^2R_L$
   * $P_{ac}$ = power in diode junction + load $=I_{rms}^2R_f+I_{rms}^2R_L=\dfrac{I_{max}^2}{4}(R_f+R_L)$
$$\eta=\frac{4}{\pi^2}\frac{R_L}{R_f+R_L}=\frac{0.406}{1+R_f/R_L}\ \xrightarrow{R_f\to0}\ \boxed{\eta_{max}\approx40.6\%}$$
7. **Ripple factor** $\gamma=\dfrac{I_{ac}}{I_{dc}}$ (the ratio of the rms value of the ac component to the dc component). Since $I_{rms}^2=I_{dc}^2+I_{ac}^2$:
$$\gamma=\frac{\sqrt{I_{rms}^2-I_{dc}^2}}{I_{dc}}=\sqrt{K_f^2-1},\qquad K_f=\frac{I_{rms}}{I_{dc}}=\frac{I_{max}/2}{I_{max}/\pi}=\frac\pi2=1.57\ \Rightarrow\ \boxed{\gamma=1.21}$$
$K_f$ is the **form factor**.

::: flag 40.5% or 40.6%?
Exactly $4/\pi^2=0.4053$ (40.5%). Your slides round it as **40.6%**; your class solution uses **40.5**. Both are accepted; quote the value your question paper’s method uses.
:::

**Disadvantages of the half-wave rectifier (slides):**
1. Output contains, besides dc, an ac component at the **input frequency**, so ripple is high and heavy filtering is needed.
2. **Low efficiency** (power is delivered only in one half-cycle).
3. **Low transformer utilisation factor.**
4. **dc saturation of the transformer core**, causing magnetising current, hysteresis loss and harmonics.

## 14.3 Centre-tap full-wave rectifier

{{fig c_ct_fwr|Centre-tap full-wave rectifier: two diodes, a centre-tapped transformer; each diode conducts on alternate half-cycles and both send current the same way through $R_L$.|78}}

* **Two diodes** connected to the two ends of a **centre-tapped secondary**; the centre tap is the ground (zero-volt) reference.
* **Positive half-cycle** (top end $P_1$ positive): $D_1$ forward biased, $D_2$ reverse biased. Current path: $P_1\to D_1\to R_L\to$ centre tap.
* **Negative half-cycle** ($P_2$ positive): $D_2$ conducts, $D_1$ is off. Path: $P_2\to D_2\to R_L\to$ centre tap.
* The current through $R_L$ has the **same direction in both half-cycles**. The output frequency is **twice** the input frequency. Output = dc plus small ac components.

**Analysis** (each half of the secondary gives peak $V_{Smax}$; one diode conducts at a time, so $I_{max}=V_{Smax}/(R_f+R_L)$):

| Quantity | Result |
|---|---|
| **PIV** | when $D_1$ conducts (ideal, zero drop) the whole secondary voltage $2V_{Smax}$ appears across $D_2$: $\boxed{PIV=2V_{Smax}}$ |
| $I_{dc}$ | $\dfrac1\pi\int_0^\pi I_{max}\sin\omega t\,d(\omega t)=\dfrac{2I_{max}}{\pi}=0.636I_{max}$ |
| $V_{dc}$ | $I_{dc}R_L=\dfrac{2I_{max}R_L}\pi\to\dfrac{2V_{Smax}}{\pi}$ |
| $I_{rms}$ | $\sqrt{\dfrac1\pi\int_0^\pi I_{max}^2\sin^2\omega t\,d(\omega t)}=\dfrac{I_{max}}{\sqrt2}$ |
| $V_{L,rms}$ | $\dfrac{I_{max}}{\sqrt2}R_L$ |
| $P_{dc}$ | $\dfrac{4}{\pi^2}I_{max}^2R_L$ |
| $P_{ac}$ | $I_{rms}^2(R_f+R_L)=\dfrac{I_{max}^2}{2}(R_f+R_L)$ |
| Efficiency | $\eta=\dfrac{8}{\pi^2}\dfrac{R_L}{R_f+R_L}=\dfrac{0.812}{1+R_f/R_L}$ → **81.2 %** max (twice the HWR) |
| Form factor | $K_f=\dfrac{I_{max}/\sqrt2}{2I_{max}/\pi}=\dfrac{\pi}{2\sqrt2}=1.11$ |
| Ripple factor | $\gamma=\sqrt{K_f^2-1}=\sqrt{1.11^2-1}=\mathbf{0.482}$ |

(Your class notes derive $V_{dc}$ and $V_{rms}$ for a full-wave sine directly: $V_{dc}=\frac1\pi\!\int_0^\pi V_m\sin\theta\,d\theta=\frac{2V_m}{\pi}$ and $V_{rms}=\frac{V_m}{\sqrt2}$, and quote $\gamma=I_{ac}/I_{dc}=0.481$.)

## 14.4 Full-wave bridge rectifier

{{fig c_bridge|Bridge rectifier: four diodes; the load is connected across the “other” diagonal of the AC source.|65}}

* **Four diodes** in a bridge. The ac source is connected to two opposite corners; the load $R_L$ to the other two.
* **Positive half-cycle** (top of source positive): one diagonal pair conducts ($D_1$ and $D_4$ in the drawing); **negative half-cycle:** the other diagonal pair ($D_2$ and $D_3$). Current flows through $R_L$ in the **same direction** both times.
* Works with or without a transformer; if a transformer is used any ordinary secondary will do (**no centre tap**).

Only two differences from the centre-tap analysis:
* **Two diodes conduct in each half-cycle**, so the total forward resistance is $2R_f$: $I_{max}=\dfrac{V_{Smax}}{2R_f+R_L}$ and $\eta=\dfrac{0.812}{1+2R_f/R_L}$.
* $V_{Smax}$ is now the peak of the **whole** secondary (in the centre-tap circuit it is the peak of **half** the secondary).
* The diodes only have to withstand the peak of the secondary: $\boxed{PIV=V_{Smax}}$ (in the bridge, the non-conducting diodes see $V_{Smax}$ because the two conducting ones short the source across them).

(The output waveform is the same as for the centre-tap circuit: see the figure in §14.1.)

## 14.5 Comparison table

| | Half-wave | Centre-tap FWR | Bridge FWR |
|---|---|---|---|
| Diodes | 1 | 2 | 4 |
| Transformer | ordinary | **centre-tapped** | ordinary (or none) |
| $I_{dc}$ | $I_{max}/\pi$ | $2I_{max}/\pi$ | $2I_{max}/\pi$ |
| $V_{dc}$ (ideal, $R_L\gg R_f$) | $V_{Smax}/\pi$ | $2V_{Smax}/\pi$ | $2V_{Smax}/\pi$ |
| $I_{rms}$ | $I_{max}/2$ | $I_{max}/\sqrt2$ | $I_{max}/\sqrt2$ |
| **PIV** | $V_{Smax}$ | $2V_{Smax}$ | $V_{Smax}$ |
| Ripple frequency | $f$ | $2f$ | $2f$ |
| Form factor $K_f$ | 1.57 | 1.11 | 1.11 |
| **Ripple factor** | **1.21** | **0.482** | **0.482** |
| Max efficiency | 40.6 % | 81.2 % | 81.2 % |
| $\eta$ with diode resistance | $\dfrac{0.406}{1+R_f/R_L}$ | $\dfrac{0.812}{1+R_f/R_L}$ | $\dfrac{0.812}{1+2R_f/R_L}$ |
| TUF <span class="tag">extra</span> | 0.287 | 0.693 | 0.812 |

::: flag Your class page and $\eta$
Class page 32 writes $\eta=\dfrac{0.812}{1+2R_f/R_L}$ right after $P_{ac}=\dfrac{I_{max}^2}{2}(R_f+R_L)$ (the centre-tap expression). With that $P_{ac}$ the result is $\dfrac{0.812}{1+R_f/R_L}$; the “$2R_f$” version belongs to the **bridge** (two diodes in series). Know both and label them correctly. Also, $8/\pi^2=0.8106$, which the slides round to 0.812.
:::

**Merits of full-wave over half-wave (slides):** double efficiency (both half-cycles used); very low residual ripple (a simple filter is enough); higher transformer utilisation factor (TUF) and output power. **Demerit:** more circuit elements, costlier.

**Bridge over centre-tap:** *Merits:* no special (centre-tapped, costly) transformer; can be built with or without a transformer; suits **high-voltage** applications (its PIV is half that of the centre-tap for the same output); higher TUF. *Demerits:* **4 diodes**; two conduct at once, so the voltage drop across diodes is **double** (0.7 V × 2), which matters at low voltages.

::: kid Which rectifier would you pick?
* Tiny cheap gadget, ripple doesn’t matter: **half-wave**.
* Low-voltage supply with a transformer that already has a centre tap: **centre-tap** (only one diode drop).
* High voltage, or no centre-tapped transformer: **bridge**.
:::

## 14.6 Solved problems

::: ex Example 14.1 (your class problem, worked both ways)
*A half-wave rectifier uses a diode with internal resistance 20 Ω and load $R_L=1\ \text{k}\Omega$. A 4:1 transformer is used and the primary voltage is 220 V rms at 50 Hz. Calculate dc output current and voltage, ac output current and voltage, PIV, efficiency and regulation.*

Secondary: $220/4=55$ V. $I_{max}=V_m/(R_f+R_L)=V_m/1020$.

| Quantity | **Class page** ($V_m=110$ V) | **Strict** ($55$ V rms secondary ⇒ $V_m=55\sqrt2=77.8$ V) |
|---|---|---|
| $I_{max}$ | 0.1078 A (page: 0.107) | 76.3 mA |
| $I_{dc}=I_{max}/\pi$ | **0.0343 A** (page: 0.034) | **24.3 mA** |
| $V_{dc}=I_{dc}R_L$ | 34.3 V (page: 35.01, then 32) | **24.3 V** |
| $I_{rms}=I_{max}/2$ | 0.0539 A (page: 0.05) | 38.1 mA |
| $V_{rms}$ across load | 53.9 V | 38.1 V |
| ac component $I_{ac}=\gamma I_{dc}$, $\gamma=1.21$ | 0.0415 A (page: 0.0411) | 29.4 mA |
| $P_{dc}=I_{dc}^2R_L$ | 1.18 W (page: 1.01) | 0.589 W |
| $P_{ac}=I_{max}^2(R_f+R_L)/4$ | 2.97 W | 1.48 W |
| **PIV** | **110 V** | **77.8 V** |
| **Efficiency** $\eta=40.6\cdot\dfrac{R_L}{R_L+R_f}$ | $40.5\times\dfrac{1000}{1020}=$ **39.7 %** | **39.7 %** (independent of $V_m$) |
| **Regulation** $=\dfrac{R_f}{R_L}\times100$ | **2 %** | **2 %** |

::: flag Why two columns?
The class solution writes “$V_m/2=V_{rms}=55$ ⇒ $V_m=110$ V”. That uses the HWR *output* relation $V_{rms}=V_m/2$ on a number (55 V) that is the *transformer secondary* rms voltage of a sinusoid, for which $V_m=\sqrt2\,V_{rms}$. The strict value is 77.8 V. **Efficiency, ripple factor and regulation do not depend on $V_m$**, so those come out the same either way. If your teacher’s answer key uses 110 V, write the method she used; mention the $\sqrt2$ version if the question says “55 V rms”. Also note the class page’s $V_{dc}=32$ V is inconsistent with $I_{dc}R_L=34.3$ V and $V_m/\pi=35.0$ V.
:::

**Regulation** here means the drop in dc output voltage from no-load to full-load: $\%\text{reg}=\dfrac{V_{NL}-V_{FL}}{V_{FL}}\times100$. $V_{NL}=V_m/\pi$; $V_{FL}=V_m/\pi-I_{dc}R_f$, so $\%\text{reg}=\dfrac{I_{dc}R_f}{V_{FL}}=\dfrac{R_f}{R_L}=\dfrac{20}{1000}=2\%$.
:::

::: ex Example 14.2 (bridge)
230 V rms mains, 10:1 step-down, silicon bridge, $R_L=100\ \Omega$. Secondary $=23$ V rms → $V_m=23\sqrt2=32.5$ V. Two silicon diodes conduct: $V_{m,eff}=32.5-2(0.7)=31.1$ V.
$$V_{dc}=\frac{2\times31.1}{\pi}=\mathbf{19.8\ V},\quad I_{dc}=\mathbf{198\ mA},\quad PIV=V_{Smax}=\mathbf{32.5\ V}\ (\text{choose a diode rated}\ge50\text{ V}),\quad f_{ripple}=100\text{ Hz}.$$
:::

::: ex Example 14.3 (centre-tap)
12–0–12 V secondary (12 V rms each half). $V_m=12\sqrt2=16.97$ V per half. Ideal: $V_{dc}=2V_m/\pi=\mathbf{10.8\ V}$; $PIV=2V_m=\mathbf{33.9\ V}$. With $R_L=100\ \Omega$: $I_{dc}=108$ mA and each diode carries $I_{dc}/2$ on average (54 mA).
:::

## 14.7 Assignment questions (the last slide of the Filters deck)

::: try Chapter 14 questions
1. What is a rectifier? Explain how a PN junction diode acts as a half-wave rectifier. Draw the output waveform.
2. Explain the centre-tap full-wave rectifier and calculate its ripple factor.
3. Explain the bridge rectifier with a neat diagram.
4. Define ripple factor and rectification efficiency.
5. A full-wave rectifier delivers $I_{max}=200$ mA to a load $R_L=50\ \Omega$ with ideal diodes. Find $I_{dc}$, $V_{dc}$, $I_{rms}$, $P_{dc}$, $P_{ac}$, $\eta$.
6. Why is PIV = $2V_{Smax}$ for the centre-tap but $V_{Smax}$ for the bridge?

<details markdown="1"><summary>Answers</summary>

1. See §14.1–14.2: a rectifier converts ac to dc; the diode conducts only in forward-bias (positive half-cycle) and blocks in reverse; the output is pulsating dc with only positive half-cycles.
2. §14.3; $\gamma=\sqrt{K_f^2-1}=0.482$ with $K_f=\pi/(2\sqrt2)=1.11$.
3. §14.4: diagonal pairs conduct alternately.
4. Ripple factor $\gamma=I_{ac,rms}/I_{dc}$ (smaller is better). Efficiency $\eta=P_{dc}/P_{ac}$ (dc power to the load ÷ ac input power).
5. $I_{dc}=2I_{max}/\pi=127.3$ mA; $V_{dc}=I_{dc}R_L=6.37$ V; $I_{rms}=I_{max}/\sqrt2=141.4$ mA; $P_{dc}=I_{dc}^2R_L=0.810$ W; $P_{ac}=I_{rms}^2R_L=1.0$ W; $\eta=81.06\%$ (=$8/\pi^2$).
6. Centre-tap: when $D_1$ conducts, its cathode is at $+V_{Smax}$ and the other end of the winding is at $-V_{Smax}$, so $D_2$ sees $2V_{Smax}$. Bridge: the two conducting diodes clamp the source across the two off diodes, which see only $V_{Smax}$.
</details>
:::
