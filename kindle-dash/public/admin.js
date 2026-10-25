'use strict';
// Companion app. Modern browsers only (it runs on your phone or PC, not the Kindle).
const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];
let state = null, lastRev = 0, sensors = [];

/* ---------- api ---------- */
const getPin = () => { try { return localStorage.getItem('kd-pin') || ''; } catch { return ''; } };
async function api(method, url, body, raw) {
  for (let attempt = 0; attempt < 2; attempt++) {
    const res = await fetch(url, {
      method, headers: { 'x-pin': getPin(), ...(raw ? {} : { 'content-type': 'application/json' }) },
      body: body === undefined ? undefined : raw ? body : JSON.stringify(body)
    });
    if (res.status === 401) {
      const pin = prompt('Enter the admin PIN');
      if (pin === null) throw new Error('PIN required');
      try { localStorage.setItem('kd-pin', pin); } catch {}
      continue;
    }
    if (!res.ok) throw new Error((await res.json().catch(() => ({}))).error || res.statusText);
    return res.json();
  }
  throw new Error('Wrong PIN');
}
async function act(...args) {
  try { setState(await api(...args)); } catch (e) { toast(e.message); }
}
function toast(msg) {
  const t = $('#toast'); t.textContent = msg; t.classList.add('on');
  clearTimeout(toast.t); toast.t = setTimeout(() => t.classList.remove('on'), 2200);
}
function setSync(ok, text) { const s = $('#sync'); s.className = 'sync ' + (ok ? 'ok' : 'bad'); $('span', s).textContent = text; }

/* ---------- render ---------- */
const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

function setState(s) {
  state = s; lastRev = s.rev; render(); setSync(true, 'synced');
}
function render() {
  const open = state.tasks.filter(t => !t.done).length;
  const d = new Date();
  $('#todayTitle').textContent = d.toLocaleDateString(undefined, { weekday: 'long' });
  $('#todaySub').textContent = `${d.toLocaleDateString(undefined, { day: 'numeric', month: 'long' })} · ${open} open, ${state.tasks.length - open} done`;

  $('#taskList').innerHTML = state.tasks.length ? state.tasks.map((t, i) => `
    <li class="item ${t.done ? 'done' : ''}" data-id="${t.id}">
      <button class="chk" data-a="toggle" aria-label="Toggle"></button>
      <div class="body"><b>${t.time ? `<span class="tag">${esc(t.time)}</span>` : ''}${esc(t.text)}</b></div>
      <button class="mini" data-a="up" ${i === 0 ? 'disabled' : ''} aria-label="Move up">↑</button>
      <button class="mini" data-a="down" ${i === state.tasks.length - 1 ? 'disabled' : ''} aria-label="Move down">↓</button>
      <button class="mini" data-a="del" aria-label="Delete">✕</button>
    </li>`).join('') : '<li class="empty">Nothing planned yet. Add your first task above.</li>';

  $('#quoteList').innerHTML = state.quotes.length ? state.quotes.map(q => `
    <li class="item" data-id="${q.id}"><div class="body"><b style="font-weight:500">“${esc(q.text)}”</b>${q.author ? `<small>— ${esc(q.author)}</small>` : ''}</div>
    <button class="mini" data-a="delq" aria-label="Delete">✕</button></li>`).join('') : '<li class="empty">No quotes. Add one above.</li>';

  const s = state.settings;
  $$('.seg[data-set]').forEach(seg => {
    const v = String(s[seg.dataset.set]);
    $$('button', seg).forEach(b => b.classList.toggle('on', b.dataset.v === v));
  });
  $$('[data-check]').forEach(c => c.checked = !!s[c.dataset.check]);
  const setVal = (el, v) => { if (document.activeElement !== el) el.value = v; };
  setVal($('#setName'), s.name); setVal($('#setMaxTasks'), s.maxTasks); setVal($('#setFlash'), s.flashMinutes);
  setVal($('#setQuoteMinutes'), s.quoteMinutes); setVal($('#setQuoteMode'), s.quoteMode);
  setVal($('#setMaxMetrics'), s.maxMetrics);
  $('#cityNow').textContent = s.lat === null ? 'No location set: the forecast stays hidden until you pick one.' : `Forecast for ${s.city || 'your location'} (${s.lat.toFixed(2)}, ${s.lon.toFixed(2)})`;
  renderSensors();
  fitPreview();
}

