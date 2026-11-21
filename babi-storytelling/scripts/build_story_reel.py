"""Immersion Day story reel (Babi talking to camera, IMG_0975 + IMG_0976) -> FCPXML for the 'Immersion Day FCP12.3' library.
Spine = pieces.json (tools/cut.py).  B-roll = BURSTS (steady shots only, muted).  Captions from tr/cut.json (the cut's own audio)."""
import json, os, re, subprocess, sys, shutil
from fractions import Fraction as F
from urllib.parse import quote
S = os.path.dirname(os.path.abspath(__file__)); W = os.path.dirname(S)
D = "/Volumes/4TBSSD_4/Babi NR Content/Media/OFFICE/November 18th Immersion Day"
EVENT = "November 18th Immersion Day"
PROJECT = sys.argv[2] if len(sys.argv) > 2 else "Immersion Day Story V1"
OUT = sys.argv[1]
UIDS = json.load(open(f"{W}/uids_all.json"))
PIECES = json.load(open(f"{W}/pieces.json"))
CUTW = [w for s in json.load(open(f"{W}/tr/cut.json")) for w in s["words"]]

DIALOGUE_DB = 5            # cut measured -21.1 LUFS -> about -16
MUSIC_DB = -20             # Skyfall (-7.5 LUFS) -> -27.5 LUFS = ~11.5 LU under speech (-16)
SONG_SRC = "/Volumes/4TBSSD_4/Babi NR Content/Songs/STORYTELLING/Jack Style/Adele - Skyfall (Lyrics) 4.mp3"
SONG = f"{D}/Sound/Skyfall.mp3"; SONG_DUR = F(28829, 100); SONG_IN = 37
if not os.path.exists(SONG): shutil.copy(SONG_SRC, SONG)
POP_SRC = "/Volumes/4TBSSD_4/Babi NR Content/Sound FX/click and keyboard/Censor sound __ Funny sound __ Mouse click sound __ Pop sound __ Slap sound __ Short sound effect.mp3"
POP = f"{D}/Sound/Pop sound.mp3"
if not os.path.exists(POP): shutil.copy(POP_SRC, POP)
CAP = dict(font="Helvetica Neue", face="Bold", size=42, y=-288, ty=5.706, max_words=3, max_chars=16, gap=0.35)
POSKEY = "9999/999166631/999166633/1/100/101"

# B-roll: line id -> (burst start offsets from the line start, burst end offset or None = end of the line)
# each shot = (offset, clip, source in-point s, (scale, x, y) or None).  All shots are steady (shake_score <= ~0.5 px/frame), muted.
BURSTS = {
 1:  [(0.9, "IMG_0699", 1.0, None), (1.7, "IMG_0724", 0.5, None), (2.4, "IMG_0726", 0.4, None)],            # arrivals, then the room full of people
 2:  [(0.8, "IMG_0776", 4.0, None), (1.7, "IMG_0745", 1.0, None), (2.5, "IMG_0744", 1.0, None)],           # members at the table
 3:  [(0.7, "IMG_0735", 8.5, None), (1.8, "IMG_0756", 4.0, None), (2.8, "IMG_0787", 1.0, None)],           # "Something big is coming", the screen, the slide
 4:  [("L2", "IMG_0798", 7.0, None)],                                                                       # how they'd react
 5:  [(0.8, "IMG_0797", 4.0, None), (1.8, "IMG_0756", 13.5, None), (2.8, "IMG_0733", 4.0, None)],           # the team
 8:  [(0.4, "IMG_0805", 9.0, None), (1.5, "IMG_0733", 8.0, None)],                                          # these walls
 9:  [(0.5, "IMG_0763", 1.0, None)],                                                                        # Stu at the whiteboard
 10: [(0.6, "IMG_0764", 10.5, None), (1.8, "IMG_0801", 12.5, None), (3.0, "IMG_0761", 1.0, None), (4.0, "IMG_0787", 2.0, None)],
 11: [(0.5, "IMG_0797", 5.5, None), (1.5, "IMG_0792", 4.0, None)],                                          # Rick
 12: [(0.8, "IMG_0806", 10.0, (1.4, 0, 6)), (2.1, "IMG_0807", 4.5, None), (3.3, "IMG_0806", 12.5, (1.4, 0, 6))],
 14: [(0.5, "IMG_0807", 5.0, None), (1.7, "IMG_0806", 11.5, (1.4, 0, 6)), (2.7, "IMG_0807", 7.0, None)],   # rebuilt it just by talking
 15: [(0.5, "IMG_0797", 6.0, None), (1.3, "IMG_0757", 3.2, None), (2.3, "IMG_0792", 5.0, None)],           # no clicking, just yapping
 16: [(0.7, "IMG_0742", 2.0, None), (1.9, "IMG_0747", 5.0, None)],                                          # hear it from them
 17: [(0.8, "IMG_0742", 4.2, None), ("L2", "IMG_0757", 8.2, None)],                                          # worth it for these reactions
}
BURST_END = {16: 3.1}      # offset where the burst ends (face comes back for "hear it from them"); others run to the line end
BURST_END[17] = None
ZOOM_ALT = 1.12            # punch-in on every second spine piece of a line (hides the jump cuts)

