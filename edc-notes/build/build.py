#!/usr/bin/env python3
"""Build EDC_Complete_Notes.html (single self-contained file) from content/*.md.

markdown (+ ::: boxes, {{fig}} tags, $math$) -> HTML, math via KaTeX (node), figures inlined as data-URI SVG,
KaTeX fonts inlined as base64 -> one file that works offline.
"""
import base64, glob, html, json, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import markdown

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(ROOT, "content")
BUILD = os.path.join(ROOT, "build")
FIGS = os.path.join(ROOT, "figs")
OUT = os.path.join(ROOT, "EDC_Complete_Notes.html")

BOX_LABEL = {
    "kid": "Explain it like I’m 10", "formula": "Formula box", "ex": "Worked example", "trap": "Exam trap",
    "try": "Try it yourself", "note": "Note", "class": "In your class notes", "flag": "Heads-up: check this",
    "remember": "Remember", "words": "Words and symbols you need", "soln": "Answers and full solutions",
}
BOX_ICON = {"kid": "🧒", "formula": "∑", "ex": "✎", "trap": "⚠", "try": "?", "note": "i", "class": "📓", "flag": "⚑", "remember": "★", "words": "Aa", "soln": "✔"}


# ---------------------------------------------------------------- nested boxes -> variable-length fences
def fix_nested_boxes(text):
    lines = text.split("\n")
    open_re = re.compile(r"^:{3,} *\w+")
    close_re = re.compile(r"^:{3,}\s*$")
    stack = []      # indices of opener lines
    height = {}     # opener idx -> subtree height
    closer_of = {}
    for i, ln in enumerate(lines):
        if open_re.match(ln):
            stack.append(i); height[i] = 0
        elif close_re.match(ln) and stack:
            o = stack.pop(); closer_of[o] = i
            if stack:
                height[stack[-1]] = max(height[stack[-1]], height[o] + 1)
    for o, c in closer_of.items():
        n = 3 + height[o]
        lines[o] = ":" * n + re.sub(r"^:{3,}", "", lines[o]); lines[c] = ":" * n
    return "\n".join(lines)


def fix_lists(text):
    out = []; prev = ""
    li = re.compile(r"^(\s*)(\d+\.|[*-]) ")
    for ln in text.split("\n"):
        if li.match(ln) and prev.strip() and not li.match(prev) and not prev.startswith((" ", "\t", "|", ":::", "<")):
            out.append("")
        out.append(ln); prev = ln
    return "\n".join(out)


def add_abbr(text):
    from glossary import G
    terms = sorted(G, key=len, reverse=True)
    chunks = re.split(r"(?m)^(?=# )", text)
    res = []
    for ch in chunks:
        lines = ch.split("\n"); done = set(); inwords = False
        for i, ln in enumerate(lines):
            if ln.startswith(":::") and "words" in ln.split()[:2]: inwords = True; continue
            if inwords:
                if re.match(r"^:{3,}\s*$", ln): inwords = False
                continue
            if ln.startswith(("#", ":::", "{{fig", "<div", "</div")) or "<summary>" in ln or "<details" in ln: continue
            parts = re.split(r"(<abbr[^>]*>.*?</abbr>|<[^>]+>)", ln)
            for pi in range(0, len(parts), 2):
                seg = parts[pi]
                found = []
                for t in terms:
                    if t in done: continue
                    m = re.search(r"(?<![\w@-])" + re.escape(t) + r"(?![\w-])", seg)
                    if m: found.append((m.start(), m.end(), t))
                found.sort(key=lambda x: (x[0], -(x[1] - x[0])))
                out = []; pos = 0
                for st, en, t in found:
                    if st < pos: continue
                    tip = G[t].replace('"', "'")
                    out.append(seg[pos:st]); out.append(f'<abbr title="{tip}">{t}</abbr>'); pos = en; done.add(t)
                out.append(seg[pos:])
                parts[pi] = "".join(out)
            ln = "".join(parts)
            lines[i] = ln
        res.append("\n".join(lines))
    return "".join(res)