function renderSensors() {
  const dark = matchMedia('(prefers-color-scheme: dark)').matches ? 'w' : 'k';
  $('#sensorList').innerHTML = sensors.length ? sensors.map(m => `
    <li class="item" data-id="${esc(m.id)}"><img class="spark" alt="" src="/api/spark/${encodeURIComponent(m.id)}.svg?w=168&h=56&c=${dark}&v=${m.t}">
    <div class="body"><b>${esc(m.label)}</b><small>${esc(m.id)} · ${new Date(m.t).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</small></div>
    <span class="val">${Math.round(m.value * 10) / 10} ${esc(m.unit)}</span>
    <button class="mini" data-a="dels" aria-label="Delete">✕</button></li>`).join('') : '<li class="empty">No sensors yet. Add a reading above or try the demo sensors below.</li>';
  const pin = getPin() ? ` -H 'x-pin: ${getPin()}'` : '';
  $('#curl').textContent = `curl -X POST ${location.origin}/api/metrics${pin} \\\n  -H 'content-type: application/json' \\\n  -d '{"id":"co2","label":"CO2","value":812,"unit":"ppm"}'`;
}

function fitPreview() {
  const [w, h] = state.settings.device.split('x').map(Number);
  const box = $('#previewBox'), f = $('#preview');
  const scale = Math.min(box.clientWidth || 300, 360) / w;
  box.style.width = Math.round(w * scale) + 'px'; box.style.height = Math.round(h * scale) + 'px';
  f.style.width = w + 'px'; f.style.height = h + 'px'; f.style.transform = `scale(${scale})`;
}
addEventListener('resize', () => state && fitPreview());

/* ---------- events ---------- */
$('#sensorForm').onsubmit = async e => {
  e.preventDefault();
  const label = $('#sLabel').value.trim(), value = $('#sValue').value;
  if (!label || value === '') return toast('Name and value needed');
  try { await api('POST', '/api/metrics', { id: label, label, value: Number(value), unit: $('#sUnit').value }); await refresh(true); toast('Saved'); } catch (err) { toast(err.message); }
  $('#sValue').value = '';
};
$('#sensorList').onclick = async e => {
  const b = e.target.closest('[data-a=dels]'); if (!b) return;
  try { await api('DELETE', '/api/metrics/' + b.closest('.item').dataset.id); await refresh(true); } catch (err) { toast(err.message); }
};
$('#demoSensors').onclick = async () => { try { await api('POST', '/api/metrics/demo', {}); await refresh(true); toast('Demo sensors added'); } catch (err) { toast(err.message); } };
$('#copyCurl').onclick = () => { navigator.clipboard?.writeText($('#curl').textContent).then(() => toast('Copied'), () => toast('Select and copy manually')); };

async function findCity() {
  const q = $('#cityQ').value.trim(); if (!q) return;
  const box = $('#cityResults'); box.innerHTML = '<li class="empty">Searching…</li>';
  try {
    const { results } = await (await fetch('/api/geocode?q=' + encodeURIComponent(q))).json();
    box.innerHTML = results?.length ? results.map((r, i) => `<li class="item pick" data-i="${i}"><div class="body"><b>${esc(r.name)}</b><small>${esc([r.region, r.country].filter(Boolean).join(', '))}</small></div></li>`).join('') : '<li class="empty">No match</li>';
    box.onclick = e => {
      const li = e.target.closest('.pick'); if (!li) return;
      const r = results[li.dataset.i]; box.innerHTML = '';
      saveSetting({ city: r.name, lat: r.lat, lon: r.lon }).then(() => toast('Location set'));
    };
  } catch { box.innerHTML = '<li class="empty">Search unavailable right now</li>'; }
}
$('#cityGo').onclick = findCity;
$('#cityQ').onkeydown = e => { if (e.key === 'Enter') { e.preventDefault(); findCity(); } };

$$('nav button').forEach(b => b.onclick = () => {
  $$('nav button').forEach(x => x.classList.toggle('on', x === b));
  $$('.tab').forEach(t => t.classList.toggle('on', t.id === 'tab-' + b.dataset.tab));
  if (b.dataset.tab === 'look') fitPreview();
});

