"""Build 'Evan Genia Run v3 ez.romo style' FCPXML from the v2 tight cut.
Usage: python3 build_v3.py <v2.fcpxml> <cut_words.json> <out.fcpxml> <plan.json>
"""
import sys, re, json
from fractions import Fraction as F
from urllib.parse import quote

v2, wordsf, out, planf = sys.argv[1:5]
X = open(v2).read()
RUN = "/Volumes/Babi's 2TB/Babiontherun/Fall26/Media/Vlogs/Nov 13 Evan Genia Run"
TB = 60  # sequence fps

def q(x):  # snap to sequence frame
    return F(round(F(x) * TB), TB)
def r(f):
    f = F(f)
    return f"{f.numerator}/{f.denominator}s" if f.denominator != 1 else f"{f.numerator}s"

# asset durations (seconds) from the v2 resources
adur = {m.group(1): F(m.group(2)[:-1]) for m in re.finditer(r'<asset id="a_(IMG_\d+)"[^>]*?duration="([^"]+)"', X)}

# --- v2 tight cut segments (cut-time map for captions) ---
V2 = [("IMG_0179",20.30,23.75),("IMG_0180",1.90,5.20),("IMG_0180",7.05,9.45),("IMG_0172",2.85,5.95),
      ("IMG_0175",2.90,8.85),("IMG_0181",0.95,2.85),("IMG_0181",8.55,14.00),("IMG_0182",3.50,10.95),
      ("IMG_0182",12.45,18.40),("IMG_0183",4.30,8.60),("IMG_0183",12.60,16.20),("IMG_0184",10.95,15.40),
      ("IMG_0184",17.95,22.75)]

# --- v3 pieces: (clip, in, out, speed, zoom(scale,x,y) or None, mute, note) ---
P = [
 ("IMG_0179",20.30,23.75,1.3,None,False,"intro day 13 (sped up 1.3x)"),
 ("IMG_0180",1.90,5.20,1.3,None,False,"uncle first time in running shoes (1.3x)"),
 ("IMG_0180",7.05,9.45,1.3,None,False,"getting my uncle out (1.3x)"),
 ("IMG_0172",2.85,4.85,1.0,None,False,"uncle: first time I will be"),
 ("IMG_0172",4.85,5.95,1.0,(1.4,10.2,-20),False,"PUNCH-IN running with running shoes + wow"),
 ("IMG_0175",2.90,8.85,1.0,None,False,"getting weird (air horn) / Evan"),
 ("IMG_0181",0.95,2.85,1.0,None,False,"scared the neighborhood away + fly buzz"),
 ("IMG_0181",8.55,14.00,1.0,None,False,"shoes little small"),
 ("IMG_0182",3.50,6.58,1.0,None,False,"how you feeling sir"),
 ("IMG_0182",6.58,8.00,1.0,(1.4,4.8,-20),False,"PUNCH-IN another 5-10 + vine boom"),
 ("IMG_0182",8.00,10.95,1.0,None,False,"increase the distance"),
 ("IMG_0182",12.45,15.48,1.2,None,False,"not get hit by cars (1.2x)"),
 ("IMG_0182",15.48,15.84,1.2,None,True,"CENSOR beep"),
 ("IMG_0182",15.84,18.40,1.2,None,False,"not doing that right now + duck"),
 ("IMG_0183",4.30,5.90,1.0,None,False,"Genia's feeling good"),
 ("IMG_0183",5.90,8.60,1.0,(1.4,-7.1,-2.8),False,"PUNCH-IN my uncle by the way + record scratch"),
 ("IMG_0183",12.60,16.20,1.0,None,False,"my cousin / brother"),
 ("IMG_0184",10.95,15.40,1.0,None,False,"did you guys get weird (air horn)"),
 ("IMG_0184",17.95,21.15,1.0,None,False,"beat us back to the house"),
 ("IMG_0184",21.15,22.75,0.75,(1.5,1.7,-3),False,"SLOW-MO PUNCH-IN he doesn't run + vine boom"),
]

