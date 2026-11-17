"""Dump every spine piece + every connected item (all tags) with timeline time, lane, src, dur, enabled, transform, volume, title text."""
import sys, xml.etree.ElementTree as ET
from fractions import Fraction as F
def T(s):
    s = (s or "0s").rstrip("s"); return F(s) if "/" not in s else F(*map(int, s.split("/")))
root = ET.parse(sys.argv[1]).getroot()
spine = root.find(".//project//spine")
rows=[]
for c in spine:
    off, st, du = T(c.get("offset")), T(c.get("start")), T(c.get("duration"))
    rows.append((float(off),0,f"SPINE {c.tag} {c.get('name')} src {float(st):.3f}-{float(st+du):.3f} dur {float(du):.3f}"))
    for k in c:
        if k.get("lane") is None: continue
        ko = T(k.get("offset")); t = off + ko - st; d=T(k.get("duration"))
        ex=[]
        tr=k.find("adjust-transform")
        if tr is not None: ex.append(f"tr pos={tr.get('position')} sc={tr.get('scale')}")
        v=k.find("adjust-volume")
        if v is not None: ex.append(f"vol={v.get('amount')}")
        for p in k.findall("param"):
            if p.get("name")=="Position": ex.append(f"P={p.get('value')}")
        if k.tag=="title":
            txt="".join(x.text or "" for x in k.iter("text-style") if x.text)
            sz=[x.get("fontSize") for x in k.iter("text-style") if x.get("fontSize")]
            ex.append(f"'{txt}' sz={sz[:1]}")
        rows.append((float(t),int(k.get("lane")),f"{k.tag} {(k.get('name') or '')[:30]} src {float(T(k.get('start'))):.3f} dur {float(d):.3f} {'OFF' if k.get('enabled')=='0' else ''} {' '.join(ex)}"))
for t,l,s in sorted(rows, key=lambda r:(r[0],r[1])):
    print(f"{t:8.3f} L{l:3d} {s}")
