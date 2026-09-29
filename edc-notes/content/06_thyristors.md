# Chapter 8: Silicon-controlled rectifier (SCR)

*Class notes pp. 4–5 · slides: SCR, TRIAC and DIAC (slides 1–13)*

::: kid A door with a lock that only a key can open once
A normal diode is a door that opens whenever you push. An **SCR** is a door with a **latch**. It stays shut even when you push forward (**forward blocking**), until you give a small **pulse on the gate**. Then it snaps open and **stays open by itself** even if you take the gate pulse away, until the current through it falls almost to zero. A tiny gate current can therefore control a huge load current, like a small key starting a large engine.
:::

## 8.1 What it is

* Introduced by **Bell Telephone Laboratories in 1956**. A power-electronics device that can **convert AC to DC and, at the same time, control the amount of power fed to the load**: it **combines the features of a rectifier and a transistor**.
* **Three terminals:** Anode (A), Cathode (K), Gate (G). **Four layers**, P-N-P-N.
* Two main uses: **switching** and **amplification** (power amplifier circuits). Class list of applications: relay control, motor control, power amplifier, switch, rectification, regulated power supplies, static switches, motor-speed control, battery chargers, heater controls.
* Made of **silicon** (much lower leakage and better temperature behaviour than germanium).

{{fig c_scr_symbol|SCR symbol.|30}}

## 8.2 Structure

{{fig p_scr_struct|Four layers and three junctions. The outer layers are the anode (P) and cathode (N); the gate is joined to the P layer next to the cathode.|72}}

The junctions are called $J_1,J_2,J_3$, numbered from the anode side ($J_1$ nearest the anode).

## 8.3 Two-transistor analogy (your class notes, p. 4)

{{fig p_scr_two_tr|The SCR as a PNP ($Tr_1$) and an NPN ($Tr_2$) transistor cross-connected.|75}}

Split the four layers into two overlapping transistors: **$Tr_1$ = $P_1N_1P_2$ (PNP)** and **$Tr_2$ = $N_1P_2N_2$ (NPN)**. The collector of each feeds the base of the other. A small gate current turns $Tr_2$ on; its collector current drives $Tr_1$’s base, which turns $Tr_1$ on harder, which feeds even more base current to $Tr_2$… a **regenerative (positive-feedback) loop** that drives both into saturation in microseconds. That is the “latching”.

<span class="tag">extra</span> In equations: with transistor current gains $\alpha_1,\alpha_2$, $I_A=\dfrac{\alpha_2I_G+I_{CBO1}+I_{CBO2}}{1-(\alpha_1+\alpha_2)}$. The SCR turns on when $\alpha_1+\alpha_2\to1$ (the denominator vanishes). Gate current raises $\alpha$s, which is why it triggers the device.

## 8.4 How it works

The load is connected in series with the anode, and the **anode is kept positive** w.r.t. the cathode. Two cases:

**Case 1: gate open.** $J_1$ and $J_3$ are forward biased but $J_2$ is **reverse biased**, so no current flows: the SCR is **cut-off** (off state).

**Case 2: gate positive w.r.t. cathode.** $J_3$ is forward biased, $J_2$ still reverse biased. Electrons from the N layer cross $J_3$; holes move the other way; the electrons that crossed $J_3$ are then attracted across $J_2$. This starts the **gate current** and $J_2$ begins to conduct. The SCR turns **on**.

## 8.5 V–I characteristic and the three states

{{fig p_scr_iv|SCR characteristic: forward blocking → (at $V_{BO}$ or a gate pulse) → forward conducting; reverse blocking on the left.|78}}

1. **Forward blocking (off state):** anode positive, gate open; the SCR blocks the forward current that an ordinary forward-biased diode would carry (only a tiny leakage flows).
2. **Forward conduction (on state):** the SCR has fired: low voltage across it, current limited by the load. It remains on until the current drops below the **holding current** $I_H$.
3. **Reverse blocking (off state):** anode negative: blocks like a reverse-biased diode. Excess reverse voltage causes reverse breakdown (avoid).

