# Chapter 18: AC analysis of the BJT

*Class notes pp. 46–54 · slides: AC Analysis re model of BJT · scans: “CE emitter-bias”, “Emitter follower”, “Collector DC feedback”*

::: kid Two jobs: “set the tap” and “wiggle the tap”
In Chapter 17 you **set** the transistor to its resting point using dc. Now a tiny signal (a voice, a radio wave) is added on top and makes the operating point **wiggle a little** around Q. For the wiggles we do not need the whole complicated transistor: we replace it by a **simple cartoon** made of a resistor and a current source, the **small-signal model**. Then the amplifier is just resistors and one “controlled current source”, and we can calculate **how big the input and output resistances are** ($Z_i$, $Z_o$) and **how much it amplifies** ($A_v$, $A_i$).
:::

## 18.1 Small-signal ac analysis

A **model** is an equivalent circuit that represents the ac characteristics of the transistor, using circuit elements that approximate its behaviour under specific operating conditions. Two models are commonly used in small-signal ac analysis (class notes p. 46):

1. **$r_e$ model**
2. **Hybrid equivalent model**

### Steps to get the ac equivalent circuit

1. Set all **dc sources to zero** and replace them by a **short circuit** (the supply $V_{CC}$ becomes an ac ground).
2. Replace all **capacitors** by a **short circuit** (coupling and bypass capacitors are “big” at signal frequencies).
3. **Remove all elements bypassed** by the short circuits from steps 1 and 2.
4. **Redraw** the network in a more convenient form.

### The four parameters of any amplifier

$$Z_i=\frac{V_i}{I_i},\qquad Z_o=\frac{V_o}{I_o}\Big|_{V_s=0},\qquad A_v=\frac{V_o}{V_i},\qquad A_i=\frac{I_o}{I_i}$$

(input impedance, output impedance, voltage gain, current gain).

## 18.2 The $r_e$ model

BJTs are basically **current-controlled devices**, so the $r_e$ model uses **a diode and a current source** to duplicate the behaviour of the transistor. *Disadvantage:* it is **sensitive to the dc level** (because $r_e$ depends on the operating current), so it is designed for specific circuit conditions.

### CE model

{{fig c_re_model_diode|CE $r_e$ model: the base–emitter diode has ac resistance $r_e$; the collector supplies a current $\beta I_b$.|68}}

Look into the base: $V_{be}=I_er_e=(I_c+I_b)r_e=(\beta I_b+I_b)r_e=(\beta+1)I_br_e$. So
$$\boxed{Z_i=\frac{V_{be}}{I_b}=(\beta+1)r_e\approx\beta r_e}$$
The diode is replaced by its ac resistance, seen from the base as $\beta r_e$:

{{fig c_re_model_ce|Improved CE model with $\beta r_e$ at the input, the controlled source $\beta I_b$ and the output resistance $r_o$.|68}}

**The value of $r_e$** (dc quantity!):
$$\boxed{r_e=\frac{26\ \text{mV}}{I_E}}\qquad(I_E\text{ is the dc emitter current at the Q-point})$$
(It is the diode’s ac resistance $\eta V_T/I$ with $\eta=1$ and $V_T\approx26$ mV.)

**Early voltage and $r_o$.** In the output characteristic the constant-$I_B$ curves have a slight upward slope; extended backward they meet the $V_{CE}$-axis at $-V_A$ (**Early voltage**).

{{fig p_early|Early effect: the extended lines meet at $-V_A$; the slope of each line is $1/r_o$.|66}}

$$r_o=\frac{\Delta V}{\Delta I}=\frac{V_A+V_{CEQ}}{I_{CQ}}\ \approx\ \boxed{\frac{V_A}{I_{CQ}}}$$
A large $r_o$ (tens of kΩ) is in parallel with the current source; often ignored when $r_o\ge10R_C$.

### CB model

{{fig c_re_model_cb|CB $r_e$ model: input $r_e$, source $\alpha I_e\approx I_e$, output $r_o$.|68}}

