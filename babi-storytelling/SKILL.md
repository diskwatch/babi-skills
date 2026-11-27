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
0. **Shared core rules first** (`shared/SETTINGS.md` › Core rules, 2026-11-27): no dialogue boost, edge recoveries, captions on the chest, headers that don't give away the payoff, a song on every reel, photo pops.
1. **Start lines on the first real word, but keep connectives inside a story.** Drop stutters, false starts and the reel's very first filler. Keep And / So / But when they start a sentence mid-story: Babi restored 12 of them on Laurier, 2026-11-27. Never cut into the first word: start ≈ 0.06 s before the RMS onset.
2. **Cut real pauses** (≈ 0.25 s+ on moving or panel speakers; ≈ 0.1 s only on scripted to-camera takes), and trim silent heads and tails to the onset and decay (+0.08 s). Let the reel's last line and laugh breathe.
3. **Never leave silent holds.** Put graphics over speech instead.
4. **Use the take that flows into the next line**, and re-check each chosen take on its own for hidden restarts.
5. **Skip takes with laughing or stumbles.**
6. **Do the edit in Final Cut** (an FCPXML import into TME), not as a rendered file, so the user can refine it.
7. **For uncertain or name-dependent B-roll,** stack options and leave only one enabled.
8. **Chat pops:** no animation, about 0.1 s apart, a pop sound on the exact frame, all ending at a hard out point.
9. **Keep overlays off the speaker's face, and off anything key in the shot** (a board, a product, a screen) unless a full-screen burst is wanted. Check on tiled frames (see shared SETTINGS, "Don't block what matters").
10. **Captions and music are ON by default.** Don't stop to ask. Use the caption table in the shared core rules. In a batch, vary the songs (repeats are fine, but not all the same). Babi turns either off if he wants.
11. **B-roll bursts start on a spoken word and cut on the beat grid (Option-B).** Show real people reacting, literal to the words. Build a burst by **jump-cutting through ONE clip** (3–5 pieces of the same take) rather than mixing many clips.
12. **When the user marks a spot (a marker), the graphic lands exactly on that marker frame.**
13. **Keep every XML on the SSD**, in `Media/OFFICE/<Mon D Topic>/XML/`, never on the Desktop.
14. **"Update that project" means replace it in place.** Export it first as a backup to the SSD XML folder, then import with the same project name and choose **Replace**.

## Rules from past rounds (details and examples in LESSONS.md)
Each rule came from a correction Babi made. The dated sections in `LESSONS.md` have the measured numbers, clips and builders. Read the matching one before building that kind of reel: Nov 16 talks, Give Oakville, Q&A hypotheticals, Immersion Day story, raw-retake stories, compound-clip captions, charity promo overlays, Laurier.
- **B-roll timing:**
  - A burst starts ≈ 2 frames before the key word.
  - It ends exactly on a spine cut, or hands straight to the next burst. Never stop within 0.8 s before a cut (builders assert it).
  - Close gaps under 0.3 s between B-roll pieces, so the face never flashes for a frame.
  - Every line opens on the speaker's face for ≥ 0.6 s.
- **B-roll choice:**
  - Show what the sentence says, with people. A "room full of people" means the widest full-room shot.
  - Screens are seasoning: about one per reel.
  - Never Babi at a desk.
  - Steady shots only (`shared/tools/shake_score.py` ≤ 0.5).
  - Muted at −96 dB.
  - Read `shared/BROLL.md` first.
- **Jump cuts inside a burst** move forward in the source with 1.3–3 s gaps. **Locked-off/tripod clips get one longer shot (2–2.5 s)**, never jump cuts.
- **Coverage:** stories 35–60 % (more on recaps, less when the speaker is the point); panel moments ≈ 20 %.
- **Joins:** re-transcribe every join and cut a duplicated word ("join | join"). Whisper invents "And"/"So" at the start of a cut piece: test by trimming +0.07/+0.13/+0.20 s and re-transcribing.
- **Captions:**
  - Expand `ref-clip` compound clips before transcribing.
  - Caption every spoken word, including interjections and strangers, with a per-piece second pass.
  - Check the title row in the timeline before saying it's done.
  - Proper-name fixes list: Alix, Michi's, start2finish, BABI, Genia.
- **The real recording played in the story** ("and Alix said…") gets a different caption style: size 56, top third, active word light blue `0.45 0.85 1 1`. With two speakers, Stu's active word is yellow and the interviewer's light blue; chunks never cross speakers.
- **Rick:** whenever "Rick" is said, pop a Rick photo with the "dick ding" on that word, one pop per mention. Photos are in ~/Downloads: `rick-1-slack-portrait.png` (default) and `rick-4-threads-portrait.jpg`. rick-2/3 are missing.
- **Bleeping a name:** split at the RMS edges, mute that piece, lay a 1 kHz sine on its own lane, and show a blurred PNG of the word (GaussianBlur ≈ 9).
- **Named charity or organisation with no footage:** screenshot its own site, or use Wikimedia Commons CC photos (Openverse is blocked). Save the licence to `photo_sources.json`.

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
   - **Start each line on its first content word** for scripted retakes and the reel's opener ("~~So~~ Marcus, one of our developers…"). **Inside a story or panel answer, keep the connective** (And / So / But): on Laurier he put back "And" ×7, "So" ×4 and "But" ×1 (2026-11-27). Superseded in part by quick rule 1.
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
   - **Pick a song for every reel.** In a batch, mix the songs up so they aren't all the same; a few reels can share one. Use `STORYTELLING/Jack Style` and its siblings.
     - Laurier picks Babi made: Green Onions, In Motion, Miss Alissa, Get Down, Everything In Its Right Place, Every Living Breathing Moment (started at ≈ 7.2 s), and Timeless (Instrumental) from 23 s, with the drop about 1 s in.
   - One lane, mostly flat, at −14 to −19 dB. He adds a fade or a −2 dB dip himself.
   - **Run the music to the last frame of the last clip** (he fixed songs that stopped short). A song longer than the cut is trimmed to the cut.
