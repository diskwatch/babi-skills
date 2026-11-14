"""ez.romo-style FCPXML builder (template). The piece table below is the final Evan Genia Run cut (Nov 13 2026) — replace it for a new video.
Defaults reflect every Babi review through v5: captions 40/48 pt capped 590 px at Position -252, header below 250 px, no tracker,
pitch OFF on every speed change, project Rec. 709, music bed -19 dB, only the SFX Babi kept.

Step 1:  python3 build_v4_ezromo.py audio  <tx_dir> <out.wav>        -> mock dialogue render for transcription
Step 2:  (transcribe out.wav with word timings -> words.json)
Step 3:  python3 build_v4_ezromo.py xml    <v2.fcpxml> <words.json> <out.fcpxml>

Notes from Babi's v3 review (2026-11-14):
- hook = Evan's last take in IMG_0179 ("we're with Babi in Oakville and we're going for a run!")
- captions were too big / went off screen -> smaller, width-capped
- Preserve Pitch OFF on every speed change (that's what makes it funny)
- yell insert (fast -> slow-mo) after "scared the whole neighborhood away"
- cut every dead space (Evan never leaves pauses); no reflective/cars clip; "sir" -> "Gen"
- removed: first air horn, duck quack, record scratch
"""
import sys, re, json, subprocess
from fractions import Fraction as F
from urllib.parse import quote

RUN = "/Volumes/Babi's 2TB/Babiontherun/Fall26/Media/Vlogs/Nov 13 Evan Genia Run"
TB = 60
def q(x): return F(round(F(x) * TB), TB)
def r(f):
    f = F(f); return f"{f.numerator}/{f.denominator}s" if f.denominator != 1 else f"{f.numerator}s"

# (clip, in, out, speed, zoom(scale,x,y)|None, note)   speed != 1 -> preserve pitch OFF
P = [
 ("IMG_0179",42.66,45.95,1.0,None,"HOOK Evan: we're with Babi in Oakville, going for a run"),
 ("IMG_0180",1.90,3.96,1.3,None,"here with my uncle, his first time"),
 ("IMG_0180",4.34,5.20,1.3,None,"wearing running shoes (0.4 s gap cut)"),
 ("IMG_0180",7.05,9.45,1.3,None,"getting my uncle out, run together"),
 ("IMG_0172",2.85,4.85,1.0,None,"uncle: first time I will be"),
 ("IMG_0172",4.85,5.95,1.0,(1.4,10.2,-20),"PUNCH-IN running with running shoes + wow"),
 ("IMG_0175",3.30,4.68,1.0,None,"we're getting weird, let's go weird"),
 ("IMG_0175",6.70,8.85,1.0,None,"this is my uncle / nice to meet you / Evan"),
 ("IMG_0181",0.95,2.85,1.0,None,"scared the whole neighborhood away + fly buzz"),
 ("IMG_0179",45.73,46.45,1.3,(1.15,0,0),"YELL ramp fast 1.3x (Babi: longer + not as fast)"),
 ("IMG_0179",46.40,46.82,0.5,(1.15,0,0),"YELL slow-mo 0.5x, shorter (pitch off)"),
 ("IMG_0181",8.55,9.55,1.0,None,"how do the shoes feel"),
 ("IMG_0181",10.32,14.00,1.0,None,"feel nice, little small, I can do it (Babi trimmed blank to 10.32)"),
 ("IMG_0182",3.50,4.10,1.0,None,"how you feeling Gen"),
 ("IMG_0182",4.86,7.86,1.0,None,"oh I feel like I can go another 5-10 (Babi removed punch-in + boom)"),
 ("IMG_0182",8.12,10.95,1.0,None,"so we might increase the distance"),
 ("IMG_0183",4.30,5.35,1.0,None,"Genia's feeling good"),
 ("IMG_0183",6.12,8.60,1.0,(1.4,-7.1,-2.8),"PUNCH-IN my uncle by the way (0.9 s dead space cut)"),
 ("IMG_0183",12.92,14.95,1.0,None,"this is my cousin / brother"),
 ("IMG_0183",15.70,16.20,1.0,None,"brother (1 s gap cut)"),
 ("IMG_0184",10.95,12.45,1.0,None,"did you guys get weird"),
 ("IMG_0184",13.45,14.78,1.0,None,"we got weird"),
 ("IMG_0184",14.78,15.40,0.5,None,"SLOW-MO Evan yells WEIRD 0.5x (pitch off)"),
 ("IMG_0184",17.95,19.57,1.0,None,"and this guy beat us"),
 ("IMG_0184",20.27,21.15,1.0,None,"back to the house (0.7 s gap cut)"),
 ("IMG_0184",21.15,22.75,0.75,(1.5,1.7,-3),"SLOW-MO PUNCH-IN he doesn't run + vine boom (pitch off)"),
]

