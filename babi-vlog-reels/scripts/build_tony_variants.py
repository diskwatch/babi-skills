#!/usr/bin/env python3
"""Trial-reel variants of Babi's "Nov 22 Tony Pulled through fun edit V1".

Reads his V1 export (assets with library uids), lays out each variant on the song's
beat grid (drop locked on "and he pulled through"), adds one-word captions
(Helvetica Neue Bold 40, white, y -165) and the music bed with V1's ducking moves.
All projects go into ONE fcpxml for the event "Nov 22 Sunday Run".
"""
import json, re, sys, os, html
import xml.etree.ElementTree as ET
from fractions import Fraction as F
import numpy as np

WORK = os.path.dirname(os.path.abspath(__file__))
V1 = "/Volumes/Babi's 2TB/Babiontherun/Fall26/Exports/XMLs/Nov 22 Tony Pulled through fun edit V1.fcpxmld/Info.fcpxml"
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(WORK, "tony_variants.fcpxml")
MEDIA = "/Volumes/Babi's 2TB/Babiontherun/Fall26/Media/Vlogs/Nov 22 Sunday Run"
SONGS = "/Volumes/Babi's 2TB/Babiontherun/Fall26/Fall26 20261018_1446_EDT.fcpbundle/SONGS/Original Media"

FD = F(1001, 60000)                     # project frame (59.94)
def fr(x): return round(F(x) / FD) * FD
def r(x):
    x = F(x)
    return "0s" if x == 0 else f"{x.numerator}/{x.denominator}s"

# ---------------------------------------------------------------- media + uids
UIDS = {l.split()[0]: l.split()[1] for l in open(os.path.join(WORK, "uids.txt"))}
DURS = {l.split()[0]: (float(l.split()[1]), l.split()[2].rstrip(",")) for l in open(os.path.join(WORK, "durs.txt"))}
SRC_FD = {"60000/1001": F(1001, 60000), "60/1": F(1, 60), "30000/1001": F(1001, 30000), "30/1": F(1, 30)}

# ---------------------------------------------------------------- words
W = {}
for fjs in ("words_main.json", "words_more.json"):
    for k, v in json.load(open(os.path.join(WORK, fjs))).items():
        W[os.path.basename(k)[:-4]] = [(a, b, t) for a, b, t in v]
# medium.en re-check of slices (whisper garbled these on the whole take)
W["IMG_1126"] = [w for w in W["IMG_1126"] if not (61.5 <= w[0] < 78)] + [
    (62.02, 62.34, "alright"), (62.34, 62.54, "helen"), (62.54, 62.6, "i'm"), (62.6, 62.82, "happy"), (62.82, 63.08, "about"),
    (63.08, 63.26, "that"), (63.48, 63.56, "nice"), (63.56, 63.6, "to"), (63.6, 63.66, "meet"), (63.66, 63.68, "you"),
    (63.68, 63.72, "have"), (63.72, 63.82, "a"), (63.82, 63.98, "great"), (63.98, 64.24, "day"), (64.44, 64.56, "thanks"),
    (64.56, 64.74, "so"), (64.74, 64.9, "much"), (65.02, 65.06, "have"), (65.06, 65.14, "an"), (65.14, 65.36, "amazing"),
    (65.36, 65.58, "day"), (65.7, 65.8, "okay"),
    (74.94, 75.34, "bye"), (75.34, 75.74, "helen"), (76.16, 76.28, "see"), (76.28, 76.68, "ya"), (76.78, 76.96, "take"),
    (76.96, 77.16, "care"), (77.28, 77.46, "bye")]
W["IMG_1126"].sort()
FIX = {"helen": "hellen", "bobby": "babi"}

# ---------------------------------------------------------------- songs
def bigger_grid():
    b = np.load(os.path.join(WORK, "bigger.wav.beats.npy"))
    return sorted(set(list(b) + list((b[:-1] + b[1:]) / 2)))
def dogdays_grid():
    p, ph = 0.3994612621199899, 112.37388829683918
    g = ph + p / 2 * np.arange(-400, 800)
    return list(g)
