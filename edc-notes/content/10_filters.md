# Chapter 15: Filters

*Class notes pp. 32–38 · slides: L-Filter, Pi-Filter (handwritten)*

::: words
| Word / symbol | Plain meaning |
|---|---|
| Filter | circuit (capacitors, inductors) that smooths the rectifier output |
| Ripple | the leftover ac wiggle on the dc output |
| $\gamma$ | **ripple factor** $=V_{ac,rms}/V_{dc}$ (smaller is better) |
| $L$, $C$ | inductance (henry, H) and capacitance (farad, F) |
| $X_L=\omega L$ | inductive reactance: opposition of an inductor to ac (Ω) |
| $X_C=1/\omega C$ | capacitive reactance: opposition of a capacitor to ac (Ω) |
| $\omega=2\pi f$ | angular frequency (rad/s). At 50 Hz, $\omega=314.16$ |
| $f$ | frequency of the supply (50 Hz). The full-wave ripple is at $2f$ (100 Hz), i.e. $2\omega$ |
| $R_L$ | load resistance |
| $V_m$ | peak voltage of the rectified wave |
| $V_{dc}$, $I_{dc}$ | dc (average) output voltage and current |
| Fourier series | writing a repeating wave as dc + sines of frequency $\omega,2\omega,3\omega,\dots$ (harmonics) |
| Harmonic | a sine component whose frequency is a multiple of the basic frequency |
| L-filter, C-filter, LC, π (CLC) | filter shapes: series coil; shunt capacitor; coil then capacitor; capacitor–coil–capacitor |
| Choke | an inductor used as a filter |
| $R_S$, $R_f$, $R_{ch}$ | transformer secondary, diode forward and choke (coil) resistances |
| Regulation | fall in output voltage with load, $=R_{series}/R_L\times100$ |
:::

::: kid Smoothing a bumpy road
The output of a rectifier is like a road full of speed bumps: the voltage rises and falls 100 times a second. Your phone wants a smooth flat road. A **filter** is a **shock absorber**.
* A **capacitor** is a small **water tank**: it fills when the water is high and gives it back when the water is low, evening out the bumps. It lets fast wiggles pass to ground but blocks steady dc.
* An **inductor (choke)** is a heavy **flywheel**: it hates sudden changes in current, so it smooths the flow. It passes steady dc easily but resists fast changes.
:::

## 15.1 Principle

Circuits that remove the **ripple (pulsating component)** from the dc output of a rectifier are **filter circuits**. They are made from inductors and capacitors in series and parallel.

* **An inductor offers an easy path to dc but a resistive (high-reactance) path to ac:** $X_L=\omega L$ grows with frequency.
* **A capacitor offers a resistive path to dc but an easy path to ac:** $X_C=\dfrac1{\omega C}$ falls with frequency.

So: **inductor in series** with the load, **capacitor in parallel** (shunt) with the load. Types in your slide: **series inductor (L) filter**, **shunt capacitor filter**, **choke-input (L-section / LC) filter**, **capacitor-input (π-section, CLC) filter**.

{{fig p_filter_waves|What each filter does to the rectified wave (dashed = raw rectifier output).|92}}

## 15.2 Fourier series of the rectifier output (why the ripple has a fixed pattern)

Any repeating wave equals a dc term plus sine/cosine terms: $f(t)=a_0+\sum(a_n\cos n\omega t+b_n\sin n\omega t)$. From your class notes:

**Half-wave** output:
$$V_o=\frac{V_m}{\pi}+\frac{V_m}{2}\sin\omega t-\frac{2V_m}{\pi}\sum_{k=2,4,6,\dots}\frac{\cos k\omega t}{(k+1)(k-1)}$$
= a "battery" $V_m/\pi$ in series with an ac source $\frac{V_m}{2}\sin\omega t$ plus higher harmonics.

