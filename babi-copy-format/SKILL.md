---
name: babi-copy-format
description: Copy the format of a reference reel onto new footage for Ariel ("Babi"). Breaks a reference video down into a reusable format spec — length, intro length, beat drop and where the big transition lands, cut rhythm (shot lengths, cuts per beat), caption style (font, size, position, case, timing, tone of the wording), text/graphic placement, music energy, structure (hook → payoff) — then applies it to the user's clips. Meant to be COMBINED with babi-storytelling, babi-vlog-reels or babi-simple-reels: this skill decides the format, the other decides taste, folders and tools. Use whenever the user gives a reference reel ("make it like this one", "notice how on the beat drop…", "take inspiration from these captions", "make 3 versions in this style").
---

# Babi copy-format

This skill turns a reference reel into a written **format spec**, then re-edits new footage to match it. It handles only the "shape" of the reel. Folders, tools, cutting taste and caption defaults come from whichever skill is paired with it:
- babi-vlog-reels for personal vlogs
- babi-simple-reels for to-camera promos
- babi-storytelling for recaps

## 1. Identify the files
- Probe everything with ffprobe (duration, fps, resolution).
- If two files have the same duration, they're likely the same edit with and without burned-in captions. The captioned one is the **style reference**; the clean one is **reusable footage**.
- Tile frames from each (`fps=2,scale=180:-1,tile=…`) to confirm which is which.
- Treat footage of the same location shot on the same day as one shared clip pool.

## 2. Measure the reference (write every number down)
- **Cuts:** run `select='gt(scene,0.08–0.25)',metadata=print`. Note the cut times and the shot-length pattern. Example: the Lake Ontario reel cut at 3.1, 4.97, 5.9, 6.8, 7.73, 8.63 s, so the shots after the drop were about 0.9 s each.
- **Beat drop:** in the audio RMS (0.1 s windows) find the jump in loudness. Check it against the first big visual change. Example: a +9 dB jump at 3.1 s exactly where the sunrise shot starts. The intro length equals the drop time.
- **Beat grid:** use `librosa.beat.beat_track` when available; otherwise use the median gap between cuts after the drop. Final Cut's Option-B grid ≈ librosa − 0.04 s.
- **Captions:** zoom on caption frames (crop with ffmpeg) and record:
  - the wording and tone (for example "POV: Lake Ontario on a random Tuesday morning": casual, location plus an everyday moment)
  - the font look (Edits "Classic" is condensed white)
  - the size (about 22pt in Edits, 2 lines)
  - the position (about 18% from the top)
  - the effect (soft shadow)
  - the timing (on only until the drop, gone at the transition)
- **Structure:** hook → setup → payoff (for example selfie intro → beat drop → scenery montage → skyline ending). Note where faces, scenery and text sit.
- **Music:** the same song or a different one, and the energy at the drop. If the user's other edits use different songs, keep the reference song when the drop timing matters.

Save it as `format-spec.json` next to the project's XML. Example fields: `{duration, drop_t, beat_period, intro, shots:[...], caption:{text_style, font, size, y, effect, on, off}, structure:[...]}`.

## 3. Apply it to new footage
- **Keep the signature move exact.** In the Lake Ontario reel, the transition to the sunrise had to land on the drop frame (frame 93 at 30 fps). Pre-cut segments to whole frames and verify the export's scene cut equals `drop_t`.
- **Re-arrange the clips onto the beat grid.** Each version should differ in a meaningful way:
  - a different intro (another selfie take, or a split intro)
  - a different shot on the drop (the purple beach vs the golden sun)
  - a different ending (the skyline vs a sun bookend)
- **Write new captions in the same style and tone,** not copies. Examples:
  - "POV: you finally became a sunrise person"
  - "POV: you set a 6am alarm just for Lake Ontario"
  - "POV: Lake Ontario before the coffee kicks in"
- **Bake each shot's slice of the song into its segment** (sample-exact, 1600 samples per frame at 48 kHz/30 fps), so the music can't drift from the cuts. A song added separately in Edits landed 0.1 s late.
- **Build in the paired skill's tool** (Edits or Final Cut), one project per version, named "<Theme> V1 - <caption idea>".

## 4. Verify and report
- Check each export:
  - the duration matches the spec
  - the scene cut is at `drop_t`
  - the audio cross-correlation against the song is ≈ 0 s
  - the caption is visible before the drop and gone after
- Deliver a short table, one row per version: the intro, the shot on the drop, the ending and the caption.

