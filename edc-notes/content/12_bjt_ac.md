# Chapter 18: AC analysis of the BJT

*Class notes pp. 46–54 · slides: AC Analysis re model of BJT · scans: "CE emitter-bias", "Emitter follower", "Collector DC feedback"*

::: words
| Word / symbol | Plain meaning |
|---|---|
| AC analysis | studying how the amplifier treats the small **signal** (as opposed to the dc bias) |
| Small-signal | so small that the transistor behaves like a straight-line (linear) device around its Q-point |
| Model | a simple equivalent circuit that behaves like the transistor for ac |
| $r_e$ model | model using $r_e$ (a small resistor) and a current source |
| Hybrid ($h$) model | model using the $h$-parameters $h_{ie},h_{re},h_{fe},h_{oe}$ |
| $r_e$ | **ac emitter resistance** $=26\text{ mV}/I_E$ ($I_E$ is the **dc** emitter current at Q) |
| $\beta r_e$ | what the base "sees" looking into the transistor |
| $r_o$ | transistor **output resistance** (large, tens of kΩ) $\approx V_A/I_{CQ}$ |
| $V_A$ | **Early voltage** (about 50–200 V) |
| $Z_i$ | **input impedance**: resistance the signal source sees |
| $Z_o$ | **output impedance**: resistance seen looking back from the load |
| $Z_b$ | impedance looking into the **base** of the transistor (excluding $R_B$) |
| $A_v=V_o/V_i$ | **voltage gain** |
| $A_i=I_o/I_i$ | **current gain** |
| $V_i$, $V_o$, $I_i$, $I_o$ | input and output **ac** voltages and currents |
| Bypass capacitor $C_E$ | capacitor across $R_E$: shorts it for ac, leaves it for dc |
| Coupling capacitor $C_1$, $C_2$ | pass the ac signal but block dc between stages |
| Short circuit / open circuit | a wire (0 Ω) / a break (∞ Ω) |
| Dependent (controlled) source | a current source whose value depends on another current, e.g. $\beta I_b$ |
| $h_{ie}$, $h_{re}$, $h_{fe}$, $h_{oe}$ | input impedance, reverse-voltage ratio, forward-current ratio, output admittance |
| $\parallel$ | in parallel with |
:::

::: kid Two jobs: "set the tap" and "wiggle the tap"
In Chapter 17 you **set** the transistor to its resting point using dc. Now a tiny signal (a voice, a radio wave) is added on top and makes the operating point **wiggle a little** around Q. For the wiggles we do not need the whole complicated transistor. We replace it by a **simple cartoon** made of a resistor and a current source: the **small-signal model**. Then the amplifier is just resistors and one "controlled current source", and we can calculate **how big the input and output resistances are** ($Z_i$, $Z_o$) and **how much it amplifies** ($A_v$, $A_i$).
:::

## 18.1 Small-signal ac analysis

A **model** is an equivalent circuit that represents the ac behaviour of the transistor, built from circuit elements that approximate its behaviour under specific operating conditions. Two models are common in small-signal ac analysis (class notes p. 46):

1. the **$r_e$ model**;
2. the **hybrid equivalent model**.

### How to get the ac equivalent circuit (four steps)

1. Set all **dc sources to zero** and replace them by a **short circuit**. (The supply $V_{CC}$ becomes an ac ground because a battery does not change during the signal.)
2. Replace all **capacitors** by **short circuits** (coupling and bypass capacitors are large enough to be wires at signal frequencies).
3. **Remove all elements bypassed** by the short circuits from steps 1 and 2.
4. **Redraw** the network in a more convenient form.

### The four amplifier quantities

$$Z_i=\frac{V_i}{I_i},\qquad Z_o=\frac{V_o}{I_o}\Big|_{\text{source}=0},\qquad A_v=\frac{V_o}{V_i},\qquad A_i=\frac{I_o}{I_i}.$$

## 18.2 The $r_e$ model

BJTs are basically **current-controlled devices**, so the $r_e$ model uses **a diode and a current source** to copy the transistor. *Disadvantage:* it is **sensitive to the dc level** ($r_e$ depends on the operating current), so it is valid only for the specific bias condition.

### CE model

{{fig c_re_model_diode|CE $r_e$ model: the base–emitter diode has ac resistance $r_e$; the collector supplies a current $\beta I_b$.|68}}

