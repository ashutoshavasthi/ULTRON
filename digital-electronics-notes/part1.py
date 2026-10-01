from helpers import *

S1 = """
<h2 id="s1">1. Number Systems &amp; Conversions</h2>
<p>A <b>number system</b> is a way of writing numbers using a fixed set of symbols (<b>digits</b>). The count of distinct digits is the <b>base</b> (also called <b>radix</b>, written <code>r</code>). A number is written <code>(N)<sub>r</sub></code>, meaning "N written in base r".</p>

<h3>1.1 Positional (weighted) notation</h3>
<p>In every positional system, each digit is multiplied by a power of the base that depends on its position. Positions to the left of the point have powers <code>r<sup>0</sup>, r<sup>1</sup>, r<sup>2</sup>…</code>; positions to the right have <code>r<sup>-1</sup>, r<sup>-2</sup>…</code>.</p>
<div class="fx">(d<sub>n</sub> … d<sub>1</sub> d<sub>0</sub> . d<sub>-1</sub> d<sub>-2</sub> …)<sub>r</sub>  =  Σ d<sub>i</sub> × r<sup>i</sup></div>
<p>Your notes' example: <code>(56)<sub>10</sub> = 5×10<sup>1</sup> + 6×10<sup>0</sup></code>.</p>

<table class="left"><tr><th>System</th><th>Base r</th><th>Digits</th><th>Typical use</th></tr>
<tr><td>Decimal</td><td>10</td><td>0–9</td><td>Everyday numbers</td></tr>
<tr><td>Binary</td><td>2</td><td>0, 1 (<b>bits</b>)</td><td>All digital hardware (a gate is ON/OFF)</td></tr>
<tr><td>Octal</td><td>8</td><td>0–7</td><td>Compact shorthand: 1 octal digit = 3 bits</td></tr>
<tr><td>Hexadecimal</td><td>16</td><td>0–9, A–F (A=10 … F=15)</td><td>Compact shorthand: 1 hex digit = 4 bits</td></tr></table>

<div class="box key"><b>Why binary?</b>A transistor switch has two reliable states (high/low voltage), so the base-2 system maps perfectly onto hardware. LSB = <i>least significant bit</i> (rightmost, weight 2<sup>0</sup>); MSB = <i>most significant bit</i> (leftmost, largest weight).</div>

<h3>1.2 Binary → Decimal</h3>
<p>Multiply each bit by its weight and add.</p>
<div class="ex"><div class="t">Example 1.1 — (101101)<sub>2</sub> to decimal</div>
<div class="fx">1×32 + 0×16 + 1×8 + 1×4 + 0×2 + 1×1 = 32 + 8 + 4 + 1 = 45</div>
<div class="t" style="margin-top:8px">Example 1.2 — (111000.0110)<sub>2</sub> to decimal (the answer of your notes' 56.42 example)</div>
<div class="fx">Integer part : 32 + 16 + 8        = 56
Fraction part: 0×½ + 1×¼ + 1×⅛ + 0×1/16 = 0.25 + 0.125 = 0.375
Total        : 56.375   (≈ 56.42, not exactly — see 1.3)</div></div>

<h3>1.3 Decimal → Binary</h3>
<h4>(a) Integer part: repeated division by 2</h4>
<p>Divide by 2 again and again, record each <b>remainder</b>, stop at quotient 0. Read the remainders <b>from bottom to top</b> (last remainder = MSB).</p>
<div class="ex"><div class="t">Example 1.3 — (56)<sub>10</sub> → binary (your notes)</div>
""" + tt(["÷","Quotient","Remainder"],[["56 ÷ 2","28","0 (LSB)"],["28 ÷ 2","14","0"],["14 ÷ 2","7","0"],["7 ÷ 2","3","1"],["3 ÷ 2","1","1"],["1 ÷ 2","0","1 (MSB)"]]) + """
<p>Read upward: <b>(111000)<sub>2</sub></b>. Check: 32+16+8 = 56 ✓.</p></div>

<h4>(b) Fraction part: repeated multiplication by 2</h4>
<p>Multiply the fraction by 2. The <b>integer part</b> that pops out (0 or 1) is the next bit; keep only the new fraction and repeat. Read bits <b>top to bottom</b> (first bit = ½ place).</p>
<div class="ex"><div class="t">Example 1.4 — (0.42)<sub>10</sub> → binary (your notes)</div>
""" + tt(["Step","Calculation","Integer bit","New fraction"],[["1","0.42 × 2 = 0.84","0","0.84"],["2","0.84 × 2 = 1.68","1","0.68"],["3","0.68 × 2 = 1.36","1","0.36"],["4","0.36 × 2 = 0.72","0","0.72"]]) + """
<p>So 0.42 ≈ <b>(0.0110)<sub>2</sub></b>, and therefore <b>(56.42)<sub>10</sub> ≈ (111000.0110)<sub>2</sub></b>.</p>
<p><i>Why "≈"?</i> Many decimal fractions never terminate in binary (like ⅓ in decimal). Four bits give 0.375; more steps (0.72→1.44→1, 0.44→0.88→0, …) give 0.0110101110… getting closer to 0.42. In an exam, stop at the number of bits asked for.</p>
<p class="box warn"><b>Margin note in your notebook</b>"42 → 101010" is the conversion of the <i>whole number</i> 42. Don't mix it up with the fraction .42, which is handled by multiplication, not division.</p></div>

<h3>1.4 Octal and Hexadecimal shortcuts</h3>
<p>Because 8 = 2<sup>3</sup> and 16 = 2<sup>4</sup>, conversion with binary is just <b>grouping bits</b> — no arithmetic.</p>
<ul><li><b>Binary → Octal:</b> group in 3s starting at the binary point (pad with zeros outward). </li>
<li><b>Binary → Hex:</b> group in 4s the same way.</li>
<li><b>Octal/Hex → Binary:</b> replace each digit by its 3-bit / 4-bit pattern.</li></ul>
<div class="ex"><div class="t">Example 1.5 — (111000.0110)<sub>2</sub></div>
<div class="fx">Octal: 111 000 . 011 000  →  (70.30)<sub>8</sub>      (7×8 = 56, .3 = 3/8 = 0.375 ✓)
Hex  : 0011 1000 . 0110  →  (38.6)<sub>16</sub>      (3×16+8 = 56, .6 = 6/16 = 0.375 ✓)</div></div>
""" + tt(["Dec","Bin","Oct","Hex"],[[i,format(i,"04b"),format(i,"o"),format(i,"X")] for i in range(16)]) + """

<h3>1.5 Binary arithmetic</h3>
<table class="tt"><tr><th colspan="2">Addition</th><th colspan="2">Subtraction</th></tr>
<tr><td>0+0 = 0</td><td>1+0 = 1</td><td>0−0 = 0</td><td>1−0 = 1</td></tr>
<tr><td>1+1 = 10 (sum 0, carry 1)</td><td>1+1+1 = 11 (sum 1, carry 1)</td><td>1−1 = 0</td><td>0−1 = 1 with <b>borrow 1</b></td></tr></table>
<p><b>Borrow</b> works like decimal: to compute 0−1 you borrow 1 from the next-higher bit, which is worth 2 in the current column, so 2−1 = 1.</p>
<div class="ex"><div class="t">Example 1.6 — (100)<sub>2</sub> − (011)<sub>2</sub> (your notes: answer 001)</div>
<div class="fx">  column 0: 0−1 → borrow from column 1 (which is 0, so it must borrow from column 2)
  column 2 becomes 0, column 1 becomes 2 → lends 1 → column 1 = 1, column 0 = 2
  column 0: 2−1 = 1 ;  column 1: 1−1 = 0 ;  column 2: 0−0 = 0
  Result = 001     (check: 4 − 3 = 1 ✓)</div></div>
<p>Borrow chains get error-prone for long numbers; hardware avoids them by using <b>complements</b> — the next section.</p>
"""

