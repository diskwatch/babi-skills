# B-roll index (read this before searching the SSD)
Built Nov 27 2026 from Babi's own finished edits and the skill notes. Only list a clip as approved if Babi used or kept it. Add a row whenever he keeps a new clip; mark rows he deletes. Mirror: `~/.claude/babi-skills/shared/BROLL.md`.

Path shorthand: `B` = `/Volumes/4TBSSD_4/Babi NR Content`, `O` = `B/Media/OFFICE`.

## 0. Added from the Laurier reels (Nov 26 panel, reviewed Nov 27)
| What it shows | Path | In-point(s) s | Babi's verdict |
|---|---|---|---|
| Stu at his studio desk, red shirt | `O/Nov 12 Black Friday/Creator Lab B-Roll/IMG_9869.MOV` | 3.1 | Praised ("exactly what we want"), Big Mistake ~32 s "building businesses my own way" |
| Stu at the office whiteboard, red shirt | `O/Nov 12 Black Friday/Creator Lab B-Roll/IMG_9905.MOV` | 2.3 | Praised, same burst |
| Stu on the QSELF stage at Queen's, gold balloons | `O/Nov 6 QSELF/A001_11061741_C034.MOV` | 1.0 | Kept (Big Mistake "what he's been doing for the last 25 years") |
| Stu presenting to students at Queen's ("If you don't ask" slide) | `O/Nov 6 QSELF/IMG_9503.MOV` | 7.1 | Kept (Big Mistake, Momentum) |
| QSELF crowd / room | `O/Nov 6 QSELF/IMG_9520, 9481, 9476, 9522.MOV` | 1.67, 0.92, 1.13, 1.12 | Kept ("Q self B-roll is pretty good", Momentum) |
| Stu at the Immersion Day boardroom whiteboard, navy | `O/November 18th Immersion Day/IMG_0763.MOV`, `IMG_0779.MOV` | 0.3; 10.5 | Laurier round 3 (AI Line), not yet reviewed |
| Rick texting the AI (zoom 1.3, pos 0 -15) | `O/November 18th Immersion Day/IMG_0806.MOV` | 9.0 | Laurier round 3 (AI Line), not yet reviewed |
| Stu + Rick laughing at a desk | `O/November 18th Immersion Day/IMG_0757.MOV` | 9.0 | Laurier round 3 (AI Line), not yet reviewed |
| Photos of Stu (grad 2002, soccer clipping, Kenya, president, family, Sam, 29029, young Stu + Amy) | `B/Photos/Stu McLaren/` (README says when to use each) | stills | Grad + family photos praised; one photo per pop |

## How approval is tiered in this file

| Tier | Meaning | Where it appears |
|---|---|---|
| A | Present in a Final Cut project Babi built or hand-edited, read from an exported XML (`Stu Queens Recap 1`, `CLR user v3` = "Creator Lab Reel - chat pops"). In-points come from that XML (`start` of each clip). | Sections 1.1 to 1.4 |
| B | Named by Babi (or in his notes) in a babi-* SKILL.md line, with in-point. | Sections 1.1 to 1.4 |
| C | Claude picked it following Babi's written note (Immersion Day Story v2). Babi's notes name the shots marked "(named)" but the finished edit was not read back. | 1.1 / 1.3, marked C |
| none | Tagged or pooled by Claude, no Babi reaction on record. | Section 5 only |

"Steady" means measured with `shared/tools/shake_score.py` at 0.0 px/frame where the source says so. All B-roll is used muted (-96 dB).

Clip locations
- Creator Lab clips: `O/Nov 12 Black Friday/Creator Lab B-Roll/IMG_98xx.MOV` (all verified present)
- Queen's / QSELF keynote clips: `O/Nov 6 QSELF/IMG_9xxx.MOV` and `O/Nov 6 QSELF/A001_*.MOV` (all verified present)
- Stew Vids (phone clips from the QSELF trip): `O/Nov 6 QSELF/Stew Vids/IMG_70xx 2.MOV` (all verified present)
- Immersion Day: `O/November 18th Immersion Day/IMG_0xxx.MOV`

---

## 1. Approved B-roll by category

### 1.1 People