def snap(x): return F(round(F(str(x)) * 30), 30)
def r(x):
    x = F(x); return f"{x.numerator}/{x.denominator}s" if x.denominator != 1 else f"{x.numerator}s"
def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;").replace('"', "&quot;")
def aid(c): return "a_" + re.sub(r"\W", "_", c)

# ---------- spine pieces on the 30 fps grid
for p in PIECES: p["o"] = F(p["off"]); p["s"] = F(p["start"]); p["d"] = F(p["dur"]); p["clip"] = "IMG_" + p["file"]
def probe(path):
    j = json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,width,height,r_frame_rate,color_transfer:stream_side_data=rotation:format=duration",
                                   "-of", "json", path], capture_output=True, text=True).stdout)
    v = next(s for s in j["streams"] if s["codec_type"] == "video")
    rot = any(abs(int(sd.get("rotation", 0))) == 90 for sd in v.get("side_data_list", []))
    w, h = (v["height"], v["width"]) if rot else (v["width"], v["height"])
    return dict(rate=v["r_frame_rate"], w=w, h=h, hlg=v.get("color_transfer") == "arib-std-b67",
                audio=any(s["codec_type"] == "audio" for s in j["streams"]), dur=F(j["format"]["duration"]).limit_denominator(600))


# ---- guests: "hear it from them" -> Mike + Lisa from the interview projects (segments.py), then back to the story
XI = f"{D}/XML/Interviews"
sys.path.insert(0, XI)
from segments import S as SEG
GUEST_SEGS = [1, 2, 3, 11, 18]              # Mike "Minds get blown", Lisa "speechless", "gone to Mars", Mike "five services to cancel", Lisa "can't wait to use it"
GAIN = {"IMG_0820": 11, "IMG_0821": 8}      # raw -27.7 / -23.8 LUFS -> about -16
GUEST_X = {"IMG_0820": 810, "IMG_0821": 840}; GUEST_Y = 1040
GUEST_NAME = {"IMG_0820": "Mike", "IMG_0821": "Lisa"}
OLD_END16 = max(p["o"] + p["d"] for p in PIECES if p["line"] == 16)
gpieces = []
sys.path.insert(0, "/Users/northresults/.claude/babi-skills/babi-storytelling/scripts")
import cutlib
GDB = {}
for k in GUEST_SEGS:
    c, a, b, z, note = SEG[k]
    if c not in GDB: GDB[c] = cutlib.load(f"{W}/tr/g{c[4:]}.wav")[1]
    thr = cutlib.speech_thr(GDB[c])
    pr = probe(f"{D}/{c}.MOV"); n, d_ = map(int, pr["rate"].split("/"))
    for j, (pa, pb) in enumerate(cutlib.split(GDB[c], thr, a, b, 0.12, 0.03)):
        st = F(round(pa * n / d_) * d_, n); du = snap(pb - pa)
        if du < F(3, 30): continue
        gpieces.append(dict(line=160 + k, k=j, file=c[4:], clip=c, s=st, d=du, text=note, off="0", seg=k, zoom=z, gain=GAIN[c], a=pa, b=pb))
