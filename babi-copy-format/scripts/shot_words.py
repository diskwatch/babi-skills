"""Per-shot word timings: transcribe [in-0.4, out+0.4] of each shot's source audio with medium.en, keep words centred inside the shot."""
import json, sys, wave, numpy as np
sys.path.insert(0, "."); from plan import P
from faster_whisper import WhisperModel
m = WhisperModel("medium.en", compute_type="int8")
PROMPT = "Shake hands with the office Claude abuser. Rick, Rickster, Stu, Alli, Andrew, Jess, Carly, Phil."
cache = {}; out = []
for name, c, segs in P:
    if c not in cache:
        w = wave.open(f"../foot/{c}.wav"); cache[c] = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    x = cache[c]
    for a, b in segs:
        a0 = max(0, a - 0.4); seg = x[int(a0*16000):int((b + 0.4)*16000)]
        ws, _ = m.transcribe(seg, word_timestamps=True, initial_prompt=PROMPT, condition_on_previous_text=False)
        got = [(a0 + w.start, a0 + w.end, w.word.strip()) for s_ in ws for w in s_.words]
        out.append([name, c, a, b, got])   # raw; the builder filters (overlap >= 0.12 s) and applies overrides
        print(f"{name:18s} {a:7.2f}: {' '.join(t for _,_,t in got)}")
json.dump(out, open("shot_words_raw.json", "w"))
