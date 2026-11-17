#!/usr/bin/env python3
"""Patch Babi's exported edit in place (round 3 notes, 2026-11-16).

  python -I patch_v3.py CONFIG.json

CONFIG keys:
  src, out, words            export Info.fcpxml, output .fcpxml, whisper words (timeline s) of the cut
  browser_names              names that already have browser clips in the event (list)
  low_graphics               still names that sit low -> captions under them use the low position
  special_ref_names          spine asset names whose audio gets the "quoted clip" caption style
  stills: [{name_prefix, w_px, cx, cy}]                    resize existing stills (fit maths)
  new_stills: [{name, path, w, h, t, dur, w_px, cx, cy, lane}]   add a graphic
  sfx: [{asset_name, t, lane, db}]                          add a sound (copies an existing asset's in/len)
  pop_fix: {asset_name, start}                              set source in-point of every clip of that asset
What it always does: removes old captions (Position 0 -288), closes B-roll gaps < 0.3 s,
regenerates captions (size 42, raised +5.706 %), adds browser clips for used media missing from the event.
"""
import json, re, sys, urllib.parse as U
from fractions import Fraction as F
import xml.etree.ElementTree as ET

cfg = json.load(open(sys.argv[1]))
def T(s):
    s = (s or "0s").rstrip("s"); return F(s) if "/" not in s else F(*map(int, s.split("/")))
def fr(x): return F(round(F(x) * 60), 60)
def rs(x):
    x = F(x); return f"{x.numerator}/{x.denominator}s" if x.denominator != 1 else f"{x.numerator}s"

tree = ET.parse(cfg["src"]); root = tree.getroot(); res = root.find("resources")
assets = {a.get("id"): a for a in res.iter("asset")}
byname = {a.get("name"): a for a in assets.values()}
ids = [int(re.sub(r"\D", "", e.get("id")) or 0) for e in res if e.get("id")]
nid = [max(ids)]
def new_id(): nid[0] += 1; return f"r{nid[0]}"
event = root.find(".//event"); project = event.find("project")
spine = project.find(".//spine")
pieces = [dict(el=c, off=T(c.get("offset")), start=T(c.get("start")), dur=T(c.get("duration")), ref=c.get("ref"))
          for c in spine if c.tag == "asset-clip"]
end_all = pieces[-1]["off"] + pieces[-1]["dur"]
def piece_at(t):
    return next((p for p in pieces if p["off"] <= t < p["off"] + p["dur"]), pieces[-1])
def attach(el, t):
    t = fr(t); p = piece_at(t)
    el.set("offset", rs(p["start"] + t - p["off"])); p["el"].append(el)
def connected():
    for p in pieces:
        for k in list(p["el"]):
            if k.get("lane") is None: continue
            t = p["off"] + T(k.get("offset")) - p["start"]
            yield p, k, t, T(k.get("duration"))
log = []

# 1. drop old captions
n = 0
for p in pieces:
    for k in list(p["el"]):
        if k.tag == "title" and any(x.get("name") == "Position" and x.get("value") == "0 -288" for x in k.findall("param")):
            p["el"].remove(k); n += 1
log.append(f"removed {n} old caption titles")

# 2. resize stills Babi dropped in full-frame
def transform_for(w, h, w_px, cx, cy):
    sc = round(w_px / (w * min(1080 / w, 1920 / h)), 4)
    return f"{round((cx - 540) / 19.2, 3)} {round(-(cy - 960) / 19.2, 3)}", f"{sc} {sc}"
fmts = {f.get("id"): f for f in res.iter("format")}
for st in cfg.get("stills", []):
    for p, k, t, d in connected():
        if k.tag == "video" and (k.get("name") or "").startswith(st["name_prefix"]):
            f = fmts[assets[k.get("ref")].get("format")]
            pos, sc = transform_for(int(f.get("width")), int(f.get("height")), st["w_px"], st["cx"], st["cy"])
            for old in k.findall("adjust-transform"): k.remove(old)
            ET.SubElement(k, "adjust-transform", position=pos, scale=sc)
            log.append(f"resized {k.get('name')[:30]} at {float(t):.3f}: {pos} / {sc}")

# 3. new stills
for ns in cfg.get("new_stills", []):
    fid, aid = new_id(), new_id()
    ET.SubElement(res, "format", id=fid, name="FFVideoFormatRateUndefined", width=str(ns["w"]), height=str(ns["h"]), colorSpace="1-13-1")
    a = ET.SubElement(res, "asset", id=aid, name=ns["name"], start="0s", duration="0s", hasVideo="1", format=fid, videoSources="1")
    ET.SubElement(a, "media-rep", kind="original-media", src="file://" + U.quote(ns["path"]))
    assets[aid] = a; byname[ns["name"]] = a; fmts[fid] = res.find(f"format[@id='{fid}']")
    v = ET.Element("video", ref=aid, lane=str(ns["lane"]), name=ns["name"], start="3600s", duration=rs(fr(ns["dur"])))
    pos, sc = transform_for(ns["w"], ns["h"], ns["w_px"], ns["cx"], ns["cy"])
    ET.SubElement(v, "adjust-transform", position=pos, scale=sc)
    attach(v, ns["t"]); log.append(f"added still {ns['name']} {ns['t']}-{ns['t'] + ns['dur']:.3f}")

