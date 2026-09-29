# Chapter 2: The PN junction diode

*Class notes p. 1 · slides: p-n Junction Diode; Unit-I First part, Topics 2–6*

::: words
| Word / symbol | Plain meaning |
|---|---|
| Diode | 2-terminal device that lets current through mainly one way |
| Anode (A) / Cathode (K) | terminal where current enters (P side) / leaves (N side, marked by the bar) |
| Bias | connecting a battery/voltage across the device |
| Forward / reverse bias | + to P and − to N (diode ON) / the opposite (diode OFF) |
| Depletion region | thin layer at the junction with no free carriers, only fixed ions |
| Potential barrier | the "wall" voltage (about 0.7 V Si, 0.3 V Ge) that carriers must overcome |
| Knee / cut-in voltage $V_\gamma$ | forward voltage where current starts to rise quickly |
| $I_0$ | **reverse saturation current**: the tiny leakage current in reverse bias |
| $V_D$, $I_D$ | voltage across, and current through, the diode |
| $V_T$ | thermal voltage $=T/11600\approx26$ mV at 300 K ($T$ in kelvin) |
| $\eta$ | "eta": 1 for germanium, 2 for silicon |
| $r_d$ or $r_{ac}$ | dynamic (ac) resistance: slope $\Delta V/\Delta I$ of the curve |
| $R_{dc}$ | static (dc) resistance $V/I$ at a point |
| $R_f$ | forward resistance of a diode in a model |
| $C_T$, $C_D$ | transition (reverse-bias) capacitance, diffusion (forward-bias) capacitance |
| $\tau$ | "tau": average lifetime of a carrier |
| PIV | peak inverse voltage: the largest reverse voltage the diode can take |
| Breakdown | sudden large reverse current at a high enough reverse voltage |
| $V_{BR}$ or $V_Z$ | the breakdown (Zener) voltage |
:::

::: kid A diode is a one-way street for electricity
Electric current is like water in a pipe. A **diode** is a pipe with a **flap valve**: water flows one way easily and the flap shuts the other way. The two ends are the **anode** (where current *enters*) and **cathode** (where it *leaves*); the arrow in the symbol points the allowed direction. The valve needs a small push to open: about **0.7 volts for silicon** and **0.3 volts for germanium**. Push too hard backwards and the valve breaks (breakdown).
:::

## 2.1 What a PN diode is

A **PN junction diode** is a 2-terminal, 2-layer, single-junction device made from one crystal of silicon or germanium, one side doped **P** (acceptors) and the other **N** (donors). The junction has to be made **inside one continuous crystal**. You cannot simply press a P block against an N block, because the crystal structure would be broken at the boundary and it would not work. Uses: switch, rectifier, regulator, clipper, clamper, voltage multiplier, detector, logic gates.

Diodes are classed by how much forward current they can carry: about 100 mA (low-current), 500 mA (medium), several amperes (power diodes).

## 2.2 No bias, forward bias, reverse bias

{{fig p_pn_bias|The depletion region (hatched) at zero bias, forward bias and reverse bias.|95}}

### No bias (nothing connected)
1. Electrons near the junction **diffuse** from N to P; holes diffuse from P to N. They meet and **recombine** (cancel).
2. The N side has lost electrons, so its layer near the junction is left with fixed **positive** ions. The P side has gained electrons, so its layer is left with fixed **negative** ions.
3. This carrier-free, charged layer is the **depletion region** (also called space-charge or transition region). It is about $10^{-6}$ m thick.
4. The ions create an electric field that pushes carriers back. This is the **potential barrier**: about **0.3 V (Ge)** and **0.7 V (Si)** as given in the slides.
5. The diffusion current (carriers spreading) and the drift current (carriers pushed back by the field) are equal and opposite. **Net current = 0.**
6. The width depends on doping: **heavy doping → thin** layer; **light doping → thick** layer.

### Forward bias (battery + to P, − to N)
1. The battery pushes majority carriers toward the junction, so the depletion region **narrows** and the barrier **falls**.
2. When the applied voltage exceeds the knee (cut-in) voltage, the barrier is almost gone and current rises **exponentially** (milliamperes).
3. Electrons carry the current in the N region, holes in the P region. At the junction they recombine, and the battery keeps supplying new ones.

