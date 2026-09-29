# Chapter 6: Light-emitting diode (LED)

*Class notes p. 3 (“LED: already known”) · slides: Different Diodes*

::: kid A diode that glows
When an electron in the “balcony” (conduction band) falls back into an empty seat (hole) in the “lower floor” (valence band), it gives away energy. In an ordinary diode that energy becomes **heat**. In an LED made of the right material, the energy comes out as **a particle of light (a photon)**. The bigger the energy gap, the more energetic (bluer) the light.
:::

## 6.1 Principle

* Electrical energy → light energy. An LED emits **monochromatic** light (a single colour, essentially one wavelength).
* It is a PN junction that works **only in forward bias**.
* Forward bias pushes electrons from the N side and holes from the P side toward the junction. Free electrons in the conduction band **recombine** with holes in the valence band and release the energy as **photons**.
* Energy of one electron crossing a voltage $V$: $E=qV$ joules ($q=1.6\times10^{-19}$ C). A photon carries $E=h\nu=hc/\lambda$.

$$E\ (\text{eV})\approx\frac{1240}{\lambda\ (\text{nm})}\qquad\text{so the forward voltage is roughly }E_g/q$$

{{fig c_sym_led|LED symbol: a diode with two arrows pointing AWAY (light out).|38}}

::: flag About the “materials” sentence in your slide
The slide says LEDs use “Phosphorus and Arsenic instead of germanium and silicon because Si and Ge do not emit energy in the form of heat”. The correct statement is: LEDs are built from **compound semiconductors** (GaAs, GaAsP, GaP, AlGaAs, InGaN, …) because in **Si and Ge the recombination energy is released mainly as heat, not light**. Write it that way in the exam.
:::

## 6.2 Colours, wavelengths and materials (from your slide)

{{fig p_led_colors|Visible spectrum with the LED colour ranges of the slide.|95}}

| Colour | Wavelength | Material |
|---|---|---|
| Infrared | $\lambda>760$ nm | GaAs, AlGaAs |
| Red | 610–760 nm | AlGaAs, GaAsP, AlGaInP, GaP |
| Green | 500–570 nm | GaP, AlGaP (traditional); InGaN / GaN (pure green) |
| Violet | 400–450 nm | InGaN |
| Purple | multiple types | dual blue/red LEDs, blue with red phosphor, white with purple plastic |
| White | broad spectrum | cool white: blue/UV diode with **yellow phosphor**; warm white: blue diode with **orange phosphor** |

Slide values quoted in words: red ≈ 700 nm, blue ≈ 400 nm, infrared ≈ 830 nm. Different colours have **different forward voltage drops** $\Delta V$ at the specified current (typically 20 mA).

::: ex Example 6.1 (photon energy)
Red 650 nm: $E=1240/650=\mathbf{1.91\ eV}$ → forward voltage about 2 V. Blue 450 nm: $1240/450=\mathbf{2.76\ eV}$ → about 3 V. Infrared 830 nm: $1240/830=\mathbf{1.49\ eV}$. Blue needs the bigger gap: that is why blue LEDs were the hard ones to invent.
:::

## 6.3 Using an LED: the series resistor

**Never connect an LED directly to a battery.** Its forward drop is nearly constant, so the current would be limited only by the tiny resistance and the LED burns out. Put a **series resistor** $R_S$:

$$R_S=\frac{V_S-V_F}{I_F}$$

{{fig c_led|LED with current-limiting resistor.|55}}

::: ex Example 6.2
5 V supply, red LED $V_F=2$ V, $I_F=20$ mA: $R_S=\dfrac{5-2}{0.020}=\mathbf{150\ \Omega}$ (a standard value). Power in the resistor $=I^2R=0.02^2\times150=60$ mW.

9 V supply, blue LED $V_F=3.2$ V, 20 mA: $R_S=(9-3.2)/0.02=290\ \Omega$ → use **330 Ω** ($I=17.6$ mA, safe).

Three red LEDs in series from 12 V: $R_S=(12-3\times2)/0.02=\mathbf{300\ \Omega}$.
:::

## 6.4 Advantages and applications (slides)

* About **5 times more efficient** than fluorescent bulbs: same light for less energy.
* Life **30,000 – 100,000 hours** vs 750–2000 hours for others.
* Run **cool** (about 90 °F) while others run at 150–400 °F.
* No mercury or harmful gases: environmentally friendly. Cheap and light.
* **Uses:** sensors, mobile phones, signals, calculators, watches, cameras, multimeters, fibre-optic data communication.

## 6.5 Try it yourself

::: try Chapter 6 questions
1. In which bias does an LED work, and how does it emit light?
2. Why are Si and Ge not used for LEDs?
3. A green LED ($V_F=2.2$ V) is to run at 15 mA from 5 V. Find $R_S$.
4. Find the photon energy for λ = 520 nm.

<details markdown="1"><summary>Answers</summary>

1. Forward bias; electron–hole recombination across the junction releases photons.
2. In Si/Ge the recombination energy mostly appears as heat, not light; LEDs use compound semiconductors (GaAs, GaP, GaAsP, InGaN…).
3. $R_S=(5-2.2)/0.015=\mathbf{187\ \Omega}$ → use 180 Ω or 220 Ω.
4. $1240/520=\mathbf{2.38\ eV}$.
</details>
:::

# Chapter 7: Photodiode (and phototransistor) {.chap}

