# Chapter 16: BJT basics, operating point and load line (Unit II)

*Class notes p. 39 · slides: ECE BJT FOT DU (Introduction, Operating Point)*

::: kid A tap controlled by a tiny hand
A **bipolar junction transistor (BJT)** is like a big water tap controlled by a very light touch. A **small current into the base** (the light touch) controls a **much bigger current flowing from the collector to the emitter** (the big flow). If the big flow is $\beta$ times the small one, then $I_C=\beta I_B$: a transistor is a **current amplifier**. To make it work as a good amplifier we first have to “set the tap” to the middle of its range, so that the signal can swing both up and down without the tap fully closing or fully opening. That setting is called **biasing**, and the middle setting is the **Q-point** (quiescent point).
:::

## 16.1 Structure and symbols

{{fig p_bjt_struct|NPN and PNP structures. The base is thin and lightly doped; the emitter is heavily doped; the collector is larger.|92}}

* A BJT has **three regions** and **two junctions**: NPN (N-P-N) or PNP (P-N-P). Terminals: **Emitter (E)**, **Base (B)**, **Collector (C)**.
* In normal (active) operation: **emitter–base junction forward biased**, **collector–base junction reverse biased**.
* The emitter **injects** carriers into the base; because the base is very thin and lightly doped, almost all of them cross to the collector, which collects them.

## 16.2 Basic current relations

::: formula Formulas from your class notes (top of p. 39)
$$I_C=\beta I_B,\qquad I_E=(\beta+1)I_B,\qquad V_{BE}\approx0.7\text{ V (Si)}$$
:::

$$I_E=I_C+I_B,\qquad\alpha=\frac{I_C}{I_E},\qquad\beta=\frac{I_C}{I_B},\qquad\alpha=\frac{\beta}{\beta+1},\qquad\beta=\frac{\alpha}{1-\alpha}$$

Since $\beta$ is large (50–300), $I_E\approx I_C$ ($\alpha\approx1$). Example: $\beta=100$ → $\alpha=0.990$. $\alpha=0.98$ → $\beta=49$.

**Three configurations:** common-emitter (CE), common-base (CB), common-collector (CC = emitter follower). CE gives both voltage and current gain and is the workhorse of Unit II.

## 16.3 Regions of operation (from the slide)

| Region | Base–emitter junction | Base–collector junction | Behaviour |
|---|---|---|---|
| **Active (linear)** | forward | reverse | amplification: $I_C=\beta I_B$ |
| **Cut-off** | reverse | reverse | transistor **off**: $I_C\approx0$ |
| **Saturation** | forward | forward | transistor fully **on**: $V_{CE}\approx0.2$ V, $I_C$ no longer $\beta I_B$ |

{{fig p_bjt_char|Input and output characteristics of a CE transistor with the three regions marked.|92}}

* **Input characteristic** ($I_B$ vs $V_{BE}$): looks like a diode curve; knee near 0.6–0.7 V.
* **Output characteristic** ($I_C$ vs $V_{CE}$ for fixed $I_B$): nearly flat lines in the active region (a small upward slope: the Early effect, Chapter 18); saturation at small $V_{CE}$; cut-off along $I_B=0$.
* Switch use: cut-off (off) ↔ saturation (on). Amplifier use: stay in the active region.

## 16.4 Why bias? Operating point (Q-point)

* Any increase in ac voltage, current or power is the result of a **transfer of energy from the dc supplies**. So the analysis and design of any electronic amplifier has **two parts: a dc part and an ac part**.
* **Biasing** = applying dc voltages to establish a **fixed level of current and voltage**.
* For a transistor amplifier, the resulting dc current and voltage establish an **operating point** on the characteristics that defines the region used for amplification. Because it is a fixed point, it is also called the **quiescent point (Q-point)**. Class note: “Q-point: to maintain the biasing (for stabilisation).”

## 16.5 DC load line

For the CE circuit with collector resistor $R_C$ (and emitter resistor $R_E$ if present), Kirchhoff’s voltage law on the output loop gives the **dc load line**:
$$V_{CE}=V_{CC}-I_CR_C\qquad\text{or}\qquad V_{CE}=V_{CC}-I_C(R_C+R_E)$$
It is a straight line on the output characteristics with two end points:

