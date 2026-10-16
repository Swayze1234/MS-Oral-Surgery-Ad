  /* ================= "Set by Hand" logo intro (0.0–4.0s) =================
     Cut-paper wreath laid on a kraft table, "Oxford" stamped down, the red
     dots flicked out from under it, then we fly through the wreath into S2. */
  const NS='http://www.w3.org/2000/svg';
  const CX=500, CY=500;
  const UMBER='#46301A';
  if(!window.__logoInit){
    window.__logoInit=true;
    const mk=(tag,attrs)=>{const e=document.createElementNS(NS,tag);for(const k in attrs)e.setAttribute(k,attrs[k]);return e;};
    const wreath=s1svg.querySelector('.wreath'), wordmark=s1svg.querySelector('.wordmark');
    // bigger lockup for TV legibility
    // ---- table group: kraft annulus, disc + shadow, sprigs + shadows
    const defs=mk('defs',{}); defs.innerHTML='<filter id="dblur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur id="dblurStd" stdDeviation="30"/></filter>';
    s1svg.insertBefore(defs,s1svg.firstChild);
    const table=mk('g',{id:'table'});
    const kraft=mk('path',{id:'kraft','fill-rule':'evenodd',fill:'#C9A66B',d:`M-1200,-1200 H2200 V2200 H-1200 Z M${CX-460},${CY} a460,460 0 1,0 920,0 a460,460 0 1,0 -920,0 Z`});
    const discShadow=mk('circle',{id:'discShadow',cx:CX,cy:CY,r:460,fill:UMBER,opacity:0.28,filter:'url(#dblur)'});
    const disc=mk('circle',{id:'disc',cx:CX,cy:CY,r:460,fill:'#F5EFE4'});
    const shadows=mk('g',{id:'sprigShadows'}), sprigs=mk('g',{id:'sprigs'});
    table.append(kraft,discShadow,disc,shadows,sprigs);
    // group each sprig's stem + leaves; clone as an umber shadow
    const S=[];
    for(let s=0;s<N_SPRIGS;s++){
      const st=stems.find(e=>+e.dataset.sprig===s); const m=/M([-\d.]+),([-\d.]+)/.exec(st.getAttribute('d'));
      const g=mk('g',{class:'sprig','data-s':s}); g.appendChild(st); leaves.filter(l=>+l.dataset.sprig===s).forEach(l=>g.appendChild(l));
      const sh=g.cloneNode(true); sh.querySelectorAll('*').forEach(e=>{ if(e.getAttribute('fill')&&e.getAttribute('fill')!=='none')e.setAttribute('fill',UMBER); if(e.getAttribute('stroke'))e.setAttribute('stroke',UMBER); });
      sh.setAttribute('opacity','0.22');
      sprigs.appendChild(g); shadows.appendChild(sh);
      S.push({g,sh,bx:+m[1],by:+m[2],ang:Math.atan2(+m[2]-CY,+m[1]-CX)});
    }
    s1svg.insertBefore(table,wreath);
    // ---- lockup group: berries, dots, text layers
    const lockup=mk('g',{id:'lockup'}); s1svg.insertBefore(lockup,wreath); lockup.appendChild(wreath); // wreath now holds only berries + dots
    berries.forEach(b=>{b.__b={x:+b.getAttribute('cx'),y:+b.getAttribute('cy')};});
    dots.forEach(d=>{d.__b={x:+d.getAttribute('cx'),y:+d.getAttribute('cy')};});
    // berry clusters ordered top -> bottom
    const clusters=[]; for(let c=0;c<Math.floor(berries.length/3);c++){ const bs=berries.slice(c*3,c*3+3); const cx=bs.reduce((a,b)=>a+b.__b.x,0)/3, cy=bs.reduce((a,b)=>a+b.__b.y,0)/3; clusters.push({bs,cx,cy,key:Math.abs(((Math.atan2(cy-CY,cx-CX)+Math.PI/2+Math.PI*3)%(Math.PI*2))-Math.PI)}); }
    clusters.sort((a,b)=>b.key-a.key); clusters.forEach((c,i)=>{c.start=1.20+i*0.07;});
    // "Oxford": shadow + red under-layer + main
    const oxSh=wOx.cloneNode(true); oxSh.setAttribute('fill',UMBER); oxSh.setAttribute('opacity','0.22'); oxSh.removeAttribute('class');
    const oxRed=wOx.cloneNode(true); oxRed.setAttribute('fill','#C8463E'); oxRed.removeAttribute('class');
    const oxG=mk('g',{id:'oxG'}); oxG.append(oxSh,oxRed,wOx); wordmark.appendChild(oxG);
    // "Christmas Galleria": split into glyphs after measuring the original
    const text=wCg.textContent; const glyphs=[];
    const n=wCg.getNumberOfChars();
    for(let i=0;i<n;i++){ const ext=wCg.getExtentOfChar(i); const ch=text[i]; if(ch===' ')continue;
      const g=mk('g',{class:'glyph'}); const base={x:ext.x,y:+wCg.getAttribute('y')};
      const red=mk('text',{x:base.x+4,y:base.y+4,'font-family':'Bree Serif','font-size':'66',fill:'#C8463E'}); red.textContent=ch;
      const main=mk('text',{x:base.x,y:base.y,'font-family':'Bree Serif','font-size':'66',fill:'#E5705A'}); main.textContent=ch;
      g.append(red,main); wordmark.appendChild(g); glyphs.push({g,cx:ext.x+ext.width/2,cy:ext.y+ext.height*0.62}); }
    wCg.style.display='none';
    wordmark.remove(); lockup.appendChild(wordmark);
    // sparkles: 5 thin gold four-point stars (HTML layer)
    const star="url(\"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><path d='M50 0 C53 35 65 47 100 50 C65 53 53 65 50 100 C47 65 35 53 0 50 C35 47 47 35 50 0 Z' fill='%23D9B45B'/></svg>\")";
    sparks1.forEach((s,i)=>{ s.style.background=star; s.style.backgroundSize='contain'; s.style.width='46px'; s.style.height='46px'; s.style.opacity=0; });
    window.__L={S,clusters,glyphs,oxG,oxSh,oxRed,table,lockup,disc,discShadow,sprigs,shadows,
      pairs:[[13,14],[12,15],[11,16],[10,17],[9,0],[8,1],[7,2],[6,3],[5,4]]};
  }
  const L=window.__L;
  const dsin=(x,f,dec)=>Math.exp(-dec*x)*Math.sin(2*Math.PI*f*x);
  const exitFade = u(t,3.6,3.8,'inCubic');          // text + small pieces leave
  const tableZoom = u(t,3.6,4.0,'inCubic');          // fly through the wreath

  /* ----- 0.05–0.40 cream disc lands on the kraft table ----- */
  { const p=u(t,0.05,0.40,'outCubic'); const pb=u(t,0.05,0.45,'outBackSoft'); const op=u(t,0.05,0.13,'linear');
    const sc=1.12-0.12*p, dy=-18*(1-pb);
    L.disc.setAttribute('transform',`translate(0,${dy}) translate(${CX},${CY}) scale(${sc}) translate(${-CX},${-CY})`);
    L.disc.style.opacity=op*(1-u(t,3.65,3.95,'linear'));
    const so=26-21*p, blur=36-28*p;
    L.discShadow.setAttribute('transform',`translate(0,${so}) translate(${CX},${CY}) scale(${sc}) translate(${-CX},${-CY})`);
    L.discShadow.style.opacity=0.28*op*(1-u(t,3.65,3.95,'linear'));
    document.getElementById('dblurStd').setAttribute('stdDeviation',Math.max(1,blur)); }

  /* ----- 0.30–1.50 sprigs set down one pair at a time, 12 o'clock downward ----- */
  L.pairs.forEach((pair,pi)=>pair.forEach((s,j)=>{ const d=L.S[s]; const t0=0.30+pi*0.09+j*0.04;
    const op=u(t,t0,t0+0.06,'linear'); const sc=1.22-0.22*u(t,t0,t0+0.38,'outCubic'); const dy=-28*(1-u(t,t0,t0+0.40,'outBackSoft'));
    const rot=((pi+j)%2?10:-10)*(1-u(t,t0,t0+0.45,'outBack'));
    const sway = 1.2*Math.sin(2*Math.PI*0.5*t + s*0.7) * u(t,2.4,2.7,'linear') * (1-u(t,3.6,3.7,'linear'));
    const tr=`translate(0,${dy}) translate(${d.bx},${d.by}) rotate(${rot+sway}) scale(${sc}) translate(${-d.bx},${-d.by})`;
    d.g.setAttribute('transform',tr); d.g.style.opacity=op*(1-u(t,3.85,4.0,'linear'));
    const sp=u(t,t0,t0+0.38,'outCubic'); const ox=10-8*sp, oy=18-14*sp;
    d.sh.setAttribute('transform',`translate(${ox},${oy}) `+tr); d.sh.style.opacity=0.22*op*(1-u(t,3.85,4.0,'linear')); }));

  /* ----- 1.20–1.90 berries pop onto their sprigs; a gold flash per cluster ----- */
  L.clusters.forEach((c,ci)=>c.bs.forEach((b,k)=>{ const t0=c.start+k*0.03; const p=u(t,t0,t0+0.28,'outBack');
    const s=t>=t0? Math.max(0.0001,p*1.0) : 0.0001; const q=b.__b;
    b.setAttribute('transform',`translate(${q.x},${q.y}) scale(${s}) translate(${-q.x},${-q.y})`); b.style.opacity=t>=t0?1:0; }));
  /* ----- 1.72–2.15 red dots flicked out from under the stamp to their ring spots ----- */
  dots.forEach((d,i)=>{ const t0=1.72+((i*7)%26)*0.012; const p=u(t,t0,t0+0.38,'outCubic'); const sb=u(t,t0,t0+0.38,'outBack');
    const q=d.__b; const x=500+(q.x-500)*p, y=560+(q.y-560)*p; const s=t>=t0?Math.max(0.0001,sb):0.0001;
    d.setAttribute('transform',`translate(${x-q.x},${y-q.y}) translate(${q.x},${q.y}) scale(${s}) translate(${-q.x},${-q.y})`); d.style.opacity=t>=t0?1:0; });

  /* ----- 1.60–2.05 "Oxford" set down from above, then stamped (one decayed squash) ----- */
  { const t0=1.60; const op=u(t,t0,t0+0.06,'linear'); const arr=u(t,t0,t0+0.12,'outCubic'); const arrB=u(t,t0,t0+0.12,'outBackSoft');
    let sx=1.30-0.30*arr, sy=sx; const dy=-30*(1-arrB); const rot=-3*(1-arr);
    if(t>=1.72 && t<2.05){ const q=dsin(t-1.72,2.6,6.5); sx=1+0.12*q*1.0; sy=1-0.10*q*1.0; }
    if(t>=2.05){ sx=1; sy=1; }
    const ex=1-0.1*exitFade;
    L.oxG.setAttribute('transform',`translate(0,${dy}) translate(500,440) scale(${sx*ex},${sy*ex}) rotate(${rot}) translate(-500,-440)`);
    L.oxG.style.opacity=op*(1-exitFade);
    const so=u(t,t0,t0+0.14,'outCubic'); L.oxSh.setAttribute('transform',`translate(${12-8*so},${20-15*so})`); L.oxRed.setAttribute('transform','translate(5,5)'); }
  /* table thump on contact (<=1.5%, 0.25s) */
  { let th=1; if(t>=1.72&&t<1.97){ const x=t-1.72; th = x<0.08 ? 1-0.015*u(x,0,0.08,'outCubic') : 0.985+0.015*u(x,0.08,0.25,'outBackSoft'); }
    const z=1+2.6*tableZoom, tw_=6*tableZoom;
    L.table.setAttribute('transform',`translate(${CX},${CY}) rotate(${tw_}) scale(${z*th}) translate(${-CX},${-CY})`); }

  /* ----- 1.95–2.55 "Christmas Galleria" set in glyph by glyph ----- */
  L.glyphs.forEach((g,i)=>{ const t0=1.95+i*0.02; const p=u(t,t0,t0+0.22,'outCubic'); const pb=u(t,t0,t0+0.22,'outBackSoft');
    const s=(0.6+0.4*pb)*(1-0.1*exitFade); const dy=10*(1-p);
    g.g.setAttribute('transform',`translate(0,${dy}) translate(${g.cx},${g.cy}) scale(${Math.max(0.0001,s)}) translate(${-g.cx},${-g.cy})`); g.g.style.opacity=p*(1-exitFade); });
  /* berries + dots leave with the text */
  L.lockup.querySelector('.wreath').style.opacity=1-exitFade;

  /* ----- sparkles: 4 cluster flashes (1.2–1.9) + 5 foil stars twinkling through the hold ----- */
  const U=1.12, px=x=>960+(x-500)*U, py=y=>540+(y-500)*U;   // svg units -> page px (svg is 1120px wide)
  sparks1.forEach((s,i)=>{ let op=0,sc=0,rot=0,x=0,y=0;
    if(i<4){ const c=L.clusters[i*2]; if(c){ const t0=c.start+0.16; const p=clamp((t-t0)/0.22,0,1); if(t>=t0&&t<=t0+0.22){op=1;sc=Math.sin(p*Math.PI)*0.9;rot=p*40;} x=px(c.cx); y=py(c.cy);} }
    else if(i<9){ const k=i-4; const spots=[[500+425*Math.cos(-Math.PI/3),500+425*Math.sin(-Math.PI/3)],[500+425*Math.cos(Math.PI/6),500+425*Math.sin(Math.PI/6)],[500+425*Math.cos(2*Math.PI/3),500+425*Math.sin(2*Math.PI/3)],[500+425*Math.cos(-5*Math.PI/6),500+425*Math.sin(-5*Math.PI/6)],[735,392]];
      x=px(spots[k][0]); y=py(spots[k][1]); const t0=2.40+k*0.15; const up=u(t,t0,t0+0.2,'outCubic'); const ph=k*1.1;
      const tw_=0.45+0.55*Math.sin(2*Math.PI*(1.3*t)+ph); op=up*tw_*(1-exitFade); sc=(0.85+0.15*Math.sin(2*Math.PI*(1.3*t)+ph))*up; rot=30*u(t,2.4,3.6,'linear'); }
    s.style.left=(x-23)+'px'; s.style.top=(y-23)+'px'; s.style.opacity=op; s.style.transform=`scale(${sc}) rotate(${rot}deg)`; });
