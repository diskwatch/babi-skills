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
# v2 B-roll (Babi 2026-11-20: "way more B-roll" of Rick/Stu presenting, Lisa's and Mike's boardroom reactions; every clip imported).
# Who's who (from the clips' own audio): Stu = navy shirt at the whiteboard; Rick = younger guy in black cap + Membership.io jacket
# (runs the slides, demos the AI by text); Andrew = older cap guy, blue shirt (IMG_0818/0819 with Mike at the monitor).
# Bursts are written in MAIN-timeline seconds: (burst start = a spoken word, [(clip, src in), ...], cut times inside, burst end = seg end).
# Each burst lives inside one segment, so the Mike/Lisa cuts reuse the same seg-relative offsets.
BURSTS = {
 3:  (4.79, [("IMG_0788", 9.0)], []),                                              # "gone to Mars" -> Lisa close-up, hands clasped
 4:  (7.13, [("IMG_0787", 0.3), ("IMG_0787", 2.8), ("IMG_0819", 2.0), ("IMG_0818", 0.5)],
     [8.25, 9.73, 11.97]),                                                          # "enter a prompt" -> Rick under "Just ask." slide; "whole backend" -> Andrew + Mike at the laptop / monitor
 5:  (16.70, [("IMG_0806", 9.0)], []),                                              # "texting it to my phone" -> Rick texting the AI (one shot: locked-off, jump cuts look identical)
 6:  (18.95, [("IMG_0807", 3.5)], []),                                              # "create a website for me" -> the text thread on the TV
 7:  (22.11, [("IMG_0798", 5.6)], []),                                              # "my colors, my style" -> Lisa filming it, smiling
 9:  (26.15, [("IMG_0745", 1.0), ("IMG_0776", 5.5), ("IMG_0789", 7.0)], [28.15, 30.2]),   # "days ... building ... fraction" -> Mike in the boardroom
 10: (33.30, [("IMG_0779", 10.5), ("IMG_0779", 12.9), ("IMG_0775", 11.0), ("IMG_0793", 4.2)],
      [34.4, 35.38, 36.44]),                                                        # "email ... WordPress ... Zapier" -> Stu open arms, Lisa laughing/filming
 11: (39.28, [("IMG_0796", 0.8), ("IMG_0742", 1.5)], [40.72]),                      # "five services ... cancel" -> Mike in the boardroom
 12: (44.64, [("IMG_0786", 3.5)], []),                                              # Babi: "...to actually launch it" -> "The next Membership.io" slide
 14: (49.15, [("IMG_0747", 1.0)], []),                                              # "landing pages" -> Lisa talking at the table
 16: (52.92, [("IMG_0775", 5.5), ("IMG_0801", 9.5)], [53.9]),                       # "comprehend it unless you see it" -> Stu grinning, Stu excited
 17: (54.67, [("IMG_0776", 22.0)], []),                                             # "whole nother level" -> Stu big gestures
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
res.append(f'<asset id="pEnd" name="end_card_membership_io"{uid("end_card_membership_io")} start="0s" duration="0s" hasVideo="1" format="ri" videoSources="1">'
           f'<media-rep kind="original-media" src="file://{quote(endp)}"/></asset>')
def fmt(c): return dur[c + "_fmt"]
def qsrc(c, t):   # frame-align a source time to the clip's own rate
    n, d_ = map(int, dur[c][1].split("/")); k = round(F(str(t)) * n / d_); return k * F(d_, n)
MAIN, _o = {}, F(0)
for _k in PROJECTS["Immersion Day Interviews"]:
    _d = q(S[_k][2]) - q(S[_k][1]); MAIN[_k] = (float(_o), float(_o + _d)); _o += _d
def snap(t):      # internal B-roll cut -> nearest beat within 0.19 s
    b = min(BEATS, key=lambda x: abs(x - t)); return b if abs(b - t) <= 0.19 else t
def broll_xml(k, st, du):
    """Connected video-only B-roll for segment k, seg-relative so it works in every project. st = segment's source start (parent time base)."""
    if k not in BURSTS: return ""
    s0, e0 = MAIN[k]; b0, shots, cuts = BURSTS[k]
    edges = [q(b0 - s0)] + [q(snap(c) - s0) for c in cuts] + [du]       # last edge = segment end exactly (no 1-frame flash)
    out = ""
    for i, (c, sin) in enumerate(shots):
        o, d = edges[i], edges[i + 1] - edges[i]
        z = BZOOM.get(c); zx = f'<adjust-transform position="{z[1]} {z[2]}" scale="{z[0]} {z[0]}"/>' if z else ""
        out += (f'<asset-clip ref="a_{c}" lane="1" offset="{r(st + o)}" name="B-roll {c}" start="{r(qsrc(c, sin))}" duration="{r(d)}" '
                f'format="{fmt(c)}" srcEnable="video" tcFormat="NDF">{zx}</asset-clip>')
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
        kids += f'<adjust-volume amount="{GAIN[c]}dB"/>'
        if i == 0:
            kids += (f'<asset-clip ref="aMusic" lane="-1" offset="{r(st)}" name="Ivory Check-in" start="{r(q(MUSIC_IN))}" duration="{r(total)}" audioRole="music">'
                     f'<adjust-volume amount="{MUSIC_DB}dB"><param name="amount"><fadeOut type="easeIn" duration="2s"/></param></adjust-volume></asset-clip>')
        kids += broll_xml(k, st, du)
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