**Deriving the input impedance.**
**Step 1.** The base–emitter voltage is across the diode's ac resistance $r_e$, carrying the **emitter** current: $V_{be}=I_er_e$.
**Step 2.** $I_e=I_c+I_b=\beta I_b+I_b=(\beta+1)I_b$.
**Step 3.** So $V_{be}=(\beta+1)I_br_e$ and $Z_i=\dfrac{V_{be}}{I_b}=(\beta+1)r_e$.
**Step 4.** Since $\beta\gg1$:
$$\boxed{Z_i=\beta r_e}\ (\text{more exactly }(\beta+1)r_e).$$
The diode is replaced by its ac resistance and, seen from the base, looks like $\beta r_e$:

{{fig c_re_model_ce|CE model with $\beta r_e$ at the input, the controlled source $\beta I_b$ and the output resistance $r_o$.|68}}

**The value of $r_e$:**
$$\boxed{r_e=\frac{26\ \text{mV}}{I_E}}\qquad(I_E\text{ is the dc emitter current at the Q-point}).$$
This is the diode ac resistance $\eta V_T/I$ from Chapter 2 with $\eta=1$ and $V_T\approx26$ mV.

::: ex Example 18.0: Computing $r_e$
**Given:** $I_E=2.4$ mA.
**Step 1.** $r_e=\dfrac{26\ \text{mV}}{2.4\ \text{mA}}$.
**Step 2.** Both in the same prefix (milli): $\dfrac{26}{2.4}=10.8\ \Omega$.
**Answer:** $r_e=10.8\ \Omega$. (Bigger bias current ⇒ smaller $r_e$.)
:::

**Early voltage and $r_o$.** In the output characteristic the constant-$I_B$ lines slope slightly upward. Extended backwards they all meet the $V_{CE}$-axis at $-V_A$ (**Early voltage**).

{{fig p_early|Early effect: the extended lines meet at $-V_A$; the slope of each line is $1/r_o$.|66}}

$$r_o=\frac{\Delta V}{\Delta I}=\frac{V_A+V_{CEQ}}{I_{CQ}}\ \approx\ \boxed{\frac{V_A}{I_{CQ}}}.$$
A large $r_o$ (tens of kΩ) sits in parallel with the current source and is often ignored when $r_o\ge10R_C$.

### CB model

{{fig c_re_model_cb|CB $r_e$ model: input $r_e$, source $\alpha I_e\approx I_e$, output $r_o$.|68}}

In the common-base configuration the input looks into the emitter: $\boxed{Z_i=r_e}$ (very small). The output source is $\alpha I_e$ ($\alpha\approx1$).

### CC model
For the common-collector configuration the **CE model is used** (no separate model), as your slide says.

### NPN versus PNP
The **dc** analysis differs (currents and voltages reversed) but the **ac** equivalent circuit is **the same**, because the signal swings both positive and negative.

### Key results (class note p. 47)

| Configuration | Input impedance seen at the transistor |
|---|---|
| CE | $\beta r_e$ (more exactly $(\beta+1)r_e$) |
| CB | $r_e$ |

### Phase relationship

{{fig p_ac_phase|CE amplifier: the output is amplified and **inverted** (180° phase shift), riding on the dc level $V_{CEQ}$.|68}}

## 18.3 CE fixed-bias configuration

{{fig c_ac_fixed|AC equivalent of the CE fixed-bias amplifier ($V_{CC}$ and capacitors replaced by shorts; $R_B$, $\beta r_e$, $\beta I_b$, $r_o$, $R_C$ all connected between the signal line and ground).|92}}

**Reading the picture:**
* **Input impedance:** the signal source sees $R_B$ and $\beta r_e$ in parallel: $\boxed{Z_i=R_B\parallel\beta r_e}$ ($\approx\beta r_e$ since $R_B\gg\beta r_e$).
* **Output impedance:** with the input source set to zero, $I_b=0$ so the current source is dead; what remains is $r_o$ and $R_C$ in parallel: $\boxed{Z_o=r_o\parallel R_C}$; if $r_o\ge10R_C$, $Z_o\approx R_C$.
* **Voltage gain:**
  **Step 1.** The input voltage is across $\beta r_e$: $V_i=I_b\,\beta r_e$, so $I_b=\dfrac{V_i}{\beta r_e}$.
  **Step 2.** The controlled current $\beta I_b$ flows down through $r_o\parallel R_C$, so $V_o=-\beta I_b\,(r_o\parallel R_C)$ (minus sign: the current flows from top to bottom through the load, so the output goes negative when $I_b$ increases).
  **Step 3.** Substitute $I_b$: $V_o=-\beta\dfrac{V_i}{\beta r_e}(r_o\parallel R_C)$.
  **Step 4.** $\beta$ cancels:
