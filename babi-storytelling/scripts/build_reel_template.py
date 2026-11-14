"""Creator Lab reel -> FCPXML (TME library, event 'Nov 12 Black Friday').
Talking head IMG_0078 cut tight; B-roll bursts (pick on lane 1 + disabled alternates above);
chat-screenshot pops with pop SFX; Ding on reveals; 'In Motion' music bed kicking on the chat payoff.
"""
import json, wave, os, re, subprocess, urllib.parse, numpy as np

SCR = os.path.dirname(os.path.abspath(__file__))
BF = os.path.join(SCR, "..", "bf")
EVENT_DIR = "/Volumes/4TBSSD_4/Babi NR Content/Media/OFFICE/Nov 12 Black Friday"
BROLL_DIR = f"{EVENT_DIR}/Creator Lab B-Roll"
CHAT_DIR = f"{EVENT_DIR}/Creator Lab Excitement"
MUSIC = "/Volumes/4TBSSD_4/Babi NR Content/Songs/STORYTELLING/Jack Style/In Motion (HD) - From the Soundtrack to _The Social Network_ 4.mp3"
OUTDIR = os.path.expanduser("~/Desktop/Creator Lab Reel.fcpxmld")
PROJECT = os.environ.get("PROJECT", "Creator Lab Reel")
FPS = 60
PRE, POST, MAX_INNER_GAP = 0.05, 0.07, 0.30
POP_HOLD = 3.4          # silent beat after "the chat absolutely lost it"
MUSIC_KICK = 181.95     # loud re-entry in 'In Motion' (song seconds)

EVENT_UID = "8CDA26A5-601A-4C11-984C-85B9695F137E"
UID_0078 = "27B3E44132404D2B59F3DDDE795355D6"
DING = dict(uid="4E71FBAE44E48B72F7129128F1654579", name="Ding - Sound Effect (HD) - Gaming Sound FX (youtube) (1)",
            src="/Volumes/4TBSSD_4/Babi NR Content/Songs/SOUND FX/Ding - Sound Effect (HD) - Gaming Sound FX (youtube) (1).mp3",
            dur="135936/44100s", rate=44100)
POP = dict(uid="AFAE54967434581F31B1054D9B88BECC", name="Censor sound __ Funny sound __ Mouse click sound __ Pop sound __ Slap sound __ Short sound effect",
           src="/Volumes/4TBSSD_4/Babi NR Content/Sound FX/click and keyboard/Censor sound __ Funny sound __ Mouse click sound __ Pop sound __ Slap sound __ Short sound effect.mp3",
           dur="231271/48000s", rate=48000)

# ---------------- talking head lines (IMG_0078): (first word, last word start, start override, end override, label)
LINES = [
    (83.66, 87.80, None, None, "hook"),
    (128.30, 132.26, None, None, "once a month"),
    (163.30, 169.58, None, None, "black friday"),
    (193.96, 199.10, None, None, "loved it"),
    (225.48, 228.46, None, None, "paused"),
    (324.88, 330.32, None, None, "new tool"),
    (452.16, 455.28, None, None, "rave"),
    (463.54, 469.52, None, None, "log off"),
    (579.26, 583.44, None, None, "marcus"),
    (586.36, 588.74, None, None, "what the heck"),
    (591.26, 592.32, None, 592.85, "doorway"),
    (627.34, 631.80, None, None, "creator lab"),
    (634.46, 637.94, None, 638.42, "chatgpt claude"),
    (727.50, 729.40, None, 730.05, "lost it"),
    ("GAP", POP_HOLD, None, None, "pop hold"),
    (776.26, 782.66, None, None, "breakout"),
    (827.54, 831.76, None, None, "vision"),
    (862.54, 866.82, None, None, "close"),
]

def snap(t): return round(t * FPS) / FPS
def r(t): return f"{round(t * FPS) * 100}/6000s"

x = np.frombuffer(wave.open(f"{BF}/IMG_0078.wav").readframes(10**9), dtype=np.int16).astype(float) / 32768
n = len(x) // 160
DB = 20 * np.log10(np.sqrt((x[:n*160].reshape(n, 160) ** 2).mean(1)) + 1e-9)
THR = np.percentile(DB, 10) + 8

def speech_end(t):
    i = int(t * 100)
    while i < len(DB) - 15:
        if (DB[i:i+15] < THR).all(): return i / 100 + POST
        i += 1
    return t + 0.5

