// Social sharing images (1200 x 630) for the pages, rendered from an HTML template in headless Chrome.
// Uses the official logo file unmodified (only scaled down), the site's own fonts and real client work.
//
//   npm ci && npm i --no-save playwright-core && CHROME=/path/to/chrome node tools/og-images.mjs
//
// Writes JPEGs into static/. build.py publishes them at the site root and points each page's
// og:image / twitter:image at its own picture.
import { createRequire } from 'node:module';
import path from 'node:path';
import fs from 'node:fs';
const require = createRequire(import.meta.url);
const { chromium } = require('playwright-core');

const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const file = p => 'file://' + path.join(root, p);
const CHROME = process.env.CHROME || '/usr/bin/google-chrome';

// Every line of text comes from the page the image belongs to.
const IMAGES = [
  { out: 'static/og-image.jpg', title: 'Websites That Turn Visitors Into Clients',
    sub: 'Shopify, WordPress and custom web development', proof: true,
    shot: 'assets/cover-hasi.webp', label: 'hasi', phone: 'assets/phone-veliora.webp' },
  { out: 'static/og-shopify-development.jpg', title: 'Custom Shopify development, built to sell and easy to run.',
    sub: 'Client work shown: Veliora, a beauty and skincare Shopify store',
    shot: 'assets/cover-veliora.webp', label: 'veliora', phone: 'assets/phone-veliora.webp' },
  { out: 'static/og-shopify-store-redesign.jpg', title: 'Shopify store design and redesign, without pausing sales.',
    sub: 'Client work shown: HASI, a travel and tour Shopify redesign',
    shot: 'assets/cover-hasi.webp', label: 'hasi', phone: 'assets/phone-hasi.webp' },
  { out: 'static/og-wordpress-development.jpg', title: 'WordPress and WooCommerce development without the bloat.',
    sub: 'Client work shown: WERK, a streetwear WooCommerce store',
    shot: 'assets/cover-werk.webp', label: 'werk', phone: 'assets/phone-werk.webp' },
];

const star = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.4l2.9 6.3 6.7.7-5 4.5 1.4 6.7L12 17.2l-6 3.4 1.4-6.7-5-4.5 6.7-.7z"/></svg>';

function page(img) {
  const long = img.title.length > 44;
  return `<!DOCTYPE html><html><head><meta charset="utf-8"><style>
@font-face{font-family:"RFC";src:url(${file('assets/roboto-flex-compressed.woff2')}) format("woff2");font-weight:300 700;size-adjust:120.8%;ascent-override:92.8%;descent-override:24.4%;line-gap-override:0%}
@font-face{font-family:"Manrope";src:url(${file('node_modules/@fontsource-variable/manrope/files/manrope-latin-wght-normal.woff2')}) format("woff2");font-weight:200 800}
*{box-sizing:border-box;margin:0}
html,body{width:1200px;height:630px;overflow:hidden}
body{position:relative;background:#19181D;font-family:"Manrope",sans-serif;color:#F5F4F1}
.glow{position:absolute;inset:0;background:radial-gradient(620px 520px at 82% 34%,rgba(231,81,57,.58),rgba(215,90,68,.18) 48%,transparent 72%),radial-gradient(900px 500px at 10% 110%,rgba(231,81,57,.12),transparent 60%)}
.grain{position:absolute;inset:0;background:linear-gradient(180deg,rgba(25,24,29,0) 60%,rgba(25,24,29,.55))}
.copy{position:absolute;left:72px;top:64px;width:${long ? 560 : 540}px;display:flex;flex-direction:column;height:502px}
.pill{display:inline-flex;align-self:flex-start;align-items:center;padding:16px 26px;border-radius:999px;background:#fff;box-shadow:0 12px 30px -16px rgba(0,0,0,.6)}
.pill img{display:block;height:34px;width:auto}
h1{margin-top:44px;font-family:"RFC",sans-serif;font-weight:500;font-size:${long ? 62 : 92}px;line-height:1.02;letter-spacing:0;color:#F5F4F1;text-wrap:balance;max-width:${long ? 500 : 540}px}
.rule{width:96px;height:4px;border-radius:4px;background:#E75139;margin-top:30px}
.sub{margin-top:22px;font-size:${long ? 21 : 24}px;font-weight:500;line-height:1.4;color:rgba(245,244,241,.74);max-width:490px;text-wrap:balance}
.foot{margin-top:auto;display:flex;align-items:center;gap:22px;font-size:18px;font-weight:600;color:rgba(245,244,241,.86)}
.proof{display:flex;align-items:center;gap:8px}
.proof svg{width:20px;height:20px;fill:#E75139}
.dot{width:5px;height:5px;border-radius:50%;background:rgba(245,244,241,.4)}
.site{color:rgba(245,244,241,.62);font-weight:500}
.browser{position:absolute;left:668px;top:118px;width:640px;border-radius:18px;overflow:hidden;background:#232228;box-shadow:0 40px 80px -30px rgba(0,0,0,.8),0 0 0 1px rgba(255,255,255,.1)}
.bar{height:38px;display:flex;align-items:center;gap:8px;padding:0 16px;background:#2A292F}
.bar i{width:10px;height:10px;border-radius:50%;background:rgba(255,255,255,.22)}
.bar span{margin-left:14px;padding:4px 14px;border-radius:999px;background:rgba(255,255,255,.08);font-size:13px;font-weight:600;color:rgba(245,244,241,.75)}
.browser img{display:block;width:640px;height:400px;object-fit:cover;object-position:top}
.phone{position:absolute;left:592px;top:246px;width:172px;height:352px;border-radius:30px;padding:7px;background:#0E0D10;box-shadow:0 30px 60px -20px rgba(0,0,0,.85),0 0 0 1px rgba(255,255,255,.12)}
.phone img{display:block;width:100%;height:100%;border-radius:23px;object-fit:cover;object-position:top}
</style></head><body>
<div class="glow"></div><div class="grain"></div>
<div class="browser"><div class="bar"><i></i><i></i><i></i><span>${img.label}</span></div><img src="${file(img.shot)}" alt=""></div>
<div class="phone"><img src="${file(img.phone)}" alt=""></div>
<div class="copy">
  <span class="pill"><img src="${file('brand/logo.png')}" alt="INFA ELITE"></span>
  <h1>${img.title}</h1>
  <div class="rule"></div>
  <p class="sub">${img.sub}</p>
  <div class="foot">${img.proof ? `<span class="proof">${star}4.9 on Fiverr from 1,400+ reviews</span><span class="dot"></span>` : ''}<span class="site">infaelite.com</span></div>
</div>
</body></html>`;
}

const browser = await chromium.launch({ executablePath: CHROME, args: ['--no-sandbox', '--allow-file-access-from-files'] });
const ctx = await browser.newContext({ viewport: { width: 1200, height: 630 }, deviceScaleFactor: 1 });
for (const img of IMAGES) {
  const p = await ctx.newPage();
  const tmp = path.join(root, '.og-render.html');
  fs.writeFileSync(tmp, page(img));
  await p.goto('file://' + tmp, { waitUntil: 'load' });
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(300);
  await p.screenshot({ path: path.join(root, img.out), type: 'jpeg', quality: 88 });
  fs.unlinkSync(tmp);
  console.log(img.out, fs.statSync(path.join(root, img.out)).size);
  await p.close();
}
await browser.close();
