# Babi skills

These are Claude Code skills for how Ariel ("Babi") edits video. Each one is built from real corrections to Claude's edits.

## How to use them (read order, kept short on purpose)
1. `shared/SETTINGS.md` › **Core rules** (gain, edges, captions, headers, music, photo pops). These override anything older.
2. The one skill that fits the content (routing below), and its **SKILL.md only**.
3. That skill's `LESSONS.md` / `FORMATS.md` section for the same kind of reel. Read it only when building that kind.
4. `shared/BROLL.md` (mirror of `Babi NR Content/BROLL-INDEX.md`) before searching the SSD for B-roll, and `Babi NR Content/Photos/Stu McLaren/README.md` for photos of Stu.
5. After Babi edits your cut: `python3 shared/tools/recover.py mine.fcpxml his/Info.fcpxml`. Put the measured lessons into the core rules or the skill, and the dated story into LESSONS.md.

**Routing:**

| Content | Skill |
|---|---|
| Story or recap with B-roll; Stu panel moments; walk-and-talk stories | babi-storytelling |
| One person, one message to camera (promo, announcement, CTA, scripted takes) | babi-simple-reels |
| Teaching: numbers, a framework, a whiteboard | babi-knowledge-reels |
| Funny bits out of long footage | babi-funny-moments |
| Swapped-question vox pop | babi-misled-interviews |
| Personal run / day / friend vlogs | babi-vlog-reels |
| Funny vlog in Evan's style | babi-ezromo-style |
| "Make it like this reel" | babi-copy-format, plus one of the above for taste |

Field Producer (`~/Code/Claude Projects/field-producer`) runs shoots end to end and must route every reel through these skills.

| Skill | Use it for |
|---|---|
| `babi-storytelling` | Stu and office storytelling recaps: tight talking head, B-roll bursts, chat pops, sound effects, music (Final Cut) |
| `babi-vlog-reels` | Personal run, friend and day vlogs: the 2TB folders, selects timelines, tight vlog cuts, small one-word captions (Edits or Final Cut) |
| `babi-simple-reels` | To-camera Instagram promos: best takes, hook first, bold yellow-keyword social captions (Final Cut) |
| `babi-ezromo-style` | Funny vlogs in ez.romo's (Evan's) style: hype hook, no dead space, pitch-off speed ramps, punch-ins, few big SFX, safe-zone one-word captions (Final Cut) |
| `babi-knowledge-reels` | Teaching / knowledge reels: internet photos that match each line popping on the chest, karaoke captions (spoken word yellow), topic header, big dollar figures, whiteboard zoom (Final Cut) |
| `babi-funny-moments` | Pull funny moments from long raw footage (meetings, team days): Sony SD ingest + NR SSD layout, laughter finder, every clip imported + one selects project with a clip per moment (Final Cut) |
| `babi-misled-interviews` | Vox-pop sketch: ask coworkers one question, swap the interviewer audio for another ("favorite part of your job?"), mute the original until the answer, top question caption + one-word captions on his Final Cut export |
| `babi-copy-format` | Copy a reference reel's format (beat drop, cut rhythm, caption style). Combine it with any of the above |

**Shared by every skill:** `shared/SETTINGS.md` (Rec. 709, Instagram safe zone, caption geometry, editing Babi's own edit in place with Replace, Final Cut import gotchas) and `shared/tools/` (fcpxml_tools.py, sound_classify.swift).

## Set up on a Mac
```bash
gh auth login
git clone https://github.com/diskwatch/babi-skills.git ~/.claude/babi-skills
mkdir -p ~/.claude/skills
for d in ~/.claude/babi-skills/*/; do ln -s "$d" ~/.claude/skills/$(basename "$d"); done
```
Then follow "Setting up on a new Mac" in `babi-storytelling/LESSONS.md` (ffmpeg, the Whisper venv, computer use).

## Keep in sync
- Before editing, run `git -C ~/.claude/babi-skills pull`.
- After a lesson, commit and push from `~/.claude/babi-skills`.