# spine items: ("clip", a, b, label) or ("gap", dur, label)
spine = []
for w0, wl, so, eo, lab in LINES:
    if w0 == "GAP":
        spine.append(("gap", snap(wl), lab)); continue
    a = so if so is not None else w0 - PRE
    b = speech_end(wl)
    if eo is not None: b = min(b, eo)
    i0, i1 = int(a * 100), int(b * 100)
    quiet = DB[i0:i1] < THR
    cur, k = a, 0
    while k < len(quiet):
        if quiet[k]:
            j = k
            while j < len(quiet) and quiet[j]: j += 1
            g0, g1 = (i0 + k) / 100, (i0 + j) / 100
            if g0 > a + 0.02 and g1 < b - 0.02 and g1 - g0 > MAX_INNER_GAP:
                spine.append(("clip", snap(cur), snap(g0 + POST), lab)); cur = g1 - PRE
            k = j
        else: k += 1
    spine.append(("clip", snap(cur), snap(b), lab))

# output timeline positions
pos, off = [], 0.0
for it in spine:
    d = it[2] - it[1] if it[0] == "clip" else it[1]
    pos.append((off, d)); off += d
TOTAL = off

def out_time(src_t):
    """source time in IMG_0078 -> output time (nearest kept piece)"""
    best = None
    for (o, d), it in zip(pos, spine):
        if it[0] != "clip": continue
        a, b = it[1], it[2]
        if a - 1e-6 <= src_t < b: return o + src_t - a
        if src_t < a and (best is None): best = o
    return best if best is not None else TOTAL

def gap_time(rel):
    for (o, d), it in zip(pos, spine):
        if it[0] == "gap": return o + rel

# ---------------- B-roll pool
pool = {s["id"]: s for s in json.load(open(f"{SCR}/broll_pool.json"))["shots"]}

# B-roll events: (anchor, dur, pick, [alternates])  anchor = source time in IMG_0078, or ("gap", rel)
BROLL = [
    (84.94, 0.72, "starting_soon", ["bf_offer_slide", "hi_im_stu_slide"]),
    (85.66, 0.80, "chat_scroll_1", ["chat_scroll_2", "dev_chat_screen"]),
    (86.46, 0.80, "wow_mouth_open", ["hands_on_head", "hand_over_mouth"]),
    (128.78, 0.80, "stu_teach_wide", ["stu_teach_wide2", "stu_desk_mic"]),
    (129.62, 0.80, "stu_on_tv_1", ["stu_on_tv_2", "team_watch_wide2"]),
    (130.46, 0.80, "team_watch_wide", ["room_wide_tv", "standing_watch"]),
    (164.60, 0.95, "starting_soon", ["bf_question_tv", "room_wide_tv"]),
    (166.52, 0.85, "bf_offer_slide", ["every_november", "hi_im_stu_slide"]),
    (168.00, 1.10, "buying_mode", ["every_november"]),
    (194.36, 0.80, "team_laugh_tv", ["woman_laugh", "striped_smile"]),
    (195.16, 0.75, "woman_laugh", ["guy_laugh_2", "glass_peek"]),
    (195.95, 0.65, "stu_teach_close", ["stu_desk_red", "stu_desk_mic_2"]),
    (226.10, 0.85, "stu_on_tv_2", ["stu_on_tv_3", "stu_desk_mic_2"]),
    (326.30, 0.80, "stu_desk_red", ["stu_teach_wide", "stu_desk_mic"]),
    (327.50, 0.85, "dev_team_1", ["dev_team_2", "dev_team_3"]),
    (328.80, 0.90, "connect_ai_screen", ["booth_laptop", "laptop_typing"]),
    (452.56, 0.80, "group_react", ["group_react_2", "team_laugh_tv"]),
    (453.90, 0.70, "booth_laptop", ["laptop_typing", "zoom_grid_laptop"]),
    (454.78, 0.75, "guy_laugh_1", ["dev_smile", "tongue_out", "guy_laugh_2"]),
    # Marcus is named: stack several developer options, only one enabled
    (579.66, 1.45, "dev_team_2", ["dev_team_1", "dev_team_3", "point_at_screen", "guy_laugh_1", "connect_ai_screen"]),
    (591.85, 0.95, "connect_ai_screen", ["dev_chat_screen", "point_at_screen"]),
    (628.45, 0.85, "zoom_grid_laptop", ["stu_on_tv_3", "stu_on_tv_1"]),
    (629.55, 0.85, "dev_chat_screen", ["chat_scroll_3", "booth_laptop"]),
    (630.75, 0.90, "booth_laptop", ["laptop_typing", "connect_ai_screen"]),
    (635.25, 0.90, "connect_ai_screen", ["dev_chat_screen", "zoom_grid_laptop"]),
    (("gap", 0.00), 0.60, "hands_on_head", ["wow_mouth_open"]),
    (("gap", 0.60), 0.55, "tongue_out", ["guy_laugh_1"]),
    (("gap", 1.15), 0.60, "hand_over_mouth", ["woman_laugh"]),
    (("gap", 1.75), 0.55, "team_laugh_tv", ["group_react_2"]),
    (("gap", 2.30), 0.55, "woman_laugh", ["striped_smile"]),
    (("gap", 2.85), 0.55, "group_react", ["glass_peek"]),
    (777.10, 0.85, "dev_team_3", ["green_watch", "dev_team_1"]),
    (778.25, 0.85, "booth_laptop", ["laptop_typing", "zoom_grid_laptop"]),
    (779.55, 0.85, "green_watch", ["dev_team_2", "standing_watch"]),
    (780.80, 1.30, "guy_laugh_1", ["dev_smile", "group_react_2", "tongue_out"]),
    (829.36, 0.62, "stu_teach_wide2", ["stu_teach_close", "stu_highfive"]),
    (830.28, 0.62, "dev_team_2", ["dev_team_1", "booth_laptop"]),
    (831.10, 0.75, "group_react_2", ["group_react", "team_laugh_tv"]),
    (862.54, 1.00, "debrief_stu_2", ["debrief_stu", "stu_highfive"]),
    (863.62, 0.95, "debrief_team", ["debrief_crew", "debrief_stu"]),
]

