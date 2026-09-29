# Chapter 0: Symbols, units and abbreviations decoder

::: kid Why this chapter exists
Electronics is written in a kind of shorthand. Every capital letter and little subscript is a word in disguise. This chapter is your **dictionary**. You do not need to memorise it. Read it once, then come back whenever a symbol looks strange. Every chapter also opens with its own short list of the words it needs.
:::

## 0.1 How to read a symbol like $I_{CQ}$

A symbol has a **main letter** (what kind of thing) and a **subscript** (which one, or where):

| Main letter | Means | Unit |
|---|---|---|
| $V$ | voltage (pressure that pushes current) | volt, V |
| $I$ | current (how much charge flows per second) | ampere, A |
| $R$ | resistance | ohm, Ω |
| $C$ | capacitance | farad, F |
| $L$ | inductance | henry, H |
| $P$ | power | watt, W |
| $f$ | frequency | hertz, Hz |
| $T$ | temperature (in **kelvin** unless it says °C) or a time period | K or s |

**Subscripts** tell you *where*:

| Subscript | Means | Example |
|---|---|---|
| $B$, $C$, $E$ | base, collector, emitter of a transistor | $I_B$ = current into the base |
| $BE$, $CE$, $CB$ | *between* two terminals | $V_{BE}$ = voltage from base to emitter |
| $CC$, $EE$, $BB$ | the supply connected to that terminal | $V_{CC}$ = collector supply voltage |
| $Q$ | at the **Q-point** (resting point, no signal) | $I_{CQ}$ = resting collector current |
| $L$ | the **load** (the thing being powered) | $R_L$ = load resistor |
| $S$ | the **source** or the transformer **secondary** | $R_S$, $V_S$ |
| $m$ or max | the **peak** (maximum) value of a wave | $V_m$ = peak voltage |
| dc, avg | the **average (steady) value** | $I_{dc}$ |
| rms | the **effective value** of a changing wave | $I_{rms}$ |
| $i$, $o$ | input, output | $V_i$, $V_o$ |
| $F$, $R$ | forward, reverse | $V_F$, $I_R$ |
| $Z$ | Zener; or impedance (when it is the main letter) | $V_Z$, $Z_i$ |
| $0$ | zero-bias / equilibrium / saturation-leakage | $I_0$, $V_0$ |

## 0.2 Metric prefixes (you will see these on every resistor)

| Prefix | Symbol | Multiply by | Example |
|---|---|---|---|
| pico | p | $10^{-12}$ | 100 pF = $100\times10^{-12}$ F |
| nano | n | $10^{-9}$ | 10 nA = $10\times10^{-9}$ A |
| micro | µ | $10^{-6}$ | 47 µF = $47\times10^{-6}$ F |
| milli | m | $10^{-3}$ | 2 mA = 0.002 A |
| (none) | | 1 | 5 V |
| kilo | k | $10^{3}$ | 2.2 kΩ = 2200 Ω |
| mega | M | $10^{6}$ | 1 MΩ = 1 000 000 Ω |
| giga | G | $10^{9}$ | 10 GHz = $10^{10}$ Hz |

::: trap The number-one source of lost marks
Most wrong answers in circuit problems are **unit slips**. Before you calculate, convert everything to volts, amperes, ohms, farads, henries. Example: $R=2.2\ \text{k}\Omega$ means 2200 in a formula, not 2.2.
:::

## 0.3 Abbreviations, in alphabetical order

| Abbreviation | Stands for | Plain meaning |
|---|---|---|
| ac | alternating current/voltage | keeps reversing direction (mains electricity) |
| AFC | automatic frequency control | circuit that keeps a radio tuned to its station |
| Al, B, Ga, In | aluminium, boron, gallium, indium | acceptor impurities (make P-type) |
| As, P, Sb | arsenic, phosphorus, antimony | donor impurities (make N-type) |
| BJT | bipolar junction transistor | the three-layer transistor of Unit II |
| BC547 | a common NPN transistor part number | used in your lab |
| CB, CC, CE | common base / collector / emitter | which terminal is shared by input and output |
| dc | direct current/voltage | steady, one direction |
| DIAC | diode for alternating current | two-terminal trigger switch |
| Ge, Si | germanium, silicon | the two semiconductors |
| GaAs, GaP, InGaN… | gallium arsenide, gallium phosphide… | compound semiconductors used in LEDs |
| FWR, HWR | full-wave / half-wave rectifier | uses both / one half of the ac wave |
| KVL | Kirchhoff's voltage law | voltages around a closed loop add to zero |
| LED | light emitting diode | diode that glows |
| LO | local oscillator | a radio's internal tuning oscillator |
| PIN | P–Intrinsic–N | photodiode with an undoped middle layer |
| PIV | peak inverse voltage | largest reverse voltage across a diode |
| PNP, NPN | layer order of a transistor | P-N-P or N-P-N |
| Q-point | quiescent point | resting dc operating point |
| rms | root mean square | effective value of a wave |
| SCR | silicon controlled rectifier | 4-layer latching switch |
| TRIAC | triode for alternating current | 3-terminal two-way switch |
| TUF | transformer utilisation factor | how well the transformer is used |
| UJT | unijunction transistor | 3-terminal, one-junction oscillator device |
| $J_1,J_2,J_3$ | junctions 1, 2, 3 | the three PN junctions in an SCR |
| MT$_1$, MT$_2$ | main terminals 1 and 2 | the two power terminals of TRIAC/DIAC |
| $B_1$, $B_2$ | base 1, base 2 | the two ends of a UJT bar |
| eV | electron-volt | energy unit: $1\ \text{eV}=1.6\times10^{-19}$ J |
| S/cm | siemens per centimetre | unit of conductivity |
| Ω·cm | ohm-centimetre | unit of resistivity |

