# Chapter 16: BJT basics, operating point and load line (Unit II)

*Class notes p. 39 · slides: ECE BJT FOT DU (Introduction, Operating Point)*

::: words
| Word / symbol | Plain meaning |
|---|---|
| BJT | Bipolar Junction Transistor: a 3-layer device that amplifies or switches |
| NPN / PNP | layer order (N-P-N or P-N-P). NPN is used in most examples |
| E, B, C | **Emitter**, **Base**, **Collector** terminals |
| $I_B$, $I_C$, $I_E$ | base, collector, emitter currents. $I_E=I_C+I_B$ |
| $V_{BE}$ | voltage from base to emitter: about **0.7 V** for silicon in normal operation |
| $V_{CE}$ | voltage from collector to emitter |
| $V_{CC}$ | the collector supply voltage |
| $\beta$ | **current gain** $I_C/I_B$ (typically 50–300) |
| $\alpha$ | $I_C/I_E$ (just under 1) |
| CE, CB, CC | common-emitter, common-base, common-collector configurations |
| Biasing | applying dc voltages to fix the transistor's resting current and voltage |
| Q-point | **quiescent point**: the resting $(V_{CE},I_C)$ with no signal |
| Active (linear) region | normal amplifying region |
| Cut-off | transistor OFF ($I_C\approx0$) |
| Saturation | transistor fully ON ($V_{CE}\approx0.2$ V) |
| Load line | straight line showing every $(V_{CE},I_C)$ the circuit allows |
| $I_{C,sat}$ | the largest collector current the circuit can allow ($V_{CC}/R_C$) |
| $R_C$, $R_E$, $R_B$ | collector, emitter and base resistors |
| Mid-band, frequency response | gain against frequency; flat in the middle |
:::

::: kid A tap controlled by a tiny hand
A **bipolar junction transistor (BJT)** is like a big water tap controlled by a very light touch. A **small current into the base** (the light touch) controls a **much bigger current from the collector to the emitter** (the big flow). If the big flow is $\beta$ times the small one, then $I_C=\beta I_B$: a transistor is a **current amplifier**. To make it work as a good amplifier we first **set the tap** to the middle of its range so the signal can swing both up and down without the tap fully closing or fully opening. That setting is **biasing**, and the middle setting is the **Q-point**.
:::

## 16.1 Structure and symbols

{{fig p_bjt_struct|NPN and PNP structures. The base is thin and lightly doped; the emitter is heavily doped; the collector is larger.|92}}

* A BJT has **three regions** and **two junctions**: NPN or PNP. Terminals: **Emitter (E)**, **Base (B)**, **Collector (C)**.
* In normal (active) operation: **emitter–base junction forward biased**, **collector–base junction reverse biased**.
* The emitter **injects** carriers into the base. Because the base is very thin and lightly doped, almost all of them cross to the collector, which collects them.

## 16.2 Basic current relations

::: formula Formulas from the top of your class p. 39
$$I_C=\beta I_B,\qquad I_E=(\beta+1)I_B,\qquad V_{BE}\approx0.7\text{ V (Si)}$$
:::

$$I_E=I_C+I_B,\qquad\alpha=\frac{I_C}{I_E},\qquad\beta=\frac{I_C}{I_B},\qquad\alpha=\frac{\beta}{\beta+1},\qquad\beta=\frac{\alpha}{1-\alpha}$$

Since $\beta$ is large, $I_E\approx I_C$ ($\alpha\approx1$).

::: ex Example 16.1: Currents and gains
**Given:** $\beta=100$, $I_B=30\ \mu$A.

**Find:** $I_C$, $I_E$, $\alpha$.

**Step 1.** $I_C=\beta I_B=100\times30\ \mu\text{A}=3000\ \mu\text{A}=3$ mA.
**Step 2.** $I_E=(\beta+1)I_B=101\times30\ \mu\text{A}=3.03$ mA. (Check: $I_C+I_B=3+0.03=3.03$ ✓.)
**Step 3.** $\alpha=\dfrac{\beta}{\beta+1}=\dfrac{100}{101}=0.990$.

**Answer:** $I_C=3$ mA, $I_E=3.03$ mA, $\alpha=0.990$.

**Another way round:** if $\alpha=0.98$ then $\beta=\dfrac{\alpha}{1-\alpha}=\dfrac{0.98}{0.02}=49$.
:::

**Three configurations:** common-emitter (CE), common-base (CB), common-collector (CC = emitter follower). CE gives both voltage and current gain and is the workhorse of Unit II.

## 16.3 Regions of operation (slide)

| Region | Base–emitter junction | Base–collector junction | Behaviour |
|---|---|---|---|
| **Active (linear)** | forward | reverse | amplification: $I_C=\beta I_B$ |
| **Cut-off** | reverse | reverse | transistor **off**: $I_C\approx0$ |
| **Saturation** | forward | forward | fully **on**: $V_{CE}\approx0.2$ V, $I_C$ no longer $\beta I_B$ |

{{fig p_bjt_char|Input and output characteristics of a CE transistor with the three regions marked.|92}}

* **Input characteristic** ($I_B$ against $V_{BE}$): like a diode curve; knee near 0.6–0.7 V.
* **Output characteristic** ($I_C$ against $V_{CE}$ for fixed $I_B$): nearly flat lines in the active region (a slight upward slope is the Early effect, Ch. 18); saturation at small $V_{CE}$; cut-off along $I_B=0$.
* As a switch: cut-off (off) ↔ saturation (on). As an amplifier: stay in the active region.

