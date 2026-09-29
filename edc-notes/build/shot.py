import sys
from playwright.sync_api import sync_playwright
url="file:///home/user/ULTRON/edc-notes/EDC_Complete_Notes.html"
anchor=sys.argv[1] if len(sys.argv)>1 else ""
w=int(sys.argv[2]) if len(sys.argv)>2 else 1300
h=int(sys.argv[3]) if len(sys.argv)>3 else 1500
theme=sys.argv[4] if len(sys.argv)>4 else "light"
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome",args=["--no-sandbox"])
    pg=b.new_page(viewport={"width":w,"height":h},color_scheme=theme); pg.goto(url+("#"+anchor if anchor else "")); pg.wait_for_timeout(1200)
    if anchor: pg.evaluate("document.getElementById('%s').scrollIntoView({behavior:'instant'})"%anchor)
    pg.wait_for_timeout(800); pg.screenshot(path="shot.png"); 
    errs=pg.evaluate("[...document.querySelectorAll('.katex-error')].length"); print("katex errors",errs)
    print("MATH ERROR text:", pg.evaluate("document.body.innerText.includes('MATH ERROR')"))
    b.close()