| What it shows | Full path | In-point(s) s | Source of approval | Notes |
|---|---|---|---|---|
| Marcus (developer) smiling, 3 jump cuts of 0.7 s | `O/Nov 12 Black Friday/Creator Lab B-Roll/IMG_9883.MOV` | 6.4, 7.6, 8.8 | A: `O/Nov 12 Black Friday/XML/CLR user v3.fcpxmld` (project "Creator Lab Reel - chat pops"). B: babi-storytelling SKILL.md, "Marcus, one of our developers" -> IMG_9883 @6.4/7.6/8.8 ("use this clip for Marcus") | Use whenever Stu says "Marcus". Babi's rule: stack options, one enabled. |
| Developer laughing at his desk | `O/Nov 12 Black Friday/Creator Lab B-Roll/IMG_9884.MOV` | 1.6, 3.3 | B: babi-storytelling SKILL.md ("people absolutely can't wait to buy") | In the skill line but NOT in the `CLR user v3` export, so Babi may have cut it later. Treat as B, lower confidence. |
| Team member in green walking through the office (follow shot, works across two lines) | `O/Nov 12 Black Friday/Creator Lab B-Roll/IMG_9892.MOV` | 1.5, 3.2, 5.0 (walking), 6.7, 7.7, 9.4, 13.2 (heading into studio) | A: CLR user v3. B: SKILL.md "teach the training" and "after the workshop they'd log off" | One person, one take, acts like a mini story. Babi's favourite; Claude had skipped it for lack of a FCP uid. |
| Team crowding round a developer's screen, 1.1 s each | `O/Nov 12 Black Friday/Creator Lab B-Roll/IMG_9890.MOV` | 1.9, 3.5, 5.1 | A: CLR user v3. B: SKILL.md "loved the training" | Group / team. |
| Pan from a developer to a colleague, 0.4-0.65 s shots | `O/Nov 12 Black Friday/Creator Lab B-Roll/IMG_9901.MOV` | 3.9, 4.8, 5.8, 7.4, 17.4 | A: CLR user v3. B: SKILL.md "it's a doorway" | Fast pan; keep each piece under 0.7 s. |
| Single shot (content not described in any note) | `O/Nov 12 Black Friday/Creator Lab B-Roll/IMG_9891.MOV` | 1.4 | A: CLR user v3 (1 used, 1 disabled copy) | No description recorded. Pool tag (Claude): team, build. A second copy is disabled in the file. |
| Not described in any note | `O/Nov 12 Black Friday/Creator Lab B-Roll/IMG_9895.MOV` | 2.6, 5.1 | A: CLR user v3 | No description recorded. Pool tag (Claude): screen, build. |
| Debrief with Stu | `O/Nov 12 Black Friday/Creator Lab B-Roll/IMG_9904.MOV` and `IMG_9905.MOV` | 9904 @33.5; 9905 @2.3 | A: CLR user v3 | No description recorded. Pool tags (Claude) call both "debrief, Stu". |
| Stu presenting / explaining with open hands at the whiteboard | `O/November 18th Immersion Day/IMG_0763.MOV`, `IMG_0761.MOV`, `IMG_0801.MOV`, `IMG_0764.MOV` | 0763 @0.3; 0761 @0.8; 0801 @10.0; 0764 @9.0 | C: `O/November 18th Immersion Day/XML/Story/build_story.py` SHOTS (Babi's 2026-11-21 notes in SKILL.md). Descriptions from `XML/notes_*.json` | Stu = navy shirt at the whiteboard. 0801 is a man in a dark shirt grinning with the whiteboard behind. All steady (0.0 px/frame). |
| Rick texting the AI (zoom 1.6, position 0,-20 hides a bald head in the foreground) | `O/November 18th Immersion Day/IMG_0806.MOV` | 9.0 (one 2.5 s shot) | B: SKILL.md "Rick: younger guy in black cap + Membership.io jacket ... shown texting the AI instead (0806 @9)" | Rick = younger guy, black cap, Membership.io jacket. Babi said to REMOVE IMG_0797 (Rick at desk with laptop) and avoid 0792. |
| Stu and Rick chatting/laughing at a desk | `O/November 18th Immersion Day/IMG_0757.MOV` | 14.0 (chatting), 9.0 (laughing) | C: build_story.py SHOTS ("our team" / "just a bit of yapping") | Best Immersion Day laugh clip per Claude tags: IMG_0757 6-9 s score 5. |
| Lisa filming the demo and smiling (woman in pink, side view) | `O/November 18th Immersion Day/IMG_0794.MOV` | 0.5 | C: build_story.py SHOTS ("rebuilt their entire landing page") | Lisa = blonde, pink jacket (IMG_0821 interview). |
| Mike chin on hand listening (bald, glasses) | `O/November 18th Immersion Day/IMG_0776.MOV` | 4.5 | C: build_story.py SHOTS comment "Lisa, Mike" | Mike = bald, glasses, grey sweater (IMG_0820 interview). The Claude note for 0776 near 4.5 s says "bald glasses guy listening chin on hand". |
| Presenter grins/chuckles, hands clasped (Stu) | `O/November 18th Immersion Day/IMG_0775.MOV` | 5.0, 12.3 | C: build_story.py SHOTS | Tight, sharp. |
| Members chatting / Lisa laughing | `O/November 18th Immersion Day/IMG_0829.MOV` | 12.0 | C: build_story.py SHOTS ("hear it from them") | Same line as Mike + Lisa interview cut-in. |
| Mike and Lisa full interviews (the real clips) | `O/November 18th Immersion Day/IMG_0820.MOV` (Mike), `IMG_0821.MOV` (Lisa) | per `XML/Interviews/segments.py` segs 1,2,3,11,18 | B: SKILL.md "Hear it from them -> cut to Mike + Lisa"; builder `XML/Story/build_story.py` GUEST_SEGS | These are A-roll guests, not B-roll, but are the approved Mike/Lisa clips. |
| Amy | none recorded | | | Memory `field-producer.md`: Amy is STU's wife (not Babi's). No Amy B-roll is cited anywhere. Laurier bookstore story names her but uses no footage of her. |

