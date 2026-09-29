# Chapter 4: Tunnel diode

*Class notes pp. 2–3 · slides: Unit-I First part Topic 8, Different Diodes*

::: words
| Word / symbol | Plain meaning |
|---|---|
| Tunnel (Esaki) diode | a very heavily doped diode whose current falls as voltage rises over a range |
| Tunnelling | electrons passing *through* a very thin barrier instead of climbing over it |
| Peak point $(V_P,I_P)$ | the top of the first hump of the curve |
| Valley point $(V_V,I_V)$ | the bottom of the dip after the hump |
| Negative resistance | region where current **decreases** when voltage **increases**: $\Delta V/\Delta I<0$ |
| $R_n$ | the (negative) resistance value in that region |
| $I_P/I_V$ | peak-to-valley current ratio; bigger is better for switching |
| Back diode | a tunnel diode used in reverse |
| Oscillator | circuit that generates a repeating signal by itself |
| GaAs | gallium arsenide, a compound semiconductor |
| nm, GHz, ps | nanometre ($10^{-9}$ m); gigahertz ($10^{9}$ Hz); picosecond ($10^{-12}$ s) |
:::

::: kid The ghost that walks through walls
Roll a ball at a hill. Normally it needs enough energy to go **over** the hill. But in the tiny quantum world, a particle sometimes just appears on the other side of a very thin wall **without going over it**. That is **tunnelling**. In a tunnel diode the wall (the depletion region) is made so thin (about 10 nm) that electrons tunnel through even at tiny voltages, faster than any normal diode can react. Weirdly, if you push the voltage further, the current goes **down**. That backwards behaviour is **negative resistance**, and it makes the tunnel diode great for oscillators.
:::

## 4.1 Construction and idea

* Invented by **Leo Esaki in 1958**, so also called the **Esaki diode**.
* A **very heavily doped** PN junction: doping about **1000 times more** (or more) than an ordinary diode, and more than a Zener.
* Depletion width is only about **10 nm** ($0.00001$ mm).
* Made mostly of **germanium**; also gallium arsenide (GaAs) and gallium antimonide (silicon is possible).
* Used in oscillators, amplifiers, frequency converters, very fast switches.
* Handle with care: low power, easily damaged by heat or static electricity.

{{fig c_sym_tunnel|Tunnel-diode symbol (two versions are used).|38}}

**Effects of the heavy doping (Different-Diodes slides):**
* the depletion layer shrinks to about 0.00001 mm;
* a **negative-resistance section** appears in the characteristic;
* reverse breakdown voltage falls almost to zero, so the diode conducts for all reverse voltages;
* the intrinsic barrier (0.3 V for Ge) is effectively lowered, which helps tunnelling.

**Tunnelling** means electrons move from the valence band on one side to the conduction band on the other **without needing a forward voltage to give them the energy to climb the barrier**. In an ordinary diode carriers must *gain energy* to cross; in a tunnel diode they *penetrate* the barrier.

## 4.2 The V–I characteristic

{{fig p_tunnel_iv|Tunnel-diode characteristic: peak point A, valley point B, negative-resistance region between them.|72}}

1. **Forward voltage from zero:** the current rises rapidly to a **peak point** $(V_P,I_P)$, because electron states on one side line up with empty states on the other and many electrons tunnel.
2. **Beyond the peak:** current **decreases** as voltage rises, down to the **valley point** $(V_V,I_V)$. The states become **misaligned**, so tunnelling falls. This region (curve A→B) is the **negative-resistance region**.
3. **Beyond the valley:** current rises again like a normal diode (B→C). Electrons no longer tunnel; ordinary diffusion current takes over.
4. **Reverse bias:** current rises about **linearly** with reverse voltage (used as a **back diode**: electrons from the P valence band tunnel to empty N conduction-band states).
5. The shaded region in the class sketch is where **tunnelling current** flows.

**Two observations from the slide:**
* Between the peak and valley one current value corresponds to **three different voltages**. This gives **bistable** (two-state) action, useful in pulse and digital circuits.
* The negative-resistance region is used in **high-frequency oscillators**.

## 4.3 Parameters

1. **Negative resistance:** $R_n=-\dfrac{\Delta V_F}{\Delta I_F}$ in region A→B. Typically **10 to 200 Ω**, depending on the material.
2. **Peak-to-valley current ratio** $I_P/I_V$: important for fast switching. Typically **about 6 for germanium** and **about 10 for gallium arsenide**.

::: ex Example 4.1: Negative resistance and peak-to-valley ratio
**Given:** peak point $(V_P,I_P)=(0.1\ \text{V},5\ \text{mA})$; valley point $(V_V,I_V)=(0.35\ \text{V},0.5\ \text{mA})$.