# 4. pop in-point fix (transient is at 0.73 s; 0.75 starts after it = silent)
pf = cfg.get("pop_fix")
if pf:
    for p, k, t, d in connected():
        if k.tag == "asset-clip" and assets[k.get("ref")].get("name") == pf["asset_name"] and abs(float(T(k.get("start"))) - pf["start"]) > 0.005:
            k.set("start", rs(F(pf["start"]).limit_denominator(1000))); log.append(f"pop at {float(t):.3f}: in-point -> {pf['start']}")

# 5. extra sound effects (copy in-point/length/volume from an existing clip of that asset)
for sx in cfg.get("sfx", []):
    tmpl = next(k for p, k, t, d in connected() if k.tag == "asset-clip" and assets[k.get("ref")].get("name") == sx["asset_name"])
    e = ET.Element("asset-clip", ref=tmpl.get("ref"), lane=str(sx["lane"]), name=tmpl.get("name"),
                   start=tmpl.get("start"), duration=tmpl.get("duration"))
    for a in ("audioRole",):
        if tmpl.get(a): e.set(a, tmpl.get(a))
    ET.SubElement(e, "adjust-volume", amount=sx.get("db", "-16dB"))
    attach(e, sx["t"]); log.append(f"added {sx['asset_name'][:12]} at {sx['t']}")

# 6. close B-roll gaps < 0.3 s (visual connected items, lane > 0, enabled)
vis = sorted([(t, t + d, k) for p, k, t, d in connected()
              if int(k.get("lane")) > 0 and k.tag in ("asset-clip", "video", "clip") and k.get("enabled", "1") == "1"],
             key=lambda r: r[0])
cur = None
for t0, t1, k in vis:
    if cur and cur[1] < t0 and t0 - cur[1] < F(3, 10):
        gap = t0 - cur[1]; e = cur[2]
        e.set("duration", rs(T(e.get("duration")) + gap))
        log.append(f"closed {float(gap)*1000:.0f} ms gap at {float(cur[1]):.3f} ({e.get('name')[:20]} -> {(k.get('name') or '')[:20]})")
        cur = (cur[0], t0, e)
    if cur is None or t1 > cur[1]: cur = (t0, t1, k)

# 7. captions
ST = dict(font="Helvetica Neue", face="Bold", size=42, white="1 1 1 1", yellow="1 0.88 0 1", lane=8,
          max_words=3, max_chars=16, gap_break=0.35, raise_ty="5.706", low_ty="-3.5")
SP = dict(size=56, pos="0 288", hi="0.45 0.85 1 1", max_chars=18)       # quoted real clip: bigger, top third, blue word
spec_win = [(p["off"], p["off"] + p["dur"]) for p in pieces if assets[p["ref"]].get("name") in cfg.get("special_ref_names", [])]
low_win = [(t, t + d) for p, k, t, d in connected() if k.tag == "video" and (k.get("name") or "") in cfg.get("low_graphics", [])]
def kind(t):
    if any(a <= t < b for a, b in spec_win): return "special"
    return "normal"
def is_low(a, b): return any(a < y and x < b for x, y in low_win)
eff = ET.SubElement(res, "effect", id=new_id(), name="Basic Title",
                    uid=".../Titles.localized/Bumper:Opener.localized/Basic Title.localized/Basic Title.moti")
FIX = {"alex": "Alix", "alix": "Alix", "alex's": "Alix's", "alix's": "Alix's", "noll": "knoll", "meechi": "michi",
       "alejandro": "alejandra", "oliver": "all over", "rung": "run"}
raw = json.load(open(cfg["words"]))
toks = []
for w in raw:
    s = w["w"]
    if toks and (s.startswith("-") or s.startswith(".")):
        toks[-1]["w"] += s; toks[-1]["e"] = w["e"]; continue
    toks.append(dict(w=s, s=w["s"], e=w["e"]))
for t in toks:
    t["end_sent"] = t["w"].endswith((".", "?", "!"))
    c = re.sub(r"[.,?!\"]+", "", t["w"].lower()).strip()
    t["c"] = FIX.get(c, c)
cl = [t["c"] for t in toks]; out = []; i = 0
while i < len(toks):
    t = toks[i]
    if cl[i:i + 3] == ["start", "to", "finish"]:
        out.append(dict(t, c="start2finish", e=toks[i + 2]["e"], end_sent=toks[i + 2]["end_sent"])); i += 3; continue
    if cl[i] == "9" and i + 1 < len(cl) and cl[i + 1] in ("am", "a.m", "am."):
        out.append(dict(t, c="9am", e=toks[i + 1]["e"], end_sent=toks[i + 1]["end_sent"])); i += 2; continue
    if cl[i:i + 4] == ["grades", "one", "to", "six"]:
        out += [dict(toks[i + k], c=c) for k, c in enumerate(["grades", "1", "to", "6"])]; i += 4; continue
    if cl[i:i + 2] == ["me", "cheese"]:
        out.append(dict(t, c="michi's", e=toks[i + 1]["e"], end_sent=toks[i + 1]["end_sent"])); i += 2; continue
    if cl[i:i + 3] == ["my", "own", "club"]:
        out += [dict(toks[i], c="my"), dict(toks[i + 1], c="run"), dict(toks[i + 2], c="club")]; i += 3; continue
    out.append(t); i += 1