S2 = """
<h2 id="s2">2. Subtraction Using Complements</h2>
<p>Computers have no separate subtractor in the CPU's core: they turn <code>A − B</code> into <code>A + (complement of B)</code> and reuse the adder. There are two complements for any base r:</p>
<table class="left"><tr><th>Name</th><th>Binary (r=2)</th><th>Decimal (r=10)</th><th>How to get it (n-digit number N)</th></tr>
<tr><td><b>Radix complement</b> (r's)</td><td>2's complement</td><td>10's complement</td><td><code>r<sup>n</sup> − N</code></td></tr>
<tr><td><b>Diminished radix complement</b> ((r−1)'s)</td><td>1's complement</td><td>9's complement</td><td><code>(r<sup>n</sup> − 1) − N</code></td></tr></table>
<div class="box key"><b>Fast hand methods</b>
<ul><li><b>1's complement</b>: flip every bit (0↔1). Equivalent: 9's complement = subtract every digit from 9.</li>
<li><b>2's complement</b>: 1's complement + 1. Shortcut: copy bits from the right up to <i>and including</i> the first 1, then flip all bits to the left.</li>
<li><b>10's complement</b> = 9's complement + 1 (add 1 at the last digit).</li></ul></div>

<h3>2.1 Subtraction by 2's complement (radix complement)</h3>
<ol><li><b>Equalise digits:</b> pad the shorter number with leading zeros so both have the same number of digits.</li>
<li><b>Complement the subtrahend</b> (the number being subtracted) → take its 2's complement.</li>
<li><b>Add</b> it to the minuend.</li>
<li><b>Look at the end carry (EOC / end-around carry):</b>
  <ul><li><b>Carry generated</b> → result is positive and correct. <b>Discard (ignore) the carry.</b></li>
  <li><b>No carry</b> → result is negative and is in 2's-complement form. Take the <b>2's complement of the sum and put a minus sign</b> (your note: "if EAC not generated, 2's complement again, put −ve sign").</li></ul></li></ol>
<div class="ex"><div class="t">Example 2.1 — 101101 − 11011 (your notes' example; 45 − 27)</div>
<div class="fx">Minuend  X = 101101
Subtrahend Y = 11011  → pad → 011011
2's comp of Y: flip → 100100, +1 → 100101

   101101
 + 100101
 ---------
 1 010010      ← carry generated → ignore it
   010010  = 10010 = 18   ✓ (45 − 27 = 18)</div></div>
<div class="ex"><div class="t">Example 2.2 — 011011 − 101101 (27 − 45, a negative answer)</div>
<div class="fx">2's comp of 101101: flip → 010010, +1 → 010011
   011011
 + 010011
 ---------
   101110   ← no carry → answer is negative
2's comp of 101110: flip → 010001, +1 → 010010 = 18  → result = −18 ✓</div></div>

<h3>2.2 Subtraction by 1's complement (diminished radix)</h3>
<p>Same steps, but with the 1's complement, and the carry rule is different:</p>
<ol><li>Pad to equal length; take the <b>1's complement</b> of the subtrahend; add.</li>
<li><b>Carry generated</b> → add that carry to the LSB of the sum (<b>end-around carry</b>); the result is positive.</li>
<li><b>No carry</b> → take the 1's complement of the sum and put a minus sign.</li></ol>
<div class="ex"><div class="t">Example 2.3 — 101101 − 011011 with 1's complement</div>
<div class="fx">1's comp of 011011 = 100100
  101101
+ 100100
--------
1 010001   ← carry out → wrap around: 010001 + 1 = 010010 = 18 ✓</div></div>
<div class="ex"><div class="t">Example 2.4 — 011011 − 101101 with 1's complement</div>
<div class="fx">1's comp of 101101 = 010010
  011011 + 010010 = 101101   ← no carry
1's comp of 101101 = 010010 = 18 → −18 ✓</div></div>

<h3>2.3 The same idea in decimal (10's and 9's complement)</h3>
<div class="ex"><div class="t">Example 2.5 — 463.42 − 546.001 using 10's complement (your notes)</div>
<div class="fx">Step 1 — equal digits: X = 463.420,  Y = 546.001
Step 2 — 10's comp of Y: 9's comp = 453.998, +0.001 → 453.999
Step 3 — add:  463.420 + 453.999 = 917.419   ← no carry out
Step 4 — no carry ⇒ negative: 10's comp of 917.419
          9's comp = 082.580, +0.001 → 082.581
Answer = −82.581      check: 463.42 − 546.001 = −82.581 ✓</div></div>
<div class="box warn"><b>Mnemonic</b>Carry → positive → drop it (r's) or add it back (r−1's). No carry → negative → complement the sum again and write "−". "Radix complement discards, diminished radix wraps around."</div>
<p><b>Why does it work?</b> A − B = A + (r<sup>n</sup> − B) − r<sup>n</sup>. The extra r<sup>n</sup> shows up as the carry out of the n-th digit, so discarding the carry removes it. If A &lt; B, the sum is r<sup>n</sup> − (B−A), i.e. the complement of the (negative) answer — hence complement it back.</p>

<h3>2.4 Practice</h3>
<details><summary>Q: Compute 1001 − 0110 and 0110 − 1001 using 2's complement</summary>
<div class="fx">9−6: 2's comp of 0110 = 1010; 1001+1010 = 1 0011 → drop carry → 0011 = 3 ✓
6−9: 2's comp of 1001 = 0111; 0110+0111 = 1101 (no carry) → 2's comp = 0011 → −3 ✓</div></details>
"""

