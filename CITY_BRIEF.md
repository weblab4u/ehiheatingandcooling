# City landing pages: writing brief

You write city landing pages for EHI Heating & Cooling, an Ontario HVAC contractor. Each page lives at
`/city-slug/` and targets "HVAC [City]" plus contractor, technician, company and service keywords.

## Read first (in this order)
1. `WRITING_BRIEF.md`: business facts, voice, hard bans. It is law. Every rule applies here too.
2. `data/cities.py`: verified local facts for each city (housing, utility, gas, climate, angle,
   neighbourhoods, layout letter). Use ONLY these local facts plus general, well-known Ontario facts.
3. `content/city-toronto.py`: the finished reference page (layout A). Match its quality and tone.
   Do NOT reuse its sentences, headings, problem titles or FAQ wording. Every page must read as its own.

## Output
One file per city: `content/city-<slug>.py` defining `PAGE = {...}`. Keys:
- `url` "/<slug>/", `city` "<slug>", `layout` (the letter in data/cities.py, do not change it), `priority` "0.7" ("0.8" only for Toronto, Ottawa, Mississauga, Hamilton).
- `title`: must START with "HVAC <City>", max 62 characters, no "EHI" or brand name. Vary the rest per city
  (e.g. "HVAC Markham | Furnace, AC & Heat Pump Contractor", "HVAC Sudbury | Heating & Cooling Technicians").
