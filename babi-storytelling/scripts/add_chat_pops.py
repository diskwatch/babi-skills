"""Add a rapid chat-screenshot pop sequence to the user's edited Creator Lab Reel.
Input: the user's own FCPXML export. Everything else in their edit is left byte-for-byte as is;
we only add screenshot assets/formats, 11 still <video> clips (no animation) and synced pop SFX,
and rename the project so it imports as a copy next to theirs.
"""
import re, os, json
from fractions import Fraction as Fr

SRC = os.path.expanduser("~/Desktop/CLR user edit.fcpxmld/Info.fcpxml")
REF = os.path.expanduser("~/Desktop/CLR fcp export.fcpxmld/Info.fcpxml")   # has uids for the screenshots
OUT = os.path.expanduser("~/Desktop/Creator Lab Reel - chat pops.fcpxmld")
FPS = 60
START_F = 3 * FPS + 1                         # 0:00:03:01
POP_SRC_START = 0.997                         # transient of the chosen pop is at 0.999 s in the file
POP_DUR = 0.12
POP_VOL = "-14dB"

s = open(SRC).read()
ref = open(REF).read()
t = lambda x: Fr(x.rstrip("s"))

# --- the parent clip that holds 0:03:01 and where "once a month" begins
spine_clips = list(re.finditer(r'<asset-clip ref="(r\d+)" offset="([^"]+)" name="(IMG_0078[^"]*)" start="([^"]+)" duration="([^"]+)"[^>]*>', s))
oam = next(m for m in spine_clips if m.group(3) == "IMG_0078 - once a month")
END = t(oam.group(2))                          # pops all end here
parent = next(m for m in spine_clips if t(m.group(2)) <= Fr(START_F, FPS) < t(m.group(2)) + t(m.group(5)))
p_off, p_start = t(parent.group(2)), t(parent.group(4))
assert t(parent.group(2)) + t(parent.group(5)) == END, "pops must sit inside the clip right before 'once a month'"

# --- screenshot assets (reuse Final Cut's uids) + their formats
shots = ["3.36.55", "3.39.23", "3.37.34", "3.39.42", "3.36.33", "4.03.54", "3.40.35", "3.58.13", "4.03.15", "3.13.26", "4.14.55"]
res_add, ids = [], {}
fmt_ids = set(re.findall(r'<format id="([^"]+)"', s))
asset_ids = set(re.findall(r'<asset id="([^"]+)"', s))
for k, stamp in enumerate(shots):
    m = re.search(r'<asset id="([^"]+)" name="Screenshot 2026-11-10 at ' + re.escape(stamp) + r'[^"]*"[^>]*>.*?</asset>', ref, re.S)
    a = m.group(0); old_id = m.group(1)
    fmt = re.search(r'format="([^"]+)"', a).group(1)
    fdef = re.search(r'<format id="' + fmt + r'"[^>]*/>', ref).group(0)
    new_fmt, new_id = f"popfmt{k}", f"popimg{k}"
    assert new_fmt not in fmt_ids and new_id not in asset_ids
    res_add.append(fdef.replace(f'id="{fmt}"', f'id="{new_fmt}"'))
    res_add.append(re.sub(r'<bookmark>.*?</bookmark>', '', a.replace(f'id="{old_id}"', f'id="{new_id}"', 1).replace(f'format="{fmt}"', f'format="{new_fmt}"'), flags=re.S))
    ids[stamp] = (new_id, re.search(r'name="([^"]+)"', a).group(1))
s = s.replace("</resources>", "\n".join(res_add) + "\n</resources>", 1)

# pop sound asset already in the user's project
pop_ref = re.search(r'<asset id="(r\d+)" name="Censor sound', s).group(1)
pop_fmt = re.search(r'<asset-clip ref="' + pop_ref + r'"[^>]*format="([^"]+)"', s)
pop_fmt = pop_fmt.group(1) if pop_fmt else None

# --- timing: 6/7-frame rhythm from 0:03:01, one pop lands on the user's existing pop (no second sound there)
p_dur = t(parent.group(5))
existing = [p_off + (t(o) - p_start) for o in re.findall(r'<asset-clip ref="' + pop_ref + r'"[^>]*offset="([^"]+)"', s)
            if p_start <= t(o) < p_start + p_dur]
existing_f = {round(float(x) * FPS) for x in existing}
frames, f, step = [], START_F, [6, 7]
while f < END * FPS - 2 and len(frames) < len(shots):
    frames.append(f); f += step[len(frames) % 2]

# layout: scattered so every bubble stays readable as they pile up (x, y in % of frame height, scale)
layout = [(0, 34, .70), (-6, 21, .66), (7, 9, .62), (-4, -3, .70), (6, -15, .66), (-7, -27, .66),
          (5, -39, .62), (-9, 40, .55), (10, 27, .55), (-3, 15, .52), (2, -6, .42)]

fr = lambda sec: f"{round(sec * FPS) * 100}/6000s"
add, lane_v, lane_a = [], 2, -2
for k, f in enumerate(frames):
    t_out = Fr(f, FPS); stamp = shots[k]; rid, nm = ids[stamp]
    local = p_start + (t_out - p_off)
    dur = END - t_out
    x, y, sc = layout[k]
    add.append(f'<video ref="{rid}" lane="{lane_v}" offset="{fr(float(local))}" name="{nm}" start="3600s" duration="{fr(float(dur))}">'
               f'<adjust-transform position="{x} {y}" scale="{sc} {sc}"/></video>')
    lane_v += 1
    if f not in existing_f and (f - 1) not in existing_f and (f + 1) not in existing_f:
        add.append(f'<asset-clip ref="{pop_ref}" lane="{lane_a}" offset="{fr(float(local))}" name="Censor sound __ Funny sound __ Mouse click sound __ Pop sound __ Slap sound __ Short sound effect" '
                   f'start="{round(POP_SRC_START * 48000)}/48000s" duration="{round(POP_DUR * 48000)}/48000s"' + (f' format="{pop_fmt}"' if pop_fmt else '') +
                   f' audioRole="dialogue"><adjust-volume amount="{POP_VOL}"/></asset-clip>')
        lane_a = -3 if lane_a == -2 else -2

# insert right after the parent clip's opening tag (re-locate: resources were edited above)
pm = re.search(re.escape(parent.group(0)), s)
s = s[:pm.end()] + "".join(add) + s[pm.end():]
# import as a copy next to the user's project
s = re.sub(r'<project name="Creator Lab Reel"( uid="[^"]+")?( modDate="[^"]+")?', '<project name="Creator Lab Reel - chat pops"', s, count=1)
os.makedirs(OUT, exist_ok=True)
open(f"{OUT}/Info.fcpxml", "w").write(s)
print("parent:", parent.group(3), "out", float(p_off), "->", float(END))
print("pop frames:", [f"{x//FPS}:{x%FPS:02d}" for x in frames], "existing user pop frames:", sorted(existing_f))
