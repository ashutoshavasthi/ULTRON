'use strict';
// End-to-end API smoke test. Run: npm test
var assert = require('assert');
var fs = require('fs');
var os = require('os');
var path = require('path');
var http = require('http');

process.env.DATA_DIR = fs.mkdtempSync(path.join(os.tmpdir(), 'kd-'));
process.env.KINDLE_PIN = '4321';
var mock = require('./mock-meteo.js');
var server;

function call(port, method, url, body, headers) {
  return new Promise(function (resolve, reject) {
    var data = body === undefined ? null : Buffer.isBuffer(body) ? body : Buffer.from(JSON.stringify(body));
    var req = http.request({ port: port, method: method, path: url, headers: Object.assign({ 'x-pin': '4321' }, headers || {}) }, function (res) {
      var chunks = [];
      res.on('data', function (c) { chunks.push(c); });
      res.on('end', function () {
        var buf = Buffer.concat(chunks), j = null;
        try { j = JSON.parse(buf.toString()); } catch (e) { /* not json */ }
        resolve({ status: res.statusCode, json: j, buf: buf });
      });
    });
    req.on('error', reject);
    if (data) req.write(data);
    req.end();
  });
}

mock(function (meteo, base) {
process.env.OPEN_METEO_URL = base; process.env.OPEN_METEO_GEO_URL = base;
server = require('../server.js');
server.listen(0, async function () {
  var port = server.address().port, r, rev;
  try {
    r = await call(port, 'GET', '/api/state'); rev = r.json.rev;
    assert.equal(r.status, 200); assert(r.json.tasks.length > 0);

    r = await call(port, 'POST', '/api/tasks', { text: 'Write tests', time: '7:05' }, {});
    assert.equal(r.status, 200); assert(r.json.rev > rev, 'rev bumps on write');
    var t = r.json.tasks[r.json.tasks.length - 1];
    assert.equal(t.text, 'Write tests'); assert.equal(t.time, '07:05');

    r = await call(port, 'PATCH', '/api/tasks/' + t.id, { done: true });
    assert.equal(r.json.tasks.filter(function (x) { return x.id === t.id; })[0].done, true);

    r = await call(port, 'POST', '/api/tasks/move', { id: t.id, dir: 'up' });
    assert.equal(r.json.tasks[r.json.tasks.length - 2].id, t.id);

    r = await call(port, 'POST', '/api/tasks/clear-done');
    assert(!r.json.tasks.some(function (x) { return x.done; }));

    r = await call(port, 'PUT', '/api/settings', { layout: 'poster', flashMinutes: '20', animations: false, evil: 1, quoteMode: 'bogus' });
    assert.equal(r.json.settings.layout, 'poster'); assert.equal(r.json.settings.flashMinutes, 20);
    assert.equal(r.json.settings.animations, false); assert.equal(r.json.settings.quoteMode, 'rotate');
    assert(!('evil' in r.json.settings));

    r = await call(port, 'POST', '/api/quotes', { text: 'Hello', author: 'Me' });
    assert.equal(r.json.quotes[r.json.quotes.length - 1].text, 'Hello');

    r = await call(port, 'PUT', '/api/wallpaper', Buffer.from('not a png at all'));
    assert.equal(r.status, 400);
    var png = Buffer.concat([Buffer.from([0x89]), Buffer.from('PNG\r\n\x1a\n'), Buffer.alloc(20)]);
    r = await call(port, 'PUT', '/api/wallpaper', png);
    assert.equal(r.status, 200); assert(r.json.wallpaper);
    r = await call(port, 'GET', '/wallpaper.png');
    assert.equal(r.status, 200); assert.equal(r.buf.length, png.length);

    r = await call(port, 'POST', '/api/tasks', { text: 'nope' }, { 'x-pin': 'wrong' });
    assert.equal(r.status, 401, 'PIN blocks writes');
    r = await call(port, 'GET', '/api/rev', undefined, { 'x-pin': '' });
    assert.equal(r.status, 200, 'PIN does not block the Kindle reading');

    r = await call(port, 'GET', '/../server.js');
    assert.notEqual(r.status, 200, 'no path traversal');
    r = await call(port, 'GET', '/'); assert.equal(r.status, 200);
    r = await call(port, 'GET', '/admin'); assert.equal(r.status, 200);

    // weather + geocode
    r = await call(port, 'GET', '/api/geocode?q=Berlin');
    assert.equal(r.json.results[0].name, 'Berlin');
    r = await call(port, 'GET', '/api/live');
    assert.equal(r.json.weather, null, 'no weather until a location is set');
    r = await call(port, 'PUT', '/api/settings', { city: 'Berlin', lat: 52.52, lon: '13.41' });
    assert.equal(r.json.settings.lon, 13.41);
    r = await call(port, 'GET', '/api/live');
    assert.equal(r.json.weather.days.length, 5); assert.equal(r.json.weather.days[0].icon, 'snow');
    assert.equal(r.json.weather.now.temp, 6.5);

    // sensors
    r = await call(port, 'POST', '/api/metrics', { id: 'CO2', label: 'CO2', value: 812, unit: 'ppm' });
    assert.equal(r.status, 200); assert.equal(r.json.id, 'co2');
    r = await call(port, 'POST', '/api/metrics', { id: 'co2', value: 'abc' });
    assert.equal(r.status, 400);
    r = await call(port, 'POST', '/api/metrics', { id: 'x', value: 1 }, { 'x-pin': 'wrong' });
    assert.equal(r.status, 401, 'sensors need the PIN');
    rev = (await call(port, 'GET', '/api/rev')).json.rev;
    await call(port, 'POST', '/api/metrics', { id: 'co2', value: 900 });
    assert.equal((await call(port, 'GET', '/api/rev')).json.rev, rev, 'sensor data must not bump rev');
    await call(port, 'POST', '/api/metrics/demo', {});
    r = await call(port, 'GET', '/api/live'); assert(r.json.metrics.length === 4);
    r = await call(port, 'GET', '/api/spark/inside.svg?c=w');
    assert.equal(r.status, 200); assert(/<polyline/.test(r.buf.toString()));
    r = await call(port, 'GET', '/api/icon/rain.svg?c=k'); assert(/<svg/.test(r.buf.toString()));
    r = await call(port, 'DELETE', '/api/metrics/co2'); assert(!r.json.metrics.some(function (m) { return m.id === 'co2'; }));

    console.log('smoke ok');
    process.exit(0);
  } catch (e) { console.error(e); process.exit(1); }
});
});
