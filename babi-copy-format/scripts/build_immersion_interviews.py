"""Immersion Day guest interviews (Nov 18 2026 footage, built 2026-11-20). Mashed-up two-guest testimonial in the style of
stumclaren Dd_4J8nDRoA (alternating one-line answers), following Babi's brief: hook -> who -> pain -> moment -> payoff -> close -> end card.
Mike = IMG_0820, Lisa = IMG_0821 (locked-off couch two-shots, guest on the right). Segments live in XML/Interviews/segments.py.
Captions: 2-3 word chunks, Avenir Next Heavy caps, KEY words yellow, timed from whole-take medium.en word timings
(slice transcription with initial_prompt repeated words, so don't use it). Writes one FCPXML with 3 projects + the new browser clips."""
import subprocess, json, os, re, sys
from fractions import Fraction as F
from urllib.parse import quote
from PIL import Image, ImageDraw, ImageFont
D = "/Volumes/4TBSSD_4/Babi NR Content/Media/OFFICE/November 18th Immersion Day"
X = f"{D}/XML/Interviews"; sys.path.insert(0, X)
from segments import S
EVENT = "November 18th Immersion Day"
PROJECTS = {   # name -> segment order
 "Immersion Day Interviews": [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,19,16,17,18],
 "Immersion Day - Mike":     [1,4,9,12,13,11],
 "Immersion Day - Lisa":     [2,5,6,7,8,10,17,18],
}
GUEST = {"IMG_0820": ("MIKE", "Membership.io customer"), "IMG_0821": ("LISA", "Membership.io customer")}
GAIN = {"IMG_0820": 11, "IMG_0821": 8}          # dialogue: Mike -27.7 LUFS, Lisa -23.8 LUFS raw -> ~-16
GUEST_X = {"IMG_0820": 810, "IMG_0821": 840}; GUEST_Y = 1040; HOST_X = 410   # face centres in the 1080x1920 frame
HOST_SEGS = {12}                                  # Babi asking: zoom on him, no label
BROLL = {4: ("IMG_0819", 2.0, 3.4, 2.6), 16: ("IMG_0736", 9.0, 0.0, 1.5)}   # seg -> (clip, src in, offset in seg, dur), video only
MUSIC_FILE, MUSIC_IN, MUSIC_DB = f"{D}/Sound/Ivory Check-in.mp3", 0.0, -14   # song -14.2 LUFS -> ~12 LU under speech
END_DUR = F(5, 2)
KEY = {"BLOWN","SPEECHLESS","MARS","PROMPT","BACKEND","FASTER","PHONE","WEBSITE","BRANDING","DONE","DAYS","FRACTION","EMAIL",
       "WORDPRESS","ZAPIER","FIVE","CANCEL","MONTHLY","LAUNCH","DAY","LANDING","MINUTES","COMPREHEND","LEVEL","WAIT","NOTHER"}
YELLOW = "1 0.835 0.149 1"
CAP_SIZE, CAP_Y, MAXC = 30, -140, 15             # calibrated in shake hands: ~38 px/letter, -140 ~ 62% down
TB = 60
def q(x): return F(round(F(str(x)) * TB), TB)
def q5994(x): n = round(F(str(x)) * F(60000, 1001)); return n * F(1001, 60000)
def r(f):
    f = F(f); return f"{f.numerator}/{f.denominator}s" if f.denominator != 1 else f"{f.numerator}s"
def esc(s): return s.replace("&","&amp;").replace("<","&lt;").replace('"',"&quot;")
def font(size, face="Heavy"):
    for i in range(16):
        try:
            ff = ImageFont.truetype("/System/Library/Fonts/Avenir Next.ttc", size, index=i)
            if ff.getname() == ("Avenir Next", face): return ff
        except Exception: pass

# ---- end card
os.makedirs(f"{D}/Graphics", exist_ok=True); endp = f"{D}/Graphics/end_card_membership_io.png"
im = Image.new("RGB", (1080,1920), (14,17,22)); d = ImageDraw.Draw(im)
d.text((540, 900), "Membership.io", font=font(104), fill=(255,255,255), anchor="mm")
d.text((540, 1030), "member.dev", font=font(64, "Demi Bold"), fill=(255,213,38), anchor="mm")
im.save(endp)

# ---- words (whole-take medium.en) per segment
WT = {c: [w for s in json.load(open(f"{X}/{c}.MOV.json")) for w in s["words"]] for c in GUEST}
def seg_words(k):
    c, a, b, z, txt = S[k]; out = []
    for s0, e0, t in WT[c]:
        if a <= (s0+e0)/2 < b or min(e0,b) - max(s0,a) >= 0.12:
            stop = bool(re.search(r"[.,?!]$", t.strip()))
            t = re.sub(r"[.,?!]", "", t.strip()).upper().replace("-", "")
            if t: out.append([max(s0,a), min(e0,b), t, stop])
    return out