* $I_C=0\ \Rightarrow\ V_{CE}=V_{CC}$ (**cut-off** end, on the horizontal axis).
* $V_{CE}=0\ \Rightarrow\ I_C=\dfrac{V_{CC}}{R_C}$ (or $\dfrac{V_{CC}}{R_C+R_E}$): the **saturation** end, $I_{C,sat}$ (on the vertical axis).

{{fig p_loadline|Load line for $V_{CC}=12$ V, $R_C=2.2\ \text{k}\Omega$. The Q-point is where the line meets the curve for the chosen $I_B$.|75}}

The **Q-point** is the intersection of the load line with the characteristic of the chosen $I_B$ (here $I_B=47\ \mu$A gives $I_{CQ}=2.35$ mA and $V_{CEQ}=6.82$ V; Example 17.1).

{{fig p_loadline_effects|How the Q-point and load line move when $I_B$, $R_C$ or $V_{CC}$ changes (slide Figs 4.13–4.15).|95}}

* **Raise $I_B$** → Q moves **up** the load line (toward saturation).
* **Increase $R_C$** → load line **slope becomes shallower** (the vertical intercept $V_{CC}/R_C$ falls; the horizontal one stays at $V_{CC}$).
* **Lower $V_{CC}$** → the line shifts parallel to itself toward the origin.
* **Best Q-point for an amplifier:** near the **middle of the load line**, i.e. $V_{CEQ}\approx V_{CC}/2$, so the output can swing equally up and down before clipping.

::: ex Example 16.1 (mid-point design)
Design a CE stage with $V_{CC}=12$ V, $I_{CQ}=2$ mA, $V_{CEQ}=6$ V, $\beta=100$, fixed bias. $R_C=(12-6)/2\text{ mA}=3\ \text{k}\Omega$. $I_B=I_C/\beta=20\ \mu$A. $R_B=(12-0.7)/20\ \mu\text{A}=565\ \text{k}\Omega$.
:::

::: trap Saturation check
If the computed $I_C=\beta I_B$ comes out **bigger than $I_{C,sat}$** then the transistor is in saturation and the formula $I_C=\beta I_B$ is invalid. Then $I_C\approx I_{C,sat}$ and $V_{CE}\approx0$. Example: $V_{CC}=12$ V, $R_B=100\ \text{k}\Omega$, $R_C=4.7\ \text{k}\Omega$, $\beta=200$: $I_B=113\ \mu$A, so $\beta I_B=22.6$ mA ≫ $I_{C,sat}=12/4.7\text{k}=2.55$ mA ⇒ **saturated**.
:::

## 16.6 Frequency response (class note, p. 40)

Class note: “Frequency response → characteristics between frequency and gain.” A CE amplifier’s gain is **flat (the mid-band gain)** over a range, and falls at low frequencies (because of the **coupling and bypass capacitors**) and at high frequencies (because of the transistor’s **internal capacitances**).

{{fig p_freq_resp|Typical amplifier frequency response.|62}}

## 16.7 Try it yourself

::: try Chapter 16 questions
1. Which junction is forward and which reverse in the active region? In saturation? In cut-off?
2. $\beta=150$. Find $\alpha$. If $I_B=20\ \mu$A find $I_C$ and $I_E$.
3. Draw the dc load line for $V_{CC}=15$ V, $R_C=3\ \text{k}\Omega$, $R_E=1\ \text{k}\Omega$. Give both intercepts and the mid-point Q.
4. Why must the Q-point be near the middle of the load line?

<details markdown="1"><summary>Answers</summary>

1. Active: BE forward, BC reverse. Saturation: both forward. Cut-off: both reverse.
2. $\alpha=150/151=0.9934$; $I_C=\beta I_B=3$ mA; $I_E=(\beta+1)I_B=3.02$ mA.
3. Intercepts: $V_{CE}=15$ V (at $I_C=0$) and $I_C=15/4\text{k}=3.75$ mA (at $V_{CE}=0$). Mid-point: $I_C\approx1.875$ mA, $V_{CE}\approx7.5$ V.
4. So the ac signal swing is symmetric: if Q is too close to saturation the negative half of the output clips; too close to cut-off, the positive half clips.
</details>
:::

# Chapter 17: DC biasing circuits {.chap}

*Class notes pp. 39–45 · slides: ECE BJT FOT DU (Transistor DC Bias Configurations, Summary tables)*

