# Chapter 11: Conductivity, carrier concentration, Fermi level

*Class notes pp. 11–18 · slides: EDC Current densities (handwritten)*

::: kid How well does a material carry electricity?
Picture a corridor with people carrying buckets. **How much water is delivered** depends on (a) *how many* people there are ($n$, $p$), (b) *how fast* each one moves when pushed ($\mu$, the mobility), and (c) *how big a bucket* each carries ($q$, the charge). Multiply them and you get the **conductivity** $\sigma$. Silicon has two kinds of “bucket-carriers”, electrons and holes, so you add both.
:::

## 11.1 Conductivity of a semiconductor

In a pure semiconductor $n=p$. Whenever an electron–hole pair is created, two carriers exist: a free electron with mobility $\mu_n$ and a hole with mobility $\mu_p$.

Total current density (drift):
$$J=J_n+J_p=q\,n\,\mu_nE+q\,p\,\mu_pE=(n\mu_n+p\mu_p)\,qE=\sigma E$$

| Symbol | Meaning |
|---|---|
| $J_n$, $J_p$ | electron and hole drift current densities |
| $n$, $p$ | free-electron and hole concentrations (per unit volume) |
| $\mu_n$, $\mu_p$ | mobilities |
| $E$ | applied electric field (V/m or V/cm) |
| $q$ | charge of electron/hole, $1.6\times10^{-19}$ C |

$$\boxed{\sigma=(n\mu_n+p\mu_p)\,q},\qquad\text{resistivity }\rho=\frac1\sigma$$

* **Intrinsic** ($n=p=n_i$): $J=n_i(\mu_n+\mu_p)qE$ and $\boxed{\sigma_i=q\,n_i(\mu_n+\mu_p)}$. It depends on $n_i$, $\mu_n$, $\mu_p$.
* **N-type** ($n\gg p$): $\sigma\approx q\,n\,\mu_n$.  **P-type** ($p\gg n$): $\sigma\approx q\,p\,\mu_p$.

::: ex Example 11.1 (class problem)
*Mobilities of free electrons and holes in pure Ge are 3800 and 1800 cm²/V·s. For pure Si they are 1300 and 500. Find the intrinsic conductivities. Take $n_i=2.5\times10^{13}\ \text{cm}^{-3}$ (Ge) and $1.5\times10^{10}$ (Si) at room temperature.*

Germanium: $\sigma_i=qn_i(\mu_n+\mu_p)=1.6\times10^{-19}\times2.5\times10^{13}\times(3800+1800)=\mathbf{0.0224\ S/cm}$

Silicon: $\sigma_i=1.6\times10^{-19}\times1.5\times10^{10}\times(1300+500)=\mathbf{4.32\times10^{-6}\ S/cm}$

Ge conducts about 5000× better than Si at room temperature because its smaller gap gives a much larger $n_i$.
:::

## 11.2 Carrier concentration in an intrinsic semiconductor

**Electrons in the conduction band:** count electrons over all energies above $E_c$: $n=\int_{E_c}^{\infty}N(E)f(E)\,dE$.

* **Density of states** $N(E)=\gamma\,(E-E_c)^{1/2}$, with $\gamma=\dfrac{4\pi}{h^3}(2m_n)^{3/2}(1.602\times10^{-19})^{3/2}$ ($m_n$ = effective mass of the electron).
* **Fermi–Dirac probability** $f(E)=\dfrac{1}{1+e^{(E-E_F)/kT}}$, with $E_F$ the Fermi level (characteristic energy of the crystal, in eV).

For $E\ge E_c$ and $E-E_F\gg kT$, $f(E)\approx e^{-(E-E_F)/kT}$ (the “Boltzmann tail”).

{{fig p_fermi|Left: the Fermi–Dirac function at three temperatures. Right: where the Fermi level sits in N-type, intrinsic and P-type material.|95}}

Substituting $E-E_c=x^2$ ($dE=2x\,dx$) and using $\int_0^\infty x^{2n}e^{-x^2/a^2}dx=\sqrt\pi\frac{(2n)!}{n!}\left(\frac a2\right)^{2n+1}$ with $n=1$, $a=\sqrt{kT}$ gives (your notes derive this line by line):
$$\boxed{n=N_c\,e^{-(E_c-E_F)/kT}},\qquad N_c=2\left(\frac{2\pi m_nkT}{h^2}\right)^{3/2}(1.602\times10^{-19})^{3/2}$$

