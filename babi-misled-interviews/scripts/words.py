import numpy as np,json,glob,re
from faster_whisper import WhisperModel
import os; S=os.environ.get("WORK",".")
m=WhisperModel("medium.en",compute_type="int8")
out={}
for p in sorted(glob.glob(S+"/mix_*.npy")):
    a=np.load(p).astype(np.float32); k=p.split("mix_")[1][:-4]
    segs,_=m.transcribe(a,language="en",word_timestamps=True,vad_filter=True,condition_on_previous_text=False)
    out[k]=[(float(w.start),float(w.end),w.word.strip()) for s in segs for w in s.words]
    print(k,round(len(a)/16000,2)," ".join(w[2] for w in out[k]),flush=True)
json.dump(out,open(S+"/words.json","w"))