In the common-base configuration the input looks into the emitter: $\boxed{Z_i=r_e}$ (small!). The output source is $\alpha I_e$ (with $\alpha\approx1$).

### CC model
For the common-collector configuration the **CE model is used** (no separate model), as your slide states.

### npn vs pnp
The **dc** analysis differs (currents and voltages reversed), but for **ac** the equivalent circuit is **the same**, because the signal swings both positive and negative.

### Key results to memorise (class note p. 47)

| Configuration | Input impedance seen at the transistor |
|---|---|
| CE | $\beta r_e$ (more exactly $(\beta+1)r_e$) |
| CB | $r_e$ |

### Phase relationship

{{fig p_ac_phase|CE amplifier: the output is amplified and **inverted** (180° phase shift), riding on the dc level $V_{CEQ}$.|68}}

## 18.3 CE fixed-bias configuration

{{fig c_ac_fixed|AC equivalent of the CE fixed-bias amplifier ($V_{CC}$ and capacitors removed; $R_B$, $\beta r_e$, $\beta I_b$, $r_o$, $R_C$ all connected between the signal line and ground).|92}}

Reading the picture:
* **Input impedance:** $\boxed{Z_i=R_B\parallel\beta r_e}$ (≈ $\beta r_e$ since $R_B\gg\beta r_e$).
* **Output impedance:** $\boxed{Z_o=r_o\parallel R_C}$; if $r_o\ge10R_C$: $Z_o\approx R_C$.
* **Voltage gain:** the input voltage is $V_i=I_b\,\beta r_e$ ⇒ $I_b=\dfrac{V_i}{\beta r_e}$. Output: $V_o=-I_oZ_o=-\beta I_b(r_o\parallel R_C)=-\beta\dfrac{V_i}{\beta r_e}(r_o\parallel R_C)$:
$$\boxed{A_v=\frac{V_o}{V_i}=-\frac{r_o\parallel R_C}{r_e}}\ \xrightarrow{r_o\ge10R_C}\ \boxed{A_v\approx-\frac{R_C}{r_e}}$$
(The minus sign = 180° phase reversal. Class page 48 writes “$R_c/R_e$” but it means the small $r_e$.)
* **Current gain:** $A_i=\dfrac{I_o}{I_i}=\dfrac{I_c}{I_b}=\dfrac{\beta I_b}{I_b}=\boxed{\beta}$ (when $R_B\gg\beta r_e$ and $r_o\gg R_C$; in general $A_i=\beta\dfrac{R_B}{R_B+\beta r_e}\dfrac{r_o}{r_o+R_C}$).

::: ex Example 18.1 (fixed bias of Example 17.1, $V_{CC}=12$ V, $R_B=240$ k, $R_C=2.2$ k, $\beta=50$)
dc: $I_B=47.08\ \mu$A; $I_E=(\beta+1)I_B=51\times47.08\ \mu=\mathbf{2.40\ mA}$.
$r_e=26\text{ mV}/2.40\text{ mA}=\mathbf{10.8\ \Omega}$; $\beta r_e=541\ \Omega$.
* $Z_i=240\text{k}\parallel541=\mathbf{540\ \Omega}$
* $Z_o\approx R_C=\mathbf{2.2\ k\Omega}$ (if $r_o=50$ kΩ: $Z_o=2.2\text{k}\parallel50\text{k}=2.11$ kΩ)
* $A_v=-R_C/r_e=-2200/10.8=\mathbf{-203}$ (with $r_o=50$ k: $-2107/10.8=-195$)
* $A_i=\beta=\mathbf{50}$
:::

## 18.4 CE self-bias (emitter-bias) configuration

Class p. 48 draws the circuit and asks two cases.

### Case 1: with the bypass capacitor $C_E$

$C_E$ shorts $R_E$ for ac, so the ac circuit is the same as fixed bias:
$$Z_i=R_B\parallel\beta r_e,\qquad Z_o=R_C\parallel r_o\approx R_C,\qquad A_v=-\frac{R_C}{r_e},\qquad A_i\approx\beta$$

### Case 2: without the bypass capacitor