{{fig p_scr_family|Gate current lowers the forward breakover voltage: with enough $I_G$ the SCR fires at a small anode voltage.|66}}

<span class="tag">extra</span> **Latching current** $I_L$ is the minimum anode current needed to keep the SCR on right after the gate pulse is removed. **Holding current** $I_H$ is the minimum anode current needed to *stay* on; below it the SCR turns off. To turn an SCR off you must reduce the anode current below $I_H$ (or reverse the anode voltage briefly: in AC circuits this happens naturally every negative half-cycle).

## 8.6 Power control: firing angle <span class="tag">extra</span>

{{fig p_phase|Top: SCR fires at α = 60° in each positive half-cycle (half-wave control). Bottom: a TRIAC does it in both half-cycles.|85}}

Delaying the gate pulse (larger firing angle $\alpha$) reduces the average power to the load. For a half-wave SCR circuit with a resistive load:
$$V_{dc}=\frac{V_m}{2\pi}(1+\cos\alpha)$$

::: ex Example 8.1
230 V rms supply ($V_m=325$ V):
* $\alpha=0^\circ$: $V_{dc}=\dfrac{325}{2\pi}\times2=\mathbf{103.5\ V}$ (same as an uncontrolled half-wave rectifier, $V_m/\pi$)
* $\alpha=60^\circ$: $\dfrac{325}{2\pi}\times1.5=\mathbf{77.6\ V}$
* $\alpha=90^\circ$: $\mathbf{51.7\ V}$; $\alpha=120^\circ$: $\mathbf{25.9\ V}$
:::

## 8.7 Importance, advantages, disadvantages

* Small size, trouble-free service, reliable, fast action, lightweight, **no mechanical parts, noiseless**; cheap, widely available; switches high currents easily.
* **Disadvantage (class note):** it conducts in **only one direction**, so it controls only dc or the forward half-cycle of ac (“takes half cycle”). This is what the TRIAC fixes.

## 8.8 Try it yourself

::: try Chapter 8 questions
1. Name the terminals and layers of an SCR. To which layer is the gate connected?
2. Which junction is reverse biased when the gate is open and the anode is positive?
3. Explain the two-transistor analogy in three sentences.
4. What happens to the SCR when the gate signal is removed after it has fired? How can it be turned off?
5. Half-wave SCR control, $V_m=325$ V, $\alpha=90^\circ$. Find $V_{dc}$.

<details markdown="1"><summary>Answers</summary>

1. Anode, cathode, gate; layers P-N-P-N ($P_1N_1P_2N_2$); the gate goes to $P_2$ (next to the cathode).
2. The middle junction $J_2$.
3. PNP ($P_1N_1P_2$) and NPN ($N_1P_2N_2$) are cross-connected: each one’s collector supplies the other’s base. A gate pulse starts $Tr_2$, which drives $Tr_1$, which drives $Tr_2$ harder: regenerative action turns both fully on.
4. It stays on (latched). Turn it off by reducing the anode current below the holding current or reversing the anode voltage.
5. $V_{dc}=\dfrac{325}{2\pi}(1+\cos90^\circ)=\mathbf{51.7\ V}$.
</details>
:::

# Chapter 9: TRIAC and DIAC {.chap}

*Class notes pp. 5–7 · slides: SCR, TRIAC and DIAC (slides 14–29)*

::: kid Two SCRs back-to-back
An SCR only lets current go one way, so it wastes the other half of an AC wave. A **TRIAC** is basically **two SCRs glued back to back, facing opposite ways, sharing one gate**. Now a single gate pulse can switch current in **either direction**, like a valve that works whichever way the water flows. That is how lamp dimmers and fan-speed controls work. A **DIAC** is the small helper that gives the TRIAC its trigger pulse. It has no gate: it just “pops” when the voltage across it reaches about 30 V.
:::

## 9.1 TRIAC