def protect_math(text):
    store = []

    def stash(tex, display):
        store.append({"id": f"m{len(store)}", "tex": tex.strip(), "display": display})
        return f"@@{store[-1]['id']}@@"

    text = re.sub(r"\$\$(.+?)\$\$", lambda m: stash(m.group(1), True), text, flags=re.S)
    text = re.sub(r"(?<![\\$])\$([^\n$]+?)\$", lambda m: stash(m.group(1), False), text)
    return text, store


def render_math(store):
    if not store:
        return {}
    p = subprocess.run(["node", os.path.join(BUILD, "katex_render.js")], input=json.dumps(store), capture_output=True, text=True, cwd=BUILD)
    if p.stderr.strip():
        print(p.stderr, file=sys.stderr)
    return json.loads(p.stdout)


md = markdown.Markdown(extensions=["tables", "fenced_code", "attr_list", "sane_lists", "md_in_html", "nl2br"])


def md_convert(text):
    md.reset()
    return md.convert(text)


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", re.sub(r"<[^>]+>|@@m\d+@@", "", s).lower()).strip("-") or "x"


def svg_data_uri(name):
    p = os.path.join(FIGS, name + ".svg")
    if not os.path.exists(p):
        print("MISSING FIGURE", name, file=sys.stderr)
        return ""
    return "data:image/svg+xml;base64," + base64.b64encode(open(p, "rb").read()).decode()


def katex_css():
    css = open(os.path.join(BUILD, "katex", "dist", "katex.min.css"), encoding="utf-8").read()
    fdir = os.path.join(BUILD, "katex", "dist", "fonts")

    def sub(m):
        fam = m.group(1)
        f = os.path.join(fdir, fam + ".woff2")
        return "url(data:font/woff2;base64," + base64.b64encode(open(f, "rb").read()).decode() + ") format('woff2')"

    css = re.sub(r"url\(fonts/(KaTeX_[A-Za-z0-9_-]+)\.woff2\) format\(\"woff2\"\),\s*url\([^)]*\) format\(\"woff\"\),\s*url\([^)]*\) format\(\"truetype\"\)", sub, css)
    css = re.sub(r"url\(fonts/(KaTeX_[A-Za-z0-9_-]+)\.woff2\) format\(\"woff2\"\)", sub, css)
    return css


