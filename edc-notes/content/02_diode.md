# Chapter 2: The PN junction diode

*Class notes p. 1 · slides: p-n Junction Diode, Unit-I First part, Topics 2–6*

::: kid A diode is a one-way street for electricity
Electric current is like water in a pipe. A **diode** is a pipe with a **flap valve**: water goes through one way easily and the flap shuts the other way. The two ends are called **anode** (where current *enters*) and **cathode** (where it *leaves*), and the arrow in the symbol shows the allowed direction. The valve needs a small push to open: about **0.7 volts for silicon** and **0.3 volts for germanium**. Push too hard backwards and the valve breaks (breakdown).
:::

## 2.1 What a PN diode is

A **PN junction diode** is a 2-terminal, 2-layer, single-junction device made from one crystal of silicon or germanium, one side doped **P** (acceptors) and the other **N** (donors). The junction must be made **inside one continuous crystal**; you cannot just push a P block against an N block, because the crystal structure would be broken at the boundary. Uses: switch, rectifier, regulator, clipper, clamper, voltage multiplier, detector, logic gates.

Terminals: **anode** (P side) and **cathode** (N side). Diodes are classified by forward current capability: about 100 mA (low-current), 500 mA (medium), several amperes (power diodes).

## 2.2 No bias, forward bias, reverse bias

{{fig p_pn_bias|The depletion region (hatched) at zero bias, forward bias and reverse bias.|95}}

**No bias (open circuit).**
* Electrons near the junction diffuse from N to P, holes from P to N, and recombine.
* The N side near the junction loses electrons → **positive ions**. The P side gains electrons → **negative ions**.
* This charged, carrier-free layer is the **depletion region** (also space-charge or transition region), roughly $10^{-6}$ m wide. It contains only **fixed, immobile ions**.
* The ions set up a field that stops further diffusion. The wall is the **potential barrier**: about **0.3 V (Ge)**, **0.7 V (Si)** as quoted in the slides.
* Net current with no bias = **0**. (Diffusion current is exactly cancelled by drift current.)
* Width depends on doping: **heavily doped → thin** depletion layer, **lightly doped → thick**.

**Forward bias** (battery **+ to P**, − to N).
* Pushes majority carriers toward the junction → depletion region **narrows**, barrier **falls**.
* Once the applied voltage exceeds the cut-in voltage the barrier is gone and current rises **exponentially** (milliamperes).
* Current in the N region is carried by electrons and in the P region by holes; at the junction they recombine, and the battery supplies replacements.

**Reverse bias** (battery **− to P**, + to N).
* Electrons and holes are pulled *away* from the junction → depletion region **widens**, barrier **rises**.
* Majority current drops to zero. Only **thermally generated minority carriers** cross, giving the tiny **reverse saturation current** $I_0$ (µA for Ge, nA for Si).
* $I_0$ is called *saturation* current because it does not increase significantly when you increase the reverse voltage (until breakdown).

::: trap Which terminal is which?
Forward bias = **positive to anode (P)**. Reverse bias = **positive to cathode (N)**. Examiners love to give a circuit with a battery drawn upside-down: check the polarity first, then decide ON/OFF.
:::

## 2.3 The V–I characteristic

{{fig p_diode_iv|Forward (mA scale) and reverse (µA scale) characteristics; the scales are different on purpose.|95}}

* **Forward:** almost no current until the **knee (cut-in / threshold) voltage** $V_\gamma$: **0.3 V Ge, 0.7 V Si**. Then the current rises rapidly, like an ordinary conductor.
* **Reverse:** a very small, nearly constant current until the **breakdown voltage** $V_{BR}$, then a sharp rise. Germanium leaks much more than silicon (µA vs nA).
* The V–I graph shows the **dc behaviour** of the diode.

| | Germanium | Silicon |
|---|---|---|
| Cut-in voltage | 0.3 V | 0.7 V |
| Reverse saturation current | µA | nA |
| $\eta$ in the diode equation | 1 | 2 |
| Leakage vs temperature | worse | better (Si is used far more) |

::: flag Two “barrier” numbers appear in your slides
The slides quote **0.7 V / 0.3 V** (cut-in or knee voltage seen on the V–I curve) and, in the capacitance formula, a barrier voltage $V_B$ of **0.6 V (Si) / 0.2 V (Ge)**. These are two related but different quantities (the knee is where the current becomes noticeable; the built-in/contact potential $V_0$ is the equilibrium barrier, computed in Chapter 13). For circuit problems use **0.7 V / 0.3 V** unless the question gives another value.
:::

