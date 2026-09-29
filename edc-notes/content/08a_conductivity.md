# Chapter 11: Conductivity, carrier concentration, Fermi level

*Class notes pp. 11–18 · slides: EDC Current densities (handwritten)*

::: words
| Word / symbol | Plain meaning |
|---|---|
| $\sigma$ | **conductivity**: how easily the material carries current (unit S/cm) |
| $\rho$ | **resistivity** $=1/\sigma$ (unit Ω·cm). (In Ch. 13 $\rho$ also means charge density.) |
| $\mu_n$, $\mu_p$ | **mobility** of electrons, holes: drift speed per unit field (cm²/V·s) |
| $n$, $p$ | free-electron and hole concentrations (per cm³) |
| $n_i$ | intrinsic concentration: $n=p=n_i$ in pure material |
| $J$ | **current density**: current per unit area (A/cm²) |
| $E$ | electric field (V/cm) |
| $q$ | charge of an electron, $1.6\times10^{-19}$ C |
| $N_D$, $N_A$ | donor and acceptor concentrations |
| $E_c$, $E_v$ | energy of the bottom of the conduction band, top of the valence band |
| $E_F$ | **Fermi level**: energy at which the chance of an electron being present is ½ |
| $E_g$ | energy gap $=E_c-E_v$ |
| $N_c$, $N_v$ | effective density of states in the conduction, valence band |
| $f(E)$ | Fermi–Dirac function: probability that an energy level is filled |
| $kT$ | thermal energy; 0.0259 eV at 300 K ($k$ in eV/K) |
| Mass-action law | $np=n_i^2$ |
| $T$ | absolute temperature in kelvin |
:::

::: kid How well does a material carry electricity?
Picture a corridor with people carrying buckets of water. How much water is delivered depends on (a) **how many** people there are ($n$, $p$), (b) **how fast** each moves when pushed ($\mu$, the mobility), and (c) **how big a bucket** each carries ($q$, the charge). Multiply them and you get the **conductivity** $\sigma$. Silicon has two kinds of bucket-carriers, electrons and holes, so you add both.
:::

## 11.1 Conductivity of a semiconductor

In a pure semiconductor $n=p$. Whenever an electron–hole pair is created, two carriers exist: a free electron with mobility $\mu_n$ and a hole with mobility $\mu_p$.

Total drift current density:
$$J=J_n+J_p=q\,n\,\mu_nE+q\,p\,\mu_pE=(n\mu_n+p\mu_p)\,qE=\sigma E$$

* $J_n$, $J_p$ = electron and hole drift current densities. $E$ = applied field.

$$\boxed{\sigma=(n\mu_n+p\mu_p)\,q},\qquad\text{resistivity }\rho=\frac1\sigma$$

* **Intrinsic** ($n=p=n_i$): $\boxed{\sigma_i=q\,n_i(\mu_n+\mu_p)}$. It depends on $n_i$, $\mu_n$ and $\mu_p$.
* **N-type** ($n\gg p$): $\sigma\approx q\,n\,\mu_n$.
* **P-type** ($p\gg n$): $\sigma\approx q\,p\,\mu_p$.

::: ex Example 11.1: Your class problem, intrinsic conductivity of Ge and Si
*Mobilities of free electrons and holes in pure germanium are 3800 and 1800 cm²/V·s; for pure silicon 1300 and 500. Find the intrinsic conductivities. Take $n_i=2.5\times10^{13}\ \text{cm}^{-3}$ (Ge) and $1.5\times10^{10}$ (Si) at room temperature.*

**Formula:** $\sigma_i=q\,n_i(\mu_n+\mu_p)$.

**Germanium**
* **Step 1:** $\mu_n+\mu_p=3800+1800=5600\ \text{cm}^2/\text{V·s}$.
* **Step 2:** $q\,n_i=1.6\times10^{-19}\times2.5\times10^{13}=4.0\times10^{-6}$.
* **Step 3:** $\sigma_i=4.0\times10^{-6}\times5600=0.0224$ S/cm.

**Silicon**
* **Step 1:** $\mu_n+\mu_p=1300+500=1800$.
* **Step 2:** $q\,n_i=1.6\times10^{-19}\times1.5\times10^{10}=2.4\times10^{-9}$.
* **Step 3:** $\sigma_i=2.4\times10^{-9}\times1800=4.32\times10^{-6}$ S/cm.

