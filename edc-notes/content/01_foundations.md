# Chapter 1: Foundations from zero

::: words
| Word / symbol | Plain meaning |
|---|---|
| Semiconductor | material (silicon Si, germanium Ge) that conducts a little; we can control how much |
| Electron | tiny negative charge; the thing that carries current in metals |
| Hole | an empty seat left when an electron leaves a bond; acts like a **positive** charge that moves |
| Energy band | a range of energies electrons are allowed to have |
| Valence band | the lower band; full of electrons stuck in bonds |
| Conduction band | the upper band; electrons here are free and carry current |
| Energy gap $E_g$ | the forbidden energy between the two bands, measured in eV |
| eV (electron-volt) | a tiny unit of energy: $1\ \text{eV}=1.6\times10^{-19}$ J |
| Covalent bond | a pair of shared electrons holding two neighbouring atoms together |
| Intrinsic | pure, undoped |
| Doping | adding a very small amount of impurity on purpose |
| Donor / acceptor | impurity giving a free electron / creating a hole |
| N-type / P-type | material with extra electrons / extra holes |
| Majority / minority carrier | the more numerous / less numerous carrier |
| Recombination | an electron falls into a hole and both vanish |
| $n$, $p$ | concentration (number per cm³) of free electrons, holes |
| $n_i$ | the concentration of each in **pure** material |
| $N_D$, $N_A$ | concentration of donor, acceptor atoms |
:::

::: kid The whole idea in one picture
Imagine a huge **cinema**. The seats on the lower floor are all full (the **valence band**). The balcony upstairs is completely empty (the **conduction band**). People can only move around freely if there is space, so those on the full lower floor are stuck. To move, someone must jump up to the balcony.

* In a **metal** the balcony is right next to (even overlapping) the full floor: people move all the time, so electricity flows easily.
* In an **insulator** the balcony is miles above: nobody can jump, so no electricity.
* In a **semiconductor** the balcony is a *short hop* away. A little heat or light and a few people jump up. That is why we can **control** how well it conducts, and that control is the whole magic of electronics.

Whoever jumps up leaves an **empty seat** behind. Neighbours shuffle into it, so the empty seat appears to move the other way. That moving empty seat is a **hole**, and it behaves like a positive charge.
:::

## 1.1 Energy bands in solids

### From single atoms to bands
1. An isolated atom lets its electrons have only certain **allowed energies** (quantised levels).
2. In a **crystal** the outer electrons are shared between neighbours, so each allowed level **splits into a huge number of closely spaced levels**. A packed group of levels is a **band**.
3. Inner electrons (in completely full inner shells) are hardly disturbed. Only the outermost shells spread into bands.
4. Silicon has atomic number 14 and configuration $1s^2\,2s^2\,2p^6\,3s^2\,3p^2$: **four outer electrons**. In the crystal these give two bands: the **valence band** (highest filled) and the **conduction band** (empty at absolute zero), separated by the **forbidden gap** $E_g$.

{{fig p_bands|Energy bands of a metal, a semiconductor and an insulator. Electrons can only sit in the coloured bands.|92}}

| | Metal | Semiconductor | Insulator |
|---|---|---|---|
| Gap $E_g$ | none (partly filled band, or bands overlap) | small: Si **1.1 eV**, Ge **0.74 eV** | large: about **6 eV**; diamond **7 eV** |
| At 0 K (absolute zero, −273 °C) | conducts | insulator | insulator |
| At room temperature | conducts very well | conducts a little | practically none |

::: class In your slides (Unit-I First part)
* **Metals:** either the conduction band is *partly filled*, or it *overlaps* the valence band. Electrons overflow into empty levels with almost no extra energy.
* The highest energy level occupied at **absolute zero** is the **Fermi level**; its energy is the **Fermi energy**.
* **Semiconductors:** at 0 K no electron can cross the gap, so it is an insulator. At room temperature some valence electrons gain more than $E_g$ and jump up. The fraction that jump is proportional to $e^{-E_g/k_BT}$, which is "sizeable" only because $E_g$ is small.
* **Insulators:** $E_g\approx6$ eV; electrons "however heated" practically cannot cross.
:::

