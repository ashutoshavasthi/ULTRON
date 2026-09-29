# Chapter 1: Foundations from zero

::: kid The whole idea in one picture
Imagine a huge **cinema**. The seats in the lower floor are all full (the **valence band**). The upper balcony is completely empty (the **conduction band**). A person can only move around freely if there is space to move, so people in the full lower floor are stuck. To move, a person has to jump up to the balcony.

* In a **metal** the balcony is right next to (even overlapping) the full floor, so people move around all the time: electricity flows easily.
* In an **insulator** the balcony is miles above. Nobody can jump that far: no electricity.
* In a **semiconductor** (silicon, germanium) the balcony is a *short hop* away. A little heat or light and a few people jump up. That is why we can **control** how well it conducts, which is the whole magic of electronics.

When a person jumps up, they leave an **empty seat** behind. People next to the empty seat shuffle into it, and the empty seat appears to move the other way. That moving empty seat is called a **hole**, and it behaves like a positive charge.
:::

## 1.1 Energy bands in solids

### From single atoms to bands

* An isolated atom can only have certain **allowed energies** for its electrons (quantised levels).
* When many atoms form a **crystal**, the outer-shell electrons are shared between neighbours and feel each other’s fields, so each level **splits into many closely spaced levels**. A huge number of tightly packed levels is a **band**.
* Inner-shell (completely filled) electrons are hardly disturbed. It is the outermost shells that spread into bands.
* Silicon has atomic number 14. Its configuration is $1s^2\,2s^2\,2p^6\,3s^2\,3p^2$ (four outer electrons). For $N$ silicon atoms you get $N$ lattice sites and, for the outer levels, two bands: the **valence band** (highest filled) and the **conduction band** (empty at 0 K), separated by the **forbidden energy gap** $E_g$.

{{fig p_bands|Energy bands of a metal, a semiconductor and an insulator. Electrons can only sit in the coloured bands.|92}}

| | Metal | Semiconductor | Insulator |
|---|---|---|---|
| Gap $E_g$ | none (partly filled band, or bands overlap) | small: Si **1.1 eV**, Ge **0.74 eV** | large: about **6 eV**, diamond **7 eV** |
| At 0 K | conducts | insulator (valence band full, conduction band empty) | insulator |
| At room temperature | conducts very well | a few electrons jump the gap and it conducts a little | practically none |

::: class In your slides (Unit-I First part)
* **Metals:** two possibilities: the conduction band is only *partially filled*, or it *overlaps* the valence band. Either way electrons overflow into empty levels with almost no extra energy.
* The highest energy level occupied by electrons at **absolute zero** is the **Fermi level**; its energy is the **Fermi energy**.
* **Semiconductors:** at 0 K no electron can jump the gap so the crystal is an insulator. At room temperature some valence electrons gain more than $E_g$ and jump. The fraction is proportional to $e^{-E_g/k_BT}$, so it is “sizeable” only because $E_g$ is small.
* **Insulators:** $E_g\approx 6$ eV; “however heated” electrons practically cannot cross.
:::

::: formula Energy unit you will keep meeting
$1\ \text{eV}=1.6\times10^{-19}\ \text{J}$ = the energy one electron gains crossing 1 volt. Thermal energy at room temperature is only $k_BT\approx0.026$ eV, much smaller than $E_g=1.1$ eV. That is why only a *tiny* fraction of electrons jump the gap.
:::

## 1.2 Electrons and holes

1. In pure silicon each atom shares its 4 outer electrons with 4 neighbours (**covalent bonds**): every bond is a pair of shared electrons, so at 0 K there are no free carriers.
2. Add energy (heat, light). One electron breaks its bond and becomes a **free electron** (in the conduction band). It leaves behind a vacancy: a **hole** (a missing bond, an unfilled level in the valence band).
3. A neighbouring bond-electron can hop into the hole; the hole appears to move the opposite way. Mathematically we treat holes as **positive charge carriers**.
4. A free electron can fall into a hole. This is **recombination** (electron–hole pair disappears).

So a semiconductor carries current with **two kinds of carriers**: electrons (negative) and holes (positive).

## 1.3 Intrinsic and extrinsic semiconductors

