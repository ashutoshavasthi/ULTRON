/* Kindle Dash display. STRICT ES5: Kindle's experimental browser is old WebKit.
   No let/const, arrow functions, template strings, fetch or Promises. */
(function () {
  var FAST = /[?&]fast=1/.test(location.search); // used by the admin live preview
  var state = null, lastRev = 0, clockTimer = null, quoteTimers = [];
  var prevClock = '', lastQuoteKey = null, lastFlash = new Date().getTime();
  var taskFit = 6, clockBase = 100, cache = {};
  var live = { weather: null, metrics: [] }, liveSig = '', lastLive = 0, online = true;
  var DAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
  var MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];

  function $(id) { return document.getElementById(id); }
  function pad(n) { return n < 10 ? '0' + n : '' + n; }
  function esc(s) {
    return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }
  // Only touch the DOM when content changed: every write costs an e-ink refresh.
  function setHtml(id, html) {
    if (cache[id] === html) { return; }
    cache[id] = html;
    $(id).innerHTML = html;
  }
  function size() {
    var w = window.innerWidth || document.documentElement.clientWidth || 758;
    var h = window.innerHeight || document.documentElement.clientHeight || 1024;
    return { w: w, h: h };
  }

  /* ---------- network ---------- */
  function get(url, cb) {
    var x = new XMLHttpRequest();
    x.open('GET', url + (url.indexOf('?') < 0 ? '?' : '&') + '_=' + new Date().getTime(), true);
    x.onreadystatechange = function () {
      if (x.readyState !== 4) { return; }
      if (x.status === 200) {
        try { cb(null, JSON.parse(x.responseText)); } catch (e) { cb(e); }
      } else { cb(new Error('http ' + x.status)); }
    };
    try { x.timeout = 8000; } catch (e2) { /* old engines */ }
    x.send(null);
  }
  function setOnline(ok) { online = ok; renderStatus(); }
  function renderStatus() {
    var hub = state && state.settings.layout === 'hub', d = new Date(), t = lastLive ? new Date(lastLive) : d;
    setHtml('status', !online ? 'offline' : hub ? 'Last update: ' + pad(t.getHours()) + ':' + pad(t.getMinutes()) : '');
  }
  function liveSignature() {
    var n = state ? Math.min(state.settings.maxMetrics, live.metrics.length) : 0;
    return (live.weather && live.weather.days.length ? 'w' : '-') + n;
  }
  function loadLive() {
    get('/api/live', function (err, l) {
      setOnline(!err);
      if (err || !state) { return; }
      live = l;
      lastLive = new Date().getTime();
      if (liveSignature() !== liveSig) { liveSig = liveSignature(); layout(); cache = {}; }
      renderAll(false);
    });
  }
  function poll() {
    get('/api/rev', function (err, r) {
      setOnline(!err);
      if (!err && r.rev !== lastRev) { loadState(); }
    });
  }
  function loadState() {
    get('/api/state', function (err, s) {
      setOnline(!err);
      if (err) { return; }
      state = s;
      lastRev = s.rev;
      cache = {};
      liveSig = liveSignature();
      layout();
      renderAll(true);
      loadLive();
    });
  }

  /* ---------- layout ---------- */
  function layout() {
    var s = state.settings, z = size(), W = z.w, H = z.h, hub = s.layout === 'hub';
    var hasWall = !!state.wallpaper && s.wallpaperMode !== 'off';
    var full = hasWall && (s.wallpaperMode === 'full' || s.layout === 'poster');
    var panel = hasWall && !full && !hub && s.layout !== 'minimal';
    var wantQuote = s.quoteMode !== 'off' && state.quotes.length > 0;
    var wantTasks = s.showTasks;
    var wantProg = s.showProgress && s.layout !== 'minimal' && !hub;
    var wantWeather = hub && !!(live.weather && live.weather.days.length);
    var nMet = hub ? Math.min(s.maxMetrics, live.metrics.length) : 0;
    var url = '/wallpaper.png?v=' + state.wallpaper;
    document.body.className = s.theme === 'dark' ? 'dark' : '';
    document.body.style.fontSize = Math.round(W / 20) + 'px';

    var app = $('app');
    app.className = hub ? 'hub' : '';
    app.style.backgroundImage = full ? 'url(' + url + ')' : 'none';

    var m = Math.round(W * 0.05), g = Math.round(H * 0.013), cw = W - 2 * m;
    var hDate = Math.round(H * (hub ? 0.078 : full ? 0.085 : 0.07));
    var hClock = Math.round(H * (hub ? 0.115 : s.layout === 'minimal' ? 0.36 : s.layout === 'poster' ? 0.22 : 0.2));
    var hProg = wantProg ? Math.round(H * 0.072) : 0;
    var hQuote = wantQuote ? Math.round(H * (s.layout === 'minimal' ? 0.2 : hub ? 0.1 : 0.15)) : 0;
    var hWeather = wantWeather ? Math.round(H * 0.185) : 0;
    var hMet = nMet ? Math.ceil(nMet / 2) * Math.round(H * 0.15) : 0;
    function room() {
      var parts = 2 + (wantProg ? 1 : 0) + (hQuote ? 1 : 0) + (panel ? 1 : 0) + (wantTasks ? 1 : 0) + (wantWeather ? 1 : 0) + (nMet ? 1 : 0);
      return H - 2 * m - hDate - hClock - hProg - hQuote - hWeather - hMet - g * (parts - 1) - (hub ? Math.round(H * 0.02) : 0);
    }
    var flex = room();
    // Hub budgets by priority: with many tiles, drop the quote first, then the task list, rather than clip.
    if (hub && wantTasks && flex < H * 0.2) { hQuote = 0; flex = room(); }
    if (hub && wantTasks && flex < H * 0.17) { wantTasks = false; flex = room(); hClock += Math.min(flex, Math.round(H * 0.05)); flex = 0; }
    var hWall = 0, hTasks = 0;
    if (panel && wantTasks) { hWall = Math.round(flex * 0.4); hTasks = flex - hWall; }
    else if (panel) { hWall = flex; }
    else if (wantTasks) { hTasks = flex; }
    else { hClock += flex; }

    var y = m;
    function place(id, h, inset, extraCls) {
      var el = $(id);
      if (h <= 0) { el.style.display = 'none'; return; }
      el.style.display = 'block';
      el.style.left = (inset ? 0 : m) + 'px';
      el.style.width = (inset ? W : cw) + 'px';
      el.style.top = y + 'px';
      el.style.height = h + 'px';
      el.className = 'blk' + (extraCls ? ' ' + extraCls : '');
      y += h + g;
    }
    var card = full ? 'card' : '';
    place('date', hDate, false, card);
    var inverted = s.layout === 'poster';
    place('clock', hClock, inverted, (inverted ? 'inverted ' : '') + (full && !inverted ? 'card' : ''));
    place('weather', hWeather, false, card);
    place('metrics', hMet, false, card);
    place('prog', hProg, false, card);
    if (panel) {
      place('wall', hWall, false, '');
      $('wall').style.backgroundImage = 'url(' + url + ')';
    } else { $('wall').style.display = 'none'; }
    place('tasks', hTasks, false, card);
    place('quote', hQuote, false, card);

    var fs = Math.round(W / 20);
    var clockPx = Math.min(hClock * 0.82, (cw - 20) / 2.75);
    var ce = $('clock');
    clockBase = Math.round(clockPx);
    ce.style.fontSize = clockBase + 'px';
    ce.style.lineHeight = hClock + 'px';
    var cap = s.layout === 'minimal' ? 3 : s.maxTasks;
    var pxInner = hTasks - (full ? 8 : 0);
    var fit = Math.floor((pxInner - fs * 0.93 - fs * 0.9) / (fs * 1.75));
    taskFit = Math.max(1, Math.min(cap, fit));
    prevClock = '';
  }

  /* ---------- renderers ---------- */
  function greeting(h) {
    return h < 5 ? 'Good night' : h < 12 ? 'Good morning' : h < 18 ? 'Good afternoon' : 'Good evening';
  }
  function isoWeek(d) {
    var t = new Date(Date.UTC(d.getFullYear(), d.getMonth(), d.getDate()));
    var dn = t.getUTCDay() || 7;
    t.setUTCDate(t.getUTCDate() + 4 - dn);
    var y0 = new Date(Date.UTC(t.getUTCFullYear(), 0, 1));
    return Math.ceil(((t - y0) / 86400000 + 1) / 7);
  }
  function renderDate(d) {
    var s = state.settings;
    if (s.layout === 'hub') {
      setHtml('date', '<div class="in"><div class="dl"><div class="dw">' + greeting(d.getHours()) + (s.name ? ', ' + esc(s.name) : '') +
        '</div><div class="dd">' + DAYS[d.getDay()] + ', ' + d.getDate() + ' ' + MONTHS[d.getMonth()] + ' ' + d.getFullYear() + '</div></div></div>');
      return;
    }
    var right = greeting(d.getHours()) + (s.name ? ',<br><b>' + esc(s.name) + '</b>' : '') +
      '<br><span class="wk">Week ' + isoWeek(d) + '</span>';
    setHtml('date', '<div class="in"><div class="dl"><div class="dw">' + DAYS[d.getDay()] + '</div><div class="dd">' +
      d.getDate() + ' ' + MONTHS[d.getMonth()] + ' ' + d.getFullYear() + '</div></div><div class="dr">' + right + '</div></div>');
  }
  function renderClock(d, noAnim) {
    var s = state.settings, h = d.getHours(), suffix = '';
    if (!s.clock24) { suffix = h >= 12 ? 'PM' : 'AM'; h = h % 12 || 12; }
    var str = (s.clock24 ? pad(h) : '' + h) + ':' + pad(d.getMinutes());
    var anim = s.animations && !noAnim && prevClock !== '' && prevClock.length === str.length && prevClock !== str;
    var html = '', changed = false, i, c, inv;
    for (i = 0; i < str.length; i++) {
      c = str.charAt(i);
      inv = anim && prevClock.charAt(i) !== c;
      if (inv) { changed = true; }
      html += '<span class="ch' + (c === ':' ? ' col' : '') + (inv ? ' inv' : '') + '">' + c + '</span>';
    }
    if (suffix) { html += '<span class="ap">' + suffix + '</span>'; }
    prevClock = str;
    setHtml('clock', html);
    fitClock();
    // Stepped "flip": changed digits show inverted for a moment, then settle.
    if (changed) { setTimeout(function () { renderClock(new Date(), true); }, 900); }
  }
  // The AM/PM suffix makes the clock wider than the digits-only estimate: shrink to fit.
  function fitClock() {
    var el = $('clock');
    el.style.fontSize = clockBase + 'px';
    if (el.scrollWidth > el.clientWidth) {
      el.style.fontSize = Math.floor(clockBase * el.clientWidth / el.scrollWidth * 0.96) + 'px';
    }
  }
  function fmtTemp(v) { return (Math.round(v * 10) / 10).toFixed(1); }
  function renderWeather() {
    if ($('weather').style.display === 'none') { return; }
    var w = live.weather, c = state.settings.theme === 'dark' ? 'w' : 'k', html = '', i, day, p, name;
    for (i = 0; i < w.days.length && i < 5; i++) {
      day = w.days[i];
      p = day.date.split('-');
      name = i === 0 ? 'Today' : DAYS[new Date(+p[0], +p[1] - 1, +p[2]).getDay()].slice(0, 3);
      html += '<div class="wd"><div class="wn">' + name + '</div><img class="wi" alt="" src="/api/icon/' + day.icon + '.svg?c=' + c +
        '"><div class="hi">' + fmtTemp(day.hi) + '&deg;</div><div class="lo">' + fmtTemp(day.lo) + '&deg;</div></div>';
    }
    setHtml('weather', html);
  }
  function fmtVal(v) {
    var out = Math.abs(v) >= 100 ? String(Math.round(v)) : String(Math.round(v * 10) / 10);
    return out.replace(/\B(?=(\d{3})+(?!\d))/g, ',');
  }
  function renderMetrics() {
    if ($('metrics').style.display === 'none') { return; }
    var n = Math.min(state.settings.maxMetrics, live.metrics.length), c = state.settings.theme === 'dark' ? 'w' : 'k', html = '', i, m;
    for (i = 0; i < n; i++) {
      m = live.metrics[i];
      html += '<div class="mt' + (i % 2 ? ' r' : '') + '"><div class="ml">' + esc(m.label) + '</div><div class="mv">' + fmtVal(m.value) +
        '<span class="mu">' + esc(m.unit) + '</span></div><img class="ms" alt="" src="/api/spark/' + encodeURIComponent(m.id) +
        '.svg?w=360&h=64&c=' + c + '&v=' + m.t + '"></div>';
    }
    setHtml('metrics', html);
  }
  function renderProgress(d) {
    if ($('prog').style.display === 'none') { return; }
    var h = d.getHours(), mins = h * 60 + d.getMinutes(), html = '<div class="bar">', i;
    for (i = 0; i < 24; i++) {
      html += '<div class="seg' + (i < h ? ' f' : i === h ? ' p' : '') + (i === 23 ? ' last' : '') + '"></div>';
    }
    html += '</div><div class="lab"><b>' + Math.round(mins / 14.4) + '%</b> of the day gone &middot; ' +
      Math.floor((1440 - mins) / 60) + 'h ' + pad((1440 - mins) % 60) + 'm left</div>';
    setHtml('prog', html);
  }
  function renderTasks(d) {
    if ($('tasks').style.display === 'none') { return; }
    var list = state.tasks.slice(), total = list.length, i, done = 0, nowStr = pad(d.getHours()) + ':' + pad(d.getMinutes());
    for (i = 0; i < total; i++) { if (list[i].done) { done++; } }
    var nextId = null;
    for (i = 0; i < total && nextId === null; i++) {
      if (!list[i].done && (!list[i].time || list[i].time >= nowStr)) { nextId = list[i].id; }
    }
    for (i = 0; i < total && nextId === null; i++) { if (!list[i].done) { nextId = list[i].id; } }
    var shown = list;
    if (total > taskFit) { // not enough room: open tasks first
      shown = [];
      for (i = 0; i < total; i++) { if (!list[i].done) { shown.push(list[i]); } }
      for (i = 0; i < total; i++) { if (list[i].done) { shown.push(list[i]); } }
      shown = shown.slice(0, taskFit);
    }
    var html = '<div class="th">TODAY<span>' + done + ' / ' + total + '</span></div>', t;
    if (!total) { html += '<div class="none">Nothing planned. Enjoy the day.</div>'; }
    for (i = 0; i < shown.length; i++) {
      t = shown[i];
      html += '<div class="tr' + (t.done ? ' dn' : '') + (t.id === nextId ? ' nx' : '') + '"><span class="tb">' +
        (t.done ? '<i></i>' : '') + '</span><span class="tt">' + (t.time ? esc(t.time) : '&nbsp;') + '</span><span class="tx">' + esc(t.text) + '</span></div>';
    }
    if (total > shown.length) { html += '<div class="tm">+' + (total - shown.length) + ' more</div>'; }
    setHtml('tasks', html);
  }

  function pickQuote(now) {
    var s = state.settings, n = state.quotes.length;
    if (!n || s.quoteMode === 'off') { return null; }
    var slot = Math.floor(now / (Math.max(1, s.quoteMinutes) * 60000)), idx;
    if (s.quoteMode === 'daily') {
      idx = Math.floor((now - new Date().getTimezoneOffset() * 60000) / 86400000) % n;
    } else if (s.quoteMode === 'random') {
      idx = (((slot * 1103515245) + 12345) % 2147483648) % n;
    } else { idx = slot % n; }
    return state.quotes[idx];
  }
  function quoteHtml(words, shownCount, author, showAuthor) {
    var out = [], i;
    for (i = 0; i < words.length; i++) {
      out.push(i < shownCount ? esc(words[i]) : '<span class="hid">' + esc(words[i]) + '</span>');
    }
    return '<div class="in"><div class="qt">&ldquo;' + out.join(' ') + '&rdquo;</div>' +
      (author ? '<div class="qa' + (showAuthor ? '' : ' hid') + '">&mdash; ' + esc(author) + '</div>' : '') + '</div>';
  }
  function renderQuote(now, force) {
    if ($('quote').style.display === 'none') { return; }
    var q = pickQuote(now);
    if (!q) { return; }
    var key = q.id + ':' + q.text;
    if (key === lastQuoteKey && !force) { return; }
    var firstDraw = lastQuoteKey === null;
    lastQuoteKey = key;
    while (quoteTimers.length) { clearTimeout(quoteTimers.pop()); }
    var words = q.text.split(' ');
    if (!state.settings.animations || firstDraw || FAST) {
      setHtml('quote', quoteHtml(words, words.length, q.author, true));
      return;
    }
    // Typewriter in 4 chunks: e-ink can't do smooth motion, so reveal in a few clean steps.
    var steps = 4, step;
    function show(k) {
      return function () {
        var count = k >= steps ? words.length : Math.ceil(words.length * k / steps);
        setHtml('quote', quoteHtml(words, count, q.author, k >= steps));
      };
    }
    for (step = 1; step <= steps; step++) { quoteTimers.push(setTimeout(show(step), (step - 1) * 600)); }
  }

  function flash() {
    var f = $('flash');
    f.style.background = '#000';
    f.style.display = 'block';
    setTimeout(function () {
      f.style.background = '#fff';
      setTimeout(function () { f.style.display = 'none'; }, 300);
    }, 400);
  }

  function renderAll(force) {
    if (!state) { return; }
    var d = new Date(), now = d.getTime();
    renderDate(d);
    renderClock(d, force);
    renderWeather();
    renderMetrics();
    renderProgress(d);
    renderTasks(d);
    renderStatus();
    renderQuote(now, force);
    var fm = state.settings.flashMinutes;
    if (!FAST && fm > 0 && now - lastFlash >= fm * 60000 - 5000) { lastFlash = now; flash(); }
  }

  /* ---------- clock loop ---------- */
  // Recompute from the real time on every tick: the Kindle sleeps and timers fire late.
  function schedule() {
    clearTimeout(clockTimer);
    clockTimer = setTimeout(tick, 60000 - (new Date().getTime() % 60000) + 250);
  }
  function tick() {
    renderAll(false);
    poll();
    loadLive();
    schedule();
  }

  window.onresize = function () { if (state) { layout(); cache = {}; renderAll(true); } };
  loadState();
  schedule();
  setInterval(poll, FAST ? 2500 : 30000);
  // If the device wakes from sleep, timers may have been frozen: catch up as soon as possible.
  setInterval(function () {
    if (new Date().getTime() - (window.__lastBeat || 0) > 90000) { tick(); }
    window.__lastBeat = new Date().getTime();
  }, 15000);
})();
