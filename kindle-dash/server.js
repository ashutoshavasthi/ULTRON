'use strict';
// Kindle Dash server. Zero dependencies: Node built-ins only.
// Serves the e-ink display (/) and the companion app (/admin).
var http = require('http');
var fs = require('fs');
var path = require('path');
var os = require('os');
var crypto = require('crypto');

var PORT = parseInt(process.env.PORT, 10) || 8080;
var PIN = process.env.KINDLE_PIN || '';
var DATA_DIR = process.env.DATA_DIR || path.join(__dirname, 'data');
var STATE_FILE = path.join(DATA_DIR, 'state.json');
var WALL_FILE = path.join(DATA_DIR, 'wallpaper.png');
var PUBLIC = path.join(__dirname, 'public');
var MAX_UPLOAD = 6 * 1024 * 1024;

var DEFAULTS = {
  rev: 1,
  tasks: [
    { id: 't1', text: 'Plan the day', time: '09:00', done: false },
    { id: 't2', text: 'Deep work block', time: '10:00', done: false },
    { id: 't3', text: 'Walk outside', time: '18:00', done: false }
  ],
  quotes: [
    { id: 'q1', text: 'What you do every day matters more than what you do once in a while.', author: '' },
    { id: 'q2', text: 'Simplicity is the ultimate sophistication.', author: 'Leonardo da Vinci' },
    { id: 'q3', text: 'The best way out is always through.', author: 'Robert Frost' },
    { id: 'q4', text: 'We are what we repeatedly do.', author: 'Will Durant' }
  ],
  wallpaper: null,
  settings: {
    name: '',
    layout: 'hub',          // hub | classic | minimal | poster
    theme: 'dark',          // dark | light
    units: 'c',             // c | f
    city: '', lat: null, lon: null,
    showWeather: true,
    maxMetrics: 2,
    wallpaperMode: 'panel', // panel | full | off
    clock24: true,
    animations: true,
    flashMinutes: 15,       // full-screen ghost-clearing flash; 0 = off
    quoteMode: 'rotate',    // rotate | daily | random | off
    quoteMinutes: 10,
    showTasks: true,
    showProgress: true,
    maxTasks: 6,
    device: '758x1024'
  }
};

var SETTING_RULES = {
  name: 'string', layout: ['hub', 'classic', 'minimal', 'poster'],
  theme: ['dark', 'light'], units: ['c', 'f'], city: 'string', lat: 'float', lon: 'float', showWeather: 'bool',
  maxMetrics: 'int',
  wallpaperMode: ['panel', 'full', 'off'], clock24: 'bool',
  animations: 'bool', flashMinutes: 'int', quoteMode: ['rotate', 'daily', 'random', 'off'],
  quoteMinutes: 'int', showTasks: 'bool', showProgress: 'bool', maxTasks: 'int',
  device: ['758x1024', '1072x1448']
};

var state = load();

function clone(o) { return JSON.parse(JSON.stringify(o)); }

function load() {
  try {
    var s = JSON.parse(fs.readFileSync(STATE_FILE, 'utf8'));
    var d = clone(DEFAULTS);
    s.settings = Object.assign(d.settings, s.settings || {});
    return Object.assign(d, s);
  } catch (e) {
    return clone(DEFAULTS);
  }
}

function save() {
  state.rev++;
  fs.mkdirSync(DATA_DIR, { recursive: true });
  var tmp = STATE_FILE + '.tmp';
  fs.writeFileSync(tmp, JSON.stringify(state, null, 2));
  fs.renameSync(tmp, STATE_FILE);
}

function uid() { return crypto.randomBytes(4).toString('hex'); }

function send(res, code, body, type) {
  var buf = Buffer.isBuffer(body) ? body : Buffer.from(typeof body === 'string' ? body : JSON.stringify(body));
  res.writeHead(code, {
    'Content-Type': type || 'application/json; charset=utf-8',
    'Content-Length': buf.length,
    'Cache-Control': 'no-store'
  });
  res.end(buf);
}

