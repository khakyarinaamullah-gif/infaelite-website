// Makes the smaller copies of the large pictures that the pages offer through srcset.
// The originals in assets/ stay untouched; every copy is written next to its original as NAME-<width>.webp
// (and NAME-<width>.avif / NAME.avif for the hero portrait).
//
//   npm i --no-save sharp && node tools/responsive-images.mjs
//
// Re-run it after replacing any of the originals listed below. build.py picks the copies up automatically.
import { createRequire } from 'node:module';
import path from 'node:path';
import fs from 'node:fs';
const require = createRequire(import.meta.url);
const sharp = require('sharp');
const dir = path.resolve(path.dirname(new URL(import.meta.url).pathname), '../assets');

const JOBS = [
  // name, widths for WebP copies, WebP quality, AVIF widths (the full width included), AVIF quality
  ['hero-portrait', [480, 720], 80, [480, 720, 975], 60],
  ['veliora-desktop', [600, 900], 70], ['werk-desktop', [600, 900], 70], ['hasi-desktop', [600, 900], 70], ['tenton-desktop', [600, 900], 70],
  ['veliora-mobile', [200], 70], ['werk-mobile', [200], 70], ['tenton-mobile', [200], 70],
  ['cover-veliora', [600, 900], 78], ['cover-hasi', [600, 900], 78], ['cover-werk', [600, 900], 78],
];

for (const [name, widths, q, avif = [], aq = 60] of JOBS) {
  const src = path.join(dir, name + '.webp');
  const { width } = await sharp(src).metadata();
  for (const w of widths) {
    if (w >= width) continue;
    const out = path.join(dir, `${name}-${w}.webp`);
    await sharp(src).resize({ width: w }).webp({ quality: q, effort: 6 }).toFile(out);
    console.log(path.basename(out), fs.statSync(out).size);
  }
  for (const w of avif) {
    const out = path.join(dir, w >= width ? `${name}.avif` : `${name}-${w}.avif`);
    await sharp(src).resize({ width: Math.min(w, width) }).avif({ quality: aq, effort: 6 }).toFile(out);
    console.log(path.basename(out), fs.statSync(out).size);
  }
}
