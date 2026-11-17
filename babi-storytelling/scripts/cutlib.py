"""Tight-cut helper: refine line edges on 10 ms RMS and split internal pauses (babi-storytelling rules)."""
import wave, numpy as np
HOP = 0.01
def load(wav):
    w = wave.open(wav); a = np.frombuffer(w.readframes(10**9), dtype=np.int16).astype(np.float32) / 32768
    n = len(a) // 160
    rms = np.sqrt((a[:n*160].reshape(n, 160) ** 2).mean(1) + 1e-12)
    db = 20 * np.log10(rms)
    return a, db
def thr_for(db):
    floor = np.percentile(db, 15)
    peak = np.percentile(db, 97)
    return max(floor + 10, peak - 32)
def refine(db, thr, a, b, pre=0.03, post=0.07, look_back=0.15, look_fwd=0.30):
    """a,b = whisper start of first word / end of last word."""
    i0, i1 = int((a - look_back) / HOP), int((a + look_fwd) / HOP)
    loud = np.where(db[i0:i1] > thr)[0]
    s = (i0 + loud[0]) * HOP - pre if len(loud) else a
    j0, j1 = int((b - 0.35) / HOP), int((b + 0.15) / HOP)
    loud = np.where(db[j0:j1] > thr)[0]
    e = (j0 + loud[-1] + 1) * HOP + post if len(loud) else b
    return round(s, 3), round(e, 3)
def split(db, thr, s, e, min_gap=0.12, keep=0.035):
    """Split [s,e] at silent runs >= min_gap, keeping `keep` s of silence on each side."""
    i0, i1 = int(s / HOP), int(e / HOP)
    quiet = db[i0:i1] <= thr
    pieces, cur, k = [], s, 0
    while k < len(quiet):
        if quiet[k]:
            m = k
            while m < len(quiet) and quiet[m]: m += 1
            g0, g1 = (i0 + k) * HOP, (i0 + m) * HOP
            if g1 - g0 >= min_gap and g0 - cur > 0.05 and e - g1 > 0.05:
                pieces.append((round(cur, 3), round(g0 + keep, 3)))
                cur = round(g1 - keep, 3)
            k = m
        else: k += 1
    pieces.append((round(cur, 3), round(e, 3)))
    return pieces

_split = split
def split(db, thr, s, e, min_gap=0.12, keep=0.035, min_piece=0.15):
    """Same as before, but pieces shorter than min_piece are merged back into a neighbour."""
    p = _split(db, thr, s, e, min_gap, keep)
    out = []
    for a, b in p:
        if out and (b - a < min_piece or out[-1][1] - out[-1][0] < min_piece):
            out[-1] = (out[-1][0], b)
        else:
            out.append((a, b))
    return out
