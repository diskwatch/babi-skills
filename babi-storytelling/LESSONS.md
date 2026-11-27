# babi-storytelling: lessons log
The dated project notes behind the rules in SKILL.md, moved here 2026-11-27 to keep SKILL.md short. Read the section for the kind of reel you are building. Newest projects are at the end.

## Babi's notes on the Nov 16 talks (2026-11-16) — apply to every storytelling edit
- **No silence at clip joins.** Babi trimmed the first cut by hand: "a month ago…" head 0.12 s / tail 0.47 s, "25 people" tail 0.10 s, "If you're new here" head **0.46 s**. All the removed audio was below about −40 dB. Cut each line's head at the speech onset and its tail at the decay with only ~0.02–0.03 s handles: threshold = p97 of the clip's 10 ms RMS − 27 dB (≈ −40 dB on IMG_0562), search ±1 s, never fall back to Whisper word times (they run long). `scripts/cutlib.py refine2` reproduced his trims within 0.02–0.05 s. Pinned (exact) starts may only move forward to the onset. Re-transcribe: a widened search re-grabs dropped "And"/"So", so pin those starts at the dip after "and" (10 ms RMS).
- **B-roll never ends just before a talking-head clip ends.** It ends on exactly the same frame as a spine clip end, or hands straight to the next burst. (v1 had bursts a frame or two short, plus mid-line endings.) Check with `scripts/check_ends.py` (0 off-edge).
- **Jump cuts inside a burst move forward in time with real gaps.** Shots 0.2 → 1.1 s from the same clip "look practically the same" and "skip 2 ms, which looks really weird". Space in-points like 2–4 s then 7–9 s (≥ ~1.3–3 s between the end of one shot and the start of the next, judged by eye). In-points must be increasing. If the clip is too short, use one longer shot (Babi's own picks were single 1.85 s and 3.25 s shots).
- **Bleeping a name** (Babi, 2026-11-20): split the spine clip at the word's RMS edges, mute that piece (−96 dB), 1 kHz sine on its own lane, and swap its caption for a blurred PNG of the word (GaussianBlur ≈ 9 at caption size) so viewers wonder what was said.
- **Locked-off (tripod/static) clips don't jump-cut.** Two in-points 2+ s apart in a static shot still look identical and read as a glitch (Immersion Day 0819, 2026-11-20). Use one longer shot (2-2.5 s) or switch clips; keep jump cuts for handheld/moving clips.
- **More B-roll.** v1 covered ~45%; v2 covered 81% (Golden Run) and 58% (charity), keeping his face at the start of most lines and on direct questions to camera. Chain bursts back to back inside a line (one clip per burst).
- **His picks:** the opener and "25 people" = the clip with the most people in frame (IMG_0276 lake path, not the meeting spot); "two random guys" = IMG_0274 @6.27 (running past) and IMG_0277 @5.07 ("how did you guys even find us"). Find who's who from the clips' own audio.
- **Captions** (knowledge karaoke style, smaller): "a little bit higher" → size 46 at Position `0 -288` (≈ y 1450; −335 rendered at ≈ 1533). Keep graphic pops above ≈ 1405 px.
- **Before changing anything, export his current project** (he edits between rounds) and diff it (`scripts/readproj.py`). The 2TB dropped out once mid-session: Final Cut showed "cannot save changes… libraries will be closed". The event DBs were already saved; press Continue, then reopen with `open -a "Final Cut Pro Creator Studio" <library>`.

## Babi's round-3 notes (Give Oakville, 2026-11-16) — apply to every storytelling edit
- **No 1-frame gaps between B-roll pieces.** v2 ended a burst on a clip end and started the next at 26.05 s, one frame later; the talking head flashed for a frame. Any gap under ~0.3 s between B-roll/graphic pieces gets closed (extend the earlier piece). `scripts/patch_v3.py` does it automatically.
- **Don't over-trim heads.** He brought back 0.52 s at "Then, she for some reason…" (src 144.47 → 143.95), 0.27 s at 446.22 → 445.95, 0.17 s at 125.82 → 125.65. "Then" / a breath before a name is part of the line: drop lead-ins only when they are filler ("And", "So"), never a word that carries the story.
- **Joins with a repeated word:** "…follow all of us **join** | **join** the Instagram channel". The tail kept "join" and the next take started with it. Re-transcribe the joins and cut the duplicate (he trimmed the tail 566.90 → 566.67).
- **Pop-ups with a Ding when a person or organisation is named** (just after the name, not on it):
  - "Jeff Knoll" → his own stills at 8:59 (Google result card + film.ca logo). Not full-frame: a collage, the main card 600 px wide at (400,1010) and the logo 380 px at (720,1160), with one Ding a frame before.
  - "Oakville Community Foundation" → OCF logo card (from theocf.org header at 4× scale, white rounded card) 440 px wide at y 1270, 1.2 s, Ding.
- **Logo size and position he wants (S2F logo):** he moved it from 380 px at y 1150 to **≈ 440 px wide, centred x 540, y ≈ 1270** (scale 0.4068 of a 205 px png, position 0 / −16.13 %). Use this for named-org logos.
- **Pop sound in-point:** "Cute Pop" transient is at 0.73 s. Starting the clip at 0.75 s cuts it off (silent). Start at **0.696 s**, placed 1 frame before the photo. Always check the transient with 10 ms RMS before using a SFX.
- **The real clip:** when he says "and Alix said…" he plays the actual recording (IMG_9966) on the spine. Caption it in a **different style**: bigger (56), top third (Position `0 288`, ≈ y 470), active word light blue `0.45 0.85 1 1`. Check the frame for faces first.
- **Captions a bit higher and smaller:** size **42**, Position `0 -288` plus `adjust-transform position="0 5.706"` (≈ y 1340, his first-caption example). While a low graphic is up (logos/photos reaching below ~1290) the captions drop under it: transform `0 -3.5` (≈ y 1515).
- **Proper names capitalised in otherwise lowercase captions:** "Alix" (not alex). Fix list: alex→Alix, me cheese→michi's, oliver→all over, rung→run, start to finish→start2finish, 9 a.m.→9am.
- **Caption every spoken word he adds**, including the outro he restored ("this took me about an hour and a half to film…"). Re-transcribe his export with `scripts/words_from_export2.py` (handles several spine sources).
- **His own B-roll habits seen in round 3:** shorter shots (0.5–0.9 s), mixing clips across days inside a burst (Nov 8 run, Nov 11 lunch, Nov 15 run), punch-in zoom (scale 1.78 / 2.1–2.3) on the same shot for energy, and music split around the real clip (cut out under it).

## Q&A / "asking Stu hypotheticals" reels (2026-11-20)
Babi off camera asks Stu hypotheticals ("would you do it?"), one locked-off shot (IMG_0609, Nov 18). Reference: Culture Pop "asking our wholesome founder hypothetical questions" (DfnmZ93sWE0): no B-roll, no music, a lowercase two-line header in the wall/ceiling band (y ≈ 480) over the first question, then just the conversation.
- **Ask:** polish his 3 versions + make 3 remixes (different order and picks, funniest first, < 1:30), captions on all. Builder: `Media/OFFICE/Nov 18 Asking Stu Hypotheticals/XML/reels.py` (`cut` / `words` / `build`): blocks per question = his own spine ranges (kept zooms 1.2), tighten = RMS −46 dB edges (−0.05/+0.08) and pauses ≥ 0.30 s cut, **0.3 s comedic beat kept before punch answers** ("No.", "Heck yeah", "Done.", "What?", "Yes."), the interviewer at the phone is ~8 dB louder than Stu, so turn HIM down to match. Never raise Stu (shared core rule 1; the old "per-piece gain to −27 dB, clamp −8/+6" boosted quiet pieces).
- **Captions with two speakers:** karaoke chunks never cross speakers or questions; active word yellow for Stu, light blue `0.45 0.85 1 1` for the interviewer. Speaker from a hand-made list of Stu's source spans. ≤ 4 words / 16 chars so "would you do it" stays one caption.
- **Whisper drops short interjections** ("What?", "yeah you'd sell it", "I'd sell it") and garbles long renders: transcribe per question block, then patch missing words by source time (RMS bursts + a medium.en pass on the 2 s slice).
- **Final Cut Helvetica Neue Bold renders ≈ 1.75–1.8× PIL width** (measured in the viewer: size 32 header = 940 px; size 42 "if it could make" = 540 px). The 1.34× in shared SETTINGS was far off for these: header size 24 (~735 px), captions 36.
- Remix picks that worked: open on the fastest punch (stu-scented candle "What?", Rick "Heck yeah", Andrew "Done. Easy-peasy"); end on a wholesome answer ("culture over talent", "I don't want them there").
- **Whenever Rick is mentioned, pop a Rick photo with a "dick ding" sound effect** (Babi's standing rule, 2026-11-23). Trigger on the spoken word "Rick" in the question or the answer, and land the photo on that word, same pop style as the chat pops. Source photos, all in `~/Downloads`: `rick-1-slack-portrait.png` (default), `rick-2-headshot.png`, `rick-3-team-photo.png`, `rick-4-threads-portrait.jpg`. Use the slack portrait unless Babi picks another. Each Rick mention gets its own pop + ding, never one for the whole block.

## Babi's notes on the Immersion Day story reel (2026-11-21): B-roll over Babi talking to camera
Builder: `Media/OFFICE/November 18th Immersion Day/XML/Story/build_story.py` (SHOTS table = the B-roll, absolute story seconds; working data in `Story/tr/`).
- **Show what the sentence says, with people.** "a room full of people" = wide shots of the full room (IMG_0765, 0791, steady), starting on the word "room" (1.18 s). The v1 cut showed arrivals and a woman watching a slide 1.2 s later.
- **Don't use clips of Babi himself sitting at a desk** (IMG_0733, 0693, 0734, "need to market app"); he named IMG_0733's clip as the problem. His own face is already the main shot.
- **Screens are seasoning, not the meal.** v1 used 14 screen/slide/monitor shots (0806/0807 six times). v2 has ONE (the TV text thread on "just by talking to it"); everything else is faces, reactions (Lisa filming and smiling, Mike chin-on-hand, a woman covering her face laughing), Stu presenting, Rick, the team.
- **Start 2 frames BEFORE the key word, never after** ("some clips start a little bit too late"). Measured lead in v2: +0.01 to +0.11 s. End exactly on a spine boundary or at least 0.8 s before one (the builder asserts it).
- **Let him speak:** every line opens on Babi's face for ≥ 0.6 s; lines 6, 7, 8, 12, 18 have no B-roll; coverage 36 % (v1 ~50 %), shots 0.8-1.4 s.
- **Rick:** younger guy in black cap + Membership.io jacket. Babi said to REMOVE the shot of him sitting at the desk with a laptop (IMG_0797); avoid 0797/0792 too. Rick is shown texting the AI instead (0806 @9, one 2.5 s shot, zoom 1.6 at position 0 −20 hides the bald head in the foreground; the old +6 shift pushed the image the wrong way: for FCPXML `adjust-transform`, negative y moves the picture DOWN, so the visible window moves UP the source).
- All B-roll muted (-96 dB) and every window steady (`shared/tools/shake_score.py`, 0.0 px/frame). Zoom 1.4 at (0, 6) on 0806 hides a bald head in the foreground.
- If he edits in Final Cut, export the event first (File > Export XML) and diff: v1 had no hand edits when redone.

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

## Setting up on a new Mac
1. Run `gh auth login`, then `git clone https://github.com/diskwatch/babi-skills.git ~/.claude/babi-skills`, then symlink each skill: `for d in ~/.claude/babi-skills/*/; do ln -s "$d" ~/.claude/skills/$(basename "$d"); done`.
2. Install Homebrew `ffmpeg`. For transcription, make a throwaway venv (`python3 -m venv … && pip install faster-whisper pillow`). The first run downloads small.en and medium.en (~1.5 GB).
3. In the Claude desktop app, turn on Computer use (Settings) and grant Screen Recording and Accessibility when macOS asks.
4. Start Claude Code sessions in the same folder each time, so memory notes stick. Put anything important in this skill, because memory doesn't sync between Macs.
5. Before editing, `git -C ~/.claude/babi-skills pull`. After any lesson, commit and push from `~/.claude/babi-skills`.
- Toolchain gotchas: PyAV 1.2.1 breaks `transcribe(path)`, so pass a 16 kHz float32 numpy array. Homebrew ffmpeg has no `drawtext`. iPhone footage is HEVC 10-bit HLG; keep it HDR.
- Overlays that block clicks: Wispr Flow's floating pill, Final Cut grabbing keyboard focus, Notification Centre. Request access to Wispr Flow / Final Cut, or use the background `app_*` tools with element_index.

## Talking-head story from raw retakes (Immersion Day story, 2026-11-21, first cut, not yet reviewed by Babi)
Two 4K vertical clips (IMG_0975 58 s, IMG_0976 8 min) of Babi retaking each line many times -> 57.8 s reel in "Immersion Day FCP12.3". Scripts: `scripts/cut_story_lines.py` (lines -> pause-split pieces on the 30 fps grid, renders the cut audio) and `scripts/build_story_reel.py` (FCPXML: spine, steady muted B-roll bursts, captions from the cut's own words, pop on the CTA graphic).
- **Pick the last clean take of each line**; read 10 ms RMS speech runs (`cutlib`, thr = p15+10 / p97-32) to get exact edges. Whisper word times are useless across long stalls (a "for" listed as 14 s long).
- **Whisper hallucinates "And"/"So" at the start of a cut piece.** Do not trust the cut transcript for lead-ins: render the piece with 0.7 s silence before it, then trim +0.07/+0.13/+0.20 s and re-transcribe; the first trim where "And" disappears and the real word survives is the start (needed +0.07, +0.20, +0.13, +0.07 s on four lines). Re-transcribe the whole cut after every change.
- **A stumble take can hide a complete one:** "and rebuilt, nope, and rebuilt" was bridged by a later run that held "and rebuilt their entire landing page..." in one go; start that run after "and" and drop the stumble piece.
- **B-roll:** steady shots only (`shared/tools/shake_score.py`; arrival hugs and selfies were 5-36 px/frame, boardroom/whiteboard clips 0.0). Bursts start about 0.7-1.0 s into a line (hook at 0.9 s), chain back to back, end on the line end; faces kept at the start of each line and on the setup lines. Coverage 65 %.
- **Captions:** pure white Helvetica Neue Bold 42, Position `0 -288` + adjust-transform `0 5.706`, 3 words / 16 chars per title; "membership.io" arrives from whisper as "membership" + ".io"; whisper hears "I could" as "it could".
- **Sound FX path:** `Babi NR Content/Sound FX/click and keyboard/` (not `Songs/SOUND FX/`). Copy it into the day folder's `Sound/` before use.
- **Import:** `open -a "Final Cut Pro Creator Studio" file.fcpxml` -> pick the library row -> Choose; the event reused the 119 existing uids (read from the event's sqlite, `ZCOLLECTIONMD`), only IMG_0975/0976 were new. zsh does not word-split `$var` in loops.

- **Babi's round-1 notes on the Immersion Day story (2026-11-21):** "tighten, there's dead space" (trim every piece to the speech decay: last frame above p97-27 dB + 0.04 s, split pauses >= 0.08 s, guest clips at >= 0.12 s; 69.5 -> 67.9 s), "more dramatic song" (Skyfall from 37 s at -20 dB, -7.5 LUFS song -> ~11.5 LU under speech), "B-roll must not end right before an A-roll switch" (a burst's last shot that stops within 0.8 s before a spine cut must run to that cut; the builder asserts it), "captions like the earlier skill: white, active word yellow" (one title per spoken word, `1 0.88 0 1`). "Hear it from them" -> cut to Mike + Lisa from the Immersion Day interview projects (segments.py 1,2,3,11,18), then back to the story.
- **Final Cut Replace prompt can't be clicked while Wispr Flow's overlay is up** (background and full-screen clicks both refused): build the XML, open it, choose the library, then ask Babi to press Replace.


## Compound clips broke the captions (Nov 22 Tony "fun edit V1", 2026-11-22, Babi: "everything should be captioned... you've failed me")
- **Spine items can be `ref-clip` compound clips** (here the first 5.49 s: Babi talking to camera, "at the end of the last one, I talked to his dad…"). `words_from_export2.py` and `add_captions.py` only read `asset-clip`s, so (1) that speech was never transcribed, (2) every later word time was 5.49 s early, (3) titles for the first seconds attached to the wrong clip. Always list the spine tags first; expand each ref-clip from its `<media>` sequence (offset + start inside the compound) before transcribing. `add_captions.py` now attaches to ref-clips too; `words_from_export2.py` still needs the expansion (see its warning).
- **"Every line" means every line.** One 12 s medium.en pass dropped short interjections ("Whoo!", "Cheers!", "Yes sir", bakery "Thank you"/"Bye"). Do a second pass per spine piece (small.en, +-0.4 s padding, keep words whose midpoint is inside the piece, skip hallucinations like "Thanks for watching") and merge words the first pass missed. Then check the result against the timeline by eye (titles under every speaking piece) before telling Babi it is done.
- **Verify the import before reporting.** The first import landed late and the Replace sheet cannot be clicked in the background; look at the title row in the timeline and the viewer at 3-4 spots, and say what was NOT checked.
- **The edit itself:** a 52 s montage of short pieces (0.3-1.5 s, many jump cuts inside one take) over Burna Boy "Bigger", one 0.9 s still graphic, no titles. Speech is sparse and comes from Babi's intro and strangers; the song, not dialogue, carries it.
- **Export notes:** Final Cut's save sheet only accepts a plain file name (no "/"), so export to Downloads/Desktop and move the .fcpxmld to the XML folder afterwards. Source must be the PROJECT selected in the browser, not a clip.


## Charity promo overlays (Nov 22 Promo Next Run V1, 2026-11-23, first pass, not yet reviewed by Babi)
Babi's own 40 s promo (4 clips, one-word captions, 3 B-roll inserts) got logo/photo cards on three spoken names; B-roll and music untouched. Builder: `Fall26/XML/Nov 22 Promo/` (`build_cards.py`, `patch_overlays.py`).
- **Export first, patch the export, Replace.** File > Export XML needs the timeline focused and full-screen control (`app_menu` File > Reveal Project in Browser, then Export XML); background `app_menu` is refused until the app is frontmost. Import the patched file, pick the Fall26 library, press Replace. The warnings "not on an edit frame boundary" come from spine clips whose source `start` is off the 30 fps grid (1/2400 s); FCP snaps them, the overlays still landed on the right frames.
- **Cards go in the sky above his head (y 300-860), captions stay at -165 (~y 1235).** Whole-frame check: his beanie top is ~y 890, so a 616x356 photo card centred at y 665 and a 470-520 px logo card at y 380 clear it. White rounded cards (radius ~34 px, 2x render), no animation.
- **Triggers:** "start to finish" -> S2F logo (hi-res from start2finishonline.org, squarespace `Start2Finish Logo FEET BESIDE.png` 1343x287) with Ding, then the S2F kids-reading photo with pop; "give Oakville" -> GIVEOakville wordmark (cropped from the theocf.org header, wordmark only, not "LIVE!") with Ding, then two Oakville photos (Town Square 2023 CC BY 4.0, Lakeshore Road CC BY 2.0, Wikimedia Commons) with pops; "coffee" -> Sutton Quantum card (logo from suttonquantum.com Wix CDN, drop the right-hand tagline) with the line "post-run DJ at Sutton Quantum Group" baked into the card, Ding. Cards end on the next spine cut.
- **Openverse is behind a Cloudflare challenge now (HTTP 403/504).** Use the Wikimedia Commons API (`action=query&generator=search&gsrnamespace=6&prop=imageinfo&iiprop=url|extmetadata&iiurlwidth=1200`, User-Agent set) for CC photos and save licence + artist to photo_sources.json.
- **Missing captions:** diff the project's titles against a medium.en transcript of the cut audio (difflib on normalised words). Here 19 words were missing (the whole 28.6-32.7 s clip + "that" + "be"); two neighbours were retimed by 1-4 frames to make room.

## Laurier lessons, round 2 (Babi's notes on the V3s, 2026-11-27)
- **Pop SFX at −16 dB, not −24.** He raised the "quiet pop" himself in Gemini Jeffrey; "a little louder".
- **The song must run to the last frame of the last clip.** He extended it by hand on Big Mistake and Momentum. Builders extend the music clip to the sequence end, and warn when the song is too short.
- **Photos on their own lane above everything.** On Be Patient the header title sat on lane 4, the same lane as the photos, and the photos didn't show in the viewer. Put photos on max(existing lanes) + 2.
- **No repeated photo in one reel.** Three grad photos in Be Patient was flagged. Use a different picture per pop: grad on "21-year-old self", 29029 on "it really sucked in the beginning", young Stu with big hair on "I'd have a lot more hair".
- **Praised:** the Big Mistake office B-roll around 32 s (Stu at his studio desk IMG_9869, then at the whiteboard IMG_9905), and the Gemini family photo. Office B-roll is wanted on panel moments too (AI Line: boardroom whiteboard IMG_0763/0779, Rick texting the AI IMG_0806, the team at a dev screen IMG_9890, a walker leaving IMG_9892 on "decided to leave", Stu + Rick laughing IMG_0757).
- **SFX on gestures:** a Vine boom (`Songs/new/Dramatic Vine_Instagram Boom…mp3`, onset 0.20 s, −8 dB) when Stu grabs Amy's butt in the walk-away shot.

## Full changelog
- 2026-11-27 v1.4: walk-and-talk reference-reel captions (trial), Laurier round-2 notes (pop −16 dB, song to the end, photo lane, no repeated photos, office B-roll on panel moments, Vine boom).
- 2026-11-23 v1.3: charity promo overlays (cards above the head, Commons photos, caption diff, export/replace flow).
- 2026-11-22 v1.2: compound-clip (ref-clip) caption bug, per-piece second transcription pass, verify-import rule (Nov 22 Tony).
- 2026-11-21 v0.10: Immersion Day story reel B-roll redo (room full of people, no desk clip, one screen shot, start on the word, let him speak).
- 2026-11-21 v1.1: Immersion Day story round-1 notes (tighter, Skyfall, B-roll end rule enforced, karaoke captions, guest cut-in).
- 2026-11-21 v1.0: Immersion Day story from raw retakes (lead-in hallucination test, stumble-bridge, steady-only B-roll, caption recipe, SFX path).
- 2026-11-20 v1.0: Q&A hypotheticals reels (Stu): speaker-coloured captions, comedic beat, per-piece leveling, FCP width ≈ 1.8× PIL, polished + remix builder.
- 2026-11-16 v0.9: round-3 notes: no tiny B-roll gaps, name pop-ups with dings, logo size/position, pop in-point 0.696, real-clip caption style, captions size 42 at ≈ y 1340, every used clip must be a browser clip (patch_v3.py).
- 2026-11-16 v0.8: Babi's notes on the Nov 16 talks: no silence at joins (onset/decay cut at p97−27 dB), B-roll ends exactly on clip ends, spaced sequential jump cuts, more B-roll (~60–80%), captions at −288.
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