## 16.4 Why bias? The operating point (Q-point)

* Any increase in ac voltage, current or power comes from **energy transferred from the dc supplies**. So the analysis of any amplifier has **two parts: dc and ac**.
* **Biasing** = applying dc voltages to establish a **fixed level of current and voltage**.
* The resulting dc current and voltage set an **operating point** on the characteristics. Because it is fixed, it is also called the **quiescent point (Q-point)**. Class note: "Q-point: to maintain the biasing (for stabilisation)."

## 16.5 DC load line

Apply Kirchhoff's voltage law (KVL: voltages around a loop add to zero) around the collector–emitter loop:
$$V_{CE}=V_{CC}-I_CR_C\qquad\text{or, with an emitter resistor,}\qquad V_{CE}=V_{CC}-I_C(R_C+R_E).$$
This straight line on the output characteristics is the **dc load line**. Its two end points:

* $I_C=0\Rightarrow V_{CE}=V_{CC}$: the **cut-off** end (on the horizontal axis).
* $V_{CE}=0\Rightarrow I_C=\dfrac{V_{CC}}{R_C}$ (or $\dfrac{V_{CC}}{R_C+R_E}$): the **saturation** end, $I_{C,sat}$ (on the vertical axis).

{{fig p_loadline|Load line for $V_{CC}=12$ V, $R_C=2.2\ \text{k}\Omega$. The Q-point is where the line meets the curve for the chosen $I_B$.|75}}

The **Q-point** is where the load line crosses the characteristic of the chosen $I_B$ (here $I_B=47\ \mu$A gives $I_{CQ}=2.35$ mA and $V_{CEQ}=6.82$ V; see Example 17.1).

{{fig p_loadline_effects|How the Q-point and load line move when $I_B$, $R_C$ or $V_{CC}$ changes (slide Figs 4.13–4.15).|95}}

* **Raise $I_B$** → Q moves **up** the load line (toward saturation).
* **Increase $R_C$** → the load line becomes **shallower** (the vertical intercept $V_{CC}/R_C$ falls; the horizontal one stays at $V_{CC}$).
* **Lower $V_{CC}$** → the line shifts parallel to itself toward the origin.
* **Best Q-point for an amplifier:** near the **middle of the load line**, $V_{CEQ}\approx V_{CC}/2$, so the output can swing equally up and down before clipping.

::: ex Example 16.2: Design a mid-point Q
**Given:** $V_{CC}=12$ V, want $I_{CQ}=2$ mA and $V_{CEQ}=6$ V, $\beta=100$, fixed bias (no $R_E$).

**Find:** $R_C$ and $R_B$.

**Step 1: voltage across $R_C$.** $V_{CC}-V_{CEQ}=12-6=6$ V.
**Step 2: collector resistor.** $R_C=\dfrac{6}{2\ \text{mA}}=3\ \text{k}\Omega$.
**Step 3: base current needed.** $I_B=\dfrac{I_C}{\beta}=\dfrac{2\ \text{mA}}{100}=20\ \mu$A.
**Step 4: base resistor.** $R_B=\dfrac{V_{CC}-V_{BE}}{I_B}=\dfrac{12-0.7}{20\times10^{-6}}=565\ \text{k}\Omega$.

**Answer:** $R_C=3\ \text{k}\Omega$, $R_B=565\ \text{k}\Omega$ (use 560 kΩ).
:::

::: ex Example 16.3: Is the transistor saturated?
**Given:** $V_{CC}=12$ V, $R_B=100\ \text{k}\Omega$, $R_C=4.7\ \text{k}\Omega$, $\beta=200$ (fixed bias).

**Step 1: base current.** $I_B=\dfrac{12-0.7}{100\ \text{k}}=113\ \mu$A.
**Step 2: collector current if active.** $I_C=\beta I_B=200\times113\ \mu\text{A}=22.6$ mA.
**Step 3: the maximum the circuit allows.** $I_{C,sat}=\dfrac{V_{CC}}{R_C}=\dfrac{12}{4.7\ \text{k}}=2.55$ mA.
**Step 4: compare.** $22.6\ \text{mA}\gg2.55$ mA, so the transistor cannot be active.

**Answer:** it is in **saturation**: $I_C\approx2.55$ mA and $V_{CE}\approx0.2$ V. The formula $I_C=\beta I_B$ does not apply.
:::

::: trap Always check for saturation
If the calculated $I_C=\beta I_B$ is bigger than $I_{C,sat}$, the transistor is saturated and $I_C\approx I_{C,sat}$, $V_{CE}\approx0$.
:::

## 16.6 Frequency response (class note, p. 40)

Class note: "Frequency response → characteristics between frequency and gain." A CE amplifier's gain is **flat (the mid-band gain)** over a range and falls at low frequencies (because of the **coupling and bypass capacitors**) and at high frequencies (because of the transistor's **internal capacitances**).

{{fig p_freq_resp|Typical amplifier frequency response.|62}}

## 16.7 Practice

::: try Questions for Chapter 16
1. Which junctions are forward and which reverse in (a) the active region, (b) saturation, (c) cut-off?
2. $\beta=150$. Find $\alpha$. If $I_B=20\ \mu$A, find $I_C$ and $I_E$.
3. Draw the dc load line for $V_{CC}=15$ V, $R_C=3\ \text{k}\Omega$, $R_E=1\ \text{k}\Omega$. Give both intercepts and the mid-point Q.
4. Why must the Q-point be near the middle of the load line?
5. $V_{CC}=10$ V, $R_B=200\ \text{k}\Omega$, $R_C=5\ \text{k}\Omega$, $\beta=100$. Is the transistor saturated?
:::

