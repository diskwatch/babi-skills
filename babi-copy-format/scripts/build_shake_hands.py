"""Shake-hands-with reel builder (Nov 18 2026). Format copied from demandthelimitslaw DeSWfvszUJ4 (+ kinso DVFpUG8iYnj).
P = people in order; each: (card, clip, [(in,out)...] source seconds). Captions: 2-3 word chunks, active word green, timed from
word timings of the planned cut (cut_words.json + idx.json made by rendering the cut audio and running medium.en)."""
import subprocess, json, os, re, sys
from fractions import Fraction as F
from urllib.parse import quote
from PIL import Image, ImageDraw, ImageFont
D = "/Volumes/4TBSSD_4/Babi NR Content/Media/OFFICE/Nov 18 shake hands with..."
HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT = "Shake Hands With 2"   # v4 (2026-11-17). Babi's "Shake Hands With 1" (his music bed) left untouched; re-import with Replace onto "2"
EVENT = "Nov 18 Shake hands with"
P = [   # chronological chain order. v3 = Babi's re-edit trims (2026-11-16) + his notes (Andrew through the glass, "back to Stu", office love)
 ("Claude abuser",   "IMG_0529", [(8.95,11.95),(22.0,23.0),(32.6,34.85)]),
 ("Emergency contact","IMG_0531",[(11.95,15.4),(24.0,27.35)]),
 ("47 Chrome tabs",  "IMG_0532", [(6.35,11.4),(23.3,25.9)]),
 ("Best snacks",     "IMG_0533", [(12.95,16.9),(20.6,22.15),(40.45,41.25),(43.3,44.1)]),   # v4: + jump cut to Rick's fruit bowl (ZOOM + vine boom)
 ("Office celebrity","IMG_0533", [(57.75,61.53)]),                     # v4: Rick handshake + Babi's "thank you" (62.9-63.77) cut
 ("Call at 2am",     "IMG_0533", [(75.1,78.35),(83.15,84.3),(84.7,85.15),(88.45,90.0)]),   # v4: walk up to Alli tightened, mic hand-off kept
 ("Smartest",        "IMG_0533", [(110.1,116.05),(122.7,127.1),(131.2,133.4)]),
 ("Not PR trained",  "IMG_0533", [(149.3,153.1),(172.0,173.0),(181.6,183.6)]),
 ("Funniest",        "IMG_0533", [(208.7,211.8),(213.15,214.2),(221.65,223.1),(225.4,228.15)]),
 ("Goes to for help","IMG_0533", [(239.77,243.5),(251.5,255.25)]),
 ("Lie for you",     "IMG_0533", [(261.65,266.28),(273.1,275.8)]),
 ("Best dressed",    "IMG_0533", [(288.85,292.05),(293.35,297.0),(298.0,302.4),(303.4,305.75)]),   # v4: Jess's "office love" kept, Babi's repeat (305.9-306.7) cut
 ("Deserves a raise","IMG_0533", [(314.5,316.3),(320.45,324.65),(326.0,327.15),(333.8,335.5)]),
 ("Office yapper",   "IMG_0533", [(353.15,355.45),(357.0,359.68)]),
]
# captions: (clip, source start of line, [words]) -> timings filled from W (source-time word list)
FIX = {"Mmm":"","Mmm,":"","clawed":"CLAUDE","y":"Y'ALL","'all":"",".m.":"AM","two":"2","Okay.":"","OK.":""}
GREEN = "0.667 0.875 0.514 1"       # reference highlight (170,223,131)
CAP_SIZE, CAP_Y = 30, -140          # measured in FCP: -215 put the caption 69% down (y~1323); -140 ~ 62% like the reference. Size 30 Avenir Next Heavy ~ 38 px per letter
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

