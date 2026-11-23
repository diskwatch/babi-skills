"""Shake Hands With V3-V10 (2026-11-23), all built from Babi's V2 ("Shake Hands With V2", 100.8 s, read from the library DB).
Rounds stay in chain order. (in, out) are source seconds."""
def seg(a, d): return (round(a, 3), round(a + d, 3))
# Babi's V2, round by round (in, dur)
V2 = [
 ("Claude abuser","IMG_0529",[(8.95,3.0),(22.0,0.517),(32.483,0.7),(33.733,1.017)]),
 ("Emergency contact","IMG_0531",[(11.95,3.067),(24.0,0.933),(25.467,1.883)]),
 ("47 Chrome tabs","IMG_0532",[(6.35,2.517),(9.45,1.783),(23.3,1.55),(25.467,0.433)]),
 ("Best snacks","IMG_0533",[(12.95,3.95),(21.067,1.083),(40.533,0.717),(43.3,0.8)]),
 ("Office celebrity","IMG_0533",[(57.75,3.783)]),
 ("Call at 2am","IMG_0533",[(75.1,3.25),(83.15,1.15),(84.7,0.45),(88.45,1.55)]),
 ("Smartest","IMG_0533",[(110.1,5.95),(122.7,4.4),(131.2,2.2)]),
 ("Not PR trained","IMG_0533",[(149.3,3.8),(172.0,1.0),(181.6,2.0)]),
 ("Funniest","IMG_0533",[(208.7,3.1),(213.15,1.05),(221.65,1.45),(225.4,2.75)]),
 ("Goes to for help","IMG_0533",[(239.767,3.733),(251.5,2.217)]),
 ("Lie for you","IMG_0533",[(261.65,4.433),(273.55,2.25)]),
 ("Best dressed","IMG_0533",[(288.85,3.2),(293.35,3.65),(298.0,4.133),(304.1,1.65)]),
 ("Deserves a raise","IMG_0533",[(314.5,1.8),(320.45,4.2),(326.0,1.15),(333.8,1.567)]),
 ("Office yapper","IMG_0533",[(353.15,2.3),(357.0,2.683)]),
]
BASE = [(n, c, [seg(a, d) for a, d in s]) for n, c, s in V2]
# FAST: V2 plus jump cuts on mid-sentence pauses (10 ms RMS), shorter silent holds, "it says" and the ASMR aside dropped
FASTR = {
 "47 Chrome tabs":   [(6.35,8.867),(9.45,11.233),(23.3,24.3),(25.467,25.9)],
 "Smartest":         [(110.45,116.05),(122.7,127.1),(131.2,132.6)],
 "Funniest":         [(208.7,211.8),(213.15,214.2),(221.65,223.1),(225.9,228.15)],
 "Goes to for help": [(239.767,242.4),(242.75,243.5),(251.5,253.717)],
 "Lie for you":      [(261.65,263.72),(264.0,265.75),(273.55,275.8)],
 "Deserves a raise": [(320.45,321.93),(322.22,324.65),(326.0,327.15),(333.8,334.8)],
}
FAST = [(n, c, FASTR.get(n, s)) for n, c, s in BASE]
def frm(rounds, name):
    i = [r[0] for r in rounds].index(name); out = rounds[i:]
    if name == "Smartest":   # open on the card, not "it says"
        out = [(out[0][0], out[0][1], [(110.45, out[0][2][0][1])] + out[0][2][1:])] + out[1:]
    return out
# cold open teaser: the funniest-person payoff, then the chain from round 1
TEASER = [("Teaser", "IMG_0533", [(209.1,211.7),(213.05,214.2)])]
VARIANTS = {
 "Shake Hands With V3":  FAST,                        # full chain, faster cut (~95 s)
 "Shake Hands With V4":  TEASER + BASE,               # full chain, V2 pacing, cold open "funniest / I think I just did"
 "Shake Hands With V5":  frm(BASE, "Best snacks"),    # starts at round 4 (snacks -> Rick's fruit bowl)
 "Shake Hands With V6":  frm(FAST, "Best snacks"),    # round 4, faster cut
 "Shake Hands With V7":  frm(BASE, "Call at 2am"),    # starts at round 6
 "Shake Hands With V8":  frm(BASE, "Smartest"),       # starts at round 7 (Andrew's busy)
 "Shake Hands With V9":  frm(FAST, "Smartest"),       # round 7, faster cut
 "Shake Hands With V10": frm(BASE, "Funniest"),       # starts at round 9 ("I think I just did")
}