::: soln Answers and full solutions
<details markdown="1"><summary>Solution 1</summary>

(a) **Active:** base–emitter forward, base–collector reverse.
(b) **Saturation:** both forward.
(c) **Cut-off:** both reverse.
</details>

<details markdown="1"><summary>Solution 2</summary>

**Step 1.** $\alpha=\dfrac{\beta}{\beta+1}=\dfrac{150}{151}=0.9934$.
**Step 2.** $I_C=\beta I_B=150\times20\ \mu\text{A}=3$ mA.
**Step 3.** $I_E=(\beta+1)I_B=151\times20\ \mu\text{A}=3.02$ mA.
</details>

<details markdown="1"><summary>Solution 3</summary>

**Formula:** $V_{CE}=V_{CC}-I_C(R_C+R_E)$.
**Step 1.** $R_C+R_E=3+1=4\ \text{k}\Omega$.
**Step 2.** Cut-off end ($I_C=0$): $V_{CE}=15$ V.
**Step 3.** Saturation end ($V_{CE}=0$): $I_C=\dfrac{15}{4\ \text{k}}=3.75$ mA.
**Step 4.** Mid-point: $V_{CE}\approx\dfrac{15}2=7.5$ V and $I_C=\dfrac{3.75}{2}\approx1.875$ mA.

Draw a straight line from $(15\ \text{V},0)$ to $(0,3.75\ \text{mA})$ and mark Q at $(7.5\ \text{V},1.875\ \text{mA})$.
</details>

<details markdown="1"><summary>Solution 4</summary>

So the ac signal can swing equally in both directions. If Q is too near saturation the negative half of the output clips; too near cut-off, the positive half clips.
</details>

<details markdown="1"><summary>Solution 5</summary>

**Step 1.** $I_B=\dfrac{10-0.7}{200\ \text{k}}=46.5\ \mu$A.
**Step 2.** $I_C=100\times46.5\ \mu\text{A}=4.65$ mA.
**Step 3.** $I_{C,sat}=\dfrac{10}{5\ \text{k}}=2$ mA.
**Step 4.** $4.65\ \text{mA}>2$ mA.

**Answer:** **saturated** ($I_C\approx2$ mA, $V_{CE}\approx0.2$ V).
</details>
:::

# Chapter 17: DC biasing circuits {.chap}

*Class notes pp. 39–45 · slides: ECE BJT FOT DU (Transistor DC Bias Configurations, Summary tables)*

::: words
| Word / symbol | Plain meaning |
|---|---|
| Fixed bias | base current set by one resistor $R_B$ from the supply |
| Emitter bias (self-bias) | fixed bias plus an emitter resistor $R_E$ for stability |
| Voltage-divider bias | base voltage set by a divider $R_1$, $R_2$ |
| Collector-feedback bias | base resistor connected from collector to base |
| Emitter follower | common-collector circuit; output taken from the emitter |
| Common-base | base grounded; input at emitter, output at collector |
| Stability | how little the Q-point moves when $\beta$ or temperature changes |
| $E_{Th}$, $R_{Th}$ | Thévenin equivalent (one voltage source + one resistor) of the divider |
| $R_1\parallel R_2$ | $R_1$ and $R_2$ in parallel $=\dfrac{R_1R_2}{R_1+R_2}$ |
| $V_B$, $V_E$, $V_C$ | voltages of base, emitter, collector **with respect to ground** |
| $V_{BC}$ | $V_B-V_C$ (must be negative for the NPN active region) |
| $V_{CC}$, $V_{EE}$ | collector supply, emitter supply |
| $I_{C,sat}$ | largest possible $I_C$ (transistor saturated) |
| Capacitors are open for dc | in dc analysis remove every capacitor |
| KVL | Kirchhoff's voltage law: voltages around a loop add to zero |
:::

::: kid Six ways to set the tap
There are several circuits for "setting the tap" at the right level. Some are simple but the setting drifts if the transistor is replaced or gets hot (**fixed bias**). Others use a helper resistor or a voltage divider that automatically **pushes back** when things drift (**emitter bias, voltage divider, collector feedback**), so the setting stays put. That "staying put" is **stability**.
:::

**The procedure to use every time (do this in the exam):**
1. Redraw the circuit for **dc**: replace all capacitors by **open circuits** and remove the ac source (your class note: "open the ac terminals").
2. Write KVL around the **base–emitter (input) loop** and solve for $I_B$.
3. $I_C=\beta I_B$ and $I_E=(\beta+1)I_B\approx I_C$.
4. Write KVL around the **collector–emitter (output) loop** and solve for $V_{CE}$.
5. If asked, find node voltages: $V_E$, $V_B=V_E+0.7$, $V_C$, and $V_{BC}=V_B-V_C$ (negative ⇒ active region).

## 17.1 Fixed-bias circuit

{{fig c_fixed_bias|Fixed-bias circuit: $R_B$ from $V_{CC}$ to the base, $R_C$ in the collector.|75}}