i16 = max(i for i, p in enumerate(PIECES) if p["line"] == 16)
PIECES[i16 + 1:i16 + 1] = gpieces
off = F(0)
for p in PIECES: p["o"] = off; off += p["d"]
GUEST_START = gpieces[0]["o"]; GUEST_END = gpieces[-1]["o"] + gpieces[-1]["d"]; SHIFT = GUEST_END - GUEST_START
TOTAL = PIECES[-1]["o"] + PIECES[-1]["d"]
lines = {}
for p in PIECES: lines.setdefault(p["line"], []).append(p)
def line_span(lid): ps = lines[lid]; return ps[0]["o"], ps[-1]["o"] + ps[-1]["d"]
def piece_at(t): return next(p for p in PIECES if p["o"] <= t < p["o"] + p["d"])

# ---------- resources
used = {p["clip"] for p in PIECES}
shots = []        # (t0, t1, clip, src, zoom)
for lid, sh in BURSTS.items():
    a, b = line_span(lid); ps = lines[lid]
    starts = []
    for off, clip, src, z in sh:
        if off == "L2": off = float(ps[1]["o"] - a)       # second spine piece of the line
        starts.append((snap(a + F(str(off))), clip, src, z))
    end = b if BURST_END.get(lid) is None else snap(a + F(str(BURST_END[lid])))
    for i, (t0, clip, src, z) in enumerate(starts):
        t1 = starts[i + 1][0] if i + 1 < len(starts) else end
        shots.append((t0, t1, clip, src, z)); used.add(clip)
BOUNDS = sorted({p["o"] for p in PIECES} | {p["o"] + p["d"] for p in PIECES})
_last = {}
for sh in shots: _last[max(0, 0)] = None
lastshots = []
for lid in BURSTS:
    a, b = line_span(lid); inl = [x for x in shots if a <= x[0] < b]
    if inl: lastshots.append(max(inl, key=lambda x: x[0]))
for x in lastshots:
    t1 = x[1]; nxt = [bd for bd in BOUNDS if bd > t1]
    if t1 not in BOUNDS and nxt and nxt[0] - t1 <= F(8, 10):
        shots[shots.index(x)] = (x[0], nxt[0], x[2], x[3], x[4]); print("extend B-roll end", float(t1), "->", float(nxt[0]))
res = ['<format id="r1" name="FFVideoFormat1080x1920p30" frameDuration="100/3000s" width="1080" height="1920" colorSpace="1-1-1 (Rec. 709)"/>',
       '<effect id="eT" name="Basic Title" uid=".../Titles.localized/Bumper:Opener.localized/Basic Title.localized/Basic Title.moti"/>']
info, fmts = {}, {}
files = {f.rsplit(".", 1)[0]: f for f in os.listdir(D) if f.lower().endswith((".mov", ".mp4", ".m4v"))}
for c in sorted(used):
    f = files[c]; pr = probe(f"{D}/{f}"); info[c] = pr
    n, d_ = map(int, pr["rate"].split("/")); cs = "9-18-9 (Rec. 2020 HLG)" if pr["hlg"] else "1-1-1 (Rec. 709)"
    key = (n, d_, pr["w"], pr["h"], cs)
    if key not in fmts:
        fmts[key] = f"rv{len(fmts)}"
        res.append(f'<format id="{fmts[key]}" frameDuration="{d_}/{n}s" width="{pr["w"]}" height="{pr["h"]}" colorSpace="{cs}"/>')
    pr["fmt"] = fmts[key]
    uid = f' uid="{UIDS[c]}"' if c in UIDS else ""
    a = ' hasAudio="1" audioSources="1" audioChannels="2" audioRate="48000"' if pr["audio"] else ""
    res.append(f'<asset id="{aid(c)}" name="{c}"{uid} start="0s" duration="{r(pr["dur"])}" hasVideo="1" format="{pr["fmt"]}" videoSources="1"{a}>'
               f'<media-rep kind="original-media" src="file://{quote(D + "/" + f)}"/></asset>')
