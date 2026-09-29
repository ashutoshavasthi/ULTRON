# Chapter 12: Drift current, diffusion current, Einstein relation

*Class notes pp. 19–21 · slides: EDC Current densities*

::: words
| Word / symbol | Plain meaning |
|---|---|
| Drift current | current due to an **electric field** pushing carriers |
| Diffusion current | current due to carriers **spreading** from high to low concentration |
| $v_d$ | drift velocity $=\mu E$ (cm/s) |
| $J_n$, $J_p$ | electron and hole current densities (A/cm²) |
| $\dfrac{dp}{dx}$, $\dfrac{dn}{dx}$ | **concentration gradient**: how quickly the concentration changes with distance $x$ |
| $D_n$, $D_p$ | **diffusion coefficients** (cm²/s) |
| $\mu_n$, $\mu_p$ | mobilities (cm²/V·s) |
| $V_T$ | thermal voltage $kT/q$ (about 26 mV) |
| $\tau$ | carrier lifetime: average time before an extra carrier recombines |
| $L$ | **diffusion length** $=\sqrt{D\tau}$: average distance an extra carrier diffuses before recombining |
| Excess carriers | extra carriers injected above the equilibrium amount |
| Einstein relation | $D/\mu=V_T$ |
:::

::: kid Two reasons water flows
Water in a channel moves for two reasons. (1) The channel is **tilted**, which is a push from a field: **drift**. (2) A **big crowd of water** sits on one side and spreads to the empty side even in a flat channel: **diffusion**. Carriers in a semiconductor do the same. Drift needs an electric field. Diffusion needs a concentration difference. The diode is a battle between the two.
:::

{{fig p_drift_diff|Drift (left) and diffusion (right).|92}}

## 12.1 Drift current

**Drift current** is the current caused by the motion of charge carriers **under an external electric field**.

Take a wire of length $l$ and cross-section $A$ holding $N$ electrons. If an electron takes time $\tau_t=l/v_d$ to cross the length:

**Step 1.** $I=\dfrac{Nq}{\tau_t}=\dfrac{Nqv_d}{l}$.
**Step 2. Current density.** $J=\dfrac IA=\dfrac{Nqv_d}{lA}=\left(\dfrac N{lA}\right)qv_d=nqv_d$, where $n=N/(lA)$ is the electron concentration.
**Step 3.** With $\rho=nq$ (charge density) this is $J=\rho v_d$.
**Step 4.** Drift velocity is proportional to the field: $v_d=\mu E$.
**Step 5.** So $J=nq\mu E=\sigma E$ with $\sigma=nq\mu$. This is **Ohm's law** in field form.

$$\boxed{J_n=q\,n\,\mu_nE\ \ (\text{A/cm}^2)},\qquad\boxed{J_p=q\,p\,\mu_pE\ \ (\text{A/cm}^2)}$$

Units: $n,p$ in cm⁻³, $\mu$ in cm²/V·s, $E$ in V/cm, $q=1.6\times10^{-19}$ C.

## 12.2 Diffusion current

Carriers tend to move from **higher to lower concentration**. Diffusion current depends on (1) the semiconductor material, (2) the type of carrier, (3) the **concentration gradient**.

For holes injected into an N-type bar, with concentration $p(x)$ falling as $x$ increases:
$$\boxed{J_p=-qD_p\frac{dp}{dx}}\ \ (\text{A/cm}^2)$$
The gradient $dp/dx$ is **negative** (concentration falls with $x$), so the minus sign makes $J_p$ positive in the $+x$ direction. For electrons:
$$\boxed{J_n=qD_n\frac{dn}{dx}}$$
$D_n$, $D_p$ are the **diffusion coefficients** (cm²/s).

**Total current** = drift + diffusion:
$$\text{P-type: }J_p=qp\mu_pE-qD_p\frac{dp}{dx},\qquad\text{N-type: }J_n=qn\mu_nE+qD_n\frac{dn}{dx}$$

## 12.3 Einstein relationship

$$\boxed{\frac{D_p}{\mu_p}=\frac{D_n}{\mu_n}=\frac{kT}{q}=V_T}$$
So $D=\mu V_T$: a carrier that is easy to push (high mobility) also spreads easily. At 300 K, $V_T\approx0.0259$ V.

## 12.4 Diffusion length