def chunks_for(k):
    ch = []; W = seg_words(k)
    for i,w in enumerate(W):
        if ch:
            last = ch[-1]; n = len(" ".join(x[2] for x in last)) + 1 + len(w[2])
            ends = w[3] or i == len(W)-1          # last word of a sentence/segment may stretch the chunk so it isn't orphaned
            if not last[-1][3] and w[0]-last[-1][1] < 0.5 and (len(last) < 3 and n <= MAXC or ends and len(w[2]) <= 3 and n <= 18):
                last.append(w); continue
        ch.append([w])
    return ch

# ---- resources
dur = {}
for f in sorted(os.listdir(D)):
    m = re.match(r"IMG_0(8(1[89]|2\d|3[01]))\.MOV$", f)
    if m or f in ("IMG_0736.MOV",):
        j = json.loads(subprocess.run(["ffprobe","-v","error","-select_streams","v:0","-show_entries","stream=r_frame_rate:format=duration","-of","json",f"{D}/{f}"],capture_output=True,text=True).stdout)
        dur[f[:-4]] = (F(j["format"]["duration"]).limit_denominator(600), j["streams"][0]["r_frame_rate"])
res = ['<format id="r1" frameDuration="100/6000s" width="1080" height="1920" colorSpace="1-1-1 (Rec. 709)"/>',
       '<format id="rv" frameDuration="100/6000s" width="1080" height="1920" colorSpace="9-18-9 (Rec. 2020 HLG)"/>',
       '<format id="rv5994" frameDuration="1001/60000s" width="1080" height="1920" colorSpace="9-18-9 (Rec. 2020 HLG)"/>',
       '<format id="ri" name="FFVideoFormatRateUndefined" width="1080" height="1920" colorSpace="1-1-1 (Rec. 709)"/>',
       '<effect id="eT" name="Basic Title" uid=".../Titles.localized/Bumper:Opener.localized/Basic Title.localized/Basic Title.moti"/>']
def fmt(c): return "rv5994" if dur[c][1].startswith("60000") else "rv"
for c,(dd,_) in dur.items():
    res.append(f'<asset id="a_{c}" name="{c}" start="0s" duration="{r(dd)}" hasVideo="1" format="{fmt(c)}" hasAudio="1" videoSources="1" audioSources="1" audioChannels="2" audioRate="48000">'
               f'<media-rep kind="original-media" src="file://{quote(D + "/" + c + ".MOV")}"/></asset>')
res.append(f'<asset id="aMusic" name="Ivory Check-in" start="0s" duration="{r(q(239.7))}" hasAudio="1" audioSources="1" audioChannels="2" audioRate="48000">'
           f'<media-rep kind="original-media" src="file://{quote(MUSIC_FILE)}"/></asset>')
res.append(f'<asset id="pEnd" name="end_card_membership_io" start="0s" duration="0s" hasVideo="1" format="ri" videoSources="1">'
           f'<media-rep kind="original-media" src="file://{quote(endp)}"/></asset>')
POSKEY = "9999/999166631/999166633/1/100/101"
tid = 0
def cap_title(ch, off_parent, dd):
    global tid
    runs = "".join(f'<text-style ref="ts{tid}{"y" if w[2] in KEY else "w"}">{esc(w[2])}{" " if i < len(ch)-1 else ""}</text-style>' for i,w in enumerate(ch))
    st_ = lambda col: (f'<text-style font="Avenir Next" fontSize="{CAP_SIZE}" fontFace="Heavy" fontColor="{col}" bold="1" strokeColor="0 0 0 1" '
                       f'strokeWidth="-2" shadowColor="0 0 0 0.75" shadowOffset="3 315" shadowBlurRadius="5" alignment="center"/>')
    defs = f'<text-style-def id="ts{tid}w">{st_("1 1 1 1")}</text-style-def><text-style-def id="ts{tid}y">{st_(YELLOW)}</text-style-def>'
    x = (f'<title ref="eT" lane="2" offset="{r(off_parent)}" name="{esc(" ".join(w[2] for w in ch))}" start="3600s" duration="{r(dd)}">'
         f'<param name="Position" key="{POSKEY}" value="0 {CAP_Y}"/><text>{runs}</text>{defs}</title>')
    tid += 1; return x
def label_title(name, role, off_parent, dd):
    global tid
    st_ = lambda sz, face, col: (f'<text-style font="Avenir Next" fontSize="{sz}" fontFace="{face}" fontColor="{col}" strokeColor="0 0 0 1" strokeWidth="-1.5" '
                                 f'shadowColor="0 0 0 0.75" shadowOffset="3 315" shadowBlurRadius="5" alignment="center"/>')
    x = (f'<title ref="eT" lane="3" offset="{r(off_parent)}" name="Label {name}" start="3600s" duration="{r(dd)}">'
         f'<param name="Position" key="{POSKEY}" value="0 260"/><text><text-style ref="ts{tid}n">{name}\n</text-style><text-style ref="ts{tid}r">{esc(role)}</text-style></text>'
         f'<text-style-def id="ts{tid}n">{st_(40,"Heavy",YELLOW)}</text-style-def><text-style-def id="ts{tid}r">{st_(22,"Demi Bold","1 1 1 1")}</text-style-def></title>')
    tid += 1; return x