**Answer:** $\sigma_{Ge}=\mathbf{0.0224\ S/cm}$; $\sigma_{Si}=\mathbf{4.32\times10^{-6}\ S/cm}$.

**What it means:** germanium conducts about 5000 times better than silicon at room temperature because its smaller gap gives a much larger $n_i$.
:::

## 11.2 Carrier concentration in an intrinsic semiconductor

**Electrons in the conduction band:** add up (integrate) the electrons at every energy above $E_c$: $n=\displaystyle\int_{E_c}^{\infty}N(E)f(E)\,dE$.

* **Density of states** (how many energy slots per unit energy) $N(E)=\gamma\,(E-E_c)^{1/2}$ with $\gamma=\dfrac{4\pi}{h^3}(2m_n)^{3/2}(1.602\times10^{-19})^{3/2}$; $m_n$ is the effective mass of the electron and $h$ is Planck's constant.
* **Fermi–Dirac probability** that a slot is filled: $f(E)=\dfrac{1}{1+e^{(E-E_F)/kT}}$.

For $E\ge E_c$ with $E-E_F\gg kT$ this becomes the "Boltzmann tail": $f(E)\approx e^{-(E-E_F)/kT}$.

{{fig p_fermi|Left: the Fermi–Dirac function at three temperatures. Right: where the Fermi level sits in N-type, intrinsic and P-type material.|95}}

**Derivation, step by step (as in your notes):**

**Step 1.** $n=\displaystyle\int_{E_c}^{\infty}\gamma(E-E_c)^{1/2}e^{-(E-E_F)/kT}dE$.
**Step 2: substitute** $E-E_c=x^2$, so $dE=2x\,dx$; at $E=E_c$, $x=0$; at $E=\infty$, $x=\infty$.
**Step 3.** $n=2\gamma\,e^{-(E_c-E_F)/kT}\displaystyle\int_0^\infty x^2e^{-x^2/kT}dx$.
**Step 4: use the standard integral** $\displaystyle\int_0^\infty x^{2n}e^{-x^2/a^2}dx=\sqrt\pi\dfrac{(2n)!}{n!}\left(\dfrac a2\right)^{2n+1}$ with $n=1$ and $a=\sqrt{kT}$.
**Step 5.** After simplifying:
$$\boxed{n=N_c\,e^{-(E_c-E_F)/kT}},\qquad N_c=2\left(\frac{2\pi m_nkT}{h^2}\right)^{3/2}(1.602\times10^{-19})^{3/2}.$$

**Holes in the valence band.** The probability that a level is **empty** is $1-f(E)\approx e^{-(E_F-E)/kT}$ for $E\le E_v$ and $E_F-E\gg kT$, and $N(E)=\gamma(E_v-E)^{1/2}$. Doing the same integral:
$$\boxed{p=N_v\,e^{-(E_F-E_v)/kT}},\qquad N_v=2\left(\frac{2\pi m_pkT}{h^2}\right)^{3/2}(1.602\times10^{-19})^{3/2}$$
($m_p$ = effective mass of the hole).

## 11.3 Fermi level in an intrinsic semiconductor

Pure material must be electrically neutral, so $n_i=p_i$:

**Step 1.** $N_ce^{-(E_c-E_F)/kT}=N_ve^{-(E_F-E_v)/kT}$.
**Step 2.** Divide: $\dfrac{N_c}{N_v}=e^{(E_c-E_F-E_F+E_v)/kT}=e^{(E_c+E_v-2E_F)/kT}$.
**Step 3.** Take the natural log: $\ln\dfrac{N_c}{N_v}=\dfrac{E_c+E_v-2E_F}{kT}$.
**Step 4.** Solve for $E_F$:
$$\boxed{E_F=\frac{E_c+E_v}{2}-\frac{kT}{2}\ln\frac{N_c}{N_v}}\qquad\text{If }N_c=N_v:\ E_F=\frac{E_c+E_v}{2}.$$
So in pure material the Fermi level sits (about) **in the middle of the gap**.

## 11.4 Fermi level in a doped semiconductor

$$\text{N-type: }\boxed{E_F=E_c-kT\ln\frac{N_c}{N_D}},\qquad\text{P-type: }\boxed{E_F=E_v+kT\ln\frac{N_v}{N_A}}$$
where $N_D=N_ce^{-(E_c-E_F)/kT}$ and $N_A=N_ve^{-(E_F-E_v)/kT}$.

