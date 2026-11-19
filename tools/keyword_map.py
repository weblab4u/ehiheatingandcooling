"""Group Google Search Console queries under the page that should rank for them, and check the built site for where each
query appears (title, H1, headings, body). Writes keyword-map.xlsx.

Run after build.py:  python3 tools/keyword_map.py "<path to Search Console export .xlsx>"
"""
import os, re, sys, html, glob, collections, importlib.util
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")

def load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, "data", name + ".py"))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

CITIES = load("cities").CITIES
ALIASES = load("search_aliases").ALIASES
NAMES = {c["name"].lower().replace("é", "e"): c["slug"] for c in CITIES}
PLACE_KEYS = sorted(list(NAMES) + list(ALIASES), key=len, reverse=True)

PRODUCTS = [("water heater", r"water heater|tankless|hot water"), ("ductless", r"ductless|mini[ -]?split"), ("heat pump", r"heat ?pump"),
            ("furnace", r"furnace"), ("air conditioner", r"air condition|\bac\b|a/c|central air|cooling"), ("air quality", r"humidif|hrv|erv|thermostat"),
            ("hvac", r"hvac|heating")]
INTENTS = [("emergency", r"emergency|24/7|same day|next day|no heat"), ("installation", r"install|new |installer|setup"), ("replacement", r"replac|upgrade"),
           ("repair", r"repair|fix|technician|broken|not working"), ("maintenance", r"maint|tune|clean|servic"), ("cost", r"cost|price|pricing|prices|how much|cheap|afford"),
           ("rebate", r"rebate|grant|incentive"), ("contractor", r"contractor|company|companies|near me|dealer|best|installers?\b")]
BRANDS = ["lennox", "goodman", "midea", "kepler", "rinnai", "carrier", "trane", "york", "daikin", "mitsubishi"]

def first(rules, q):
    for k, p in rules:
        if re.search(p, q): return k
    return "general"

def place(q):
    qq = q.replace("é", "e")
    for k in PLACE_KEYS:
        if re.search(r"(?<![a-z])" + re.escape(k) + r"(?![a-z])", qq):
            return ALIASES.get(k) or NAMES[k]
    return None

def exists(u): return os.path.exists(os.path.join(SITE, u.strip("/"), "index.html")) if u != "/" else True

def target(q):
    p, i, city = first(PRODUCTS, q), first(INTENTS, q), place(q)
    b = next((x for x in BRANDS if re.search(r"\b" + x + r"\b", q)), None)
    if re.search(r"^ehi$|efficient home|efficiency home|dustin|reviews", q): return "/reviews/" if "review" in q else "/about-ehi/"
    if b == "lennox":
        return {"air conditioner": "/brands/lennox/air-conditioners/", "heat pump": "/brands/lennox/heat-pumps/", "furnace": "/brands/lennox/furnaces/"}.get(p, "/brands/lennox/")
    if b == "goodman": return "/brands/goodman/furnaces/" if p == "furnace" else "/brands/goodman/"
    if b == "midea": return "/brands/midea/heat-pumps/" if p == "heat pump" else "/brands/midea/"
    if city:
        cands = {"furnace": [f"/{city}/furnace/", f"/{city}/furnace-repair/"] if i in ("repair", "emergency", "maintenance") else [f"/{city}/furnace/"],
                 "heat pump": [f"/{city}/heat-pump/", f"/{city}/heat-pump-installation/"], "water heater": [f"/{city}/tankless-water-heater/"],
                 "air conditioner": [f"/{city}/ac-repair/"] if i in ("repair", "emergency", "maintenance") else []}.get(p, [])
        for u in cands:
            if exists(u): return u
        return f"/{city}/"
    if "rebate" in q:
        return {"water heater": "/heat-pump-rebates/", "furnace": "/furnace/", "heat pump": "/heat-pump-rebates/"}.get(p, "/heat-pump-rebates/")
    if re.search(r"emergency|24/7", q): return "/services/emergency-hvac/"
    if re.search(r"cold (climate|weather)", q): return "/heat-pump/cold-climate/"
    if re.search(r"dual fuel", q): return "/heat-pump/hybrid-furnace-systems/"
    if re.search(r"central heat pump", q): return "/heat-pump/central/"
    if re.search(r"electric furnace", q): return "/furnace/electric-air-handlers/"
    if re.search(r"high efficiency", q): return "/furnace/high-efficiency/"
    if re.search(r"furnace warranty", q): return "/warranty/"
    if p == "ductless": return "/ac/ductless-mini-split/repair/" if i in ("repair", "maintenance") else "/ac/ductless-mini-split/"
    if p == "air quality": return "/services/humidifiers/"
    rep = i in ("repair", "maintenance")
    return {"furnace": "/furnace/repair-maintenance/" if rep else "/furnace/", "heat pump": "/heat-pump/repair-maintenance/" if rep else "/heat-pump/",
            "air conditioner": "/ac/repair-maintenance/" if rep else "/ac/", "water heater": "/water-heater/repair-maintenance/" if rep else "/water-heater/"}.get(p, "/")

