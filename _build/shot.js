const {chromium}=require('playwright');
(async()=>{
const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});
const shots=[
 ['/', 'shot-index-top.png', false],
 ['/', 'shot-index-full.png', true],
 ['/agency/ai-syndicate','shot-profile-aisyndicate.png',true],
 ['/agency/webfx','shot-profile-webfx.png',true],
 ['/findings','shot-findings.png',true],
 ['/methodology','shot-methodology.png',true],
 ['/about','shot-about.png',true],
];
for(const [p,file,full] of shots){
  const pg=await b.newPage({viewport:{width:1440,height:960},deviceScaleFactor:2});
  const errs=[]; pg.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
  pg.on('pageerror',e=>errs.push(String(e)));
  const r=await pg.goto('http://127.0.0.1:8899'+(p==='/'?'/index.html':p+'.html'),{waitUntil:'networkidle'});
  await pg.screenshot({path:'screenshots/'+file,fullPage:full});
  const h=await pg.evaluate(()=>({t:document.title,h1:document.querySelectorAll('h1').length,ld:document.querySelectorAll('script[type="application/ld+json"]').length,ow:document.documentElement.scrollWidth,cw:document.documentElement.clientWidth}));
  console.log(p.padEnd(30), r.status(), 'title:',h.t.slice(0,40),'| h1:',h.h1,'| ld:',h.ld,'| overflow:',h.ow>h.cw?('YES '+h.ow+'>'+h.cw):'no','| jsErrors:',errs.length);
  await pg.close();
}
// mobile
const m=await b.newPage({viewport:{width:390,height:844},deviceScaleFactor:2,isMobile:true});
await m.goto('http://127.0.0.1:8899/index.html',{waitUntil:'networkidle'});
await m.screenshot({path:'screenshots/shot-mobile.png',fullPage:false});
const mo=await m.evaluate(()=>document.documentElement.scrollWidth>document.documentElement.clientWidth);
console.log('mobile 390px overflow:', mo?'YES':'no');
await b.close();
})();