* N-type: $E_F$ is **just below $E_c$** (near the donor level $E_D$). More donors → $E_F$ moves **up toward $E_c$**.
* P-type: $E_F$ is **just above $E_v$** (near the acceptor level $E_A$). More acceptors → $E_F$ moves **down toward $E_v$**.

::: ex Example 11.2: Fermi level and temperature (class problem)
*In an N-type semiconductor the Fermi level is 0.3 eV below the conduction band at 300 K. If the temperature increases to 360 K, find the new position of the Fermi level.*

**Given:** $(E_c-E_F)_1=0.3$ eV at $T_1=300$ K; $T_2=360$ K.

**Formula:** $E_c-E_F=kT\ln(N_c/N_D)$.

**Step 1.** Write it for both temperatures: $(E_c-E_F)_1=kT_1\ln\dfrac{N_c}{N_D}$ and $(E_c-E_F)_2=kT_2\ln\dfrac{N_c}{N_D}$.
**Step 2.** Divide and treat $\ln(N_c/N_D)$ as constant (the class assumption): $\dfrac{(E_c-E_F)_2}{(E_c-E_F)_1}=\dfrac{T_2}{T_1}=\dfrac{360}{300}=1.2$.
**Step 3.** $(E_c-E_F)_2=0.3\times1.2=0.36$ eV.

**Answer:** the Fermi level is now **0.36 eV below $E_c$**, i.e. it moved *away* from the conduction band.

::: flag Assumption
Treating $N_c/N_D$ as constant is an idealisation (in reality $N_c\propto T^{3/2}$ also changes). Use it exactly as taught.
:::
:::

::: ex Example 11.3: Doping changes the Fermi level (class problem)
*In an N-type semiconductor the Fermi level is 0.2 eV below the conduction band. Find the new position if the donor concentration is increased by a factor of 4. Take $kT=0.025$ eV.*

**Given:** $E_c-E_{F0}=0.2$ eV, $N_D\to4N_D$, $kT=0.025$ eV.

**Formula:** $N_D=N_ce^{-(E_c-E_F)/kT}$.

**Step 1: before.** $N_{D0}=N_ce^{-0.2/0.025}=N_ce^{-8}$.
**Step 2: after.** $4N_{D0}=N_ce^{-(E_c-E_{F1})/0.025}$.
**Step 3: divide the two.** $4=e^{-(E_c-E_{F1})/0.025+8}$.
**Step 4: natural log.** $\ln4=8-\dfrac{E_c-E_{F1}}{0.025}$, and $\ln4=1.386$.
**Step 5: solve.** $\dfrac{E_c-E_{F1}}{0.025}=8-1.386=6.614$, so $E_c-E_{F1}=6.614\times0.025=0.165$ eV.

**Answer:** **0.165 eV** below $E_c$.

**Check by shortcut:** the shift is $kT\ln4=0.025\times1.386=0.0347$ eV, and $0.2-0.0347=0.165$ ✓. **Meaning:** more donors push $E_F$ upward, closer to the conduction band.
:::

## 11.5 Mass-action law and charge densities

$$\boxed{n\,p=n_i^2}$$
This holds whether the crystal is pure or doped, at a given temperature. Proof from the formulas above: $np=N_cN_v\,e^{-(E_c-E_v)/kT}=N_cN_ve^{-E_g/kT}=n_i^2$.

**Charge neutrality in N-type:** $n_N=N_D+p_N\approx N_D$ (because $p_N$ is tiny), and $p_N=\dfrac{n_i^2}{n_N}\approx\dfrac{n_i^2}{N_D}\ll n_N$.
**In P-type:** $p_P=N_A+n_P\approx N_A$, and $n_P=\dfrac{n_i^2}{p_P}\approx\dfrac{n_i^2}{N_A}\ll p_P$.

**Extrinsic conductivity:** $\sigma_N=qn_N\mu_n\approx qN_D\mu_n$ and $\sigma_P=qp_P\mu_p\approx qN_A\mu_p$.

::: ex Example 11.4: Mixed doping (class problem)
*A sample at temperature $T$ in intrinsic condition has resistivity $2.5\times10^{4}\ \Omega\cdot$cm. It is doped with $4\times10^{10}$ donors/cm³ and $10^{10}$ acceptors/cm³. Find the total conduction current density for $E=4$ V/cm. $\mu_n=1250$, $\mu_p=475$ cm²/V·s.*