{{fig c_ac_unbypassed|AC equivalent without $C_E$: the emitter current $I_e=(\beta+1)I_b$ flows through $R_E$.|82}}

The base current flows through $\beta r_e$; the emitter current $I_e=(\beta+1)I_b$ flows through $R_E$. From the base looking in ($V_i$ across the base–ground):
$$V_i=I_b\beta r_e+I_eR_E=I_b\beta r_e+(\beta+1)I_bR_E$$
$$Z_b=\frac{V_i}{I_b}=\beta r_e+(\beta+1)R_E\approx\beta(r_e+R_E)\ \ (\approx\beta R_E\ \text{if }R_E\gg r_e)$$
$$\boxed{Z_i=R_B\parallel Z_b},\qquad\boxed{Z_o=R_C}\ \ (\text{for }r_o\ge10(R_C+R_E))$$
Gain: $I_b=V_i/Z_b$; $V_o=-I_oR_C=-\beta I_bR_C=-\beta\dfrac{V_i}{Z_b}R_C$:
$$\boxed{A_v=-\frac{\beta R_C}{Z_b}=-\frac{R_C}{r_e+R_E}}\ \xrightarrow{R_E\gg r_e}\ \boxed{-\frac{R_C}{R_E}},\qquad A_i\approx\beta\ (\text{if }R_B\gg Z_b)$$

::: kid Why does the bypass capacitor matter so much?
Without $C_E$, the emitter resistor is “in the way” of the signal: the gain drops from $-R_C/r_e$ (a few hundred) to $-R_C/R_E$ (a few). With $C_E$ the signal skips $R_E$ (while the dc bias still enjoys the stability $R_E$ provides). **You get stability for dc and gain for ac.** That is the whole point of the bypass capacitor.
:::

::: ex Example 18.2 (your class numerical: self-bias, without and with $C_E$)
*For the self-bias network without $C_E$ (unbypassed) determine $r_e$, $Z_i$, $Z_o$, $A_v$, where $R_B=470\ \text{k}\Omega$, $\beta=120$, $R_C=2.2\ \text{k}\Omega$, $r_o=40\ \text{k}\Omega$, $R_E=0.56\ \text{k}\Omega$.*

DC: $V_{CC}=20$ V (implied by the $I_B$ given): 
$$I_B=\frac{V_{CC}-V_{BE}}{R_B+(\beta+1)R_E}=\frac{19.3}{470\text{k}+121(0.56\text{k})}=\frac{19.3}{537.8\text{k}}=\mathbf{35.89\ \mu A}$$
$I_E=(\beta+1)I_B=121\times35.89\ \mu=\mathbf{4.34\ mA}$; $r_e=\dfrac{26\text{ mV}}{4.34\text{ mA}}=\mathbf{5.99\ \Omega}$.

(b) Check $r_o\ge10(R_C+R_E)$: $40\text{k}\ge10(2.2\text{k}+0.56\text{k})=27.6$ k ✓ satisfied, so ignore $r_o$.

$Z_b\approx\beta(r_e+R_E)=120(5.99+560)=\mathbf{67.9\ k\Omega}$
$Z_i=R_B\parallel Z_b=470\text{k}\parallel67.92\text{k}=\mathbf{59.3\ k\Omega}$
$Z_o=R_C=\mathbf{2.2\ k\Omega}$
$A_v=-\dfrac{\beta R_C}{Z_b}=-\dfrac{120\times2200}{67{,}920}=\mathbf{-3.89}$

**With $C_E$:** $A_v=-\dfrac{R_C}{r_e}=-\dfrac{2200}{5.99}=\mathbf{-367}$ (your page has −369.28 from slightly different rounding of $r_e$). “A significant increase” (~95×).
:::

## 18.5 CE voltage-divider bias

With bypass: $Z_i=R_1\parallel R_2\parallel\beta r_e$; $Z_o=R_C\parallel r_o\approx R_C$; $A_v=-R_C/r_e$.
Without bypass: $Z_b=\beta(r_e+R_E)$; $Z_i=R_1\parallel R_2\parallel Z_b$; $Z_o=R_C$; $A_v=-R_C/(r_e+R_E)\approx-R_C/R_E$.

