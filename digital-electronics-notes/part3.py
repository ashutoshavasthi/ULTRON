from helpers import *

S7 = """
<h2 id="s7">7. Karnaugh Maps (K-maps)</h2>
<p>A <b>K-map</b> is a graphical truth table arranged so that <b>physically adjacent cells differ in exactly one variable</b>. Merging adjacent 1s applies <code>xy + xy' = x</code> visually, giving the minimal SOP without algebra.</p>

<h3>7.1 Layout</h3>
<ul><li>n variables → 2<sup>n</sup> cells. Each cell = one minterm; the small number in the corner of each cell below is the minterm index.</li>
<li><b>Row/column labels follow Gray code</b> — 00, 01, <b>11</b>, <b>10</b> (not 00,01,10,11!) so neighbours differ by one bit.</li>
<li>The map is a <b>torus</b>: the left edge is adjacent to the right edge, the top edge to the bottom edge, and the four corners are mutually adjacent.</li></ul>

<h3>7.2 Rules for grouping</h3>
<ol><li>Groups contain only 1s (or X's — see don't cares) and are <b>rectangles</b> (including wrap-around).</li>
<li>Group size must be a <b>power of 2</b>: 1, 2, 4, 8, 16. No diagonals, no L-shapes.</li>
<li>Make each group <b>as large as possible</b> (a largest possible group = a <b>prime implicant</b>, PI).</li>
<li>Cover <b>every 1</b> using the <b>fewest</b> groups. Start with 1s that can be covered by only one PI (<b>essential PIs</b>), then cover the rest.</li>
<li>Groups may <b>overlap</b>; a group that is entirely covered by others is redundant — drop it.</li>
<li><b>Reading a group:</b> a variable that is constant in the group appears in the product (as x if constant 1, x' if constant 0); variables that change inside the group disappear. A group of 2<sup>k</sup> cells eliminates k variables.</li></ol>

<h3>7.3 Two-variable map</h3>
<div class="ex"><div class="t">Example 7.1 — f = xy + xy' (your notes)</div>
<div class="pair">""" + kmap("x","y",{2,3},groups=[("x = 1 row (both cells)",[2,3])],title="f(x,y)") + tt(["x","y","f"],[[0,0,0],[0,1,0],[1,0,1],[1,1,1]]) + """</div>
<p>In the group x stays 1 while y takes both values → y disappears. <b>f = x</b> (algebra: xy + xy' = x(y+y') = x).</p></div>

<h3>7.4 Three-variable map</h3>
<div class="ex"><div class="t">Example 7.2 — f = Σ(1,3,5,6) (map 1 of your notes)</div>
""" + kmap("x","yz",{1,3,5,6},groups=[("x'z",[1,3]),("y'z",[1,5]),("xyz'",[6])],title="f(x,y,z)") + """
<p>Cell 1 belongs to two groups (overlap is fine). Cell 6 has no neighbour that is 1 → stays a full minterm. <b>f = x'z + y'z + xyz'</b> ✓ (matches the notes).</p></div>

<div class="ex"><div class="t">Example 7.3 — four corners: f<sub>1</sub> = Σ(0,2,4,6) and f<sub>2</sub> = Π(0,2,4,6)</div>
<div class="pair">""" + kmap("x","yz",{0,2,4,6},groups=[("z' (4 cells, wrap-around)",[0,2,4,6])],title="f1 = Σ(0,2,4,6)") + kmap("x","yz",{1,3,5,7},groups=[("z",[1,3,5,7])],title="f2 = Π(0,2,4,6)  (ones are the other cells)") + """</div>
<p>In f<sub>1</sub> the 1s are at columns yz = 00 and 10, which are adjacent through the wrap-around. Both y and x vary → only z' remains: <b>f<sub>1</sub> = z'</b>. For f<sub>2</sub>, a Π list names the <i>zeros</i>, so the ones are 1,3,5,7 → <b>f<sub>2</sub> = z</b>. (Notice f<sub>2</sub> = f<sub>1</sub>'.)</p></div>

<div class="ex"><div class="t">Example 7.4 — f = Σ(0,1,4,6)</div>
""" + kmap("x","yz",{0,1,4,6},groups=[("x'y'",[0,1]),("xz'",[4,6])]) + """
<p><b>f = x'y' + xz'</b> (notes ✓). The pair (4,6) shares x=1, z=0; the pair (0,1) shares x=0, y=0.</p></div>

<div class="ex"><div class="t">Example 7.5 — more 3-variable maps from your notes</div>
<div class="pair">""" + kmap("x","yz",{0,1,2,4,5,6},groups=[("y'",[0,1,4,5]),("z'",[0,2,4,6])],title="Σ(0,1,2,4,5,6)") + kmap("x","yz",{0,1,3,5},groups=[("x'y'",[0,1]),("x'z",[1,3]),("y'z",[1,5])],title="Σ(0,1,3,5)") + kmap("x","yz",{0,1,2,3,4,5,6},groups=[("x'",[0,1,2,3]),("y'",[0,1,4,5]),("z'",[0,2,4,6])],title="Σ(0..6) (all but 7)") + """</div>
<p>Results: <b>y' + z'</b>; <b>x'y' + x'z + y'z</b> (all three groups are essential — each covers a minterm no other group covers); <b>x' + y' + z'</b> (= (xyz)').</p></div>

<h3>7.5 Four-variable map</h3>
<p>16 cells; rows = first two variables, columns = last two, both in Gray order. Possible groups: 1, 2, 4 (a row, a column, a 2×2 block or the four corners), 8 (two adjacent rows/columns) and 16.</p>
<div class="ex"><div class="t">Example 7.6 — your notes' 4-variable map (variables x y z w)</div>
""" + kmap("xy","zw",{0,1,4,5,7,8,9,10,11,12,14,15},groups=[("z'w' (column 00)",[0,4,8,12]),("x'yw",[5,7]),("y'z'",[0,1,8,9]),("xz",[10,11,14,15])],title="f(x,y,z,w)") + """
<p><b>f = z'w' + x'yw + y'z' + xz</b> — identical to the answer in your notes. Two groups of 4 plus another 4 (y'z' is a 2×2 block formed with wrap-around from rows 00 and 10) and one pair.</p></div>

<div class="ex"><div class="t">Example 7.7 — f(A,B,C,D) = Σ(0,1,2,5,8,9,10), worked fully</div>
""" + kmap("AB","CD",{0,1,2,5,8,9,10},groups=[("B'D' (four corners)",[0,2,8,10]),("B'C'",[0,1,8,9]),("A'C'D",[1,5])],title="f(A,B,C,D)") + """
<ol><li>Four corners {0,2,8,10} → B'D'.</li><li>Rows 00 and 10 in columns 00/01 {0,1,8,9} → B'C'.</li><li>Cell 5 is only adjacent (as a 1) to cell 1 → pair {1,5} → A'C'D.</li></ol>
<p><b>f = B'D' + B'C' + A'C'D</b>. Check minterm 5 (A=0,B=1,C=0,D=1): A'C'D = 1 ✓; minterm 7 (0111): B'D'=0, B'C'=0, A'C'D=0 → 0 ✓.</p></div>

<h3>7.6 Don't-care conditions</h3>
<p>For some input combinations the output is <b>irrelevant</b> — they never occur (e.g. BCD inputs 1010–1111) or we don't care. Mark them <b>X</b> (written d(…)). In the K-map an X can be treated as <b>1 if it helps make a bigger group</b>, otherwise ignored (as 0). Never create a group made only of X's.</p>
<div class="ex"><div class="t">Example 7.8 — f = Σ(1,2,6,8,10) + d(0,4,9) (your notes)</div>
""" + kmap("xy","zw",{1,2,6,8,10},dc={0,4,9},groups=[("y'w'",[0,2,8,10]),("y'z'",[0,1,8,9]),("x'w'",[0,2,4,6])],title="f(x,y,z,w)") + """
<p>The X at 0 joins all three groups; X at 9 completes y'z'; X at 4 helps x'w'. <b>f = y'w' + y'z' + x'w'</b> ✓ (matches the notes). Without don't cares the groups would be far smaller.</p></div>
<div class="ex"><div class="t">Example 7.9 — f = Σ(1,5,6,10) + d(3,8) (your notes; variables a b c d)</div>
""" + kmap("ab","cd",{1,5,6,10},dc={3,8},groups=[("ab'd'",[8,10]),("a'c'd",[1,5]),("a'bcd'",[6])],title="f(a,b,c,d)") + """
<p>X at 8 pairs with 10 → ab'd'. X at 3 is <i>not</i> needed (using it would not enlarge any group), so we leave it as 0. <b>f = ab'd' + a'c'd + a'bcd'</b> ✓.</p></div>

<h3>7.7 POS K-map (product of sums)</h3>
<p>To get the minimal <b>POS</b>, group the <b>0s</b> instead of the 1s (X's still usable). Each group gives a <b>sum term</b> in which a variable is written <b>complemented if it is constant 1</b> in the group and <b>true if constant 0</b> (the opposite of SOP reading). The product of all sum terms is f. Reason: grouping zeros gives f' as SOP; complementing with De Morgan flips the polarity.</p>
<div class="ex"><div class="t">Example 7.10 — f = Σ(0,1,4,6,8,12,14) + d(2,3,5), minimal POS</div>
<p>The notes write this as Π(7,8,9,10,11,13,15). Listing all 16 cells: ones {0,1,4,6,8,12,14}, don't-cares {2,3,5} ⇒ zeros are {7,9,10,11,13,15}. (Minterm 8 appears in the notes' Π list but also in the Σ list — one of those is a slip. I solved with the Σ list.)</p>
""" + kmap("xy","zw",{7,9,10,11,13,15},dc={2,3,5},zero_mode=True,groups=[("yw → (y'+w')",[5,7,13,15]),("xw → (x'+w')",[9,11,13,15]),("y'z → (y+z')",[2,3,10,11])],title="Group the 0s") + """
<div class="fx">f = (y' + w')(x' + w')(y + z')</div>
<p>Check: minterm 7 (0111) → y'+w' = 0+0 = 0 ✓ (should be 0); minterm 0 (0000) → all three sums are 1 ✓. Equivalent SOP of complement: f' = yw + xw + y'z.</p></div>
<div class="box key"><b>Which to choose?</b>If the problem asks for SOP use the 1s; for POS use the 0s. Both give a correct minimal circuit; use whichever has fewer/larger groups when the form is not specified. SOP → NAND-NAND; POS → NOR-NOR.</div>

<h3>7.8 Five-variable map</h3>
<p>Variables x y z w r (x = MSB, r = LSB). Use <b>two 4-variable maps</b> stacked on top of each other: one for x = 0 (minterms 0–15) and one for x = 1 (minterms 16–31). Rows are yz and columns wr (Gray order) in both. Your notes show this layout, and an alternative that splits on r instead (r = 0 holds the even minterms, r = 1 the odd ones).</p>
<div class="pair">""" + kmap("yz","wr",set(),title="x = 0 (minterms 0–15)") + kmap("yz","wr",set(),title="x = 1 (minterms 16–31)",off=16) + """</div>
<p><b>Adjacency in 5 variables:</b> (i) the usual 4-variable adjacency inside each layer (including wrap-around); (ii) <b>the same cell position in the two layers is adjacent</b> (x changes, nothing else) — imagine the x = 1 map laid directly over the x = 0 map. Groups can therefore span both layers: a group of 8 gives a 2-variable term, 16 gives 1 variable, etc.</p>
<div class="ex"><div class="t">Example 7.11 — f = Σ(0,2,4,6,11,15,16,18,20,22,27,31)</div>
<div class="pair">""" + kmap("yz","wr",{0,2,4,6,11,15},groups=[("y'r' (layer 0 part)",[0,2,4,6]),("ywr (layer 0 part)",[11,15])],title="x = 0") + kmap("yz","wr",{16,18,20,22,27,31},off=16,groups=[("y'r' (layer 1 part)",[16,18,20,22]),("ywr (layer 1 part)",[27,31])],title="x = 1") + """</div>
<ul><li>Group A: cells 0,2,4,6 (layer 0) <i>and</i> 16,18,20,22 (layer 1) — 8 cells. Constant in the group: y=0 and r=0. x, z, w change. → <b>y'r'</b>.</li>
<li>Group B: cells 11,15 and 27,31 — 4 cells. Constant: y=1, w=1, r=1. → <b>ywr</b>.</li></ul>
<p><b>f = y'r' + ywr.</b> (Verified by listing all 12 minterms.)</p></div>
<p>For six variables use four 4-variable maps; beyond that use the <b>Quine–McCluskey</b> tabular method (same idea, computer-friendly).</p>

<h3>7.9 K-map checklist for the exam</h3>
<ol><li>Fill the map from the truth table / minterm list (double-check the Gray-order row/column labels).</li><li>Mark isolated 1s first, then 1s with exactly one possible largest group.</li><li>Use X's only to enlarge groups.</li><li>Verify by testing two or three cells against your final expression.</li></ol>
"""

