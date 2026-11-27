# Shared settings and tools (ALL Babi skills)

Every Babi skill (storytelling, vlog-reels, simple-reels, copy-format, ezromo-style, knowledge-reels) follows this page. Read it before building anything. A skill's own page adds style rules on top. When a lesson applies to every skill, it goes here, not in one skill.

## Core rules (Laurier review, 2026-11-27). These override older notes anywhere in the skills
Measured from Babi's re-edits of 12 Laurier reels: 38 edge changes, captions, headers, levels, music and pops. The diff tool is `shared/tools/recover.py`.
1. **Never raise dialogue gain automatically.** Default 0 dB.
   - Field Producer's −16 LUFS normaliser added +5.7 to +8.2 dB, and Babi set every reel back to 0 or +1 dB ("I brought everything pretty much back to 0 dB").
   - Older notes where *he* raised a clip (+3.3 dB road trip, Mike +11 / Lisa +8) are his manual moves, not a rule to copy.
   - Balancing two speakers in one clip is allowed only by turning the louder one down.
2. **Edges, from his recoveries:**
   - **Keep connective lead-ins inside a story** (And / So / But starting a sentence): he restored 12 of them, 0.08–0.43 s each. Drop only stutters, false starts and the reel's very first filler word.
   - **Never cut inside a first word.** Start ≈ 0.06 s before the 10 ms RMS onset; soft onsets run −25 to −45 dB. He restored 5 clipped words ("how", "had", "it's", "be", "we").
   - **One-line-per-file takes:** whisper's first-word time runs ~0.5 s early, so cut the head to the RMS onset. He trimmed +0.50 to +0.93 s of silence on 7 takes.
   - **Tails end ≈ 0.08 s after the decay.** He cut 0.18–0.30 s of silent tail 9 times.
   - **Let the reel's ending breathe:** keep the closing kicker or laugh. He added +1.12 s and +1.72 s ("So, you know, there's that too.").
3. **Captions sit on the chest, measured on a frame of each shot:**

   | Shot | Position | Height on screen |
   |---|---|---|
   | Seated or panel crop (1.6×) | `0 -60` + transform `0 5.706` | y ≈ 950 |
   | Standing or walking, karaoke | `0 -230` + `0 5.706` | y ≈ 1235 |
   | Walk-and-talk small captions (see babi-storytelling) | `0 -115` | y ≈ 1150 |
   | One-word caps | `0 -140` | y ≈ 1195 |
   | While a mid-frame photo is up | `0 -288` + `0 5.706` | y ≈ 1331 |

   - **When Babi moves one caption in a reel, move every caption in that reel by the same amount** (Balloon Animals −82, Be Patient −43).
   - When he cuts or extends clips, rebuild the captions from the cut's own audio, so restored words get captioned.
4. **Headers set up the question; they never give away the payoff.**
   - His rewrites, before → after:
     - "we hired 6 people to replace 1 developer" → "What was your biggest business "failure"?"
     - "she makes six figures teaching balloon animals" → "when people ask me who my company serves..."
     - "his students call their teacher Gemini Jeffrey" → "My son caught his teacher using AI 😭"
     - "I knew I failed calculus. then my professor winked" → "POV: ur back at Laurier getting flashbacks"
     - "what I'd tell my 21-year-old self" → "Laurier Student asks alumni: "What would you tell your 21-yo self?""
   - POV, quoted questions and emoji are OK.
   - On seated shots put the header at Position ≈ 385 (y ≈ 315), just under the 250 px band. On walking shots he sometimes lowers it to stay off the head.
   - **A header never runs across a photo.** In Bookstore Amy he split the header and dropped the second half under the photo.
5. **Every reel gets a song; don't stop to ask.**
   - **In a batch, mix the songs up so they're not all the same.** Repeats are fine: Babi used 6 songs for 12 reels ("every reel doesn't need its own song… if we're making a lot of reels, they shouldn't just all be the same", 2026-11-27).
   - Start past the intro (Every Living Breathing Moment from ≈ 7.2 s).
   - Most reels sit at −14 to −19 dB.
   - The music clip runs to the last frame of the sequence; the builder extends it and warns if the song is too short.
6. **Photo pops:**
   - Real photos of the people beat logo cards. He deleted the Laurier and Golden Hawks cards placed under the captions (y ≈ 1530) in 3 reels.
   - On seated shots, a white rounded card in the middle (y ≈ 990, ≤ 470 px tall). On standing shots, above the head (y ≈ 440, ≤ 380 px tall).
   - A quiet pop at **−16 dB** with each one.
   - A different photo for each pop in a reel.
   - Photos go on their own lane: max(existing lanes) + 2. A header on the same lane hid them.
   - Stu's photos and what each fits: `Babi NR Content/Photos/Stu McLaren/README.md`.
