# Chapter 13: Formation of the PN junction

*Class notes pp. 21–28 · slides: Formation of PN Junction (handwritten), PN Junction Energy Band Diagram*

::: words
| Word / symbol | Plain meaning |
|---|---|
| Space-charge region | another name for the depletion region (it contains fixed charge) |
| Abrupt (alloy) junction | doping changes suddenly from P to N |
| Graded (grown) junction | doping changes gradually |
| $\rho$ | **charge density** (C/cm³) in this chapter |
| $N_A$, $N_D$ | acceptor and donor concentrations |
| $x_1$, $x_2$ | edges of the depletion region: $x_1<0$ on the P side, $x_2>0$ on the N side; the junction is at $x=0$ |
| $W$ | total depletion width $=x_2-x_1$ (write $|x_1|+x_2$) |
| $V(x)$ | electric potential at position $x$ |
| $V_0$ | **contact (built-in) potential**: total voltage across the depletion region |
| $E_0=qV_0$ | the energy barrier in eV |
| Poisson's equation | $\dfrac{d^2V}{dx^2}=-\dfrac{\rho}{\varepsilon}$: links charge to potential |
| $\varepsilon=\varepsilon_0\varepsilon_r$ | permittivity of the material |
| $E_{cp}$, $E_{vp}$, $E_{cn}$, $E_{vn}$ | conduction/valence band edges in the P and N regions |
| $E_G$ | energy gap |
| $E_F$ | Fermi level |
| $V_R$ | applied **reverse** voltage |
| Equilibrium | steady state with no external voltage or light |
:::

::: kid Building the wall
Start with a bar that is P on the left and N on the right. Electrons from the N side wander across and fall into holes on the P side. But each electron that leaves the N side uncovers a **positive donor ion**, and each hole that gets filled on the P side uncovers a **negative acceptor ion**. So a layer of plus forms on the N side and a layer of minus on the P side. Plus next to minus makes an **electric field** pointing from N to P. That field pushes electrons back toward N. The rush stops when the field is strong enough. That built-in voltage is the **contact potential $V_0$**, and the width of the charged layer is the **depletion width $W$**. Everything below is just the mathematics of that story.
:::

## 13.1 The physical picture

{{fig p_pn_formation|(a) the junction, (b) carrier concentration, (c) space-charge density for an abrupt (alloy) junction, (d) electric field, (e) potential. Taken from your handwritten set.|75}}

* Half the crystal is doped **P** (many holes), half **N** (many free electrons).
* At the junction, free electrons diffuse to the P side and holes to the N side (**diffusion**).
* When electrons leave, the **donor ions become positively charged** (positive charge on the N side). Similarly acceptor ions become negative on the P side.
* The layer emptied of mobile carriers is the **depletion region** (space-charge or transition region), about $10^{-6}$ m thick.
* Far from the junction the carrier concentrations are $p=N_A$ (P side) and $n=N_D$ (N side).
* The shape of the charge density $\rho$ depends on how the junction is made:
  * **abrupt (alloy) junction**: sudden change from acceptors to donors; $\rho$ is a rectangle;
  * **graded (grown) junction**: gradual change; $\rho$ is a sloping line through zero.

## 13.2 Setting up (abrupt junction)

The space-charge region holds negative acceptor ions on the P side and positive donor ions on the N side. Put $x=0$ at the junction, the depletion region from $x_1$ (negative, P side) to $x_2$ (positive, N side). Assume **no free carriers inside** and **all donors and acceptors ionised**:

$$\rho=-qN_A\ (x_1<x<0),\qquad\rho=+qN_D\ (0<x<x_2),\qquad\rho=0\ \text{elsewhere}$$

The field made by this charge produces a potential difference: the P side sits at a **lower potential** than the N side (so electrons on the P side have greater potential energy).

## 13.3 Poisson's equation and the depletion width, step by step

Poisson's equation in one dimension is
$$\frac{d^2V}{dx^2}=-\frac{\rho}{\varepsilon_0\varepsilon_r}.$$

**P-side ($x_1<x<0$):** $\rho=-qN_A$.