# ---- words in source time: each shot transcribed from its own padded source slice (shot_words.py -> shot_words_raw.json)
NO_CAPS = {("IMG_0529",22.0),("IMG_0532",23.3),("IMG_0533",131.2),("IMG_0533",172.0),("IMG_0533",333.8),("IMG_0533",43.3)}  # silent walk/handshake/laugh shots: whisper invents words
OVERRIDE = {  # (clip, shot in) -> what was actually said (Babi's names, missed or clipped words)
 ("IMG_0533",40.45):"ALL RIGHT RICKSTER", ("IMG_0533",83.15):"RIGHT HERE", ("IMG_0533",84.7):"ALLI",
 ("IMG_0533",88.45):"ALL RIGHT", ("IMG_0533",122.7):"ARE YOU BUSY OH OKAY", ("IMG_0533",225.4):"OH BACK TO STU",
 ("IMG_0533",251.5):"SHE'S LIKE OH I'M GETTING MY HANDSHAKE", ("IMG_0533",181.6):"HOW'S IT GOING BUDDY",
 ("IMG_0533",298.0):"YOU ALWAYS HAVE NICE CLOTHES AND THRIFTED CLOTHES", ("IMG_0533",326.0):"NO PRESSURE",
 ("IMG_0533",213.15):"I THINK I JUST DID"}
# exact source timings where whisper misses a quiet off-mic reply; "|" forces a new caption (v4: Jess's "stop that's a lie")
TIMED = {("IMG_0533",293.35): [(293.35,293.62,"HI"),(293.62,294.15,"JESS"),(294.2,294.75,"|STOP"),
                               (294.95,295.22,"|THAT'S"),(295.22,295.34,"A"),(295.34,295.9,"LIE")]}
# jump-cut zooms: (clip, shot in) -> (scale, source px x, source px y to centre); BOOM = shots that get the vine boom on their first frame
ZOOM = {("IMG_0533",43.3): (2.4, 820, 1520)}   # Rick's fruit bowl (bowl spans x 670-970, y 1510-1745 in the 1080x1920 frame)
BOOM = {("IMG_0533",43.3)}
# Babi's music bed (added by him in "Shake Hands With 1", read from the library 2026-11-17): from 39.45 s into the song, whole video, -16 dB
MUSIC_FILE, MUSIC_IN, MUSIC_DB = f"{D}/Sound/mozart_eine_kleine_allegro.mp3", 39.449, -16
BOOM_FILE, BOOM_IN, BOOM_DB = f"{D}/Sound/vine_boom.mp3", 0.2, -8   # onset at 0.20 s in the file; file is ~-4 dB RMS, -8 dB sits at speech level
RAW = json.load(open(f"{HERE}/shot_words_raw.json"))
FULL = {"IMG_0533": json.load(open(f"{HERE}/full533_words.json"))}   # whole-take medium.en, fallback for shots RAW doesn't cover
def shot_src_words(c, a, b):
    best = max((min(b, rb) - max(a, ra), got) for _, rc, ra, rb, got in RAW if rc == c) if any(x[1] == c for x in RAW) else (0, [])
    return best[1] if best[0] > 0 else FULL.get(c, [])
words = []
for name, c, segs in P:
  for a, b in segs:
    if (c, a) in NO_CAPS: continue
    if (c, a) in TIMED:
        words += [[name, c, s0, e0, t, a] for s0, e0, t in TIMED[(c, a)]]; continue
    got = shot_src_words(c, a, b)
    got = [(max(s0, a), min(e0, b), t) for s0, e0, t in got if a <= (s0 + e0) / 2 < b or min(e0, b) - max(s0, a) >= 0.12]
    if (c, a) in OVERRIDE:
        ws = OVERRIDE[(c, a)].split()
        s0 = got[0][0] if got else a + 0.2; e0 = got[-1][1] if got else b - 0.2
        L = [len(w) + 2 for w in ws]; tot = sum(L); t = s0; got = []
        for w, l in zip(ws, L):
            d = (e0 - s0) * l / tot; got.append((t, t + d, w)); t += d
    words += [[name, c, s0, e0, t, a] for s0, e0, t in got]
