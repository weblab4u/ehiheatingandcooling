"""Structured data (JSON-LD) for every page.

Local SEO model, following Google's guidance for service-area businesses:
- ONE business entity (HVACBusiness + LocalBusiness) at the real Stouffville address, identical on every page
  and referenced everywhere by @id. City pages never claim a local office.
- Each city is a Place node (#city) with its region, province, country and the neighbourhoods we cover.
  The business lists every city in areaServed; a city page carries the full node for its own city.
- City pages describe "HVAC services in <City>" as a Service provided by the business, with keyword variants,
  the services offered there (OfferCatalog), from-prices and the city as areaServed.
- Ratings and reviews sit on the business only (they are reviews of the business, not of a city page).
"""
import re

B = None   # the build module, injected by build.py (B.SITE, B.CITIES, ...)

REGION_NAMES = {"Toronto and York Region": "Toronto and York Region", "Peel and Halton": "Peel and Halton", "Durham Region": "Durham Region",
                "Simcoe, Muskoka and cottage country": "Simcoe County and Muskoka", "Hamilton and Niagara": "Hamilton and the Niagara Region",
                "Southwestern Ontario": "Southwestern Ontario", "Eastern Ontario": "Eastern Ontario", "Northern Ontario": "Northern Ontario"}

CORE_SERVICES = [
    ("HVAC installation and replacement", "/services/hvac-installation-replacement/", None),
    ("HVAC repair and maintenance", "/services/hvac-repair-maintenance/", None),
    ("Emergency HVAC service", "/services/emergency-hvac/", None),
    ("Cold-climate heat pump installation", "/heat-pump/cold-climate/", "heat_pump"),
    ("Heat pump repair and maintenance", "/heat-pump/repair-maintenance/", None),
    ("Hybrid heat pump and furnace systems", "/heat-pump/hybrid-furnace-systems/", None),
    ("High-efficiency gas furnace installation", "/furnace/high-efficiency/", "furnace"),
    ("Furnace repair and tune-ups", "/furnace/repair-maintenance/", None),
    ("Central air conditioner installation", "/ac/", None),
    ("AC repair and maintenance", "/ac/repair-maintenance/", None),
    ("Ductless mini split installation", "/ac/ductless-mini-split/", None),
    ("Multi-zone ductless systems", "/ac/multi-zone-ductless-system/", None),
    ("Tankless water heater installation", "/water-heater/", "tankless"),
    ("Whole-home humidifiers", "/services/humidifiers/", None),
    ("HRV and ERV ventilation", "/services/hrv-erv/", None),
    ("Smart thermostat installation", "/services/thermostats/", None),
    ("Heat pump rebate applications", "/heat-pump-rebates/", None),
    ("HVAC financing", "/financing/", None),
]
KEYWORDS = ["HVAC contractor", "HVAC company", "HVAC services", "heating and cooling", "HVAC installation", "HVAC repair", "HVAC maintenance",
            "emergency HVAC", "furnace repair", "furnace installation", "heat pump installation", "cold climate heat pump", "air conditioning",
            "AC repair", "ductless mini split", "tankless water heater", "Ontario heat pump rebate", "HVAC financing", "licensed HVAC technician"]

def org_id(): return B.SITE + "/#organization"
def city_id(slug): return f"{B.SITE}/{slug}/#city"

def _offer(name, url, from_key, area=None):
    o = {"@type": "Offer", "itemOffered": {"@type": "Service", "name": name, "url": B.SITE + url, "provider": {"@id": org_id()},
                                           **({"areaServed": area} if area else {})}}
    if from_key:
        price = B.PRICING.FROM[from_key].replace(",", "")
        o.update({"priceCurrency": "CAD", "priceSpecification": {"@type": "PriceSpecification", "minPrice": price, "priceCurrency": "CAD",
                  "description": "Installed price from; final price depends on size and installation requirements, quoted in writing"}})
    return o

