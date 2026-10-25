# Kindle Dash

Turn an old **Kindle Paperwhite** into a clean e-ink dashboard: big clock, date, today's tasks, rotating quotes and your own wallpaper. You control it from a companion web app on your phone or PC.

```
 phone / PC  ──(admin app)──►  Node server  ◄──(polls every 30s)──  Kindle browser
```

No dependencies and no build step. Just Node 16+.

## Quick start

```bash
cd kindle-dash
KINDLE_PIN=1234 npm start      # PIN is optional but recommended on shared Wi-Fi
```

The server prints two addresses:

| Where | Address |
|---|---|
| Kindle | `http://<your-pc-ip>:8080/` |
| Phone / PC (companion app) | `http://<your-pc-ip>:8080/admin` |

Run the server on anything that stays on: a spare PC, a Raspberry Pi, a NAS. Kindle and server must be on the same Wi-Fi.

## Kindle setup (no jailbreak needed)

1. Settings → Wi-Fi: connect to the same network as the server.
2. Open **Experimental Browser** (Menu → Experimental Browser).
3. Type the Kindle address from above and **bookmark** it. Use plain `http://`, because old Kindles often can't do modern HTTPS.
4. Hide the browser bars for a full-screen look (menu → *Enter full screen*).
5. Keep it **plugged in**. On older firmware you can type `;debugOn` then `~ds` in the search box to disable the screensaver. On newer firmware the screensaver can't be turned off without a jailbreak; just tap to wake and the page catches up by itself.

The page recomputes the time from the device clock on every tick, so it recovers on its own after sleep or Wi-Fi drops.

## The companion app (`/admin`)

- **Today**: add, tick off, reorder and delete tasks (with optional times). The next task is highlighted on the Kindle.
- **Quotes**: add your own; choose rotate, shuffle, one-per-day or off.
- **Look**: Classic, Minimal or Poster layouts, 12/24 h, name greeting, progress bar, live Kindle preview.
- **Wallpaper studio**: pick a generated preset or upload any photo. It is cropped to your Kindle's screen, converted to grayscale and Floyd-Steinberg dithered to the panel's 16 gray levels, right in your browser.

Choose your model under *Live preview*: Paperwhite 1/2 = 758×1024, Paperwhite 3 and later = 1072×1448.

Edits appear on the Kindle within about 30 seconds (it polls a tiny `/api/rev` endpoint and only reloads when something changed).

## E-ink friendly animations

E-ink can't animate smoothly, so motion is done in stepped, low-refresh ways (toggle in *Look*):

- **Flip digits**: changed clock digits briefly invert, then settle.
- **Typewriter quotes**: new quotes appear in four clean steps.
- **Anti-ghost flash**: a black/white flash every N minutes (default 15) clears ghosting.
- The clock only ticks once a minute, aligned to the minute, to spare the panel.

## Configuration

| Env var | Default | Meaning |
|---|---|---|
| `PORT` | `8080` | Server port |
| `KINDLE_PIN` | none | Required (header `x-pin`) for every change. The Kindle only reads, so it never needs it |
| `DATA_DIR` | `./data` | Where `state.json` and `wallpaper.png` live |

## Development

```bash
npm test     # API smoke test
```

The Kindle page (`public/kindle.js`, `kindle.css`) is deliberately **ES5 and old-WebKit CSS only**: no `let`/`const`, arrow functions, `fetch`, grid or CSS variables. Keep it that way. The admin app is free to use modern JS.

## Going further (needs a jailbreak)

With a jailbroken Kindle you can skip the browser and use something like *kindle-dash* or *Online Screensaver* to pull a rendered image on a schedule, which is gentler on battery. The `/` page can be screenshotted headlessly for that.