# chat pops: (anchor, screenshot index, (x, y), scale, hold_until_anchor or None)
CHAT = sorted(os.listdir(CHAT_DIR))
POPS = [
    # hook: chat losing it
    (87.36, 6, (0, -16), 0.80, 88.30),
    (87.70, 4, (0, -31), 0.80, 88.30),
    # payoff: the wall of chat
    (("gap", 0.00), 3, (0, 31), 0.78, ("gap", POP_HOLD)),
    (("gap", 0.38), 7, (-8, 18), 0.80, ("gap", POP_HOLD)),
    (("gap", 0.76), 1, (9, 0), 0.50, ("gap", POP_HOLD)),
    (("gap", 1.14), 14, (-5, -17), 0.80, ("gap", POP_HOLD)),
    (("gap", 1.52), 4, (4, -30), 0.80, ("gap", POP_HOLD)),
    (("gap", 1.90), 0, (-6, -42), 0.72, ("gap", POP_HOLD)),
    # breakout rooms: people getting set up
    (781.00, 8, (0, -17), 0.70, 783.10),
    (781.45, 11, (0, -29), 0.70, 783.10),
    (781.90, 13, (0, -41), 0.70, 783.10),
    # close: testimonial
    (864.20, 15, (0, -22), 0.60, 867.60),
]
DINGS = [591.95, 628.50, 864.20]

def T(anchor):
    if isinstance(anchor, tuple): return gap_time(anchor[1])
    return out_time(anchor)

# ---------------- assets
def probe(path):
    j = json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_entries",
        "format=duration:stream=codec_type,r_frame_rate,width,height", "-of", "json", path], capture_output=True, text=True).stdout)
    v = [s for s in j["streams"] if s["codec_type"] == "video"]
    return float(j["format"].get("duration", 0)), (v[0]["r_frame_rate"] if v else None), (v[0].get("width"), v[0].get("height")) if v else None

url = lambda p: "file://" + urllib.parse.quote(p)
FMT = {"60/1": ("fv60", "100/6000s"), "60000/1001": ("fv5994", "1001/60000s"), "30/1": ("fv30", "100/3000s")}
formats = {f'<format id="r1" frameDuration="100/6000s" width="1080" height="1920" colorSpace="9-18-9 (Rec. 2020 HLG)"/>'}
assets, aid = [], {}

