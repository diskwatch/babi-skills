#!/usr/bin/env python3
"""Build the two Nov 16 talking-head storytelling projects (babi-storytelling rules).

  python3 -I build_talks.py CUT_DIR BEATS_DIR SHEET_DIR

CUT_DIR holds cut_0562.json / cut_0564.json (talking-head pieces in source seconds, from the
RMS-refined, pause-split plan). BEATS_DIR holds <song>_beats.json (librosa beat_track).
Writes one FCPXML per project into each project's XML folder, plus a contact sheet of every
B-roll in-point into SHEET_DIR for checking.
"""
import json, os, subprocess, sys, urllib.parse
from fractions import Fraction as F
from xml.sax.saxutils import escape as esc

CUT_DIR, BEATS_DIR, SHEET_DIR = sys.argv[1:4]
ROOT = "/Volumes/Babi's 2TB/Babiontherun/Fall26/Media/Vlogs"
LIB = "/Volumes/Babi's 2TB/Babiontherun/Fall26/Fall26 20261018_1446_EDT.fcpbundle/"
FD = F(1, 60)                        # project frame (talking heads are 60.000 fps)
FW, FH = 1080, 1920
GR = "Nov 15 Golden Run Cafe Panchita"
AP = "Nov 15 Appleby College Give Oakville w Michi"
AX = "Nov 11 Alix Lunch"
N8 = "Nov 8 Golden Run Met Alex/Babi clips"

def url(p): return "file://" + urllib.parse.quote(p)
def ft(x):
    x = F(x)
    return "0s" if x == 0 else f"{x.numerator}/{x.denominator}s"
def snap(sec, fd=FD): return round(F(sec).limit_denominator(1000000) / fd) * fd

_probe = {}
def probe(path):
    if path not in _probe:
        o = json.loads(subprocess.check_output(["ffprobe", "-v", "quiet", "-print_format", "json",
                                                "-show_streams", "-show_format", path]))
        v = [s for s in o["streams"] if s["codec_type"] == "video"]
        a = [s for s in o["streams"] if s["codec_type"] == "audio"]
        info = {"dur": F(o["format"]["duration"]).limit_denominator(1000000)}
        if v:
            v = v[0]; num, den = map(int, v["r_frame_rate"].split("/"))
            rot = any(abs(int(sd.get("rotation", 0))) == 90 for sd in v.get("side_data_list", []))
            w, h = (v["height"], v["width"]) if rot else (v["width"], v["height"])
            info.update(fd=F(den, num), w=w, h=h, hlg=v.get("color_transfer") == "arib-std-b67")
        if a:
            info.update(rate=int(a[0]["sample_rate"]), ch=int(a[0].get("channels", 2)))
        _probe[path] = info
    return _probe[path]

class Build:
    def __init__(self, project, event):
        self.project, self.event = project, event
        self.formats, self.assets, self.fmt_ids, self.asset_ids = [], [], {}, {}
    def fmt(self, key, xml):
        if key not in self.fmt_ids:
            fid = f"f{len(self.fmt_ids) + 1}"; self.fmt_ids[key] = fid
            self.formats.append(xml.replace("{ID}", fid))
        return self.fmt_ids[key]
    def asset(self, path):
        if path in self.asset_ids: return self.asset_ids[path]
        name = os.path.splitext(os.path.basename(path))[0]
        aid = f"a{len(self.asset_ids) + 1}"; self.asset_ids[path] = aid
        ext = os.path.splitext(path)[1].lower()
        if ext in (".png", ".jpg", ".jpeg"):
            from PIL import Image
            w, h = Image.open(path).size
            fid = self.fmt(("still", w, h), f'<format id="{{ID}}" name="FFVideoFormatRateUndefined" width="{w}" height="{h}"/>')
            self.assets.append(f'<asset id="{aid}" name="{esc(name)}" start="0s" duration="0s" hasVideo="1" format="{fid}" '
                               f'videoSources="1"><media-rep kind="original-media" src="{esc(url(path))}"/></asset>')
            return aid
        p = probe(path)
        if "fd" in p:
            cs = "9-18-9 (Rec. 2020 HLG)" if p["hlg"] else "1-1-1 (Rec. 709)"
            fid = self.fmt((p["fd"], p["w"], p["h"], cs),
                           f'<format id="{{ID}}" frameDuration="{ft(p["fd"])}" width="{p["w"]}" height="{p["h"]}" colorSpace="{cs}"/>')
            d = (p["dur"] / p["fd"]).__floor__() * p["fd"]
            self.assets.append(f'<asset id="{aid}" name="{esc(name)}" start="0s" duration="{ft(d)}" hasVideo="1" hasAudio="1" '
                               f'format="{fid}" audioSources="1" audioChannels="{p.get("ch", 2)}" audioRate="{p.get("rate", 48000)}">'
                               f'<media-rep kind="original-media" src="{esc(url(path))}"/></asset>')
        else:
            d = F(int(p["dur"] * p["rate"]), p["rate"])
            self.assets.append(f'<asset id="{aid}" name="{esc(name)}" start="0s" duration="{ft(d)}" hasAudio="1" '
                               f'audioSources="1" audioChannels="{p["ch"]}" audioRate="{p["rate"]}">'
                               f'<media-rep kind="original-media" src="{esc(url(path))}"/></asset>')
        return aid

