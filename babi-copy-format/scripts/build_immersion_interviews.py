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
MAIN_ORDER = [1,2,3,4,5,6,7,8,9,10,20,21,22,11,12,13,14,15,19,16,17,18]
PROJECTS = {   # name -> segment order
 "Immersion Day Interviews": MAIN_ORDER,
 "Immersion Day - Mike":     [1,4,9,12,13,11],
 "Immersion Day - Lisa":     [2,5,6,7,8,10,20,21,22,17,18],
 # v3 (Babi 2026-11-20): second version opens on the bleeped tease "You mean I can get rid of [beep] [beep]?", then the main cut
 "Immersion Day Interviews - Bleep Hook": [24,20,22] + MAIN_ORDER,
}
# company names are bleeped (1 kHz tone, dialogue muted) and their caption is a blurred image "to make people wonder"
BLEEP = {20: "WORDPRESS", 22: "ZAPIER"}
BLEEP_FILE, BLEEP_DB = f"{D}/Sound/bleep_1khz.wav", -6
GUEST = {"IMG_0820": ("MIKE", "Membership.io customer"), "IMG_0821": ("LISA", "Membership.io customer")}
GAIN = {"IMG_0820": 0, "IMG_0821": 0}      # Babi 2026-11-27: no automatic boost (was +11/+8)
GUEST_X = {"IMG_0820": 810, "IMG_0821": 840}; GUEST_Y = 1040; HOST_X = 410   # face centres in the 1080x1920 frame
HOST_SEGS = {12}                                  # Babi asking: zoom on him, no label
# B-roll (v3, Babi 2026-11-20). Who's who (from the clips' own audio): Stu = navy shirt at the whiteboard; Rick = younger guy in
# black cap + Membership.io jacket (slides, AI-by-text demo); Andrew = older cap guy, blue shirt (IMG_0818/0819 with Mike).
# v3 rules from Babi's own trims of v2: shots ~0.7-1.4 s, the guest's face comes back BETWEEN shots inside a line (B-roll must not cover
# all of Mike's talking), only steady shots (global shake <= ~0.5 px/frame at 144 px wide, scripts in the skill), every B-roll muted.
# seg -> [(start in seg, end in seg, clip, src in)]; relative to the segment so every project reuses it.
BROLL = {
 3:  [(1.04, 2.15, "IMG_0802", 1.0)],                                   # "gone to Mars" -> Lisa watching, chin on hands (steady)
 4:  [(1.23, 2.18, "IMG_0787", 0.3), (3.65, 4.60, "IMG_0819", 2.0), (6.20, 7.43, "IMG_0818", 0.5)],   # Babi's v2 trims: Rick "Just ask." slide, Andrew+Mike x2
 5:  [(0.20, 1.10, "IMG_0763", 1.0), (2.68, 4.07, "IMG_0807", 3.5)],   # "done so much faster" -> Stu explaining; Babi's pick: text thread on the TV                                   # Babi's pick: "texting it to my phone" -> the text thread on the TV
 9:  [(1.17, 2.07, "IMG_0745", 1.0), (3.24, 4.22, "IMG_0776", 5.5)],    # Mike listening, Mike chin on hand
 10: [(0.13, 1.00, "IMG_0829", 6.0), (2.15, 2.97, "IMG_0779", 10.5)],   # Lisa standing, talking; "email service provider" -> Stu, arms open                                  # "email service provider" -> Stu, arms open
 21: [(0.06, 1.00, "IMG_0794", 0.5)],                                   # "you mean I can get rid of" -> Lisa filming it on her phone (steady)
 11: [(0.98, 1.90, "IMG_0796", 0.8), (3.06, 4.00, "IMG_0742", 1.5)],    # Mike in the boardroom
 12: [(1.67, 2.67, "IMG_0786", 3.5), (2.67, 4.01, "IMG_0792", 3.5)],    # Babi asks "launch it" -> "The next Membership.io", Rick smiling
 14: [(1.22, 1.90, "IMG_0747", 1.0)],                                   # "landing pages" -> Lisa at the table
 16: [(1.20, 2.16, "IMG_0775", 5.5), (2.16, 2.95, "IMG_0801", 9.5)],    # "unless you see it" -> Stu grinning, Stu excited
 17: [(0.00, 0.93, "IMG_0764", 8.0)],                                   # "whole nother level" -> Stu gesturing (steady; 0776 @22 was shaky)
}
BZOOM = {"IMG_0806": (1.3, 0, -15.0)}   # (scale, x, y): crop the bald head in the foreground, keep Rick + phone
BEATS = json.load(open(f"{X}/beats.json"))   # librosa beat times - 0.04 s (FCP Option-B grid); music starts at song 0 = timeline 0
UIDS = json.load(open(f"{X}/fcp_uids.json"))  # media already in the library (read from the event DB) -> reuse, no duplicates
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

