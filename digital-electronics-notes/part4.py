from helpers import *

# ---------- generic "AND array" circuit generator (decoder / demux / mux style) ----------
def and_array(vars_, rows, outs, or_label=None):
    """vars_: [(name, has_complement)], rows: list of literal-lists, outs: output labels per row,
    or_label: if given, all AND outputs feed one OR gate with that output label."""
    x = 40
    bus = {}
    s = ""
    ybot = 0
    n_pins = max(len(r) for r in rows)
    H = 12 * (n_pins + 1)
    sp = H + 14
    top = 56
    ybot = top + len(rows) * sp
    for name, comp in vars_:
        bus[name] = x
        s += txt(x, 10, name, "middle")
        s += wire((x, 14), (x, ybot - 8)) + dot(x, 22)
        if comp:
            xc = x + 30
            bus[name + "'"] = xc
            s += wire((x, 22), (x + 7, 22))
            s += '<path d="M%d,16 L%d,22 L%d,28 Z"/>' % (x + 7, x + 19, x + 7)
            s += '<circle cx="%d" cy="22" r="3" fill="none"/>' % (x + 22)
            s += wire((x + 25, 22), (xc, 22)) + wire((xc, 22), (xc, ybot - 8))
            x += 70
        else:
            x += 42
    gx = x + 10
    ow = 24 + H // 2
    for i, r in enumerate(rows):
        y0 = top + i * sp
        s += '<path d="M%d,%d H%d A%d,%d 0 0 1 %d,%d H%d Z" class="gp"/>' % (gx, y0, gx + 24, H // 2, H // 2, gx + 24, y0 + H, gx)
        for j, lit in enumerate(r):
            py = y0 + 12 * (j + 1)
            s += wire((bus[lit], py), (gx, py)) + dot(bus[lit], py)
        oy = y0 + H // 2
        s += wire((gx + ow, oy), (gx + ow + 30, oy if not or_label else oy))
        if not or_label:
            s += txt(gx + ow + 34, oy + 4, outs[i])
    if or_label:
        ox = gx + ow + 30
        ytop = top - 6
        yb = top + (len(rows) - 1) * sp + H + 6
        mid = (ytop + yb) / 2
        s += '<path d="M%d,%d Q%d,%d %d,%d Q%d,%d %d,%d Q%d,%d %d,%d Z" class="gp"/>' % (
            ox, ytop, ox + 40, ytop, ox + 66, mid, ox + 40, yb, ox, yb, ox + 14, mid, ox, ytop)
        s += wire((ox + 66, mid), (ox + 96, mid)) + txt(ox + 100, mid + 4, or_label)
        w = ox + 120
    else:
        w = gx + ow + 90
    return svg(int(w), int(ybot + 10), s.replace('class="gp"', 'class="gp" style="fill:var(--card)"'))

def mux_table(ones, sel_vars, data_var, n=3, names="ABC"):
    """Return rows [select-bits, minterm pair, data input]"""
    rows = []
    idx = {v: names.index(v) for v in names}
    k = len(sel_vars)
    for s in range(2 ** k):
        bits = format(s, "0%db" % k)
        vals = []
        for dv in (0, 1):
            assign = {}
            for v, b in zip(sel_vars, bits):
                assign[v] = int(b)
            assign[data_var] = dv
            m = sum(assign[v] << (n - 1 - idx[v]) for v in names)
            vals.append(1 if m in ones else 0)
        expr = {(0, 0): "0", (1, 1): "1", (0, 1): data_var, (1, 0): data_var + "'"}[tuple(vals)]
        mins = sorted(sum(({**{v: int(b) for v, b in zip(sel_vars, bits)}, data_var: d}[v] << (n - 1 - idx[v])) for v in names) for d in (0, 1))
        rows.append([bits, "m%d, m%d" % tuple(mins), "I<sub>%d</sub> = %s" % (s, expr)])
    return rows

mux2_svg = and_array([("I1", False), ("I0", False), ("S0", True)], [["I0", "S0'"], ["I1", "S0"]], [], or_label="M")
demux14_svg = and_array([("I", False), ("S1", True), ("S0", True)], [["I", "S1'", "S0'"], ["I", "S1'", "S0"], ["I", "S1", "S0'"], ["I", "S1", "S0"]], ["m0", "m1", "m2", "m3"])
demux12_svg = and_array([("I", False), ("S0", True)], [["I", "S0'"], ["I", "S0"]], ["m0", "m1"])
dec24_svg = and_array([("E", False), ("A1", True), ("A0", True)], [["E", "A1'", "A0'"], ["E", "A1'", "A0"], ["E", "A1", "A0'"], ["E", "A1", "A0"]], ["D0", "D1", "D2", "D3"])
mux41_svg = and_array([("I0", False), ("I1", False), ("I2", False), ("I3", False), ("S1", True), ("S0", True)],
                      [["I0", "S1'", "S0'"], ["I1", "S1'", "S0"], ["I2", "S1", "S0'"], ["I3", "S1", "S0"]], [], or_label="Y")

def enc_svg():
    s = ""
    for k, (a, b) in enumerate([("E2", "E3"), ("E1", "E3")]):
        y = k * 70
        s += g_("or", 100, y + 10)
        s += txt(30, y + 24, a, "end") + wire((36, y + 20), (90, y + 20))
        s += txt(30, y + 44, b, "end") + wire((36, y + 40), (90, y + 40))
        s += wire((160, y + 30), (190, y + 30)) + txt(194, y + 34, "Y1" if k == 0 else "Y0")
    return svg(250, 150, s)

def bcd_adder_svg():
    s = box(20, 30, 210, 54, "4-bit binary adder I")
    s += wire((60, 0), (60, 30)) + txt(60, -6, "A3..A0 (digit 1)", "middle")
    s += wire((190, 0), (190, 30)) + txt(190, -6, "B3..B0 (digit 2)", "middle")
    s += wire((230, 57), (262, 57)) + txt(266, 61, "Cin (0 or carry from previous digit)") if False else ""
    s += wire((230, 40), (290, 40), (290, 122), (320, 122)) + txt(236, 36, "K (carry-out)")
    s += wire((60, 84), (60, 196)) + txt(66, 112, "S3 S2 S1 S0 (binary sum)")
    s += dot(60, 142) + wire((60, 142), (320, 142)) + txt(160, 138, "S3 S2 S1")
    s += box(320, 106, 230, 50, "Correction logic", "X = K + S3.S2 + S3.S1")
    s += wire((550, 131), (590, 131)) + txt(594, 135, "X = carry-out")
    s += box(20, 196, 210, 54, "4-bit binary adder II")
    s += wire((435, 156), (435, 223), (230, 223)) + txt(320, 218, "adds 0 X X 0 (= 0110 when X = 1)")
    s += wire((125, 250), (125, 282)) + txt(125, 296, "corrected BCD digit (BCD sum)", "middle")
    return svg(720, 300, s)

S9 = """
<h2 id="s9">9. Combinational Circuits &amp; Building Blocks</h2>
<p>A <b>combinational circuit</b> is a digital circuit whose outputs depend <b>only on the present inputs</b> (no memory, no feedback). Contrast: a <i>sequential</i> circuit has memory (flip-flops). Design procedure: (1) read the specification, (2) make a truth table, (3) simplify each output with K-maps, (4) draw with gates. Standard MSI blocks are the <b>multiplexer, demultiplexer, encoder, decoder</b> and the <b>adders</b>.</p>
<div class="gates" style="grid-template-columns:repeat(auto-fill,minmax(210px,1fr))">
<div class="g"><h4>Multiplexer</h4><p>2<sup>n</sup> data inputs → <b>1</b> output; <b>n select lines</b> choose which input passes. "Data selector".</p></div>
<div class="g"><h4>Demultiplexer</h4><p>1 input → one of 2<sup>n</sup> outputs; n select lines choose which output gets the data. "Data distributor".</p></div>
<div class="g"><h4>Encoder</h4><p>2<sup>n</sup> input lines → <b>n</b>-bit binary code (the number of the active line). Enable E.</p></div>
<div class="g"><h4>Decoder</h4><p><b>n</b>-bit code → 2<sup>n</sup> lines, exactly one active ("minterm generator"). Enable E.</p></div></div>
<p>An <b>Enable</b> pin allows the block to work only when asserted: <b>high-enabled → E</b>, <b>low-enabled → Ē (bar)</b> (your note "for noise").</p>

<h3>9.1 Multiplexer (MUX)</h3>
<h4>2:1 MUX</h4>
<div class="fx">M = S0'·I0 + S0·I1       S0 = 0 → M = I0 ;  S0 = 1 → M = I1</div>
<div class="pair"><div>""" + mux2_svg + """<p class="sm" style="text-align:center">Gate-level 2:1 MUX: AND gate A passes I0 when S0' = 1, AND gate B passes I1 when S0 = 1; the OR combines.</p></div></div>
<p>Your notes' example: inputs I1 = 0, I0 = 1, S0 = 0 → M = I0 = 1. 4:1 example: data (I0,I1,I2,I3) = (0,1,0,0), select S1S0 = 01 → output = I1 = 1.</p>
<h4>4:1 MUX</h4>
<div class="fx">Y = S1'S0'·I0 + S1'S0·I1 + S1S0'·I2 + S1S0·I3</div>
""" + tt(["S1","S0","Y"],[[0,0,"I0"],[0,1,"I1"],[1,0,"I2"],[1,1,"I3"]]) + mux41_svg + """
<p><b>General:</b> 2<sup>n</sup>:1 MUX has n select lines; Y = Σ m<sub>i</sub>·I<sub>i</sub> where m<sub>i</sub> is the select-line minterm. A MUX is itself a <b>universal logic block</b>.</p>

<h3>9.2 Demultiplexer (DEMUX)</h3>
<p>Opposite of a MUX: <b>I</b> is routed to the output chosen by the select lines; all other outputs are 0.</p>
<div class="pair"><div><b>1:2</b>""" + demux12_svg + """<div class="fx">m0 = S0'·I
m1 = S0·I</div></div></div>
<div><b>1:4</b>""" + demux14_svg + """<div class="fx">m0 = S1'S0'·I     m1 = S1'S0·I     m2 = S1S0'·I     m3 = S1S0·I</div></div>
<div class="box key"><b>DEMUX = decoder</b>A 1:2<sup>n</sup> demultiplexer and an n:2<sup>n</sup> decoder with enable are the same circuit: the DEMUX data input I plays the role of the decoder's enable E. Look at the two diagrams — they are identical.</div>

<h3>9.3 Decoder</h3>
<p>An <b>n:2<sup>n</sup> decoder</b> activates exactly <b>one</b> of 2<sup>n</sup> output lines according to the binary input. Each output is a <b>minterm</b> of the inputs: D<sub>i</sub> = m<sub>i</sub> (when enabled).</p>
""" + dec24_svg + """
""" + tt(["E","A1","A0","D3","D2","D1","D0"],[[0,"X","X",0,0,0,0],[1,0,0,0,0,0,1],[1,0,1,0,0,1,0],[1,1,0,0,1,0,0],[1,1,1,1,0,0,0]]) + """
<p>Your notes' example: inputs (A1,A0) = (1,0) with E = 1 → D2 = 1, all other outputs 0.</p>
<p><b>Complementary (active-low) decoder:</b> outputs are the <b>inverted</b> minterms, D<sub>i</sub>' = M<sub>i</sub> — the selected line is 0 and all others are 1. Built by replacing the AND gates with NAND gates. (Real chips such as the 74138 are of this kind.)</p>
<h4>Decoder tree (building a big decoder from small ones)</h4>
<ul><li><b>3:8 from two 2:4 decoders:</b> use A2 as the enable — A2' enables the first decoder (outputs D0–D3), A2 enables the second (D4–D7); A1,A0 go to both.</li>
<li><b>4:16 from five 2:4 decoders:</b> one decoder decodes A3A2 and each of its four outputs enables one of four decoders that decode A1A0 (1 + 4 = 5).</li></ul>

<h3>9.4 Encoder</h3>
<p>A <b>2<sup>n</sup>:n encoder</b> is the opposite of a decoder: exactly one of the 2<sup>n</sup> inputs is high and the output is the <b>binary number of that input</b>.</p>
""" + tt(["E3","E2","E1","E0","Y1","Y0","Meaning"],[[0,0,0,0,"X","X","no input active – meaningless"],[0,0,0,1,0,0,"input 0 (zeroth pin) is high"],[0,0,1,0,0,1,"input 1 is high"],[0,1,0,0,1,0,"input 2 is high"],[1,0,0,0,1,1,"input 3 is high"]]) + """
<div class="fx">Y1 = E2 + E3          Y0 = E1 + E3</div>""" + enc_svg() + """
<p><b>Problems of a plain encoder:</b> (a) when <b>no</b> input is high the output 00 is ambiguous with "input 0 active"; (b) if <b>two inputs</b> are high (e.g. 1100) the OR gates give a wrong code (11 = input 3). Solution: the <b>priority encoder</b>.</p>
<h4>Priority encoder</h4>
<p>When several inputs are high, the output shows the <b>highest-priority</b> one (convention: highest index = highest priority — E3 in your notes). Inputs below the winner are don't cares. A <b>valid bit V</b> (V = E3+E2+E1+E0) tells whether any input is active, resolving the all-zeros ambiguity.</p>
""" + tt(["E3","E2","E1","E0","Y1","Y0","V"],[[0,0,0,0,"X","X",0],[0,0,0,1,0,0,1],[0,0,1,"X",0,1,1],[0,1,"X","X",1,0,1],[1,"X","X","X",1,1,1]]) + """
<div class="fx">Y1 = E3 + E2            Y0 = E3 + E2'·E1            V = E3+E2+E1+E0</div>
<div class="ex"><div class="t">Example 9.1 — input 1100 into a priority encoder</div>
<p>E3 = 1 has the highest priority → Y1Y0 = 11, regardless of E2. Equations: Y1 = 1+1 = 1; Y0 = 1 + 1'·0 = 1 → 11 ✓. A plain encoder would also give 11 here but by accident; for 0110 a plain encoder gives Y1 = 1, Y0 = 1 (wrong, 3 instead of 2), the priority encoder gives Y0 = 0 + 1'·1 = 0 → 10 ✓.</p></div>

<h3>9.5 Implementing functions with a MUX</h3>
<p>A 2<sup>n</sup>:1 MUX with the n variables on the select lines can implement <b>any</b> n-variable function: tie each data input I<sub>i</sub> to <b>1 if m<sub>i</sub> is in the function, else 0</b>. A smarter trick implements an n-variable function on a <b>2<sup>n−1</sup>:1</b> MUX: put n−1 variables on the select lines and connect the remaining variable (or its complement, 0, or 1) to the data inputs.</p>
<div class="ex"><div class="t">Example 9.2 — F(A,B,C) = Σ(0,1,3,7) (your notes)</div>
""" + tt(["A","B","C","F"],[[(i>>2)&1,(i>>1)&1,i&1,1 if i in (0,1,3,7) else 0] for i in range(8)]) + """
<h4>(a) 8:1 MUX, select = ABC</h4>
<div class="fx">I0 = 1, I1 = 1, I2 = 0, I3 = 1, I4 = 0, I5 = 0, I6 = 0, I7 = 1      (S2 S1 S0 = A B C)</div>
<h4>(b) 4:1 MUX, select = A,B; data from C</h4>
""" + tt(["A B","Minterm pair","Data input"],mux_table({0,1,3,7},"AB","C")) + """
<p>So I0 = 1, I1 = C, I2 = 0, I3 = C (matches the notes' sketch).</p>
<h4>(c) 4:1 MUX, select = B,C; data from A</h4>
""" + tt(["B C","Minterm pair","Data input"],mux_table({0,1,3,7},"BC","A")) + """
<p>So I0 = A', I1 = A', I2 = 0, I3 = 1 (matches the notes).</p>
<h4>(d) 2:1 MUX, select = C; data are functions of A,B</h4>
<p>C = 0: F = Σ(0) → only A'B'C' → F|<sub>C=0</sub> = A'B' = (A+B)'  → I0 = NOR(A,B).<br>
C = 1: F = Σ(1,3,7) → A'B' + A'B + AB = A' + B → I1 = A' + B (a 2-input OR with inverted A).</p>
<p>The little K-maps in your notes (C=0 → A'B'; C=1 → A'+B) are exactly this step.</p></div>
<p><b>Procedure with a 2<sup>n−1</sup>:1 MUX:</b> pair the minterms that differ only in the data variable (the "minterm pair" column); for each pair the data input is 0 (neither), 1 (both), the variable (only the "1" half) or its complement (only the "0" half).</p>

<h3>9.6 Implementing functions with a decoder</h3>
<p>A decoder produces all minterms; <b>OR gates</b> (outside) combine the ones needed: <code>F = Σ m(…)</code> → OR the decoder outputs for the listed minterms. Several functions can share one decoder (one OR gate per function).</p>
<div class="ex"><div class="t">Example 9.3 — F(A,B,C) = Σ(1,2,4,6) (your notes' table)</div>
""" + tt(["A","B","C","F"],[[(i>>2)&1,(i>>1)&1,i&1,1 if i in (1,2,4,6) else 0] for i in range(8)]) + """
<p>3:8 decoder with inputs A,B,C → outputs D1, D2, D4, D6 are ORed: <b>F = D1 + D2 + D4 + D6</b> (a 4-input OR gate).</p></div>
<div class="box key"><b>Minimum-hardware choice (your note)</b>
<table class="left"><tr><th>Decoder type</th><th>Use the 1-minterms</th><th>Use the 0-minterms (if fewer)</th></tr>
<tr><td>Normal (active-high) decoder</td><td><b>OR</b> gate of the 1-minterms</td><td><b>NOR</b> gate of the 0-minterms (F = (Σ zeros)')</td></tr>
<tr><td>Complementary (active-low) decoder</td><td><b>NAND</b> gate of the 1-minterm outputs (F = (D'<sub>a</sub>·D'<sub>b</sub>…)')</td><td><b>AND</b> gate of the 0-minterm outputs</td></tr></table>
Pick whichever list (ones or zeros) is shorter so the output gate has fewer inputs.</div>
<div class="ex"><div class="t">Example 9.4 — Full adder with one 3:8 decoder</div>
<div class="fx">Sum  = Σ(1,2,4,7)  = D1 + D2 + D4 + D7       (4-input OR)
Cout = Σ(3,5,6,7)  = D3 + D5 + D6 + D7       (4-input OR)</div></div>

<h3>9.7 MUX tree</h3>
<p>Bigger multiplexers are built from smaller ones in a tree: the <b>low-order select lines drive the first level</b>, the high-order select lines drive the next level.</p>
<ul><li><b>8:1 from 4:1 and 2:1</b>: two 4:1 MUXes (both with S1,S0) take I0–I3 and I4–I7; a 2:1 MUX controlled by S2 picks between their outputs.</li>
<li><b>16:1 from 4:1</b>: four 4:1 MUXes (S1,S0) feed one 4:1 MUX (S3,S2): 5 MUXes in total.</li>
<li>2<sup>n</sup>:1 from 2:1 MUXes needs <b>2<sup>n</sup> − 1</b> MUXes.</li></ul>

<h3>9.8 Adders (needed for the BCD adder)</h3>
<p><b>Half adder</b> (adds two bits): Sum = A⊕B, Carry = A·B.<br>
<b>Full adder</b> (adds two bits + carry-in): Sum = A⊕B⊕C<sub>in</sub>, C<sub>out</sub> = AB + C<sub>in</sub>(A⊕B) = AB + BC<sub>in</sub> + AC<sub>in</sub>.</p>
""" + tt(["A","B","Cin","Sum","Cout"],[[(i>>2)&1,(i>>1)&1,i&1,((i>>2)^(i>>1)^i)&1, 1 if bin(i).count('1')>=2 else 0] for i in range(8)]) + """
<p>A <b>4-bit ripple-carry adder</b> chains four full adders: each carry-out feeds the next stage's carry-in. Delay grows with the number of bits (carry must ripple); carry-look-ahead adders fix this.</p>

<h3>9.9 BCD adder</h3>
<p>BCD stores one decimal digit in 4 bits. If we add two BCD digits with a <i>binary</i> adder, the result is right only while the sum is ≤ 9. Your notes' examples:</p>
<div class="fx">2 + 9:  0010 + 1001 = 1011   → 1011 is not a valid BCD digit (it's 11)
7 + 9:  0111 + 1001 = 1 0000 → carry 1 and digit 0000 — but 7+9 = 16, expected 0001 0110</div>
<p><b>Why?</b> 4 bits have 16 combinations but a decimal digit wraps at 10. Six codes (1010–1111) are skipped. So whenever the binary sum is ≥ 10 we are "6 short" in the units digit — <b>add 6 (0110)</b> to skip the invalid codes and generate the proper decimal carry.</p>
<div class="box key"><b>Correction rule</b> Add 0110 when:  (a) the binary adder produced a carry (K = 1: sum ≥ 16), <b>or</b> (b) the 4-bit sum is 1010–1111 i.e. S3·S2 = 1 or S3·S1 = 1.<br>
<code>X = K + S3·S2 + S3·S1</code> (your note: "AB + AC" form). X is also the carry-out to the next BCD digit.</div>
""" + bcd_adder_svg() + """
<p>Operation: Adder I adds the two digits (and the carry-in from the previous digit). If X = 1, Adder II adds <code>0 X X 0</code> = 0110 to the sum; otherwise it adds 0000. Adder II's carry-out is ignored (it only occurs when X = 1 and is already represented by X).</p>
<div class="ex"><div class="t">Example 9.5 — BCD addition cases</div>
""" + tt(["Sum","Binary adder (K S3 S2 S1 S0)","X","After +0110","Result"],[
["5 + 4","0 1001","0","—","9 (1001)"],
["2 + 9","0 1011","1 (S3S1)","1011 + 0110 = 1 0001","carry 1, digit 0001 → 11"],
["7 + 9","1 0000","1 (K)","0000 + 0110 = 0110","carry 1, digit 0110 → 16"],
["8 + 7","0 1111","1 (S3S2)","1111 + 0110 = 1 0101","carry 1, digit 0101 → 15"],
["9 + 9 + 1(cin)","1 0011","1 (K)","0011 + 0110 = 1001","carry 1, digit 1001 → 19"]]) + """
</div>
<div class="ex"><div class="t">Example 9.6 — two-digit BCD addition: 69 + 92 (your notes' digits)</div>
<div class="fx">69 = 0110 1001      92 = 1001 0010
Units : 1001 + 0010 = 1011 → X=1 → +0110 → 0001, carry 1
Tens  : 0110 + 1001 + 1(carry) = 1 0000 → K=1 → X=1 → +0110 → 0110, carry 1
Result: carry 1 | 0110 | 0001 = 161  ✓ (69 + 92 = 161)</div></div>
"""

S10 = """
<h2 id="s10">10. Exam Toolkit</h2>
<h3>10.1 One-page formula sheet</h3>
<div class="fx">COMPLEMENTS  r's: rⁿ − N   |  (r−1)'s: (rⁿ − 1) − N
2's = 1's + 1 ; carry → drop (2's) / add to LSB (1's) ; no carry → complement result, negative
SIGNED (n bits)  SM & 1's: ±(2ⁿ⁻¹−1)  |  2's: −2ⁿ⁻¹ … 2ⁿ⁻¹−1
DE MORGAN  (xy)' = x'+y'   (x+y)' = x'y'      NAND = bubbled OR, NOR = bubbled AND
XOR  A⊕B = A'B+AB'  (odd # of 1s)   XNOR = AB+A'B' (even # of 1s)
LAWS  x+x'y = x+y ; x+xy = x ; xy+xy' = x ; x+yz = (x+y)(x+z) ; xy+x'z+yz = xy+x'z
Σ(list of 1s) ↔ Π(list of 0s) ;  f' = Σ(L) ⇒ f = Π(L)
K-MAP  Gray order 00 01 11 10 ; groups 1,2,4,8,16 ; SOP: group 1s, const 1 → x, const 0 → x'
       POS: group 0s, const 1 → x', const 0 → x ; X = free
CODES  BCD 8421 | 2421, 5211, 84(−2)(−1), 642(−3): Σweights = 9 → self-compl. | XS-3 = BCD+3
GRAY   G = B ⊕ (B>>1) ;  B(i) = B(i+1) ⊕ G(i)
MUX    Y = Σ mᵢ·Iᵢ ; 2ⁿ:1 → n select ; 2ⁿ−1 two-to-one MUXes in a tree
DECODER Dᵢ = mᵢ (n:2ⁿ) ; DEMUX = decoder with E as data ; ENCODER 2ⁿ:n ; priority: Y1=E3+E2, Y0=E3+E2'E1
FULL ADDER S = A⊕B⊕C ; Cout = AB + C(A⊕B)
BCD ADDER  add 0110 if X = K + S3S2 + S3S1</div>

<h3>10.2 Common mistakes (and how to avoid them)</h3>
<ul>
<li><b>K-map labels 00,01,10,11</b> — must be 00,01,<b>11,10</b>.</li>
<li>Forgetting wrap-around groups (corners, left–right edges).</li>
<li>Groups of 3, 5, 6 — only powers of 2.</li>
<li>In POS K-map: writing the term in SOP polarity. Remember: constant 1 → complemented in the <b>sum</b> term.</li>
<li>Using Π(0,3,7) as the "POS of Σ(0,3,7)" — Π lists the <i>missing</i> minterms.</li>
<li>Using a don't-care as 1 when it doesn't enlarge any group (adds a needless term).</li>
<li>2's-complement subtraction: not padding to equal length; mis-reading the end carry (carry → positive in both methods).</li>
<li>Gray→binary: XOR-ing with the previous <i>Gray</i> bit instead of the previous <i>binary</i> bit.</li>
<li>Reading minterm index with the wrong bit order — first variable = MSB.</li>
<li>BCD adder: forgetting that a carry out of the first adder also needs correction (e.g. 7+9).</li>
</ul>

<h3>10.3 Practice problems</h3>
<p>Try each one before opening the answer.</p>
<details><summary>1. Convert (101101.101)<sub>2</sub> to decimal and (75.3125)<sub>10</sub> to binary.</summary>
<div class="fx">101101.101 = 32+8+4+1 + 0.5 + 0.125 = 45.625
75 = 1001011 ; 0.3125×2 = 0.625(0), ×2 = 1.25(1), 0.25×2 = 0.5(0), 0.5×2 = 1.0(1) → .0101
75.3125 = 1001011.0101</div></details>
<details><summary>2. Compute 1101 − 0111 using 2's complement and using 1's complement.</summary>
<div class="fx">2's: 2's comp of 0111 = 1001; 1101 + 1001 = 1 0110 → drop carry → 0110 = 6
1's: 1's comp of 0111 = 1000; 1101 + 1000 = 1 0101 → add carry: 0101 + 1 = 0110 = 6 ✓</div></details>
<details><summary>3. Write −13 in 8-bit sign-magnitude, 1's complement, 2's complement.</summary>
<div class="fx">+13 = 00001101
SM: 10001101 ; 1's: 11110010 ; 2's: 11110011</div></details>
<details><summary>4. Prove (A+B')(A'+B) = AB + A'B' and name the gate.</summary>
<div class="fx">(A+B')(A'+B) = AA' + AB + A'B' + BB' = 0 + AB + A'B' + 0 = AB + A'B'  → XNOR</div></details>
<details><summary>5. Simplify F = Σ(0,2,5,7,8,10,13,15) (A,B,C,D).</summary>
<div class="fx">{0,2,8,10} = B'D' (four corners) ; {5,7,13,15} = BD  → F = B'D' + BD = (B ⊙ D)</div></details>
<details><summary>6. Write F = x'y + xz as Σ and Π.</summary>
<div class="fx">x'y → 010,011 = 2,3 ; xz → 101,111 = 5,7  → F = Σ(2,3,5,7) = Π(0,1,4,6)</div></details>
<details><summary>7. Draw F = AB + CD using only NAND gates.</summary>
<div class="fx">F = ((AB)'·(CD)')' → three 2-input NANDs: NAND(A,B), NAND(C,D), then NAND of both outputs.</div></details>
<details><summary>8. Implement F = Σ(1,2,4,7) with a 4:1 MUX (select A,B).</summary>
""" + tt(["A B","Minterm pair","Data input"],mux_table({1,2,4,7},"AB","C")) + """
<p>F is the 3-input XOR (odd parity): I0 = C, I1 = C', I2 = C', I3 = C.</p></details>
<details><summary>9. Convert Gray 1101 to binary and binary 0110 to Gray.</summary>
<div class="fx">Gray 1101 → B3=1, B2=1⊕1=0, B1=0⊕0=0, B0=0⊕1=1 → 1001
Binary 0110 → G3=0, G2=0⊕1=1, G1=1⊕1=0, G0=1⊕0=1 → 0101</div></details>
<details><summary>10. Add 47 + 38 in BCD.</summary>
<div class="fx">Units: 0111 + 1000 = 1111 → X = S3S2 = 1 → +0110 = 1 0101 → digit 5, carry 1
Tens : 0100 + 0011 + 1 = 1000 → no correction → 8      → 85 ✓</div></details>
<details><summary>11. Which of these is a valid self-complementary weighted code: 3 3 2 1, 4 2 2 1, 6 3 1 1, 7 4 2 1?</summary>
<p>Sum of weights must be 9 (and include a 1): 3+3+2+1 = 9 ✓, 4+2+2+1 = 9 ✓, 6+3+1+1 = 11 ✗, 7+4+2+1 = 14 ✗. (Also check that all digits 0–9 can be formed; 3321 and 4221 can.)</p></details>
<details><summary>12. Draw a 3:8 decoder-based full adder.</summary>
<p>3:8 decoder with inputs A,B,Cin; Sum = OR(D1,D2,D4,D7); Cout = OR(D3,D5,D6,D7).</p></details>
<details><summary>13. A priority encoder receives E3E2E1E0 = 0110. What is Y1Y0?</summary>
<p>E2 is the highest active input → Y1Y0 = 10. (Using the equations: Y1 = E3+E2 = 1, Y0 = E3 + E2'E1 = 0.)</p></details>
<details><summary>14. How many 2:1 MUXes make a 16:1 MUX, and how many 2:4 decoders make a 4:16 decoder?</summary>
<p>15 (2<sup>4</sup>−1); 5 (1 + 4).</p></details>

<h3>10.4 Discrepancies found while rewriting your class notes</h3>
<ul>
<li><b>XNOR rule</b>: "even 0s" should be "even number of 1s" (equal only for 2 inputs).</li>
<li><b>Gray ⇄ binary labels</b> on the bracket are swapped relative to the procedure written beside them (see 8.6).</li>
<li><b>Π(0,3,7)</b> crossed out in your notes is indeed wrong for Σ(0,3,7); the right answer is Π(1,2,4,5,6).</li>
<li><b>Signed range</b>: "−2³ to 2³" should be −2³ … 2³−1 for 4-bit 2's complement.</li>
<li><b>POS K-map example</b>: Π list includes 8, while the Σ list also includes 8 — I solved with the Σ list (see 7.7).</li>
<li>A few handwritten K-maps (the fourth 4-variable map with answer "a'd' + cd' + ab'c + abd", the 5-variable examples and the first POS map) were too unclear to reproduce exactly; I replaced them with fully verified examples of the same type (7.7, 7.11). Please compare with your notebook.</li>
</ul>
"""
