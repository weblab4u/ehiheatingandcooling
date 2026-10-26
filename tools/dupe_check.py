"""Compare the copy of all city pages: shared 8-word phrases, repeated headings and FAQ questions."""
import glob, importlib.util, re, itertools, collections
def copy_of(pg):
    parts = [pg["h1"], pg.get("tagline", ""), pg["intro"]] + pg.get("hero_points", [])
    heads = [pg["h1"]]
    for b in pg["blocks"]:
        for k in ("h2", "lead", "html", "text", "card_h", "card_text"):
            if b.get(k): parts.append(b[k])
        if b.get("h2"): heads.append(b["h2"])
        for i in b.get("items", []) or []:
            if isinstance(i, dict):
                parts += [str(v) for k, v in i.items() if k not in ("icon", "url")]
                for k in ("problem", "title"):
                    if i.get(k): heads.append(i[k])
            else: parts.append(str(i))
        for r in b.get("rows", []) or []: parts += r
    parts += [q + " " + a for q, a in pg.get("faqs", [])]
    return re.sub(r"<[^>]+>", " ", " ".join(parts)), heads, [q for q, a in pg.get("faqs", [])]
pages = {}
for f in sorted(glob.glob("content/city-*.py")):
    spec = importlib.util.spec_from_file_location("p", f); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    pages[m.PAGE["city"]] = m.PAGE
import importlib.util as _u
_sp = _u.spec_from_file_location("c", "data/cities.py"); _c = _u.module_from_spec(_sp); _sp.loader.exec_module(_c)
names = {}
for _x in _c.CITIES:
    names[_x["slug"]] = _x["name"]
names = {k: v for k, v in sorted(names.items(), key=lambda kv: -len(kv[1]))}
def norm(t, city):  # neutralise the city name so "X in Toronto" == "X in Markham"
    t = t.lower()
    for n in names.values(): t = t.replace(n.lower(), "@city")
    t = t.replace("kitchener", "@city").replace("waterloo", "@city")
    return re.findall(r"[a-z0-9@$%°']+", t)
sh = {}; heads = {}; faqs = {}
for s, pg in pages.items():
    txt, hs, fq = copy_of(pg); w = norm(txt, s)
    sh[s] = {" ".join(w[i:i+8]) for i in range(len(w) - 7)}
    heads[s] = {" ".join(norm(h, s)) for h in hs}; faqs[s] = {" ".join(norm(q, s)) for q in fq}
print(f"{len(pages)} city pages")
worst = []
for a, b in itertools.combinations(pages, 2):
    inter = len(sh[a] & sh[b]); ratio = inter / max(1, min(len(sh[a]), len(sh[b])))
    worst.append((ratio, a, b, inter))
worst.sort(reverse=True)
print("Highest 8-word phrase overlap between two pages:")
for r, a, b, n in worst[:8]: print(f"  {r:6.1%}  {a} / {b}  ({n} shared phrases)")
def repeats(d, label):
    c = collections.defaultdict(list)
    for s, items in d.items():
        for x in items: c[x].append(s)
    rep = {k: v for k, v in c.items() if len(v) > 1}
    print(f"{label} reused across pages: {len(rep)}")
    for k, v in list(rep.items())[:15]: print(f"   '{k}'  ->  {', '.join(v)}")
repeats(heads, "Headings / problem titles"); repeats(faqs, "FAQ questions")