### Reverse bias (battery − to P, + to N)
1. Electrons and holes are pulled *away* from the junction, so the depletion region **widens** and the barrier **rises**.
2. The majority current falls to zero.
3. Only **thermally generated minority carriers** can cross, giving a tiny current $I_0$ (µA for Ge, nA for Si).
4. It is called *saturation* current because it hardly increases when the reverse voltage increases (until breakdown).

::: trap Which terminal is which?
Forward bias = **positive to anode (P)**. Reverse bias = **positive to cathode (N)**. In exam circuits the battery is often drawn "upside-down": always check the polarity first, then decide ON or OFF.
:::

## 2.3 The V–I characteristic

{{fig p_diode_iv|Forward (mA scale) and reverse (µA scale) characteristics. The scales are different on purpose.|95}}

* **Forward:** almost no current until the **knee (cut-in / threshold) voltage** $V_\gamma$: **0.3 V Ge, 0.7 V Si**. After that the current rises rapidly.
* **Reverse:** a very small, nearly constant current until the **breakdown voltage** $V_{BR}$, then a sharp rise. Germanium leaks much more than silicon.
* This graph describes the **dc behaviour** of the diode.

| | Germanium | Silicon |
|---|---|---|
| Cut-in voltage | 0.3 V | 0.7 V |
| Reverse saturation current | µA | nA |
| $\eta$ | 1 | 2 |

::: flag Two "barrier" numbers appear in your slides
The slides say **0.7 V / 0.3 V** (the knee on the V–I curve) and, in the capacitance formula, a barrier voltage $V_B$ of **0.6 V (Si) / 0.2 V (Ge)**. They are related but not identical: the knee is where current becomes noticeable; the built-in potential $V_0$ (Chapter 13) is the barrier at equilibrium. For circuit problems use **0.7 V / 0.3 V** unless the question gives another value.
:::

## 2.4 The diode current equation

$$I_D=I_0\left(e^{V_D/\eta V_T}-1\right),\qquad V_T=\frac{T}{11600}$$

* $I_D$ is the current through the diode; $I_0$ is the reverse saturation current.
* $V_D$ is the voltage across the diode: **positive for forward bias**, negative for reverse bias.
* $V_T$ is the thermal voltage with $T$ in kelvin. At 300 K: $V_T=300/11600=0.02586$ V $\approx26$ mV.
* $\eta=1$ for Ge and $2$ for Si.
* Since $1/V_T\approx40\ \text{V}^{-1}$, your slides write $I=I_0\left(e^{40V/\eta}-1\right)$, so **Ge:** $I_0(e^{40V}-1)$ and **Si:** $I_0(e^{20V}-1)$.

**Two limiting cases (both in your class notes):**

* **Forward, $V_D\gg\eta V_T$** (say $V_D>0.1$ V): the exponential is huge, so the "$-1$" does not matter: $I_D\approx I_0e^{V_D/\eta V_T}$.
* **Reverse, large negative $V_D$:** $e^{-|V_D|/\eta V_T}\to0$, so $I_D\approx-I_0$. The minus sign only says the current flows backward. It stays at $-I_0$ until breakdown.

::: kid Why an exponential?
Picture a hill (the barrier). Carriers get over it only if they have enough energy, and the number of carriers with a given energy falls off exponentially. Lowering the hill by just a little suddenly lets **many more** carriers over. So the current does not rise politely; it explodes.
:::

::: ex Example 2.1: Forward current of a germanium diode
**Given:** Ge diode ($\eta=1$), $I_0=1\ \mu\text{A}=10^{-6}$ A, $T=300$ K, $V_D=0.2$ V.

**Find:** $I_D$.

**Formula:** $I_D=I_0\left(e^{V_D/\eta V_T}-1\right)$.

**Step 1: thermal voltage.** $V_T=300/11600=0.02586$ V.

**Step 2: the exponent.** $\dfrac{V_D}{\eta V_T}=\dfrac{0.2}{1\times0.02586}=7.734$.

**Step 3: the exponential.** $e^{7.734}=2285$ (use a calculator: $e^{7}=1096.6$, $e^{0.734}=2.083$, product 2285).

**Step 4: subtract 1 and multiply.** $I_D=10^{-6}\times(2285-1)=10^{-6}\times2284=2.284\times10^{-3}$ A.

