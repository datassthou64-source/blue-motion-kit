# Blue Motion kit

Give it a voiceover. Get back blue-gradient motion graphics as MP4s, plus an XML that
drops each one onto your timeline at the right spot.

Your AI agent (Claude Code or Codex) does the transcription, research, logo sourcing, animation,
checking and rendering. You review a live preview and say "render".

▶ **See the target look first:** `reference/grok-bot/renders/agent-fleet.mp4`

---

## 1. One-time setup (≈10 minutes, macOS)

```bash
git clone https://github.com/datassthou64-source/blue-motion-kit.git
cd blue-motion-kit
bash setup.sh
```

`setup.sh` installs what is missing (Node, FFmpeg, whisper-cpp, the HyperFrames CLI and its
agent skills, a render-only Chrome), then scaffolds a test project to prove it all works. It ends
with **Ready** or a short list of what to fix. Re-run it any time; `bash setup.sh --check`
verifies without installing.

You need [Homebrew](https://brew.sh) and either
[Claude Code](https://claude.com/claude-code) or Codex.

## 2. Every video

1. Open the kit in your agent:
   ```bash
   cd blue-motion-kit
   claude          # or: codex
   ```
   The first time, it asks you four quick questions (where projects go, which editing app,
   when to stop for your OK). That's saved on your machine only.
2. Give it the audio:
   > Here's the VO for the new video: ~/Downloads/vo.wav

   Or drop the file(s) into `inbox/` and say *"make motion graphics for what's in inbox"*.
3. It builds, checks every scene, and gives you a **preview link**. Watch it. Ask for changes
   in plain words: *"scene 4 is too busy"*, *"use the real HubSpot logo"*, *"slow the ending"*.
4. Say **"looks good, render"**. You get:
   - `renders/MG01-….mp4`, `MG02-….mp4`, … — one per motion-graphics passage
   - `premiere-cuts.xml` — **Premiere:** File ▸ Import. **Resolve:** File ▸ Import ▸ Timeline.
     Each clip lands at its real position against the VO.

## 3. Staying up to date

The lead editor updates the style and templates in this repo. Your agent pulls the latest automatically
at the start of each session (or run `git pull`). Your projects and audio are never touched by
an update — they live in `projects/` and `inbox/`, which git ignores.

Found a bug or a better way? Tell your agent *"propose this as a kit change"*, then send the file it
writes to the lead editor. See [`CONTRIBUTING.md`](CONTRIBUTING.md).

No GitHub account needed: the repo is public, so cloning and updating just work.

---

## What's in here

| Path | What |
|---|---|
| `CLAUDE.md` (= `AGENTS.md`) | Instructions your agent reads first |
| `library/design.md` | The style spec: palette, type, objects, motion, honesty rules |
| `library/scenes/`, `library/patterns/` | Ready-made, verified animated scenes the agent adapts |
| `library/assets/` | The blue gradient loop and verified official logos |
| `.claude/skills/` | The step-by-step workflow and export scripts (Codex sees them via `.agents/skills`) |
| `brand/creator.md` | Who watches and how the creator talks |
| `reference/grok-bot/` | The approved reference build |
| `inbox/`, `projects/` | Your audio and builds (not committed) |

## Troubleshooting

| Problem | Fix |
|---|---|
| `setup.sh` says something is missing | Install what it names, re-run `bash setup.sh`. |
| Preview shows flat navy, no gradient | Tell the agent; it's a known trap (`build-recipe.md` §3). |
| A render looks purple/washed out | HDR iPhone footage in the project. The export script converts it; make sure numpy is installed. |
| The agent asks about colours or style | Point it at `library/design.md` — style is not your call to make each time. |
| Transcription misspells a tool name | Normal; the agent fixes names by hand from `brand/creator.md`. |
