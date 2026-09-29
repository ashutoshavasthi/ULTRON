// Reads JSON [{id, tex, display}] on stdin, writes JSON {id: html} on stdout
const katex = require('./katex/dist/katex.js');
let data = '';
process.stdin.on('data', c => data += c);
process.stdin.on('end', () => {
  const items = JSON.parse(data);
  const out = {};
  for (const it of items) {
    try {
      out[it.id] = katex.renderToString(it.tex, {displayMode: it.display, throwOnError: true, strict: 'ignore',
        macros: {"\\ohm": "\\Omega"}});
    } catch (e) {
      out[it.id] = '<span style="color:red">MATH ERROR: ' + String(e.message).replace(/</g,'&lt;') + ' in ' + it.tex.replace(/</g,'&lt;') + '</span>';
      console.error('MATH ERROR', it.tex, e.message);
    }
  }
  process.stdout.write(JSON.stringify(out));
});