**Given:** $\rho_i=2.5\times10^{4}\ \Omega$·cm; $N_D=4\times10^{10}$; $N_A=10^{10}$; $E=4$ V/cm; $\mu_n=1250$; $\mu_p=475$.

**Find:** $J$.

**Step 1: intrinsic conductivity.** $\sigma_i=1/\rho_i=1/(2.5\times10^{4})=4\times10^{-5}$ S/cm.
**Step 2: find $n_i$.** $\sigma_i=qn_i(\mu_n+\mu_p)$ ⇒ $n_i=\dfrac{\sigma_i}{q(\mu_n+\mu_p)}=\dfrac{4\times10^{-5}}{1.6\times10^{-19}\times1725}=1.45\times10^{10}\ \text{cm}^{-3}$.
**Step 3: net doping.** Donors and acceptors partly cancel: $n\approx N_D-N_A=4\times10^{10}-10^{10}=3\times10^{10}$ cm⁻³.
**Step 4: holes (mass-action law).** $p=\dfrac{n_i^2}{n}=\dfrac{(1.45\times10^{10})^2}{3\times10^{10}}=\dfrac{2.10\times10^{20}}{3\times10^{10}}=0.70\times10^{10}$ cm⁻³.
**Step 5: conductivity.** $\sigma=q(n\mu_n+p\mu_p)=1.6\times10^{-19}(3\times10^{10}\times1250+0.7\times10^{10}\times475)$.
The bracket: $3.75\times10^{13}+3.33\times10^{12}=4.08\times10^{13}$. So $\sigma=1.6\times10^{-19}\times4.08\times10^{13}=6.5\times10^{-6}$ S/cm ($=0.65\times10^{-5}$).
**Step 6: current density.** $J=\sigma E=6.5\times10^{-6}\times4=2.6\times10^{-5}$ A/cm².

**Answer:** $J=\mathbf{2.6\times10^{-5}\ A/cm^{2}}$ (matches your class answer).
:::

::: ex Example 11.5: Minority carrier concentration (class problem)
*Si PN junction at 300 K, $n_i=1.5\times10^{10}\ \text{cm}^{-3}$, N-type doping $1\times10^{10}\ \text{cm}^{-3}$, forward bias 0.6 V. Find the minority-hole concentration at the edge of the space-charge region.*

**Class solution (equilibrium value):**
**Step 1.** Mass-action law: $p=n_i^2/N_D$.
**Step 2.** $p=\dfrac{(1.5\times10^{10})^2}{10^{10}}=\dfrac{2.25\times10^{20}}{10^{10}}=2.25\times10^{10}\ \text{cm}^{-3}$.

**Answer:** $2.25\times10^{10}\ \text{cm}^{-3}$.

::: flag What this does and does not do
The class calculation gives the **thermal-equilibrium** hole density $p_{n0}=n_i^2/N_D$ in the N-region. Under forward bias $V$, the value at the depletion edge is larger: $p_{n0}\,e^{V/V_T}$ (the "law of the junction"). The class stopped at $p_{n0}$; write it as taught. (Because $N_D$ here is close to $n_i$, the approximation $n\approx N_D$ is also rough.)
:::
:::

## 11.6 Variation with temperature