8. **Captions.** On by default; geometry is in the shared core rules (the chest, not the knees).
   - Seated or panel stories: karaoke (Helvetica Neue Bold 42, active word yellow).
   - Walk-and-talk: the small lowercase style (section below).
   - Promos: one-word caps.
   - The old "size 46 at Position 0 −335 (≈ y 1533)" spec is retired: it sat too low. Run `scripts/add_captions.py` on an export, then Replace. The Black Friday reel used one word at a time, Avenir Next Heavy, white with a black outline, and key words/numbers in yellow. Creator Lab had none.
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

## Knowledge / teaching reels
Teaching reels (Stu explaining numbers or a framework, Toni Blog, Hal Eldro, Black Friday Knowledge) moved to **babi-knowledge-reels**: internet photos with pops, karaoke captions, section headers, dollar figures and a board zoom.

## Personal vlogs and caption reels
These moved to the separate skill **babi-vlog-reels** (repo `diskwatch/babi-vlog-reels`): run vlogs on Babi's 2TB, the Edits app recipe, and one-word captions.

## Updating this skill
All Babi skills live in ONE private repo, `diskwatch/babi-skills`, cloned at `~/.claude/babi-skills`. Each skill folder is symlinked into `~/.claude/skills/<name>`. The old `diskwatch/babi-storytelling` repo is retired; don't push there.
1. Edit `SKILL.md`, or the scripts, with the new lesson. Keep it concrete: numbers, before/after, the clip or project it came from.
2. Add a line to the changelog below.
3. Commit and push: `cd ~/.claude/babi-skills && git add -A && git commit -m "<skill>: <lesson>" && git push`. On the other Mac, `git -C ~/.claude/babi-skills pull` gets the update.


- **Where a lesson goes:** a rule that applies to every reel goes in `shared/SETTINGS.md` › Core rules. A storytelling rule goes in Quick rules or Rules from past rounds here. The dated story of a project (clips, numbers, builders) goes in `LESSONS.md`. Keep this file short: it is read before every edit.

## Walk-and-talk captions: the "reference reel" look (TRIAL, Laurier round 3, 2026-11-27, not yet approved)
Babi asked for this on reels where the speaker walks and talks to camera (Laurier: Big Mistake, Momentum, Calculus Professor, Bookstore Amy). Reference: instagram.com/p/DflEwe7RFn5 ("How to work at a startup"). Seated panel reels keep the karaoke style.
- **Normal captions:**
  - Small lowercase sans, 2–3 words / ≤ 16 characters per title, no karaoke colour and no outline.
  - A soft shadow: `0 0 0 0.6`, offset `3 315`, blur 12.
  - They sit on the chest in the middle of the frame.
  - FCP values: Helvetica Neue **Medium 36**, Position `0 -115` (≈ y 1150), white.
  - A new chunk starts after a 0.35 s gap or at a sentence end.
  - Names and "I" stay capitalised (`tokens()` PROPER list).
- **Big words and clicks are OFF for now** (Babi, 2026-11-27 3:33 pm: "get rid of all the clicks and all the big captions… I do love how you have the rest of the captions"). Small captions only, until he asks to work on the big words again (`BIG_WORDS = False` in v4.py). The spec below is kept for that.
- **Key words (paused):** about one every 6–8 s, a key word takes over on its own as a **big high-contrast serif**. The reference used "technical.", "Pipeline" and "Phase 1".
  - FCP values: **Didot Regular**, size fitted to ≤ 600 px (max 118), squeezed horizontally with `adjust-transform scale="0.82 1"` to look condensed, Position `0 -95`, on from the word's start to its end + 0.5 s.
  - Pick nouns that carry the story:
    - mistake, traditional, student, championships, way
    - university, momentum, graduated, home
    - calculus, winked, extra
    - wife, bookstore, flirting, worker, teammate
- **Every big serif word gets a mouse click sound** (Babi, 2026-11-27: "like on mistake, it should be a sound").
  - File: `Sound FX/click and keyboard/Mouse Click Sound Effect 4.mp3`, in-point 0.51 s for 0.25 s (press at 0.53 s, release at 0.61 s), −12 dB.
  - Placed so the press lands on the frame the word appears.
- Builder: `Media/OFFICE/Nov 26 Laurier Panel/XML/v3_tools/v4.py` (`walk_caps`).
- **Waiting on Babi's verdict;** record what he keeps or changes here.

## Changelog
- 2026-11-27 v1.4: walk-and-talk reference-reel captions (trial), Laurier round-2 notes (pop −16 dB, song to the end, photo lane, no repeated photos, office B-roll on panel moments, Vine boom).
- 2026-11-23 v1.3: charity promo overlays (cards above the head, Commons photos, caption diff, export/replace flow).
- 2026-11-22 v1.2: compound-clip (ref-clip) caption bug, per-piece second transcription pass, verify-import rule (Nov 22 Tony).
- 2026-11-21 v0.10: Immersion Day story reel B-roll redo (room full of people, no desk clip, one screen shot, start on the word, let him speak).
- 2026-11-21 v1.1: Immersion Day story round-1 notes (tighter, Skyfall, B-roll end rule enforced, karaoke captions, guest cut-in).
- 2026-11-21 v1.0: Immersion Day story from raw retakes (lead-in hallucination test, stumble-bridge, steady-only B-roll, caption recipe, SFX path).
- Older entries: see LESSONS.md.
