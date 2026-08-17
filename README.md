# The GEO Agency Index

**This folder is the website. Deploy this folder as-is.**

`index.html` is right here at the top level on purpose, so Vercel's default settings work.

## Deploying

Import the repo on Vercel and change nothing:

- Framework Preset: **Other**
- **Root Directory: leave it EMPTY.** Do not set it to `site` — there is no `site` folder any more.
- Build Command: empty. Output Directory: empty.

If you see `404: NOT_FOUND` after deploying, the Root Directory has been set to something.
Clear it and redeploy.

## Rebuilding

Everything here is generated from `_build/data.json`:

```
cd _build
python3 build.py && python3 mkog.py && python3 verify.py
```

`verify.py` must print `ALL PASS`. It refuses to pass unless `index.html` is at the top level
and every URL in the site matches the domain the site is actually served from.

## Changing the domain

```
cd _build
bash set-domain.sh https://www.yourdomain.com
python3 verify.py
```

Currently pointing at: `https://aisyndicate-ranking-site.vercel.app`

## House style — read this before changing the design

This site has its own look on purpose. It does **not** use aisyndicate.com's colours, fonts,
logo or buttons. A ranking site that looks like the marketing site of the agency ranked first
in it reads as a sales page, and then the numbers stop doing their job.

- **Paper and ink, one accent.** Paper `#faf8f3`, ink `#191814`, one muted green `#1f5c4d`.
  No gradients, no pill buttons, no shadows, no rounded corners.
- **Type:** Source Serif 4 for headlines and figures, IBM Plex Sans for text, IBM Plex Mono for
  labels, dates and stamps. **Self-hosted in `/fonts`** — the site calls no font service.
  Keep the `fonts/` folder when you deploy or every page falls back to Times.
- **The mark** is a 3x3 grid of pass/fail squares, drawn flat in `build.py`.
- It all lives in the `CSS` string and the `head()` / `foot()` helpers in `_build/build.py`.
  One edit there changes all 33 pages. Never hand-edit an HTML file — the next build
  overwrites it. That includes this README, which `build.py` writes too.

**What must never be removed:** the strip at the top of every page naming AI Syndicate as the
publisher. `verify.py` fails the build if a page loses it, and the rigging test on
`/methodology` — the strongest thing on the site — only works because the conflict is stated
up front.

Measured 14 August 2026. Published by AI Syndicate (https://www.aisyndicate.com/), which is ranked in the index.
