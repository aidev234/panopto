import { spawn } from 'node:child_process';
import fs from 'node:fs/promises';
import path from 'node:path';
import puppeteer from 'puppeteer';

const root = path.resolve('.');
const out = path.join(root, 'docs', 'poc-platform-screenshots');
const port = 8044;
await fs.mkdir(out, { recursive: true });
const server = spawn('.venv/bin/python', ['-c', `from frontend.server import run; run(port=${port})`], { cwd: root, stdio: 'ignore' });
const base = `http://127.0.0.1:${port}`;
const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
async function api(pathname, options) { const r = await fetch(`${base}${pathname}`, options); if (!r.ok) throw new Error(`${pathname}: ${r.status}`); return r.json(); }
async function ready() { for (let i=0;i<80;i+=1) { try { await api('/api/cases'); return; } catch (_) { await sleep(200); } } throw new Error('POC server did not start'); }

try {
  await ready();
  let cases = (await api('/api/cases')).cases || [];
  let target = cases.filter((x) => Number(x.post_count || 0) > 0).sort((a,b) => Number(b.post_count||0)-Number(a.post_count||0))[0];
  if (!target) { target = await api('/api/cases/demo/vip-threat', { method:'POST' }); cases = (await api('/api/cases')).cases || []; target = cases.find((x) => x.case_id === target.case_id) || target; }
  const browser = await puppeteer.launch({headless:true,args:['--no-sandbox','--disable-setuid-sandbox'],defaultViewport:{width:1600,height:1000,deviceScaleFactor:1}});
  const page = await browser.newPage();
  const snap = (name) => page.screenshot({path:path.join(out, name),fullPage:true});
  await page.goto(`${base}/`, {waitUntil:'networkidle0'});
  await page.waitForSelector('.case-tile');
  await snap('01-case-management.png');
  await page.click(`[data-case-id="${target.case_id}"]`);
  await page.waitForSelector('#dashboardPanel:not(.hidden)');
  await sleep(600);
  await snap('02-posts-dashboard.png');
  await page.click('#filterToggleBtn'); await sleep(200); await snap('03-post-filters.png');
  await page.click('#insightsTabSignals'); await sleep(200); await snap('04-threat-assessment.png');
  await page.click('#viewWorkflowBtn'); await sleep(200); await snap('05-case-overview.png');
  await page.click('#viewGuideBtn'); await sleep(200); await snap('06-investigation-guide.png');
  await page.click('#viewFootprintBtn'); await sleep(350); await snap('07-profiles.png');
  await page.click('#viewPatternLifeBtn'); await sleep(350); await snap('08-pattern-of-life.png');
  await page.click('#viewTimelineBtn'); await sleep(350); await snap('09-timeline.png');
  await page.click('#viewEntityGraphBtn'); await sleep(350); await snap('10-entity-graph.png');
  await page.click('#openCaseNotesTopBtn'); await sleep(300); await snap('11-case-file.png');
  await page.click('#caseNotesCloseBtn'); await sleep(200);
  await page.click('#newCollectionBtn'); await sleep(200); await snap('12-operation-chooser.png');
  await page.click('#modeReconBtn'); await sleep(200); await snap('13-recon.png');
  await page.click('#closeSetupBtn'); await sleep(100);
  await page.evaluate(() => document.querySelector('#setupModal')?.classList.add('hidden'));
  await page.evaluate(() => document.querySelector('#modeCollectionBtn')?.click()); await sleep(200); await snap('14-collection.png');
  await page.click('#closeSetupBtn'); await page.evaluate(() => document.querySelector('#setupModal')?.classList.add('hidden'));
  await page.evaluate(() => document.querySelector('#openManualInsertBtn')?.click()); await sleep(200); await snap('15-manual-content.png');
  await browser.close();
  process.stdout.write(`${out}\n`);
} finally {
  server.kill('SIGTERM');
  setTimeout(() => process.exit(0), 250);
}
