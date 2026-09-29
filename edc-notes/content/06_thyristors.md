# Chapter 8: Silicon-controlled rectifier (SCR)

*Class notes pp. 4–5 · slides: SCR, TRIAC and DIAC (slides 1–13)*

::: words
| Word / symbol | Plain meaning |
|---|---|
| SCR | Silicon Controlled Rectifier: a 4-layer switch that a small gate pulse turns ON |
| Thyristor | the family of latching switches (SCR, TRIAC, DIAC) |
| Anode (A), Cathode (K), Gate (G) | the three SCR terminals; the gate is the control input |
| P-N-P-N | the four alternating layers: $P_1$, $N_1$, $P_2$, $N_2$ |
| $J_1,J_2,J_3$ | the three PN junctions, counted from the anode |
| Forward blocking | anode positive but SCR still OFF |
| Forward conducting | SCR ON, current flows anode → cathode |
| Reverse blocking | anode negative: SCR OFF |
| $V_{BO}$ | forward **breakover voltage**: anode voltage at which the SCR switches on by itself |
| $I_G$ | gate current |
| $I_H$ | **holding current**: minimum anode current to stay ON |
| Latching | staying ON after the gate pulse has gone |
| Firing angle $\alpha$ | the point in the AC half-cycle where the gate pulse is applied |
| Regenerative | self-reinforcing (positive feedback) |
| $V_{dc}$ | average (dc) output voltage |
:::

::: kid A door with a latch
A normal diode is a door that opens whenever you push. An **SCR** is a door with a **latch**. It stays shut even when you push forward (**forward blocking**) until you give a small **pulse on the gate**. Then it snaps open and **stays open by itself**, even after you remove the gate pulse, until the current through it falls almost to zero. A tiny gate current can therefore control a huge load current, like a small key starting a big engine.
:::

## 8.1 What it is

* Introduced by **Bell Telephone Laboratories in 1956**. A power-electronics device that can **convert AC to DC and also control the amount of power fed to the load**: it **combines the features of a rectifier and a transistor**.
* **Three terminals:** Anode (A), Cathode (K), Gate (G). **Four layers:** P-N-P-N.
* Two main uses: **switching** and **amplification** (power-amplifier circuits). Applications in your notes: relay control, motor control, power amplifier, switch, rectification, regulated power supplies, static switches, motor-speed control, battery chargers, heater controls.
* Made of **silicon** (much smaller leakage and better temperature behaviour than germanium).

{{fig c_scr_symbol|SCR symbol.|30}}

## 8.2 Structure

{{fig p_scr_struct|Four layers and three junctions. The outer layers are the anode (P) and cathode (N); the gate is joined to the P layer next to the cathode.|72}}

The junctions are $J_1,J_2,J_3$, numbered from the anode side ($J_1$ is nearest the anode).

## 8.3 Two-transistor analogy (class notes, p. 4)

{{fig p_scr_two_tr|The SCR as a PNP transistor ($Tr_1$) and an NPN transistor ($Tr_2$) cross-connected.|75}}

Split the four layers into two overlapping transistors: **$Tr_1$ = $P_1N_1P_2$ (PNP)** and **$Tr_2$ = $N_1P_2N_2$ (NPN)**. The collector of each feeds the base of the other.

1. A small gate current turns $Tr_2$ on.
2. $Tr_2$'s collector current is the base current of $Tr_1$, so $Tr_1$ turns on.
3. $Tr_1$'s collector current is more base current for $Tr_2$, so $Tr_2$ turns on harder.
4. This repeats in a loop: **regenerative (positive) feedback**. Both transistors go into saturation within microseconds. That is the "latching".

<span class="tag">extra</span> In equations: with current gains $\alpha_1,\alpha_2$, $I_A=\dfrac{\alpha_2I_G+I_{CBO1}+I_{CBO2}}{1-(\alpha_1+\alpha_2)}$. The SCR turns on when $\alpha_1+\alpha_2\to1$; gate current raises the $\alpha$s.

## 8.4 How it works

The load is connected in series with the anode, and the **anode is kept positive** relative to the cathode. Two cases:

**Case 1: gate open (no gate voltage).**
* $J_1$ and $J_3$ are forward biased but $J_2$ is **reverse biased**.
* A reverse-biased junction blocks current, so almost no current flows: the SCR is **cut-off (OFF)**.