assets.append(f'<asset id="a_th" name="IMG_0078" uid="{UID_0078}" start="0s" duration="522725/600s" hasVideo="1" format="r1" '
              f'hasAudio="1" videoSources="1" audioSources="1" audioChannels="2" audioRate="48000">'
              f'<media-rep kind="original-media" src="{url(EVENT_DIR + "/IMG_0078.MOV")}"/></asset>')
broll_files = sorted(f for f in os.listdir(BROLL_DIR) if f.upper().endswith(".MOV"))
BDUR = {}
for f in broll_files:
    p = f"{BROLL_DIR}/{f}"; d, rate, _ = probe(p); fid, fd = FMT[rate]
    formats.add(f'<format id="{fid}" frameDuration="{fd}" width="1080" height="1920" colorSpace="9-18-9 (Rec. 2020 HLG)"/>')
    k = f[:-4]; aid[k] = f"b_{k}"; BDUR[k] = d
    assets.append(f'<asset id="b_{k}" name="{k}" start="0s" duration="{round(d*600)}/600s" hasVideo="1" format="{fid}" '
                  f'hasAudio="1" videoSources="1" audioSources="1" audioChannels="2" audioRate="48000">'
                  f'<media-rep kind="original-media" src="{url(p)}"/></asset>')
for i, f in enumerate(CHAT):
    p = f"{CHAT_DIR}/{f}"; _, _, (w, h) = probe(p)
    formats.add(f'<format id="fi{i}" name="FFVideoFormatRateUndefined" width="{w}" height="{h}" colorSpace="1-13-1"/>')
    nm = f[:-4]
    assets.append(f'<asset id="c{i}" name="{nm}" start="0s" duration="0s" hasVideo="1" format="fi{i}" videoSources="1">'
                  f'<media-rep kind="original-media" src="{url(p)}"/></asset>')
formats.add('<format id="fa" name="FFVideoFormatRateUndefined"/>')
md, _, _ = probe(MUSIC)
assets.append(f'<asset id="m_music" name="In Motion (HD) - From the Soundtrack to _The Social Network_ 4" start="0s" duration="{round(md*48000)}/48000s" '
              f'hasAudio="1" audioSources="1" audioChannels="2" audioRate="48000"><media-rep kind="original-media" src="{url(MUSIC)}"/></asset>')
for key, s in (("s_ding", DING), ("s_pop", POP)):
    assets.append(f'<asset id="{key}" name="{s["name"]}" uid="{s["uid"]}" start="0s" duration="{s["dur"]}" hasAudio="1" audioSources="1" '
                  f'audioChannels="2" audioRate="{s["rate"]}"><media-rep kind="original-media" src="{url(s["src"])}"/></asset>')

# ---------------- connected items per spine element
children = [[] for _ in spine]
def parent_of(t):
    for i, ((o, d), it) in enumerate(zip(pos, spine)):
        if o - 1e-6 <= t < o + d - 1e-6: return i
    return len(spine) - 1
def local(i, t):
    o, _ = pos[i]; it = spine[i]
    base = it[1] if it[0] == "clip" else 3600.0
    return base + (t - o)

used_lanes = {}
def broll_clip(shot_id, t, dur, lane, enabled=True, role_name=""):
    s = pool[shot_id]; k = s["clip"]; st = s["in"]
    dur = min(dur, BDUR[k] - st - 0.05)
    i = parent_of(t)
    return i, (f'<asset-clip ref="{aid[k]}" lane="{lane}" offset="{r(local(i, t))}" name="{k} - {shot_id}{role_name}" '
                f'start="{r(st)}" duration="{r(dur)}"' + ('' if enabled else ' enabled="0"') +
                f' format="r1" tcFormat="NDF" audioRole="dialogue"><adjust-volume amount="-96dB"/></asset-clip>')

broll_log = []
for anchor, dur, pick, alts in BROLL:
    t = T(anchor)
    if t is None: raise SystemExit(f"anchor {anchor} not in cut")
    i, xml = broll_clip(pick, t, dur, 1); children[i].append((t, xml))
    for j, alt in enumerate(alts):
        i2, xml2 = broll_clip(alt, t, dur, 2 + j, enabled=False, role_name=" (alt)"); children[i2].append((t, xml2))
    broll_log.append((t, pick, alts))