out = []
for n,c,a,b,t,sh in words:
    t2 = FIX.get(t, t); t2 = re.sub(r"[.,?!]", "", t2).upper()
    if t2: out.append([n,c,a,b,t2,sh])
out.sort(key=lambda w: ([x[0] for x in P].index(w[0]), w[2]))
words = [w for i,w in enumerate(out) if not (w[4]=="A" and i+1 < len(out) and out[i+1][4]=="AM")]
# chunks: same shot, gap < 0.5 s, <= 3 words, <= MAXC chars; "|" or SHAKE starts a new one
chunks = []
for wd in words:
    brk = wd[4].startswith("|"); wd[4] = wd[4].lstrip("|")
    if chunks and not brk:
        last = chunks[-1]; s_ = " ".join(x[4] for x in last)
        if wd[4] != "SHAKE" and last[-1][0]==wd[0] and last[-1][5]==wd[5] and wd[2]-last[-1][3] < 0.5 and len(last) < 3 and len(s_)+1+len(wd[4]) <= MAXC:
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
# pass 1: shot placement on the timeline
shots = []; off = F(0)
for k,(name,c,segs) in enumerate(P):
    for a,b in segs:
        st, en = q(a), q(b); shots.append(dict(k=k, name=name, c=c, a=a, b=b, st=st, en=en, off=off)); off += en - st
TOTAL = off
# pass 2: one title per word (active word green), in TIMELINE time, then de-overlap globally so captions never stack
caps = []
for sh in shots:
    for ch in chunks:
        if ch[0][0] != sh["name"] or ch[0][1] != sh["c"] or ch[0][5] != sh["a"]: continue
        cend = min(ch[-1][3] + 0.25, sh["b"])
        for wi,wd in enumerate(ch):
            t0 = max(q(wd[2]), sh["st"]) if wi else max(q(wd[2]) - F(2,60), sh["st"])
            t1 = min(q(ch[wi+1][2]) if wi+1 < len(ch) else q(cend), sh["en"])
            caps.append([sh["off"] + t0 - sh["st"], sh["off"] + t1 - sh["st"], ch, wi])
caps.sort(key=lambda x: x[0])
for i in range(len(caps) - 1):
    caps[i][1] = min(caps[i][1], caps[i+1][0])
caps = [x for x in caps if x[1] - x[0] >= F(2,60)]
for i in range(len(caps) - 1): assert caps[i][1] <= caps[i+1][0], "caption overlap"
# pass 3: emit clips; each title is anchored to the shot it starts in (lane 1), header lane 2, boom lane -1
spine = []; tid = 0; plan = []
def title_xml(ch, wi, off_in_parent, dur):
    global tid
    runs = ""
    for wj,x in enumerate(ch):
        sp = " " if wj < len(ch)-1 else ""
        runs += f'<text-style ref="ts{tid}{"g" if wj==wi else "w"}">{esc(x[4])}{sp}</text-style>'
    st_ = lambda col: (f'<text-style font="Avenir Next" fontSize="{CAP_SIZE}" fontFace="Heavy" fontColor="{col}" bold="1" '
                       f'strokeColor="0 0 0 1" strokeWidth="-2" shadowColor="0 0 0 0.75" shadowOffset="3 315" shadowBlurRadius="5" alignment="center"/>')
    defs = f'<text-style-def id="ts{tid}g">{st_(GREEN)}</text-style-def>'
    if len(ch) > 1: defs = f'<text-style-def id="ts{tid}w">{st_("1 1 1 1")}</text-style-def>' + defs
    x = (f'<title ref="eT" lane="1" offset="{r(off_in_parent)}" name="{esc(" ".join(x[4] for x in ch))}" start="3600s" duration="{r(dur)}">'
         f'<param name="Position" key="{POSKEY}" value="0 {CAP_Y}"/><text>{runs}</text>{defs}</title>')
    tid += 1; return x
