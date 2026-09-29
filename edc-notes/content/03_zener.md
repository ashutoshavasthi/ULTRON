# Chapter 3: Zener diode

*Class notes p. 1 · slides: Unit-I First part, Topic 7*

::: words
| Word / symbol | Plain meaning |
|---|---|
| Zener diode | a diode built to work in reverse breakdown, holding a steady voltage |
| $V_Z$ | Zener voltage: the (nearly constant) voltage across it in breakdown |
| $I_Z$ | current through the Zener |
| $I_{ZK}$ (or $I_{ZT}$-knee) | **minimum** Zener current needed to stay in regulation (the "knee") |
| $I_{ZM}$ | **maximum** Zener current before it overheats |
| $P_{ZM}$ | maximum power the Zener can dissipate |
| $r_Z$ | Zener resistance $=\Delta V_Z/\Delta I_Z$: how much $V_Z$ creeps up as current rises |
| Regulator | circuit that keeps output voltage steady when input or load changes |
| $V_{in}$ | the unregulated input voltage |
| $R_S$ | series resistor that drops the extra voltage and limits current |
| $R_L$, $I_L$ | load resistor and load current |
| $I_S$ | the total current through $R_S$ ($=I_Z+I_L$) |
| Regulating region | the steep part of the reverse curve where the voltage stays constant |
:::

::: kid The pressure-relief valve
Your pressure cooker has a **safety valve**: when the pressure gets too high the valve opens and lets steam out, so the pressure never goes above a fixed limit. A **Zener diode** is that valve for voltage. Connect it backwards across something. As long as the voltage stays below the Zener voltage nothing happens. Try to push the voltage higher and the Zener suddenly conducts a lot of current, **holding the voltage at (nearly) the same value**. That makes it a *voltage regulator* or *voltage reference*.
:::

## 3.1 What it is

* Also called **breakdown diode**, **voltage-reference diode**, **voltage-regulator diode**.
* A PN diode designed to work **in the reverse breakdown region**.
* **Heavily doped**, so the depletion region is very thin. The breakdown voltage $V_Z$ is set during manufacture by controlling the doping.
* Symbol: a diode with a bent bar on the cathode.

{{fig c_sym_zener|Zener diode symbol.|35}}

::: class Class notes (p. 1)
"Zener diode: highly doped; for voltage regulation." The sketch shows the symbol, the reverse breakdown curve with $V_Z$ marked, the forward-bias region on the right, and the **equivalent circuit: a battery $V_Z$ in series with a small resistance $r_Z$**.
:::

## 3.2 The V–I characteristic

{{fig p_zener_iv|Zener characteristic. The useful region is the steep reverse breakdown line, between $I_{ZK}$ and $I_{ZM}$.|72}}

* **Forward:** like an ordinary diode.
* **Reverse:** the current is negligible until the breakdown point ($V_Z$), then rises very steeply. That steep part is the **regulating region**.
* It is not perfectly vertical because of the **zener resistance** $r_Z=\Delta V_Z/\Delta I_Z$.
* **$I_{ZK}$ (knee / break-over current):** the minimum current that must be kept flowing; below it regulation is lost.
* **$I_{ZM}$:** the maximum current; above it the diode is damaged by heat.

## 3.3 Two mechanisms

* **Zener effect:** a strong electric field across a very thin junction directly breaks covalent bonds and frees electrons. Dominates for breakdown **below about 6 V**.
* **Avalanche effect:** accelerated carriers ionise atoms by collision, creating more carriers in a chain. Dominates **above about 6 V**.

Both give the same kind of curve and the device is still called a "Zener".

## 3.4 Specifications and equivalent circuit

A Zener is specified by four numbers: **$V_Z$**, **$P_{ZM}$**, **$I_{ZK}$**, **$r_Z$**.

$$P_{DZ}=V_ZI_Z,\qquad I_{ZM}=\frac{P_{ZM}}{V_Z},\qquad r_Z=\frac{\Delta V_Z}{\Delta I_Z},\qquad V_Z'=V_Z+I_Zr_Z$$

An ideal Zener has $r_Z=0$; real ones have a few ohms to several hundred ohms. $V_Z'$ is the actual terminal voltage: it rises slightly with current (the tilt of the curve).