::: ex Example 18.3 (bias of Example 17.3: $R_1=82$ k, $R_2=22$ k, $R_C=5.6$ k, $R_E=1.2$ k, $\beta=50$)
$I_B=39.6\ \mu$A, $I_E=51\times39.6\ \mu=2.02$ mA, $r_e=26/2.02=12.9\ \Omega$.
* **Bypassed:** $Z_i=82\text{k}\parallel22\text{k}\parallel(50\times12.9=644\ \Omega)=\mathbf{621\ \Omega}$; $A_v=-5600/12.9=\mathbf{-435}$; $Z_o\approx5.6$ kΩ.
* **Unbypassed:** $Z_b=50(12.9+1200)=60.6$ kΩ; $Z_i=17.35\text{k}\parallel60.6\text{k}=\mathbf{13.5\ k\Omega}$; $A_v=-5600/1212.9=\mathbf{-4.62}$.
:::

## 18.6 Emitter-follower (common-collector) configuration

{{fig c_ac_follower|AC equivalent of the emitter follower: the collector is at ac ground (hence “common collector”); the output is taken from the emitter across $R_E$.|82}}

**Input impedance:**
$$Z_b=\beta r_e+(\beta+1)R_E\approx\beta(r_e+R_E)\approx\beta R_E,\qquad\boxed{Z_i=R_B\parallel Z_b}$$
**Output impedance:** $I_b=V_{in}/Z_b$, so
$$I_e=(\beta+1)I_b=\frac{(\beta+1)V_{in}}{\beta r_e+(\beta+1)R_E}\approx\frac{V_{in}}{r_e+R_E}$$
Looking back into the emitter: $r_e$ in series with the source; $R_E$ to ground:
$$\boxed{Z_o=R_E\parallel r_e\approx r_e}\quad(\text{very small})$$
**Voltage gain:** $V_o=I_eR_E=\dfrac{R_EV_{in}}{R_E+r_e}$:
$$\boxed{A_v=\frac{V_o}{V_{in}}=\frac{R_E}{R_E+r_e}\approx1}$$
Output **in phase** with input (no inversion): the emitter *follows* the base.

::: ex Example 18.4 (Example 17.6: $R_B=240$ k, $R_E=2$ k, $\beta=90$, $I_E=4.16$ mA)
$r_e=26/4.16=6.25\ \Omega$. $Z_b=90(6.25+2000)=180.6$ kΩ; $Z_i=240\text{k}\parallel180.6\text{k}=\mathbf{103\ k\Omega}$; $Z_o=2\text{k}\parallel6.25=\mathbf{6.23\ \Omega}$; $A_v=\dfrac{2000}{2006.25}=\mathbf{0.997}$.
:::

**Use:** a **buffer**: high input impedance (does not load the source), very low output impedance (can drive a heavy load), voltage gain ≈ 1 but large current gain.

## 18.7 Collector-feedback configuration

{{fig c_ac_collfb|AC equivalent: $R_{F1}$ appears across the input, $R_{F2}$ across the output (the junction of $R_{F1}$ and $R_{F2}$ is bypassed to ground by a capacitor).|92}}

From the class scan (with $r_o\ge10R_C$):
$$Z_i=R_{F1}\parallel\beta r_e,\qquad Z_o=R_C\parallel R_{F2}\parallel r_o\ \approx\ R_C\parallel R_{F2}$$
Gain: with $R'=r_o\parallel R_{F2}\parallel R_C$, $V_o=-\beta I_bR'$ and $I_b=V_i/\beta r_e$:
$$\boxed{A_v=\frac{V_o}{V_i}=-\frac{r_o\parallel R_{F2}\parallel R_C}{r_e}}\ \xrightarrow{r_o\ge10R_C}\ -\frac{R_{F2}\parallel R_C}{r_e}$$

