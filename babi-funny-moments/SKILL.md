---
name: babi-funny-moments
description: Ariel ("Babi") playbook for pulling funny moments out of long raw footage (office meetings, team days, events, BTS shot on the Sony camera) into a Final Cut selects timeline he can refine. Covers ingesting a Sony SD card onto a North Results SSD (and setting up a fresh SSD with the "Babi NR Content" folders + ORGANIZER.md), transcribing everything, finding real room laughs with Apple SoundAnalysis, choosing and trimming the moments, and building an FCPXML where EVERY source clip is imported into the event first and the project holds one clip per moment (name, note, marker). Use for "pull the funny moments", "find the funny bits from today", "what were the funniest things people said", "blooper/funny reel from the meeting". For cutting the final funny reel in ez.romo style use babi-ezromo-style; for storytelling recaps use babi-storytelling.
---

# Babi funny moments (selects from long footage)

**Read `~/.claude/babi-skills/shared/SETTINGS.md` first** (Rec. 709, safe zone, Final Cut import gotchas). Living document: after each correction from Babi, add the lesson with numbers, a changelog line, then commit and push.

## Babi's brief (2026-11-17)
- "Look through the footage from today and pull any funny moments of people saying funny things."
- **Edit in Final Cut** (not Edits) and **import everything before you edit**, so he can refine later (find alternates with Shift-F, browse the full clips).
- Output is a **selects project**, not a finished reel: one clip per moment, in shooting order, each named and noted. No music, captions or SFX unless asked.

## 1. Drives and folders
- **SD card** (Sony, mounts as "Untitled"): clips in `PRIVATE/M4ROOT/CLIP/C####.MP4` + `C####M01.XML` sidecars. "Today's footage" = files whose mtime is today (`ls -lT`); the card also holds older days.
- **NR SSD layout** (same as `/Volumes/4TBSSD_4/Babi NR Content/`). On a fresh drive create it and drop `ORGANIZER.md` at the root:
  ```
  Babi NR Content/
    Media/4k Media/<Mon>/<Mon D Title>/   Sony card footage (+ M01.XML sidecars, XML/ subfolder for our files)
    Media/OFFICE/<Mon D Topic>/            office / iPhone footage
    Media/TRAVEL/<Trip>/
    Exports/OFFICE/   Exports/PERSONAL/
    Libraries/                             Final Cut libraries
    Songs/{STORYTELLING,HAPPY EDIT,SOUND FX,new}   Sound FX/   Photos/
  ```
  First used on the 2 TB SanDisk "Extreme SSD" (2026-11-17): library `Libraries/NR Content.fcpbundle`.
- **Ingest:** copy today's clips first with `cp -p` then `cmp` each one, so work can start; copy the older days in the background into `4k Media/<Mon>/<Mon D>/` (one folder per mtime date). Never wipe the card. Rename the dated folder once you know what it is ("Nov 17 Office Meeting").

