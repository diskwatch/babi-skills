import sys,json
from faster_whisper import WhisperModel
m=WhisperModel("small.en",compute_type="int8")
for c in sys.argv[2:]:
    segs,_=m.transcribe(f"{sys.argv[1]}/wav/{c}.wav",word_timestamps=True,vad_filter=True)
    out=[]
    with open(f"{sys.argv[1]}/{c}.txt","w") as t:
        for s in segs:
            out.append({"s":s.start,"e":s.end,"t":s.text,"w":[(w.start,w.end,w.word) for w in s.words]})
            t.write(f"[{s.start:7.2f}-{s.end:7.2f}] {s.text.strip()}\n")
    json.dump(out,open(f"{sys.argv[1]}/{c}.json","w"))
    print(c,"done",flush=True)
