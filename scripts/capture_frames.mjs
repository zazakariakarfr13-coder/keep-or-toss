// Capture an animated HTML pin frame by frame with exact timing.
// Usage: node scripts/capture_frames.mjs <page.html> <out_dir> <seconds> <fps>
// Uses the Playwright install that ships with the kaz-map-animation skill.
import { createRequire } from "node:module";
import { mkdirSync } from "node:fs";
import { pathToFileURL } from "node:url";
import os from "node:os";
import path from "node:path";

const require = createRequire(path.join(os.homedir(), ".claude/skills/kaz-map-animation/package.json"));
const { chromium } = require("playwright");

const [, , page_html, outDir, seconds = "8", fps = "30"] = process.argv;
mkdirSync(outDir, { recursive: true });
const total = Math.round(Number(seconds) * Number(fps));

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1000, height: 1500 }, deviceScaleFactor: 1 });
await page.goto(pathToFileURL(path.resolve(page_html)).href, { waitUntil: "networkidle" });
await page.evaluate(() => document.fonts.ready);
await page.evaluate(() => document.getAnimations().forEach((a) => a.pause()));

for (let i = 0; i < total; i++) {
  const t = (i * 1000) / Number(fps);
  await page.evaluate((ms) => document.getAnimations().forEach((a) => { a.currentTime = ms; }), t);
  await page.screenshot({ path: path.join(outDir, `${String(i).padStart(4, "0")}.png`) });
}
await browser.close();
console.log(`captured ${total} frames`);
