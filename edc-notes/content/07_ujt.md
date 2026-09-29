# Chapter 10: Unijunction transistor (UJT) and the relaxation oscillator

*Class notes pp. 8–10 · slides: UJT and Photodiode; scan "EDC UJT" (oscillator notes)*

::: words
| Word / symbol | Plain meaning |
|---|---|
| UJT | Unijunction Transistor: 3 terminals, only one PN junction |
| $E$, $B_1$, $B_2$ | Emitter, Base 1, Base 2 terminals |
| $R_{BB}$ | inter-base resistance $=R_{B1}+R_{B2}$, measured with the emitter open |
| $R_{B1}$, $R_{B2}$ | the parts of the bar below and above the emitter joint |
| $V_{BB}$ | supply voltage across $B_2$ (+) and $B_1$ |
| $\eta$ | "eta": **intrinsic stand-off ratio** $=R_{B1}/(R_{B1}+R_{B2})$ (0.4–0.85) |
| $V_P$ | **peak-point voltage**: emitter voltage at which the UJT turns ON $=\eta V_{BB}$ (+0.7 V) |
| $I_P$ | peak-point current |
| $V_V$, $I_V$ | **valley point** voltage and current |
| $V_D$ | emitter-diode drop, about 0.7 V |
| Conductivity modulation | injected holes suddenly lowering $R_{B1}$ |
| Relaxation oscillator | a circuit that charges a capacitor slowly and discharges it quickly, repeating |
| $R_E$, $C_E$ | the resistor and capacitor that set the timing |
| $\tau=R_EC_E$ | time constant of the charging circuit |
| $T$, $f$ | period (time of one cycle) and frequency $f=1/T$ |
| Sawtooth | a waveform that rises slowly and drops suddenly |
:::

::: kid The bucket that tips
Fill a bucket slowly from a tap. When the water reaches a **certain level** the bucket tips over and empties in a flash. Then it starts filling again. Fill, tip, fill, tip: that is a **relaxation oscillator**. In electronics the "bucket" is a **capacitor** filling through a resistor. The "tipping" is done by the **UJT**: it stays off until the capacitor voltage reaches the **peak-point voltage $V_P$**, then suddenly turns on and dumps the capacitor's charge. The result is a saw-tooth wave and sharp pulses.
:::

## 10.1 What it is

* A **three-terminal** device with **only one PN junction**, hence "uni-junction". Terminals: **Emitter (E)**, **Base 1 ($B_1$)**, **Base 2 ($B_2$)**.
* It shows a **negative-resistance** characteristic, which makes it useful in oscillators.
* A heavily doped emitter region on a **lightly doped** N-type silicon bar.

{{fig p_ujt_struct|UJT: a lightly-doped N bar with two base contacts and one heavily-doped P emitter joint.|72}}

* The N-type silicon bar (very lightly doped) is the base; ohmic contacts $B_1$ and $B_2$ are at its ends. A **P-type impurity** introduced into the bar makes one PN junction: the **emitter**, which behaves like an ordinary diode.
* A **complementary UJT** has a P-type bar and N-type emitter; same behaviour with opposite polarities.

{{fig c_ujt_symbol|UJT symbol: the arrow on the emitter points toward the bar.|30}}

## 10.2 Equivalent circuit and stand-off ratio

{{fig c_ujt_equiv|Equivalent circuit: $R_{B2}$ and $R_{B1}$ form a voltage divider; the emitter diode connects to their junction A.|55}}

* With the emitter open, the resistance from $B_2$ to $B_1$ is just the bar's resistance: the **inter-base resistance**
$$R_{BB}=R_{B1}+R_{B2},\qquad\text{typically }5\text{ to }10\ \text{k}\Omega\ (\text{high because the bar is lightly doped}).$$
* $R_{B2}$ is between $B_2$ and point A; $R_{B1}$ is between A and $B_1$. The junction is made so that (class notes)
$$\frac{R_{B1}}{R_{B2}}=\frac23.$$
* $V_{BB}$ is applied between $B_2$ (+) and $B_1$. With the emitter open ($I_E=0$) the same current flows through both parts: $I_1=I_2=V_{BB}/R_{BB}$.
* The voltage at A (the divider point) is
$$V_A=V_{BB}\frac{R_{B1}}{R_{B1}+R_{B2}}=\eta V_{BB},\qquad\boxed{\eta=\frac{R_{B1}}{R_{B1}+R_{B2}}}.$$
$\eta$ is the **intrinsic stand-off ratio**, a property of the UJT, **always below 1, usually 0.4 to 0.85**. With $R_{B1}/R_{B2}=2/3$: $\eta=\dfrac{2}{2+3}=0.4$.

