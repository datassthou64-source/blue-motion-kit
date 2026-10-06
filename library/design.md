# Blue Motion — design direction

The canonical spec for every Blue Motion piece. Read this before
writing composition HTML; read `scenes/` when you need a scene primitive.

**Reference build:** `reference/grok-bot/` — three HyperFrames projects
(`hyperframe/` 40 scenes, `agent-fleet-hyperframe/`, `agents-version-of-you-hyperframe/`).
The lead editor approved that look. Everything below is sampled from it, not invented.

---

## 0. The one idea

**The blue gradient is one continuous world, and white + cyan vector objects
are the moving logic inside it.** Mount one full-duration background video in
the parent composition so scene cuts never reset or change it (one clip per
passage when the passages are separate cut-outs; see the skill's `build-recipe.md`).

Not slides. Not a dashboard. A machine that is running while you watch.

---

## 1. Frame

- **1920 × 1080, 30 fps.** Author at 1080p even though he uploads 4K.
- Root `data-duration` = the real audio length (whisper over-runs by a few hundred ms).
- **Hard cuts.** No crossfades, no background resets, no fade-to-black.
- Scene length **4–8s** typical. Under 3s flickers; over 10s goes static.
- **A scene may not cut mid-word.** End after the last word's `end` time.

## 2. Palette — these hexes and nothing else

| Token | Value | Use |
|---|---|---|
| Caption white | `#FDFDFD` | labels, structural strokes |
| **Accent cyan** | `#5FE6FD` | the *active* object or current state — one idea at a time |
| Gradient deep | `#004CCF` | darkest area of the loop |
| Gradient mid | `#0083F2` | the loop's dominant blue |
| Gradient bright | `#01B7F9` | brightest area of the loop |
| Card ink | `#0A2F6B` | dark text/marks inside a light card |
| **Deep pool** | `#001642` | the vignette and every glass surface |

Alpha variants are free — glows, trails, glass, depth layers.
**No other hues.** No purple, no rainbow gradients, no full black.

### The cyan rule

Cyan marks *what is active right now* — the travelling token, the state that
just changed, the payoff word. If two things are cyan at once and neither is
the subject, you have diluted the only signal you have.

One exception, proven in `agent-fleet`: a **real product surface** reproduced
faithfully (a dark app window, its own greens and greys) may keep its true
colours. It is a quoted object, not a designed one. Everything around it stays
in palette.

## 3. The deep pool — required, not decorative

White over the loop's bright zone fails WCAG (2.1–2.6:1). Every scene carries
a vignette behind its focal content:

```css
.shade{position:absolute;inset:0;
  background:radial-gradient(ellipse 60% 66% at 50% 48%,
    rgba(0,22,66,.28), rgba(0,22,66,.75));}
```

This is what makes objects read as lit from within rather than pasted on, and
it is what makes `hyperframes check` pass contrast. If a label still fails,
give **that label** a plate — never change the colour.

## 4. Type

**Inter** for display, **JetBrains Mono** for tiny state metadata only.
Declare them directly — the renderer substitutes Inter anyway, and an
undeclared font is a preview/render mismatch.

| Role | Size | Weight | Tracking |
|---|---|---|---|
| Payoff slam | 76–120px | 900 | `.14em`, uppercase |
| Scene tag / hero label | 44–58px | 900 | `.14–.16em`, uppercase |
| System node label | 26–36px | 900 | `.12–.14em`, uppercase |
| Chip / satellite | 24–32px | 600–700 | `.12em`, uppercase |
| Mono metadata | 20–24px | 500 | `.16–.18em`, uppercase |

**Uppercase + wide tracking is the house signature.** Sentence case reads as a
Figma diagram; letterspaced caps read as a machine's own readout.

Glow on type over the gradient:

```css
text-shadow:0 0 26px rgba(0,0,0,.75),0 4px 18px rgba(0,0,0,.6),0 0 44px rgba(255,255,255,.26);
/* cyan type swaps the white bloom for rgba(95,230,253,.45) */
```

**Text budget: 1–3 words per label.** Delete every word in the scene — the idea
must still land. If it doesn't, the visual is wrong, and more text won't fix it.

## 5. Objects — the closed vocabulary

Heavy strokes and real glow. Thin hairlines look like a wireframe, not his edit.

| Object | Spec |
|---|---|
| **System node** | circle or pill, `border:4–5px solid #FDFDFD`, `background:rgba(0,22,66,.84)`, `box-shadow:0 0 36px rgba(95,230,253,.24)` |
| **Agent core** | 248–300px circle, white 5px border, `inset 0 0 84px rgba(1,183,249,.36)` + outer cyan bloom, `4px dashed rgba(95,230,253,.7)` ring inset ~38px |
| **Guide path** | `stroke:rgba(253,253,253,.4)`, `stroke-width:4`, `stroke-dasharray:12 16` — the route, at rest |
| **Flow pulse** | `stroke:#5FE6FD`, `stroke-width:6–8`, `drop-shadow(0 0 15px rgba(95,230,253,.75))` — the route, carrying something |
| **Travelling token** | cyan circle `r≈15` + halo `r≈38` at `.2` alpha + `drop-shadow(0 0 20px)` |
| **Glass card / window** | `rgba(4,26,72,.62–.9)` fill, `rgba(253,253,253,.38–.6)` 3–5px stroke, radius 22–34 |
| **Tool plate** | 156–180px rounded square, white 4px border, glass fill, logo at 56% |
| **White plate** | same, filled `#FDFDFD` — for a logo that needs a light ground |
| **Corner brackets** | white or cyan L's, 34–120px, inset from the subject — reticle framing for a payoff |
| **Registration ticks** | sparse 3×26px edge marks that make a frame feel engineered, not empty |
| **Scene pips** | small dots that fill cyan as each stage lands |

Corner radii live in a **20–68px soft-mechanical range**. Circles and orbits are
intentional, never a fallback.

**Use each feature object once per piece.** Repetition is what makes a build
feel like a template instead of an edit. Paths, nodes and plates are the bed
and may repeat freely.

## 6. Motion verbs

Compose 2–4 per scene. Everything finite and seek-safe — **no `repeat:-1`**.

| Verb | Tween |
|---|---|
| spring-pop entrance | `opacity 0→1, scale .7→1, y 40→0, .45–.55s, back.out(1.4–1.6)` |
| scatter-to-formation | from a per-object offset + rotation, `.72s, power3.out`, stagger `.085` |
| svg-path-draw | `strokeDashoffset L→0, .6–1.5s, power2.inOut` |
| flow pulse | dash `90 L*2`, offset `0 → -L-90`, `.7–.9s, power1.inOut`, then hide |
| token ride | `getPointAtLength` on the real path, `power1.inOut` — arrival is the payoff |
| control-target sync | a token moves; the station it reaches pops on the same beat |
| unlock | `borderColor → #5FE6FD` + `box-shadow` bloom + `scale 1→1.07→1` |
| scale-swap | old object `scale .86 + opacity 0, power2.in`; new one pops on top |
| word slam | `opacity 0→1, scale 1.2–1.25→1, .42s, power4.out` |
| reticle close | four brackets from ±50–60px diagonal offsets, `.5s, power3.out`, stagger `.06` |
| recede | `opacity → .3–.6, .45s` — never delete an object that is still relevant |

Objects **settle** with `power3.out`; they **leave** with `power2.in`. Bouncy
cartoon easing is wrong for him.

**Acceleration carries meaning.** Exchanges that get faster read as compounding
or as tedium, depending on context — it is the cheapest way to say either.

## 7. Layering

Track index is temporal only. Paint order is `z-index`:

```
0  the one parent-level blue gradient loop
1  real product footage framed by a scene above it
7  scene compositions
20 audio (no visual)
```

Inside a scene: shade → svg geometry → objects → labels → payoff → brackets.
Give each concurrent group its own `data-track-index`; two clips on one track
may never overlap in time.

## 8. Layout

- **Two focal points minimum** per scene: a primary object plus an active path,
  orbit, or state change. One static object centred in frame is a dead scene.
- **Fill the frame vertically.** A diagram living in the top third with 600px of
  empty gradient below reads as unfinished. Start content low and **lift it**
  when a second tier arrives — the lift is a free motion beat.
- Something must move in every second. If a stretch has no beat, the fix is
  never a longer hold; it is an ambient bloom, a pulse, or an outline drawing on.

## 9. Honesty rules — these are not style preferences

- **Every named entity earns a real, sourced asset.** If the VO says Slack,
  Clay, Cursor, n8n — fetch the official mark. Never a generic box, never the
  name set as plain type. Load `/motion-visual-sourcing` first.
- **Generic AI gets the Grok Bot mark.** An unnamed AI, LLM, model or "your
  agents" uses `assets/logos/grokbot-app-icon.png` set inside the agent core at
  ~50% of its diameter — never a blank core or three dots. The same file is the
  Grok Bot logo. Products the VO names (Claude, Cursor, Clay…) keep their own marks.
- **Official marks keep their real colours — recolouring one is a fabrication.**
  Every logo sits on a white plate or a glass `rgba(0,22,66,.8)` plate with a 4px
  `#FDFDFD` stroke and a cyan bloom, which quarantines off-palette colour inside
  a shape the system owns. The plate is the object you animate; the mark rides on it.
- **Never fabricate** screenshots, dashboards, tweets, claims or numbers. A
  count-up must be a real figure from the real product.
- Reproduce a product's UI only when you have actually seen it. If you can't
  verify it, use an abstract primitive instead.
- Settled devices never pulse or change dimensions; laptop screens stay ~16:9.

## 10. Never

Face cam · footage windows · picture-in-picture · karaoke captions · sentence
cards · paragraphs · equal card grids · generic dashboards · decorative
background grids or lines · purple · rainbow · full black · cartoon easing ·
infinite loops · a bare text card as a payoff.

---

## 11. How to build a piece

1. Transcribe with word timings. Correct proper nouns by hand.
2. Cut the transcript into semantic beats: time range, meaning, visual subject,
   action, research need. One complete scene per beat, 4–8s (§1).
3. Research every named product; save real assets locally; log sources in
   `RESEARCH.md`.
4. Map each beat's **argument shape** to a scene primitive (table below).
   Adapt the smallest one that matches. Never force a topic into a template
   because it exists.
5. Author `index.html` as a shell of `data-composition-src` clips over one
   full-duration gradient.
6. `npx hyperframes check`, then `snapshot` the payoff frame of every scene and
   actually look at it. Geometry bugs pass `check` silently.
7. Preview locally for the editor. **Do not render until they approve.**

### Argument shape → primitive

| He is saying | Reach for |
|---|---|
| "everyone thinks it's X — it's not" | `01-crack-reveal` |
| "it has its own computer / it signs into your tools" | `02-tool-unlock-row` |
| "a whole fleet of them" / scale | `03-fleet-formation` |
| "you apply this to all of them" | `04-source-fanout` |
| "you ask once and it delegates" | `05-chief-fanout-ack` |
| "they talk to each other" | `06-peer-mesh` |
| "everything reports up into one place" | `07-converge-rollup` |
| "each one is sealed off" / security | `08-sealed-containers` |
| "it watches what comes in and notices" | `09-stream-notice` |
| "it's an extension of you" | `10-twin-extension` |
| "and THAT is when you get leverage" | `11-modules-into-core` |
| the end card | `12-lockup-outro` |
| a beat that must land on the real product | `13-ui-panel-meter` |
| one repo becoming a personal copy | `patterns/github-fork` |
| upstream commits moving into a fork | `patterns/github-sync` |
| remote source landing on a laptop | `patterns/github-clone-local` |
| a local object opening into editable parts | `patterns/local-workshop` |
| parts assembling into a finished system | `patterns/build-system` |
| exactly three research objects | `patterns/web-research-three-node` |
| two products connected by direct access | `patterns/product-data-bridge` |

Unprefixed names are in `scenes/`. Use each feature device at most once per
piece. Hand-built devices proven on screen (line-bends-into-ring, plate swap,
guardrail lane…) are catalogued in the skill's `references/scene-patterns.md`.

---

## 12. Using a template

Copy the `.html` (and its `.motion.json`) into the project's `compositions/`,
then:

1. **Edit the `CFG` block at the top of the `<script>`.** Labels, counts,
   timings and asset paths all live there. Geometry regenerates from them.
2. **Replace every placeholder mark** with a real sourced logo. The inline
   placeholders exist so the file renders standalone — they are never shippable
   for a product the VO names.
3. **Retime to the words.** Move `CFG` beat times onto the transcript's word
   boundaries; adjust the root `data-duration`.
4. **Change the metaphor when the concept differs.** A template is direction,
   not content. If the VO isn't about the thing the template argues, pick a
   different one or build a new scene from §5 and §6.
5. Using one template twice in a project? Rename its prefix:
   `sed -i '' 's/cf-/s14-/g' compositions/05-chief-fanout-ack.html`
   (also rename the `data-composition-id` and the `window.__timelines[...]` key).

A template is a **verified motion skeleton**. It guarantees the choreography,
the easing, the palette and the seek-safety. It guarantees nothing about
whether it's the right idea for this beat — that is still your call.