7. **Before searching the SSD for B-roll,** read `Babi NR Content/BROLL-INDEX.md` (mirror: `shared/BROLL.md`).

## Project settings (Final Cut)
- **Projects are always Rec. 709.**
  - In FCPXML the sequence format must say `colorSpace="1-1-1 (Rec. 709)"`. The clips keep their own `9-18-9 (Rec. 2020 HLG)` tag, and Final Cut converts them on render.
  - Never copy the clips' HLG tag onto the project; that is why projects came out "Rec. 2020 HLG".
  - Final Cut has no global default: a project made by hand on Automatic settings copies its first clip (HLG). Use Use Custom Settings › Color Space › Standard – Rec. 709, or Inspector › Modify on an existing project.
- **Check the Final Cut version before promising to open a library.** As of 2026-11-16 this MacBook Air runs macOS 27 with Final Cut **12.4** (it was 12.3 on macOS 26 before), so 12.4 libraries such as `Fall26 20261018_1446_EDT` open again. A library saved by a newer version than the app won't open. Compare `CurrentVersion.plist` catalogVersion with the app's version.
- **Media and sounds live next to the project.** Copy any song or SFX you use into the run or project folder first. The 4TB SSD can unmount mid-session (`ls /Volumes`).

## Instagram safe zone (Babi's overlay, 1080×1920)
- Keep text and graphics out of the **top 250 px** and the **bottom 320 px**, and keep **120 px** clear on each side.
- Keep clear of the **right-hand button column (x > 845, y > 1130)**: like, comment, share.
- Captions centred at x 540 below y 1130 must therefore be **≤ ~590 px wide**.
- "Not super strict", but stay on the safe side.

## Don't block what matters (every skill)
Babi, 2026-11-16: before laying any overlay (photos, captions, headers, logos, chat pops), think about what in the shot must stay visible: a whiteboard or slide, a product, a screen, a face, a demo.
- **Check it on real frames.** Render 2–3 frames per spine clip in output space (apply zoom crops), draw the planned boxes with PIL, and tile them.
- **Move or shrink overlays into space that is free in every clip.** Don't remove them.
- Example: Black Friday, small photos plus one-line headers in the ceiling band above the whiteboard (babi-knowledge-reels).

## Captions in Final Cut (geometry only; size and style come from each skill)
- **Captions are made in Final Cut by default.** Babi compared FCP and Edits captions on 2026-11-14 and chose Final Cut. The Edits recipe in babi-vlog-reels is a fallback.
- **Basic Title `Position` units ≈ 1.67 px** in a 1080×1920 project:
  - −252 puts the centre at y ≈ 1380 (72% down).
  - +368 puts it at about y 345 (a header just below the top band).
- **The Position-to-pixels mapping isn't fixed for small text.** A size-30 header at Position 302 rendered at y ≈ 370, not 455, and 235 rendered at ≈ 500. Check each new size in the viewer and adjust.
- **Helvetica Neue Bold in FCP ≈ 1.34 × PIL's width at the same size** (FCP 30 ≈ PIL 40) for small headers; for Basic Title captions/headers in a 1080×1920 project it measured **≈ 1.8×** (2026-11-20, Stu hypotheticals). Check one title in the viewer before trusting either.
- **Arial Black ≈ 1.45 × fontSize px per capital**, so width-cap with size ≤ maxWidth / (1.45 × letters). Calibrate once for any other font.
- **Fill plus outline:** `strokeWidth` must be negative. The font must be installed, or Final Cut silently swaps it.
- **Time captions from the cut's own audio.** Render the planned cut with ffmpeg (atrim, plus atempo for speed changes), transcribe that, and caption from it. Raw-clip whisper drifts up to 1.2 s across pauses. Re-check unclear lines with medium.en on just that slice.
- **Spellings:**
  - **BABI** (whisper and the voice typer write "Bobby").
  - Uncle **Genia**, nickname **Gen**.
  - No punctuation in captions.

