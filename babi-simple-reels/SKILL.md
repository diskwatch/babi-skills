---
name: babi-simple-reels
description: Ariel ("Babi") playbook for simple Instagram reels. These are one person talking to camera with a single message: a promo, an announcement, a tip, a CTA ("Black Friday" style). The work is picking the best take of each line from many retakes, cutting it very tight, adding a hook and bold one-word social captions, and building it as a Final Cut timeline (or in Edits). Use for "make a reel of this", "cut this promo", "best takes + captions", "Instagram reel from these takes". Not for storytelling recaps with B-roll bursts (babi-storytelling) or personal vlogs (babi-vlog-reels). Combine with babi-copy-format when the user gives a reference reel to copy.
---

# Babi simple Instagram reels

A simple reel is one speaker and one message, usually 30–60 s, made from takes shot with a producer. Every rule here came from the user correcting Claude. Add new lessons with numbers, then commit and push (see the end of this file).

## Rules (from the Black Friday reel, Nov 12)
1. **Edit in Final Cut, not as a rendered file.** The user rejected an ffmpeg render, so build an FCPXML. Media and library details are in babi-storytelling's "Where things live" (TME library, `/Volumes/4TBSSD_4/Babi NR Content/Media/OFFICE/<Mon D Topic>/`, XML in `…/XML/`).
2. **Use the best take of each line.** Read the whole transcript; producer sessions are full of retakes. Take the last clean one, then re-transcribe each chosen take on its own to catch hidden restarts.
3. **Skip takes where the speaker laughs or stumbles,** even if the words are right. For example, the "packaged it" take at 668 s was out for laughing, and the 454 s take was out for a stumble ("plans of our software"), replaced by the take at 422.8 s.
4. **Cut very tight:**
   - Start each line on its first content word; drop "And / So / But / Okay".
   - Cut every pause of about 0.1 s or more, including inside lines.
   - Leave no silent holds.
   - Whisper's word ends run long, so find the real end in the 10 ms RMS energy and keep a trailing "s".
5. **Open on the hook.** The first line should be the most striking claim or number, not "Hey guys".
6. **End on the CTA** if there is one (for example, IMG_0087 7.0–11.6 s for Black Friday), then cut out right after the last word.

## Captions (default for these reels; still confirm with the user)
- One word at a time, **Avenir Next Heavy, all caps**, white with a black outline and a soft shadow, just below centre.
- **Numbers and key words in yellow.**
- No punctuation.
- Black Friday had 172 Basic Title captions.
- **Final Cut title gotchas:**
  - `font` must be an installed family ("SF Pro" silently becomes Helvetica at the wrong size).
  - `strokeWidth` must be **negative** for fill plus outline.
  - `shadowOffset="5 315"`.
  - The Basic Title uid is `.../Titles.localized/Bumper:Opener.localized/Basic Title.localized/Basic Title.moti`.
- Avoid one-frame overlaps between consecutive captions (the Black Friday v1 had 15). Make each caption end exactly where the next starts.
- If built in **Edits** instead: CC › Generate captions › the plain one-word template, 20pt, "Apply to track", then Replace "." "," "?" with nothing.

- **Projects are ALWAYS Rec. 709** (Babi, 2026-11-14). In FCPXML the *sequence* format must say `colorSpace="1-1-1 (Rec. 709)"`. Never copy the clips' `9-18-9 (Rec. 2020 HLG)` onto it, because that is why projects came out "Rec. 2020 HLG". Asset formats keep HLG; FCP converts on render. Final Cut has no global default: a new project made by hand with Automatic settings copies the first clip (HLG). So use Use Custom Settings › Color Space › Standard – Rec. 709 (FCP remembers the last custom settings), or fix an existing project with Inspector › Modify › Color Space.

## Music and SFX
- Ask. Default to none, or a quiet bed at about −13 dB flat. Songs are in `/Volumes/4TBSSD_4/Babi NR Content/Songs/`.
- Use a pop or ding only on a big number or reveal. The sounds and levels are in babi-storytelling.

## Workflow
1. Copy the takes to the SSD media folder.
2. Probe them: HEVC 10-bit HLG, vertical.
3. Transcribe with medium.en word timings.
4. Write a line list: hook → points → CTA, with the chosen take and the in/out for each.
5. Build the FCPXML: talking head on the spine, captions as titles on lane 1, music on −1. Import into TME under a new project name, never overwriting the user's.
6. Verify:
   - Render the cut audio and re-transcribe it to confirm no clipped words.
   - Check caption frames in the viewer (Control-P plus a timecode).
   - Report what you checked.
7. The user exports with ⌘E; Claude can't press Share. Exports go to `/Volumes/4TBSSD_4/Babi NR Content/Exports/OFFICE/`.

## Updating this skill
This lives in the same skills repo as the others (see babi-storytelling's "Updating this skill").
1. Edit with the lesson: numbers, before/after, which reel it came from.
2. Add a changelog line.
3. Commit and push.

## Changelog
- 2026-11-14: projects always Rec. 709 (sequence format colour space).
- 2026-11-14 v0.1: split out from the Black Friday reel lessons (best takes, no laughing or stumbles, tight cuts, social captions, edit in Final Cut).
