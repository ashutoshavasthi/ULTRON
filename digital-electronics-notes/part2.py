from helpers import *

def universal(kind):
    """NOT/AND/OR built from only `kind` gates (nand or nor)."""
    L = kind.upper()
    out = ""
    # NOT
    s = g_(kind, 30, 10) + wire((0, 30), (10, 30)) + wire((10, 20), (10, 40)) + wire((10, 20), (20, 20)) + wire((10, 40), (20, 40)) + dot(10, 30)
    s += txt(0, 24, "A") + txt(94, 34, "A'")
    out += '<div><b>NOT from %s</b>' % L + svg(110, 60, s + wire((90, 30), (100, 30))) + '<p class="sm">Tie both inputs together: (A·A)\' = A\'</p></div>' if kind == "nand" else '<div><b>NOT from %s</b>' % L + svg(110, 60, s + wire((90, 30), (100, 30))) + '<p class="sm">Tie both inputs together: (A+A)\' = A\'</p></div>'
    # AND (nand) / OR (nor) = gate followed by NOT
    s = g_(kind, 30, 10) + g_(kind, 130, 10)
    s += wire((0, 20), (20, 20)) + wire((0, 40), (20, 40))
    s += wire((90, 30), (110, 30)) + wire((110, 20), (110, 40)) + wire((110, 20), (120, 20)) + wire((110, 40), (120, 40)) + dot(110, 30)
    s += wire((190, 30), (210, 30)) + txt(0, 16, "A") + txt(0, 36, "B")
    lab = "AND" if kind == "nand" else "OR"
    sub = "(AB)'' = AB" if kind == "nand" else "(A+B)'' = A+B"
    out += '<div><b>%s from %s</b>' % (lab, L) + svg(230, 60, s + txt(212, 34, "Y")) + '<p class="sm">%s followed by an inverter. %s</p></div>' % (L, sub)
    # OR (nand) / AND (nor): invert both inputs then gate
    s = g_(kind, 30, 0) + g_(kind, 30, 60) + g_(kind, 130, 30)
    s += wire((0, 20), (10, 20)) + wire((10, 10), (10, 30)) + wire((10, 10), (20, 10)) + wire((10, 30), (20, 30)) + dot(10, 20)
    s += wire((0, 80), (10, 80)) + wire((10, 70), (10, 90)) + wire((10, 70), (20, 70)) + wire((10, 90), (20, 90)) + dot(10, 80)
    s += wire((90, 20), (105, 20), (105, 40), (120, 40)) + wire((90, 80), (105, 80), (105, 60), (120, 60))
    s += wire((190, 50), (210, 50)) + txt(0, 16, "A") + txt(0, 76, "B") + txt(212, 54, "Y")
    lab = "OR" if kind == "nand" else "AND"
    sub = "(A'·B')' = A+B" if kind == "nand" else "(A'+B')' = A·B"
    out += '<div><b>%s from %s</b>' % (lab, L) + svg(230, 110, s) + '<p class="sm">Invert both inputs, then %s. %s (De Morgan)</p></div>' % (L, sub)
    return '<div class="pair">%s</div>' % out

def two_level():
    def d(kind1, kind2):
        s = g_(kind1, 40, 0) + g_(kind1, 40, 60) + g_(kind2, 140, 30)
        s += wire((0, 10), (30, 10)) + wire((15, 10), (15, 70), (30, 70)) + dot(15, 10)
        s += wire((0, 30), (30, 30)) + wire((0, 90), (30, 90))
        s += wire((100, 20), (115, 20), (115, 40), (130, 40)) + wire((100, 80), (115, 80), (115, 60), (130, 60))
        s += wire((200, 50), (230, 50)) + txt(0, 6, "A") + txt(0, 26, "B") + txt(0, 86, "C") + txt(232, 54, "f")
        return svg(260, 110, s)
    return '<div class="pair"><div><b>AND–OR (SOP)</b>%s</div><div><b>NAND–NAND (same function)</b>%s</div></div>' % (d("and", "or"), d("nand", "nand"))

def gate_card(name, kind, expr, rows, note):
    return '<div class="g"><h4>%s</h4>%s<div class="mono">%s</div>%s<p style="font-size:.85rem;margin:4px 0 0">%s</p></div>' % (
        name, gate_icon(kind), expr, tt(["A","B","Y"], rows), note)

R2 = lambda f: [[a, b, f(a, b)] for a in (0, 1) for b in (0, 1)]

