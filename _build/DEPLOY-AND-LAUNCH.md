# The GEO Agency Index — deploy and launch

**Read this first: the folder you deploy is the folder that contains `index.html`.**
That is the top level of this repo. There is no `site` subfolder any more, and Vercel's
**Root Directory setting must stay empty.** That one setting is what caused the 404 on the
last two builds.

---

## What is in here

| Path | What it is |
|---|---|
| `index.html`, `agency/`, `llms.txt`, `robots.txt`, `sitemap.xml`… | **The website. Deploy this level.** |
| `_build/` | Build tooling. Excluded from the deploy by `.vercelignore`. |
| `_build/data.json` | **The only file with facts in it.** Every agency, check and evidence sentence. |
| `_build/build.py` | Regenerates the whole site from `data.json`. |
| `_build/verify.py` | Loads the built site over real HTTP and runs 360 checks, including a deploy preflight. |
| `_build/set-domain.sh` | Points every URL at a real domain in one command. |
| `README.md` | Short version of this file, so the next person sees it in GitHub. |

---

## Step 1 — Replace what is in the repo

The old layout had the site inside `site/`. That folder is gone. If your local repo still has
it, clear the old files out first or Vercel will keep finding them.

1. Open **Cursor**, `File → Open Folder`, choose your `geo-agency-index` repo.
2. Open the Terminal inside Cursor (`Ctrl` + backtick).
3. Paste this and press Return — it removes every tracked file but keeps the `.git` history:

```
git rm -r --cached . -q
```

4. In Finder, delete everything in the repo folder **except the hidden `.git` folder**.
5. Copy everything from this folder into the repo folder.
6. Back in Cursor's terminal:

```
git add -A
git commit -m "Site at repo root so Vercel needs no Root Directory setting"
git push
```

---

## Step 2 — Check the Vercel setting is empty

This is the whole reason for the restructure. Check it once and it never needs touching again.

1. Go to **vercel.com** → the `aisyndicate-ranking-site` project.
2. **Settings** → **Build and Deployment**.
3. Find **Root Directory**. It must be **empty**. If it says `site` or anything else, clear it
   and click **Save**.
4. Framework Preset: **Other**. Build Command: empty. Output Directory: empty.
5. Go to **Deployments**, open the newest one, click the **…** menu, choose **Redeploy**.

---

## Step 3 — Prove it worked before telling anyone

Open these four URLs. All four must load:

- `https://aisyndicate-ranking-site.vercel.app/` — the ranking table
- `https://aisyndicate-ranking-site.vercel.app/methodology`
- `https://aisyndicate-ranking-site.vercel.app/llms.txt` — must be **plain text**, not a web page
- `https://aisyndicate-ranking-site.vercel.app/sitemap.xml`

If the homepage 404s, the Root Directory is set to something. That is the only cause.

---

## Step 4 — Attach the real domain

1. In Vercel: project → **Settings** → **Domains** → type the domain → **Add**.
2. Vercel gives you an A record (usually `76.76.21.21`) or a CNAME. Add it at the registrar.
3. **Then look at the registrar for a second, conflicting A record on the same name.** On GoDaddy
   an old "WebsiteBuilder Site" A record sat alongside Vercel's and made the domain answer from
   two places. Vercel showed "Invalid Configuration" until it was deleted.
4. **Then point the site's own URLs at the new domain**, or every canonical, the sitemap and
   llms.txt will keep naming the Vercel address:

```
cd _build
bash set-domain.sh https://www.thedomainyoupicked.com
python3 verify.py
```

`verify.py` must print `ALL PASS`. It fails on purpose if any URL still points at the old
address. Then commit and push; Vercel redeploys on its own.

---

## Step 5 — Tell the search engines

1. **Bing Webmaster Tools** — bing.com/webmasters. Sign in with Google **in an Incognito window**
   (Google OAuth fails in a multi-account Chrome profile).
2. Add the site. Verify by **XML file**: Bing gives you `BingSiteAuth.xml`; drop it in at the top
   level, commit, push, then click Verify. Do not wait on "DNS auto verification" — it stalls for
   up to 48 hours.
3. Submit `https://yourdomain.com/sitemap.xml`.
4. **Google Search Console** — search.google.com/search-console. Add the domain, verify by DNS
   TXT record, submit the same sitemap.
5. Optional, reaches Bing/Yandex/DuckDuckGo fast: make an IndexNow key (32 hex characters), save
   it at the top level as `<thatkey>.txt` containing only the key with **no trailing newline**,
   then open:
   `https://api.indexnow.org/indexnow?url=<your-url>&key=<thatkey>`
   A blank page means accepted.

---

## Step 6 — The one thing this site needs that we cannot do for it

**Nothing links to it yet.** A brand new domain with no inbound links gets crawled slowly and
cited by AI almost never. The highest-value action after launch is one real link from a site
that already gets crawled — the obvious one being aisyndicate.com.

---

## Publishing a new edition

1. Re-run the checks against each domain (the method is written out on `/methodology`).
2. Edit `_build/data.json` — flip the `true`/`false` values, update the `evidence` sentences.
3. Change `"measured_on"` in `data.json` and `MEASURED_LONG` in `build.py`.
4. ```
   cd _build
   python3 build.py && python3 mkog.py && python3 verify.py
   ```
5. Commit and push.

Scores, ranks, ties, the rigging table, llms.txt, the sitemap and every headline number are all
computed from `data.json`. Nothing is typed twice, so nothing can disagree with itself.

---

## What `verify.py` will not let you ship

- `index.html` anywhere other than the top level
- a leftover `site/` folder
- any page, sitemap or llms.txt still naming a domain the site is not served from
- a dead internal link, a JSON-LD block that does not parse, a missing canonical
- a score on screen that disagrees with the raw data
- a missing publisher disclosure on any page
- a dofollow link to a competitor, or an untagged link to aisyndicate.com
- any of the 15 defects the fact-check found on the first build

---

## Note added 17 August 2026 — fonts are now part of the deploy

The site no longer loads fonts from Google. Three families are served from **`/fonts`**
(8 woff2 files, 228 KB total). When you copy this folder into the repo, **copy `fonts/` too**
or every page falls back to Times.

The look was rebuilt the same day: paper-and-ink research-report style, no gradients, no pill
buttons, no shared tokens with aisyndicate.com, and the permanent "AI Syndicate" button is gone
from the navigation. The publisher disclosure strip stays on every page — `verify.py` fails the
build without it. Full notes in `README.md` under "House style".
