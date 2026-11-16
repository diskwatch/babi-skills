"""Shake-hands-with reel builder (Nov 18 2026). Format copied from demandthelimitslaw DeSWfvszUJ4 (+ kinso DVFpUG8iYnj).
P = people in order; each: (card, clip, [(in,out)...] source seconds). Captions: 2-3 word chunks, active word green, timed from
word timings of the planned cut (cut_words.json + idx.json made by rendering the cut audio and running medium.en)."""
import subprocess, json, os, re, sys
from fractions import Fraction as F
from urllib.parse import quote
from PIL import Image, ImageDraw, ImageFont
D = "/Volumes/4TBSSD_4/Babi NR Content/Media/OFFICE/Nov 18 shake hands with..."
HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT = "Shake Hands With"
EVENT = "Nov 18 Shake hands with"
P = [
 ("Claude abuser",   "IMG_0529", [(8.95,11.95),(22.0,23.0),(32.6,34.85)]),
 ("Office yapper",   "IMG_0533", [(353.15,355.45),(357.0,359.7)]),
 ("Funniest",        "IMG_0533", [(208.7,211.8),(213.15,214.2),(221.65,223.1),(225.4,227.4)]),
 ("Smartest",        "IMG_0533", [(110.1,116.05),(122.7,123.9),(131.2,133.4)]),
 ("47 Chrome tabs",  "IMG_0532", [(6.35,11.4),(23.3,25.9)]),
 ("Deserves a raise","IMG_0533", [(314.5,316.3),(320.45,324.65),(326.0,327.15),(333.8,335.5)]),
 ("Best dressed",    "IMG_0533", [(288.85,292.05),(293.35,297.0)]),
 ("Lie for you",     "IMG_0533", [(261.65,266.0),(273.1,275.8)]),
 ("Call at 2am",     "IMG_0533", [(75.1,78.45),(83.1,85.2),(88.0,90.0)]),
 ("Office celebrity","IMG_0533", [(57.75,64.1)]),
]
# captions: (clip, source start of line, [words]) -> timings filled from W (source-time word list)
FIX = {"clawed":"CLAUDE","y":"Y'ALL","'all":"","2":"2","a":"A",".m.":"AM","like...":"","Well,":"WELL"}
DROP_LINES = ["Oh, back to something"]
GREEN = "0.667 0.875 0.514 1"       # reference highlight (170,223,131)
CAP_SIZE, CAP_Y = 30, -215          # Basic Title Position units (~1.67 px): -215 -> y ~ 1180-1320 (61-68% down)
MAXC = 15
TB = 60
def q(x): return F(round(F(str(x)) * TB), TB)
def r(f):
    f = F(f); return f"{f.numerator}/{f.denominator}s" if f.denominator != 1 else f"{f.numerator}s"
def esc(s): return s.replace("&","&amp;").replace("<","&lt;")

# ---- header PNG (white caps on black rounded box, like the reference; top edge below the 250 px IG band)
hp = f"{D}/Graphics/header_shake_hands_with.png"
im = Image.new("RGBA", (1080,1920), (0,0,0,0)); d = ImageDraw.Draw(im)
f = ImageFont.truetype("/System/Library/Fonts/Avenir Next.ttc", 62, index=8)
for i in range(12):
    try:
        ff = ImageFont.truetype("/System/Library/Fonts/Avenir Next.ttc", 62, index=i)
        if ff.getname() == ("Avenir Next","Heavy"): f = ff; break
    except Exception: pass
txt = "SHAKE HANDS WITH..."
w = d.textlength(txt, font=f); bw, bh, cy = w + 56, 104, 345
d.rounded_rectangle([540-bw/2, cy-bh/2, 540+bw/2, cy+bh/2], 14, fill=(0,0,0,255))
d.text((540, cy-2), txt, font=f, fill=(255,255,255,255), anchor="mm")
im.save(hp); print("header", f.getname(), "box", int(540-bw/2), int(cy-bh/2), int(540+bw/2), int(cy+bh/2))

# ---- words in source time
idx = json.load(open(f"{HERE}/idx.json")); cw = json.load(open(f"{HERE}/cut_words.json"))
def seg_of(t):
    k = 0
    for i,(n,c,a,b,t0) in enumerate(idx):
        if t >= t0 - 0.02: k = i
    return k
words = []   # (clip, src_start, src_end, text, person)
for i,(a,b,t) in enumerate(cw):
    k = seg_of(a)
    # a leading "Shake" that whisper glued to the previous segment belongs to the next word's segment
    if i+1 < len(cw) and seg_of(cw[i+1][0]) != k and t.lower().startswith("shake"):
        k = seg_of(cw[i+1][0]); n,c,sa,sb,t0 = idx[k]; a = max(t0+0.08, cw[i+1][0]-0.45); b = cw[i+1][0]
    n,c,sa,sb,t0 = idx[k]
    words.append([n, c, sa + (a-t0), sa + (min(b, t0+sb-sa)-t0), t])
txtall = " ".join(w[4] for w in words)
for dl in DROP_LINES:
    ws = dl.split()
    for i in range(len(words)-len(ws)+1):
        if [w[4] for w in words[i:i+len(ws)]] == ws: del words[i:i+len(ws)]; break
out = []
for n,c,a,b,t in words:
    t2 = FIX.get(t, t); t2 = re.sub(r"[.,?!]", "", t2).upper()
    if t2: out.append([n,c,a,b,t2])
words = [w for i,w in enumerate(out) if not (w[4]=="A" and i+1 < len(out) and out[i+1][4]=="AM")]
# chunks: same person+clip, gap < 0.5 s, <= 3 words, <= MAXC chars
chunks = []
for wd in words:
    if chunks:
        last = chunks[-1]; s = " ".join(x[4] for x in last)
        if last[-1][0]==wd[0] and wd[2]-last[-1][3] < 0.5 and len(last) < 3 and len(s)+1+len(wd[4]) <= MAXC:
            last.append(wd); continue
    chunks.append([wd])

