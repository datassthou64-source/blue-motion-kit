# Build recipe — the composition contract and the traps

`library/design.md` is *what it looks like*. This file is
*how to make it render correctly*.

---

## 1. Two project shapes, both valid

### Sub-composition (preferred for 5+ scenes)

`index.html` is a shell holding one clip per scene plus the audio; each scene is
its own file with scene-prefixed CSS. This is what the reference `reference/grok-bot/hyperframe/`
project does and it scales cleanly.

```html
<div id="root" data-composition-id="main" data-start="0" data-duration="31.229"
     data-width="1920" data-height="1080">
  <video id="global-bg" class="clip" src="assets/blue-gradient-loop.mp4"
         data-start="0" data-duration="31.229" data-media-start="0"
         data-track-index="0" muted playsinline></video>
  <div id="el-s1" class="clip" data-composition-id="s1-one-message"
       data-composition-src="compositions/01-one-message.html"
       data-start="0" data-duration="5.25" data-track-index="1"
       data-width="1920" data-height="1080"></div>
  <!-- … one per scene … -->
  <audio id="narration" class="clip" src="assets/vo.mp3"
         data-start="0" data-duration="31.229" data-track-index="20" data-volume="1"></audio>
</div>
<script>
  window.__timelines = window.__timelines || {};
  window.__timelines.main = gsap.timeline({ paused: true });
</script>
```

Each scene file wraps its content in `<template>` and scopes every class with a
scene prefix (`.s6-ring`, `.s6-node`) so nothing collides.

### Single file (fine for ≤ 4 scenes, or one continuous morph)

One `index.html`, one timeline, background videos and scene clips as siblings.
**Choose this when the piece is one object evolving** rather than a series of
distinct scenes — a continuous morph across sub-composition boundaries is far
more trouble than it is worth.

## 2. Framework rules that bite

1. `<video>` and `<audio>` may **never** sit inside a timed wrapper `<div>`. Mount
   one full-duration gradient `<video>` directly under the parent root; scene
   compositions stay transparent.
2. Every media element needs an **`id`** — without one the renderer cannot
   discover it and the video renders **frozen**. `check` catches this as
   `media_missing_id`; do not ship past it.
3. Do not split or restart the gradient at scene boundaries. A single media clock
   prevents visible background changes. The one exception: when the motion-graphics
   passages are separate cut-outs of a longer video, mount one gradient clip per
   passage (`reference/grok-bot/hyperframe/` has eleven). It still never breaks within a passage.
4. `class="clip"` on every timed div; visual clips are direct children of the root.
5. Root `data-duration` is read once at compile time.
6. Only deterministic logic — no `Date.now()`, no `Math.random()`, no fetches.
   That is why the word array is inlined into `tools/words.js` via a `<script
   src>` instead of fetching `transcript.json`.

### The version pin is deliberate

The starter pins `hyperframes@0.7.87` in `package.json`, and every template plus the export
script is verified on it. The `/hyperframes` skill will suggest `upgrade --project`; **do not bump
a Blue Motion project's pin.** A bump happens once, in `library/starter/package.json`, after all 13
scenes pass `check` and snapshot clean on the new version. That is a kit change (`CONTRIBUTING.md`).

## 3. The bugs that pass `hyperframes check` clean

Each shipped a broken frame on a Blue Motion build and none produced a check error.
Snapshots caught every one.

### `svgOrigin` drifts on SVG groups

GSAP's `svgOrigin` leaves a residual translate in this renderer — a ring authored
at (960,540) rendered ~130 px off-centre with no warning.

**Never use `svgOrigin`.** Instead make the animated group's geometry symmetric
about its own pivot, so GSAP's default bbox origin *is* the pivot. For something
that orbits a point it does not sit on, add an invisible counterweight:

```html
<g id="token-orbit">
  <circle class="token-halo" cx="960" cy="250" r="44" />
  <circle class="token-core" cx="960" cy="250" r="21" />
  <!-- pulls the group's bbox centre onto the ring centre (960,540) -->
  <circle cx="960" cy="830" r="44" fill="none" stroke="none" />
</g>
```

`check` will still warn `rotation_pivot_drift` for a true orbit — it measures the
*painted* bbox, which is supposed to move. That warning is correct behaviour;
leave it and say so.

### Round line-caps paint on a fully dashed-off stroke

A checkmark hidden with `strokeDashoffset = length` still drew a dot at its start
point — visible for the entire piece. Anything hidden by dashoffset also needs
`opacity: 0` in CSS, with a `tl.set(el, { opacity: 1 }, at)` when it draws.

### Dash patterns wrap around

A travelling pulse built as `strokeDasharray: "90 L"` animated to `-L - 90` brings
the *next* repeat of the pattern onto the path start. Make the gap `L * 2`:

```js
function flow(tl, sel, at, dur) {
  const el = document.querySelector(sel);
  const L = el.getTotalLength();
  el.style.strokeDasharray = 90 + " " + L * 2;   // gap >> path, so it cannot wrap
  el.style.strokeDashoffset = 0;
  tl.set(el, { opacity: 1 }, at);
  tl.fromTo(el, { strokeDashoffset: 0 },
    { strokeDashoffset: -L - 90, duration: dur, ease: "power1.inOut", immediateRender: false }, at);
  tl.set(el, { opacity: 0 }, at + dur);
}
```

