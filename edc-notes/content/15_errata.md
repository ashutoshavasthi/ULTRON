# Chapter 22: Errata, source coverage and glossary

## 22.1 Places where your material has a slip or two versions

Each item says what the source says, what is correct, and **what to write in the exam**.

| # | Where | What the source says | Correct / clean version | What to do |
|---|---|---|---|---|
| 1 | Class p. 29–30, half-wave rectifier problem | “$V_m/2=V_{rms}=55$ ⇒ $V_m=110$ V”; $V_{dc}$ written as 35.01 then 32 V; $P_{dc}=1.01$ | 55 V is the *secondary rms* of a sine ⇒ $V_m=55\sqrt2=77.8$ V. With 110 V: $V_{dc}=34.3$ V, $P_{dc}=1.18$ W. Efficiency (39.7 %), ripple (1.21), regulation (2 %) are independent of $V_m$ | Follow your teacher’s key, show the method (Ch. 14, Ex. 14.1) |
| 2 | Class p. 32 | $\eta=0.812/(1+2R_f/R_L)$ under $P_{ac}=I_{max}^2(R_f+R_L)/2$ | That $P_{ac}$ gives $0.812/(1+R_f/R_L)$ (centre-tap). The $2R_f$ version is the **bridge** | Label the circuit |
| 3 | Class p. 28 (two versions) | $W=0.00288\ldots$ and “0.8 µm” | Mixed SI and cm units. Correct $W=2.9\ \mu$m for the data (with $V_0=0.7$ V; 2.87 µm with the exact $V_0=0.634$ V) | Keep all SI or all cm |
| 4 | Current-densities notes, Ge diode problem | $N_D=4.111\times10^{-14}$ | $4.11\times10^{+14}\ \text{cm}^{-3}$ | Exponent sign slip |
| 5 | Same problem | $V_T=0.025$ V (class) vs 0.026 V (worksheet) | $V_0=0.149$ V / 0.1545 V; doubled 0.183 V / 0.1905 V | Quote the $V_T$ you use |
| 6 | Class p. 16 | Fermi level vs temperature assumes $N_c/N_D$ constant | Idealised; fine for the exam | Use $E_c-E_F\propto T$ |
| 7 | Class p. 17 / Current-densities | “minority hole concentration at the edge of the SCR” computed as $n_i^2/N_D$ | That is the equilibrium value; under forward bias it is multiplied by $e^{V/V_T}$ | Give $p_{n0}$ as taught |
| 8 | Different Diodes slide (LED) | Si and Ge “do not emit energy in the form of heat” and P/As are the LED materials | Si/Ge release the energy mostly as **heat**; LEDs use GaAs, GaP, GaAsP, InGaN… | Write the correct version |
| 9 | SCR/TRIAC slide, four modes | “sensitivity in mode 2 and 3 high … mode 1 more sensitive than 2 and 3” | Standard ranking: modes with gate polarity same as $MT_2$ (1 and 3) best, mode 2 weaker, mode 4 worst | Say mode 4 is least preferred |
| 10 | UJT | Class: $V_P=\eta V_{BB}$; slide: $V_P=V_D+\eta V_{BB}$ | Both valid; $V_D\approx0.7$ V | Use class form unless $V_D$ given |
| 11 | Class p. 37 (π-filter) | $X_{L1}=1/2\omega L_1$, $X_{L2}=1/2\omega L_2$ | These are $X_{C1}=1/2\omega C_1$, $X_{C2}=1/2\omega C_2$; $X_L=2\omega L$ | Write $X_C$ |
| 12 | Efficiency and ripple numbers | 40.5 / 40.6 %; 81.2 % ($8/\pi^2=81.06$ %); FWR $\gamma$ = 0.481 / 0.482 (exact 0.483); L-filter limit 0.48 (exact $\sqrt2/3=0.471$) | Rounding differences | Use the value in your source, state the exact expression |
| 13 | Class p. 48 | $A_v=-R_c/R_e$ (fixed bias) | Should be $-R_C/r_e$ (small $r_e$, the ac emitter resistance) | Use $r_e$ |
| 14 | Class p. 50 numerical | $A_v=-369.28$ with $C_E$ | $-R_C/r_e=-367$ with $r_e=5.99\ \Omega$ | Rounding of $r_e$ |
| 15 | Unit-I First part slides (Topic 2, “PN Junction” and V–I characteristics) | “Reverse voltage above 25 V destroys the junction”; “above 3 V the forward current increases sharply” | Device-specific loose statements: breakdown voltage depends on doping; forward current rises from the knee (0.3/0.7 V) | Do not quote as general facts |
| 16 | Two barrier numbers | 0.7/0.3 V (knee) vs 0.6/0.2 V (in $C_T=K/(V_B-V)^n$) | Knee vs built-in potential (related, not equal) | Use the pair the question gives |
| 17 | Class p. 40–41 | “Self-bias circuit (emitter bias)” | The slides call this **emitter bias**; it is the same circuit | Name it either way |
| 18 | Slide (Diff. Diodes) | “Output of LED ranges from 700 nm red, blue 400, infrared 830 nm” | Approximate; ranges in the table | Use the table |
| 19 | Emitter-bias / divider sums | Current gain $A_i\approx\beta$ | Exactly $\beta R_B/(R_B+Z_b)$ (current divider); $\approx\beta$ if $R_B\gg Z_b$ | State the assumption |

