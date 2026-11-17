import sys, json, subprocess, numpy as np
sys.path.insert(0, sys.argv[0].rsplit('/', 1)[0])
from cutlib import load, thr_for, refine, split
wav16, plan, out, wav48 = sys.argv[1:5]
a, db = load(wav16); thr = thr_for(db)
lines = []
for label, ranges in json.load(open(plan)):
    pieces = []
    for r in ranges:
        s, e = r[0], r[1]; fl = r[2] if len(r) > 2 else ""
        rs, re_ = refine(db, thr, s, e)
        if "s" in fl: rs = s
        if "e" in fl: re_ = e
        pieces += split(db, thr, rs, re_)
    lines.append({"label": label, "pieces": pieces})
json.dump(lines, open(out, "w"), indent=1)
# render the cut audio for an ear check
filt = []; n = 0
for L in lines:
    for (s, e) in L["pieces"]:
        filt.append(f"[0:a]atrim={s}:{e},asetpts=PTS-STARTPTS[p{n}]"); n += 1
filt.append("".join(f"[p{i}]" for i in range(n)) + f"concat=n={n}:v=0:a=1[o]")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", wav48, "-filter_complex", ";".join(filt), "-map", "[o]", out.replace(".json", ".wav")], check=True)
tot = sum(e - s for L in lines for s, e in L["pieces"])
print(f"thr {thr:.1f} dB, {n} pieces, {tot:.1f}s")
for L in lines: print(L["label"][:40], [(round(s,2), round(e,2)) for s, e in L["pieces"]])
