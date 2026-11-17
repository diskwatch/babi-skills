---
name: babi-copy-format
description: Copy the format of a reference reel onto new footage for Ariel ("Babi"). Breaks a reference video down into a reusable format spec — length, intro length, beat drop and where the big transition lands, cut rhythm (shot lengths, cuts per beat), caption style (font, size, position, case, timing, tone of the wording), text/graphic placement, music energy, the song and sound effects (always identified), structure (hook → payoff) — then applies it to the user's clips. Meant to be COMBINED with babi-storytelling, babi-vlog-reels or babi-simple-reels: this skill decides the format, the other decides taste, folders and tools. Use whenever the user gives a reference reel ("make it like this one", "notice how on the beat drop…", "take inspiration from these captions", "make 3 versions in this style"), including AI reveal formats such as coworkers aged to how long they have worked here (ChatGPT image generation).
---

# Babi copy-format

**Shared settings and tools: read `~/.claude/babi-skills/shared/SETTINGS.md` first.** It covers Rec. 709 projects, the Instagram safe zone, caption geometry, working on Babi's own edit in place with Replace, Final Cut import gotchas, and the helper scripts. It applies to every Babi skill.

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
- **Sound effects and song:** always find both; see "Always copy the SOUND too" below. Never deliver with "no SFX" or a stand-in song until that search is done.
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
- **Find the sound effects:** Apple's SoundAnalysis classifier, `~/.claude/babi-skills/shared/tools/sound_classify.swift`. Build it with `swiftc -O sound_classify.swift -o sa`, then run `./sa file.wav`. Drop the music, speech and instrument labels and keep hits ≥55. It also finds clean sounds inside SFX compilation mp3s.
- **Find speed changes:** syllables per second per shot, from whisper word timings. Normal is 4–5; ≥6 means sped up; below 2 on a few words is a comic slow-mo.
- **FCPXML speed:** a `<timeMap preservesPitch="0">` with linear timepoints, `start=in/s`, `duration=(out−in)/s`. Preserve Pitch defaults to ON if you omit the attribute; Babi wants it OFF for comedy.
- **Basic Title `Position`** units are about 1.67 px in 1080×1920 (−252 ≈ 72% down). Zoom position is in % of frame height.

## Loop + escalating caption format (worked example: "would you slap your boss for...", 2026-11-16)
- Reference DfqEYpRglVo: one locked-off office shot, 9 hard cuts every **0.96 s** (23 f @ 23.976), each a slap take; quoted white caption at mid-frame changes on every cut down a price ladder (a million → $100k → … → free → "Coworker"); music loop, no speech. Measure cuts with a frame-difference scan when `scene` finds nothing (same angle every shot).
- Babi's version: his own single take looped (IMG_0507 12.98–14.22 s, **1.23 s** loop — kept, since his run-in is longer), 11 loops, captions “Would you slap / your boss for $X?” from $1 billion to $1. Built straight into the Edits project with `scripts/build_slap_edits.py` (see babi-vlog-reels' Edits recipe for the DB rules).