**Base–emitter loop:** $V_{CC}-I_BR_B-V_{BE}=0$, so
$$\boxed{I_B=\frac{V_{CC}-V_{BE}}{R_B}},\qquad I_C=\beta I_B.$$
**Collector–emitter loop:** $V_{CC}-I_CR_C-V_{CE}=0$, so
$$\boxed{V_{CE}=V_{CC}-I_CR_C}.$$
Node voltages: $V_E=0$, $V_B=V_{BE}$, $V_C=V_{CE}$; $V_{BC}=V_B-V_C$.
**Saturation:** with $V_{CE}\approx0$: $\boxed{I_{C,sat}=\dfrac{V_{CC}}{R_C}}$.

::: ex Example 17.1: Fixed bias (slide Ex 4.1)
**Given:** $V_{CC}=12$ V, $R_B=240\ \text{k}\Omega$, $R_C=2.2\ \text{k}\Omega$, $\beta=50$.

**Find:** $I_B$, $I_C$, $V_{CE}$, $V_B$, $V_C$, $V_{BC}$.

**Step 1: base current.** $I_B=\dfrac{12-0.7}{240\ \text{k}}=\dfrac{11.3}{240\,000}=47.08\ \mu$A.
**Step 2: collector current.** $I_C=\beta I_B=50\times47.08\ \mu\text{A}=2.354$ mA.
**Step 3: voltage across $R_C$.** $I_CR_C=2.354\ \text{mA}\times2.2\ \text{k}=5.18$ V.
**Step 4: $V_{CE}$.** $V_{CE}=12-5.18=6.82$ V.
**Step 5: node voltages.** $V_B=0.7$ V; $V_C=V_{CE}=6.82$ V.
**Step 6: $V_{BC}$.** $0.7-6.82=-6.12$ V.
**Step 7: check saturation.** $I_{C,sat}=12/2.2\ \text{k}=5.45$ mA $>2.35$ mA ✓.

**Answer:** $I_B=47.08\ \mu$A; $I_C=2.35$ mA; $V_{CE}=6.82$ V; $V_B=0.7$ V; $V_C=6.82$ V; $V_{BC}=-6.12$ V (negative: collector junction reverse biased ✓, active region).
:::

::: trap The big weakness of fixed bias
$I_B$ is fixed by $R_B$, but $I_C=\beta I_B$ follows $\beta$, which varies between transistors and with temperature. In the example above, if $\beta$ doubles from 50 to 100: $I_B$ is unchanged, $I_C$ goes from 2.35 to **4.71 mA**, and $V_{CE}=12-4.71\times2.2=\mathbf{1.64\ V}$ (nearly saturated). The Q-point is unstable.
:::

## 17.2 Emitter-bias (self-bias) circuit

*Your class notes call it the **self-bias circuit (emitter bias)**.*

{{fig c_emitter_bias|Emitter bias: an emitter resistor $R_E$ is added.|75}}

**Base–emitter loop:** $V_{CC}-I_BR_B-V_{BE}-I_ER_E=0$ with $I_E=(\beta+1)I_B$:
$$\boxed{I_B=\frac{V_{CC}-V_{BE}}{R_B+(\beta+1)R_E}}$$
The emitter resistor appears in the base loop **multiplied by $(\beta+1)$**.

**Collector–emitter loop:** $V_{CC}-I_CR_C-V_{CE}-I_ER_E=0$ with $I_E\approx I_C$:
$$\boxed{V_{CE}=V_{CC}-I_C(R_C+R_E)}$$
Then $V_E=I_ER_E$, $V_B=V_{BE}+V_E$, $V_C=V_{CE}+V_E=V_{CC}-I_CR_C$. **Saturation:** $I_{C,sat}=\dfrac{V_{CC}}{R_C+R_E}$.

**Why it is more stable:** if $I_C$ tries to rise, $V_E=I_ER_E$ rises, which **reduces $V_{BE}$ and so $I_B$**. That is negative feedback: the dc currents and voltages stay closer to their design values when temperature or $\beta$ change.

::: ex Example 17.2: Emitter bias (slide Ex 4.4)
**Given:** $V_{CC}=20$ V, $R_B=430\ \text{k}\Omega$, $R_C=2\ \text{k}\Omega$, $R_E=1\ \text{k}\Omega$, $\beta=50$.

**Find:** $I_B$, $I_C$, $V_{CE}$, $V_C$, $V_E$, $V_B$, $V_{BC}$.

**Step 1: base loop denominator.** $R_B+(\beta+1)R_E=430\ \text{k}+51\times1\ \text{k}=481\ \text{k}\Omega$.
**Step 2: base current.** $I_B=\dfrac{20-0.7}{481\ \text{k}}=\dfrac{19.3}{481\,000}=40.12\ \mu$A.
**Step 3: collector current.** $I_C=50\times40.12\ \mu\text{A}=2.006$ mA.
**Step 4: $V_{CE}$.** $V_{CE}=20-2.006\ \text{mA}\times(2+1)\ \text{k}=20-6.02=13.98$ V.
**Step 5: node voltages.** $V_E=I_ER_E\approx2.006\ \text{mA}\times1\ \text{k}=2.01$ V; $V_B=0.7+2.01=2.71$ V; $V_C=20-2.006\times2=15.99$ V.
**Step 6: $V_{BC}$.** $2.71-15.99=-13.28$ V.

**Answer:** $I_B=40.1\ \mu$A; $I_C=2.01$ mA; $V_{CE}=13.98$ V; $V_E=2.01$ V; $V_B=2.71$ V; $V_C=15.99$ V; $V_{BC}=-13.3$ V.