**Full-wave** output:
$$V_o=\frac{2V_m}{\pi}-\frac{4V_m}{\pi}\sum_{k=2,4,6,\dots}\frac{\cos k\omega t}{(k+1)(k-1)}=\frac{2V_m}{\pi}-\frac{4V_m}{3\pi}\cos2\omega t-\frac{4V_m}{15\pi}\cos4\omega t-\cdots$$
(check $k=2$: $(k+1)(k-1)=3$; $k=4$: $15$.)

**The biggest ripple in a full-wave rectifier is the second harmonic ($2\omega$); the $4\omega$ and higher terms are much smaller.** So a filter only has to deal with $2\omega$.

## 15.3 Series inductor (L) filter

{{fig c_filter_l|Series inductor filter.|85}}

### Half-wave rectifier with an L-filter
* When the current tends to **rise**, the inductor **opposes the growth** and stores the extra energy in its **magnetic field**.
* When the current tends to **fall**, it **opposes the decay** and returns stored energy.
* So current flows through $R_L$ for a **longer part of the cycle**: the diode conducts for $\pi+\theta$ instead of $\pi$ ($\theta$ is an extra angle), and the load current is smoother.
* Impedance for the ac component: $Z=\sqrt{R_L^2+\omega^2L^2}$. For dc ($\omega=0$): $Z=R_L$. The high ac impedance blocks the ac and passes the dc.

### Full-wave rectifier with an L-filter: ripple factor (class derivation)

Let the rectified wave have peak $E_0$ ($=V_m$).

**Step 1: dc part.** $E_{dc}=\dfrac{2E_0}{\pi}$, so $\boxed{I_{dc}=\dfrac{2E_0}{\pi R_L}}$. (The inductor has no resistance for dc.)
**Step 2: keep only the $2\omega$ term.** Its amplitude is $\dfrac{4E_0}{3\pi}$. Its impedance is $Z_2=\sqrt{R_L^2+(2\omega L)^2}$. So the peak ac current is
$$I_{peak}=\frac{4E_0/(3\pi)}{\sqrt{R_L^2+4\omega^2L^2}}.$$
**Step 3: rms of the ac current.** $I_{rms}=\dfrac{I_{peak}}{\sqrt2}=\dfrac{4E_0}{3\pi\sqrt2\sqrt{R_L^2+4\omega^2L^2}}$.
**Step 4: ratio.** $\gamma=\dfrac{I_{rms}}{I_{dc}}=\dfrac{4E_0}{3\pi\sqrt2\,Z_2}\times\dfrac{\pi R_L}{2E_0}$ (the $E_0$ and $\pi$ cancel):
$$\boxed{\gamma=\frac{2}{3\sqrt2}\frac{R_L}{\sqrt{R_L^2+4\omega^2L^2}}=\frac{\sqrt2}{3}\left[1+\frac{4\omega^2L^2}{R_L^2}\right]^{-1/2}}.$$
**Step 5: two limits.**
* $R_L\gg2\omega L$: the bracket $\to1$, so $\gamma\to\dfrac{\sqrt2}{3}=0.47$ (your slide says about 0.48): **the same as no filter**. An L-filter works poorly for a large $R_L$ (light load).
* $2\omega L\gg R_L$: $\gamma\to\dfrac{\sqrt2}{3}\cdot\dfrac{R_L}{2\omega L}=\boxed{\dfrac{R_L}{3\sqrt2\,\omega L}}$. A **bigger $L$ gives a smaller ripple**.

::: ex Example 15.1: Your class problem (full-wave rectifier with L-filter)
*A full-wave rectifier uses a 50-0-50 V transformer and diodes with internal resistance 25 Ω. An inductor $L=4$ H with dc resistance 20 Ω is in series with the load $R_L=750\ \Omega$. Line frequency 50 Hz, secondary resistance 50 Ω. Calculate the ripple factor, (i) dc output voltage, (ii) ac output voltage, and the % regulation.*

**Given:** 50-0-50 V (each half 50 V rms), $R_f=25\ \Omega$, $L=4$ H, $R_{ind}=20\ \Omega$, $R_L=750\ \Omega$, $f=50$ Hz, $R_{sec}=50\ \Omega$.

