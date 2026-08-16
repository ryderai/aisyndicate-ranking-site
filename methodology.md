# Methodology — The GEO Agency Index

Version 1.0. Every point in The GEO Agency Index comes from something a browser can fetch. There is no survey, no questionnaire and no opinion score.

## The seven checks



**llms.txt published — 22 points (AI readiness).** A plain-text file at /llms.txt that lists the site's important pages for AI assistants. How it was checked: Request https://DOMAIN/llms.txt. Counts only if the response is real plain text. A page of HTML, a redirect to the homepage, or a 404 does not count.

**Runs its own tracking software — 20 points (AI readiness).** The agency operates its own named software for tracking AI visibility, that a client can log into — rather than reselling somebody else's tool or sending a PDF. How it was checked: Look for a named product with its own product page AND a working customer login or signup. Naming a third-party tool (Semrush, Ahrefs, Profound, Peec, Otterly, Scrunch) does not count. An internal "framework" or "methodology" the agency's own team runs does not count — the client has to be able to log in.

**Names the AI engines it covers — 14 points (AI readiness).** A public page names at least three specific AI engines the agency works on, so a buyer knows what they are paying for. How it was checked: Look for at least three of: ChatGPT, Perplexity, Gemini, Google AI Overviews, Google AI Mode, Copilot, Claude, Grok, Meta AI, DeepSeek, Mistral, Alexa, Siri. Saying "AI search engines" or "LLMs" in general does not count. If a site's bot protection stops an automated client reading the page, it does not count — an AI cannot read it either.

**robots.txt names AI crawlers — 14 points (AI readiness).** The robots.txt file names AI crawlers by name and says what they may do, instead of leaving them to a catch-all rule. How it was checked: Read https://DOMAIN/robots.txt and look for any of: GPTBot, OAI-SearchBot, ChatGPT-User, PerplexityBot, ClaudeBot, anthropic-ai, CCBot, Google-Extended, Applebot-Extended, Bytespider, Amazonbot. Full points only if at least one is named and none of the eleven is denied site-wide access. A rule blocking a single path, such as an API directory, is not site-wide denial.

**Price readable by a machine — 14 points (AI readiness).** A real price for the agency's own work sits inside a plain-text file an AI can read, not only inside a web page. How it was checked: Look for a dollar figure for their own service inside /llms.txt, /llms-full.txt or /agents.md on their own domain. A price on an HTML page only does not count — that is the whole point of the check.

**llms-full.txt published — 8 points (AI readiness).** The long version of llms.txt: the site's actual content in one text file, so an AI can read it without crawling. How it was checked: Request https://DOMAIN/llms-full.txt. Same rule: plain text only.

**agents.md published — 8 points (AI readiness).** A file that tells AI agents who the business is and what it is allowed to be quoted on. How it was checked: Request https://DOMAIN/agents.md. Same rule: plain text only.

**Prices published — 15 points (Buyer transparency).** A real dollar figure for their own work is on a public page. "Contact us for a quote" does not count. How it was checked: Check the homepage, /pricing, and any pricing link in the navigation. The figure has to be attached to their own service, not to a client's result or an industry average. Any public URL on their own domain counts, including a text file — one agency publishes its minimum fee only inside llms.txt, and it scores.

**Team named on their own site — 10 points (Buyer transparency).** At least one real person, named, on the agency's own website. How it was checked: Check the homepage, /about and /team, and any public text file on their own domain. LinkedIn does not count. People quoted as clients in testimonials are not that agency's staff.

**Case studies name the client — 10 points (Buyer transparency).** Published work that names the actual client, not "a B2B SaaS company". How it was checked: Check the case studies or results page for at least one named client.

**Case studies carry a number — 5 points (Buyer transparency).** At least one published result with a specific figure attached. How it was checked: Check the same pages for a stated percentage, dollar figure or multiple.

**You can buy without a sales call — 0 points (Buyer transparency).** A visitor can start paying, or start a free trial, without booking a call or filling in a lead form first. How it was checked: Look for a public signup, a checkout, a "start free trial", or a plan button that leads to creating an account. "Book a call", "Get a proposal", "Request a quote", "Contact us" and a "free audit" that is really a form all count as no.

## Rules fixed before the audit

A file counts only if it returns plain text; HTML or a soft 404 scores zero. A file behind a cross-host redirect still counts, with the redirect noted on that agency's profile. A sitemap counts at /sitemap.xml or at any path named in robots.txt. People must be named on the agency's own site — LinkedIn and client testimonials do not count. A price must be the agency's own price, not a client result or an industry average. Equal scores share a rank.

## What this does not measure

This is not a measure of whether an agency does good work. It measures whether the public evidence a buyer can check lines up with what the agency sells. Ahrefs (15 June 2026, 137,210 domains) found 97% of llms.txt files got no requests in the month measured; the file is scored here as a clean public signal, not as a traffic driver. Pew (22 July 2025) and Ahrefs (12 December 2025) both find off-site brand mentions correlate with AI citation far more than on-site markup does.

Every measurement is dated 14 August 2026. Raw data: https://aisyndicate-ranking-site.vercel.app/data.json
