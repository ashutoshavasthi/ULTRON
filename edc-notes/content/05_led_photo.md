# Chapter 6: Light-emitting diode (LED)

*Class notes p. 3 ("LED: already known") · slides: Different Diodes*

::: words
| Word / symbol | Plain meaning |
|---|---|
| LED | Light Emitting Diode: a diode that gives out light when forward biased |
| Photon | a packet of light energy $E=h\nu=hc/\lambda$ |
| $\lambda$ | "lambda": wavelength of light, in nanometres (nm) |
| Monochromatic | a single colour (one wavelength) |
| $E$ (eV) | energy of one photon in electron-volts |
| $V_F$ | forward voltage drop of the LED at its working current (about 1.8–3.5 V depending on colour) |
| $I_F$ | forward current (typically 20 mA) |
| $R_S$ | series resistor that limits the LED current |
| Recombination | electron falls into a hole and releases energy |
| Phosphor | coating that converts blue light to yellow/white |
| Infrared | light just beyond red, invisible ($\lambda>760$ nm) |
:::

::: kid A diode that glows
When an electron in the "balcony" (conduction band) falls into an empty seat (hole) in the "lower floor" (valence band), it gives away energy. In an ordinary diode that energy becomes **heat**. In an LED made of the right material, the energy comes out as **a particle of light (a photon)**. The bigger the energy gap, the more energetic (bluer) the light.
:::

## 6.1 Principle

* An LED turns electrical energy into light. It emits **monochromatic** light.
* It is a PN junction that works **only in forward bias**.
* Forward bias pushes electrons from the N side and holes from the P side toward the junction. Free electrons in the conduction band **recombine** with holes in the valence band and release the energy as **photons**.
* Energy of one electron crossing a voltage $V$: $E=qV$ joules, with $q=1.6\times10^{-19}$ C. A photon carries $E=h\nu=hc/\lambda$.

$$E\ (\text{eV})\approx\frac{1240}{\lambda\ (\text{nm})}\qquad\text{and the forward voltage is roughly }E_g/q.$$

{{fig c_sym_led|LED symbol: a diode with two arrows pointing AWAY (light out).|38}}

::: flag About the "materials" sentence in your slide
The slide says LEDs use "phosphorus and arsenic instead of germanium and silicon because Si and Ge do not emit energy in the form of heat". The correct statement is: LEDs are built from **compound semiconductors** (GaAs, GaAsP, GaP, AlGaAs, InGaN…) because in **Si and Ge the recombination energy is released mainly as heat, not light**. Write it that way in the exam.
:::

## 6.2 Colours, wavelengths and materials (your slide)

{{fig p_led_colors|Visible spectrum with the LED colour ranges of the slide.|95}}

| Colour | Wavelength | Material |
|---|---|---|
| Infrared | $\lambda>760$ nm | GaAs, AlGaAs |
| Red | 610–760 nm | AlGaAs, GaAsP, AlGaInP, GaP |
| Green | 500–570 nm | GaP, AlGaP (traditional); InGaN / GaN (pure green) |
| Violet | 400–450 nm | InGaN |
| Purple | several types | dual blue/red LEDs, blue with red phosphor, white with purple plastic |
| White | broad spectrum | cool white: blue/UV diode + **yellow phosphor**; warm white: blue diode + **orange phosphor** |

Different colours have **different forward voltage drops** at the specified current (typically 20 mA).

::: ex Example 6.1: Photon energy and colour
**Given:** red 650 nm, blue 450 nm, infrared 830 nm.

**Formula:** $E=1240/\lambda$ (eV, with $\lambda$ in nm).

**Step 1.** Red: $1240/650=1.91$ eV.
**Step 2.** Blue: $1240/450=2.76$ eV.
**Step 3.** Infrared: $1240/830=1.49$ eV.

**Answer:** 1.91 eV, 2.76 eV, 1.49 eV. An LED's forward voltage is about equal to the photon energy, so a red LED needs about 2 V and a blue one about 3 V.

**What it means:** blue needs the largest gap, which is why blue LEDs were the hardest to invent.
:::

## 6.3 Using an LED: the series resistor

**Never connect an LED directly to a battery.** Its forward voltage is almost constant, so the current would be limited only by tiny resistances and the LED would burn out. Add a **series resistor** $R_S$:

$$R_S=\frac{V_S-V_F}{I_F}$$

{{fig c_led|LED with current-limiting resistor.|55}}

::: ex Example 6.2: Choose the resistor
**Given:** supply $V_S=5$ V, red LED $V_F=2$ V, wanted current $I_F=20$ mA.

**Find:** $R_S$ and its power.

**Step 1: voltage the resistor must drop.** $V_S-V_F=5-2=3$ V.
**Step 2: Ohm's law.** $R_S=3/0.020=150\ \Omega$.
**Step 3: resistor power.** $P=I^2R=(0.020)^2\times150=0.06$ W $=60$ mW (a normal ¼ W resistor is fine).

**Answer:** $R_S=\mathbf{150\ \Omega}$.
:::

