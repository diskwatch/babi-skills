---
name: babi-ezromo-style
description: Edit Ariel ("Babi") vlogs in the style of ez.romo (Evan, @ez.romo on Instagram), built in Final Cut Pro with Final Cut captions. Covers the hype to-camera hook, cutting every dead space, sped-up exposition and slow-mo shouts with Preserve Pitch OFF, hard punch-ins, a few big meme sound effects (Vine boom, wow), one-word Arial Black captions inside the Instagram safe zone, a top header over the hook, a quiet instrumental bed, Rec. 709 projects, and iterating on Babi's own edit in place with Replace. Use for "edit this like Evan / ez.romo", "make it funny like Evan's videos", "ez.romo style", or a run/friend vlog that should feel like his reels. Pair it with babi-vlog-reels (folders, ingest, transcription, selects). For copying a different creator, use babi-copy-format.
---

# ez.romo style (Final Cut)

**Shared settings and tools: read `~/.claude/babi-skills/shared/SETTINGS.md` first.** It covers Rec. 709 projects, the Instagram safe zone, caption geometry, working on Babi's own edit in place with Replace, Final Cut import gotchas, and the helper scripts. It applies to every Babi skill.

This skill was built from the Nov 13 2026 "Evan Genia Run" (Babi + Evan + uncle Genia). Babi reviewed five versions (v3 → v5). Every rule below is something he kept, changed or asked for. The reference analysis is in `Fall26/Media/Vlogs/Nov 13 Evan Genia Run/XML/format-spec ez.romo.json`.

**Captions are made in Final Cut, not Edits.** Babi compared the two side by side on 2026-11-14 and chose Final Cut. Build the captions in the first pass.

## The look in one breath
Open on the most hyped to-camera line. Cut every pause. Speed up the talky bits and slow-mo the shouts, with **pitch off**. Hard-cut punch-ins on punchlines. Use two big sound effects per ~40 s, not ten. Small one-word captions sit inside the safe zone. A 2–3 line header runs over the hook only. A quiet instrumental bed goes under everything.

## Workflow
1. **Ingest and transcribe** with babi-vlog-reels (2TB folders, ffprobe, whisper small.en/medium.en, contact sheets).
2. **Write the piece table** in `scripts/build_ezromo.py`: `(clip, in, out, speed, zoom, note)`. The current table is the final Evan Genia cut; use it as the example.
3. **Mock-render the dialogue:** `python3 build_ezromo.py audio <tx_dir> cut.wav`. This uses ffmpeg atrim + atempo. Transcribe `cut.wav` with word timings, and re-check unclear lines with medium.en on just that slice.
4. **Build the XML:** `python3 build_ezromo.py xml <selects.fcpxml> words.json out.fcpxml "<Project name>"`. Open it in Final Cut and pick the library.
5. **Babi reviews and edits in Final Cut.** Then:
   - Export XML of his project, and diff it against yours: `python3 ~/.claude/babi-skills/shared/tools/fcpxml_tools.py diff mine.fcpxml "<his>.fcpxmld"`.
   - Apply his notes, and **re-import the same project name with Replace**. Don't make v2, v3… (storage). For caption-only changes, patch his export: `fcpxml_tools.py patch`.
