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

Measured 14 August 2026. Published by AI Syndicate (https://www.aisyndicate.com/), which is ranked in the index.