function readBody(req, cb) {
  var chunks = [], size = 0, dead = false;
  req.on('data', function (c) {
    size += c.length;
    if (size > MAX_UPLOAD) { dead = true; req.destroy(); return; }
    chunks.push(c);
  });
  req.on('end', function () { if (!dead) cb(Buffer.concat(chunks)); });
}

function readJson(req, res, cb) {
  readBody(req, function (buf) {
    var j;
    try { j = buf.length ? JSON.parse(buf.toString('utf8')) : {}; }
    catch (e) { return send(res, 400, { error: 'bad json' }); }
    cb(j);
  });
}

function clean(s, max) { return String(s == null ? '' : s).replace(/\s+/g, ' ').trim().slice(0, max); }

function cleanTime(t) {
  t = clean(t, 5);
  return /^([01]?\d|2[0-3]):[0-5]\d$/.test(t) ? (t.length === 4 ? '0' + t : t) : '';
}

function applySettings(inp) {
  Object.keys(SETTING_RULES).forEach(function (k) {
    if (!(k in inp)) return;
    var rule = SETTING_RULES[k], v = inp[k];
    if (rule === 'string') state.settings[k] = clean(v, 60);
    else if (rule === 'float') {
      v = (v === null || v === '') ? NaN : parseFloat(v);
      state.settings[k] = isFinite(v) ? Math.max(-180, Math.min(180, v)) : null;
    }
    else if (rule === 'bool') state.settings[k] = !!v;
    else if (rule === 'int') {
      v = parseInt(v, 10);
      if (!isNaN(v)) state.settings[k] = Math.max(0, Math.min(v, 1440));
    } else if (rule.indexOf(v) !== -1) state.settings[k] = v;
  });
  state.settings.quoteMinutes = Math.max(1, state.settings.quoteMinutes);
  state.settings.maxTasks = Math.max(1, Math.min(state.settings.maxTasks, 12));
  state.settings.maxMetrics = Math.min(state.settings.maxMetrics, 6);
}

function authed(req) {
  if (!PIN) return true;
  var a = Buffer.from(String(req.headers['x-pin'] || ''));
  var b = Buffer.from(PIN);
  return a.length === b.length && crypto.timingSafeEqual(a, b);
}


/* ---------- sensors (metrics) ---------- */
var METRICS_FILE = path.join(DATA_DIR, 'metrics.json');
var metrics = (function () {
  try { return JSON.parse(fs.readFileSync(METRICS_FILE, 'utf8')); } catch (e) { return []; }
})();
var metricsTimer = null;

function saveMetricsSoon() {
  if (metricsTimer) return;
  metricsTimer = setTimeout(flushMetrics, 30000);
  if (metricsTimer.unref) metricsTimer.unref();
}
function flushMetrics() {
  metricsTimer = null;
  try {
    fs.mkdirSync(DATA_DIR, { recursive: true });
    fs.writeFileSync(METRICS_FILE, JSON.stringify(metrics));
  } catch (e) { /* keep running; data is in memory */ }
}

function pushMetric(j, at) {
  var id = clean(j.id, 32).toLowerCase().replace(/[^a-z0-9_-]+/g, '-').replace(/^-+|-+$/g, '');
  var v = Number(j.value);
  if (!id || j.value === '' || j.value === null || !isFinite(v)) return null;
  var m = metrics.filter(function (x) { return x.id === id; })[0];
  if (!m) {
    if (metrics.length >= 24) return null;
    m = { id: id, label: id, unit: '', value: v, t: 0, points: [] };
    metrics.push(m);
  }
  if ('label' in j && clean(j.label, 24)) m.label = clean(j.label, 24);
  if ('unit' in j) m.unit = clean(j.unit, 8);
  var now = at || Date.now(), last = m.points[m.points.length - 1];
  // One point per 5 minutes keeps ~24h of history small.
  if (last && now - last[0] < 5 * 60000) m.points[m.points.length - 1] = [now, v];
  else m.points.push([now, v]);
  if (m.points.length > 288) m.points.shift();
  m.value = v; m.t = now;
  saveMetricsSoon();
  return m;
}