**Step 1: angular frequency.** $\omega=2\pi f=2\pi\times50=314.16$ rad/s.
**Step 2: check which limit applies.** $2\omega L=2\times314.16\times4=2513\ \Omega\gg R_L=750\ \Omega$ ✓ (so use the simple formula).
**Step 3: ripple factor.** $\gamma=\dfrac{R_L}{3\sqrt2\,\omega L}=\dfrac{750}{3\times1.4142\times314.16\times4}=\dfrac{750}{5331.6}=0.1407$.
(The exact formula gives 0.135.)
**Step 4: peak voltage of each half.** $V_m=50\sqrt2=70.7$ V. The ideal dc output would be $\dfrac{2V_m}{\pi}=\dfrac{2\times70.7}{3.1416}=45.0$ V.
**Step 5: series resistance in the current path.** Only half the secondary and one diode carry current at a time: $R=\dfrac{R_{sec}}{2}+R_f+R_{ind}=\dfrac{50}{2}+25+20=70\ \Omega$.
**Step 6: (i) dc output.** The dc current flows through $R$ and $R_L$: $I_{dc}=\dfrac{2V_m/\pi}{R+R_L}$, so $V_{dc}=I_{dc}R_L=\dfrac{2V_m/\pi}{1+R/R_L}=\dfrac{45.0}{1+70/750}=\dfrac{45.0}{1.0933}=41.2$ V.
**Step 7: (ii) ac output.** $V_{ac,rms}=\gamma V_{dc}=0.1407\times41.2=5.8$ V.
**Step 8: regulation.** $\dfrac{R}{R_L}\times100=\dfrac{70}{750}\times100=9.33\%$.

**Answer:** $\gamma=0.141$; $V_{dc}=41.2$ V; $V_{ac}=5.8$ V (class 5.75 V from rounding); regulation $=9.33\%$.
:::

::: flag Class notation slip
Page 37 writes $X_{L1}=\frac{1}{2\omega L_1}$ and $X_{L2}=\frac1{2\omega L_2}$ next to the π-filter. Those are the **capacitive** reactances $X_{C1}=\dfrac1{2\omega C_1}$ and $X_{C2}=\dfrac1{2\omega C_2}$. The inductive reactance is $X_L=2\omega L$. (The factor 2 is because the ripple is at $2\omega$.)
:::

## 15.4 Shunt capacitor filter (C filter)

{{fig c_filter_c|Capacitor filter: capacitor in parallel with the load.|85}}

The capacitor charges up to the peak while the rectifier voltage is rising, then discharges slowly through $R_L$ when the rectifier voltage falls below the capacitor voltage. The diodes conduct only for a short time near each peak.

$$\boxed{\gamma=\frac{1}{4\sqrt3\,fCR_L}}\ \text{(full-wave)}\qquad f=50\text{ Hz}:\ \gamma=\frac{2890}{C\,R_L}\ (C\text{ in }\mu\text{F},\ R_L\text{ in }\Omega)$$

**Derivation sketch** <span class="tag">extra</span>:
**Step 1.** Between peaks (time $1/2f$) the capacitor loses charge $I_{dc}/(2f)$. So the peak-to-peak ripple is $V_r=\dfrac{I_{dc}}{2fC}$.
**Step 2.** Treat the ripple as a triangular (sawtooth) wave: its rms value is $\dfrac{V_r}{2\sqrt3}$.
**Step 3.** With $V_{dc}\approx I_{dc}R_L$: $\gamma=\dfrac{V_r/(2\sqrt3)}{V_{dc}}=\dfrac{I_{dc}/(2fC)}{2\sqrt3\,I_{dc}R_L}=\dfrac{1}{4\sqrt3\,fCR_L}$.

* Larger $C$ or larger $R_L$ (lighter load) → smaller ripple. Regulation is poor (the dc voltage drops as load current rises).
* Your class note beside it says this one gives higher dc output than the L filter ("more efficient").

::: ex Example 15.2: Capacitor filter
**Given:** $C=1000\ \mu$F, $R_L=100\ \Omega$, $f=50$ Hz, full-wave.