# timeline layout
pieces = []; off = F(0)
for clip,a,b,s,z,mute,note in P:
    s = F(s).limit_denominator(100)
    st = q(F(a) / s)                    # clip-time start (retimed domain)
    du = q(F(b - a) / s)
    pieces.append(dict(clip=clip,a=a,b=b,s=s,z=z,mute=mute,note=note,off=off,st=st,du=du,kids=[]))
    off += du
TOTAL = off

def src2tl(clip, t):
    for p in pieces:
        if p["clip"] == clip and p["a"] - 1e-6 <= t < p["b"] + 1e-6:
            return p["off"] + (F(t) - F(p["a"])) / p["s"]
    return None
def tl2piece(t):
    for p in pieces:
        if p["off"] <= t < p["off"] + p["du"]:
            return p
    return pieces[-1]
def attach(t, xml):  # xml has {OFF}
    t = q(t); p = tl2piece(t)
    p["kids"].append(xml.replace("{OFF}", r(p["st"] + (t - p["off"]))))

# cut-time -> timeline
cut = []; c = F(0)
for clip,a,b in V2:
    d = F(round((b - a) * 60), 60); cut.append((c, c + d, clip, a)); c += d
def cut2tl(t):
    for c0,c1,clip,a in cut:
        if c0 <= t < c1:
            return src2tl(clip, float(a + (F(t) - c0)))
    return None

# ---------- captions ----------
W = json.load(open(wordsf))
FIX = {"riding":"running"}
words = []
skip_next = set()
for i,(s0,e0,t) in enumerate(W):
    w = re.sub(r"[^\w'\-*]", "", t).strip()
    if not w: continue
    lw = w.lower()
    # targeted corrections (whisper mishears, checked against the raw-clip transcripts)
    if abs(s0-12.76)<0.05 and lw=="look": w="we're"
    elif abs(s0-12.88)<0.05 and lw=="at": w="getting"
    elif abs(s0-13.76)<0.05 and lw=="with": continue
    elif abs(s0-13.64)<0.05 and lw=="let's": s0 = 13.50
    elif abs(s0-28.94)<0.05 and lw=="five": w="5-10"
    elif abs(s0-29.16)<0.05 and lw=="times": continue
    elif lw=="shit": w="sh*t"
    w = FIX.get(w.lower(), w)
    words.append([F(s0).limit_denominator(1000), F(e0).limit_denominator(1000), w.upper()])

EMPH = {"13TH","UNCLE","FIRST","SHOES","WEIRD","EVAN","NEIGHBORHOOD","SMALL","5-10","DISTANCE","CARS","SH*T",
        "REFLECTIVE","GENIA'S","EARLIER","COUSIN","BROTHER","HOUSE","RUN","BABI","OAKVILLE","YEAR"}
caps = []
for i,(s0,e0,w) in enumerate(words):
    t0 = cut2tl(s0);
    if t0 is None: continue
    t0 = q(t0)
    nxt = cut2tl(words[i+1][0]) if i+1 < len(words) else TOTAL
    end_cap = q(cut2tl(min(e0, s0 + F(3,5))) or t0 + F(1,2)) + F(6,60)
    t1 = q(min(nxt if nxt else TOTAL, end_cap, TOTAL))
    if caps and caps[-1][1] > t0: caps[-1][1] = t0
    if t1 - t0 < F(6,60): t1 = t0 + F(6,60)
    caps.append([t0, t1, w])
# remove overlaps / zero length
clean = []
for c0,c1,w in caps:
    if clean and c0 < clean[-1][1]: clean[-1][1] = c0
    if clean and clean[-1][1] <= clean[-1][0]: clean.pop()
    clean.append([c0,c1,w])
caps = [c for c in clean if c[1] > c[0]]
# merge flashes shorter than 5 frames into the next word (keeps 1-2 words per card)
merged = []
i = 0
while i < len(caps):
    c0, c1, w = caps[i]
    while c1 - c0 < F(5,60) and i + 1 < len(caps) and len(w.split()) < 3:
        i += 1; c1 = caps[i][1]; w = w + " " + caps[i][2]
    merged.append([c0, c1, w]); i += 1