### 1.2 Places

| What it shows | Full path | In-point(s) s | Source of approval | Notes |
|---|---|---|---|---|
| Queen's / QSELF event footage: audience, stage, panel, venue (13 shots, 0.78-0.85 s each) | `O/Nov 6 QSELF/IMG_9399.MOV` | 0.5, 3.4, 0.6, 3.1, 12.0, 16.5 | A: `O/Nov 9 QSELF Stu Recap/XML/Stu Queens Recap 1.fcpxmld` (Babi's reference edit) | Most-used clip in the reference edit (6 pieces). What exactly is in frame was not recorded; pull a frame before using. |
| Same reference edit, further QSELF clips | `O/Nov 6 QSELF/IMG_9401.MOV` @1.5, 2.9; `IMG_9408` @6.6; `IMG_9398` @2.4; `IMG_9418` @24.2; `IMG_9420` @1.4, 5.2; `IMG_9426` @2.1, 3.5; `IMG_9441` @12.9 (2.4 s); `IMG_9442` @9.0, 10.8; `IMG_9444` @0.0; `IMG_9446` @8.2 (panel room); `IMG_9358` @1.4; `IMG_9374` @5.3; `IMG_9392` @2.2, 3.3, 4.5; `IMG_9487` @1.6; `IMG_9503` @7.1, 10.7 | as listed | A: Stu Queens Recap 1.fcpxmld | Each piece is ~0.8 s (one-clip bursts of 3-5 jump cuts). Only IMG_9446 has a text description (panel room, from `Nov 9 .../build_reel_format.py`). |
| QSELF crowd / event moments, second half of the recap | `O/Nov 6 QSELF/IMG_9449.MOV` @3.5; `IMG_9464` @3.6; `IMG_9466` @0.4 (1.1 s); `IMG_9468` @1.6; `IMG_9474` @2.3; `IMG_9476` @1.1; `IMG_9520` @1.7; `IMG_9522` @1.1; `IMG_9529` @5.4 (2.7 s); `IMG_9532` @8.6 (1.85 s) | as listed | A: Stu Queens Recap 1.fcpxmld | Used in the last third of the recap. Contents not described. |
| Phone clips from the trip ("Stew Vids") | `O/Nov 6 QSELF/Stew Vids/IMG_7061 2.MOV` @22.1, 5.1, 22.0; `IMG_7064 2` @9.3; `IMG_7066 2` @2.9; `IMG_7073 2` @1.2, 4.6; `IMG_7075 2` @21.8, 24.2; `IMG_7076 2` @20.8; `IMG_7089 2` @6.2, 7.3; `IMG_7091 2` @3.1, 7.8; `IMG_7092 2` @50.1 | as listed | A: Stu Queens Recap 1.fcpxmld | Used in the opening and middle of the recap. Contents not described. Keyword "stew vids" is already on them in the TME library. |
| Walk from the lab room into Stu's studio | `O/Nov 12 Black Friday/Creator Lab B-Roll/IMG_9865.MOV` | 3.1 (3.1 s), and speed-ramp walk from the lab room into Stu's studio (Fast 1091% then 149%) | A: CLR user v3 (@3.1). B: SKILL.md "I run a workshop" | Skill note: speed ramp. |
| Lab TV with Black Friday slides | `O/Nov 12 Black Friday/Creator Lab B-Roll/IMG_9874.MOV` | 19.8, 21.4, 24.3 | A: CLR user v3. B: SKILL.md "Black Friday" | Screen shots, 0.6-0.8 s each. |
| "Wide shots of the full room" (Immersion Day) | `O/November 18th Immersion Day/IMG_0765.MOV`, `IMG_0791.MOV` | 0765 @0.5; 0791 @1.0 | B: SKILL.md "a room full of people = wide shots of the full room (IMG_0765, 0791, steady), starting on the word 'room'" (named by Babi) | Steady. Notes tag 0765 "wide room shot, audience at table, static"; 0791 "wide shot of cap guys speaking at table, audience from behind". |
| Room reacting to the presenter | `O/November 18th Immersion Day/IMG_0766.MOV` | 0.5 | C: build_story.py SHOTS | Side wide of presenter + audience. |
| Immersion Day: the one approved screen shot (TV iMessage-style assistant demo) | `O/November 18th Immersion Day/IMG_0807.MOV` | 5.0 | C: build_story.py SHOTS ("just by talking to it"). SKILL.md: "ONE screen shot" rule | Do not stack screens; Babi said "screens are seasoning". |
| Lake path (most people in frame) and runners | `/Volumes/Babi's 2TB/...` Fall26 Vlogs (not mounted); clip names IMG_0276 (lake path), IMG_0274 @6.27 and IMG_0277 @5.07 | 0274 @6.27; 0277 @5.07 | B: SKILL.md "Personal storytelling talks" (Golden Run) | Names only: the path is on the 2TB and was not verified. |
| Laurier | no approved footage | | | Logo cards only (see 1.4). Laurier panel B-roll candidates are in section 5. |