function seedDemo() {
  var now = Date.now(), i;
  var defs = [
    { id: 'inside', label: 'Inside', unit: '°C', base: 21.5, amp: 1.2 },
    { id: 'outside', label: 'Outside', unit: '°C', base: 8, amp: 4 },
    { id: 'humidity', label: 'Humidity', unit: '%', base: 46, amp: 6 },
    { id: 'co2', label: 'CO2', unit: 'ppm', base: 900, amp: 380 }
  ];
  metrics = metrics.filter(function (m) { return !defs.some(function (d) { return d.id === m.id; }); });
  defs.forEach(function (d, k) {
    for (i = 48; i >= 0; i--) {
      var t = now - i * 30 * 60000;
      pushMetric({ id: d.id, label: d.label, unit: d.unit,
        value: d.base + d.amp * Math.sin((48 - i) / 7 + k) + d.amp * 0.3 * Math.sin((48 - i) / 2.3 + k * 2) }, t);
    }
  });
}

function summary(m) { return { id: m.id, label: m.label, unit: m.unit, value: m.value, t: m.t }; }

/* ---------- svg: weather icons and sparklines (served as images; old WebKit renders <img src=svg>) ---------- */
var CLOUD = 'M20 46h26a10 10 0 0 0 1.5-19.9A15 15 0 0 0 18.5 29 8.5 8.5 0 0 0 20 46z';
function sunRays(cx, cy, r1, r2) {
  var out = '', a, i;
  for (i = 0; i < 8; i++) {
    a = i * Math.PI / 4;
    out += 'M' + (cx + Math.cos(a) * r1).toFixed(1) + ' ' + (cy + Math.sin(a) * r1).toFixed(1) +
      'L' + (cx + Math.cos(a) * r2).toFixed(1) + ' ' + (cy + Math.sin(a) * r2).toFixed(1);
  }
  return out;
}
function iconSvg(name, dark) {
  var fg = dark ? '#fff' : '#000', bg = dark ? '#000' : '#fff';
  var g = '', cloud = '<path d="' + CLOUD + '" fill="' + bg + '"/>';
  if (name === 'sun') g = '<circle cx="32" cy="32" r="10"/><path d="' + sunRays(32, 32, 16, 24) + '"/>';
  else if (name === 'partly') g = '<circle cx="24" cy="24" r="7"/><path d="' + sunRays(24, 24, 11, 16) + '"/><g transform="translate(8 8) scale(.8)">' + cloud + '</g>';
  else if (name === 'cloud') g = cloud;
  else if (name === 'rain') g = cloud + '<path d="M24 52l-3 7M34 52l-3 7M44 52l-3 7"/>';
  else if (name === 'snow') g = cloud + '<g fill="' + fg + '" stroke="none"><circle cx="24" cy="54" r="2.2"/><circle cx="34" cy="58" r="2.2"/><circle cx="44" cy="54" r="2.2"/></g>';
  else if (name === 'storm') g = cloud + '<path d="M35 42l-7 11h8l-6 10"/>';
  else g = '<path d="M14 24h36M10 34h40M16 44h36M12 54h30"/>'; // fog
  return '<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 64 64"><g fill="none" stroke="' + fg +
    '" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round">' + g + '</g></svg>';
}
function sparkSvg(m, dark, w, h) {
  var fg = dark ? '#fff' : '#000', cutoff = Date.now() - 24 * 3600 * 1000;
  var pts = m.points.filter(function (p) { return p[0] >= cutoff; });
  if (pts.length < 2) pts = m.points.slice(-2);
  var step = Math.max(1, Math.ceil(pts.length / 60)), use = [], i;
  for (i = 0; i < pts.length; i += step) use.push(pts[i]);
  if (use[use.length - 1] !== pts[pts.length - 1]) use.push(pts[pts.length - 1]);
  var lo = Infinity, hi = -Infinity;
  use.forEach(function (p) { lo = Math.min(lo, p[1]); hi = Math.max(hi, p[1]); });
  var padx = 6, pady = 7, span = hi - lo || 1, t0 = use[0][0], tspan = (use[use.length - 1][0] - t0) || 1;
  var coords = use.map(function (p) {
    return [padx + (use.length > 1 ? (p[0] - t0) / tspan : 0.5) * (w - 2 * padx),
      hi === lo ? h / 2 : pady + (1 - (p[1] - lo) / span) * (h - 2 * pady)];
  });
  var last = coords[coords.length - 1];
  return '<svg xmlns="http://www.w3.org/2000/svg" width="' + w + '" height="' + h + '" viewBox="0 0 ' + w + ' ' + h + '">' +
    '<polyline fill="none" stroke="' + fg + '" stroke-width="3" stroke-linejoin="round" stroke-linecap="round" points="' +
    coords.map(function (c) { return c[0].toFixed(1) + ',' + c[1].toFixed(1); }).join(' ') + '"/>' +
    '<circle cx="' + last[0].toFixed(1) + '" cy="' + last[1].toFixed(1) + '" r="4.5" fill="' + fg + '"/></svg>';
}

