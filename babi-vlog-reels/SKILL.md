---
name: babi-vlog-reels
description: Ariel ("Babi") playbook for simple vlogs and caption reels that are NOT storytelling recaps. Covers run vlogs (Babiontherun, run-every-day series), friend and day vlogs, surprise moments, and vlog-style reels with small on-screen captions. Covers moving AirDropped clips to the right folder on "Babi's 2TB", picking good clips, a selects timeline in Final Cut, tight vlog cuts in the Edits app or Final Cut, one-word captions, and exporting. Use for "make a vlog", "edit this run", "put the good clips in a timeline", "add captions". For a reference reel to copy, also use babi-copy-format. For to-camera promo reels, use babi-simple-reels. For talking-head storytelling recaps with B-roll bursts, chat pops and music (Stu / office reels), use babi-storytelling instead.
---

# Babi vlog and caption reels

These are quick personal vlogs and caption reels. Every rule here came from the user correcting Claude's cuts. It's a living document: after each correction, add the lesson with numbers, then commit and push (see the end of this file).

## Where things live (drive "Babi's 2TB")
- **Raw footage:** `/Volumes/Babi's 2TB/Babiontherun/Fall26/Media/Vlogs/<Mon D Title>/`. Examples: "Nov 11 Night Rain Run", "Nov 13 Evan Genia Run".
  - "Put the airdropped vids in the corresponding folder" means: take the newest `IMG_*.MOV` in `~/Downloads` (check the creation dates), make a new dated folder like the existing ones, then copy, `cmp`, and delete the Downloads copy.
  - Ask if the date or title is unclear.
- **Finished exports:** `/Volumes/Babi's 2TB/Babiontherun/Fall26/Exports/PERSONAL/`. Name them "<Mon D Title>.mp4".
- **Final Cut library:** `Fall26/Fall26 FCP12.3.fcpbundle` on this Mac (wide-HDR). Put XMLs in `<run folder>/XML/`.
  - **Check versions first.** This MacBook Air runs macOS 26 with Final Cut **12.3** (build 450152). Final Cut 12.4 needs macOS 27, so the App Store offers no update here.
  - `Fall26 20261018_1446_EDT.fcpbundle` was saved by **12.4** (its `CurrentVersion.plist` catalogVersion says `12.4`), so 12.3 refuses to open it. The Nov 13 Evan Genia user trims (10:32–10:38) are stuck in it.
  - Before promising to "open" a library, compare `catalogVersion` with the installed app's `CFBundleShortVersionString`. If the library is newer, either export XML from a Mac with 12.4 or rebuild from the run's XML into the 12.3 library.
  - To import XML into a new library: `open -a "Final Cut Pro Creator Studio" file.fcpxml`, then choose New… in the "which library" dialog.
- **Edits app** (Instagram Edits for Mac): exports go to `~/Movies/Edits/Exports/`. Copy the final export to Exports/PERSONAL, or to Downloads if it isn't a run vlog.
- Office or Stu work lives on `/Volumes/4TBSSD_4/Babi NR Content/`. That's the storytelling skill, not this one.

## Workflow
1. **Ingest** (as above), then probe with ffprobe. iPhone footage is HEVC 10-bit HLG, vertical (rotation −90), at mixed fps (24/30/60/120). Some clips have a second `apple_apac` spatial-audio stream, so always use `-map 0:a:0`.
2. **Transcribe** every clip with word timings: faster-whisper small.en, and medium.en for unclear lines. Read the whole transcript.
3. **Look** at contact sheets (`ffmpeg -vf fps=…,scale=-2:180,tile=…`) to see what each clip shows.
4. **Pick and cut** using the rules below.
5. **Build** in the tool the user asked for:
   - **Final Cut** ("put them in a timeline"): FCPXML with an event "<Mon D Title>", a project with the selects, and a `<note>` per clip. Import with File › Import › XML.
   - **Edits** ("open Edits"): pre-cut segments with ffmpeg, then import and assemble (see the Edits recipe).
6. **Verify** the export with ffprobe (duration, scene cuts, audio cross-correlation against the planned cut) and a frame sheet. Report what you checked and what you couldn't (you can't hear the mix).