## 2.4 The diode current equation

$$I_D=I_0\left(e^{V_D/\eta V_T}-1\right),\qquad V_T=\frac{T}{11600}$$

| Symbol | Meaning |
|---|---|
| $I_D$ | diode current |
| $I_0$ | reverse saturation current |
| $V_D$ | voltage across the diode: **positive for forward**, negative for reverse |
| $V_T$ | thermal (“volt-equivalent of temperature”) voltage, $T$ in kelvin: $\approx 26$ mV at 300 K |
| $\eta$ | 1 for Ge, 2 for Si |

With $V_T=26$ mV, $1/V_T\approx 40\ \text{V}^{-1}$, so your slides write
$$I=I_0\left(e^{40V/\eta}-1\right)\ \Rightarrow\ \text{Ge: } I_0(e^{40V}-1),\qquad \text{Si: } I_0(e^{20V}-1).$$

**Two limiting cases (they are in your class notes):**

* **Forward, $V_D\gg\eta V_T$:** the exponential is huge so the “$-1$” is negligible: $I_D\approx I_0e^{V_D/\eta V_T}$.
* **Reverse, large negative $V_D$:** $e^{-|V_D|/\eta V_T}\to0$, so $I_D\approx-I_0$. The minus sign only means the current flows backwards. This holds *until breakdown*.

::: kid Why an exponential?
Think of a hill (the barrier). Carriers get over the hill only if they have enough energy, and the number of carriers with a given energy falls off exponentially. Lowering the hill by just a little (forward voltage) suddenly lets **a lot more** carriers over. That is why the current does not rise politely: it explodes.
:::

::: ex Example 2.1 (forward, germanium)
A Ge diode has $I_0=1\ \mu\text{A}$ at 300 K. Find $I_D$ at $V_D=0.2$ V.

$V_T=300/11600=0.02586$ V. $V_D/\eta V_T=0.2/0.02586=7.734$. $e^{7.734}\approx2285$.
$$I_D=1\ \mu\text{A}\,(2285-1)\approx\mathbf{2.28\ mA}$$
:::

::: ex Example 2.2 (reverse)
Same diode at $V_D=-5$ V: $V_D/V_T\approx-193$, so $e^{-193}\approx0$ and $I_D=-I_0=\mathbf{-1\ \mu A}$. Doubling the reverse voltage changes nothing. This is “saturation”.
:::

::: ex Example 2.3 (forward, silicon, η = 2)
Si diode, $I_0=10$ nA, $V_D=0.6$ V, 300 K. $\eta V_T=0.05172$ V, $0.6/0.05172=11.60$, $e^{11.60}=1.09\times10^{5}$.
$$I_D\approx10\text{ nA}\times1.09\times10^{5}=\mathbf{1.09\ mA}$$
:::

::: ex Example 2.4 (thermal voltage)
$V_T$ at 27 °C ($T=300$ K) $=300/11600=\mathbf{25.9\ mV}$. At 127 °C ($T=400$ K) $=400/11600=\mathbf{34.5\ mV}$. Always convert °C → K by adding 273 (or 273.15).
:::

## 2.5 Effect of temperature

{{fig p_diode_temp|As the temperature rises the forward curve moves LEFT: the cut-in voltage drops.|66}}

* **Reverse saturation current doubles for every 10 °C rise:**
$$I_{02}=I_{01}\cdot2^{(T_2-T_1)/10}$$
* **Cut-in voltage decreases** as temperature rises. <span class="tag">extra</span> For silicon the drop is roughly 2 mV per °C.
* In the reverse region the leakage current rises with temperature. Your slides also note that the **breakdown voltage increases** with temperature (this is the avalanche behaviour; see Chapter 3 for the Zener case).

::: ex Example 2.5
$I_0=2$ nA at 25 °C. Find $I_0$ at 75 °C. $\Delta T=50$ °C → 5 doublings: $2\times2^5=\mathbf{64\ nA}$.

Another: $I_0=5$ nA at 25 °C → at 65 °C: $\Delta T=40$ → 4 doublings: $5\times16=\mathbf{80\ nA}$.
:::

## 2.6 Diode resistances

{{fig p_diode_res|Static resistance is the slope of the line from the origin to Q; dynamic resistance is the slope of the tangent at Q.|60}}