/* ---------- weather (Open-Meteo: free, no API key) ---------- */
var METEO = process.env.OPEN_METEO_URL || 'https://api.open-meteo.com';
var GEO = process.env.OPEN_METEO_GEO_URL || 'https://geocoding-api.open-meteo.com';
var weatherCache = { key: '', t: 0, data: null };

function iconFor(code) {
  if (code === 0) return 'sun';
  if (code <= 2) return 'partly';
  if (code === 3) return 'cloud';
  if (code === 45 || code === 48) return 'fog';
  if (code >= 71 && code <= 77 || code === 85 || code === 86) return 'snow';
  if (code >= 95) return 'storm';
  return 'rain';
}
async function fetchJson(url) {
  var ctl = new AbortController(), timer = setTimeout(function () { ctl.abort(); }, 8000);
  try {
    var r = await fetch(url, { signal: ctl.signal });
    var j = await r.json();
    if (!r.ok || j.error) throw new Error(j.reason || 'http ' + r.status);
    return j;
  } finally { clearTimeout(timer); }
}
async function getWeather() {
  var s = state.settings;
  if (!s.showWeather || s.lat === null || s.lon === null) return null;
  var key = [s.lat, s.lon, s.units].join(',');
  if (weatherCache.key === key && Date.now() - weatherCache.t < 20 * 60000) return weatherCache.data;
  try {
    var j = await fetchJson(METEO + '/v1/forecast?latitude=' + s.lat + '&longitude=' + s.lon +
      '&daily=weather_code,temperature_2m_max,temperature_2m_min&current=temperature_2m,weather_code' +
      '&timezone=auto&forecast_days=5&temperature_unit=' + (s.units === 'f' ? 'fahrenheit' : 'celsius'));
    var r1 = function (v) { return Math.round(v * 10) / 10; };
    var data = {
      city: s.city, unit: s.units === 'f' ? '°F' : '°C',
      now: { temp: r1(j.current.temperature_2m), icon: iconFor(j.current.weather_code) },
      days: j.daily.time.map(function (d, i) {
        return { date: d, icon: iconFor(j.daily.weather_code[i]), hi: r1(j.daily.temperature_2m_max[i]), lo: r1(j.daily.temperature_2m_min[i]) };
      })
    };
    weatherCache = { key: key, t: Date.now(), data: data };
    return data;
  } catch (e) {
    // Keep showing the last good forecast if the service hiccups (or rate-limits us).
    if (weatherCache.key === key && weatherCache.data) { weatherCache.t = Date.now() - 15 * 60000; return weatherCache.data; }
    return null;
  }
}

function svgSend(res, svg) { send(res, 200, svg, 'image/svg+xml'); }