def region_of(slug):
    for g, names in B.AREA_GROUPS:
        for n in names:
            u = B.city_href(n)
            if u and u.strip("/") == slug: return REGION_NAMES.get(g, g)
    return None

def city_place(slug, full=False):
    """The City node. full=True adds neighbourhoods and the containment chain (used on that city's own pages)."""
    c = B.CITY_BY_SLUG[slug]
    node = {"@type": "City", "@id": city_id(slug), "name": c["name"]}
    if not full: return node
    region = region_of(slug)
    node.update({
        "alternateName": f'{c["name"]}, Ontario',
        "description": f'{c["name"]} ({c["region"]}): {c["housing"]}.',
        "containedInPlace": {"@type": "AdministrativeArea", "name": region or c["region"],
                             "containedInPlace": {"@type": "State", "name": "Ontario", "containedInPlace": {"@type": "Country", "name": "Canada"}}},
        "containsPlace": [{"@type": "Place", "name": f'{n}, {c["name"]}'} for n in c["neighbourhoods"]],
        "url": f"{B.SITE}/{slug}/",
    })
    return node

def business():
    reviews = [r for r in B.load_reviews() if not r.get("reviews_page_only")]
    hours = [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], "opens": "08:00", "closes": "20:00"},
             {"@type": "OpeningHoursSpecification", "dayOfWeek": "Sunday", "opens": "10:00", "closes": "17:00"}]
    cid = int(B.GBP_FTID.split(":")[1], 16)
    node = {
        "@type": ["HVACBusiness", "LocalBusiness"], "@id": org_id(),
        "name": B.SITE_NAME, "legalName": B.LEGAL, "alternateName": ["EHI", B.LEGAL],
        "description": ("EHI Heating And Cooling is a licensed HVAC contractor based in Whitchurch-Stouffville, Ontario, serving homes and businesses "
                        "from the GTA to Northern Ontario for more than 20 years. Heat pump installation, furnace repair and replacement, air conditioning, "
                        "ductless mini splits, tankless water heaters, emergency HVAC service, Ontario heat pump rebates and HVAC financing."),
        "slogan": "Heating and cooling done right. Priced once. Backed for years.",
        "url": B.SITE + "/",
        "logo": {"@type": "ImageObject", "@id": B.SITE + "/#logo", "url": B.SITE + "/assets/img/ehi-logo.webp", "caption": B.SITE_NAME},
        "image": [B.SITE + "/assets/img/ehi-team.webp", B.SITE + "/assets/img/ehi-logo.webp"],
        "telephone": B.PHONE_TEL, "email": B.EMAIL,
        "address": {"@type": "PostalAddress", "streetAddress": B.ADDRESS["street"], "addressLocality": B.ADDRESS["city"],
                    "addressRegion": B.ADDRESS["region"], "postalCode": B.ADDRESS["postal"], "addressCountry": "CA"},
        "geo": {"@type": "GeoCoordinates", "latitude": B.GBP_LAT, "longitude": B.GBP_LNG},
        "hasMap": f"https://maps.google.com/?cid={cid}",
        "sameAs": [B.GBP_URL, f"https://maps.google.com/?cid={cid}"],
        "openingHoursSpecification": hours,
        "contactPoint": [{"@type": "ContactPoint", "contactType": "customer service", "telephone": B.PHONE_TEL, "email": B.EMAIL,
                          "areaServed": "CA-ON", "availableLanguage": "English", "hoursAvailable": hours},
                         {"@type": "ContactPoint", "contactType": "emergency HVAC service", "telephone": B.PHONE_TEL, "areaServed": "CA-ON",
                          "availableLanguage": "English", "description": "Emergency heating and cooling service evenings, weekends and holidays"}],
        "priceRange": "$$", "currenciesAccepted": "CAD",
        "naics": "238220",
        "knowsAbout": KEYWORDS,
        "keywords": ", ".join(KEYWORDS),
        "award": ["HomeStars Best Company 2019", "HomeStars Best Company 2020", "HomeStars Best Company 2021"],
        "brand": [{"@type": "Brand", "name": n} for n in ["Midea", "Lennox", "Kepler", "Rinnai"]],
        "areaServed": [city_place(c["slug"]) for c in B.CITIES] + [{"@type": "State", "name": "Ontario", "containedInPlace": {"@type": "Country", "name": "Canada"}}],
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "HVAC services in Ontario",
                            "itemListElement": [_offer(n, u, k) for n, u, k in CORE_SERVICES if u in B.REG]},
    }
    if B.GBP_RATING:
        node["aggregateRating"] = {"@type": "AggregateRating", "ratingValue": B.GBP_RATING[0], "reviewCount": B.GBP_RATING[1], "bestRating": "5", "worstRating": "1"}
    if reviews:
        node["review"] = [{"@type": "Review", "author": {"@type": "Person", "name": r.get("name", "Google reviewer")},
                           "reviewRating": {"@type": "Rating", "ratingValue": str(r.get("stars", 5)), "bestRating": "5", "worstRating": "1"},
                           "reviewBody": r["text"], "publisher": {"@type": "Organization", "name": "Google"},
                           **({"datePublished": B._review_date(r["date"])} if B._review_date(r.get("date")) else {})} for r in reviews]
    creds = ([f"TSSA contractor registration {B.TSSA_NUMBER}"] if B.TSSA_NUMBER else []) + ([f"ESA/ECRA licence {B.ESA_NUMBER}"] if B.ESA_NUMBER else [])
    if creds:
        node["hasCredential"] = [{"@type": "EducationalOccupationalCredential", "name": n} for n in creds]
    return node