::: ex Example 10.1: Stand-off ratio from the resistances
**Given:** $R_{B1}=4\ \text{k}\Omega$, $R_{B2}=6\ \text{k}\Omega$, $V_{BB}=20$ V.

**Find:** $R_{BB}$, $\eta$ and $V_A$.

**Step 1.** $R_{BB}=R_{B1}+R_{B2}=4+6=10\ \text{k}\Omega$.
**Step 2.** $\eta=\dfrac{R_{B1}}{R_{BB}}=\dfrac{4}{10}=0.4$ (this is the $2/3$ ratio: $4/6=2/3$).
**Step 3.** $V_A=\eta V_{BB}=0.4\times20=8$ V.

**Answer:** $R_{BB}=10\ \text{k}\Omega$; $\eta=0.4$; $V_A=8$ V.

**What it means:** while the emitter is below about 8 V the emitter diode is reverse biased and the UJT is OFF.
:::

## 10.3 Working

1. The emitter diode is **reverse biased** as long as $V_E<\eta V_{BB}$ (plus the diode drop). Only leakage flows: the UJT is **OFF** (cut-off region).
2. When $V_E$ reaches the **peak-point voltage**
$$V_P=\eta V_{BB}+V_D\qquad(V_D\approx0.7\text{ V}),$$
the diode turns ON and emitter current starts to flow. This current is the **peak-point current** $I_P$.
3. **Holes** are injected from the heavily doped P emitter into the lightly doped N bar. They live a long time there and drift toward $B_1$, so the number of carriers in the $B_1$ part **increases greatly**: $R_{B1}$ **collapses** (down to about **50 Ω**). This is **conductivity modulation**.
4. Because $R_{B1}$ falls, the voltage at A falls, so the diode is held on with **more current but lower emitter voltage**: **negative resistance**.

::: flag Two forms of $V_P$ in your material
The class notes write $V_P=\eta V_{BB}$ (neglecting the diode drop). The slides write $V_P=V_D+\eta V_{BB}$ and say the UJT turns on when $V_E$ exceeds $\eta V_{BB}$ by 0.7 V. They agree if $V_D$ is treated as small. **Use $V_P=\eta V_{BB}$ (class) unless the question gives $V_D$.**
:::

## 10.4 Emitter characteristic

{{fig p_ujt_iv|Emitter voltage against emitter current for a UJT at fixed $V_{BB}$.|72}}

* **Cut-off region** ($0\le V_E<V_P$): only leakage emitter current.
* **Negative-resistance region:** after the **peak point** $(I_P,V_P)$, $I_E$ rises while $V_E$ **falls**, down to the **valley point** $(I_V,V_V)$.
* **Saturation region** (beyond the valley): $I_E$ and $V_E$ rise together; positive resistance again. $R_{B1}$ can be as low as about 50 Ω.

## 10.5 UJT as a relaxation oscillator

{{fig c_ujt_osc|UJT relaxation oscillator: $R_E$ charges $C_E$; $R_1$ and $R_2$ give the output pulses at $B_1$ and $B_2$.|60}}

**Circuit:** the supply $V_{BB}$ charges the capacitor $C_E$ through the variable resistor $R_E$. The UJT's emitter is connected to the capacitor. Small resistors $R_2$ (in series with $B_2$) and $R_1$ (in series with $B_1$) give the output spikes. The circuit generates a **saw-tooth**.

**The cycle:**
1. When $V_{BB}$ is switched on, $C_E$ charges **exponentially** through $R_E$.
2. When the capacitor voltage reaches $V_P$, the UJT fires (conducts).
3. $C_E$ **discharges rapidly** through $E$–$B_1$ and $R_1$ (the UJT provides a low-resistance path).
4. When the capacitor voltage falls near the valley voltage, the UJT switches OFF and the capacitor starts to charge again.
5. This repeats: **saw-tooth across $C_E$** (slow charge, fast discharge).

