---
name: babi-knowledge-reels
description: Ariel ("Babi") playbook for knowledge / teaching reels. These are one person talking to camera to TEACH something (numbers, a framework, a tip, "how we made $320k"), not to tell a story. Over the talking head, pull photos from the internet that literally match what's being said, landing on the lower chest with a pop. Captions are word-by-word in 2–3 word groups with the spoken word in yellow, plus a topic header near the top. Big yellow dollar figures appear when money is mentioned, and the camera can be zoomed onto a whiteboard he points at. Built as FCPXML on top of Babi's own cut in Final Cut. Learned from Babi's "Toni Blog" and "Hal Eldro" reels (TME library) and a Nick Tarmossin reference reel. Use for "knowledge reel", "add photos from the internet over what he's saying", "teaching reel", "zoom on the board", "captions like this reel", or when the subject is explaining or giving advice. For story recaps with B-roll bursts use babi-storytelling; for plain promo takes use babi-simple-reels.
---

# Babi Knowledge Reels

**Shared settings and tools: read `~/.claude/babi-skills/shared/SETTINGS.md` first.** It covers Rec. 709, the Instagram safe zone, caption geometry, Replace-in-place, and Final Cut import gotchas.

A knowledge reel **teaches**. The speaker explains something, and every few seconds a photo pops up showing exactly the thing he just named. The photos are internet images, not our own B-roll. The talking head stays on screen the whole time; photos sit *over* it.

## The references (measured)
### Babi's own: "Toni Blog" (50.4 s) and "Hal Eldro" (79 s), TME › event 2026-09-24
Exports: `Exports/OFFICE/Toni Blog.m4v`, `Exports/OFFICE/Nov 3 Hal Eldro.m4v`. XML: `Media/OFFICE/Nov 12 Black Friday/XML/{Toni Blog,Hal Eldro}.fcpxmld`.
- **One photo at a time, on lane 1, centred on the lower chest.** Position y is −19.3 to −23 % (centre ≈ y 1330–1400 px); Toni has one at −24.8 %. Scale (relative to fit) is 0.42–0.87, i.e. roughly 450–900 px wide.
- **Each photo lands with a pop** (the "Censor sound … Pop sound" mp3, source 0.991 s, 0.156 s long) at **−12 dB (Hal) / −13 dB (Toni)**, on lane −2, on the same frame.
- **Photos chain back to back.** Each holds until the next one arrives, usually 1–4 s (range 1.0–6.9 s). They often start on a spine-clip start, otherwise on the key word.
- **Literal, not artistic.** Hal: "podcast" → podcast-mic clip art; "Stu McLaren" → his photo; "no one reads books" → a no-book icon; "booking calendar" → calendar illustration; "audience" → auditorium vector. Screenshots of the guest/podcast are mixed with stock photos and flat illustrations (istock, pixabay, freepik).
- **Music under it:** an upbeat song at −14 dB (Green Onions) or −16 dB (Just Like Heaven) on lane −1, the full length.
- Neither had captions. Hal has about 22 photos in 79 s (one every ~3.5 s).

### Caption reference: Nick Tarmossin reel (instagram.com/p/DY2aurJxtMn)
- **2–3 words at a time, lowercase, bold sans (looks like SF / Helvetica Bold), white with a soft shadow and no outline.** The word being spoken turns **yellow**, karaoke style.
- Captions sit at about **77 % down (y ≈ 1490 px)**, roughly 60–70 px type.
- **A two-line topic header near the top** (≈ y 340–420 px, smaller, white) names what the section is about, and changes per section ("you're not doing as bad as you think / (your brain is tricking you)").
- **Numbers are shown as numbers, in yellow:** "$100,000 a month".
- Charts and illustrations appear on the chest, just above the caption line; an occasional full-screen photo.

## Babi's verdict on the first build (2026-11-16, Black Friday)
- **Photos: "the photos make sense and the timing makes sense, very well done"**, so keep this recipe for knowledge reels in general. **But NOT when the speaker teaches from a board, screen or prop.** On Black Friday he removed all 18 photos (and their pops) because they covered the whiteboard. Rule: if the visual is already in the shot (whiteboard, slide, product), let the zoom and the yellow figures carry it, with no photo overlays. Use photos only when he is just talking.
- **Board zoom: "really good".** Keep 1.45× on the board clips, verified with an ffmpeg crop first.
- **Captions (karaoke words and yellow dollar figures): good.** No changes.
- **The header was too high.** He dragged the first header down with Transform y **−9.27 %** (≈ 178 px), from ≈ 345 px to **≈ 523 px from the top**, and asked for all the others to match. New default: Position `0 368` plus `adjust-transform position="0 -9.27"`, or simply head_y ≈ 262.
- **The CTA header goes toward the centre.** Exact centre (≈ 921 px) sat on Stu's mouth (in the CTA clips his face spans about 760–1200 px), so it went on his chest just under the chin, at **≈ 1270 px** (transform y −48.18), above the word captions at 1500. Mock the position on two frames per clip with PIL before importing.
- In a title, `adjust-transform` must come **after** `param`, `text` and `text-style-def` (DTD order), or the import fails validation.

