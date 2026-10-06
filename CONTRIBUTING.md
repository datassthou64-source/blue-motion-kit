# Changing the kit

`main` is the version every editor pulls. The lead editor owns it.

## Editors

Don't edit tracked files in your copy; local edits stop the automatic update. Instead ask your
agent to **"propose this as a kit change"**. It writes `kit-proposals/<date>-<topic>.md` (never
committed) with:

- what broke, or what you want added, and why
- the exact file and the change (a new trap goes in `build-recipe.md` §3; a new scene goes in
  `library/scenes/` with a `CFG` block, a `.motion.json`, a header comment, and rows in
  `library/PATTERNS.md` and the `design.md` §11 map)
- a snapshot path if it's visual

Send that file to the lead editor. Once it's merged, you get it at your next session start.

## Lead editor

Edit in place (your local template and skill folders are symlinks into this repo), then:

```bash
git add -A && git commit -m "…" && git push
```

Before pushing, remember the repo is **public**: no creator or client names, audio, transcripts
or private footage in tracked files.
