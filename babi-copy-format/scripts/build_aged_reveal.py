"""Aged-reveal reel builder ("How long have you been working here", Nov 16 2026). Edit P / ANS for new footage.
Needs AI stills named AI_NN_<name>.png in <folder>/AI Frames and grab (shared/tools/grab_sdr_frame.swift, compiled next to this script's parent).
Babi's final changed: Mozart bed ~-9 dB, pop on every AI cut, AI hold ~1.0 s, captions "Name\n(Role)" FCP ~60 pt. Update those defaults before reuse.
"""
import subprocess, json, os, numpy as np
from fractions import Fraction as F
from urllib.parse import quote
from PIL import ImageFont
D = "/Volumes/4TBSSD_4/Babi NR Content/Media/OFFICE/How long have you been working here?"
AI = D + "/AI Frames"; os.makedirs(AI, exist_ok=True); os.makedirs(D + "/XML", exist_ok=True)
GRAB = os.path.join(os.path.dirname(__file__), "..", "grab")
PROJECT = "How Long Have You Been Working Here"
AI_LEN = F(13, 10)   # reference AI holds 1.03-1.87 s, median ~1.3 s   # 1.6 s aged clip after each answer (reference: ~1.2-1.8 s)
# answer start (source s) -> punch-in jump cut 0.15 s before it (reference: wide intro, close-up for the answer)
ANS = {"IMG_0519":3.04,"IMG_0512":3.24,"IMG_0516":2.52,"IMG_0521":3.28,"IMG_0518":4.36,"IMG_0511":2.12,"IMG_0517":2.80,
       "IMG_0522":4.28,"IMG_0515":2.40,"IMG_0510":3.84,"IMG_0514":4.32,"IMG_0509":6.16,"IMG_0513":4.46}
PUNCH = "1.2"
TAIL = 0.25   # reaction beat after the answer before the AI cut (reference ~0.3 s)
# name, clip, [(in,out)...], answer, AI age prompt
P = [
 ("Alex",   "IMG_0519", [(0.68,3.65)],              "Seven months",          "a 7-month-old baby"),
 ("Rick",   "IMG_0512", [(0.00,0.55),(1.10,3.95)],  "Seven years",           "a 7-year-old child"),
 ("Kat",    "IMG_0516", [(0.58,3.25)],              "Four years",            "a 4-year-old child"),
 ("Rashid", "IMG_0521", [(0.78,3.75)],              "Ten years",             "a 10-year-old child"),
 ("Tyler",  "IMG_0518", [(1.22,2.95),(4.22,5.45)],  "Three and a half years","a 3-and-a-half-year-old child"),
 ("NAME?",  "IMG_0511", [(0.32,2.85)],              "Four years",            "a 4-year-old child"),
 ("Jake",   "IMG_0517", [(0.00,3.30)],              "Seven years",           "a 7-year-old child"),
 ("Brandon","IMG_0522", [(2.06,5.15)],              "About two and a half",  "a 2-and-a-half-year-old toddler"),
 ("Ali",    "IMG_0515", [(0.36,3.05)],              "Four years",            "a 4-year-old child"),
 ("NAME?",  "IMG_0510", [(0.00,1.75),(3.72,5.90)],  "Two and a half years",  "a 2-and-a-half-year-old toddler"),
 ("NAME?",  "IMG_0514", [(3.08,6.55)],              "10 15 years maybe",     "a 12-year-old kid"),
 ("Stu",    "IMG_0509", [(2.20,3.75),(6.05,7.20)],  "Since the beginning",   "a newborn baby"),
 ("Andrew", "IMG_0513", [(2.50,5.45)],              "Since I was a baby",    "a baby about 9 months old"),
]
TB = 60
def q(x): return F(round(F(x) * TB), TB)
def r(f):
    f = F(f); return f"{f.numerator}/{f.denominator}s" if f.denominator != 1 else f"{f.numerator}s"

