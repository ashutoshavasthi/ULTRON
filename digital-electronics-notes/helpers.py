# Helpers: K-map tables, truth tables, SVG gate drawing
COLORS = ["#e11d48", "#2563eb", "#16a34a", "#d97706", "#7c3aed", "#0891b2"]

def gray(n):
    return [i ^ (i >> 1) for i in range(2 ** n)]

def kmap(rowvars, colvars, ones, dc=(), groups=(), title="", zero_mode=False, off=0):
    """rowvars/colvars: strings like 'xy','zw'. cells hold minterm numbers.
    groups: list of (label, [minterms]). zero_mode shows 0s as the target (POS)."""
    nr, nc = len(rowvars), len(colvars)
    rg = [format(g, "0%db" % nr) for g in gray(nr)]
    cg = [format(g, "0%db" % nc) for g in gray(nc)]
    ones, dc = set(ones), set(dc)
    gl = {}
    for gi, (lab, cells) in enumerate(groups):
        for c in cells:
            gl.setdefault(c, []).append(gi)
    h = '<div class="kmwrap"><table class="kmap">'
    if title:
        h += '<caption>%s</caption>' % title
    h += '<tr><th class="corner"><span class="rv">%s</span>\\<span class="cv">%s</span></th>' % (rowvars, colvars)
    for c in cg:
        h += '<th>%s</th>' % c
    h += '</tr>'
    for r in rg:
        h += '<tr><th>%s</th>' % r
        for c in cg:
            m = int(r + c, 2) + off
            if m in dc: v, cls = "X", "dc"
            elif m in ones: v, cls = ("0" if zero_mode else "1"), "one"
            else: v, cls = ("1" if zero_mode else "0"), "zero"
            if zero_mode:
                # in zero_mode `ones` lists the zeros of f
                pass
            dots = "".join('<i style="background:%s"></i>' % COLORS[g % 6] for g in gl.get(m, []))
            bg = ""
            if m in gl:
                bg = ' style="background:%s22"' % COLORS[gl[m][0] % 6]
            h += '<td class="%s"%s><b>%s</b><small>%d</small><span class="dots">%s</span></td>' % (cls, bg, v, m, dots)
        h += '</tr>'
    h += '</table>'
    if groups:
        h += '<ul class="glegend">'
        for gi, (lab, cells) in enumerate(groups):
            h += '<li><i style="background:%s"></i> %s &nbsp;<span class="mono">(cells %s)</span></li>' % (COLORS[gi % 6], lab, ",".join(map(str, sorted(cells))))
        h += '</ul>'
    return h + '</div>'

def tt(headers, rows, cls=""):
    h = '<table class="tt %s"><tr>' % cls + "".join("<th>%s</th>" % x for x in headers) + "</tr>"
    for r in rows:
        h += "<tr>" + "".join("<td>%s</td>" % x for x in r) + "</tr>"
    return h + "</table>"

# ---------- SVG gates (each drawn in a 60x40 box at origin, out at (60,20)) ----------
def g_(kind, x, y, label=""):
    s = '<g transform="translate(%d,%d)" class="gate">' % (x, y)
    body = {
        "and": 'M0,0 H28 A20,20 0 0 1 28,40 H0 Z',
        "or": 'M0,0 Q22,0 48,20 Q22,40 0,40 Q12,20 0,0 Z',
        "xor": 'M6,0 Q28,0 52,20 Q28,40 6,40 Q18,20 6,0 Z',
        "not": 'M0,4 L34,20 L0,36 Z',
    }
    k = kind.replace("nand", "and").replace("xnor", "xor").replace("nor", "or")
    s += '<path d="%s"/>' % body[k]
    if k == "xor":
        s += '<path d="M0,0 Q12,20 0,40" fill="none"/>'
    bub = kind in ("nand", "nor", "xnor", "not")
    outx = {"and": 48, "or": 48, "xor": 52, "not": 34}[k]
    if bub:
        s += '<circle cx="%d" cy="20" r="4" fill="#fff"/>' % (outx + 4)
        outx += 8
    s += '<path d="M%d,20 H60" fill="none"/>' % outx
    if k == "not":
        s += '<path d="M-10,20 H0" fill="none"/>'
    else:
        s += '<path d="M-10,10 H%d M-10,30 H%d" fill="none"/>' % (4 if k != "xor" else 8, 4 if k != "xor" else 8)
    if label:
        s += '<text x="22" y="24" class="gl">%s</text>' % label
    return s + '</g>'

def gate_icon(kind):
    return '<svg viewBox="-14 -2 84 44" width="110" height="58">%s</svg>' % g_(kind, 0, 0)

def svg(w, h, inner):
    return '<svg class="circ" viewBox="-16 -18 %d %d" width="%d" style="max-width:100%%">%s</svg>' % (w + 16, h + 18, w + 16, inner)

def wire(*pts):
    return '<polyline points="%s" fill="none"/>' % " ".join("%d,%d" % p for p in pts)

def dot(x, y):
    return '<circle cx="%d" cy="%d" r="2.8" class="jd"/>' % (x, y)

def txt(x, y, s, anchor="start", cls="t"):
    return '<text x="%d" y="%d" text-anchor="%s" class="%s">%s</text>' % (x, y, anchor, cls, s)

def box(x, y, w, h, label, sub=""):
    s = '<rect x="%d" y="%d" width="%d" height="%d" rx="4" class="bx"/>' % (x, y, w, h)
    s += '<text x="%d" y="%d" text-anchor="middle" class="t b">%s</text>' % (x + w // 2, y + h // 2 + (0 if not sub else -2), label)
    if sub:
        s += '<text x="%d" y="%d" text-anchor="middle" class="t sm">%s</text>' % (x + w // 2, y + h // 2 + 14, sub)
    return s