res.append(f'<asset id="aMusic" name="Skyfall" start="0s" duration="{r(SONG_DUR)}" hasAudio="1" audioSources="1" audioChannels="2" audioRate="48000">'
           f'<media-rep kind="original-media" src="file://{quote(SONG)}"/></asset>')
res.append(f'<asset id="aPop" name="Pop sound" start="0s" duration="3s" hasAudio="1" audioSources="1" audioChannels="2" audioRate="48000">'
           f'<media-rep kind="original-media" src="file://{quote(POP)}"/></asset>')

def qsrc(c, t):
    n, d_ = map(int, info[c]["rate"].split("/")); k = round(F(str(t)) * n / d_); return k * F(d_, n)

# ---------- attach helper: connected item at timeline time t goes on the spine piece that contains t
attached = {id(p): [] for p in PIECES}
def attach(t, xml_fn):
    p = piece_at(t); attached[id(p)].append(xml_fn(p.get("s") + (t - p["o"])))

# B-roll
cover = F(0)
for t0, t1, clip, src, z in sorted(shots):
    assert info[clip]["dur"] >= F(str(src)) + (t1 - t0), (clip, src, float(t1 - t0), float(info[clip]["dur"]))
    zx = f'<adjust-transform position="{z[1]} {z[2]}" scale="{z[0]} {z[0]}"/>' if z else ""
    attach(t0, lambda o, t0=t0, t1=t1, clip=clip, src=src, zx=zx:
           f'<asset-clip ref="{aid(clip)}" lane="1" offset="{r(o)}" name="B-roll {clip}" start="{r(qsrc(clip, src))}" duration="{r(t1 - t0)}" '
           f'format="{info[clip]["fmt"]}" tcFormat="NDF">{zx}<adjust-volume amount="-96dB"/></asset-clip>')
    cover += t1 - t0

# captions: from the cut's own words
KEEP_CAP = {"i", "i'm", "stu", "rick", "january", "membership.io"}
def clean(w):
    c = re.sub(r"[.,?!\"]", "", w.strip()).lower()
    return {"stu's": "Stu's"}.get(c, c)
toks = []
WT = {}
GW = []
for gp in gpieces:
    if gp["clip"] not in WT: WT[gp["clip"]] = [w for sg in json.load(open(f"{XI}/{gp['clip']}.MOV.json")) for w in sg["words"]]
    for s0, e0, t in WT[gp["clip"]]:
        if gp["a"] <= (s0 + e0) / 2 < gp["b"]:
            GW.append((t, float(gp["o"]) + max(s0, gp["a"]) - gp["a"], float(gp["o"]) + min(e0, gp["b"]) - gp["a"], 0))
STORY = []
for w, a, b, q in CUTW:
    if a >= float(OLD_END16) - 0.001: a += float(SHIFT); b += float(SHIFT)
    STORY.append((w, a, b, q))
for w, a, b, _ in sorted(STORY + GW, key=lambda x: x[1]):
    c = clean(w)
    if toks and w.strip().startswith("."): toks[-1].update(c=toks[-1]["c"] + "." + c.lstrip("."), e=b); continue
    if toks and toks[-1]["c"] == "wait" and c == "list": toks[-1].update(c="waitlist", e=b); continue
    toks.append(dict(c=c, s=a, e=b, end=bool(re.search(r"[.?!]$", w.strip()))))
