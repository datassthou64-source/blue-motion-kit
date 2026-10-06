# Blue Motion kit — agent instructions

> `AGENTS.md` is a symlink to this file (Codex reads that name). Edit either; never replace the
> symlink with a copy.

This repo turns a **creator voiceover** into **blue-gradient HyperFrames motion
graphics**, rendered per passage with a Premiere/Resolve XML that drops them onto the edit.
The person talking to you is a video editor. They may have no context on the creator, the style, or
HyperFrames. Do the work; don't make them learn the system.

## Who's who

- **The creator** — the person whose voiceover this is. Context: `brand/creator.md`.
- **The lead editor** — owner of this kit. They approved the look and maintain `main`.
- **The editor** — whoever is running this session. They approve previews before renders.

## This repo is public

Anyone can read it. Never write the creator's name, a client's name, a channel or company name,
transcripts, audio, or anything from `editor.local.md` into a tracked file. Refer to "the creator".
Product names and their official logos (Clay, Cursor, Grok…) are fine.

## Start of every session

1. **Update the kit.** Run `git pull --ff-only --quiet` in this repo (a SessionStart hook does it in
   Claude Code; in Codex, run it yourself). If it fails because of local edits, tell the editor in
   one line and carry on with what is on disk.
2. **First run on this machine?** If `editor.local.md` does not exist, do the onboarding below
   before anything else.
3. **Tools present?** If `npx hyperframes` or `ffmpeg` is missing, run `bash setup.sh` and report
   only what it could not fix.

## Onboarding (once per machine)

Run `bash setup.sh` first. Then ask the editor these four questions in **one** round (use
AskUserQuestion in Claude Code), with the recommended option first:

1. **Projects folder** — where should builds go? Recommended: `projects/` inside this repo
   (git-ignored). Alternative: a folder next to their Premiere projects.
2. **Editing app** — Premiere Pro (recommended, the XML is built for it), DaVinci Resolve (imports
   the same XML), Final Cut Pro (no XML; they place the MP4s by the timecodes you print), or
   After Effects (place MP4s by timecode).
3. **Storyboard check** — stop after the storyboard for their OK, or go straight to building?
   Recommended: go straight to building; they review the live preview.
4. **Rendering** — render only after they approve the preview (recommended), or render
   automatically once checks pass?

Write the answers to `editor.local.md` (git-ignored) in this shape, then continue with whatever
they asked for:

```markdown
# Editor preferences (this machine)
- Name: <their name if they gave it>
- Projects folder: <absolute path>
- Editing app: <app>
- Storyboard sign-off: yes | no
- Render: after approval | automatic
```

## The one job: audio in → motion graphics out

When the editor gives you audio (a path, a drag-drop, or a file in `inbox/`), with or without
instructions, that is a request for motion graphics. **Use the `blue-motion` skill**
and follow it end to end. It loads `motion-visual-sourcing` and the HyperFrames skills.

- Project name: derive a short slug from the audio filename or topic; don't ask.
- Several audio files are one timeline, in the order given (or filename order).
- Ask a question only when the transcript is genuinely ambiguous about something on screen
  (e.g. which product they mean). Never ask about style — `library/design.md` decides.
- At the end, give the editor: the preview URL first; after approval, the `renders/` folder, the
  `premiere-cuts.xml` path, and how to import it (Premiere: File ▸ Import the XML; Resolve:
  File ▸ Import ▸ Timeline). List any logo or fact you could not verify.

Other requests the editor may make, all inside an existing project:
"change scene 4", "make this slower", "swap the logo", "re-render 3 and 8"
(`render_passages.py PROJECT --only 3,8`), "give me the XML again" (`--xml-only`).

## What lives where (one home per kind of rule)

| Kind | Home |
|---|---|
| Look, palette, objects, motion, honesty | `library/design.md` — wins any conflict |
| Procedure, render traps, export | `.claude/skills/blue-motion/` |
| Visual-first + real-logo laws | `.claude/skills/motion-visual-sourcing/` |
| Creator audience and voice | `brand/creator.md` |
| This machine's preferences | `editor.local.md` (never committed) |
| One video's notes | that project's `BRIEF.md` / `RESEARCH.md` / `STORYBOARD.md` |

Don't put durable rules in agent memory; they belong in the files above so every editor gets them.

## Improving the kit

Editors don't change tracked kit files — local edits would block the automatic `git pull`.
If the editor finds a new trap, or wants a scene added, write a proposal to
`kit-proposals/<YYYY-MM-DD>-<topic>.md` (git-ignored): what broke or what's wanted, the exact
file and change, and a snapshot path if it's visual. Tell the editor to send that file to the lead
editor. Details: `CONTRIBUTING.md`.
