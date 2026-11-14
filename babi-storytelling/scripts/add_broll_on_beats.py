"""Add one round of B-roll to a copy of the user's Creator Lab edit.
Rule (from the user's own picks): a burst STARTS on a word Stu says, cuts INSIDE the burst land on the song's
beat grid (Final Cut Option-B grid ~= librosa beats - 0.04 s), and the burst ENDS on the talking-head clip's end.
"""
import re, os, json
from fractions import Fraction as Fr

SRC = os.path.expanduser("~/Desktop/CLR user broll.fcpxmld/Info.fcpxml")
REF = os.path.expanduser("~/Desktop/CLR fcp export.fcpxmld/Info.fcpxml")
OUT = os.path.expanduser("~/Desktop/Creator Lab Reel - broll v1.fcpxmld")
HERE = os.path.dirname(os.path.abspath(__file__))
FPS = 60
GRID_SHIFT = -0.04

beats = [b + GRID_SHIFT for b in json.load(open(f"{HERE}/beats.json"))["beats"]]

# (start word time, [shots]) ; a shot is (clip, in) or a list of alternates [(clip,in) enabled, (clip,in) disabled...]
# optional 'cuts' overrides beat-snapped cut points (used where the words themselves are the rhythm)
BURSTS = [
    dict(at=15.13, why="loved it", shots=[("9873", 0.5), ("9862", 7.0)]),
    dict(at=18.39, why="lost their minds", shots=[[("9879", 7.0), ("9879", 11.8)]]),
    dict(at=22.04, why="major announcement", shots=[("9866", 0.3)]),
    dict(at=24.04, why="teach / brand new tool", shots=[("9868", 1.0), ("9887", 4.5), ("9884", 12.0), ("9888", 3.2)]),
    dict(at=28.95, why="love it / rave", shots=[("9883", 0.3), ("9894", 0.3), ("9872", 0.6)]),
    dict(at=32.38, why="log off", shots=[("9865", 10.0)]),
    dict(at=36.48, why="Marcus (name -> stacked)", shots=[[("9887", 1.0), ("9888", 0.5), ("9890", 3.0)], ("9878", 7.5)]),
    dict(at=41.07, why="looked at him like", shots=[[("9891", 2.0), ("9894", 7.0)]]),
    dict(at=43.07, why="doorway", shots=[("9865", 13.5)]),
    dict(at=45.09, why="Creator Lab", shots=[("9860", 3.4)]),
    dict(at=46.63, why="where you're already working", shots=[("9884", 26.4)]),
    dict(at=49.50, why="Claude / any AI tool", shots=[("9879", 17.0), ("9883", 10.5)]),
    dict(at=54.66, why="chat absolutely lost it", shots=[("9878", 14.5), ("9879", 11.8)]),
    dict(at=56.61, why="team / breakout rooms / stuff done / excited",
         shots=[("9891", 4.0), ("9895", 2.4), ("9890", 3.0), ("9890", 6.0), ("9894", 7.0), ("9873", 5.4)]),
    dict(at=64.10, why="teach / do / get the thing done", shots=[("9869", 2.5), ("9895", 5.0), ("9855", 4.6)],
         cuts=[65.02, 65.84]),
    dict(at=68.39, why="done in 90 minutes / new world", shots=[("9899", 20.0), ("9904", 18.0), ("9905", 1.5)]),
]

s = open(SRC).read()
ref = open(REF).read()
t = lambda x: Fr(x.rstrip("s")) if x else Fr(0)
snap = lambda sec: Fr(round(sec * FPS), FPS)
fr = lambda f: f"{int(f * 6000)}/6000s" if (f * 6000).denominator == 1 else f"{f.numerator * 100}/{f.denominator * 100}s"

def ftime(f):  # Fraction -> fcpxml rational
    f = Fr(f).limit_denominator(60000)
    return f"{f.numerator}/{f.denominator}s" if f.denominator != 1 else f"{f.numerator}s"

# spine clips (top-level children of the project spine)
proj = s.find("<spine>", s.find("<project"))
spine_clips = []
depth = 0
for m in re.finditer(r"<(/?)(asset-clip|clip|gap|video|title)\b([^>]*?)(/?)>", s[proj:]):
    closing, tag, attrs, selfclose = m.group(1), m.group(2), m.group(3), m.group(4)
    if closing:
        depth -= 1
        continue
    if depth == 0 and 'lane=' not in attrs:
        g = lambda k: (re.search(k + r'="([^"]+)"', attrs) or [None, None])[1]
        spine_clips.append(dict(tag=tag, raw=m.group(0), pos=proj + m.start(), off=t(g("offset")), start=t(g("start")),
                                dur=t(g("duration")), name=g("name")))
    if not selfclose:
        depth += 1
