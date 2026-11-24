import xml.etree.ElementTree as ET, json, re
from fractions import Fraction as F
import os; S=os.environ.get("WORK",".")
HEADER="What's the favorite part\nof your job?"
WORD_Y="0 -100"; HEAD_Y="0 368"
W=json.load(open(S+"/words.json"))
def t(s):
    s=s.rstrip("s"); return F(s) if "/" in s else F(int(s))
def fr(x):
    x=F(x); return f"{x.numerator}/{x.denominator}s" if x.denominator!=1 else f"{x.numerator}s"
g=lambda x: F(round(F(x)*60),60)
# manual fixes (whisper vs source transcript / energy)
FIX={}
for k in ["V1_02","V2_04","V3_05","V4_07"]: FIX[k]=[(0.30,0.80,"hi"),(1.82,2.15,"hey")]
FIX["V4_00_toe"]=True
def clean(w):
    w=w.lower().replace("-","").strip(" .,!?\"")
    return w
cnt=[0]
def mk(parent_lane,off,du,name,text,y,size):
    cnt[0]+=1; i=cnt[0]
    el=ET.Element("title",dict(ref="eT",lane=str(parent_lane),offset=fr(off),name=name,start="3600s",duration=fr(du)))
    for n,k,v in [("Position","9999/999166631/999166633/1/100/101",y),("Flatten","9999/999166631/999166633/2/351","1"),("Alignment","9999/999166631/999166633/2/354/999169573/401","1 (Center)")]:
        ET.SubElement(el,"param",dict(name=n,key=k,value=v))
    tx=ET.SubElement(el,"text"); ts=ET.SubElement(tx,"text-style",dict(ref=f"ts{i}")); ts.text=text
    d=ET.SubElement(el,"text-style-def",dict(id=f"ts{i}"))
    ET.SubElement(d,"text-style",dict(font="Helvetica Neue",fontSize=str(size),fontFace="Bold",fontColor="1 1 1 1",shadowColor="0 0 0 0.75",shadowOffset="4 315",shadowBlurRadius="8",alignment="center"))
    return el
tree=ET.parse(S+"/event.fcpxml"); root=tree.getroot()
res=root.find("resources")
ET.SubElement(res,"effect",dict(id="eT",name="Basic Title",uid=".../Titles.localized/Bumper:Opener.localized/Basic Title.localized/Basic Title.moti"))
# drop event-level browser clips (event already has them)
ev=root.find("library/event")
for ac in list(ev.findall("asset-clip")): ev.remove(ac)
report={}
for proj in ev.findall("project"):
    pn=proj.get("name"); tag=pn[-2:]
    spine=proj.find("sequence/spine"); clips=[c for c in spine if c.tag=="asset-clip"]
    # header span
    d0=float(t(clips[0].get("duration")))
    hend=min(max(d0,3.0),5.0)
    tl=F(0); log=[]
    for ci,ac in enumerate(clips):
        st=t(ac.get("start")); du=t(ac.get("duration")); k=f"{tag}_{ci:02d}"
        # header parts
        if tl<F(str(hend)):
            hs=tl; he=min(tl+du,g(hend))
            if he>hs: ac.append(mk(2,st,he-hs,"Header",HEADER,HEAD_Y,42)); log.append(("HEADER",float(hs),float(he)))
        words=[(a,b,clean(x)) for a,b,x in (FIX[k] if k in FIX else W[k])]
        if ci==0:  # skip the question words (covered by header)
            raw=[clean(x) for a,b,x in W[k]]
            if "job" in raw: words=words[raw.index("job")+1:]
        # manual word fixes
        words=[(a,b,("toe" if (k.startswith("V4_00") and w=="job" and a>2) else {"played":"play"}.get(w,w))) for a,b,w in words]
        words=[w for w in words if w[2]]
        fixed=[]
        for a,b,w in words:
            if fixed and a<fixed[-1][0]+0.09: a=fixed[-1][0]+0.09; b=max(b,a+0.1)
            fixed.append((a,b,w))
        words=fixed
        for i,(a,b,w) in enumerate(words):
            nxt=words[i+1][0] if i+1<len(words) else None
            end=(nxt if (nxt is not None and nxt-b<0.35) else b+0.15)
            s0=g(max(a,0)); e0=g(min(end,float(du)))
            if e0-s0<F(1,30): e0=min(s0+F(1,30),g(float(du)))
            if e0<=s0: continue
            ac.append(mk(1,st+s0,e0-s0,w,w,WORD_Y,40))
            log.append((w,float(tl+s0),float(tl+e0)))
        tl+=du
    report[pn]=log
# write
ET.indent(root,space="    ")
out=S+"/captioned.fcpxml"
open(out,"w",encoding="utf-8").write('<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE fcpxml>\n\n'+ET.tostring(root,encoding="unicode")+"\n")
json.dump(report,open(S+"/caption_report.json","w"))
print({k:len(v) for k,v in report.items()})