*Class notes pp. 3 and 8 · slides: UJT and Photodiode*

::: kid The opposite of an LED
An LED turns electricity into light. A **photodiode** does the reverse: **light in → electric current out**. When a photon (a particle of light) hits the junction with enough energy, it kicks an electron loose, making a free electron and a hole. The junction’s built-in field sweeps them apart, and you get a current that is proportional to how bright the light is. That is how remote-control receivers, smoke detectors and CD players “see”.
:::

## 7.1 Definition

A **photodiode** is a semiconductor light sensor that generates current or voltage when its PN junction is illuminated. It converts light energy into electrical energy (**inner photoelectric effect**): a photon with enough energy creates an electron–hole pair. A **solar cell** is an example.

{{fig c_sym_photo|Photodiode symbol: the arrows point IN (light in).|38}}

Three modes (from the slide):
1. **Photovoltaic** mode, no bias: acts as a solar cell.
2. **Reverse-biased** (photoconductive) mode: used as a **photodetector**. A photodiode is *designed to operate in reverse bias*.
3. **Forward-biased**: behaves like an LED.

## 7.2 Operation

{{fig c_photodiode|Reverse-biased photodiode: the current is proportional to the light.|60}}

* Photons absorbed **in or near the depletion region** create electron–hole pairs that are **immediately separated** by the junction field. This flow of carriers is the **photocurrent**.
* Photons absorbed *within the depletion region* give the fastest response; a **thicker depletion region** makes the device faster and raises the **quantum efficiency**.
* **Quantum efficiency** = ratio of photocurrent (electrons per second) to incident light intensity (photons per second).
* In the dark only a small **dark (reverse leakage) current** flows.

{{fig p_photodiode_iv|Photodiode characteristics: the reverse current (third quadrant) rises with light level; with no bias the device becomes a voltage source (solar-cell mode).|72}}

## 7.3 Construction (from the slide)

* Start with **N-type silicon**. A thin **P layer** (usually boron-doped) is formed on the front by thermal diffusion or ion implantation. The interface is the PN junction.
* Small metal contacts on the front, the whole back coated with a contact metal. **Back contact = cathode, front contact = anode.**
* The active area is coated with silicon nitride, monoxide or dioxide for protection and as an **anti-reflection coating** (its thickness is tuned to particular wavelengths).
* Light enters through the **thin P layer**; light intensity falls off exponentially with depth.
* Many photodiodes use a **PIN junction** (an intrinsic layer between P and N) to increase the speed of response. Types: **PIN**, **PN**, **avalanche** photodiode.

## 7.4 Materials and wavelength range

| Material | Wavelength range (nm) |
|---|---|
| Silicon | 190 – 1110 |
| Germanium | 400 – 1700 |
| Indium gallium arsenide | 800 – 2600 |
| Lead sulphide | 100 – 3500 (as listed in your slide) |

Cross-check: the longest wavelength a material can detect is set by its gap, $\lambda_c\approx1240/E_g$ nm: Si ($E_g=1.1$ eV) → 1130 nm ✓; Ge (0.74 eV) → 1680 nm ✓.

## 7.5 Features and applications

* **Features:** excellent linearity with light, low noise, wide spectral response, mechanically rugged, compact and light, long life.
* **Applications:** CD players, smoke detectors, infrared-remote receivers (TVs, air conditioners), light sensors, accurate light-intensity measurement, and medical uses (CT-scan detectors, sample analysers, pulse oximeters).

::: ex Example 7.1 (responsivity)
A silicon photodiode has quantum efficiency $\eta_q=0.8$ at $\lambda=900$ nm. Responsivity $R=\eta_q\dfrac{q\lambda}{hc}=\eta_q\dfrac{\lambda(\mu\text{m})}{1.24}=0.8\times\dfrac{0.9}{1.24}=\mathbf{0.58\ A/W}$. With 10 µW of light: $I_{ph}=0.58\times10\ \mu\text{W}=\mathbf{5.8\ \mu A}$; across $R_L=100\ \text{k}\Omega$ that is 0.58 V.
:::

## 7.6 Phototransistor <span class="tag">extra</span>

Your Unit-I syllabus lists “photo diodes & photo transistors”, but none of your files describe the phototransistor, so here is the short standard version.

* A **phototransistor** is a BJT whose **base–collector junction is exposed to light** (often the base lead is left open). Light creates the base current, and the transistor **amplifies it by $\beta$**: $I_C\approx\beta\,I_{photo}$.
* Advantage over a photodiode: **much higher sensitivity** (built-in gain). Disadvantage: **slower** (larger capacitance), and less linear.
* Uses: opto-couplers, object detectors, light-operated switches, encoders.

## 7.7 Try it yourself

::: try Chapter 7 questions
1. In what bias is a photodiode normally operated? What happens to the reverse current when light intensity rises?
2. What is quantum efficiency?
3. Why is a PIN structure used?
4. Which photodiode material would you choose to detect 1500 nm light: Si or Ge?

<details markdown="1"><summary>Answers</summary>

1. Reverse bias; the reverse (photo)current increases in proportion to the light intensity.
2. The ratio of the number of photo-generated electrons (photocurrent) to the number of incident photons.
3. The intrinsic layer widens the depletion region: faster response and higher quantum efficiency.
4. Germanium (Si only responds up to about 1110 nm).
</details>
:::