S3 = """
<h2 id="s3">3. Signed Numbers</h2>
<p>To store negative numbers in hardware we dedicate the <b>MSB as the sign bit S</b>: <b>0 → positive (+ve), 1 → negative (−ve)</b>. The remaining bits hold the magnitude (or its complement). There are three standard formats. The notes use 4 bits and the number 6:</p>
""" + tt(["Format","+6","−6","How −6 is made"],[["Sign-magnitude","0110","1110","Flip only the sign bit"],["1's complement","0110","1001","Flip <i>all</i> bits of +6"],["2's complement","0110","1010","1's complement + 1 (1001 + 1)"]]) + """
<p>(Your notes show these three codes for −6: <code>1001, 1010, 1110</code>.)</p>

<h3>3.1 Range of n-bit numbers</h3>
""" + tt(["Format","Range (n bits)","n = 4","Zeros"],[["Sign-magnitude","−(2<sup>n−1</sup>−1) … +(2<sup>n−1</sup>−1)","−7 … +7","Two (+0 = 0000, −0 = 1000)"],["1's complement","−(2<sup>n−1</sup>−1) … +(2<sup>n−1</sup>−1)","−7 … +7","Two (0000, 1111)"],["2's complement","−2<sup>n−1</sup> … +(2<sup>n−1</sup>−1)","−8 … +7","<b>One</b> (0000)"]]) + """
<p>(Your note "−2³ to 2³" is the rough range; precisely it is <b>−2<sup>3</sup> to 2<sup>3</sup>−1</b> for 2's complement with 4 bits.)</p>
<div class="box key"><b>Why 2's complement wins</b>One zero, a single adder works for both signed and unsigned operands, and subtraction = addition. Almost every computer uses it.</div>

<h3>3.2 Reading a signed number</h3>
<div class="ex"><div class="t">Example 3.1 — what does 1011 mean (4-bit)?</div>
<div class="fx">Sign-magnitude : sign 1, magnitude 011 = 3          → −3
1's complement : negative, flip → 0100 = 4          → −4
2's complement : negative, flip+1 → 0101 = 5        → −5
Weighted view (2's comp): −8 + 0 + 2 + 1 = −5  ✓</div></div>

<h3>3.3 Overflow</h3>
<p>If the true result doesn't fit in n bits, the answer is wrong. For 2's-complement addition: overflow occurs when two operands of the <b>same sign</b> give a result of the <b>opposite sign</b> (equivalently carry into the MSB ≠ carry out of the MSB). Adding numbers of opposite sign can never overflow.</p>
<div class="ex"><div class="t">Example 3.2 — 4-bit: 5 + 6</div>
<div class="fx">0101 + 0110 = 1011 → looks like −5 : OVERFLOW (11 is outside −8…+7)</div></div>

<h3>3.4 Sign extension</h3>
<p>To widen a 2's-complement number copy the sign bit leftwards: 1010 (−6) → 11111010 (−6); 0110 (+6) → 00000110.</p>
"""