## Cut rules for vlogs (from the user's re-edit of "Nov 11 Night Rain Run": 51.6 s → 35.3 s)
- **Cut B-roll with no talking.** They deleted a jacket-on shot.
- **Keep only 1–2 of any repeated reaction.** They cut 4 "Ah!" clips down to 1.
- **Trim each reaction to the sound itself:** just "Bruh" (0.55 s), just "argh argh argh" (1.3 s), a 0.8 s "Ah".
- **Split out pauses over about 1 s inside a sentence.** They removed 1.3 s from the middle of "feeling spectacular now … crazy how that shakers changed".
- **End right after the last spoken word.** Drop the trailing peace sign or gesture.
- **Ignore off-topic takes.** In the rain run that was the Golden Run Group "all paces welcome" promo takes.
- **Keep the main spoken lines in order:** intro (day count), the "I'm tired / it's raining" setup, the reactions on the run, then the outro ("of course I feel better… good night").
- **Never "fix" what he says.** He said "day 12" when the user called it day 11; it was kept as spoken.
- **Selects timeline** ("choose the good clips and put them all in a timeline"):
  - Use the last clean take of each retake.
  - Trim false starts and dead air, plus lines like "Alright, I'm filming already".
  - Keep shooting order, or story order when it reads better (e.g. "just got to Duncan's house" before "what are you guys doing").
  - Don't add music, captions or B-roll yet.
- **Surprise or friend moments** ("10K Cake Surprise", 35.6 s): setup line → confusion → the locked door → the reveal through "thanks guys" → one reaction line → candles → "I love you guys". Cut the long cheering stretches and the pause before the candles.

## Captions
- **Ask** each time unless the user already said. For example, the cake surprise was "no captions".
- **Vlog captions (Edits):** auto captions, **one word at a time, small (20pt), no commas, periods or question marks**.
- **Bold social captions** (Avenir Next Heavy, yellow key words) are the **babi-simple-reels** style; use them only if asked.
- **"Captions like this reference reel":** see babi-copy-format.

## Edits app recipe (computer use)
- **New project:** File › New project (via app_menu). Double-click the title to rename it. Media › Import (cmd+shift+G with a path works in the picker; type-select the folder name, then Return). Each project has its own media library.
- **Select all and drag:** select all clips in a media folder (click one, cmd+a) and drag them to the timeline. They land in name order, so name the segments C01, C02….
- **Bake audio into each segment.** Pre-cut segments **with their audio embedded**. A separate song dragged onto the audio lane landed 0.1 s late, and dragging couldn't fix it. When cutting a song into segments, slice it sample-exact (1600 samples per frame at 48 kHz/30 fps) so it plays back seamlessly.
- **Text layer:** Text › "None" style, typed through app_type on the AXTextArea, Classic font, size field (click the digits, app_type focused with overwrite), Effects › Soft Shadow. Move it with a slow full-screen drag (mouse down, several moves, mouse up). The background drag doesn't move it.
- **Auto captions:** CC › Generate captions › the plain small one-word template (row 4, column 1). Then set the size to 20 with "Apply to track" on. Then transcript › Replace: "." → "", "," → "", "?" → "".
- **Export:** use **File › Export project** from the menu, because the toolbar Export button sometimes misses. The output is 1440×2560 HLG.
- **Learn from the user's own Edits re-edit:** read `~/Movies/Edits/Libraries/*.bsledits/Projects/<id>/Timeline.db`, table `timelines.composition_data`, which is JSON. Each element has inPoint, outPoint and startTime; map `sourceMedia.id` to file names through `Media.db` `media_assets.name`.
- **Focus traps:**
  - Wispr Flow's overlay, Final Cut holding keyboard focus, and Notification Centre swallow clicks and keys. Request access to Wispr Flow and Final Cut, or use `app_*` tools with element_index.
  - Never type while focus is unclear: a stray Space or letter acts as a timeline shortcut.

## Funny vlog style (ez.romo) — Babi's v3 review, 2026-11-14
Evan Genia Run went v3 (53.5 s) → v4 (42.9 s). What Babi said:
- **Hook = the most energetic to-camera take, even if it drops info.** Use Evan's last take ("we're with Babi in Oakville and we're going for a run!", IMG_0179 42.66–45.95), not the "13th day…" take. The header text can carry the day count.
- **His name is "Babi"** (B-A-B-I). Whisper and the voice typer write "Bobby", so always caption it BABI. The uncle is **Genia**; when Babi says "how you feeling Gen" (whisper hears "sir" or "Zhen"), caption it GEN.
- **Captions were too big and ran off screen at 72/96 pt.** Use 50 pt, 62 for key words, and cap the width. Arial Black in FCP measures about **1.45 × fontSize px per capital**, so size ≤ 860 / (1.45 × letters). "NEIGHBORHOOD" ends up about 49 pt.
- **Preserve Pitch OFF on every speed change.** Babi turned it off on all retimed clips; the chipmunk and slow-mo voices are the joke. In FCPXML: `<timeMap preservesPitch="0">`.
- **Kept and praised:**
  - the uncle-at-the-house cutaway right when "my uncle" is said
  - the fly buzz after "scared the whole neighborhood away"
  - the slow-mo "he doesn't run" with a Vine boom
  - the bleeped swear (good technique, though that clip was cut this time)
  - the punch-in on "my uncle by the way"
