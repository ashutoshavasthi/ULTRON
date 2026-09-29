# Chapter 4: Tunnel diode

*Class notes pp. 2–3 · slides: Unit-I First part Topic 8, Different Diodes*

::: kid The ghost that walks through walls
Imagine you roll a ball at a hill. Normally the ball needs enough energy to go **over** the hill. But in the tiny quantum world, a particle sometimes just appears on the other side of a very thin wall **without going over it**. This is called **tunnelling**. In a tunnel diode the wall (the depletion region) is made so thin (about 10 nm) that electrons tunnel through even at tiny voltages, and *faster than any normal diode can react*. Weirdly, if you push the voltage further the current goes **down**. That backwards behaviour is called **negative resistance**, and it is what makes the tunnel diode great for oscillators.
:::

## 4.1 Construction and idea

* Invented by **Leo Esaki in 1958**, so also called the **Esaki diode**.
* A **very heavily doped** PN junction: doping about **1000 times more** (or more) than an ordinary diode, and **more than a Zener**.
* Depletion width is only about **10 nm** ($0.00001$ mm).
* Made mostly of **germanium**, also gallium arsenide and gallium antimonide (silicon is possible).
* Used in oscillators, amplifiers, frequency converters, very fast switches.
* Handle with care: low power, easily damaged by heat or static.

{{fig c_sym_tunnel|Tunnel-diode symbol (two versions are used).|38}}

**Effects of the heavy doping (Different-Diodes slides):**
* the depletion layer shrinks to about 0.00001 mm;
* a **negative-resistance section** appears in the characteristic;
* reverse breakdown voltage is reduced almost to zero, so the diode conducts for all reverse voltages;
* the forbidden gaps are small; the intrinsic barrier (0.3 V for Ge) is effectively lowered, which helps tunnelling.

**Tunnelling:** the movement of valence electrons from the valence band of one side to the conduction band of the other, **with no applied forward voltage needed to give them the energy to climb the barrier**. In an ordinary diode carriers must *acquire energy* to cross; in a tunnel diode they *penetrate* the barrier.

## 4.2 The V–I characteristic

{{fig p_tunnel_iv|Tunnel-diode characteristic: peak point A, valley point B, negative-resistance region between them.|72}}

1. **Forward voltage from zero:** current rises rapidly to a **peak point** $(V_P,I_P)$, because electron and hole states line up and many electrons tunnel.
2. **Beyond the peak:** current **decreases** as voltage rises, reaching a minimum, the **valley point** $(V_V,I_V)$. Electron and hole states become **misaligned**, so tunnelling falls. This region (curve A→B) shows **negative resistance**.
3. **Beyond the valley:** current rises again like an ordinary diode (curve B→C). Electrons no longer tunnel; normal diffusion current takes over.
4. **Reverse bias:** current rises approximately **linearly** with reverse voltage (the diode then behaves as a **back diode**: electrons in the P valence band tunnel to empty N conduction-band states).
5. The shaded region in the class sketch is the region where **tunnelling current** flows.

**Two useful observations from the slide:**
* Between the peak and valley a single current value corresponds to **three different voltages** ($V_1$, $V_2$, $V_3$ in your sketch). This gives **bistable** action, useful in pulse and digital circuits.
* The negative-resistance region is exploited in **high-frequency oscillators**.

## 4.3 Parameters

1. **Negative resistance:** $R_n=-\dfrac{\Delta V_F}{\Delta I_F}$ in the region A→B. Its value depends on the material and is typically **10 to 200 Ω**.
2. **Peak-to-valley current ratio** $I_P/I_V$: important for fast switching. Typical values: **about 6 for germanium** and **about 10 for gallium arsenide**.

::: ex Example 4.1
Peak $(0.1\text{ V},5\text{ mA})$ and valley $(0.35\text{ V},0.5\text{ mA})$. $\Delta V=0.25$ V, $\Delta I=-4.5$ mA.
$$R_n=\frac{0.25}{-4.5\times10^{-3}}=\mathbf{-55.6\ \Omega}$$ (negative, and inside the 10–200 Ω range). $I_P/I_V=5/0.5=\mathbf{10}$, typical of GaAs.
:::

## 4.4 Equivalent circuit

{{fig c_tunnel_eq|Equivalent circuit of a tunnel diode (values from the slides).|80}}

* **Series resistance $R_S$:** leads, contacts and semiconductor. **1 – 5 Ω**.
* **Series inductance $L_S$:** lead lengths. **0.1 – 4 nH**.
* **Junction capacitance $C$:** diffusion capacitance plus applied voltage. **0.35 – 100 pF**.
* **Negative resistance $-R_n$** in parallel with $C$.