function publicApi(req, res, url) {
  var p = url.pathname, mm;
  if (p === '/api/live') {
    getWeather().then(function (w) {
      send(res, 200, { now: Date.now(), weather: w, metrics: metrics.map(summary) });
    });
    return true;
  }
  if (p === '/api/geocode') {
    var q = clean(url.searchParams.get('q'), 60);
    if (!q) { send(res, 200, { results: [] }); return true; }
    fetchJson(GEO + '/v1/search?count=5&language=en&name=' + encodeURIComponent(q)).then(function (j) {
      send(res, 200, { results: (j.results || []).map(function (r) {
        return { name: r.name, region: r.admin1 || '', country: r.country || '', lat: r.latitude, lon: r.longitude };
      }) });
    }).catch(function () { send(res, 502, { error: 'location search unavailable' }); });
    return true;
  }
  if (p === '/api/metrics') { send(res, 200, { metrics: metrics.map(summary) }); return true; }
  if ((mm = p.match(/^\/api\/icon\/(\w+)\.svg$/))) {
    svgSend(res, iconSvg(mm[1], url.searchParams.get('c') === 'w')); return true;
  }
  if ((mm = p.match(/^\/api\/spark\/([\w-]+)\.svg$/))) {
    var m = metrics.filter(function (x) { return x.id === mm[1]; })[0];
    if (!m || !m.points.length) { send(res, 404, { error: 'no such metric' }); return true; }
    var w = Math.max(60, Math.min(parseInt(url.searchParams.get('w'), 10) || 320, 800));
    var h = Math.max(24, Math.min(parseInt(url.searchParams.get('h'), 10) || 64, 300));
    svgSend(res, sparkSvg(m, url.searchParams.get('c') === 'w', w, h)); return true;
  }
  return false;
}

function metricsWrite(req, res, url) {
  var p = url.pathname, m = req.method, mm;
  if (m === 'POST' && p === '/api/metrics') { readJson(req, res, function (j) {
    var r = pushMetric(j);
    if (!r) return send(res, 400, { error: 'need id and numeric value (max 24 sensors)' });
    send(res, 200, summary(r));
  }); return true; }
  if (m === 'POST' && p === '/api/metrics/demo') { seedDemo(); flushMetrics(); send(res, 200, { metrics: metrics.map(summary) }); return true; }
  if (m === 'DELETE' && (mm = p.match(/^\/api\/metrics\/([\w-]+)$/))) {
    metrics = metrics.filter(function (x) { return x.id !== mm[1]; });
    flushMetrics(); send(res, 200, { metrics: metrics.map(summary) }); return true;
  }
  return false;
}

function api(req, res, url) {
  var m = req.method, p = url.pathname, mm;

  if (m === 'GET' && p === '/api/rev') return send(res, 200, { rev: state.rev });
  if (m === 'GET' && p === '/api/state') return send(res, 200, state);
  if (m === 'GET' && publicApi(req, res, url)) return;
  if (m === 'GET' && p === '/api/auth') return send(res, 200, { pinRequired: !!PIN, ok: authed(req) });

  if (m === 'GET') return send(res, 404, { error: 'not found' });
  if (!authed(req)) return send(res, 401, { error: 'pin required' });

  if (metricsWrite(req, res, url)) return;

  if (m === 'POST' && p === '/api/tasks') return readJson(req, res, function (j) {
    var text = clean(j.text, 120);
    if (!text) return send(res, 400, { error: 'text required' });
    state.tasks.push({ id: uid(), text: text, time: cleanTime(j.time), done: false });
    save(); send(res, 200, state);
  });
  if (m === 'POST' && p === '/api/tasks/clear-done') {
    state.tasks = state.tasks.filter(function (t) { return !t.done; });
    save(); return send(res, 200, state);
  }
  if (m === 'POST' && p === '/api/tasks/move') return readJson(req, res, function (j) {
    var i = state.tasks.findIndex(function (t) { return t.id === j.id; });
    var n = i + (j.dir === 'up' ? -1 : 1);
    if (i < 0 || n < 0 || n >= state.tasks.length) return send(res, 200, state);
    var t = state.tasks.splice(i, 1)[0];
    state.tasks.splice(n, 0, t);
    save(); send(res, 200, state);
  });
  if ((mm = p.match(/^\/api\/tasks\/(\w+)$/))) {
    var task = state.tasks.filter(function (t) { return t.id === mm[1]; })[0];
    if (!task) return send(res, 404, { error: 'no such task' });
    if (m === 'DELETE') {
      state.tasks = state.tasks.filter(function (t) { return t !== task; });
      save(); return send(res, 200, state);
    }
    if (m === 'PATCH') return readJson(req, res, function (j) {
      if ('text' in j) { var tx = clean(j.text, 120); if (tx) task.text = tx; }
      if ('time' in j) task.time = cleanTime(j.time);
      if ('done' in j) task.done = !!j.done;
      save(); send(res, 200, state);
    });
  }

  if (m === 'POST' && p === '/api/quotes') return readJson(req, res, function (j) {
    var text = clean(j.text, 220);
    if (!text) return send(res, 400, { error: 'text required' });
    state.quotes.push({ id: uid(), text: text, author: clean(j.author, 60) });
    save(); send(res, 200, state);
  });
  if (m === 'DELETE' && (mm = p.match(/^\/api\/quotes\/(\w+)$/))) {
    state.quotes = state.quotes.filter(function (q) { return q.id !== mm[1]; });
    save(); return send(res, 200, state);
  }

  if (m === 'PUT' && p === '/api/settings') return readJson(req, res, function (j) {
    applySettings(j); save(); send(res, 200, state);
  });

  if (m === 'PUT' && p === '/api/wallpaper') return readBody(req, function (buf) {
    if (buf.length < 8 || buf.toString('latin1', 1, 4) !== 'PNG') return send(res, 400, { error: 'PNG required' });
    fs.mkdirSync(DATA_DIR, { recursive: true });
    fs.writeFileSync(WALL_FILE, buf);
    state.wallpaper = Date.now();
    save(); send(res, 200, state);
  });
  if (m === 'DELETE' && p === '/api/wallpaper') {
    try { fs.unlinkSync(WALL_FILE); } catch (e) { /* already gone */ }
    state.wallpaper = null;
    save(); return send(res, 200, state);
  }

  send(res, 404, { error: 'not found' });
}