caps = merged

TITLE_UID = ".../Titles.localized/Bumper:Opener.localized/Basic Title.localized/Basic Title.moti"
POSKEY = "9999/999166631/999166633/1/100/101"
tsn = [0]
def title(t0, t1, text, size, y, lane, font="Arial Black", face="Regular", stroke="-6", shadow="0 0 0 0.75", name="Caption"):
    tsn[0] += 1; tid = f"ts{tsn[0]}"
    lines = text.split("\n")
    body = "".join(f'<text-style ref="{tid}">{l}{"&#10;" if k < len(lines)-1 else ""}</text-style>' for k,l in enumerate(lines))
    xml = (f'<title ref="eT" lane="{lane}" offset="{{OFF}}" name="{name} - {lines[0][:24]}" start="3600s" duration="{r(t1-t0)}">'
           f'<param name="Position" key="{POSKEY}" value="0 {y}"/>'
           f'<text>{body}</text>'
           f'<text-style-def id="{tid}"><text-style font="{font}" fontSize="{size}" fontFace="{face}" fontColor="1 1 1 1" '
           f'strokeColor="0 0 0 1" strokeWidth="{stroke}" shadowColor="{shadow}" shadowOffset="5 315" shadowBlurRadius="6" alignment="center"/></text-style-def>'
           f'</title>')
    attach(t0, xml)

for c0,c1,w in caps:
    base = 96 if any(x in EMPH for x in w.split()) else 72
    size = min(base, int(950 / (0.80 * max(len(w),1))))
    if " " in w: size = min(size, 72)
    title(c0, c1, w.replace("&","&amp;"), size, -311, 1)

# header + day tracker (ez.romo: "Finding the HARDEST fitness challenge / Part 3", then "5km (3h)")
intro_end = pieces[2]["off"] + pieces[2]["du"]
title(F(0), intro_end, "Running every day\ntill the end of the year", 42, 460, 2, font="Helvetica Neue", face="Medium", stroke="0", name="Header")
title(F(0), intro_end, "Day 13", 44, 335, 3, font="Helvetica Neue", face="Medium", stroke="0", name="Header day")
title(intro_end, TOTAL, "Day 13", 46, 470, 2, font="Helvetica Neue", face="Medium", stroke="0", name="Tracker")

# ---------- sound effects ----------
SND = {  # id: (file, in, len, vol dB, name)
 "boom":   ("vine_boom.mp3", 0.22, 1.30, "-9dB", "SFX vine boom"),
 "horn":   ("air_horn.mp3", 0.24, 1.10, "-10dB", "SFX air horn"),
 "wow":    ("wow.mp3", 0.33, 1.30, "-12dB", "SFX wow"),
 "scratch":("record_scratch.mp3", 1.82, 0.90, "-14dB", "SFX record scratch"),
 "fly":    ("sfx_pack_kaushal.mp3", 22.82, 0.60, "-10dB", "SFX fly buzz"),
 "duck":   ("sfx_pack_kaushal.mp3", 53.28, 0.70, "-14dB", "SFX duck quack"),
 "beep":   ("sfx_pack_kaushal.mp3", 0.15, None, "-16dB", "SFX censor beep"),
}
sfx_assets = {}
def sfx(key, t, length=None, lane=-1):
    f, a, ln, vol, name = SND[key]
    ln = length if length is not None else ln
    sfx_assets[f] = True
    aid = "s_" + re.sub(r"\W", "_", f[:-4])
    attach(t, f'<asset-clip ref="{aid}" lane="{lane}" offset="{{OFF}}" name="{name}" start="{r(F(a).limit_denominator(1000))}" '
              f'duration="{r(q(ln))}" audioRole="effects"><adjust-volume amount="{vol}"/></asset-clip>')