$$\boxed{A_v=\frac{V_o}{V_i}=-\frac{r_o\parallel R_C}{r_e}}\ \xrightarrow{r_o\ge10R_C}\ \boxed{A_v\approx-\frac{R_C}{r_e}}.$$
  The minus sign is the 180° phase reversal. (Class page 48 writes "$R_c/R_e$": it means the small $r_e$.)
* **Current gain:** $A_i=\dfrac{I_o}{I_i}=\dfrac{\beta I_b}{I_b}=\boxed{\beta}$ (when $R_B\gg\beta r_e$ and $r_o\gg R_C$; in general $A_i=\beta\dfrac{R_B}{R_B+\beta r_e}\dfrac{r_o}{r_o+R_C}$).

::: ex Example 18.1: Full ac analysis of the fixed-bias circuit
**Given:** the circuit of Example 17.1: $V_{CC}=12$ V, $R_B=240\ \text{k}\Omega$, $R_C=2.2\ \text{k}\Omega$, $\beta=50$; ignore $r_o$ (or take $r_o=50\ \text{k}\Omega$ as a second case).

**Find:** $r_e$, $Z_i$, $Z_o$, $A_v$, $A_i$.

**Step 1: the dc emitter current.** From Ex 17.1, $I_B=47.08\ \mu$A, so $I_E=(\beta+1)I_B=51\times47.08\ \mu\text{A}=2.40$ mA.
**Step 2: $r_e$.** $r_e=\dfrac{26\ \text{mV}}{2.40\ \text{mA}}=10.8\ \Omega$.
**Step 3: $\beta r_e$.** $50\times10.8=541\ \Omega$.
**Step 4: input impedance.** $Z_i=R_B\parallel\beta r_e=\dfrac{240\,000\times541}{240\,000+541}=540\ \Omega$.
**Step 5: output impedance.** $Z_o\approx R_C=2.2\ \text{k}\Omega$. (With $r_o=50$ k: $2.2\text{k}\parallel50\text{k}=2.11\ \text{k}\Omega$.)
**Step 6: voltage gain.** $A_v=-\dfrac{R_C}{r_e}=-\dfrac{2200}{10.8}=-203$. (With $r_o=50$ k: $-\dfrac{2107}{10.8}=-195$.)
**Step 7: current gain.** $A_i=\beta=50$.

**Answer:** $r_e=10.8\ \Omega$; $Z_i=540\ \Omega$; $Z_o=2.2\ \text{k}\Omega$; $A_v=-203$; $A_i=50$.

**What it means:** the amplifier makes the signal about 200 times larger and flips it upside-down; its input resistance is low (540 Ω), so it loads the source noticeably.
:::

## 18.4 CE self-bias (emitter-bias) configuration

Class p. 48 draws the circuit and asks two cases.

### Case 1: with the bypass capacitor $C_E$
$C_E$ shorts $R_E$ for ac, so the ac circuit is the same as fixed bias:
$$Z_i=R_B\parallel\beta r_e,\qquad Z_o=R_C\parallel r_o\approx R_C,\qquad A_v=-\frac{R_C}{r_e},\qquad A_i\approx\beta.$$

### Case 2: without the bypass capacitor

{{fig c_ac_unbypassed|AC equivalent without $C_E$: the emitter current $I_e=(\beta+1)I_b$ flows through $R_E$.|82}}