::: formula Why only a few electrons jump
Thermal energy at room temperature is $k_BT\approx0.026$ eV. The gap of silicon is 1.1 eV, about 42 times bigger. The chance of an electron having enough energy falls off like $e^{-E_g/k_BT}=e^{-42}$, a very small number. That is why pure silicon conducts only a tiny amount.
:::

## 1.2 Electrons and holes

1. In pure silicon each atom shares its 4 outer electrons with 4 neighbours. Each shared pair is a **covalent bond**. At 0 K every electron is locked in a bond: **no free carriers**.
2. Add energy (heat or light). One electron breaks free of its bond and becomes a **free electron**. It leaves a vacancy: a **hole**.
3. A neighbouring bond-electron can hop into the hole. The hole appears to move the opposite way. We treat holes as **positive carriers**.
4. A free electron can fall into a hole: **recombination**. Pairs are created and destroyed all the time; at a given temperature the two rates balance.

So a semiconductor carries current with **two kinds of carriers**: electrons (negative) and holes (positive).

## 1.3 Intrinsic and extrinsic semiconductors

::: kid Plain rice and seasoned rice
*Pure* (intrinsic) silicon is like plain rice: it hardly conducts. Adding a **tiny pinch of the right impurity** (doping) is like adding salt: a very small amount changes the behaviour a lot. There are two "flavours" of pinch: one adds extra free electrons (**N-type**), the other adds extra empty seats (**P-type**).
:::

| | Intrinsic (pure) | N-type | P-type |
|---|---|---|---|
| What is added | nothing | **donor** atoms (5 outer electrons: P, As, Sb) | **acceptor** atoms (3 outer electrons: B, Al, Ga, In) |
| Why | – | 4 electrons make bonds; the 5th is loose and becomes free | only 3 electrons: one bond is missing an electron, which is a hole |
| Free electrons $n$ | $n_i$ | large ($\approx N_D$) | tiny |
| Holes $p$ | $n_i$ | tiny | large ($\approx N_A$) |
| **Majority** carriers | – (equal numbers) | electrons | holes |
| **Minority** carriers | – | holes | electrons |
| Fixed ions left behind | none | positive donor ions | negative acceptor ions |

::: trap N-type is NOT negatively charged
An N-type bar has many free electrons but also exactly as many **fixed positive donor ions**. The whole bar is electrically **neutral**. Charge appears only when electrons leave their ions behind (this is how the depletion region forms in Chapter 13).
:::

::: ex Example 1.1: How strong is doping?
**Given:** silicon has about $5\times10^{22}$ atoms per cm³. At 300 K, $n_i=1.5\times10^{10}\ \text{cm}^{-3}$. We add donors at $N_D=10^{16}\ \text{cm}^{-3}$.

**Find:** how many atoms there are per free electron in pure Si, and how much doping boosts the electron count.

**Step 1: atoms per free electron (pure).** $\dfrac{5\times10^{22}}{1.5\times10^{10}}=3.3\times10^{12}$. So only one atom in about three million million has released an electron.

**Step 2: how many donor atoms per atom.** $\dfrac{10^{16}}{5\times10^{22}}=2\times10^{-7}$, i.e. one donor per 5 million atoms.

**Step 3: electron boost.** Each donor gives one electron, so $n\approx N_D=10^{16}$. Compare with $n_i$: $\dfrac{10^{16}}{1.5\times10^{10}}=6.7\times10^{5}$.

**Answer:** one donor per 5 million atoms makes the electron count about **700 000 times** larger.

**What it means:** doping is extremely powerful. A tiny pinch of impurity changes conductivity by a factor of a million.
:::

## 1.4 Two ways charge moves: drift and diffusion (preview)

* **Drift:** an electric field pushes carriers. Current density $J=\sigma E$.
* **Diffusion:** carriers spread from where they are crowded to where they are scarce, even with no field.