def build(cfg):
    b = Build(cfg["project"], cfg["event"])
    th_path = cfg["talking_head"]; th = b.asset(th_path); thfd = probe(th_path)["fd"]
    lines = json.load(open(cfg["cut"]))
    # --- spine
    spine, off, line_tl = [], F(0), {}
    for L in lines:
        k = L["label"][:3]; t0 = off
        for i, (s, e) in enumerate(L["pieces"]):
            st = snap(s, thfd); du = snap(F(e).limit_denominator(100000) - st)
            spine.append(dict(start=st, off=off, dur=du, src=(s, e), kids=[], note=L["label"] if i == 0 else ""))
            off += du
        line_tl[k] = (t0, off)
    total = off
    def tl(src_t):
        """source time on the talking head -> timeline time"""
        for p in spine:
            if p["start"] <= F(src_t).limit_denominator(100000) < p["start"] + p["dur"]:
                return p["off"] + F(src_t).limit_denominator(100000) - p["start"]
        best = min(spine, key=lambda p: abs(p["start"] - F(src_t).limit_denominator(100000)))
        return best["off"]
    def attach(at, xml):
        at = snap(at)
        p = next(p for p in spine if p["off"] <= at < p["off"] + p["dur"]) if at < total else spine[-1]
        p["kids"].append(xml.replace("{OFF}", ft(p["start"] + at - p["off"])))
    # --- beat grid in timeline time (FCP Option-B grid ~= librosa - 0.04 s)
    bj = json.load(open(cfg["beats"]))
    beats = [F(x - 0.04 - cfg["song_in"]).limit_denominator(100000) for x in bj["beats"]]
    beats = [x for x in beats if 0 < x < total]
    report, sheet = [], []
    # --- B-roll bursts: start on the spoken word, cut on beats, one clip jump-cut
    for burst in cfg["bursts"]:
        k, word_src, rel, ins = burst["line"], burst["word"], burst["clip"], burst["ins"]
        path = f"{ROOT}/{rel}"; aid = b.asset(path); p = probe(path); bfd = p["fd"]
        t0 = snap(tl(word_src)); t_end = snap(burst.get("end_tl", line_tl[k][1]) if "end_src" not in burst else tl(burst["end_src"]))
        cuts = [t0]
        while len(cuts) < len(ins) + 1:
            t = cuts[-1]
            cand = [x for x in beats if t + F(55, 100) <= x <= t + F(125, 100)]
            nxt = snap(cand[0]) if cand else snap(t + F(9, 10))
            if nxt >= t_end - F(35, 100):
                cuts.append(t_end); break
            cuts.append(nxt)
        lane = burst.get("lane", 1)
        for i, (a, z) in enumerate(zip(cuts, cuts[1:])):
            src_in = snap(ins[i], bfd); dur = snap(z - a)
            if src_in + dur > p["dur"]: src_in = snap(p["dur"] - dur - F(1, 10), bfd)
            en = '' if burst.get("enabled", True) else ' enabled="0"'
            attach(a, f'<asset-clip ref="{aid}" lane="{lane}" offset="{{OFF}}" name="{esc(os.path.basename(rel)[:-4])}" '
                      f'start="{ft(src_in)}" duration="{ft(dur)}" tcFormat="NDF"{en} audioRole="dialogue">'
                      f'<note>{esc(burst["note"])}</note><adjust-volume amount="-96dB"/></asset-clip>')
            sheet.append((path, float(src_in), f'{float(a):.2f} {os.path.basename(rel)[4:8]}@{float(src_in):.1f}'))
        report.append(f'{float(t0):7.2f}-{float(cuts[-1]):6.2f}  {len(cuts)-1} x {os.path.basename(rel)}'
                      f'{"" if burst.get("enabled", True) else " (disabled alt)"}  {burst["note"]}')
    # --- graphic pops (stills) with Ding on the first, pop on the rest
    for g in cfg.get("graphics", []):
        from PIL import Image
        aid = b.asset(g["path"]); w, h = Image.open(g["path"]).size
        fit = min(FW / w, FH / h); sc = round(g["width_px"] / (w * fit), 4)
        x = round((g["cx"] - FW / 2) / FH * 100, 3); y = round(-(g["cy"] - FH / 2) / FH * 100, 3)
        at = snap(tl(g["word"])); out = snap(line_tl[g["out_line"]][1])
        attach(at, f'<video ref="{aid}" lane="{g["lane"]}" offset="{{OFF}}" name="{esc(os.path.basename(g["path"])[:-4])}" '
                   f'start="3600s" duration="{ft(out - at)}"><adjust-transform position="{x} {y}" scale="{sc} {sc}"/></video>')
        sfx = cfg["ding"] if g["sfx"] == "ding" else cfg["pop"]
        said = b.asset(sfx["path"])
        attach(at - F(sfx["lead"]).limit_denominator(1000),
               f'<asset-clip ref="{said}" lane="-1" offset="{{OFF}}" name="{esc(os.path.basename(sfx["path"])[:-4])}" '
               f'start="{ft(F(sfx["in"]).limit_denominator(1000))}" duration="{ft(F(sfx["len"]).limit_denominator(1000))}" '
               f'audioRole="effects"><adjust-volume amount="{sfx["vol"]}"/></asset-clip>')
        report.append(f'{float(at):7.2f}-{float(out):6.2f}  graphic {os.path.basename(g["path"])}  + {g["sfx"]}')
    # --- music: one lane, flat level, trimmed to the cut
    mid = b.asset(cfg["song"])
    attach(0, f'<asset-clip ref="{mid}" lane="-2" offset="{{OFF}}" name="{esc(os.path.basename(cfg["song"])[:-4])}" '
              f'start="{ft(F(cfg["song_in"]).limit_denominator(1000))}" duration="{ft(total)}" audioRole="music">'
              f'<adjust-volume amount="{cfg["song_db"]}"/></asset-clip>')
    # --- XML
    clips = []
    for p in spine:
        note = f'<note>{esc(p["note"])}</note>' if p["note"] else ""
        clips.append(f'<asset-clip ref="{th}" offset="{ft(p["off"])}" name="{os.path.basename(th_path)[:-4]}" start="{ft(p["start"])}" '
                     f'duration="{ft(p["dur"])}" tcFormat="NDF" audioRole="dialogue">{note}{"".join(p["kids"])}</asset-clip>')
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE fcpxml>\n<fcpxml version="1.11">\n<resources>\n'
           '<format id="r1" name="FFVideoFormat1080x1920p60" frameDuration="1/60s" width="1080" height="1920" colorSpace="1-1-1 (Rec. 709)"/>\n'
           + "\n".join(b.formats) + "\n" + "\n".join(b.assets) + "\n</resources>\n"
           f'<library location="{esc(url(LIB))}" colorProcessing="wide-hdr">\n<event name="{esc(cfg["event"])}">\n'
           f'<project name="{esc(cfg["project"])}"><sequence format="r1" duration="{ft(total)}" tcStart="0s" tcFormat="NDF" '
           f'audioLayout="stereo" audioRate="48k"><spine>\n' + "\n".join(clips) + '\n</spine></sequence></project>\n'
           '</event>\n</library>\n</fcpxml>\n')
    out = f'{ROOT}/{cfg["event"]}/XML/{cfg["project"]}.fcpxml'
    open(out, "w").write(xml)
    print(f"== {out}\n   {float(total):.2f}s, {len(spine)} talking-head pieces")
    print("\n".join("   " + r for r in sorted(report)))
    return sheet

