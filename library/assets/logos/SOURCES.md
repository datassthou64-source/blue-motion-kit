# .media/logos — resolved official marks

All files downloaded from official first-party sources on 2026-08-17. No redrawn, recolored, or invented marks.

| File | Brand | Source | Notes |
|---|---|---|---|
| `grok.svg` | Grok (xAI) | reused from `library/.media` | 1024px vector, official mark |
| `xai.png` | xAI | `https://x.ai/apple-icon.png` | 180px, monochrome glyph |
| `x.svg` | X | reused from template `.media` | official monochrome glyph |
| `spacex.svg` | SpaceX | simpleicons CDN (`spacex`) | official wordmark path |
| `cursor.svg` | Cursor | simpleicons CDN (`cursor`) | official cube mark, monochrome |
| `cursor-mark.svg` | Cursor | `https://cursor.com/marketing-static/favicon.svg` | full-color official favicon |
| `openclaw.svg` | OpenClaw | `https://openclaw.ai/favicon.svg` | official lobster mascot, red gradient `#ff4d4d → #9…` |
| `openclaw-mark.png` | OpenClaw | `https://openclaw.ai/apple-touch-icon.png` | 180px raster fallback, verified visually |
| `nous.png` | Nous Research | `https://avatars.githubusercontent.com/NousResearch` | 400px — **stand-in for Hermes**, see caveat below |
| `slack.svg` | Slack | Wikimedia Commons `Slack_icon_2019.svg` | official 4-color hash mark |
| `whatsapp.svg` | WhatsApp | simpleicons CDN | official glyph |
| `stripe.svg` | Stripe | simpleicons CDN | official wordmark |
| `googlechrome.svg` | Google Chrome | simpleicons CDN | official mark |
| `github.svg` | GitHub | simpleicons CDN | official Octocat mark |
| `apple.svg` | Apple | simpleicons CDN | for the iOS/iPhone beat |
| `instantly.svg` | Instantly.ai | `cdn.prod.website-files.com/…_instantly-logo.svg` (instantly.ai) | official vector wordmark |
| `heyreach.png` | HeyReach | `…_HeyReach_Logo-Primary-Light.png` (heyreach.io) | 1626×310, **light version — white wordmark, use on blue only** |
| `heyreach-icon.png` | HeyReach | `…_HeyReach_Icon-Primary-Dark.png` (heyreach.io) | 1559×1133 icon-only |
| `hubspot.svg` | HubSpot | simpleicons CDN | official sprocket |
| `claude.svg` / `anthropic.svg` | Claude / Anthropic | simpleicons CDN | held in reserve |
| `githubcopilot.svg` | GitHub Copilot | simpleicons CDN | held in reserve |

## Caveats

- **Hermes has no cleanly resolvable official mark.** Hermes Agent is a Nous Research product; the top-ranking `hermesagent.agency` / `hermes-agent.org` / `hermes-ai.net` domains are SEO clones I would not trust as a brand source. I resolved the **Nous Research** official mark instead and label the object `HERMES · NOUS RESEARCH`. If the creator has the real Hermes mark, swap it in.
- **Not resolved (no first-party vector found):** Prospeo, Ocean, Email Bison, PartnerStack, Lead Magic. These only appear in the CLI-list section he shows on screen, so no graphic needs them.

## Treatment rule for logos in the blue world

The palette is closed for *our* objects, but official marks keep their real colors — recoloring a brand mark is a fabrication. So every logo sits on a **white or glass `rgba(0,22,66,.8)` plate** with a 4px `#FDFDFD` stroke and a cyan bloom, which quarantines off-palette color (OpenClaw's red, Slack's four colors, HeyReach's rainbow, Chrome's RGB) inside a shape that belongs to the system. The plate is the object we animate; the mark rides on it.