var TYPES = {
  '.html': 'text/html; charset=utf-8', '.js': 'application/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8', '.png': 'image/png', '.svg': 'image/svg+xml',
  '.json': 'application/json', '.ico': 'image/x-icon'
};

function serveFile(res, file) {
  fs.readFile(file, function (err, buf) {
    if (err) return send(res, 404, 'not found', 'text/plain');
    send(res, 200, buf, TYPES[path.extname(file)] || 'application/octet-stream');
  });
}

var server = http.createServer(function (req, res) {
  var url = new URL(req.url, 'http://x');
  var p = url.pathname;
  try {
    if (p.indexOf('/api/') === 0) return api(req, res, url);
    if (p === '/') return serveFile(res, path.join(PUBLIC, 'kindle.html'));
    if (p === '/admin' || p === '/admin/') return serveFile(res, path.join(PUBLIC, 'admin.html'));
    if (p === '/wallpaper.png') return serveFile(res, WALL_FILE);
    var file = path.normalize(path.join(PUBLIC, p));
    if (file.indexOf(PUBLIC + path.sep) !== 0) return send(res, 403, 'forbidden', 'text/plain');
    return serveFile(res, file);
  } catch (e) {
    send(res, 500, { error: 'server error' });
  }
});

function lanUrls() {
  var out = [], ifs = os.networkInterfaces();
  Object.keys(ifs).forEach(function (n) {
    ifs[n].forEach(function (a) { if (a.family === 'IPv4' && !a.internal) out.push('http://' + a.address + ':' + PORT); });
  });
  return out;
}

process.on('SIGINT', function () { flushMetrics(); process.exit(0); });
process.on('SIGTERM', function () { flushMetrics(); process.exit(0); });

if (require.main === module) {
  server.listen(PORT, '0.0.0.0', function () {
    console.log('\n  Kindle Dash is running\n');
    var urls = lanUrls();
    if (!urls.length) urls = ['http://localhost:' + PORT];
    urls.forEach(function (u) {
      console.log('  Type on the Kindle : ' + u + '/');
      console.log('  Open on your phone : ' + u + '/admin');
    });
    console.log(PIN ? '\n  Admin PIN is enabled.\n' : '\n  Tip: set KINDLE_PIN=1234 to protect the admin app.\n');
  });
}

module.exports = server;