::: ex Example 6.3: Two more supplies
**(a)** 9 V supply, blue LED $V_F=3.2$ V, 20 mA: $R_S=(9-3.2)/0.02=290\ \Omega$. Preferred value 330 Ω, giving $I=(9-3.2)/330=17.6$ mA (safe).
**(b)** Three red LEDs (2 V each) in series from 12 V at 20 mA: total LED drop $=3\times2=6$ V, $R_S=(12-6)/0.02=300\ \Omega$.
:::

## 6.4 Advantages and applications (slides)

* About **5 times more efficient** than fluorescent bulbs (same light for less energy).
* Life **30,000–100,000 hours** versus 750–2000 hours for others.
* Runs **cool** (about 90 °F) while others run at 150–400 °F.
* No mercury or harmful gases; cheap and light.
* **Uses:** sensors, mobile phones, signals, calculators, watches, cameras, multimeters, fibre-optic data communication.

## 6.5 Practice

::: try Questions for Chapter 6
1. In which bias does an LED work, and how does it emit light?
2. Why are Si and Ge not used for LEDs?
3. A green LED ($V_F=2.2$ V) must run at 15 mA from a 5 V supply. Find $R_S$.
4. Find the photon energy for $\lambda=520$ nm.
5. An LED is connected straight across a 3 V battery with no resistor. Why does it fail?
:::

::: soln Answers and full solutions
<details markdown="1"><summary>Solution 1</summary>

Forward bias. The forward voltage pushes electrons and holes into the junction region; when an electron recombines with a hole, the released energy leaves as a photon (light).
</details>

<details markdown="1"><summary>Solution 2</summary>

In silicon and germanium recombination releases energy mostly as **heat** (lattice vibrations), not photons. LEDs use compound semiconductors (GaAs, GaP, GaAsP, InGaN…) where recombination gives light.
</details>

<details markdown="1"><summary>Solution 3</summary>

**Given:** $V_S=5$ V, $V_F=2.2$ V, $I_F=15$ mA.
**Step 1.** Voltage across $R_S$: $5-2.2=2.8$ V.
**Step 2.** $R_S=2.8/0.015=186.7\ \Omega$.

**Answer:** about **187 Ω** (use 180 Ω or 220 Ω).
</details>

<details markdown="1"><summary>Solution 4</summary>

**Step 1.** $E=1240/\lambda=1240/520=2.385$ eV.
**Answer:** **2.38 eV**.
</details>

<details markdown="1"><summary>Solution 5</summary>

Once the voltage exceeds the LED's forward voltage (about 2 V), current rises exponentially. Nothing but tiny internal resistance and the battery's resistance limits it, so the current becomes far above the 20 mA rating and the junction overheats. A series resistor sets the current.
</details>
:::

# Chapter 7: Photodiode (and phototransistor) {.chap}

*Class notes pp. 3 and 8 · slides: UJT and Photodiode*

::: words
| Word / symbol | Plain meaning |
|---|---|
| Photodiode | a diode that turns light into current |
| Photoelectric effect | light knocking electrons free from a material |
| Photocurrent $I_{ph}$ | the current produced by light |
| Dark current | the small leakage current when there is no light |
| Photovoltaic mode | no bias: the light itself produces a voltage (a solar cell) |
| Photoconductive mode | reverse biased: current is proportional to light |
| Quantum efficiency $\eta_q$ | (electrons collected) ÷ (photons arriving) |
| Responsivity $R$ | photocurrent per watt of light (A/W) |
| PIN photodiode | photodiode with an undoped (intrinsic) layer between P and N for speed |
| Avalanche photodiode | photodiode with internal gain from carrier multiplication |
| Phototransistor | a transistor whose base current comes from light |
| $\lambda_c$ | the longest wavelength the material can detect |
:::

::: kid The opposite of an LED
An LED turns electricity into light. A **photodiode** does the reverse: **light in → electric current out**. When a photon of light with enough energy hits the junction, it kicks an electron loose, making a free electron and a hole. The junction's built-in field sweeps them apart, and you get a current proportional to how bright the light is. That is how remote-control receivers, smoke detectors and CD players "see".
:::

## 7.1 Definition

A **photodiode** is a semiconductor light sensor that generates current or voltage when its PN junction is illuminated. It converts light energy into electrical energy (**inner photoelectric effect**): a photon with enough energy creates an electron–hole pair. A **solar cell** is an example.

{{fig c_sym_photo|Photodiode symbol: the arrows point IN (light in).|38}}

Three ways to use it (from the slide):
1. **Photovoltaic** mode, no bias: works as a solar cell.
2. **Reverse-biased** (photoconductive) mode: works as a **photodetector**. A photodiode is *designed to operate in reverse bias*.
3. **Forward-biased**: behaves like an LED.

## 7.2 Operation

{{fig c_photodiode|Reverse-biased photodiode: the current is proportional to the light.|60}}

* Photons absorbed **in or near the depletion region** create electron–hole pairs that are **immediately separated** by the junction field. This flow is the **photocurrent**.
* Carriers created inside the depletion region respond fastest; a **thicker depletion region** makes the device faster and raises the **quantum efficiency**.
* In the dark only a small **dark (reverse leakage) current** flows.