**Holes in the valence band:** the probability that a level is *empty* is $1-f(E)=\dfrac{e^{(E-E_F)/kT}}{1+e^{(E-E_F)/kT}}\approx e^{-(E_F-E)/kT}$ for $E_F-E\gg kT$, $E\le E_v$, and $N(E)=\gamma(E_v-E)^{1/2}$. Then
$$\boxed{p=N_v\,e^{-(E_F-E_v)/kT}},\qquad N_v=2\left(\frac{2\pi m_pkT}{h^2}\right)^{3/2}(1.602\times10^{-19})^{3/2}$$
($m_p$ = effective mass of the hole).

## 11.3 Fermi level in an intrinsic semiconductor

Charge neutrality requires $n_i=p_i$:
$$N_ce^{-(E_c-E_F)/kT}=N_ve^{-(E_F-E_v)/kT}\ \Rightarrow\ \ln\frac{N_c}{N_v}=\frac{E_c+E_v-2E_F}{kT}$$
$$\boxed{E_F=\frac{E_c+E_v}{2}-\frac{kT}{2}\ln\frac{N_c}{N_v}}\qquad\text{if }N_c=N_v:\ E_F=\frac{E_c+E_v}{2}$$
So in an intrinsic semiconductor the Fermi level is (about) **in the middle of the gap**.

## 11.4 Fermi level in a semiconductor with impurities

$$\text{N-type: }\boxed{E_F=E_c-kT\ln\frac{N_c}{N_D}},\qquad\text{P-type: }\boxed{E_F=E_v+kT\ln\frac{N_v}{N_A}}$$
where $N_D=N_ce^{-(E_c-E_F)/kT}$ is the donor concentration and $N_A=N_ve^{-(E_F-E_v)/kT}$ the acceptor concentration.

* N-type: $E_F$ lies **just below $E_c$** (close to the donor level $E_D$). More donors → $E_F$ moves **up** toward $E_c$.
* P-type: $E_F$ lies **just above $E_v$** (close to the acceptor level $E_A$). More acceptors → $E_F$ moves **down** toward $E_v$.

::: ex Example 11.2 (class: Fermi level vs temperature)
*In an N-type semiconductor the Fermi level is 0.3 eV below the conduction level at 300 K. If the temperature increases to 360 K, find the new position of the Fermi level.*

From $E_c-E_F=kT\ln(N_c/N_D)$ and treating $\ln(N_c/N_D)$ as constant:
$$\frac{(E_c-E_F)_2}{(E_c-E_F)_1}=\frac{T_2}{T_1}=\frac{360}{300}\Rightarrow(E_c-E_F)_2=0.3\times1.2=\mathbf{0.36\ eV}\text{ below }E_c.$$
::: flag Assumption
The class answer treats $N_c/N_D$ as constant. In reality $N_c\propto T^{3/2}$ also changes and the donors become fully ionised, so this is an idealised exam calculation. Use it exactly as taught.
:::
:::

::: ex Example 11.3 (class: doping changes)
*In an N-type semiconductor the Fermi level is 0.2 eV below the conduction band. Find the new position if the donor concentration is increased by a factor 4. Take $kT=0.025$ eV.*

Initially $N_{D0}=N_ce^{-0.2/0.025}=N_ce^{-8}$. After: $4N_{D0}=N_ce^{-(E_c-E_{F1})/0.025}$.
$$4e^{-8}=e^{-40(E_c-E_{F1})}\Rightarrow\ln4-8=-40(E_c-E_{F1})\Rightarrow E_c-E_{F1}=\frac{8-1.386}{40}=\mathbf{0.165\ eV}$$
The Fermi level moves **closer** to $E_c$ (from 0.2 to 0.165 eV): more donors push it up. Shortcut: $\Delta=kT\ln4=0.0347$ eV, and $0.2-0.0347=0.165$ ✓.
:::

## 11.5 Mass-action law and charge densities