## Always copy the SOUND too: find the song and the SFX (Babi, 2026-11-16)
"That's why you watch the reference reel, find the song, and find the sound effects." Never report "no SFX" or keep a stand-in song without doing all of this:
- **SFX: look for identical bursts at the cuts.** Take the RMS (10 ms) around every cut of the same kind. If the same shape repeats each time (here −17 dB for 90 ms on every AI cut, none on the cuts back), it's one SFX sample. The SoundAnalysis classifier misses short hits under music, so don't trust "nothing found" from it.
- **Identify it by spectrum, not label:** average the 9 bursts (the music cancels out) and take band energies. 600–2400 Hz with nothing above 4.8 kHz means a tonal **pop**, not a whoosh, because a whoosh has highs. Then match onsets in the SFX library by band profile plus envelope (`scripts/find_ref_sfx.py`). Winner: `Songs/new/10 Pop sound effect for your video ✨ 4.mp3` at 16.93 s.
- **Song:** if Instagram says "Original audio" (no tag), the classifier still names the instruments: brass + strings + pizzicato = a classical or comedic orchestral piece. Babi found it himself: **Mozart, Eine kleine Nachtmusik K.525 I. Allegro**, started from the top. Next time, try these first:
  - well-known classical pieces matching the instruments, downloaded into `Songs/`
  - chroma-match the music-only stretches against the library (the reference's own song gives ≥0.97; random songs give ~0.89)
  - ask Babi to Shazam it on his phone. ShazamKit from a command-line Swift binary fails with error 202 (no entitlement).
- **Level: copy what Babi keeps, not the reference's raw RMS.** Babi ran the bed at about −9 dB on a −10 LUFS file (final mix −20 LUFS). My −24 dB "reference-matched" bed was far too quiet. The pop sits at speech peak or a bit above (about −6 dBFS RMS).

## AI aged-reveal format (worked example: "How long have you been working here?", 2026-11-16)
Reference: maria.wendt DfQS0FjSVeE, "I turned my coworkers into how long they've been working here". Each person gets a question and their answer with a "Name (Role)" caption, then a hard cut **with a pop** to an AI version of them at the age = time worked (7 months → baby, 4 years → 4-year-old), in the same pose and room, with no caption.
- **Footage:** `Media/OFFICE/How long have you been working here?/` (13 clips plus `Reference/`, `AI Frames/`, `Sound/`, `XML/`). Project: TME › "Nov 16 How long have you been working here" › "How Long Have You Been Working Here". Export: `Exports/OFFICE/How Long Have You Been Working Here.m4v` (50.45 s).
- **AI images:** run the ChatGPT desktop app with full-screen control (see shared/SETTINGS.md › ChatGPT images). One new chat per person: paste the answer frame, then prompt "turn this man/woman into a N-year-old version of himself/herself, keep face features, eye/hair colour, same clothes in kid size, same pose holding the small mic, same background, lighting, angle and framing, photorealistic iPhone photo, vertical 9:16". About 60–70 s each, 941×1672 output.
  - The source frame is the last frame of the answer, grabbed in SDR with `shared/tools/grab_sdr_frame.swift`. It tone-maps the HLG; ffmpeg here has no zscale.
- **Joke answers get a joke image, not a skip.** Stu ("since the beginning", the co-founder) stays his own age and becomes a **caveman with dinosaurs and a volcano**. Babi made that image himself. Andrew ("since I was a baby") → baby. "Ten, fifteen years maybe" → about 12 years old.
- **Babi regenerated 2 of 12** (Rick and Karleigh) when the face drifted. Check every image for likeness before building.
- **Babi's final cut (50.45 s, 13 people, ≈3.9 s each):**
  - question and answer, with a **punch-in jump cut (1.2×) 0.15 s before the answer**, kept on every person
  - about 0.3 s reaction after the answer
  - the AI still holds **0.85–1.53 s, median 1.03 s** (I built 1.3; the reference median is ≈1.3). Babi cut them shorter.
  - **Order:** he opened with Alli (a quick, clean 4-year answer, AI at 2.5 s) rather than the baby, then Jess, Stu/caveman third as the early laugh, and closed on Andrew "since I was a little baby".
  - He dropped the dead air before each question: the question starts about 0.25 s after the cut.
- **Captions:** Babi's are **two lines, "Name" / "(Role)"**, Helvetica Neue Bold at about **60 pt** in FCP, white with a soft shadow, block centred at y ≈ 1295 (67% down), on the real footage only. Long roles wrap to 3 lines ("Alli / (Executive Operations / Lead)", 894 px wide). Keep the role short or allow it.
- **Names and roles come from Babi.** Whisper heard "Alexa" for Alexey, "Ali" for Alli, and missed Jess, Karleigh and Asim. Leave `NAME?`/`(ROLE)` placeholders and ask.
- Builder: `scripts/build_aged_reveal.py`, the spine plus AI stills with a 6% push-in, pop SFX and music. Update its defaults to Babi's numbers above before reuse.

## Chain-game format (worked example: "Shake hands with...", 2026-11-16)
References: demandthelimitslaw DeSWfvszUJ4 (16.6k likes, the one to weight) and kinso.app DVFpUG8iYnj (1.8k likes). yt-dlp returns likes, not views.
- **Winner's numbers:** 73 s, 10 people, about 7.3 s each: card read 2-3 s, walk 1-2 s, handshake plus one line about 2 s. No music, raw lav audio with the laughter. The weaker one has 4-7 s walks and 8.3 s per person.
- **Look:** header "SHAKES HANDS WITH..." white caps on a black box on the whole video (ours centred y 345, below the 250 px band); captions in 2-3 word chunks, white caps, the spoken word green (170,223,131), about 61-63% down.
- **Ending:** the winner ends with the card that picks the cameraman ("office celebrity"). Ours ends the same way (Rick shakes Babi's hand).
- **First build (rejected order):** 72.4 s, 10 of 14 rounds, ordered by interest. Footage `Media/OFFICE/Nov 18 shake hands with.../`, project TME FCP12.3 > "Nov 18 Shake hands with" > "Shake Hands With". Builder `scripts/build_shake_hands.py` (needs idx.json and cut_words.json from rendering the cut audio and running medium.en; whisper glues a leading "Shake" onto the previous shot, the builder moves it).
- **TME does not open on this Mac** (saved by 12.4, this Mac has 12.3: "created with a newer version"). A fresh `.lock-info` does not prove it opens. The project went into a new library, `Libraries/TME FCP12.3.fcpbundle` (New... in the import dialog). Re-import with the same project name and press Replace.
- **Caption calibration (Avenir Next Heavy, size 30):** about 38 px per letter, so 15 letters is about 575 px. Position -215 put it 69% down; **-140 is 62%** like the reference. Open the project with Clip > Open Clip when double-clicking the thumbnail does nothing.
- **Babi's first correction (2026-11-16): a chain game must stay in the order it happened.** Each person who gets the handshake reads the next card, so reordering "by interest" breaks it ("that's the only way it really works"). I had reordered and dropped 4 of 14 rounds; the fix is all 14 rounds in shooting order (0529 -> 0531 -> 0532 -> 0533), 104 s. Tighten inside each round instead of reordering or dropping. Captions and header were "okay for now".
- **Babi's v2 re-edit (read via Export XML, 2026-11-16) and notes — what to learn:**
  - **Cut production chatter:** "OK, all right, thank you, go on the mic" (best snacks) and "now Stu, do you mind filming me" (celebrity) are not part of the video.
  - **Cut tails after the payoff:** he ended on "Hi Stu" (dropped "all right, thanks guys", −1.8 s); "lie for you" and "for help" trimmed ~0.3–0.5 s.
  - **Finish the reply's phrase:** "oh, back to Stu" was cut at "back to"; he extended the shot 0.75 s to land "Stu".
  - **Keep the transition when it tells the story:** after "it would be Andrew, but he's busy", keep the camera zooming on Andrew through the glass (IMG_0533 123.9–127.1) before the boardroom handshake.
  - **Keep the warm moments:** "you always have nice clothes" → "office love, office love" (298–307.4) after "Hi Jess". Scan the gaps between rounds for reactions like this before cutting them.
  - v3 = 110.7 s, imported with **Keep Both** ("Shake Hands With 1") so his edit stays intact.
- **Captions: transcribe each shot from its own padded source slice** (`scripts/shot_words.py`, medium.en, ±0.4 s), not the whole rendered cut: whole-cut whisper glued "Shake" onto the previous shot and drifted. Keep a word if its centre is in the shot or it overlaps ≥0.12 s; a new caption always starts at "SHAKE"; `NO_CAPS` for silent walk/handshake shots (whisper writes "Thanks for watching!"); `OVERRIDE` for names and clipped lines.
- **Babi's v3 notes (2026-11-17) → v4 ("Shake Hands With 2", 107.9 s):**
  - **Stacked captions came from overlapping titles.** A chunk's tail (+0.25 s) ran into the next chunk, and chunks could span two shots, so Final Cut bumped titles into 2-3 lanes. Fix in the builder: a chunk never crosses a shot, every title's times are computed on the timeline, and each title is clipped to end where the next starts (asserted). Check the timeline shows ONE caption row.
  - **Caption everything said, including quiet off-mic replies.** Jess's "stop, that's a lie" (off-mic, about −40 dB) was in the cut but uncaptioned because an OVERRIDE ("HI JESS") replaced the shot's words. Whisper only found it with an `initial_prompt` of the expected line; use `TIMED` for exact per-word times and "|" to force a new caption. Audit every shot, NO_CAPS ones too, against a whole-take medium.en transcript: "how's it going buddy" had been NO_CAPS.
  - **Cut the thank-you tail after a handshake** (Babi shaking Rick's hand + "thank you", 62.9-63.77) and **cut Babi repeating someone's punchline** (Jess "office love" kept, his echo at 305.9 cut, found in 10 ms RMS).
  - **Tighten the walk-up, keep the mic hand-off:** Alli round trimmed inside (silence 84.3-84.7 cut, handshake shot starts at speech 88.45).
  - **Funny details get a jump-cut zoom + vine boom:** Rick's fruit bowl, a 0.8 s insert (43.3-44.1) at 2.4x centred on the bowl (zoom formula: x = −s(cx−540)/19.2, y = s(cy−960)/19.2), with `Songs/new/Dramatic Vine_Instagram Boom...mp3` (onset 0.20 s) at −8 dB on lane −1. Copy SFX into `<project>/Sound/`.
  - **Babi adds his own music in his copy.** He put Mozart (Eine kleine Nachtmusik, from 39.45 s, −16 dB, whole video) under "Shake Hands With 1". Export XML was disabled (an Export File window was open), so I read it from the library: `<project>/CurrentVersion.fcpevent` is SQLite; ZCOLLECTIONMD.ZDICTIONARYDATA holds NSKeyedArchiver plists (`clippedRange`, `anchorPair` as rational seconds) and the volume sits in an ozml `<parameter name="Volume">` curve value (0.158 = −16 dB). Carry it into every rebuild.

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

## Updating this skill
This lives in the same skills repo as the others. After the user reacts to a copied format, add what they kept or changed, with numbers, then commit and push.

## Changelog
- 2026-11-17 v0.8: shake hands v4 from Babi's notes (caption de-overlap, caption every line, fruit-bowl zoom + vine boom, tails/echo cuts, his Mozart bed read from the library DB).
- 2026-11-16 v0.7: shake hands v3 from Babi's re-edit (chatter/tails cut, transitions and warm moments kept), per-shot captions.
- 2026-11-16 v0.6: chain-game format (shake hands with...), first build, not yet reviewed.
- 2026-11-16 v0.6: AI aged-reveal format (ChatGPT age-swap images, pop on each reveal, Mozart bed) and "always find the song + SFX" rules, from Babi's final "How Long Have You Been Working Here".
- 2026-11-16 v0.5: loop + escalating-caption format (slap your boss), built directly into Edits.
- 2026-11-14: shared settings/tools moved to `shared/SETTINGS.md` (applies to all Babi skills).
- 2026-11-14 v0.4: ez.romo specifics moved to babi-ezromo-style; captions default to Final Cut.
- 2026-11-14: projects always Rec. 709 (sequence format colour space).
- 2026-11-14 v0.3: lessons from the ez.romo review — read the user's re-edit via Export XML, SFX frequency across all reels, fewer bigger SFX, captions timed from the cut's own render, caption width calibration.
- 2026-11-14 v0.2: comedy vlog format from ez.romo (SFX classifier, speech-rate speed detection, FCPXML retime/zoom/title-position recipe). Applied to Evan Genia Run v3.
- 2026-11-14 v0.1: from the Lake Ontario sunrise task (3 versions in Edits, sunrise on the 3.1 s drop, POV captions in Classic 22pt with a soft shadow).
