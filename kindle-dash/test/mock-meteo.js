'use strict';
// Tiny stand-in for Open-Meteo so tests and screenshots work offline.
var http = require('http');
module.exports = function start(cb) {
  var srv = http.createServer(function (req, res) {
    var u = new URL(req.url, 'http://x'), out;
    if (u.pathname === '/v1/search') {
      out = { results: [{ name: 'Berlin', admin1: 'Berlin', country: 'Germany', latitude: 52.52, longitude: 13.41 }] };
    } else {
      var d = new Date(), days = [], i, codes = [71, 71, 61, 3, 1], hi = [6.7, 8.1, 7.6, 8.5, 6], lo = [4.1, 3.3, 1.1, 3.7, 2.6];
      for (i = 0; i < 5; i++) { var x = new Date(d.getTime() + i * 86400000); days.push(x.toISOString().slice(0, 10)); }
      out = { current: { temperature_2m: 6.5, weather_code: 3 },
        daily: { time: days, weather_code: codes, temperature_2m_max: hi, temperature_2m_min: lo } };
    }
    res.writeHead(200, { 'content-type': 'application/json' });
    res.end(JSON.stringify(out));
  });
  srv.listen(0, function () { cb(srv, 'http://127.0.0.1:' + srv.address().port); });
};