S4 = """
<h2 id="s4">4. Logic Gates</h2>
<p>A <b>logic gate</b> is an electronic circuit with one or more inputs and one output that implements a Boolean function. Inputs/outputs are <b>HIGH (1)</b> or <b>LOW (0)</b>. A <b>truth table</b> lists the output for every input combination (2<sup>n</sup> rows for n inputs).</p>

<h3>4.1 The seven gates</h3>
<div class="gates">
""" + gate_card("1. AND", "and", "Y = A·B", R2(lambda a,b:a&b), "Output 1 only if <b>all</b> inputs are 1.") \
+ gate_card("2. OR", "or", "Y = A+B", R2(lambda a,b:a|b), "Output 1 if <b>at least one</b> input is 1.") \
+ gate_card("3. NOT (inverter)", "not", "Y = A' = Ā", [[0,1],[1,0]], "Single input; flips it. The bubble ○ always means inversion.").replace("<th>B</th>","").replace("<th>A</th><th>Y</th>","<th>A</th><th>Y</th>") \
+ gate_card("4. NAND (A↑B)", "nand", "Y = (A·B)'", R2(lambda a,b:1-(a&b)), "AND followed by NOT. Output 0 only when all inputs are 1. <b>Universal.</b>") \
+ gate_card("5. NOR (A↓B)", "nor", "Y = (A+B)'", R2(lambda a,b:1-(a|b)), "OR followed by NOT. Output 1 only when all inputs are 0. <b>Universal.</b>") \
+ gate_card("6. XOR (A⊕B)", "xor", "Y = A⊕B = A'B + AB'", R2(lambda a,b:a^b), "<b>Odd number of 1s → output high.</b> Detects <i>difference</i>.") \
+ gate_card("7. XNOR (A⊙B)", "xnor", "Y = (A⊕B)' = AB + A'B'", R2(lambda a,b:1-(a^b)), "Complement of XOR. <b>Even number of 1s → high.</b> Also called <i>equivalence</i> — high when inputs are equal.") + """
</div>
<div class="box warn"><b>Correction of a small slip in the class note</b>The note says XNOR is high "if there are even 0's". For 2 inputs that is true, but the general (n-input) rule is: <b>XNOR is high when the number of 1s is even</b> (including zero 1s). Example 3 inputs 000: XNOR = 1 although there are three (odd) zeros. Use "even number of 1s".</div>
<p><b>Useful XOR identities:</b> A⊕0 = A, A⊕1 = A', A⊕A = 0, A⊕A' = 1, commutative and associative (so A⊕B⊕C = parity of the three bits). XOR is the "sum" bit of an adder and the heart of Gray-code conversion (Section 8).</p>

<h3>4.2 Universal gates</h3>
<p>A gate is <b>universal</b> if NOT, AND and OR (hence <i>any</i> function) can be built from it alone. <b>NAND and NOR are universal</b>. In practice a whole design is often built from one gate type because it is cheaper and faster.</p>
<h4>Using only NAND</h4>""" + universal("nand") + """
<h4>Using only NOR</h4>""" + universal("nor") + """
<div class="ex"><div class="t">Example 4.1 — XOR using only NAND (4 gates)</div>
<div class="fx">Let P = (A·B)'
Q = (A·P)'      R = (B·P)'
A⊕B = (Q·R)'
Check A=1,B=0: P=1, Q=(1·1)'=0, R=(0·1)'=1, out=(0·1)'=1 ✓</div></div>

<h3>4.3 De Morgan's laws</h3>
<div class="fx">(x·y)' = x' + y'       "break the bar, change the sign"
(x+y)' = x'·y'</div>
<p>Valid for any number of variables: (ABC)' = A'+B'+C'. In words: <b>NAND = OR with inverted inputs (bubbled OR)</b> and <b>NOR = AND with inverted inputs (bubbled AND)</b> — exactly what your notes say. This is the key to redrawing circuits with NANDs/NORs.</p>
""" + tt(["x","y","(x·y)'","x'+y'","(x+y)'","x'·y'"],[[x,y,1-(x&y),(1-x)|(1-y),1-(x|y),(1-x)&(1-y)] for x in (0,1) for y in (0,1)]) + """

<h3>4.4 Two-level implementation (SOP with NAND-NAND)</h3>
<p>A <b>two-level</b> circuit has an AND level feeding one OR level (sum of products). To convert to <b>NAND only</b>: replace <i>every</i> gate by a NAND. Why it works: draw a NAND as a bubbled OR; the bubble on each first-level NAND output and the bubble at the second-level inputs <b>cancel</b> ("put two bubbles always" in your note).</p>
<div class="ex"><div class="t">Example 4.2 — f = A·B + A·C with NAND gates (your notes)</div>
""" + two_level() + """
<div class="fx">f = ((A·B)' · (A·C)')'  = (AB)'' + (AC)''  = AB + AC     (De Morgan on the last NAND)</div>
<p>Rule: <b>SOP → NAND–NAND</b>. Likewise <b>POS → NOR–NOR</b> (OR level then AND level; each replaced by NOR). If a literal feeds the 2nd level directly (e.g. f = AB + C), pass C through an inverter (a NAND with tied inputs) or equivalently feed C' — otherwise the double-bubble rule breaks.</p></div>

<h3>4.5 Multi-level implementation</h3>
<p>If the expression is allowed to have more than two levels (factored form such as <code>A(B+C)</code> or <code>(A+B)(C+D)E</code>) there is <b>no need to convert to SOP or POS</b>: implement the expression as it stands. It often needs fewer gates and fan-in but takes more gate delays (slower). Trade-off: two-level = fast, multi-level = small.</p>
"""