pieces = []; off = F(0)
for clip,a,b,s,z,note in P:
    s = F(s).limit_denominator(100)
    pieces.append(dict(clip=clip,a=a,b=b,s=s,z=z,note=note,off=off,st=q(F(a)/s),du=q(F(b-a)/s),kids=[]))
    off += pieces[-1]["du"]
TOTAL = off

def src2tl(clip, t):
    for p in pieces:
        if p["clip"] == clip and p["a"] - 1e-6 <= t < p["b"] + 1e-6:
            return p["off"] + (F(t) - F(p["a"])) / p["s"]
    raise ValueError(f"{clip}@{t} not in cut")

mode = sys.argv[1]
if mode == "audio":
    tx, outwav = sys.argv[2], sys.argv[3]
    ins, parts = [], []
    for i,p in enumerate(pieces):
        ins += ["-i", f"{tx}/{p['clip']}.wav"]
        f = f"[{i}:a]atrim={p['a']}:{p['b']},asetpts=PTS-STARTPTS"
        if p["s"] != 1: f += f",atempo={float(p['s'])}"
        parts.append(f + f",apad=whole_dur={float(p['du'])},atrim=0:{float(p['du'])}[p{i}]")
    fc = ";".join(parts) + ";" + "".join(f"[p{i}]" for i in range(len(pieces))) + f"concat=n={len(pieces)}:v=0:a=1[o]"
    subprocess.run(["ffmpeg","-v","error","-y",*ins,"-filter_complex",fc,"-map","[o]","-ar","16000","-ac","1",outwav],check=True)
    print("rendered", float(TOTAL)); sys.exit()

v2, wordsf, out = sys.argv[2:5]
PROJECT = sys.argv[5] if len(sys.argv) > 5 else 'ez.romo style'   # same name each round -> re-import with Replace
X = open(v2).read()
X = re.sub(r'(<format id="r1"[^>]*colorSpace=")[^"]*(")', r'\g<1>1-1-1 (Rec. 709)\g<2>', X)  # project always Rec. 709
adur = {m.group(1): F(m.group(2)[:-1]) for m in re.finditer(r'<asset id="a_(IMG_\d+)"[^>]*?duration="([^"]+)"', X)}

def tl2piece(t):
    for p in pieces:
        if p["off"] <= t < p["off"] + p["du"]: return p
    return pieces[-1]
def attach(t, xml):
    t = q(t); p = tl2piece(t)
    p["kids"].append(xml.replace("{OFF}", r(p["st"] + (t - p["off"]))))

# ---------- captions from the v4 render's own transcript ----------
yell0 = pieces[9]["off"]; yell1 = pieces[10]["off"] + pieces[10]["du"]
W = json.load(open(wordsf))
words = []
for s0,e0,t in W:
    w = re.sub(r"[^\w'\-*]", "", t).strip()
    if not w: continue
    if yell0 - 0.05 <= s0 < yell1: continue          # no captions on the scream
    lw = w.lower()
    w = {"bobby":"Babi","riding":"running","sir":"Gen","zhen":"Gen","ride":"run","zhenya's":"Genia's","zhenya":"Genia","times":"10"}.get(lw, w)
    words.append([F(s0).limit_denominator(1000), F(e0).limit_denominator(1000), w.upper()])
# "five ten" / "5 10" -> one card "5-10"
i = 0; m = []
while i < len(words):
    if words[i][2] in ("FIVE","5") and i+1 < len(words) and words[i+1][2] in ("TEN","10"):
        m.append([words[i][0], words[i+1][1], "5-10"]); i += 2; continue
    m.append(words[i]); i += 1
words = m
# lines the transcriber mangles: use the raw-clip word timings instead (source seconds)
RAW = {"IMG_0175":[(3.42,3.60,"WE'RE"),(3.60,3.62,"GETTING"),(3.62,3.94,"WEIRD"),(4.20,4.28,"LET'S"),(4.28,4.44,"GO"),(4.44,4.60,"WEIRD")],
       "IMG_0184":[(13.62,13.92,"WE"),(13.92,14.12,"GOT"),(14.12,14.36,"WEIRD"),(14.40,14.54,"WE"),(14.54,14.80,"GOT"),(14.80,15.14,"WEIRD")]}