def contact(sheet, out):
    from PIL import Image, ImageDraw
    import io
    W, H = 120, 213; cols = 10
    rows = (len(sheet) + cols - 1) // cols
    im = Image.new("RGB", (cols * W, rows * (H + 14)), "black"); d = ImageDraw.Draw(im)
    for i, (path, t, lab) in enumerate(sheet):
        png = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t + 0.15:.2f}", "-i", path, "-frames:v", "1",
                              "-vf", f"scale={W}:{H}", "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout
        x, y = (i % cols) * W, (i // cols) * (H + 14)
        try: im.paste(Image.open(io.BytesIO(png)), (x, y))
        except Exception: pass
        d.text((x + 2, y + H), lab, fill="yellow")
    im.save(out)

POP = dict(path=f"{ROOT}/Nov 16 Give Oakville Charity Talk/Sound/Cute Pop Sound Effects - SOUNDFX FREE (youtube) (2).mp3",
           **{"in": 0.75, "len": 0.25, "lead": 0.02, "vol": "-14dB"})
DING = dict(path=f"{ROOT}/Nov 16 Give Oakville Charity Talk/Sound/Ding - Sound Effect (HD) - Gaming Sound FX (youtube) (1).mp3",
            **{"in": 0.21, "len": 0.85, "lead": 0.02, "vol": "-16dB"})
GFX = f"{ROOT}/Nov 16 Give Oakville Charity Talk/Graphics"

GOLDEN = dict(
    project="Golden Run One Month - storytelling v1", event="Nov 16 Golden Run One Month Talk",
    talking_head=f"{ROOT}/Nov 16 Golden Run One Month Talk/IMG_0562.MOV", cut=f"{CUT_DIR}/cut_0562.json",
    song=f"{ROOT}/Nov 16 Golden Run One Month Talk/Sound/Evergreen (feat. Caamp) 4.mp3", song_in=15.0, song_db="-20dB",
    beats=f"{BEATS_DIR}/evergreen_beats.json",
    bursts=[
        dict(line="G01", word=40.44, clip=f"{GR}/03 Run/IMG_0264.MOV", ins=[2.6, 3.7], note="golden run group in Oakville: the meeting spot"),
        dict(line="G02", word=54.14, clip=f"{GR}/03 Run/IMG_0269.MOV", ins=[0.2, 1.1, 2.0, 2.8], note="over 25 people showed up: the pack takes off"),
        dict(line="G03", word=116.44, clip=f"{GR}/03 Run/IMG_0272.MOV", ins=[0.9, 2.7, 6.2, 11.5], note="we host free community runs: down the street"),
        dict(line="G04", word=171.66, end_src=174.24, clip=f"{GR}/03 Run/IMG_0276.MOV", ins=[1.3, 3.9, 6.5, 9.1], note="beautiful 6K run early in the morning: lake path"),
        dict(line="G04", word=182.60, end_src=184.20, clip=f"{GR}/03 Run/IMG_0287.MOV", ins=[26.3, 27.2], note="music playing: he has the speaker"),
        dict(line="G05", word=200.64, clip=f"{GR}/03 Run/IMG_0278.MOV", ins=[0.2, 0.9, 1.6], end_src=202.70, note="completely free: runners in the park"),
        dict(line="G06", word=222.22, clip=f"{GR}/03 Run/IMG_0266.MOV", ins=[0.3, 1.4, 3.2], note="two random guys running past us"),
        dict(line="G08", word=239.58, end_src=240.70, clip=f"{GR}/03 Run/IMG_0267.MOV", ins=[0.2, 0.9], note="then they just joined us: handshake"),
        dict(line="G08", word=243.90, clip=f"{GR}/03 Run/IMG_0302.MOV", ins=[4.0, 12.1, 14.8], note="we literally just saw you guys running: the two guys"),
        dict(line="G10", word=250.06, clip=f"{GR}/03 Run/IMG_0326.MOV", ins=[3.8, 6.4, 8.9], note="two random old ladies (with their dogs)"),
        dict(line="G11", word=256.62, clip=f"{GR}/03 Run/IMG_0330.MOV", ins=[1.0, 5.8, 6.6], note="this random dad (check: is this him?)"),
        dict(line="G12", word=267.72, end_src=269.60, clip=f"{GR}/04 Cafe Panchita/IMG_9174.MOV", ins=[0.6, 1.8], note="got coffee after at Panchita Cafe"),
        dict(line="G12", word=269.84, clip=f"{GR}/04 Cafe Panchita/IMG_0332.MOV", ins=[5.1, 8.5], note="shout out Alejandra"),
        dict(line="G13", word=288.08, clip=f"{GR}/03 Run/IMG_0303.MOV", ins=[0.5, 3.4, 7.4], note="already poppin: group photo"),
        dict(line="G14", word=295.36, end_src=296.80, clip=f"{GR}/03 Run/IMG_0279.MOV", ins=[2.4, 3.3], note="vibes at an all time high"),
    ])

CHARITY = dict(
    project="Give Oakville Charity - storytelling v1", event="Nov 16 Give Oakville Charity Talk",
    talking_head=f"{ROOT}/Nov 16 Give Oakville Charity Talk/IMG_0564.MOV", cut=f"{CUT_DIR}/cut_0564.json",
    song=f"{ROOT}/Nov 16 Give Oakville Charity Talk/Sound/Every Living Breathing Moment - Grant Steller (Piano Cover).mp3",
    song_in=3.0, song_db="-14dB", beats=f"{BEATS_DIR}/elbm_beats.json", ding=DING, pop=POP,
    bursts=[
        dict(line="C02", word=107.18, end_src=109.80, clip=f"{AX}/IMG_9966.MOV", ins=[97.7, 120.0, 136.8], note="pitching my run club to a room full of community leaders"),
        dict(line="C02", word=110.36, clip=f"{AX}/IMG_9970.MOV", ins=[2.5, 3.2, 3.9], note="Jeff Knoll, Oakville's new mayor: handshake"),
        dict(line="C03", word=121.12, clip=f"{N8}/IMG_9754.MOV", ins=[0.4, 1.2, 2.0], note="at the end of one of our run clubs (Nov 8 run)"),
        dict(line="C04", word=126.24, end_src=127.30, clip=f"{AP}/IMG_0427.MOV", ins=[7.6, 8.4], note="this is Alix"),
        dict(line="C04", word=127.42, clip=f"{AP}/IMG_0420.MOV", ins=[1.9, 5.7], note="Oakville Community Foundation table"),
        dict(line="C05", word=135.64, clip=f"{AX}/IMG_9775.MOV", ins=[2.4, 5.6, 8.7], note="same day we hopped on a call (Nov 8 FaceTime)"),
        dict(line="C06", word=145.78, end_src=147.40, clip=f"{AX}/IMG_9945.MOV", ins=[2.0, 3.7], note="invite me to her home"),
        dict(line="C06", word=147.72, clip=f"{AX}/IMG_9948.MOV", ins=[5.0, 5.8, 6.4], note="where she was hosting a lunch"),
        dict(line="C07", word=172.30, clip=f"{AX}/IMG_9962.MOV", ins=[10.3, 30.8, 51.3], note="big room of local Oakville politicians"),
        dict(line="C08", word=249.24, clip=f"{AX}/IMG_9967.MOV", ins=[3.5, 5.8, 8.2], note="Alix on the mic with Jeff seated: come up here"),
        dict(line="C10", word=281.00, clip=f"{AX}/IMG_9966.MOV", ins=[254.0, 214.9, 293.1], note="locked in and even set my phone up: the pitch"),
        dict(line="C15", word=355.24, clip=f"{AP}/IMG_0461.MOV", ins=[1.7, 3.0, 4.3], note="including right here in Oakville: Give Oakville crowd"),
        dict(line="C16", word=365.80, clip=f"{AP}/IMG_0409.MOV", ins=[0.7, 2.0, 3.3], note="my co-founder Michi"),
        dict(line="C17", word=384.32, clip=f"{AP}/IMG_0410.MOV", ins=[0.2, 1.0, 1.9], note="they said yes: Start to finish baby"),
        dict(line="C18", word=389.86, clip=f"{AP}/IMG_0405.MOV", ins=[2.4, 3.5, 4.3], note="Michi came all the way from Waterloo"),
        dict(line="C19", word=414.34, end_src=418.10, clip=f"{AP}/IMG_0421.MOV", ins=[7.0, 12.5, 15.3, 16.0], note="charity networking event: 70+ charities"),
        dict(line="C19", word=418.18, clip=f"{AP}/IMG_0468.MOV", ins=[3.3, 4.3], note="Give Oakville: donations slide"),
        dict(line="C20", word=433.24, end_src=434.30, clip=f"{AP}/IMG_0458.MOV", ins=[1.9, 2.6], note="met a bunch of other charities"),
        dict(line="C20", word=434.36, clip=f"{AP}/IMG_0427.MOV", ins=[10.6, 11.6, 14.2], note="Michi got to meet Alix in person"),
        dict(line="C21", word=447.38, clip=f"{AP}/IMG_0423.MOV", ins=[14.0, 15.0, 16.0],
             note="people at Start2Finish? Sam: I'll be there Nov 29 (check)"),
        dict(line="C21", word=447.38, clip=f"{AP}/IMG_0459.MOV", ins=[1.0, 4.8, 8.6], lane=2, enabled=False,
             note="ALT for people at Start2Finish: Michi talking at a booth"),
        dict(line="C23", word=496.40, end_src=499.30, clip=f"{GR}/03 Run/IMG_0269.MOV", ins=[0.2, 1.1, 2.0, 2.8], note="our regular Sunday run"),
        dict(line="C24", word=520.68, end_src=522.10, clip=f"{GR}/03 Run/IMG_0264.MOV", ins=[2.6, 3.7], note="same meeting spot, same route"),
        dict(line="C25", word=540.66, clip=f"{GR}/03 Run/IMG_0283.MOV", ins=[0.3, 1.6, 3.0], note="every pace is welcome as always"),
        dict(line="C28", word=566.10, clip=f"{AP}/IMG_0469.MOV", ins=[0.5, 2.7, 7.0], note="follow all of us: Ariel and Michi"),
        dict(line="C29", word=587.24, clip=f"{AP}/IMG_0427.MOV", ins=[17.3, 23.4], note="a random lady coming to the run club: Alix"),
        dict(line="C30", word=593.64, clip=f"{GR}/03 Run/IMG_0303.MOV", ins=[0.5, 3.4, 7.4], note="running for kids all over Oakville together"),
    ],
    graphics=[
        dict(path=f"{GFX}/S2F logo.png", word=303.54, out_line="C11", width_px=420, cx=482, cy=1170, lane=3, sfx="ding"),
        dict(path=f"{GFX}/S2F Running Reading Club title.png", word=311.48, out_line="C12", width_px=700, cx=482, cy=1130, lane=3, sfx="pop"),
        dict(path=f"{GFX}/S2F kids reading.png", word=312.20, out_line="C12", width_px=300, cx=300, cy=1400, lane=4, sfx="pop"),
        dict(path=f"{GFX}/S2F year-end girl.png", word=313.40, out_line="C12", width_px=300, cx=640, cy=1400, lane=5, sfx="pop"),
    ])

if __name__ == "__main__":
    os.makedirs(SHEET_DIR, exist_ok=True)
    for cfg in (GOLDEN, CHARITY):
        sheet = build(cfg)
        contact(sheet, f"{SHEET_DIR}/{cfg['event']}.png")