**Case 2: gate positive with respect to the cathode.**
* $J_3$ is forward biased; $J_2$ is still reverse biased.
* Electrons from the N layer cross $J_3$ and holes move the other way. The electrons that crossed $J_3$ are then attracted across $J_2$. This starts the **gate current**, and $J_2$ begins to conduct.
* The SCR turns **ON**.

## 8.5 V–I characteristic and the three states

{{fig p_scr_iv|SCR characteristic: forward blocking → (at $V_{BO}$ or with a gate pulse) → forward conducting; reverse blocking on the left.|78}}

1. **Forward blocking (OFF state):** anode positive, gate open. The SCR blocks the forward current that an ordinary forward-biased diode would carry; only a tiny leakage flows.
2. **Forward conduction (ON state):** the SCR has fired. Voltage across it is low; current is limited by the load. It stays on until the anode current falls below the **holding current** $I_H$.
3. **Reverse blocking (OFF state):** anode negative: blocks like a reverse-biased diode. Too much reverse voltage causes reverse breakdown (avoid it).

{{fig p_scr_family|Gate current lowers the forward breakover voltage: with enough $I_G$ the SCR fires at a small anode voltage.|66}}

<span class="tag">extra</span> **Latching current** $I_L$ is the minimum anode current needed to keep the SCR on right after the gate pulse is removed; **holding current** $I_H$ is the minimum to stay on afterwards. To turn an SCR off, reduce its anode current below $I_H$ or reverse the anode voltage briefly (in ac circuits this happens automatically every negative half-cycle).

## 8.6 Power control by firing angle <span class="tag">extra</span>

{{fig p_phase|Top: an SCR fires at $\alpha=60^\circ$ in each positive half-cycle. Bottom: a TRIAC does it in both half-cycles.|85}}

Delaying the gate pulse (larger firing angle $\alpha$) reduces the average power to the load. For a half-wave SCR circuit with a resistive load:
$$V_{dc}=\frac{V_m}{2\pi}\left(1+\cos\alpha\right)$$
Here $V_m$ is the peak of the supply voltage and $\alpha$ is the firing angle.

::: ex Example 8.1: Average voltage versus firing angle
**Given:** 230 V rms supply, half-wave SCR circuit, resistive load.

**Find:** $V_{dc}$ for $\alpha=0^\circ,60^\circ,90^\circ,120^\circ$.

**Step 1: peak voltage.** $V_m=230\times\sqrt2=325$ V.
**Step 2: the constant.** $\dfrac{V_m}{2\pi}=\dfrac{325}{6.283}=51.7$ V.
**Step 3: each angle.** Compute $1+\cos\alpha$ then multiply by 51.7 V:

| $\alpha$ | $\cos\alpha$ | $1+\cos\alpha$ | $V_{dc}=51.7\times(1+\cos\alpha)$ |
|---|---|---|---|
| 0° | 1 | 2 | **103.5 V** |
| 60° | 0.5 | 1.5 | **77.6 V** |
| 90° | 0 | 1 | **51.7 V** |
| 120° | −0.5 | 0.5 | **25.9 V** |

**What it means:** at $\alpha=0^\circ$ the SCR acts like an ordinary half-wave rectifier ($V_m/\pi=103.5$ V). Delaying the trigger gives smooth control down to zero.
:::

## 8.7 Importance, advantages, disadvantages

* Small size, trouble-free service, reliable, fast action, lightweight, **no moving parts, silent**; cheap, widely available; switches high currents easily.
* **Disadvantage (class note):** it conducts in **only one direction**, so it controls only dc or the forward half-cycle of an ac wave ("takes half cycle"). The TRIAC fixes this.

## 8.8 Practice

::: try Questions for Chapter 8
1. Name the terminals and layers of an SCR. To which layer is the gate connected?
2. Which junction is reverse biased when the gate is open and the anode is positive?
3. Explain the two-transistor analogy in three or four sentences.
4. What happens to the SCR when the gate signal is removed after firing? How can it be turned off?
5. A half-wave SCR circuit has $V_m=325$ V and $\alpha=90^\circ$. Find $V_{dc}$.
6. Find $V_{dc}$ for $V_m=170$ V and $\alpha=30^\circ$.
:::

::: soln Answers and full solutions
<details markdown="1"><summary>Solution 1</summary>

Terminals: **anode, cathode, gate**. Layers: $P_1N_1P_2N_2$ (four layers, P-N-P-N). The gate is connected to $P_2$, the P layer next to the cathode.
</details>