**Step 1: input voltage.** The signal $V_i$ is across $\beta r_e$ (carrying $I_b$) **plus** $R_E$ (carrying the emitter current $I_e=(\beta+1)I_b$):
$$V_i=I_b\beta r_e+I_eR_E=I_b\beta r_e+(\beta+1)I_bR_E.$$
**Step 2: impedance looking into the base.**
$$Z_b=\frac{V_i}{I_b}=\beta r_e+(\beta+1)R_E\approx\beta(r_e+R_E)\ \ (\approx\beta R_E\text{ if }R_E\gg r_e).$$
**Step 3:** $\boxed{Z_i=R_B\parallel Z_b}$, and $\boxed{Z_o=R_C}$ (for $r_o\ge10(R_C+R_E)$).
**Step 4: gain.** $I_b=V_i/Z_b$ and $V_o=-\beta I_bR_C=-\beta\dfrac{V_i}{Z_b}R_C$:
$$\boxed{A_v=-\frac{\beta R_C}{Z_b}=-\frac{R_C}{r_e+R_E}}\ \xrightarrow{R_E\gg r_e}\ \boxed{-\frac{R_C}{R_E}},\qquad A_i\approx\beta\ (R_B\gg Z_b).$$

::: kid Why does the bypass capacitor matter so much?
Without $C_E$, the emitter resistor is "in the way" of the signal, and the gain drops from $-R_C/r_e$ (a few hundred) to $-R_C/R_E$ (a few). With $C_E$ the signal skips over $R_E$ (while dc still enjoys the stability $R_E$ gives). **You get stability for dc and gain for ac.** That is the whole point of the bypass capacitor.
:::

::: ex Example 18.2: Your class numerical (self-bias, without and with $C_E$)
*For the self-bias network without $C_E$ (unbypassed) determine $r_e$, $Z_i$, $Z_o$, $A_v$, where $R_B=470\ \text{k}\Omega$, $\beta=120$, $R_C=2.2\ \text{k}\Omega$, $r_o=40\ \text{k}\Omega$, $R_E=0.56\ \text{k}\Omega$.*

**Given:** the dc supply is 20 V (implied by the given $I_B$).

**Step 1: dc base current.** $I_B=\dfrac{V_{CC}-V_{BE}}{R_B+(\beta+1)R_E}$. Denominator: $470\ \text{k}+121\times0.56\ \text{k}=470+67.76=537.76\ \text{k}\Omega$. $I_B=\dfrac{19.3}{537\,760}=35.89\ \mu$A.
**Step 2: dc emitter current.** $I_E=(\beta+1)I_B=121\times35.89\ \mu\text{A}=4.343$ mA.
**Step 3: $r_e$.** $r_e=\dfrac{26\ \text{mV}}{4.343\ \text{mA}}=5.99\ \Omega$.
**Step 4: can we ignore $r_o$?** Test $r_o\ge10(R_C+R_E)$: $10\times(2.2+0.56)\ \text{k}=27.6\ \text{k}$, and $r_o=40\ \text{k}\ge27.6\ \text{k}$ ✓. Yes.
**Step 5: base-side impedance.** $Z_b\approx\beta(r_e+R_E)=120\times(5.99+560)=120\times565.99=67.9\ \text{k}\Omega$.
**Step 6: $Z_i$.** $Z_i=R_B\parallel Z_b=\dfrac{470\times67.92}{470+67.92}\ \text{k}=59.3\ \text{k}\Omega$.
**Step 7: $Z_o$.** $Z_o=R_C=2.2\ \text{k}\Omega$.
**Step 8: $A_v$.** $A_v=-\dfrac{\beta R_C}{Z_b}=-\dfrac{120\times2200}{67\,920}=-3.89$.

**Answer (without $C_E$):** $r_e=5.99\ \Omega$; $Z_i=59.3\ \text{k}\Omega$; $Z_o=2.2\ \text{k}\Omega$; $A_v=-3.89$.

**With $C_E$:** $A_v=-\dfrac{R_C}{r_e}=-\dfrac{2200}{5.99}=-367$. (Your page shows $-369.28$ from slightly different rounding of $r_e$.) The gain rose by a factor of about **95**: "a significant increase".
:::

## 18.5 CE voltage-divider bias

**With bypass:** $Z_i=R_1\parallel R_2\parallel\beta r_e$; $Z_o=R_C\parallel r_o\approx R_C$; $A_v=-R_C/r_e$.
**Without bypass:** $Z_b=\beta(r_e+R_E)$; $Z_i=R_1\parallel R_2\parallel Z_b$; $Z_o=R_C$; $A_v=-R_C/(r_e+R_E)\approx-R_C/R_E$.