6. **Exports:** Babi presses ⌘E himself (Claude can't use File › Share). For a caption-free copy: `fcpxml_tools.py strip <his>.fcpxmld out.fcpxml "<name> no captions"`.

## Cutting
- **Hook = the most energetic to-camera take, even if it drops info.** Evan's last take, "we're with Babi in Oakville and we're going for a run!", beat the "13th day of running…" take. The header text carries the day count.
- Then a quick setup (who's here and why), cut into a **cutaway on the mention**. The uncle tying his shoes, right as "my uncle… first time wearing running shoes" is said, was "very, very well done".
- **Cut every dead space ≥0.4 s, even inside a punch-in.**
  - Babi flagged 0.9 s between "Genia's feeling good" and "this is my uncle".
  - Also shave the blank right before an answer: uncle's "feel nice" moved from 10.05 to 10.32 s.
  - Find gaps with 20 ms RMS below (75th percentile − 15 dB) lasting ≥0.4 s, and keep about 0.1 s of air either side.
- **Trim greetings** to the funny bit: "we're getting weird, let's go weird" + "this is my uncle… Evan" (drop "what's up dude, how's it going").
- **Drop off-tone lines** even when funny: the "wear reflective sh*t" PSA was cut. Bleeping the swear was good technique, just the wrong clip.
- End on the punchline: "he told me he doesn't run", in slow-mo with a Vine boom.

## Speed (Preserve Pitch OFF on every retimed clip)
- In FCPXML, use `<timeMap preservesPitch="0">`. Babi turned pitch off on all seven retimed clips: "that's what makes it funny".
- **Exposition:** 1.3× (Evan's own reels measure 6–9 syllables/s, against 4–5 normal).
- **Yell ramp** (after "we scared the whole neighborhood away"):
  - Fast part: **1.3×, about 0.55 s** on the timeline. Not 2×; Babi made it longer and slower.
  - Then **0.5× for about 0.8 s** of the scream face.
  - Zoom 1.15 on both parts.
- **Slow-mo the last shout of a hype clip:** Evan's final "WEIRD" at 0.5× (IMG_0184 14.78–15.40).
- **Ending punchline:** 0.75× + punch-in 1.5 + Vine boom.
- Recipe:
  - Timepoints: `<timept time="0s" value="0s"/>` and `<timept time="{D/s}" value="{D}"/>`, both `interp="linear"`.
  - Clip timing: `start = in/s`, `duration = (out−in)/s`, in retimed clip time.
  - Child offsets: `start + (timeline − clip offset)`.

## Punch-ins
- Hard cut (no animation) to `<adjust-transform scale="1.4 1.4" position="x y">`. Position is in % of frame height; aim the face roughly at centre.
- Keepers: the uncle's "running with running shoes" (+ wow), "this is my uncle by the way", and the "doesn't run" ending (1.5).
- Babi removed the "5-10" punch-in and its boom. Don't punch in on every number.

## Sound
- **About two SFX per 40 s.** Babi kept only the **wow** on the uncle's running-shoes punch-in and the **Vine boom** on the final slow-mo.
- Removed across reviews: air horns (both), duck quack, record scratch, fly buzz, the whoosh on the yell ramp, and the boom on "5-10" ("nice try, but not really it").
- Evan's own SFX frequency (24 reels, from Apple's SoundAnalysis classifier, `shared/tools/sound_classify.swift`): frog opener 3, duck/goose 5, slap 5, fly buzz 5, boom 3, whoosh/door 6, sheep 2, gong 2. Weight by how many reels use a sound, and still keep it sparse.
- The kit used is in `<run>/Sound/`:
  - `vine_boom.mp3`: onset 0.22 s, −9 dB
  - `wow.mp3`: 0.33 s, −12 dB
  - `sfx_pack_kaushal.mp3`: fly buzz 22.82, duck 53.28, beep 0.15, whoosh peak at 24.33
  - `air_horn.mp3`
- Copy any sound into the run folder first. The 4TB SSD can unmount mid-session.
- **Music:** an instrumental bed (Wii Sports title theme) at **−19 dB** under the whole thing. −13 was too loud.

## Captions (Final Cut, Basic Title)
- One word per card; merge up to 3 words only when a card would be under 5 frames. All caps, **Arial Black**, white fill, `strokeWidth="-5"` black, soft shadow `4 315`.
- **Size: 40 pt, 48 pt for key words**, capped at **590 px wide** (Arial Black ≈ 1.45 × fontSize px per capital, so size ≤ 590 / (1.45 × letters)). Babi shrank them twice: 72/96 → 50/62 → 40/48.
- **Position −252** (Basic Title units are about 1.67 px), so the centre sits at y ≈ 1380, about 72% down.
- **Time captions from the cut's own audio** (step 3), never from raw-clip whisper, which drifts up to 1.2 s.
- Hard-code the lines whisper mangles:
  - "Bobby" / "Wood Bobby" → **BABI**
  - "sir" / "Zhen" / "Jay" → **GEN**
  - "Zhenya's" / "Jen is" → **GENIA'S**
  - "riding" / "ride" → RUN(NING)
  - "five ten" → **5-10**
  - "look at this" → "WE'RE GETTING WEIRD"
  - drop "whoa" noise
- No captions on the scream ramp.
- **Header over the hook only:** "Running every day / till the end of the year" in Helvetica Neue Medium 42 at Position 368, and "Day 13" (44) at Position 243. Babi moved it down out of the top 250 px. **No persistent tracker** after the hook; he deleted it.

## Safe zone, project settings, import, tools
All in `shared/SETTINGS.md`: Rec. 709, the Instagram safe zone, Position units, the Final Cut 12.3 library, import gotchas, and `fcpxml_tools.py`. ez.romo-specific: captions at Position −252, the header at 368/243, width cap 590 px.

## Updating this skill
This lives in the babi-skills repo (see babi-storytelling's "Updating this skill").
1. After each of Babi's reviews, export his XML, run `fcpxml_tools.py diff`, and write what he kept or changed here with numbers.
2. Add a changelog line.
3. Commit and push.

## Changelog
- 2026-11-14: shared settings/tools moved to `shared/SETTINGS.md` (applies to all Babi skills).
- 2026-11-14 v1.0: created from the Evan Genia Run reviews v3 → v5 and the FCP-vs-Edits caption comparison (Babi chose Final Cut captions).
