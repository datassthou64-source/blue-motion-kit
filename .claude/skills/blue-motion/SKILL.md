---
name: blue-motion
description: Turn creator voiceover audio into researched, visual-first HyperFrames motion graphics. Use when anyone provides one or more audio files for a creator video and asks to transcribe, analyze, research the concepts or products online, build or revise pure motion graphics, preview locally, or render in the established continuous blue-gradient style.
---

# Blue Motion graphics

Build a factual visual explanation around the voiceover. Favor recognizable objects, product UI language, official logos, and transformations over captions or abstract text cards.

> **Load `/motion-visual-sourcing` first.** It owns the two laws this style depends on — *visual
> first, text second* (delete every word; the idea must still land) and *every named entity earns a
> real, sourced asset* (fetch the true logo, real UI or a site capture for any company, product,
> site or repo the VO names — never a generic box or the name as plain type). This skill's blue
> gradient governs how it looks; those laws govern what goes on screen.

## Where everything is

All paths below are relative to **`KIT`**, the root of the `blue-motion-kit` repo.
`bash <this skill folder>/scripts/kit-root.sh` prints it (it resolves symlinks, so it is right
whether this skill was loaded from the repo or through a link).

| Path | What |
|---|---|
| `library/design.md` | The one visual spec — palette, type, objects, motion verbs, honesty rules, and the argument-shape → scene map. **Wins any conflict.** Read it before storyboarding. |
| `library/scenes/` | 13 config-driven templates from the approved Grok Bot build. Copy the `.html` + `.motion.json` into `compositions/` and edit the `CFG` block at the top of its `<script>`; geometry regenerates from it. |
| `library/patterns/` | The earlier static primitives. Still valid. |
| `library/PATTERNS.md` | Index of both. |
| `library/assets/logos/` | Frozen, verified official marks (Grok, Grok Bot, xAI, X, Cursor, Claude, Slack, Instantly, HeyReach, HubSpot, GitHub…). `SOURCES.md` is the provenance table. Check here before fetching. |
| `reference/grok-bot/` | The approved reference build: scene source, contact sheets and two finished renders. Look, don't copy wholesale. |
| `brand/creator.md` | Who watches and how the creator talks. |
| `KIT/editor.local.md` | This machine's editor preferences from the first-run interview (projects folder, NLE, approval gates). Read it if it exists. |
| `references/build-recipe.md` (this skill) | The composition contract and the bugs that pass `check` clean. Read when authoring or debugging. |
| `references/scene-patterns.md` (this skill) | Hand-built devices that are not templates. |
| `scripts/` (this skill) | `bootstrap-project.sh` (new project), `render_passages.py` (export), `hlg_to_sdr.py` (HDR footage fix), `fetch-logo.py` (logo resolver), `kit-root.sh`. |

A template supplies the choreography, easing, palette and seek-safety. It supplies
nothing about whether it is the right idea for this beat. Change the text and the
metaphor to match what is actually said; re-research every newly named product and
use its current official assets. Never ship a template's placeholder mark.

## Workflow

1. Read `brand/creator.md`, and `editor.local.md` if present.
2. Use the mandatory HyperFrames, motion-graphics, media-use, and CLI skills.
3. Inspect only the supplied audio. Ignore earlier work for that audio unless the editor explicitly asks to reuse it.
4. Scaffold the project: `bash SKILL_DIR/scripts/bootstrap-project.sh PROJECTS_DIR/<video-slug> AUDIO...`
   (`PROJECTS_DIR` comes from `editor.local.md`; default `KIT/projects`). It copies the starter,
   gradient, logos and both template generations, and prints each audio file's duration.
5. Transcribe every file with word timings (`npx hyperframes transcribe assets/audio-01.<ext> --dir .`
   or the current media-use path). Sanity-read it and correct obvious proper-name errors
   (Clay, n8n, Instantly, HeyReach, Prospeo, Apify, Grok, Cursor, Claude Code, Codex, MCP).
6. For multiple files, preserve the originals and place them sequentially on one timeline. Use `ffprobe` for exact offsets.
7. Turn the transcript into semantic beats: time range, meaning, visual subject, action, and research need.
8. Research unfamiliar concepts and current product branding before drawing. Prefer official sources, save resolved assets locally, and record sources in `RESEARCH.md`. Logos: `python3 SKILL_DIR/scripts/fetch-logo.py --manifest logos.txt assets/logos`, then open every file it returns.
9. Storyboard the full audio before authoring (`STORYBOARD.md`). Target one complete visual scene per 4–8 seconds. If `editor.local.md` asks for storyboard sign-off, stop here and show it.
10. Put the blue-gradient video in the parent timeline, one unbroken clip per motion-graphics passage, and keep every scene transparent so the background never resets at cuts.
11. Adapt the smallest semantically matching pattern. Do not force a topic into a template merely because it exists.
12. Run `npx hyperframes check`, then snapshot the payoff frame of **every** scene and look at the images. Geometry bugs — an object landing at the wrong coordinates, one element sliding over another — pass `check` silently and only show up in a frame.
13. Open the local preview (`npm run dev`) and give the editor the URL. Do not render until the editor explicitly approves (unless `editor.local.md` says auto-render).
14. After approval, export with the default script. Do not run a full-timeline render.

    ```bash
    python3 SKILL_DIR/scripts/render_passages.py PROJECT_DIR
    ```

    It renders each motion-graphics passage to `renders/MGNN-<label>.mp4`. It converts any HLG footage to SDR first, and it checks every file for 1920×1080, 30 fps, frame count, audio and SDR BT.709. It then writes `premiere-cuts.xml`, which places each file at its real position on the VO timeline (imports into Premiere and DaVinci Resolve). Use `--dry-run` to list passages, `--only 3,8` to re-render some, and `--xml-only` to rebuild the XML. Then look at a frame from each file; the script's checks cannot see a missing layer. Details and why: `references/build-recipe.md` §7.

15. Finish with a short hand-off: project path, the renders, the XML, and any assets you could not verify.

`SKILL_DIR` is this skill's folder: `KIT/.claude/skills/blue-motion`.

## Speed and token discipline

- Reuse the exact gradient, style tokens, and verified scene primitives.
- Research only nouns that affect factual visuals: products, logos, interfaces, workflows, or physical objects.
- Prefer one authoritative source for a simple fact; add more only when ambiguous.
- Keep `BRIEF.md`, `RESEARCH.md`, and `STORYBOARD.md` compact.
- Reuse accurate geometry for laptops, repository windows, app tiles, and routes.
- Show snapshots or the local preview instead of narrating CSS choices.

## Non-negotiables

The look and honesty rules are `library/design.md` §9–10: no face cam, no captions or
sentence cards, 1–3-word labels, real sourced marks on plates, and nothing fabricated. On top of those:

- Laptop screens stay near 16:9 and settled devices never pulse or change dimensions.
- Moving objects travel continuously. Do not pause halfway unless the narration describes a stop. Use smooth ping-pong motion for back-and-forth ideas.
- Make each scene one dominant visual idea with a clear state change, using a tangible verb: split, copy, sync, pull, push, search, assemble, route, unlock, compare, transform.

## Changing the kit itself

A new durable rule (a style call, a default asset, a new trap) goes into its one home —
look in `library/design.md`, trap/procedure in this skill, creator facts in `brand/creator.md` —
never into a project's notes or the agent's memory. Then commit it so every editor gets it
(see `CONTRIBUTING.md` at the kit root).