SONG = {
    "bigger": dict(file="Burna Boy - Bigger (From Grand Theft Auto VI_ The Album).mp3", uid="BEDBD51135A279B7678D49B98707C413",
                   samples=8125127, drop=19.613, trim=0, grid=bigger_grid(), hb=0.2336, name="Burna Boy - Bigger (From Grand Theft Auto VI_ The Album)"),
    "dogdays": dict(file="Florence + The Machine - Dog Days Are Over (2010 Version) (Official Music Video) 4.mp3", uid="4EAC4A79220DFAAE688C8C2FF2A45F39",
                    samples=int(round(219.208 * 48000)), drop=124.715, trim=-7, grid=dogdays_grid(), hb=0.1997,
                    name="Florence + The Machine - Dog Days Are Over (2010 Version) (Official Music Video) 4"),
}

# ---------------------------------------------------------------- building blocks (src seconds from Babi's V1)
def T(clip, a, b, **k): return dict(kind="talk", clip=clip, i=a, o=b, **k)
def M(clip, a, n, **k): return dict(kind="broll", clip=clip, i=a, d=n * 0.2336, **k)   # n = half-beats of Bigger (nominal)

INTRO = [T("IMG_1060", 1.718, 3.370), T("IMG_1060", 3.820, 4.738), T("IMG_1060", 4.955, 5.055),
         T("IMG_0330", 0.133, 1.067), T("IMG_0330", 1.418, 2.102), T("IMG_0330", 6.356, 7.557)]
DADFIRST = [T("IMG_0330", 0.133, 1.067), T("IMG_0330", 1.418, 2.102), T("IMG_0330", 6.356, 7.557),
            T("IMG_1060", 1.718, 3.370), T("IMG_1060", 3.820, 4.738, snap=False)]
DROP = [T("IMG_1060", 7.307, 9.443, drop=True), T("IMG_1060", 11.511, 12.696, snap=True)]
DROP_SHORT = [T("IMG_1060", 7.307, 9.443, drop=True, snap=True)]

# V1 montage, his src in-points and lengths (in half-beats of Bigger ~0.234 s)
def m1(hb=0.2336):
    rows = [("IMG_1058", 18.151, .317), ("IMG_1058", 19.503, .434), ("IMG_1058", 21.205, .350), ("IMG_1058", 36.570, .434),
            ("IMG_1042", 1.251, .617), ("IMG_1045", 8.859, .267), ("IMG_1045", 9.443, .317), ("IMG_1045", 11.028, .450),
            ("IMG_4383", 1.468, .450), ("IMG_4383", 2.669, .317), ("IMG_1052", 7.174, .601), ("IMG_1068", 1.583, .300),
            ("IMG_1068", 3.067, .300), ("IMG_1068", 4.400, .350), ("IMG_7527", 1.450, .851), ("IMG_7525", 0.734, 1.101, "vox"),
            ("IMG_7525", 2.336, 1.018, "vox"), ("IMG_7528", 1.983, .317), ("IMG_7528", 3.167, .450), ("IMG_7528", 4.317, .450),
            ("IMG_1074", 0.000, .317), ("IMG_1074", 2.069, .450), ("IMG_1074", 4.338, .450), ("IMG_1074", 6.173, .317),
            ("IMG_1100", 5.033, .434, "aud"), ("IMG_1100", 7.967, .484, "aud"), ("IMG_1100", 10.183, .884, "aud"),
            ("IMG_1100", 12.600, .617, "aud"), ("IMG_1105", 5.205, 1.201, "aud", "ov"), ("IMG_1105", 11.628, 1.051, "aud")]
    out = []
    for row in rows:
        c, a, d = row[:3]; fl = row[3:]
        m = M(c, a, 1, vox="vox" in fl, aud=("aud" in fl or "vox" in fl), ov="ov" in fl); m["d"] = d
        if (c, a) == ("IMG_7525", 2.336): m["min"] = 1.03
        if (c, a) == ("IMG_1105", 11.628): m["min"] = 1.17
        out.append(m)
    return out
M1 = m1()
def drop_clips(ms, *names_idx):
    return [m for k, m in enumerate(ms) if k not in names_idx]

# Tony-focused montage from the rest of the day
M2 = [M("IMG_1070", 0.45, 2), M("IMG_1070", 2.45, 2), M("IMG_1044", 1.0, 3), M("IMG_1053", 3.05, 2), M("IMG_1053", 4.2, 2),
      M("IMG_1083", 0.95, 7, aud=True, vox=True, min=1.75), M("IMG_1102", 1.9, 3), M("IMG_1102", 3.1, 2), M("IMG_1103", 3.85, 2),
      M("IMG_1059", 17.4, 2), M("IMG_1109", 4.55, 3), M("IMG_4388", 0.2, 2), M("IMG_1093", 2.2, 2), M("IMG_1093", 6.1, 3),
      M("IMG_7526", 7.8, 4), M("IMG_1105", 5.205, 5, aud=True, ov=True), M("IMG_1105", 11.628, 5, aud=True, min=1.17)]

