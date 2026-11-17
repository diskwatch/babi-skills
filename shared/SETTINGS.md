# Shared settings and tools (ALL Babi skills)

Every Babi skill (storytelling, vlog-reels, simple-reels, copy-format, ezromo-style, knowledge-reels) follows this page. Read it before building anything. A skill's own page adds style rules on top. When a lesson applies to every skill, it goes here, not in one skill.

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
- **Helvetica Neue Bold in FCP ≈ 1.34 × PIL's width at the same size** (FCP 30 ≈ PIL 40). Use this to width-check lines before building.
- **Arial Black ≈ 1.45 × fontSize px per capital**, so width-cap with size ≤ maxWidth / (1.45 × letters). Calibrate once for any other font.
- **Fill plus outline:** `strokeWidth` must be negative. The font must be installed, or Final Cut silently swaps it.
- **Time captions from the cut's own audio.** Render the planned cut with ffmpeg (atrim, plus atempo for speed changes), transcribe that, and caption from it. Raw-clip whisper drifts up to 1.2 s across pauses. Re-check unclear lines with medium.en on just that slice.
- **Spellings:**
  - **BABI** (whisper and the voice typer write "Bobby").
  - Uncle **Genia**, nickname **Gen**.
  - No punctuation in captions.

## Working with Babi's edits (every skill)
- **Read his edit before changing anything.** Use File › Export XML (FCP writes `<name>.fcpxmld/Info.fcpxml`), then `python3 ~/.claude/babi-skills/shared/tools/fcpxml_tools.py diff mine.fcpxml "<his>.fcpxmld"`. His export often shows more than he mentioned (e.g. pitch off on every retimed clip).
- **Iterate in place, no v2/v3/v4 projects** (storage). Patch his exported XML and re-import the **same project name**, then press **Replace**. This keeps every manual change he made.
  - `fcpxml_tools.py patch` resizes captions to the safe zone.
  - `fcpxml_tools.py strip` makes a caption-free copy under a new name.
- **Exports:** Claude can't use File › Share (blocked), so **Babi presses ⌘E**. Claude can use File › Export XML.
- After each review, write the lesson, with numbers, into the right skill, or here if it applies to all. Then commit and push.

## Final Cut import gotchas
- **Vertical iPhone clips: declare the asset format as 1080×1920, never 1920×1080.** ffprobe reports rotated clips as 1920×1080 with rotation −90; a from-scratch FCPXML that copies those numbers makes Final Cut pillarbox every clip tiny in the viewer (Nov 15 Golden Run, 2026-11-15). Final Cut's own exports write `width="1080" height="1920"`. Swap width/height whenever the stream has rotation side data.
- **Validate before importing:** `xmllint --noout --dtdvalid <copy of FCPXMLv1_11.dtd> file.fcpxml` (the DTD is in `Final Cut Pro Creator Studio.app/Contents/Frameworks/Interchange.framework/Versions/A/Resources/`; copy it somewhere without spaces first).
- Import with `open -a "Final Cut Pro Creator Studio" file.fcpxml`, then pick the library (Down, Return). A new library comes from New… in that dialog.
- Final Cut **reads the XML when the dialog opens**. Rebuild the file first; if you rebuilt while the dialog was up, cancel and re-open.
- **Wispr Flow's floating window blocks clicks** on dialogs. Press buttons through accessibility (`app_screenshot` the alert window, then `app_click` by element_index) or use the keyboard.
- **A `title` with `adjust-transform`:** the transform must come after `param`, `text` and `text-style-def` (DTD order), or validation fails.
- **Double-clicking the viewer opens full-screen playback**, which ignores background keys. Press Esc with full-screen control. To open a project, double-click its thumbnail in the browser, not the viewer.
- Double-clicking a project to open it can switch on a clip's transform handles. Click Done in the viewer; nothing moves.

## Tools (`~/.claude/babi-skills/shared/tools/`)
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