# ---- bleep tone + blurred caption images (v3)
if not os.path.exists(BLEEP_FILE):
    subprocess.run(["ffmpeg","-v","error","-y","-f","lavfi","-i","sine=frequency=1000:sample_rate=48000:duration=3","-af","volume=0.5","-ac","2",BLEEP_FILE], check=True)
from PIL import ImageFilter
BLURP = {}
CAP_PX, CAP_CY = 54, 1184     # FCP Avenir Next Heavy 30 at Position 0 -140 ~ PIL 75 px, centre y 1184 (measured in the viewer)
for k, word in BLEEP.items():
    im = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.text((540, CAP_CY), word, font=font(CAP_PX), fill=(255, 213, 38, 255), anchor="mm", stroke_width=4, stroke_fill=(0, 0, 0, 255))
    im = im.filter(ImageFilter.GaussianBlur(9))
    BLURP[k] = f"{D}/Graphics/blur_{word.lower()}.png"; im.save(BLURP[k])

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

# ---- resources: EVERY file in the day folder becomes an asset + a browser clip (Babi: "import all the videos, then choose B-roll")
def probe(path):
    j = json.loads(subprocess.run(["ffprobe","-v","error","-show_entries","stream=codec_type,width,height,r_frame_rate,color_transfer:stream_side_data=rotation:format=duration",
                                   "-of","json",path],capture_output=True,text=True).stdout)
    vs = [s for s in j["streams"] if s["codec_type"] == "video"]; v = vs[0]
    rot = any(abs(int(sd.get("rotation", 0))) == 90 for sd in v.get("side_data_list", []))
    w, h = (v["height"], v["width"]) if rot else (v["width"], v["height"])
    return dict(rate=v["r_frame_rate"], w=w, h=h, hlg=v.get("color_transfer") == "arib-std-b67",
                audio=any(s["codec_type"] == "audio" for s in j["streams"]), dur=F(j["format"].get("duration", "0")).limit_denominator(600))
dur, fmts = {}, {}
res = ['<format id="r1" frameDuration="100/6000s" width="1080" height="1920" colorSpace="1-1-1 (Rec. 709)"/>',
       '<format id="ri" name="FFVideoFormatRateUndefined" width="1080" height="1920" colorSpace="1-1-1 (Rec. 709)"/>',
       '<effect id="eT" name="Basic Title" uid=".../Titles.localized/Bumper:Opener.localized/Basic Title.localized/Basic Title.moti"/>']
FILES = sorted(f for f in os.listdir(D) if not f.startswith(".") and os.path.isfile(f"{D}/{f}") and f.lower().endswith((".mov",".mp4",".m4v",".heic")))
def aid(c): return "a_" + re.sub(r"\W", "_", c)
def uid(c): return f' uid="{UIDS[c]}"' if c in UIDS else ""
for f in FILES:
    c = os.path.splitext(f)[0]; p = probe(f"{D}/{f}")
    if f.lower().endswith(".heic"):
        res.append(f'<format id="f_{c}" name="FFVideoFormatRateUndefined" width="{p["w"]}" height="{p["h"]}"/>')
        res.append(f'<asset id="a_{c}" name="{c}" start="0s" duration="0s" hasVideo="1" format="f_{c}" videoSources="1">'
                   f'<media-rep kind="original-media" src="file://{quote(D + "/" + f)}"/></asset>')
        dur[c] = (None, None); continue
    n, d_ = map(int, p["rate"].split("/")); cs = "9-18-9 (Rec. 2020 HLG)" if p["hlg"] else "1-1-1 (Rec. 709)"
    key = (n, d_, p["w"], p["h"], cs)
    if key not in fmts:
        fmts[key] = f"rv{len(fmts)}"
        res.append(f'<format id="{fmts[key]}" frameDuration="{d_}/{n}s" width="{p["w"]}" height="{p["h"]}" colorSpace="{cs}"/>')
    a = ' hasAudio="1" audioSources="1" audioChannels="2" audioRate="48000"' if p["audio"] else ""
    res.append(f'<asset id="{aid(c)}" name="{esc(c)}"{uid(c)} start="0s" duration="{r(p["dur"])}" hasVideo="1" format="{fmts[key]}" videoSources="1"{a}>'
               f'<media-rep kind="original-media" src="file://{quote(D + "/" + f)}"/></asset>')
    dur[c] = (p["dur"], p["rate"]); dur[c + "_fmt"] = fmts[key]
res.append(f'<asset id="aMusic" name="Ivory Check-in"{uid("Ivory Check-in")} start="0s" duration="{r(q(239.7))}" hasAudio="1" audioSources="1" audioChannels="2" audioRate="48000">'
           f'<media-rep kind="original-media" src="file://{quote(MUSIC_FILE)}"/></asset>')
