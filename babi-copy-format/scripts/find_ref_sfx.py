import librosa, numpy as np, glob, re, soundfile as sf
sr=22050
y,_=librosa.load("ref48.wav",sr=sr)
cuts=[2.48,6.15,10.85,15.07,19.2,24.1,28.0,32.15,35.9]
# align each burst on its onset, then average -> template (music averages out)
segs=[]
for t in cuts:
    segs.append(y[int((t-0.02)*sr):int((t+0.35)*sr)])
n=min(len(s) for s in segs); T=np.mean([s[:n] for s in segs],0); sf.write("sfx_template.wav",T,sr)
M=np.abs(librosa.stft(T,n_fft=1024,hop_length=128)); M=librosa.amplitude_to_db(M,ref=np.max)
print("template centroid",librosa.feature.spectral_centroid(y=T,sr=sr).mean(), "dur(-20dB)", (np.abs(T)>0.1*np.abs(T).max()).nonzero()[0][-1]/sr)
def mel(x): 
    m=librosa.power_to_db(librosa.feature.melspectrogram(y=x,sr=sr,n_mels=48,hop_length=128)); return m
Tm=mel(T); Tm=(Tm-Tm.mean())/Tm.std()
files=[f for f in glob.glob("/Volumes/4TBSSD_4/Babi NR Content/Songs/**/*.*",recursive=True) if re.search(r"(?i)sound|sfx|effect|whoosh|pop|click|ding|shutter|swoosh|camera",f) and re.search(r"(?i)\.(mp3|wav|m4a)$",f)]
res=[]
for f in files:
    try: x,_=librosa.load(f,sr=sr,duration=120)
    except Exception: continue
    X=mel(x); w=Tm.shape[1]; best=(-9,0)
    for i in range(0,X.shape[1]-w,2):
        s=X[:,i:i+w]; s=(s-s.mean())/(s.std()+1e-6); c=(s*Tm).mean()
        if c>best[0]: best=(c,i*128/sr)
    res.append((best[0],best[1],f.split("Songs/")[1]))
for r in sorted(res,reverse=True)[:12]: print(round(r[0],3), round(r[1],2), r[2])