**Answer:** $I_D\approx\mathbf{2.28\ mA}$.

**What it means:** only 0.2 V gives milliamperes in germanium. The "−1" changed the answer by 0.04 % here, which is why it is dropped in the forward case.
:::

::: ex Example 2.2: The same diode in reverse
**Given:** same diode, $V_D=-5$ V.

**Find:** $I_D$.

**Step 1.** $\dfrac{V_D}{\eta V_T}=\dfrac{-5}{0.02586}=-193.3$.
**Step 2.** $e^{-193.3}\approx10^{-84}$, which is zero for all practical purposes.
**Step 3.** $I_D=I_0(0-1)=-I_0=-1\ \mu\text{A}$.

**Answer:** $\mathbf{-1\ \mu A}$ (1 µA flowing in the reverse direction).

**What it means:** doubling the reverse voltage to −10 V gives the same current. That is why $I_0$ is called *saturation* current.
:::

::: ex Example 2.3: Forward current of a silicon diode ($\eta=2$)
**Given:** Si diode, $I_0=10$ nA $=10^{-8}$ A, $T=300$ K, $V_D=0.6$ V.

**Find:** $I_D$.

**Step 1.** $V_T=0.02586$ V, so $\eta V_T=2\times0.02586=0.05172$ V.
**Step 2.** Exponent: $0.6/0.05172=11.60$.
**Step 3.** $e^{11.60}=1.09\times10^{5}$ ($e^{11}=59\,874$, $e^{0.6}=1.822$, product $109\,100$).
**Step 4.** $I_D=10^{-8}\times1.09\times10^{5}=1.09\times10^{-3}$ A.

**Answer:** $I_D\approx\mathbf{1.09\ mA}$.
:::

::: ex Example 2.4: Thermal voltage at two temperatures
**Given:** $T=27$ °C and $T=127$ °C.

**Step 1.** Convert to kelvin (add 273): $300$ K and $400$ K.
**Step 2.** $V_T=T/11600$: $300/11600=0.02586$ V and $400/11600=0.03448$ V.

**Answer:** **25.9 mV** at 27 °C, **34.5 mV** at 127 °C.

**Trap:** using 27 and 127 directly in $T/11600$ (forgetting kelvin) gives a wrong answer 10 times too small.
:::

## 2.5 Effect of temperature

{{fig p_diode_temp|As temperature rises, the forward curve moves LEFT: the cut-in voltage drops.|66}}

* **Reverse saturation current doubles for every 10 °C rise:**
$$I_{02}=I_{01}\cdot2^{(T_2-T_1)/10}$$
where $I_{01}$ is the leakage at temperature $T_1$ and $I_{02}$ at $T_2$.
* **The cut-in voltage decreases** as temperature rises. <span class="tag">extra</span> For silicon it drops roughly 2 mV per °C.
* In reverse bias the leakage current increases with temperature. Your slides also say the **breakdown voltage increases** with temperature.

::: ex Example 2.5: Leakage current versus temperature
**Given:** $I_0=2$ nA at 25 °C.

**Find:** $I_0$ at 75 °C.

**Formula:** $I_{02}=I_{01}\times2^{(T_2-T_1)/10}$.

**Step 1.** Temperature rise: $75-25=50$ °C.
**Step 2.** Number of doublings: $50/10=5$.
**Step 3.** $2^5=32$.
**Step 4.** $I_{02}=2\ \text{nA}\times32=64$ nA.

**Answer:** **64 nA**.

**A second one:** $I_0=5$ nA at 25 °C, find at 65 °C. Rise 40 °C = 4 doublings = ×16, so $5\times16=\mathbf{80\ nA}$.
:::

## 2.6 Diode resistances

{{fig p_diode_res|Static resistance is the slope of the line from the origin to Q; dynamic resistance is the slope of the tangent at Q.|60}}

A real diode is **not** a perfect switch: it never has zero resistance forward or infinite resistance in reverse.