::: kid Six ways to set the tap
There are several circuits for “setting the tap” at the right level. Some are simple but the setting drifts if the transistor is replaced or gets hot (**fixed bias**). Others use a helper resistor or a voltage divider that automatically **pushes back** when things drift (**emitter bias, voltage divider, collector feedback**), so the setting stays put. That “staying put” is called **stability**.
:::

**Procedure every time (do this in the exam):**
1. Redraw the circuit for **dc**: replace all capacitors by **open circuits**, ac sources removed (“**open the ac terminals**” in your class notes).
2. Write KVL around the **base–emitter (input) loop** to get $I_B$.
3. $I_C=\beta I_B$, $I_E=(\beta+1)I_B\approx I_C$.
4. Write KVL around the **collector–emitter (output) loop** to get $V_{CE}$.
5. Get node voltages if asked: $V_B,V_E,V_C$, $V_{BC}=V_B-V_C$ (must be negative for the active region: BC reverse biased).

## 17.1 Fixed-bias circuit

{{fig c_fixed_bias|Fixed-bias circuit ($R_B$ from $V_{CC}$ to the base, $R_C$ in the collector).|75}}

**Base–emitter loop:** $V_{CC}-I_BR_B-V_{BE}=0$
$$\boxed{I_B=\frac{V_{CC}-V_{BE}}{R_B}}\ ,\qquad I_C=\beta I_B$$
**Collector–emitter loop:** $V_{CC}-I_CR_C-V_{CE}=0$
$$\boxed{V_{CE}=V_{CC}-I_CR_C}$$
Node voltages: $V_E=0$, $V_B=V_{BE}$, $V_C=V_{CE}$; $V_{BC}=V_B-V_C$.

**Saturation:** at saturation $V_{CE}\approx0$: $\boxed{I_{C,sat}=\dfrac{V_{CC}}{R_C}}$.

::: ex Example 17.1 (slide Ex 4.1)
$V_{CC}=12$ V, $R_B=240\ \text{k}\Omega$, $R_C=2.2\ \text{k}\Omega$, $\beta=50$. Find $I_B,I_C,V_{CE},V_B,V_C,V_{BC}$.
* $I_B=\dfrac{12-0.7}{240\text{k}}=\mathbf{47.08\ \mu A}$; $I_C=50\times47.08\ \mu\text{A}=\mathbf{2.35\ mA}$
* $V_{CE}=12-2.35\text{ mA}\times2.2\text{k}=\mathbf{6.83\ V}$
* $V_B=0.7$ V; $V_C=V_{CE}=6.83$ V; $V_{BC}=0.7-6.83=\mathbf{-6.13\ V}$ (negative ⇒ collector junction reverse-biased ✓ linear region)
:::

::: trap The big weakness of fixed bias
$I_B$ is fixed by $R_B$, but $I_C=\beta I_B$ follows **$\beta$**, which varies from one transistor to another and with temperature. For the example above, if $\beta$ doubles from 50 to 100: $I_C$ goes 2.35 → **4.71 mA** and $V_{CE}$ falls 6.83 → **1.64 V** (almost saturated). The Q-point is unstable.
:::

## 17.2 Emitter-bias (self-bias) circuit

*(Your class notes call it the **self-bias circuit (emitter bias)**.)*

{{fig c_emitter_bias|Emitter bias: an emitter resistor $R_E$ is added.|75}}

**Base–emitter loop:** $V_{CC}-I_BR_B-V_{BE}-I_ER_E=0$ with $I_E=(\beta+1)I_B$:
$$\boxed{I_B=\frac{V_{CC}-V_{BE}}{R_B+(\beta+1)R_E}}$$
The emitter resistor appears in the base loop **multiplied by $(\beta+1)$**: “reflected” resistance $R_i=(\beta+1)R_E$.

**Collector–emitter loop:** $V_{CC}-I_CR_C-V_{CE}-I_ER_E=0$ with $I_E\approx I_C$:
$$\boxed{V_{CE}=V_{CC}-I_C(R_C+R_E)}$$
$V_E=I_ER_E$, $V_B=V_{BE}+V_E$, $V_C=V_{CE}+V_E=V_{CC}-I_CR_C$.
**Saturation:** $I_{C,sat}=\dfrac{V_{CC}}{R_C+R_E}$.

**Why it is more stable:** if $I_C$ tries to rise, $V_E=I_ER_E$ rises, which **reduces $V_{BE}$ and so $I_B$**: negative feedback. The dc currents and voltages stay closer to their designed values when temperature or $\beta$ change.