This is the seek-safe way to send a token along a curve — no MotionPathPlugin,
which is not in the GSAP CDN build.

### `immediateRender: false` leaves frame 0 wrong

A `fromTo` with `immediateRender: false` does **not** apply its from-state until
the tween runs, so the element renders at its natural CSS value beforehand. Every
element that should start hidden needs its initial state in **CSS or an SVG
attribute**, not only in the tween:

```css
#node, #plate, #win { opacity: 0; }
```

### A visible from-state renders at frame 0

The inverse of the above: a `fromTo` whose *from* state has `opacity > 0`
renders that state from frame 0 (immediateRender), long before the tween's start
time. Pass `immediateRender: false` whenever the from-state is visible.

### A gradient clip without positioning CSS never shows

The starter styles its one gradient by id (`#global-bg`). When a project splits the
gradient into one clip per passage with new ids, that rule no longer matches. The clips get no
size or position, and Studio shows flat navy. `check` passes. Style the gradients with a class
(`.bg-loop{position:absolute;inset:0;width:1920px;height:1080px;z-index:0;object-fit:cover}`)
and put `class="clip bg-loop"` on every gradient clip, as `reference/grok-bot/hyperframe/` does.

### The vignette paints over scenes unless the scene root is raised

With a parent-level `.shade` (z-index 1), every scene's own root needs `z-index:7`
(`#sN-root{position:absolute;inset:0;z-index:7;…}`). Otherwise white plates render grey
under the vignette.

### Sub-composition scripts share one global scope

Every scene file's `<script>` runs in the same window, so a top-level `const W`
in two scenes throws and kills the second one. Wrap each scene script in an IIFE.

## 4. Percent-translate centring fights GSAP scale

Do not centre absolutely-positioned HTML labels with `transform: translate(-50%,-50%)`
and then tween `scale` on them — GSAP parses the computed matrix and the two
fight. Centre through GSAP's own transform channel instead:

```js
gsap.set(".node-lbl, .chip", { xPercent: -50, yPercent: -50 });
```

Then `left`/`top` are the true centre coordinates, and `scale`, `x`, `y` compose
cleanly on top.

## 5. Anchoring

```js
const W = (i) => WORDS[i].s;
tl.to("#lbl-verify", { opacity: 1, duration: .35, ease: "power1.out" }, W(50));
```

Anchor everything to `WORDS[n].s`. A hand-typed `15.52` is a landmine the next
time the take is re-cut. When a beat needs a lead-in, offset the anchor
(`W(77) - .35`) rather than typing an absolute time.

## 6. Verification loop

```bash
npx hyperframes check .                       # must reach "Check passed"
npx hyperframes snapshot . --at 3,7.8,10.9,13.6,16,19.2,22,24.5,26.3,30.2
# read snapshots/contact-sheet.jpg, then full-res any frame that looks wrong
```

Export is §7, not a full-timeline `render`.

Expected non-blocking warnings: `rotation_pivot_drift` on a real orbit,
`clip_media_fit` when the audio slot is a few frames longer than the file, and
`studio_missing_editable_id` on elements you do not intend to edit in Studio.
Everything else gets fixed.

## 7. Export — per passage, not the full timeline

```bash
python3 KIT/.claude/skills/blue-motion/scripts/render_passages.py PROJECT_DIR
```

This is the default for every Blue Motion build. Approved on a past build (2026-09-26).

- **Why:** a body project is mostly empty timeline between passages. a past build had 148s of
  graphics inside 482s. A full-timeline `render` captures every empty frame and was pacing
  for about an hour. The script exported all eight passages in 2.5 minutes.
- **Passages:** one per blue-gradient clip. With a single full-length gradient (an intro),
  the passages are the runs of back-to-back composition clips instead.
- **Entry files:** each passage gets a temporary `_render-NN.html`. It holds every parent
  clip overlapping the window (gradient, shade, footage, VO slice, scenes), shifted to 0.
  The parent `main` timeline is replayed with `P.tweenFromTo(start, end)` placed at 0.
  Adding the parent timeline as a child at a negative start (`tl.add(P, -start)`) renders
  nothing, and on a past build the road footage silently vanished.
- **HDR guard:** iPhone footage is HLG (BT.2020). One HDR source flips the whole render to
  10-bit BT.2020 HLG, which shifts the gradient toward purple and drops to the slow
  layered-composite path (4 minutes instead of 26s for one scene). The script converts HLG
  clips to SDR BT.709 in place with `hlg_to_sdr.py` and keeps the original in
  `_hdr-originals/`. The conversion keeps HLG's tone curve and only converts the primaries.
  A full reference-white tone map blew out the sky. PQ footage stops the script.
- **Verification:** 1920×1080, `30/1`, the expected frame count (±1), audio present, and
  transfer not HLG/PQ. Still look at one frame per file: a missing layer passes every probe.
- **XML:** `premiere-cuts.xml`, in xmeml v4, 30 fps NDF, the same format as
  the Grok Bot build (`reference/grok-bot/hyperframe/`). Each clip is named `00N MG 0N` and sits at
  `round(start × 30)` on a sequence as long as the VO, so it drops over the A-roll.