**Step 1.** $\dfrac{d^2V}{dx^2}=\dfrac{qN_A}{\varepsilon_0\varepsilon_r}$ (the two minus signs cancel).
**Step 2. Integrate once.** $\dfrac{dV}{dx}=\dfrac{qN_A}{\varepsilon_0\varepsilon_r}x+C$.
**Step 3. Integrate again.** $V=\dfrac{qN_A}{2\varepsilon_0\varepsilon_r}x^2+Cx+D$.
**Step 4. Boundary condition 1:** take the potential zero at the junction, $V=0$ at $x=0$, so $D=0$.
**Step 5. Boundary condition 2:** outside the depletion region the field is zero, so at $x=x_1$: $\dfrac{dV}{dx}=0$. Then $0=\dfrac{qN_A}{\varepsilon_0\varepsilon_r}x_1+C$, so $C=-\dfrac{qN_Ax_1}{\varepsilon_0\varepsilon_r}$.
**Step 6.** $V=\dfrac{qN_A}{\varepsilon_0\varepsilon_r}\left(\dfrac{x^2}{2}-x_1x\right)$.
**Step 7. Evaluate at $x=x_1$:** $V_1=\dfrac{qN_A}{\varepsilon_0\varepsilon_r}\left(\dfrac{x_1^2}{2}-x_1^2\right)$:
$$\boxed{V_1=-\frac{qN_A}{2\varepsilon_0\varepsilon_r}x_1^2}$$
**N-side, the same way:**
$$\boxed{V_2=\frac{qN_D}{2\varepsilon_0\varepsilon_r}x_2^2}$$

**Contact potential:**
$$\boxed{V_0=V_2-V_1=\frac{q}{2\varepsilon_0\varepsilon_r}\left(N_Dx_2^2+N_Ax_1^2\right)}$$

**Charge neutrality** (positive charge on the N side equals negative on the P side):
$$N_A|x_1|=N_Dx_2\qquad(\text{class writes }N_Ax_1=-N_Dx_2\text{ with }x_1<0).$$

**Step 8. Solve for $x_1$ and $x_2$.** From neutrality $|x_1|=x_2N_D/N_A$. Substitute in $V_0$:
$$V_0=\frac{q}{2\varepsilon}\left(N_Dx_2^2+N_A\frac{N_D^2}{N_A^2}x_2^2\right)=\frac{qN_D}{2\varepsilon}x_2^2\left(1+\frac{N_D}{N_A}\right),$$
$$x_2=\left[\frac{2\varepsilon V_0}{qN_D\left(1+\frac{N_D}{N_A}\right)}\right]^{1/2},\qquad|x_1|=\left[\frac{2\varepsilon V_0}{qN_A\left(1+\frac{N_A}{N_D}\right)}\right]^{1/2}.$$

**Step 9. Total width** $W=x_2+|x_1|$ (equal to $x_2-x_1$ in the class sign convention). Squaring and simplifying gives
$$\boxed{W=\left[\frac{2\varepsilon_0\varepsilon_rV_0}{q}\left(\frac{N_A+N_D}{N_AN_D}\right)\right]^{1/2}}$$
$W\propto\sqrt{V_0}$. With an external voltage, replace $V_0$ by $V_0+V_R$ (reverse) or $V_0-V_F$ (forward): **$W\propto\sqrt{V_0+V_R}$**.

::: remember Which side is wider?
$N_A|x_1|=N_Dx_2$ means the depletion region extends **further into the more lightly doped side**. In the problem below $N_A=10^{16}\gg N_D=10^{15}$, so about $10/11$ of $W$ lies in the N-side.
:::

## 13.4 Energy-band structure of the open-circuited junction

{{fig p_pn_bands|Band diagram: the Fermi level $E_F$ is the same all through; the bands bend across the space-charge region by $E_0=qV_0$.|80}}

From the figure in your notes:
$$E_0=E_1+E_2=E_{cp}-E_{cn}=E_{vp}-E_{vn}$$
$$E_F-E_{vp}=\tfrac12E_G-E_1,\qquad E_{cn}-E_F=\tfrac12E_G-E_2$$
Add the last two equations and rearrange:
$$E_0=E_1+E_2=E_G-(E_{cn}-E_F)-(E_F-E_{vp}).$$

**Contact potential from the bands, step by step.**

**Step 1.** $np=n_i^2=N_cN_ve^{-E_G/kT}$, so $E_G=kT\ln\dfrac{N_cN_v}{n_i^2}$.
**Step 2.** N-side: $E_{cn}-E_F=kT\ln\dfrac{N_c}{N_D}$.
**Step 3.** P-side: $E_F-E_{vp}=kT\ln\dfrac{N_v}{N_A}$.
**Step 4.** Substitute in $E_0$: $E_0=kT\left[\ln\dfrac{N_cN_v}{n_i^2}-\ln\dfrac{N_c}{N_D}-\ln\dfrac{N_v}{N_A}\right]$.
**Step 5.** Combine the logs: $E_0=kT\ln\left[\dfrac{N_cN_v}{n_i^2}\cdot\dfrac{N_D}{N_c}\cdot\dfrac{N_A}{N_v}\right]=kT\ln\dfrac{N_AN_D}{n_i^2}$.
**Step 6.** Since $E_0=qV_0$:
$$\boxed{V_0=\frac{kT}{q}\ln\frac{N_AN_D}{n_i^2}=V_T\ln\frac{N_AN_D}{n_i^2}}$$
Equivalent forms using $n_{n0}=N_D$, $p_{n0}=n_i^2/N_D$, $p_{p0}=N_A$, $n_{p0}=n_i^2/N_A$: $E_0=kT\ln\dfrac{p_{p0}}{p_{n0}}=kT\ln\dfrac{n_{n0}}{n_{p0}}$ (subscript 0 = thermal equilibrium).