def build():
    files = sorted(glob.glob(os.path.join(CONTENT, "*.md")))
    raw = "\n\n".join(open(f, encoding="utf-8").read() for f in files)
    raw = fix_nested_boxes(raw)
    raw = fix_lists(raw)
    raw, store = protect_math(raw)
    raw = add_abbr(raw)

    stash_html = []

    def keep(h):
        stash_html.append(h)
        return f"\n\n@@H{len(stash_html)-1}@@\n\n"

    def fig(m):
        parts = [p.strip() for p in m.group(1).split("|")]
        name = parts[0]; cap = parts[1] if len(parts) > 1 else ""; w = parts[2] if len(parts) > 2 else "80"
        cap_html = md_convert(cap).replace("<p>", "").replace("</p>", "") if cap else ""
        alt = html.escape(re.sub(r"@@m\d+@@", "", re.sub(r"<[^>]+>", "", cap_html)))
        return keep(f'<figure style="width:min(100%,{w}%)"><div class="figcard"><img loading="lazy" alt="{alt}" src="{svg_data_uri(name)}"/></div>'
                    f'<figcaption>{cap_html}</figcaption></figure>')

    raw = re.sub(r"\{\{fig\s+([^}]+)\}\}", fig, raw)
    raw = raw.replace("<!--TOOLS-->", keep(open(os.path.join(BUILD, "tools.html"), encoding="utf-8").read()) if os.path.exists(os.path.join(BUILD, "tools.html")) else "")

    # boxes, longest fence first
    for n in range(3, 9):
        pat = re.compile(rf"^:{{{n}}} *(\w+)[ \t]*([^\n]*)\n(.*?)^:{{{n}}}[ \t]*$", re.S | re.M)

        def box(m):
            kind, title, body = m.group(1), m.group(2).strip(), m.group(3)
            label = BOX_LABEL.get(kind, kind.title())
            t = html.escape(label) + (f": {md_convert(title).replace('<p>','').replace('</p>','')}" if title else "")
            return keep(f'<div class="box {kind}"><div class="bt"><span class="bi">{BOX_ICON.get(kind, "")}</span>{t}</div>{md_convert(body)}</div>')

        raw = pat.sub(box, raw)

    body = md_convert(raw)
    for _ in range(6):
        if "@@H" not in body:
            break
        for i in range(len(stash_html) - 1, -1, -1):
            body = body.replace(f"<p>@@H{i}@@</p>", stash_html[i]).replace(f"@@H{i}@@", stash_html[i])

    # heading ids + navigation
    nav = []
    used = set()

    def head(m):
        level, attrs, inner = int(m.group(1)), m.group(2), m.group(3)
        if "notoc" in attrs:
            return m.group(0)
        s = slug(inner); base, n = s, 2
        while s in used:
            s = f"{base}-{n}"; n += 1
        used.add(s)
        if level <= 2:
            nav.append((level, s, inner))
        return f'<h{level} id="{s}"{attrs}><a class="anchor" href="#{s}" aria-label="link">#</a>{inner}</h{level}>'

    body = re.sub(r"<h([1-3])([^>]*)>(.*?)</h\1>", head, body, flags=re.S)

    # wrap each chapter in a <section>
    parts = re.split(r'(?=<h1 id=)', body)
    body = parts[0] + "".join(f'<section class="chapter">{p}</section>' for p in parts[1:])

    math = render_math(store)
    texmap = {m["id"]: m["tex"] for m in store}
    nav_plain = {}
    for (l, sl, i) in nav:
        p = re.sub(r"<[^>]+>", "", i)
        p = re.sub(r"@@(m\d+)@@", lambda m: texmap.get(m.group(1), ""), p)
        nav_plain[sl] = re.sub(r"\\[a-z]+\s?|[{}_^]", lambda m: "" if m.group(0) in "{}" else ("" if m.group(0).startswith("\\") else "" if m.group(0) in "_^" else m.group(0)), p)
    for k, v in math.items():
        body = body.replace(f"@@{k}@@", v)

    navhtml = []
    for level, s, inner in nav:
        plain = nav_plain.get(s, re.sub(r"<[^>]+>", "", inner))
        if level == 1:
            navhtml.append(f'<li class="n1"><label class="done" title="mark chapter as studied"><input type="checkbox" data-ch="{s}"><span></span></label><a href="#{s}">{plain}</a></li>')
        else:
            navhtml.append(f'<li class="n2"><a href="#{s}">{plain}</a></li>')

    css = open(os.path.join(BUILD, "style.css"), encoding="utf-8").read()
    js = open(os.path.join(BUILD, "app.js"), encoding="utf-8").read()
    doc = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>EDC Complete Mastery Notes</title>
<style>{katex_css()}</style>
<style>{css}</style></head>
<body>
<header class="top"><button id="menu" aria-label="menu">☰</button><span class="brand">EDC · Mastery Notes</span>
<span class="sp"></span><button id="ans" title="reveal or hide every answer">Answers: hidden</button><button id="theme" title="dark / light">◐</button></header>
<nav id="side"><div class="search"><input id="q" placeholder="filter chapters…" autocomplete="off"></div><ul>{''.join(navhtml)}</ul>
<div class="prog"><div id="bar"></div></div><div class="progtxt" id="progtxt"></div></nav>
<main id="main">{body}</main>
<script>{js}</script>
</body></html>"""
    open(OUT, "w", encoding="utf-8").write(doc)
    print("built", OUT, f"{os.path.getsize(OUT)/1e6:.1f} MB", "sections:", len([n for n in nav if n[0] == 1]))


if __name__ == "__main__":
    build()