S5 = """
<h2 id="s5">5. Boolean Algebra</h2>
<p><b>Boolean algebra</b> is algebra over the two-element set {0,1} with operations + (OR), · (AND) and ' (NOT). Every digital circuit corresponds to a Boolean expression, and simplifying the expression simplifies the circuit.</p>

<h3>5.1 Basic laws (definitions)</h3>
<table class="left"><tr><th>Law</th><th>OR form</th><th>AND form</th></tr>
<tr><td>Commutative</td><td>x + y = y + x</td><td>x·y = y·x</td></tr>
<tr><td>Associative</td><td>x + (y+z) = (x+y) + z</td><td>x(yz) = (xy)z</td></tr>
<tr><td>Identity element</td><td>x + 0 = x (0 is the identity of +)</td><td>x·1 = x (1 is the identity of ·)</td></tr>
<tr><td>Inverse (complement)</td><td>x + x' = 1</td><td>x·x' = 0</td></tr>
<tr><td>Distributive</td><td>x(y+z) = xy + xz</td><td><b>x + yz = (x+y)(x+z)</b></td></tr></table>
<p class="box warn"><b>Watch out</b>The second distributive law (+ over ·) is <i>false</i> in ordinary algebra but <i>true</i> in Boolean algebra. Examiners love it.</p>

<h3>5.2 Duality principle</h3>
<p>The <b>dual</b> of a Boolean expression is obtained by interchanging <b>+ ↔ ·</b> and <b>0 ↔ 1</b> (variables and complements stay). <b>If an identity is true, its dual is also true</b> — this holds in Boolean algebra (that is why every law above comes in a pair). E.g. dual of x + 0 = x is x·1 = x; dual of x + x'y = x + y is x(x'+y) = xy.</p>
<div class="box bad"><b>Careful</b>The dual of an <i>expression</i> is not equal to the expression. Duality gives you a second true <i>theorem</i>, not an equality between f and f<sup>d</sup>. (Don't confuse with complement: f' = f<sup>d</sup> with every variable complemented.)</div>

<h3>5.3 Postulates &amp; theorems (with the labels used in your notes)</h3>
<table class="left"><tr><th>Label</th><th>Name</th><th>(a)</th><th>(b) dual</th></tr>
<tr><td>P2</td><td>Identity</td><td>x + 0 = x</td><td>x·1 = x</td></tr>
<tr><td>P3</td><td>Commutative</td><td>x + y = y + x</td><td>xy = yx</td></tr>
<tr><td>P4</td><td>Distributive</td><td>x(y+z) = xy + xz</td><td>x + yz = (x+y)(x+z)</td></tr>
<tr><td>P5</td><td>Complement</td><td>x + x' = 1</td><td>x·x' = 0</td></tr>
<tr><td>T1</td><td>Idempotent</td><td>x + x = x</td><td>x·x = x</td></tr>
<tr><td>T2</td><td>Null / dominance</td><td>x + 1 = 1</td><td>x·0 = 0</td></tr>
<tr><td>T3</td><td>Involution</td><td colspan="2">(x')' = x</td></tr>
<tr><td>T4</td><td>Associative</td><td>x + (y+z) = (x+y)+z</td><td>x(yz) = (xy)z</td></tr>
<tr><td>T5</td><td>De Morgan</td><td>(x+y)' = x'y'</td><td>(xy)' = x'+y'</td></tr>
<tr><td>T6</td><td>Absorption</td><td>x + xy = x</td><td>x(x+y) = x</td></tr></table>

<h4>Two more very useful (not in your list)</h4>
<div class="fx">Simplification 1:  x + x'y = x + y        dual: x(x'+y) = xy
Simplification 2:  xy + xy' = x  (combining/adjacency)    dual: (x+y)(x+y') = x</div>
<div class="ex"><div class="t">Proof of absorption x + xy = x</div>
<div class="fx">x + xy = x·1 + xy       (P2)
       = x(1 + y)       (P4)
       = x·1            (T2)
       = x              (P2)   ∎</div>
<div class="t" style="margin-top:8px">Proof of x + x'y = x + y</div>
<div class="fx">x + x'y = (x + x')(x + y)   (second distributive law)
        = 1·(x + y) = x + y   ∎</div></div>

<h3>5.4 Consensus theorem</h3>
<div class="fx">(a)  xy + x'z + yz = xy + x'z
(b)  (x+y)(x'+z)(y+z) = (x+y)(x'+z)</div>
<p>The term <code>yz</code> (the <i>consensus</i> of xy and x'z) is <b>redundant</b>: whenever yz = 1, either x=1 (then xy = 1) or x=0 (then x'z = 1), so the sum is already 1.</p>
<div class="ex"><div class="t">Proof of (a)</div>
<div class="fx">xy + x'z + yz = xy + x'z + yz(x + x')
              = xy + x'z + xyz + x'yz
              = xy(1+z) + x'z(1+y) = xy + x'z   ∎</div></div>
<div class="ex"><div class="t">Example 5.1 — simplify F = AB + A'C + BC + BCD</div>
<div class="fx">BC is the consensus of AB and A'C → delete BC; BCD is absorbed by BC (and also redundant)
F = AB + A'C</div></div>

<h3>5.5 Worked proofs</h3>
<div class="ex"><div class="t">Example 5.2 — Prove (A+B)(A'C'+C)·(B'+AC)' = A'B (your notes' exercise)</div>
<p><i>(In the notes the last factor is the complement of (B' + AC).)</i></p>
<div class="fx">Step 1  A'C' + C = A' + C            (x + x'y = x + y with x = C)
Step 2  (B' + AC)' = B·(AC)' = B(A' + C')     (De Morgan twice)
Step 3  LHS = (A+B)(A'+C)·B(A'+C')
Step 4  B(A+B) = B                            (absorption)
        LHS = B·(A'+C)(A'+C')
Step 5  (A'+C)(A'+C') = A' + CC' = A' + 0 = A'   (2nd distributive)
Step 6  LHS = B·A' = A'B  = RHS   ∎</div></div>
<div class="ex"><div class="t">Example 5.3 — simplify F = A'B'C + A'BC + AB'C + ABC + AB'C'</div>
<div class="fx">Group the first four: C(A'B' + A'B + AB' + AB) = C(1) = C
F = C + AB'C' = C + AB'      (x + x'y = x + y, with C' ≡ x')</div></div>
<div class="ex"><div class="t">Example 5.4 — simplify and give the NAND implementation of F = (A+B)(A+C)</div>
<div class="fx">F = A + BC  (second distributive law)
NAND form: F = ((A')·(BC)')' → NAND(A', NAND(B,C))</div></div>

<h3>5.6 Strategy when simplifying</h3>
<ol><li>Look for common factors; apply x+x'=1 and xy+xy'=x.</li><li>Apply absorption and x+x'y = x+y repeatedly.</li><li>Use consensus to kill redundant terms.</li><li>If it gets messy, <b>switch to a K-map</b> (Section 7) — it is mechanical and gives the minimum.</li><li>To prove an identity, work on the more complicated side only, or evaluate both sides with a truth table.</li></ol>
"""