### 1.3 Moments (laughing, reactions, presenting, crowds, high-fives)

| What it shows | Full path | In-point(s) s | Source of approval | Notes |
|---|---|---|---|---|
| Team laughing at the TV ("chat absolutely lose it") | `O/Nov 12 Black Friday/Creator Lab B-Roll/IMG_9856.MOV` | 3.9 | A: CLR user v3. B: SKILL.md "IMG_9856 @3.9 s team laughing at TV" | The anchor example of a good B-roll. 0.8 s. |
| Stu high-five / reaction ("a major announcement") | `O/Nov 12 Black Friday/Creator Lab B-Roll/IMG_9855.MOV` | 5.4 | A: CLR user v3. B: SKILL.md "IMG_9855 @5.4 s" | 0.9 s. |
| Used on the "paused" line (content not described) | `O/Nov 12 Black Friday/Creator Lab B-Roll/IMG_9869.MOV` | 3.1 (1.4 s) | A: CLR user v3 | Pool tag (Claude): stu_teach. |
| Presenter/Stu grin or chuckle | `O/November 18th Immersion Day/IMG_0775.MOV` | 5.0 | C: build_story.py SHOTS | See 1.1. |
| Woman covers face laughing + bald man gesturing ("pretty worth it for these reactions") | `O/November 18th Immersion Day/IMG_0742.MOV` | 4.2 | C: build_story.py SHOTS | Reaction; Claude score 4. |
| Stu + Rick laugh together | `O/November 18th Immersion Day/IMG_0757.MOV` | 9.0 | C: build_story.py SHOTS | Score 5. |
| Unsure face ("no idea how they'd react") | `O/November 18th Immersion Day/IMG_0804.MOV` | 1.0 | C: build_story.py SHOTS | Blonde woman sitting, little motion. |
| Pink-jacket woman hands clasped, attentive smile | `O/November 18th Immersion Day/IMG_0788.MOV` | 11.0 | C: build_story.py SHOTS | |
| Team at the monitor | `O/November 18th Immersion Day/IMG_0818.MOV` | 0.3 | C: build_story.py SHOTS | |
| Most-reused Queen's recap clips | see 1.2 (IMG_9399, 9392, 9442, 9426) | | A | Contents not described; look at frames to confirm. |
| High-fives | none cited | | | Only "Stu high-five" (IMG_9855 above). |

### 1.4 Logos and photos (stills)

