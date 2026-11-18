"""Assembles src/*.html + figs/*.png into one self-contained vlsi_notes.html"""
import base64, glob, os, re, html
here = os.path.dirname(os.path.abspath(__file__))
parts = sorted(glob.glob(os.path.join(here, "src", "*.html")))
head = open(parts[0]).read()
body = "\n".join(open(p).read() for p in parts[1:])

def fig(m):
    name, _, cap = m.group(1).partition("|")
    data = base64.b64encode(open(os.path.join(here, "figs", name + ".png"), "rb").read()).decode()
    alt = html.escape(cap or name)
    return f'<figure><img alt="{alt}" src="data:image/png;base64,{data}">' + (f"<figcaption>{cap}</figcaption>" if cap else "") + "</figure>"
body = re.sub(r"\{\{fig:([^}]+)\}\}", fig, body)
body = re.sub(r"\[\[(.+?)\|(.+?)\]\]", lambda m: f'<span class="frac"><span>{m.group(1).strip()}</span><span>{m.group(2).strip()}</span></span>', body)

toc = []
for m in re.finditer(r'<section class="chapter" id="(ch\d+)">\s*<h2><span class="num">CHAPTER (\d+)</span>(.*?)</h2>', body, re.S):
    toc.append(f'<a href="#{m.group(1)}"><b>{int(m.group(2)):02d}</b>{m.group(3)}</a>')
nav = '<nav class="rail"><div class="brand">VLSI Mastery Notes</div><div class="list">' + "".join(toc) + "</div></nav>"
out = head + '\n<div class="wrap">' + nav + "<main>" + body + "</main></div>\n"
open(os.path.join(here, "vlsi_notes.html"), "w").write(out)
print(len(out) / 1e6, "MB;", len(toc), "chapters")
assert "{{" not in re.sub(r"data:image[^\"]+", "", out), "unreplaced fig"
assert "[[" not in re.sub(r"data:image[^\"]+", "", out), "unreplaced frac"
