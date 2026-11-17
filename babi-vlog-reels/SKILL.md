---
name: babi-vlog-reels
description: Ariel ("Babi") playbook for simple vlogs and caption reels that are NOT storytelling recaps. Covers run vlogs (Babiontherun, run-every-day series), friend and day vlogs, surprise moments, and vlog-style reels with small on-screen captions. Covers moving AirDropped clips to the right folder on "Babi's 2TB", picking good clips, a selects timeline in Final Cut, tight vlog cuts in the Edits app or Final Cut, one-word captions, and exporting. Use for "make a vlog", "edit this run", "put the good clips in a timeline", "add captions". For a reference reel to copy, also use babi-copy-format. For to-camera promo reels, use babi-simple-reels. For talking-head storytelling recaps with B-roll bursts, chat pops and music (Stu / office reels), use babi-storytelling instead.
---

# Babi vlog and caption reels

**Shared settings and tools: read `~/.claude/babi-skills/shared/SETTINGS.md` first.** It covers Rec. 709 projects, the Instagram safe zone, caption geometry, working on Babi's own edit in place with Replace, Final Cut import gotchas, and the helper scripts. It applies to every Babi skill.

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
- **Repeated line = use the LAST take** (Babi, 2026-11-16, Day 17 run): "if I say the same line multiple times, the last one is usually the good one, because that's when I was satisfied and stopped re-recording." This holds across clips too, not just inside one:
  - Day line said in IMG_0572 and again in IMG_0576 → 0576. "I got it done" (0584) vs "we got it done" (0585) → 0585. Two outros ("have a good night" in 0585 and 0586) → keep only 0586's.
  - Inside a clip: "but honestly it's kind of nice to… but honestly it's kind of nice" → second one; "keep your… keep your perspective intact" → start at the second "keep".
  - Whisper can merge a restart into one line with wrong word times (it put "Keep your perspective" at 2.1 s when the kept take starts at 4.33 s). Re-transcribe the rendered cut; a doubled phrase there means a retake slipped in. Find the real onset with 50 ms RMS.
- **A stranger / street moment** ("I came up to some random dude"): keep the whole ask and the answer in one piece (13.7 s on Day 17, including the ~1.3 s wait before the "No"), then his reaction lines after it.
- **Never "fix" what he says.** He said "day 12" when the user called it day 11; it was kept as spoken.
- **Selects timeline** ("choose the good clips and put them all in a timeline"):
  - Use the last clean take of each retake.
  - Trim false starts and dead air, plus lines like "Alright, I'm filming already".
  - Keep shooting order, or story order when it reads better (e.g. "just got to Duncan's house" before "what are you guys doing").
  - Don't add music, captions or B-roll yet.
- **Surprise or friend moments** ("10K Cake Surprise", 35.6 s): setup line → confusion → the locked door → the reveal through "thanks guys" → one reaction line → candles → "I love you guys". Cut the long cheering stretches and the pause before the candles.

