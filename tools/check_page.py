"""Check guide and city-service content files without touching site/. Usage: python3 tools/check_page.py content/<file>.py ..."""
import sys, os, re, importlib.util
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, ROOT)
spec = importlib.util.spec_from_file_location("build", os.path.join(ROOT, "build.py")); B = importlib.util.module_from_spec(spec); sys.modules["build"] = B; spec.loader.exec_module(B)
import schema as _S; _S.B = B._BuildGlobals()
bad = False
for f in sys.argv[1:]:
    spec = importlib.util.spec_from_file_location("p", f); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); pg = m.PAGE; probs = []
    B.REG.setdefault(pg["url"], (re.sub("<[^>]+>", "", pg["h1"]), pg["description"]))
    if pg.get("city_service"):
        for c in B.CITIES:
            B.CITY_PAGES.add(f"/{c['slug']}/"); B.REG.setdefault(f"/{c['slug']}/", (f"HVAC {c['name']}", ""))
        for b in pg["blocks"]:
            if b.get("photo") or b["type"] == "mosaic": b["_imgs"] = [next(k for k in B.CITY_PHOTOS if os.path.exists(os.path.join(ROOT, "assets", "img", "work", k + ".webp")))]
        svc = pg["url"].rstrip("/").split("/")[-1]; city = B.CITY_BY_SLUG[pg["city_service"]]["name"]
        kw = {"heat-pump-installation": "heat pump installation", "furnace-repair": "furnace repair", "ac-repair": "ac repair"}[svc]
        h1 = re.sub("<[^>]+>", "", pg["h1"]).lower()
        if kw not in h1 or city.lower() not in h1: probs.append(f'H1 must contain "{kw}" and "{city}"')
        if not pg["title"].lower().startswith(kw.replace("ac ", "ac ")): probs.append(f'title must start with "{kw.title()}"')
        types = [b["type"] for b in pg["blocks"]]
        for need in ("problems", "cost_guide", "steps", "equipment", "checklist", "split", "money"):
            if need not in types: probs.append(f"missing {need} block")
        if len(pg.get("faqs", [])) < 6: probs.append("needs 6 FAQs")
        if f"/{pg['city_service']}/" not in repr(pg["blocks"]) + repr(pg["faqs"]): probs.append("link to the city page once in body copy")
    if pg.get("guide"):
        texts = [b for b in pg["blocks"] if b["type"] == "text"]
        if len(texts) < 8: probs.append(f"only {len(texts)} text sections (need 8 to 10)")
        words = len(re.sub("<[^>]+>", " ", " ".join(b["html"] for b in texts)).split())
        if words < 1700: probs.append(f"only {words} words (need 1,800+)")
        if "<table" not in repr(pg["blocks"]): probs.append("needs a comparison table")
        if 'class="checklist"' not in repr(pg["blocks"]): probs.append("needs a checklist")
        h1 = re.sub("<[^>]+>", "", pg["h1"]).lower(); c = pg["guide_city"].lower()
        if not (f"hvac company in {c}" in h1 or f"{c} hvac compan" in h1): probs.append('H1 must contain "HVAC company in <City>" or "<City> HVAC companies"')
    html = B.render(pg)
    lp = B.lint(pg["url"], html)
    if lp: probs.append(f"LINT {lp}")
    if len(pg["title"]) > 62: probs.append(f"title {len(pg['title'])} chars")
    if len(pg["description"]) > 158: probs.append(f"description {len(pg['description'])} chars")
    if re.search(r"\bEHI\b|Efficient Home", pg["title"] + pg["description"]): probs.append("no brand in title/description")
    print(f"{f}: " + ("OK" if not probs else ""))
    for p in probs: print("   FAIL", p); bad = True
print("ALL OK" if not bad else "FIX THE FAILS ABOVE"); sys.exit(1 if bad else 0)