<details markdown="1"><summary>Solution 2</summary>

The **middle junction $J_2$** (between $N_1$ and $P_2$). $J_1$ and $J_3$ are forward biased.
</details>

<details markdown="1"><summary>Solution 3</summary>

**Step 1.** Treat $P_1N_1P_2$ as a PNP transistor and $N_1P_2N_2$ as an NPN transistor sharing layers.
**Step 2.** The collector of each is joined to the base of the other.
**Step 3.** A gate pulse turns the NPN on. Its collector current is the PNP's base current, so the PNP turns on, and its collector current feeds the NPN's base further.
**Step 4.** This self-reinforcing loop drives both transistors into saturation: the SCR latches ON.
</details>

<details markdown="1"><summary>Solution 4</summary>

It **stays ON** (latched) because the regenerative loop holds itself on. It turns off when the anode current falls below the holding current $I_H$ or when the anode voltage is reversed.
</details>

<details markdown="1"><summary>Solution 5</summary>

**Formula:** $V_{dc}=\dfrac{V_m}{2\pi}(1+\cos\alpha)$.
**Step 1.** $\cos90^\circ=0$, so $1+\cos\alpha=1$.
**Step 2.** $V_{dc}=\dfrac{325}{2\pi}\times1=51.7$ V.

**Answer:** **51.7 V**.
</details>

<details markdown="1"><summary>Solution 6</summary>

**Step 1.** $\cos30^\circ=0.866$, so $1+\cos\alpha=1.866$.
**Step 2.** $\dfrac{V_m}{2\pi}=\dfrac{170}{6.283}=27.06$ V.
**Step 3.** $V_{dc}=27.06\times1.866=50.5$ V.

**Answer:** **50.5 V**.
</details>
:::

# Chapter 9: TRIAC and DIAC {.chap}

*Class notes pp. 5–7 · slides: SCR, TRIAC and DIAC (slides 14–29)*

::: words
| Word / symbol | Plain meaning |
|---|---|
| TRIAC | Triode for Alternating Current: a gated switch that conducts both ways |
| DIAC | Diode for Alternating Current: a 2-terminal trigger switch, no gate |
| $MT_1$, $MT_2$ | Main Terminal 1 and 2 (also called $A_1$, $A_2$) |
| G | gate terminal (TRIAC only) |
| Bidirectional | works for current in either direction |
| Inverse-parallel | two devices connected side by side but facing opposite ways |
| Quadrant | a quarter of the V–I graph; TRIAC works in quadrants I and III |
| $V_{DRM}$ | peak repetitive **forward** off-state voltage (largest forward voltage it can block) |
| $I_{DRM}$ | peak forward **blocking** current (leakage while blocking forward) |
| $V_{RRM}$ | peak repetitive **reverse** off-state voltage |
| $I_{RRM}$ | peak reverse blocking current |
| $V_{TM}$ | maximum **on-state** voltage (voltage drop while conducting) |
| $I_H$ | holding current |
| $V_{BO}$ | breakover voltage |
| $di/dt$, $dv/dt$ | how fast current / voltage change; devices have limits on both |
| Phase control | firing the switch part-way through each half-cycle to set the average power |
:::

::: kid Two SCRs back-to-back
An SCR lets current go only one way, so it wastes the other half of an AC wave. A **TRIAC** is basically **two SCRs glued back to back, facing opposite ways, sharing one gate**. Now a single gate pulse can switch current in **either direction**, like a valve that works whichever way the water flows. That is how lamp dimmers and fan-speed controls work. A **DIAC** is the small helper that gives the TRIAC its trigger pulse. It has no gate: it just "pops" when the voltage across it reaches about 30 V.
:::

## 9.1 TRIAC

* TRIAC = **Tri**ode for **A**lternating **C**urrent. Formal name: *bidirectional triode thyristor*. Three terminals: **$MT_1$**, **$MT_2$** and **G**.
* It conducts current in **either direction** when triggered. A thyristor is like a relay: a small voltage/current controls a much larger voltage/current.
* Triggering at a controlled **phase angle** of the AC wave gives **phase control** of the average current: speed control of induction motors, lamp dimming, heater control.

{{fig c_triac_symbol|TRIAC symbol: two opposite diodes with one gate.|40}}

**SCR versus TRIAC (your slide):**