**Find:** $R_n$ and $I_P/I_V$.

**Step 1: change in voltage.** $\Delta V=0.35-0.10=+0.25$ V.
**Step 2: change in current.** $\Delta I=0.5-5=-4.5$ mA (negative: the current fell).
**Step 3: ratio.** $\dfrac{\Delta V}{\Delta I}=\dfrac{0.25}{-4.5\times10^{-3}}=-55.6\ \Omega$.
**Step 4: peak/valley.** $I_P/I_V=5/0.5=10$.

**Answer:** $R_n=\mathbf{-55.6\ \Omega}$ (inside the typical 10–200 Ω range); $I_P/I_V=\mathbf{10}$ (typical of GaAs).

**What it means:** the minus sign is not a mistake; it says "more voltage gives less current".
:::

## 4.4 Equivalent circuit

{{fig c_tunnel_eq|Equivalent circuit of a tunnel diode (values from the slides).|80}}

* **Series resistance $R_S$:** leads, contacts and semiconductor; **1–5 Ω**.
* **Series inductance $L_S$:** from lead length; **0.1–4 nH**.
* **Junction capacitance $C$:** diffusion capacitance plus applied voltage; **0.35–100 pF**.
* **Negative resistance $-R_n$** in parallel with $C$.

## 4.5 Applications, advantages, disadvantages

* **Applications:** ultra-high-speed switching (nanoseconds to picoseconds; tunnelling is essentially at the speed of light); logic memory storage; microwave oscillator at about **10 GHz**; relaxation oscillators (negative resistance); satellite communication equipment.
* **Advantages:** very high speed; can oscillate at microwave frequencies.
* **Disadvantages:** poor reproducibility (hard to manufacture identically); low peak-to-valley ratio; low power handling.

## 4.6 Practice

::: try Questions for Chapter 4
1. Why is a tunnel diode more heavily doped than a Zener?
2. Sketch the tunnel-diode V–I curve and label the peak, valley and negative-resistance region.
3. A tunnel diode has peak $(0.08\ \text{V},\ 4.5\ \text{mA})$ and valley $(0.30\ \text{V},\ 0.6\ \text{mA})$. Find the average negative resistance and $I_P/I_V$.
4. Give two applications that use the negative resistance.
5. Why is a tunnel diode very fast?
:::

::: soln Answers and full solutions
<details markdown="1"><summary>Solution 1</summary>

Tunnelling needs a barrier only about 10 nm thick. The heavier the doping, the thinner the depletion region, so the tunnel diode is doped far more than a Zener (whose thin region is only thin enough for field breakdown).
</details>

<details markdown="1"><summary>Solution 2</summary>

Draw axes $V_F$ (horizontal) and $I_F$ (vertical). The curve rises to a peak A $(V_P,I_P)$, falls to a valley B $(V_V,I_V)$, then rises again (C). The part A→B is the negative-resistance region. See Figure in §4.2.
</details>

<details markdown="1"><summary>Solution 3</summary>

**Step 1.** $\Delta V=0.30-0.08=0.22$ V.
**Step 2.** $\Delta I=0.6-4.5=-3.9$ mA.
**Step 3.** $R_n=\dfrac{0.22}{-3.9\times10^{-3}}=-56.4\ \Omega$.
**Step 4.** $I_P/I_V=4.5/0.6=7.5$.

**Answer:** $R_n\approx\mathbf{-56\ \Omega}$; $I_P/I_V=\mathbf{7.5}$.
</details>

<details markdown="1"><summary>Solution 4</summary>

Microwave/high-frequency oscillators, and relaxation oscillators (also amplifiers and bistable pulse circuits).
</details>

<details markdown="1"><summary>Solution 5</summary>

Conduction is by tunnelling, which does not need carriers to diffuse or to be stored and removed, so it is limited only by the tiny capacitance and inductance of the device (switching times of ns to ps).
</details>
:::

# Chapter 5: Varactor diode {.chap}

*Class notes p. 3 · slides: Different Diodes*