for i,sh in enumerate(shots):
    st, en, off = sh["st"], sh["en"], sh["off"]; du = en - st; kids = ""; key = (sh["c"], sh["a"])
    if key in ZOOM:
        s_, cx, cy = ZOOM[key]
        kids += f'<adjust-transform position="{-s_*(cx-540)/19.2:.4f} {s_*(cy-960)/19.2:.4f}" scale="{s_} {s_}"/>'
    if i == 0:
        kids += f'<video ref="pH" lane="2" offset="{r(st)}" name="Header - SHAKE HANDS WITH..." start="0s" duration="{r(TOTAL)}"/>'
        kids += (f'<asset-clip ref="aMusic" lane="-2" offset="{r(st)}" name="Mozart - Eine kleine Nachtmusik" start="{r(q(MUSIC_IN))}" duration="{r(TOTAL)}" audioRole="music">'
                 f'<adjust-volume amount="{MUSIC_DB}dB"/></asset-clip>')
    if key in BOOM:
        kids += (f'<asset-clip ref="aBoom" lane="-1" offset="{r(st)}" name="Vine boom" start="{r(q(BOOM_IN))}" duration="{r(q(1.6))}" audioRole="effects">'
                 f'<adjust-volume amount="{BOOM_DB}dB"/></asset-clip>')
    for t0,t1,ch,wi in caps:
        if off <= t0 < off + du:
            kids += title_xml(ch, wi, st + (t0 - off), t1 - t0)
    spine.append(f'<asset-clip ref="a_{sh["c"]}" name="{sh["k"]+1:02d} {esc(sh["name"])}" offset="{r(off)}" start="{r(st)}" duration="{r(du)}" tcFormat="NDF" audioRole="dialogue">{kids}</asset-clip>')
    plan.append(dict(person=sh["k"]+1, card=sh["name"], clip=sh["c"], src_in=float(st), src_out=float(en), tl=float(off), dur=float(du)))
res = ['<format id="r1" frameDuration="100/6000s" width="1080" height="1920" colorSpace="1-1-1 (Rec. 709)"/>',
       '<format id="rv" frameDuration="100/6000s" width="1080" height="1920" colorSpace="9-18-9 (Rec. 2020 HLG)"/>',
       '<format id="ri" name="FFVideoFormatRateUndefined" width="1080" height="1920" colorSpace="1-1-1 (Rec. 709)"/>',
       f'<effect id="eT" name="Basic Title" uid="{TITLE_UID}"/>']
for c,dd in probe.items():
    res.append(f'<asset id="a_{c}" name="{c}" start="0s" duration="{r(dd)}" hasVideo="1" format="rv" hasAudio="1" videoSources="1" audioSources="1" audioChannels="2" audioRate="48000">'
               f'<media-rep kind="original-media" src="file://{quote(D + "/" + c + ".MOV")}"/></asset>')
res.append(f'<asset id="aMusic" name="Mozart_ Eine kleine Nachtmusik, K. 525_ I. Allegro 4" start="0s" duration="{r(q(347.4))}" hasAudio="1" audioSources="1" audioChannels="2" audioRate="48000">'
           f'<media-rep kind="original-media" src="file://{quote(MUSIC_FILE)}"/></asset>')
res.append(f'<asset id="aBoom" name="vine_boom" start="0s" duration="{r(q(3.0))}" hasAudio="1" audioSources="1" audioChannels="2" audioRate="48000">'
           f'<media-rep kind="original-media" src="file://{quote(BOOM_FILE)}"/></asset>')
res.append(f'<asset id="pH" name="header_shake_hands_with" start="0s" duration="0s" hasVideo="1" format="ri" videoSources="1">'
           f'<media-rep kind="original-media" src="file://{quote(hp)}"/></asset>')
X = ('<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE fcpxml>\n<fcpxml version="1.11"><resources>\n' + "\n".join(res) + '\n</resources>\n'
     '<library location="file:///Volumes/4TBSSD_4/Babi%20NR%20Content/Libraries/TME%20FCP12.3.fcpbundle/" colorProcessing="wide-hdr">'
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
