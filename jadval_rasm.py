# -*- coding: utf-8 -*-
"""Agentlar haftalik hudud jadvali: ma'lumot + rasm chizish."""
import io
import os
from PIL import Image, ImageDraw, ImageFont

KUNLAR = ["Dushanba", "Seshanba", "Chorshanba", "Payshanba", "Juma", "Shanba", "Yakshanba"]
AGENTLAR = ["Abduqodir aka", "Ibrohimjon aka", "Abdumalik aka", "Atxamjon aka", "Abbos aka", "Davronjon aka", "Abdulloh aka"]

# Guruhlar: har bir guruhga alohida rasm + matn yuboriladi
GURUHLAR = [
    ("SUXOY", ["Abduqodir aka", "Abdumalik aka"]),
    ("PENO PLAST", ["Ibrohimjon aka", "Atxamjon aka", "Abbos aka", "Davronjon aka", "Abdulloh aka"]),
]

REGION = {
 "Abduqodir aka": {"Dushanba":"Dang'ara, Oqjar, G'urumsaroy","Seshanba":"Pop, To'raqo'rg'on, Jomashuy","Chorshanba":"Tojikiston","Payshanba":"Uchko'prik, Buvayda, Sariqo'rg'on","Shanba":"Goriski, Beshariq, Yaypan","Yakshanba":"Shahar"},
 "Ibrohimjon aka": {"Dushanba":"Ofisda (majlis)","Seshanba":"Rapqon, Goriski, Beshariq, Yaypan","Chorshanba":"Buvayda, Bachqir, Yangiqo'rg'on, Uchko'prik","Payshanba":"Rishton, Bog'dod","Shanba":"Ofisda","Yakshanba":"Marg'ilon, Oltiariq, Chimyon"},
 "Abdumalik aka": {"Dushanba":"Bog'dod, Rishton","Seshanba":"Buvayda, Yangiqo'rg'on, Bachqir","Chorshanba":"So'x","Payshanba":"Oltiariq, Chimyon, Vodil","Shanba":"Marg'ilon, Yozyovon","Yakshanba":"Rapqon, Yaypan"},
 "Atxamjon aka": {"Dushanba":"Bog'dod, Rishton, Oltiariq","Seshanba":"Marg'ilon, Chimyon, Quva","Chorshanba":"Yaypan, Beshariq, Goriski, Rapqon","Payshanba":"Andijon","Shanba":"Dang'ara, G'urumsaroy, Pop, Chust, To'raqo'rg'on, Namangan","Yakshanba":"Uchko'prik, Buvayda, Bachqir, Yangiqo'rg'on"},
 "Abbos aka": {"Dushanba":"Dang'ara, G'urumsaroy","Seshanba":"Pop, Chust, To'raqo'rg'on, Jomashuy","Chorshanba":"Buvayda, Bachqir","Payshanba":"Uchko'prik, Yangiqo'rg'on","Shanba":"Beshariq, Goriski","Yakshanba":"Rapqon, Yaypan"},
 "Davronjon aka": {"Dushanba":"Paxtaobod, Izboskan, Poytug', Shahrixon","Seshanba":"Rishton (0,5)","Chorshanba":"Quva, Toshloq","Payshanba":"Oltiariq","Shanba":"Rishton (0,5), Chimyon","Yakshanba":"Shahar"},
 "Abdulloh aka": {"Dushanba":"—","Seshanba":"Bog'dod (0,5)","Chorshanba":"Marg'ilon, Farg'ona (xanting)","Payshanba":"So'x","Shanba":"Bog'dod (0,5)","Yakshanba":"Marg'ilon, Vodil, Avval"},
}

_D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")
def F(size, bold=False):
    return ImageFont.truetype(os.path.join(_D, "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"), size)

# ranglar
NAVY="#1F3A5F"; HEAD="#2E6DB4"; DAYCOL="#E8EFF8"; GRID="#C9D3E0"; TXT="#1E2430"
WHITE="#FFFFFF"; ALT="#F7F9FC"; GREEN="#2E9E5B"; GREEN_BG="#D7F2E1"; RED="#C0392B"; RED_BG="#FBE3E1"

def _wrap(d, text, font, w):
    words, lines, cur = text.split(" "), [], ""
    for wd in words:
        t = (cur+" "+wd).strip()
        if d.textlength(t, font=font) <= w: cur = t
        else:
            if cur: lines.append(cur)
            cur = wd
    if cur: lines.append(cur)
    return lines

def _fit(d, text, size, bold, maxw):
    while size > 10 and d.textlength(text, font=F(size, bold)) > maxw:
        size -= 1
    return F(size, bold)

