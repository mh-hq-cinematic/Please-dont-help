const { chromium } = require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1280,height:720}});
p.on('pageerror',e=>console.log('ERR',e.message));
await p.goto('file://'+process.cwd()+'/scene.html');await p.waitForTimeout(500);
for(const t of process.argv.slice(2)){await p.evaluate(t=>render(+t),t);await p.waitForTimeout(80);await p.screenshot({path:`snap-${t}.png`});}
await b.close();})();
