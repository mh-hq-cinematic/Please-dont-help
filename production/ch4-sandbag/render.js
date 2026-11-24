const { chromium } = require('playwright'); const { spawn } = require('child_process');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1280,height:720},deviceScaleFactor:1.5});
await p.goto('file://'+process.cwd()+'/scene.html');await p.waitForTimeout(500);
const ff=spawn('ffmpeg',['-y','-v','error','-f','image2pipe','-framerate','24','-c:v','png','-i','-','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','video.mp4']);
const N=101*24;
for(let i=0;i<N;i++){await p.evaluate(t=>render(t),i/24);const buf=await p.screenshot({type:'png'});
 if(!ff.stdin.write(buf)) await new Promise(r=>ff.stdin.once('drain',r)); if(i%240==0) console.log('frame',i);}
ff.stdin.end(); await new Promise(r=>ff.on('close',r)); await b.close(); console.log('done');})();