* $n=N_ce^{-(E_c-E_F)/kT}$, $p=N_ve^{-(E_F-E_v)/kT}$, so $np=N_cN_ve^{-E_g/kT}$.
* **Intrinsic concentration is extremely temperature sensitive:**
$$n_i^2=A_0T^3e^{-E_{G0}/kT}$$
($A_0$ is a constant independent of temperature; $E_{G0}$ is the gap at 0 K in eV; $k=8.617\times10^{-5}$ eV/K).
* In an **intrinsic** semiconductor, $T\uparrow\Rightarrow n_i\uparrow\Rightarrow\sigma\uparrow$.
* In an **N-type** semiconductor the number of free electrons $n$ hardly changes with temperature (set by $N_D$). In **P-type** the number of holes is likewise fixed (the class notes' remark that free electrons in P-type rise with temperature refers to the **minority** electrons).
* **Conductivity** rises with temperature because the number of pairs rises even though mobility falls: $\sigma=\sigma_0[1+\alpha(T-T_0)]$ (class form).
* **The energy gap decreases** with temperature: $E_G(T)=E_{G0}-\beta T$.

{{fig p_ni_temp|$n_i^2$ grows exponentially with $T$; the majority concentration in doped material is nearly constant.|62}}

::: ex Example 11.6: How much does $n_i$ change for a 50 K rise?
**Given:** silicon, $E_g\approx1.1$ eV, from 300 K to 350 K.

**Formula:** $n_i\propto T^{3/2}e^{-E_g/2kT}$, so $\dfrac{n_i(350)}{n_i(300)}=\left(\dfrac{350}{300}\right)^{3/2}\exp\!\left[-\dfrac{E_g}{2k}\left(\dfrac1{350}-\dfrac1{300}\right)\right]$.

**Step 1: power term.** $(350/300)^{1.5}=1.1667^{1.5}=1.260$.
**Step 2: the bracket.** $\dfrac1{350}-\dfrac1{300}=0.0028571-0.0033333=-0.00047619$.
**Step 3: the exponent.** $\dfrac{E_g}{2k}=\dfrac{1.1}{2\times8.617\times10^{-5}}=6382.6$ K, so exponent $=-6382.6\times(-0.00047619)=+3.039$.
**Step 4.** $e^{3.039}=20.9$.
**Step 5.** Ratio $=1.260\times20.9=26.3$.

**Answer:** $n_i$ becomes about **26 times larger** for just a 50 K rise.
:::

## 11.7 Practice

::: try Questions for Chapter 11
1. Write $\sigma$ for intrinsic, N-type and P-type material.
2. N-type Si has $N_D=10^{16}\ \text{cm}^{-3}$ and $N_c=2.8\times10^{19}\ \text{cm}^{-3}$ at 300 K ($kT=0.02585$ eV). How far below $E_c$ is $E_F$?
3. State the mass-action law. If $N_D=5\times10^{15}$ and $n_i=1.5\times10^{10}$, find $p$.
4. An N-type semiconductor has $E_c-E_F=0.25$ eV at 300 K. Find $E_c-E_F$ at 450 K (class method).
5. Does the Fermi level lie above or below the middle of the gap in P-type material?
6. N-type Ge: $N_D=10^{15}\ \text{cm}^{-3}$, $\mu_n=3800\ \text{cm}^2/\text{V·s}$. Find $\sigma$ and the current density for $E=10$ V/cm.
:::

::: soln Answers and full solutions
<details markdown="1"><summary>Solution 1</summary>

* Intrinsic: $\sigma_i=q\,n_i(\mu_n+\mu_p)$.
* N-type: $\sigma\approx q\,n\,\mu_n\approx qN_D\mu_n$.
* P-type: $\sigma\approx q\,p\,\mu_p\approx qN_A\mu_p$.
</details>

<details markdown="1"><summary>Solution 2</summary>

**Formula:** $E_c-E_F=kT\ln\dfrac{N_c}{N_D}$.
**Step 1.** $\dfrac{N_c}{N_D}=\dfrac{2.8\times10^{19}}{10^{16}}=2800$.
**Step 2.** $\ln2800=7.937$.
**Step 3.** $E_c-E_F=0.02585\times7.937=0.2052$ eV.

**Answer:** about **0.205 eV** below $E_c$.
</details>

<details markdown="1"><summary>Solution 3</summary>

**Law:** $np=n_i^2$.
**Step 1.** $n\approx N_D=5\times10^{15}$.
**Step 2.** $p=n_i^2/n=\dfrac{(1.5\times10^{10})^2}{5\times10^{15}}=\dfrac{2.25\times10^{20}}{5\times10^{15}}=4.5\times10^{4}\ \text{cm}^{-3}$.
</details>

<details markdown="1"><summary>Solution 4</summary>

**Class method:** $E_c-E_F\propto T$.
**Step 1.** Ratio $=450/300=1.5$.
**Step 2.** $0.25\times1.5=0.375$ eV.

**Answer:** **0.375 eV**.
</details>

<details markdown="1"><summary>Solution 5</summary>

**Below** the middle of the gap, close to the valence band ($E_F=E_v+kT\ln(N_v/N_A)$).
</details>

<details markdown="1"><summary>Solution 6</summary>

**Step 1.** $\sigma=q\,n\,\mu_n$ with $n\approx N_D=10^{15}$.
**Step 2.** $\sigma=1.6\times10^{-19}\times10^{15}\times3800=0.608$ S/cm.
**Step 3.** $J=\sigma E=0.608\times10=6.08$ A/cm².

**Answer:** $\sigma=0.608$ S/cm; $J=6.08\ \text{A/cm}^2$.
</details>
:::