**Find:** the ripple factor.

**Step 1.** $4\sqrt3=6.928$.
**Step 2.** $fCR_L=50\times1000\times10^{-6}\times100=5$.
**Step 3.** $\gamma=\dfrac{1}{6.928\times5}=\dfrac1{34.64}=0.0289$.
**Check with the shortcut:** $\dfrac{2890}{1000\times100}=0.0289$ ✓.

**Answer:** $\gamma=\mathbf{0.029}$ (2.9 %).

**Second part:** full-wave rectifier, $C=470\ \mu$F, $I_{dc}=100$ mA, $V_m=20$ V. Then $V_{dc}\approx V_m-\dfrac{I_{dc}}{4fC}=20-\dfrac{0.1}{4\times50\times470\times10^{-6}}=20-\dfrac{0.1}{0.094}=20-1.06=\mathbf{18.9\ V}$.
:::

## 15.5 L-section (choke-input, LC) filter

{{fig c_filter_lc|L-section filter: series choke, then shunt capacitor.|85}}

Uses both parts: the inductor first blocks most of the ac, then the capacitor bypasses what got through.
$$\boxed{\gamma=\frac{\sqrt2}{3}\cdot\frac{1}{4\omega^2LC}}\qquad f=50\text{ Hz}:\ \gamma=\frac{1.194}{LC}\quad(L\text{ in H},\ C\text{ in }\mu\text{F})$$

::: ex Example 15.3: LC filter
**Given:** $L=5$ H, $C=100\ \mu$F, 50 Hz.

**Step 1: shortcut formula.** $\gamma=\dfrac{1.194}{LC}=\dfrac{1.194}{5\times100}=0.00239$.
**Step 2: check with the full formula.** $\omega^2=314.16^2=98\,696$; $4\omega^2LC=4\times98\,696\times5\times100\times10^{-6}=197.4$; $\dfrac{\sqrt2}{3}\times\dfrac1{197.4}=0.4714\times0.005066=0.00239$ ✓.

**Answer:** $\gamma=\mathbf{0.0024}$ (0.24 %): very small.
:::

## 15.6 Capacitor-input (π-section, CLC) filter

{{fig c_filter_pi|π filter: $C_1$, then $L$, then $C_2$ (shaped like the Greek letter π).|92}}

* It is the **L-section plus a capacitor filter**. It is used when a **higher dc voltage** than the L-section gives is needed, and it gives **very good ripple rejection**. It suits **low output current**.
* **Role of each part** (your Pi-Filter notes):
  * **$C_1$:** low reactance to the ac part of the rectifier output, blocks dc: it bypasses part of the ac to ground and passes dc on to $L$.
  * **$L$:** very high reactance to ac, low to dc: it opposes the ac and passes the dc.
  * **$C_2$:** bypasses the ac that the inductor could not stop, so almost pure dc reaches $R_L$.
* The output waveform is very nearly flat.

### Ripple-factor derivation (your handwritten notes), step by step