def refine_out(path, a, b):
    """end = last loud 10 ms frame near b + 0.12 s (whisper times run long/short)"""
    x = np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i",path,"-ac","1","-ar","16000","-f","f32le","-"],capture_output=True).stdout, np.float32)
    rms = 20*np.log10(np.sqrt(np.convolve(x**2, np.ones(160)/160, "same"))[::160] + 1e-9)
    floor = np.percentile(rms, 10) + 8
    lo, hi = int((b-0.6)*100), min(int((b+0.4)*100), len(rms)-1)
    loud = [i for i in range(lo, hi) if rms[i] > floor]
    return min(round(loud[-1]/100 + 0.12, 2), b + 0.3) if loud else b

probe = {}
for _,c,_,_,_ in P:
    if c in probe: continue
    j = json.loads(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","json",f"{D}/{c}.MOV"],capture_output=True,text=True).stdout)
    probe[c] = F(j["format"]["duration"]).limit_denominator(600)

font = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 100, index=1)  # Bold
def fcp_size(text, maxw=560, base=46):
    w100 = font.getlength(text) * 1.34       # FCP Helvetica Neue Bold ~1.34 x PIL width at same size
    return min(base, int(maxw * 100 / w100))

spine = []; off = F(0); rows = []
TITLE_UID = ".../Titles.localized/Bumper:Opener.localized/Basic Title.localized/Basic Title.moti"
POSKEY = "9999/999166631/999166633/1/100/101"
for k,(name,c,segs,ans,age) in enumerate(P):
    path = f"{D}/{c}.MOV"
    segs = [(a, min(refine_out(path,a,b) + TAIL, float(probe[c]) - 0.05) if i == len(segs)-1 else b) for i,(a,b) in enumerate(segs)]
    p = ANS[c] - 0.15; sp = []
    for a,b in segs:
        if a + 0.4 < p < b - 0.3: sp += [(a,p),(p,b)]
        else: sp.append((a,b))
    segs = sp
    person0 = off; first = True
    real_len = sum(q(b)-q(a) for a,b in segs)
    for a,b in segs:
        st, du = q(a), q(b)-q(a)
        kids = f'<adjust-transform scale="{PUNCH} {PUNCH}"/>' if a >= p - 0.4 else ""
        if first:
            label = f"{name} (ROLE)"
            sz = fcp_size(label)
            kids += (f'<title ref="eT" lane="1" offset="{r(st)}" name="Name - {name}" start="3600s" duration="{r(real_len)}">'
                    f'<param name="Position" key="{POSKEY}" value="0 -219"/><text><text-style ref="ts{k}">{label}</text-style></text>'
                    f'<text-style-def id="ts{k}"><text-style font="Helvetica Neue" fontSize="{sz}" fontFace="Bold" fontColor="1 1 1 1" '
                    f'shadowColor="0 0 0 0.6" shadowOffset="3 315" shadowBlurRadius="6" alignment="center"/></text-style-def></title>')
            first = False
        if not spine:
            kids += (f'<asset-clip ref="m_song" lane="-1" offset="{r(st)}" name="Music - Fun Fun Fun (bed)" start="0s" duration="{{TOTAL}}" audioRole="music">'
                     f'<adjust-volume amount="-24dB"/></asset-clip>')
        spine.append(f'<asset-clip ref="a_{c}" name="{c} {name}" offset="{r(off)}" start="{r(st)}" duration="{r(du)}" tcFormat="NDF" audioRole="dialogue">{kids}</asset-clip>')
        off += du
    # source frame for the AI version = last frame of the answer
    png = f"{AI}/{k+1:02d} {name.replace('?','')} {c}.png"
    t_grab = float(segs[-1][1]) - 0.1
    subprocess.run([GRAB, path, f"{t_grab:.2f}", png], check=True, capture_output=True)
    pid = f"p{k}"
    import glob
    ai = glob.glob(f"{AI}/AI_{k+1:02d}_*.png")
    if name == "Stu" or not ai:
        rows.append(dict(n=k+1, name=name, clip=c, answer=ans, age=None, frame=None, t=0, tl=float(off))); continue
    png = ai[0]
    zoom = (f'<adjust-transform scale="1 1"><param name="scale"><keyframeAnimation>'
            f'<keyframe time="0s" value="1 1"/><keyframe time="{r(AI_LEN)}" value="1.06 1.06"/></keyframeAnimation></param></adjust-transform>')
    spine.append(f'<video ref="{pid}" name="AI {name} as {age}" offset="{r(off)}" start="0s" duration="{r(AI_LEN)}">'
                 f'{zoom}<asset-clip ref="s_pop" lane="-2" offset="0s" name="SFX pop (AI reveal)" start="1693/100s" duration="2/5s" audioRole="effects"><adjust-volume amount="-1dB"/></asset-clip><marker start="0s" duration="1/60s" value="AI: {name} as {age}"/></video>')
    rows.append(dict(n=k+1, name=name, clip=c, answer=ans, age=age, frame=png, t=round(t_grab,2), tl=float(off)))
    off += AI_LEN