## Recipe (what the first build used)
Script: `scripts/build_knowledge_reel.py plan.json`. It adds everything as connected clips to an **exported copy of Babi's cut**. The spine is untouched, and the result is imported as **a new project, "<Title> - Knowledge"**.
1. **Export Babi's cut** (File › Export XML into `Media/OFFICE/<topic>/XML/`). Read the spine.
2. **Transcribe the cut's own audio.** Concatenate the spine clips' source ranges with ffmpeg, then run medium.en with word timestamps. Those times are the timeline times. Whisper writes "$320" ",000" and "50" "%" as separate tokens; the script joins them.
3. **Pick a photo for each concrete noun or idea**, about one every 2–4 s:
   - Search Openverse (`api.openverse.org/v1/images/?q=…&license_type=commercial`, fetched with **curl**: Python urllib fails on SSL here).
   - Download 4 candidates per idea into `<topic>/Knowledge Photos/candidates/`, look at a contact sheet, and copy the picks as `NN name.jpg`. Keep `photo_sources.json`, with the licence and creator, for credit.
   - Convert WebP files that come down with a .jpg name to real JPEG.
   - Openverse is hit and miss (no good "software dashboard" or "40% off"). Re-query with plainer words, or reuse a photo.
4. **Photos:** lane 1, centre y −12 % (≈ 1190 px), fitted inside 600×440 px, each with a pop at −12 dB on lane −1. Hold each until the next idea. Clear them before a big figure, so the board or face is visible when the money shows.
5. **Captions:** a Basic Title per word, Helvetica Neue Bold 64, white `1 1 1 1`, the active word `1 0.88 0 1`, shadow `0 0 0 0.75` offset "4 315" blur 8, Position `0 -323` (≈ y 1500).
   - Groups are at most 3 words or 16 characters.
   - Break at sentence ends and at gaps over 0.35 s.
   - Lowercase, no punctuation, but keep `$`, `%` and the thousands commas in numbers.
6. **Dollar figures:** when a dollar amount is spoken, replace the caption with a big yellow figure (Helvetica Neue Bold 124, same Position) for the length of the word, up to the next line, with a **Ding at −16 dB** (source 0.21 s, 0.85 s long). Black Friday used $320,000 / $46,000 / $152,000 / $123,000 / $321,000.
7. **Header:** Helvetica Neue Bold **40** (50 was too wide, about 85 % of the frame), two lines, one per section ("2023: 50% off upgrade / for existing customers").
   - **Place it at ≈ y 523** (Position `0 368` plus a transform of −9.27; see Babi's verdict).
   - The final CTA header goes on the chest under the chin, ≈ y 1270.
8. **Whiteboard zoom** (Black Friday): a static `adjust-transform` on the spine clips where Stu stands at the board.
   - Scale 1.45, centred on source px (700, 1120), giving position −12.08 / +12.08.
   - Formula: `x% = −s·(cx−540)/19.2`, `y% = s·(cy−960)/19.2`.
   - **Check it first with an ffmpeg crop** (`crop=1080/s:1920/s:cx−w/2:cy−h/2`) on two frames per clip. That showed clips 1–2 and 16 cut Stu's face off, so leave those unzoomed, and shift clip 3 left (cx 640).
9. **Music:** one song on lane −3 under the whole reel at a flat level, trimmed to the video (plan key `"music": {file, start, db, length}`).
   - Prefer an **instrumental with a groove** so it doesn't fight the voice (Babi used Green Onions for Hal).
   - **Start where the band comes in, not on a sparse intro.** Find it with 1 s RMS in librosa, then 10 ms RMS around the jump.
   - Black Friday: "Take Five" (Dave Brubeck, `Songs/new/`). The drums-only intro is about −34 dB until 16 s, and the band comes in at 20.85 s, so the song starts at **20.85 s**. Its sax lands at 21.2 s, under "$320,000".
   - Level **−15 dB**, between the references' −14 and −16. Measured with ffmpeg ebur128, that is **13.4 LU under the speech** (−20.7 vs −34.1 LUFS). That's a good bed level to aim for: 12–15 LU under.
10. Validate against `FCPXMLv1_14.dtd`, import into TME, and check frames with Ctrl-P + timecode (typing `1430` = 14 s 30 f; `31200` is 3 min 12 s). Zoom the viewer region to read text.

## Open questions for Babi (ask, then record the answer here)
- Music: Babi asked for a song; Claude chose Take Five. Record whether he keeps it or swaps it.
- Keep the topic header, or captions only?
- Photo source: is Openverse (CC) fine, or does he want Google-image style picks like Hal's (istock and freepik previews)?

## Changelog
- 2026-11-16 v0.3: Babi's review. Photos removed when a board is in shot, headers lowered to ≈ 523 px, CTA header on the chest (≈ 1270 px); zoom, captions and figures approved. His export backed up as "Black Friday Reel - Knowledge (Babi edit backup).fcpxmld"; the patch is "Black Friday Reel - Knowledge v2.fcpxml".
- 2026-11-16 v0.2: Babi said "add a song". Take Five from 20.85 s at −15 dB on lane −3, trimmed to 53.32 s; the builder now has a `music` plan key.
- 2026-11-16 v0.1: created from the Toni Blog and Hal Eldro XML, plus the Nick Tarmossin caption reference. First build: "Black Friday Reel - Knowledge" (TME › Nov 12 Black Friday): 18 photo pops, 66 caption groups, 5 dollar figures with dings, 7 headers, a 1.45× board zoom on clips 3–15. Plan: `Media/OFFICE/Nov 12 Black Friday/XML/BF knowledge plan.json`.
