#!/usr/bin/env python3
"""Nov 16 Day 17 Run - regular vlog cut + one-word captions (Final Cut, Rec. 709, 1080x1920 @ 30).

  python build_day17.py plan   WORDS_RAW.json CUT.wav          -> pieces.json + rendered cut audio
  python build_day17.py build  WORDS_CUT.json OUT.fcpxml       -> FCPXML (captions timed from the cut's own audio)

Take choice: when a line is said more than once, the LAST take is used (Babi, 2026-11-16).
"""
import json, subprocess, sys, os, re
from fractions import Fraction as F
from urllib.parse import quote

RUN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FPS = 30
# (clip, first word ~s, last word ~s, note)   times are rough whisper times; edges are refined below
SEGS = [
    ("IMG_0567", 3.12, 3.64, "long couple days"),
    ("IMG_0568", 0.00, 2.68, "9:10, just got back from work"),
    ("IMG_0571", 0.00, 5.58, "ended work at five, stayed later"),
    ("IMG_0572", 0.74, 1.60, "but yeah absolutely brutal (day line dropped: 0576 is the last take)"),
    ("IMG_0576", 0.00, 3.42, "17th day running consecutively (LAST take of the day line)"),
    ("IMG_0576", 6.32, 7.36, "kind of hard to get out tonight"),
    ("IMG_0576", 11.40, 12.06, "but honestly it's kind of nice (2nd/last take)"),
    ("IMG_0576", 14.26, 22.92, "I deserve a break to run and be outside"),
    ("IMG_0576", 24.12, 24.90, "Whoo! Perspective!"),
    ("IMG_0577", 4.36, 17.08, "the random runner: asks, gets a no"),
    ("IMG_0578", 0.44, 1.50, "you know what, that's ok"),
    ("IMG_0580", 0.00, 8.52, "bro did not want to be part of that"),
    ("IMG_0581", 0.94, 2.10, "finish this run up"),
    ("IMG_0585", 1.78, 2.86, "okay we got it done (LAST take; 0584 dropped)"),
    ("IMG_0585", 4.40, 10.18, "fellow run every dayers, is this sustainable"),
    ("IMG_0585", 14.70, 20.16, "mental health / Casey Neistat"),
    ("IMG_0585", 20.60, 23.34, "give me tips"),
    ("IMG_0585", 23.84, 26.66, "running a 5k every day, but I think I"),
    ("IMG_0585", 27.74, 28.64, "should maybe structure it better (0.9 s pause cut)"),
    ("IMG_0585", 29.52, 29.92, "let me know (its 'good night' dropped: 0586 is the last outro)"),
    ("IMG_0586", 2.72, 5.20, "keep your perspective intact (LAST take: first 'keep your...' at 2.1 s dropped)"),
    ("IMG_0586", 6.74, 9.26, "long day but this was kind of nice"),
    ("IMG_0586", 10.16, 11.20, "I love you, have a good night"),
    ("IMG_0586", 12.20, 14.52, "happy Monday night, happy Tuesday tomorrow - END on last word"),
]
PRE, POST = 0.07, 0.14
# exact source edges (from 50 ms RMS) where whisper's word times were off
EXACT = {("IMG_0586", 2.72): (4.27, 6.33), ("IMG_0586", 6.74): (6.60, None), ("IMG_0585", 1.78): (1.15, None)}
CAP = dict(font="Helvetica Neue", face="Bold", size=40, y=-165)   # storytelling caption look, ONE word, every title same size
FIX = {"bobby": "babi", "ok": "okay"}

def q(x): return F(round(F(x) * FPS), FPS)
def r(x):
    x = F(x); return f"{x.numerator}/{x.denominator}s" if x.denominator != 1 else f"{x.numerator}s"

def probe(clip):
    p = f"{RUN}/{clip}.MOV"
    j = json.loads(subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
        "stream=r_frame_rate,duration", "-of", "json", p]))["streams"][0]
    n, d = map(int, j["r_frame_rate"].split("/"))
    return F(n, d), F(j["duration"]).limit_denominator(100000)

