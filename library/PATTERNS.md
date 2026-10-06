# Pattern library

Two generations live here. **Read `design.md` first** — it carries the visual
spec and the argument-shape → primitive mapping.

---

## `scenes/` — current generation (from the Grok Bot build)

Thirteen config-driven scene templates extracted from the Grok Bot projects the lead editor
approved. Each is a complete, standalone HyperFrames sub-composition with a
`CFG` block at the top of its `<script>`: labels, counts, timings and asset
paths live there, and the geometry regenerates from them. All thirteen pass
`hyperframes check` clean (0 errors, 0 warnings, WCAG AA).

| Template | The argument it makes |
|---|---|
| `01-crack-reveal` | "Everyone thinks it's X — it's not." The familiar object cracks and the real one lands in the hole |
| `02-tool-unlock-row` | A machine that signs into N tools; each unlocks as a pulse reaches it, then the output lands in one of them |
| `03-fleet-formation` | Scale. N units scatter in, lock into a grid, power on column by column, get wired to one rail |
| `04-source-fanout` | One source applied to N receivers; a token rides each real route and lights its node on arrival |
| `05-chief-fanout-ack` | Delegation. A person asks one hub, it splits N ways, and every branch reports back up |
| `06-peer-mesh` | "They talk to each other." Nodes on a ring, exchanges that accelerate |
| `07-converge-rollup` | Aggregation. N workers each fire one packet up into a single stack, then the cycle marker closes |
| `08-sealed-containers` | Isolation. Walled boxes, a probe that bounces off, outside apps docking without getting in |
| `09-stream-notice` | Monitoring. A continuous stream crosses past a watcher that scans, reacts, and can pull one item out |
| `10-twin-extension` | "An extension of literally you." A figure and its counterpart separate but stay tethered |
| `11-modules-into-core` | The payoff closer. Modules snap into a core, it goes fully cyan, reticle closes, word slams |
| `12-lockup-outro` | The end card. Hero frame, connector rail, two pillars, reticle |
| `13-ui-panel-meter` | A beat that must land on a real product surface — pointer, tooltip, meter that fills and holds |

Each `.html` has a matching `.motion.json` validation manifest, and a header
comment naming its argument, its swappable config, its ID prefix, and its
asset requirements.

How to adapt one (CFG, real logos, retiming, prefix renames) is `design.md` §12.

---

## `patterns/` — earlier generation (Audio 2 + Audio 3 build)

Static scene primitives, no config block. Still correct and still useful when
one matches exactly.

| Pattern | Best use |
|---|---|
| `github-fork` | One repository becoming a connected personal copy |
| `github-sync` | Upstream commits or data moving into a fork |
| `github-clone-local` | Remote source transferring into a local laptop; includes corrected 16:9 screen geometry |
| `local-workshop` | A local object opening into editable parts |
| `build-system` | Parts assembling into a finished system |
| `web-research-three-node` | Exactly three research objects: fetch, central search, search results |
| `product-data-bridge` | Two official product/brand objects connected by direct access |

---

## `starter/`

A minimal project shell — `index.html` with one gradient clip and one scene
slot, plus `hyperframes.json`, `meta.json`, `package.json`. Copy it, drop
scenes into `compositions/`, mount them in `index.html`.

## `assets/`

`blue-gradient-loop.mp4` — the one continuous world. Mount it once in the
parent for the full duration. It never resets at a cut.
