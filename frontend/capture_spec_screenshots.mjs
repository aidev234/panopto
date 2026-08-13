import { spawn } from 'node:child_process';
import fs from 'node:fs/promises';
import path from 'node:path';
import puppeteer from 'puppeteer';

const root = path.resolve('.');
const output = path.join(root, 'docs', 'actual-poc-screenshots');
const port = 8042;
await fs.mkdir(output, { recursive: true });

const server = spawn('.venv/bin/python', ['-c', `from frontend.server import run; run(port=${port})`], {
  cwd: root, stdio: ['ignore', 'pipe', 'pipe'],
});
let serverError = '';
server.stderr.on('data', (data) => { serverError += data.toString(); });

async function ready() {
  for (let i = 0; i < 60; i += 1) {
    try {
      const response = await fetch(`http://127.0.0.1:${port}/api/cases`);
      if (response.ok) return;
    } catch (_) {}
    await new Promise((resolve) => setTimeout(resolve, 250));
  }
  throw new Error(`POC server did not start. ${serverError}`);
}

try {
  await ready();
  const created = await fetch(`http://127.0.0.1:${port}/api/cases`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      case_name: 'Demo case — Pep Mangione', status: 'Under Investigation',
      threat_level: 'Unassessed', data_retention_period: '3 months',
      known_location: 'Not recorded',
    }),
  }).then((r) => r.json());
  const browser = await puppeteer.launch({ headless: true, args: ['--no-sandbox', '--disable-setuid-sandbox'], defaultViewport: { width: 1600, height: 1000, deviceScaleFactor: 1 } });
  const page = await browser.newPage();
  await page.goto(`http://127.0.0.1:${port}/`, { waitUntil: 'networkidle0' });
  await page.waitForSelector('.case-tile');
  await page.screenshot({ path: path.join(output, '01-case-management.png'), fullPage: true });
  await page.click(`[data-case-id="${created.case_id}"]`);
  await page.waitForSelector('#dashboardPanel:not(.hidden)');
  await page.screenshot({ path: path.join(output, '02-case-dashboard.png'), fullPage: true });
  await page.click('#newCollectionBtn');
  await page.waitForSelector('#setupModal:not(.hidden)');
  await page.click('#modeReconBtn');
  await page.waitForSelector('#reconForm:not(.hidden)');
  const selectorInput = await page.$('#reconSelectorsList input');
  if (selectorInput) await selectorInput.type('lnmangione');
  await page.screenshot({ path: path.join(output, '03-recon-setup.png'), fullPage: true });
  await page.click('#closeSetupBtn');
  await page.evaluate(() => {
    const modal = document.querySelector('#setupModal');
    modal?.classList.add('hidden');
    modal?.setAttribute('aria-hidden', 'true');
  });
  await page.click('#openCaseNotesTopBtn');
  await page.waitForSelector('#caseNotesModal:not(.hidden)');
  await page.$eval('#caseNotesNameInput', (input) => { input.value = 'Pep Mangione'; input.dispatchEvent(new Event('input', { bubbles: true })); });
  await page.$eval('#caseNotesSelectorUsernamesInput', (input) => { input.value = 'lnmangione'; input.dispatchEvent(new Event('input', { bubbles: true })); });
  await page.screenshot({ path: path.join(output, '04-case-file.png'), fullPage: true });
  await browser.close();
  process.stdout.write(`${output}\n`);
} finally {
  server.kill('SIGTERM');
}