def city_keywords(name):
    n = name
    return [f"HVAC {n}", f"HVAC contractor {n}", f"{n} HVAC contractor", f"HVAC company {n}", f"{n} HVAC companies", f"HVAC technician {n}",
            f"HVAC services {n}", f"heating and cooling {n}", f"furnace repair {n}", f"furnace installation {n}", f"heat pump installation {n}",
            f"AC repair {n}", f"air conditioning {n}", f"emergency HVAC {n}", f"ductless mini split {n}", f"heat pump rebate {n}"]

def city_catalog(slug):
    """Services offered in a city: the city's own service pages first, then province-wide pages."""
    c = B.CITY_BY_SLUG[slug]; n = c["name"]; area = {"@id": city_id(slug)}
    local = [(f"Heat pump installation in {n}", f"/{slug}/heat-pump-installation/", "heat_pump"),
             (f"Furnace repair in {n}", f"/{slug}/furnace-repair/", None),
             (f"AC repair in {n}", f"/{slug}/ac-repair/", None)]
    items = [(nm, u, k) for nm, u, k in local if u in B.REG]
    have = {nm.split(" in ")[0].lower() for nm, _, _ in items}
    general = [(f"Heat pump installation in {n}", "/heat-pump/cold-climate/", "heat_pump"), (f"Furnace repair in {n}", "/furnace/repair-maintenance/", None),
               (f"AC repair in {n}", "/ac/repair-maintenance/", None), (f"Furnace installation in {n}", "/furnace/high-efficiency/", "furnace"),
               (f"Ductless mini split installation in {n}", "/ac/ductless-mini-split/", None), (f"Emergency HVAC service in {n}", "/services/emergency-hvac/", None),
               (f"HVAC maintenance in {n}", "/services/hvac-repair-maintenance/", None), (f"Tankless water heater installation in {n}", "/water-heater/", "tankless"),
               (f"Heat pump rebate applications in {n}", "/heat-pump-rebates/", None)]
    items += [(nm, u, k) for nm, u, k in general if nm.split(" in ")[0].lower() not in have and u in B.REG]
    return {"@type": "OfferCatalog", "name": f"HVAC services in {n}", "itemListElement": [_offer(nm, u, k, area) for nm, u, k in items]}