## 22.2 Source coverage checklist

Every file you sent, and where its content lives in these notes.

| File | Pages | Content | Chapter(s) |
|---|---|---|---|
| **EDC-25-09-26** (class notes) | 54 | the timeline | all (map in §22.3) |
| **EDC Unit-I First part** | 70 | syllabus; energy bands; PN formation; PN diode; ratings; diode equation; capacitances; Zener; tunnel | 1, 2, 3, 4, 13 |
| **p-n Junction Diode** | 21 | intro, biasing, characteristics, equation, resistance, models, temperature, breakdown | 2, 3 |
| **EDC Different Diodes** | 22 | LED, varactor, tunnel diode | 4, 5, 6 |
| **SCR, TRIAC and DIAC** | 29 | SCR structure/working/characteristics; TRIAC construction/modes; DIAC | 8, 9 |
| **UJT and Photodiode** | 23 | UJT structure, equivalent circuit, working, characteristics; photodiode | 7, 10 |
| **EDC UJT** (scan) | 7 | UJT relaxation oscillator, frequency, numerical; conductivity of a semiconductor | 10, 11 |
| **EDC Current densities** | 20 | conductivity, carrier concentration, Fermi level, mass action, temperature; drift, diffusion, Einstein; junction numericals | 11, 12, 13 |
| **Formation of PN Junction** | 9 | charge/field/potential, Poisson, depletion width, band structure, contact potential | 13 |
| **PN Junction Energy Band Diagram** | 2 | band structure with $E_1,E_2,E_0$ | 13 |
| **Rectifiers** | 19 | HWR, CT-FWR, bridge analysis; merits/demerits | 14 |
| **half-wave rectifier** | 6 | rectifier types, HWR working, analysis | 14 |
| **EDC L-Filter** | 12 | filter principle, HWR/FWR with L, ripple factor, π filter, assignment | 15 |
| **EDC Pi-Filter** | 7 | π-filter operation and ripple-factor derivation | 15 |
| **ECE BJT FOT DU** | 22 | operating point, all DC bias configurations, examples, summary tables | 16, 17 |
| **AC Analysis re model of BJT** | 12 | ac model, $r_e$ model (CE, CB, CC), Early voltage, CE fixed bias | 16, 18 |
| **SCAN …122928063** | 3 | CE emitter-bias ac (unbypassed), numerical | 18 |
| **SCAN …130133488** | 2 | emitter-follower ac analysis | 18 |
| **SCAN …130213105** | 2 | collector DC-feedback ac analysis | 18 |
| **Photo 1** | – | BC547 output-characteristic set-up (fixed 5 V base source) | 19 |
| **Photo 2** | – | BC547 input/output characteristics test bench | 19 |
| **Photo 3** | – | self-bias CE amplifier with bypass capacitor | 18, 19 |

## 22.3 Class notes, page by page

