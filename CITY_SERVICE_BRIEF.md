# City-plus-service pages and "how to choose" guides: writing brief

Read WRITING_BRIEF.md first (business facts, voice, hard bans: it is law), then CITY_BRIEF.md for the keyword style and uniqueness rules, then data/cities.py for the city's facts. Everything below adds to those.

## A. City-plus-service pages
URL pattern: `/<city-slug>/<service-slug>/` for three services:
- `heat-pump-installation` (primary keyword "heat pump installation <City>"; secondary: heat pump installers, heat pump cost, cold climate heat pump, heat pump rebate)
- `furnace-repair` (primary "furnace repair <City>"; secondary: furnace not heating, furnace repair cost, emergency furnace repair, furnace tune up)
- `ac-repair` (primary "AC repair <City>"; secondary: air conditioner repair, AC not cooling, emergency AC repair, AC repair cost)

File: `content/cs-<city-slug>-<service-slug>.py` with `PAGE = {...}`:
- `url`, `city_service`: "<city-slug>", `priority` "0.7".
- `title`: starts with the service and city ("Heat Pump Installation Markham | ..."), max 62 chars, no brand name.
- `description`: max 158 chars, primary keyword, benefit, call to action, no brand.
- `eyebrow`: e.g. "Heat Pump Installation · Markham".
- `h1`: contains the exact primary keyword ("Heat Pump Installation in Markham ...").
- `tagline` (one line), `intro` (2 to 3 sentences, keyword in the first), `hero_points` (4), `hero_image` (short description; a job photo is picked automatically).
- `service`: `{"name": "<Service> in <City>", "type": "<service type>", "area": "<City>"}`.
- `blocks`, in this order:
  1. `problems` (6 to 8 items specific to the service AND the city's housing/climate angle)
  2. `cost_guide` (h2 with the city; set `"keys"` to the 2 or 3 rows that fit the service, e.g. heat pump pages: `["heat_pump_ducted", "ductless_single"]`; furnace repair: `["furnace_repair", "furnace_install"]`; AC repair: `["ac_repair", "ac_install", "heat_pump_ducted"]`)
  3. `steps` (4 steps: what a visit or install looks like for this service)
  4. `equipment` (heat pump pages: `["heat_pumps"]`; furnace repair: `["furnaces"]`; AC repair: `["heat_pumps"]` with a lead explaining a heat pump is the modern AC replacement)
  5. `checklist` with `"photo": "in"` or `"out"` (what's included)
  6. `split` with `"photo": "sys"` (an expert section: e.g. repair vs replace rule, how we size, what the rebate needs)
  7. `money`
- `faqs`: 6, at least 3 containing the primary keyword or city, one about cost (from-price + written quote, never an invented range), one about timing (no promised arrival times), one about rebates/financing where relevant.
- `related`: the province-wide service page for this service plus 3 or 4 others, and the city page `/<city-slug>/`.
- Link to the city page once in body copy and to the province-wide service page once.
- Body copy target: 900 to 1,200 words of your own. Every page must differ from the city page, the province-wide service page (read it: /furnace/repair-maintenance/, /ac/repair-maintenance/, /heat-pump/cold-climate/) and the other two services for that city.

## B. "How to choose an HVAC company in <City>" guides
URL: `/blog/how-to-choose-an-hvac-company-in-<city-slug>/`. File: `content/guide-<city-slug>.py` with `PAGE = {...}`:
- `url`, `layout`: "article", `guide`: True, `guide_city`: "<City>", `published`: "2026-10-27", `priority` "0.6".
- `title`: "How to Choose an HVAC Company in <City> (2026 Guide)" or similar, max 62 chars, no brand.
- `description`: max 158, includes "HVAC companies in <City>" or "<City> HVAC companies".
- `h1`: contains "HVAC company in <City>" or "<City> HVAC companies".
- `meta_line`: "Published October 2026 · Written by the EHI Heating And Cooling team · Reviewed against current TSSA, ESA and Home Renovation Savings Program rules".
- `intro`: 2 or 3 sentences that answer the search directly: what a good HVAC company in this city looks like and what the guide covers.
- `blocks`: 8 to 10 `{"type": "text", "h2": "...", "html": "..."}` sections. Required sections, in your own words and order:
  - What a licensed HVAC company in <City> must have (TSSA gas registration, licensed refrigeration techs, ESA/ECRA for electrical, WSIB, insurance; how to check each one)
  - The 7 questions to ask before you sign (written quote with model numbers, who does the install, permits, heat-loss sizing, warranty registration, rebate pre-approval, what happens if the price changes)
  - Red flags (phone quotes without a visit, "today only" pricing, no permit, rental pushes, cash-only, no model numbers)
  - What HVAC work typically costs in <City> (use data/pricing.py from-prices and "written quote"; may cite that typical furnace repairs are a few hundred dollars and installs run from the from-price up depending on size; never invent exact ranges)
  - How <City>'s homes change the answer (use the city's housing, climate and angle from data/cities.py)
  - Rebates and financing in <City> (program facts from WRITING_BRIEF.md; local hydro and gas names where known)
  - A comparison table (HTML `<table>`) of "what to compare" across 4 to 5 kinds of company: national chain, rental/utility provider, big local firm, small independent, EHI. Compare on: who does the work, written guaranteed price, rebate paperwork, brands, warranty terms, after-hours service. Be fair and factual about the other kinds; do not name competitors.
  - Why we'd put EHI on your shortlist (one honest section: 20+ years, HomeStars Best Company 2019 to 2021, authorized Midea/Lennox/Kepler/Rinnai, guaranteed pricing, rebate paperwork; no invented numbers)
  - A printable checklist (`<ul class="checklist">`) to take to every quote
- `cta_h2` / `cta_text` for the closing box.
- Length: 1,800 to 2,400 words. Plain, direct, useful. Link to the city page and to 3 or 4 service pages.

## C. Deepening thin city pages
For each assigned city page, add to the existing `content/city-<slug>.py` without rewriting what is there:
- A `cost_guide` block (h2 with the city, 1 or 2 sentence lead) placed after the problems block.
- An `equipment` block with the groups that fit the city's angle, placed before `money` (or before `neighbourhoods` if there is no money block).
- One cost FAQ if the page has none ("How much does ... cost in <City>?") answered with the from-price and written-quote line.
- 150 to 300 more words of your own in the sections that are thinnest for that city: another problem item, a longer split section, or a fuller FAQ. Keep everything specific to the city's angle; no padding.
- Run `python3 tools/check_city.py content/city-<slug>.py` and fix until ALL OK.

## Checks
- A and B pages: run `python3 tools/check_page.py <file>` (lint, meta lengths, keyword in H1). Fix until ALL OK.
- Never run build.py. Never edit files other than your own. All hard bans apply: no dashes, no banned words, no invented facts, offices, staff, response times or statistics.