**Stability check:** for $\beta=100$: $I_B=19.3/(430+101)\ \text{k}=36.3\ \mu$A, $I_C=3.63$ mA (up 81 %, versus 100 % for fixed bias) and $V_{CE}=20-3.63\times3=9.1$ V.
:::

## 17.3 Voltage-divider bias

{{fig c_vdiv|Voltage-divider bias: $R_1$ and $R_2$ set the base voltage.|75}}

The best-known stable circuit. Two methods: **exact** (Thévenin) and **approximate**.

### Exact analysis (Thévenin's theorem, as in your class notes)

{{fig c_thevenin|Replacing the divider by $E_{Th}$ and $R_{Th}$ as seen from the base.|68}}

Thévenin's theorem replaces the divider $R_1$, $R_2$ (seen from the base) by one battery and one resistor:
$$R_{Th}=R_1\parallel R_2=\frac{R_1R_2}{R_1+R_2},\qquad E_{Th}=\frac{R_2}{R_1+R_2}V_{CC}.$$
KVL on the base loop: $E_{Th}-I_BR_{Th}-V_{BE}-I_ER_E=0$ with $I_E=(\beta+1)I_B$:
$$\boxed{I_B=\frac{E_{Th}-V_{BE}}{R_{Th}+(\beta+1)R_E}},\qquad I_C=\beta I_B,\qquad\boxed{V_{CE}=V_{CC}-I_C(R_C+R_E)}.$$

### Approximate analysis
Valid when $R_i=(\beta+1)R_E\approx\beta R_E\ge10R_2$ (the base draws so little current that it does not disturb the divider). Then
$$V_B=\frac{R_2}{R_1+R_2}V_{CC},\qquad V_E=V_B-V_{BE},\qquad I_E=\frac{V_E}{R_E}\approx I_C,\qquad V_{CE}=V_{CC}-I_C(R_C+R_E).$$
$\beta$ does not appear, so $I_C$ hardly depends on it. **Saturation:** $I_{C,sat}=\dfrac{V_{CC}}{R_C+R_E}$.

::: ex Example 17.3: Divider bias where the approximation fails (slide Ex 4.11)
**Given:** $V_{CC}=18$ V, $R_1=82\ \text{k}\Omega$, $R_2=22\ \text{k}\Omega$, $R_C=5.6\ \text{k}\Omega$, $R_E=1.2\ \text{k}\Omega$, $\beta=50$.

**Find:** $I_{CQ}$ and $V_{CEQ}$ (exact and approximate).

**Step 1: test the approximation.** $\beta R_E=50\times1.2\ \text{k}=60\ \text{k}\Omega$. $10R_2=220\ \text{k}\Omega$. Since $60\ \text{k}<220\ \text{k}$, the condition **fails**.

**Exact method**
**Step 2: Thévenin resistance.** $R_{Th}=\dfrac{82\times22}{82+22}\ \text{k}=\dfrac{1804}{104}\ \text{k}=17.35\ \text{k}\Omega$.
**Step 3: Thévenin voltage.** $E_{Th}=\dfrac{22}{104}\times18=3.81$ V.
**Step 4: base current.** $I_B=\dfrac{3.81-0.7}{17.35\ \text{k}+51\times1.2\ \text{k}}=\dfrac{3.11}{17.35\ \text{k}+61.2\ \text{k}}=\dfrac{3.11}{78.55\ \text{k}}=39.6\ \mu$A.
**Step 5:** $I_{CQ}=\beta I_B=50\times39.6\ \mu\text{A}=1.98$ mA.
**Step 6:** $V_{CEQ}=18-1.98\ \text{mA}\times(5.6+1.2)\ \text{k}=18-13.46=4.54$ V.

**Approximate method (for comparison)**
**Step 7:** $V_B=E_{Th}=3.81$ V; $V_E=3.81-0.7=3.11$ V.
**Step 8:** $I_E=\dfrac{3.11}{1.2\ \text{k}}=2.59$ mA.
**Step 9:** $V_{CE}=18-2.59\ \text{mA}\times6.8\ \text{k}=18-17.61=0.39$ V.

**Step 10: compare.** The approximate method says the transistor is almost saturated ($V_{CE}=0.39$ V), while the exact method says it is comfortably active ($4.54$ V). They disagree badly because the test in Step 1 failed.


| | $I_{CQ}$ | $V_{CEQ}$ |
|---|---|---|
| Exact | 1.98 mA | 4.54 V |
| Approximate (invalid here) | 2.59 mA | 0.39 V |

**Answer:** use the exact method: $I_{CQ}=1.98$ mA, $V_{CEQ}=4.54$ V.
:::

::: ex Example 17.4: Divider bias where the approximation works
**Given:** $V_{CC}=20$ V, $R_1=47\ \text{k}\Omega$, $R_2=10\ \text{k}\Omega$, $R_C=3.3\ \text{k}\Omega$, $R_E=2\ \text{k}\Omega$, $\beta=100$.

**Step 1: test.** $\beta R_E=200\ \text{k}\ge10R_2=100\ \text{k}$ ✓.
**Approximate:**
**Step 2:** $V_B=\dfrac{10}{57}\times20=3.51$ V; $V_E=3.51-0.7=2.81$ V.
**Step 3:** $I_E=\dfrac{2.81}{2\ \text{k}}=1.40$ mA.
**Step 4:** $V_{CE}=20-1.40\ \text{mA}\times(3.3+2)\ \text{k}=20-7.45=12.6$ V.
**Exact:**
**Step 5:** $R_{Th}=\dfrac{47\times10}{57}\ \text{k}=8.25\ \text{k}$; $E_{Th}=3.51$ V.
**Step 6:** $I_B=\dfrac{3.51-0.7}{8.25\ \text{k}+101\times2\ \text{k}}=\dfrac{2.81}{210.25\ \text{k}}=13.4\ \mu$A; $I_C=1.34$ mA.
**Step 7:** $V_{CE}=20-1.34\times5.3=12.9$ V.

