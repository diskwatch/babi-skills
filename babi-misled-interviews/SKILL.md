---
name: babi-misled-interviews
description: Ariel ("Babi") playbook for "misled interview" reels, a vox-pop sketch where coworkers are asked one question on camera ("What's your secret talent?") and Babi swaps the interviewer's audio for a different question ("What's your favorite part of your job?"), so every answer becomes a funny non sequitur. Covers how Babi cuts it (the question audio goes on a connected lane, the original audio is muted until the answer starts), which answers work, how many versions he makes, and how to add the top question caption plus one-word captions to his Final Cut export. Use for "interview questions reel", "misled/misleading questions", "ask them one thing, make the question another", "put the question audio from the last clip", or captions on these reels. Pair with babi-simple-reels / babi-vlog-reels for general cutting and shared/SETTINGS.md for Final Cut gotchas.
---

# Babi misled interviews

**Shared settings and tools: read `~/.claude/babi-skills/shared/SETTINGS.md` first.**

Format learned from Babi's own edit of the Nov 23 office vox-pop (IMG_1188–1191, library `Becks Ad.fcpbundle`, event "fav part of your job?", projects "fav part of job V1–V4"), 2026-11-24. He built it himself and said "all of these versions, I like, and I'm going to post". Claude's first attempt (a plain selects XML of every answer) was ignored; the real format is below.

## The trick (what Babi did)
1. Shoot: Babi walks the office with a mic puck and asks each person the **same real question** ("What's your secret talent?"). 1188–1190 are the answers.
2. At the end he records the **fake question** on its own (IMG_1191): "What's your favorite part of your job?", several retakes, plus one answer ("Quoting."). Only its AUDIO is used. Clean takes in 1191: 4.28–5.87 s, 18.94–20.2 s, 26.17–27.59 s.
3. In the timeline, per answer, the picture is the person being asked, and:
   - the 1191 question audio is a **connected clip on lane −1** (a `<clip>` containing a `<gap>` with the 1191 `<audio>`), placed at the very start of the answer clip (offset ≈ clip start + 0.0–0.1 s), 1.26–1.58 s long;
   - the original clip's own audio gets **volume keyframes: −96 dB from the clip start, then up to 0 dB (sometimes +12 dB on quiet people: his own manual move, never automate it) over 0.26–0.65 s right where the answer begins** (e.g. 27.671 s → 27.987 s on IMG_1190). That mutes the real question and the fake one plays instead;
   - when the picture is only the question being asked (nothing to say yet), the clip is a short **1.58 s piece with `adjust-volume amount="-96dB"`** and the answer is the next clip (Jess, V2/V3/V4).
4. **Cut the answer at a word boundary and cut out right after it.** Clips are 1.1–7.6 s; no dead air; the person's reaction while the fake question plays is the joke.
5. Four versions (V1 37.5 s, V2 44.6 s, V3 46.2 s, V4 51.6 s) are the same ~10–13 answers re-ordered and trimmed; V4 opens with the toe trick, V1 with the finger snap. Make versions like this when asked, don't make a new "format".

**Best pairings (in his order of use):** "I could snap both my fingers at the same time", "Washing the dishes" (literally a job answer, the biggest laugh), "I play guitar, bass, drums… one-man band", "I am like a secret detective", "I can quote every early 2000s comedy movie line for line", "I can do a weird thing with my toe" (double-jointed toes), "I can tap dance", "No, I don't know, man". Short interjections ("Hi", "Hey", "Uh, I don't know") stay in if they react.

## Reading his edit (don't guess)
- The Becks Ad library is on the Extreme SSD. `CurrentVersion.fcpevent` in each project folder is SQLite (see video-tooling memory) but **does not show volume keyframes** (`audioLevelChannelData` is null). Use a real XML export instead: select the **event** in the sidebar (full-screen click on the DELL, Final Cut is usually on `DELL SE2719H`), `app_menu` File › Export XML… (menu path works in background), then release app control and click **Save** with full-screen control (background clicks on a save sheet are refused). The export lands in `~/Downloads/<folder>/<event>.fcpxmld/Info.fcpxml` and contains every project in the event with `adjust-volume` keyframes and the connected question clips.
- Rebuild each cut's audio from the XML with `scripts/audio.py` (trim source, apply the dB keyframes, add the lane −1 clip at its offset), then `scripts/words.py` (medium.en, word times per piece). This is the "cut's own audio" the shared captions rule asks for.

## Captions (Babi's ask, 2026-11-24)
- **Top caption at the start:** "What's the favorite part of your job?" (two lines: "What's the favorite part" / "of your job?"), Helvetica Neue Bold 42, white, shadow `0 0 0 0.75`, offset `4 315`, blur 8, Position `0 368` (≈ y 345, below the 250 px safe zone). It stays from 0 s to the end of the first clip, clamped to **3–5 s** (V1 5.0, V2 3.0, V3 3.55, V4 4.77). If the first clip is shorter than that, add a second header title on the next clip (don't let a connected title overhang).
- **One word at a time**, Helvetica Neue Bold 40, same white + shadow, lowercase, no punctuation, Position `0 −100` (≈ y 1125: below faces, above the button column) as `lane="1"` titles attached to the spine clip they sit on (offset = the clip's `start` + time in the clip, on the 1/60 s grid). A caption ends where the next begins (gap < 0.35 s) or 0.15 s after its word.
- **Skip the first question's words** (the header already says them) but caption every later question and every answer word, including "uh", "hi", "hey", "no".
- **Check the transcript, whisper garbles these:** "toe" came out as "job" (the fake question word bleeding in), "play" as "played", "Hi/Hey" as "Oi!", and an "I" collapsed onto the next word (enforce ≥ 0.09 s between word starts). Fix from the source transcript / energy profile, not by guessing.
- **Use `scripts/captions.py`:** patches his export in place. Keep project names and uids so Final Cut offers **Replace**. Remove the event-level browser `asset-clip`s (the event already has them) and add the `Basic Title` effect resource (`id="eT"`). Validate with the 1.14 DTD (`FCPXMLv1_14.dtd` in the Final Cut app's Interchange.framework) before telling him it is ready.
- Deliver in `~/Downloads/<folder>/`, never import for him. Say that the XML is a snapshot of his projects at export time (he was still editing), so Replace overwrites later changes.

## Workflow checklist
1. Find the footage and his projects (`find` is slow on `/`: look in `~/Downloads`, the Extreme SSD library, `~/Movies/Final Cut Backups.localized`).
2. If he hasn't cut it yet: ask for the fake question to be recorded last (a separate 1191-style clip, 3–5 retakes of the question, clean audio), then build the answers with the swap above. Don't hand him a selects XML of everything; he does not use it.
3. If he has cut it: export the event XML, rebuild audio, transcribe, add captions, validate, mock the caption positions on real frames (render a frame with PIL; faces are at y 500–900), deliver.
4. Report: versions captioned, counts of titles, what was not verified (not opened in Final Cut, mock frames only, word timing from whisper).

## Changelog
- 2026-11-24 v0.1: created from Babi's "fav part of job" V1–V4 and the caption request. Scripts are the ones used that day (set `WORK` to a scratch dir containing `event.fcpxml` and `wav/IMG_xxxx.wav`, 16 kHz mono).