Chapter 12 covers both properly. The diode works because these two currents fight each other and cancel.

## 1.5 A first look at the PN diode

::: kid The one-way door
Take an N room packed with people (electrons) and a P room full of empty seats (holes). Open the door between them. People rush across and sit in empty seats near the door. But everyone who leaves the N side leaves behind a "forgotten name tag": a fixed **positive** ion. Everyone arriving on the P side fills a seat and makes a fixed **negative** ion. Those name tags build a **wall** (an electric field) that pushes back on the next people trying to cross. Soon the wall is strong enough to stop the rush.

* Push people toward the door (**forward bias**): the wall gets lower and thinner, and lots of current flows.
* Pull people away from the door (**reverse bias**): the wall gets higher and thicker, and almost no current flows.
:::

## 1.6 Practice

::: try Questions for Chapter 1
1. Why is a semiconductor an insulator at 0 K but a weak conductor at room temperature?
2. Give the majority and minority carriers of (a) N-type and (b) P-type material, and which impurity atoms make each.
3. N-type silicon has $N_D=10^{16}\ \text{cm}^{-3}$ and $n_i=1.5\times10^{10}\ \text{cm}^{-3}$. Find $n$ and $p$ using the mass-action law $np=n_i^2$.
4. Is an N-type crystal charged? Explain in one sentence.
5. Thermal energy is 0.026 eV. Estimate $e^{-E_g/k_BT}$ for silicon ($E_g=1.1$ eV) and for diamond ($E_g=7$ eV).
:::

::: soln Answers and full solutions
<details markdown="1"><summary>Solution 1</summary>

**Step 1.** At 0 K there is no heat energy, so every valence electron stays in its bond and the conduction band is empty. No free carriers means no current: insulator.
**Step 2.** At room temperature thermal energy (0.026 eV on average) can occasionally lift an electron across the small gap (1.1 eV for Si).
**Step 3.** Each jump makes a free electron and a hole, so both carry a small current.

**Answer:** it is an insulator at 0 K because nothing can cross the gap; at room temperature heat lifts a few electrons across the gap, so it conducts weakly.
</details>

<details markdown="1"><summary>Solution 2</summary>

**(a) N-type:** made by **donor** atoms with 5 outer electrons (phosphorus, arsenic, antimony). Majority = electrons. Minority = holes.
**(b) P-type:** made by **acceptor** atoms with 3 outer electrons (boron, aluminium, gallium). Majority = holes. Minority = electrons.
</details>

<details markdown="1"><summary>Solution 3</summary>

**Given:** $N_D=10^{16}$, $n_i=1.5\times10^{10}$.
**Step 1.** In N-type nearly every donor gives one electron: $n\approx N_D=10^{16}\ \text{cm}^{-3}$.
**Step 2.** Mass-action law: $np=n_i^2$, so $p=\dfrac{n_i^2}{n}$.
**Step 3.** $n_i^2=(1.5\times10^{10})^2=2.25\times10^{20}$.
**Step 4.** $p=\dfrac{2.25\times10^{20}}{10^{16}}=2.25\times10^{4}\ \text{cm}^{-3}$.

**Answer:** $n=10^{16}\ \text{cm}^{-3}$ and $p=2.25\times10^{4}\ \text{cm}^{-3}$. The holes are a trillion times fewer than the electrons.
</details>

<details markdown="1"><summary>Solution 4</summary>

No. An N-type crystal has as many fixed positive donor ions as it has free electrons, so the total charge is zero.
</details>

<details markdown="1"><summary>Solution 5</summary>

**Step 1.** Silicon: $E_g/k_BT=1.1/0.026=42.3$, so $e^{-42.3}=4\times10^{-19}$.
**Step 2.** Diamond: $7/0.026=269$, so $e^{-269}\approx10^{-117}$.

**Answer:** silicon about $10^{-18}$, diamond about $10^{-117}$ (essentially zero). This is why diamond is an insulator.
</details>
:::