::: words
| Word / symbol | Plain meaning |
|---|---|
| Varactor / varicap | a diode used as a voltage-controlled capacitor |
| $C$ | capacitance |
| $C=\varepsilon A/d$ | capacitance = (permittivity × plate area) ÷ plate separation |
| $C_T$ | transition (depletion-layer) capacitance |
| $V_R$ | reverse voltage |
| Tuning | changing a radio circuit's frequency to select a station |
| LC tank | an inductor $L$ and capacitor $C$ that resonate at $f=1/(2\pi\sqrt{LC})$ |
| AFC | automatic frequency control |
| LO | local oscillator (a radio's own tuning oscillator) |
:::

::: kid A capacitor you can tune with a knob
A capacitor stores charge on two plates with a gap between them. **Far apart = small capacitance; close together = big capacitance.** In a reverse-biased diode the plates are the P and N regions and the gap is the depletion region. Turn up the reverse voltage and the gap grows, so the capacitance falls. So the voltage acts as a **tuning knob for capacitance**, exactly what a radio needs to change station.
:::

## 5.1 Definition and names

A **varactor** diode is a PN diode designed so that its **junction capacitance is controlled by the reverse-bias voltage**. It always works in **reverse bias**. Other names: **varicap**, **voltcap**, **tuning diode**, **variable-capacitance diode**, **voltage-variable capacitor**, **variable-reactance diode**.

{{fig c_sym_varactor|Varactor symbol (diode with a capacitor).|38}}

## 5.2 Operation

{{fig p_varactor|Capacitance falls as reverse voltage rises because the depletion layer (the "gap between the plates") gets wider.|92}}

$$C=\frac{\varepsilon A}{d}$$

* P and N regions = **plates**; depletion region = **dielectric (insulator)**; its width = **plate separation $d$**.
* More reverse voltage → depletion region widens → $d$ increases → **$C$ falls**. At small reverse voltage the capacitance is high.
* Relation from Chapter 2: $C_T=K/(V_B+V_R)^n$.
* Made with an **abrupt doping profile** (class notes). Gallium arsenide varactors reach very high frequency (up to almost 1000 GHz according to the slide).
* Equivalent circuit: a variable capacitor $C_T$ in series with a small resistance $R_S$.

## 5.3 Applications

1. **Electronic tuning** in radio, TV and other receivers (variable resonant LC circuits).
2. **AFC:** sets the local-oscillator frequency.
3. **Frequency modulator** in radio/TV; frequency multiplier in microwave-receiver oscillators; RF phase shifter; variable reactor in microwave circuits.

::: ex Example 5.1: Tuning range of a radio
**Given:** an LC circuit with $L=100\ \mu\text{H}=10^{-4}$ H and a varactor whose capacitance changes from 10 pF to 40 pF as $V_R$ is varied.

**Find:** the range of resonant frequency.

**Formula:** $f=\dfrac{1}{2\pi\sqrt{LC}}$.

**Step 1: with $C=40$ pF.** $LC=10^{-4}\times40\times10^{-12}=4\times10^{-15}$. $\sqrt{LC}=6.32\times10^{-8}$. $2\pi\sqrt{LC}=3.97\times10^{-7}$. $f=1/(3.97\times10^{-7})=2.52\times10^{6}$ Hz.
**Step 2: with $C=10$ pF.** $LC=10^{-15}$, $\sqrt{LC}=3.16\times10^{-8}$, $2\pi\sqrt{LC}=1.987\times10^{-7}$, $f=5.03\times10^{6}$ Hz.

**Answer:** the radio tunes from **2.52 MHz to 5.03 MHz**.

**What it means:** a 4× change in capacitance gives only a 2× change in frequency, because $f\propto1/\sqrt{C}$.
:::

## 5.4 Practice

::: try Questions for Chapter 5
1. What happens to a varactor's capacitance as the reverse voltage increases? Why?
2. Which bias does it use: forward or reverse?
3. Name two applications.
4. An LC circuit has $L=50\ \mu$H. What capacitance is needed to resonate at 1 MHz?
:::

::: soln Answers and full solutions
<details markdown="1"><summary>Solution 1</summary>

The capacitance **decreases**. A higher reverse voltage widens the depletion layer (the dielectric), which increases the effective plate separation $d$, and $C=\varepsilon A/d$.
</details>

<details markdown="1"><summary>Solution 2</summary>

Reverse bias only.
</details>

<details markdown="1"><summary>Solution 3</summary>

Electronic tuning of radio/TV receivers; automatic frequency control; frequency modulation; frequency multiplication.
</details>

<details markdown="1"><summary>Solution 4</summary>

**Formula:** $f=\dfrac1{2\pi\sqrt{LC}}$, so $C=\dfrac{1}{(2\pi f)^2L}$.
**Step 1.** $2\pi f=2\pi\times10^6=6.283\times10^6$.
**Step 2.** $(2\pi f)^2=3.948\times10^{13}$.
**Step 3.** $(2\pi f)^2L=3.948\times10^{13}\times50\times10^{-6}=1.974\times10^{9}$.
**Step 4.** $C=1/1.974\times10^9=5.07\times10^{-10}$ F.

**Answer:** **507 pF**.
</details>
:::