**Step 1: output of $C_1$.** From the capacitor filter: $V_{C1}=V_{dc}-\dfrac{V_r}{\pi}\sin2\omega t-\cdots$, where $V_r$ is the peak-to-peak ripple. Neglecting the higher harmonics, and using $V_r=\dfrac{I_{dc}}{2fC_1}$:
$$V_{C1}=V_{dc}-\frac{I_{dc}}{2\pi fC_1}\sin2\omega t.$$
The second term is the ac component.
**Step 2: its rms value.** $V_{ac,rms}\big|_{C1}=\dfrac{I_{dc}}{2\pi fC_1}\cdot\dfrac1{\sqrt2}$. With $X_{C1}=\dfrac{1}{2\omega C_1}=\dfrac{1}{4\pi fC_1}$, this equals $\sqrt2\,I_{dc}X_{C1}$.
**Step 3: divide the ripple between $L$ and $C_2$.** The ripple from $C_1$ drives a divider: $L$ in series, $C_2$ to ground. Output ripple $=\text{input ripple}\times\dfrac{X_{C2}}{X_L+X_{C2}}$ ($X_L$ is $2\omega L$ and $X_{C2}$ is $\dfrac1{2\omega C_2}$):
$$V_{ac,out}=\sqrt2\,I_{dc}X_{C1}\,\frac{X_{C2}}{X_L+X_{C2}}.$$
**Step 4: ripple factor.** Divide by $V_{dc}=I_{dc}R_L$:
$$\boxed{\gamma=\sqrt2\,\frac{X_{C1}X_{C2}}{R_L\,(X_L+X_{C2})}}.$$
**Step 5: simplify.** Usually $X_L\gg X_{C2}$, so
$$\gamma=\sqrt2\frac{X_{C1}X_{C2}}{R_LX_L}=\sqrt2\cdot\frac{1}{2\omega C_1}\cdot\frac{1}{2\omega C_2}\cdot\frac{1}{2\omega L}\cdot\frac1{R_L}=\boxed{\frac{\sqrt2}{8\omega^3LC_1C_2R_L}}.$$
**Step 6: output dc voltage.**
$$V_{dc}=V_m-\frac{I_{dc}}{4fC_1}-I_{dc}(R_S+R_f+R_{choke}).$$
($R_f$ = diode forward resistance, $R_S$ = transformer secondary winding resistance, $R_{choke}$ = resistance of the choke.)

::: ex Example 15.4: π filter
**Given:** $C_1=C_2=100\ \mu$F, $L=5$ H, $R_L=1\ \text{k}\Omega$, 50 Hz.

**Step 1: $\omega$.** $\omega=314.16$ rad/s.
**Step 2: capacitive reactances.** $X_C=\dfrac1{2\omega C}=\dfrac1{2\times314.16\times100\times10^{-6}}=\dfrac{1}{0.06283}=15.9\ \Omega$ (same for both).
**Step 3: inductive reactance.** $X_L=2\omega L=2\times314.16\times5=3141.6\ \Omega$.
**Step 4: formula.** $\gamma=\dfrac{\sqrt2\,X_{C1}X_{C2}}{R_L(X_L+X_{C2})}=\dfrac{1.4142\times15.9\times15.9}{1000\times(3141.6+15.9)}=\dfrac{357.5}{3.1575\times10^{6}}=1.13\times10^{-4}$.

**Answer:** $\gamma=1.13\times10^{-4}$ (0.011 %): nearly pure dc.
:::

## 15.7 Comparison

| Filter | Ripple factor $\gamma$ | Good for | Weak point |
|---|---|---|---|
| none (FWR) | 0.482 | – | large ripple |
| L (series inductor) | $\dfrac{R_L}{3\sqrt2\,\omega L}$ | **heavy load (small $R_L$)**; bigger $L$ gives smaller $\gamma$ | useless for large $R_L$ |
| C (shunt capacitor) | $\dfrac{1}{4\sqrt3fCR_L}$ | **light load (large $R_L$)** | poor regulation |
| LC (L-section) | $\dfrac{\sqrt2}{3}\dfrac1{4\omega^2LC}$ (no $R_L$ in it) | wide load range | bulky choke |
| π (CLC) | $\dfrac{\sqrt2}{8\omega^3LC_1C_2R_L}$ | high dc voltage, lowest ripple | low output current; poor regulation |

## 15.8 Practice (including the assignment in your Filters deck)

::: try Questions for Chapter 15
1. What is a filter circuit? Explain (i) the L-filter and (ii) the π-section filter and give the ripple factor for each.
2. Define (i) ripple factor and (ii) rectification efficiency.
3. A full-wave rectifier has $V_m=30$ V (each half), $R_L=200\ \Omega$ and a C filter with $C=2200\ \mu$F at 50 Hz. Find the ripple factor and the approximate dc output (ignore diode drop).
4. Why does an L-filter not help when $R_L$ is very large?
5. An LC filter uses $C=470\ \mu$F. Find $L$ for $\gamma=0.5\%$ at 50 Hz.
6. A π filter uses $C_1=C_2=220\ \mu$F, $L=2$ H, $R_L=500\ \Omega$ at 50 Hz. Find $\gamma$.
:::

