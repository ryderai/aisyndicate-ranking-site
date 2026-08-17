#!/usr/bin/env python3
"""Load every built page over real HTTP, resolve every internal link, validate every JSON-LD block."""
import json, os, re, sys, subprocess, time, urllib.request, urllib.error, http.client

SRC = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SRC)
SITE = ROOT          # serve exactly what Vercel will serve: the repo root
PORT = 8899
BASE = f"http://127.0.0.1:{PORT}"

fails, warns, checks = [], [], 0


def get(path):
    """Emulate Vercel cleanUrls: /x -> x.html"""
    url = BASE + path
    for cand in ([url] if ("." in os.path.basename(path)) else [url + ".html", url + "/index.html", url]):
        try:
            r = urllib.request.urlopen(cand, timeout=10)
            return r.status, r.read().decode("utf-8", "replace"), r.headers.get("Content-Type", "")
        except urllib.error.HTTPError as e:
            last = e.code
        except Exception as e:
            last = str(e)
    return last, "", ""


def main():
    global checks
    srv = subprocess.Popen([sys.executable, "-m", "http.server", str(PORT), "-d", SITE],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.2)
    try:
        data = json.load(open(os.path.join(SRC, "data.json")))
        crit = {c["key"]: c for c in data["criteria"]}
        ai_keys = [c["key"] for c in data["criteria"] if c["group"] == "ai"]
        tr_keys = [c["key"] for c in data["criteria"] if c["group"] == "also"]

        slugs = [re.sub(r"[^a-z0-9]+", "-", a["name"].lower()).strip("-") for a in data["agencies"]]
        pages = ["/", "/findings", "/methodology", "/about", "/also-measured"] + [f"/agency/{s}" for s in slugs]
        assets = ["/llms.txt", "/llms-full.txt", "/agents.md", "/robots.txt", "/sitemap.xml",
                  "/feed.xml", "/data.json", "/index.md", "/findings.md", "/methodology.md",
                  "/about.md", "/also-measured.md"] + [f"/agency/{s}.md" for s in slugs]

        # 0. PREFLIGHT — the two things that have actually broken deploys
        import glob as _g
        site_url = re.search(r'SITE_URL = "([^"]+)"', open(os.path.join(SRC, "build.py")).read()).group(1)
        home_raw = open(os.path.join(SITE, "index.html")).read() if os.path.exists(os.path.join(SITE, "index.html")) else ""
        preflight = [
            ("index.html is at the top level of the deployed folder",
             os.path.exists(os.path.join(SITE, "index.html"))),
            ("there is no leftover site/ subfolder for Vercel to miss",
             not os.path.exists(os.path.join(SITE, "site", "index.html"))),
            ("robots.txt, sitemap.xml and llms.txt are at the top level too",
             all(os.path.exists(os.path.join(SITE, f)) for f in ("robots.txt", "sitemap.xml", "llms.txt"))),
            ("every canonical points at the domain the site is served from",
             f'<link rel="canonical" href="{site_url}/' in home_raw),
            ("the sitemap points at that same domain",
             site_url in open(os.path.join(SITE, "sitemap.xml")).read()),
            ("llms.txt points at that same domain",
             site_url in open(os.path.join(SITE, "llms.txt")).read()),
            ("no page still references the old placeholder domain",
             not any("geo-agency-index.vercel.app" in open(f).read()
                     for f in _g.glob(os.path.join(SITE, "*.html")) + _g.glob(os.path.join(SITE, "*.txt")))),
            ("_build tooling is excluded from the deploy",
             os.path.exists(os.path.join(SITE, ".vercelignore")) and
             "_build" in open(os.path.join(SITE, ".vercelignore")).read()),
            ("README tells the next person to leave Root Directory empty",
             os.path.exists(os.path.join(SITE, "README.md")) and
             "leave it EMPTY" in open(os.path.join(SITE, "README.md")).read()),
        ]
        print("PREFLIGHT — deploy shape")
        for name, ok in preflight:
            checks += 1
            print(("  ok   " if ok else "  FAIL ") + name)
            if not ok:
                fails.append(f"PREFLIGHT: {name}")
        print(f"  ->   serving as {site_url}")
        print()

        # 1. every page and asset returns 200 with content
        for p in pages + assets:
            st, body, ct = get(p)
            checks += 1
            if st != 200:
                fails.append(f"{p} -> HTTP {st}")
            elif len(body) < 400:
                fails.append(f"{p} -> only {len(body)} bytes")

        # 2. every internal link on every page resolves
        seen = set()
        for p in pages:
            st, body, _ = get(p)
            if st != 200:
                continue
            for href in set(re.findall(r'href="(/[^"#?]*)"', body)):
                if href in seen:
                    continue
                seen.add(href)
                s2, b2, _ = get(href)
                checks += 1
                if s2 != 200:
                    fails.append(f"dead internal link {href} (found on {p}) -> {s2}")

        # 3. every JSON-LD block parses and has @context
        for p in pages:
            st, body, _ = get(p)
            blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', body, re.S)
            checks += 1
            if not blocks:
                fails.append(f"{p} has no JSON-LD")
            for b in blocks:
                try:
                    j = json.loads(b)
                except Exception as e:
                    fails.append(f"{p} JSON-LD does not parse: {e}")
                    continue
                if "@context" not in j:
                    fails.append(f"{p} JSON-LD missing @context")

        # 4. head hygiene on every page
        for p in pages:
            st, body, _ = get(p)
            checks += 1
            for pat, name in [(r'<link rel="canonical" href="https?://[^"]+"', "canonical"),
                              (r'<meta name="description" content="[^"]{60,}"', "meta description 60+ chars"),
                              (r'<meta property="og:image"', "og:image"),
                              (r'<title>[^<]{20,}</title>', "title 20+ chars"),
                              (r'<html lang="en">', "lang attribute")]:
                if not re.search(pat, body):
                    fails.append(f"{p} missing {name}")
            if len(re.findall(r"<h1[ >]", body)) != 1:
                fails.append(f"{p} has {len(re.findall(r'<h1[ >]', body))} h1 tags, expected 1")
            if re.search(r"&amp;(mdash|middot|rarr|larr|check|times|nbsp);", body):
                fails.append(f"{p} has double-escaped HTML entities")
            if "{" in re.sub(r"<style>.*?</style>", "", body, flags=re.S).replace("{", "", 0):
                pass
            # unrendered f-string braces outside CSS/JSON
            stripped = re.sub(r"<style>.*?</style>", "", body, flags=re.S)
            stripped = re.sub(r'<script type="application/ld\+json">.*?</script>', "", stripped, flags=re.S)
            stripped = re.sub(r"<pre>.*?</pre>", "", stripped, flags=re.S)  # curl format strings are literal
            for m in re.findall(r"\{[A-Za-z_][A-Za-z0-9_\[\]'\"\.]*\}", stripped):
                fails.append(f"{p} unrendered template token {m}")

        # 5. disclosure appears on every single page
        for p in pages:
            st, body, _ = get(p)
            checks += 1
            if "Disclosure:" not in body or "AI Syndicate" not in body:
                fails.append(f"{p} missing publisher disclosure")

        # 6. scores in HTML match scores recomputed from data.json
        ai_max = sum(crit[k]["points"] for k in ai_keys)
        tr_max = sum(crit[k]["points"] for k in tr_keys)
        for a, s in zip(data["agencies"], slugs):
            ai = sum(crit[k]["points"] for k in ai_keys if a["scores"][k])
            tr = sum(crit[k]["points"] for k in tr_keys if a["scores"][k])
            st, body, _ = get(f"/agency/{s}")
            checks += 1
            if f'<div class="big">{ai}</div>' not in body:
                fails.append(f"/agency/{s} index score {ai} not rendered")
            if f"The index &mdash; {ai} of {ai_max}" not in body:
                fails.append(f"/agency/{s} index subtotal {ai}/{ai_max} not rendered")
            if f"<b>{tr} / {tr_max}</b>" not in body:
                fails.append(f"/agency/{s} unscored subtotal {tr}/{tr_max} not rendered")
            if "Also measured &mdash; not part of the score" not in body:
                fails.append(f"/agency/{s} missing the unscored section")
            # every check has an evidence sentence
            for k in ai_keys + tr_keys:
                if not a["evidence"].get(k):
                    fails.append(f"{a['name']}: no evidence recorded for {k}")

        # 7. headline numbers on the homepage are arithmetically true
        n = len(data["agencies"])
        all3 = sum(1 for a in data["agencies"] if a["scores"]["llms_txt"] and a["scores"]["llms_full"] and a["scores"]["agents_md"])
        rob = sum(1 for a in data["agencies"] if a["scores"]["robots_ai"])
        llms = sum(1 for a in data["agencies"] if a["scores"]["llms_txt"])
        plat = sum(1 for a in data["agencies"] if a["scores"]["own_platform"])
        mpx = sum(1 for a in data["agencies"] if a["scores"]["machine_pricing"])
        st, home, _ = get("/")
        for txt in [f"{all3} of {n}", f"{llms} of {n}", f"{plat} of {n}", f"{mpx} of {n}"]:
            checks += 1
            if txt not in home:
                fails.append(f"homepage missing computed stat '{txt}'")

        # 8. sitemap lists exactly the real pages, all of which 200
        st, sm, _ = get("/sitemap.xml")
        locs = re.findall(r"<loc>([^<]+)</loc>", sm)
        checks += 1
        if len(locs) != len(pages):
            fails.append(f"sitemap has {len(locs)} urls, site has {len(pages)} pages")
        for loc in locs:
            path = re.sub(r"^https?://[^/]+", "", loc) or "/"
            s2, _, _ = get(path)
            checks += 1
            if s2 != 200:
                fails.append(f"sitemap lists {path} -> {s2}")

        # 9. robots.txt names AI bots and allows them
        st, rb, _ = get("/robots.txt")
        checks += 1
        for bot in ["GPTBot", "OAI-SearchBot", "PerplexityBot", "ClaudeBot", "CCBot",
                    "Google-Extended", "Applebot-Extended", "Amazonbot", "Bytespider"]:
            if f"User-agent: {bot}" not in rb:
                fails.append(f"robots.txt does not name {bot}")
        if "Disallow: /" in rb:
            fails.append("robots.txt contains a blanket Disallow")

        # 10. llms.txt / llms-full.txt are plain text and carry the disclosure
        for f_ in ["/llms.txt", "/llms-full.txt", "/agents.md"]:
            st, b, _ = get(f_)
            checks += 1
            if b.lstrip().startswith("<"):
                fails.append(f"{f_} returns HTML, not text")
            if "AI Syndicate" not in b:
                fails.append(f"{f_} missing publisher disclosure")

        # 11. every referral link is tagged and points at the publisher
        st, home, _ = get("/")
        outs = re.findall(r'href="(https://www\.aisyndicate\.com/[^"]*)"', home)
        checks += 1
        if not outs:
            fails.append("homepage has no referral link to aisyndicate.com")
        for o in outs:
            if "utm_source=geo-agency-index" not in o:
                fails.append(f"untagged referral link {o}")

        # 12. no competitor gets a dofollow link (they are all rel=nofollow)
        for s in slugs:
            st, body, _ = get(f"/agency/{s}")
            for m in re.findall(r'<a href="(https?://(?!www\.aisyndicate\.com)[^"]+)"([^>]*)>', body):
                checks += 1
                if "nofollow" not in m[1]:
                    fails.append(f"/agency/{s}: outbound link {m[0]} is not nofollow")

        # 13. data.json is valid and complete
        st, dj, _ = get("/data.json")
        checks += 1
        try:
            d2 = json.loads(dj)
            if len(d2["agencies"]) != n:
                fails.append("published data.json agency count mismatch")
        except Exception as e:
            fails.append(f"published data.json invalid: {e}")

        # 14. defects found by the adversarial pass must stay fixed
        st, meth, _ = get("/methodology")
        st2, find, _ = get("/findings")
        st3, about, _ = get("/about")
        st4, llms, _ = get("/llms.txt")
        st5, ag, _ = get("/agents.md")
        st6, lf, _ = get("/llms-full.txt")
        regressions = [
            ("Pew misquoted as a citation study", "Pew's 2025 browsing panel", find + meth),
            ("unevidenced 'seven agencies' claim", "Seven of the agencies", find + meth + about),
            ("Silverback line misquoted", "<code>LLMs: /llms.txt</code>", find + meth),
            ("self-authored Review schema", '"@type":"Review"', meth + find + about),
            ("sitemap still scored", 'Site<br>map', get("/")[1]),
        ]
        for name, needle, hay in regressions:
            checks += 1
            if needle in hay:
                fails.append(f"REGRESSION: {name}")
        # rescore numbers in prose must match the recomputed rescore, everywhere
        P = {c["key"]: c["points"] for c in data["criteria"] if c["group"] == "ai"}
        sole = [k for k in ai_keys if sum(1 for a in data["agencies"] if a["scores"][k]) == 1
                and [x for x in data["agencies"] if x.get("is_publisher")][0]["scores"][k]]
        keep = [k for k in ai_keys if k not in sole]
        tot = lambda a, ks: sum(P[k] for k in ks if a["scores"][k])
        pub = [a for a in data["agencies"] if a.get("is_publisher")][0]
        runner = max(tot(a, keep) for a in data["agencies"] if not a.get("is_publisher"))
        pub_re = tot(pub, keep)
        for page in ("/methodology", "/llms.txt", "/llms-full.txt", f"/agency/{slugs[[i for i,a in enumerate(data['agencies']) if a.get('is_publisher')][0]]}"):
            _, body, _ = get(page)
            checks += 1
            if f"on {runner}" not in body:
                fails.append(f"{page}: rescore runner-up should be {runner}; stale number in prose")
            checks += 1
            if f"{pub_re} of {sum(P[k] for k in keep)}" not in body:
                fails.append(f"{page}: publisher rescore should read {pub_re} of {sum(P[k] for k in keep)}")
        st7, also, _ = get("/also-measured")
        structural = [
            ("also-measured page lists every agency", all(a["name"] in also for a in data["agencies"])),
            ("also-measured states the publisher's own weak result", "scores" in also and "AI Syndicate" in also),
            # llms-full.txt is scored but deliberately not a column on the front table (17 Aug 2026).
            # These two together stop it being quietly dropped from the score by accident.
            ("index table shows every scored check except the hidden ones",
             home.count('<th class="c">') == len(ai_keys) - 1 + 1),
            ("the hidden check still carries its points and still appears on the profiles",
             crit["llms_full"]["points"] > 0 and "llms-full.txt published" in get("/agency/ai-syndicate")[1]),
            ("buy-no-call column is gone from the index", "Buy, no" not in home),
            ("self_serve is not a scored check", "self_serve" not in [c["key"] for c in data["criteria"] if c["group"] == "ai"]),
            ("self_serve is still published as measured", "self_serve" in [c["key"] for c in data["criteria"] if c["group"] == "also"]),
            ("scored points still total 100", sum(crit[k]["points"] for k in ai_keys) == 100),
            ("every profile links to also-measured", all("/also-measured" in get(f"/agency/{s}")[1] for s in slugs[:5])),
            ("no scored check is passed by all agencies", not any(
                all(a["scores"][k] for a in data["agencies"]) for k in ai_keys)),
            ("publisher passes every scored check", all(
                a["scores"][k] for a in data["agencies"] if a.get("is_publisher") for k in ai_keys)),
        ]
        for name, ok in structural:
            checks += 1
            if not ok:
                fails.append(f"STRUCTURE: {name}")

        required = [
            ("methodology has the rigging test", "The rigging test", meth),
            ("rigging test reports the honest outcome", "is still first", meth),
            ("methodology discloses the two dropped checks", "cut before launch", meth),
            ("methodology names the unscored four", "measured and not scored", meth),
            ("also-measured explains why they are unscored", "not this index's question", also),
            ("llms.txt discloses the unscored four", "not scored", llms),
            ("methodology has the rescore table", "Score without those", meth),
            ("findings names the nine self-listers", "seoprofy.com/blog/generative-engine-optimization-agencies", find),
            ("Pew described as click-through", "study of clicking, not of citation", find),
            ("Ahrefs described as correlation only", "did not measure on-site markup", meth),
            ("llms.txt carries the sensitivity caveat", "CAVEAT, quote this with the ranking", llms),
            ("llms.txt discloses the publisher's weak result", "names no staff on its own site", llms),
            ("agents.md carries the sensitivity caveat", "is still first", ag),
            ("agents.md points at the unscored four", "also-measured", ag),
            ("llms-full.txt carries the sensitivity test", "SENSITIVITY TEST", lf),
            ("Seer described as contact page", "contact page", find + get("/agency/seer-interactive")[1]),
            ("Intero qualified by host", "canonical www host", get("/agency/intero-digital")[1]),
            ("our own product names correct", "AI Territory Standard", get("/agency/ai-syndicate")[1]),
        ]
        for name, needle, hay in required:
            checks += 1
            if needle not in hay:
                fails.append(f"MISSING: {name} (looked for '{needle}')")

    finally:
        srv.terminate()

    print(f"\n{checks} checks run")
    if warns:
        print(f"\n{len(warns)} warnings:")
        for w in warns:
            print("  ~", w)
    if fails:
        print(f"\nFAILED ({len(fails)}):")
        for f in fails:
            print("  x", f)
        sys.exit(1)
    print("\nALL PASS")


if __name__ == "__main__":
    main()
