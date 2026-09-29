# Chapter 10: Unijunction transistor (UJT) and the relaxation oscillator

*Class notes pp. 8–10 · slides: UJT and Photodiode; scan “EDC UJT” (oscillator notes)*

::: kid The see-saw that flips when the water reaches the top
Fill a bucket slowly from a tap. When the water reaches a **certain level**, the bucket tips over and empties in a flash. Then it starts filling again. Fill, flip, fill, flip: that is a **relaxation oscillator**. In electronics the “bucket” is a **capacitor** filling through a resistor. The “tipping” is done by the **UJT**: it stays off until the capacitor voltage reaches the **peak-point voltage $V_P$**, then suddenly turns on and dumps the capacitor’s charge. This makes a saw-tooth wave and sharp pulses.
:::

## 10.1 What it is

* A **three-terminal** device with **only one PN junction**, hence “uni-junction”. Terminals: **Emitter (E)**, **Base 1 ($B_1$)**, **Base 2 ($B_2$)**.
* It shows a **negative-resistance** characteristic, which makes it useful in oscillator circuits.
* Highly doped emitter region on a **lightly doped** N-type silicon bar.

{{fig p_ujt_struct|UJT: a lightly-doped N bar with two base contacts and one heavily-doped P emitter joint.|72}}

* The N-type silicon bar (very lightly doped) acts as the base; ohmic contacts $B_1$ and $B_2$ at its ends. A **P-type impurity** introduced into the bar makes a single PN junction: the **emitter**, which behaves like an ordinary diode.
* A **complementary UJT** has a P-type bar and N-type emitter; same behaviour with opposite polarities.

{{fig c_ujt_symbol|UJT symbol: the arrow on the emitter points toward the bar.|30}}

## 10.2 Equivalent circuit and intrinsic stand-off ratio

{{fig c_ujt_equiv|Equivalent circuit: two resistances $R_{B2}$ and $R_{B1}$ forming a voltage divider, with the emitter diode connected to their junction A.|55}}

* With the emitter open, the resistance from $B_2$ to $B_1$ is just the silicon bar: the **inter-base resistance**
$$R_{BB}=R_{B1}+R_{B2},\qquad\text{typically }5\text{ to }10\ \text{k}\Omega\ (\text{high because the bar is lightly doped}).$$
* $R_{B2}$ is between $B_2$ and point A; $R_{B1}$ between A and $B_1$. The junction is formed so that (class notes)
$$\frac{R_{B1}}{R_{B2}}=\frac23$$
* $V_{BB}$ is applied between $B_2$ (positive) and $B_1$. With $I_E=0$, $I_1=I_2=V_{BB}/R_{BB}$.
* The voltage at A is
$$V_A=V_{BB}\frac{R_{B1}}{R_{B1}+R_{B2}}=\eta V_{BB}$$
where
$$\boxed{\eta=\frac{R_{B1}}{R_{B1}+R_{B2}}}$$
is the **intrinsic stand-off ratio**: a property of the UJT, **always less than 1, usually 0.4 to 0.85**. With $R_{B1}/R_{B2}=2/3$: $\eta=\tfrac{2}{5}=0.4$.

::: ex Example 10.1
$R_{B1}=4$ kΩ, $R_{B2}=6$ kΩ: $R_{BB}=10$ kΩ, $\eta=4/10=\mathbf{0.4}$ (this is the $2/3$ ratio). With $V_{BB}=20$ V the divider point is at $V_A=\eta V_{BB}=8$ V.
:::

## 10.3 Working