| SCR | TRIAC |
|---|---|
| unidirectional (one way) | **bidirectional** |
| gate current can only be **positive** | gate current can be **positive or negative** |
| works in **one quadrant** of the V–I graph | works in **two quadrants** (I and III) |

### Construction

{{fig p_triac_struct|Five-layer TRIAC structure and its equivalent: two SCRs in inverse-parallel.|75}}

A TRIAC is a **three-terminal, five-layer** device whose forward and reverse characteristics are the same as the forward characteristic of an SCR. It is equivalent to **two SCRs in inverse-parallel** (anode of each joined to the cathode of the other) with the gates joined. Your class sketch shows layers $N_4,P_1,N_1,P_2,N_2,N_3$ and the equivalent circuit: SCR$_1$ ($P_1N_1P_2N_2$) and SCR$_2$ ($P_2N_1P_1N_4$).

### V–I characteristic

{{fig p_triac_iv|TRIAC characteristic: the same shape in the first and third quadrants.|68}}

Your class notes label these rated quantities; know the symbols:

| Symbol | Meaning |
|---|---|
| $V_{DRM}$ | peak repetitive **forward off-state** voltage |
| $I_{DRM}$ | peak **forward blocking** current |
| $V_{RRM}$ | peak repetitive **reverse off-state** voltage |
| $I_{RRM}$ | peak **reverse blocking** current |
| $V_{TM}$ | maximum **on-state** voltage |
| $I_H$ | **holding** current |

### Four modes of operation (slide)

A TRIAC turns on by a gate pulse (or when the voltage exceeds breakover). There are four polarity combinations, all measured relative to $MT_1$:

1. **$MT_2$ +, Gate +:** path $P_1N_1P_2N_2$; $P_1N_1$ and $P_2N_2$ are forward biased, $N_1P_2$ is reverse biased. The positive gate forward-biases $P_2N_2$ and the device breaks over into conduction.
2. **$MT_2$ +, Gate −:** current still follows $P_1N_1P_2N_2$; the negative gate forward-biases $P_2N_3$ and injects carriers into $P_2$.
3. **$MT_2$ −, Gate −:** path $P_2N_1P_1N_4$; $P_2N_1$ and $P_1N_4$ are forward biased, $N_1P_1$ reverse.
4. **$MT_2$ −, Gate +:** $P_2N_2$ is forward biased, carriers are injected and the TRIAC turns on. **Disadvantage:** this mode should not be used for high $di/dt$ circuits.

A gate pulse of about **35 µs** can turn the TRIAC on when the applied voltage is below breakover.

::: flag Sensitivity of the four modes
The slide's sentence about the sensitivity of modes 2 and 3 is muddled. The standard ranking <span class="tag">extra</span> is: modes 1 and 3 (gate polarity same as $MT_2$) are most sensitive; mode 2 is less sensitive; mode 4 is least sensitive and has the $di/dt$ limit your slide mentions. If asked, say **mode 4 is least preferred**.
:::

### Advantages, disadvantages, uses

* **Advantages:** triggered by gate pulses of either polarity; needs only **one heat sink** (slightly larger) where two SCRs would need two smaller ones; **one fuse**; safe breakdown in either direction (an SCR needs a parallel diode for protection).
* **Disadvantages** (class notes p. 6): **not as reliable as an SCR**; **$dv/dt$ rating lower than an SCR**; lower ratings available; take care with the trigger circuit since it can be triggered in either direction.
* **Uses:** control circuits, high-power lamp switching, AC power control.

## 9.2 DIAC

* DIAC = **Di**ode for **A**lternating **C**urrent: a **bidirectional semiconductor switch** turned on in either direction when the voltage exceeds its **breakdown (breakover) voltage**. It belongs to the thyristor family and is mainly used to **trigger TRIACs and other thyristors**. Class: "Same as TRIAC but **no gate terminal**; working principle similar to a transistor."
* Symbol: two diodes in **inverse-parallel**, two terminals **$MT_1$, $MT_2$** (or $A_1$, $A_2$). It is bidirectional, so you cannot name an anode and cathode: the pins are **reversible**, like a resistor.

{{fig c_diac_symbol|DIAC symbol: two terminals, no gate.|38}}