for clip, ws in RAW.items():
    ps = [p for p in pieces if p["clip"] == clip and p["a"] <= ws[0][0] < p["b"]]
    t0 = ps[0]["off"]; t1 = ps[0]["off"] + ps[0]["du"]
    words = [w for w in words if not (t0 <= w[0] < t1 - F(1,10) and (clip != "IMG_0184" or w[0] >= src2tl(clip, 13.45)))]
    words += [[src2tl(clip, a), src2tl(clip, b), w] for a,b,w in ws]
words = sorted([w for w in words if w[2] not in ("WHOA",)], key=lambda w: w[0])

EMPH = {"BABI","OAKVILLE","RUN","UNCLE","FIRST","SHOES","WEIRD","EVAN","NEIGHBORHOOD","SMALL","5-10","DISTANCE",
        "GEN","GENIA'S","EARLIER","COUSIN","BROTHER","HOUSE"}
def width(w, size): return len(w) * 1.45 * size   # measured: Arial Black in FCP ~1.45 x fontSize px per capital
def size_for(w):
    base = 48 if any(x in EMPH for x in w.split()) else 40   # Babi v5: 40/48 (72/96 and 50/62 were too big)
    return int(min(base, 590 / (1.45 * max(len(w),1))))       # <=590 px wide: clear of IG buttons (x>845)

caps = []
for i,(s0,e0,w) in enumerate(words):
    t0 = q(s0)
    nxt = q(words[i+1][0]) if i+1 < len(words) else TOTAL
    t1 = min(nxt, q(e0) + F(8,60), TOTAL)
    if t1 - t0 < F(4,60): t1 = t0 + F(4,60)
    if caps and caps[-1][1] > t0: caps[-1][1] = t0
    caps.append([t0, t1, w])
caps = [c for c in caps if c[1] > c[0]]
merged = []; i = 0
while i < len(caps):
    c0,c1,w = caps[i]
    while c1 - c0 < F(5,60) and i+1 < len(caps) and len(w.split()) < 2 and width(w + " " + caps[i+1][2], 40) < 590:
        i += 1; c1 = caps[i][1]; w = w + " " + caps[i][2]
    merged.append([c0,c1,w]); i += 1
caps = merged

TITLE_UID = ".../Titles.localized/Bumper:Opener.localized/Basic Title.localized/Basic Title.moti"
POSKEY = "9999/999166631/999166633/1/100/101"   # units ~1.67 px in 1080x1920
tsn = [0]
def title(t0, t1, text, size, y, lane, font="Arial Black", face="Regular", stroke="-5", name="Caption"):
    tsn[0] += 1; tid = f"ts{tsn[0]}"; lines = text.split("\n")
    body = "".join(f'<text-style ref="{tid}">{l}{"&#10;" if k < len(lines)-1 else ""}</text-style>' for k,l in enumerate(lines))
    attach(t0, f'<title ref="eT" lane="{lane}" offset="{{OFF}}" name="{name} - {lines[0][:24]}" start="3600s" duration="{r(t1-t0)}">'
               f'<param name="Position" key="{POSKEY}" value="0 {y}"/><text>{body}</text>'
               f'<text-style-def id="{tid}"><text-style font="{font}" fontSize="{size}" fontFace="{face}" fontColor="1 1 1 1" '
               f'strokeColor="0 0 0 1" strokeWidth="{stroke}" shadowColor="0 0 0 0.75" shadowOffset="4 315" shadowBlurRadius="5" alignment="center"/></text-style-def></title>')
for c0,c1,w in caps:
    title(c0, c1, w, size_for(w), -252, 1)   # centre y~1380 px (72% down), inside IG safe zone
hook_end = pieces[0]["du"]
title(F(0), hook_end, "Running every day\ntill the end of the year", 42, 368, 2, font="Helvetica Neue", face="Medium", stroke="0", name="Header")   # below the 250 px top band
title(F(0), hook_end, "Day 13", 44, 243, 3, font="Helvetica Neue", face="Medium", stroke="0", name="Header day")
# no persistent tracker after the hook (Babi deleted it in v5)