::: ex Example 18.5 (Example 17.5: $R_{F1}=91$ k, $R_{F2}=110$ k, $R_C=3.3$ k, $\beta=75$, $I_B=35.5\ \mu$A)
$I_E=76\times35.5\ \mu=2.70$ mA, $r_e=9.64\ \Omega$. $Z_i=91\text{k}\parallel(75\times9.64=723)=\mathbf{717\ \Omega}$; $Z_o=3.3\text{k}\parallel110\text{k}=\mathbf{3.20\ k\Omega}$; $A_v=-3204/9.64=\mathbf{-332}$.
:::

## 18.8 Common-base configuration <span class="tag">extra</span>

(The model is in your slides; the results below are the standard textbook ones.) $Z_i=R_E\parallel r_e\approx r_e$; $Z_o\approx R_C$; $A_v\approx\dfrac{R_C}{r_e}$ (**positive**: in phase); $A_i\approx-\alpha\approx-1$.

Example 17.7: $I_E=2.75$ mA, $r_e=26/2.75=9.45\ \Omega$; $Z_i=1.2\text{k}\parallel9.45=9.38\ \Omega$; $A_v=2400/9.45=254$.

## 18.9 Hybrid equivalent model

A general **two-port** with the hybrid ($h$) parameters:
$$V_i=h_{11}I_i+h_{12}V_o,\qquad I_o=h_{21}I_i+h_{22}V_o\qquad\Longleftrightarrow\qquad\begin{bmatrix}V_i\\I_o\end{bmatrix}=\begin{bmatrix}h_{11}&h_{12}\\h_{21}&h_{22}\end{bmatrix}\begin{bmatrix}I_i\\V_o\end{bmatrix}$$

| Parameter | Definition | Meaning | CE name |
|---|---|---|---|
| $h_{11}$ | $\dfrac{V_i}{I_i}\Big|_{V_o=0}$ | **input impedance** | $h_{ie}$ |
| $h_{12}$ | $\dfrac{V_i}{V_o}\Big|_{I_i=0}$ | **reverse voltage ratio** | $h_{re}$ |
| $h_{21}$ | $\dfrac{I_o}{I_i}\Big|_{V_o=0}$ | **forward current ratio** | $h_{fe}$ |
| $h_{22}$ | $\dfrac{I_o}{V_o}\Big|_{I_i=0}$ | **output admittance** | $h_{oe}$ |

{{fig c_hybrid|Hybrid model: input resistance $h_{ie}$, reverse-voltage source $h_{re}V_o$, current source $h_{fe}I_i$, output admittance $h_{oe}$ (=1/$r_o$). Usually $h_{re}$ is ignored.|78}}

**Link to the $r_e$ model** (class notes, p. 53):
$$h_{ie}=\beta r_e,\qquad h_{fe}=\beta,\qquad h_{oe}=\frac{1}{r_o}$$

### Fixed bias with the hybrid model (class p. 54)

$$\boxed{Z_i=R_B\parallel h_{ie}},\qquad\boxed{Z_o=\frac1{h_{oe}}\parallel R_C\approx R_C},\qquad\boxed{A_i=h_{fe}}$$
$V_i=h_{ie}I_b$ and $V_o=-I_oZ_o=-h_{fe}I_b\left(\frac1{h_{oe}}\parallel R_C\right)$, so
$$\boxed{A_v=-\frac{h_{fe}R_C}{h_{ie}}}\quad\left(\text{exact: }-\frac{h_{fe}}{h_{ie}}\left(\tfrac1{h_{oe}}\parallel R_C\right)\right)$$
Self-bias (class p. 54 sketch): with the bypass capacitor it reduces to the same result; <span class="tag">extra</span> without the bypass replace $h_{ie}$ by $h_{ie}+(1+h_{fe})R_E$: $A_v=-\dfrac{h_{fe}R_C}{h_{ie}+(1+h_{fe})R_E}$.

