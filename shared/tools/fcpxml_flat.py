import sys, re, xml.etree.ElementTree as ET
from fractions import Fraction as F
def t(s):
    if not s: return F(0)
    s=s.rstrip('s')
    if '/' in s: a,b=s.split('/'); return F(int(a),int(b))
    return F(s)
def load(path):
    root=ET.parse(path).getroot()
    assets={}
    for a in root.iter('asset'):
        mr=a.find('media-rep'); src=mr.get('src') if mr is not None else ''
        assets[a.get('id')]=(a.get('name'),src.split('/')[-1].replace('%20',' '))
    for m in root.iter('media'): assets[m.get('id')]=(m.get('name'),'COMPOUND')
    effects={e.get('id'):e.get('name') for e in root.iter('effect')}
    projs={}
    for p in root.iter('project'):
        projs[p.get('name')]=(p, assets, effects)
    return projs
KIND={'asset-clip','clip','title','video','audio','ref-clip','gap','sync-clip'}
def vol(el):
    v=el.find('adjust-volume')
    if v is None:
        ac=el.find('audio-channel-source')
        v=ac.find('adjust-volume') if ac is not None else None
    if v is None: return None
    kf=[k.get('value') for k in v.iter('keyframe')]
    return v.get('amount') or ('kf:'+','.join(kf) if kf else None)
def xf(el):
    x=el.find('adjust-transform')
    if x is None: return ''
    return 'pos=%s sc=%s'%(x.get('position'),x.get('scale'))
def text(el):
    return ''.join(el.itertext()).strip() if el.tag=='title' else ''
def walk(el, parent_abs, parent_start, lane, out, assets, effects, depth=0):
    for c in el:
        if c.tag not in KIND: continue
        off=t(c.get('offset')); start=t(c.get('start')); dur=t(c.get('duration'))
        absol=parent_abs+(off-parent_start)
        ln=int(c.get('lane')) if c.get('lane') else lane
        ref=c.get('ref')
        nm=c.get('name') or ''
        src=assets.get(ref,(None,''))[1] if ref else ''
        if c.tag=='title': src=effects.get(ref,'')
        # for clip wrapper with video child
        if c.tag=='clip' and not ref:
            v=c.find('video') or c.find('audio')
            if v is not None: src=assets.get(v.get('ref'),('',''))[1]
        pos=''
        if c.tag=='title':
            for prm in c.findall('param'):
                if prm.get('name')=='Position': pos=prm.get('value')
        tsd=c.find('.//text-style-def/text-style')
        sz=tsd.get('fontSize') if tsd is not None else ''
        out.append(dict(tag=c.tag,lane=ln,abs=float(absol),start=float(start),dur=float(dur),end=float(absol+dur),
            name=nm,src=src,en=c.get('enabled','1'),vol=vol(c),xf=xf(c),text=text(c),pos=pos,size=sz,depth=depth,
            retime=c.find('timeMap') is not None))
        # children connected relative to this clip: child offset in parent's source time
        walk(c, absol, start, ln if depth else 0, out, assets, effects, depth+1)
def flatten(proj, assets, effects):
    seq=proj.find('sequence'); spine=seq.find('spine'); out=[]
    walk(spine, F(0), F(0), 0, out, assets, effects)
    return out, float(t(seq.get('duration')))
if __name__=='__main__':
    for nm,(p,a,e) in load(sys.argv[1]).items():
        if len(sys.argv)>2 and sys.argv[2] not in nm: continue
        items,d=flatten(p,a,e); print('##',nm,'dur %.2f'%d)
        for i in items:
            print('%s L%-3s %-9s %7.2f-%7.2f src@%7.2f %-22s en=%s vol=%s %s %s %s'%('  '*i['depth'],i['lane'],i['tag'],i['abs'],i['end'],i['start'],(i['src'] or i['name'])[:22],i['en'],i['vol'],i['xf'],('T:'+i['text'][:30]+' p='+i['pos']+' s='+i['size']) if i['text'] else '','RT' if i['retime'] else ''))