spine_clips = [c for c in spine_clips if c["dur"]]

def parent_at(x):
    return next(c for c in spine_clips if c["off"] <= x < c["off"] + c["dur"])

# --- assets: reuse from user's export, else copy from REF with its format
assets = {m.group(2): m.group(1) for m in re.finditer(r'<asset id="([^"]+)" name="(IMG_\d+)"', s)}
res_add = []
def asset_id(clip):
    name = f"IMG_{clip}"
    if name in assets:
        return assets[name]
    m = re.search(r'<asset id="([^"]+)" name="' + name + r'"[^>]*>.*?</asset>', ref, re.S)
    assert m, f"{name} not in user export or reference export"
    a, old = m.group(0), m.group(1)
    fmt = re.search(r'format="([^"]+)"', a).group(1)
    fdef = re.search(r'<format id="' + fmt + r'"[^>]*/>', ref).group(0)
    nid, nfmt = f"br_{clip}", f"brfmt_{clip}"
    res_add.append(fdef.replace(f'id="{fmt}"', f'id="{nfmt}"'))
    a = a.replace(f'id="{old}"', f'id="{nid}"', 1).replace(f'format="{fmt}"', f'format="{nfmt}"', 1)
    res_add.append(re.sub(r"<bookmark>.*?</bookmark>", "", a, flags=re.S))
    assets[name] = nid
    return nid

def clip_end_after(x):
    return parent_at(x)["off"] + parent_at(x)["dur"]

inserts = {}  # parent pos -> list of xml
report = []
for b in BURSTS:
    a = snap(b["at"])
    end = clip_end_after(a)
    n = len(b["shots"])
    if "cuts" in b:
        cuts = [snap(c) for c in b["cuts"]]
    else:
        cand = [snap(x) for x in beats if float(a) + 0.4 < x < float(end) - 0.4]
        cuts = []
        for k in range(1, n):
            ideal = float(a) + (float(end) - float(a)) * k / n
            pool = [c for c in cand if c not in cuts and (not cuts or c > cuts[-1])]
            assert pool, f"not enough beats for burst at {b['at']}"
            cuts.append(min(pool, key=lambda c: abs(float(c) - ideal)))
    edges = [a] + cuts + [end]
    p = parent_at(a)
    for k, shot in enumerate(b["shots"]):
        t0, t1 = edges[k], edges[k + 1]
        alts = shot if isinstance(shot, list) else [shot]
        for j, (clip, src_in) in enumerate(alts):
            rid = asset_id(clip)
            local = p["start"] + (t0 - p["off"])
            xml = (f'<asset-clip ref="{rid}" lane="{1 + j}" offset="{ftime(local)}" name="IMG_{clip}" '
                   f'start="{ftime(snap(src_in))}" duration="{ftime(t1 - t0)}"' + (' enabled="0"' if j else '') +
                   f' audioRole="dialogue"><adjust-volume amount="-96dB"/></asset-clip>')
            inserts.setdefault(p["pos"], []).append(xml)
        report.append(f'{float(t0):6.2f}-{float(t1):6.2f}  {b["why"]:<45} ' +
                      " | ".join(f"IMG_{c}@{i}" + ("" if j == 0 else " (off)") for j, (c, i) in enumerate(alts)))

# insert bottom-up so earlier positions stay valid
for pos in sorted(inserts, reverse=True):
    tag_end = s.find(">", pos) + 1
    if s[tag_end - 2] == "/":  # self-closing parent: open it up
        tag = re.match(r"<([\w-]+)", s[pos:]).group(1)
        s = s[:tag_end - 2] + ">" + "".join(inserts[pos]) + f"</{tag}>" + s[tag_end:]
    else:
        s = s[:tag_end] + "".join(inserts[pos]) + s[tag_end:]
s = s.replace("</resources>", "\n".join(res_add) + "\n</resources>", 1)
s = re.sub(r'<project name="[^"]+"( uid="[^"]+")?( modDate="[^"]+")?', '<project name="Creator Lab Reel - broll v1"', s, count=1)
os.makedirs(OUT, exist_ok=True)
open(f"{OUT}/Info.fcpxml", "w").write(s)
print("\n".join(report))
print("new assets:", [x for x in assets.values() if x.startswith("br_")])