A diode is **not** a perfect switch: it never has zero resistance forward or infinite resistance in reverse.

* **Static (dc) resistance:** $R_{dc}=V_D/I_D$ at the operating point. It is **larger near the knee and below**, and smaller on the steep part. In reverse it is very large (**several megohms**).
* **Dynamic (ac) resistance:** used for small ac signals around a bias point. $r_{ac}=\dfrac{\Delta V}{\Delta I}$ with the change as small as possible (slope of the tangent). Typical value **1 to 25 Ω** (forward). From the diode equation, $r_d=\dfrac{\eta V_T}{I_D}$.
* **Reverse resistance:** several megohms because only leakage flows.

::: ex Example 2.6
Ge diode ($\eta=1$) carrying $I_D=2$ mA: $r_d=\eta V_T/I_D=25.86\text{ mV}/2\text{ mA}=\mathbf{12.9\ \Omega}$. (The quick rule $r_d\approx26\text{ mV}/I_D$ gives 13 Ω.) Silicon with $\eta=2$ at 5 mA: $2(25.86)/5=10.3\ \Omega$.

Static resistance of a diode that has 0.7 V across it at 10 mA: $R_{dc}=0.7/0.01=70\ \Omega$, while its dynamic resistance at the same point is only about $r_d\approx2.6\ \Omega$ ($\eta=1$). They are different numbers for different jobs.
:::

## 2.7 Diode equivalent circuits (models)

{{fig p_diode_models|The real curve (dashed grey) replaced by straight-line approximations.|95}}

In circuit analysis we replace the curve by straight segments.

| Model | Circuit | Use when |
|---|---|---|
| 1. Piecewise-linear | switch + battery $V_\gamma$ + resistor $R_f$ | you know the forward resistance |
| 2. Simplified (neglect slope, $R_f=0$) | switch + battery $V_\gamma$ | most textbook problems |
| 3. Ideal diode (neglect $V_\gamma$ too) | switch only | high voltages, quick estimates |

{{fig c_diode_m1|Model 1: cut-in battery $V_\gamma$ and forward resistance $R_f$ (valid only when the diode is forward biased and above cut-in).|80}}

::: ex Example 2.7
A Si diode ($V_\gamma=0.7$ V, $R_f=20\ \Omega$) is in series with 5 V and 1 kΩ. $I=\dfrac{5-0.7}{1000+20}=\mathbf{4.22\ mA}$.

Same circuit but 12 V, 470 Ω, $R_f=0$: $I=(12-0.7)/470=\mathbf{24.0\ mA}$.

{{fig c_diode_series|Series circuit used in the two examples.|55}}
:::

::: trap Method for diode circuits
1. Assume the diode is **ON**; replace it by its model.
2. Solve. If $I>0$, the assumption is right. If $I<0$ (or $V<V_\gamma$), the diode is **OFF**: replace it by an open circuit and re-solve.
:::

## 2.8 Junction capacitances

::: kid Two “hidden capacitors” in every diode
A capacitor is two plates with a gap. In a reverse-biased diode the two charged layers of ions are like two plates with an empty depletion region in between: that is the **transition capacitance**. In a forward-biased diode, extra carriers are stored in the crystal near the junction like water stored in a tank: that is the **diffusion capacitance**.
:::

* **Transition (depletion / space-charge) capacitance $C_T$** exists in **reverse bias**. The depletion layer is the dielectric, the P and N regions are the plates.
$$C_T=\frac{K}{(V_B-V)^n}$$
where $K$ depends on the material, $V_B$ is the barrier voltage (**0.6 V Si, 0.2 V Ge** per the slide), $V$ is the applied voltage (**negative** in reverse bias, so $V_B-V=V_B+|V|$), and $n$ depends on the junction type (<span class="tag">extra</span> $n=\tfrac12$ abrupt, $\tfrac13$ graded). More reverse voltage → wider layer → **smaller** $C_T$. This is used in the **varactor** (Chapter 5).
* **Diffusion (storage) capacitance $C_D$** exists in **forward bias**, is much larger than $C_T$, and is proportional to the forward current:
$$C_D=\frac{\tau I}{\eta V_T}$$
with $\tau$ the mean carrier lifetime. If you suddenly reverse-bias a forward-biased junction, the stored charge must be removed first: this limits the switching speed.