$$\boxed{n\,p=n_i^2}$$
(product of electron and hole concentrations is a constant at a given temperature, whether the crystal is pure or doped). Proof from the formulas above: $np=N_cN_ve^{-(E_c-E_v)/kT}=N_cN_ve^{-E_g/kT}=n_i^2$.

**Charge neutrality in N-type:** $n_N=N_D+p_N\approx N_D$ (since $p_N$ is tiny), and $p_N=\dfrac{n_i^2}{n_N}\approx\dfrac{n_i^2}{N_D}\ll n_N$.
**In P-type:** $p_P=N_A+n_P\approx N_A$, and $n_P=\dfrac{n_i^2}{p_P}\approx\dfrac{n_i^2}{N_A}\ll p_P$.

**Extrinsic conductivity:** $\sigma_N=qn_N\mu_n\approx qN_D\mu_n$ and $\sigma_P=qp_P\mu_p\approx qN_A\mu_p$.

::: ex Example 11.4 (class: mixed doping and resistivity)
*A sample at temperature $T$ in intrinsic condition has resistivity $2.5\times10^{4}\ \Omega\cdot$cm. It is doped with $4\times10^{10}$ donors/cm³ and $10^{10}$ acceptors/cm³. Find the total conduction current density for $E=4$ V/cm. $\mu_n=1250$, $\mu_p=475$ cm²/V·s.*

1. Intrinsic: $\sigma_i=1/\rho=q\,n_i(\mu_n+\mu_p)$ ⇒ $n_i=\dfrac{1}{2.5\times10^4\times1.6\times10^{-19}\times1725}=\mathbf{1.45\times10^{10}\ cm^{-3}}$.
2. Net donors: $n\approx N_D-N_A=4\times10^{10}-10^{10}=3\times10^{10}$ cm⁻³. $p=n_i^2/n=(1.45\times10^{10})^2/3\times10^{10}=\mathbf{0.7\times10^{10}}$ cm⁻³.
3. $\sigma=q(n\mu_n+p\mu_p)=1.6\times10^{-19}(3\times10^{10}\times1250+0.7\times10^{10}\times475)=\mathbf{0.65\times10^{-5}\ S/cm}$.
4. $J=\sigma E=0.65\times10^{-5}\times4=\mathbf{2.6\times10^{-5}\ A/cm^2}$.
:::

::: ex Example 11.5 (class: minority-carrier concentration)
*Si PN junction at 300 K, $n_i=1.5\times10^{10}$ cm⁻³, N-type doping $N_D=1\times10^{10}$ cm⁻³, forward bias 0.6 V. Find the minority-hole concentration at the edge of the space-charge region.*

Class solution (equilibrium value): $p=\dfrac{n_i^2}{N_D}=\dfrac{(1.5\times10^{10})^2}{10^{10}}=\mathbf{2.25\times10^{10}\ cm^{-3}}$.

::: flag What the class problem does and does not do
It computes the **thermal-equilibrium** hole concentration $p_{n0}=n_i^2/N_D$ in the N-region. Under forward bias $V$ the value at the depletion edge is raised to $p_{n0}\,e^{V/V_T}$ (the “law of the junction”). The class stopped at $p_{n0}$; write it as taught. (With $N_D$ this small, comparable to $n_i$, the strict $n\approx N_D$ approximation is also rough.)
:::
:::

## 11.6 Variation with temperature

* $n=N_ce^{-(E_c-E_F)/kT}$, $p=N_ve^{-(E_F-E_v)/kT}$, so $np=N_cN_ve^{-E_g/kT}$.
* **Intrinsic concentration is extremely temperature sensitive:**
$$n_i^2=A_0T^3e^{-E_{G0}/kT}$$
($A_0$ constant independent of temperature; $E_{G0}$ = forbidden gap at 0 K in eV; $k$ = Boltzmann constant in eV/K $=8.617\times10^{-5}$).
* In an **intrinsic** semiconductor, $T\uparrow\Rightarrow n_i\uparrow\Rightarrow\sigma\uparrow$.
* In an **N-type** semiconductor the number of free electrons $n$ does not change appreciably with temperature (fixed by $N_D$); in **P-type** the number of holes is likewise fixed (class notes phrase this “for P-type free electrons increase with temperature”, meaning the *minority* electrons increase).
* **Conductivity** rises with temperature because the number of electron–hole pairs rises even though mobility falls: $\sigma=\sigma_0[1+\alpha(T-T_0)]$ (class form).
* **Energy gap decreases** with temperature: $E_G(T)=E_{G0}-\beta T$.

