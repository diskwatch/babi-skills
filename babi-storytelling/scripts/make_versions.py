import re, os
from fractions import Fraction as Fr
XD="/Volumes/4TBSSD_4/Babi NR Content/Media/OFFICE/Nov 12 Black Friday/XML"
base=open(f"{XD}/CLR user v3.fcpxmld/Info.fcpxml").read()
t=lambda x: Fr(x.rstrip('s')) if x else Fr(0)
def ft(f):
    f=Fr(f).limit_denominator(720000); return f"{f.numerator}/{f.denominator}s" if f.denominator!=1 else f"{f.numerator}s"

def elements(s):
    """top-level spine children as (start_idx, end_idx, attrs dict)"""
    i=s.find('<spine>',s.find('<project'))+7
    out=[];depth=0;cur=None
    for m in re.finditer(r'<(/?)(asset-clip|clip|gap|video|title|spine|ref-clip|audition)\b([^>]*?)(/?)>',s[i:]):
        c,tag,a,sc=m.groups()
        if c:
            depth-=1
            if depth==0: out.append((cur[0], i+m.end(), cur[1])); 
            continue
        if depth==0:
            g=lambda k:(re.search(' '+k+r'="([^"]+)"',a) or [None,None])[1]
            cur=(i+m.start(), dict(off=t(g('offset')),dur=t(g('duration')),start=t(g('start')),name=g('name')))
            if sc: out.append((cur[0], i+m.end(), cur[1])); continue
        if not sc: depth+=1
        if tag=='spine' and depth==0: break
    return out

def make(name, cut_ranges=(), drop_children=(), trim_children_to_parent_end=()):
    s=base
    # drop specific connected clips by (name, start) identity
    for frag in drop_children:   # exact attribute fragment that identifies one connected clip
        k=s.find(frag); assert k>0 and s.count(frag)==1, frag
        a=s.rfind('<',0,k); tag=re.match(r'<([\w-]+)',s[a:]).group(1)
        e=s.find('>',k)
        if s[e-1]=='/': b=e+1
        else: b=s.find(f'</{tag}>',e)+len(f'</{tag}>')
        s=s[:a]+s[b:]
    els=elements(s)
    removed=Fr(0); pieces=[]; last=els[0][0]; head=s[:els[0][0]]
    body=""
    for (a,b,d) in els:
        seg=s[a:b]
        if any(lo<=float(d['off'])<hi for lo,hi in cut_ranges):
            removed+=d['dur']; continue
        if removed:
            seg=seg.replace(f'offset="{re.search(r"offset=\"([^\"]+)\"",seg).group(1)}"', f'offset="{ft(d["off"]-removed)}"',1)
        # trim named connected clips so they end at this parent's end
        for nm in trim_children_to_parent_end:
            for m in re.finditer(r'<(asset-clip|video)\b([^>]*name="'+re.escape(nm)+r'"[^>]*)>',seg):
                a2=m.group(2); off=t(re.search(r'offset="([^"]+)"',a2).group(1)); du=t(re.search(r'duration="([^"]+)"',a2).group(1))
                pend=d['start']+d['dur']
                if off+du>pend:
                    seg=seg.replace(m.group(0), m.group(0).replace(f'duration="{re.search(r"duration=\"([^\"]+)\"",a2).group(1)}"', f'duration="{ft(pend-off)}"',1),1)
        body+=seg
    tail=s[els[-1][1]:]
    s=head+body+tail
    # new total = end of last spine clip
    els=elements(s); total=els[-1][2]['off']+els[-1][2]['dur']
    s=re.sub(r'(<sequence [^>]*duration=")[^"]+',lambda m:m.group(1)+ft(total),s,count=1)
    # music (lane -1 child of first clip, the song) trimmed to total
    m=re.search(r'<asset-clip ref="[^"]+" lane="-1" offset="([^"]+)" name="Every Living[^"]*" start="[^"]+" duration="([^"]+)"',s)
    s=s.replace(m.group(0), m.group(0).replace(f'duration="{m.group(2)}"', f'duration="{ft(total - (t(m.group(1)) - els[0][2]["start"]))}"'),1)
    s=re.sub(r'<project name="[^"]+"( uid="[^"]+")?( modDate="[^"]+")?', f'<project name="{name}"', s, count=1)
    out=f"{XD}/{name}.fcpxmld"; os.makedirs(out,exist_ok=True); open(f"{out}/Info.fcpxml","w").write(s)
    print(name, "removed", float(removed), "total", float(total))

make("Creator Lab Reel V1")
make("Creator Lab Reel V2", cut_ranges=[(47.9,51.3)], trim_children_to_parent_end=["ChatGPT logo","Claude logo","IMG_9900"])
make("Creator Lab Reel V3", cut_ranges=[(53.19,53.21)],
     drop_children=['offset="2197/3s" name="Screenshot 2026-11-10 at 3.37.58',
                    'offset="4394000/6000s" name="IMG_9895"',
                    'offset="35152000/48000s" name="Censor'])
