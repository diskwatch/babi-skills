import sys, xml.etree.ElementTree as ET
from fractions import Fraction as F
def T(s):
    s = (s or "0s").rstrip("s"); return F(s) if "/" not in s else F(*map(int, s.split("/")))
root = ET.parse(sys.argv[1]).getroot(); spine = root.find(".//project//spine")
ends, clips = set(), []
for c in spine:
    off, st, du = T(c.get("offset")), T(c.get("start")), T(c.get("duration")); ends.add(off + du)
    for k in c:
        if k.tag == "asset-clip" and k.get("lane") and int(k.get("lane")) > 0 and k.get("enabled", "1") == "1":
            t = off + T(k.get("offset")) - st; clips.append((t, t + T(k.get("duration")), k.get("name")))
clips.sort(); starts = {c[0] for c in clips}; bad = 0
for a, z, n in clips:
    if z not in starts and z not in ends:
        bad += 1; near = min(ends, key=lambda e: abs(e - z))
        print(f"  B-roll {n} ends {float(z):.3f}, nearest clip end {float(near):.3f} (off by {float(z-near)*60:+.1f} frames)")
print(f"{sys.argv[1].split('/')[-1]}: {len(clips)} B-roll shots, {bad} end off a clip edge")