::: soln Answers and full solutions
<details markdown="1"><summary>Solution 1</summary>

**Filter circuit:** a circuit of inductors/capacitors that removes the ripple from the rectifier output.
**(i) L-filter:** series inductor. $X_L=\omega L$ is large for ac, zero for dc, so ac is blocked and dc passes. $\gamma=\dfrac{2}{3\sqrt2}\dfrac{R_L}{\sqrt{R_L^2+4\omega^2L^2}}\approx\dfrac{R_L}{3\sqrt2\,\omega L}$ (§15.3).
**(ii) π-filter:** $C_1$ bypasses ac, $L$ blocks ac, $C_2$ bypasses the remainder. $\gamma=\dfrac{\sqrt2}{8\omega^3LC_1C_2R_L}$ (§15.6).
</details>

<details markdown="1"><summary>Solution 2</summary>

* Ripple factor $\gamma=\dfrac{\text{rms of the ac component}}{\text{dc value}}$.
* Efficiency $\eta=\dfrac{\text{dc output power}}{\text{ac input power}}$.
</details>

<details markdown="1"><summary>Solution 3</summary>

**Formula:** $\gamma=\dfrac{1}{4\sqrt3\,fCR_L}$.
**Step 1.** $C=2200\ \mu\text{F}=2.2\times10^{-3}$ F.
**Step 2.** $fCR_L=50\times2.2\times10^{-3}\times200=22$.
**Step 3.** $4\sqrt3=6.928$; $\gamma=\dfrac{1}{6.928\times22}=\dfrac{1}{152.4}=0.00656$.

**dc output:** $V_{dc}=V_m-\dfrac{I_{dc}}{4fC}$ with $I_{dc}=V_{dc}/R_L$.
**Step 4.** $\dfrac{1}{4fCR_L}=\dfrac{1}{4\times50\times2.2\times10^{-3}\times200}=\dfrac1{88}=0.01136$.
**Step 5.** $V_{dc}=30-0.01136\,V_{dc}$, so $V_{dc}(1.01136)=30$ and $V_{dc}=29.66$ V.

**Answer:** $\gamma=0.0066$ (0.66 %); $V_{dc}\approx29.7$ V.
</details>

<details markdown="1"><summary>Solution 4</summary>

For large $R_L$ the ratio $R_L/(2\omega L)$ is large, so the inductor's ac impedance is negligible compared with $R_L$. Then $\gamma\to\sqrt2/3=0.47$, about the same as with no filter. The choke helps only when $2\omega L\gg R_L$.
</details>

<details markdown="1"><summary>Solution 5</summary>

**Formula:** $\gamma=\dfrac{1.194}{LC}$ ($L$ in H, $C$ in µF).
**Step 1.** $\gamma=0.5\%=0.005$.
**Step 2.** $L=\dfrac{1.194}{\gamma C}=\dfrac{1.194}{0.005\times470}=\dfrac{1.194}{2.35}=0.508$ H.

**Answer:** about **0.51 H**.
</details>

<details markdown="1"><summary>Solution 6</summary>

**Step 1.** $\omega=314.16$.
**Step 2.** $X_C=\dfrac1{2\omega C}=\dfrac1{2\times314.16\times220\times10^{-6}}=\dfrac1{0.13823}=7.23\ \Omega$.
**Step 3.** $X_L=2\omega L=2\times314.16\times2=1256.6\ \Omega$.
**Step 4.** $\gamma=\dfrac{\sqrt2X_{C1}X_{C2}}{R_L(X_L+X_{C2})}=\dfrac{1.4142\times7.23^2}{500\times(1256.6+7.23)}=\dfrac{73.9}{500\times1263.8}=\dfrac{73.9}{631\,900}$.
**Step 5.** $\gamma=1.17\times10^{-4}$.

**Answer:** **$1.17\times10^{-4}$** (0.0117 %).
</details>
:::
