import subprocess, numpy as np, json, sys
D="/Volumes/4TBSSD_4/Babi NR Content/Media/OFFICE/November 18th Immersion Day"
W,H,FPS=144,256,15
clips=sys.argv[1].split(",")
out={}
def shift(a,b):
    A=np.fft.fft2(a); B=np.fft.fft2(b); R=A*np.conj(B); R/=np.abs(R)+1e-9
    r=np.fft.ifft2(R).real; y,x=np.unravel_index(np.argmax(r),r.shape)
    if y>H/2: y-=H
    if x>W/2: x-=W
    return x,y
win=np.outer(np.hanning(H),np.hanning(W))
for c in clips:
    raw=subprocess.run(["ffmpeg","-v","error","-i",f"{D}/{c}.MOV","-vf",f"fps={FPS},scale={W}:{H}","-f","rawvideo","-pix_fmt","gray","-"],capture_output=True).stdout
    n=len(raw)//(W*H); g=np.frombuffer(raw[:n*W*H],np.uint8).reshape(n,H,W).astype(np.float32)
    g=(g-g.mean(axis=(1,2),keepdims=True))*win
    s=np.array([shift(g[i],g[i-1]) for i in range(1,n)],float)   # px per frame at 144 wide
    sp=np.hypot(s[:,0],s[:,1])
    out[c]=sp.tolist()
    # per-second summary
    per=[round(float(np.mean(sp[i*FPS:(i+1)*FPS])),2) for i in range(int(len(sp)/FPS))]
    print(c, per, flush=True)
json.dump(out,open("shake_%s.json"%sys.argv[2],"w"))