| What it shows | Full path | In-point(s) s | Source of approval | Notes |
|---|---|---|---|---|
| Laurier logo card (white, centred, with Ding) | `B/Libraries/TME.fcpbundle/Songs/Original Media/laurier-logo-1200x560.jpg` (file name only; also `laurier.png` in the same folder) | stills | A: Stu Queens Recap 1.fcpxmld (lane 2/3 opener). B: SKILL.md "Stacked graphics ... Laurier, Queen's, QSELF" | Lives inside the library. Should be copied out to a loose Logos folder (section 4). |
| Queen's University photo | `B/Libraries/TME.fcpbundle/2026-09-24/Original Media/queens_university.jpg` | still | A: Stu Queens Recap 1.fcpxmld | Same. |
| QSELF logo | `B/Libraries/TME.fcpbundle/2026-09-24/Original Media/qself logo.webp` | still | A: Stu Queens Recap 1.fcpxmld | Same. |
| Opener screenshot stack (Queen's keynote text) | `B/Libraries/TME.fcpbundle/2026-09-24/Original Media/Screenshot 2026-11-10 at 4.37.52 PM.png` (also `... 4.39.00 PM.png`) | stills | A: Stu Queens Recap 1.fcpxmld | Chat / social screenshots. |
| ChatGPT and Claude logos (side by side, lower third, x +-12%, y -27%, ~340 px, Ding each 0.35 s apart) | `O/Nov 12 Black Friday/Logos/ChatGPT logo.png`, `O/Nov 12 Black Friday/Logos/Claude logo.png` | stills | A: CLR user v3 ("where you're already working"). B: SKILL.md line "Logos at a marker" | Held over Stu, not over B-roll (Babi disabled the B-roll under them, IMG_9900). |
| Chat / social screenshots, rapid pop run | `B/Libraries/TME.fcpbundle/Nov 12 Black Friday/Original Media/Screenshot 2026-11-10 at 3.36.33 PM.png`, `3.36.55`, `3.37.34`, `3.39.23`, `3.39.42`, `3.58.13`, `4.03.15`, `4.03.54`, `3.40.35`, `3.37.58`; also copies in `O/Nov 12 Black Friday/` (Screenshot ... 3.36.33 PM.png etc.) | stills | A: CLR user v3 (Babi's slow pop run, pop sound at ~0.12 s, 0.37-1.6 s each) | Pop sound: `B/Sound FX/click and keyboard/Censor sound ... Pop sound...mp3`, 1.00 s in, 0.12 s, -14 dB. |
| Rick photos (pop on every spoken "Rick" with "dick ding") | `/Users/arielbabichev/Downloads/rick-1-slack-portrait.png` (default), `/Users/arielbabichev/Downloads/rick-4-threads-portrait.jpg` | still | B: babi-storytelling SKILL.md, "Whenever Rick is mentioned, pop a Rick photo..." (Babi's standing rule 2026-11-23) | rick-2-headshot.png and rick-3-team-photo.png are named in the skill but DO NOT exist in ~/Downloads (see gaps). No "dick ding" SFX file exists yet. |
| Knowledge-reel internet photos (Black Friday, Hal Elrod, Toni Blog) | `O/Nov 12 Black Friday/Knowledge Photos/01 black friday crowd.jpg` ... `16 playbook.jpg` (16 files) plus `membership.io/m01..m09 *.jpg` and `full_*.png`; sources in `Knowledge Photos/photo_sources.json` | stills | A: `O/Nov 12 Black Friday/XML/Black Friday Reel - Knowledge (Babi edit backup).fcpxmld`; skill babi-knowledge-reels | Licensed web photos, lower-chest pop. The `candidates/` folder inside is the un-picked pool. |
| Laurier / Queen's campus stills (Wikimedia, white rounded cards) | `O/Nov 26 Laurier Panel/Stills/_web/laurier_text.png`, `goldenhawks.png`, `laurier_sign.jpg`, `queens_grant_hall.jpg`; cards `Stills/card_laurier.png`, `card_goldenhawks.png`; photos `Stills/photo_laurier.png`, `photo_queens.png` | stills | NOT Babi-approved: built by Claude for the Nov 26 Laurier reels (field-producer CLAUDE.md rule "named places/orgs pop with a Ding") | Licence in `Stills/_web/photo_sources.json`. List under candidates (section 5). |
| Stu photos | `~/Downloads/Stu McLaren-Jan-06-2024-11-02-41-2100-AM.webp`; keynote deck `~/Downloads/StuMcLaren-Queens_Believe2026.pptx` | stills / slides | none (Nov 2 and Nov 27 files, no skill line) | Keynote slides: no approved slide stills yet; the deck is the source. |
| Charity cards (S2F, GIVE Oakville, Sutton Quantum) and Oakville photos | `/Volumes/Babi's 2TB/Babiontherun/Fall26/XML/Nov 22 Promo/` (not mounted) | | B: SKILL.md "cards in the sky above his head", sizes 440-520 px | Not verified (2TB off). |

---

## 2. Folder map of `O` (Media/OFFICE)

Counts = video files (recursive) / stills. "XML builder?" = a `.py` builder or an FCPXML export lives in the folder. "Transcript?" = a words/transcript json or folder exists.

| Folder | Date / topic | Clips (video / stills) | XML builder? | Transcript? |
|---|---|---|---|---|
| `How long have you been working here?` | Nov 16, AI aged-reveal reel (IMG_0509-0522) | 14 / 25 (AI Frames) | yes (`XML/ai_plan.json`, format-spec) | no |
| `May 11 10 Year Replay` | May 11 2026 alumni-day event replay | 12 / 15 | no | no |
| `Nov 12 Black Friday` | Nov 12 Black Friday and Creator Lab. Holds Creator Lab B-Roll (IMG_9850-9905, ~56 clips), Creator Lab Excitement (4 clips), Logos, Knowledge Photos | 76 / 121 | yes (28 `.fcpxmld`, incl. Babi's `CLR user v*`) | yes (`BF knowledge words.json`) |
| `Nov 13 Day at NR` | Nov 13 office day (IMG_0151-0171) | 14 / 0 | no | no |
| `Nov 18 Asking Stu Hypotheticals` | Nov 18 off-camera hypotheticals with Stu (IMG_0608, 0609) | 3 / 0 | yes (`XML/reels.py`) | no |
| `Nov 18 shake hands with...` | Nov 18 shake-hands sketch (IMG_0507-0533) | 12 / 1 | yes (`build_shake_hands.py`, `plan.py`, `variants.py`) | yes (`cut_words.json`) |
| `Nov 18, testing out Zoom broadcast thing` | Nov 18 Zoom broadcast test (IMG_0534-0542) | 17 / 0 | no | no |
| `Nov 2 Hal Elrod` | Nov 2 Hal Elrod talk clips | 3 / 0 | no | no |
| `Nov 20 Mio Becks Ad` | Nov 20 Becks film shoot (IMG_0917-0954), Plan, Rewind, Music, Sound, XML | 52 / 0 | yes (`Plan/claude-v2-scripts/*.py`, handoff md) | no |
| `Nov 26 Laurier Panel` | Nov 26 Laurier panel (Field Producer first run). Folders: B-Roll (3), Clips, Takes, Panel, Stills, Inbox (4 HEIC), XML (23 fcpxml) | 129 / 12 | yes (fcpxml, `_pipeline`) | yes (`_pipeline/transcripts`) |
| `Nov 3 Dr Selz` | Nov 3 Dr Selz (IMG_9131-9134) | 4 / 0 | no | no |
| `Nov 4 pre QSELF Content` | Nov 4 pre-QSELF (IMG_9198-9205) plus an `untitled folder` | 10 / 0 | no | no |
| `Nov 4 what would you do if you were actually good?` | Nov 4 (IMG_9177-9193) | 17 / 0 | yes (1 script) | no |
| `Nov 6 QSELF` | Nov 6 QSELF at Queen's (A001_11061741-C031-C047, IMG_9xxx, Stew Vids, Stu Keynote Talk.mp4, video-23xx_singular_display) | 165 / 0 | no (XML for it sits in Nov 9) | no |
| `Nov 9 QSELF Stu Recap` | Nov 9 Stu Queens Recap (IMG_9815/9816 A-roll). XML has Babi's `Stu Queens Recap 1.fcpxmld` | 26 (mostly cutouts) / 47 (graphics) | yes (`build_reel_format*.py`, `make_graphics.py`) | yes (`reel_format_words.json`) |
| `November 18th Immersion Day` | Nov 18 Immersion Day (IMG_0687-0850, IMG_0975/0976 retakes), Graphics | 120 / 4 | yes (`build_broll.py`, `Story/`, `Interviews/`, `Versions Nov 23`) | yes (`Interviews/seg_words.json`, `Story/tr`, `broll_transcripts.json`) |
| `Oct 16 First Day in the Office` | Oct 16 first day at office (IMG_6628+) | 110 / 0 | no | no |
| `Oct 16 Stu Tesla Almost Died` | Oct 16 Stu Tesla story (IMG_2992+) | 42 / 0 | no | no |
| `Oct 19 Day at NR` | Oct 19 (IMG_6951+) | 25 / 0 | no | no |
| `Oct 20 Day at NR` | Oct 20; clips live in ` New` (leading space) and `New Folder With Items` | 112 / 0 | no | no |
| `Oct 26 Memberdev teaser` | Oct 26 (IMG_8429-8433) | 5 / 0 | no | no |
| `Oct 27 toni reel` | Oct 27 (IMG_8552) | 1 / 0 | no | no |
| `Oct 28 Day 2 Reel from charleston` | Oct 28 Charleston (A001_10281400_C029.mov, 1.5 GB) | 1 / 0 | no | no |
| `Oct 28 funny interiew reel` (typo) | Oct 28 funny interviews (IMG_8604+) | 42 / 0 | no | no |
| `Oct 29 Laura Philips` | Oct 29 podcast recap (IMG_8687) | 1 / 24 screenshots | no | no |
| `Oct 30 Stu Phone podcast clips` | Oct 30 (IMG_8713+) | 24 / 0 | no | no |
| `Stu podcast recordings RAW` | Podcast recordings (43 - 29 Oct 2026, 44 - 29 Oct 2026, Podcast 02-25-2026 01...) | 48 / 0 | no | no |
| `_Field Producer Test Laura` | Field Producer test, only `_pipeline` | 0 / 0 | pipeline only | n/a |

Other roots (not in OFFICE)
- `B/Photos/`: 7 Sony photos DSC05591, 05597, 05685, 05692-05695 (Oct 22, loose, no notes).
- `B/Exports/PHOTOS/CH Mastermind PHOTO/` (27 DSC) and `B/Exports/PHOTOS/Second half Mastermind/` (114 DSC): exported Mastermind selects.
- `B/Exports/TRAVEL/Nov2026 QSELF/` holds `Stu Queens Recap - Gaps Removed.m4v`, `Stu Queens Recap 2.m4v`, `Trial Reels` (the finished recap exports).
- `B/Libraries/`: Becks Ad, Camera Stuff, Immersion Day FCP12.3, NR Reels, TME FCP12.3, TME (Babi's recap and Creator Lab edits live in TME).
- `B/Songs/` (CINEMATIC, HAPPY EDIT, SOUND FX, STORYTELLING, new, Old), `B/Sound FX/` (POPPING SOUNDS, Risers, Swoosh, SHUTTER, click and keyboard, Fortnite).

---


## Candidates (NOT approved, no Babi sign-off on record)

Use as a search shortlist only; check frames before using.

| What it shows | Path | In-point(s) s | Source of tag | Notes |
|---|---|---|---|---|
| Immersion Day: curly guy laughing while eating, big grin | `O/November 18th Immersion Day/IMG_0754.MOV` | 6.5-8.5 | Claude notes `XML/notes_*.json`, score 5 | Top-scored laugh. |
| Curly guy laughs big hugging purple-jacket woman | `.../IMG_0688.MOV` | 19-22 | notes, score 4 | |
| Curly plaid guy laughs, arms open / green shirt guy big smile | `.../IMG_0690.MOV` | 60-64 / 73-75 | notes, score 4 | |
| Cap guy (Rick) smiles/laughs looking down; cap guy grins at demo | `.../IMG_0792.MOV` @2-6; `.../IMG_0756.MOV` @0-2, 3-9 | | notes, score 4 | Babi said avoid IMG_0792/0797 for Rick. Check before use. |
| Two men look at "future of Membership.io" on monitor | `.../IMG_0756.MOV` | 3-9 | notes, score 4 | |
| Pink woman smiles filming phone, tall guy filming behind | `.../IMG_0798.MOV` | 5-9 | notes, score 4 | |
| Blonde woman in black smiling at presenter | `.../IMG_0780.MOV` | 9-13 | notes, score 4 | |
| Presenter gestures / open-arm shrugs at whiteboard | `.../IMG_0776.MOV` @21-28; `.../IMG_0779.MOV` @10-16; `.../IMG_0814.MOV` @0-5 | | notes, score 4 | |
| Pink-jacket woman talking with gestures | `.../IMG_0747.MOV` | 0-8 | notes, score 4 | |
| Green shirt funny face, curly guy grins | `.../IMG_0753.MOV` | 12.6-13.4 | notes, score 4 | |
| Woman in blue smiling serving food | `.../IMG_0758.MOV` | 3-6 | notes, score 4 | |
| Babi's own desk clips (Babi said do not use) | `.../IMG_0733.MOV`, `IMG_0693`, `IMG_0734`, `IMG_0797` | | | AVOID per Babi 2026-11-21. |
| Creator Lab pool (53 tagged shots, Claude's first pass that Babi deleted and replaced) | `O/Nov 12 Black Friday/Creator Lab B-Roll/IMG_9850-9905` per `~/.claude/babi-skills/babi-storytelling/scripts/broll_pool_example.json` | per file | Claude tags: laugh, reaction, team, stu_teach, chat/screen | Babi deleted Claude's picks, so only use ones that also appear in section 1. Alternates worth a look: IMG_9873 @0.5 and @5.4, IMG_9879 @7.0, IMG_9894 @0.3 and @7.0, IMG_9876 @11.0 (laugh tags). |
| Claude's Nov 6 gap-fillers for the Queen's recap | `O/Nov 6 QSELF/IMG_9447.MOV` @3.8 and @1.2 (panelists seated), `IMG_9450` @19.0 (panel), `IMG_9421` @1.0 (Stu at laptop), `IMG_9394` @2.4 (Stu driving, next morning) and @4.95 (disabled alt in Babi's file), `IMG_9477` @0.5 (room), `IMG_9525` @1.0, `IMG_9517` @4.6, `IMG_9523` @25.0, `A001_11061741_C034.MOV` @1.0 (Stu on keynote stage), `A001_11061741_C031.MOV` @3.5 and @11.5 (keynote slide), `Stew Vids/IMG_7062 2.MOV` @10.0 (night before), `IMG_7065 2` @4.0 (laptop slides), `IMG_7087/7088 2` (not used) | per file | `O/Nov 9 QSELF Stu Recap/XML/build_reel_format.py` comments | Used in Claude's Reel Format V1-V3 on Babi's cut, not in Babi's own `Stu Queens Recap 1`. The Laurier recap builder (field-producer) borrows from this. |
| Laurier panel phone B-roll | `O/Nov 26 Laurier Panel/B-Roll/IMG_1579.MOV` (4.8 s, tagged for "Video 2 Momentum"), `IMG_1624.MOV` (2.7 s, "Video 1 Big mistake"), `IMG_1639.MOV` (0.95 s, "Bookstore") | whole clips | `_pipeline/groups.json` `broll` tags + state.json kind: broll | Babi answered "Build it" on groups but gave no verdict on the B-roll. Check the V2 projects. |
| Laurier panel wide / audience clips | `O/Nov 26 Laurier Panel/Panel/IMG_1644.MOV`, `IMG_1657.MOV`, `IMG_1662.MOV` | whole | folder name | Panel moments; not tagged as B-roll. |
| Laurier / Queen's stills | `O/Nov 26 Laurier Panel/Stills/*` (see 1.4) | | Claude-built | |
| Rick cards (Claude-made) | `O/Nov 9 QSELF Stu Recap/XML/Graphics/rick1_card.png` ... `rick4_card.png` | stills | Claude, Reel Format V3 | Probably built from the Rick photos; Babi has not said these are OK. |
| Mastermind photos (Sony DSC, Oct 22) | `B/Exports/PHOTOS/CH Mastermind PHOTO/` (27 files), `B/Exports/PHOTOS/Second half Mastermind/` (114 files), `B/Photos/DSC05591, 05597, 05685, 05692-05695.JPG` | stills | Folder placement under Exports suggests Babi exported them as selects, but no note says so | HIGH likelihood approved, needs Babi to confirm; no skill refers to them. |
| Hypotheticals footage with Rick/Andrew/Bill answers | `O/Nov 18 Asking Stu Hypotheticals/IMG_0608.MOV`, `IMG_0609.MOV` (Rick at 226-244 s in the 0609 timeline per `XML/reels.py`) | | `XML/reels.py` RICK/KEY/CANDLE blocks | A-roll answers, not B-roll. |
| Summer clip catalog (2,465 clips, laughter timestamps, Vision tags) | `/Volumes/Babi's 2TB/Babiontherun/CLIP CATALOG/CATALOG.md` + `summer_clips_catalog.json` | per clip | memory `summer-camera-roll-reel.md` | 2TB not mounted. Search this first for run/vlog/summer. |

