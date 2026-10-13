# Page writing task (for content writers)

You are writing sales-oriented, SEO-optimized service pages for EHI Heating & Cooling, an HVAC contractor in Ontario, Canada.

## Read first, in this order
1. `WRITING_BRIEF.md` (business facts, voice, hard bans, page structure, internal link URLs). Treat it as law.
2. `KEYWORDS.md` (primary and secondary keywords per target page).
3. `content/heat-pump.py` (the exemplar page; copy its shape, quality and tone).
4. `build.py` (see `render_block` for every block type you can use: text, problems, cards, checklist, steps, split, table, money, cta, image, stats, html, why, areas, brands, reviews, faq, form).

## Output
- One Python file per page in `content/`, named from the URL with slashes turned into dashes: `/furnace/repair-maintenance/` -> `content/furnace-repair-maintenance.py`, `/services/hvac-installation-replacement/` -> `content/services-hvac-installation-replacement.py`, `/ac/ductless-mini-split/repair/` -> `content/ac-ductless-mini-split-repair.py`, `/brands/lennox-furnaces/` -> `content/brands-lennox-furnaces.py`.
- Each file defines `PAGE = {...}` with the same keys as the exemplar: url, title (<= 60 chars, include "Ontario" and brand "EHI"), description (<= 155 chars, include primary keyword, a benefit and a call to action), priority ("0.8" for main services, "0.7" for sub-pages), eyebrow, h1, intro (HTML, 2 to 3 sentences, primary keyword in it), hero_points (4 short trust/benefit bullets), hero_image (describe the photo we'll shoot), service ({"name","type","from_price" if we have a from-price: furnaces 3300, heat pumps 5500, tankless 3300; omit from_price otherwise}), blocks (list), faqs (5 to 7 tuples), related (4 to 6 URLs from the brief).
- Recommended block order for a service page: problems -> cards or checklist (options / what's included) -> steps -> table (cost) or money -> {"type":"money"} -> {"type":"why"} -> {"type":"areas"}. Use a "split" block with an image when you want a short expert section (e.g. "What a two-stage furnace actually does"). Use a "cta" block mid-page on longer pages.
- Body copy per page: about 700 to 1,100 words across blocks. Tight, concrete, no fluff. Every problem/solution pair must name the real symptom a homeowner notices and the real fix.
- Repair pages: the "problems" block lists symptoms (no heat, blower runs but no warm air, ignitor clicking, error codes, ice on coil, water around unit, short cycling, loud noises, smell) with what usually causes them and what we do. Include a "repair vs replace" guidance paragraph. Mention same-day service and that diagnostics come with a written quote before work.
- Maintenance content: list what the tune-up checklist includes, how often, and why it protects warranty.
- Installation pages: include a cost table with "Installed from" and honest ranges, and mention rebates/financing where relevant.
- Brand pages: hero, "why this brand" split block, a models table (sizes, efficiency, key features from the brief), "who it's right for" cards, problems it solves, what's included in install, money block, why block, FAQ (brand-specific), related.
- Use Canadian spelling and Ontario references. Use the primary keyword in title, H1 (or close variant), intro, one H2 and one FAQ. Weave secondary keywords naturally, synonyms are fine. Do not stuff.
- HTML inside strings: use `&amp;` for ampersands in text, plain `<a href="...">` for links, `<strong>` sparingly. Escape double quotes inside Python strings or use single-quoted HTML attributes.
- Do not fabricate reviews, statistics, awards, certifications, licence numbers, or specific customer stories. "Pricing from" numbers only as given in the brief. Everything else is "Quote".

## Check your work
Run `python3 build.py` from the project root. It prints `LINT <url> [...]` for any banned word, dash or exclamation issue, and `META` lines for over-length titles/descriptions. Fix until your pages print nothing. Do not edit build.py, the CSS, or other writers' files. Do not create pages you weren't assigned.