for i, t in enumerate(toks):                  # whisper hears "it could" for Babi's "I could"
    if t["c"] == "it" and i + 1 < len(toks) and toks[i + 1]["c"] == "could" and toks[i + 1]["s"] - t["e"] < 0.1 and t["s"] > 44 and t["s"] < 46: t["c"] = "i"
for t in toks:
    if t["c"] in ("i", "i'm", "stu", "rick", "january", "membership.io"):
        t["c"] = {"i": "I", "i'm": "I'm", "stu": "Stu", "rick": "Rick", "january": "January", "membership.io": "Membership.io"}[t["c"]]
for i, t in enumerate(list(toks)):
    if t["c"] == "could" and 43 < t["s"] < 44.6 and toks[i - 1]["c"] not in ("i", "I", "it"):
        toks.insert(i, dict(c="I", s=max(t["s"] - 0.16, toks[i - 1]["e"]), e=t["s"], end=False)); break
chunks, cur = [], []
for t in toks:
    if cur and (len(cur) >= CAP["max_words"] or len(" ".join(x["c"] for x in cur + [t])) > CAP["max_chars"] or t["s"] - cur[-1]["e"] > CAP["gap"]):
        chunks.append(cur); cur = []
    cur.append(t)
    if t["end"]: chunks.append(cur); cur = []
if cur: chunks.append(cur)
tn = [0]
YEL = "1 0.88 0 1"
def cap_xml(ch, wi, t0, t1):
    """one title per spoken word: the chunk in white, the active word yellow (babi-storytelling karaoke)"""
    runs, defs = "", ""
    for i, x in enumerate(ch):
        tn[0] += 1; tid = f"cap{tn[0]}"
        runs += f'<text-style ref="{tid}">{esc(x["c"])}{" " if i < len(ch) - 1 else ""}</text-style>'
        defs += (f'<text-style-def id="{tid}"><text-style font="{CAP["font"]}" fontSize="{CAP["size"]}" fontFace="{CAP["face"]}" fontColor="{YEL if i == wi else "1 1 1 1"}" '
                 f'shadowColor="0 0 0 0.75" shadowOffset="4 315" shadowBlurRadius="8" alignment="center"/></text-style-def>')
    nm = esc(" ".join(x["c"] for x in ch))[:40]
    return (lambda o: f'<title ref="eT" lane="6" offset="{r(o)}" name="{nm}" start="3600s" duration="{r(t1 - t0)}">'
            f'<param name="Position" key="{POSKEY}" value="0 {CAP["y"]}"/><param name="Flatten" key="9999/999166631/999166633/2/351" value="1"/>'
            f'<param name="Alignment" key="9999/999166631/999166633/2/354/999169573/401" value="1 (Center)"/>'
            f'<text>{runs}</text>{defs}<adjust-transform position="0 {CAP["ty"]}"/></title>')
ncap = 0
cstarts = [snap(max(c[0]["s"] - 0.03, 0)) for c in chunks]
for i, ch in enumerate(chunks):
    cend = min(cstarts[i + 1] if i + 1 < len(chunks) else TOTAL, snap(ch[-1]["e"] + 0.4), TOTAL)
    ws = [cstarts[i] if k == 0 else snap(x["s"]) for k, x in enumerate(ch)]
    for k, x in enumerate(ch):
        t0 = ws[k]; t1 = ws[k + 1] if k + 1 < len(ch) else cend
        if t1 <= t0: t1 = t0 + F(1, 30)
        if k + 1 < len(ch) and ws[k + 1] <= t0: continue
        attach(t0, cap_xml(ch, k, t0, t1)); ncap += 1