## Captions
- **Ask** each time unless the user already said. For example, the cake surprise was "no captions".
- **Vlog captions in Final Cut (Day 17 run, 2026-11-16):** the storytelling caption look (Basic Title, Helvetica Neue Bold, white, soft shadow, lowercase, no punctuation) but **one word per title**, "pretty small" = size 40, **every title the same size**, a little below the middle (Position `0 -165`, ≈ y 1235). Time them from the cut's own audio. Builder: `scripts/build_day17_example.py` (from-scratch FCPXML, mixed-fps iPhone clips, 30 fps Rec. 709 project). Not yet reviewed by Babi.
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
- **Write an Edits timeline directly (exact, no clicking)** — tested 2026-11-16 on "would you slap your boss for...":
  - Project names are in `Library.db` `project_refs` (Project.db's own name can be stale). Text layers are elements on a `trackType: "overlay"`, `timelineBehavior: "free"` track; copy a plain one (`content.text._0` with `text`, `style.fontFamily/fontSize`, `effectTypeRaw` e.g. `text_soft_shadow`, `transform.position` in px from frame centre, y down). Times are `{value, timescale}` (600 works).
  - **Quit Edits first** (`osascript -e 'tell application "Edits" to quit'`), write, then `open -a Edits`.
  - **Store `composition_data` as a BLOB** (`json.encode('utf-8')`). Writing it as TEXT made Edits say "Unable to open project … may be corrupted".
  - **Back up the whole project folder including `-wal`/`-shm`**: the live data sits in `Timeline.db-wal`; restoring only `Timeline.db` gives an empty DB. Builder: `babi-copy-format/scripts/build_slap_edits.py`.
  - Size calibration, IGUIBetav9-Heavy: **20** ≈ the reference's IG-native caption (2 lines, second line ~66% of frame width); 30 was 1.5× too big and wrapped to 3 lines. Position y +40 → caption centre ~51% down.
- **Edits captions, tested 2026-11-14 ("Evan Genia Run - Edits captions", next to "- FCP captions" for comparison):**
  - Import with **File › Import Media** from the menu (cmd+shift+G a full file path, then Return twice). Wispr Flow's floating window blocks clicks on the Import button.
  - Captions › Generate captions (All audio, Auto-detect). Pick the bold one-word template (Captions › All, row 2, middle). It shows one word at a time.
  - **Fix the transcript in Captions › Edit:** each line is an AXTextArea. Use `app_type` with mode=replace on its element_index; the result echoes the old text, which confirms you're on the right line. **Re-run `app_ax_find` after every scroll, and map indices by y-position**: one batch hit the wrong lines because the first index belonged to the line above. Retyping each line removes the punctuation and fixes the mishearings in one pass. Edits mishears Babi as "Wood Bobby", Gen as "Jay", Genia's as "Jen is", and "Oh" as "How?". Replacing a line with an empty string blanks a noise caption ("Whoa").
  - **Style matched to the FCP captions:** Style › Capitalization **AA** (all caps), font size **26 pt** (about the FCP width; 36 pt was ~66% of frame width), Effects › **Black Offset** for the outline look. Apply to track is on by default.
  - **Header text:** Text › None at the playhead, then type the lines with `app_type`. In the font size field, double-click the digits, type, and press **Tab**. Return doesn't commit, and it starts playback. Use 17 pt. Drag the box in the viewer with `app_drag` (several path points) to about 20% from the top and centred, then Effects › Soft Shadow. Stretch the clip's right edge to the end of the hook.
  - Final Cut's File › Share is blocked for Claude, so Babi exports with ⌘E. Claude can do Export XML.
- **Focus traps:**
  - Wispr Flow's overlay, Final Cut holding keyboard focus, and Notification Centre swallow clicks and keys. Request access to Wispr Flow and Final Cut, or use `app_*` tools with element_index.
  - Never type while focus is unclear: a stray Space or letter acts as a timeline shortcut.

## Funny vlog style (ez.romo)
Use **babi-ezromo-style**: it holds all of Babi's v3–v5 notes, the builder and the helpers. General vlog rules from that work that apply everywhere:
- Caption his name **BABI** (whisper says "Bobby"). The uncle is **Genia**, nickname **Gen**.
- Keep text inside the Instagram safe zone (top 250 px, bottom 320 px, 120 px sides, right buttons x > 845 / y > 1130).
- **Captions are made in Final Cut by default** (Babi compared FCP and Edits captions on 2026-11-14 and chose FCP). Use the Edits recipe below only when asked.
- Iterate on Babi's own edit in place (Export XML → patch → re-import with Replace) instead of new versions.

## Copying a reference reel
When the user gives a reference reel, also use **babi-copy-format**: it measures the drop, cut rhythm and caption style and applies them. This skill supplies the vlog taste, folders and tools.

## Updating this skill
This lives in the same skills repo as the others (see babi-storytelling's "Updating this skill").
1. Edit SKILL.md with the lesson: numbers, before/after, which video it came from.
2. Add a changelog line.
3. Commit and push.

## Changelog
- 2026-11-16: last take wins for any repeated line (also across clips); stranger moment kept whole; one-word Final Cut vlog captions (size 40, y≈1235); `build_day17_example.py`.
- 2026-11-16: write Edits timelines directly (blob, quit first, back up WAL), IGUIBetav9-Heavy size calibration.
- 2026-11-14: shared settings/tools moved to `shared/SETTINGS.md` (applies to all Babi skills).
- 2026-11-14 v0.7: ez.romo details moved to babi-ezromo-style; Final Cut captions are the default.
- 2026-11-14 v0.6: Edits auto-caption recipe tested end to end (transcript fixes via AXTextArea, caps, 26 pt, Black Offset, header).
- 2026-11-14: projects always Rec. 709 (sequence format colour space).
- 2026-11-14 v0.5: IG safe zone (Babi's overlay), smaller 40/48 captions capped at 590 px, header below 250 px, no tracker, iterate in place with Replace.
- 2026-11-14 v0.4: Babi's v4 edit — fewer SFX, music −19 dB, yell ramp timing, slow-mo on a clip's last shout.
- 2026-11-14 v0.3: Babi's v3 notes on the ez.romo-style Evan Genia Run (hook, Babi/Gen captions, smaller width-capped captions, pitch off, 0.4 s dead-space cuts, yell ramp, which SFX stayed).
- 2026-11-14 v0.1: split from babi-storytelling. Run vlog rules from the Nov 11 re-edit, Edits recipe and captions, 2TB folder layout, selects timeline (Evan Genia Run), cake surprise cut, reference-reel versions.
- 2026-11-14 v0.2: Final Cut version trap (12.4 library vs 12.3 on macOS 26) and the new `Fall26 FCP12.3` library. Evan Genia tight cut v2: 92 s selects → 56.1 s.