::: ex Example 17.2 (slide Ex 4.4)
$V_{CC}=20$ V, $R_B=430\ \text{k}\Omega$, $R_C=2\ \text{k}\Omega$, $R_E=1\ \text{k}\Omega$, $\beta=50$.
* $I_B=\dfrac{20-0.7}{430\text{k}+51(1\text{k})}=\dfrac{19.3}{481\text{k}}=\mathbf{40.1\ \mu A}$; $I_C=50\times40.1\ \mu\text{A}=\mathbf{2.01\ mA}$
* $V_{CE}=20-2.01\text{ mA}(3\text{k})=\mathbf{13.97\ V}$
* $V_C=V_{CC}-I_CR_C=20-4.02=\mathbf{15.98\ V}$; $V_E=I_ER_E\approx\mathbf{2.01\ V}$; $V_B=0.7+2.01=\mathbf{2.71\ V}$; $V_{BC}=2.71-15.98=\mathbf{-13.27\ V}$ (reverse-biased ✓)
* Stability: with $\beta=100$: $I_C=3.63$ mA (only +81 %, versus +100 % for fixed bias) and $V_{CE}=9.1$ V (falls 35 %, versus 76 % for fixed bias).
:::

## 17.3 Voltage-divider bias

{{fig c_vdiv|Voltage-divider bias: $R_1$ and $R_2$ set the base voltage.|75}}

The best-known stable circuit. Two methods: **exact** (Thévenin) and **approximate**.

### Exact analysis (Thévenin’s theorem, as in your class notes)

{{fig c_thevenin|Replacing the divider by $E_{Th}$ and $R_{Th}$ as seen from the base.|68}}

$$R_{Th}=R_1\parallel R_2=\frac{R_1R_2}{R_1+R_2},\qquad E_{Th}=\frac{R_2}{R_1+R_2}V_{CC}$$
KVL on the base loop: $E_{Th}-I_BR_{Th}-V_{BE}-I_ER_E=0$, $I_E=(\beta+1)I_B$:
$$\boxed{I_B=\frac{E_{Th}-V_{BE}}{R_{Th}+(\beta+1)R_E}},\qquad I_C=\beta I_B,\qquad\boxed{V_{CE}=V_{CC}-I_C(R_C+R_E)}$$

### Approximate analysis

Valid when $R_i=(\beta+1)R_E\approx\beta R_E\ \ge\ 10R_2$ (the base current is small compared with the divider current, so the divider is not “loaded”). Then:
$$V_B=\frac{R_2}{R_1+R_2}V_{CC},\qquad V_E=V_B-V_{BE},\qquad I_E=\frac{V_E}{R_E}\approx I_C,\qquad V_{CE}=V_{CC}-I_C(R_C+R_E)$$
Now $\beta$ does not appear at all, so $I_C$ hardly depends on $\beta$. **Saturation:** $I_{C,sat}=\dfrac{V_{CC}}{R_C+R_E}$.

::: ex Example 17.3 (slide Ex 4.11: approximation fails, so compare)
$V_{CC}=18$ V, $R_1=82\ \text{k}\Omega$, $R_2=22\ \text{k}\Omega$, $R_C=5.6\ \text{k}\Omega$, $R_E=1.2\ \text{k}\Omega$, $\beta=50$.

Test: $\beta R_E=60$ k vs $10R_2=220$ k: **60 k < 220 k ⇒ condition not satisfied.**

*Exact:* $R_{Th}=82\parallel22=17.35\text{ k}\Omega$, $E_{Th}=\dfrac{22\times18}{104}=3.81$ V.
$I_B=\dfrac{3.81-0.7}{17.35\text{k}+51(1.2\text{k})}=\dfrac{3.11}{78.55\text{k}}=39.6\ \mu\text{A}$; $I_{CQ}=\mathbf{1.98\ mA}$; $V_{CEQ}=18-1.98\text{ m}(6.8\text{k})=\mathbf{4.54\ V}$.

*Approximate:* $V_B=3.81$ V, $V_E=3.11$ V, $I_E=3.11/1.2\text{k}=\mathbf{2.59\ mA}$, $V_{CE}=18-2.59\text{ m}(6.8\text{k})=\mathbf{3.88\ V}$.

| | $I_{CQ}$ | $V_{CEQ}$ |
|---|---|---|
| Exact | 1.98 mA | 4.54 V |
| Approximate | 2.59 mA | 3.88 V |