toks = [t for t in out if t["c"]]
for t in toks: t["k"] = kind(t["s"] + 0.02)
chunks, cur = [], []
for t in toks:
    mc = SP["max_chars"] if t["k"] == "special" else ST["max_chars"]
    if cur and (len(cur) >= ST["max_words"] or len(" ".join(x["c"] for x in cur + [t])) > mc
                or t["s"] - cur[-1]["e"] > ST["gap_break"] or t["k"] != cur[-1]["k"]):
        chunks.append(cur); cur = []
    cur.append(t)
    if t["end_sent"]: chunks.append(cur); cur = []
if cur: chunks.append(cur)
tsn = [0]; ncap = 0
def title(t0, t1, spans, name, k):
    global ncap
    sp = k == "special"; low = (not sp) and is_low(float(fr(t0)), float(fr(t1)))
    e = ET.Element("title", ref=eff.get("id"), lane=str(ST["lane"]), name=name[:40], start="3600s", duration=rs(fr(t1) - fr(t0)))
    ET.SubElement(e, "param", name="Position", key="9999/999166631/999166633/1/100/101", value=SP["pos"] if sp else "0 -288")
    ET.SubElement(e, "param", name="Flatten", key="9999/999166631/999166633/2/351", value="1")
    ET.SubElement(e, "param", name="Alignment", key="9999/999166631/999166633/2/354/999169573/401", value="1 (Center)")
    txt = ET.SubElement(e, "text"); defs = []
    for s, hot in spans:
        tsn[0] += 1; tid = f"cap{tsn[0]}"
        ET.SubElement(txt, "text-style", ref=tid).text = s
        d = ET.Element("text-style-def", id=tid)
        col = (SP["hi"] if sp else ST["yellow"]) if hot else ST["white"]
        ET.SubElement(d, "text-style", font=ST["font"], fontSize=str(SP["size"] if sp else ST["size"]), fontFace=ST["face"],
                      fontColor=col, shadowColor="0 0 0 0.75", shadowOffset="4 315", shadowBlurRadius="8", alignment="center")
        defs.append(d)
    for d in defs: e.append(d)
    if not sp:
        ET.SubElement(e, "adjust-transform", position=f"0 {ST['low_ty'] if low else ST['raise_ty']}")
    attach(e, t0); ncap += 1
starts = [c[0]["s"] for c in chunks] + [float(end_all)]
for ci, ch in enumerate(chunks):
    chunk_end = min(starts[ci + 1], ch[-1]["e"] + 0.5, float(end_all))
    for wi, t in enumerate(ch):
        a = t["s"]; b = ch[wi + 1]["s"] if wi + 1 < len(ch) else chunk_end
        if fr(b) <= fr(a): continue
        title(a, b, [((" " if j else "") + x["c"], j == wi) for j, x in enumerate(ch)], " ".join(x["c"] for x in ch), ch[0]["k"])
log.append(f"captions: {len(chunks)} groups, {ncap} titles; special groups: "
           + " | ".join(" ".join(x["c"] for x in c) for c in chunks if c[0]["k"] == "special"))

# 8. browser clips for used media that has none in the event
used = set()
for el in project.iter():
    if el.get("ref") in assets: used.add(el.get("ref"))
have = set(cfg.get("browser_names", []))
pos = list(event).index(project); added = []
for rid in sorted(used, key=lambda r: assets[r].get("name")):
    a = assets[rid]; nm = a.get("name")
    if nm in have: continue
    if T(a.get("duration")) == 0:
        c = ET.Element("clip", name=nm, start="3600s", duration="10s"); ET.SubElement(c, "video", ref=rid, duration="0s")
    else:
        c = ET.Element("asset-clip", ref=rid, name=nm, start=a.get("start") or "0s", duration=a.get("duration"), tcFormat="NDF")
        if a.get("format"): c.set("format", a.get("format"))
        c.set("audioRole", "dialogue" if a.get("hasVideo") == "1" else "effects" if re.search(r"Pop|Ding", nm) else "music")
    event.insert(pos, c); pos += 1; added.append(nm)
log.append(f"browser clips added ({len(added)}): {', '.join(added)}")

project.set("modDate", project.get("modDate"))
ET.indent(tree, "  ")
with open(cfg["out"], "wb") as fh:
    fh.write(b'<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE fcpxml>\n\n')
    tree.write(fh, encoding="utf-8", xml_declaration=False)
print("\n".join(log))
