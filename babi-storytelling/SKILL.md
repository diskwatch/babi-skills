---
name: babi-storytelling
description: Ariel's ("Babi") storytelling video editing playbook. The goal is videos like "Stu Queens Recap 1" (QSELF Stu recap, TME library), with great B-roll, well-timed sound effects, tight pacing and the right song. Use when cutting a talking-head storytelling reel, recap, vlog or short-form video in Final Cut Pro (or Edits). This includes picking the best takes from producer-led recordings, tightening dead air, laying B-roll, popping chat or Zoom screenshots with sound effects, choosing music and captions, and importing the edit as FCPXML into the TME library. Also use when the user asks Claude to "learn from my edit" or update this skill. Early version, still improving.
---

# Babi Storytelling

**Shared settings and tools: read `~/.claude/babi-skills/shared/SETTINGS.md` first.** It covers Rec. 709 projects, the Instagram safe zone, caption geometry, working on Babi's own edit in place with Replace, Final Cut import gotchas, and the helper scripts. It applies to every Babi skill.

This is how Ariel ("Babi") wants storytelling videos cut. The usual subject is Stu talking to camera, with B-roll from the office or events, made into vertical reels in **Final Cut Pro**.

Claude builds a first cut as **FCPXML**, imports it into the **TME** library, and the user refines it by hand. Every rule below came from the user's own fixes to Claude's cuts. Follow them before your own taste.

> **This skill is a living document.** Whenever the user corrects an edit, apply the "When the user edits Claude's cut" section, then add the lesson here with measured numbers and before/after examples. Commit and push the change to the skill's GitHub repo (see "Updating this skill").

