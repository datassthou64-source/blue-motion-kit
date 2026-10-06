# Grok Bot — motion graphics design direction

Everything in this folder's HyperFrames projects follows the Blue Motion
system. **The spec is
`library/design.md`.**
This page records only what is specific to *this video*.

This folder is the reference build for the whole system — the thirteen templates
in `library/scenes/` were extracted from these projects.
When adding a scene here, take a template and reconfigure it rather than starting
from an empty file.

---

## Projects in this folder

| Project | Content | Devices used |
|---|---|---|
| `hyperframe/` | the full video — 40 scenes across the whole VO | the complete vocabulary: crack-reveal, tool unlock, fleet lattice, sealed sandboxes, delegate routing, guardrail lanes, inbox stream, leak/pipe, chain of command, triad assembly, lockup outro |
| `agent-fleet-hyperframe/` | one 7.1s beat — "a whole agent fleet for various functions" | the Grok Bot app window standing up, agents stepping out of their sidebar rows into cards, routes converging into one core |
| `agents-version-of-you-hyperframe/` | 14.4s — "an extension of literally you" | twin extension, the real composer panel with a context meter that fills and holds, source fan-out to four agents |

Versioned renders sit at the folder root as `<project>_<date>.mp4`; the highest
timestamp is current.

---

## Resolved assets — use these, do not re-source

`.media/logos/` (mirrored into `hyperframe/.media/logos/`) holds 24 official
marks resolved from first-party sources on 2026-08-17. `.media/index.md` is the
provenance table — read it before adding any logo. Highlights:

`grok.svg` · `xai.png` · `x.svg` · `spacex.svg` · `cursor.svg` / `cursor-mark.svg` ·
`openclaw.svg` · `slack.svg` · `whatsapp.svg` · `stripe.svg` ·
`googlechrome-color.svg` · `github.svg` · `instantly.svg` ·
`heyreach.png` / `heyreach-icon.png` · `hubspot.svg` · `apple.svg`

`agents-version-of-you-hyperframe/assets/logos/grokbot-app-icon.png` is the real
Grok Bot app icon — use it for any Grok Bot object rather than the generic mark.

`agent-fleet-hyperframe/assets/logos/` holds the model marks (Claude, Gemini,
OpenAI, DeepSeek, Grok) with a `marks.json` manifest.

### Two standing caveats

- **Hermes has no cleanly resolvable official mark.** `hermes.png` / `nous.png`
  are the Nous Research mark used as a stand-in, labelled
  `HERMES · NOUS RESEARCH`. Swap in the real mark if the creator supplies one.
- **Not resolved, and not needed:** Prospeo, Ocean, Email Bison, PartnerStack,
  Lead Magic. They only appear in the on-screen CLI list, which is real footage.

### The logo treatment rule

Every mark here follows the plate rule in `library/design.md`
§9. That rule is what contains OpenClaw's red, Slack's four colours, HeyReach's
rainbow and Chrome's RGB.

---

## Real footage inside the graphics

`hyperframe/index.html` mounts two real clips at **parent level, z-index 1**,
underneath the scene that frames them:

- `#demo01` — `assets/grokbot-demo.mp4`, at `615,245 690×384`, framed by the
  aperture in `05-own-computer-tools`
- `#logo01` — `assets/grokbot-logo-anim.mp4`, at `490,120 940×529`, framed by
  the outlined frame in `42-outro-lockup`

That is the pattern for any real footage: **the scene draws the bezel, the
parent plays the video.** The scene stays transparent so the gradient and the
footage both show through.

`agent-fleet-hyperframe/compositions/00-fleet.html` takes the other approach —
it *reproduces* the Grok Bot app window in HTML because the beat needs the
window to come apart. That is only legitimate because the real app was on hand
to copy. **Never reconstruct a UI you have not actually seen.**

---

## The gradient

Note that `hyperframe/index.html` mounts **eleven** gradient clips rather than
one, because the video's motion-graphics passages are non-contiguous — each one
covers a separate cut-out section of the timeline. Within any single passage the
gradient is still one unbroken clip. The single-beat projects
(`agent-fleet`, `agents-version-of-you`) mount exactly one for their full length,
which is the normal case.

---

## When adding a scene here

1. Read `library/design.md`.
2. Pick the template whose *argument* matches the beat — see the map in
   `library/design.md` §11.
3. Copy it into the project's `compositions/`, edit its `CFG` block, point its
   logo paths at `.media/logos/` or `assets/logos/`.
4. Retime `CFG` beats onto the transcript's word boundaries.
5. `npx hyperframes check`, then snapshot the payoff frame and look at it.
6. Preview for the editor. Do not render until they approve.