- **Removed:** the air horn on "getting weird", the duck quack and the record scratch ("nice try, but not really it"). The air horn on "we got weird" stayed.
- **Cut every dead space ≥0.4 s, even inside a punch-in.** He flagged 0.9 s between "Genia's feeling good" and "this is my uncle". Find gaps with 20 ms RMS below (75th percentile − 15 dB) lasting ≥0.4 s, and keep ~0.1 s of air either side. This is stricter than the plain-vlog 1 s rule.
- **Add a yell insert after a "we scared everyone" line:** a speed ramp of 2× run-up then 0.5× scream, pitch off, with a whoosh peaking on the ramp. Here it came from the tail of the hook take (IMG_0179 45.95–47.00).
- **Trim long greetings.** In "hey / what's up dude / how's it going / this is my uncle", keep "we're getting weird, let's go weird" plus "this is my uncle… Evan".
- **Drop off-tone lines** even when they're funny: the "wear reflective sh*t" PSA.
- **Babi's v4 → v5 edit (2026-11-14):**
  - **Fewer SFX again.** Removed the fly buzz and whoosh after "neighborhood", the "5-10" punch-in and its boom, and muted the "we got weird" air horn. Only the wow (uncle's running shoes) and the final Vine boom (slow-mo "doesn't run") survived. Default to about two SFX per 40 s reel.
  - **Music bed −19 dB** (down from −13).
  - **Yell ramp:** the fast part runs **longer and not as fast** (1.3× from 45.73 to 46.45 s, not 2× for 0.43 s); the slow part is **shorter** (0.5× for 0.42 s source → 0.83 s on the timeline). Zoom 1.15, pitch off.
  - **Shave blank space right before an answer:** the uncle's "feel nice" now starts at IMG_0181 10.32, not 10.05.
  - **Slow-mo the last shout of a hype clip:** Evan's final "WEIRD" (IMG_0184 14.78–15.40) at 0.5×, pitch off.
  - Praised as-is: the hook + uncle preview up to 7 s, the shoe-tying cutaway, "this is my uncle… Evan", and the slow-mo "doesn't run" + Vine boom ending.
- Files: the v5 builder is `<run>/XML/build_v5_ezromo.py`.
- Files: the builder is `<run>/XML/build_v4_ezromo.py` (piece table, then a mock audio render → whisper → captions from the render's own transcript). The sound kit is in `<run>/Sound/`.

## Copying a reference reel
When the user gives a reference reel, also use **babi-copy-format**: it measures the drop, cut rhythm and caption style and applies them. This skill supplies the vlog taste, folders and tools.

## Updating this skill
This lives in the same skills repo as the others (see babi-storytelling's "Updating this skill").
1. Edit SKILL.md with the lesson: numbers, before/after, which video it came from.
2. Add a changelog line.
3. Commit and push.

## Changelog
- 2026-11-14 v0.4: Babi's v4 edit — fewer SFX, music −19 dB, yell ramp timing, slow-mo on a clip's last shout.
- 2026-11-14 v0.3: Babi's v3 notes on the ez.romo-style Evan Genia Run (hook, Babi/Gen captions, smaller width-capped captions, pitch off, 0.4 s dead-space cuts, yell ramp, which SFX stayed).
- 2026-11-14 v0.1: split from babi-storytelling. Run vlog rules from the Nov 11 re-edit, Edits recipe and captions, 2TB folder layout, selects timeline (Evan Genia Run), cake surprise cut, reference-reel versions.
- 2026-11-14 v0.2: Final Cut version trap (12.4 library vs 12.3 on macOS 26) and the new `Fall26 FCP12.3` library. Evan Genia tight cut v2: 92 s selects → 56.1 s.
