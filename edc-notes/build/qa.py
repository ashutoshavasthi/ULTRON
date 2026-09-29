from playwright.sync_api import sync_playwright
url="file:///home/user/ULTRON/edc-notes/EDC_Complete_Notes.html"
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome",args=["--no-sandbox"])
    pg=b.new_page(viewport={"width":1300,"height":900}); msgs=[]
    pg.on("console",lambda m: msgs.append(m.text)); pg.on("pageerror",lambda e: msgs.append("PAGEERR "+str(e)))
    pg.goto(url); pg.wait_for_timeout(2500)
    print("errors:",msgs[:5])
    txt=pg.evaluate("document.body.innerText")
    for bad in ["MATH ERROR","@@","{{fig",":::","$$","\\frac","\\dfrac"]:
        print(bad, txt.count(bad))
    print("katex-error", pg.evaluate("document.querySelectorAll('.katex-error').length"))
    print("imgs", pg.evaluate("document.querySelectorAll('img').length"))
    pg.evaluate("document.querySelectorAll('img').forEach(i=>i.loading='eager')"); pg.wait_for_timeout(2500)
    print("broken imgs", pg.evaluate("[...document.querySelectorAll('img')].filter(i=>!i.complete||i.naturalWidth===0).length"))
    print("boxes",pg.evaluate("document.querySelectorAll('.box').length"),"details",pg.evaluate("document.querySelectorAll('details').length"))
    # stray raw markdown
    import re
    for pat in [r"\*\*[A-Za-z]", r"^\|.*\|$"]:
        m=re.findall(pat,txt,re.M); print(pat,len(m), m[:3])
    # calculators
    def setv(i,val): pg.evaluate("(a)=>{var e=document.getElementById(a[0]);e.value=a[1];e.dispatchEvent(new Event('input'))}",[i,str(val)])
    def out(i): return pg.evaluate("document.getElementById('%s').textContent"%i)
    setv('d-i0',1);setv('d-v',0.2);setv('d-t',27);pg.select_option('#d-eta','1');print(out('d-out'))
    print(out('z-out'))
    setv('r-vm',110);print(out('r-out'))
    pg.select_option('#f-type','l');setv('f-l',4);setv('f-rl',750);print(out('f-out'))
    pg.select_option('#f-type','pi');setv('f-l',5);setv('f-rl',1000);setv('f-c1',100);setv('f-c2',100);print(out('f-out'))
    print(out('u-out'))
    print(out('b-out'))
    pg.select_option('#b-cfg','divider');setv('b-vcc',18);setv('b-beta',50);setv('b-rc',5.6);setv('b-re',1.2);pg.select_option('#b-by','1');print(out('b-out'))
    pg.select_option('#b-cfg','follower');setv('b-vcc',20);setv('b-beta',90);setv('b-rb',240);setv('b-re',2);print(out('b-out'))
    b.close()