::: ex Example 18.3: Divider bias, both cases
**Given:** the bias of Example 17.3: $R_1=82\ \text{k}$, $R_2=22\ \text{k}$, $R_C=5.6\ \text{k}$, $R_E=1.2\ \text{k}$, $\beta=50$, with $I_B=39.6\ \mu$A.

**Step 1:** $I_E=51\times39.6\ \mu\text{A}=2.02$ mA.
**Step 2:** $r_e=\dfrac{26}{2.02}=12.9\ \Omega$; $\beta r_e=50\times12.9=644\ \Omega$.
**Bypassed:**
**Step 3:** $Z_i=R_1\parallel R_2\parallel\beta r_e$: $R_1\parallel R_2=17.35\ \text{k}$; $17\,350\parallel644=\dfrac{17\,350\times644}{17\,350+644}=621\ \Omega$.
**Step 4:** $A_v=-\dfrac{5600}{12.9}=-434$; $Z_o\approx5.6\ \text{k}\Omega$.
**Unbypassed:**
**Step 5:** $Z_b=50\times(12.9+1200)=60.6\ \text{k}\Omega$.
**Step 6:** $Z_i=17.35\ \text{k}\parallel60.6\ \text{k}=\dfrac{17.35\times60.6}{17.35+60.6}=13.5\ \text{k}\Omega$.
**Step 7:** $A_v=-\dfrac{5600}{12.9+1200}=-4.62$.

**Answer:** bypassed: $Z_i=621\ \Omega$, $A_v=-434$. Unbypassed: $Z_i=13.5\ \text{k}\Omega$, $A_v=-4.62$.
:::

## 18.6 Emitter-follower (common-collector) configuration

{{fig c_ac_follower|AC equivalent of the emitter follower: the collector is at ac ground (hence "common collector"); the output is taken from the emitter across $R_E$.|82}}

**Input impedance.** As before: $Z_b=\beta r_e+(\beta+1)R_E\approx\beta(r_e+R_E)\approx\beta R_E$ and $\boxed{Z_i=R_B\parallel Z_b}$.

**Output impedance.** The current in the emitter: $I_b=V_{in}/Z_b$, so
$$I_e=(\beta+1)I_b=\frac{(\beta+1)V_{in}}{\beta r_e+(\beta+1)R_E}\approx\frac{V_{in}}{r_e+R_E}.$$
Looking back into the emitter we see $r_e$ (small) with $R_E$ to ground:
$$\boxed{Z_o=R_E\parallel r_e\approx r_e}\qquad(\text{very small}).$$

**Voltage gain.** $V_o=I_eR_E=\dfrac{R_E\,V_{in}}{R_E+r_e}$:
$$\boxed{A_v=\frac{V_o}{V_{in}}=\frac{R_E}{R_E+r_e}\approx1}.$$
The output is **in phase** with the input (no inversion): the emitter *follows* the base.

::: ex Example 18.4: Emitter follower
**Given:** the bias of Example 17.6: $R_B=240\ \text{k}$, $R_E=2\ \text{k}$, $\beta=90$, $I_E=4.16$ mA.

**Step 1:** $r_e=\dfrac{26}{4.16}=6.25\ \Omega$.
**Step 2:** $Z_b=90\times(6.25+2000)=90\times2006.25=180.6\ \text{k}\Omega$.
**Step 3:** $Z_i=240\ \text{k}\parallel180.6\ \text{k}=\dfrac{240\times180.6}{240+180.6}=103\ \text{k}\Omega$.
**Step 4:** $Z_o=2000\parallel6.25=\dfrac{2000\times6.25}{2006.25}=6.23\ \Omega$.
**Step 5:** $A_v=\dfrac{2000}{2000+6.25}=0.997$.

**Answer:** $Z_i=103\ \text{k}\Omega$; $Z_o=6.23\ \Omega$; $A_v=0.997$.
:::

**Use:** a **buffer**: high input impedance (does not load the source), very low output impedance (can drive a heavy load), voltage gain $\approx1$ but a large current gain.

## 18.7 Collector-feedback configuration

{{fig c_ac_collfb|AC equivalent: $R_{F1}$ appears across the input, $R_{F2}$ across the output (the junction of $R_{F1}$ and $R_{F2}$ is bypassed to ground by a capacitor).|92}}

