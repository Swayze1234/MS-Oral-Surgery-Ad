  /* ================= "Set by Hand" logo intro, wordmark edition (0.0–4.0s) =================
     Cream card lands on a kraft table; OXFORD letters are set down one by one, "Christmas"
     is written on with a gold pen tip, the tree pops onto the i, GALLERIA letters are set,
     a short hold with foil-star twinkles, then the card grows to hand off to scene 2. */
  if(!window.__logoInit){
    window.__logoInit=true;
    const star="url(\"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><path d='M50 0 C53 35 65 47 100 50 C65 53 53 65 50 100 C47 65 35 53 0 50 C35 47 47 35 50 0 Z' fill='%23D9B45B'/></svg>\")";
    sparks1.forEach(s=>{ s.style.background=star; s.style.backgroundSize='contain'; s.style.width='46px'; s.style.height='46px'; s.style.opacity=0; });
  }
  const dsin=(x,f,dec)=>Math.exp(-dec*x)*Math.sin(2*Math.PI*f*x);
  const exitFade=u(t,3.66,3.94,'inCubic');          // logo pieces
  const tableZoom=u(t,3.55,4.0,'inCubic');          // card + kraft grow toward the viewer
  const LS=1.25, LX=394.5, LY=291;                       // #logo scale + offset: native px -> screen px
  const toScreen=(x,y)=>[960+(x-452.5)*LS, 540+(y-199)*LS];

  /* ----- 0.05–0.40 card lands on the table ----- */
  { const p=u(t,0.05,0.40,'outCubic'); const pb=u(t,0.05,0.45,'outBackSoft'); const op=u(t,0.05,0.13,'linear');
    const sc=1.12-0.12*p, dy=-18*(1-pb);
    const card=document.getElementById('card'), sh=document.getElementById('cardShadow');
    const leave=u(t,3.68,3.97,'inCubic');
    card.style.transform=`translateY(${dy}px) scale(${sc})`; card.style.opacity=op*(1-leave);
    sh.style.transform=`translateY(${dy+26-21*p}px) scale(${sc})`; sh.style.opacity=0.28*op*(1-leave); sh.style.filter=`blur(${Math.max(2,36-28*p)}px)`;
    document.getElementById('kraft').style.opacity=1-leave;
    const z=1+1.6*tableZoom; document.getElementById('table').style.transform=`scale(${z})`; }

  /* ----- stamp helper: piece set down from above, shadow tightens in sync ----- */
  function stamp(name,t0,dur,rot){ const P=PIECES[name]; if(!P) return;
    const op=u(t,t0,t0+0.06,'linear'); const sc=1.22-0.22*u(t,t0,t0+dur*0.9,'outCubic'); const dy=-28*(1-u(t,t0,t0+dur*0.95,'outBackSoft'));
    const r=rot*(1-u(t,t0,t0+dur,'outBack')); const ex=1-0.1*exitFade;
    P.el.style.transform=`translateY(${dy}px) rotate(${r}deg) scale(${sc*ex})`; P.el.style.opacity=op*(1-exitFade);
    const sp=u(t,t0,t0+dur*0.9,'outCubic'); const ox=10-8*sp, oy=18-14*sp;
    P.sh.style.transform=`translate(${ox}px,${oy+dy}px) rotate(${r}deg) scale(${sc*ex})`; P.sh.style.opacity=0.22*op*(1-exitFade); }

  /* ----- 0.35–1.17 OXFORD, one letter at a time ----- */
  OX.forEach((n,k)=>stamp(n,0.35+k*0.08,0.42,(k%2?8:-8)));

  /* ----- 0.85–1.95 "Christmas" written on, left to right, pen tip leads the edge ----- */
  { const P=PIECES.script; const p=u(t,0.85,1.95,'inOutCubic'); const ex=1-0.1*exitFade;
    const lead=p*112, tail=Math.max(0,p*112-12);   // slanted edge, percentages of the piece width
    const clip=`polygon(0 0, ${lead}% 0, ${tail}% 100%, 0 100%)`;
    P.el.style.clipPath=clip; P.sh.style.clipPath=clip;
    P.el.style.opacity=(t>=0.85?1:0)*(1-exitFade); P.el.style.transform=`scale(${ex})`;
    P.sh.style.opacity=(t>=0.85?0.2:0)*(1-exitFade); P.sh.style.transform=`translate(4px,6px) scale(${ex})`;
    // pen-tip sparkle (sparks1[0]) rides the reveal edge: baseline rises to the right
    const s0=sparks1[0]; if(t>=0.85&&t<=2.0){ const px=P.x+Math.min(1,p*1.05)*P.w, py=P.y+P.h*(0.72-0.42*p); const [sx,sy]=toScreen(px,py);
      s0.style.left=(sx-23)+'px'; s0.style.top=(sy-23)+'px'; s0.style.opacity=1-u(t,1.9,2.0,'linear'); s0.style.transform=`scale(${0.8+0.3*Math.sin(t*40)}) rotate(${t*300}deg)`; } else { s0.style.opacity=0; } }

  /* ----- 1.95–2.25 tree pops onto the i; star flash ----- */
  { const P=PIECES.tree; const p=u(t,1.95,2.25,'outBack'); const ex=1-0.1*exitFade; const s=(t>=1.95?Math.max(0.0001,p):0.0001);
    P.el.style.transform=`scale(${s*ex})`; P.el.style.opacity=(t>=1.95?1:0)*(1-exitFade);
    P.sh.style.transform=`translate(${6-4*p}px,${10-7*p}px) scale(${s*ex})`; P.sh.style.opacity=(t>=1.95?0.22:0)*(1-exitFade);
    const f=sparks1[1]; const [sx,sy]=toScreen(P.x+P.w/2,P.y+4); const q=clamp((t-2.12)/0.26,0,1);
    f.style.left=(sx-23)+'px'; f.style.top=(sy-23)+'px'; f.style.opacity=(t>=2.12&&t<=2.38)?1:0; f.style.transform=`scale(${Math.sin(q*Math.PI)*1.1}) rotate(${q*45}deg)`; }

  /* ----- 1.95–2.62 GALLERIA letters set in ----- */
  GA.forEach((n,k)=>stamp(n,1.95+k*0.05,0.32,(k%2?-6:6)));

  /* ----- 2.4–3.6 foil-star twinkles in the gaps (never on the letters) ----- */
  { const spots=[[230,20],[700,15],[120,330],[880,330],[300,392]]; // native coords around the wordmark
    spots.forEach(([x,y],k)=>{ const s=sparks1[2+k]; const [sx,sy]=toScreen(x,y); const t0=2.40+k*0.15; const up=u(t,t0,t0+0.2,'outCubic'); const ph=k*1.1;
      const tw_=0.45+0.55*Math.sin(2*Math.PI*1.3*t+ph); s.style.left=(sx-23)+'px'; s.style.top=(sy-23)+'px';
      s.style.opacity=up*tw_*(1-exitFade); s.style.transform=`scale(${(0.85+0.15*Math.sin(2*Math.PI*1.3*t+ph))*up}) rotate(${30*u(t,2.4,3.6,'linear')}deg)`; });
    for(let i=7;i<sparks1.length;i++) sparks1[i].style.opacity=0; }
