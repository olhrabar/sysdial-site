// Headless Chrome: no horizontal page overflow at 390 px (light + dark) for en and uk index/pricing/privacy.
// Needs Node >= 22 (built-in WebSocket/fetch) and Chrome (CHROME env var, or google-chrome on PATH).
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import {spawn} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import os from 'node:os';
const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');
const PAGES = ['index.html', 'pricing.html', 'privacy.html', 'uk/index.html', 'uk/pricing.html', 'uk/privacy.html'];
const MIME = {'.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript', '.webp': 'image/webp', '.png': 'image/png', '.woff2': 'font/woff2', '.svg': 'image/svg+xml'};
const server = http.createServer((req, res) => {
  let p = decodeURIComponent(req.url.split('?')[0]); if (p.endsWith('/')) p += 'index.html';
  const f = path.join(ROOT, p);
  if (!f.startsWith(ROOT) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { res.writeHead(404); return res.end(); }
  res.writeHead(200, {'content-type': MIME[path.extname(f)] || 'application/octet-stream'}); fs.createReadStream(f).pipe(res);
});
await new Promise(r => server.listen(0, '127.0.0.1', r));
const base = 'http://127.0.0.1:' + server.address().port;
const chromeBin = process.env.CHROME || ['google-chrome', 'google-chrome-stable', 'chromium', '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'].find(c => c.startsWith('/') ? fs.existsSync(c) : true);
const port = 9400 + Math.floor(Math.random() * 400);
const prof = fs.mkdtempSync(path.join(os.tmpdir(), 'chrome-ci-'));
const chrome = spawn(chromeBin, ['--headless=new', '--no-sandbox', '--disable-gpu', '--disable-dev-shm-usage', '--remote-debugging-port=' + port, '--user-data-dir=' + prof, 'about:blank'], {stdio: ['ignore', 'ignore', 'pipe']});
let chromeErr = ''; chrome.stderr.on('data', d => { chromeErr += d; });
chrome.on('error', e => { chromeErr += String(e); });
const done = (code) => { try { chrome.kill(); } catch {} server.close(); process.exit(code); };
let version; for (let i = 0; i < 150 && !version; i++) { try { version = await (await fetch(`http://127.0.0.1:${port}/json/version`)).json(); } catch { await new Promise(r => setTimeout(r, 200)); } }
if (!version) { console.error('Chrome did not start (' + chromeBin + ')\n' + chromeErr.slice(-2000)); done(2); }
const tab = await (await fetch(`http://127.0.0.1:${port}/json/new?about:blank`, {method: 'PUT'})).json();
const ws = new WebSocket(tab.webSocketDebuggerUrl); await new Promise(r => ws.onopen = r);
let id = 0; const pend = {}; let errors = [];
ws.onmessage = e => { const m = JSON.parse(e.data); if (m.id && pend[m.id]) { pend[m.id](m.result); delete pend[m.id]; }
  if (m.method === 'Runtime.exceptionThrown') errors.push(m.params.exceptionDetails.text + ' ' + (m.params.exceptionDetails.exception?.description || '')); };
const send = (method, params = {}) => new Promise(r => { const i = ++id; pend[i] = r; ws.send(JSON.stringify({id: i, method, params})); });
await send('Page.enable'); await send('Runtime.enable');
let failed = 0;
for (const pg of PAGES) for (const theme of ['light', 'dark']) {
  errors = [];
  await send('Emulation.setDeviceMetricsOverride', {width: 390, height: 900, deviceScaleFactor: 1, mobile: true});
  await send('Emulation.setEmulatedMedia', {features: [{name: 'prefers-color-scheme', value: theme}]});
  await send('Page.navigate', {url: `${base}/${pg}`});
  await new Promise(r => setTimeout(r, 1500));
  const r = (await send('Runtime.evaluate', {returnByValue: true, expression: 'JSON.stringify({sw: document.documentElement.scrollWidth, iw: innerWidth, dark: matchMedia("(prefers-color-scheme: dark)").matches})'})).result.value;
  const v = JSON.parse(r);
  const ok = v.sw <= v.iw && v.dark === (theme === 'dark') && errors.length === 0;
  if (!ok) failed++;
  console.log(`${ok ? 'ok  ' : 'FAIL'} ${pg} ${theme} scrollWidth=${v.sw} innerWidth=${v.iw}${errors.length ? ' js-errors: ' + errors.join('; ') : ''}`);
}
done(failed ? 1 : 0);
