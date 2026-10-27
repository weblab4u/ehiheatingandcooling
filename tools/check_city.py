"""Check one or more city content files without touching site/.
Usage: python3 tools/check_city.py content/city-markham.py [more files...]
Prints lint problems, meta lengths, keyword placement and word count. Exit code 1 if anything fails."""
import sys, os, re, importlib.util
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
spec = importlib.util.spec_from_file_location("build", os.path.join(ROOT, "build.py")); B = importlib.util.module_from_spec(spec); sys.modules["build"] = B; spec.loader.exec_module(B)
import schema as _S; _S.B = B._BuildGlobals()
LAYOUT_FORM = {"A": True, "B": True, "C": False, "D": False, "E": False, "F": True}
bad = False
for f in sys.argv[1:]:
    spec = importlib.util.spec_from_file_location("p", f); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    pg = m.PAGE; c = B.CITY_BY_SLUG[pg["city"]]; name = c["name"]; probs = []
    if pg["url"] != f"/{c['slug']}/": probs.append("url must be /" + c["slug"] + "/")
    if pg["layout"] != c["layout"]: probs.append(f"layout must be {c['layout']} (from data/cities.py)")
    B.CITY_PAGES.add(pg["url"]); B.REG.setdefault(pg["url"], (f"HVAC {name}", ""))
    B.allocate_city_photos([pg])
    html = B.render(pg)
    lp = B.lint(pg["url"], html)
    if lp: probs.append(f"LINT {lp}")
    if len(pg["title"]) > 62: probs.append(f"title {len(pg['title'])} chars (max 62)")
    if len(pg["description"]) > 158: probs.append(f"description {len(pg['description'])} chars (max 158)")
    if re.search(r"\bEHI\b|Efficient Home", pg["title"] + pg["description"]): probs.append("no brand name in title/description")
    if not pg["title"].lower().startswith(f"hvac {name.lower()}"): probs.append(f'title must start with "HVAC {name}"')
    low = html.lower(); n = name.lower()
    variants = [f"hvac {n}", f"hvac contractor in {n}", f"{n} hvac contractor", f"hvac technician in {n}", f"{n} hvac technician", f"{n} hvac companies",
                f"hvac companies in {n}", f"hvac services in {n}", f"{n} hvac services", f"heating and cooling in {n}", f"{n} heating and cooling",
                f"furnace repair in {n}", f"heat pump installation in {n}", f"ac repair in {n}", f"hvac in {n}", f"{n} hvac", f"hvac company in {n}",
                f"emergency hvac in {n}", f"hvac repair in {n}", f"air conditioning in {n}", f"furnace installation in {n}"]
    heads = " ".join(re.findall(r"<h[1-3][^>]*>(.*?)</h[1-3]>", low, re.S))
    in_heads = sorted({v for v in variants if v in heads})
    if len(in_heads) < 4: probs.append(f"only {len(in_heads)} exact-match keyword variants in H1-H3 (need 4+): {in_heads}")
    if n not in re.sub("<[^>]+>", " ", pg["h1"]).lower(): probs.append("H1 must contain the city name")
    if LAYOUT_FORM[pg["layout"]] is False and not any(b["type"] == "quote_split" for b in pg["blocks"]): probs.append("this layout needs a quote_split block")
    if pg["layout"] in ("C", "F") and len(pg.get("hero_stats", [])) < 3: probs.append("layout C/F needs hero_stats (3 or 4 tuples)")
    text = re.sub(r"<script.*?</script>|<header.*?</header>|<footer.*?</footer>|<nav.*?</nav>", " ", html, flags=re.S)
    words = len(re.sub("<[^>]+>", " ", text).split())
    print(f"{f}: layout {pg['layout']}, ~{words} words on page, keyword variants in headings: {len(in_heads)}")
    for p in probs: print("   FAIL", p); bad = True
print("ALL OK" if not bad else "FIX THE FAILS ABOVE")
sys.exit(1 if bad else 0)