From your class scan (with $r_o\ge10R_C$):
$$Z_i=R_{F1}\parallel\beta r_e,\qquad Z_o=R_C\parallel R_{F2}\parallel r_o\approx R_C\parallel R_{F2}.$$
**Gain, step by step.** Let $R'=r_o\parallel R_{F2}\parallel R_C$.
**Step 1.** $V_o=-\beta I_bR'$.
**Step 2.** $I_b=\dfrac{V_i}{\beta r_e}$.
**Step 3.** $V_o=-\beta\dfrac{V_i}{\beta r_e}R'$, so
$$\boxed{A_v=\frac{V_o}{V_i}=-\frac{r_o\parallel R_{F2}\parallel R_C}{r_e}}\ \xrightarrow{r_o\ge10R_C}\ -\frac{R_{F2}\parallel R_C}{r_e}.$$

::: ex Example 18.5: Collector feedback
**Given:** Example 17.5: $R_{F1}=91\ \text{k}$, $R_{F2}=110\ \text{k}$, $R_C=3.3\ \text{k}$, $\beta=75$, $I_B=35.5\ \mu$A.

**Step 1:** $I_E=76\times35.5\ \mu\text{A}=2.70$ mA; $r_e=\dfrac{26}{2.70}=9.64\ \Omega$.
**Step 2:** $\beta r_e=75\times9.64=723\ \Omega$; $Z_i=91\ \text{k}\parallel723=717\ \Omega$.
**Step 3:** $Z_o=3.3\ \text{k}\parallel110\ \text{k}=\dfrac{3.3\times110}{113.3}=3.20\ \text{k}\Omega$.
**Step 4:** $A_v=-\dfrac{3204}{9.64}=-332$.

**Answer:** $Z_i=717\ \Omega$; $Z_o=3.20\ \text{k}\Omega$; $A_v=-332$.
:::

## 18.8 Common-base configuration <span class="tag">extra</span>

(The model is in your slides; the results are the standard textbook ones.) $Z_i=R_E\parallel r_e\approx r_e$; $Z_o\approx R_C$; $A_v\approx\dfrac{R_C}{r_e}$ (**positive**, in phase); $A_i\approx-\alpha\approx-1$.

::: ex Example 18.6: Common base
**Given:** Example 17.7: $I_E=2.75$ mA, $R_E=1.2\ \text{k}$, $R_C=2.4\ \text{k}$.
**Step 1:** $r_e=26/2.75=9.45\ \Omega$.
**Step 2:** $Z_i=1200\parallel9.45=9.38\ \Omega$.
**Step 3:** $A_v=R_C/r_e=2400/9.45=254$.
**Answer:** $Z_i\approx9.4\ \Omega$ (very low); $A_v\approx254$ (positive).
:::

## 18.9 Hybrid equivalent model

The transistor is treated as a two-port network and described by its **hybrid ($h$) parameters**:
$$V_i=h_{11}I_i+h_{12}V_o,\qquad I_o=h_{21}I_i+h_{22}V_o.$$

| Parameter | Definition | Meaning | CE name |
|---|---|---|---|
| $h_{11}$ | $\dfrac{V_i}{I_i}\Big|_{V_o=0}$ | **input impedance** | $h_{ie}$ |
| $h_{12}$ | $\dfrac{V_i}{V_o}\Big|_{I_i=0}$ | **reverse voltage ratio** | $h_{re}$ |
| $h_{21}$ | $\dfrac{I_o}{I_i}\Big|_{V_o=0}$ | **forward current ratio** | $h_{fe}$ |
| $h_{22}$ | $\dfrac{I_o}{V_o}\Big|_{I_i=0}$ | **output admittance** | $h_{oe}$ |

{{fig c_hybrid|Hybrid model: input resistance $h_{ie}$, reverse-voltage source $h_{re}V_o$, current source $h_{fe}I_i$, output admittance $h_{oe}$ ($=1/r_o$). Usually $h_{re}$ is ignored.|78}}

**Link to the $r_e$ model** (class notes p. 53):
$$h_{ie}=\beta r_e,\qquad h_{fe}=\beta,\qquad h_{oe}=\frac1{r_o}.$$