# ---------- sound: Babi kept only the wow (uncle's shoes) and the final Vine boom; ~2 SFX per 40 s ----------
SND = {
 "boom":  ("vine_boom.mp3", 0.22, 1.30, "-9dB", "SFX vine boom"),
 "horn":  ("air_horn.mp3", 0.24, 1.10, "-10dB", "SFX air horn"),
 "wow":   ("wow.mp3", 0.33, 1.30, "-12dB", "SFX wow"),
 "fly":   ("sfx_pack_kaushal.mp3", 22.82, 0.60, "-10dB", "SFX fly buzz"),
 "whoosh":("sfx_pack_kaushal.mp3", 23.95, 0.65, "-12dB", "SFX whoosh"),
}
used = set()
def sfx(key, t, length=None, lane=-1):
    f,a,ln,vol,name = SND[key]; ln = length if length is not None else ln; used.add(f)
    aid = "s_" + re.sub(r"\W","_", f.rsplit(".",1)[0])
    attach(t, f'<asset-clip ref="{aid}" lane="{lane}" offset="{{OFF}}" name="{name}" start="{r(F(a).limit_denominator(1000))}" '
              f'duration="{r(q(ln))}" audioRole="effects"><adjust-volume amount="{vol}"/></asset-clip>')
T = src2tl
sfx("wow",  T("IMG_0172", 4.85))
b = T("IMG_0184", 22.20); sfx("boom", b, length=min(1.3, float(TOTAL - q(b))))
used.add("music_wii_sports_title.mp3")
attach(F(0), f'<asset-clip ref="s_music_wii_sports_title" lane="-3" offset="{{OFF}}" name="Music - Wii Sports title (bed)" start="1/10s" '
             f'duration="{r(TOTAL)}" audioRole="music"><adjust-volume amount="-19dB"/></asset-clip>')

META = {"vine_boom.mp3":("3088/1000s","48000","2"),"air_horn.mp3":("1645/1000s","44100","1"),"wow.mp3":("4937/1000s","44100","2"),
        "sfx_pack_kaushal.mp3":("63947/1000s","44100","2"),"music_wii_sports_title.mp3":("134420/1000s","44100","2"),
        "sound_effects_main.m4a":("11264/1000s","48000","2")}
res = [f'<effect id="eT" name="Basic Title" uid="{TITLE_UID}"/>']
for f in sorted(used):
    d,rate,ch = META[f]; aid = "s_" + re.sub(r"\W","_", f.rsplit(".",1)[0])
    res.append(f'<asset id="{aid}" name="{f.rsplit(".",1)[0]}" start="0s" duration="{d}" hasAudio="1" audioSources="1" audioChannels="{ch}" '
               f'audioRate="{rate}"><media-rep kind="original-media" src="file://{quote(RUN + "/Sound/" + f)}"/></asset>')
X = X.replace("</resources>", "\n".join(res) + "\n</resources>")

def clipxml(p):
    s = p["s"]; D = adur[p["clip"]]; inner = f'<note>{p["note"]}</note>'
    if s != 1:
        inner += (f'<timeMap preservesPitch="0"><timept time="0s" value="0s" interp="linear"/>'
                  f'<timept time="{r(D/s)}" value="{r(D)}" interp="linear"/></timeMap>')
    if p["z"]:
        sc,x,y = p["z"]; inner += f'<adjust-transform position="{x} {y}" scale="{sc} {sc}"/>'
    inner += "".join(p["kids"])
    return (f'<asset-clip ref="a_{p["clip"]}" name="{p["clip"]}" offset="{r(p["off"])}" start="{r(p["st"])}" '
            f'duration="{r(p["du"])}" tcFormat="NDF" audioRole="dialogue">{inner}</asset-clip>')
proj = (f'<project name="{PROJECT}"><sequence format="r1" duration="{r(TOTAL)}" tcStart="0s" tcFormat="NDF" '
        f'audioLayout="stereo" audioRate="48k"><spine>\n' + "\n".join(clipxml(p) for p in pieces) + '\n</spine></sequence></project>')
X = re.sub(r'<project name=.*?</project>', '', X, flags=re.S).replace("</event>", proj + "</event>")
open(out, "w").write(X)
print(f"total {float(TOTAL):.2f}s, {len(pieces)} pieces, {len(caps)} captions, max caption width "
      f"{max(width(w, size_for(w)) for _,_,w in caps):.0f}px")
json.dump([[float(a),float(b),w] for a,b,w in caps], open(out.replace(".fcpxml","_captions.json"),"w"))
