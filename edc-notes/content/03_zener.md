# Chapter 3: Zener diode

*Class notes p. 1 · slides: Unit-I First part, Topic 7*

::: kid The pressure-relief valve
Your kitchen pressure cooker has a **safety valve**: when the pressure gets too high the valve opens and lets steam out, so the pressure never goes above a fixed limit. A **Zener diode** is that valve for voltage. Connect it backwards across something: as long as the voltage stays below the Zener voltage, nothing happens. Try to push the voltage higher and the Zener suddenly conducts a lot of current, **holding the voltage at (nearly) the same value**. That makes it a *voltage regulator* or *voltage reference*.
:::

## 3.1 What it is

* Also called **breakdown diode**, **voltage-reference diode**, **voltage regulator diode**.
* It is a PN diode designed to work **in the reverse breakdown region**.
* It is **heavily doped**, so the depletion region is very thin. The breakdown voltage $V_Z$ is set during manufacture by controlling the doping.
* Symbol: a diode with a bent bar on the cathode. Anode = A, cathode = K.

{{fig c_sym_zener|Zener diode symbol.|35}}

::: class Class notes (p. 1)
“Zener diode: highly doped; for voltage regulation.” The sketch shows the symbol, the reverse breakdown curve with $V_Z$ marked, the forward-bias region on the right, and the **equivalent circuit: a battery $V_Z$ in series with a small resistance $r_Z$**.
:::

## 3.2 The V–I characteristic

{{fig p_zener_iv|Zener characteristic. The useful region is the steep reverse breakdown line, between $I_{ZK}$ and $I_{ZM}$.|72}}

* **Forward:** like an ordinary diode.
* **Reverse:** current is negligible until the breakdown point ($V_Z$), then rises very steeply. The steep region is the **regulating region**.
* The slope is not perfectly vertical because of the **zener resistance** $r_Z=\Delta V_Z/\Delta I_Z$.
* **Minimum current $I_{ZK}$ (“knee” or break-over current):** below this the diode drops out of regulation. It must be maintained.
* **Maximum current $I_{ZM}$:** above this the diode is **damaged** by heat.

## 3.3 Two mechanisms

* **Zener effect:** a high electric field across a very thin junction directly breaks covalent bonds and frees electrons. Dominates for breakdown **below about 6 V**.
* **Avalanche effect:** accelerated carriers ionise atoms by collision, creating more carriers in a chain. Dominates **above about 6 V**.

Both give the same kind of curve, and the device is still called a “Zener” diode.

## 3.4 Specifications and equivalent circuit

A Zener is specified by four things:

1. $V_Z$: Zener (breakdown) voltage,
2. $P_{DZ}$ (or $P_{ZM}$): maximum power dissipation,
3. $I_{ZK}$: knee / break-over current,
4. $r_Z$: Zener resistance.

$$P_{DZ}=V_ZI_Z,\qquad I_{ZM}=\frac{P_{ZM}}{V_Z},\qquad r_Z=\frac{\Delta V_Z}{\Delta I_Z},\qquad V_Z'=V_Z+I_Zr_Z$$

The ideal $r_Z$ is zero; in practice it is from a few ohms to several hundred ohms. The terminal voltage $V_Z'=V_Z+I_Zr_Z$ rises slightly with current (this is the tilt of the curve).

## 3.5 The Zener voltage regulator

{{fig c_zener_reg_load|Shunt regulator: series resistor $R_S$, Zener across the load $R_L$.|72}}

Operation: $V_{in}$ is the unregulated supply. $R_S$ **drops the extra voltage**. The Zener holds $V_{out}\approx V_Z$. If $V_{in}$ rises, the extra current flows through the Zener (not the load) and the extra voltage drops across $R_S$. If $R_L$ changes, the Zener current changes in the opposite direction so the load voltage stays put.

$$I_S=\frac{V_{in}-V_Z}{R_S},\qquad I_L=\frac{V_Z}{R_L},\qquad I_Z=I_S-I_L$$

**Design rules** (this is what examiners ask):