# minterm tables
def mm_rows(n=3):
    vs = "xyz" if n == 3 else "wxyz"
    rows = []
    for i in range(2 ** n):
        bits = format(i, "0%db" % n)
        mt = "".join(v if b == "1" else v + "'" for v, b in zip(vs, bits))
        mx = "+".join(v if b == "0" else v + "'" for v, b in zip(vs, bits))
        rows.append([bits, "m<sub>%d</sub>" % i, mt, "M<sub>%d</sub>" % i, "(%s)" % mx])
    return rows

S6 = """
<h2 id="s6">6. Minterms, Maxterms &amp; Canonical Forms</h2>
<p>Any Boolean function can be written in two standard ("canonical") forms in which <b>every term contains every variable</b>:</p>
<ul><li><b>SOP</b> — Sum of Products (OR of AND terms) built from <b>minterms</b>.</li><li><b>POS</b> — Product of Sums (AND of OR terms) built from <b>maxterms</b>.</li></ul>
<h3>6.1 Definitions</h3>
<div class="box key"><b>Minterm m<sub>i</sub></b> — a product (AND) of all variables, each variable in true form if its bit is <b>1</b> and complemented if its bit is 0. It equals 1 for <b>exactly one</b> input combination (number i).<br>
<b>Maxterm M<sub>i</sub></b> — a sum (OR) of all variables, each variable in true form if its bit is <b>0</b> and complemented if 1. It equals 0 for <b>exactly one</b> combination.<br>
<b>Relation:</b> M<sub>i</sub> = (m<sub>i</sub>)'  and  m<sub>i</sub> = (M<sub>i</sub>)'.</div>
<p>Your notes' shortcut: <b>SOP (·) → "choose 1"</b> (read the rows where f = 1); <b>POS (+) → "choose 0"</b> (read the rows where f = 0).</p>
<div class="scroll">""" + tt(["x y z","Minterm index","Minterm","Maxterm index","Maxterm"], mm_rows(), "") + """</div>

<h3>6.2 Writing f in canonical form</h3>
<p>Notation: <code>f = Σ m(…)</code> lists rows where f = 1; <code>f = Π M(…)</code> lists rows where f = 0. For an n-variable function, <b>the indices missing from Σ are exactly those in Π</b> (from 0 to 2<sup>n</sup>−1).</p>
<div class="ex"><div class="t">Example 6.1 — the notes' f<sub>1</sub> = Σ(m<sub>0</sub>, m<sub>3</sub>, m<sub>7</sub>)</div>
""" + tt(["x y z","f<sub>1</sub>"],[[format(i,'03b'), 1 if i in (0,3,7) else 0] for i in range(8)]) + """
<div class="fx">SOP: f<sub>1</sub> = Σ(0,3,7) = x'y'z' + x'yz + xyz
POS: rows with f=0 are 1,2,4,5,6 →
     f<sub>1</sub> = Π(1,2,4,5,6) = (x+y+z')(x+y'+z)(x'+y+z)(x'+y+z')(x'+y'+z)</div>
<p class="box warn"><b>Why Π(0,3,7) is wrong</b>(it is crossed out in your notes). Π lists the <i>zero</i> rows, not the same numbers as Σ. Σ(0,3,7) ≠ Π(0,3,7); the correct partner is Π(1,2,4,5,6) = "the rest".</p></div>

<div class="ex"><div class="t">Example 6.2 — going via the complement (your notes' working)</div>
<p>Suppose we know f' = x'y'z' + x'yz' + x'yz + xy'z + xyz' = Σ(0,2,3,5,6). Then f = (f')' — complementing by De Morgan:</p>
<div class="fx">f = (x'y'z')'·(x'yz')'·(x'yz)'·(xy'z)'·(xyz')'
  = (x+y+z)(x+y'+z)(x+y'+z')(x'+y+z')(x'+y'+z)
  = M<sub>0</sub>·M<sub>2</sub>·M<sub>3</sub>·M<sub>5</sub>·M<sub>6</sub> = Π(0,2,3,5,6) = Σ(1,4,7)</div>
<p><b>Rule:</b> f' = Σ(list) ⟹ f = Π(same list). Complement of a function swaps Σ ↔ Π with the <i>same</i> index list.</p></div>

<h3>6.3 Expanding a non-canonical expression</h3>
<p>To convert to canonical SOP: for every term missing a variable v, multiply by (v + v') and expand. For POS, add v·v' to a sum term and distribute.</p>
<div class="ex"><div class="t">Example 6.3 — F(A,B,C) = A + B'C in canonical SOP and POS</div>
<div class="fx">A      = A(B+B')(C+C') = ABC + ABC' + AB'C + AB'C'  = m7+m6+m5+m4
B'C    = B'C(A+A')       = AB'C + A'B'C                = m5+m1
F = Σ(1,4,5,6,7)
POS: zeros are 0,2,3 → F = Π(0,2,3) = (A+B+C)(A+B'+C)(A+B'+C')</div></div>
<h3>6.4 Counting</h3>
<p>n variables → 2<sup>n</sup> minterms and 2<sup>2<sup>n</sup></sup> distinct functions (n=2: 16 functions; n=3: 256; n=4: 65 536).</p>
<h3>6.5 Non-canonical (minimal) forms</h3>
<p>A canonical form is long. We want a <b>minimal SOP/POS</b> (fewest terms, then fewest literals) — found with K-maps (next section).</p>
"""