**Output waveforms:**
* **Across $C_E$ (emitter):** saw-tooth between $V_V$ and $V_P$.
* **At $B_1$ ($V_{B1}$):** **positive-going spikes** because the surge of current through $B_1$ makes a voltage drop across $R_1$.
* **At $B_2$ ($V_{B2}$):** **negative-going spikes**: when the UJT fires, $V_{EB1}$ falls and $I_2$ momentarily increases, giving a jump across $R_2$.

{{fig p_ujt_wave|Simulated oscillator waveforms (charging is slow, discharging is very fast).|80}}

**Frequency:** the time constant $R_EC_E$ controls it. Changing $C_E$ or $R_E$ changes the frequency.

### Derivation of the frequency (from your notes), step by step

Assume the capacitor starts near 0 V and the discharge is instantaneous.

**Step 1: capacitor charging law.** $v_C=V_{BB}\left(1-e^{-t/R_EC_E}\right)$.
**Step 2: firing condition.** The capacitor fires when $v_C=V_P=\eta V_{BB}$ at time $t=T$:
$$\eta V_{BB}=V_{BB}\left(1-e^{-T/R_EC_E}\right).$$
**Step 3: cancel $V_{BB}$.** $\eta=1-e^{-T/R_EC_E}$, so $e^{-T/R_EC_E}=1-\eta$.
**Step 4: take natural logs.** $-T/R_EC_E=\ln(1-\eta)$, so
$$\boxed{T=R_EC_E\ln\frac{1}{1-\eta}=2.303\,R_EC_E\log_{10}\frac{1}{1-\eta}},\qquad\boxed{f=\frac1T}.$$

<span class="tag">extra</span> A more exact version including the valley voltage: $T=R_EC_E\ln\dfrac{V_{BB}-V_V}{V_{BB}-V_P}$. For the circuit to oscillate, $R_E$ must lie between $\dfrac{V_{BB}-V_V}{I_V}$ (large enough that the UJT can turn OFF) and $\dfrac{V_{BB}-V_P}{I_P}$ (small enough that it can turn ON).

::: ex Example 10.2: Your class problem
*A UJT has a peak potential of 20 V. It is connected across a capacitor of a series RC circuit with $R=100\ \text{k}\Omega$, $C=1000$ pF, supplied by a 40 V dc source. Find the period of the sawtooth.*

**Given:** $R_E=100\times10^{3}\ \Omega$; $C_E=1000\times10^{-12}$ F $=10^{-9}$ F; $V_P=20$ V; $V_{BB}=40$ V.

**Find:** the period $T$ (and frequency).

**Step 1: stand-off ratio.** $\eta=V_P/V_{BB}=20/40=0.5$.
**Step 2: time constant.** $R_EC_E=10^{5}\times10^{-9}=10^{-4}$ s $=100\ \mu$s.
**Step 3: formula.** $T=R_EC_E\ln\dfrac1{1-\eta}=100\ \mu\text{s}\times\ln\dfrac1{0.5}=100\ \mu\text{s}\times\ln2$.
**Step 4: number.** $\ln2=0.6931$, so $T=69.31\ \mu$s.
**Step 5: frequency.** $f=1/T=1/(69.31\times10^{-6})=14\,430$ Hz.

**Answer:** $T=\mathbf{69.3\ \mu s}$ (matches your class answer); $f\approx\mathbf{14.4\ kHz}$.

**Same via the direct equation:** $20=40(1-e^{-t/RC})$ ⇒ $e^{-t/RC}=0.5$ ⇒ $t=RC\ln2$.
:::

::: ex Example 10.3: Frequency and the oscillation condition
**Given:** $\eta=0.6$, $V_{BB}=12$ V, $R_E=47\ \text{k}\Omega$, $C_E=0.01\ \mu\text{F}$. Also $I_P=5\ \mu$A, $V_V=2$ V, $I_V=5$ mA.

**Find:** $V_P$, $T$, $f$, and check whether it oscillates.