::: kid Pure vs. “seasoned”
*Pure* (intrinsic) silicon is like plain rice: it hardly conducts. Adding a **tiny pinch of the right impurity** (doping) is like adding salt: a very small amount changes the behaviour completely. There are two "flavours" of pinch: one adds extra free electrons (**N-type**), the other adds extra empty seats (**P-type**).
:::

| | Intrinsic (pure) | N-type | P-type |
|---|---|---|---|
| What is added | nothing | **donor** atoms (5 outer electrons: P, As, Sb) | **acceptor** atoms (3 outer electrons: B, Al, Ga, In) |
| Free electrons $n$ | $=n_i$ | large ($\approx N_D$) | tiny |
| Holes $p$ | $=n_i$ | tiny | large ($\approx N_A$) |
| **Majority** carriers | none: $n=p$ | electrons | holes |
| **Minority** carriers | — | holes | electrons |
| Fixed ions left behind | none | positive donor ions ($N_D^+$) | negative acceptor ions ($N_A^-$) |

::: trap N-type is NOT negatively charged
An N-type bar has lots of free electrons but also exactly as many **fixed positive donor ions**. The whole bar is electrically **neutral**. This is the key to understanding the depletion region later: charge appears only when electrons leave their ions behind.
:::

### How tiny is doping?
Silicon has about $5\times10^{22}$ atoms per cm³, while $n_i\approx1.5\times10^{10}\ \text{cm}^{-3}$ at 300 K, roughly one free electron for every $3\times10^{12}$ atoms. Adding one donor per five million atoms ($N_D=10^{16}\ \text{cm}^{-3}$) makes the electron concentration about **$10^{6}$ times bigger** than the intrinsic value. That is the power of doping.

## 1.4 Two ways charge moves: drift and diffusion (preview)

* **Drift:** an electric field pushes carriers. Current density $J=\sigma E$.
* **Diffusion:** carriers spread from where they are crowded to where they are scarce (even with no field). Current density $\propto$ concentration gradient.

Both are studied properly in Chapter 12. The diode works *because* these two currents fight each other and balance out.

## 1.5 A first look at the PN diode

::: kid The one-way door
Take an N room packed with people (electrons) and a P room full of empty seats (holes). Open the door between them. People rush across and sit down in the empty seats near the door. But everybody who leaves the N side leaves behind a “forgotten name tag”: a fixed **positive** ion. Everybody who arrives on the P side fills a seat and creates a fixed **negative** ion. Those name tags build a **wall** (an electric field) that pushes back on the next people trying to cross. Soon the wall is strong enough to stop the rush: **no more net movement**.

* Push people toward the door (**forward bias**) and the wall gets lower and thinner: lots of current.
* Pull people away from the door (**reverse bias**) and the wall gets higher and thicker: almost no current.
:::

That one-way behaviour is what Chapters 2–15 use again and again.

## 1.6 Try it yourself

::: try Chapter 1 questions
1. Why is a semiconductor an insulator at 0 K but a (weak) conductor at room temperature?
2. Give the majority and minority carriers of (a) N-type, (b) P-type material. Which impurity atoms make each?
3. N-type silicon has $N_D=10^{16}\ \text{cm}^{-3}$ and $n_i=1.5\times10^{10}\ \text{cm}^{-3}$. Estimate $n$ and $p$ (mass-action law: $np=n_i^2$).
4. Is an N-type crystal charged? Explain in one sentence.

<details markdown="1"><summary>Answers</summary>

1. At 0 K every valence electron is in its bond and none has energy to cross $E_g$. At 300 K thermal energy lifts a few electrons across the small gap (fraction $\propto e^{-E_g/k_BT}$), leaving holes behind, so both carriers exist.
2. (a) majority electrons, minority holes, donors (P, As, Sb). (b) majority holes, minority electrons, acceptors (B, Al, Ga).
3. $n\approx N_D=10^{16}\ \text{cm}^{-3}$; $p=n_i^2/n=(1.5\times10^{10})^2/10^{16}=2.25\times10^{4}\ \text{cm}^{-3}$.
4. No. It has as many fixed positive donor ions as free electrons, so it is neutral overall.
</details>
:::
