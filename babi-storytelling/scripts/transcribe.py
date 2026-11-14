"""Word-level transcript of one or more clips.

Usage (inside a venv with faster-whisper):  python transcribe.py OUT_DIR clip1.MOV [clip2.MOV ...]
Writes OUT_DIR/<name>.wav (16 kHz mono), <name>.txt (readable lines) and <name>.json (segments + words).
Uses medium.en (small.en garbles mumbled lines). The audio is passed as a numpy array because
PyAV 1.2.1 breaks faster-whisper's own file loader ("unexpected keyword metadata_errors").
"""
import sys, os, json, wave, subprocess
import numpy as np
from faster_whisper import WhisperModel

out_dir = sys.argv[1]; os.makedirs(out_dir, exist_ok=True)
model = WhisperModel(os.environ.get("WHISPER_MODEL", "medium.en"), device="cpu", compute_type="int8")
for clip in sys.argv[2:]:
    name = os.path.splitext(os.path.basename(clip))[0]
    wav = f"{out_dir}/{name}.wav"
    if not os.path.exists(wav):
        subprocess.run(["ffmpeg", "-nostats", "-loglevel", "error", "-y", "-i", clip, "-vn", "-ac", "1", "-ar", "16000", wav], check=True)
    audio = np.frombuffer(wave.open(wav).readframes(10**9), dtype=np.int16).astype(np.float32) / 32768
    segs, _ = model.transcribe(audio, word_timestamps=True, vad_filter=False, condition_on_previous_text=False)
    out = []
    with open(f"{out_dir}/{name}.txt", "w") as t:
        for s in segs:
            out.append({"start": s.start, "end": s.end, "text": s.text, "words": [[w.start, w.end, w.word] for w in s.words]})
            t.write(f"[{s.start:7.2f}-{s.end:7.2f}] {s.text.strip()}\n")
    json.dump(out, open(f"{out_dir}/{name}.json", "w"))
    print("done", name, flush=True)