$('#taskForm').onsubmit = async e => {
  e.preventDefault();
  const text = $('#taskText').value.trim(); if (!text) return;
  await act('POST', '/api/tasks', { text, time: $('#taskTime').value });
  $('#taskText').value = ''; $('#taskTime').value = ''; $('#taskText').focus();
};
$('#taskList').onclick = e => {
  const btn = e.target.closest('button[data-a]'); if (!btn) return;
  const id = btn.closest('.item').dataset.id, t = state.tasks.find(x => x.id === id);
  ({
    toggle: () => act('PATCH', '/api/tasks/' + id, { done: !t.done }),
    up: () => act('POST', '/api/tasks/move', { id, dir: 'up' }),
    down: () => act('POST', '/api/tasks/move', { id, dir: 'down' }),
    del: () => act('DELETE', '/api/tasks/' + id)
  })[btn.dataset.a]();
};
$('#clearDone').onclick = () => act('POST', '/api/tasks/clear-done');

$('#quoteForm').onsubmit = async e => {
  e.preventDefault();
  const text = $('#quoteText').value.trim(); if (!text) return;
  await act('POST', '/api/quotes', { text, author: $('#quoteAuthor').value });
  $('#quoteText').value = ''; $('#quoteAuthor').value = '';
};
$('#quoteList').onclick = e => {
  const btn = e.target.closest('[data-a=delq]'); if (btn) act('DELETE', '/api/quotes/' + btn.closest('.item').dataset.id);
};

const saveSetting = patch => act('PUT', '/api/settings', patch);
$$('.seg[data-set]').forEach(seg => seg.onclick = e => {
  const b = e.target.closest('button'); if (!b) return;
  const k = seg.dataset.set;
  saveSetting({ [k]: seg.hasAttribute('data-bool') ? b.dataset.v === 'true' : b.dataset.v });
});
$$('[data-check]').forEach(c => c.onchange = () => saveSetting({ [c.dataset.check]: c.checked }));
const debounced = (el, key, conv = v => v) => el.oninput = () => {
  clearTimeout(el.t); el.t = setTimeout(() => saveSetting({ [key]: conv(el.value) }), 500);
};
debounced($('#setName'), 'name'); debounced($('#setMaxMetrics'), 'maxMetrics', Number); debounced($('#setMaxTasks'), 'maxTasks', Number);
debounced($('#setFlash'), 'flashMinutes', Number); debounced($('#setQuoteMinutes'), 'quoteMinutes', Number);
$('#setQuoteMode').onchange = e => saveSetting({ quoteMode: e.target.value });

/* ---------- wallpaper studio ---------- */
const PRESETS = {
  Dunes: (x, y, w, h) => {
    const u = x / w, v = y / h;
    const band = .5 + .5 * Math.sin(v * 30 + Math.sin(u * 6 + v * 4) * 1.6 + Math.sin(v * 3) * 2);
    return .25 + .6 * (v * .6 + band * .4);
  },
  Ripples: (x, y, w, h) => {
    const a = Math.hypot(x - w * .3, y - h * .35), b = Math.hypot(x - w * .75, y - h * .7);
    return .5 + .25 * Math.sin(a / (w / 38)) + .25 * Math.sin(b / (w / 38));
  },
  Horizon: (x, y, w, h) => {
    const u = x / w, v = y / h, hor = .62;
    if (Math.hypot(x - w * .5, y - h * .45) < w * .22) return .98;
    if (v < hor) return .18 + .55 * Math.pow(v / hor, 1.4);
    const k = (v - hor) / (1 - hor), stripe = Math.sin(k * k * 90) > 0 ? 1 : 0;
    return .08 + .25 * (1 - k) + .12 * stripe * (1 - k);
  },
  Dots: (x, y, w, h) => {
    const cell = w / 26, cx = (Math.floor(x / cell) + .5) * cell, cy = (Math.floor(y / cell) + .5) * cell;
    const g = 1 - (cy / h) * .85, r = cell * .5 * (.2 + g * .85);
    return Math.hypot(x - cx, y - cy) < r ? .05 : .96;
  }
};
const cv = $('#canvas'), ctx = cv.getContext('2d', { willReadFrequently: true });
let source = null; // {type:'preset', fn} | {type:'image', img}

function targetSize() { return state.settings.device.split('x').map(Number); }