PAGE_TYPES = {"/about-ehi/": "AboutPage", "/contact/": "ContactPage", "/reviews/": "WebPage", "/service-areas/": "CollectionPage",
              "/blog/": "CollectionPage", "/answers/": "FAQPage"}

def graph(page, canonical, crumbs_ld):
    url = page["url"]
    g = [business()]
    city_slug = page.get("city") or page.get("city_service")
    ptype = PAGE_TYPES.get(url, "WebPage")
    if ptype == "FAQPage" and page.get("faqs"): ptype = "WebPage"   # avoid two FAQPage nodes
    webpage = {"@type": ptype, "@id": canonical + "#webpage", "url": canonical, "name": page["title"], "description": page["description"],
               "isPartOf": {"@id": B.SITE + "/#website"}, "inLanguage": "en-CA", "dateModified": page.get("updated", B.TODAY),
               "publisher": {"@id": org_id()}, "about": [{"@id": org_id()}]}
    if crumbs_ld: webpage["breadcrumb"] = {"@id": canonical + "#breadcrumb"}
    img = page.get("hero_img") or page.get("hero_photo")
    if img: webpage["primaryImageOfPage"] = {"@type": "ImageObject", "url": B.SITE + img}
    if url == "/": webpage["mainEntity"] = {"@id": org_id()}
    g.append(webpage)
    g.append({"@type": "WebSite", "@id": B.SITE + "/#website", "url": B.SITE + "/", "name": B.SITE_NAME, "alternateName": ["EHI", B.LEGAL],
              "publisher": {"@id": org_id()}, "inLanguage": "en-CA"})
    if crumbs_ld:
        crumbs_ld = dict(crumbs_ld, **{"@id": canonical + "#breadcrumb"}); g.append(crumbs_ld)

    if page.get("city"):
        c = B.CITY_BY_SLUG[page["city"]]; n = c["name"]
        g.append(city_place(page["city"], full=True))
        webpage["about"].append({"@id": city_id(page["city"])})
        webpage["keywords"] = ", ".join(city_keywords(n))
        webpage["mainEntity"] = {"@id": canonical + "#service"}
        g.append({"@type": "Service", "@id": canonical + "#service", "name": f"HVAC services in {n}",
                  "alternateName": city_keywords(n)[:8],
                  "serviceType": ["HVAC contractor", "Heating and cooling", "Heat pump installation", "Furnace repair and installation",
                                  "Air conditioning repair and installation", "Emergency HVAC service"],
                  "description": page["description"], "url": canonical, "provider": {"@id": org_id()},
                  "areaServed": {"@id": city_id(page["city"])},
                  "availableChannel": {"@type": "ServiceChannel", "serviceUrl": canonical, "servicePhone": {"@type": "ContactPoint", "telephone": B.PHONE_TEL, "contactType": "customer service"}},
                  "hasOfferCatalog": city_catalog(page["city"]),
                  "audience": {"@type": "Audience", "audienceType": "Homeowners, landlords and businesses in " + n},
                  "brand": [{"@type": "Brand", "name": b} for b in ["Midea", "Lennox", "Kepler", "Rinnai"]],
                  "termsOfService": B.SITE + "/terms/"})
    elif page.get("city_service"):
        slug = page["city_service"]; n = B.CITY_BY_SLUG[slug]["name"]; s = page.get("service", {})
        kind = url.rstrip("/").split("/")[-1]
        kw = {"heat-pump-installation": ["heat pump installation", "heat pump installers", "cold climate heat pump", "heat pump rebate"],
              "furnace-repair": ["furnace repair", "furnace not heating", "emergency furnace repair", "furnace tune up"],
              "ac-repair": ["AC repair", "air conditioner repair", "AC not cooling", "emergency AC repair"]}.get(kind, [])
        g.append(city_place(slug, full=True))
        webpage["about"].append({"@id": city_id(slug)})
        webpage["keywords"] = ", ".join(f"{k} {n}" for k in kw)
        webpage["mainEntity"] = {"@id": canonical + "#service"}
        fk = {"heat-pump-installation": "heat_pump"}.get(kind)
        svc = {"@type": "Service", "@id": canonical + "#service", "name": s.get("name", re.sub("<[^>]+>", "", page["h1"])),
               "alternateName": [f"{k} {n}" for k in kw], "serviceType": s.get("type", kw[0] if kw else "HVAC service"),
               "description": page["description"], "url": canonical, "provider": {"@id": org_id()}, "areaServed": {"@id": city_id(slug)},
               "isRelatedTo": {"@type": "Service", "name": f"HVAC services in {n}", "url": f"{B.SITE}/{slug}/"},
               "availableChannel": {"@type": "ServiceChannel", "serviceUrl": canonical, "servicePhone": {"@type": "ContactPoint", "telephone": B.PHONE_TEL, "contactType": "customer service"}}}
        if fk: svc["offers"] = _offer(svc["name"], url, fk, {"@id": city_id(slug)})
        g.append(svc)
    elif page.get("service"):
        s = page["service"]
        svc = {"@type": "Service", "@id": canonical + "#service", "name": s["name"], "serviceType": s.get("type", s["name"]),
               "description": page["description"], "url": canonical, "provider": {"@id": org_id()},
               "areaServed": {"@type": "State", "name": "Ontario", "containedInPlace": {"@type": "Country", "name": "Canada"}},
               "availableChannel": {"@type": "ServiceChannel", "serviceUrl": canonical, "servicePhone": {"@type": "ContactPoint", "telephone": B.PHONE_TEL, "contactType": "customer service"}}}
        if s.get("from_price"):
            svc["offers"] = {"@type": "Offer", "priceCurrency": "CAD", "priceSpecification": {"@type": "PriceSpecification", "minPrice": str(s["from_price"]),
                             "priceCurrency": "CAD", "description": "Installed price from; varies by size and installation requirements"}}
        webpage["mainEntity"] = {"@id": canonical + "#service"}
        g.append(svc)
    if url == "/service-areas/":
        webpage["about"] += [city_place(c["slug"]) for c in B.CITIES if f'/{c["slug"]}/' in B.CITY_PAGES]

    if page.get("faqs"):
        g.append({"@type": "FAQPage", "@id": canonical + "#faq", "isPartOf": {"@id": canonical + "#webpage"}, "mainEntity": [
            {"@type": "Question", "name": re.sub("<[^>]+>", "", q), "acceptedAnswer": {"@type": "Answer", "text": re.sub("<[^>]+>", "", a)}} for q, a in page["faqs"]]})
    if page.get("guide"):
        gc = page.get("guide_city", "Ontario")
        gslug = next((c["slug"] for c in B.CITIES if c["name"] == gc), None)
        g.append({"@type": "Article", "@id": canonical + "#article", "headline": re.sub("<[^>]+>", "", page["h1"]), "description": page["description"],
                  "author": {"@id": org_id()}, "publisher": {"@id": org_id()}, "datePublished": page.get("published", B.TODAY),
                  "dateModified": page.get("updated", B.TODAY), "mainEntityOfPage": {"@id": canonical + "#webpage"}, "inLanguage": "en-CA",
                  "about": ({"@id": city_id(gslug)} if gslug else {"@type": "State", "name": "Ontario"}),
                  "keywords": f"HVAC companies {gc}, HVAC company {gc}, best HVAC company {gc}, HVAC contractor {gc}, how to choose an HVAC contractor"})
        if gslug: g.append(city_place(gslug, full=True))
    for extra in page.get("extra_ld", []):
        g.append(extra)
    return g
