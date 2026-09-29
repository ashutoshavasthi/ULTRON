# Chapter 15: Filters

*Class notes pp. 32–38 · slides: L-Filter, Pi-Filter (handwritten)*

::: kid Smoothing a bumpy road
The output of a rectifier is like a road full of speed bumps: the voltage goes up and down 100 times every second. Your phone or radio wants a smooth flat road. A **filter** is a **shock absorber**:
* A **capacitor** is like a small **water tank**: it fills up when the water is high and gives water back when the water is low, evening out the bumps. (It lets fast wiggles pass to ground but blocks steady dc.)
* An **inductor (choke)** is like a heavy **flywheel**: it hates sudden changes in current, so it smooths the flow. (It passes steady dc easily but resists fast ac.)
:::

## 15.1 Principle

The circuits that remove the **ripple (pulsating component)** from the dc output of a rectifier are **filter circuits**. They are made from inductors and capacitors connected in series and parallel.

* **An inductor offers an easy path to dc but a resistive (high-reactance) path to ac:** $X_L=\omega L$ grows with frequency.
* **A capacitor offers a resistive path to dc but an easy path to ac:** $X_C=\dfrac1{\omega C}$ falls with frequency.

So: **inductor in series** with the load, **capacitor in parallel** with the load. Types in your slide: **series inductor (L) filter**, **shunt capacitor filter**, **choke-input (L-section / LC) filter**, **capacitor-input (π-section, CLC) filter**.

{{fig p_filter_waves|What each filter does to the rectified wave (dashed = raw rectifier output).|92}}

## 15.2 Fourier series of the rectifier output (why ripple has a fixed pattern)

Any periodic wave is a sum of a dc term and sine/cosine terms: $f(t)=a_0+\sum(a_n\cos n\omega t+b_n\sin n\omega t)$. Your class notes give:

**Half-wave** output:
$$V_o=\frac{V_m}{\pi}+\frac{V_m}{2}\sin\omega t-\frac{2V_m}{\pi}\sum_{k=2,4,6,\dots}\frac{\cos k\omega t}{(k+1)(k-1)}$$
= a battery $V_m/\pi$ (dc) in series with an ac source $\frac{V_m}2\sin\omega t$ + higher harmonics.

**Full-wave** output:
$$V_o=\frac{2V_m}{\pi}-\frac{4V_m}{\pi}\sum_{k=2,4,6,\dots}\frac{\cos k\omega t}{(k+1)(k-1)}=\frac{2V_m}{\pi}-\frac{4V_m}{3\pi}\cos2\omega t-\frac{4V_m}{15\pi}\cos4\omega t-\cdots$$
(equivalent to a battery $2V_m/\pi$ in series with an ac source $-\frac{4V_m}{3\pi}\cos2\omega t$). **The biggest ripple is the second harmonic ($2\omega$); harmonics $4\omega$ and higher are small.** So a filter only needs to deal with $2\omega$.

## 15.3 Series inductor (L) filter

### Half-wave rectifier with an L-filter

{{fig c_filter_l|Series inductor filter: the inductor in series with the load.|85}}

* When the current tends to **increase**, the inductor **opposes the growth** and stores the excess energy in its **magnetic field**.
* When the current tends to **decrease**, it **opposes the decay** and returns stored energy.
* Result: the current flows through $R_L$ for a **longer part of the cycle**. The diode conducts for $\pi+\theta$ instead of $\pi$ (θ is the extra angle) and the load current is smoother.
* Impedance for the ac component: $Z_L=\left[R_L^2+\omega^2L^2\right]^{1/2}$; for dc ($\omega=0$): $Z_L=R_L$. The high ac impedance blocks the ac component and lets the dc through.
* The **time constant** of the circuit is $L/R$.

### Full-wave rectifier with an L-filter: ripple factor (class derivation)

With $E=E_0\sin\omega t$ across the secondary:

1. DC term: $E_{dc}=\dfrac{2E_0}{\pi}$, so $\boxed{I_{dc}=\dfrac{E_{dc}}{R_L}=\dfrac{2E_0}{\pi R_L}}$.
2. Only the $2\omega$ term matters: amplitude $\dfrac{4E_0}{3\pi}$ across $Z=\sqrt{R_L^2+(2\omega L)^2}$:
$$I_{peak}=\frac{4E_0/3\pi}{\sqrt{R_L^2+(2\omega L)^2}},\qquad I_{rms}=\frac{I_{peak}}{\sqrt2}=\frac{4E_0}{3\pi\sqrt2\sqrt{R_L^2+4\omega^2L^2}}$$
3. Ripple factor $\gamma=I_{rms}/I_{dc}$:
$$\boxed{\gamma=\frac{2}{3\sqrt2}\,\frac{R_L}{\sqrt{R_L^2+4\omega^2L^2}}=\frac{\sqrt2}{3}\left[1+\frac{4\omega^2L^2}{R_L^2}\right]^{-1/2}}$$
4. Two limits:
   * $R_L\gg2\omega L$: $\gamma\to\dfrac{\sqrt2}{3}=0.47$ (about 0.48), about the same as **no filter**: the inductor does nothing if the load is light. **An L-filter works poorly for a large $R_L$ (light load).**
   * $2\omega L\gg R_L$: $\gamma\to\dfrac{\sqrt2}{3}\cdot\dfrac{R_L}{2\omega L}=\boxed{\dfrac{R_L}{3\sqrt2\,\omega L}}$. **A bigger $L$ gives a smaller ripple.**

(The same result appears in the other class derivation using $I_{rms}=\dfrac{\sqrt2V_m}{3\pi\omega L}$ and $I_{dc}=\dfrac{2V_m}{\pi R_L}$.)

::: ex Example 15.1 (your class problem: FWR + L filter)
*A FWR uses a 50-0-50 V transformer and diodes having internal resistance 25 Ω. An inductor $L=4$ H with dc resistance 20 Ω is connected in series with the load $R_L=750\ \Omega$. The line frequency is 50 Hz and the secondary resistance is 50 Ω. Calculate the ripple factor, (i) dc output voltage, (ii) ac output voltage, and the % regulation.*

$\omega=2\pi f=100\pi=314.16$ rad/s. Ripple factor (using $2\omega L\gg R_L$: $2\omega L=2513\ \Omega$):
$$\gamma=\frac{R_L}{3\sqrt2\,\omega L}=\frac{750}{3\sqrt2\times100\pi\times4}=\frac{750}{5331.6}=\mathbf{0.1406}$$
(The exact formula $\frac{2}{3\sqrt2}\frac{R_L}{\sqrt{R_L^2+4\omega^2L^2}}$ gives 0.135. Use the approximate one as the class did.)

Series resistance: each half of the secondary is in use by one diode at a time, so use half the secondary-resistance value: $R=\dfrac{R_{sec}}2+R_f+R_{ind}=\dfrac{50}2+25+20=\mathbf{70\ \Omega}$. $V_m=50\sqrt2=70.7$ V (each half).

(i) $V_{dc}=\dfrac{2V_m}\pi-I_{dc}R=\dfrac{2V_m}\pi-\dfrac{V_{dc}}{R_L}R\ \Rightarrow\ V_{dc}\left(1+\dfrac{R}{R_L}\right)=\dfrac{2V_m}{\pi}$
$$V_{dc}=\frac{2\sqrt2\times50/\pi}{1+70/750}=\frac{45.02}{1.0933}=\mathbf{41.2\ V}$$
(ii) $V_{ac,rms}=\gamma V_{dc}=0.1406\times41.17=\mathbf{5.8\ V}$ (class: 5.75 V from rounding 0.14 × 41.1).

% regulation $=\dfrac{R}{R_L}\times100=\dfrac{70}{750}\times100=\mathbf{9.33\%}$.
:::

::: flag Class notation slip
Page 37 writes $X_{L1}=\frac{1}{2\omega L_1}$ and $X_{L2}=\frac1{2\omega L_2}$ next to the π-filter; those are the **capacitive** reactances $X_{C1}=\dfrac1{2\omega C_1}$ and $X_{C2}=\dfrac1{2\omega C_2}$. The inductive reactance is $X_L=2\omega L_1$. (The factor 2 is because the ripple is at $2\omega$.)
:::

## 15.4 Shunt capacitor filter (C filter)

{{fig c_filter_c|Capacitor filter: capacitor in parallel with the load.|85}}

The capacitor charges to the peak while the rectifier voltage is rising, and discharges slowly through $R_L$ when the rectifier voltage falls below the capacitor voltage. The diodes conduct only for a short time near each peak.

$$\boxed{\gamma=\frac{1}{4\sqrt3\,fCR_L}}\ \text{(full-wave)}\qquad\Rightarrow\qquad f=50\text{ Hz}:\ \gamma=\frac{2890}{C\,R_L}\ (C\text{ in }\mu\text{F},\ R_L\text{ in }\Omega)$$