# "COMMENT WAITLIST" graphic + pop at the spoken word
cw = next(t for t in toks if t["c"] == "comment")
g0 = snap(cw["s"]); g1 = TOTAL
def gfx(o):
    return (f'<title ref="eT" lane="7" offset="{r(o)}" name="Comment WAITLIST" start="3600s" duration="{r(g1 - g0)}">'
            f'<param name="Position" key="{POSKEY}" value="0 -114"/><param name="Flatten" key="9999/999166631/999166633/2/351" value="1"/>'
            f'<param name="Alignment" key="9999/999166631/999166633/2/354/999169573/401" value="1 (Center)"/>'
            f'<text><text-style ref="gfx1">COMMENT&#10;WAITLIST</text-style></text>'
            f'<text-style-def id="gfx1"><text-style font="Helvetica Neue" fontSize="50" fontFace="Bold" fontColor="1 1 1 1" '
            f'shadowColor="0 0 0 0.75" shadowOffset="4 315" shadowBlurRadius="8" alignment="center"/></text-style-def></title>')
attach(g0, gfx)
POP_IN = F(696, 1000)       # Cute Pop transient lives at 0.73 s -> start 0.696 (babi-storytelling)
attach(g0 - F(1, 30), lambda o: f'<asset-clip ref="aPop" lane="-2" offset="{r(o)}" name="Pop" start="{r(POP_IN)}" duration="{r(F(12, 100))}" audioRole="effects"><adjust-volume amount="-14dB"/></asset-clip>')

# name labels on each guest's first segment (brief: who they are, as on-screen text)
seen = set(); tl = 0
for gp in gpieces:
    if gp["clip"] in seen: continue
    seen.add(gp["clip"]); tl += 1; nm = GUEST_NAME[gp["clip"]]
    lab = (lambda o, nm=nm, tl=tl, dd=min(gp["d"], F(75, 30)): (
        f'<title ref="eT" lane="7" offset="{r(o)}" name="Label {nm}" start="3600s" duration="{r(dd)}">'
        f'<param name="Position" key="{POSKEY}" value="0 150"/><param name="Flatten" key="9999/999166631/999166633/2/351" value="1"/>'
        f'<param name="Alignment" key="9999/999166631/999166633/2/354/999169573/401" value="1 (Center)"/>'
        f'<text><text-style ref="lab{tl}n">{nm}&#10;</text-style><text-style ref="lab{tl}r">Membership.io customer</text-style></text>'
        f'<text-style-def id="lab{tl}n"><text-style font="Helvetica Neue" fontSize="46" fontFace="Bold" fontColor="1 1 1 1" shadowColor="0 0 0 0.75" shadowOffset="4 315" shadowBlurRadius="8" alignment="center"/></text-style-def>'
        f'<text-style-def id="lab{tl}r"><text-style font="Helvetica Neue" fontSize="26" fontFace="Medium" fontColor="1 1 1 1" shadowColor="0 0 0 0.75" shadowOffset="4 315" shadowBlurRadius="8" alignment="center"/></text-style-def></title>'))
    attach(gp["o"], lab)

# sanity: no B-roll ends just before a spine cut (the 'flash'), no B-roll starts a hair after one
for t0, t1, *_ in shots:
    for bd in BOUNDS:
        assert not (t1 < bd <= t1 + F(8, 10)) or t1 in BOUNDS or any(x[0] == t1 for x in shots), ("B-roll ends just before a cut", float(t1), float(bd))
