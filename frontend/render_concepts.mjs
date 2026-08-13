import fs from 'node:fs/promises';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import puppeteer from 'puppeteer';

const root = path.resolve('frontend/static/concepts');
const outputDir = path.join(root, 'screenshots');
const concepts = [
  'mantine-case-workspace.svg',
  'mantine-active-case-dashboard.svg',
  'mantine-case-notes-settings.svg',
];

await fs.mkdir(outputDir, { recursive: true });

const browser = await puppeteer.launch({
  headless: true,
  defaultViewport: { width: 1600, height: 1000, deviceScaleFactor: 1.5 },
  args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage'],
});

try {
  const page = await browser.newPage();

  for (const concept of concepts) {
    const inputPath = path.join(root, concept);
    const outputPath = path.join(outputDir, concept.replace(/\.svg$/, '.png'));
    await page.goto(pathToFileURL(inputPath).href, { waitUntil: 'networkidle0' });
    await page.screenshot({ path: outputPath });
    process.stdout.write(`${path.relative(process.cwd(), outputPath)}\n`);
  }
} finally {
  await browser.close();
}