## 0.4 Greek letters and special symbols

| Symbol | Name | Where used | Meaning |
|---|---|---|---|
| $\alpha$ | alpha | BJT | $I_C/I_E$, just under 1 |
| $\beta$ | beta | BJT | $I_C/I_B$, the current gain (50–300) |
| $\gamma$ | gamma | rectifier/filter | **ripple factor** (ac wiggle ÷ dc) |
| $\eta$ | eta | diode; UJT; rectifier | (diode) 1 for Ge, 2 for Si; (UJT) stand-off ratio; (rectifier) efficiency |
| $\mu$ | mu | semiconductors | **mobility** of carriers |
| $\sigma$ | sigma | semiconductors | **conductivity** |
| $\rho$ | rho | semiconductors | **resistivity**, or **charge density** in junction maths |
| $\tau$ | tau | diodes, UJT | carrier **lifetime**, or an RC **time constant** |
| $\varepsilon$ | epsilon | junction | **permittivity** ($\varepsilon_0\varepsilon_r$) |
| $\omega$ | omega | ac | angular frequency $=2\pi f$ (rad/s) |
| $\Omega$ | capital omega | everywhere | ohm |
| $\Delta$ | delta | slopes | "a small change in", so $\Delta V/\Delta I$ = slope |
| $\approx$ | | | approximately equal |
| $\gg$ | | | much greater than |
| $\propto$ | | | proportional to |
| $\parallel$ | | | in parallel with: $R_1\parallel R_2=\dfrac{R_1R_2}{R_1+R_2}$ |
| $\sqrt{\ }$, $\ln$, $\log_{10}$, $e^x$ | | | square root; natural log; common log; exponential |

## 0.5 Constants you will use

| Constant | Value |
|---|---|
| electron charge $q$ | $1.6\times10^{-19}$ C |
| Boltzmann constant $k$ | $8.617\times10^{-5}$ eV/K |
| thermal voltage $V_T=kT/q$ | $T/11600$; **25.9 mV at 300 K** |
| vacuum permittivity $\varepsilon_0$ | $8.85\times10^{-12}$ F/m $=8.85\times10^{-14}$ F/cm |
| relative permittivity of Si, $\varepsilon_r$ | 12 |
| $\pi$ | 3.1416 |
| Si: $E_g$, $n_i$ (300 K) | 1.1 eV; $1.5\times10^{10}\ \text{cm}^{-3}$ |
| Ge: $E_g$, $n_i$ (300 K) | 0.74 eV; $2.5\times10^{13}\ \text{cm}^{-3}$ |
| °C to K | add 273 |

## 0.6 Three rules that make every circuit problem easier

1. **Draw first, then calculate.** Draw the circuit and label every voltage and current with a direction.
2. **Units first.** Convert prefixes (k, m, µ, n, p) into base units.
3. **Say what you assume.** For example: "assume silicon, so $V_{BE}=0.7$ V". Examiners give marks for stated assumptions.

::: try Quick check
1. What does $V_{CEQ}$ mean, letter by letter?
2. Write 4.7 kΩ, 100 nF and 20 mA in base units.
3. What is $R_1\parallel R_2$ for 6 kΩ and 3 kΩ?
:::

::: soln Answers and full solutions
<details markdown="1"><summary>Solution 1</summary>

**Step 1.** Main letter $V$: a voltage.
**Step 2.** Subscript $CE$: measured between the collector and the emitter.
**Step 3.** Last subscript $Q$: at the Q-point, the resting (no-signal) condition.

**Answer:** the resting (dc) voltage from collector to emitter of a transistor.
</details>

<details markdown="1"><summary>Solution 2</summary>

**Step 1.** k means $10^3$: $4.7\ \text{k}\Omega=4.7\times1000=4700\ \Omega$.
**Step 2.** n means $10^{-9}$: $100\ \text{nF}=100\times10^{-9}=10^{-7}$ F.
**Step 3.** m means $10^{-3}$: $20\ \text{mA}=20\times10^{-3}=0.02$ A.
</details>

<details markdown="1"><summary>Solution 3</summary>

**Formula:** $R_1\parallel R_2=\dfrac{R_1R_2}{R_1+R_2}$.
**Step 1.** Multiply: $6\text{k}\times3\text{k}=18\ \text{k}^2$.
**Step 2.** Add: $6\text{k}+3\text{k}=9\ \text{k}$.
**Step 3.** Divide: $18/9=2$ kΩ.

**Answer:** 2 kΩ. (The parallel value is always smaller than the smallest resistor.)
</details>
:::