::: ex Example 18.6
$R_B=240$ k, $R_C=2.2$ k, $h_{ie}=1.5$ k, $h_{fe}=100$, $h_{oe}=20\ \mu$S ($1/h_{oe}=50$ k). $Z_i=240\text{k}\parallel1.5\text{k}=\mathbf{1.49\ k\Omega}$; $Z_o=50\text{k}\parallel2.2\text{k}=\mathbf{2.11\ k\Omega}$; $A_v\approx-\dfrac{100\times2200}{1500}=\mathbf{-147}$ (exact with $1/h_{oe}$: $-140$); $A_i=\mathbf{100}$.
:::

## 18.10 Summary of amplifier behaviour

| | CE | CB | CC (emitter follower) |
|---|---|---|---|
| $Z_i$ | medium ($\beta r_e$) | **very low** ($r_e$) | **high** ($\approx\beta R_E$) |
| $Z_o$ | medium-high ($R_C$) | high ($R_C$) | **very low** ($\approx r_e$) |
| $A_v$ | **large, negative** ($-R_C/r_e$) | large, positive | $\approx1$ |
| $A_i$ | $\beta$ | $\approx1$ | $\approx\beta+1$ |
| Phase | **180°** | 0° | 0° |

## 18.11 Try it yourself

::: try Chapter 18 questions
1. Give the four steps to obtain the ac equivalent of a transistor amplifier.
2. Fixed bias, $V_{CC}=15$ V, $R_B=470$ k, $R_C=3.3$ k, $\beta=100$ (Q1 of Chapter 17). Find $r_e$, $Z_i$, $Z_o$, $A_v$ (ignore $r_o$).
3. Self-bias: $V_{CC}=12$ V, $R_B=330$ k, $R_C=2.2$ k, $R_E=470\ \Omega$, $\beta=100$ (Q2 of Chapter 17). Find $A_v$ (a) without and (b) with a bypass capacitor.
4. Emitter follower: $I_E=2$ mA, $R_E=1$ kΩ, $R_B=100$ kΩ, $\beta=100$. Find $Z_i$, $Z_o$, $A_v$.
5. Hybrid model: $h_{ie}=1.2$ kΩ, $h_{fe}=120$, $R_B=470$ kΩ, $R_C=2$ kΩ. Find $Z_i$, $A_v$, $A_i$.
6. Explain why $r_e$ is a **dc** quantity, and why the CE amplifier inverts the signal.
7. Early voltage $V_A=100$ V, $I_{CQ}=2$ mA. Find $r_o$.

<details markdown="1"><summary>Answers</summary>

1. Set dc sources to zero (short circuit); replace capacitors by short circuits; remove elements bypassed by those shorts; redraw.
2. $I_B=30.4\ \mu$A, $I_E=3.07$ mA; $r_e=26/3.07=\mathbf{8.46\ \Omega}$; $Z_i=470\text{k}\parallel846=\mathbf{844\ \Omega}$; $Z_o=\mathbf{3.3\ k\Omega}$; $A_v=-3300/8.46=\mathbf{-390}$.
3. $I_E=3.02$ mA, $r_e=8.6\ \Omega$. (a) $Z_b=100(8.6+470)=47.9$ k; $A_v=-\beta R_C/Z_b=\mathbf{-4.6}$. (b) $A_v=-R_C/r_e=\mathbf{-256}$.
4. $r_e=26/2=13\ \Omega$; $Z_b=100(13+1000)=101.3$ k; $Z_i=100\text{k}\parallel101.3\text{k}=\mathbf{50.3\ k\Omega}$; $Z_o=1000\parallel13=\mathbf{12.8\ \Omega}$; $A_v=1000/1013=\mathbf{0.987}$.
5. $Z_i=470\text{k}\parallel1.2\text{k}=\mathbf{1.197\ k\Omega}$; $A_v=-120\times2000/1200=\mathbf{-200}$; $A_i=\mathbf{120}$.
6. $r_e=26\text{ mV}/I_E$ with $I_E$ the **dc** bias current, so it depends on the Q-point. A rise in $V_i$ increases $I_B$ and $I_C$, so more drop across $R_C$ and a *lower* collector voltage: the output moves opposite to the input.
7. $r_o\approx V_A/I_{CQ}=100/2\text{ mA}=\mathbf{50\ k\Omega}$.
</details>
:::