* **Static (dc) resistance:** $R_{dc}=V_D/I_D$ at the operating point. It is **larger near the knee and below**, and smaller on the steep part. In reverse it is very large (**several megohms**).
* **Dynamic (ac) resistance:** used for small ac signals around a bias point:
$$r_{ac}=\frac{\Delta V}{\Delta I}\ (\text{as small a change as possible}),\qquad\text{from the diode equation: }r_d=\frac{\eta V_T}{I_D}$$
Typical forward value **1 to 25 Ω**.
* **Reverse resistance:** several megohms, because only leakage flows.

::: ex Example 2.6: Static and dynamic resistance
**Given:** a Ge diode ($\eta=1$) at 300 K carries $I_D=2$ mA with $V_D=0.2$ V.

**Find:** $R_{dc}$ and $r_d$.

**Step 1: static.** $R_{dc}=\dfrac{V_D}{I_D}=\dfrac{0.2}{0.002}=100\ \Omega$.
**Step 2: dynamic.** $r_d=\dfrac{\eta V_T}{I_D}=\dfrac{1\times0.02586}{0.002}=12.9\ \Omega$.

**Answer:** $R_{dc}=100\ \Omega$; $r_d=12.9\ \Omega$ (the quick rule $26\text{ mV}/2\text{ mA}=13\ \Omega$ agrees).

**What it means:** the two are different numbers because the curve is not a straight line through the origin. Use $R_{dc}$ for dc calculations and $r_d$ for small ac signals.
:::

## 2.7 Diode equivalent circuits (models)

{{fig p_diode_models|The real curve (dashed grey) replaced by straight-line approximations.|95}}

In circuit analysis we replace the curve with straight lines so the maths is easy.

| Model | What it is | Use when |
|---|---|---|
| 1. Piecewise linear | switch + battery $V_\gamma$ + resistor $R_f$ | forward resistance is given |
| 2. Simplified ($R_f=0$) | switch + battery $V_\gamma$ | most textbook problems |
| 3. Ideal diode | switch only ($V_\gamma=0$) | high voltages, quick estimates |

{{fig c_diode_m1|Model 1: cut-in battery $V_\gamma$ and forward resistance $R_f$ (valid when the diode is forward biased and above cut-in).|80}}

::: trap Method for every diode circuit
1. **Assume the diode is ON** and replace it by its model.
2. Solve the circuit.
3. If the current comes out **positive**, the assumption was right. If it comes out **negative** (or the diode voltage is below $V_\gamma$), the diode is **OFF**: replace it by an open circuit and solve again.
:::

::: ex Example 2.7: Diode in series with a resistor
**Given:** Si diode ($V_\gamma=0.7$ V, $R_f=20\ \Omega$) in series with a 5 V source and $R=1\ \text{k}\Omega$.

**Find:** the current $I$.

**Formula (KVL: voltages around the loop add to zero):** $V_S-V_\gamma-IR_f-IR=0$.

**Step 1.** Rearrange: $I=\dfrac{V_S-V_\gamma}{R+R_f}$.
**Step 2.** Numbers: $I=\dfrac{5-0.7}{1000+20}=\dfrac{4.3}{1020}$.
**Step 3.** $I=4.216\times10^{-3}$ A.

**Answer:** $I=\mathbf{4.22\ mA}$.

**Check the assumption:** $I>0$, so the diode is indeed ON.

{{fig c_diode_series|The series circuit.|55}}
:::

::: ex Example 2.8: Same circuit, ideal-ish diode
**Given:** 12 V source, 470 Ω, Si diode with $R_f=0$.
**Step 1.** $V_R=12-0.7=11.3$ V across the resistor.
**Step 2.** $I=11.3/470=0.02404$ A.
**Answer:** **24.0 mA**.
:::

## 2.8 Junction capacitances

::: kid Two hidden capacitors in every diode
A capacitor is two plates with a gap. In a reverse-biased diode the two layers of ions are like plates with an empty depletion region in between: the **transition capacitance**. In a forward-biased diode, extra carriers are stored near the junction like water in a tank: the **diffusion capacitance**.
:::