# ---- spine
probe = {}
for _,c,_ in P:
    if c not in probe:
        j = json.loads(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","json",f"{D}/{c}.MOV"],capture_output=True,text=True).stdout)
        probe[c] = F(j["format"]["duration"]).limit_denominator(600)
TITLE_UID = ".../Titles.localized/Bumper:Opener.localized/Basic Title.localized/Basic Title.moti"
POSKEY = "9999/999166631/999166633/1/100/101"
spine = []; off = F(0); tid = 0; plan = []
for k,(name,c,segs) in enumerate(P):
    for si,(a,b) in enumerate(segs):
        st, en = q(a), q(b); du = en - st; kids = ""
        if not spine:
            kids += f'<video ref="pH" lane="2" offset="{r(st)}" name="Header - SHAKE HANDS WITH..." start="0s" duration="{{TOTAL}}"/>'
        for ch in chunks:
            if ch[0][0] != name or ch[0][1] != c: continue
            if not (a - 0.05 <= ch[0][2] < b): continue
            cend = min(ch[-1][3] + 0.25, b)
            for wi,wd in enumerate(ch):
                t0 = max(q(wd[2]), st) if wi else max(q(wd[2]) - F(2,60), st)
                t1 = q(ch[wi+1][2]) if wi+1 < len(ch) else q(cend)
                t1 = min(t1, en)
                if t1 - t0 < F(2,60): continue
                runs = ""
                for wj,x in enumerate(ch):
                    sp = " " if wj < len(ch)-1 else ""
                    runs += f'<text-style ref="ts{tid}{"g" if wj==wi else "w"}">{esc(x[4])}{sp}</text-style>'
                st_ = lambda col: (f'<text-style font="Avenir Next" fontSize="{CAP_SIZE}" fontFace="Heavy" fontColor="{col}" bold="1" '
                                   f'strokeColor="0 0 0 1" strokeWidth="-2" shadowColor="0 0 0 0.75" shadowOffset="3 315" shadowBlurRadius="5" alignment="center"/>')
                defs = f'<text-style-def id="ts{tid}g">{st_(GREEN)}</text-style-def>'
                if len(ch) > 1: defs = f'<text-style-def id="ts{tid}w">{st_("1 1 1 1")}</text-style-def>' + defs
                kids += (f'<title ref="eT" lane="1" offset="{r(t0)}" name="{esc(" ".join(x[4] for x in ch))}" start="3600s" duration="{r(t1-t0)}">'
                         f'<param name="Position" key="{POSKEY}" value="0 {CAP_Y}"/><text>{runs}</text>{defs}</title>')
                tid += 1
        spine.append(f'<asset-clip ref="a_{c}" name="{k+1:02d} {esc(name)}" offset="{r(off)}" start="{r(st)}" duration="{r(du)}" tcFormat="NDF" audioRole="dialogue">{kids}</asset-clip>')
        plan.append(dict(person=k+1, card=name, clip=c, src_in=float(st), src_out=float(en), tl=float(off), dur=float(du)))
        off += du
TOTAL = off
spine = [x.replace("{TOTAL}", r(TOTAL)) for x in spine]
res = ['<format id="r1" frameDuration="100/6000s" width="1080" height="1920" colorSpace="1-1-1 (Rec. 709)"/>',
       '<format id="rv" frameDuration="100/6000s" width="1080" height="1920" colorSpace="9-18-9 (Rec. 2020 HLG)"/>',
       '<format id="ri" name="FFVideoFormatRateUndefined" width="1080" height="1920" colorSpace="1-1-1 (Rec. 709)"/>',
       f'<effect id="eT" name="Basic Title" uid="{TITLE_UID}"/>']
for c,dd in probe.items():
    res.append(f'<asset id="a_{c}" name="{c}" start="0s" duration="{r(dd)}" hasVideo="1" format="rv" hasAudio="1" videoSources="1" audioSources="1" audioChannels="2" audioRate="48000">'
               f'<media-rep kind="original-media" src="file://{quote(D + "/" + c + ".MOV")}"/></asset>')
res.append(f'<asset id="pH" name="header_shake_hands_with" start="0s" duration="0s" hasVideo="1" format="ri" videoSources="1">'
           f'<media-rep kind="original-media" src="file://{quote(hp)}"/></asset>')
X = ('<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE fcpxml>\n<fcpxml version="1.11"><resources>\n' + "\n".join(res) + '\n</resources>\n'
     '<library location="file:///Volumes/4TBSSD_4/Babi%20NR%20Content/Libraries/TME.fcpbundle/" colorProcessing="wide-hdr">'
     f'<event name="{EVENT}">'
     f'<project name="{PROJECT}"><sequence format="r1" duration="{r(TOTAL)}" tcStart="0s" tcFormat="NDF" audioLayout="stereo" audioRate="48k"><spine>\n'
     + "\n".join(spine) + '\n</spine></sequence></project></event></library></fcpxml>\n')
outp = f"{D}/XML/{PROJECT}.fcpxml"; open(outp,"w").write(X)
json.dump(plan, open(f"{D}/XML/cut_plan.json","w"), indent=1)
print(f"total {float(TOTAL):.2f}s, {tid} caption titles -> {outp}")
t=0
for k,(name,c,segs) in enumerate(P):
    dur=sum(float(q(b)-q(a)) for a,b in segs); print(f"{k+1:2d} {name:18s} {t:6.2f}s  {dur:5.2f}s  {len(segs)} shots"); t+=dur
print(" | ".join(" ".join(x[4] for x in ch) for ch in chunks))
