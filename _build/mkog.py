from PIL import Image, ImageDraw, ImageFont
W,H=1200,630
INK=(10,34,69); ACC=(99,102,241); ACC2=(139,92,246); DIM=(90,114,144); FAINT=(158,177,199)
img=Image.new('RGB',(W,H),(255,255,255)); d=ImageDraw.Draw(img)
def f(sz,bold=True):
    for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",):
        try: return ImageFont.truetype(p,sz)
        except: pass
    return ImageFont.load_default()
# faint grid, same device as the marketing hero
for x in range(0,W,64): d.line([(x,0),(x,H)],fill=(236,242,248))
for y in range(0,H,64): d.line([(0,y),(W,y)],fill=(236,242,248))
# gradient top rule
for x in range(W):
    t=x/W; d.line([(x,0),(x,8)],fill=(int(99+(139-99)*t),int(102+(92-102)*t),int(241+(246-241)*t)))
# brand mark: hub and spokes
import math
cx,cy,S=92,96,1.0
for i in range(8):
    a=math.radians(i*45-90)
    d.line([(cx,cy),(cx+22*math.cos(a),cy+22*math.sin(a))],fill=ACC2,width=3)
    nx,ny=cx+26*math.cos(a),cy+26*math.sin(a)
    d.ellipse([nx-5,ny-5,nx+5,ny+5],fill=(255,255,255),outline=ACC,width=3)
d.ellipse([cx-8,cy-8,cx+8,cy+8],fill=ACC2)
d.text((152,80),"GEO AGENCY INDEX",font=f(26),fill=INK)
d.text((70,178),"29 agencies sell",font=f(56),fill=INK)
d.text((70,246),"AI search visibility.",font=f(56),fill=INK)
d.text((70,314),"1 has done it on",font=f(56),fill=ACC)
d.text((70,382),"its own website.",font=f(56),fill=ACC)
d.line([70,478,1130,478],fill=(225,232,240),width=2)
d.text((70,506),"Eight public checks. Every score verifiable.",font=f(27,False),fill=DIM)
d.text((70,552),"Measured 14 August 2026  ·  Published by AI Syndicate, which is ranked in it",font=f(20,False),fill=FAINT)
import os; img.save(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'og.png')); print("og.png", img.size)