{{fig p_ni_temp|$n_i^2$ grows exponentially with T; the majority concentration in doped material is nearly constant.|62}}

::: ex Example 11.6
For silicon ($E_g\approx1.1$ eV), how much does $n_i$ change from 300 K to 350 K? $\dfrac{n_i(350)}{n_i(300)}=\left(\dfrac{350}{300}\right)^{3/2}\exp\!\left[-\dfrac{E_g}{2k}\left(\dfrac1{350}-\dfrac1{300}\right)\right]=1.26\times e^{3.04}=1.26\times20.9\approx\mathbf{26}$ times larger for just a 50 K rise.
:::

## 11.7 Try it yourself

::: try Chapter 11 questions
1. Write $\sigma$ for intrinsic, N-type and P-type material.
2. N-type Si has $N_D=10^{16}$ cm⁻³ and $N_c=2.8\times10^{19}$ cm⁻³ at 300 K ($kT=0.02585$ eV). How far below $E_c$ is $E_F$?
3. State the mass-action law. If $N_D=5\times10^{15}$ and $n_i=1.5\times10^{10}$, find $p$.
4. An N-type semiconductor has $E_c-E_F=0.25$ eV at 300 K. Find $E_c-E_F$ at 450 K (class method).
5. Does the Fermi level lie above or below the middle of the gap in P-type?

<details markdown="1"><summary>Answers</summary>

1. $\sigma_i=qn_i(\mu_n+\mu_p)$; N: $\sigma\approx qn\mu_n$; P: $\sigma\approx qp\mu_p$.
2. $E_c-E_F=kT\ln(N_c/N_D)=0.02585\ln(2800)=0.02585\times7.937=\mathbf{0.205\ eV}$.
3. $np=n_i^2$; $p=(1.5\times10^{10})^2/5\times10^{15}=\mathbf{4.5\times10^{4}\ cm^{-3}}$.
4. $0.25\times450/300=\mathbf{0.375\ eV}$.
5. Below the middle (near the valence band).
</details>
:::

# Chapter 12: Drift current, diffusion current, Einstein relation {.chap}

*Class notes pp. 19–21 · slides: EDC Current densities*

::: kid Two reasons water flows
Water in a channel moves for two reasons: (1) the channel is **tilted** (a push from a field: **drift**), or (2) a **big crowd of water** on one side spreads to the empty side even in a flat channel (**diffusion**). Carriers in a semiconductor do exactly the same. Drift needs an electric field. Diffusion needs a concentration difference. The diode is a battle between the two.
:::

{{fig p_drift_diff|Drift (left) and diffusion (right).|92}}

## 12.1 Drift current

**Drift current** is the flow of electric current due to the motion of charge carriers **under an external electric field**.

Take a wire of length $l$ and area $A$ containing $N$ electrons. If an electron takes time $\tau=l/v_d$ to cross:
$$I=\frac{Nq}{\tau}=\frac{Nqv_d}{l}$$
Current density $J=\dfrac IA=\dfrac{Nqv_d}{lA}=nqv_d=\rho v_d$ where $n=N/(lA)$ is the electron concentration and $\rho=nq$ the charge density. With $v_d=\mu E$ (mobility × field):
$$J=nq\mu E=\sigma E\ \ (\text{Ohm’s law}),\qquad\sigma=nq\mu\ (\text{S/m}),\qquad v_d=\mu E$$

$$\boxed{J_n=q\,n\,\mu_nE\ \ (\text{A/cm}^2)},\qquad\boxed{J_p=q\,p\,\mu_pE\ \ (\text{A/cm}^2)}$$

Units: $n,p$ in cm⁻³, $\mu$ in cm²/V·s, $E$ in V/cm, $q=1.6\times10^{-19}$ C.

## 12.2 Diffusion current

