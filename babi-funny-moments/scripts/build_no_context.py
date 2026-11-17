"""'Moments from the office w/o context' reel -> FCPXML (Final Cut), copying Membership.io's own format
(refs DfQiRczRI7m, DfsArX5O_1e, 2026-11-17):

  9:16 project, the 4K 16:9 shot in a middle BAND (y 656-1264, black above/below via band_mask PNG on top),
  two-line condensed header above the band for the whole reel, one small bold white caption per line under it,
  rapid out-of-context one-liners (0.5-3 s), punch-in zooms (jump to 1.4-2x on a word), and video-only
  close-up inserts of hands/details over the speaker's audio.

  python build_no_context.py spec.json OUT.fcpxml

spec.json:
 {"media_dir":..., "mask":".../band_mask_1080x1920.png", "event":..., "project":...,
  "header":{"text":"line1\\nline2","font":"Avenir Next Condensed","face":"Medium","size":34,"y":234},
  "cap":{"font":"Helvetica Neue","face":"Bold","size":27,"y":-210},
  "pieces":[{"clip":"C4693","in":121.46,"out":123.5,"tail":0.25,
             "zoom":[s,u,v],                       # optional static punch for the whole piece (u,v = 0..1 in the 16:9 frame)
             "split":[{"at":95.9,"zoom":[1.6,0.45,0.42]}],   # optional jump-cut punch-ins inside the piece (source time)
             "caps":[["you're gonna type in a question",121.46,122.7],["blah blah blah",123.1,123.5]],
             "inserts":[{"clip":"C4693","src":176.6,"from":123.05,"to":123.5,"zoom":[2.0,0.55,0.45]}]}]}
Edges: in = given - 0.05 s; out = given, extended until the audio falls to the room floor (<= tail, default 0.25 s) + 0.05 s.
"""
import json, subprocess, sys
import numpy as np
from fractions import Fraction as F
from urllib.parse import quote
from xml.sax.saxutils import escape

cfg = json.load(open(sys.argv[1])); OUT = sys.argv[2]; D = cfg["media_dir"]
FD = F(1001, 30000); PW, PH = 1080, 1920; BAND_H = PW * 9 / 16

def g(x): return F(round(F(x) / FD)) * FD
def r(x):
    x = F(x); return f"{x.numerator}/{x.denominator}s" if x.denominator != 1 else f"{x.numerator}s"

_rms = {}
def rms(c):
    if c not in _rms:
        a = np.frombuffer(subprocess.check_output(["ffmpeg", "-v", "error", "-i", f"{D}/{c}.MP4", "-map", "0:a:0",
            "-ac", "1", "-ar", "16000", "-f", "s16le", "-"]), np.int16).astype(np.float32)
        n = len(a) // 800; v = 20 * np.log10(np.sqrt((a[:n * 800].reshape(n, 800) ** 2).mean(1)) + 1e-3)
        _rms[c] = (v, np.percentile(v, 10))
    return _rms[c]

def out_edge(c, b, tail):
    v, fl = rms(c); k = int(b / 0.05); lim = k + int(tail / 0.05)
    while k < lim and v[k] > fl + 8: k += 1
    return max(b, k * 0.05) + 0.05

def dur(c):
    return F(json.loads(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json",
        f"{D}/{c}.MP4"]))["format"]["duration"]).limit_denominator(100000)

def xform(z):
    if not z: return ""
    s, u, v = z; h = 1 / (2 * s)
    u = min(max(u, h), 1 - h); v = min(max(v, h), 1 - h)               # never show past the frame edge
    X = PW * u; Y = PH / 2 + (v - 0.5) * BAND_H
    px = -s * (X - PW / 2) / (PH / 100); py = s * (Y - PH / 2) / (PH / 100)
    return f'<adjust-transform position="{px:.3f} {py:.3f}" scale="{s:.4f} {s:.4f}"/>'

def title(lane, off, d, name, text, st, n):
    return (f'<title ref="eT" lane="{lane}" offset="{off}" name="{escape(name)}" start="3600s" duration="{r(d)}">'
            f'<param name="Position" key="9999/999166631/999166633/1/100/101" value="0 {st["y"]}"/>'
            f'<param name="Flatten" key="9999/999166631/999166633/2/351" value="1"/>'
            f'<param name="Alignment" key="9999/999166631/999166633/2/354/999169573/401" value="1 (Center)"/>'
            f'<text><text-style ref="ts{n}">{escape(text)}</text-style></text>'
            f'<text-style-def id="ts{n}"><text-style font="{st["font"]}" fontSize="{st["size"]}" fontFace="{st["face"]}" fontColor="1 1 1 1" '
            f'alignment="center"/></text-style-def></title>')

# ---- spine: pieces (split into punch-in segments) ----
clips = sorted({p["clip"] for p in cfg["pieces"]} | {i["clip"] for p in cfg["pieces"] for i in p.get("inserts", [])})
spine = []; off = F(0); log = []
for k, p in enumerate(cfg["pieces"], 1):
    a = g(p["in"] - 0.05); b = g(out_edge(p["clip"], p["out"], p.get("tail", 0.25)))
    pts = [a] + [g(s["at"]) for s in p.get("split", [])] + [b]
    zs = [p.get("zoom")] + [s["zoom"] for s in p.get("split", [])]
    p["_t0"] = off; p["_a"] = a; p["_len"] = b - a
    for j in range(len(pts) - 1):
        spine.append(dict(clip=p["clip"], st=pts[j], du=pts[j + 1] - pts[j], off=off, zoom=zs[j], name=f'{k:02d}{"abc"[j] if len(pts) > 2 else ""} {p["caps"][0][0] if p.get("caps") else ""}'[:40], kids=[]))
        off += pts[j + 1] - pts[j]
    log.append(f'{float(p["_t0"]):6.2f} +{float(b - a):4.2f}s {p["clip"]} {float(a):7.2f}  {" / ".join(c[0] for c in p.get("caps", []))}')