def table_code(weights, codes):
    return tt(["Digit"] + [str(w) for w in weights], [[d] + list(c) for d, c in codes.items()])

b2421 = {0:'0000',1:'0001',2:'0010',3:'0011',4:'0100',5:'1011',6:'1100',7:'1101',8:'1110',9:'1111'}
b5211 = {0:'0000',1:'0001',2:'0011',3:'0101',4:'0111',5:'1000',6:'1010',7:'1100',8:'1110',9:'1111'}
b84 = {0:'0000',1:'0111',2:'0110',3:'0101',4:'0100',5:'1011',6:'1010',7:'1001',8:'1000',9:'1111'}

def codes_table():
    h = '<div class="scroll"><table class="tt"><tr><th>Digit</th><th>BCD 8421</th><th>2421</th><th>5211</th><th>8 4 −2 −1</th><th>Excess-3</th><th>Gray (4-bit idx)</th></tr>'
    for d in range(10):
        h += "<tr><td>%d</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (d, format(d,"04b"), b2421[d], b5211[d], b84[d], format(d+3,"04b"), format(d^(d>>1),"04b"))
    return h + "</table></div>"

def gray_table():
    return tt(["Dec","Binary","Gray"],[[i,format(i,"04b"),format(i^(i>>1),"04b")] for i in range(16)])