## Comedy vlog format (worked example: ez.romo → babi-ezromo-style)
Use this when the reference is a funny talking vlog rather than a music-drop reel. The finished result of copying ez.romo became its own skill, **babi-ezromo-style**; read it for a full example of what copying turns into.
- **Get the references:** `brew install yt-dlp`, then `yt-dlp -o "%(id)s.%(ext)s" --write-info-json <reel url>`. yt-dlp can't list a profile, so collect the reel URLs from the profile page in the built-in browser (`a[href*="/reel/"]`). Download all of them, not one.
- **Find the sound effects:** Apple's SoundAnalysis classifier, `scripts/sound_classify.swift`. Build it with `swiftc -O sound_classify.swift -o sa`, then run `./sa file.wav`. Drop the music, speech and instrument labels and keep hits ≥55. It also finds clean sounds inside SFX compilation mp3s.
- **Find speed changes:** syllables per second per shot, from whisper word timings. Normal is 4–5; ≥6 means sped up; below 2 on a few words is a comic slow-mo.
- **FCPXML speed:** a `<timeMap preservesPitch="0">` with linear timepoints, `start=in/s`, `duration=(out−in)/s`. Preserve Pitch defaults to ON if you omit the attribute; Babi wants it OFF for comedy.
- **Basic Title `Position`** units are about 1.67 px in 1080×1920 (−252 ≈ 72% down). Zoom position is in % of frame height.

## Lessons from copying ez.romo (v3 → v4 review)
- **Read the user's re-edit before rebuilding.** Use File › Export XML on their project; FCP 12.x writes a `.fcpxmld` bundle, so read `<name>.fcpxmld/Info.fcpxml`. Diff the spine (clips, start, duration, `timeMap preservesPitch`) and the connected SFX against what you built. Here the export showed the user had turned pitch off on all 7 retimed clips, which is more than they mentioned.
- **Build an SFX frequency table across ALL of the creator's reels** (24 for ez.romo), not one. Counts: frog opener 3, duck/goose 5, slap 5, fly buzz 5, boom 3, door/whoosh 6, sheep 2, gong 2, choir 1, foghorn 1. Air horns came almost entirely from one reel, and the user cut them, so weight by how many reels use a sound, not by total hits.
- **Copy the feel, not every trick.** The user kept 5 of 9 SFX. Prefer fewer, bigger moments (boom on the final punchline, fly buzz on an awkward line) over a sound every 3 s.
- **Check the SFX library is mounted first** (`ls /Volumes`): the 4TB SSD unmounted mid-session. Copy every sound you use into `<run>/Sound/` so the project never references the SSD.
- **Time captions from the cut's own audio.** Render the planned cut with ffmpeg (atrim plus atempo for speed changes), transcribe that with whisper, and time the captions from it. Raw-clip whisper timings drift by up to 1.2 s across pauses. Hard-code lines whisper mangles (e.g. "we're getting weird" → "look at this") from raw-clip word timings.
- **Import gotcha:** Final Cut reads the XML when the "which library" dialog opens. If you rebuild the file while that dialog is up, the import uses the stale file, so cancel and re-open. Wispr Flow's overlay can block clicks on Final Cut dialogs; press the button through accessibility (`app_screenshot` the alert window, then `app_click` by element_index) or use the keyboard (Down, Return).
- **Whisper varies between runs on noisy run audio.** Re-check unclear lines with medium.en on just that short slice of the render, and splice those words in.
- **Fit the copied format inside the platform safe zone.** For Instagram Reels 1080×1920: top 250 px, bottom 320 px, 120 px sides, and the right-hand buttons (x > 845, y > 1130) are unsafe. The reference creator's caption size and height are only a starting point: Babi shrank the ez.romo-sized captions twice, from 72/96 to 50/62 to 40/48.
- **Update the existing project with Replace** (export, patch, re-import) instead of creating v2, v3… Babi wants to save storage.
- **Calibrate caption width once per font:** FCP Arial Black is about 1.45 × fontSize px per capital in 1080 wide.

- **Projects are ALWAYS Rec. 709** (Babi, 2026-11-14). In FCPXML the *sequence* format must say `colorSpace="1-1-1 (Rec. 709)"`. Never copy the clips' `9-18-9 (Rec. 2020 HLG)` onto it, because that is why projects came out "Rec. 2020 HLG". Asset formats keep HLG; FCP converts on render. Final Cut has no global default: a new project made by hand with Automatic settings copies the first clip (HLG). So use Use Custom Settings › Color Space › Standard – Rec. 709 (FCP remembers the last custom settings), or fix an existing project with Inspector › Modify › Color Space.

## Updating this skill
This lives in the same skills repo as the others. After the user reacts to a copied format, add what they kept or changed, with numbers, then commit and push.

## Changelog
- 2026-11-14 v0.4: ez.romo specifics moved to babi-ezromo-style; captions default to Final Cut.
- 2026-11-14: projects always Rec. 709 (sequence format colour space).
- 2026-11-14 v0.3: lessons from the ez.romo review — read the user's re-edit via Export XML, SFX frequency across all reels, fewer bigger SFX, captions timed from the cut's own render, caption width calibration.
- 2026-11-14 v0.2: comedy vlog format from ez.romo (SFX classifier, speech-rate speed detection, FCPXML retime/zoom/title-position recipe). Applied to Evan Genia Run v3.
- 2026-11-14 v0.1: from the Lake Ontario sunrise task (3 versions in Edits, sunrise on the 3.1 s drop, POV captions in Classic 22pt with a soft shadow).