| Page | Topic | Ch. |
|---|---|---|
| 1 | PN summary, diode equation, temperature, breakdown, Zener | 2, 3 |
| 2 | Tunnel diode: I–V, parameters, equivalent circuit | 4 |
| 3 | Tunnel applications; varactor; LED; photodiode (start) | 4, 5, 6, 7 |
| 4 | SCR: terminals, structure, two-transistor model, characteristic | 8 |
| 5 | SCR stages; TRIAC symbol, construction | 8, 9 |
| 6 | TRIAC V–I labels, operation, disadvantages | 9 |
| 7 | DIAC: symbol, working, V–I | 9 |
| 8 | UJT symbol, equivalent circuit, $\eta$, characteristic; photodiode | 10, 7 |
| 9 | UJT oscillator, waveforms, frequency | 10 |
| 10 | UJT numerical | 10 |
| 11–12 | conductivity; numerical | 11 |
| 13–14 | carrier concentration ($n$, $p$) | 11 |
| 15–16 | Fermi level; numericals; mass-action law | 11 |
| 17 | charge densities; extrinsic conductivity; numerical | 11 |
| 18 | temperature variation | 11 |
| 19–21 | drift, diffusion, Einstein, diffusion length | 12 |
| 21–25 | formation of PN junction; Poisson; $W$; bands; $V_0$ | 13 |
| 26–28 | numericals ($J$, $V_0$, $E_0$, $W$) | 11, 13 |
| 29–31 | rectifiers; HWR problem; PIV; $V_{dc}$, $V_{rms}$ | 14 |
| 32 | efficiency, ripple; filters list; HWR Fourier | 14, 15 |
| 33–35 | Fourier equivalents; L filter (HWR, FWR) | 15 |
| 36–38 | C filter; π filter; LC filter; numerical | 15 |
| 39 | Unit II: BJT, CE, Q-point, fixed bias | 16, 17 |
| 40–41 | dc analysis; self-bias | 17 |
| 42–43 | voltage divider (Thévenin, approximate); collector feedback | 17 |
| 44–45 | emitter follower; common base | 17 |
| 46 | ac analysis; $r_e$ model; Early voltage | 18 |
| 47–48 | fixed-bias ac; self-bias | 18 |
| 49–51 | without bypass; voltage-divider ac; follower | 18 |
| 52 | follower $Z_i,Z_o,A_v$ | 18 |
| 53–54 | hybrid model; fixed bias, self-bias | 18 |

## 22.4 Glossary

| Term | Meaning |
|---|---|
| Acceptor / donor | impurity that creates holes (P) / free electrons (N) |
| Anode / cathode | terminal where conventional current enters / leaves the diode |
| Avalanche | breakdown by carrier multiplication |
| Base | thin middle region of a BJT |
| Bias | dc voltage/current applied to fix the operating point |
| Bypass capacitor | capacitor that shorts a resistor for ac only |
| Breakover voltage ($V_{BO}$) | voltage at which an SCR/DIAC/TRIAC turns on without gate |
| Conduction band / valence band | upper (empty at 0 K) / lower (filled) allowed energy bands |
| Contact potential $V_0$ | built-in potential across the junction at equilibrium |
| Cut-in (knee) voltage | forward voltage at which the diode starts to conduct noticeably |
| Depletion region | carrier-free region around the junction |
| Diffusion | motion from high to low concentration |
| Drift | motion due to an electric field |
| Early voltage | extrapolation voltage $-V_A$ giving $r_o\approx V_A/I_{CQ}$ |
| Fermi level | energy where the occupation probability is ½ |
| Form factor | $I_{rms}/I_{dc}$ |
| Holding current | minimum current to keep an SCR/TRIAC on |
| Hole | vacancy in a bond acting as a positive carrier |
| Intrinsic / extrinsic | pure / doped semiconductor |
| Load line | straight line of allowed $(V_{CE},I_C)$ from the output loop |
| Majority / minority carriers | the more / less numerous carrier type |
| Mobility $\mu$ | drift velocity per unit field |
| Negative resistance | region where current falls as voltage rises |
| PIV | peak inverse voltage a diode must withstand |
| Q-point | quiescent (dc) operating point |
| Ripple factor $\gamma$ | rms of ac component ÷ dc component |
| Saturation (BJT) | both junctions forward biased, $V_{CE}\approx0.2$ V |
| Stand-off ratio $\eta$ | UJT $R_{B1}/(R_{B1}+R_{B2})$ |
| Thermal voltage $V_T$ | $kT/q=T/11600$ |
| Transition / diffusion capacitance | junction capacitance in reverse / forward bias |
| Tunnelling | quantum passage through a thin barrier |