TOTAL = off

def host(t):
    for s in spine:
        if s["off"] <= t < s["off"] + s["du"]: return s
    return spine[-1]
def attach(t, xml):
    s = host(t); s["kids"].append(xml.replace("@OFF@", r(s["st"] + (t - s["off"]))))

# ---- captions (one lane, clipped so they never overlap) ----
caps = []
for p in cfg["pieces"]:
    for txt, ca, cb in p.get("caps", []):
        caps.append([g(p["_t0"] + max(F(ca) - p["_a"], 0)), g(p["_t0"] + F(cb) - p["_a"] + F(1, 10)), txt])
caps.sort()
for i in range(len(caps)):
    nxt = caps[i + 1][0] if i + 1 < len(caps) else TOTAL
    caps[i][1] = min(caps[i][1], nxt)
    assert caps[i][1] > caps[i][0], caps[i]
for n, (ca, cb, txt) in enumerate(caps, 2):
    attach(ca, title(4, "@OFF@", cb - ca, txt, txt, cfg["cap"], n))

# ---- inserts (video only, lane 1) ----
for p in cfg["pieces"]:
    for ins in p.get("inserts", []):
        t0 = g(p["_t0"] + F(ins["from"]) - p["_a"]); t1 = g(p["_t0"] + F(ins["to"]) - p["_a"])
        t1 = min(t1, p["_t0"] + p["_len"])
        attach(t0, f'<asset-clip ref="a_{ins["clip"]}" lane="1" offset="@OFF@" name="insert {ins["clip"]} {ins["src"]}" start="{r(g(ins["src"]))}" '
                   f'duration="{r(t1 - t0)}" srcEnable="video" tcFormat="NDF">{xform(ins.get("zoom"))}</asset-clip>')

# ---- header + mask over the whole reel, anchored to the first clip ----
hdr = cfg["header"]
spine[0]["kids"].insert(0, title(3, r(spine[0]["st"]), TOTAL, "header", hdr["text"], hdr, 1))
spine[0]["kids"].insert(0, f'<video ref="mask" lane="2" offset="{r(spine[0]["st"])}" name="band mask" start="3600s" duration="{r(TOTAL)}"/>')

res = [f'<format id="r1" name="FFVideoFormat1080x1920p2997" frameDuration="{r(FD)}" width="1080" height="1920" colorSpace="1-1-1 (Rec. 709)"/>',
       f'<format id="r2" name="FFVideoFormat2160p2997" frameDuration="{r(FD)}" width="3840" height="2160" colorSpace="1-1-1 (Rec. 709)"/>',
       '<format id="r3" name="FFVideoFormatRateUndefined" width="1080" height="1920" colorSpace="1-1-1 (Rec. 709)"/>']
for c in clips:
    res.append(f'<asset id="a_{c}" name="{c}" start="0s" duration="{r(g(dur(c)) - FD)}" hasVideo="1" format="r2" hasAudio="1" videoSources="1" '
               f'audioSources="1" audioChannels="2" audioRate="48000"><media-rep kind="original-media" src="file://{quote(D + "/" + c + ".MP4")}"/></asset>')
res.append(f'<asset id="mask" name="band_mask_1080x1920" start="0s" duration="0s" hasVideo="1" format="r3" videoSources="1">'
           f'<media-rep kind="original-media" src="file://{quote(cfg["mask"])}"/></asset>')
res.append('<effect id="eT" name="Basic Title" uid=".../Titles.localized/Bumper:Opener.localized/Basic Title.localized/Basic Title.moti"/>')
sp = []
for s in spine:
    sp.append(f'<asset-clip ref="a_{s["clip"]}" name="{escape(s["name"])}" offset="{r(s["off"])}" start="{r(s["st"])}" duration="{r(s["du"])}" '
              f'tcFormat="NDF" audioRole="dialogue">{xform(s["zoom"])}' + "".join(s["kids"]) + '</asset-clip>')
X = ('<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE fcpxml>\n<fcpxml version="1.11">\n<resources>\n' + "\n".join(res) + '\n</resources>\n'
     f'<library><event name="{escape(cfg["event"])}"><project name="{escape(cfg["project"])}">'
     f'<sequence format="r1" duration="{r(TOTAL)}" tcStart="0s" tcFormat="NDF" audioLayout="stereo" audioRate="48k"><spine>\n'
     + "\n".join(sp) + '\n</spine></sequence></project></event></library>\n</fcpxml>\n')
open(OUT, "w").write(X)
print("\n".join(log)); print(f"TOTAL {float(TOTAL):.2f}s  spine clips {len(spine)}  captions {len(caps)}  inserts {sum(len(p.get('inserts', [])) for p in cfg['pieces'])}")
