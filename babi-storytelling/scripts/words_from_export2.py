"""Render a project's spine audio (any number of source assets) and transcribe -> timeline word times.
   python words_from_export2.py EXPORT.fcpxml OUT.json [--extra t0 t1 ...]"""
import sys, json, subprocess, urllib.parse as U, numpy as np
import xml.etree.ElementTree as ET
from fractions import Fraction as F
from faster_whisper import WhisperModel
xml_path, out = sys.argv[1:3]
def T(s): s = (s or "0s").rstrip("s"); return F(s) if "/" not in s else F(*map(int, s.split("/")))
root = ET.parse(xml_path).getroot()
src = {a.get("id"): U.unquote(a.find("media-rep").get("src")).replace("file://", "") for a in root.iter("asset")}
spine = root.find(".//project//spine")
pieces = [(T(c.get("offset")), T(c.get("start")), T(c.get("duration")), c.get("ref")) for c in spine if c.tag == "asset-clip"]
files = sorted(set(p[3] for p in pieces)); idx = {r: i for i, r in enumerate(files)}
args = ["ffmpeg", "-v", "error"]
for r in files: args += ["-i", src[r]]
filt = [f"[{idx[r]}:a]atrim={float(s):.6f}:{float(s + d):.6f},asetpts=PTS-STARTPTS,aformat=sample_rates=48000:channel_layouts=stereo[p{i}]"
        for i, (o, s, d, r) in enumerate(pieces)]
filt.append("".join(f"[p{i}]" for i in range(len(pieces))) + f"concat=n={len(pieces)}:v=0:a=1,aresample=16000[o]")
x = subprocess.run(args + ["-filter_complex", ";".join(filt), "-map", "[o]", "-ac", "1", "-f", "f32le", "-"],
                   capture_output=True, check=True).stdout
a = np.frombuffer(x, np.float32)
np.save(out.replace(".json", ".npy"), a)
print(f"rendered {len(a)/16000:.2f}s vs timeline {float(sum(p[2] for p in pieces)):.2f}s")
m = WhisperModel("medium.en", device="cpu", compute_type="int8")
segs, _ = m.transcribe(a, word_timestamps=True, condition_on_previous_text=False)
words = [dict(w=w.word.strip(), s=round(w.start, 3), e=round(w.end, 3), p=round(w.probability, 2)) for s in segs for w in s.words]
json.dump(words, open(out, "w"), indent=0)
print(" ".join(w["w"] for w in words))