_cache = {}
def page_parts(u):
    if u not in _cache:
        f = os.path.join(SITE, u.strip("/"), "index.html") if u != "/" else os.path.join(SITE, "index.html")
        if not os.path.exists(f): _cache[u] = None; return None
        h = open(f, encoding="utf-8").read()
        main = re.search(r"<main.*?</main>", h, re.S)
        main = re.sub(r"<script.*?</script>", " ", main.group(0) if main else h, flags=re.S)
        txt = lambda x: re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", x))).strip().lower()
        faq_qs = re.findall(r'"@type": "Question", "name": "([^"]+)"', h)
        _cache[u] = {"Title": txt(re.search(r"<title>(.*?)</title>", h, re.S).group(1)), "Meta description": txt(re.search(r'<meta name="description" content="([^"]*)"', h).group(1)),
                     "H1": txt(" ".join(re.findall(r"<h1[^>]*>(.*?)</h1>", h, re.S))), "H2/H3": txt(" | ".join(re.findall(r"<h[23][^>]*>(.*?)</h[23]>", main, re.S))),
                     "FAQ": txt(" | ".join(faq_qs)), "Body": txt(main)}
    return _cache[u]

def norm(x): return re.sub(r"[^a-z0-9$%]+", " ", x.lower().replace("&", " and ").replace("é", "e")).strip()
STOP = {"in", "on", "the", "a", "for", "of", "near", "me", "ontario", "or", "ca", "canada", "and", "to", "is", "my", "services", "service"}

def stem(w):
    """Crude stemming so company/companies, conditioner/conditioning, service/servicing count as one word, as they do for Google."""
    for suf, rep in (("ies", "y"), ("ing", ""), ("ers", ""), ("er", ""), ("es", ""), ("s", ""), ("e", "")):
        if len(w) > 4 and w.endswith(suf): return w[: -len(suf)] + rep
    return w

def where(q, parts):
    if not parts: return "", ""
    nq = norm(q)
    exact = [k for k, v in parts.items() if f" {nq} " in f" {norm(v)} "]
    words = {stem(w) for w in nq.split() if w not in STOP}
    allw = [k for k, v in parts.items() if words and words <= {stem(w) for w in norm(v).split()}]
    return ", ".join(exact), ", ".join(allw)

GAPS = [(r"hamilton (oh|township)", "Off-target: not our Hamilton (Hamilton, Ohio / Hamilton Township in Northumberland)"),
        (r"electric water heater", "Not served: electric tank water heaters; pages cover tankless"),
        (r"dehumidifier rebate", "No matching program on the site; leave"),
        (r"carrier|trane|el22xpv", "Brand or model we do not install; covered as repair only where relevant"),
        (r"efficiency home|^alectra$|^high efficiency$|heat pump rental", "Ambiguous or another company's name; no page targets it"),
        (r"cheap", "Price-shopping wording; pages say guaranteed pricing and financing rather than cheap"),
        (r"rockland|clarence|lasalle|amherstburg|belle river|flamborough", "Nearby town that is not on our service-area list; add it to the list first if EHI serves it"),
        (r"hvac (design|consulting)|residential hvac design|in floor heating", "Service not offered as its own page (HVAC design/consulting, in-floor heating)"),
        (r"24/7", "Site promises evenings, weekends and holidays, not 24/7, so this is not claimed")]
def gap(q):
    return next((note for pat, note in GAPS if re.search(pat, q)), "")

def main(src):
    wb = openpyxl.load_workbook(src, read_only=True)
    Q = [str(r[0]).strip().lower() for r in list(wb.worksheets[0].iter_rows(values_only=True))[1:] if r and r[0]]
    rows, by_page = [], collections.defaultdict(list)
    for q in Q:
        u = target(q); parts = page_parts(u); ex, aw = where(q, parts)
        live = "Live" if exists(u) else "Not built"
        rows.append([q, first(PRODUCTS, q), first(INTENTS, q), next((b.title() for b in BRANDS if re.search(r"\b" + b + r"\b", q)), ""),
                     (place(q) or "Ontario / no city").replace("-", " ").title(), u, live, ex or "-", aw or "-", gap(q)])
        by_page[u].append(q)
    out = openpyxl.Workbook(); ws = out.active; ws.title = "Keyword map"
    head = ["Query", "Product", "Intent", "Brand", "Location", "Target page", "Page status", "Exact match found in", "All words found in", "Note"]
    ws.append(head); [ws.append(r) for r in rows]
    ws2 = out.create_sheet("Pages"); ws2.append(["Target page", "Queries", "Exact matches on page", "Queries grouped here"])
    for u, qs in sorted(by_page.items(), key=lambda x: -len(x[1])):
        p = page_parts(u); ex = sum(1 for q in qs if where(q, p)[0])
        ws2.append([u, len(qs), ex, " | ".join(qs)])
    for w in (ws, ws2):
        for c in w[1]: c.font = Font(bold=True, color="FFFFFF"); c.fill = PatternFill("solid", fgColor="0B2540")
        w.freeze_panes = "A2"
        for col, width in zip("ABCDEFGHIJ", (42, 14, 13, 10, 20, 38, 11, 34, 34, 50) if w is ws else (40, 9, 12, 120)): w.column_dimensions[col].width = width
    for r in ws2.iter_rows(min_row=2): r[3].alignment = Alignment(wrap_text=True, vertical="top")
    path = os.path.join(ROOT, "keyword-map.xlsx"); out.save(path)
    n = len(rows); ex = sum(1 for r in rows if r[7] != "-"); aw = sum(1 for r in rows if r[8] != "-")
    print(f"{n} queries -> {len(by_page)} pages. Exact phrase on target page: {ex}. All words on target page: {aw}. Saved {path}")
    return rows

if __name__ == "__main__":
    main(sys.argv[1])
