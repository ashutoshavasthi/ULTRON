'use strict';
// End-to-end API smoke test. Run: npm test
var assert = require('assert');
var fs = require('fs');
var os = require('os');
var path = require('path');
var http = require('http');

process.env.DATA_DIR = fs.mkdtempSync(path.join(os.tmpdir(), 'kd-'));
process.env.KINDLE_PIN = '4321';
var server = require('../server.js');

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

    console.log('smoke ok');
    process.exit(0);
  } catch (e) { console.error(e); process.exit(1); }
});