def pop_clip(idx, t, until, xy, sc, lane):
    i = parent_of(t); L = local(i, t)
    dur = max(until - t, 0.3)
    k1, k2 = L + 4 / FPS, L + 8 / FPS
    fr = lambda v: f"{round(v * FPS) * 100}/6000s"
    # stills live at start 3600s in their own time; keyframes are in the still's local time
    s0 = 3600.0
    return i, (f'<video ref="c{idx}" lane="{lane}" offset="{r(L)}" name="{CHAT[idx][:-4]}" start="3600s" duration="{r(dur)}">'
               f'<adjust-transform position="{xy[0]} {xy[1]}" scale="{sc} {sc}">'
               f'<param name="scale"><keyframeAnimation>'
               f'<keyframe time="{fr(s0)}" value="{sc*0.35:.3f} {sc*0.35:.3f}"/>'
               f'<keyframe time="{fr(s0 + 4/FPS)}" value="{sc*1.08:.3f} {sc*1.08:.3f}"/>'
               f'<keyframe time="{fr(s0 + 8/FPS)}" value="{sc:.3f} {sc:.3f}"/>'
               f'</keyframeAnimation></param></adjust-transform></video>')

sfx_lane = [-2]
def sfx(key, t, start, dur, vol):
    i = parent_of(t); lane = sfx_lane[0]; sfx_lane[0] = -3 if lane == -2 else -2
    return i, (f'<asset-clip ref="{key}" lane="{lane}" offset="{r(local(i, t))}" name="{DING["name"] if key=="s_ding" else POP["name"]}" '
               f'start="{r(start)}" duration="{r(dur)}" format="fa" audioRole="dialogue"><adjust-volume amount="{vol}"/></asset-clip>')

pop_lane = {}
for n_, (anchor, idx, xy, sc, until) in enumerate(POPS):
    t = T(anchor); u = T(until)
    grp = str(until)
    pop_lane.setdefault(grp, 8); lane = pop_lane[grp]; pop_lane[grp] += 1
    i, xml = pop_clip(idx, t, u, xy, sc, lane); children[i].append((t, xml))
    i, xml = sfx("s_pop", t, 0.0, 0.40, "-14dB"); children[i].append((t, xml))
for a in DINGS:
    t = T(a); i, xml = sfx("s_ding", t, 0.21, 0.85, "-16dB"); children[i].append((t, xml))

# music: kick lands on the first payoff pop
kick_out = gap_time(0.0)
song_start = MUSIC_KICK - kick_out
assert song_start > 0
fr = lambda v: f"{round(v * 48000)}/48000s"
mk = [(song_start, "-11dB"), (song_start + 1.2, "-16dB"), (MUSIC_KICK - 0.25, "-16dB"), (MUSIC_KICK, "-8dB"),
      (MUSIC_KICK + POP_HOLD - 0.2, "-8dB"), (MUSIC_KICK + POP_HOLD + 0.3, "-16dB"),
      (song_start + TOTAL - 1.6, "-16dB"), (song_start + TOTAL, "-40dB")]
music = (f'<asset-clip ref="m_music" lane="-1" offset="{r(spine[0][1])}" name="In Motion (HD) - From the Soundtrack to _The Social Network_ 4" '
         f'start="{fr(song_start)}" duration="{r(TOTAL)}" format="fa" audioRole="music"><adjust-volume><param name="amount"><keyframeAnimation>' +
         "".join(f'<keyframe time="{fr(t)}" value="{v}"/>' for t, v in mk) + '</keyframeAnimation></param></adjust-volume></asset-clip>')
children[0].append((0.0, music))

# ---------------- Final Cut uids for re-imports
UIDS = json.load(open(f"{SCR}/uids.json")) if os.path.exists(f"{SCR}/uids.json") and os.environ.get("USE_UIDS") == "1" else {}
def add_uid(a):
    m = re.match(r'<asset id="([^"]+)" name="([^"]+)"( uid="[^"]+")?', a)
    if m and not m.group(3) and m.group(2) in UIDS:
        a = a.replace(f'name="{m.group(2)}"', f'name="{m.group(2)}" uid="{UIDS[m.group(2)]}"', 1)
    return a
assets = [add_uid(a) for a in assets]