## 3.5 The Zener voltage regulator

{{fig c_zener_reg_load|Shunt regulator: series resistor $R_S$, Zener across the load $R_L$.|72}}

**How it works:**
1. $V_{in}$ is the unregulated supply. $R_S$ **drops the extra voltage** and limits the current.
2. The Zener holds $V_{out}\approx V_Z$ across the load.
3. If $V_{in}$ rises, the extra current flows through the Zener (not the load) and the extra voltage is dropped across $R_S$.
4. If the load draws more current, the Zener current falls by the same amount, and $V_{out}$ stays put.

$$I_S=\frac{V_{in}-V_Z}{R_S},\qquad I_L=\frac{V_Z}{R_L},\qquad I_Z=I_S-I_L$$

**Design rules** (favourite exam question):
* At the **lowest** input voltage and **heaviest** load (largest $I_L$), $I_Z$ must still be at least $I_{ZK}$.
* At the **highest** input voltage and **lightest** load (no load, $I_L=0$), all of $I_S$ goes through the Zener, so $V_ZI_S$ must not exceed $P_{ZM}$.
* Series resistor: $R_S=\dfrac{V_{in,min}-V_Z}{I_{Z,min}+I_{L,max}}$.

::: ex Example 3.1: Choosing $R_S$
**Given:** input 12 V, Zener 5.1 V, load $R_L=1\ \text{k}\Omega$, we want $I_Z=10$ mA.

**Find:** $R_S$, and the Zener power.

**Step 1: load current.** $I_L=V_Z/R_L=5.1/1000=5.1$ mA.
**Step 2: total current through $R_S$.** $I_S=I_Z+I_L=10+5.1=15.1$ mA.
**Step 3: voltage across $R_S$.** $V_{in}-V_Z=12-5.1=6.9$ V.
**Step 4: value of $R_S$.** $R_S=\dfrac{6.9}{0.0151}=457\ \Omega$. The nearest preferred value is 470 Ω.
**Step 5: check with 470 Ω.** $I_S=6.9/470=14.68$ mA, so $I_Z=14.68-5.1=9.58$ mA (fine).
**Step 6: Zener power.** $P=V_ZI_Z=5.1\times9.58\ \text{mA}=48.9$ mW, well inside a 500 mW rating.

**Answer:** $R_S=457\ \Omega$ (use **470 Ω**); Zener dissipates about **49 mW**.
:::

::: ex Example 3.2: The input voltage varies
**Given:** 9.1 V Zener, $R_S=330\ \Omega$, $R_L=1\ \text{k}\Omega$, $V_{in}$ varies from 15 V to 20 V, $P_{ZM}=500$ mW.

**Find:** $I_Z$ at both extremes, the worst-case power, and how much the output really moves if $r_Z=8\ \Omega$.

**Step 1: load current (same in both cases).** $I_L=9.1/1000=9.1$ mA.
**Step 2: at $V_{in}=15$ V.** $I_S=(15-9.1)/330=5.9/330=17.88$ mA. $I_Z=17.88-9.1=8.78$ mA.
**Step 3: at $V_{in}=20$ V.** $I_S=(20-9.1)/330=10.9/330=33.03$ mA. $I_Z=33.03-9.1=23.93$ mA.
**Step 4: worst-case power.** $P=9.1\times23.93=217.8$ mW $<500$ mW ✓. (Also $I_{ZM}=500/9.1=54.9$ mA $>23.93$ mA ✓.)
**Step 5: how much does $V_{out}$ move?** $\Delta I_Z=23.93-8.78=15.15$ mA. $\Delta V_{out}=\Delta I_Z\times r_Z=0.01515\times8=0.121$ V.

**Answer:** $I_Z$ swings 8.8 → 23.9 mA (safe). While the input moved **5 V**, the output moved only **0.12 V** (about 1.3 %). That is regulation.
:::

::: trap Common mistakes
* Putting the Zener the wrong way round. It must be **reverse biased**; forward it is just a 0.7 V diode.
* Forgetting $R_S$. Without it the current is unlimited and the Zener burns out.
* Forgetting that with the load **removed** the whole $I_S$ flows through the Zener: check $V_ZI_S\le P_{ZM}$.
:::