* **Transition (depletion) capacitance $C_T$** exists in **reverse bias**:
$$C_T=\frac{K}{(V_B-V)^n}$$
$K$ depends on the material; $V_B$ is the barrier voltage (**0.6 V Si, 0.2 V Ge**); $V$ is the applied voltage (**negative** in reverse, so $V_B-V=V_B+|V|$); $n$ depends on the junction type. <span class="tag">extra</span> $n=\tfrac12$ for an abrupt junction, $\tfrac13$ for a graded one. More reverse voltage → wider layer → **smaller** $C_T$. This is used in the varactor (Chapter 5).
* **Diffusion (storage) capacitance $C_D$** exists in **forward bias**, is much larger than $C_T$ and is proportional to the forward current:
$$C_D=\frac{\tau I}{\eta V_T}$$
$\tau$ is the mean carrier lifetime. If you suddenly reverse-bias a forward-biased diode, the stored charge must be removed first; this limits switching speed.

::: ex Example 2.9: Diffusion capacitance
**Given:** $\tau=100$ ns $=10^{-7}$ s, $I=10$ mA, $\eta=1$, $V_T=0.02586$ V.

**Formula:** $C_D=\tau I/(\eta V_T)$.

**Step 1.** $\tau I=10^{-7}\times10^{-2}=10^{-9}$.
**Step 2.** $\eta V_T=0.02586$.
**Step 3.** $C_D=10^{-9}/0.02586=3.87\times10^{-8}$ F.

**Answer:** $C_D=\mathbf{38.7\ nF}$. Doubling $I$ doubles $C_D$.
:::

::: ex Example 2.10: Transition capacitance versus reverse voltage
**Given:** $n=\tfrac12$, $V_B=0.6$ V, and $C_T=100$ pF at $V=-2$ V.

**Find:** $C_T$ at $V=-8$ V.

**Step 1: find $K$.** $C_T=K/(V_B-V)^{1/2}$ with $V_B-V=0.6+2=2.6$. So $100=K/\sqrt{2.6}$ and $K=100\times1.612=161.2$ pF·V$^{1/2}$.
**Step 2: new denominator.** At $-8$ V: $V_B-V=0.6+8=8.6$, $\sqrt{8.6}=2.933$.
**Step 3.** $C_T=161.2/2.933=54.97$ pF.

**Answer:** about **55 pF**. Quadrupling the reverse voltage (2 → 8 V) cut the capacitance almost in half.
:::

## 2.9 Ratings: power, current, PIV

* **Power dissipation:** forward $P_D=V_FI_F$; reverse $P_D=V_RI_R$. The largest power the diode can dissipate without damage is its **power rating**; above it the diode is destroyed. Example: **1N914 = 250 mW**.
* **Current rating:** the maximum current the diode can carry. Some data sheets give this instead of power. Example: **1N4003 = 1 A** (the slide lists its power rating as 1 W).
* **PIV (peak inverse voltage):** the largest reverse voltage that can be applied before breakdown.
* **Two categories:** **small-signal diodes** (power below 0.5 W, e.g. 1N914) and **power / rectifier diodes** (above 0.5 W, e.g. 1N4003).

::: ex Example 2.11: Is the diode safe?
**Given:** a 1N914 (rated 250 mW) carries 10 mA with 0.75 V across it.
**Step 1.** $P=V_FI_F=0.75\times0.010=7.5$ mW.
**Step 2.** Compare: $7.5\ \text{mW}\ll250\ \text{mW}$.
**Answer:** safe; it is using 3 % of its rating.
:::

## 2.10 Breakdown

If the reverse voltage becomes too large, the current suddenly shoots up. The voltage at which this happens is the **breakdown voltage** ($V_{BR}$ or $V_Z$).

| | **Avalanche** breakdown | **Zener** breakdown |
|---|---|---|
| Doping | **lightly** doped | **heavily** doped |
| Depletion layer | wide | very thin |
| Mechanism | carriers speed up in the field, hit atoms, knock out more carriers, which knock out still more (chain reaction) | the field across the thin layer is so strong it directly **rips electrons out of their bonds** |
| Voltage | higher: **above about 6 V** | lower: **below about 6 V** |

At low reverse voltages the Zener mechanism is more important; at higher voltages, avalanche dominates.

::: kid Two ways to break a wall
*Avalanche* is a snowball rolling downhill, gathering more snow as it goes. *Zener* is a very thin wall that simply tears when pulled hard. Thin wall → Zener. Long slope → avalanche.
:::

## 2.11 Applications listed in your slides

Rectifiers and power diodes in dc power supplies · signal diodes in communication circuits · Zener diodes for voltage stabilisation · varactor diodes for radio and TV receivers · switches in logic circuits of computers.