* TRIAC = **Tri**ode for **A**lternating **C**urrent. Formal name: *bidirectional triode thyristor*. Three terminals: **MT$_1$**, **MT$_2$** (Main Terminals; also A$_1$, A$_2$) and **G**.
* Conducts current in **either direction** when triggered. A thyristor is analogous to a relay: a small voltage/current controls a much larger voltage/current.
* Trigger at a controlled **phase angle** of the AC waveform → **phase control** of the average current: speed control of induction motors, lamp dimming, electric-heater control.

{{fig c_triac_symbol|TRIAC symbol: two opposite diodes with one gate.|40}}

**SCR vs TRIAC (your slide):**

| SCR | TRIAC |
|---|---|
| unidirectional | **bidirectional** |
| gate current can be only **positive** | gate current can be **positive or negative** |
| operates in **one quadrant** of the V–I characteristic | operates in **two quadrants** (I and III) |

### Construction

{{fig p_triac_struct|Five-layer TRIAC structure and its equivalent: two SCRs in inverse-parallel.|75}}

A TRIAC is a **three-terminal, five-layer** device whose forward and reverse characteristics are identical to the forward characteristic of an SCR. It is equivalent to **two SCRs in inverse parallel** (anode of each connected to the cathode of the other) with the gates commoned. Your class sketch shows the layers $N_4,P_1,N_1,P_2,N_2,N_3$ and the electrical equivalent: SCR$_1$ ($P_1N_1P_2N_2$) and SCR$_2$ ($P_2N_1P_1N_4$).

### V–I characteristic

{{fig p_triac_iv|TRIAC characteristic: same shape in the first and third quadrants.|68}}

Your class notes label the rated quantities (know these symbols):

| Symbol | Meaning |
|---|---|
| $V_{DRM}$ | peak repetitive **forward off-state** voltage |
| $I_{DRM}$ | peak **forward blocking** current |
| $V_{RRM}$ | peak repetitive **reverse off-state** voltage |
| $I_{RRM}$ | peak **reverse blocking** current |
| $V_{TM}$ | maximum **on-state** voltage |
| $I_H$ | **holding** current |

### Four modes of operation (slide order)

The TRIAC can be turned on with a gate pulse (you can also turn it on by exceeding the breakover voltage without a gate). Four combinations of polarity:

1. **$MT_2$ +, Gate +** (w.r.t. $MT_1$): path $P_1N_1P_2N_2$; $P_1N_1$ and $P_2N_2$ forward, $N_1P_2$ reverse. Positive gate forward-biases $P_2N_2$ and breakdown occurs.
2. **$MT_2$ +, Gate −:** current path still $P_1N_1P_2N_2$; the gate forward-biases $P_2N_3$ and injects carriers into $P_2$.
3. **$MT_2$ −, Gate −:** path $P_2N_1P_1N_4$; $P_2N_1$ and $P_1N_4$ forward, $N_1P_1$ reverse (“negatively biased region”).
4. **$MT_2$ −, Gate +:** $P_2N_2$ forward biased; carriers injected, the triac turns on. **Disadvantage:** this mode should not be used for high $di/dt$ circuits.

A gate pulse of about **35 µs** can turn it on when the applied voltage is below breakover.

::: flag Sensitivity of the four modes
The slide’s sentence about “mode 2 and 3 sensitivity” is muddled. The standard ranking (<span class="tag">extra</span>): modes 1 and 3 (gate polarity same as $MT_2$) are the most sensitive; mode 2 is less sensitive; mode 4 is the least sensitive and has the $di/dt$ limitation your slide mentions. If the exam asks, say **mode 4 is least preferred**.
:::

### Advantages, disadvantages, uses

* **Advantages:** can be triggered by gate pulses of either polarity; needs only **one heat sink** (slightly larger) where two SCRs would need two smaller; **one fuse** for protection; safe breakdown in either direction (an SCR needs a parallel diode for protection).
* **Disadvantages** (class notes, p. 6): **not as reliable as an SCR**; **$dv/dt$ rating is lower than an SCR**; lower ratings available; take care with the trigger circuit since it can be triggered in either direction.
* **Uses:** control circuits, high-power lamp switching, AC power control.

