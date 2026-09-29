import sys, glob, os
from playwright.sync_api import sync_playwright
names = sys.argv[2:] 
figs = sorted(glob.glob("../figs/"+sys.argv[1])) if not names else [f"../figs/{n}.svg" for n in names]
html = "<body style='margin:0;background:#fff;font-family:sans-serif'><div style='display:flex;flex-wrap:wrap;gap:10px;padding:8px'>"
for f in figs:
    html += f"<div style='border:1px solid #ccc;padding:4px;width:440px'><div style='font-size:11px;color:#555'>{os.path.basename(f)}</div><img src='file://{os.path.abspath(f)}' style='width:100%'></div>"
html += "</div></body>"
open("prev.html","w").write(html)
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome", args=["--no-sandbox","--allow-file-access-from-files"])
    pg = b.new_page(viewport={"width":1400,"height":900}); pg.goto("file://"+os.path.abspath("prev.html")); pg.wait_for_timeout(500)
    pg.screenshot(path="prev.png", full_page=True); b.close()