# ---------------- spine xml
sp = []
for i, (it, (o, d)) in enumerate(zip(spine, pos)):
    kids = "".join(x for _, x in sorted(children[i], key=lambda z: z[0]))
    if it[0] == "clip":
        sp.append(f'<asset-clip ref="a_th" offset="{r(o)}" name="IMG_0078 - {it[3]}" start="{r(it[1])}" duration="{r(d)}" '
                  f'format="r1" tcFormat="NDF" audioRole="dialogue">{kids}</asset-clip>')
    else:
        sp.append(f'<gap offset="{r(o)}" name="Chat pops" start="3600s" duration="{r(d)}">{kids}</gap>')

# ---------------- event clips (all B-roll + screenshots) with keyword ranges
KW = {"laugh": "B-Roll - Laughing", "reaction": "B-Roll - Reactions", "screen": "B-Roll - Screens and Slides",
      "slide": "B-Roll - Screens and Slides", "chat": "B-Roll - Zoom Chat", "stu_teach": "B-Roll - Stu Teaching",
      "stu_tv": "B-Roll - Stu Teaching", "team": "B-Roll - Team", "build": "B-Roll - Team Building", "lab": "B-Roll - Lab Room",
      "debrief": "B-Roll - Debrief", "open": "B-Roll - Openers"}
kw_by_clip = {}
for s in pool.values():
    for tg in s["tags"]:
        if tg in KW: kw_by_clip.setdefault(s["clip"], []).append((s["in"], KW[tg]))
ev = []
for f in broll_files:
    k = f[:-4]; d = BDUR[k]; kws = ""
    for st, v in sorted(set(kw_by_clip.get(k, []))):
        kws += f'<keyword start="{r(st)}" duration="{r(min(2.5, d - st))}" value="{v}"/>'
    kws += f'<keyword start="0s" duration="{r(d)}" value="Creator Lab B-Roll"/>'
    ev.append(f'<asset-clip ref="{aid[k]}" name="{k}" duration="{round(d*600)}/600s" format="r1" tcFormat="NDF" audioRole="dialogue">{kws}</asset-clip>')
for i, f in enumerate(CHAT):
    ev.append(f'<asset-clip ref="c{i}" name="{f[:-4]}" duration="5s"><keyword start="0s" duration="5s" value="Creator Lab Chat"/></asset-clip>')

xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE fcpxml>
<fcpxml version="1.14">
<resources>
{chr(10).join(sorted(formats))}
{chr(10).join(assets)}
</resources>
<library location="file:///Volumes/4TBSSD_4/Babi%20NR%20Content/Libraries/TME.fcpbundle/" colorProcessing="wide-hdr">
<event name="Nov 12 Black Friday" uid="{EVENT_UID}">
{chr(10).join(ev) if os.environ.get("EVENT_CLIPS", "1") == "1" else ""}
<project name="{PROJECT}">
<sequence format="r1" duration="{r(TOTAL)}" tcStart="0s" tcFormat="NDF" audioLayout="stereo" audioRate="48k">
<spine>
{chr(10).join(sp)}
</spine>
</sequence>
</project>
</event>
</library>
</fcpxml>
'''
if os.environ.get("EVENT_CLIPS", "1") != "1":
    used = set(re.findall(r'ref="([^"]+)"', xml.split("<library")[1]))
    keep = [a for a in assets if re.match(r'<asset id="([^"]+)"', a).group(1) in used]
    xml = xml.replace(chr(10).join(assets), chr(10).join(keep))
os.makedirs(OUTDIR, exist_ok=True)
open(f"{OUTDIR}/Info.fcpxml", "w").write(xml)

prev = None
for it, (o, d) in zip(spine, pos):
    lab = it[3] if it[0] == "clip" else it[2]
    src = f"{it[1]:8.2f}-{it[2]:8.2f}" if it[0] == "clip" else "     (gap)       "
    print(f"{o:6.2f} {'' if lab != prev else '  ↳ '}{lab:15s} {src} {d:5.2f}s"); prev = lab
print(f"TOTAL {TOTAL:.2f}s | song starts at {song_start:.2f}s, kick at out {kick_out:.2f}s | broll events {len(BROLL)} | pops {len(POPS)}")
json.dump({"spine": spine, "pos": pos, "broll": broll_log, "total": TOTAL,
           "pops": [(T(a), CHAT[i]) for a, i, *_ in POPS]}, open(f"{SCR}/lab_plan.json", "w"))