## 4.5 Applications, advantages, disadvantages

* **Applications:** ultra-high-speed switching (nanoseconds to picoseconds, tunnelling is essentially at the speed of light); logic memory storage; microwave oscillator at about **10 GHz**; relaxation oscillators (negative resistance); satellite communication equipment.
* **Advantages:** very high speed; can oscillate at microwave frequencies.
* **Disadvantages:** poor reproducibility (hard to manufacture repeatably); low peak-to-valley ratio; low power handling.

## 4.6 Try it yourself

::: try Chapter 4 questions
1. Why is a tunnel diode more heavily doped than a Zener?
2. Draw and label the tunnel-diode V–I curve: peak, valley, negative-resistance region.
3. What is the peak-to-valley ratio of a GaAs tunnel diode, roughly?
4. Give two applications that use the negative resistance.

<details markdown="1"><summary>Answers</summary>

1. To make the depletion layer only about 10 nm thick so that electrons can tunnel through it.
2. See Fig. above: rises to peak $(V_P,I_P)$, falls to valley $(V_V,I_V)$, rises again; A→B is the negative-resistance region.
3. About 10 (Ge is about 6).
4. High-frequency (microwave) oscillators, relaxation oscillators; also amplifiers and bistable/pulse circuits.
</details>
:::

# Chapter 5: Varactor diode {.chap}

*Class notes p. 3 · slides: Different Diodes*

::: kid A capacitor you can tune with a knob
A capacitor stores charge on two plates with a gap between them. **Far apart = small capacitance; close together = big capacitance.** In a reverse-biased diode the two plates are the P and N regions and the gap is the depletion region. Turn up the reverse voltage and the gap grows, so the capacitance falls. So the voltage acts as a **tuning knob for capacitance**, exactly what a radio needs to change station.
:::

## 5.1 Definition and names

A **varactor** diode is a PN diode designed so that its **junction capacitance is controlled by the reverse-bias voltage**. It always operates in **reverse bias**. Also called **varicap**, **voltcap**, **tuning diode**, **variable-capacitance diode**, **voltage-variable capacitor**, **variable-reactance diode**.

{{fig c_sym_varactor|Varactor symbol (diode with a capacitor).|38}}

## 5.2 Operation

{{fig p_varactor|Capacitance falls as reverse voltage rises because the depletion layer (the “gap between the plates”) gets wider.|92}}

$$C=\frac{\varepsilon A}{d}$$

* P and N regions = **plates**; depletion region = **dielectric (insulator)**; its width = **plate separation $d$**.
* Increase the reverse voltage → depletion region widens → $d\uparrow$ → **$C\downarrow$**. At small reverse voltage the capacitance is high.
* Relation from Chapter 2: $C_T=K/(V_B+V_R)^n$.
* Made with an **abrupt doping profile** (class notes). Gallium arsenide varactors reach very high frequency (up to almost 1000 GHz according to the slide).
* Equivalent circuit: a variable capacitor $C_T$ in series with a small resistance $R_S$.

## 5.3 Applications

1. **Electronic tuning** in radio, TV and other commercial receivers (variable resonant LC tank circuits).
2. **AFC** (Automatic Frequency Control): sets the local oscillator (LO) frequency.
3. **Frequency modulator** in radios/TV; frequency multiplier in microwave-receiver LO; RF phase shifter; variable reactor in microwave circuits.

::: ex Example 5.1 (tuning range)
An LC tank has $L=100\ \mu$H and a varactor whose capacitance varies from 10 pF to 40 pF as $V_R$ changes. Resonant frequency $f=\dfrac{1}{2\pi\sqrt{LC}}$:
* $C=40$ pF → $f=\mathbf{2.52\ MHz}$
* $C=10$ pF → $f=\mathbf{5.03\ MHz}$

Tuning ratio is $\sqrt{40/10}=2$: a 4× change in $C$ gives a 2× change in frequency.
:::

## 5.4 Try it yourself

::: try Chapter 5 questions
1. What happens to a varactor’s capacitance as the reverse voltage increases? Why?
2. Which bias does it use: forward or reverse?
3. Name two applications.

<details markdown="1"><summary>Answers</summary>

1. It decreases: the depletion layer (dielectric) widens so the effective plate separation increases.
2. Reverse bias only.
3. Electronic tuning of radio/TV receivers; AFC; frequency modulation; frequency multiplication.
</details>
:::
