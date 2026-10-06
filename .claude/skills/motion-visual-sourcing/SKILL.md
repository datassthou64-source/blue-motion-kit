---
name: motion-visual-sourcing
description: The two governing laws for every HyperFrames motion graphic — (1) visual first, text second, and (2) every named entity in the narration earns a real, sourced asset on screen. Use when building or revising ANY motion graphic, storyboard, or beat from narration, when the speaker names a company, product, tool, website, or GitHub repo, when deciding what goes on screen for a line, when a beat is drifting toward text cards or bullet lists, or when sourcing logos, product UI or site captures. Applies across every HyperFrames workflow.
---

# Visual first. Text second. Every name earns a real asset.

Two laws. They apply to every beat and every workflow.

---

## Law 1 — Visual first, text second

**People don't read. They scan.** A motion graphic is a picture that moves, not a slide with
animation on it. The mechanism carries the meaning; words only label it.

The test, applied to every beat before you build it:

> **Delete every word from the frame. Does the idea still land?**
> If no, the visual is not doing its job yet — fix the visual, don't add words.

Text is a *supporting element*. It names what the viewer is already looking at. It never carries a
claim the picture doesn't already make.

**Do**
- Show the mechanism moving: route, transform, fill, count, sort, converge, branch.
- Use real logos, real product UI, real screens as the evidence.
- One short label per major object — 1–3 words.
- One hero number, only when the narration speaks it.

**Don't**
- Paste the narration on screen. Captions are two lines maximum, never paragraphs.
- Build a bullet list, an agenda card or a wall of text cards. A list is a constellation or a
  converging hub, not stacked bullets.
- Use a text card because the idea was hard to visualise. That is the moment to work harder on the
  visual, not to give up and type.
- Let a label state something the mechanism doesn't show.

**Ratio of attention:** budget roughly 80% of your build effort on the moving object and 20% on the
type. If you spent it the other way round, the beat is wrong.

---

## Law 2 — Every named entity earns a real, sourced asset

When the narration names **anything that exists online** — a company, a product, a tool, a website,
a GitHub repo, a model, a framework — **go and get the real thing and put it on screen.**

Named entities are *evidence*. A viewer who hears "Clay" and sees the actual Clay mark believes you.
A viewer who hears "Clay" and sees the word "Clay" in Inter does not.

Never draw a generic box, invent a mark, approximate a logo from memory, or leave the name as plain
type when a real asset exists.

### What to source, in order of value

| Entity named | Get this |
|---|---|
| A company or tool | Its real full-colour logo mark |
| A product with a UI | A real screen of that UI, plus the logo |
| A website | A capture of the actual site — `npx hyperframes capture <url>` |
| A GitHub repo | The repo's own avatar/mark, and the README or repo surface |
| A model / framework | The vendor's mark (Anthropic, OpenAI, …) |
| A person | Only with a supplied asset. Do not scrape someone's photo. |

### How to source

**Check the frozen library first.** Verified marks live in `library/assets/logos/` (provenance in its
`SOURCES.md`). Never re-fetch what is already frozen and checked.

**Logos** — use the resolver, don't hand-hunt:

```bash
cat > logos.txt <<'EOF'
clay      clay.com
anthropic wikipedia:Anthropic
linkedin  commons:LinkedIn icon
acme      https://acme.com/press/logo.svg
EOF
python3 KIT/.claude/skills/blue-motion/scripts/fetch-logo.py --manifest logos.txt <project>/assets/logos
```

Ladder: explicit URL → Wikipedia → Wikimedia Commons → the site's own app icon → simple-icons →
favicon. Prefer the first four; simple-icons is monochrome and most house styles want full colour.

**Sites and product surfaces** — capture the real page:

```bash
npx hyperframes capture https://<site> --json --max-screenshots 12
```

Screenshots land locally as layered scenes with assets downloaded. Treat a non-zero exit, `ok:false`
or a `BLOCKED.md` as a hard stop — never infer a brand's design from a partial capture.

### Verify before you build — always

- **Open every asset that comes back.** A wrong logo is worse than no logo.
- The fetcher warns under 6 KB, and a Commons search can return a near-miss (wrong company, old
  mark, fan art). Look at it.
- Prefer the **current** mark. Companies rebrand; Wikipedia lags.
- Record provenance. `fetch-logo.py` appends to `assets/logos/SOURCES.md` automatically — keep it.

### Keep it local and legal

- Copy every asset into the clip's own `assets/`. **No CDN, no network at render time**, ever.
- Third-party marks are used nominatively — to refer to the thing being discussed. Don't restyle a
  logo, imply endorsement, or use a mark as your own branding.
- If no real asset can be found or verified, say so and use the object-class visual instead. Do not
  invent a mark to fill the hole.

---

## Where this bites in the workflow

1. **Source selection** — for every window, record *which entities the line names*. That list is
   the fetch manifest. A window naming an entity with no asset planned is an incomplete selection.
2. **Storyboard** — each frame states its visual thesis and the real assets it needs. If a frame's
   thesis is only expressible as a sentence on screen, re-think the frame.
3. **Build** — assets go in `assets/`, referenced locally, verified by eye.
4. **Review** — squint at the snapshot. If you can only tell what the beat means by reading it,
   Law 1 is broken. If a named brand shows as plain type, Law 2 is broken.

## House style still wins

These laws govern *what* goes on screen. *How* it looks is `library/design.md`: source the real asset,
then stage it in the house style (on a plate, under the deep-pool vignette, inside a glass card).