S8 = """
<h2 id="s8">8. Codes</h2>
<p>A <b>code</b> is a systematic way to represent symbols (here, decimal digits or numbers) by bit patterns. Different codes are chosen for ease of arithmetic, error reduction, or hardware simplicity.</p>

<h3>8.1 Classification</h3>
<div class="fx">Codes
 ├─ Weighted      (each bit position has a fixed weight; value = Σ weight × bit)
 │    ├─ Positively weighted : 8 4 2 1 (BCD), 2 4 2 1, 5 2 1 1
 │    └─ Negatively weighted : 8 4 −2 −1,  6 4 2 −3   (some weights are negative)
 └─ Non-weighted  (no positional weights)   : Excess-3 (XS-3), Gray</div>

<h3>8.2 Weighted codes and BCD</h3>
<p><b>BCD (Binary Coded Decimal, 8421)</b> writes each decimal digit 0–9 as its 4-bit binary value. A multi-digit number is coded digit by digit: <code>92 → 1001 0010</code> and <code>69 → 0110 1001</code> (your notes). It is <b>not</b> the same as the binary value of 92 (1011100). Codes 1010–1111 are <b>invalid</b> in BCD (6 wasted combinations) — they become <b>don't cares</b> in design.</p>
<h4>How to choose weights for a valid decimal code (your notes)</h4>
<ul><li>The <b>sum of all weights must be at least 9</b> (otherwise 9 cannot be made).</li><li>There must be a weight of <b>1</b> (so that the digit 1 can be represented).</li></ul>
<p>Examples that work: 8 4 2 1 (sum 15), 2 4 2 1 (sum 9), 5 2 1 1 (sum 9).</p>

<h3>8.3 Self-complementary codes</h3>
<div class="box key"><b>Definition</b>A decimal code is <b>self-complementary</b> if the <b>9's complement</b> of a digit is obtained by simply <b>inverting all four bits</b> of its code word: code(9−N) = (code(N))'. Useful because decimal subtraction by 9's complement needs no extra circuit.<br>
<b>Condition (weighted codes):</b> the weights must add up to exactly <b>9</b>. So 2421, 5211, 8 4 −2 −1, 6 4 2 −3 and (non-weighted) Excess-3 are self-complementary; <b>8421 BCD is not</b> (sum = 15).</div>
<h4>The 2421 code (from your notes)</h4>
<p>Generation trick: write digits 0–4 as 0000,0001,0010,0011,0100 and obtain <b>5–9 by complementing the codes of 4–0</b> (5 = comp(4), 6 = comp(3), …). That guarantees self-complementation.</p>
""" + codes_table() + """
<p>Check weights for 2421, digit 7 = 1101 → 2+4+0+1 = 7 ✓; digit 5 = 1011 → 2+0+2+1 = 5 ✓. For 8 4 −2 −1, digit 7 = 1001 → 8 −1 = 7 ✓. For 5211, digit 8 = 1110 → 5+2+1 = 8 ✓. (Several code words can represent the same digit in these weight systems; the table lists the self-complementary choice.)</p>
<div class="ex"><div class="t">Example 8.1 — verify self-complementing for 2421: digit 3 and 6</div>
<div class="fx">3 → 0011,  complement → 1100 → that is digit 6 = 9 − 3 ✓
2 → 0010,  complement → 1101 → digit 7 = 9 − 2 ✓</div></div>

<h3>8.4 Converting 2421 to BCD (design with K-maps)</h3>
<p>Let the 2421 input bits be <b>x y z w</b> (weights 2,4,2,1) and the BCD output bits be <b>B3 B2 B1 B0</b>. Valid 2421 words are digits 0–9 (cells 0,1,2,3,4,11,12,13,14,15); cells 5,6,7,8,9,10 never occur → <b>don't cares</b>. Solve four K-maps (the notes show B<sub>0</sub> and B<sub>1</sub>).</p>
<p>Truth table (input → desired BCD):</p>
<div class="scroll">""" + tt(["Digit","x y z w (2421)","B3 B2 B1 B0 (BCD)"],[[d, b2421[d], format(d,"04b")] for d in range(10)]) + """</div>
<div class="pair">""" + kmap("xy","zw",{1,3,11,13,15},dc={5,6,7,8,9,10},groups=[("w (all odd cells)",[1,3,5,7,9,11,13,15])],title="B0 = w") + kmap("xy","zw",{2,3,12,13},dc={5,6,7,8,9,10},groups=[("x'z",[2,3,6,7]),("xz'",[8,9,12,13])],title="B1 = x'z + xz'") + """</div>
<div class="pair">""" + kmap("xy","zw",{4,11,12,13},dc={5,6,7,8,9,10},groups=[("yz'",[4,5,12,13]),("xy'",[8,9,10,11])],title="B2 = yz' + xy'") + kmap("xy","zw",{14,15},dc={5,6,7,8,9,10},groups=[("yz",[6,7,14,15])],title="B3 = yz") + """</div>
<div class="fx">B0 = w          B1 = x'z + xz' = x ⊕ z          B2 = yz' + xy'          B3 = yz</div>
<p>Test: digit 8 = 1110 (x=1,y=1,z=1,w=0): B3 = 1·1 = 1; B2 = 1·0 + 1·0 = 0; B1 = 1⊕1 = 0; B0 = 0 → 1000 = 8 ✓. Digit 5 = 1011: B3 = 0·1 = 0; B2 = 0·0 + 1·1 = 1; B1 = 1⊕1 = 0; B0 = 1 → 0101 ✓.</p>

<h3>8.5 Excess-3 (XS-3) code</h3>
<p><b>XS-3 = BCD + 3 (0011)</b>. It is non-weighted. Its purpose, as in your note: <b>to avoid the all-zero code word</b> (a dead line looks like 0000) — and it is self-complementary, which simplifies subtraction.</p>
""" + tt(["Digit","BCD","XS-3","Digit","BCD","XS-3"],[[d, format(d,"04b"), format(d+3,"04b"), d+5, format(d+5,"04b"), format(d+8,"04b")] for d in range(5)]) + """
<p>Unused XS-3 words: 0000, 0001, 0010, 1101, 1110, 1111. Self-complement check: 3 → 0110, complement 1001 = 6 = 9−3 ✓ (arrow in your notes).</p>
<div class="ex"><div class="t">Example 8.2 — XS-3 addition rule</div>
<p>Adding two XS-3 digits adds an excess of 6. <b>If a carry results, add 3 (0011) to the sum; if no carry, subtract 3 (add 1101, ignore carry).</b></p>
<div class="fx">4 + 3:  0111 + 0110 = 1101 (no carry) → subtract 3 → 1010 = XS-3 of 7 ✓
8 + 7:  1011 + 1010 = 1 0101 (carry) → add 3 to 0101 → 1000 = XS-3 of 5, carry digit 1 → XS-3 0100
        result 0100 1000 = XS-3 of 15 ✓</div></div>

<h3>8.6 Gray code</h3>
<p>The <b>Gray code</b> (reflected binary code) is a <b>cyclic, non-weighted</b> code in which <b>only one bit changes between consecutive code words</b> (including from the last word back to the first). This prevents transient errors when several bits would otherwise change at once (e.g. in rotary encoders) and is the reason K-map axes use 00,01,11,10.</p>
<h4>Reflect-and-prefix construction (shown in your notes)</h4>
<ol><li>1-bit Gray: <code>0, 1</code>.</li><li>To get the (n+1)-bit code: write the n-bit list, then <b>reflect</b> (write it again in reverse order below a mirror line); prefix <b>0</b> to the top half and <b>1</b> to the mirrored bottom half.</li></ol>
<div class="fx">1 bit: 0 1
2 bit: 00 01 | 11 10         (mirror after 01; prefix 0 on top, 1 on bottom)
3 bit: 000 001 011 010 | 110 111 101 100
4 bit: (above, with 0 prefix) | (reflected with 1 prefix) → table below</div>
""" + gray_table() + """
<h4>Binary ⇄ Gray with XOR</h4>
<div class="box key"><b>Binary → Gray:</b> MSB copied as is; every other Gray bit = <b>XOR of two adjacent binary bits</b>: G<sub>i</sub> = B<sub>i+1</sub> ⊕ B<sub>i</sub>.<br>
<b>Gray → Binary:</b> MSB copied as is; every other binary bit = <b>previous (higher) <u>binary</u> bit XOR current Gray bit</b>: B<sub>i</sub> = B<sub>i+1</sub> ⊕ G<sub>i</sub>. (Running XOR down the word.)</div>
<p class="box warn"><b>Notebook clarification</b>The notes list "second = first ⊕ second, third = second ⊕ third, …". Applied to the <i>given</i> bits (adjacent pairs of the input) that is the <b>binary → Gray</b> rule (as the arrow picture for 1110 shows). For Gray → binary you XOR with the <i>already-computed binary</i> bit, not with the previous Gray bit.</p>
<div class="ex"><div class="t">Example 8.3 — binary 1110 → Gray</div>
<div class="fx">G3 = 1
G2 = B3⊕B2 = 1⊕1 = 0
G1 = B2⊕B1 = 1⊕1 = 0
G0 = B1⊕B0 = 1⊕0 = 1        → Gray = 1001   (table: 14 → 1001 ✓)</div>
<div class="t" style="margin-top:8px">Example 8.4 — Gray 1011 → binary</div>
<div class="fx">B3 = 1
B2 = B3⊕G2 = 1⊕0 = 1
B1 = B2⊕G1 = 1⊕1 = 0
B0 = B1⊕G0 = 0⊕1 = 1        → binary = 1101 = 13   (table: 13 → 1011 ✓)</div></div>

<h3>8.7 Summary table of all codes</h3>
""" + codes_table() + """
"""