::: trap What is constant?
At equilibrium the **Fermi level is the same** on both sides (a flat line). It is the **band edges** that bend. The height of the bend is $E_0=qV_0$, the barrier carriers must climb.
:::

## 13.5 Worked problems from your class

::: ex Example 13.1: Contact potential of a germanium diode
*Resistivities of the P and N regions of a Ge diode are 6 Ω·cm and 4 Ω·cm. Find the contact potential $V_0$ and barrier energy $E_0$. If the doping of both regions is doubled, find the new $V_0$ and $E_0$.* Given $q=1.6\times10^{-19}$ C, $n_i=2.5\times10^{13}\ \text{cm}^{-3}$, $\mu_p=1800$, $\mu_n=3800$ cm²/V·s, $V_T=0.025$ V (class) or 0.026 V (worksheet).

**Find:** $N_A$, $N_D$, then $V_0$, $E_0$, and the same after doubling.

**Step 1: acceptor doping from P resistivity.** $\rho_p=\dfrac{1}{qN_A\mu_p}$ ⇒ $N_A=\dfrac{1}{\rho_pq\mu_p}=\dfrac{1}{6\times1.6\times10^{-19}\times1800}=\dfrac{1}{1.728\times10^{-15}}=5.79\times10^{14}\ \text{cm}^{-3}$.
**Step 2: donor doping from N resistivity.** $N_D=\dfrac{1}{\rho_nq\mu_n}=\dfrac{1}{4\times1.6\times10^{-19}\times3800}=\dfrac{1}{2.432\times10^{-15}}=4.11\times10^{14}\ \text{cm}^{-3}$.
**Step 3: the ratio.** $n_i^2=(2.5\times10^{13})^2=6.25\times10^{26}$; $N_AN_D=5.79\times10^{14}\times4.11\times10^{14}=2.38\times10^{29}$; $\dfrac{N_AN_D}{n_i^2}=\dfrac{2.38\times10^{29}}{6.25\times10^{26}}=381$.
**Step 4: $\ln381=5.943$.**
**Step 5: contact potential.** $V_0=V_T\ln381$.

| | $V_T=0.025$ V (class page) | $V_T=0.026$ V (worksheet) |
|---|---|---|
| $V_0=V_T\times5.943$ | **0.149 V** ($E_0=0.149$ eV) | **0.1545 V** |
| Doubled: $N_AN_D$ becomes 4×, so $\ln(4\times381)=\ln1524=7.329$ | **0.183 V** | **0.1905 V** |

**Answer:** $V_0\approx0.149$ V and $E_0=qV_0=0.149$ eV; after doubling $V_0\approx0.183$ V.

**What it means:** doubling both dopings raised $V_0$ by only $V_T\ln4=35$ mV, because $V_0$ depends on the **logarithm** of the doping. Note that the barrier energy in eV equals the potential in volts.

::: flag Slip in the class page
The page writes $N_D=4.111\times10^{-14}$; the correct exponent is $\mathbf{+14}$ (the later steps use $10^{14}$).
:::
:::

::: ex Example 13.2: Depletion width of a silicon junction under reverse bias
*Si PN junction at 300 K, $N_A=10^{16}\ \text{cm}^{-3}$, $N_D=10^{15}\ \text{cm}^{-3}$, $n_i=1.5\times10^{10}$, $\varepsilon_r=12$. Find the width of the space-charge region when a reverse bias $V_R=5$ V is applied.*

**Given:** the class takes $V_0\approx0.7$ V.

**Find:** $W$, and how it splits between P and N sides.

**Formula:** $W=\left[\dfrac{2\varepsilon_0\varepsilon_r(V_0+V_R)}{q}\cdot\dfrac{N_A+N_D}{N_AN_D}\right]^{1/2}$.

