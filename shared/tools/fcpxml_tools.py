"""Small FCPXML helpers for iterating on Babi's own edits (no new project per round).

  diff    <mine.fcpxml> <babi.fcpxmld|.fcpxml>   spine clips (source in/out, speed, pitch) + SFX/music, side by side
  patch   <babi.fcpxmld|.fcpxml> <out.fcpxml>    shrink/raise talking captions to the IG safe zone (40/48 pt, <=590 px, Position -252)
  strip   <babi.fcpxmld|.fcpxml> <out.fcpxml> <new project name>   copy with every <title> removed (caption-free export)

After patch: open the .fcpxml in Final Cut, choose the library, then press **Replace** (same project name = edit in place).
After strip: the new name imports as a separate small project; Babi exports it with Cmd-E.
"""
import sys, re, os
from fractions import Fraction as F

def load(p):
    if p.endswith(".fcpxmld") or os.path.isdir(p): p = os.path.join(p, "Info.fcpxml")
    return open(p).read()

def t(s): return F(s.rstrip("s")) if s else F(0)

def spine(x):
    sp = re.search(r"<spine>(.*)</spine>", x, re.S).group(1)
    out, depth = [], 0
    for m in re.finditer(r"<(/?)(asset-clip|clip|gap|title|video|audio|ref-clip)\b([^>]*?)(/?)>", sp):
        close, tag, a, selfc = m.groups()
        if close: depth -= 1; continue
        if depth == 0:
            g = lambda k: (re.search(" " + k + r'="([^"]*)"', a) or [None, None])[1]
            seg = sp[m.end():m.end() + 3000]
            seg = re.sub(r"<title.*?</title>", "", seg, flags=re.S)
            seg = seg[:seg.find("</asset-clip>")] if "</asset-clip>" in seg else seg[:800]
            tm = re.search(r"<timeMap([^>]*)>(.*?)</timeMap>", seg, re.S)
            s, pitch = F(1), "-"
            if tm:
                pts = re.findall(r'time="([^"]+)" value="([^"]+)"', tm.group(2))
                (t0, v0), (t1, v1) = pts[0], pts[-1]
                s = (t(v1) - t(v0)) / (t(t1) - t(t0))
                pitch = (re.search(r'preservesPitch="(\d)"', tm.group(1)) or [0, "1"])[1]
            st, du = t(g("start")), t(g("duration"))
            z = re.search(r'<adjust-transform[^>]*scale="([^"]+)"', seg)
            out.append((g("name"), float(t(g("offset"))), float(st * s), float((st + du) * s), float(s), pitch, z.group(1) if z else ""))
        if not selfc: depth += 1
    return out

def sounds(x):
    return [(n, v) for n, v in re.findall(r'<asset-clip [^>]*?name="((?:SFX|Music)[^"]*)"[^>]*>\s*(?:<adjust-volume amount="([^"]+)")?', x)]

def cmd_diff(a, b):
    for label, x in (("MINE", load(a)), ("BABI", load(b))):
        print(label)
        for n, o, s0, s1, sp, p, z in spine(x):
            print(f"  {n:10} @{o:6.2f}  src {s0:6.2f}-{s1:6.2f}  x{sp:.2f}  pitch:{p}  {('zoom ' + z) if z else ''}")
        print("  sounds:", sounds(x))

def cmd_patch(src, out):
    x = load(src); n = [0]
    def fix(m):
        tt = m.group(0)
        if 'name="Caption - ' not in tt[:300]: return tt
        word = " ".join(re.findall(r'<text-style ref="[^"]+">([^<]*)</text-style>', tt)).strip()
        old = int(re.search(r'fontSize="(\d+)"', tt).group(1))
        size = int(min(48 if old >= 60 or old == 48 else 40, 590 / (1.45 * max(len(word), 1))))
        tt = re.sub(r'fontSize="\d+"', f'fontSize="{size}"', tt, 1)
        tt = re.sub(r'(key="9999/999166631/999166633/1/100/101" value=")0 -?\d+(")', r"\g<1>0 -252\g<2>", tt)
        n[0] += 1; return tt
    x = re.sub(r"<title [^>]*>.*?</title>", fix, x, flags=re.S)
    open(out, "w").write(x); print("captions patched:", n[0])

def cmd_strip(src, out, name):
    x = load(src); k = len(re.findall(r"<title ", x))
    x = re.sub(r"<title [^>]*>.*?</title>", "", x, flags=re.S)
    x = re.sub(r'<project name="[^"]*"', f'<project name="{name}"', x, 1)
    open(out, "w").write(x); print("titles removed:", k)

if __name__ == "__main__":
    c = sys.argv[1]
    {"diff": lambda: cmd_diff(*sys.argv[2:4]), "patch": lambda: cmd_patch(*sys.argv[2:4]),
     "strip": lambda: cmd_strip(*sys.argv[2:5])}[c]()
