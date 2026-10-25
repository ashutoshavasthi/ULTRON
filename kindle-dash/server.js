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
    layout: 'classic',      // classic | minimal | poster
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
  name: 'string', layout: ['classic', 'minimal', 'poster'],
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
    if (rule === 'string') state.settings[k] = clean(v, 40);
    else if (rule === 'bool') state.settings[k] = !!v;
    else if (rule === 'int') {
      v = parseInt(v, 10);
      if (!isNaN(v)) state.settings[k] = Math.max(0, Math.min(v, 1440));
    } else if (rule.indexOf(v) !== -1) state.settings[k] = v;
  });
  state.settings.quoteMinutes = Math.max(1, state.settings.quoteMinutes);
  state.settings.maxTasks = Math.max(1, Math.min(state.settings.maxTasks, 12));
}

function authed(req) {
  if (!PIN) return true;
  var a = Buffer.from(String(req.headers['x-pin'] || ''));
  var b = Buffer.from(PIN);
  return a.length === b.length && crypto.timingSafeEqual(a, b);
}

function api(req, res, url) {
  var m = req.method, p = url.pathname, mm;

  if (m === 'GET' && p === '/api/rev') return send(res, 200, { rev: state.rev });
  if (m === 'GET' && p === '/api/state') return send(res, 200, state);
  if (m === 'GET' && p === '/api/auth') return send(res, 200, { pinRequired: !!PIN, ok: authed(req) });

  if (m === 'GET') return send(res, 404, { error: 'not found' });
  if (!authed(req)) return send(res, 401, { error: 'pin required' });

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