The approximation is 30 % off in $I_C$ because the condition fails; when $\beta R_E\ge10R_2$ the two agree closely.
:::

::: ex Example 17.4 (approximation valid)
$V_{CC}=20$ V, $R_1=47\ \text{k}\Omega$, $R_2=10\ \text{k}\Omega$, $R_C=3.3\ \text{k}\Omega$, $R_E=2\ \text{k}\Omega$, $\beta=100$. Test: $\beta R_E=200\text{k}\ge10R_2=100\text{k}$ ✓.
* Approx: $V_B=\dfrac{10\times20}{57}=3.51$ V, $V_E=2.81$ V, $I_E=1.40$ mA, $V_{CE}=20-1.40\text{ m}(5.3\text{k})=\mathbf{12.6\ V}$.
* Exact: $R_{Th}=8.25\text{k}$, $I_B=\dfrac{3.51-0.7}{8.25\text{k}+101(2\text{k})}=13.4\ \mu$A, $I_C=1.34$ mA, $V_{CE}=\mathbf{12.9\ V}$ (close ✓).
* Stability: doubling $\beta$ to 200 changes $I_C$ from 1.336 to only **1.369 mA (+2.5 %)**, compared with +100 % for fixed bias. That is what a good bias circuit does.
:::

## 17.4 Collector-feedback bias

{{fig c_coll_fb|Collector feedback: $R_F$ connects the collector to the base.|75}}

$R_F$ feeds a fraction of the collector voltage back to the base: if $I_C$ rises, $V_C$ falls, which reduces $I_B$ (negative feedback).

Let $I_C'=I_C+I_B\approx I_C\approx I_E$ (since $I_B$ is very small). KVL on the base–emitter loop:
$$V_{CC}-I_C'R_C-I_BR_F-V_{BE}-I_ER_E=0\ \Rightarrow\ V_{CC}-I_BR_F-V_{BE}-\beta I_B(R_C+R_E)=0$$
$$\boxed{I_B=\frac{V_{CC}-V_{BE}}{R_F+\beta(R_C+R_E)}},\qquad I_C=\beta I_B,\qquad\boxed{V_{CE}=V_{CC}-I_C(R_C+R_E)}$$
**Saturation:** $I_{C,sat}=\dfrac{V_{CC}}{R_C+R_E}$. The load line is the same as for the voltage-divider and emitter-bias circuits; only the $I_{BQ}$ formula depends on the circuit.

::: ex Example 17.5 (slide Ex 4.14)
$V_{CC}=18$ V, $R_C=3.3\ \text{k}\Omega$, $R_E=510\ \Omega$, $R_F=R_{F1}+R_{F2}=91\text{k}+110\text{k}=201\ \text{k}\Omega$ (the capacitor at their junction is open for dc), $\beta=75$.
$I_B=\dfrac{18-0.7}{201\text{k}+75(3.3\text{k}+0.51\text{k})}=\dfrac{17.3}{486.75\text{k}}=\mathbf{35.5\ \mu A}$; $I_C=75\times35.5\ \mu=\mathbf{2.66\ mA}$; $V_C=18-2.66\text{ m}(3.3\text{k})=\mathbf{9.22\ V}$.
:::

## 17.5 Emitter-follower (common-collector) bias

{{fig c_emitter_follower|Emitter follower: collector at dc ground (0 V), emitter resistor to $-V_{EE}$, output taken from the emitter.|75}}

Input loop: $-I_BR_B-V_{BE}-I_ER_E+V_{EE}=0$ with $I_E=(\beta+1)I_B$:
$$\boxed{I_B=\frac{V_{EE}-V_{BE}}{R_B+(\beta+1)R_E}},\qquad I_E=(\beta+1)I_B$$
Output loop: $-V_{CE}-I_ER_E+V_{EE}=0$:
$$\boxed{V_{CE}=V_{EE}-I_ER_E}$$

::: ex Example 17.6 (slide Ex 4.16)
$V_{EE}=20$ V, $R_B=240\ \text{k}\Omega$, $R_E=2\ \text{k}\Omega$, $\beta=90$. $I_B=\dfrac{20-0.7}{240\text{k}+91(2\text{k})}=\mathbf{45.73\ \mu A}$; $I_E=91\times45.73\ \mu=\mathbf{4.16\ mA}$; $V_{CE}=20-4.16\text{ m}(2\text{k})=\mathbf{11.68\ V}$.
:::

