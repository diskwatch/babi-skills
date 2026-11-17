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

## 5. Report
List the moments with timeline time, source clip + timecode, the line, and laugh strength; name the best 2–3; flag the ones that name people; say what you couldn't check (you can't hear the mix, unclear words such as "each of her addicted").

## Nov 17 example (Office Meeting, C4690–C4693, 18 min)
13 moments, 2:36. Best: "the longer the commute, the more productive you are… we gotta get you a longer drive" (C4693 6:31–7:01, laugh peak 95), "was that a line? the timeline?" (8:25), "Bob's your uncle" (10:49), "a day or a month, I'm sorry" (C4692 4:10). Moments list: `Media/4k Media/Nov/Nov 17 Office Meeting/XML/moments.json`.

## Changelog
- 2026-11-17 v0.1: created from the Nov 17 office meeting. SD ingest + fresh SSD layout, laughter finder, import-everything FCPXML builder, Sony rotation-tag fix, FCP XML import copies media → relink.