**Step 1: convert everything to SI.** $N_A=10^{16}\ \text{cm}^{-3}=10^{22}\ \text{m}^{-3}$, $N_D=10^{21}\ \text{m}^{-3}$, $\varepsilon_0=8.85\times10^{-12}$ F/m.
**Step 2: total barrier.** $V_0+V_R=0.7+5=5.7$ V.
**Step 3: first factor.** $\dfrac{2\times8.85\times10^{-12}\times12\times5.7}{1.6\times10^{-19}}$. Numerator: $2\times8.85\times10^{-12}=1.77\times10^{-11}$; $\times12=2.124\times10^{-10}$; $\times5.7=1.211\times10^{-9}$. Divide by $1.6\times10^{-19}$: $7.567\times10^{9}$.
**Step 4: second factor.** $\dfrac{N_A+N_D}{N_AN_D}=\dfrac{10^{22}+10^{21}}{10^{22}\times10^{21}}=\dfrac{1.1\times10^{22}}{10^{43}}=1.1\times10^{-21}$.
**Step 5: multiply.** $7.567\times10^{9}\times1.1\times10^{-21}=8.32\times10^{-12}$.
**Step 6: square root.** $W=\sqrt{8.32\times10^{-12}}=2.885\times10^{-6}$ m.
**Step 7: split.** $x_n=W\dfrac{N_A}{N_A+N_D}=2.885\times\dfrac{10}{11}=2.62\ \mu$m (in the lightly doped N side); $x_p=2.885-2.62=0.26\ \mu$m.

**Answer:** $W\approx\mathbf{2.9\ \mu m}$.

::: flag Units in the class page
The class page uses $\varepsilon_0=8.85\times10^{-12}$ F/**m** together with concentrations in cm⁻³, which mixes units and gives "0.00288…" (another page shows "0.8 µm"), neither of which is a correct width. Keep **all SI**: 2.9 µm. Also, the exact built-in voltage here is $V_0=0.02585\ln\dfrac{10^{16}\times10^{15}}{(1.5\times10^{10})^2}=0.634$ V, giving $W=2.87\ \mu$m; the class used 0.7 V.
:::
:::

## 13.6 Practice

::: try Questions for Chapter 13
1. Si junction, $N_A=10^{17}$, $N_D=10^{16}\ \text{cm}^{-3}$, $n_i=1.5\times10^{10}\ \text{cm}^{-3}$, $V_T=0.0259$ V. Find $V_0$.
2. Explain why the depletion region extends more into the lightly-doped side.
3. What happens to $W$ if the reverse bias is raised from 5 V to 20 V (take $V_0=0.7$ V)?
4. Why is the Fermi level flat across the junction at equilibrium?
5. A Ge junction has $N_A=10^{16}$ and $N_D=10^{16}\ \text{cm}^{-3}$, $n_i=2.5\times10^{13}\ \text{cm}^{-3}$, $V_T=0.0259$ V. Find $V_0$.
:::

::: soln Answers and full solutions
<details markdown="1"><summary>Solution 1</summary>

**Formula:** $V_0=V_T\ln\dfrac{N_AN_D}{n_i^2}$.
**Step 1.** $N_AN_D=10^{17}\times10^{16}=10^{33}$.
**Step 2.** $n_i^2=2.25\times10^{20}$.
**Step 3.** Ratio $=\dfrac{10^{33}}{2.25\times10^{20}}=4.44\times10^{12}$.
**Step 4.** $\ln(4.44\times10^{12})=\ln4.44+12\ln10=1.491+27.631=29.12$.
**Step 5.** $V_0=0.0259\times29.12=0.754$ V.

**Answer:** **0.754 V**.
</details>

<details markdown="1"><summary>Solution 2</summary>

**Step 1.** Charge neutrality: the total negative charge on the P side equals the total positive charge on the N side, $N_A|x_1|=N_Dx_2$.
**Step 2.** Fewer dopant ions per unit volume on the lightly doped side means a thicker layer is needed to uncover the same total charge.
**Answer:** so the region extends further into the lightly doped side.
</details>

<details markdown="1"><summary>Solution 3</summary>

**Formula:** $W\propto\sqrt{V_0+V_R}$.
**Step 1.** At 5 V: $\sqrt{0.7+5}=\sqrt{5.7}=2.387$.
**Step 2.** At 20 V: $\sqrt{20.7}=4.550$.
**Step 3.** Ratio $=4.550/2.387=1.906$.

**Answer:** $W$ increases by a factor of about **1.9**: nearly doubles.
</details>

<details markdown="1"><summary>Solution 4</summary>

At equilibrium there is no net current: drift and diffusion of each carrier type cancel. That requires a single Fermi level throughout. Only the band edges move (they bend by $E_0=qV_0$).
</details>

<details markdown="1"><summary>Solution 5</summary>

**Step 1.** $N_AN_D=10^{32}$.
**Step 2.** $n_i^2=6.25\times10^{26}$.
**Step 3.** Ratio $=1.6\times10^{5}$; $\ln(1.6\times10^5)=\ln1.6+5\ln10=0.470+11.513=11.98$.
**Step 4.** $V_0=0.0259\times11.98=0.310$ V.

**Answer:** **0.31 V**. (Smaller than silicon because germanium has a much larger $n_i$.)
</details>
:::