{{fig p_photodiode_iv|Photodiode characteristics: reverse current rises with light level; with no bias the device becomes a voltage source (solar-cell mode).|72}}

## 7.3 Construction (from the slide)

* Start with **N-type silicon**. A thin **P layer** (usually boron-doped) is formed on the front by thermal diffusion or ion implantation. The interface is the PN junction.
* Small metal contacts on the front; the whole back is coated with a contact metal. **Back contact = cathode; front contact = anode.**
* The active area is coated with silicon nitride, monoxide or dioxide for protection and as an **anti-reflection coating** (thickness tuned to particular wavelengths).
* Light enters through the **thin P layer**; light intensity falls off exponentially with depth.
* Many photodiodes use a **PIN junction** (intrinsic layer between P and N) to speed up the response. Types: **PIN**, **PN**, **avalanche**.

## 7.4 Materials and wavelength range

| Material | Wavelength range (nm) |
|---|---|
| Silicon | 190–1110 |
| Germanium | 400–1700 |
| Indium gallium arsenide | 800–2600 |
| Lead sulphide | 100–3500 (as listed in your slide) |

Cross-check: the longest wavelength a material detects is set by its gap: $\lambda_c\approx1240/E_g$ nm. Si ($E_g=1.1$ eV) → 1127 nm ✓. Ge ($0.74$ eV) → 1676 nm ✓.

## 7.5 Features and applications

* **Features:** excellent linearity with light, low noise, wide spectral response, rugged, compact, long life.
* **Applications:** CD players, smoke detectors, infrared-remote receivers (TV, air conditioner), light sensors, accurate light measurement, medical uses (CT scanners, sample analysers, pulse oximeters).

::: ex Example 7.1: Photocurrent of a silicon photodiode
**Given:** quantum efficiency $\eta_q=0.8$, wavelength $\lambda=900$ nm, light power $P=10\ \mu$W, load $R_L=100$ kΩ.

**Find:** responsivity, photocurrent, voltage across the load.

**Formula:** responsivity $R=\eta_q\dfrac{q\lambda}{hc}=\eta_q\dfrac{\lambda(\mu\text{m})}{1.24}$ A/W.

**Step 1: wavelength in µm.** $900\ \text{nm}=0.9\ \mu\text{m}$.
**Step 2: responsivity.** $R=0.8\times\dfrac{0.9}{1.24}=0.581$ A/W.
**Step 3: photocurrent.** $I_{ph}=R\times P=0.581\times10\times10^{-6}=5.8\times10^{-6}$ A.
**Step 4: load voltage.** $V=I_{ph}R_L=5.8\times10^{-6}\times10^{5}=0.58$ V.

**Answer:** $R=0.58$ A/W, $I_{ph}=5.8\ \mu$A, $V=0.58$ V.
:::

## 7.6 Phototransistor <span class="tag">extra</span>

Your syllabus lists "photo diodes & photo transistors" but none of your files describes the phototransistor, so here is the short standard version.

* A **phototransistor** is a BJT whose **base–collector junction is exposed to light** (the base lead is often left open). Light creates the base current, and the transistor **amplifies it by $\beta$**: $I_C\approx\beta I_{photo}$.
* Advantage over a photodiode: **much more sensitive** (built-in gain). Disadvantage: **slower** and less linear.
* Uses: opto-couplers, object detectors, light-operated switches, encoders.

## 7.7 Practice

::: try Questions for Chapter 7
1. In what bias is a photodiode normally used? What happens to the reverse current when light gets brighter?
2. What is quantum efficiency?
3. Why is a PIN structure used?
4. Which material would you choose to detect 1500 nm light: Si or Ge? Give a reason with numbers.
5. A photodiode has responsivity 0.5 A/W. Find the photocurrent for 20 µW of light.
:::

::: soln Answers and full solutions
<details markdown="1"><summary>Solution 1</summary>

Reverse bias. The reverse (photo)current increases in proportion to the light intensity.
</details>

<details markdown="1"><summary>Solution 2</summary>

Quantum efficiency = (number of photo-generated electrons collected per second) ÷ (number of photons arriving per second).
</details>

<details markdown="1"><summary>Solution 3</summary>

The intrinsic (undoped) layer widens the depletion region. More light is absorbed inside it, so the response is faster and the quantum efficiency higher.
</details>

<details markdown="1"><summary>Solution 4</summary>

**Step 1.** Cut-off wavelengths: Si $\approx1240/1.1=1127$ nm; Ge $\approx1240/0.74=1676$ nm.
**Step 2.** 1500 nm is above Si's limit (1127 nm) but below Ge's (1676 nm).

**Answer:** **germanium**.
</details>

<details markdown="1"><summary>Solution 5</summary>

**Formula:** $I_{ph}=R\times P$.
**Step 1.** $P=20\ \mu\text{W}=20\times10^{-6}$ W.
**Step 2.** $I_{ph}=0.5\times20\times10^{-6}=10\times10^{-6}$ A.

**Answer:** **10 µA**.
</details>
:::
