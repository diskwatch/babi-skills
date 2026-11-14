"""Add (1) ChatGPT + Claude logos with dings at a marker and (2) a slower chat-screenshot pop run
to an exported copy of the user's edit. Everything else stays byte-for-byte as the user left it.
Output goes to the SSD XML folder, same project name (the old project gets renamed in Final Cut).
"""
import re, os, urllib.parse
from fractions import Fraction as Fr

BF = "/Volumes/4TBSSD_4/Babi NR Content/Media/OFFICE/Nov 12 Black Friday"
SRC = f"{BF}/XML/CLR user v2.fcpxmld/Info.fcpxml"
OUT = f"{BF}/XML/Creator Lab Reel - chat pops (logos).fcpxmld"
PROJECT_NAME = "Creator Lab Reel - chat pops"
FPS = 60
FRAME_W, FRAME_H = 1080, 1920

# --- what to add -------------------------------------------------------------------------------
LOGO_IN = None            # None = use the project's marker ("Marker 1" at 0:46:56)
LOGO_GAP = 0.35           # Claude lands this long after ChatGPT (on "already")
LOGO_OUT = 51.317         # hold through "that's ChatGPT, Claude, or any other AI tool" (clip end)
LOGOS = [  # file, x, y (% of frame height, y up), displayed width in px
    (f"{BF}/Logos/ChatGPT logo.png", -12, -27, 340),
    (f"{BF}/Logos/Claude logo.png", 12, -27, 340),
]
DING = dict(uid="4E71FBAE44E48B72F7129128F1654579", name="Ding - Sound Effect (HD) - Gaming Sound FX (youtube) (1)",
            src="/Volumes/4TBSSD_4/Babi NR Content/Songs/SOUND FX/Ding - Sound Effect (HD) - Gaming Sound FX (youtube) (1).mp3",
            dur="135936/44100s", start=0.21, length=0.85, vol="-16dB")

# "and that's when the chat absolutely lost it": 5 shots, gaps grow so each one can be read
import glob
SS = lambda stamp: glob.glob(f"{BF}/Creator Lab Excitement/Screenshot 2026-11-10 at {stamp}*PM.png")[0]
POPS = [  # time, screenshot, x, y, displayed width px
    (54.150, "3.36.43", -6, 42, 640),    # OMG LOVE IT!
    (54.417, "3.40.42", -5, -22, 800),    # I got it working already!! Pretty rad!
    (54.733, "3.59.55", -2, 24, 860),    # I'm using Claude ... Black Friday offer. Let's GOOOOO!
    (55.083, "4.18.28", -3, -38, 800),   # I'm creating a 50% off bundle... plus a bonus
    (55.500, "3.37.58", 15, 0, 420),    # the chat flood (Heck yeh / Super excited!!!!)
]
POPS_OUT = 56.000         # clip end before "then our team took people into breakout rooms"
POP_VOL = "-14dB"

# -------------------------------------------------------------------------------------------------
s = open(SRC).read()
t = lambda x: Fr(x.rstrip("s")) if x else Fr(0)
snap = lambda sec: Fr(round(sec * FPS), FPS)
def ft(f):
    f = Fr(f).limit_denominator(600000)
    return f"{f.numerator}/{f.denominator}s" if f.denominator != 1 else f"{f.numerator}s"

proj = s.find("<spine>", s.find("<project"))
spine, depth = [], 0
for m in re.finditer(r"<(/?)(asset-clip|clip|gap|video|title|spine|ref-clip)\b([^>]*?)(/?)>", s[proj + 7:]):
    closing, tag, attrs, sc = m.groups()
    if closing:
        depth -= 1; continue
    if depth == 0 and tag != "spine":
        g = lambda k: (re.search(" " + k + r'="([^"]+)"', attrs) or [None, None])[1]
        spine.append(dict(pos=proj + 7 + m.start(), off=t(g("offset")), start=t(g("start")), dur=t(g("duration")), name=g("name")))
    if not sc:
        depth += 1
parent_at = lambda x: next(c for c in spine if c["off"] <= x < c["off"] + c["dur"])

if LOGO_IN is None:  # marker -> timeline time
    for c in spine:
        seg = s[c["pos"]: (spine[spine.index(c) + 1]["pos"] if c is not spine[-1] else len(s))]
        mk = re.search(r'<marker start="([^"]+)"', seg)
        if mk:
            LOGO_IN = float(c["off"] + t(mk.group(1)) - c["start"]); break

# --- resources
res = []
def still_asset(path, key):
    from PIL import Image
    w, h = Image.open(path).size
    res.append(f'<format id="fmt_{key}" name="FFVideoFormatRateUndefined" width="{w}" height="{h}"/>')
    url = "file://" + urllib.parse.quote(path)
    name = os.path.splitext(os.path.basename(path))[0]
    res.append(f'<asset id="a_{key}" name="{name}" start="0s" duration="0s" hasVideo="1" format="fmt_{key}" videoSources="1">'
               f'<media-rep kind="original-media" src="{url}"/></asset>')
    return f"a_{key}", name, w, h

