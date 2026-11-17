"""Render a project's dialogue from its exported spine and transcribe it -> timeline word times."""
import sys, json, subprocess, re, numpy as np
import xml.etree.ElementTree as ET
from fractions import Fraction as F
from faster_whisper import WhisperModel
xml_path, wav48, out = sys.argv[1:4]
def T(s): s = s.rstrip("s"); return F(s) if "/" not in s else F(*map(int, s.split("/")))
root = ET.parse(xml_path).getroot()
spine = root.find(".//spine")
pieces = [(T(c.get("offset")), T(c.get("start")), T(c.get("duration"))) for c in spine if c.tag == "asset-clip"]
filt = []
for i, (o, s, d) in enumerate(pieces):
    filt.append(f"[0:a]atrim={float(s):.6f}:{float(s + d):.6f},asetpts=PTS-STARTPTS[p{i}]")
filt.append("".join(f"[p{i}]" for i in range(len(pieces))) + f"concat=n={len(pieces)}:v=0:a=1,aresample=16000[o]")
x = subprocess.run(["ffmpeg", "-v", "error", "-i", wav48, "-filter_complex", ";".join(filt), "-map", "[o]", "-ac", "1",
                    "-f", "f32le", "-"], capture_output=True, check=True).stdout
a = np.frombuffer(x, np.float32)
print(f"rendered {len(a)/16000:.2f}s vs timeline {float(sum(p[2] for p in pieces)):.2f}s")
m = WhisperModel("medium.en", device="cpu", compute_type="int8")
segs, _ = m.transcribe(a, word_timestamps=True, condition_on_previous_text=False)
words = [dict(w=w.word.strip(), s=round(w.start, 3), e=round(w.end, 3), p=round(w.probability, 2)) for s in segs for w in s.words]
json.dump(words, open(out, "w"), indent=0)
print(" ".join(w["w"] for w in words))
