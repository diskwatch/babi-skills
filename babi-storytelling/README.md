# Babi Storytelling

A Claude skill that holds how Ariel ("Babi") edits storytelling videos in Final Cut Pro: tight talking-head cuts, B-roll, chat-screenshot pops with sound effects, music and captions. It's built from real corrections to Claude's edits and is updated as we go.

- `SKILL.md`: the playbook Claude follows. Start with the "Quick rules" section.
- `scripts/`: helper tools:
  - `transcribe.py`: word-level transcripts
  - `build_reel_template.py`: first-cut FCPXML builder
  - `add_chat_pops.py`: synced screenshot pops
  - `broll_pool_example.json`: B-roll pool format

## Install

**Claude Code (Mac, any device):**

```bash
git clone https://github.com/diskwatch/babi-storytelling.git ~/.claude/skills/babi-storytelling
```

Start a new Claude Code session; the skill loads automatically when you ask for this kind of edit, or run `/babi-storytelling`.

**Get the latest version:**

```bash
cd ~/.claude/skills/babi-storytelling && git pull
```

**claude.ai / Claude desktop chat:** download the repo as a ZIP (Code → Download ZIP). Then upload it under **Settings → Capabilities → Skills**. Re-upload after updates.

**Share with someone:** add them as a collaborator (repo **Settings → Collaborators**). They then install it the same way.

## Requirements for the scripts
`ffmpeg`/`ffprobe` (Homebrew), Python 3, and a venv with `faster-whisper` and `pillow`. Several paths in `SKILL.md` point at Ariel's own drive (`/Volumes/4TBSSD_4/...`). Change them for your own setup.