## 17.6 Common-base bias

{{fig c_common_base|Common-base configuration: input at the emitter, base grounded, output at the collector.|78}}

Input loop: $-V_{EE}+I_ER_E+V_{BE}=0$:
$$\boxed{I_E=\frac{V_{EE}-V_{BE}}{R_E}},\qquad I_C\approx I_E,\qquad I_B=\frac{I_E}{\beta+1}$$
Whole circuit: $-V_{EE}+I_ER_E+V_{CE}+I_CR_C-V_{CC}=0$:
$$\boxed{V_{CE}=V_{EE}+V_{CC}-I_E(R_C+R_E)},\qquad\boxed{V_{CB}=V_{CC}-I_CR_C}$$

::: ex Example 17.7 (slide Ex 4.17)
$V_{EE}=4$ V, $V_{CC}=10$ V, $R_E=1.2\ \text{k}\Omega$, $R_C=2.4\ \text{k}\Omega$, $\beta=60$. $I_E=\dfrac{4-0.7}{1.2\text{k}}=\mathbf{2.75\ mA}$; $I_B=\dfrac{2.75\text{ mA}}{61}=\mathbf{45.08\ \mu A}$; $V_{CE}=4+10-2.75\text{ m}(3.6\text{k})=\mathbf{4.1\ V}$; $V_{CB}=10-60(45.08\ \mu)(2.4\text{k})=\mathbf{3.51\ V}$ (positive: the collector junction is reverse biased for an NPN ✓).
:::

## 17.7 Miscellaneous configurations

::: ex Example 17.8 (slide Ex 4.18: collector feedback without $R_E$)
$V_{CC}=20$ V, $R_C=4.7\ \text{k}\Omega$, $R_B=680\ \text{k}\Omega$ connected from the **collector to the base**, $\beta=120$, no emitter resistor. The absence of $R_E$ simply removes it from the equation: $I_B=\dfrac{V_{CC}-V_{BE}}{R_B+\beta R_C}=\dfrac{19.3}{680\text{k}+120(4.7\text{k})}=\dfrac{19.3}{1.244\text{M}}=\mathbf{15.51\ \mu A}$; $I_C=\beta I_B=\mathbf{1.86\ mA}$; $V_{CE}=20-1.86\text{ m}(4.7\text{k})=\mathbf{11.26\ V}$; $V_B=0.7$ V, $V_C=11.26$ V, $V_E=0$, $V_{BC}=-10.56$ V.
:::

::: ex Example 17.9 (slide Ex 4.19: NPN with a negative emitter supply)
$V_{EE}=-9$ V at the emitter, $R_B=100\ \text{k}\Omega$ (base to ground), $R_C=1.2\ \text{k}\Omega$ (collector to ground), $\beta=45$. Base loop: $I_B=\dfrac{9-0.7}{100\text{k}}=\mathbf{83\ \mu A}$; $I_C=45\times83\ \mu=\mathbf{3.735\ mA}$; $V_C=-I_CR_C=\mathbf{-4.48\ V}$; $V_B=-I_BR_B=\mathbf{-8.3\ V}$ (0.7 V above the emitter at $-9$ V ✓). Nothing special: “negative” supplies just shift the reference level; the method is unchanged. For a PNP transistor all currents and polarities reverse.
:::

## 17.8 Summary table (slides)

| Configuration | $I_B$ | Other equations |
|---|---|---|
| Fixed bias | $\dfrac{V_{CC}-V_{BE}}{R_B}$ | $I_C=\beta I_B$; $V_{CE}=V_{CC}-I_CR_C$ |
| Emitter bias | $\dfrac{V_{CC}-V_{BE}}{R_B+(\beta+1)R_E}$ | $V_{CE}=V_{CC}-I_C(R_C+R_E)$; $R_i=(\beta+1)R_E$ |
| Voltage divider (exact) | $\dfrac{E_{Th}-V_{BE}}{R_{Th}+(\beta+1)R_E}$, $R_{Th}=R_1\|R_2$, $E_{Th}=\frac{R_2V_{CC}}{R_1+R_2}$ | $V_{CE}=V_{CC}-I_C(R_C+R_E)$ |
| Voltage divider (approx., $\beta R_E\ge10R_2$) | – | $V_B=\frac{R_2V_{CC}}{R_1+R_2}$; $V_E=V_B-V_{BE}$; $I_E=V_E/R_E$ |
| Collector feedback | $\dfrac{V_{CC}-V_{BE}}{R_F+\beta(R_C+R_E)}$ | $V_{CE}=V_{CC}-I_C(R_C+R_E)$ |
| Emitter follower | $\dfrac{V_{EE}-V_{BE}}{R_B+(\beta+1)R_E}$ | $V_{CE}=V_{EE}-I_ER_E$ |
| Common base | $I_E=\dfrac{V_{EE}-V_{BE}}{R_E}$ | $V_{CE}=V_{EE}+V_{CC}-I_E(R_C+R_E)$; $V_{CB}=V_{CC}-I_CR_C$ |

