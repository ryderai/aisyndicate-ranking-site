# The GEO Agency Index — build, deploy and launch

Built 14 August 2026. Everything here is plain HTML, CSS and text files. No framework, no
build step at deploy time, no database. Vercel just serves the `site/` folder.

---

## What this folder is

| File / folder | What it is |
|---|---|
| `data.json` | **The only file with facts in it.** Every agency, every check, every evidence sentence. |
| `build.py` | Turns `data.json` into the whole website. Re-runnable. |
| `verify.py` | Loads the built site over real HTTP and runs 327 checks on it. |
| `mkog.py` | Makes the social share image (`site/og.png`). |
| `set-domain.sh` | Points the whole site at a real domain in one command. |
| `site/` | **The finished website. This is what gets deployed.** |
| `screenshots/` | Proof shots taken from the real rendered pages. |

---

## Step 1 — Pick the domain

Right now every URL in the site says `https://geo-agency-index.vercel.app`. That is a
placeholder. Andrew has spare domains; whichever one gets used, run this once:

1. Open Terminal.
2. Type `cd` then a space, then drag this folder onto the Terminal window. Press Return.
3. Paste this, replacing the address with the real one, then press Return:

```
bash set-domain.sh https://www.thedomainyoupicked.com
```

4. Paste this and press Return:

```
python3 verify.py
```

It should print `ALL PASS`. If it does not, stop and read what it says — it names the exact
page and the exact problem.

**Do not skip this.** If the domain in the files does not match the domain the site is served
from, canonical tags, the sitemap and every JSON-LD block point at a site that does not exist.
That exact mistake blocked indexing on the Justin Dyar ranking site for a week.

---

## Step 2 — Put it on GitHub

1. Open **Cursor**.
2. `File → Open Folder`, choose this folder.
3. Open the Terminal inside Cursor (`Ctrl` + backtick).
4. Paste these one at a time:

```
git init
git add .
git commit -m "GEO Agency Index 2026 — 29 agencies audited 14 Aug 2026"
```

5. Go to **github.com/new**. Repository name: `geo-agency-index`. Leave it **Private** for now.
   Do **not** tick "Add a README". Click **Create repository**.
6. GitHub shows you two lines starting `git remote add origin`. Paste both into Cursor's
   terminal and press Return.

---

## Step 3 — Deploy on Vercel

1. Go to **vercel.com/new**.
2. Pick the `geo-agency-index` repo, click **Import**.
3. Framework Preset: **Other**.
4. Root Directory: click **Edit**, choose **`site`**. This matters — the deployable website is
   inside `site/`, not at the top of the repo.
5. Leave Build Command and Output Directory empty.
6. Click **Deploy**.

When it finishes, open the URL it gives you and check `/llms.txt` loads as plain text.

---

## Step 4 — Attach the real domain

1. In Vercel, open the project → **Settings** → **Domains**.
2. Type the domain, click **Add**.
3. Vercel shows you an A record (`76.76.21.21` or similar) or a CNAME. Add it at the registrar.
4. **Then check the registrar for a second, conflicting A record on the same name.** On
   GoDaddy an old "WebsiteBuilder Site" A record sat alongside Vercel's and made the domain
   answer from two places. Vercel showed "Invalid Configuration" until it was deleted.

---

## Step 5 — Tell the search engines

1. **Bing Webmaster Tools** — bing.com/webmasters. Sign in with Google **in an Incognito
   window** (Google OAuth fails in a multi-account Chrome profile).
2. Add the site. Verify by **XML file**: Bing gives you a `BingSiteAuth.xml`, drop it into
   `site/`, commit, push, then click Verify. The file method takes seconds. Do not wait on
   "DNS auto verification" — it stalls for up to 48 hours.
3. Submit `https://yourdomain.com/sitemap.xml`.
4. **Google Search Console** — search.google.com/search-console. Add the domain, verify by
   DNS TXT record, submit the same sitemap.
5. Optional, gets it in front of Bing/Yandex/DuckDuckGo fast: make an IndexNow key (32
   hex characters), save it as `site/<thatkey>.txt` containing only the key with **no trailing
   newline**, then paste this into a browser:
   `https://api.indexnow.org/indexnow?url=<your-url>&key=<thatkey>`
   A blank page means accepted.

---

## Step 6 — The one thing this site needs that we cannot do for it

**Nothing links to it yet.** A brand new domain with no inbound links gets crawled slowly and
cited by AI engines almost never. The single highest-value action after launch is one real
link from a site that already gets crawled. The obvious candidates are a link from
aisyndicate.com, and the agencies who come out well in the index, who have a reason to share it.

---

## Re-running the audit later

The whole point of the build is that it is repeatable. To publish a new edition:

1. Re-run the checks against each domain (the method is written out on `/methodology`).
2. Edit `data.json` — flip the `true`/`false` values and update the `evidence` sentences.
3. Change `"measured_on"` and `MEASURED_LONG` in `build.py`.
4. `python3 build.py && python3 mkog.py && python3 verify.py`
5. Commit and push. Vercel redeploys on its own.

The score, the rankings, the ties, the sensitivity table, the llms.txt, the sitemap and every
headline number on the homepage are all computed from `data.json`. Nothing is typed twice, so
nothing can disagree with itself.

---

## What is deliberately in here

- **A disclosure strip on every single page** saying AI Syndicate publishes the index and is
  ranked in it. `verify.py` fails the build if any page is missing it.
- **A "rigging test" section** on `/methodology` that deletes the three checks only AI Syndicate
  passes and republishes the ranking. AI Syndicate falls to rank 17. This is on the site on
  purpose — it is the answer to the first thing a competitor will say.
- **Every outbound link to a competitor is `rel="nofollow noopener"`.** Only the links to
  aisyndicate.com are dofollow, and all of them are UTM-tagged
  (`utm_source=geo-agency-index&utm_medium=referral&utm_campaign=2026-geo-agency-index`).
- **No competitor rating in the structured data.** An earlier draft emitted `schema.org/Review`
  with a numeric rating of each named competitor, authored by AI Syndicate. That was pulled —
  it is a self-serving review under Google's guidelines and the "this does not measure quality"
  caveat does not travel with the JSON-LD. It is now `AnalysisNewsArticle` + `Dataset`.