Carriers tend to move from **higher concentration to lower concentration**. The diffusion current depends on: (1) the semiconductor material, (2) the type of carriers, (3) the **concentration gradient**.

For holes injected into an N-type bar (concentration $p(x)$ decreasing with $x$):
$$\boxed{J_p=-qD_p\frac{dp}{dx}}\ \ (\text{A/cm}^2)$$
The gradient $dp/dx$ is **negative** (concentration falls with $x$), so the minus sign makes $J_p$ positive in the $+x$ direction. For electrons:
$$\boxed{J_n=qD_n\frac{dn}{dx}}$$
$D_n,D_p$ = **diffusion coefficients** (cm²/s).

**Total current** = drift + diffusion:
$$\text{P-type: }J_p=qp\mu_pE-qD_p\frac{dp}{dx},\qquad\text{N-type: }J_n=qn\mu_nE+qD_n\frac{dn}{dx}$$

## 12.3 Einstein relationship

$$\boxed{\frac{D_p}{\mu_p}=\frac{D_n}{\mu_n}=\frac{kT}{q}=V_T}$$
So $D=\mu V_T$: a carrier that is easy to push (high mobility) also diffuses easily. At 300 K, $V_T\approx0.0259$ V.

## 12.4 Diffusion length

Injected excess carriers survive only a finite **lifetime** $\tau$ before recombining. The average distance they diffuse during their lifetime is the **diffusion length**
$$\boxed{L=\sqrt{D\tau}},\qquad D=\mu\frac{kT}{q}$$
($D$ = diffusion coefficient, $\mu$ = drift mobility, $\tau$ = lifetime of the excess carriers.) In your class notes “τ” is described as the lifetime of excess charge carriers.

::: ex Example 12.1
Electrons in silicon: $\mu_n=1350$ cm²/V·s at 300 K.
* Drift velocity at $E=100$ V/cm: $v_d=\mu E=1350\times100=\mathbf{1.35\times10^{5}\ cm/s}$.
* Einstein: $D_n=\mu_nV_T=1350\times0.02585=\mathbf{34.9\ cm^2/s}$.
* If $\tau=1\ \mu$s: $L_n=\sqrt{34.9\times10^{-6}}=5.9\times10^{-3}$ cm $=\mathbf{59\ \mu m}$.
* Holes: $\mu_p=480$, $D_p=12.4$ cm²/s. If $dp/dx=-10^{18}$ cm⁻⁴: $J_p=-qD_p\,dp/dx=1.6\times10^{-19}\times12.4\times10^{18}=\mathbf{1.99\ A/cm^2}$.
:::

::: trap Signs and units
* Diffusion current has the sign of $-dp/dx$ for holes but $+dn/dx$ for electrons (electron charge is negative and they flow down the gradient).
* Mixing cm and m: use **all cm** ($\mu$ in cm²/V·s, $n$ in cm⁻³) or **all m** ($\mu$ in m²/V·s, $n$ in m⁻³). Never mix.
:::

## 12.5 Try it yourself

::: try Chapter 12 questions
1. Write the total current density for an N-type semiconductor.
2. Find $D_p$ for holes with $\mu_p=1800$ cm²/V·s at 300 K (Ge).
3. Find the diffusion length for those holes if $\tau=50\ \mu$s.
4. Electrons in a semiconductor have $\mu_n=3800$ cm²/V·s and $n=10^{15}$ cm⁻³. Find $\sigma$ and the drift current density for $E=10$ V/cm.

<details markdown="1"><summary>Answers</summary>

1. $J_n=qn\mu_nE+qD_n\,dn/dx$.
2. $D_p=\mu_pV_T=1800\times0.02585=\mathbf{46.5\ cm^2/s}$.
3. $L=\sqrt{46.5\times50\times10^{-6}}=\sqrt{2.33\times10^{-3}}=\mathbf{0.048\ cm}$ (0.48 mm).
4. $\sigma=qn\mu_n=1.6\times10^{-19}\times10^{15}\times3800=\mathbf{0.608\ S/cm}$; $J=\sigma E=\mathbf{6.08\ A/cm^2}$.
</details>
:::

# Chapter 13: Formation of the PN junction {.chap}