def pieces(words):
    out = []; off = F(0)
    for clip, a, b, note in SEGS:
        ws = words[clip]
        i0 = min(range(len(ws)), key=lambda i: abs(ws[i]["s"] - a))
        i1 = min(range(len(ws)), key=lambda i: abs(ws[i]["s"] - b))
        st = max(ws[i0]["s"] - PRE, ws[i0 - 1]["e"] if i0 else 0, 0)
        st = min(st, ws[i0]["s"])
        en = ws[i1]["e"] + POST
        if i1 + 1 < len(ws): en = min(en, max(ws[i1 + 1]["s"] - 0.03, ws[i1]["e"]))
        ex = EXACT.get((clip, a))
        if ex: st, en = (ex[0] if ex[0] is not None else st), (ex[1] if ex[1] is not None else en)
        fps, dur = probe(clip)
        st = F(round(F(st) * fps), fps)                       # source frame grid
        en = min(F(en), dur)
        du = q(en - st)
        if st + du > dur: du -= F(1, FPS)
        out.append(dict(clip=clip, st=st, du=du, off=off, note=note, text=" ".join(w["w"] for w in ws[i0:i1 + 1])))
        off += du
    return out

def main():
    mode = sys.argv[1]
    if mode == "plan":
        P = pieces(json.load(open(sys.argv[2])))
        ins, fl = [], []
        for k, p in enumerate(P):
            ins += ["-i", f"{RUN}/{p['clip']}.MOV"]
            fl.append(f"[{k}:a:0]atrim={float(p['st'])}:{float(p['st'] + p['du'])},asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=mono[a{k}]")
        fl.append("".join(f"[a{k}]" for k in range(len(P))) + f"concat=n={len(P)}:v=0:a=1[o]")
        subprocess.check_call(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", ";".join(fl), "-map", "[o]", sys.argv[3]])
        for p in P: print(f"{float(p['off']):6.2f} {p['clip']} {float(p['st']):6.2f}+{float(p['du']):5.2f}  {p['text']}")
        print("TOTAL", float(P[-1]["off"] + P[-1]["du"]))
        json.dump([dict(p, st=str(p["st"]), du=str(p["du"]), off=str(p["off"])) for p in P], open(os.path.splitext(sys.argv[3])[0] + "_pieces.json", "w"), indent=1)
        return
    words = json.load(open(sys.argv[2])); OUT = sys.argv[3]
    P = json.load(open(sys.argv[4]))
    for p in P:
        for k in ("st", "du", "off"): p[k] = F(p[k])
    TOTAL = P[-1]["off"] + P[-1]["du"]
    res = ['<format id="r1" name="FFVideoFormat1080x1920p30" frameDuration="100/3000s" width="1080" height="1920" colorSpace="1-1-1 (Rec. 709)"/>']
    fmts = {}
    assets = []
    for clip in dict.fromkeys(p["clip"] for p in P):
        fps, dur = probe(clip)
        if fps not in fmts:
            fmts[fps] = f"r{len(fmts) + 2}"
            res.append(f'<format id="{fmts[fps]}" name="FFVideoFormatRateUndefined" frameDuration="{fps.denominator}/{fps.numerator}s" width="1080" height="1920" colorSpace="9-18-9 (Rec. 2020 HLG)"/>')
        assets.append(f'<asset id="a_{clip}" name="{clip}" start="0s" duration="{r(dur)}" hasVideo="1" format="{fmts[fps]}" hasAudio="1" videoSources="1" audioSources="1" audioChannels="2" audioRate="48000">'
                      f'<media-rep kind="original-media" src="file://{quote(RUN + "/" + clip + ".MOV")}"/></asset>')
    res += assets
    res.append('<effect id="eT" name="Basic Title" uid=".../Titles.localized/Bumper:Opener.localized/Basic Title.localized/Basic Title.moti"/>')

    # captions: one word each, from the cut's own audio
    toks = []
    for w in words:
        c = re.sub(r"[^\w':]+", "", w["w"].lower()).strip("'")
        if w["w"].startswith((".", "-", ":")) and toks:
            toks[-1]["c"] += re.sub(r"[^\w:]", "", w["w"].lower()) if not w["w"].startswith(".") else ":" + c; toks[-1]["e"] = w["e"]; continue
        c = FIX.get(c, c)
        if c: toks.append(dict(c=c, s=w["s"], e=w["e"]))
    # "9, 10 a.m." -> one caption "9:10" (am/pm left out: whisper hears a.m. on a 9 pm clip)
    for i in range(len(toks) - 1):
        if toks[i]["c"] in ("nine", "9") and toks[i + 1]["c"] == "10":
            j = i + 2
            while j < len(toks) and toks[j]["c"] in ("a", "m", "am", "a:m", "pm", "p", "p:m"): j += 1
            toks[i] = dict(c="9:10", s=toks[i]["s"], e=toks[j - 1]["e"]); del toks[i + 1:j]; break
    for i, t in enumerate(toks):
        # whisper stretches a short word back over the pause before it: pull its start to the word itself
        if t["e"] - t["s"] > 0.5 and len(t["c"]) <= 5: t["s"] = round(t["e"] - 0.3, 2)
        # raw clip (and the uncut onset) says "today was a long day"; the cut pass heard "it was"
        if t["c"] == "it" and [x["c"] for x in toks[i + 1:i + 4]] == ["was", "a", "long"]: t["c"] = "today"
    caps = {k: [] for k in range(len(P))}
    n = 0
    for i, t in enumerate(toks):
        a = q(t["s"]); nxt = toks[i + 1]["s"] if i + 1 < len(toks) else float(TOTAL)
        b = q(min(nxt, t["e"] + 0.3, float(TOTAL)))
        if b <= a: b = a + F(1, FPS)
        k = next((k for k, p in enumerate(P) if p["off"] <= a < p["off"] + p["du"]), len(P) - 1)
        p = P[k]; n += 1
        caps[k].append(
            f'<title ref="eT" lane="1" offset="{r(p["st"] + a - p["off"])}" name="{t["c"]}" start="3600s" duration="{r(b - a)}">'
            f'<param name="Position" key="9999/999166631/999166633/1/100/101" value="0 {CAP["y"]}"/>'
            f'<param name="Flatten" key="9999/999166631/999166633/2/351" value="1"/>'
            f'<param name="Alignment" key="9999/999166631/999166633/2/354/999169573/401" value="1 (Center)"/>'
            f'<text><text-style ref="ts{n}">{t["c"]}</text-style></text>'
            f'<text-style-def id="ts{n}"><text-style font="{CAP["font"]}" fontSize="{CAP["size"]}" fontFace="{CAP["face"]}" fontColor="1 1 1 1" '
            f'shadowColor="0 0 0 0.75" shadowOffset="4 315" shadowBlurRadius="8" alignment="center"/></text-style-def></title>')
    spine = []
    for k, p in enumerate(P):
        note = p["note"].replace("&", "and").replace('"', "'")
        spine.append(f'<asset-clip ref="a_{p["clip"]}" name="{p["clip"]}" offset="{r(p["off"])}" start="{r(p["st"])}" duration="{r(p["du"])}" tcFormat="NDF" audioRole="dialogue">'
                     f'<note>{note}</note>' + "".join(caps[k]) + '</asset-clip>')
    X = ('<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE fcpxml>\n<fcpxml version="1.11">\n<resources>\n' + "\n".join(res) + '\n</resources>\n'
         '<library><event name="Nov 16 Day 17 Run"><project name="Nov 16 Day 17 Run">'
         f'<sequence format="r1" duration="{r(TOTAL)}" tcStart="0s" tcFormat="NDF" audioLayout="stereo" audioRate="48k"><spine>\n'
         + "\n".join(spine) + '\n</spine></sequence></project></event></library>\n</fcpxml>\n')
    open(OUT, "w").write(X)
    print(f"{OUT}: {len(P)} pieces, {float(TOTAL):.2f}s, {n} captions")
    print(" ".join(t["c"] for t in toks))

main()