- `description`: max 158 characters, no brand name, includes "HVAC <City>" or "<City> HVAC", a benefit and a call to action.
- `eyebrow`: short pin label, e.g. "Markham · York Region".
- `h1`: contains the city name and an exact-match keyword ("HVAC Contractor in <City>", "<City> HVAC Services", "<City> Heating and Cooling ...").
- `tagline` (optional, one short line), `intro` (HTML `<p>`, 2 to 3 sentences, "HVAC" + city in the first sentence).
- `hero_points`: 4 short trust or benefit bullets (vary them per city; do not copy Toronto's).
- `hero_stats` (layouts C and F only): 3 tuples for C, 4 for F, as `(value, label)`, e.g. `("-30°C", "Heat pump rating")`,
  `("Alectra", "Local hydro utility")`, `("Same day", "Replies in most cases")`, `("Up to $7,500", "Heat pump rebate")`.
  Facts only from the brief or data/cities.py.
- `service`: `{"name": "HVAC services in <City>", "type": "HVAC contractor", "area": "<City>"}`.
- `blocks`: follow the outline for the page's layout below. Same block order. Write all the copy yourself.
- `faqs`: 5 to 7 tuples. City-specific questions, direct one-sentence answer first. At least 2 FAQs contain an exact-match keyword.
- `related`: 5 or 6 service URLs from WRITING_BRIEF.md that fit this city's angle.

## Layout outlines (block order is fixed per layout)
- **A** (hero has a quote form and a photo strip): snapshot, problems, mosaic (count 5), svc_links, steps, money, neighbourhoods, reviews
- **B** (full-width photo hero with form): split (photo "out"), svc_links, problems, mosaic (count 4), table (cost guide), neighbourhoods, why, cta
- **C** (photo mosaic hero, NO form in hero, needs hero_stats x3): problems, snapshot, split (photo "in", reverse True), steps, quote_split (photo "sys"), mosaic (count 3), money
- **D** (centred hero with 4 photo tiles, NO form in hero): svc_links, checklist (photo "out"), split (photo "in"), mosaic (count 5), quote_split (photo "any"), gbp, neighbourhoods
- **E** (navy hero with a photo card, NO form in hero): snapshot, cards (3 or 4 "who we serve" cards with icons), problems, mosaic (count 6), steps, quote_split (photo "out"), reviews
- **F** (navy hero with form and a 4-item facts bar, needs hero_stats x4): split (photo "in"), problems, svc_links, table (cost guide), mosaic (count 4), why, neighbourhoods, cta

## Block formats
Photos are assigned automatically: never write image paths. Just add `"photo": "out" | "in" | "sys" | "any"` where the outline says.
- `{"type": "snapshot", "h2", "lead", "items": [{"icon", "label", "value", "text"} x4]}`: local facts (homes, hydro/gas, climate, access, rebate tier, hours).
- `{"type": "problems", "h2", "lead", "items": [{"problem", "solution"} x5 to 7]}`: problem = what the homeowner notices; solution = what causes it and what we do. Rooted in this city's angle.
- `{"type": "mosaic", "count": N, "h2", "lead"}`: photo grid. Lead must NOT claim the photos were taken in this city ("a few of our recent Ontario jobs" style).
- `{"type": "svc_links", "h2", "lead", "items": [{"url", "title", "text"} x6 to 8]}`: titles use the city ("Furnace repair in Oakville"). URLs only from WRITING_BRIEF.md internal links.
- `{"type": "split", "h2", "html", "photo": kind, "reverse": bool}`: an expert section about this city's angle (`<p>` and optionally `<ul class="checklist"><li>..</li></ul>`).
- `{"type": "checklist", "h2", "lead", "items": [6 to 8 strings], "photo": "out"}`.
- `{"type": "steps", "h2", "lead", "items": [{"title", "text"} x4]}`.
- `{"type": "table", "h2", "lead", "headers": [...], "rows": [[...]], "note"}`: cost guide. Only these from-prices exist: furnaces from $3,300, heat pumps from $5,500, tankless from $3,300. Everything else is "Quote". Mention rebates and financing in the note.
- `{"type": "quote_split", "h2", "html", "photo": kind, "form_h3" (optional)}`: persuasive copy + checklist next to the quote form.
- `{"type": "cards", "h2", "lead", "items": [{"icon", "title", "text"}]}`: icons from: heatpump furnace flame snow ac ductless multizone wrench bolt water tankless air humidity hrv thermostat install house dollar percent rebate shield clock calendar leaf check phone pin chat truck clipboard gauge noise alert plug duct tag star.
- `{"type": "neighbourhoods", "h2", "lead"}`: the chip list comes from data/cities.py automatically.
- `{"type": "money"}`, `{"type": "why"}`, `{"type": "reviews"}`, `{"type": "gbp", "h2", "lead"}`: shared blocks, no copy needed except gbp h2/lead.
- `{"type": "cta", "h2", "text"}`: short closing band.

## Keyword strategy (same as the rest of the site)
- Primary: "HVAC <City>". Supporting exact matches (use at least 5 different ones per page, at least 4 inside H1/H2/H3 headings):
  HVAC contractor in <City> · <City> HVAC contractor · HVAC technician in <City> · <City> HVAC companies · HVAC services in <City> ·
  heating and cooling in <City> · furnace repair in <City> · heat pump installation in <City> · AC repair in <City> · emergency HVAC in <City> ·
  HVAC company in <City> · furnace installation in <City> · air conditioning in <City>.
- Pick a DIFFERENT mix and different heading wording per city. Never stuff; every heading must read naturally.
- Mention the city name naturally 8 to 14 times; mention 2 to 4 local neighbourhoods in body copy.

## Uniqueness (the most important rule)
- Each page is built around its city's `angle` in data/cities.py. The problems, split section, FAQs and snapshot should mostly be about that angle.
- No two pages may share a sentence, heading or FAQ question. Vary sentence structure, not just the city name.
- Never invent offices, staff names, customers, projects, response times, statistics or awards. Our only office is in Stouffville.
- Don't claim photos were taken in the city. Don't promise a specific arrival time.
- Body copy target: 900 to 1,200 words of your own writing per page.

## Check your work
Run `python3 tools/check_city.py content/city-<slug>.py` for each of your files and fix until it prints ALL OK.
Do NOT run `python3 build.py` (other writers are working at the same time). Do not edit any file except your own `content/city-*.py` files.

## Batch 2 notes (the remaining service-area communities)
- **Districts of a bigger city** (Scarborough, North York, Etobicoke, Thornhill, Woodbridge, Stoney Creek, Ancaster, Kanata, Orléans, Nepean):
  the parent city already has a page. Your page must be built on the district's own angle in data/cities.py, use different
  headings and problems from the parent page (read it first: content/city-<parent>.py), and link to the parent once in body copy
  (e.g. `<a href="/toronto/">HVAC in Toronto</a>`). Parents: Scarborough, North York, Etobicoke -> /toronto/;
  Thornhill -> /vaughan/ and /markham/; Woodbridge -> /vaughan/; Stoney Creek, Ancaster -> /hamilton/; Kanata, Orléans, Nepean -> /ottawa/.
- **Pages that also cover a neighbouring place** (named in the region field): Georgina covers Keswick, Caledon covers Bolton,
  Georgetown covers Halton Hills and Acton, Bowmanville covers Clarington, Midland covers Penetanguishene, Alliston covers Angus,
  St. Catharines covers Thorold, Kawartha Lakes covers Lindsay. Mention the covered place by name in the intro and at least one heading.
- **Small towns** (under roughly 30,000 people) can be shorter: 800 to 1,000 words of your own copy is enough. Don't pad.
- Use the exact `name` from data/cities.py in keyword headings, including punctuation and accents (e.g. "St. Catharines", "Orléans",
  "Niagara-on-the-Lake", "Sault Ste. Marie").
- Before finishing, compare your pages against ALL other content/city-*.py files (there are 27 published already plus other
  writers' new ones) and reword any shared sentence, heading, problem title or FAQ question.

## Deepening pass (October 2026): two new blocks, available on every layout
- `{"type": "cost_guide", "h2": "...", "lead": "..."}`: a price table rendered from data/pricing.py (from-prices and "written quote" until EHI confirms ranges). Write only the h2 and lead; optional `"keys"` picks which rows. Write the h2 with the city, e.g. "What HVAC work costs in Whitby".
- `{"type": "equipment", "h2": "...", "lead": "...", "groups": ["heat_pumps", "furnaces"]}`: model cards (specs and warranty) from data/pricing.py. Groups: furnaces, heat_pumps, water_heaters. Pick the groups that fit the city's angle.
- Add a cost FAQ to every page that lacks one: "How much does [a heat pump / a new furnace / furnace repair] cost in <City>?", answered with the from-price and the written-quote line. Never invent a range.
