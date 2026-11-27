"""What did Babi change? Compare Claude's FCPXML with Babi's export of the same projects.

  python3 recover.py mine.fcpxml "his export/Info.fcpxml" [project-substring]

Per project: edges he restored (RECOVER) or trimmed (TRIM) on each spine piece, with the words in that slice (whisper,
optional) and its loudness (10 ms RMS max from the source file; quiet < -35 dB = silence), pieces cut or added,
connected clips added/removed/moved (B-roll, photos, SFX, music: level, length), caption/header position + size moves,
and dialogue gain changes. Feed the numbers into the skill (SETTINGS core rules), not vague adjectives.
"""
import sys, subprocess, urllib.parse, collections, numpy as np
import xml.etree.ElementTree as ET
from fcpxml_flat import load, flatten

def srcpaths(path):
    out = {}
    for a in ET.parse(path).getroot().iter("asset"):
        mr = a.find("media-rep")
        if mr is not None:
            out[mr.get("src").split("/")[-1].replace("%20", " ")] = urllib.parse.unquote(mr.get("src")[7:])
    return out

_cache = {}
def rms_max(path, a, b):
    if path not in _cache:
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", "16000", "-f", "s16le", "-"], capture_output=True).stdout
        _cache[path] = np.frombuffer(raw, np.int16).astype(float) / 32768
    x = _cache[path][int(min(a, b) * 16000): int(max(a, b) * 16000)]
    if len(x) < 160:
        return -99.0
    f = x[: len(x) // 160 * 160].reshape(-1, 160)
    return round(float(20 * np.log10(np.sqrt((f ** 2).mean(1)).max() + 1e-9)), 1)

def main(mine, his, only=""):
    A, B, P = load(mine), load(his), srcpaths(his)
    for name in sorted(B):
        if only not in name or name not in A:
            continue
        ma, _ = flatten(*A[name]); hb, hd = flatten(*B[name])
        print(f"\n## {name}  ({hd:.2f}s)")
        ms = [i for i in ma if i["depth"] == 0]; hs = [i for i in hb if i["depth"] == 0]; used = set()
        for h in hs:
            c = [(min(m["start"] + m["dur"], h["start"] + h["dur"]) - max(m["start"], h["start"]), k) for k, m in enumerate(ms) if m["src"] == h["src"]]
            c = [x for x in c if x[0] > 0]
            if not c:
                print(f"  NEW piece {h['src']} {h['start']:.2f}-{h['start'] + h['dur']:.2f}"); continue
            k = max(c)[1]; m = ms[k]; used.add(k)
            for side, a, b in (("HEAD", m["start"], h["start"]), ("TAIL", m["start"] + m["dur"], h["start"] + h["dur"])):
                d = b - a
                if abs(d) >= 0.02:
                    kind = "RECOVER" if (side == "HEAD" and d < 0) or (side == "TAIL" and d > 0) else "TRIM"
                    lvl = rms_max(P[h["src"]], a, b) if h["src"] in P else None
                    print(f"  {kind:7} {side} {d:+.2f}s  {h['src']} @{a:.2f}  max {lvl} dB  {'(silence)' if lvl is not None and lvl < -35 else '(speech)'}")
            if m["vol"] != h["vol"]:
                print(f"  GAIN {h['src']} {m['vol']} -> {h['vol']}")
        for k, m in enumerate(ms):
            if k not in used:
                print(f"  CUT piece {m['src']} {m['start']:.2f}-{m['start'] + m['dur']:.2f} ({m['dur']:.2f}s)")
        key = lambda i: (i["tag"], i["src"] or i["name"])
        ca = [i for i in ma if i["depth"] > 0 and i["tag"] != "title"]; cb = [i for i in hb if i["depth"] > 0 and i["tag"] != "title"]
        hit = set()
        for x in cb:
            m = [k for k, y in enumerate(ca) if k not in hit and key(y) == key(x) and abs(y["start"] - x["start"]) < 0.05]
            if not m:
                print(f"  + {x['tag']} {(x['src'] or x['name'])[:40]} {x['abs']:.2f}-{x['end']:.2f} vol={x['vol']} {x['xf']}"); continue
            y = ca[m[0]]; hit.add(m[0]); d = []
            for f in ("dur",):
                if abs(x[f] - y[f]) > 0.02: d.append(f"len {y[f]:.2f}->{x[f]:.2f}")
            if abs(x["abs"] - y["abs"]) > 0.2: d.append(f"moved {x['abs'] - y['abs']:+.2f}s")
            if x["vol"] != y["vol"]: d.append(f"vol {y['vol']}->{x['vol']}")
            if x["en"] != y["en"]: d.append(f"enabled {y['en']}->{x['en']}")
            if x["xf"].replace("0.0 ", "0 ") != y["xf"].replace("0.0 ", "0 "): d.append(f"transform {y['xf']} -> {x['xf']}")
            if d: print(f"  ~ {x['tag']} {(x['src'] or x['name'])[:40]}: " + ", ".join(d))
        for k, y in enumerate(ca):
            if k not in hit:
                print(f"  - {y['tag']} {(y['src'] or y['name'])[:40]} {y['abs']:.2f}-{y['end']:.2f}")
        ta = collections.Counter((t["pos"], t["xf"], t["size"]) for t in ma if t["tag"] == "title")
        tb = collections.Counter((t["pos"], t["xf"], t["size"]) for t in hb if t["tag"] == "title")
        if ta != tb:
            print(f"  titles (Position, transform, size): mine {dict(ta)}\n                                       his  {dict(tb)}")

if __name__ == "__main__":
    main(*sys.argv[1:4])