HELLEN_FULL = [T("IMG_1126", 42.776, 43.560, g=2), T("IMG_1126", 44.161, 46.697, g=3), T("IMG_1126", 46.997, 50.133, g=3),
               T("IMG_1126", 51.585, 58.025, g=3), T("IMG_1126", 58.525, 61.895, g=2), T("IMG_1126", 62.396, 64.364, g=2),
               T("IMG_1126", 64.364, 65.916, g=2, snap=True)]
CAFE = [M("IMG_4391", 12.512, 3), M("IMG_1116", 3.971, 1), M("IMG_1116", 5.339, 2), M("IMG_1116", 6.924, 3),
        M("IMG_1111", 7.491, 2), M("IMG_1111", 8.842, 2), M("IMG_1111", 9.643, 2)]
ENDCLIP = [T("IMG_1126", 73.273, 77.527, end=True,
             kf=[(73.552, "12dB"), (73.786, "-2dB"), (74.537, "-2dB"), (74.760, "3dB")])]
HOOK_ACTION = [T("IMG_1126", 44.161, 46.697, g=3, hook=True)]
HOOK_FRIENDS = [T("IMG_1126", 58.525, 60.70, g=2, hook=True)]
BOATS_END = [T("IMG_1105", 10.30, 14.30), T("IMG_1105", 14.80, 15.45, last=True)]

VARIANTS = [
    ("V2", "bigger", "same start, tighter montage, ends on the cafe (no Hellen ending)",
     INTRO + DROP + drop_clips(M1, 4, 11, 12, 13, 23) + HELLEN_FULL[:5] + HELLEN_FULL[6:] + CAFE),
    ("V3", "bigger", "hook: Hellen 'you have to take action with your life to change it'",
     HOOK_ACTION + INTRO + DROP + M1 + HELLEN_FULL + CAFE + ENDCLIP),
    ("V4", "bigger", "starts on Tony's dad 'are you coming next week', Tony montage",
     DADFIRST + DROP + M2 + HELLEN_FULL[:5] + HELLEN_FULL[6:] + CAFE + ENDCLIP),
    ("V5", "bigger", "short: intro, quick montage, Hellen's 2 best lines",
     INTRO + DROP_SHORT + [M1[k] for k in (0, 1, 5, 7, 10, 14, 15, 16, 26, 28, 29)] + HELLEN_FULL[1:3] + [HELLEN_FULL[6]] + CAFE[:4]),
    ("V6", "bigger", "Tony only: story + montage, ends on 'who's going to carry the boats'",
     INTRO + DROP + [m for m in M2 if m["clip"] != "IMG_1105"] + [M1[k] for k in (14, 15, 16)] + BOATS_END),
    ("V7", "bigger", "hook: Hellen 'and now I have too many friends'",
     HOOK_FRIENDS + INTRO + DROP + drop_clips(M1, 0, 2, 9, 19, 21) + HELLEN_FULL[:6] + [HELLEN_FULL[6]] + CAFE[:4]),
    ("V8", "dogdays", "Dog Days Are Over, V1 structure",
     INTRO + DROP + M1 + HELLEN_FULL + CAFE + ENDCLIP),
    ("V9", "dogdays", "Dog Days, Tony's dad first, Tony montage, no Hellen ending",
     DADFIRST + DROP + M2 + HELLEN_FULL[:5] + HELLEN_FULL[6:] + CAFE),
    ("V10", "dogdays", "Dog Days, hook 'take action', short",
     HOOK_ACTION + INTRO + DROP_SHORT + [M2[k] for k in (0, 1, 2, 5, 6, 7, 10, 14, 15)] + HELLEN_FULL[2:3] + [HELLEN_FULL[6]] + CAFE[:4]),
]