Derivation sketch <span class="tag">extra</span>: the capacitor loses charge $I_{dc}/2f$ between peaks (full-wave), so the peak-to-peak ripple is $V_r=\dfrac{I_{dc}}{2fC}$. Treat the ripple as a sawtooth: $V_{ac,rms}=\dfrac{V_r}{2\sqrt3}$. With $V_{dc}\approx I_{dc}R_L$: $\gamma=\dfrac{V_{ac,rms}}{V_{dc}}=\dfrac{1}{4\sqrt3fCR_L}$.

* Larger $C$ or larger $R_L$ (lighter load) → smaller ripple. Bad regulation (the dc voltage drops noticeably as load current rises).
* Your class note beside it: “**more efficient**” (i.e., it gives a higher dc output than the L-filter).

::: ex Example 15.2
$C=1000\ \mu$F, $R_L=100\ \Omega$, $f=50$ Hz (full-wave): $\gamma=\dfrac{1}{4\sqrt3\times50\times10^{-3}\times100}=\dfrac1{34.64}=\mathbf{0.0289}$ (2.9 %), and via the shortcut $2890/(1000\times100)=0.0289$ ✓.

Full-wave rectifier with $C_1=470\ \mu$F, $I_{dc}=100$ mA, $V_m=20$ V: $V_{dc}\approx V_m-\dfrac{I_{dc}}{4fC}=20-\dfrac{0.1}{4\times50\times470\times10^{-6}}=\mathbf{18.9\ V}$.
:::

## 15.5 L-section (choke-input, LC) filter

{{fig c_filter_lc|L-section filter: series choke, shunt capacitor.|85}}

Uses both components: the inductor first (blocks ac), then the capacitor (bypasses what got through).
$$\boxed{\gamma=\frac{\sqrt2}{3}\cdot\frac{1}{4\omega^2LC}}\qquad f=50\text{ Hz}:\ \gamma=\frac{1.194}{LC}\quad(L\text{ in H},\ C\text{ in }\mu\text{F})$$

::: ex Example 15.3
$L=5$ H, $C=100\ \mu$F, 50 Hz: $\gamma=\dfrac{1.194}{5\times100}=\mathbf{0.00239}$ (0.24 %), very small.
:::

## 15.6 Capacitor-input (π-section, CLC) filter

{{fig c_filter_pi|π filter: $C_1$ — $L$ — $C_2$ (shaped like the Greek letter π).|92}}

* A **combination of the L-section and the capacitor filter**; used when a **higher dc voltage** than an L-section gives is required, with **very good ripple rejection** and a **low output current**.
* **Role of each part** (your Pi-Filter notes):
  * **$C_1$:** low reactance to the ac component of the rectifier output, but blocks dc → bypasses part of the ac to ground; dc passes to $L$.
  * **$L$:** very high reactance to ac, low to dc → opposes ac, passes dc.
  * **$C_2$:** bypasses the ac that the inductor could not block → nearly pure dc reaches $R_L$.
* The output waveform is very nearly flat.

### Ripple-factor derivation (from your handwritten notes)

1. Output of $C_1$ (capacitor filter): $V_{C1}=V_{dc}-\dfrac{V_r}{\pi}\sin2\omega t-\dots$ (neglect higher harmonics; $V_r$ = peak-to-peak ripple), with $V_r=\dfrac{I_{dc}}{2fC_1}$. So
$$V_{C1}=V_{dc}-\frac{I_{dc}}{2\pi fC_1}\sin2\omega t$$
The second term is the ac component. Its rms value:
$$V_{ac,rms}\big|_{C_1}=\frac{I_{dc}}{2\pi fC_1}\cdot\frac1{\sqrt2}=\sqrt2\,I_{dc}X_{C_1},\qquad X_{C_1}=\frac1{2\omega C_1}=\frac{1}{4\pi fC_1}$$
2. This ripple is applied to the divider $L$–$C_2$: 
$$V_{ac,out}=V_{ac,rms}\big|_{C_1}\times\frac{X_{C_2}}{X_L+X_{C_2}}=\sqrt2I_{dc}X_{C_1}\frac{X_{C_2}}{X_L+X_{C_2}}$$
3. With $I_{dc}=V_{dc}/R_L$: $\gamma=\dfrac{V_{ac,out}}{V_{dc}}$
$$\boxed{\gamma=\sqrt2\,\frac{X_{C_1}X_{C_2}}{R_L(X_L+X_{C_2})}}$$
4. Usually $X_L\gg X_{C_2}$:
$$\gamma=\sqrt2\,\frac{X_{C_1}}{R_L}\cdot\frac{X_{C_2}}{X_L}=\frac{\sqrt2}{2\omega C_1\cdot2\omega C_2\cdot2\omega L\cdot R_L}=\boxed{\frac{\sqrt2}{8\omega^3LC_1C_2R_L}}\ \left(=\frac{1}{4\sqrt2\,\omega^3LC_1C_2R_L}\right)$$
5. **Output dc voltage:** 
$$V_{dc}=V_m-\frac{I_{dc}}{4fC_1}-I_{dc}(R_S+R_f+R_{choke})$$
($R_f$ = diode forward resistance, $R_S$ = transformer secondary winding resistance, $R_{choke}$ = resistance of the choke).

