"""Laughter finder. Runs Apple SoundAnalysis (shared/tools/sound_classify.swift, built as ./sa) on each clip's
audio and prints laugh windows (laughter/giggling/chuckle/snicker >= THRESH), merged into runs.

  python find_laughs.py SA_BINARY WAV48_DIR [THRESH=30]     (WAV48_DIR holds <clip>_48.wav, 48 kHz mono)
Strength = peak score; runs with peak >= 60 were the real room laughs on Nov 17 (commute joke 413 s = 95).
"""
import sys, re, glob, os, subprocess
sa, d = sys.argv[1], sys.argv[2]; th = int(sys.argv[3]) if len(sys.argv) > 3 else 30
for w in sorted(glob.glob(f"{d}/*_48.wav")):
    out = subprocess.check_output([sa, w], text=True)
    hits = []
    for line in out.splitlines():
        t, rest = line.split(" ", 1)
        v = [int(x) for n, x in re.findall(r"([a-z_]+) (\d+)", rest) if re.search("laugh|giggl|chuckl|snicker", n)]
        if v and max(v) >= th: hits.append((float(t), max(v)))
    runs = []
    for t, v in hits:
        if runs and t - runs[-1][1] <= 1.5: runs[-1] = [runs[-1][0], t, max(runs[-1][2], v)]
        else: runs.append([t, t, v])
    print(f"== {os.path.basename(w)[:-7]}")
    for a, b, v in runs: print(f"  {a:7.1f}-{b + 1:7.1f}s  peak {v}{'  <-- big' if v >= 60 else ''}")