### Fixed bias with the hybrid model (class p. 54)
$$\boxed{Z_i=R_B\parallel h_{ie}},\qquad\boxed{Z_o=\frac1{h_{oe}}\parallel R_C\approx R_C},\qquad\boxed{A_i=h_{fe}}.$$
$V_i=h_{ie}I_b$ and $V_o=-I_oZ_o=-h_{fe}I_b\left(\frac1{h_{oe}}\parallel R_C\right)$, so
$$\boxed{A_v=-\frac{h_{fe}R_C}{h_{ie}}}\quad\left(\text{exact: }-\frac{h_{fe}}{h_{ie}}\left(\tfrac1{h_{oe}}\parallel R_C\right)\right).$$
Self-bias (class p. 54 sketch): with the bypass capacitor it reduces to the same result. <span class="tag">extra</span> Without the bypass, replace $h_{ie}$ by $h_{ie}+(1+h_{fe})R_E$: $A_v=-\dfrac{h_{fe}R_C}{h_{ie}+(1+h_{fe})R_E}$.

::: ex Example 18.7: Hybrid-model amplifier
**Given:** $R_B=240\ \text{k}$, $R_C=2.2\ \text{k}$, $h_{ie}=1.5\ \text{k}$, $h_{fe}=100$, $h_{oe}=20\ \mu\text{S}$.

**Step 1: $1/h_{oe}$.** $1/(20\times10^{-6})=50\ \text{k}\Omega$.
**Step 2: $Z_i$.** $240\ \text{k}\parallel1.5\ \text{k}=\dfrac{240\times1.5}{241.5}=1.49\ \text{k}\Omega$.
**Step 3: $Z_o$.** $50\ \text{k}\parallel2.2\ \text{k}=\dfrac{50\times2.2}{52.2}=2.11\ \text{k}\Omega$.
**Step 4: $A_v$ (simple).** $-\dfrac{h_{fe}R_C}{h_{ie}}=-\dfrac{100\times2200}{1500}=-147$. (Exact, using $Z_o=2.11$ k: $-\dfrac{100\times2110}{1500}=-140.5$.)
**Step 5: $A_i$.** $h_{fe}=100$.

**Answer:** $Z_i=1.49\ \text{k}\Omega$; $Z_o=2.11\ \text{k}\Omega$; $A_v\approx-147$ ($-140$ exact); $A_i=100$.
:::

## 18.10 Summary of amplifier behaviour

| | CE | CB | CC (emitter follower) |
|---|---|---|---|
| $Z_i$ | medium ($\beta r_e$) | **very low** ($r_e$) | **high** ($\approx\beta R_E$) |
| $Z_o$ | medium-high ($R_C$) | high ($R_C$) | **very low** ($\approx r_e$) |
| $A_v$ | **large, negative** ($-R_C/r_e$) | large, positive | $\approx1$ |
| $A_i$ | $\beta$ | $\approx1$ | $\approx\beta+1$ |
| Phase | **180°** | 0° | 0° |

## 18.11 Practice

::: try Questions for Chapter 18
1. Give the four steps to obtain the ac equivalent of a transistor amplifier.
2. Fixed bias with $V_{CC}=15$ V, $R_B=470\ \text{k}$, $R_C=3.3\ \text{k}$, $\beta=100$ (Question 1 of Chapter 17). Find $r_e$, $Z_i$, $Z_o$, $A_v$ (ignore $r_o$).
3. Self-bias: $V_{CC}=12$ V, $R_B=330\ \text{k}$, $R_C=2.2\ \text{k}$, $R_E=470\ \Omega$, $\beta=100$ (Question 2 of Chapter 17). Find $A_v$ (a) without and (b) with a bypass capacitor.
4. Emitter follower: $I_E=2$ mA, $R_E=1\ \text{k}$, $R_B=100\ \text{k}$, $\beta=100$. Find $Z_i$, $Z_o$, $A_v$.
5. Hybrid model: $h_{ie}=1.2\ \text{k}$, $h_{fe}=120$, $R_B=470\ \text{k}$, $R_C=2\ \text{k}$. Find $Z_i$, $A_v$, $A_i$.
6. Explain why $r_e$ is a **dc** quantity, and why the CE amplifier inverts the signal.
7. $V_A=100$ V, $I_{CQ}=2$ mA. Find $r_o$.
:::

::: soln Answers and full solutions
<details markdown="1"><summary>Solution 1</summary>

1. Set all dc sources to zero and replace them by short circuits.
2. Replace all capacitors by short circuits.
3. Remove all elements bypassed by those shorts.
4. Redraw the network in a convenient form.
</details>