*Class notes pp. 21–28 · slides: Formation of PN Junction (handwritten), PN Junction Energy Band Diagram*

::: kid Building the wall
Start with a bar that is P on the left and N on the right. Electrons from the N side wander over to the P side and fall into holes. But each electron that leaves the N side uncovers a **positive donor ion**, and each hole that gets filled on the P side uncovers a **negative acceptor ion**. So a layer of *plus* forms on the N side and a layer of *minus* on the P side. Plus next to minus makes an **electric field** pointing from N to P. That field pushes electrons back toward N. The rush stops when the field is strong enough: that field/potential is the **contact (built-in) potential $V_0$**. The width of the charged layer is the **depletion width $W$**. Everything below is just the mathematics of that story.
:::

## 13.1 The physical picture

{{fig p_pn_formation|(a) the junction, (b) carrier concentration, (c) space-charge density for an abrupt (alloy) junction, (d) electric field, (e) potential. Taken from your handwritten set.|75}}

* Half the crystal is doped **P** (high hole concentration), half **N** (high free-electron concentration).
* At the junction, free electrons diffuse to the P side and holes to the N side (**diffusion**).
* When electrons leave, the **donor ions become positively charged** (positive charge on the N side of the junction). Similarly acceptor ions become negative on the P side.
* The layer depleted of mobile carriers is the **depletion region** (space-charge region or transition region, thickness about $10^{-6}$ m).
* Far from the junction the carrier concentrations are $p=N_A$ (P side) and $n=N_D$ (N side).
* The **shape of the space-charge density $\rho$ depends on how the junction is made**:
  * **abrupt (alloy) junction**: sudden change from acceptors to donors; $\rho$ is a rectangle;
  * **graded (grown) junction**: gradual change; $\rho$ is a linear ramp through zero.

## 13.2 Setting up the maths (abrupt junction)

The space-charge region contains negative acceptor ions on the P side and positive donor ions on the N side. Take $x=0$ at the metallurgical junction, the depletion region from $x_1$ (negative, on the P side) to $x_2$ (positive, N side). Assume **no free carriers inside** and **all donors/acceptors ionised**:

$$\rho=-qN_A\ (x_1<x<0),\qquad\rho=+qN_D\ (0<x<x_2),\qquad\rho=0\ \text{elsewhere}$$

The field established by this charge produces a potential difference: the P side sits at a **lower potential** than the N side (so electrons on the P side have **greater potential energy**).

## 13.3 Poisson’s equation

$$\nabla^2V=-\frac{\rho}{\varepsilon},\qquad\varepsilon=\varepsilon_0\varepsilon_r$$
In one dimension: $\dfrac{d^2V}{dx^2}=-\dfrac{\rho}{\varepsilon_0\varepsilon_r}$.

**P-side ($x_1<x<0$):** $\rho=-qN_A$, so
$$\frac{d^2V}{dx^2}=\frac{qN_A}{\varepsilon_0\varepsilon_r}\ \Rightarrow\ V=\frac{qN_A}{2\varepsilon_0\varepsilon_r}x^2+Cx+D$$
Boundary conditions: $V=0$ at $x=0$ ⇒ $D=0$. Beyond $x_1$ the potential is constant so $dV/dx=0$ at $x=x_1$: $C=-\dfrac{qN_Ax_1}{\varepsilon_0\varepsilon_r}$. Hence
$$V=\frac{qN_A}{\varepsilon_0\varepsilon_r}\left(\frac{x^2}{2}-x_1x\right)$$
At $x=x_1$, $V=V_1$:
$$\boxed{V_1=-\frac{qN_A}{2\varepsilon_0\varepsilon_r}x_1^2}\qquad\text{similarly (N-side): }\boxed{V_2=\frac{qN_D}{2\varepsilon_0\varepsilon_r}x_2^2}$$

**Contact (built-in) potential:**
$$\boxed{V_0=V_2-V_1=\frac{q}{2\varepsilon_0\varepsilon_r}\left(N_Dx_2^2+N_Ax_1^2\right)}$$

**Charge neutrality** (the positive charge on the N side equals the negative charge on the P side):
$$N_Ax_1=-N_Dx_2\ \ (\text{or in magnitudes }N_A|x_1|=N_Dx_2)$$