**Answer:** approximate $I_C\approx1.40$ mA, $V_{CE}\approx12.6$ V; exact $1.34$ mA and $12.9$ V: close ✓.

**Stability:** if $\beta$ doubles to 200, $I_B=2.81/(8.25+201\times2)\ \text{k}=2.81/410.25\ \text{k}=6.85\ \mu$A and $I_C=200\times6.85\ \mu\text{A}=1.37$ mA: only **+2.5 %** (fixed bias would double). That is why divider bias is preferred.
:::

## 17.4 Collector-feedback bias

{{fig c_coll_fb|Collector feedback: $R_F$ connects the collector to the base.|75}}

$R_F$ feeds part of the collector voltage back to the base: if $I_C$ rises, $V_C$ falls, which lowers $I_B$ (negative feedback).

Let $I_C'=I_C+I_B\approx I_C\approx I_E$. KVL on the base–emitter loop:
$$V_{CC}-I_C'R_C-I_BR_F-V_{BE}-I_ER_E=0.$$
With $I_C'\approx I_E=\beta I_B$: $V_{CC}-V_{BE}-I_BR_F-\beta I_B(R_C+R_E)=0$, so
$$\boxed{I_B=\frac{V_{CC}-V_{BE}}{R_F+\beta(R_C+R_E)}},\qquad I_C=\beta I_B,\qquad\boxed{V_{CE}=V_{CC}-I_C(R_C+R_E)}.$$
**Saturation:** $I_{C,sat}=\dfrac{V_{CC}}{R_C+R_E}$. The load line is the same as for the other circuits; only $I_{BQ}$ depends on the circuit.

::: ex Example 17.5: Collector feedback (slide Ex 4.14)
**Given:** $V_{CC}=18$ V, $R_C=3.3\ \text{k}\Omega$, $R_E=510\ \Omega$, $R_F=R_{F1}+R_{F2}=91\ \text{k}+110\ \text{k}=201\ \text{k}\Omega$ (the capacitor between them is open for dc), $\beta=75$.

**Step 1: $R_C+R_E$.** $3.3+0.51=3.81\ \text{k}\Omega$.
**Step 2: $\beta(R_C+R_E)$.** $75\times3.81\ \text{k}=285.75\ \text{k}\Omega$.
**Step 3: denominator.** $R_F+285.75\ \text{k}=201\ \text{k}+285.75\ \text{k}=486.75\ \text{k}\Omega$.
**Step 4: $I_B$.** $\dfrac{18-0.7}{486.75\ \text{k}}=\dfrac{17.3}{486\,750}=35.5\ \mu$A.
**Step 5: $I_C$.** $75\times35.5\ \mu\text{A}=2.66$ mA.
**Step 6: $V_C$.** $V_C=V_{CC}-I_CR_C=18-2.66\ \text{mA}\times3.3\ \text{k}=18-8.78=9.22$ V.

**Answer:** $I_B=35.5\ \mu$A; $I_C=2.66$ mA; $V_C=9.22$ V.
:::

## 17.5 Emitter-follower (common-collector) bias

{{fig c_emitter_follower|Emitter follower: collector at dc ground (0 V), emitter resistor to $-V_{EE}$, output from the emitter.|75}}

Input loop: $-I_BR_B-V_{BE}-I_ER_E+V_{EE}=0$ with $I_E=(\beta+1)I_B$:
$$\boxed{I_B=\frac{V_{EE}-V_{BE}}{R_B+(\beta+1)R_E}},\qquad I_E=(\beta+1)I_B.$$
Output loop: $-V_{CE}-I_ER_E+V_{EE}=0$:
$$\boxed{V_{CE}=V_{EE}-I_ER_E}.$$

::: ex Example 17.6: Emitter follower (slide Ex 4.16)
**Given:** $V_{EE}=20$ V, $R_B=240\ \text{k}\Omega$, $R_E=2\ \text{k}\Omega$, $\beta=90$.

**Step 1:** $(\beta+1)R_E=91\times2\ \text{k}=182\ \text{k}$; denominator $240+182=422\ \text{k}\Omega$.
**Step 2:** $I_B=\dfrac{20-0.7}{422\ \text{k}}=45.73\ \mu$A.
**Step 3:** $I_E=91\times45.73\ \mu\text{A}=4.162$ mA.
**Step 4:** $V_{CE}=20-4.162\ \text{mA}\times2\ \text{k}=20-8.32=11.68$ V.

**Answer:** $I_B=45.7\ \mu$A; $I_E=4.16$ mA; $V_{CE}=11.68$ V.
:::

## 17.6 Common-base bias

{{fig c_common_base|Common-base configuration: input at the emitter, base grounded, output at the collector.|78}}

Input loop: $-V_{EE}+I_ER_E+V_{BE}=0$:
$$\boxed{I_E=\frac{V_{EE}-V_{BE}}{R_E}},\qquad I_C\approx I_E,\qquad I_B=\frac{I_E}{\beta+1}.$$
Whole circuit: $-V_{EE}+I_ER_E+V_{CE}+I_CR_C-V_{CC}=0$:
$$\boxed{V_{CE}=V_{EE}+V_{CC}-I_E(R_C+R_E)},\qquad\boxed{V_{CB}=V_{CC}-I_CR_C}.$$