TOTAL = off
spine = [x.replace("{TOTAL}", r(TOTAL)) for x in spine]

res = ['<format id="r1" frameDuration="100/6000s" width="1080" height="1920" colorSpace="1-1-1 (Rec. 709)"/>',
       '<format id="rv" frameDuration="100/6000s" width="1080" height="1920" colorSpace="9-18-9 (Rec. 2020 HLG)"/>',
       '<format id="ri" name="FFVideoFormatRateUndefined" width="1080" height="1920" colorSpace="1-1-1 (Rec. 709)"/>',
       f'<effect id="eT" name="Basic Title" uid="{TITLE_UID}"/>']
for c,d in probe.items():
    res.append(f'<asset id="a_{c}" name="{c}" start="0s" duration="{r(d)}" hasVideo="1" format="rv" hasAudio="1" videoSources="1" audioSources="1" audioChannels="2" audioRate="48000">'
               f'<media-rep kind="original-media" src="file://{quote(D + "/" + c + ".MOV")}"/></asset>')
res.append(f'<asset id="s_pop" name="pop_pack" start="0s" duration="17879/1000s" hasAudio="1" audioSources="1" audioChannels="2" audioRate="48000">'
           f'<media-rep kind="original-media" src="file://{quote(D + "/Sound/pop_pack.mp3")}"/></asset>')
res.append(f'<asset id="m_song" name="fun_fun_fun" start="0s" duration="205960/1000s" hasAudio="1" audioSources="1" audioChannels="2" audioRate="48000">'
           f'<media-rep kind="original-media" src="file://{quote(D + "/Sound/fun_fun_fun.mp3")}"/></asset>')
for k,row in enumerate(rows):
    if not row["frame"]: continue
    res.append(f'<asset id="p{k}" name="{os.path.basename(row["frame"])[:-4]}" start="0s" duration="0s" hasVideo="1" format="ri" videoSources="1">'
               f'<media-rep kind="original-media" src="file://{quote(row["frame"])}"/></asset>')
X = ('<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE fcpxml>\n<fcpxml version="1.11"><resources>\n' + "\n".join(res) + '\n</resources>\n'
     '<library location="file:///Volumes/4TBSSD_4/Babi%20NR%20Content/Libraries/TME.fcpbundle/" colorProcessing="wide-hdr">'
     '<event name="Nov 16 How long have you been working here">'
     f'<project name="{PROJECT}"><sequence format="r1" duration="{r(TOTAL)}" tcStart="0s" tcFormat="NDF" audioLayout="stereo" audioRate="48k"><spine>\n'
     + "\n".join(spine) + '\n</spine></sequence></project></event></library></fcpxml>\n')
out = f"{D}/XML/{PROJECT}.fcpxml"; open(out,"w").write(X)
json.dump(rows, open(f"{D}/XML/ai_plan.json","w"), indent=1)
print(f"total {float(TOTAL):.2f}s -> {out}")
for row in rows: print(row["n"], row["name"], row["clip"], "|", row["answer"], "->", row["age"], "@", row["t"])
