"""Plan the story cut: lines (file, a, b) -> pause-split pieces on the 30 fps grid; render the cut audio for transcription."""
import sys, json, subprocess
sys.path.insert(0, "/Users/northresults/.claude/babi-skills/babi-storytelling/scripts")
import cutlib, numpy as np
from fractions import Fraction as F
# (id, file, a, b, text)   a/b are speech-run edges read from 10 ms RMS runs
LINES = [
 (1,  "0975", 49.07, 52.17, "Earlier this week, we brought a room full of people right here into our office"),
 (2,  "0976", 102.21, 105.40, "for context these are people who have been running their memberships for years"),
 (3,  "0976", 125.38, 129.22, "on this day we showed them something that nobody outside of our team has ever seen"),
 (4,  "0976", 140.35, 142.42, "honestly we had no idea how they'd react"),
 (5,  "0976", 153.12, 156.93, "since January our team has been rebuilding our entire platform"),
 (6,  "0976", 165.34, 167.51, "I'm not talking about adding a few features"),
 (7,  "0976", 177.14, 179.72, "I mean tearing it down and starting all over"),
 (8,  "0976", 197.95, 200.48, "until today it has never left these walls"),
 (9,  "0976", 217.05, 219.29, "Stu explain the whole thing in one line"),
 (10, "0976", 259.88, 264.55, "you're doing all the talking and the behind-the-scenes and Membership.io is doing all the building"),
 (11, "0976", 272.64, 275.26, "then Rick showed them what this actually looks like"),
 (12, "0976", 307.45, 311.41, "the night before this day Rick took one of our clients' existing free offers"),
 (14, "0976", 322.29, 326.30, "entire landing page, their email flow just by talking to it"),
 (15, "0976", 372.49, 375.75, "no clicking around, no dragging boxes, just a bit of yapping"),
 (16, "0976", 381.10, 386.23, "I could tell you how the room reacted but you don't need me, hear it from them"),
 (17, "0976", 408.83, 413.80, "I think it's safe to say keeping this quiet for almost a year, pretty worth it for these reactions"),
 (18, "0976", 488.36, 493.30, "if you think this is something you'd want to try using, we got a waitlist, so comment waitlist and we'll send you the link"),
]
PIN = {2: 102.3, 3: 125.48, 4: 140.44, 6: 165.46, 8: 197.95, 14: 322.48, 16: 381.84, 17: 409.14}
G = F(1, 30)
def snap(x): return F(round(F(str(x)) * 30), 30)
DB = {}
pieces = []
for lid, f, a, b, txt in LINES:
    if f not in DB:
        _, db = cutlib.load(f"tr/{f}.wav"); DB[f] = (db, cutlib.thr_for(db))
    db, thr = DB[f]
    s, e = a - 0.02, b + 0.05
    if lid in PIN:
        c = PIN[lid]; i0, i1 = int((c-0.12)/0.01), int((c+0.12)/0.01)
        sm = np.convolve(db[i0-1:i1+2], np.ones(3)/3, 'valid')
        s = (i0 + int(np.argmin(sm))) * 0.01 + 0.01
        s += {2: 0.07, 3: 0.20, 4: 0.133, 6: 0.07, 16: -0.03}.get(lid, 0)
        print('pin', lid, 'whisper', c, '-> dip', round(s,3), 'dB', round(float(sm.min()),1))
    parts = cutlib.split(db, thr, s, e, 0.12, 0.035) 
    for k, (ps, pe) in enumerate(parts):
        st = snap(ps); du = snap(pe) - st
        if du < F(2, 30): continue
        pieces.append(dict(line=lid, k=k, file=f, start=str(st), dur=str(du), text=txt))
# timeline offsets
off = F(0)
for p in pieces:
    p["off"] = str(off); off += F(p["dur"])
json.dump(pieces, open("pieces.json", "w"), indent=1)
print(len(pieces), "pieces, total", float(off))
for lid in sorted({p["line"] for p in pieces}):
    ps = [p for p in pieces if p["line"] == lid]
    print(lid, [round(float(F(p["dur"])), 2) for p in ps], "line starts", round(float(F(ps[0]["off"])), 2))
# render the cut audio (16 kHz) for transcription / loudness
fc = []; ins = []
for i, p in enumerate(pieces):
    st = float(F(p["start"])); du = float(F(p["dur"]))
    fc.append(f"[{0 if p['file']=='0975' else 1}:a]atrim=start={st}:duration={du},asetpts=PTS-STARTPTS[a{i}]")
fc.append("".join(f"[a{i}]" for i in range(len(pieces))) + f"concat=n={len(pieces)}:v=0:a=1[o]")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "tr/0975.wav", "-i", "tr/0976.wav", "-filter_complex", ";".join(fc), "-map", "[o]", "-ar", "16000", "-ac", "1", "tr/cut.wav"], check=True)
print("cut.wav rendered")