Injected excess carriers survive only for a **lifetime** $\tau$ before they recombine. The average distance they diffuse in that time is the **diffusion length**
$$\boxed{L=\sqrt{D\tau}},\qquad D=\mu\frac{kT}{q}.$$
($D$ = diffusion coefficient, $\mu$ = mobility, $\tau$ = lifetime of the excess carriers.)

::: ex Example 12.1: Drift velocity, diffusion coefficient and diffusion length
**Given:** electrons in silicon at 300 K, $\mu_n=1350\ \text{cm}^2/\text{V·s}$, field $E=100$ V/cm, lifetime $\tau=1\ \mu\text{s}$, $V_T=0.02585$ V.

**Find:** (a) $v_d$; (b) $D_n$; (c) $L_n$.

**(a) Step 1.** $v_d=\mu_nE=1350\times100=1.35\times10^{5}$ cm/s.
**(b) Step 2.** Einstein: $D_n=\mu_nV_T=1350\times0.02585=34.9\ \text{cm}^2/\text{s}$.
**(c) Step 3.** $D_n\tau=34.9\times10^{-6}=3.49\times10^{-5}\ \text{cm}^2$.
**Step 4.** $L_n=\sqrt{3.49\times10^{-5}}=5.9\times10^{-3}$ cm $=59\ \mu$m.

**Answer:** $v_d=1.35\times10^{5}$ cm/s; $D_n=34.9$ cm²/s; $L_n=59\ \mu$m.
:::

::: ex Example 12.2: Diffusion current density
**Given:** holes in silicon, $\mu_p=480\ \text{cm}^2/\text{V·s}$, concentration gradient $dp/dx=-10^{18}\ \text{cm}^{-4}$.

**Find:** $J_p$.

**Step 1.** $D_p=\mu_pV_T=480\times0.02585=12.4\ \text{cm}^2/\text{s}$.
**Step 2.** $J_p=-qD_p\dfrac{dp}{dx}=-(1.6\times10^{-19})(12.4)(-10^{18})$.
**Step 3.** $=1.6\times10^{-19}\times12.4\times10^{18}=1.99$.

**Answer:** $J_p=\mathbf{1.99\ A/cm^2}$, positive (pointing in the $+x$ direction, the way the holes spread).
:::

::: trap Signs and units
* The diffusion current for holes carries a **minus** sign ($-dp/dx$) but for electrons a **plus** ($+dn/dx$).
* Do not mix cm and m. Use **all cm** ($\mu$ in cm²/V·s, $n$ in cm⁻³) or **all m**.
:::

## 12.5 Practice

::: try Questions for Chapter 12
1. Write the total current density for an N-type semiconductor.
2. Find $D_p$ for holes with $\mu_p=1800\ \text{cm}^2/\text{V·s}$ at 300 K (Ge).
3. Find the diffusion length for those holes if $\tau=50\ \mu$s.
4. Electrons have $\mu_n=3800\ \text{cm}^2/\text{V·s}$ and $n=10^{15}\ \text{cm}^{-3}$. Find $\sigma$ and the drift current density for $E=10$ V/cm.
5. What is the drift velocity of carriers with $\mu=1350$ in a field of 50 V/cm?
:::

::: soln Answers and full solutions
<details markdown="1"><summary>Solution 1</summary>

Drift plus diffusion: $J_n=qn\mu_nE+qD_n\dfrac{dn}{dx}$.
</details>

<details markdown="1"><summary>Solution 2</summary>

**Formula:** $D_p=\mu_pV_T$.
**Step 1.** $D_p=1800\times0.02585=46.5$.

**Answer:** **46.5 cm²/s**.
</details>

<details markdown="1"><summary>Solution 3</summary>

**Formula:** $L=\sqrt{D\tau}$.
**Step 1.** $\tau=50\ \mu\text{s}=50\times10^{-6}$ s.
**Step 2.** $D\tau=46.5\times50\times10^{-6}=2.325\times10^{-3}$.
**Step 3.** $L=\sqrt{2.325\times10^{-3}}=0.0482$ cm.

**Answer:** **0.048 cm** (0.48 mm).
</details>

<details markdown="1"><summary>Solution 4</summary>

**Step 1.** $\sigma=qn\mu_n=1.6\times10^{-19}\times10^{15}\times3800=0.608$ S/cm.
**Step 2.** $J=\sigma E=0.608\times10=6.08$ A/cm².
</details>

<details markdown="1"><summary>Solution 5</summary>

$v_d=\mu E=1350\times50=67\,500$ cm/s $=675$ m/s.
</details>
:::