::: ex Example 17.7: Common base (slide Ex 4.17)
**Given:** $V_{EE}=4$ V, $V_{CC}=10$ V, $R_E=1.2\ \text{k}\Omega$, $R_C=2.4\ \text{k}\Omega$, $\beta=60$.

**Step 1:** $I_E=\dfrac{4-0.7}{1.2\ \text{k}}=\dfrac{3.3}{1200}=2.75$ mA.
**Step 2:** $I_B=\dfrac{I_E}{\beta+1}=\dfrac{2.75\ \text{mA}}{61}=45.08\ \mu$A.
**Step 3:** $V_{CE}=4+10-2.75\ \text{mA}\times(2.4+1.2)\ \text{k}=14-9.9=4.1$ V.
**Step 4:** $I_C=\beta I_B=60\times45.08\ \mu\text{A}=2.705$ mA; $V_{CB}=10-2.705\times2.4=10-6.49=3.51$ V.

**Answer:** $I_E=2.75$ mA; $I_B=45.1\ \mu$A; $V_{CE}=4.1$ V; $V_{CB}=3.51$ V (positive: the collector junction is reverse biased for an NPN ✓).
:::

## 17.7 Miscellaneous configurations

::: ex Example 17.8: Collector feedback with no $R_E$ (slide Ex 4.18)
**Given:** $V_{CC}=20$ V, $R_C=4.7\ \text{k}\Omega$, $R_B=680\ \text{k}\Omega$ connected from the **collector to the base**, $\beta=120$, no emitter resistor.

With $R_E=0$ the collector-feedback formula becomes $I_B=\dfrac{V_{CC}-V_{BE}}{R_B+\beta R_C}$.

**Step 1:** $\beta R_C=120\times4.7\ \text{k}=564\ \text{k}$; denominator $680+564=1244\ \text{k}\Omega$.
**Step 2:** $I_B=\dfrac{19.3}{1\,244\,000}=15.51\ \mu$A.
**Step 3:** $I_C=120\times15.51\ \mu\text{A}=1.86$ mA.
**Step 4:** $V_{CE}=20-1.86\ \text{mA}\times4.7\ \text{k}=20-8.74=11.26$ V.
**Step 5:** $V_B=0.7$ V, $V_C=11.26$ V, $V_E=0$, $V_{BC}=0.7-11.26=-10.56$ V.

**Answer:** $I_B=15.5\ \mu$A, $I_C=1.86$ mA, $V_{CE}=11.26$ V.
:::

::: ex Example 17.9: Negative emitter supply (slide Ex 4.19)
**Given:** an NPN transistor with the emitter at $V_{EE}=-9$ V, $R_B=100\ \text{k}\Omega$ (base to ground), $R_C=1.2\ \text{k}\Omega$ (collector to ground), $\beta=45$.

**Step 1:** the base is at $V_B=V_E+0.7=-9+0.7=-8.3$ V, so the voltage across $R_B$ is 8.3 V, and $I_B=\dfrac{8.3}{100\ \text{k}}=83\ \mu$A.
**Step 2:** $I_C=45\times83\ \mu\text{A}=3.735$ mA.
**Step 3:** $V_C=-I_CR_C=-3.735\ \text{mA}\times1.2\ \text{k}=-4.48$ V.

**Answer:** $I_B=83\ \mu$A; $I_C=3.735$ mA; $V_C=-4.48$ V; $V_B=-8.3$ V. Negative supplies only shift the reference level; the method is unchanged. For a PNP transistor all currents and polarities reverse.
:::

## 17.8 Summary table (slides)

| Configuration | $I_B$ | Other equations |
|---|---|---|
| Fixed bias | $\dfrac{V_{CC}-V_{BE}}{R_B}$ | $I_C=\beta I_B$; $V_{CE}=V_{CC}-I_CR_C$ |
| Emitter bias | $\dfrac{V_{CC}-V_{BE}}{R_B+(\beta+1)R_E}$ | $V_{CE}=V_{CC}-I_C(R_C+R_E)$ |
| Voltage divider (exact) | $\dfrac{E_{Th}-V_{BE}}{R_{Th}+(\beta+1)R_E}$ | $R_{Th}=R_1\parallel R_2$; $E_{Th}=\frac{R_2V_{CC}}{R_1+R_2}$ |
| Voltage divider (approx., $\beta R_E\ge10R_2$) | – | $V_B=\frac{R_2V_{CC}}{R_1+R_2}$; $V_E=V_B-V_{BE}$; $I_E=V_E/R_E$ |
| Collector feedback | $\dfrac{V_{CC}-V_{BE}}{R_F+\beta(R_C+R_E)}$ | $V_{CE}=V_{CC}-I_C(R_C+R_E)$ |
| Emitter follower | $\dfrac{V_{EE}-V_{BE}}{R_B+(\beta+1)R_E}$ | $V_{CE}=V_{EE}-I_ER_E$ |
| Common base | $I_E=\dfrac{V_{EE}-V_{BE}}{R_E}$ | $V_{CE}=V_{EE}+V_{CC}-I_E(R_C+R_E)$; $V_{CB}=V_{CC}-I_CR_C$ |

**Stability (best to worst):** voltage divider ≳ collector feedback / emitter bias ≫ fixed bias.