**Stability ranking (best → worst):** voltage divider ≳ collector feedback / emitter bias ≫ fixed bias.

## 17.9 Quick sanity checks <span class="tag">extra</span>

* Active region ⇒ $V_{BE}\approx0.7$ V and $V_{CE}>0.2$ V, and (NPN) $V_{BC}<0$.
* $V_{CE}\approx0.2$ V or less ⇒ **saturated**. $V_{CE}\approx V_{CC}$ (or $I_C\approx0$) ⇒ **cut-off**.
* $I_C$ cannot exceed $I_{C,sat}=V_{CC}/(R_C+R_E)$.

## 17.10 Try it yourself

::: try Chapter 17 questions
1. Fixed bias: $V_{CC}=15$ V, $R_B=470\ \text{k}\Omega$, $R_C=3.3\ \text{k}\Omega$, $\beta=100$. Find $I_B$, $I_C$, $V_{CE}$. Is it saturated?
2. Emitter bias: $V_{CC}=12$ V, $R_B=330\ \text{k}\Omega$, $R_C=2.2\ \text{k}\Omega$, $R_E=470\ \Omega$, $\beta=100$. Find $I_C$, $V_{CE}$, $V_E$.
3. Voltage divider: $V_{CC}=12$ V, $R_1=33\ \text{k}\Omega$, $R_2=6.8\ \text{k}\Omega$, $R_C=2.2\ \text{k}\Omega$, $R_E=1\ \text{k}\Omega$, $\beta=100$. Check the approximation condition, then find $I_C$ and $V_{CE}$ (approximate).
4. Collector feedback: $V_{CC}=10$ V, $R_C=2\ \text{k}\Omega$, $R_F=200\ \text{k}\Omega$, $R_E=0$, $\beta=100$. Find $I_C$, $V_{CE}$.
5. Explain in words why emitter resistance improves stability.

<details markdown="1"><summary>Answers</summary>

1. $I_B=(15-0.7)/470\text{k}=30.4\ \mu$A; $I_C=3.04$ mA; $V_{CE}=15-3.04\times3.3=\mathbf{4.97\ V}$; $I_{C,sat}=15/3.3\text{k}=4.55$ mA > 3.04 mA ⇒ **not saturated**.
2. $I_B=\dfrac{11.3}{330\text{k}+101(0.47\text{k})}=\dfrac{11.3}{377.5\text{k}}=29.9\ \mu$A; $I_C=\mathbf{2.99\ mA}$; $V_{CE}=12-2.99(2.67)=\mathbf{4.02\ V}$; $V_E=I_ER_E=3.02\times0.47=\mathbf{1.42\ V}$.
3. $\beta R_E=100\text{k}$ vs $10R_2=68\text{k}$ ⇒ condition satisfied. $V_B=\dfrac{6.8\times12}{39.8}=2.05$ V; $V_E=1.35$ V; $I_E=1.35$ mA ≈ $I_C$; $V_{CE}=12-1.35(3.2)=\mathbf{7.68\ V}$.
4. $I_B=\dfrac{10-0.7}{200\text{k}+100(2\text{k})}=\dfrac{9.3}{400\text{k}}=23.25\ \mu$A; $I_C=\mathbf{2.325\ mA}$; $V_{CE}=10-2.325\times2=\mathbf{5.35\ V}$.
5. If $I_C$ rises, $V_E=I_ER_E$ rises, reducing $V_{BE}$ (=$V_B-V_E$) and therefore $I_B$, which pushes $I_C$ back down (negative feedback), so the Q-point moves less when $\beta$ or temperature changes.
</details>
:::
