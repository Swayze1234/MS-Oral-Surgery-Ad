from PIL import Image
import numpy as np

def make_cover(src, out, W=1500, H=1000,
               left_a=0.80, left_span=0.62,
               top_a=0.50, top_span=0.55,
               base=0.14, tint=(8,18,38)):
    im = Image.open(src).convert("RGB")
    # crop to 3:2 (center)
    w,h = im.size
    target = W/H
    if w/h > target:
        nw = int(h*target); x0=(w-nw)//2
        im = im.crop((x0,0,x0+nw,h))
    else:
        nh = int(w/target); y0=(h-nh)//2
        im = im.crop((0,y0,w,y0+nh))
    im = im.resize((W,H), Image.LANCZOS)
    arr = np.asarray(im).astype(float)
    xs = np.linspace(0,1,W)[None,:]
    ys = np.linspace(0,1,H)[:,None]
    aL = np.clip(left_a*(1 - xs/left_span),0,1)      # dark on left
    aT = np.clip(top_a*(1 - ys/top_span),0,1)        # dark on top
    a = 1-(1-aL)*(1-aT)                              # combine
    a = np.clip(a + base, 0, 1)                       # overall base darken
    a = a[:,:,None]
    tint = np.array(tint,float)[None,None,:]
    out_arr = arr*(1-a) + tint*a
    Image.fromarray(out_arr.astype('uint8')).save(out, quality=92)

if __name__=="__main__":
    import os
    base=os.path.dirname(os.path.abspath(__file__))
    src=os.path.join(base,"source")
    # Cover: Tupelo City Hall with a navy legibility scrim (dark top-left for the headline)
    make_cover(os.path.join(src,"tupelo_city_hall_cover.jpg"),
               os.path.join(base,"cover.jpg"),
               left_a=0.80, left_span=0.60, top_a=0.40, top_span=0.66, base=0.12)
    print("wrote cover.jpg")
    # Back page: downtown Tupelo, no scrim (no text overlays it)
    make_cover(os.path.join(src,"tupelo_downtown_backpage.jpg"),
               os.path.join(base,"back.jpg"),
               left_a=0, top_a=0, base=0)
    print("wrote back.jpg")