* **Construction:** a five-layer structure; the layers near the terminals combine P and N regions so it can conduct both ways.
* **Working (slide):** with $MT_1$ positive, conduction follows $P_1N_2P_2N_3$; $P_1N_2$ and $P_2N_3$ are forward biased, $N_2P_2$ is reverse biased. With $MT_2$ positive, conduction follows $P_2N_2P_1N_1$; $P_2N_2$ and $P_1N_1$ are forward biased, $N_2P_1$ reverse.

{{fig p_diac_iv|DIAC characteristic: blocking below $V_{BO}$ (about 30 V), then it snaps into conduction with a lower voltage across it.|66}}

* **V–I behaviour:**
  1. At first the resistance is high (a reverse-biased junction inside), so only a small leakage current flows: the **blocking state**.
  2. When the applied voltage reaches the **breakover voltage** ($V_{BO1}$ for one polarity, $V_{BO2}$ for the other; typically about **30 V**), the resistance drops abruptly, the voltage across the device falls and the current increases: the **conduction state**.
  3. It stays on until the current drops below the **holding current**.
* **Applications:** almost only for **triggering TRIACs** and other thyristors: phase-control circuits, motor-speed control, **light dimmers**, heat controls.

::: kid The dimmer trick
In a lamp dimmer a resistor–capacitor pair charges as the AC wave rises. When the capacitor voltage reaches the DIAC's breakover voltage (about 30 V), the DIAC suddenly conducts and dumps a pulse into the TRIAC's gate, firing it. A bigger resistor makes the capacitor charge more slowly, so the TRIAC fires **later** in each half-cycle and the lamp receives **less power**: it dims.
:::

## 9.3 Comparison

| | SCR | TRIAC | DIAC |
|---|---|---|---|
| Terminals | 3 (A, K, G) | 3 ($MT_1$, $MT_2$, G) | 2 ($MT_1$, $MT_2$) |
| Layers | 4 (PNPN) | 5 | 5 |
| Direction | one | both | both |
| Gate | yes (positive) | yes (+ or −) | **none** |
| Turns on by | gate pulse or $V_{BO}$ | gate pulse (either polarity) or $V_{BO}$ | voltage above $V_{BO}$ (about 30 V) |
| Main use | dc / half-wave power control, switching | ac full-wave power control | triggering a TRIAC |

## 9.4 Practice

::: try Questions for Chapter 9
1. Why is a TRIAC preferred to an SCR for AC power control?
2. Draw the SCR equivalent of a TRIAC.
3. What do $V_{DRM}$, $I_{DRM}$, $V_{TM}$ and $I_H$ mean?
4. Why does a DIAC have no gate? What is its typical breakover voltage?
5. Give two disadvantages of a TRIAC compared with an SCR.
6. Which of the four TRIAC modes is least preferred, and why?
:::

::: soln Answers and full solutions
<details markdown="1"><summary>Solution 1</summary>

**Step 1.** An SCR conducts one way only, so it can control only half of an AC wave.
**Step 2.** A TRIAC conducts in **both** directions, so it controls **both half-cycles**.
**Step 3.** It can be triggered by a gate pulse of **either polarity**, needs one heat sink and one fuse.
</details>

<details markdown="1"><summary>Solution 2</summary>

Two SCRs connected in **inverse-parallel**: the anode of SCR$_1$ to the cathode of SCR$_2$ (terminal $MT_2$) and the cathode of SCR$_1$ to the anode of SCR$_2$ (terminal $MT_1$), with both gates joined to a single gate terminal G.
</details>

<details markdown="1"><summary>Solution 3</summary>

* $V_{DRM}$: peak repetitive forward off-state voltage (most it can block in the forward direction).
* $I_{DRM}$: peak forward blocking current (leakage while blocking forward).
* $V_{TM}$: maximum on-state voltage (voltage drop while conducting).
* $I_H$: holding current (minimum current to stay ON).
</details>

<details markdown="1"><summary>Solution 4</summary>

A DIAC is switched on purely by the applied voltage exceeding its breakover voltage in either polarity, so no control terminal is needed. Typical breakover voltage: about **30 V**.
</details>

<details markdown="1"><summary>Solution 5</summary>

(Any two.) A TRIAC is **less reliable** than an SCR; its **$dv/dt$ rating is lower**; only **lower ratings** are available; the trigger circuit needs care because it can be triggered in either direction.
</details>

<details markdown="1"><summary>Solution 6</summary>

Mode 4 ($MT_2$ negative, gate positive). It is the least sensitive and must not be used for circuits with high $di/dt$.
</details>
:::