1. The emitter diode is **reverse biased** as long as $V_E<\eta V_{BB}$ (plus the diode drop). Only leakage flows: the UJT is **off** (cut-off region).
2. When $V_E$ reaches the **peak-point voltage**
$$V_P=\eta V_{BB}+V_D\qquad(V_D\approx0.7\text{ V})$$
the diode turns on (forward biased) and the emitter current starts to flow. This current is the **peak-point current** $I_P$.
3. **Holes** are injected from the heavily doped P emitter into the lightly doped N bar. They have a long lifetime there and drift toward $B_1$, so the number of carriers in the $B_1$ part **increases a lot**: the resistance $R_{B1}$ **collapses** (down to about **50 Ω**). This process is **conductivity modulation**.
4. Since $R_{B1}$ falls, the voltage at A falls, holding the diode on with **more current but lower emitter voltage**: **negative resistance**.

::: flag Two forms of $V_P$ in your material
The class notes write $V_P=\eta V_{BB}$ (neglecting the emitter diode drop). The UJT slides write $V_P=V_D+\eta V_{BB}$ and say the UJT turns on when $V_E$ exceeds $\eta V_{BB}$ by 0.7 V. They agree if you regard $V_D$ as small. **Use $V_P=\eta V_{BB}$ (class) unless the question gives $V_D$.**
:::

## 10.4 Emitter characteristic

{{fig p_ujt_iv|Emitter voltage vs emitter current for a UJT at fixed $V_{BB}$.|72}}

* **Cut-off region** ($0\le V_E<V_P$): only leakage emitter current.
* **Negative-resistance region:** after the **peak point** $(I_P,V_P)$, $I_E$ increases while $V_E$ **decreases**, down to the **valley point** $(I_V,V_V)$.
* **Saturation region** (beyond the valley): $I_E$ and $V_E$ increase together; positive resistance again. $R_{B1}$ here can be as low as about 50 Ω.

## 10.5 UJT as a relaxation oscillator

{{fig c_ujt_osc|UJT relaxation oscillator: $R_E$ charges $C_E$; $R_1$ and $R_2$ give the output pulses at $B_1$ and $B_2$.|60}}

**Circuit:** the supply $V_{BB}$ charges the capacitor $C_E$ through the variable resistor $R_E$. The UJT’s emitter is connected to the capacitor. Small resistors $R_2$ (in series with $B_2$) and $R_1$ (in series with $B_1$) give the output spikes. It is meant for generating a **saw-tooth** waveform.

**Cycle:**
1. When $V_{BB}$ is switched on, $C_E$ charges **exponentially** through $R_E$.
2. When the capacitor voltage reaches $V_P$, the UJT fires (conducts).
3. $C_E$ **discharges rapidly** through $E$–$B_1$ and $R_1$. The UJT gives negative resistance for the discharge path.
4. When the capacitor voltage falls to (about) the valley voltage, the UJT switches off and the capacitor starts charging again.
5. The cycle repeats: **saw-tooth across $C_E$** (charging slowly, discharging quickly).

**Output waveforms:**
* **Across $C_E$ (emitter):** saw-tooth between $V_V$ and $V_P$.
* **At $B_1$ ($V_{B1}$):** **positive-going spikes**: the sudden surge of current through $B_1$ causes a drop across $R_1$.
* **At $B_2$ ($V_{B2}$):** **negative-going spikes**: when the UJT fires, $V_{EB1}$ falls and $I_2$ increases rapidly, so the drop across $R_2$ jumps.

{{fig p_ujt_wave|Simulated oscillator waveforms (charging is slow, discharging is very fast).|80}}

**Frequency:** the time constant $R_EC_E$ controls it. Changing $C_E$ or $R_E$ changes the frequency.

### Derivation (from your notes)

While charging (assuming $C_E$ starts near 0 V and the discharge is instantaneous):
$$v_C=V_{BB}\left(1-e^{-t/R_EC_E}\right)$$
The capacitor fires when $v_C=V_P=\eta V_{BB}$:
$$\eta V_{BB}=V_{BB}\left(1-e^{-T/R_EC_E}\right)\ \Rightarrow\ e^{-T/R_EC_E}=1-\eta$$
$$\boxed{T=R_EC_E\ln\frac{1}{1-\eta}=2.303\,R_EC_E\log_{10}\frac{1}{1-\eta}},\qquad\boxed{f_0=\frac1T=\frac{1}{2.303R_EC_E\log_{10}\!\left(\frac1{1-\eta}\right)}}$$