def rasm_yasash(bugun: str, sana: str, agentlar=None, guruh="AGENTLAR"):
    AGENTLAR_ = agentlar or AGENTLAR
    S = 2  # sifat uchun masshtab
    pad, dayw, colw = 24*S, 150*S, 210*S
    f_title, f_sub, f_head, f_day, f_cell, f_cellb = F(30*S,True), F(17*S), F(17*S,True), F(17*S,True), F(15*S), F(15*S,True)
    tmp = ImageDraw.Draw(Image.new("RGB",(10,10)))
    lh, cpad = 21*S, 12*S
    # qator balandliklari
    heights=[]
    for k in KUNLAR:
        mx=1
        if k!="Juma":
            for a in AGENTLAR_:
                mx=max(mx,len(_wrap(tmp,REGION[a].get(k,"-"),f_cellb if k==bugun else f_cell,colw-2*cpad)))
        heights.append(max(52*S, mx*lh+2*cpad))
    W = pad*2+dayw+colw*len(AGENTLAR_)
    titleh, headh = 96*S, 50*S
    H = pad+titleh+headh+sum(heights)+pad+30*S
    img = Image.new("RGB",(W,H),WHITE); d = ImageDraw.Draw(img)

    # sarlavha
    d.rounded_rectangle([pad,pad,W-pad,pad+titleh-12*S],radius=14*S,fill=NAVY)
    sarlavha = f"{guruh} AGENTLARI"
    pastki = (f"Haftalik hudud jadvali  |  Bugun: {bugun}  |  {sana}" if sana else "Haftalik hudud jadvali")
    d.text((W/2,pad+32*S),sarlavha,font=_fit(d,sarlavha,30*S,True,W-2*pad-24*S),fill=WHITE,anchor="mm")
    d.text((W/2,pad+66*S),pastki,font=_fit(d,pastki,17*S,False,W-2*pad-24*S),fill="#BFD3EC",anchor="mm")

    x0, y = pad, pad+titleh
    # ustun sarlavhalari
    d.rectangle([x0,y,x0+dayw,y+headh],fill=HEAD,outline=GRID)
    d.text((x0+dayw/2,y+headh/2),"Kun",font=f_head,fill=WHITE,anchor="mm")
    for i,a in enumerate(AGENTLAR_):
        cx=x0+dayw+i*colw
        d.rectangle([cx,y,cx+colw,y+headh],fill=HEAD,outline=GRID)
        d.text((cx+colw/2,y+headh/2),a,font=_fit(d,a,17*S,True,colw-16*S),fill=WHITE,anchor="mm")
    y+=headh

    for ri,(k,h) in enumerate(zip(KUNLAR,heights)):
        is_today, is_dam = (k==bugun), (k=="Juma")
        rowbg = GREEN_BG if is_today else (RED_BG if is_dam else (WHITE if ri%2==0 else ALT))
        dbg = GREEN if is_today else (RED_BG if is_dam else DAYCOL)
        dtxt = WHITE if is_today else (RED if is_dam else TXT)
        d.rectangle([x0,y,x0+dayw,y+h],fill=dbg,outline=GRID)
        d.text((x0+dayw/2,y+h/2),("▶ " if is_today else "")+k,font=f_day,fill=dtxt,anchor="mm")
        for i,a in enumerate(AGENTLAR_):
            cx=x0+dayw+i*colw
            d.rectangle([cx,y,cx+colw,y+h],fill=rowbg,outline=GRID)
            if is_dam:
                d.text((cx+colw/2,y+h/2),"Dam",font=f_cellb,fill=RED,anchor="mm"); continue
            f = f_cellb if is_today else f_cell
            lines=_wrap(d,REGION[a].get(k,"-"),f,colw-2*cpad)
            ty=y+(h-len(lines)*lh)/2
            for ln in lines:
                d.text((cx+colw/2,ty+lh/2),ln,font=f,fill="#145A32" if is_today else TXT,anchor="mm"); ty+=lh
        y+=h
    if bugun in KUNLAR:
      yy=pad+titleh+headh+sum(heights[:KUNLAR.index(bugun)])
      hh=heights[KUNLAR.index(bugun)]
      d.rectangle([x0,yy,W-pad,yy+hh],outline=GREEN,width=4*S)
    d.text((W-pad,H-pad),"CP Concrete  •  avtomatik hisobot",font=F(12*S),fill="#8A94A6",anchor="rs")
    buf=io.BytesIO(); img.save(buf,format="PNG",optimize=True); buf.seek(0)
    return buf