<details markdown="1"><summary>Solution 2</summary>

**Step 1: dc base current** (from Solution 1 of Ch. 17): $I_B=\dfrac{15-0.7}{470\ \text{k}}=30.4\ \mu$A.
**Step 2:** $I_E=101\times30.4\ \mu\text{A}=3.07$ mA.
**Step 3:** $r_e=\dfrac{26}{3.07}=8.47\ \Omega$; $\beta r_e=847\ \Omega$.
**Step 4:** $Z_i=470\ \text{k}\parallel847\ \Omega=\dfrac{470\,000\times847}{470\,847}=845\ \Omega$.
**Step 5:** $Z_o=R_C=3.3\ \text{k}\Omega$.
**Step 6:** $A_v=-\dfrac{R_C}{r_e}=-\dfrac{3300}{8.47}=-390$.

**Answer:** $r_e=8.47\ \Omega$; $Z_i\approx845\ \Omega$; $Z_o=3.3\ \text{k}\Omega$; $A_v=-390$.
</details>

<details markdown="1"><summary>Solution 3</summary>

**Step 1:** from Ch. 17: $I_B=29.9\ \mu$A, so $I_E=101\times29.9\ \mu\text{A}=3.02$ mA and $r_e=\dfrac{26}{3.02}=8.6\ \Omega$.
**(a) Without $C_E$:**
**Step 2:** $Z_b=\beta(r_e+R_E)=100\times(8.6+470)=47.9\ \text{k}\Omega$.
**Step 3:** $A_v=-\dfrac{\beta R_C}{Z_b}=-\dfrac{100\times2200}{47\,900}=-4.59$ (equivalently $-\dfrac{R_C}{r_e+R_E}=-\dfrac{2200}{478.6}=-4.6$).
**(b) With $C_E$:**
**Step 4:** $A_v=-\dfrac{R_C}{r_e}=-\dfrac{2200}{8.6}=-256$.

**Answer:** (a) $A_v\approx-4.6$; (b) $A_v\approx-256$.
</details>

<details markdown="1"><summary>Solution 4</summary>

**Step 1:** $r_e=\dfrac{26}{2}=13\ \Omega$.
**Step 2:** $Z_b=\beta(r_e+R_E)=100\times1013=101.3\ \text{k}\Omega$.
**Step 3:** $Z_i=R_B\parallel Z_b=100\ \text{k}\parallel101.3\ \text{k}=\dfrac{100\times101.3}{201.3}=50.3\ \text{k}\Omega$.
**Step 4:** $Z_o=R_E\parallel r_e=\dfrac{1000\times13}{1013}=12.8\ \Omega$.
**Step 5:** $A_v=\dfrac{R_E}{R_E+r_e}=\dfrac{1000}{1013}=0.987$.

**Answer:** $Z_i=50.3\ \text{k}\Omega$; $Z_o=12.8\ \Omega$; $A_v=0.987$.
</details>

<details markdown="1"><summary>Solution 5</summary>

**Step 1:** $Z_i=R_B\parallel h_{ie}=470\ \text{k}\parallel1.2\ \text{k}=\dfrac{470\times1.2}{471.2}=1.197\ \text{k}\Omega$.
**Step 2:** $A_v=-\dfrac{h_{fe}R_C}{h_{ie}}=-\dfrac{120\times2000}{1200}=-200$.
**Step 3:** $A_i=h_{fe}=120$.
</details>

<details markdown="1"><summary>Solution 6</summary>

**$r_e$ is a dc quantity** because $r_e=26\ \text{mV}/I_E$ uses the **dc** emitter current at the Q-point; changing the bias changes $r_e$ (the diode's ac resistance depends on where you bias it).
**Inversion:** when the input rises, $I_B$ and $I_C$ rise, so the drop $I_CR_C$ across the collector resistor increases and the collector voltage $V_C=V_{CC}-I_CR_C$ **falls**. Output moves opposite to input: 180° phase shift.
</details>

<details markdown="1"><summary>Solution 7</summary>

**Formula:** $r_o\approx V_A/I_{CQ}$.
**Step 1.** $r_o=\dfrac{100\ \text{V}}{2\times10^{-3}\ \text{A}}=50\,000\ \Omega$.

**Answer:** **50 kΩ**.
</details>
:::