# ---------------------------------------------------------------- layout
def layout(pieces, song):
    S = SONG[song]
    P = [dict(p) for p in pieces]
    # pre-drop: exact durations
    t = F(0); k = 0
    while not P[k].get("drop"):
        p = P[k]; p["off"] = fr(t); p["du"] = fr(F(p["o"]) - F(p["i"])); t = p["off"] + p["du"]; k += 1
    t_drop = fr(t)
    s0 = S["drop"] - float(t_drop)               # song time at timeline 0
    assert s0 > 0, s0
    G = [g - s0 for g in S["grid"]]
    def nearest(x, after, mn=0.15):
        c = [g for g in G if g >= after + mn]
        return min(c, key=lambda g: abs(g - x))
    def up(x): return min(g for g in G if g >= x - 0.02)
    ideal = float(t)
    for p in P[k:]:
        p["off"] = fr(t)
        if p["kind"] == "talk":
            end = float(t) + (p["o"] - p["i"])
            if p.get("snap"): end = up(end)
            ideal = end
        else:
            ideal += p["d"] * S["hb"] / 0.2336
            end = nearest(ideal, float(t), max(0.26, p.get("min", 0)))
        p["du"] = fr(end) - p["off"]
        assert p["du"] > 0
        t = p["off"] + p["du"]
    total = t
    for p in P:
        fps = DURS[p["clip"]][1]; sfd = SRC_FD[fps]
        p["st"] = round(F(p["i"]) / sfd) * sfd
        assert float(p["st"] + p["du"]) <= DURS[p["clip"]][0] + 0.01, (p["clip"], float(p["st"] + p["du"]))
    return P, total, s0, t_drop

# ---------------------------------------------------------------- captions
def captions(P, total):
    caps = []
    for k, p in enumerate(P):
        if not (p["kind"] == "talk" or p.get("aud")): continue
        a, b = float(p["st"]), float(p["st"] + p["du"])
        for ws, we, wt in W.get(p["clip"], []):
            if we - ws > 0.35: ws = we - 0.3          # whisper stretches a word back over the pause before it
            c = (ws + we) / 2
            ov = min(b, we) - max(a, ws)
            if not (a <= c < b or (ov >= 0.08 and ov >= 0.4 * (we - ws))): continue
            txt = re.sub(r"[^\w']", "", wt.lower()).strip("'")
            txt = FIX.get(txt, txt)
            if not txt: continue
            s = float(p["off"]) + max(0, ws - a); e = float(p["off"]) + min(b, we + 0.3) - a
            caps.append([s, e, txt, k])
    caps.sort()
    out = []
    for i, c in enumerate(caps):
        s = fr(c[0]); e = fr(c[1])
        if i + 1 < len(caps): e = min(e, fr(caps[i + 1][0]))
        e = min(e, total)
        if out and s < out[-1][1]: s = out[-1][1]
        if e - s < 3 * FD:
            e = s + 3 * FD
            if i + 1 < len(caps) and e > fr(caps[i + 1][0]): caps[i + 1][0] = float(e)
        out.append([s, e, c[2], c[3]])
    for i in range(1, len(out)): assert out[i][0] >= out[i - 1][1], out[i]
    return out

# ---------------------------------------------------------------- music volume (Babi's V1 moves)
def music_keys(P, total, s0, t_drop, has_end):
    k = []  # (timeline t, dB)
    k += [(0.2, -13)]
    k += [(float(t_drop) - 1.15, -9), (float(t_drop) + 0.30, 0)]
    # hook before the intro: same -16 bed as under Hellen
    if P[0].get("hook"):
        k = [(0.0, -16), (float(P[0]["off"] + P[0]["du"]) - 0.05, -16), (float(P[0]["off"] + P[0]["du"]) + 0.2, -13)] + k[1:]
    # Hellen talk blocks after the drop
    i = 0; post = [p for p in P if float(p["off"]) > float(t_drop) + 0.5]
    while i < len(post):
        if post[i]["kind"] == "talk" and post[i]["clip"] == "IMG_1126" and not post[i].get("end"):
            j = i
            while j + 1 < len(post) and post[j + 1]["kind"] == "talk" and post[j + 1]["clip"] == "IMG_1126" and not post[j + 1].get("end"): j += 1
            s = float(post[i]["off"]); e = float(post[j]["off"] + post[j]["du"])
            k += [(s - 1.0, 0), (s + 0.45, -16)]
            if j + 1 < len(post) and not post[j + 1].get("end"): k += [(e - 1.0, -16), (e + 0.5, 0)]
            i = j + 1; continue
        if post[i].get("vox"):
            s = float(post[i]["off"]); j = i
            while j + 1 < len(post) and post[j + 1].get("vox"): j += 1
            e = float(post[j]["off"] + post[j]["du"])
            k += [(s - 0.12, 0), (s + 0.08, -5), (e - 0.2, -5), (e + 0.05, 0)]
            i = j + 1; continue
        i += 1
    if has_end:
        mend = float(P[-1]["off"])
        k += [(mend - 0.6, k[-1][1] if k else 0), (mend, -16)]
    else:
        k += [(float(total) - 0.6, 0), (float(total), -30)]
    k.sort()
    clean = []
    for t, d in k:
        if clean and t <= clean[-1][0] + 0.01: continue
        clean.append((t, d))
    return clean