* Choose $R_S$ so that $I_Z\ge I_{ZK}$ at the **lowest** input and **heaviest** load, and $I_Z\le I_{ZM}$ at the **highest** input and **lightest** load (load removed: all $I_S$ goes through the Zener).
* $R_S=\dfrac{V_{in}-V_Z}{I_Z+I_L}$.

::: ex Example 3.1 (choose $R_S$)
Input 12 V, Zener 5.1 V, load $R_L=1\ \text{k}\Omega$, want $I_Z=10$ mA.
$I_L=5.1/1000=5.1$ mA, $I_S=10+5.1=15.1$ mA.
$$R_S=\frac{12-5.1}{15.1\text{ mA}}=\mathbf{457\ \Omega}\ \ (\text{use }470\ \Omega\ \text{preferred value: }I_S=14.7\text{ mA},\ I_Z=9.6\text{ mA})$$
Zener power $=V_ZI_Z=5.1\times10\text{ mA}=51$ mW, which is comfortably within a 500 mW device.
:::

::: ex Example 3.2 (input varies)
9.1 V Zener, $R_S=330\ \Omega$, $R_L=1\ \text{k}\Omega$, $V_{in}$ varies from 15 V to 20 V.

$I_L=9.1$ mA always.
* $V_{in}=15$ V: $I_S=(15-9.1)/330=17.88$ mA → $I_Z=17.88-9.1=\mathbf{8.78\ mA}$.
* $V_{in}=20$ V: $I_S=(20-9.1)/330=33.03$ mA → $I_Z=\mathbf{23.9\ mA}$.

Worst-case power: $9.1\times23.9=218$ mW. A 500 mW Zener is fine: $I_{ZM}=500/9.1=54.9$ mA.

With $r_Z=8\ \Omega$ the output moves by only $\Delta I_Z\,r_Z=(23.9-8.8)\text{ mA}\times8=0.12$ V (about 1.3%) while the input moved 5 V. That is regulation.
:::

::: trap Common mistakes
* Putting the Zener the wrong way round (it must be **reverse biased**). Forward it is just a 0.7 V diode.
* Forgetting $R_S$. With no series resistor the current is unlimited and the Zener burns out.
* Forgetting that with the load **disconnected** the whole $I_S$ flows through the Zener: check $P=V_ZI_S\le P_{ZM}$.
:::

## 3.6 Applications (from the slides)

1. Voltage regulator.
2. Fixed reference voltage in transistor biasing circuits.
3. Peak clippers in wave-shaping circuits.
4. Meter protection against accidental over-voltage.

## 3.7 Try it yourself

::: try Chapter 3 questions
1. Why must a Zener be heavily doped?
2. Zener specs: $V_Z=6.8$ V, $P_{ZM}=1$ W. Find $I_{ZM}$.
3. A 10 V Zener has $r_Z=8\ \Omega$ and carries 20 mA. What is the terminal voltage $V_Z'$ if the quoted $V_Z$ was measured at the knee, with $V_Z'=V_Z+I_Zr_Z$?
4. 12 V supply, 5.6 V Zener, $R_S=220\ \Omega$, load 1 kΩ. Find $I_S$, $I_L$, $I_Z$.
5. Why does the regulator keep $V_{out}$ constant when $V_{in}$ rises?

<details markdown="1"><summary>Answers</summary>

1. Heavy doping makes the depletion region very thin, so a moderate reverse voltage gives a very large field, producing sharp, low-voltage breakdown.
2. $I_{ZM}=1\text{ W}/6.8\text{ V}=\mathbf{147\ mA}$.
3. $V_Z'=10+0.020\times8=\mathbf{10.16\ V}$.
4. $I_S=(12-5.6)/220=29.1$ mA; $I_L=5.6/1000=5.6$ mA; $I_Z=29.1-5.6=\mathbf{23.5\ mA}$.
5. Extra input current goes through the Zener (its current rises steeply for a tiny voltage rise), and the extra voltage is dropped across $R_S$; the load sees the nearly constant $V_Z$.
</details>
:::
