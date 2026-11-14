# Babi skills

These are Claude Code skills for how Ariel ("Babi") edits video. Each one is built from real corrections to Claude's edits.

| Skill | Use it for |
|---|---|
| `babi-storytelling` | Stu and office storytelling recaps: tight talking head, B-roll bursts, chat pops, sound effects, music (Final Cut) |
| `babi-vlog-reels` | Personal run, friend and day vlogs: the 2TB folders, selects timelines, tight vlog cuts, small one-word captions (Edits or Final Cut) |
| `babi-simple-reels` | To-camera Instagram promos: best takes, hook first, bold yellow-keyword social captions (Final Cut) |
| `babi-ezromo-style` | Funny vlogs in ez.romo's (Evan's) style: hype hook, no dead space, pitch-off speed ramps, punch-ins, few big SFX, safe-zone one-word captions (Final Cut) |
| `babi-copy-format` | Copy a reference reel's format (beat drop, cut rhythm, caption style). Combine it with any of the above |

**Shared by every skill:** `shared/SETTINGS.md` (Rec. 709, Instagram safe zone, caption geometry, editing Babi's own edit in place with Replace, Final Cut import gotchas) and `shared/tools/` (fcpxml_tools.py, sound_classify.swift).

## Set up on a Mac
```bash
gh auth login
git clone https://github.com/diskwatch/babi-skills.git ~/.claude/babi-skills
mkdir -p ~/.claude/skills
for d in ~/.claude/babi-skills/*/; do ln -s "$d" ~/.claude/skills/$(basename "$d"); done
```
Then follow "Setting up on a new Mac" in `babi-storytelling/SKILL.md` (ffmpeg, the Whisper venv, computer use).

## Keep in sync
- Before editing, run `git -C ~/.claude/babi-skills pull`.
- After a lesson, commit and push from `~/.claude/babi-skills`.
