#!/usr/bin/env python3
"""Rebuild the Edits project "would you slap your boss for..." in the copied format.

- Keeps Babi's slap loop (IMG_0507 12.983-14.217 s, 74/60 s) and repeats it once per price.
- Adds one quoted caption per loop on a free overlay track, changing exactly on each cut.
Usage: python3 build_slap_edits.py [--write]   (Edits must be quit before --write)
"""
import json, sqlite3, sys, uuid, copy, shutil, time, os

LIB = os.path.expanduser("~/Movies/Edits/Libraries/59436377384.bsledits")
PID = "32830BD3-4A29-4CA2-BA74-346B18A5A627"
DB = f"{LIB}/Projects/{PID}/Timeline.db"
LADDER = ["$1 billion", "$100 million", "$10 million", "$1 million", "$500,000",
          "$100,000", "$10,000", "$1,000", "$100", "$10", "$1"]
LOOP = 74            # 60ths of a second (Babi's loop, 1.233 s)
FONT, SIZE = "IGUIBetav9-Heavy", 20   # Babi's own office reel ("mfs will go to work only to do this")
POS = [0.0, 40.0]    # px from frame centre; reference caption centre sits at y ~1000 of 1920

def U(): return str(uuid.uuid4()).upper()
def t(v, ts): return {"value": v, "timescale": ts, "flags": 1, "epoch": 0}

con = sqlite3.connect(DB)
row = con.execute("select rowid, composition_data from timelines").fetchone()
d = json.loads(row[1])
json.dump(d, open(os.path.join(os.path.dirname(__file__), "timeline_before.json"), "w"))

main = d["tracks"][0]
tmpl = main["elements"][0]
main["elements"] = []
for i in range(len(LADDER)):
    e = copy.deepcopy(tmpl)
    e["id"] = U()
    e["startTime"] = {"timescale": 60, "flags": 1, "epoch": 0, "value": i * LOOP}
    main["elements"].append(e)

style = {"lineHeightMultiplier": 1, "textColor": {"red": 1, "green": 1, "blue": 1, "alpha": 1},
         "letterSpacing": 0, "alignment": "center", "strokeWidth": 0, "isBold": False,
         "isItalic": False, "fontSize": SIZE, "fontFamily": FONT}
xf = {"rotation": 0, "scale": [1, 1], "isFlippedHorizontally": False, "anchorPoint": [0.5, 0.5],
      "isFlippedVertically": False, "position": POS}
texts = []
for i, price in enumerate(LADDER):
    dur = t(LOOP * 10, 600)          # 74/60 s == 740/600 s
    texts.append({
        "inPoint": t(0, 600), "outPoint": dur, "isReversed": False,
        "content": {"text": {"_0": {"effectTypeRaw": "text_soft_shadow",
                                    "text": f"“Would you slap\nyour boss for {price}?”",
                                    "transform": copy.deepcopy(xf), "style": copy.deepcopy(style),
                                    "animationTypeRaw": "none"}}},
        "opacity": 1, "duration": dur, "fullDuration": dur, "effects": [], "isMuted": False,
        "speed": 1, "id": U(), "volume": 1, "transform": copy.deepcopy(xf), "isDisabled": False,
        "startTime": t(i * LOOP * 10, 600)})

d["tracks"] = [main] + [tr for tr in d["tracks"][1:] if tr.get("trackType") != "overlay"] + [{
    "transitions": [], "timelineBehavior": "free",
    "state": {"volume": 1, "isLocked": False, "isMuted": False, "isVisible": True,
              "isSolo": False, "isExpanded": False},
    "trackType": "overlay", "elements": texts, "id": U()}]

out = json.dumps(d)
print(f"{len(main['elements'])} loops, {len(texts)} captions, {len(LADDER)*LOOP/60:.2f} s")
if "--write" in sys.argv:
    bak = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"edits_backup-{time.strftime('%Y%m%d-%H%M%S')}")
    shutil.copytree(os.path.dirname(DB), bak)
    con.execute("update timelines set composition_data=? where rowid=?", (out.encode("utf-8"), row[0]))
    con.commit()
    con.execute("pragma wal_checkpoint(TRUNCATE)")
    print("written; backup at", bak)
