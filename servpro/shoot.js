const { chromium } = require('playwright'); const path=require('path');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1920,height:1080}});
await p.goto('file://'+path.resolve('board_mock.html'));await p.evaluate(()=>document.fonts.ready);
await p.screenshot({path:'board_brand_compliant.png'});await b.close();console.log('ok');})();