## 17.9 Quick sanity checks <span class="tag">extra</span>

* Active region ⇒ $V_{BE}\approx0.7$ V, $V_{CE}>0.2$ V and (NPN) $V_{BC}<0$.
* $V_{CE}\approx0.2$ V or less ⇒ **saturated**. $V_{CE}\approx V_{CC}$ ⇒ **cut-off**.
* $I_C$ can never exceed $I_{C,sat}=V_{CC}/(R_C+R_E)$.

## 17.10 Practice

::: try Questions for Chapter 17
1. Fixed bias: $V_{CC}=15$ V, $R_B=470\ \text{k}\Omega$, $R_C=3.3\ \text{k}\Omega$, $\beta=100$. Find $I_B$, $I_C$, $V_{CE}$. Is it saturated?
2. Emitter bias: $V_{CC}=12$ V, $R_B=330\ \text{k}\Omega$, $R_C=2.2\ \text{k}\Omega$, $R_E=470\ \Omega$, $\beta=100$. Find $I_C$, $V_{CE}$, $V_E$.
3. Voltage divider: $V_{CC}=12$ V, $R_1=33\ \text{k}\Omega$, $R_2=6.8\ \text{k}\Omega$, $R_C=2.2\ \text{k}\Omega$, $R_E=1\ \text{k}\Omega$, $\beta=100$. Test the approximation, then find $I_C$ and $V_{CE}$.
4. Collector feedback: $V_{CC}=10$ V, $R_C=2\ \text{k}\Omega$, $R_F=200\ \text{k}\Omega$, $R_E=0$, $\beta=100$. Find $I_C$, $V_{CE}$.
5. Explain in words why an emitter resistor improves stability.
:::

::: soln Answers and full solutions
<details markdown="1"><summary>Solution 1</summary>

**Step 1.** $I_B=\dfrac{15-0.7}{470\ \text{k}}=\dfrac{14.3}{470\,000}=30.4\ \mu$A.
**Step 2.** $I_C=100\times30.4\ \mu\text{A}=3.04$ mA.
**Step 3.** $V_{CE}=15-3.04\ \text{mA}\times3.3\ \text{k}=15-10.03=4.97$ V.
**Step 4: saturation check.** $I_{C,sat}=15/3.3\ \text{k}=4.55$ mA $>3.04$ mA ⇒ **not saturated**.

**Answer:** $I_B=30.4\ \mu$A; $I_C=3.04$ mA; $V_{CE}=4.97$ V; active region.
</details>

<details markdown="1"><summary>Solution 2</summary>

**Step 1.** $R_B+(\beta+1)R_E=330\ \text{k}+101\times0.47\ \text{k}=330+47.5=377.5\ \text{k}\Omega$.
**Step 2.** $I_B=\dfrac{12-0.7}{377.5\ \text{k}}=29.9\ \mu$A.
**Step 3.** $I_C=100\times29.9\ \mu\text{A}=2.99$ mA.
**Step 4.** $V_{CE}=12-2.99\ \text{mA}\times(2.2+0.47)\ \text{k}=12-7.98=4.02$ V.
**Step 5.** $I_E=101\times29.9\ \mu\text{A}=3.02$ mA; $V_E=I_ER_E=3.02\ \text{mA}\times0.47\ \text{k}=1.42$ V.

**Answer:** $I_C=2.99$ mA; $V_{CE}=4.02$ V; $V_E=1.42$ V.
</details>

<details markdown="1"><summary>Solution 3</summary>

**Step 1: test.** $\beta R_E=100\times1\ \text{k}=100\ \text{k}$; $10R_2=68\ \text{k}$. $100\ge68$ ✓, so the approximation is valid.
**Step 2.** $V_B=\dfrac{6.8}{33+6.8}\times12=\dfrac{6.8}{39.8}\times12=2.05$ V.
**Step 3.** $V_E=2.05-0.7=1.35$ V.
**Step 4.** $I_E=\dfrac{1.35}{1\ \text{k}}=1.35$ mA $\approx I_C$.
**Step 5.** $V_{CE}=12-1.35\ \text{mA}\times(2.2+1)\ \text{k}=12-4.32=7.68$ V.

**Answer:** $I_C\approx1.35$ mA; $V_{CE}\approx7.68$ V.
</details>

<details markdown="1"><summary>Solution 4</summary>

**Step 1.** With $R_E=0$: $I_B=\dfrac{V_{CC}-V_{BE}}{R_F+\beta R_C}=\dfrac{9.3}{200\ \text{k}+100\times2\ \text{k}}=\dfrac{9.3}{400\ \text{k}}=23.25\ \mu$A.
**Step 2.** $I_C=100\times23.25\ \mu\text{A}=2.325$ mA.
**Step 3.** $V_{CE}=10-2.325\ \text{mA}\times2\ \text{k}=10-4.65=5.35$ V.

**Answer:** $I_C=2.33$ mA; $V_{CE}=5.35$ V.
</details>

<details markdown="1"><summary>Solution 5</summary>

**Step 1.** If $I_C$ (and so $I_E$) tries to rise, the voltage $V_E=I_ER_E$ across the emitter resistor rises.
**Step 2.** The base–emitter voltage is $V_{BE}=V_B-V_E$, so it falls.
**Step 3.** A smaller $V_{BE}$ reduces $I_B$ and therefore $I_C$: the change is opposed (negative feedback).
**Answer:** so the Q-point moves less when $\beta$ or temperature change.
</details>
:::