## 9.2 DIAC

* DIAC = **Di**ode for **A**lternating **C**urrent: a **bidirectional semiconductor switch** turned on in either direction when the applied voltage exceeds its **breakdown (breakover) voltage**. It is a member of the thyristor family, used mainly to **trigger TRIACs and other thyristors**. Class: “Same as TRIAC but **no gate terminal**; working principle similar to a transistor.”
* Symbol: two diodes in **inverse-parallel**, two terminals **MT$_1$, MT$_2$ (or A$_1$, A$_2$)**. Because it is bidirectional you cannot name anode/cathode: the pins are **reversible**, like a resistor.

{{fig c_diac_symbol|DIAC symbol: two terminals, no gate.|38}}

* **Construction:** a five-layer structure; layers near the terminals combine P and N regions so the device can conduct in both directions.
* **Working (from the slide):** with $MT_1$ positive, conduction follows $P_1N_2P_2N_3$; $P_1N_2$ and $P_2N_3$ are forward biased, $N_2P_2$ is reverse biased. With $MT_2$ positive, conduction follows $P_2N_2P_1N_1$; $P_2N_2$ and $P_1N_1$ forward, $N_2P_1$ reverse.

{{fig p_diac_iv|DIAC characteristic: blocking below $V_{BO}$ (≈ 30 V), then it snaps into conduction with a voltage drop.|66}}

* **V–I behaviour:** initially the resistance is high (reverse-biased junction inside), so only a small leakage flows (**blocking state**). When the applied voltage reaches the **breakover voltage** ($V_{BO1}$ for one polarity, $V_{BO2}$ for the other; typically about **30 V**), the resistance drops abruptly, the voltage across the device falls and the current increases (**conduction state**). It stays on until the current drops below the **holding current**.
* **Applications:** almost only for **triggering TRIACs** and other thyristors: phase-control circuits, motor-speed control, **light dimmers**, heat controls.

::: kid The dimmer trick
In a lamp dimmer a resistor-and-capacitor pair slowly charges as the AC wave rises. When the capacitor voltage reaches the DIAC’s breakover voltage (about 30 V), the DIAC suddenly conducts and dumps a pulse into the TRIAC’s gate, firing it. A bigger resistor makes the capacitor charge more slowly, so the TRIAC fires **later** in each half-cycle, and the lamp gets **less power**: dimmer.
:::

## 9.3 Comparison table

| | SCR | TRIAC | DIAC |
|---|---|---|---|
| Terminals | 3 (A, K, G) | 3 (MT1, MT2, G) | 2 (MT1, MT2) |
| Layers | 4 (PNPN) | 5 | 5 |
| Direction | one | both | both |
| Gate | yes (positive) | yes (+ or −) | **none** |
| Turns on by | gate pulse or $V_{BO}$ | gate pulse (either polarity) or $V_{BO}$ | voltage exceeding $V_{BO}$ (~30 V) |
| Main use | dc / half-wave power control, switching | ac full-wave power control | triggering TRIAC |

## 9.4 Try it yourself

::: try Chapter 9 questions
1. Why is a TRIAC preferred to an SCR for ac power control?
2. Draw the SCR equivalent of a TRIAC.
3. What are $V_{DRM}$, $I_{DRM}$, $V_{TM}$, $I_H$?
4. Why does a DIAC not have a gate? What is its typical breakover voltage?
5. Two disadvantages of a TRIAC compared to an SCR.

<details markdown="1"><summary>Answers</summary>

1. It conducts in both directions (both half-cycles), can be triggered by either gate polarity, and needs one heat sink and one fuse.
2. Two SCRs in inverse parallel with a common gate (see Fig).
3. Peak repetitive forward off-state voltage; peak forward blocking current; maximum on-state voltage; holding current.
4. It is turned on simply by the applied voltage exceeding its breakdown voltage in either polarity; about 30 V.
5. Less reliable and a lower $dv/dt$ rating; must take care with triggering because it can be triggered in either direction; lower ratings available.
</details>
:::