def zoom_xml(k):
    c, a, b, s, _ = S[k]
    if s == 1.0: return ""
    cx = HOST_X if k in HOST_SEGS else GUEST_X[c]
    lim = (s-1)*540/s; dx = max(-lim, min(lim, cx-540)); limy = (s-1)*960/s; dy = max(-limy, min(limy, GUEST_Y-960))
    return f'<adjust-transform position="{-s*dx/19.2:.3f} {s*dy/19.2:.3f}" scale="{s} {s}"/>'

def project(name, order):
    spine = []; off = F(0); seen = set(); plan = []
    segs = [(k, q(S[k][1]), q(S[k][2])) for k in order]
    total = sum(b-a for _,a,b in segs) + END_DUR
    for i,(k,st,en) in enumerate(segs):
        c = S[k][0]; du = en - st; kids = zoom_xml(k)
        kids += f'<adjust-volume amount="{GAIN[c]}dB"/>'
        if i == 0:
            kids += (f'<asset-clip ref="aMusic" lane="-1" offset="{r(st)}" name="Ivory Check-in" start="{r(q(MUSIC_IN))}" duration="{r(total)}" audioRole="music">'
                     f'<adjust-volume amount="{MUSIC_DB}dB"><param name="amount"><fadeOut type="easeIn" duration="2s"/></param></adjust-volume></asset-clip>')
        if k in BROLL:
            bc, bin_, bo, bd = BROLL[k]
            bst = q5994(bin_) if fmt(bc) == "rv5994" else q(bin_)
            kids += f'<asset-clip ref="a_{bc}" lane="1" offset="{r(st + q(bo))}" name="B-roll {bc}" start="{r(bst)}" duration="{r(q(bd))}" srcEnable="video" tcFormat="NDF"/>'
        if c not in seen and k not in HOST_SEGS:
            seen.add(c); kids += label_title(*GUEST[c], st, min(du, F(5,2)))
        CH = chunks_for(k)
        for j,ch in enumerate(CH):
            t0 = max(q(ch[0][0]) - F(2,60), st)
            t1 = min(q(CH[j+1][0][0]) - F(2,60), q(ch[-1][1] + 0.4)) if j+1 < len(CH) else en
            if t1 - t0 >= F(4,60): kids += cap_title(ch, t0, t1 - t0)
        spine.append(f'<asset-clip ref="a_{c}" name="{k:02d} {esc(S[k][4][:40])}" offset="{r(off)}" start="{r(st)}" duration="{r(du)}" tcFormat="NDF" audioRole="dialogue">{kids}</asset-clip>')
        plan.append((k, c, float(st), float(en), float(off))); off += du
    spine.append(f'<video ref="pEnd" offset="{r(off)}" name="End card" start="0s" duration="{r(END_DUR)}"/>')
    xml = (f'<project name="{name}"><sequence format="r1" duration="{r(total)}" tcStart="0s" tcFormat="NDF" audioLayout="stereo" audioRate="48k"><spine>\n'
           + "\n".join(spine) + '\n</spine></sequence></project>')
    return xml, total, plan

projs = []; plans = {}
for name, order in PROJECTS.items():
    xml, total, plan = project(name, order); projs.append(xml); plans[name] = plan
    print(f"{name}: {float(total):.2f}s")
# browser clips for every new AirDropped clip (IMG_0818-0831); IMG_0736 is already in the event
evclips = [f'<asset-clip ref="a_{c}" name="{c}" start="0s" duration="{r(dd)}" format="{fmt(c)}" tcFormat="NDF" audioRole="dialogue"/>'
           for c,(dd,_) in dur.items() if c != "IMG_0736"]
out = ('<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE fcpxml>\n<fcpxml version="1.11"><resources>\n' + "\n".join(res) + '\n</resources>\n'
       '<library colorProcessing="wide-hdr">'
       f'<event name="{EVENT}">\n' + "\n".join(evclips) + "\n" + "\n".join(projs) + '\n</event></library></fcpxml>\n')
op = f"{X}/Immersion Day Interviews.fcpxml"; open(op, "w").write(out)
json.dump(plans, open(f"{X}/cut_plan.json", "w"), indent=1)
print(tid, "titles ->", op)
for k in PROJECTS["Immersion Day Interviews"]: print(k, " | ".join(" ".join(w[2] for w in ch) for ch in chunks_for(k)))