Combining: 
$$x_1=-\left[\frac{2\varepsilon_0\varepsilon_rV_0}{qN_A\left(1+\frac{N_A}{N_D}\right)}\right]^{1/2},\qquad x_2=\left[\frac{2\varepsilon_0\varepsilon_rV_0}{qN_D\left(1+\frac{N_D}{N_A}\right)}\right]^{1/2}$$

**Total depletion width** $W=x_2-x_1$:
$$\boxed{W=\left[\frac{2\varepsilon_0\varepsilon_rV_0}{q}\left(\frac{N_A+N_D}{N_AN_D}\right)\right]^{1/2}}$$
For an abrupt junction $W\propto\sqrt{V_0}$. With an external voltage the barrier becomes $V_0+V_R$ (reverse) or $V_0-V_F$ (forward), so **$W\propto\sqrt{V_0+V_R}$**.

::: remember Which side is wider?
$N_A|x_1|=N_Dx_2$, so the depletion region extends **further into the more lightly doped side**. In the class problem below $N_A=10^{16}$ ≫ $N_D=10^{15}$, so it mostly lies in the N-side (10/11 of $W$).
:::

## 13.4 Energy-band structure of the open-circuited junction

{{fig p_pn_bands|Band diagram: the Fermi level $E_F$ is constant; the bands bend across the space-charge region by $E_0=qV_0$.|80}}

From the figure in your notes ($E_{cp},E_{vp}$ = band edges in P; $E_{cn},E_{vn}$ in N; $E_G$ = gap):
$$E_0=E_1+E_2=E_{cp}-E_{cn}=E_{vp}-E_{vn}$$
$$E_F-E_{vp}=\tfrac12E_G-E_1,\qquad E_{cn}-E_F=\tfrac12E_G-E_2$$
$$\Rightarrow\ E_0=E_1+E_2=E_G-(E_{cn}-E_F)-(E_F-E_{vp})$$

**Contact potential from the bands.** Use $np=n_i^2=N_cN_ve^{-E_G/kT}$ ⇒ $E_G=kT\ln\dfrac{N_cN_v}{n_i^2}$; for the N-side $E_{cn}-E_F=kT\ln\dfrac{N_c}{N_D}$; for the P-side $E_F-E_{vp}=kT\ln\dfrac{N_v}{N_A}$. Substituting:
$$E_0=kT\left[\ln\frac{N_cN_v}{n_i^2}-\ln\frac{N_c}{N_D}-\ln\frac{N_v}{N_A}\right]=kT\ln\frac{N_DN_A}{n_i^2}$$
With $E_0=qV_0$:
$$\boxed{V_0=\frac{kT}{q}\ln\frac{N_AN_D}{n_i^2}=V_T\ln\frac{N_AN_D}{n_i^2}}$$
Using $n_n=N_D$, $p_n=n_i^2/N_D$, $p_p=N_A$, $n_p=n_i^2/N_A$ this can also be written $E_0=kT\ln\dfrac{p_{p0}}{p_{n0}}=kT\ln\dfrac{n_{n0}}{n_{p0}}$ (subscript 0 = thermal equilibrium).

::: trap What is constant?
In equilibrium the **Fermi level is the same** on both sides (flat). It is the *bands* that bend. The height of the bend is $E_0=qV_0$, and it is what carriers must climb.
:::

## 13.5 Worked problems from your class

::: ex Example 13.1 (contact potential, Ge)
*Resistivities of the P and N regions of a Ge diode are 6 Ω·cm and 4 Ω·cm. Find the contact potential $V_0$ and barrier energy $E_0$. If doping densities of both regions are doubled, find the new $V_0$ and $E_0$.* Given $q=1.6\times10^{-19}$ C, $n_i=2.5\times10^{13}\ \text{cm}^{-3}$, $\mu_p=1800$, $\mu_n=3800$ cm²/V·s, $V_T=0.025$ V (class) or 0.026 V (worksheet).