## Working with Babi's edits (every skill)
- **Read his edit before changing anything.** Use File › Export XML (FCP writes `<name>.fcpxmld/Info.fcpxml`), then `python3 ~/.claude/babi-skills/shared/tools/fcpxml_tools.py diff mine.fcpxml "<his>.fcpxmld"`. His export often shows more than he mentioned (e.g. pitch off on every retimed clip).
- **Reading his edit with volume keyframes (2026-11-24):** the project SQLite (`CurrentVersion.fcpevent`) does not show `adjust-volume` keyframes. Select the EVENT in the sidebar, `app_menu` File › Export XML… (opens the sheet in the background), `app_release` Final Cut, then press **Save** with full-screen control (Final Cut can be on the DELL: `switch_display`). One export holds every project in the event. Strip the event-level browser clips before re-importing a patched copy and keep project names + uids so Final Cut offers Replace.
- **Iterate in place, no v2/v3/v4 projects** (storage). Patch his exported XML and re-import the **same project name**, then press **Replace**. This keeps every manual change he made.
  - `fcpxml_tools.py patch` resizes captions to the safe zone.
  - `fcpxml_tools.py strip` makes a caption-free copy under a new name.
- **Exports:** Claude can't use File › Share (blocked), so **Babi presses ⌘E**. Claude can use File › Export XML.
- After each review, write the lesson, with numbers, into the right skill, or here if it applies to all. Then commit and push.
- **Version naming he uses (2026-11-21):** `<Topic> <Type> V<n>`, e.g. "Road Trip TH V1" (TH = talking head, 30 s hook), "Road Trip TH Full V1", "Coronation Vlog Long V1/V2", "Coronation Vlog talking V1", "Coronation Short Vlog V1". When he asks for "a second version", make a NEW project "… V2" from his V1 (here V2 projects are wanted; in-place Replace is for fixes).

## Babi's Nov 21 notes on rendered "real edits" (every skill)
Learned from his fixes to 12 edits built from raw footage (`Fall26/Exports/Trial Reels/Nov 21 Real Edits`, builders in `_tools/`):
- **No 1-frame clips at the end.** Every in-point, offset and duration in an FCPXML must sit on the project's 30 fps grid. Off-grid values (0.68 s shots, `start` with 1/1000 s precision) made Final Cut append a 0.033 s sliver of EVERY shot after the last clip. Round with `F(round(x*30), 30)` for `start`, `offset` and `duration`.
- **No clip shorter than ~0.25 s anywhere** (Babi, 2026-11-24: he deleted a 0.1 s sliver in the Tony variants). It came from flattening his compound clip, whose last piece was trimmed to 0.1 s. Copy only what's visibly on screen, and have every builder assert a minimum clip length.
- **B-roll back to back must abut exactly.** Per-shot rounding left 1-frame gaps/overlaps (Road Trip TH at 8:20). Snap a shot's end to the next shot's start when they're within 3 frames; never overlap on one lane.
- **B-roll on screen by ~1 s.** "At 1 second you should have B-roll going already… people have already scrolled." First burst at 0.9–1.0 s, not 4.6 s.
- **A burst doesn't spill into the next line** unless it hands off straight to the next burst (he moved IMG_1413 out of the next line, extended IMG_1440/1609 to fill to the line end).
- **Levels:** music was too quiet everywhere: he set the road-trip song to −11/−13 dB (I had −22/−23), Upside Down −15 (I had −24), Harvest Moon −11 (−21), The Mountain Is You −10 (−23). The road-trip talking clip (IMG_1902) was recorded quietly: he added +3.3/+3.4 dB on every line himself. That was his manual move on one quiet clip; never lift dialogue automatically (core rule 1).
- **Talking vlogs get little B-roll.** On Coronation he kept 3 of 9 shots (Long V1), 2 (talking V1, Short Vlog V1), 0 (Long V2): "it doesn't really make sense for this type of vlog". Keep his face; B-roll only for a real view/sunrise.
- **Never butt two different takes together as one thought** ("we got some boys training for the Ironman" + "we got people swimming" were separate takes; he cut one).
- **Keep the human tails** ("at least for now, it's like…" stays).
- **Don't cut inside-the-car → outside → inside-the-car**; drop the odd location clip (Coronation Vlog Long V2, ~20 s).
- **Don't clip soft first words / word tails:** "Today" (whisper 0.94) was cut at 1.25 by an energy onset; he pulled it to 0.87. "Vancouver" tail cut at 1.78, he extended to 1.83. Never start after whisper's first-word start − 0.07 s or end before its last-word end + 0.08 s (unless the stamp is stretched > 0.35 s).
- **Captions and top text are PURE WHITE** (the storytelling-skill look: Helvetica Neue Bold, `1 1 1 1`, shadow 0.75 / 4 @ 315 / blur 8). When burning text into an HLG render, draw it at RGB 255, not the 208 "HLG reference white": 208 looked dim grey to him (Nov 21). No yellow highlights on top captions unless asked.
- **Final Cut Basic Titles don't wrap:** a long top caption ran off screen (Montage 2). Insert line breaks (`&#10;`) yourself at ≈ 860 px using FCP width ≈ 1.8 × PIL.
- **Montage labels must sit on their footage** (province labels drifted a frame per 0.68 s shot): use whole-frame shot lengths.
- Reading his edits without asking: File › Export XML of each project (select in browser, `app_menu` File › Export XML…, then a full-screen click on Save to Desktop), then `_tools/fromxml.py` turns his export into a render spec so his version can be rendered as posted.