## 2. Probe — and the Sony rotation trap
- Sony FX/ZV clips: 3840×2160 H.264 29.97, PCM stereo, a data stream (use `-map 0:a:0`), gamma `s-cinetone` (standard Rec. 709, no LUT needed).
- **Check rotation on every clip:** `ffprobe -show_entries stream_side_data=rotation`. On Nov 17, C4691/C4692 carried `rotation=-90` although the picture was a normal horizontal shot (the camera's tilt sensor tagged it). Final Cut showed them as a sideways vertical frame pillarboxed in the 16:9 project.
  - Fix losslessly before importing: `ffmpeg -display_rotation 0 -i C4692.MP4 -map 0:v:0 -map 0:a:0 -c copy C4692_upright.MP4` (ffmpeg 7+). Move the camera originals into `Camera originals (wrong rotation tag)/` and give the fixed copy the original name.
  - Check with `ffmpeg -noautorotate` frame grabs which way is really up before "fixing" anything.

## 3. Find the moments
1. **Transcribe everything** (`scripts/transcribe.py`, faster-whisper small.en, word timings, VAD). Read all of it.
2. **Find the laughs** — the best signal for "funny": build `shared/tools/sound_classify.swift` as `sa`, make 48 kHz mono wavs, run `scripts/find_laughs.py sa <wavdir>`. Peaks ≥ 60 are real room laughs; 30–50 is a chuckle. On Nov 17 the commute joke peaked at 95 (413 s) and was clearly the best moment.
3. **Re-transcribe each laugh window with medium.en** (±15 s) to get the actual line: small.en merged/garbled lines in crosstalk.
4. **Look at frames** (`ffmpeg -ss … -vf fps=1/3,scale=400:-2,tile=4x2`; this ffmpeg has no drawtext) to confirm people are laughing on camera.
5. **What counts:** a line that gets a room laugh; a slip ("a day before… or a day or a month, I'm sorry"); a roast/joke at someone ("we gotta get you a longer drive"); deadpan one-liners ("party tricks all day long", "Bob's your uncle"). Skip pure plan/strategy talk even if it's clever.
6. **Each moment = setup + line + the laugh until it dies.** Start at the setup sentence, not mid-thought. If two moments overlap or the laugh runs into the next bit, merge them into one clip (commute joke + "you only have five minutes… two really" became one 30 s clip).
7. **Flag names:** if a moment names a client or a person who isn't in the room (Kelsey's "30-page life document", Lisa), say so in the clip note and in your report — Babi decides whether it can be posted.

