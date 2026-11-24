import xml.etree.ElementTree as ET, wave, numpy as np, json, re
from fractions import Fraction as F
import os; S=os.environ.get("WORK",".")
SR=16000
def t(s): 
    if s is None: return F(0)
    s=s.rstrip("s"); 
    return F(s) if "/" in s else F(int(s))
def load(n):
    w=wave.open(f"{S}/wav/{n}.wav"); return np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float32)/32768
src={n:load(n) for n in ["IMG_1188","IMG_1189","IMG_1190","IMG_1191"]}
root=ET.parse(S+"/event.fcpxml").getroot()
assets={a.get("id"):a.get("name") for a in root.iter("asset")}
def seg(name,a,b):
    a=float(a);b=float(b); x=src[name][int(round(a*SR)):int(round(b*SR))]
    return x
def gain(kfs,tt,const):
    if not kfs: return np.full_like(tt,10**(const/20))
    ts=np.array([float(k[0]) for k in kfs]);ds=np.array([k[1] for k in kfs])
    return 10**(np.interp(tt,ts,ds)/20)
pieces={}
for proj in root.iter("project"):
    pn=proj.get("name"); plist=[]
    for ac in proj.find("sequence/spine"):
        if ac.tag!="asset-clip": print("SKIP",ac.tag); continue
        name=assets[ac.get("ref")]; st=t(ac.get("start")); du=t(ac.get("duration"))
        x=seg(name,st,st+du); tt=np.arange(len(x))/SR+float(st)
        kfs=[];const=0
        av=ac.find("adjust-volume")
        if av is not None:
            if av.get("amount"): const=float(av.get("amount").replace("dB",""))
            for k in av.iter("keyframe"): kfs.append((t(k.get("time")),float(k.get("value").replace("dB",""))))
        x=x*gain(kfs,tt,const)
        for c in ac.findall("clip"):
            off=t(c.get("offset"));cs=t(c.get("start"));cd=t(c.get("duration"))
            y=seg("IMG_1191",cs,cs+cd)
            i0=int(round(float(off-st)*SR)); n=min(len(y),len(x)-i0)
            if i0<0: raise SystemExit("neg")
            x[i0:i0+n]+=y[:n]
        plist.append(dict(name=name,start=str(st),dur=str(du),n=len(x)))
        np.save(f"{S}/mix_{pn[-2:]}_{len(plist)-1:02d}.npy",x)
    pieces[pn]=plist
json.dump(pieces,open(S+"/pieces.json","w"),indent=1)
print({k:len(v) for k,v in pieces.items()})
