"""Funny-moments selects -> FCPXML (Final Cut). Every source clip goes into the event as a browser clip,
then one project with each funny moment as its own clip (note + marker), in shooting order.

  python build_funny_moments.py moments.json OUT.fcpxml
moments.json = {"media_dir":..., "event":..., "project":..., "clips":["C4690",...],
                "moments":[{"clip":"C4693","in":391.6,"out":421.5,"label":"commute joke","laugh":true}, ...]}
Edges: in snaps to the quiet point just before speech (50 ms RMS); out runs until the room is quiet again
(laughs kept to their end, max +2 s), then +0.15 s.
"""
import json, subprocess, sys, os
import numpy as np
from fractions import Fraction as F
from urllib.parse import quote
from xml.sax.saxutils import escape

cfg = json.load(open(sys.argv[1])); OUT = sys.argv[2]
D = cfg["media_dir"]

def probe(c):
    j = json.loads(subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
        "stream=r_frame_rate,width,height:format=duration", "-of", "json", f"{D}/{c}.MP4"]))
    s = j["streams"][0]; n, d = map(int, s["r_frame_rate"].split("/"))
    return F(d, n), F(j["format"]["duration"]).limit_denominator(100000), s["width"], s["height"]

_rms = {}
def rms(c):
    if c not in _rms:
        a = np.frombuffer(subprocess.check_output(["ffmpeg", "-v", "error", "-i", f"{D}/{c}.MP4", "-map", "0:a:0",
            "-ac", "1", "-ar", "16000", "-f", "s16le", "-"]), np.int16).astype(np.float32)
        h = 800; n = len(a) // h
        r = 20 * np.log10(np.sqrt((a[:n * h].reshape(n, h) ** 2).mean(1)) + 1e-3)
        _rms[c] = (r, np.percentile(r, 10))
    return _rms[c]

def snap(c, a, b):
    r, floor = rms(c); thr = floor + 8; i = lambda t: int(t / 0.05)
    s = i(a)
    for k in range(i(a), max(i(a) - 8, 0), -1):          # walk back up to 0.4 s to the gap before the first word
        if r[k] < thr: s = k; break
    e = i(b)
    for k in range(i(b), min(i(b) + 40, len(r) - 1)):     # let the line/laugh die out (max +2 s)
        e = k
        if all(r[k:k + 4] < thr): break
    return max(s * 0.05 - 0.1, 0), e * 0.05 + 0.15

info = {c: probe(c) for c in cfg["clips"]}
fd = info[cfg["clips"][0]][0]; W, H = info[cfg["clips"][0]][2:]
def g(x): return F(round(F(x) / fd)) * fd
def r(x):
    x = F(x); return f"{x.numerator}/{x.denominator}s" if x.denominator != 1 else f"{x.numerator}s"

fmt = f"FFVideoFormat{W}x{H}p{round(1/float(fd)*100)}"
res = [f'<format id="r1" name="{fmt}" frameDuration="{r(fd)}" width="{W}" height="{H}" colorSpace="1-1-1 (Rec. 709)"/>']
for c in cfg["clips"]:
    _, dur, _, _ = info[c]
    res.append(f'<asset id="a_{c}" name="{c}" start="0s" duration="{r(g(dur) - fd)}" hasVideo="1" format="r1" hasAudio="1" videoSources="1" '
               f'audioSources="1" audioChannels="2" audioRate="48000"><media-rep kind="original-media" src="file://{quote(D + "/" + c + ".MP4")}"/></asset>')
browser = [f'<asset-clip ref="a_{c}" name="{c}" start="0s" duration="{r(g(info[c][1]) - fd)}" format="r1" tcFormat="NDF" audioRole="dialogue"/>' for c in cfg["clips"]]
spine, off, log = [], F(0), []
for n, m in enumerate(cfg["moments"], 1):
    a, b = snap(m["clip"], m["in"], m["out"])
    st = g(a); du = g(min(b, float(info[m["clip"]][1]) - 0.1) - a)
    lab = escape(f'{n:02d} {m["label"]}')
    spine.append(f'<asset-clip ref="a_{m["clip"]}" name="{lab}" offset="{r(off)}" start="{r(st)}" duration="{r(du)}" tcFormat="NDF" audioRole="dialogue">'
                 f'<note>{escape(m.get("note", m["label"]))}</note><marker start="{r(st)}" duration="{r(fd)}" value="{lab}"/></asset-clip>')
    log.append(f'{float(off):7.2f}  {m["clip"]} {float(st):7.2f}-{float(st+du):7.2f} ({float(du):5.2f}s)  {m["label"]}')
    off += du
X = ('<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE fcpxml>\n<fcpxml version="1.11">\n<resources>\n' + "\n".join(res) + '\n</resources>\n'
     f'<library><event name="{escape(cfg["event"])}">\n' + "\n".join(browser) +
     f'\n<project name="{escape(cfg["project"])}"><sequence format="r1" duration="{r(off)}" tcStart="0s" tcFormat="NDF" audioLayout="stereo" audioRate="48k"><spine>\n'
     + "\n".join(spine) + '\n</spine></sequence></project></event></library>\n</fcpxml>\n')
open(OUT, "w").write(X)
print("\n".join(log)); print(f"TOTAL {float(off):.2f}s, {len(spine)} moments -> {OUT}")
