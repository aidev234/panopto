import {spawn} from 'node:child_process';
import path from 'node:path';
import puppeteer from 'puppeteer';
const root=path.resolve('.'),port=8060,base=`http://127.0.0.1:${port}`;
const server=spawn('.venv/bin/python',['-c',`from frontend.server import run; run(port=${port})`],{cwd:root,stdio:['ignore','pipe','pipe']});
server.stdout.on('data',d=>process.stderr.write(d));server.stderr.on('data',d=>process.stderr.write(d));
const pause=(n)=>new Promise(r=>setTimeout(r,n));
async function request(url,opts){return fetch(url,{...opts,signal:AbortSignal.timeout(1500)})}
try {
 for(let i=0;i<40;i++){try{const r=await request(`${base}/api/cases`);if(r.ok)break}catch{}await pause(200)}
 let rows=(await (await request(`${base}/api/cases`)).json()).cases||[];
 let target=rows.find(x=>Number(x.post_count||0)>0);
 if(!target){await request(`${base}/api/cases/demo/vip-threat`,{method:'POST'});rows=(await (await request(`${base}/api/cases`)).json()).cases||[];target=rows.find(x=>Number(x.post_count||0)>0)}
 const browser=await puppeteer.launch({headless:true,args:['--no-sandbox'],defaultViewport:{width:1600,height:1000}});const page=await browser.newPage();
 await page.goto(base,{waitUntil:'domcontentloaded',timeout:10000});await page.waitForSelector('.case-tile',{timeout:10000});
 await page.evaluate(id=>document.querySelector(`[data-case-id="${id}"]`)?.click(),target.case_id);await page.waitForSelector('#dashboardPanel:not(.hidden)',{timeout:10000});await pause(750);
 await page.evaluate(()=>document.querySelector('#openCaseNotesTopBtn')?.click());await page.waitForSelector('#caseNotesModal:not(.hidden)',{timeout:10000});
 const card=await page.$('.case-notes-card');
 await card.screenshot({path:path.join(root,'docs/poc-platform-screenshots/11-case-notes-expanded.png')});
 await page.evaluate(()=>document.querySelector('#caseNotesEvidencePopoutBtn')?.click());await pause(200);
 await card.screenshot({path:path.join(root,'docs/poc-platform-screenshots/12-case-notes-collapsed.png')});
 await page.evaluate(()=>document.querySelector('[data-case-notes-section-panel="selectors"]')?.scrollIntoView({block:'center'}));await pause(150);
 const selectors=await page.$('[data-case-notes-section-panel="selectors"]');
 await selectors.screenshot({path:path.join(root,'docs/poc-platform-screenshots/13-selector-corroboration.png')});
 await page.evaluate(()=>document.querySelector('#caseNotesEvidenceSection')?.scrollIntoView({block:'center'}));await pause(150);
 const evidence=await page.$('#caseNotesEvidenceSection');
 await evidence.screenshot({path:path.join(root,'docs/poc-platform-screenshots/14-evidence-capture.png')});
 await browser.close();
} finally {server.kill('SIGTERM');setTimeout(()=>process.exit(0),150)}