for k, pth in BLURP.items():
    res.append(f'<asset id="pBlur{k}" name="{os.path.basename(pth)[:-4]}" start="0s" duration="0s" hasVideo="1" format="ri" videoSources="1">'
               f'<media-rep kind="original-media" src="file://{quote(pth)}"/></asset>')
res.append(f'<asset id="aBleep" name="bleep_1khz" start="0s" duration="3s" hasAudio="1" audioSources="1" audioChannels="2" audioRate="48000">'
           f'<media-rep kind="original-media" src="file://{quote(BLEEP_FILE)}"/></asset>')
res.append(f'<asset id="pEnd" name="end_card_membership_io"{uid("end_card_membership_io")} start="0s" duration="0s" hasVideo="1" format="ri" videoSources="1">'
           f'<media-rep kind="original-media" src="file://{quote(endp)}"/></asset>')
def fmt(c): return dur[c + "_fmt"]
def qsrc(c, t):   # frame-align a source time to the clip's own rate
    n, d_ = map(int, dur[c][1].split("/")); k = round(F(str(t)) * n / d_); return k * F(d_, n)
def broll_xml(k, st, du):
    """Connected, muted B-roll for segment k (seg-relative). st = the segment's source start (parent time base)."""
    out = ""
    for a0, b0, c, sin in BROLL.get(k, []):
        o = q(a0); d = min(q(b0), du) - o
        z = BZOOM.get(c); zx = f'<adjust-transform position="{z[1]} {z[2]}" scale="{z[0]} {z[0]}"/>' if z else ""
        out += (f'<asset-clip ref="a_{c}" lane="1" offset="{r(st + o)}" name="B-roll {c}" start="{r(qsrc(c, sin))}" duration="{r(d)}" '
                f'format="{fmt(c)}" srcEnable="video" tcFormat="NDF">{zx}<adjust-volume amount="-96dB"/></asset-clip>')
    return out
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
        kids += f'<adjust-volume amount="{-96 if k in BLEEP else GAIN[c]}dB"/>'
        if k in BLEEP:   # 1 kHz bleep over the muted name + the name's caption as a blurred image
            kids += (f'<asset-clip ref="aBleep" lane="-2" offset="{r(st)}" name="Bleep" start="0s" duration="{r(du)}" audioRole="effects">'
                     f'<adjust-volume amount="{BLEEP_DB}dB"/></asset-clip>')
            kids += f'<video ref="pBlur{k}" lane="2" offset="{r(st)}" name="Blurred {BLEEP[k]}" start="0s" duration="{r(du)}"/>'
        if i == 0:
            kids += (f'<asset-clip ref="aMusic" lane="-1" offset="{r(st)}" name="Ivory Check-in" start="{r(q(MUSIC_IN))}" duration="{r(total)}" audioRole="music">'
                     f'<adjust-volume amount="{MUSIC_DB}dB"><param name="amount"><fadeOut type="easeIn" duration="2s"/></param></adjust-volume></asset-clip>')
        kids += broll_xml(k, st, du)
        if c not in seen and k not in HOST_SEGS:
            seen.add(c); kids += label_title(*GUEST[c], st, min(du, F(5,2)))
        CH = [] if k in BLEEP else chunks_for(k)
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
# browser clips for EVERY file in the folder, except the 14 that already have one in the event (IMG_0818-0831, from v1)
HAVE = {f"IMG_08{n}" for n in range(18, 32)}
evclips = []
for f in FILES:
    c = os.path.splitext(f)[0]
    if c in HAVE: continue
    if dur[c][0] is None:   # still
        evclips.append(f'<clip name="{c}" start="3600s" duration="10s"><video ref="a_{c}" duration="0s"/></clip>')
    else:
        evclips.append(f'<asset-clip ref="{aid(c)}" name="{esc(c)}" start="0s" duration="{r(dur[c][0])}" format="{fmt(c)}" tcFormat="NDF" audioRole="dialogue"/>')
out = ('<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE fcpxml>\n<fcpxml version="1.11"><resources>\n' + "\n".join(res) + '\n</resources>\n'
       '<library colorProcessing="wide-hdr">'
       f'<event name="{EVENT}">\n' + "\n".join(evclips) + "\n" + "\n".join(projs) + '\n</event></library></fcpxml>\n')
op = f"{X}/Immersion Day Interviews.fcpxml"; open(op, "w").write(out)
json.dump(plans, open(f"{X}/cut_plan.json", "w"), indent=1)
print(tid, "titles ->", op)
for k in PROJECTS["Immersion Day Interviews"]: print(k, " | ".join(" ".join(w[2] for w in ch) for ch in chunks_for(k)))