## 4. Build in Final Cut — import everything first
- `scripts/build_funny_moments.py moments.json OUT.fcpxml` (copy it and the json into the shoot's `XML/` folder):
  - Event-level `<asset-clip>` for **every** source clip (so all footage is in the browser), then a project "<Mon D> Funny Moments" with one clip per moment named "NN label", a `<note>` with the full line, and a marker at its start.
  - 4K 29.97 project, `colorSpace="1-1-1 (Rec. 709)"`. Times snapped to the 1001/30000 grid.
  - Edges: in walks back ≤0.4 s to the quiet gap before speech (−0.1 s); out runs until the room is quiet again (≤ +2 s, keeps the laugh) + 0.15 s. In a noisy room the out often hits the +2 s cap; that's fine for selects.
- Validate with the DTD (shared/SETTINGS.md), then `open -a "Final Cut Pro Creator Studio" file.fcpxml` → New… → name the library, cmd+shift+G to `…/Babi NR Content/Libraries`, Save.
- **Final Cut COPIES the media on XML import** into `Libraries/Final Cut Original Media/<date>/` (it did on Nov 17, 8.6 GB). Babi wants the media left in place, so afterwards: select the event in the sidebar → File › Relink Files › Original Media… → **All** → Locate All → the shoot folder → Choose → Relink Files. Check the event's symlinks (`find <bundle>/<event> -type l`) point at `Media/4k Media/…`, then delete `Libraries/Final Cut Original Media`. Relink only covers what's selected: with one browser clip selected it listed 1 file — select the event.
- A library must keep at least one event: to redo an import into a library you just made, close the library (File › Close Library) and delete the bundle, then import again with New….
- Open the project, Shift-Z, screenshot to check: every clip upright and full-frame, names/markers visible.

## The reel: "Posting moments from the office w/o context" (Babi, 2026-11-17)
After the selects, Babi gave two references (Membership.io's own series: DfQiRczRI7m "Day 1…", 18.6 s; DfsArX5O_1e "…pt. 2", 37 s; saved in the shoot's `Reference/`): **"much quicker cuts, and the funny zoom-ins on hands and stuff."** The selects' 5–30 s moments were far too long for this.
- **Measured:** ref 1 = 26 shots in 18.6 s (median **0.7 s**), ref 2 ≈ 1–1.5 s with whip pans. Detect cuts by frame-to-frame **correlation < 0.7 on the middle band only** (`scene` misses punch-ins; plain frame-diff fires on handheld motion).
- **Layout:** 1080×1920, the 16:9 shot full-width in a **middle band y 656–1264**, black above/below. Header (2 lines, condensed white, e.g. "Posting moments from the office / w/o context pt. 3") centred y ≈ 570 for the whole reel; one small bold white caption per line centred y ≈ 1320, sentence case, no end punctuation.
  - FCP: header Avenir Next Condensed Medium **25**, Position y **+234**; captions Helvetica Neue Bold **18**, Position y **−210**. (34/27 were ~1.4× too big against the ref: header ≈ 49% of frame width, captions ≈ 16 px/char.)
  - The band is a `Graphics/band_mask_1080x1920.png` (black, transparent band) on lane 2 over everything, so punch-ins stay inside the band.
- **Content:** out-of-context one-liners only, 0.5–3.5 s each, ~18 lines ≈ 32 s. Keep a short laugh only on the big one ("we gotta get you a longer drive" + 1.3 s laugh). Lines that work: an odd phrase alone ("blah blah blah", "for my dog walking membership", "party tricks all day long"), a line said twice ("So Thursday's not realistic" / "It is" / "Thursday's not realistic"), a slip, a sign-off ("I gotta go" / "Great job"). Start a line after a name if the name is a client ("She gave us her whole life document", not "Kelsey's…").
- **Zooms:** jump punch-ins 1.4–1.9× on a face or hands (split the line on a word), and **video-only hand/detail inserts at 1.5–2×** over the speaker's audio (fidgeting fingers, typing next to the coffee cup, hands clasped on a knee, hand on the phone). Find them with 3 s contact sheets of every clip; a sideways meeting cam has lots. Also cover any line whose own picture is a whip-pan blur with an insert.
  - Zoom math (u,v = 0..1 in the 16:9 source, s = scale): X = 1080u, Y = 960 + (v−0.5)·607.5; Position = (−s(X−540)/19.2, s(Y−960)/19.2); clamp u,v to [1/2s, 1−1/2s].
- **Builder:** `scripts/build_no_context.py spec.json OUT.fcpxml` (spec: header/cap styles, pieces with in/out, optional zoom, split punch-ins, caps, inserts). Example spec: `Media/4k Media/Nov/Nov 17 Office Meeting/XML/no_context.json`. Imported into the same event as the selects ("Nov 17 Office No Context"); a second import re-used the already-relinked clips (only the PNG got copied).
- **Verify edges by rendering the cut's audio** (atrim+concat of the spine) and transcribing it with medium.en: it caught a leading "and", "It is, I just" (tail leaked into the next word: use tail 0 there) and a clipped "She".
- **Sound:** ref 1 has a comedic brass/sax bed plus a slap (7 s) and a cow moo at the end; ref 2 also brass/sax. The SFX/songs library is on the 4TB SSD — if it isn't mounted, say so; don't fake it.

## 5. Report
List the moments with timeline time, source clip + timecode, the line, and laugh strength; name the best 2–3; flag the ones that name people; say what you couldn't check (you can't hear the mix, unclear words such as "each of her addicted").

## Nov 17 example (Office Meeting, C4690–C4693, 18 min)
13 moments, 2:36. Best: "the longer the commute, the more productive you are… we gotta get you a longer drive" (C4693 6:31–7:01, laugh peak 95), "was that a line? the timeline?" (8:25), "Bob's your uncle" (10:49), "a day or a month, I'm sorry" (C4692 4:10). Moments list: `Media/4k Media/Nov/Nov 17 Office Meeting/XML/moments.json`.

## Changelog
- 2026-11-17 v0.2: "office w/o context" reel format from Babi's two references (0.7 s cuts, band layout, hand-zoom inserts, punch-ins), build_no_context.py.
- 2026-11-17 v0.1: created from the Nov 17 office meeting. SD ingest + fresh SSD layout, laughter finder, import-everything FCPXML builder, Sony rotation-tag fix, FCP XML import copies media → relink.
