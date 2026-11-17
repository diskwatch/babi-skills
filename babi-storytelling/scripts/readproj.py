"""Dump an FCPXML project: spine pieces (src ranges) and connected video clips in timeline time."""
import sys, xml.etree.ElementTree as ET
from fractions import Fraction as F
def T(s):
    s = (s or "0s").rstrip("s"); return F(s) if "/" not in s else F(*map(int, s.split("/")))
root = ET.parse(sys.argv[1]).getroot()
names = {a.get("id"): a.get("name") for a in root.iter("asset")}
spine = root.find(".//project//spine")
print("SPINE")
conn = []
for c in spine:
    if c.tag != "asset-clip": print("  ", c.tag, c.get("name")); continue
    off, st, du = T(c.get("offset")), T(c.get("start")), T(c.get("duration"))
    print(f"  tl {float(off):6.2f}-{float(off+du):6.2f}  src {float(st):7.2f}-{float(st+du):7.2f}  {c.get('name')}")
    for k in c:
        if k.tag in ("asset-clip", "video", "clip") and k.get("lane"):
            ko = T(k.get("offset")); t = off + ko - st
            ref = k.get("ref") or ""
            conn.append((float(t), int(k.get("lane")), k.get("name"), float(T(k.get("start"))), float(T(k.get("duration"))), k.get("enabled", "1")))
print("CONNECTED (lane>0 video / lane<0 audio)")
for t, ln, nm, s, d, en in sorted(conn):
    if ln > 0 or "Pop" in nm or "Ding" in nm:
        print(f"  tl {t:6.2f}-{t+d:6.2f} lane {ln:2d}  {nm[:28]:28s} src {s:7.2f}  dur {d:4.2f} {'(off)' if en=='0' else ''}")
