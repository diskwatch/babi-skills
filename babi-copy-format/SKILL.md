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

## Always copy the SOUND too: find the song and the SFX (Babi, 2026-11-16)
"That's why you watch the reference reel, find the song, and find the sound effects." Never report "no SFX" or keep a stand-in song without doing all of this:
- **SFX: look for identical bursts at the cuts.** Take the RMS (10 ms) around every cut of the same kind. If the same shape repeats each time (here −17 dB for 90 ms on every AI cut, none on the cuts back), it's one SFX sample. The SoundAnalysis classifier misses short hits under music, so don't trust "nothing found" from it.
- **Identify it by spectrum, not label:** average the 9 bursts (the music cancels out) and take band energies. 600–2400 Hz with nothing above 4.8 kHz means a tonal **pop**, not a whoosh, because a whoosh has highs. Then match onsets in the SFX library by band profile plus envelope (`scripts/find_ref_sfx.py`). Winner: `Songs/new/10 Pop sound effect for your video ✨ 4.mp3` at 16.93 s.
- **Song:** if Instagram says "Original audio" (no tag), the classifier still names the instruments: brass + strings + pizzicato = a classical or comedic orchestral piece. Babi found it himself: **Mozart, Eine kleine Nachtmusik K.525 I. Allegro**, started from the top. Next time, try these first:
  - well-known classical pieces matching the instruments, downloaded into `Songs/`
  - chroma-match the music-only stretches against the library (the reference's own song gives ≥0.97; random songs give ~0.89)
  - ask Babi to Shazam it on his phone. ShazamKit from a command-line Swift binary fails with error 202 (no entitlement).
- **Level: copy what Babi keeps, not the reference's raw RMS.** Babi ran the bed at about −9 dB on a −10 LUFS file (final mix −20 LUFS). My −24 dB "reference-matched" bed was far too quiet. The pop sits at speech peak or a bit above (about −6 dBFS RMS).

## Formats already copied (full worked examples in FORMATS.md)
Read the matching section of `FORMATS.md` before copying a similar reel. Each one records Babi's corrections.
- **Comedy vlog (ez.romo):** its own skill, babi-ezromo-style. FORMATS.md keeps the copying lessons (SFX frequency table, speed via syllables per second).
- **Loop + escalating caption ("slap your boss"):** one locked-off loop, a caption ladder changing on every cut, built in Edits.
- **AI aged-reveal ("how long have you been working here"):** ChatGPT age-swap stills with a pop, AI still ≈ 1.0 s, Name/(Role) captions.
- **Chain game ("shake hands with…"):** keep the chain in shooting order, cut production chatter, caption quiet off-mic lines, trial-reel variants.
- **Mashed-up guest testimonials (Immersion Day):** alternate guests per line, B-roll of the people presenting, bleep and blur company names.
- **Camera-roll montage (Otis Redding):** one lowercase line, a hard cut on the drop, montage cut on the song's phrases.
- **Walk-and-talk small captions (Laurier, 2026-11-27):** lives in babi-storytelling.

## Updating this skill
This lives in the same skills repo as the others. After the user reacts to a copied format, add what they kept or changed, with numbers, then commit and push.

- New formats go in `FORMATS.md` (worked example + Babi's fixes) with one line in the list above.

## Changelog
- 2026-11-25 v0.13: camera-roll montage format (Otis Redding reel), laughter + Vision clip catalog.
- 2026-11-23 v0.12: shake hands trial-reel variants V3–V10 from Babi's V2 (his V2 changes read from the DB, later-start + fast-cut recipe, multi-project fcpxml, Locate… import).
- 2026-11-20 v0.11: Immersion Day v3: quicker B-roll with faces between, shake scoring, B-roll muted (srcEnable ignored), bleep + blurred caption for company names, bleep-hook version.
- 2026-11-20 v0.10: Immersion Day v2: import every clip, way more B-roll (Rick/Stu presenting, boardroom reactions), single shots on locked-off clips.
- Older entries: see FORMATS.md.