# ---------- spine
spine = []
for p in PIECES:
    kids = ""
    k = p["k"]
    if "seg" in p:                      # guest: zoom on the guest's face (same maths as the interview builder), own gain
        sc = p["zoom"]
        if sc != 1.0:
            lim = (sc - 1) * 540 / sc; dx = max(-lim, min(lim, GUEST_X[p["clip"]] - 540))
            limy = (sc - 1) * 960 / sc; dy = max(-limy, min(limy, GUEST_Y - 960))
            kids += f'<adjust-transform position="{-sc * dx / 19.2:.3f} {sc * dy / 19.2:.3f}" scale="{sc} {sc}"/>'
        kids += f'<adjust-volume amount="{p["gain"]}dB"/>'
    else:
        if k % 2 == 1: kids += f'<adjust-transform scale="{ZOOM_ALT} {ZOOM_ALT}"/>'
        kids += f'<adjust-volume amount="{DIALOGUE_DB}dB"/>'
    if p is PIECES[0]:
        kids += (f'<asset-clip ref="aMusic" lane="-1" offset="{r(p["s"])}" name="Skyfall" start="{SONG_IN}s" duration="{r(TOTAL)}" audioRole="music">'
                 f'<adjust-volume amount="{MUSIC_DB}dB"><param name="amount"><fadeOut type="easeIn" duration="2s"/></param></adjust-volume></asset-clip>')
    kids += "".join(attached[id(p)])
    spine.append(f'<asset-clip ref="{aid(p["clip"])}" name="{p["line"]:02d} {esc(p["text"][:36])}" offset="{r(p["o"])}" start="{r(p["s"])}" duration="{r(p["d"])}" '
                 f'format="{info[p["clip"]]["fmt"]}" tcFormat="NDF" audioRole="dialogue">{kids}</asset-clip>')
proj = (f'<project name="{PROJECT}"><sequence format="r1" duration="{r(TOTAL)}" tcStart="0s" tcFormat="NDF" audioLayout="stereo" audioRate="48k"><spine>\n'
        + "\n".join(spine) + '\n</spine></sequence></project>')
# browser clips for the two new videos (the event doesn't have them yet)
ev = ""
for c in ("IMG_0975", "IMG_0976"):
    if c not in info:
        f = files[c]; pr = probe(f"{D}/{f}"); n, d_ = map(int, pr["rate"].split("/")); cs = "9-18-9 (Rec. 2020 HLG)" if pr["hlg"] else "1-1-1 (Rec. 709)"
        key = (n, d_, pr["w"], pr["h"], cs)
        if key not in fmts: fmts[key] = f"rv{len(fmts)}"; res.append(f'<format id="{fmts[key]}" frameDuration="{d_}/{n}s" width="{pr["w"]}" height="{pr["h"]}" colorSpace="{cs}"/>')
        a = ' hasAudio="1" audioSources="1" audioChannels="2" audioRate="48000"' if pr["audio"] else ""
        res.append(f'<asset id="{aid(c)}" name="{c}" start="0s" duration="{r(pr["dur"])}" hasVideo="1" format="{fmts[key]}" videoSources="1"{a}>'
                   f'<media-rep kind="original-media" src="file://{quote(D + "/" + f)}"/></asset>')
        info[c] = dict(pr, fmt=fmts[key])
    ev += f'<asset-clip ref="{aid(c)}" name="{c}" start="0s" duration="{r(info[c]["dur"])}" format="{info[c]["fmt"]}" tcFormat="NDF" audioRole="dialogue"/>\n'
out = ('<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE fcpxml>\n<fcpxml version="1.11"><resources>\n' + "\n".join(res) + '\n</resources>\n'
       f'<library colorProcessing="wide-hdr"><event name="{EVENT}">\n' + ev + proj + '\n</event></library></fcpxml>\n')
open(OUT, "w").write(out)
print(f"{PROJECT}: {float(TOTAL):.2f}s, {len(PIECES)} spine pieces, {len(shots)} B-roll shots ({float(cover):.1f}s = {100 * float(cover) / float(TOTAL):.0f}% covered), {len(chunks)} caption groups ({ncap} word titles), pop at {float(g0):.2f}")
json.dump(dict(lines={k: [float(line_span(k)[0]), float(line_span(k)[1])] for k in lines}, shots=[(float(a), float(b), c, s) for a, b, c, s, z in sorted(shots)]),
          open(f"{W}/plan.json", "w"), indent=1)
print(" | ".join(" ".join(x["c"] for x in c) for c in chunks))
