# Hand-built scene devices

> The packaged templates and the argument-shape → scene map live in
> `library/design.md` §11. This file holds only the
> devices that are **not** packaged as templates.

These appear in the Grok Bot build and are worth rebuilding by hand when a beat
needs them. Like the templates, use each at most once per piece:

- **Line bends into a ring** — a horizontal track collapses while a circle
  draws in its place. The strongest transformation in the catalogue; use when
  anything turns into a loop, cycle, or system.
- **Orbit with stations** — a ring with 2–3 labelled nodes and a token
  travelling between them. Keep labels clear of the ring.
- **Progress arc** — cyan stroke accumulating around a ring, reaching full on
  the word that says the goal is met. Pair with an orbit that decelerates to a
  dead stop.
- **Card split** — one card becomes two: author both at final positions, start
  them stacked with GSAP `x` offsets, tween the offsets to 0. Exactly right for
  fork, copy, replicate.
- **Tier lift** — start the top tier low so it owns the frame alone, then
  translate it up as the lower object enters. Solves top-heavy-empty-bottom and
  buys a motion beat for free.
- **Machine window** — a glass card with a header strip and three dots holding
  abstract code bars, which can re-length, recolour, or get sliced back. The
  cheapest way to show "make changes" without a fake screenshot.
- **Guardrail lane + hard blocker** — a token races a lane and slams a wall;
  only the human opens it. Used for approvals, spend limits, publish gates.
- **Pipe with a leak** — spend dripping out of an unused seat, then cut out of
  the line, and the pipe seals behind it.
- **Plate swap** — the ordinary thing is fully built, dropped
  (`scale .86 + opacity 0, power2.in`), and a cyan-framed replacement takes its
  exact position. Start the replacement's outline drawing *on the turn word*.
- **Shatter into fleet** — a single window shatters outward and the fleet rises
  out of the debris.