## The target: "Stu Queens Recap 1"
This is the gold standard for what these videos should feel like (TME library, a 73 s vertical recap of the Queen's QSELF talk). Before building a new storytelling video, export its XML and study it. What makes it work, measured from its timeline:
- **Pacing:**
  - The talking head is cut into about 30 short pieces (0.4–6.7 s), with no dead air.
  - The story moves every few seconds.
- **B-roll:**
  - Rapid bursts of about 0.8 s per shot, 3–6 shots in a row, on a connected storyline, all muted (−96 dB).
  - The bursts show exactly what Stu is talking about at that moment: the event, the crowd, the venue, the people.
  - Between bursts, the talking head comes back so the viewer reconnects with Stu.
- **Opening:**
  - Stacked graphics (screenshots and logos: Laurier, Queen's, QSELF) on lanes 1–3, scaled to about 0.45–0.8 and offset from centre.
  - A Ding on the first reveal and a pop on each later reveal.
- **Sound effects:** Ding at about −16 dB, pop at about −14 dB, timed to the frame each graphic lands. Used sparingly, at story beats.
- **Music:** "Skyfall", started partway into the song (37 s) so its energy fits. Volume keyframes ride it from about −8 dB in the intro down to −12 to −16 dB under speech, then out at −21 dB.
- **Alternates:** a few disabled clips (`enabled="0"`) are left in the timeline as options.

When a cut is done, compare it against this checklist. Is the B-roll on-topic and quick? Do the sound effects land on beats? Is there any dead air? Does the song fit the emotion?

## Quick rules (read first)
1. **Start lines on the first real word.** Drop lead-ins like "And", "So", "But", "He said".
2. **Cut every pause of about 0.1 s or more**, including pauses inside a line.
3. **Never leave silent holds.** Put graphics over speech instead.
4. **Use the take that flows into the next line**, and re-check each chosen take on its own for hidden restarts.
5. **Skip takes with laughing or stumbles.**
6. **Do the edit in Final Cut** (an FCPXML import into TME), not as a rendered file, so the user can refine it.
7. **For uncertain or name-dependent B-roll,** stack options and leave only one enabled.
8. **Chat pops:** no animation, about 0.1 s apart, a pop sound on the exact frame, all ending at a hard out point.
9. **Keep overlays off the speaker's face, and off anything key in the shot** (a board, a product, a screen) unless a full-screen burst is wanted. Check on tiled frames (see shared SETTINGS, "Don't block what matters").
10. **Ask about captions and music for each video.** Defaults are in the sections below.
11. **B-roll bursts start on a spoken word and cut on the beat grid (Option-B).** Show real people reacting, literal to the words. Build a burst by **jump-cutting through ONE clip** (3–5 pieces of the same take) rather than mixing many clips.
12. **When the user marks a spot (a marker), the graphic lands exactly on that marker frame.**
13. **Keep every XML on the SSD**, in `Media/OFFICE/<Mon D Topic>/XML/`, never on the Desktop.
14. **"Update that project" means replace it in place.** Export it first as a backup to the SSD XML folder, then import with the same project name and choose **Replace**.

## Where things live
- **Library:** `/Volumes/4TBSSD_4/Babi NR Content/Libraries/TME.fcpbundle`. The `<library>` element needs `colorProcessing="wide-hdr"`.
- **Media:** `/Volumes/4TBSSD_4/Babi NR Content/Media/OFFICE/<Mon D Topic>/`. Copy new footage there from `~/Downloads` before importing, and put B-roll and screenshots in subfolders.
- **Music:** `/Volumes/4TBSSD_4/Babi NR Content/Songs/`. Storytelling reels use `STORYTELLING/Jack Style/`.
- **Sound effects:**
  - Pop: `Sound FX/click and keyboard/Censor sound __ … Pop sound … .mp3`. Use the **short pop at 0.997 s for 0.12 s, −14 dB**. Its transient is at 0.999 s, so the sound lands on the frame.
  - Ding: `Songs/SOUND FX/Ding - Sound Effect (HD)…mp3`, from 0.21 s for 0.85 s at −16 dB.
- **Reference edit for style:** the "Stu Queens Recap 1" project in TME.

## Workflow
1. **Ingest.** Copy the clips to the SSD media folder. Probe them with ffprobe (all iPhone HEVC 10-bit HLG, 1080×1920, 30/59.94/60 fps).
2. **Transcribe.** `scripts/transcribe.py` gives word timings (medium.en). Use a throwaway venv with `faster-whisper pillow`; the models are cached in `~/.cache/huggingface`. Recordings with a producer are full of retakes, so read the whole transcript before choosing.
3. **Pick takes.** Take the last clean take of each scripted line. **Babi's on-camera cue (2026-11-16):** when he says "that's the one" in a recording, the take just before it is the pick, even if he retakes after. If no cue, the last clean take wins; but when the last take has a stumble or a long stall mid-line ("Michi… she and myself"), use the earlier clean take. Then re-transcribe each chosen take **on its own**: a take that reads clean in the full transcript can hide a restart (for example "because there came a point… because there was a point…").
4. **Cut tight** (the user's rules, measured from their edit: 80.5 s → 72.2 s):
   - **Start each line on its first content word.** Drop lead-ins like **And, So, But, He said, Okay, Whether**. Examples: "~~And~~ people absolutely loved it", "~~So~~ Marcus, one of our developers…".
   - **Cut every pause inside a line that's about 0.1 s or longer.** The user removed gaps as short as 0.08 s. Split the clip at breaths. Claude's old 0.30 s threshold was far too loose.
   - **Never leave a silent hold** in the talking. The user removed a 3.4 s silent beat Claude added for chat pops. Overlays go *over* speech, not in gaps.
   - **Prefer the take that connects.** Example: "the important thing is it's where people already work… and that's when the chat absolutely lost it" beat the standalone "that's when the chat absolutely lost it".
   - **Find real cut points in the audio.** Whisper's word ends run long. Find the true end in 10 ms RMS energy, and listen for trailing "s" sounds.
   - **Verify by ear:** render the cut audio with ffmpeg, transcribe it, and confirm every word is intact. Words flagged low-confidence (<0.6) usually mean a clipped word.
5. **B-roll** (learned from the user's own picks in "Creator Lab Reel - chat pops", 2026-11-13. They deleted Claude's first pass: "you don't understand what good B-roll is"):
   - **What to show: real people and real emotion.** Faces laughing and reacting, high-fives, the team watching Stu on the big TV in the lab room, slides on the TV. **Not** empty rooms, floors, shaky pans or generic desk shots.
   - **Be literal to the words.** The user's picks:
     - "I watched the chat absolutely lose it" → team laughing at the TV (IMG_9856 @3.9 s)
     - "a major announcement" → Stu high-five / reaction (IMG_9855 @5.4 s)
     - "Black Friday" → Black Friday slides on the lab TV (IMG_9874 @19.8 / 21.5 / 24.3 s)
     - "people absolutely can't wait to buy" → developer laughing at his desk (IMG_9884 @1.6 / 3.3 s)
     - "I run a workshop" → speed-ramped walk from the lab room into Stu's studio (IMG_9865, retime Fast 1091% then 149%)
   - **Shot length:** about 0.6–1.2 s each (the user's own range was 0.37–1.2 s), 3–5 shots per burst.
   - **One clip per burst, jump-cut** (learned from the user's own B-roll in "Creator Lab Reel - chat pops", 2026-11-13). They took one take and cut 3–5 moments out of it, each placed in a connected storyline:
     - "loved the training" → IMG_9890 @1.9 / 3.6 / 5.1 s: the team crowding round a developer's screen (1.1 s each)
     - "teach the training… brand new tool" → IMG_9892 @1.5 / 3.2 / 5.0 s: a team member in green walking through the office (a follow shot)
     - "after the workshop they'd log off" → **the same walker** IMG_9892 @6.7 / 7.7 / 9.4 / 13.3 s heading into the studio. A follow shot that continues across two lines works like a mini story.
     - "Marcus, one of our developers" → IMG_9883 @6.4 / 7.6 / 8.8 s (Marcus smiling, 0.7 s each). Use this clip for Marcus.
     - "it's a doorway" → IMG_9901 @3.9 / 4.8 / 5.9 / 7.4 / 17.5 s (a pan from the developer to a colleague, 0.37–0.65 s)
     - "where you're already working" → IMG_9900 @2.7 (one shot, 1.1 s)
   - **Don't skip a clip because it has no Final Cut uid.** The user's favourites (IMG_9892, IMG_9901) were ones Claude avoided for that reason. Export the event, or let the import add the clip.
   - **Timing (the most important part):**
     - **A burst starts on a word Stu is saying**, the key word of the phrase. Not on a beat, not on a clip boundary. Example: the burst at 12.78 s starts on "absolutely … can't wait to buy".
     - **Cuts inside a burst land on the song's beats.** Final Cut's beat-detection grid (Option-B in the timeline) shows them; the user cut at 9.33, 9.97, 10.58 and 13.68 s, all on that grid. Compute the same grid with `librosa.beat.beat_track` on the song: **FCP grid ≈ librosa beat time − 0.04 s**. Convert song time to timeline time by subtracting the song clip's source start offset (and adding its timeline offset).
     - **A burst usually ends near the end of the talking-head clip**, so the next line opens on Stu's face. In the user's own edit only 1 of 5 bursts ended exactly on a clip end; others ran 0.25–0.5 s past it or stopped 0.3–0.5 s short. Treat it as a guide, not a hard rule.
     - Between bursts, Stu stays on screen for at least the start of each line.
   - Mute B-roll (−96 dB) in most picks. Put it on connected lanes above the talking head.
   - **Name-dependent spots** (e.g. "Marcus, one of our developers"): stack 2–4 options on lanes, **one enabled and the rest disabled** (`enabled="0"`, the V key).
   - **Before choosing, build a contact sheet** of candidate in-points: grab a frame at each in-point with ffmpeg, tile them with Pillow, and look at it. Check every chosen in-point frame, not just the clip's thumbnail.
   - Add keyword ranges to the event clips (laughing, reactions, screens/slides, chat, team, Stu teaching) so the user can browse alternates.
6. **Chat and screenshot pops** (exact recipe the user asked for):
   - **Opening burst:** 9 screenshots about 0.1 s apart (the user cut Claude's 11 down to 9, dropping the two long, wordy ones: 3.13.26 and the long 4.14.55 paragraph). Short, punchy bubbles only. Delete disabled alternates nobody asked for.
   - **A later "the chat lost it" moment:** about half as many (5), **slower and slowing down**, so each can be read. The user re-timed Claude's run (0.27 / 0.32 / 0.35 / 0.42 s) to **first pop 0.2 s into the line, then gaps of 0.32 / 0.35 / 0.42 / 0.50 s**, ending 0.1 s before the clip end. Put all the pop sounds on one lane (−1). Each still gets a pop. Pick fresh, exciting lines ("OMG LOVE IT!", "I got it working already!!", "I'm using Claude… Let's GOOOOO!", "50% off bundle…"), and finish on the big chat flood. Lay them out so nothing hides an earlier bubble's text.
   - **Logos at a marker** (e.g. ChatGPT + Claude when Stu says "where you're already working"): the first logo lands on the marker frame and the second 0.35 s later, each with a **Ding** (−16 dB). Place them side by side in the lower third (x ±12 %, y −27 %, about 340 px wide) and hold them until the clip end after the names are spoken. The user **disabled the B-roll under the logos** (IMG_9900), so logos sit over Stu, not over B-roll. They also cut the repeated line "the important thing is it's where people already work" once the logos carried that idea. App logos come from the installed apps' icons (`iconutil -c iconset /Applications/X.app/Contents/Resources/*.icns`); copy them to `Media/OFFICE/<topic>/Logos/`.
   - **No animation.** Each screenshot simply appears.
   - Space them about 6–7 frames apart (~0.1 s).
   - Give each one its own lane, or they hide each other.
   - Put a pop sound on exactly the same frame as each screenshot.
   - Each screenshot holds until a hard out point (for example, the start of the next line's clip), then all of them vanish together.
   - Over the talking head, keep them off Stu's face (lower third). Fill the whole frame only where the user asks for a burst.
   - `scripts/add_broll_on_beats.py`: adds a B-roll pass to an exported copy of the user's edit. Each burst starts on a word, cuts on beats (librosa grid − 0.04 s ≈ Final Cut's Option-B grid) and ends on the talking-head clip's end. Edit the BURSTS table; it needs `beats.json` from librosa `beat_track`, converted to timeline time.
- `scripts/add_chat_pops.py` adds this to an **exported copy of the user's own edit** and leaves everything else untouched.
7. **Music.**
   - Ask which song, or choose from `STORYTELLING/Jack Style`. The user chose "Every Living Breathing Moment" (the Grant Steller piano cover) over Claude's "In Motion".
   - Put it on a single lane at a flat level (the user used −13 dB). Don't add elaborate volume keyframes unless asked.
   - Trim the music to end with the video. A song longer than the cut makes the project longer than the video.
8. **Captions.** Ask for each reel. For Babi's own talks (Nov 16) he chose the **knowledge-reel karaoke style, smaller**: size 46, Position `0 -335` (≈ y 1533), lane 6 above B-roll and pops; move graphics up so they end above ≈ 1475 px. Run `scripts/add_captions.py` on an export, then Replace. The Black Friday reel used one word at a time, Avenir Next Heavy, white with a black outline, and key words/numbers in yellow. Creator Lab had none.
9. **Import and verify.**
   - Import with File → Import → XML.
   - Check frames in the viewer with Control-P plus a typed timecode. Don't click the ruler.
   - Report what you checked and what you didn't (you can't hear the mix).

## When the user edits Claude's cut
- Export their project XML (focus the timeline first, then File → Export XML).
- Diff it against Claude's plan: which takes they swapped, trim offsets at the start and end of lines, gaps removed, B-roll picks, music, sound effects.
- Write the lesson into this file. Add measured numbers and before/after examples, not vague adjectives.
- Never overwrite the user's project. Add changes to a copy of their export and import it under a new name (for example "… - chat pops").

## Versions and exports
- **The user asks for A/B/C versions** ("as is", "without these clips"). Build each as its own project from an export of their timeline:
  - Remove whole spine clips; their connected B-roll goes with them.
  - Ripple the later offsets.
  - Trim connected clips that overhang into a removed part (e.g. the logos).
  - Remove the pop sound along with its screenshot.
  - Trim the music to the new length, or the video ends on black.
- Name them "<Title> V1/V2/V3" and import them side by side.
- **"Rewatch them":** rebuild each version's dialogue from the spine clips' source ranges (numpy plus the 16 kHz wav) and transcribe it with medium.en. Read the joins at each cut.
- **Claude can't press Share / Export File in Final Cut** (the computer-use grant blocks Share items). Ask the user to press ⌘E for each project. Exports go to `/Volumes/4TBSSD_4/Babi NR Content/Exports/OFFICE/`.
- **Edits app captions** for these reels: a single line, with no commas, periods or other punctuation.

## FCPXML gotchas (all hit in practice)
- **Asset IDs:** reuse the `uid`s Final Cut assigned (get them from an export) and leave unused assets and event clips out, or a re-import duplicates media. The TME event "Nov 12 Black Friday" has uid `8CDA26A5-601A-4C11-984C-85B9695F137E`.
- **Title text:** `font` must be an installed family (SF Pro is not; use Avenir Next / Heavy). `strokeWidth` must be **negative** for fill plus outline. `shadowOffset` is "distance angle".
- **Overlapping connected clips:** they need separate lanes.
- **Stills:** they start at `3600s`. Position units are % of frame height (y+ is up); scale is relative to the fitted size.
- **The Import/Export dialog can open on either display** (DELL or built-in). Check `app_list_windows` bounds before typing, or the keystrokes hit Final Cut as shortcuts (E appends, B blades…).
- **Background `app_click` doesn't move Final Cut's focus.** Use a full-screen click to select the clip, event or timeline before Export XML.
- **Corner brackets in the viewer** around a parked title or still are on-screen guides only.
- **Timecode format:** 0:03:01 means 3 s + 1 frame at 60 fps. `ctrl+p` then digits jumps there.

## Scripts
- `scripts/transcribe.py`: word-level transcripts.
- `scripts/build_reel_template.py`: the Creator Lab first-cut builder (talking-head pieces, B-roll with disabled alternates, pops, sound effects, music, keyword collections). Copy it and edit the LINES/BROLL/POPS tables. Update its cutting thresholds to the rules above (lead-in words, ~0.1 s gaps, no silent holds) before relying on it.
- `scripts/add_chat_pops.py`: adds synced chat-screenshot pops to an exported copy of the user's edit.
- `scripts/make_versions.py`: builds V1/V2/V3 projects from an export by removing spine clips (ripple, overhang trims, music trim).
- `scripts/add_logos_and_pops.py`: logos with dings at the project's marker, plus a slower, readable screenshot pop run. It uses the "Fit" scale maths (width in px → scale). Screenshot filenames have a narrow no-break space before "PM", so glob them. After the first import, export again and copy the uids Final Cut gave the new stills into the XML before re-importing, or the media gets duplicated.
- `scripts/broll_pool_example.json`: format for a tagged B-roll pool.

## Other formats the user has asked for
- **Run vlogs / day vlogs** (Edits app or Final Cut):
  - Cut B-roll that has no talking.
  - Keep only 1–2 of any repeated reactions, and trim each to the sound itself ("Bruh", a 0.8 s "Ah").
  - Split out pauses over 1 s inside sentences.
  - End right after the last spoken words, with no trailing gesture.
  - Captions: auto captions, one word at a time, small, no commas or periods.
- **Silence removal on long talks:** cutting on loudness alone (−40 dB, 0.5 s gaps) was judged "pretty bad". Cut on word timings from the transcript instead, using the tightening rules above.
- **Social captions (Black Friday reel):** one word at a time, Avenir Next Heavy, all caps, white with a black outline and soft shadow, just below centre. Numbers and key words go in yellow. No punctuation.

## Personal storytelling talks (Babi on camera, Babi's 2TB)
Learned 2026-11-16 ("Golden Run One Month" 55.7 s, "Give Oakville Charity" 135.4 s):
- These are Babi talking to camera about runs and events; footage lives on **Babi's 2TB** (`Fall26/Media/Vlogs/<Mon D Title>/`), not the 4TB. Import into `Fall26 20261018_1446_EDT.fcpbundle`, one event per talk. When the 4TB is unmounted, songs are in `/Volumes/Babi's 2TB/Songs/STORYTELLING/` (same Jack Style folder) and SFX in `Songs/SOUND FX/` (Ding at 0.21 s; "Cute Pop" transient at 0.77 s).
- B-roll comes from the earlier day folders: read the old builders' `<note>`s and the clips' own audio (small.en) to find who is who (e.g. Alix = Oakville Community Foundation; IMG_9775 = the Nov 8 FaceTime call; IMG_0427 = Michi and Babi meet Alix at Give Oakville).
- For a named charity with no footage, screenshot its own site (start2finishonline.org) and pop 3 crops in the lower band under the chin (y 1060-1590, x 120-845), Ding on the first, pop on the rest.
- Cutting tool: RMS-refine each line's edges, then split pauses >= 0.12 s, but mark an edge **exact** where the refine pulls a dropped lead-in back in ("So", "said", "Like"); re-transcribe the render and fix every stray lead-in. Builder: `Nov 16 Give Oakville Charity Talk/XML/build_talks.py` (bursts start on a word, cut on librosa beats - 0.04 s).

## Knowledge / teaching reels
Teaching reels (Stu explaining numbers or a framework, Toni Blog, Hal Eldro, Black Friday Knowledge) moved to **babi-knowledge-reels**: internet photos with pops, karaoke captions, section headers, dollar figures and a board zoom.

## Personal vlogs and caption reels
These moved to the separate skill **babi-vlog-reels** (repo `diskwatch/babi-vlog-reels`): run vlogs on Babi's 2TB, the Edits app recipe, and one-word captions.

## Setting up on a new Mac
1. Run `gh auth login`, then `git clone https://github.com/diskwatch/babi-skills.git ~/.claude/babi-skills`, then symlink each skill: `for d in ~/.claude/babi-skills/*/; do ln -s "$d" ~/.claude/skills/$(basename "$d"); done`.
2. Install Homebrew `ffmpeg`. For transcription, make a throwaway venv (`python3 -m venv … && pip install faster-whisper pillow`). The first run downloads small.en and medium.en (~1.5 GB).
3. In the Claude desktop app, turn on Computer use (Settings) and grant Screen Recording and Accessibility when macOS asks.
4. Start Claude Code sessions in the same folder each time, so memory notes stick. Put anything important in this skill, because memory doesn't sync between Macs.
5. Before editing, `git -C ~/.claude/babi-skills pull`. After any lesson, commit and push from `~/.claude/babi-skills`.
- Toolchain gotchas: PyAV 1.2.1 breaks `transcribe(path)`, so pass a 16 kHz float32 numpy array. Homebrew ffmpeg has no `drawtext`. iPhone footage is HEVC 10-bit HLG; keep it HDR.
- Overlays that block clicks: Wispr Flow's floating pill, Final Cut grabbing keyboard focus, Notification Centre. Request access to Wispr Flow / Final Cut, or use the background `app_*` tools with element_index.

## Updating this skill
All five Babi skills (babi-storytelling, babi-vlog-reels, babi-simple-reels, babi-copy-format, babi-ezromo-style) live in ONE private repo, `diskwatch/babi-skills`, cloned at `~/.claude/babi-skills`. Each skill folder is symlinked into `~/.claude/skills/<name>`. The old `diskwatch/babi-storytelling` repo is retired; don't push there.
1. Edit `SKILL.md`, or the scripts, with the new lesson. Keep it concrete: numbers, before/after, the clip or project it came from.
2. Add a line to the changelog below.
3. Commit and push: `cd ~/.claude/babi-skills && git add -A && git commit -m "<skill>: <lesson>" && git push`. On the other Mac, `git -C ~/.claude/babi-skills pull` gets the update.

## Changelog
- 2026-11-16: captions on talks = knowledge karaoke style at size 46 (add_captions.py).
- 2026-11-16: "that's the one" take cue; personal storytelling talks on the 2TB (folders, songs, charity-site pops, exact-edge cuts).
- 2026-11-14: shared settings/tools moved to `shared/SETTINGS.md` (applies to all Babi skills).
- 2026-11-14: projects always Rec. 709 (sequence format colour space).
- 2026-11-14 v0.7: moved into the shared repo diskwatch/babi-skills alongside vlog-reels, simple-reels and copy-format.
- 2026-11-14 v0.6: run vlog and Edits material moved to the new babi-vlog-reels skill; this skill stays storytelling-only.
- 2026-11-14 v0.5: personal run vlog workflow on Babi's 2TB (folders, Fall26 library, selects string-out), Edits app recipe, new-Mac setup checklist.
- 2026-11-13 v0.1:
  - First version, from:
    - the Stu Queens Recap silence-removal feedback
    - the run vlog trims
    - the Black Friday reel (captions, best takes)
    - the Creator Lab reel (the user's tightening from 80.5 s to 72.2 s, music choice, the chat-pop recipe)
  - B-roll taste was still to be learned (resolved in v0.2).
- 2026-11-13 v0.4: user's re-timed slow pop run, logos over Stu (B-roll disabled), versioned exports (V1/V2/V3) and the rewatch-by-transcript check.
- 2026-11-13 v0.3:
  - B-roll as one-clip jump-cut bursts, from the user's own picks.
  - The clip-end rule loosened.
  - Opening pops trimmed to 9 short ones.
  - A slower second pop run.
  - Logos with dings at a marker.
  - XML lives on the SSD; "update the project" means Replace.
- 2026-11-13 v0.2: B-roll taste and timing learned from the user's Creator Lab picks (word-start / beat-cut / clip-end rule, Option-B beat grid ≈ librosa − 0.04 s).
