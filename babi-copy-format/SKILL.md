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

## Comedy vlog format (from ez.romo / Evan, Nov 14 2026)
Use this when the reference is a funny talking vlog rather than a music-drop reel. The full spec is `Nov 13 Evan Genia Run/XML/format-spec ez.romo.json`.
- **Get the references:** `brew install yt-dlp`, then `yt-dlp -o "%(id)s.%(ext)s" --write-info-json <reel url>`. yt-dlp can't list a profile, so collect the reel URLs from the profile page in the built-in browser (`a[href*="/reel/"]`).
- **Find the sound effects:** Apple's SoundAnalysis classifier (`SNClassifySoundRequest(classifierIdentifier: .version1)`, 1 s window, 0.5 overlap) names them with no download. The source is `scripts/sound_classify.swift`; compile it with `swiftc -O sound_classify.swift -o sa`, then run `./sa file.wav`. The builder is `scripts/build_ezromo_style.py` (edit its piece table). Drop the music/speech/instrument labels and keep hits ≥55. It also finds clean sounds inside the user's SFX compilation mp3s.
- **Find sped-up clips:** measure syllables per second from whisper word timings for each shot. Normal speech is about 4–5; ≥6 means sped up (Evan uses 1.3–1.6×). Below 2 on a few words means a comic slow-mo.
- **Evan's moves:** 1-word heavy captions at 77% down; a 2-line header plus "Part N" at the top of the intro, then a top-centre progress tracker; a hard punch-in (1.4–1.5×) with a Vine boom on punchlines; an air horn on hype words ("we got weird"); fly buzz after an awkward line; duck quack on a self-own; a censor beep on a swear; an instrumental bed about 9 dB under speech.
- **FCPXML recipe:**
  - Speed: `<timeMap><timept time="0s" value="0s" interp="linear"/><timept time="{D/s}" value="{D}" interp="linear"/></timeMap>`, with `start=a/s` and `duration=(b-a)/s` in retimed clip time. Preserve Pitch comes out ON (checked under Modify › Retime).
  - Child offsets inside a retimed clip are `start + (timeline − clip offset)`.
  - Zoom: `<adjust-transform scale="1.4 1.4" position="x y"/>`, where position is in % of frame height.
  - **Basic Title `Position` units in a 1080×1920 project are about 1.67 px each.** −311 puts the text 77% down; +470 puts the top tracker about 5% from the top. My first try of −518 landed at 95%.
  - A re-import with the same project name asks Keep Both / Replace. Replace swaps in the new project and leaves the other projects alone.

## Updating this skill
This lives in the same skills repo as the others. After the user reacts to a copied format, add what they kept or changed, with numbers, then commit and push.

## Changelog
- 2026-11-14 v0.2: comedy vlog format from ez.romo (SFX classifier, speech-rate speed detection, FCPXML retime/zoom/title-position recipe). Applied to Evan Genia Run v3.
- 2026-11-14 v0.1: from the Lake Ontario sunrise task (3 versions in Edits, sunrise on the 3.1 s drop, POV captions in Classic 22pt with a soft shadow).