::: ex Example 15.4
$C_1=C_2=100\ \mu$F, $L=5$ H, $R_L=1\ \text{k}\Omega$, 50 Hz. $X_{C}=\dfrac1{2\omega C}=\dfrac{1}{2\times314.16\times10^{-4}}=15.9\ \Omega$, $X_L=2\omega L=3142\ \Omega$.
$$\gamma=\frac{\sqrt2\,X_{C1}X_{C2}}{R_L(X_L+X_{C2})}=\frac{1.414\times15.9\times15.9}{1000\times3158}=\mathbf{1.13\times10^{-4}}\ (0.011\%)$$
:::

## 15.7 Comparison

| Filter | Ripple factor $\gamma$ | Good for | Weak point |
|---|---|---|---|
| none (FWR) | 0.482 | – | large ripple |
| L (series inductor) | $\dfrac{R_L}{3\sqrt2\,\omega L}$ | **heavy load (small $R_L$)**; $\gamma\downarrow$ with $L\uparrow$ | useless when $R_L$ large |
| C (shunt capacitor) | $\dfrac{1}{4\sqrt3fCR_L}$ | **light load (large $R_L$)** | poor regulation |
| LC (L-section) | $\dfrac{\sqrt2}{3}\dfrac1{4\omega^2LC}$ (independent of $R_L$) | wide load range | bulky choke |
| π (CLC) | $\dfrac{\sqrt2}{8\omega^3LC_1C_2R_L}$ | high dc voltage, lowest ripple | low output current; poor regulation |

## 15.8 Assignment (Filters deck): model answers

::: try Chapter 15 questions
1. What is a filter circuit? Explain the (i) L-filter and (ii) π-section filter and calculate the ripple factor for each.
2. Define (i) ripple factor and (ii) rectification efficiency.
3. FWR, $V_m=30$ V per half, $R_L=200\ \Omega$, C-filter with $C=2200\ \mu$F, 50 Hz. Find the ripple factor and the approximate dc output (ignore diode drop).
4. Why does an L-filter not help for a very large $R_L$?
5. LC filter: find $L$ (with $C=470\ \mu$F) to get $\gamma=0.5\%$ at 50 Hz.
6. A π-filter uses $C_1=C_2=220\ \mu$F, $L=2$ H, $R_L=500\ \Omega$, 50 Hz. Compute $\gamma$.

<details markdown="1"><summary>Answers</summary>

1. See §15.1 (definition), §15.3 (L), §15.6 (π); $\gamma_L=R_L/(3\sqrt2\omega L)$ (for $2\omega L\gg R_L$), $\gamma_\pi=\sqrt2/(8\omega^3LC_1C_2R_L)$.
2. Ripple factor $=$ rms value of ac component ÷ dc value; efficiency $=P_{dc}/P_{ac}$.
3. $\gamma=\dfrac{1}{4\sqrt3\times50\times2200\times10^{-6}\times200}=\dfrac1{152.4}=\mathbf{0.00656}$ (0.66 %); $V_{dc}\approx V_m-\dfrac{I_{dc}}{4fC}$: $I_{dc}\approx V_{dc}/R_L$; solving $V_{dc}=30-\dfrac{V_{dc}/200}{4\times50\times2200\times10^{-6}}=30-0.01136V_{dc}$ → $V_{dc}=\mathbf{29.66\ V}$.
4. When $R_L\gg2\omega L$ the inductor’s ac impedance is negligible compared with $R_L$, so $\gamma\to\sqrt2/3$, the same as with no filter.
5. $\gamma=\dfrac{1.194}{LC}$ ⇒ $L=\dfrac{1.194}{0.005\times470}=\mathbf{0.51\ H}$.
6. $X_C=\dfrac1{2\times314.16\times220\times10^{-6}}=7.23\ \Omega$; $X_L=2\times314.16\times2=1257\ \Omega$; $\gamma=\dfrac{\sqrt2\times7.23^2}{500\times(1257+7.23)}=\dfrac{73.9}{632{,}100}=\mathbf{1.17\times10^{-4}}$.
</details>
:::