## Final Cut import gotchas
- **Every clip used in an edit must be a browser clip in the event (Shift-F must find it), imported with "Leave files in place".** An FCPXML whose event holds only the project creates the assets but no browser clips: Shift-F finds nothing and Babi can't browse alternates (Golden Run event had 0 clips, 2026-11-16). Two parts:
  1. In the XML, add an event-level `<asset-clip ref=… name=… start duration format tcFormat="NDF" audioRole=…/>` for every used asset that has none (stills: `<clip name start="3600s" duration="10s"><video ref duration="0s"/></clip>`). Export the event first (select it in the sidebar, File › Export XML) to see which already exist, or re-imports duplicate them. `babi-storytelling/scripts/patch_v3.py` does this.
  2. Then File › Import › Media (⌘I) on the event: select the source folders the B-roll came from, **Add to existing event**, **Leave files in place**, keywords from folders, Import Selected, Continue past "unsupported files" (xml/py/json). Already-imported files are skipped.
- **Import the whole day folder, not just the clips the edit uses** (Babi, 2026-11-20: "import all the videos, then choose B-roll to put over it, then I can still go back and look at all the videos"). Every builder writes an asset + event browser clip for every file in the folder (stills as `<clip><video/></clip>`), and only then picks B-roll from it.
- **Reusing media already in a library without Final Cut access:** the event's `CurrentVersion.fcpevent` is SQLite; in `ZCOLLECTION` join `ZCOLLECTIONMD`, each `FFMediaRep` blob holds the file name and a 32-hex id, and that id is the FCPXML asset `uid`. Put it on the asset (`uid="…"`) so a re-import reuses the media instead of duplicating it. Skip event clips for files that already have a browser clip (count `FFAnchoredCollection`).
- **Asset ids must be XML names:** a file like "need to market app.M4V" needs a sanitized id (`a_need_to_market_app`), or DTD validation fails.
- **`srcEnable="video"` is ignored on import** (2026-11-20): B-roll came in WITH its audio. Mute every B-roll clip with `<adjust-volume amount="-96dB"/>`.
- **Shaky B-roll is out** (Babi, 2026-11-20). Score camera shake before picking: `tools/shake_score.py CLIP1,CLIP2 tag` prints mean global motion per second (px/frame at 144 px wide); keep windows ≤ ~0.5.
- **Re-importing a patched XML:** export the project again first and patch that export. A project export has no event clips and keeps Final Cut's uids, so nothing duplicates. Rebuilding from the older export re-adds browser clips and new still assets.
- **Vertical iPhone clips: declare the asset format as 1080×1920, never 1920×1080.** ffprobe reports rotated clips as 1920×1080 with rotation −90; a from-scratch FCPXML that copies those numbers makes Final Cut pillarbox every clip tiny in the viewer (Nov 15 Golden Run, 2026-11-15). Final Cut's own exports write `width="1080" height="1920"`. Swap width/height whenever the stream has rotation side data.
- **HLG browser clips look blown out after an FCPXML import (2026-11-25, Summer Camera Roll):** Final Cut 12.4 gives XML-imported browser clips Color Conform = Automatic / Conversion None, so the HLG plays unconverted in the browser and viewer (thumbnails cyan/yellow, clipped), while the same clips in a Rec. 709 project look right. Fix in the UI: select the event's clips (click one, cmd+A), Inspector › Video › Color Conform › Type **Manual**, Conversion Type **HDR (HLG) to SDR**; then put any SDR clip (e.g. an h264 bt709 MP4) back to Automatic. Re-importing a fixed XML does NOT help: Final Cut relinks the existing assets (the new event gets no Original Media).
- **Never AXPress (app_click by element) a browser clip:** pressing a clip's AXGroup APPENDS it to the open project's storyline (it added 3 clips to Babi's open project). Select browser clips with a real full-screen left_click only, and check Edit › Undo's title after any click in the browser.
- **Validate before importing:** `xmllint --noout --dtdvalid <copy of FCPXMLv1_11.dtd> file.fcpxml` (the DTD is in `Final Cut Pro Creator Studio.app/Contents/Frameworks/Interchange.framework/Versions/A/Resources/`; copy it somewhere without spaces first).
- Import with `open -a "Final Cut Pro Creator Studio" file.fcpxml`, then pick the library (Down, Return). A new library comes from New… in that dialog.
- Final Cut **reads the XML when the dialog opens**. Rebuild the file first; if you rebuilt while the dialog was up, cancel and re-open.
- **Wispr Flow's floating window blocks clicks** on dialogs. Press buttons through accessibility (`app_screenshot` the alert window, then `app_click` by element_index) or use the keyboard.
- **A `title` with `adjust-transform`:** the transform must come after `param`, `text` and `text-style-def` (DTD order), or validation fails.
- **Double-clicking the viewer opens full-screen playback**, which ignores background keys. Press Esc with full-screen control. To open a project, double-click its thumbnail in the browser, not the viewer.
- Double-clicking a project to open it can switch on a clip's transform handles. Click Done in the viewer; nothing moves.

## Tools (`~/.claude/babi-skills/shared/tools/`)
- `shake_score.py`: per-second camera-shake score for clips in the Nov 18 folder (edit `D` for another folder).
- `fcpxml_tools.py`: `diff` / `patch` / `strip` (see above).
- `sound_classify.swift`: Apple SoundAnalysis sound labeller, no download needed. Build with `swiftc -O sound_classify.swift -o sa`, then run `./sa file.wav` (48 kHz mono). It names SFX in a reference reel and finds clean sounds inside SFX compilation mp3s.
- Whisper venv: `~/.claude/whisper-venv/bin/python` (faster-whisper small.en / medium.en, cached).
- `yt-dlp` (Homebrew) downloads reference reels. Collect profile reel URLs in the built-in browser.
- **Screenshots of our own sites** (membership.io, stumclaren.com) beat stock photos whenever the speaker names our product, pricing or offer. Capture full pages with headless Chrome (`--headless=new --window-size=1440,7000 --screenshot=…`) and crop with PIL (see babi-knowledge-reels).
- **Internet photos (fallback):** Openverse API (`https://api.openverse.org/v1/images/?q=…&license_type=commercial`). Fetch with **curl**, because Python urllib fails SSL on this Mac. Save the licence and creator to `photo_sources.json`, and convert WebP files that arrive named .jpg. The builder is `babi-knowledge-reels/scripts/build_knowledge_reel.py`.
- `grab_sdr_frame.swift`: exact-frame PNG grab from iPhone HLG clips, tone-mapped to SDR via AVFoundation (`swiftc -O grab_sdr_frame.swift -o grab; ./grab clip.MOV 3.68 out.png`). Use it for stills you send to AI image tools.
- **ChatGPT images (desktop app, Babi's account):** it age-swaps or restyles real people well (2026-11-16, 12 of 12 accepted on the first try).
  - Load the frame with `osascript -e 'set the clipboard to (read (POSIX file "…png") as «class PNGf»)'`, then with **full-screen control** press cmd+N (new chat), click the message box, cmd+V, type the prompt, Return, and wait about 70 s.
  - To save, right-click the image › Save image as… › type the name (cmd+A is blocked in the save sheet; typing replaces the name) › Return. It lands in ~/Downloads; then move it.
  - Wispr Flow's invisible overlay blocks clicks in the centre-bottom of that screen. Click the left part of the message box (x≈300) and the upper-left of the image.
  - Stop if Claude becomes frontmost mid-type (the user is clicking around). The draft persists into the next chat, so clear it with cmd+A, Delete.
  - Background `app_menu` Paste is refused (clipboard), so this needs full-screen control.
- **Reading Babi's finished edit without taking his screen:** File › Export XML is disabled in the background. Use his export instead (`Exports/OFFICE/<project>.m4v`): frame-diff cuts, whisper for timings, RMS bursts for SFX, cross-correlation against candidate songs for the music offset and gain, and pixel scans for caption size and position. `Original Media/` in the event lists every file he added (e.g. his own regenerated images). Find new songs with `find … -newermt` on ~/Downloads and the Songs folder.
- **Music level check:** ffmpeg `ebur128` on the dialogue render and on the song slice at its dB; a bed 12–15 LU under speech sits well (Take Five at −15 dB was 13.4 LU under).