T = lambda clip, s: src2tl(clip, s)
sfx("wow",   T("IMG_0172", 4.85))
sfx("horn",  T("IMG_0175", 3.62))
sfx("fly",   T("IMG_0181", 2.78))
sfx("boom",  T("IMG_0182", 6.86))
beep_p = [p for p in pieces if p["mute"]][0]
sfx("beep",  beep_p["off"], length=beep_p["du"])
sfx("duck",  T("IMG_0182", 18.30), lane=-2)
sfx("scratch", T("IMG_0183", 5.86))
sfx("horn",  T("IMG_0184", 13.68))
boom_end = T("IMG_0184", 22.20)
sfx("boom",  boom_end, length=min(1.3, float(TOTAL - q(boom_end))))

# music bed (instrumental, ~9 dB under speech)
MUS = "music_wii_sports_title.mp3"; sfx_assets[MUS] = True
attach(F(0), f'<asset-clip ref="s_music_wii_sports_title" lane="-3" offset="{{OFF}}" name="Music - Wii Sports title (bed)" start="1/10s" '
             f'duration="{r(TOTAL)}" audioRole="music"><adjust-volume amount="-13dB"/></asset-clip>')

# ---------- resources ----------
dur = {"vine_boom.mp3":"3088/1000s","air_horn.mp3":"1645/1000s","wow.mp3":"4937/1000s","record_scratch.mp3":"6295/1000s",
       "sfx_pack_kaushal.mp3":"63947/1000s","music_wii_sports_title.mp3":"134420/1000s"}
rate = {"vine_boom.mp3":"48000","air_horn.mp3":"44100"}
chans = {"air_horn.mp3":"1"}
res = [f'<effect id="eT" name="Basic Title" uid="{TITLE_UID}"/>']
for f in sfx_assets:
    aid = "s_" + re.sub(r"\W", "_", f[:-4])
    src = "file://" + quote(f"{RUN}/Sound/{f}")
    res.append(f'<asset id="{aid}" name="{f[:-4]}" start="0s" duration="{dur[f]}" hasAudio="1" audioSources="1" '
               f'audioChannels="{chans.get(f,"2")}" audioRate="{rate.get(f,"44100")}"><media-rep kind="original-media" src="{src}"/></asset>')
X = X.replace("</resources>", "\n".join(res) + "\n</resources>")

# ---------- spine ----------
def clipxml(p):
    a = F(p["a"]).limit_denominator(1000); s = p["s"]; D = adur[p["clip"]]
    inner = f'<note>{p["note"]}</note>'
    if s != 1:
        inner += (f'<timeMap><timept time="0s" value="0s" interp="linear"/>'
                  f'<timept time="{r(D / s)}" value="{r(D)}" interp="linear"/></timeMap>')
    if p["z"]:
        sc,x,y = p["z"]; inner += f'<adjust-transform position="{x} {y}" scale="{sc} {sc}"/>'
    if p["mute"]:
        inner += '<adjust-volume amount="-96dB"/>'
    inner += "".join(p["kids"])
    return (f'<asset-clip ref="a_{p["clip"]}" name="{p["clip"]}" offset="{r(p["off"])}" start="{r(p["st"])}" '
            f'duration="{r(p["du"])}" tcFormat="NDF" audioRole="dialogue">{inner}</asset-clip>')

proj = (f'<project name="Evan Genia Run v3 ez.romo style"><sequence format="r1" duration="{r(TOTAL)}" tcStart="0s" tcFormat="NDF" '
        f'audioLayout="stereo" audioRate="48k"><spine>\n' + "\n".join(clipxml(p) for p in pieces) + '\n</spine></sequence></project>')
# keep only the new project in this file (event clips stay so media matches)
X = re.sub(r'<project name=.*?</project>', '', X, flags=re.S)
X = X.replace("</event>", proj + "</event>")
open(out, "w").write(X)

plan = dict(total=float(TOTAL), pieces=[dict(clip=p["clip"],a=p["a"],b=p["b"],speed=float(p["s"]),zoom=p["z"],mute=p["mute"],
            off=float(p["off"]),dur=float(p["du"]),note=p["note"]) for p in pieces],
            captions=[[float(a),float(b),w] for a,b,w in caps])
json.dump(plan, open(planf,"w"), indent=1)
print(f"total {float(TOTAL):.2f}s, {len(pieces)} pieces, {len(caps)} captions, sfx files {list(sfx_assets)}")
