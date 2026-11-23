#!/usr/bin/env python3
"""Add knowledge-reel karaoke captions (smaller) to an exported Final Cut project, in place.

  python3 -I add_captions.py EXPORT_Info.fcpxml WORDS.json OUT.fcpxml [--s2f]

Caption recipe = babi-knowledge-reels (Basic Title, Helvetica Neue Bold, white, spoken word yellow
1 0.88 0 1, soft shadow, lowercase, no punctuation, <= 3 words / 16 chars), but SIZE 46 instead of 64
(Babi 2026-11-16: "use the caption style from here, but just smaller").
WORDS.json = whisper words on the project's own spine audio (timeline seconds).
--s2f also shrinks/lifts the Start2Finish pops so the caption line stays clear.
"""
import json, re, sys
from fractions import Fraction as F
import xml.etree.ElementTree as ET

SRC, WORDS, OUT = sys.argv[1:4]
S2F = "--s2f" in sys.argv
ST = dict(font="Helvetica Neue", face="Bold", size=46, white="1 1 1 1", yellow="1 0.88 0 1",
          cap_y=-288, lane=6, max_words=3, max_chars=16, gap_break=0.35)
BASIC_TITLE = ".../Titles.localized/Bumper:Opener.localized/Basic Title.localized/Basic Title.moti"
FIX = {"alex": "alix", "alex's": "alix's", "noll": "knoll", "meechi": "michi", "alejandro": "alejandra",
       "one": None}  # "one" handled in context below

def T(s):
    s = (s or "0s").rstrip("s")
    return F(s) if "/" not in s else F(*map(int, s.split("/")))
def fr(x): return F(round(F(x) * 60), 60)
def rs(x):
    x = F(x); return f"{x.numerator}/{x.denominator}s" if x.denominator != 1 else f"{x.numerator}s"

tree = ET.parse(SRC); root = tree.getroot(); res = root.find("resources")
ids = [int(re.sub(r"\D", "", e.get("id")) or 0) for e in res if e.get("id")]
nid = [max(ids) + 1]
eff = ET.SubElement(res, "effect", id=f"r{nid[0]}", name="Basic Title", uid=BASIC_TITLE)
spine = root.find(".//project//spine")
info = [dict(el=c, off=T(c.get("offset")), start=T(c.get("start")), dur=T(c.get("duration")))
        for c in spine if c.tag in ("asset-clip", "ref-clip")]   # ref-clip = compound clip; skipping it misplaced every caption (Nov 22 Tony)
end_all = info[-1]["off"] + info[-1]["dur"]
def attach(el, t):
    t = fr(t)
    p = next((c for c in info if c["off"] <= t < c["off"] + c["dur"]), info[-1])
    el.set("offset", rs(p["start"] + t - p["off"])); p["el"].append(el)

# --- tokens: clean, merge, fix spellings
raw = json.load(open(WORDS))
toks = []
for w in raw:
    s = w["w"]
    if toks and (s.startswith("-") or s.startswith(".")):        # "co -founder", "a .m."
        toks[-1]["w"] += s; toks[-1]["e"] = w["e"]; continue
    if toks and re.sub(r"\W", "", s.lower()) == re.sub(r"\W", "", toks[-1]["w"].lower()) and s.lower() in ("in",):
        continue                                                  # doubled "in In"
    toks.append(dict(w=s, s=w["s"], e=w["e"]))
for i, t in enumerate(toks):
    t["end_sent"] = t["w"].endswith((".", "?", "!"))
    c = re.sub(r"[.,?!\"]+", "", t["w"].lower()).strip()
    c = FIX.get(c, c) or c
    t["c"] = c
cl = [t["c"] for t in toks]
out = []
i = 0
while i < len(toks):
    t = toks[i]
    if cl[i:i + 3] == ["start", "to", "finish"]:
        m = dict(t, c="start2finish", e=toks[i + 2]["e"], end_sent=toks[i + 2]["end_sent"]); out.append(m); i += 3; continue
    if cl[i:i + 2] == ["9", "am"] or (cl[i] == "9" and i + 1 < len(cl) and cl[i + 1] in ("am", "a.m", "am.")):
        out.append(dict(t, c="9am", e=toks[i + 1]["e"], end_sent=toks[i + 1]["end_sent"])); i += 2; continue
    if cl[i:i + 4] == ["grades", "one", "to", "six"]:
        for k, c in enumerate(["grades", "1", "to", "6"]):
            out.append(dict(toks[i + k], c=c))
        i += 4; continue
    if cl[i:i + 3] == ["my", "own", "club"]:
        out += [dict(toks[i], c="my"), dict(toks[i + 1], c="run"), dict(toks[i + 2], c="club")]; i += 3; continue
    if cl[i] == "now" and i > 0 and out and out[-1]["c"] == "start2finish" and t["end_sent"]:
        out[-1]["end_sent"] = True; t = dict(t, end_sent=False)  # "...start to finish. now it's real"
    out.append(t); i += 1