<span class="tag">extra</span> A more accurate expression that includes the valley voltage: $T=R_EC_E\ln\dfrac{V_{BB}-V_V}{V_{BB}-V_P}$. For oscillation, $R_E$ must satisfy $\dfrac{V_{BB}-V_V}{I_V}<R_E<\dfrac{V_{BB}-V_P}{I_P}$ (large enough that the UJT can turn off, small enough that it can turn on).

::: ex Example 10.2 (your class problem)
*A UJT has a peak potential of 20 V. It is connected across a capacitor of a series RC circuit with $R=100\ \text{k}\Omega$, $C=1000$ pF, supplied by a source of 40 V dc. Find the time period of the sawtooth.*

$R_E=100\times10^3\ \Omega$, $C_E=1000\times10^{-12}$ F, $V_P=20$ V, $V_{BB}=40$ V, so $\eta=V_P/V_{BB}=0.5$.
$$20=40\left(1-e^{-t/R_EC_E}\right)\Rightarrow e^{-t/RC}=0.5\Rightarrow t=RC\ln2$$
$$T=10^{5}\times10^{-9}\times0.6931=\mathbf{69.3\ \mu s},\qquad f=\frac1T\approx\mathbf{14.4\ kHz}$$
(matches your class answer 69.3 µs).
:::

::: ex Example 10.3
$\eta=0.6$, $V_{BB}=12$ V, $R_E=47\ \text{k}\Omega$, $C_E=0.01\ \mu$F.
$V_P=0.6\times12=7.2$ V (or 7.9 V with $V_D=0.7$ V).
$T=47\text{k}\times10\text{nF}\times\ln(1/0.4)=4.7\times10^{-4}\times0.916=\mathbf{431\ \mu s}$ → $f=\mathbf{2.32\ kHz}$.

Check the oscillation condition with $I_P=5\ \mu$A, $V_V=2$ V, $I_V=5$ mA: $R_E<(12-7.9)/5\ \mu\text{A}=820\ \text{k}\Omega$ and $R_E>(12-2)/5\ \text{mA}=2\ \text{k}\Omega$. Since $2\text{k}<47\text{k}<820\text{k}$, it oscillates.
:::

## 10.6 Applications

Trigger device for **SCRs and TRIACs**, non-sinusoidal (relaxation) oscillators, sawtooth generators, phase control, timing circuits.

## 10.7 Try it yourself

::: try Chapter 10 questions
1. Why is it called a “uni-junction” transistor?
2. Define intrinsic stand-off ratio. Typical range?
3. Explain conductivity modulation and the resulting negative resistance.
4. UJT: $\eta=0.65$, $R_E=22$ kΩ, $C_E=0.047\ \mu$F. Find $T$ and $f$.
5. Why are the outputs at $B_1$ and $B_2$ spikes of opposite polarity?

<details markdown="1"><summary>Answers</summary>

1. It has only one PN junction (the emitter–bar junction).
2. $\eta=R_{B1}/(R_{B1}+R_{B2})$; 0.4–0.85.
3. Above $V_P$ holes are injected from the P emitter into the lightly doped N bar; they lower $R_{B1}$ sharply, so the emitter voltage falls even though the current rises: negative resistance.
4. $T=22\text{k}\times47\text{n}\times\ln(1/0.35)=1.034\text{ ms}\times1.0498=\mathbf{1.086\ ms}$, $f=\mathbf{921\ Hz}$.
5. At firing the current through $B_1$ surges (positive spike across $R_1$), while $V_{EB1}$ falls and $I_2$ momentarily changes, giving a negative spike across $R_2$.
</details>
:::