function buildPresets() {
  $('#presets').innerHTML = '';
  Object.keys(PRESETS).forEach(name => {
    const b = document.createElement('button');
    const c = document.createElement('canvas'); c.width = 96; c.height = 128;
    const cx = c.getContext('2d'), im = cx.createImageData(96, 128);
    for (let y = 0; y < 128; y++) for (let x = 0; x < 96; x++) {
      const v = Math.max(0, Math.min(1, PRESETS[name](x, y, 96, 128))) * 255, i = (y * 96 + x) * 4;
      im.data[i] = im.data[i + 1] = im.data[i + 2] = v; im.data[i + 3] = 255;
    }
    cx.putImageData(im, 0, 0);
    b.append(c); const sp = document.createElement('span'); sp.textContent = name; b.append(sp);
    b.onclick = () => { source = { type: 'preset', fn: PRESETS[name] }; processWall(); };
    $('#presets').append(b);
  });
}

function processWall() {
  if (!source) return;
  const [w, h] = targetSize();
  cv.width = w; cv.height = h;
  const gray = new Float32Array(w * h);
  if (source.type === 'preset') {
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) gray[y * w + x] = source.fn(x, y, w, h) * 255;
  } else { // cover-crop the photo to the screen ratio
    const im = source.img, s = Math.max(w / im.width, h / im.height);
    const dw = im.width * s, dh = im.height * s;
    ctx.fillStyle = '#fff'; ctx.fillRect(0, 0, w, h);
    ctx.drawImage(im, (w - dw) / 2, (h - dh) / 2, dw, dh);
    const d = ctx.getImageData(0, 0, w, h).data;
    for (let i = 0; i < w * h; i++) gray[i] = .299 * d[i * 4] + .587 * d[i * 4 + 1] + .114 * d[i * 4 + 2];
  }
  const br = +$('#wBright').value, ct = +$('#wContrast').value, inv = $('#wInvert').checked, dither = $('#wDither').checked;
  const cf = (259 * (ct + 255)) / (255 * (259 - ct));
  for (let i = 0; i < gray.length; i++) {
    let v = cf * (gray[i] + br - 128) + 128;
    v = Math.max(0, Math.min(255, v)); gray[i] = inv ? 255 - v : v;
  }
  const STEP = 17; // 16 gray levels: what the Paperwhite panel can show
  if (dither) { // Floyd–Steinberg
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
      const i = y * w + x, old = gray[i], nw = Math.max(0, Math.min(255, Math.round(old / STEP) * STEP)), err = old - nw;
      gray[i] = nw;
      if (x + 1 < w) gray[i + 1] += err * 7 / 16;
      if (y + 1 < h) {
        if (x > 0) gray[i + w - 1] += err * 3 / 16;
        gray[i + w] += err * 5 / 16;
        if (x + 1 < w) gray[i + w + 1] += err / 16;
      }
    }
  } else for (let i = 0; i < gray.length; i++) gray[i] = Math.round(gray[i] / STEP) * STEP;
  const out = ctx.createImageData(w, h);
  for (let i = 0; i < gray.length; i++) { const v = Math.max(0, Math.min(255, gray[i])); out.data.set([v, v, v, 255], i * 4); }
  ctx.putImageData(out, 0, 0);
  $('#studio').hidden = false;
}

$('#file').onchange = e => {
  const f = e.target.files[0]; if (!f) return;
  const img = new Image();
  img.onload = () => { source = { type: 'image', img }; processWall(); URL.revokeObjectURL(img.src); };
  img.onerror = () => toast('Could not read that image');
  img.src = URL.createObjectURL(f);
};
['#wBright', '#wContrast', '#wDither', '#wInvert'].forEach(s => $(s).oninput = () => processWall());
$('#applyWall').onclick = () => cv.toBlob(async blob => {
  toast('Sending…');
  await act('PUT', '/api/wallpaper', blob, true);
  toast('Wallpaper sent to Kindle');
}, 'image/png');
$('#removeWall').onclick = () => act('DELETE', '/api/wallpaper');

/* ---------- boot / sync ---------- */
async function refresh(force) {
  try {
    const { rev } = await (await fetch('/api/rev')).json();
    sensors = (await (await fetch('/api/metrics')).json()).metrics;
    if (force || rev !== lastRev) setState(await (await fetch('/api/state')).json());
    else { setSync(true, 'synced'); renderSensors(); }
  } catch { setSync(false, 'offline'); }
}
refresh(true).then(buildPresets);
setInterval(() => document.hidden || refresh(), 5000);