toks = [t for t in out if t["c"]]

# --- chunks
chunks, cur = [], []
for t in toks:
    if cur and (len(cur) >= ST["max_words"] or len(" ".join(x["c"] for x in cur + [t])) > ST["max_chars"]
                or t["s"] - cur[-1]["e"] > ST["gap_break"]):
        chunks.append(cur); cur = []
    cur.append(t)
    if t["end_sent"]:
        chunks.append(cur); cur = []
if cur: chunks.append(cur)

tsn = [0]
def title(t0, t1, spans, name):
    e = ET.Element("title", ref=eff.get("id"), lane=str(ST["lane"]), name=name[:40], start="3600s", duration=rs(fr(t1) - fr(t0)))
    ET.SubElement(e, "param", name="Position", key="9999/999166631/999166633/1/100/101", value=f"0 {ST['cap_y']}")
    ET.SubElement(e, "param", name="Flatten", key="9999/999166631/999166633/2/351", value="1")
    ET.SubElement(e, "param", name="Alignment", key="9999/999166631/999166633/2/354/999169573/401", value="1 (Center)")
    txt = ET.SubElement(e, "text"); defs = []
    for s, col in spans:
        tsn[0] += 1; tid = f"cap{tsn[0]}"
        ET.SubElement(txt, "text-style", ref=tid).text = s
        d = ET.Element("text-style-def", id=tid)
        ET.SubElement(d, "text-style", font=ST["font"], fontSize=str(ST["size"]), fontFace=ST["face"], fontColor=col,
                      shadowColor="0 0 0 0.75", shadowOffset="4 315", shadowBlurRadius="8", alignment="center")
        defs.append(d)
    for d in defs: e.append(d)
    attach(e, t0)

starts = [c[0]["s"] for c in chunks] + [float(end_all)]
n = 0
for ci, ch in enumerate(chunks):
    chunk_end = min(starts[ci + 1], ch[-1]["e"] + 0.5, float(end_all))
    for wi, t in enumerate(ch):
        a = t["s"]; b = ch[wi + 1]["s"] if wi + 1 < len(ch) else chunk_end
        if fr(b) <= fr(a): continue
        spans = [((" " if k else "") + x["c"], ST["yellow"] if k == wi else ST["white"]) for k, x in enumerate(ch)]
        title(a, b, spans, " ".join(x["c"] for x in ch)); n += 1

# --- keep the Start2Finish pops clear of the caption line (caption centre ~1520 px)
if S2F:
    from PIL import Image
    gfx = {"S2F Running Reading Club title": (640, 520, 1120), "S2F kids reading": (215, 405, 1336),
           "S2F year-end girl": (220, 640, 1336)}
    sizes = {"S2F Running Reading Club title": (695, 150), "S2F kids reading": (720, 915), "S2F year-end girl": (450, 560)}
    for v in root.iter("video"):
        nm = v.get("name")
        if nm in gfx:
            wpx, cx, cy = gfx[nm]; w, h = sizes[nm]
            sc = round(wpx / (w * min(1080 / w, 1920 / h)), 4)
            tr = v.find("adjust-transform")
            tr.set("position", f"{round((cx - 540) / 19.2, 3)} {round(-(cy - 960) / 19.2, 3)}"); tr.set("scale", f"{sc} {sc}")

ET.indent(tree, "  ")
with open(OUT, "wb") as fh:
    fh.write(b'<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE fcpxml>\n\n')
    tree.write(fh, encoding="utf-8", xml_declaration=False)
widest = max(chunks, key=lambda c: len(" ".join(x["c"] for x in c)))
print(f"{OUT.split('/')[-1]}: {len(chunks)} caption groups, {n} titles; widest: '{' '.join(x['c'] for x in widest)}'")
print(" | ".join(" ".join(x["c"] for x in c) for c in chunks))
