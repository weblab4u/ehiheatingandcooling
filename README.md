# EHI Heating & Cooling website

Static, SEO-first website for EHI Heating & Cooling (Efficient Home Improvements), targeting Ontario.

## Build and preview
```bash
python3 build.py
```
Output goes to `site/`. Serve it locally with `python3 -m http.server 8765 --directory site` and open http://localhost:8765/.

The build also writes `site/sitemap.xml`, `site/robots.txt` and `site/404.html`, and prints:
- `LINT <url> [...]` when a page contains an em/en dash, a banned word, 3+ uses of unique/ensure/utmost, or more than one exclamation mark.
- `META <url>` when a title is over 62 characters or a description over 158.

## Publishing
Branches: `source` holds this project (builder, content, assets). `main` holds only the built website (the contents of `site/`, with index.html at its root). Hostinger auto-deploys `main`.
After editing content, run:
```bash
./deploy.sh
```
It rebuilds, commits and pushes `source`, then publishes `site/` to `main`. Never merge `source` into `main`: that would put the source files on the web server.

## Structure
- `build.py`: header, mega menu, footer, sticky mobile CTA, quote form, breadcrumbs, JSON-LD (HVACBusiness, WebPage, BreadcrumbList, Service, FAQPage), block renderers, lint, sitemap.
- `content/*.py`: one `PAGE` dict (or a `PAGES` list) per file. See `content/heat-pump.py` for the exemplar.
- `assets/css/style.css`, `assets/js/main.js`, `assets/img/` (all raster images are WebP; `ehi-icon.png` stays PNG for favicon compatibility).
- Icons: `ICONS` dict in `build.py` (stroke SVGs in brand green). Add a key there and reference it with `"icon": "name"` in any card.
- Grids with leftover cells get a green CTA card automatically (`fill_cta` in `build.py`). Pass `"no_fill": True` on a cards block to turn it off.
- Page templates: homepage uses the photo hero; service pages (URLs under /services/, /furnace/, /ac/, /heat-pump/, /water-heater/) use the light green hero with the quote form; every other page uses the navy `page-hero`; privacy and terms use `"layout": "article"`.
- Section variants: problems, cards, checklist, steps, table, money, why and FAQ sections each have three designs (v0, v1, v2). `with_variant` in `build.py` picks one per page from the URL, never stacks two dark bands, and keeps the homepage on v0. Add `"no_variants": True` to a page to force the default look.
- Service areas: `AREA_GROUPS` in `build.py` drives the city columns on every page and the service-areas page.
- `WRITING_BRIEF.md`: business facts and voice rules every page follows. `KEYWORDS.md`: keyword map from the research sheet. `AGENT_TASK.md`: the writer brief.

## Before launch (checklist)
1. **Brand photos**: brand pages use manufacturer product photos in `assets/img/brands/` (WebP), taken from mideacomfort.us, lennox.com, kepler-canada.com and rinnai.us, each with an "Image: [brand]" credit. They appear in the hero and the "Why [brand]" section. Confirm with each manufacturer that EHI's dealer agreement covers web use.
1a. **Job photos**: 16 real EHI install photos from the shared Drive (AC and Heat Pumps folders) live in `assets/img/work/` as WebP, with location data stripped. They are used on service pages, Midea brand pages, the homepage rebate card, About, Reviews, Rebates and Our Work, each credited "EHI install". Furnace, Product graphics and Jobs folders were empty; add photos there and they can be placed the same way. Add city names to the Our Work cards (they currently say "Ontario").
1b. **Images**: no placeholders remain. Slots without a matching EHI job photo (Lennox, Kepler, Rinnai, central AC, tankless, HRV, commercial) currently use credited manufacturer photos or a close EHI install. Swap in your own job photos as you shoot them by changing `image_src` / `hero_img` in the page's content file.
2. **Reviews**: review cards are placeholders. Paste real HomeStars/Google reviews, then add AggregateRating schema with the true rating and count.
3. **Licence numbers and founder story**: add TSSA, ODP/refrigeration and ESA/ECRA numbers, insurance details, and the founder name/year founded on `/about-ehi/` (content/about-reviews.py). Add a live seasonal offer on `/offers/` when one is running.
3b. **Google reviews**: paste 5 to 10 real Google reviews into `data/reviews.json` and run `./deploy.sh`; they appear on the homepage, About, Reviews and Our Work.
4. **Hours**: Mon to Sat 8 am to 8 pm, Sun 10 am to 5 pm, matching the Google Business Profile. Hours live in `build.py` (top bar, footer, map section, schema) and the contact page.
5. **Emergency claims**: pages say "same-day" and "evenings, weekends and holidays", not "24/7". Change only if a true 24/7 line exists.
6. **Rebate figures**: check the Home Renovation Savings Program for current amounts before launch and each quarter. The site states up to $7,500 (non-gas homes), commonly up to $2,000 (Enbridge gas homes), $12,000 ground-source, $100 smart thermostat.
7. **Form handler**: `form[data-quote-form]` posts to `/contact/`. Wire it to your form service or CRM and set `data-live="1"` on the form to disable the demo success state in `main.js`.
8. **Brand logos**: Midea, Lennox, Rinnai and Kepler logos are in `assets/img/` as WebP (Kepler from kepler-canada.com). Confirm dealer logo usage rights with each manufacturer before launch.
9. **Google Business Profile**: the map section (home, about, contact and every service page) embeds the Stouffville listing from `GBP_URL` in `build.py`. The rating line reads from `GBP_RATING` (currently 4.5 from 87 reviews, taken from the listing on 2026-10-12); update it when the listing changes. Google's self-serving review rules mean this is shown as text only, not as AggregateRating schema.
10. **Google Business Profile and HomeStars links** on `/reviews/`, and social URLs in the `sameAs` array in `build.py`.
11. **URL note**: the navigation sheet had a typo (`/heat-pump/electriic-air-handler-systems/`). The site uses `/heat-pump/electric-air-handler-systems/`. Keep that spelling in any city pages.
12. **Legal pages**: have privacy and terms reviewed.
13. **City pages**: when ready, add `/<city>/...` pages by reusing the content modules with the city injected (title, H1, intro, FAQ, schema areaServed).