def scale_for(w, h, width_px):
    fit = min(FRAME_W / w, FRAME_H / h)          # Final Cut "Fit"
    return round(width_px / (w * fit), 4)

existing = re.search(r'<asset id="([^"]+)" name="Ding', s)
ding_id = existing.group(1) if existing else "a_ding"
if not existing:
    res.append(f'<asset id="a_ding" name="{DING["name"]}" uid="{DING["uid"]}" start="0s" duration="{DING["dur"]}" hasAudio="1" '
               f'audioSources="1" audioChannels="2" audioRate="44100"><media-rep kind="original-media" sig="{DING["uid"]}" '
               f'src="file://{urllib.parse.quote(DING["src"])}"/></asset>')
pop_id = re.search(r'<asset id="([^"]+)" name="Censor sound', s).group(1)
pop_name = re.search(r'<asset id="[^"]+" name="(Censor sound[^"]*)"', s).group(1)

inserts = {}
def add(at, xml):
    p = parent_at(at)
    local = p["start"] + (snap(at) - p["off"])
    inserts.setdefault(p["pos"], []).append(xml.replace("{OFF}", ft(local)))

# lanes: start above anything the user already has in that parent
def top_lane(at):
    p = parent_at(at); i = spine.index(p)
    seg = s[p["pos"]: spine[i + 1]["pos"] if i + 1 < len(spine) else len(s)]
    return max([int(x) for x in re.findall(r'lane="(\d+)"', seg)] + [0])

report = []
lane = top_lane(LOGO_IN) + 1
for k, (path, x, y, wpx) in enumerate(LOGOS):
    at = LOGO_IN + k * LOGO_GAP
    rid, nm, w, h = still_asset(path, f"logo{k}")
    sc = scale_for(w, h, wpx)
    add(at, f'<video ref="{rid}" lane="{lane + k}" offset="{{OFF}}" name="{nm}" start="3600s" duration="{ft(snap(LOGO_OUT) - snap(at))}">'
            f'<adjust-transform position="{x} {y}" scale="{sc} {sc}"/></video>')
    add(at, f'<asset-clip ref="{ding_id}" lane="{-4 - k}" offset="{{OFF}}" name="{DING["name"]}" start="{ft(Fr(DING["start"]).limit_denominator(1000))}" '
            f'duration="{ft(Fr(DING["length"]).limit_denominator(1000))}" audioRole="dialogue"><adjust-volume amount="{DING["vol"]}"/></asset-clip>')
    report.append(f"{float(snap(at)):6.3f}  {nm}  -> {LOGO_OUT}  + ding")

lane = top_lane(POPS[0][0]) + 1
for k, (at, stamp, x, y, wpx) in enumerate(POPS):
    rid, nm, w, h = still_asset(SS(stamp), f"pop{k}")
    sc = scale_for(w, h, wpx)
    add(at, f'<video ref="{rid}" lane="{lane + k}" offset="{{OFF}}" name="{nm}" start="3600s" duration="{ft(snap(POPS_OUT) - snap(at))}">'
            f'<adjust-transform position="{x} {y}" scale="{sc} {sc}"/></video>')
    add(at, f'<asset-clip ref="{pop_id}" lane="{-4 - k % 2}" offset="{{OFF}}" name="{pop_name}" start="{round(0.997 * 48000)}/48000s" '
            f'duration="{round(0.12 * 48000)}/48000s" audioRole="dialogue"><adjust-volume amount="{POP_VOL}"/></asset-clip>')
    report.append(f"{float(snap(at)):6.3f}  {stamp}  -> {POPS_OUT}  + pop")

for pos in sorted(inserts, reverse=True):
    tag_end = s.find(">", pos) + 1
    if s[tag_end - 2] == "/":
        tag = re.match(r"<([\w-]+)", s[pos:]).group(1)
        s = s[:tag_end - 2] + ">" + "".join(inserts[pos]) + f"</{tag}>" + s[tag_end:]
    else:
        s = s[:tag_end] + "".join(inserts[pos]) + s[tag_end:]
s = s.replace("</resources>", "\n".join(res) + "\n</resources>", 1)
s = re.sub(r'<project name="[^"]+"( uid="[^"]+")?( modDate="[^"]+")?', f'<project name="{PROJECT_NAME}"', s, count=1)
os.makedirs(OUT, exist_ok=True)
open(f"{OUT}/Info.fcpxml", "w").write(s)
print("logo in (marker):", LOGO_IN); print("\n".join(report)); print("->", OUT)