::: ex Example 2.8
$\tau=100$ ns, $I=10$ mA, $\eta=1$, $V_T=25.86$ mV: $C_D=\dfrac{10^{-7}\times10^{-2}}{0.02586}=\mathbf{38.7\ nF}$. Doubling $I$ doubles $C_D$.

Transition capacitance: with $n=\tfrac12$, $V_B=0.6$ V and $C_T=100$ pF at $V=-2$ V, we get $K=100\text{ pF}\sqrt{2.6}=161$ pF·V$^{1/2}$, so at $-8$ V: $C_T=161/\sqrt{8.6}=\mathbf{55\ pF}$.
:::

## 2.9 Ratings: power, current, PIV

* **Power dissipation:** forward $P_D=V_F I_F$, reverse $P_D=V_RI_R$. The largest power the diode can dissipate without damage is its **power rating**; exceed it and the diode is destroyed. Example: **1N914 = 250 mW**.
* **Current rating:** the maximum current the diode can carry. Some data sheets give this instead of power. Example: **1N4003 = 1 A** (the slide also lists its power rating as 1 W).
* **Peak inverse voltage (PIV):** the maximum reverse voltage that can be applied before entering breakdown.
* **Two categories:** **small-signal diodes** (power below 0.5 W, e.g. 1N914 at 0.25 W) and **power / rectifier diodes** (above 0.5 W, e.g. 1N4003).

## 2.10 Breakdown

If the reverse voltage is made too large the current suddenly shoots up. The voltage at which this happens is the **breakdown voltage** $V_{BR}$ (or $V_Z$).

| | **Avalanche** breakdown | **Zener** breakdown |
|---|---|---|
| Doping | **lightly** doped diode | **heavily** doped diode |
| Depletion layer | wide | very thin |
| Mechanism | minority carriers, accelerated by the field, collide with lattice atoms, knock out more carriers, which knock out more (chain reaction, “multiplication”) | the field across the thin layer is so strong that it **directly rips electrons out of the covalent bonds** |
| Voltage | higher: **above about 6 V** | lower: **below about 6 V** |

At low reverse voltages the Zener mechanism is more important; at higher voltages avalanche dominates.

::: kid Two ways to break a wall
*Avalanche* is a snowball rolling downhill, growing as it goes. *Zener* is a very thin wall that simply tears when pulled hard. Thin wall → Zener. Long slope → avalanche.
:::

## 2.11 Applications listed in your slides

Rectifiers and power diodes in dc power supplies · signal diodes in communication circuits · Zener diodes for voltage stabilisation · varactor diodes for radio and TV receivers · switches in logic circuits of computers.

## 2.12 Try it yourself

::: try Chapter 2 questions
1. Find $V_T$ at 27 °C and 127 °C.
2. A Ge diode ($\eta=1$) has $I_0=2\ \mu$A at 300 K. Find the forward current at $V_D=0.25$ V.
3. $I_0=5$ nA at 25 °C. What is $I_0$ at 65 °C?
4. A Si diode ($V_\gamma=0.7$ V, $R_f=0$) is in series with 12 V and 470 Ω. Find the current.
5. State the difference between static and dynamic resistance. Which one is used for small ac signals?
6. Why does avalanche breakdown occur in lightly doped diodes and Zener breakdown in heavily doped ones?
7. A diode has $C_D$ proportional to what? What happens to $C_T$ when the reverse voltage is increased?

<details markdown="1"><summary>Answers</summary>

1. 25.9 mV and 34.5 mV.
2. $e^{0.25/0.02586}=e^{9.667}=1.58\times10^{4}$ → $I=2\ \mu\text{A}\times(1.58\times10^4-1)\approx\mathbf{31.6\ mA}$.
3. 4 doublings: $5\times2^4=\mathbf{80\ nA}$.
4. $(12-0.7)/470=\mathbf{24.0\ mA}$.
5. Static = $V/I$ at a point (slope of line from the origin); dynamic = $\Delta V/\Delta I$ (slope of tangent), used for small ac signals ($r_d\approx\eta V_T/I_D$).
6. Light doping → wide depletion layer, so carriers travel far, gain enough energy to ionise atoms by collision (avalanche). Heavy doping → very thin layer, so even a modest voltage gives an enormous field that pulls electrons out of bonds directly (Zener).
7. $C_D$ is proportional to the forward current ($C_D=\tau I/\eta V_T$). $C_T$ **decreases** as reverse voltage increases (wider depletion layer).
</details>
:::