Doping from resistivity ($\rho=1/(qN\mu)$):
$$N_A=\frac{1}{6\times1.6\times10^{-19}\times1800}=5.79\times10^{14},\qquad N_D=\frac{1}{4\times1.6\times10^{-19}\times3800}=4.11\times10^{14}\ \text{cm}^{-3}$$
$$\frac{N_AN_D}{n_i^2}=\frac{5.79\times10^{14}\times4.11\times10^{14}}{6.25\times10^{26}}=381$$

| | $V_T=0.025$ V (class page) | $V_T=0.026$ V (worksheet) |
|---|---|---|
| $V_0=V_T\ln381$ | **0.149 V** ($E_0=0.149$ eV) | **0.1545 V** |
| Doubled ($\times4$ inside ln): $V_T\ln1524$ | **0.183 V** | **0.1905 V** |

Doubling both dopings raises $V_0$ by $V_T\ln4$ (35 mV) only: $V_0$ depends on the **logarithm** of doping. $E_0=qV_0$ in eV equals $V_0$ in volts.
::: flag Slip in the class page
The page writes $N_D=4.111\times10^{-14}$; the correct exponent is $\mathbf{+14}$ (the value used afterwards, and the ln, are consistent with $10^{14}$).
:::
:::

::: ex Example 13.2 (depletion width, Si)
*Si PN junction at 300 K, $N_A=10^{16}$ cm⁻³, $N_D=10^{15}$ cm⁻³, $n_i=1.5\times10^{10}$, $\varepsilon_r=12$. Find the width of the space-charge region when a reverse bias $V_R=5$ V is applied.*

Total barrier $=V_0+V_R$. The class uses $V_0\approx0.7$ V, so $V_0+V_R=5.7$ V. Work in SI (metres, $\varepsilon_0=8.85\times10^{-12}$ F/m, $N_A=10^{22}$, $N_D=10^{21}\ \text{m}^{-3}$):
$$W=\left[\frac{2\times8.85\times10^{-12}\times12\times5.7}{1.6\times10^{-19}}\times\frac{10^{22}+10^{21}}{10^{22}\times10^{21}}\right]^{1/2}=\left[7.567\times10^{9}\times1.1\times10^{-21}\right]^{1/2}=2.885\times10^{-6}\ \text{m}$$
$$\boxed{W\approx2.9\ \mu\text{m}}$$
Split: $x_n=W\dfrac{N_A}{N_A+N_D}=2.62\ \mu$m (lightly-doped N side), $x_p=0.26\ \mu$m. Peak field $E_{max}=qN_Dx_n/\varepsilon=\ 3.95\times10^{4}$ V/cm.

::: flag Units in the class page
The class page inserts $\varepsilon_0=8.85\times10^{-12}$ F/**m** together with concentrations in cm⁻³, giving “0.00288…” (and another page “0.8 µm”), which is not a width in any unit. Keep **all SI**: the answer is **2.9 µm**. Also, the exact built-in voltage for these dopings is $V_0=V_T\ln\frac{10^{16}\times10^{15}}{(1.5\times10^{10})^2}=0.634$ V (giving $W=2.87$ µm); the class used $V_0=0.7$ V.
:::
:::

## 13.6 Try it yourself

::: try Chapter 13 questions
1. Si junction, $N_A=10^{17}$, $N_D=10^{16}$ cm⁻³, $n_i=1.5\times10^{10}$, $V_T=0.0259$ V. Find $V_0$.
2. Explain why the depletion region extends more into the lightly-doped side.
3. What happens to $W$ if the reverse bias is raised from 5 V to 20 V (take $V_0=0.7$ V)?
4. Why is the Fermi level flat across the junction at equilibrium?

<details markdown="1"><summary>Answers</summary>

1. $V_0=0.0259\ln\dfrac{10^{17}\times10^{16}}{2.25\times10^{20}}=0.0259\ln(4.44\times10^{12})=0.0259\times29.12=\mathbf{0.754\ V}$.
2. Charge neutrality $N_A|x_1|=N_Dx_2$: the side with fewer dopants must extend farther to uncover the same total charge.
3. $W\propto\sqrt{V_0+V_R}$: $\sqrt{20.7/5.7}=1.91$, so $W$ nearly doubles.
4. With no net current the electron/hole flows (drift and diffusion) cancel, which requires a single Fermi level throughout; only the band edges shift.
</details>
:::