## 2.12 Practice

::: try Questions for Chapter 2
1. Find $V_T$ at 27 °C and at 127 °C.
2. A Ge diode ($\eta=1$) has $I_0=2\ \mu$A at 300 K. Find the forward current at $V_D=0.25$ V.
3. $I_0=5$ nA at 25 °C. What is $I_0$ at 65 °C?
4. A Si diode ($V_\gamma=0.7$ V, $R_f=0$) is in series with 12 V and 470 Ω. Find the current.
5. State the difference between static and dynamic resistance. Which is used for small ac signals?
6. Why does avalanche breakdown occur in lightly doped diodes and Zener breakdown in heavily doped ones?
7. A diode has $C_D$ proportional to what? What happens to $C_T$ when the reverse voltage is increased?
8. A Si diode ($\eta=2$) carries 5 mA at 300 K. Find its dynamic resistance.
:::

::: soln Answers and full solutions
<details markdown="1"><summary>Solution 1</summary>

Worked in Example 2.4: **25.9 mV** at 27 °C (300 K) and **34.5 mV** at 127 °C (400 K).
</details>

<details markdown="1"><summary>Solution 2</summary>

**Given:** $\eta=1$, $I_0=2\ \mu\text{A}$, $V_D=0.25$ V, $T=300$ K.
**Formula:** $I_D=I_0(e^{V_D/\eta V_T}-1)$.
**Step 1.** $V_T=300/11600=0.02586$ V.
**Step 2.** Exponent: $0.25/0.02586=9.667$.
**Step 3.** $e^{9.667}=15\,800$ ($e^{9}=8103$, $e^{0.667}=1.948$, product $15\,785$).
**Step 4.** $I_D=2\times10^{-6}\times(15\,785-1)=2\times10^{-6}\times15\,784=0.03157$ A.

**Answer:** $I_D\approx\mathbf{31.6\ mA}$.
</details>

<details markdown="1"><summary>Solution 3</summary>

**Step 1.** Rise $=65-25=40$ °C.
**Step 2.** Doublings $=40/10=4$, so factor $2^4=16$.
**Step 3.** $I_{02}=5\times16=80$ nA.

**Answer:** **80 nA**.
</details>

<details markdown="1"><summary>Solution 4</summary>

**Step 1.** Silicon and $R_f=0$: the diode is a 0.7 V battery in the forward direction.
**Step 2.** KVL: $12-0.7-I\times470=0$.
**Step 3.** $I=\dfrac{11.3}{470}=0.02404$ A.

**Answer:** **24.0 mA**. Positive, so the diode is indeed ON.
</details>

<details markdown="1"><summary>Solution 5</summary>

**Static (dc) resistance:** $R_{dc}=V_D/I_D$ at one point (slope of the line from the origin to that point).
**Dynamic (ac) resistance:** $r_{ac}=\Delta V/\Delta I$ (slope of the tangent at the point), equal to $\eta V_T/I_D$.
**Answer:** dynamic resistance is used for small ac signals because the signal moves the operating point only a little around Q.
</details>

<details markdown="1"><summary>Solution 6</summary>

**Lightly doped:** the depletion layer is wide, so carriers travel a long distance in the field and gain enough energy to knock loose new carriers from atoms (chain reaction = avalanche).
**Heavily doped:** the layer is very thin, so even a modest reverse voltage produces an enormous field across it, which pulls electrons directly out of their bonds (Zener effect).
</details>

<details markdown="1"><summary>Solution 7</summary>

**Step 1.** From $C_D=\tau I/(\eta V_T)$, $C_D$ is proportional to the **forward current** $I$.
**Step 2.** From $C_T=K/(V_B+|V|)^n$, raising the reverse voltage makes the denominator bigger, so $C_T$ **decreases** (the depletion layer widens).
</details>

<details markdown="1"><summary>Solution 8</summary>

**Formula:** $r_d=\dfrac{\eta V_T}{I_D}$.
**Step 1.** $\eta V_T=2\times0.02586=0.05172$ V.
**Step 2.** $r_d=\dfrac{0.05172}{0.005}=10.3\ \Omega$.

**Answer:** **10.3 Ω**.
</details>
:::
