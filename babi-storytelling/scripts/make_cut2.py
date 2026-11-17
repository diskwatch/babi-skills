import sys, json, subprocess
sys.path.insert(0, sys.argv[0].rsplit('/', 1)[0])
from cutlib import load, thr_for, speech_thr, refine2, split
wav16, plan, out, wav48 = sys.argv[1:5]
a, db = load(wav16); thr_split = thr_for(db); thr = speech_thr(db)
lines = []
for label, ranges in json.load(open(plan)):
    pieces = []
    for r in ranges:
        s, e = r[0], r[1]; fl = r[2] if len(r) > 2 else ""
        rs, re_ = refine2(db, thr, s, e, "s" in fl, "e" in fl)
        pieces += split(db, thr_split, rs, re_, min_gap=0.12, keep=0.025)
    lines.append({"label": label, "pieces": pieces})
json.dump(lines, open(out, "w"), indent=1)
filt, n = [], 0
for L in lines:
    for (s, e) in L["pieces"]:
        filt.append(f"[0:a]atrim={s}:{e},asetpts=PTS-STARTPTS[p{n}]"); n += 1
filt.append("".join(f"[p{i}]" for i in range(n)) + f"concat=n={n}:v=0:a=1[o]")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", wav48, "-filter_complex", ";".join(filt), "-map", "[o]", out.replace(".json", ".wav")], check=True)
print(f"speech thr {thr:.1f} dB, {n} pieces, {sum(e - s for L in lines for s, e in L['pieces']):.2f}s")
