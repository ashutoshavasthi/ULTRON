import part1, part2, part3, part4
css = open("style.css").read()
toc = [("s1","Number Systems & Conversions"),("s2","Subtraction Using Complements"),("s3","Signed Numbers"),("s4","Logic Gates"),("s5","Boolean Algebra"),("s6","Minterms, Maxterms & Canonical Forms"),("s7","Karnaugh Maps"),("s8","Codes (BCD, 2421, XS-3, Gray…)"),("s9","Combinational Circuits (MUX, DEMUX, Encoder, Decoder, BCD Adder)"),("s10","Exam Toolkit: formula sheet, mistakes, practice")]
t = "".join('<li><a href="#%s">%s</a></li>' % x for x in toc)
body = part1.S1 + part1.S2 + part1.S3 + part2.S4 + part2.S5 + part2.S6 + part3.S7 + part3.S8 + part4.S9 + part4.S10
html = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Digital Electronics Complete Notes</title><style>%s</style></head>
<body><div class="wrap">
<header class="hero"><h1>Digital Electronics — Complete Study Notes</h1>
<p>Number systems → complements → gates → Boolean algebra → K-maps → codes → combinational circuits. Rebuilt from your class notes with full explanations, derivations and worked examples.</p></header>
<nav class="toc"><b>Contents</b><ol>%s</ol></nav>
<div class="box"><b>How to read these notes</b>Every section starts with the idea, then the rules, then worked examples tagged <i>(your notes)</i> where they come from your notebook. Prime (') means complement: A' = Ā. Σ = sum of minterms, Π = product of maxterms. Coloured dots in K-maps mark which group(s) a cell belongs to. Open the <i>practice</i> answers only after trying.</div>
%s
<p style="margin-top:40px;color:var(--mut)">End of notes — good luck!</p>
</div></body></html>""" % (css, t, body)
open("Digital_Electronics_Complete_Notes.html", "w").write(html)
print(len(html))