# ---------------------------------------------------------------- xml
def main():
    src = open(V1).read()
    res_block = src[src.index("<resources>") + len("<resources>"): src.index("</resources>")]
    # drop the two compound clips (we flatten them) — keep everything else from his export
    res_block = re.sub(r'<media id="r2".*?</media>', "", res_block, flags=re.S)
    res_block = re.sub(r'<media id="r8".*?</media>', "", res_block, flags=re.S)
    root = ET.fromstring(src)
    have = {}
    for a in root.iter("asset"):
        nm = html.unescape(a.find("media-rep").get("src")).split("/")[-1]
        have[nm.replace("%20", " ").rsplit(".", 1)[0]] = a.get("id")
    fmt_of = {a.get("id"): a.get("format") for a in root.iter("asset")}
    extra = []
    FMT_NEW = {"30/1": "rx30"}
    extra.append('<format id="rx30" frameDuration="1/30s" width="1080" height="1920" colorSpace="9-18-9 (Rec. 2020 HLG)"/>')
    ASSET_FMT = {"60000/1001": "r4", "60/1": "r4", "30000/1001": "r13", "30/1": "rx30"}
    used = set()
    for v in VARIANTS:
        for p in v[3]: used.add(p["clip"])
    for c in sorted(used):
        if c in have: continue
        dur, fps = DURS[c]
        aid = "a_" + c
        extra.append(f'<asset id="{aid}" name="{c}" uid="{UIDS[c + ".MOV"]}" start="0s" duration="{round(dur*600)}/600s" hasVideo="1" format="{ASSET_FMT[fps]}" hasAudio="1" videoSources="1" audioSources="1" audioChannels="2" audioRate="48000">'
                     f'<media-rep kind="original-media" sig="{UIDS[c + ".MOV"]}" src="file://{MEDIA.replace(" ", "%20")}/{c}.MOV"/></asset>')
        have[c] = aid
    S = SONG["dogdays"]
    extra.append(f'<asset id="a_dogdays" name="{S["name"]}" uid="{S["uid"]}" start="0s" duration="{S["samples"]}/48000s" hasAudio="1" audioSources="1" audioChannels="2" audioRate="48000">'
                 f'<media-rep kind="original-media" sig="{S["uid"]}" src="file://{SONGS.replace(" ", "%20").replace("+", "%2B")}/{S["file"].replace(" ", "%20").replace("+", "%2B")}"/></asset>')
    extra.append('<effect id="eT" name="Basic Title" uid=".../Titles.localized/Bumper:Opener.localized/Basic Title.localized/Basic Title.moti"/>')
    SONG["bigger"]["ref"] = "r6"; SONG["dogdays"]["ref"] = "a_dogdays"

    def clipfmt(c):
        fps = DURS[c][1]
        if fps == "60000/1001": return 'format="r5"', ""
        if fps == "60/1": return 'format="r4"', '<conform-rate srcFrameRate="60"/>'
        if fps == "30000/1001": return 'format="r14"', '<conform-rate scaleEnabled="0" srcFrameRate="29.97"/>'
        return 'format="rx30"', '<conform-rate srcFrameRate="30"/>'

    projects = []; report = []; ts_n = [0]
    for name, song, desc, pieces in VARIANTS:
        P, total, s0, t_drop = layout(pieces, song)
        caps = captions(P, total)
        has_end = P[-1].get("end", False)
        keys = music_keys(P, total, s0, t_drop, has_end)
        mdur = (P[-1]["off"] if has_end else total)
        Sg = SONG[song]
        spine = []
        for k, p in enumerate(P):
            ref = have[p["clip"]]; fa, conf = clipfmt(p["clip"])
            vol = ""
            if p.get("kf"):
                vol = "<adjust-volume><param name=\"amount\"><keyframeAnimation>" + "".join(
                    f'<keyframe time="{r(round(F(t) * 720000) / F(720000))}" value="{v}"/>' for t, v in p["kf"]) + "</keyframeAnimation></param></adjust-volume>"
            elif p["kind"] == "broll" and not p.get("aud"): vol = '<adjust-volume amount="-96dB"/>'
            elif p.get("g"): vol = f'<adjust-volume amount="{p["g"]}dB"/>'
            inner = []
            if k == 0:
                mstart = round(F(s0) * 48000) / F(48000)
                kf = "".join(f'<keyframe time="{r(round((F(s0) + F(t)) * 720000) / F(720000))}" value="{max(-96, d + Sg["trim"])}dB"/>' for t, d in keys)
                inner.append(f'<asset-clip ref="{Sg["ref"]}" lane="-1" offset="{r(p["st"])}" name="{html.escape(Sg["name"])}" start="{r(mstart)}" duration="{r(mdur)}" audioRole="music">'
                             f'<adjust-volume><param name="amount"><keyframeAnimation>{kf}</keyframeAnimation></param></adjust-volume></asset-clip>')
            if p.get("ov"):
                nxt = P[k + 1] if k + 1 < len(P) else None
                od = min(F(135135, 60000), p["du"] + (nxt["du"] if nxt else 0))
                inner.append(f'<video ref="r25" lane="1" offset="{r(p["st"])}" name="IMG_1137" start="3600s" duration="{r(od)}">'
                             '<adjust-transform position="-14.4363 -8.4077" scale="0.4786 0.4786"/></video>')
            for s, e, txt, kk in caps:
                if kk != k: continue
                ts_n[0] += 1; n = ts_n[0]
                inner.append(f'<title ref="eT" lane="2" offset="{r(p["st"] + s - p["off"])}" name="{txt}" start="3600s" duration="{r(e - s)}">'
                             '<param name="Position" key="9999/999166631/999166633/1/100/101" value="0 -165"/>'
                             '<param name="Flatten" key="9999/999166631/999166633/2/351" value="1"/>'
                             '<param name="Alignment" key="9999/999166631/999166633/2/354/999169573/401" value="1 (Center)"/>'
                             f'<text><text-style ref="ts{n}">{txt}</text-style></text>'
                             f'<text-style-def id="ts{n}"><text-style font="Helvetica Neue" fontSize="40" fontFace="Bold" fontColor="1 1 1 1" '
                             'shadowColor="0 0 0 0.75" shadowOffset="4 315" shadowBlurRadius="8" alignment="center"/></text-style-def></title>')
            iso = '<audio-channel-source srcCh="1, 2"><adjust-voiceIsolation amount="33"/></audio-channel-source>' if p["clip"] in ("IMG_1060", "IMG_0330") else ""
            spine.append(f'<asset-clip ref="{ref}" offset="{r(p["off"])}" name="{p["clip"]}" start="{r(p["st"])}" duration="{r(p["du"])}" {fa} tcFormat="NDF" audioRole="dialogue">'
                         f'{conf}{vol}{"".join(inner)}{iso}</asset-clip>')
        pname = f"Nov 22 Tony Pulled through fun edit {name}"
        projects.append(f'<project name="{pname}"><sequence format="r1" duration="{r(total)}" tcStart="0s" tcFormat="NDF" audioLayout="stereo" audioRate="48k"><spine>\n'
                        + "\n".join(spine) + "\n</spine></sequence></project>")
        report.append(dict(name=pname, song=song, desc=desc, dur=float(total), drop=float(t_drop), s0=s0, n=len(P), caps=len(caps),
                           ends_hellen=has_end, cuts=[float(p["off"]) for p in P], pieces=[(p["clip"], float(p["st"]), float(p["du"]), p["kind"], bool(p.get("aud")) or p["kind"]=="talk") for p in P],
                           capwords=" ".join(c[2] for c in caps), keys=keys))
    X = ('<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE fcpxml>\n<fcpxml version="1.15">\n<resources>' + res_block + "\n" + "\n".join(extra) +
         '\n</resources>\n<library><event name="Nov 22 Sunday Run" uid="3AC9A9C6-8DD4-4F31-BB74-ADB093EFEA96">\n' + "\n".join(projects) +
         "\n</event></library>\n</fcpxml>\n")
    open(OUT, "w").write(X)
    json.dump(report, open(os.path.join(WORK, "report.json"), "w"), indent=1)
    for x in report:
        print(f'{x["name"][-3:]:>4} {x["song"]:8s} {x["dur"]:5.1f}s drop@{x["drop"]:.2f} song0={x["s0"]:.2f} pieces={x["n"]} caps={x["caps"]} endHellen={x["ends_hellen"]}  {x["desc"]}')

main()