**Step 1: peak voltage.** $V_P=\eta V_{BB}=0.6\times12=7.2$ V. (With the diode drop, $7.9$ V.)
**Step 2: time constant.** $R_EC_E=47\times10^{3}\times10\times10^{-9}=4.7\times10^{-4}$ s.
**Step 3: period.** $\ln\dfrac1{1-0.6}=\ln2.5=0.9163$, so $T=4.7\times10^{-4}\times0.9163=4.31\times10^{-4}$ s $=431\ \mu$s.
**Step 4: frequency.** $f=1/431\ \mu\text{s}=2320$ Hz.
**Step 5: check the oscillation range.**
* Upper limit: $\dfrac{V_{BB}-V_P}{I_P}=\dfrac{12-7.9}{5\times10^{-6}}=820\ \text{k}\Omega$.
* Lower limit: $\dfrac{V_{BB}-V_V}{I_V}=\dfrac{12-2}{5\times10^{-3}}=2\ \text{k}\Omega$.
* $2\ \text{k}\Omega<47\ \text{k}\Omega<820\ \text{k}\Omega$ ✓.

**Answer:** $V_P=7.2$ V, $T=431\ \mu$s, $f=2.32$ kHz; it oscillates.
:::

## 10.6 Applications

Trigger device for **SCRs and TRIACs**; non-sinusoidal (relaxation) oscillators; sawtooth generators; phase control; timing circuits.

## 10.7 Practice

::: try Questions for Chapter 10
1. Why is it called a "uni-junction" transistor?
2. Define the intrinsic stand-off ratio. What is its usual range?
3. Explain conductivity modulation and the negative resistance that results.
4. A UJT oscillator has $\eta=0.65$, $R_E=22\ \text{k}\Omega$, $C_E=0.047\ \mu\text{F}$. Find $T$ and $f$.
5. Why are the output spikes at $B_1$ and $B_2$ of opposite polarity?
6. A UJT has $R_{B1}=5\ \text{k}\Omega$, $R_{B2}=3\ \text{k}\Omega$ and $V_{BB}=16$ V. Find $\eta$ and $V_P$ (ignore $V_D$).
:::

::: soln Answers and full solutions
<details markdown="1"><summary>Solution 1</summary>

Because it has only **one PN junction** (between the P emitter and the N bar). A normal transistor has two.
</details>

<details markdown="1"><summary>Solution 2</summary>

$\eta=\dfrac{R_{B1}}{R_{B1}+R_{B2}}$: the fraction of $V_{BB}$ that appears between the emitter joint and $B_1$ when the emitter is open. Usually **0.4 to 0.85**.
</details>

<details markdown="1"><summary>Solution 3</summary>

**Step 1.** When $V_E$ exceeds $V_P$, holes are injected from the heavily doped P emitter into the lightly doped N bar.
**Step 2.** They live a long time there and move toward $B_1$, greatly increasing the number of carriers in the $B_1$ part.
**Step 3.** So $R_{B1}$ falls sharply (to about 50 Ω), and the voltage at the emitter joint falls.
**Step 4.** The emitter current therefore rises while the emitter voltage falls: $\Delta V/\Delta I<0$, negative resistance.
</details>

<details markdown="1"><summary>Solution 4</summary>

**Step 1.** $R_EC_E=22\times10^{3}\times47\times10^{-9}=1.034\times10^{-3}$ s.
**Step 2.** $\ln\dfrac1{1-0.65}=\ln\dfrac1{0.35}=\ln2.857=1.0498$.
**Step 3.** $T=1.034\ \text{ms}\times1.0498=1.086$ ms.
**Step 4.** $f=1/1.086\ \text{ms}=921$ Hz.

**Answer:** $T=1.09$ ms; $f=921$ Hz.
</details>

<details markdown="1"><summary>Solution 5</summary>

When the UJT fires, current through $B_1$ surges, so the voltage across $R_1$ jumps **up** (positive spike at $B_1$). At the same instant the emitter–$B_1$ voltage falls and the current $I_2$ through $R_2$ changes, so the voltage at $B_2$ drops (negative spike).
</details>

<details markdown="1"><summary>Solution 6</summary>

**Step 1.** $R_{BB}=5+3=8$ kΩ.
**Step 2.** $\eta=5/8=0.625$.
**Step 3.** $V_P=\eta V_{BB}=0.625\times16=10$ V.

**Answer:** $\eta=0.625$, $V_P=10$ V.
</details>
:::
