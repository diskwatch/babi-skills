#!/usr/bin/env python3
"""Build a Babi "knowledge reel" pass on top of an exported copy of the user's edit.

Adds, as connected clips on the user's own spine (nothing in the spine is cut):
  * internet photos on the lower chest (lane 1), each landing with a pop (lane -1)
  * a static zoom (adjust-transform) on chosen spine clips, e.g. onto a whiteboard
  * word-by-word captions: 2-3 word chunks, lowercase, the spoken word in yellow (lane 2)
  * big yellow "figure" titles for dollar amounts, each with a Ding (lane 3 / -2)
  * a two-line topic header near the top that changes per section (lane 4)

Usage:
  python3 build_knowledge_reel.py plan.json
plan.json keys (times are TIMELINE seconds, from words.json made on the cut's own audio):
  source_xml, out_xml, project_name, words, photo_dir,
  photos:  [{"file":..., "t0":..., "t1":...}]
  zoom:    [{"clips":[idx,...], "scale":1.45, "cx":700, "cy":1120}]   (cx/cy = source px to centre)
  figures: [{"text":"$46,000", "t0":..., "t1":...}]
  headers: [{"text":"line one\\nline two", "t0":..., "t1":...}]
  style:   optional overrides (see STYLE below)
"""
import json, sys, re, os, urllib.parse, copy
from fractions import Fraction as F
import xml.etree.ElementTree as ET
from PIL import Image

STYLE = dict(
    font="Helvetica Neue", face="Bold", size=64, white="1 1 1 1", yellow="1 0.88 0 1",
    cap_y=-323,            # Basic Title Position units (~1.67 px): -323 -> centre y ~1500 px
    fig_size=124, fig_y=-323,
    head_size=40, head_y=261,   # +261 -> centre y ~523 px (Babi lowered the header from 345 px, 2026-11-16)
    photo_x=0.0,           # adjust-transform % of frame height, + is right
    head_x=0,              # Basic Title Position units (~1.67 px), + is right
    photo_y=-12.0,         # adjust-transform % of frame height: -12 -> centre y ~1190 px
    photo_box=(600, 440),  # max photo size in px
    pop_db=-12, ding_db=-16,
    max_words=3, max_chars=16, gap_break=0.35,
)
FPS = 60
POP = dict(uid="AFAE54967434581F31B1054D9B88BECC", name="Pop",
           src="/Volumes/4TBSSD_4/Babi NR Content/Sound FX/click and keyboard/Censor sound __ Funny sound __ Mouse click sound __ Pop sound __ Slap sound __ Short sound effect.mp3",
           dur=F(231271, 48000), start=F(713654, 720000), len=F(112036, 720000))
DING = dict(uid="4E71FBAE44E48B72F7129128F1654579", name="Ding",
            src="/Volumes/4TBSSD_4/Babi NR Content/Songs/SOUND FX/Ding - Sound Effect (HD) - Gaming Sound FX (youtube) (1).mp3",
            dur=None, start=F(21, 100), len=F(85, 100))
BASIC_TITLE = ".../Titles.localized/Bumper:Opener.localized/Basic Title.localized/Basic Title.moti"


def T(s):
    s = (s or "0s").rstrip("s")
    return F(s) if "/" not in s else F(int(s.split("/")[0]), int(s.split("/")[1]))


def fr(x):  # snap seconds to a 60 fps frame, as a Fraction
    return F(round(F(x) * FPS), FPS)


def rs(x):  # rational string
    x = F(x)
    return f"{x.numerator}/{x.denominator}s" if x.denominator != 1 else f"{x.numerator}s"


def url(p):
    return "file://" + urllib.parse.quote(p)