## 3.6 Applications (from the slides)

1. Voltage regulator. 2. Fixed reference voltage in transistor biasing circuits. 3. Peak clippers in wave-shaping circuits. 4. Meter protection against accidental over-voltage.

## 3.7 Practice

::: try Questions for Chapter 3
1. Why must a Zener be heavily doped?
2. A Zener has $V_Z=6.8$ V and $P_{ZM}=1$ W. Find $I_{ZM}$.
3. A 10 V Zener has $r_Z=8\ \Omega$ and carries 20 mA. Using $V_Z'=V_Z+I_Zr_Z$, what is the terminal voltage?
4. 12 V supply, 5.6 V Zener, $R_S=220\ \Omega$, load 1 kΩ. Find $I_S$, $I_L$ and $I_Z$.
5. Explain in your own words why the regulator keeps $V_{out}$ constant when $V_{in}$ rises.
6. Design $R_S$: input 16–20 V, $V_Z=6.2$ V, load current 0–20 mA, minimum Zener current 5 mA. Which power rating is needed?
:::

::: soln Answers and full solutions
<details markdown="1"><summary>Solution 1</summary>

Heavy doping makes the depletion region very thin (about nanometres). A thin region means a moderate reverse voltage already produces a huge electric field ($E=V/d$), which frees electrons and gives sharp breakdown at a low, well-defined voltage.
</details>

<details markdown="1"><summary>Solution 2</summary>

**Formula:** $I_{ZM}=P_{ZM}/V_Z$.
**Step 1.** $I_{ZM}=\dfrac{1\ \text{W}}{6.8\ \text{V}}=0.1471$ A.

**Answer:** **147 mA**.
</details>

<details markdown="1"><summary>Solution 3</summary>

**Formula:** $V_Z'=V_Z+I_Zr_Z$.
**Step 1.** $I_Zr_Z=0.020\ \text{A}\times8\ \Omega=0.16$ V.
**Step 2.** $V_Z'=10+0.16=10.16$ V.

**Answer:** **10.16 V**.
</details>

<details markdown="1"><summary>Solution 4</summary>

**Step 1: $I_S$.** Voltage across $R_S$ is $12-5.6=6.4$ V, so $I_S=6.4/220=0.02909$ A $=29.1$ mA.
**Step 2: $I_L$.** $I_L=V_Z/R_L=5.6/1000=5.6$ mA.
**Step 3: $I_Z$.** $I_Z=I_S-I_L=29.1-5.6=23.5$ mA.

**Answer:** $I_S=29.1$ mA, $I_L=5.6$ mA, $I_Z=23.5$ mA.
</details>

<details markdown="1"><summary>Solution 5</summary>

**Step 1.** The Zener's voltage is almost fixed in the steep region, so $V_{out}\approx V_Z$.
**Step 2.** When $V_{in}$ rises, the current through $R_S$ increases: $I_S=(V_{in}-V_Z)/R_S$.
**Step 3.** The load current is fixed by $V_Z/R_L$, so the extra current has nowhere to go but through the Zener.
**Step 4.** The extra voltage appears across $R_S$, not the load.

**Answer:** the Zener absorbs the extra current and $R_S$ absorbs the extra voltage, so the load sees a steady $V_Z$.
</details>

<details markdown="1"><summary>Solution 6</summary>

**Formula:** $R_S=\dfrac{V_{in,min}-V_Z}{I_{Z,min}+I_{L,max}}$.
**Step 1.** $V_{in,min}-V_Z=16-6.2=9.8$ V.
**Step 2.** $I_{Z,min}+I_{L,max}=5+20=25$ mA.
**Step 3.** $R_S=9.8/0.025=392\ \Omega\to$ use **390 Ω**.
**Step 4: worst-case power.** Highest input (20 V), no load: $I_S=(20-6.2)/390=35.4$ mA, all through the Zener. $P=6.2\times35.4\ \text{mA}=219$ mW.
**Step 5: check minimum.** At 16 V with 20 mA load: $I_S=9.8/390=25.1$ mA, so $I_Z=5.1$ mA $\ge5$ mA ✓.

**Answer:** $R_S=390\ \Omega$; use a **500 mW** Zener (needs at least 219 mW).
</details>
:::
