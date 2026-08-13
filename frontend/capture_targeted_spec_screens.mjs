import {spawn} from 'node:child_process'; import fs from 'node:fs/promises'; import path from 'node:path'; import puppeteer from 'puppeteer';
const root=path.resolve('.'), out=path.join(root,'docs','poc-platform-screenshots'), port=8045, base=`http://127.0.0.1:${port}`;
await fs.mkdir(out,{recursive:true}); const server=spawn('.venv/bin/python',['-c',`from frontend.server import run; run(port=${port})`],{cwd:root,stdio:'ignore'});
const sleep=(n)=>new Promise(r=>setTimeout(r,n));
async function get(p,o){const r=await fetch(base+p,o);if(!r.ok)throw Error(p);return r.json()}
try { for(let i=0;i<80;i++){try{await get('/api/cases');break}catch{await sleep(200)}}
 let rows=(await get('/api/cases')).cases||[]; let c=rows.filter(x=>Number(x.post_count||0)>0)[0]; if(!c){await get('/api/cases/demo/vip-threat',{method:'POST'});rows=(await get('/api/cases')).cases||[];c=rows.filter(x=>Number(x.post_count||0)>0)[0]}
 const b=await puppeteer.launch({headless:true,args:['--no-sandbox'],defaultViewport:{width:1600,height:1000}}), p=await b.newPage();
 await p.goto(base,{waitUntil:'networkidle0'});await p.waitForSelector('.case-tile');await p.evaluate(id=>document.querySelector(`[data-case-id="${id}"]`)?.click(),c.case_id);await p.waitForSelector('#dashboardPanel:not(.hidden)');await sleep(500);
 async function click(sel){await p.evaluate(s=>document.querySelector(s)?.click(),sel);await sleep(250)}
 await click('#openCaseNotesTopBtn'); await p.waitForSelector('#caseNotesModal:not(.hidden)'); await p.screenshot({path:path.join(out,'11-case-file.png'),fullPage:true});
 await click('#caseNotesEvidencePopoutBtn'); await p.screenshot({path:path.join(out,'12-case-file-evidence.png'),fullPage:true});
 await click('#caseNotesCloseBtn'); await click('#newCollectionBtn'); await p.screenshot({path:path.join(out,'13-operation-chooser.png'),fullPage:true});
 await click('#modeCollectionBtn'); await p.screenshot({path:path.join(out,'14-collection.png'),fullPage:true});
 await click('#closeSetupBtn'); await p.evaluate(()=>document.querySelector('#setupModal')?.classList.add('hidden')); await p.evaluate(()=>document.querySelector('#openManualInsertBtn')?.click()); await sleep(250);await p.screenshot({path:path.join(out,'15-manual-content.png'),fullPage:true});
 await b.close();
} finally {server.kill('SIGTERM');setTimeout(()=>process.exit(0),200)}