def main(plan_path):
    plan = json.load(open(plan_path))
    st = {**STYLE, **plan.get("style", {})}
    tree = ET.parse(plan["source_xml"])
    root = tree.getroot()
    res = root.find("resources")
    ids = [int(re.sub(r"\D", "", e.get("id")) or 0) for e in res if e.get("id")]
    nid = [max(ids) + 1 if ids else 1]

    def new_id():
        nid[0] += 1
        return f"r{nid[0]}"

    project = root.find(".//project")
    project.set("name", plan["project_name"])
    project.attrib.pop("uid", None)
    project.attrib.pop("modDate", None)
    spine = project.find(".//spine")
    clips = [c for c in spine if c.tag in ("asset-clip", "clip", "video")]
    info = [dict(el=c, off=T(c.get("offset")), start=T(c.get("start")), dur=T(c.get("duration"))) for c in clips]

    def parent_at(t):
        for c in info:
            if c["off"] <= t < c["off"] + c["dur"]:
                return c
        return info[-1]

    def attach(el, t):
        """Anchor element el at timeline time t to the spine clip under t."""
        p = parent_at(t)
        el.set("offset", rs(p["start"] + (fr(t) - p["off"])))
        p["el"].append(el)

    # --- resources
    eff = ET.SubElement(res, "effect", id=new_id(), name="Basic Title", uid=BASIC_TITLE)
    title_ref = eff.get("id")
    audfmt = ET.SubElement(res, "format", id=new_id(), name="FFVideoFormatRateUndefined")

    def sfx_asset(d):
        a = ET.SubElement(res, "asset", id=new_id(), name=d["name"], uid=d["uid"], start="0s",
                          hasAudio="1", audioSources="1", audioChannels="2", audioRate="48000")
        if d["dur"]:
            a.set("duration", rs(d["dur"]))
        else:
            a.set("duration", "5s")
        ET.SubElement(a, "media-rep", kind="original-media", src=url(d["src"]))
        return a.get("id")

    pop_ref, ding_ref = sfx_asset(POP), sfx_asset(DING)

    def sfx(ref, d, t, db, lane):
        e = ET.Element("asset-clip", ref=ref, lane=str(lane), name=d["name"], start=rs(d["start"]),
                       duration=rs(d["len"]), format=audfmt.get("id"), audioRole="effects")
        ET.SubElement(e, "adjust-volume", amount=f"{db}dB")
        attach(e, t)

    # --- zoom on spine clips
    for z in plan.get("zoom", []):
        s = z["scale"]
        x = -s * (z["cx"] - 540) / 19.2
        y = s * (z["cy"] - 960) / 19.2
        for i in z["clips"]:
            c = clips[i]
            for old in c.findall("adjust-transform"):
                c.remove(old)
            tr = ET.Element("adjust-transform", position=f"{x:.4f} {y:.4f}", scale=f"{s} {s}")
            kids = list(c)
            pos = 0
            for k, ch in enumerate(kids):
                if ch.tag in ("note", "conform-rate", "timeMap", "adjust-crop", "adjust-corners", "adjust-conform"):
                    pos = k + 1
            c.insert(pos, tr)

    # --- photos (one asset per file, reused if a photo appears twice)
    photo_assets = {}
    for ph in plan.get("photos", []):
        path = os.path.join(plan["photo_dir"], ph["file"])
        w, h = Image.open(path).size
        if path not in photo_assets:
            fmt = ET.SubElement(res, "format", id=new_id(), name="FFVideoFormatRateUndefined", width=str(w), height=str(h))
            a = ET.SubElement(res, "asset", id=new_id(), name=os.path.splitext(ph["file"])[0], start="0s", duration="0s",
                              hasVideo="1", format=fmt.get("id"), videoSources="1")
            ET.SubElement(a, "media-rep", kind="original-media", src=url(path))
            photo_assets[path] = a
        a = photo_assets[path]
        fit = min(1080 / w, 1920 / h)
        bw, bh = st["photo_box"]
        sc = min(bw / (w * fit), bh / (h * fit))
        t0, t1 = fr(ph["t0"]), fr(ph["t1"])
        v = ET.Element("video", ref=a.get("id"), lane="1", name=a.get("name"), start="3600s", duration=rs(t1 - t0))
        ET.SubElement(v, "adjust-transform", position=f"{st['photo_x']} {ph.get('y', st['photo_y'])}", scale=f"{sc:.4f} {sc:.4f}")
        attach(v, t0)
        sfx(pop_ref, POP, t0, st["pop_db"], -1)

    # --- titles
    tsn = [0]

    def title(lane, t0, t1, spans, size, y, name, x=0):
        e = ET.Element("title", ref=title_ref, lane=str(lane), name=name[:40], start="3600s", duration=rs(fr(t1) - fr(t0)))
        ET.SubElement(e, "param", name="Position", key="9999/999166631/999166633/1/100/101", value=f"{x} {y}")
        ET.SubElement(e, "param", name="Flatten", key="9999/999166631/999166633/2/351", value="1")
        ET.SubElement(e, "param", name="Alignment", key="9999/999166631/999166633/2/354/999169573/401", value="1 (Center)")
        txt = ET.SubElement(e, "text")
        defs = []
        for s, col in spans:
            tsn[0] += 1
            tid = f"kts{tsn[0]}"
            ET.SubElement(txt, "text-style", ref=tid).text = s
            d = ET.Element("text-style-def", id=tid)
            ET.SubElement(d, "text-style", font=st["font"], fontSize=str(size), fontFace=st["face"], fontColor=col,
                          shadowColor="0 0 0 0.75", shadowOffset="4 315", shadowBlurRadius="8", alignment="center")
            defs.append(d)
        for d in defs:
            e.append(d)
        attach(e, t0)

    # captions from words
    raw = json.load(open(plan["words"]))
    toks = []
    for w in raw:
        s = w["w"]
        if toks and (s[:1] in ",%" or s.startswith("-")) and not toks[-1]["end_sent"]:
            toks[-1]["w"] += s
            toks[-1]["e"] = w["e"]
            toks[-1]["end_sent"] = s.endswith((".", "?", "!"))
            continue
        toks.append(dict(w=s, s=w["s"], e=w["e"], end_sent=s.endswith((".", "?", "!"))))
    for t in toks:
        t["c"] = re.sub(r"[.,?!]+$", "", t["w"].lower()).replace('"', "")
    figs = plan.get("figures", [])
    infig = lambda t: any(f["t0"] - 0.02 <= t < f["t1"] for f in figs)
    toks = [t for t in toks if not infig(t["s"])]
    chunks, cur = [], []
    for i, t in enumerate(toks):
        if cur and (len(cur) >= st["max_words"] or len(" ".join(x["c"] for x in cur + [t])) > st["max_chars"]
                    or t["s"] - cur[-1]["e"] > st["gap_break"]
                    or any(cur[-1]["e"] <= f["t0"] <= t["s"] for f in figs)):
            chunks.append(cur)
            cur = []
        cur.append(t)
        if t["end_sent"]:
            chunks.append(cur)
            cur = []
    if cur:
        chunks.append(cur)
    end_all = float(sum((c["dur"] for c in info), F(0)))
    starts = [c[0]["s"] for c in chunks] + [end_all]
    for ci, ch in enumerate(chunks):
        nxt = starts[ci + 1]
        for f in figs:  # never run into a figure
            if ch[-1]["e"] <= f["t0"] < nxt:
                nxt = f["t0"]
        chunk_end = min(nxt, ch[-1]["e"] + 0.5)
        for wi, t in enumerate(ch):
            a = t["s"]
            b = ch[wi + 1]["s"] if wi + 1 < len(ch) else chunk_end
            if fr(b) <= fr(a):
                continue
            spans = []
            for k, x in enumerate(ch):
                spans.append(((" " if k else "") + x["c"], st["yellow"] if k == wi else st["white"]))
            title(2, a, b, spans, st["size"], st["cap_y"], " ".join(x["c"] for x in ch))

    # --- music: one song on lane -3 under the whole reel, flat level, trimmed to the video
    mu = plan.get("music")
    if mu:
        a = ET.SubElement(res, "asset", id=new_id(), name=os.path.splitext(os.path.basename(mu["file"]))[0], start="0s",
                          duration=rs(fr(mu["length"])), hasAudio="1", audioSources="1", audioChannels="2", audioRate="48000")
        ET.SubElement(a, "media-rep", kind="original-media", src=url(mu["file"]))
        e = ET.Element("asset-clip", ref=a.get("id"), lane="-3", name=a.get("name"), start=rs(fr(mu["start"])),
                       duration=rs(fr(end_all)), format=audfmt.get("id"), audioRole="music")
        ET.SubElement(e, "adjust-volume", amount=f"{mu.get('db', -15)}dB")
        attach(e, 0)

    for f in figs:
        title(3, f["t0"], f["t1"], [(f["text"], st["yellow"])], st["fig_size"], st["fig_y"], f["text"])
        sfx(ding_ref, DING, f["t0"], st["ding_db"], -2)
    for h in plan.get("headers", []):
        title(4, h["t0"], h["t1"], [(h["text"], st["white"])], st["head_size"], h.get("y", st["head_y"]), h["text"].split("\n")[0], h.get("x", st["head_x"]))

    # Rec. 709 sequence
    seqfmt = res.find(f"format[@id='{project.find('sequence').get('format')}']")
    seqfmt.set("colorSpace", "1-1-1 (Rec. 709)")
    ET.indent(tree, "  ")
    with open(plan["out_xml"], "wb") as fh:
        fh.write(b'<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE fcpxml>\n\n')
        tree.write(fh, encoding="utf-8", xml_declaration=False)
    print("wrote", plan["out_xml"], "captions:", len(chunks), "photos:", len(plan.get("photos", [])))


if __name__ == "__main__":
    main(sys.argv[1])
