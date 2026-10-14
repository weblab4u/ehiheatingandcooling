#!/usr/bin/env python3
"""Static site builder for EHI Heating & Cooling.
Usage: python3 build.py   -> writes ./site/
Each page lives in content/<name>.py and defines PAGE = {...} (see content/heat-pump.py for the exemplar).
"""
import os, re, json, glob, importlib.util, html, datetime, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "site")
SITE = "https://efficienthomeimprovements.ca"
BRAND = "EHI Heating & Cooling"
LEGAL = "Efficient Home Improvements"
PHONE = "1-647-694-5845"
PHONE_TEL = "+16476945845"
EMAIL = "efficienthomecomfort@gmail.com"
ADDRESS = {"street": "4261 Bloomington Road", "city": "Whitchurch-Stouffville", "region": "ON", "postal": "L4A 3Y6"}
TODAY = datetime.date.today().isoformat()
GBP_URL = "https://maps.app.goo.gl/hPDoCQ6tHRCjxoDd9"
GBP_LAT, GBP_LNG = "43.9919795", "-79.3224239"
GBP_RATING = ("4.5", "87")   # from the Google listing embed data; update when it changes
GBP_FTID = "0x882b2b96937f7999:0x4e1e3d096ab36ce7"
GBP_PLACE_ID = "ChIJmXl_k5YrK4gR52yzagk9Hk4"
GBP_REVIEWS_URL = f"https://search.google.com/local/reviews?placeid={GBP_PLACE_ID}"
GBP_WRITE_REVIEW_URL = f"https://search.google.com/local/writereview?placeid={GBP_PLACE_ID}"
MAP_EMBED = (f"https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2872.4!2d{GBP_LNG}!3d{GBP_LAT}!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1"
             f"!3m3!1m2!1s{GBP_FTID}!2sEfficient%20Home%20Improvements!5e0!3m2!1sen!2sca!4v1760300000000!5m2!1sen!2sca")
DIRECTIONS_URL = f"https://www.google.com/maps/dir/?api=1&destination={GBP_LAT},{GBP_LNG}"

# ---------------------------------------------------------------- registry
# url -> (nav title, short blurb used in related-service cards)
REG = {
 "/": ("Home", "HVAC contractor serving Ontario homes and businesses."),
 "/services/": ("All HVAC Services", "Every heating, cooling, water heating and air quality service we offer across Ontario."),
 "/services/hvac-installation-replacement/": ("HVAC Installation & Replacement", "Full system replacements: furnace, AC, heat pump or all three, sized right and installed in a day."),
 "/services/hvac-repair-maintenance/": ("HVAC Repair & Maintenance", "Diagnosis, honest repair quotes and tune-ups that keep your system out of trouble."),
 "/services/emergency-hvac/": ("Emergency HVAC Service", "No heat or no cooling? Same-day emergency furnace and AC repair across Ontario."),
 "/services/humidifiers/": ("Humidifiers", "Whole-home furnace humidifiers to fix dry winter air, static and cracked trim."),
 "/services/hrv-erv/": ("HRV & ERV Systems", "Fresh air ventilation for tight homes: installation, repair and cleaning."),
 "/services/thermostats/": ("Thermostats", "Smart and heat-pump-ready thermostat installation and replacement."),
 "/furnace/": ("Furnace Installation & Replacement", "High-efficiency Lennox and Midea gas furnaces, from $3,300 installed."),
 "/furnace/repair-maintenance/": ("Furnace Repair & Tune-Up", "Furnace not heating? Repairs, blower motors, ignitors and annual maintenance."),
 "/furnace/high-efficiency/": ("High-Efficiency Furnaces", "96% to 97% AFUE two-stage, variable-speed furnaces that cut gas bills."),
 "/furnace/electric-air-handlers/": ("Electric Furnaces & Air Handlers", "Electric heating and air handlers for homes without gas, or paired with a heat pump."),
 "/ac/": ("AC Installation & Replacement", "Central air conditioner installation and replacement, sized for Ontario summers."),
 "/ac/repair-maintenance/": ("AC Repair & Tune-Up", "AC not cooling, leaking or short cycling? Fast repair and seasonal maintenance."),
 "/ac/ductless-mini-split/": ("Ductless Mini-Split Installation", "Heat and cool rooms without ductwork: single-zone mini-split heat pumps."),
 "/ac/ductless-mini-split/repair/": ("Ductless Mini-Split Repair", "Mini-split repair, cleaning and maintenance for any brand."),
 "/ac/multi-zone-ductless-system/": ("Multi-Zone Ductless Systems", "One outdoor unit, up to five indoor heads, each room on its own thermostat."),
 "/heat-pump/": ("Heat Pump Installation", "Cold-climate heat pump installation with up to $7,500 in Ontario rebates."),
 "/heat-pump/repair-maintenance/": ("Heat Pump Repair & Maintenance", "Heat pump not heating or cooling? Repairs and tune-ups for every brand."),
 "/heat-pump/cold-climate/": ("Cold Climate Heat Pumps", "Heat pumps rated to -30°C that replace your furnace and AC in one."),
 "/heat-pump/central/": ("Ducted (Central) Heat Pumps", "Central heat pumps that use your existing ductwork to heat and cool the whole house."),
 "/heat-pump/hybrid-furnace-systems/": ("Hybrid Furnace + Heat Pump", "Dual-fuel systems: heat pump most of the year, gas furnace on the coldest nights."),
 "/heat-pump/electric-air-handler-systems/": ("Heat Pump + Electric Air Handler", "All-electric central heating and cooling for homes without gas."),
 "/water-heater/": ("Tankless Water Heater Installation", "Rinnai condensing tankless water heaters, endless hot water from $3,300."),
 "/water-heater/repair-maintenance/": ("Tankless Water Heater Repair", "Rinnai and other tankless repair, descaling flush and maintenance."),
 "/brands/": ("Brands We Install", "Authorized dealer for Midea, Lennox, Kepler and Rinnai."),
 "/brands/midea-heat-pumps/": ("Midea Heat Pumps", "Midea EVOX G3 and Extreme Hyper Heat cold-climate heat pumps, 2 to 5 ton."),
 "/brands/midea-ductless-mini-splits/": ("Midea Ductless Mini-Splits", "Midea Hyper Heat single-zone and multi-zone ductless systems."),
 "/brands/midea-furnace-air-handlers/": ("Midea Furnaces & Air Handlers", "Midea MGH96 furnaces and EVOX G3 electric air handlers."),
 "/brands/kepler-heat-pumps/": ("Kepler Heat Pumps", "Kepler cold-climate heat pumps built for Canadian winters."),
 "/brands/lennox-furnaces/": ("Lennox Furnaces", "Lennox ML296V and EL297V two-stage, variable-speed gas furnaces."),
 "/brands/lennox-air-conditioners/": ("Lennox Air Conditioners", "Lennox central air conditioners installed by an authorized dealer."),
 "/brands/lennox-heat-pumps/": ("Lennox Heat Pumps", "Lennox heat pumps and cold-climate options."),
 "/brands/rinnai-tankless-water-heaters/": ("Rinnai Tankless Water Heaters", "Rinnai RX160iN and RX199iN condensing tankless water heaters."),
 "/heat-pump-rebates/": ("Heat Pump Rebates Ontario", "Up to $7,500 through the Home Renovation Savings Program. We handle the paperwork."),
 "/financing/": ("HVAC Financing", "0% interest for 3, 6 or 9 months, or open loans from 2.99% OAC."),
 "/offers/": ("Offers", "Guaranteed final pricing and we may beat comparable quotes by up to 10%."),
 "/our-work/": ("Our Work", "Recent heat pump, furnace, AC and tankless installations across Ontario."),
 "/warranty/": ("Warranty", "Up to 12 years parts and labour on select systems."),
 "/about-ehi/": ("About EHI", "20+ years of HVAC experience, voted Best Company 2019 to 2021."),
 "/reviews/": ("Reviews", "What Ontario homeowners and business owners say about EHI."),
 "/blog/": ("Blog", "Heating, cooling and rebate guides for Ontario homeowners."),
 "/answers/": ("Your Questions Answered", "Straight answers to the HVAC questions Ontario homeowners and businesses ask us."),
 "/contact/": ("Contact / Get a Quote", "Call 1-647-694-5845 or request a free guaranteed quote."),
 "/service-areas/": ("Service Areas", "Where we work across Ontario."),
 "/privacy-policy/": ("Privacy Policy", ""),
 "/terms/": ("Terms of Service", ""),
}

TOP_NAV = [
 ("Home", "/", None),
 ("About EHI", "/about-ehi/", [("About EHI", ["/about-ehi/", "/our-work/", "/warranty/", "/offers/"])]),
 ("Reviews", "/reviews/", None),
 ("Service Areas", "/service-areas/", None),
 ("Resources", "/answers/", [("Resources", ["/answers/", "/blog/", "/financing/"])]),
]
NAV = [
 ("Services", "/services/", [("General HVAC", ["/services/", "/services/hvac-installation-replacement/", "/services/hvac-repair-maintenance/", "/services/emergency-hvac/"])]),
 ("Heat Pumps", "/heat-pump/", [("Heat Pumps", ["/heat-pump/", "/heat-pump/repair-maintenance/", "/heat-pump/cold-climate/", "/heat-pump/central/", "/heat-pump/hybrid-furnace-systems/", "/heat-pump/electric-air-handler-systems/"])]),
 ("Furnaces", "/furnace/", [("Furnaces", ["/furnace/", "/furnace/repair-maintenance/", "/furnace/high-efficiency/", "/furnace/electric-air-handlers/"])]),
 ("Air Conditioning", "/ac/", [("Air Conditioning", ["/ac/", "/ac/repair-maintenance/", "/ac/ductless-mini-split/", "/ac/ductless-mini-split/repair/", "/ac/multi-zone-ductless-system/"])]),
 ("Water Heaters", "/water-heater/", [("Tankless", ["/water-heater/", "/water-heater/repair-maintenance/"])]),
 ("Air Quality", "/services/humidifiers/", [("Air quality and controls", ["/services/humidifiers/", "/services/hrv-erv/", "/services/thermostats/"])]),
 ("Brands", "/brands/", [
   ("Midea", ["/brands/midea-heat-pumps/", "/brands/midea-ductless-mini-splits/", "/brands/midea-furnace-air-handlers/"]),
   ("Lennox", ["/brands/lennox-furnaces/", "/brands/lennox-air-conditioners/", "/brands/lennox-heat-pumps/"]),
   ("Kepler and Rinnai", ["/brands/kepler-heat-pumps/", "/brands/rinnai-tankless-water-heaters/"]),
 ]),
 ("Rebates & Financing", "/heat-pump-rebates/", [("Save money", ["/heat-pump-rebates/", "/financing/", "/offers/", "/warranty/"])]),
]

AREA_GROUPS = [
 ("Toronto and York Region", ["Toronto", "Scarborough", "North York", "Etobicoke", "East York", "Markham", "Richmond Hill", "Vaughan", "Thornhill", "Woodbridge", "Maple", "Aurora", "Newmarket", "King City", "Stouffville", "East Gwillimbury", "Georgina", "Keswick"]),
 ("Peel and Halton", ["Mississauga", "Brampton", "Caledon", "Bolton", "Oakville", "Burlington", "Milton", "Halton Hills", "Georgetown"]),
 ("Durham Region", ["Pickering", "Ajax", "Whitby", "Oshawa", "Clarington", "Bowmanville", "Courtice", "Uxbridge", "Port Perry", "Beaverton"]),
 ("Simcoe, Muskoka and cottage country", ["Barrie", "Innisfil", "Bradford", "Orillia", "Collingwood", "Wasaga Beach", "Midland", "Penetanguishene", "Alliston", "Angus", "Gravenhurst", "Bracebridge", "Huntsville", "Parry Sound"]),
 ("Hamilton and Niagara", ["Hamilton", "Stoney Creek", "Ancaster", "Dundas", "Grimsby", "St. Catharines", "Niagara Falls", "Welland", "Thorold", "Niagara-on-the-Lake", "Fort Erie", "Port Colborne"]),
 ("Southwestern Ontario", ["Kitchener", "Waterloo", "Cambridge", "Guelph", "Brantford", "Woodstock", "Stratford", "London", "St. Thomas", "Sarnia", "Chatham-Kent", "Windsor", "Leamington", "Tillsonburg", "Ingersoll", "Owen Sound"]),
 ("Eastern Ontario", ["Kingston", "Belleville", "Quinte West", "Cobourg", "Port Hope", "Peterborough", "Lindsay", "Kawartha Lakes", "Brockville", "Cornwall", "Ottawa", "Kanata", "Orleans", "Nepean", "Pembroke", "Petawawa", "Renfrew", "Arnprior"]),
 ("Northern Ontario", ["North Bay", "Sudbury", "Timmins", "Sault Ste. Marie", "Thunder Bay", "Elliot Lake", "Temiskaming Shores", "Kirkland Lake", "Kenora"]),
]
AREAS = ["Toronto", "Stouffville", "Markham", "Richmond Hill", "Vaughan", "Aurora", "Newmarket", "Brampton", "Mississauga",
         "Milton", "Oakville", "Ajax", "Pickering", "Whitby", "Oshawa", "Barrie", "Wasaga Beach", "Hamilton",
         "Kitchener-Waterloo", "London", "Sarnia", "Kingston", "Ottawa", "Pembroke", "North Bay", "Sudbury", "Timmins"]

# ---------------------------------------------------------------- helpers
def esc(s): return html.escape(str(s), quote=True)

def title_of(url): return REG[url][0]
def blurb_of(url): return REG[url][1]

def img_frame(desc, ratio="4/3", cls="", src=None, fit="contain", credit=None, eager=False, pos="50% 55%"):
    """Real image when src is given, otherwise a labelled placeholder frame to replace later."""
    if src:
        cap = f'<figcaption class="credit">{esc(credit)}</figcaption>' if credit else ""
        load = 'fetchpriority="high"' if eager else 'loading="lazy"'
        return (f'<figure class="img-real fit-{fit} {cls}" style="aspect-ratio:{ratio}"><img src="{src}" alt="{esc(desc)}" {load} decoding="async" style="object-position:{pos}">{cap}</figure>')
    return (f'<figure class="img-frame {cls}" style="aspect-ratio:{ratio}" role="img" aria-label="{esc(desc)}">'
            f'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 5h16a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1zm1 2v9l4.5-4.5L13 15l3-3 3 3V7H5zm12 2.5a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3z"/></svg>'
            f'<figcaption>Image: {esc(desc)}</figcaption></figure>')

ICONS = {
 # stroke icons, 24x24, drawn for this site. Keys are referenced by content files.
 "heatpump": '<rect x="3" y="5" width="18" height="14" rx="2"/><circle cx="10" cy="12" r="4"/><path d="M10 9.5v5M7.5 12h5M17.5 9v6"/>',
 "furnace": '<rect x="5" y="3" width="14" height="18" rx="2"/><path d="M9 7h6M12 10.5c.4 2 2.5 2.8 2.5 5a2.5 2.5 0 0 1-5 0c0-1.2.6-2 1.2-2.6.2.7.6 1.1 1.3 1.4-.3-1.4-.2-2.6 0-3.8z"/>',
 "flame": '<path d="M12 2.5c.5 3.5 4.5 5 4.5 10a4.5 4.5 0 0 1-9 0c0-2 1-3.5 2-4.5.3 1.2 1 2 2 2.5-.5-3 0-5.5.5-8z"/><path d="M12 21.5v-2"/>',
 "snow": '<path d="M12 2v20M3.3 7l17.4 10M20.7 7 3.3 17M12 2l-2.5 2.5M12 2l2.5 2.5M12 22l-2.5-2.5M12 22l2.5-2.5M3.3 7l3.4.5M3.3 7 4 10.4M20.7 17l-3.4-.5M20.7 17 20 13.6"/>',
 "ac": '<rect x="2" y="5" width="20" height="11" rx="2"/><path d="M6 9h12M6 12.5h12M8 19l-1 2.5M12 19v2.5M16 19l1 2.5"/>',
 "ductless": '<rect x="2" y="6" width="20" height="9" rx="2"/><path d="M5 12h14M5 9h3M7 18l-1 3M12 18v3M17 18l1 3"/>',
 "multizone": '<rect x="2" y="4" width="9" height="6" rx="1.5"/><rect x="13" y="4" width="9" height="6" rx="1.5"/><rect x="2" y="14" width="9" height="6" rx="1.5"/><path d="M15 17h5M17.5 14.5v5"/>',
 "wrench": '<path d="M14.5 5.5a4.5 4.5 0 0 1 5.6 5.6l-8.4 8.4a2 2 0 0 1-2.8-2.8l8.4-8.4"/><path d="M14.5 5.5 18 9M4.5 19.5l.1.1"/>',
 "bolt": '<path d="M13 2 4 14h7l-1 8 9-12h-7z"/>',
 "water": '<path d="M12 3s6 6.5 6 11a6 6 0 0 1-12 0c0-4.5 6-11 6-11z"/><path d="M9.5 14a2.5 2.5 0 0 0 2 2.5"/>',
 "tankless": '<rect x="7" y="3" width="10" height="14" rx="2"/><path d="M10 7h4M12 10c.3 1.2 1.5 1.7 1.5 3a1.5 1.5 0 0 1-3 0c0-1 .8-1.6 1.5-3zM9 17v2a3 3 0 0 0 3 3 3 3 0 0 0 3-3v-2"/>',
 "air": '<path d="M3 8h10.5a2.5 2.5 0 1 0-2.5-2.5M3 12h15a3 3 0 1 1-3 3M3 16h7a2.5 2.5 0 1 1-2.5 2.5"/>',
 "humidity": '<path d="M12 3s6 6.5 6 11a6 6 0 0 1-12 0c0-4.5 6-11 6-11z"/><path d="M8 15c1.3-1 2.7-1 4 0s2.7 1 4 0"/>',
 "hrv": '<path d="M4 8h14l-3-3M20 16H6l3 3"/><path d="M4 4v16M20 4v16"/>',
 "thermostat": '<circle cx="12" cy="12" r="9"/><path d="M8 14.5a4.5 4.5 0 1 1 8 0M12 12V9"/>',
 "install": '<path d="M3 11.5 12 4l9 7.5M5.5 10v10h13V10"/><path d="M12 12.5v5M9.5 15h5"/>',
 "house": '<path d="M3 11.5 12 4l9 7.5M5.5 10v10h13V10"/><path d="M10 20v-5h4v5"/>',
 "dollar": '<circle cx="12" cy="12" r="9"/><path d="M12 6.5v11M14.8 9.3c-.2-1.1-1.3-1.8-2.8-1.8-1.6 0-2.8.8-2.8 2 0 2.6 5.6 1.4 5.6 4 0 1.3-1.2 2.1-2.8 2.1-1.7 0-2.9-.8-3-2"/>',
 "percent": '<circle cx="12" cy="12" r="9"/><path d="M8.5 15.5l7-7"/><circle cx="9" cy="9" r="1.2"/><circle cx="15" cy="15" r="1.2"/>',
 "rebate": '<path d="M3 6.5A1.5 1.5 0 0 1 4.5 5h15A1.5 1.5 0 0 1 21 6.5V9a2 2 0 0 0 0 4v2.5a1.5 1.5 0 0 1-1.5 1.5h-15A1.5 1.5 0 0 1 3 15.5V13a2 2 0 0 0 0-4z"/><path d="M9 9.5l6 5M9 14.5l6-5"/>',
 "shield": '<path d="M12 3l7 3v5c0 5-3.5 8.5-7 10-3.5-1.5-7-5-7-10V6z"/><path d="M9 12l2 2 4-4"/>',
 "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
 "calendar": '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4M8 14h3M13 14h3M8 17.5h3"/>',
 "leaf": '<path d="M4 20c0-9 5.5-14.5 16-15.5C19 15 13.5 20.5 4 20z"/><path d="M4 20c3-5 7-8.5 12-11.5"/>',
 "check": '<path d="M5 12.5l4.5 4.5L19 7"/>',
 "phone": '<path d="M5 4h3l2 5-2.5 1.5a11 11 0 0 0 6 6L15 14l5 2v3a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/>',
 "pin": '<path d="M12 21s-7-6.5-7-12a7 7 0 0 1 14 0c0 5.5-7 12-7 12z"/><circle cx="12" cy="9" r="2.5"/>',
 "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
 "chat": '<path d="M4 5h16v11H9l-5 4z"/><path d="M8 9h8M8 12h5"/>',
 "truck": '<path d="M3 7h11v9H3zM14 10h4l3 3v3h-7z"/><circle cx="7" cy="18" r="1.8"/><circle cx="17" cy="18" r="1.8"/>',
 "clipboard": '<rect x="5" y="4" width="14" height="17" rx="2"/><path d="M9 4V3h6v1M9 11l2 2 4-4M9 16.5h6"/>',
 "gauge": '<path d="M4 16a8 8 0 1 1 16 0"/><path d="M12 16l4-5M12 16h.01"/>',
 "noise": '<path d="M4 10v4h3l5 4V6l-5 4z"/><path d="M15 9.5a3.5 3.5 0 0 1 0 5M17.5 7a7 7 0 0 1 0 10"/>',
 "alert": '<path d="M12 3 2.5 19.5h19z"/><path d="M12 10v4M12 17h.01"/>',
 "plug": '<path d="M9 3v5M15 3v5M6 8h12v3a6 6 0 0 1-12 0zM12 17v4"/>',
 "duct": '<path d="M3 6h8a4 4 0 0 1 4 4v8h6"/><path d="M3 9h8a1 1 0 0 1 1 1v8h9"/>',
 "tag": '<path d="M3 12V4h8l9 9-8 8z"/><circle cx="7.5" cy="8.5" r="1.3"/>',
 "star": '<path class="fill" d="M12 3l2.8 5.7 6.2.9-4.5 4.4 1.1 6.2L12 17.3 6.4 20.2l1.1-6.2L3 9.6l6.2-.9z"/>',
}

def icon(name):
    if name not in ICONS: raise KeyError(f"unknown icon {name}")
    return f'<svg class="ic" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</svg>'

def fill_cta(n, cols=(4,2), tag="li", h="Not sure which option fits your home?", text="Tell us about your house and we'll recommend the right system, with a guaranteed price and your rebate estimate."):
    """CTA card that occupies the leftover cells of a grid. cols = (desktop columns, tablet columns)."""
    cd, ct = cols
    rd, rt = (-n) % cd, (-n) % ct
    return (f'<{tag} class="fill-cta d{cd}-{rd} t{ct}-{rt}"><div><h3>{h}</h3><p>{text}</p></div>'
            f'<div class="btn-group small"><a class="btn btn-primary" href="/contact/">Get a Free Quote{icon("arrow")}</a>'
            f'<a class="btn btn-secondary" href="tel:{PHONE_TEL}">{icon("phone")}Call {PHONE}</a></div></{tag}>')

def cta_buttons(primary="Get a Free Quote", secondary=True, small=False):
    cls = "btn-group small" if small else "btn-group"
    s = f'<div class="{cls}"><a class="btn btn-primary" href="/contact/">{esc(primary)}{icon("arrow")}</a>'
    if secondary:
        s += f'<a class="btn btn-secondary" href="tel:{PHONE_TEL}">{icon("phone")}Call {PHONE}</a>'
    return s + '</div>'

# ---------------------------------------------------------------- chrome
def nav_items(nav):
    items = []
    for label, href, cols in nav:
        if cols:
            colhtml = ""
            for colname, urls in cols:
                links = "".join(f'<li><a href="{u}">{esc(title_of(u))}</a></li>' for u in urls)
                colhtml += f'<div class="mega-col"><h4>{esc(colname)}</h4><ul>{links}</ul></div>'
            items.append(f'<li class="has-mega"><a href="{href}" aria-haspopup="true" aria-expanded="false">{esc(label)}<span class="chev"></span></a>'
                         f'<div class="mega">{colhtml}</div></li>')
        else:
            items.append(f'<li><a href="{href}">{esc(label)}</a></li>')
    return "".join(items)

def header():
    return f'''<a class="skip" href="#main">Skip to content</a>
<div class="topbar"><div class="wrap">
  <span>{icon("pin")} Serving homes and businesses across Ontario</span>
  <span class="topbar-right"><span>{icon("clock")} Mon to Sat 8 am to 8 pm, Sun 10 am to 5 pm</span>
  <a href="tel:{PHONE_TEL}">{icon("phone")} {PHONE}</a></span>
</div></div>
<header class="site-header" id="top">
 <div class="wrap top-row">
  <a class="logo" href="/" aria-label="{esc(BRAND)} home"><img src="/assets/img/ehi-logo.webp" alt="{esc(BRAND)} logo" width="160" height="80"></a>
  <nav class="top-nav" aria-label="Company"><ul>{nav_items(TOP_NAV)}</ul></nav>
  <div class="header-cta">
    <a class="emerg" href="/services/emergency-hvac/">{icon("phone")}<span><small>Emergency?</small><strong>Book here</strong></span></a>
    <a class="btn btn-service" href="/services/emergency-hvac/">I Need Service</a>
    <a class="btn btn-quote" href="/contact/">Contact Us</a>
  </div>
  <a class="btn btn-call mob-call" href="tel:{PHONE_TEL}" aria-label="Call {PHONE}">{icon("phone")}</a>
  <button class="nav-toggle" aria-label="Open menu" aria-expanded="false" aria-controls="mobile-nav"><span></span><span></span><span></span></button>
 </div>
 <div class="main-bar"><nav class="main-nav wrap" aria-label="Services"><ul>{nav_items(NAV)}</ul></nav></div>
</header>'''

def footer(show_cta=True):
    svc = "".join(f'<li><a href="{u}">{esc(title_of(u))}</a></li>' for u in
                  ["/heat-pump/", "/furnace/", "/ac/", "/ac/ductless-mini-split/", "/water-heater/", "/services/emergency-hvac/", "/services/hvac-repair-maintenance/", "/services/"])
    co = "".join(f'<li><a href="{u}">{esc(title_of(u))}</a></li>' for u in
                 ["/about-ehi/", "/reviews/", "/heat-pump-rebates/", "/financing/", "/offers/", "/warranty/", "/brands/", "/answers/", "/blog/", "/contact/"])
    areas = ", ".join(f'<a href="/service-areas/">{a}</a>' if i == 0 else a for i, a in enumerate(AREAS))
    cta = f'''<section class="final-cta" aria-labelledby="final-cta-h"><div class="wrap">
  <div><h2 id="final-cta-h">Ready for a guaranteed quote?</h2>
  <p>Home or business, tell us what's going on with your heating, cooling or hot water. We'll size it right, price it once, and show you every rebate you qualify for.</p></div>
  {cta_buttons("Request My Free Quote")}
</div></section>''' if show_cta else ""
    return f'''{cta}
<footer class="site-footer"><div class="wrap grid-4">
  <div class="f-brand">
    <img src="/assets/img/ehi-logo.webp" alt="{esc(BRAND)}" width="180" height="90" loading="lazy">
    <p><strong>{esc(BRAND)}</strong> ({esc(LEGAL)}) is a licensed residential and commercial HVAC contractor with 20+ years of experience. Authorized dealer for Midea, Lennox, Kepler and Rinnai.</p>
    <p><a href="tel:{PHONE_TEL}">{PHONE}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a><br>{ADDRESS["street"]}, {ADDRESS["city"]}, {ADDRESS["region"]} {ADDRESS["postal"]}</p>
    <img class="badge" src="/assets/img/homestars-verified.webp" alt="HomeStars Verified badge" width="90" height="90" loading="lazy">
  </div>
  <div><h3>Services</h3><ul>{svc}</ul></div>
  <div><h3>Company</h3><ul>{co}</ul></div>
  <div><h3>Service Areas</h3><p class="areas">{areas} and surrounding communities.</p>
    <h3>Hours</h3><p>Monday to Saturday, 8:00 am to 8:00 pm<br>Sunday, 10:00 am to 5:00 pm<br>Emergency service evenings, weekends and holidays</p></div>
</div>
<div class="wrap foot-bottom"><p>&copy; {datetime.date.today().year} {esc(LEGAL)}. All rights reserved. <a href="/privacy-policy/">Privacy Policy</a> · <a href="/terms/">Terms</a> · <a href="/sitemap.xml">Sitemap</a></p>
<p class="small">Rebate amounts and eligibility are set by the Home Renovation Savings Program and can change. This website is not operated by any government program. Financing on approved credit.</p></div>
</footer>
<div class="sticky-cta" aria-hidden="false">
  <a class="btn btn-call" href="tel:{PHONE_TEL}">{icon("phone")}Call Now</a>
  <a class="btn btn-primary" href="/contact/">Free Quote</a>
</div>
<nav id="mobile-nav" class="mobile-nav" aria-label="Mobile" hidden><button class="m-close" type="button" aria-label="Close menu">Close &#10005;</button>{mobile_nav()}</nav>
<script src="/assets/js/main.js?v={ASSET_V['js']}" defer></script>'''

def mobile_nav():
    out = []
    for label, href, cols in NAV + TOP_NAV:
        if cols:
            inner = ""
            for colname, urls in cols:
                inner += f'<p class="m-col">{esc(colname)}</p><ul>' + "".join(f'<li><a href="{u}">{esc(title_of(u))}</a></li>' for u in urls) + '</ul>'
            out.append(f'<details><summary>{esc(label)}</summary><a class="m-all" href="{href}">All {esc(label)}</a>{inner}</details>')
        else:
            out.append(f'<a class="m-top" href="{href}">{esc(label)}</a>')
    out.append(f'<a class="btn btn-primary" href="/contact/">Get a Free Quote</a><a class="btn btn-secondary" href="tel:{PHONE_TEL}">Call {PHONE}</a>')
    return "".join(out)

def breadcrumbs(url):
    parts = [p for p in url.split("/") if p]
    crumbs = [("/", "Home")]
    acc = ""
    for p in parts:
        acc += "/" + p
        u = acc + "/"
        if u in REG:
            crumbs.append((u, title_of(u)))
    # heat-pump-rebates etc live under none; fine.
    if len(crumbs) < 2: return "", ""
    lis = "".join(
        (f'<li><a href="{u}">{esc(t)}</a></li>' if i < len(crumbs) - 1 else f'<li aria-current="page">{esc(t)}</li>')
        for i, (u, t) in enumerate(crumbs))
    ld = {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": t, "item": SITE + u} for i, (u, t) in enumerate(crumbs)]}
    return f'<nav class="crumbs" aria-label="Breadcrumb"><div class="wrap"><ol>{lis}</ol></div></nav>', ld

# ---------------------------------------------------------------- blocks
def h2(b, default=""):
    t = b.get("h2", default)
    return f'<h2>{t}</h2>' if t else ""

def lead(b):
    return f'<p class="lead">{b["lead"]}</p>' if b.get("lead") else ""

def render_block(b, page):
    t = b["type"]
    if t == "text":
        return f'<section class="sec text"><div class="wrap narrow">{h2(b)}{b["html"]}</div></section>'
    if t == "problems":
        items = "".join(f'<li class="prob"><h3>{i["problem"]}</h3><p>{i["solution"]}</p></li>' for i in b["items"])
        items += fill_cta(len(b["items"]), (3, 2), "li", "Sound familiar?", "Describe the problem and we'll tell you what it usually is, what it costs to fix, and whether it's worth fixing.")
        return f'<section class="sec problems"><div class="wrap">{h2(b, "Problems we fix")}{lead(b)}<ul class="prob-grid">{items}</ul></div></section>'
    if t == "cards":
        items = ""
        for i in b["items"]:
            link = f'<a class="more" href="{i["link"]}">{esc(i.get("link_text","Learn more"))}{icon("arrow")}</a>' if i.get("link") else ""
            ic = f'<span class="card-icon">{icon(i["icon"])}</span>' if i.get("icon") else ""
            items += f'<article class="card">{ic}<h3>{i["title"]}</h3><p>{i["text"]}</p>{link}</article>'
        if not b.get("no_fill"): items += fill_cta(len(b["items"]), (4, 2), "div")
        return f'<section class="sec cards-sec {b.get("cls","")}"><div class="wrap">{h2(b)}{lead(b)}<div class="cards">{items}</div></div></section>'
    if t == "checklist":
        items = "".join(f'<li>{icon("check")}<span>{i}</span></li>' for i in b["items"])
        img = img_frame(b["image"], src=b.get("image_src"), fit=b.get("image_fit", "contain"), credit=b.get("image_credit"), pos=b.get("image_pos", "50% 55%")) if b.get("image") else ""
        inner = f'<div class="split"><div>{h2(b)}{lead(b)}<ul class="checklist">{items}</ul></div>{img}</div>' if img else f'{h2(b)}{lead(b)}<ul class="checklist cols">{items}</ul>'
        return f'<section class="sec checklist-sec"><div class="wrap">{inner}</div></section>'
    if t == "steps":
        items = "".join(f'<li><span class="num">{n+1}</span><div><h3>{i["title"]}</h3><p>{i["text"]}</p></div></li>' for n, i in enumerate(b["items"]))
        return f'<section class="sec steps-sec"><div class="wrap"><div class="steps-head"><div>{h2(b, "How it works")}{lead(b)}</div>{cta_buttons(b.get("cta","Start With a Free Quote"), small=True)}</div><ol class="steps n{len(b["items"])}">{items}</ol></div></section>'
    if t == "split":
        img = img_frame(b.get("image", "Photo"), src=b.get("image_src"), fit=b.get("image_fit", "contain"), credit=b.get("image_credit"), pos=b.get("image_pos", "50% 55%"))
        rev = " reverse" if b.get("reverse") else ""
        body = re.sub(r'<ul class="checklist">(.*?)</ul>', lambda m: '<ul class="checklist">' + re.sub(r'<li>(?!<svg)', '<li>' + icon("check") + '<span>', m.group(1)).replace('</li>', '</span></li>') + '</ul>', b["html"], flags=re.S)
        return f'<section class="sec split-sec"><div class="wrap split{rev}"><div>{h2(b)}{body}</div>{img}</div></section>'
    if t == "table":
        head = "".join(f"<th>{h}</th>" for h in b["headers"])
        rows = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in b["rows"])
        note = f'<p class="note">{b["note"]}</p>' if b.get("note") else ""
        return f'<section class="sec table-sec"><div class="wrap narrow">{h2(b)}{lead(b)}<div class="table-wrap"><table><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table></div>{note}</div></section>'
    if t == "money":
        return money_block(b)
    if t == "cta":
        return (f'<section class="sec cta-band"><div class="wrap"><div><h2>{b.get("h2","Want a guaranteed price for your home?")}</h2>'
                f'<p>{b.get("text","Free quote, honest sizing, and every rebate you qualify for.")}</p></div>{cta_buttons(b.get("primary","Get a Free Quote"))}</div></section>')
    if t == "image":
        return f'<section class="sec img-sec"><div class="wrap">{img_frame(b["desc"], b.get("ratio","21/9"))}</div></section>'
    if t == "gallery":
        items = "".join(f'<figure class="work">{img_frame(i["image"], "4/3", src=i.get("src"), fit="cover", pos=i.get("pos", "50% 55%"))}<figcaption><span class="work-tag">{i["tag"]}</span><h3>{i["title"]}</h3><p>{i["meta"]}</p></figcaption></figure>' for i in b["items"])
        return f'<section class="sec gallery-sec"><div class="wrap">{h2(b)}{lead(b)}<div class="work-grid">{items}</div></div></section>'
    if t == "gbp":
        return gbp_block(b)
    if t == "g_reviews":
        return g_reviews_block(b)
    if t == "testimonials":
        return testimonials_block(b)
    if t == "svc_cards":
        cards = "".join(f'<a class="svc-card" href="{u}"><span class="card-icon">{icon(ic)}</span><h3>{esc(title)}</h3><p>{esc(txt)}</p></a>' for ic, title, txt, u in b["items"])
        return f'<section class="sec svc-cards-sec"><div class="wrap"><h2 class="center">{b["h2"]}</h2><div class="svc-cards">{cards}</div></div></section>'
    if t == "type_lists":
        cols = "".join(f'<div><h3>{esc(g)}</h3><ul class="type-list">' + "".join(f'<li>{icon("check")}<a href="{u}">{esc(title_of(u) if not lbl else lbl)}</a></li>' for u, lbl in links) + '</ul></div>' for g, links in b["groups"])
        img = img_frame(b["image"], "4/5", src=b.get("image_src"), fit="cover", credit=b.get("image_credit"), pos=b.get("image_pos", "50% 55%"))
        return f'<section class="sec type-lists-sec"><div class="wrap split"><div><h2>{b["h2"]}</h2><div class="type-cols">{cols}</div></div>{img}</div></section>'
    if t == "locations_cta":
        pins = "".join(f'<li>{icon("pin")}{esc(c)}</li>' for g, cities in AREA_GROUPS for c in cities[:6])
        return (f'<section class="sec loc-cta-sec"><div class="wrap loc-cta"><div><h2>{b["h2"]}</h2><p class="lead">{b["lead"]}</p><ul class="pin-list">{pins}</ul>'
                f'<p><a class="more" href="/service-areas/">See every city we serve{icon("arrow")}</a></p></div>'
                f'<aside class="quote-card"><h3>{b["cta_h"]}</h3><p>{b["cta_text"]}</p>{cta_buttons("Get a Fast Quote", small=True)}'
                f'{img_frame(b["image"], "4/3", src=b.get("image_src"), fit="cover", pos=b.get("image_pos","50% 40%"))}</aside></div></section>')
    if t == "linkgrid":
        cols = ""
        for g in b["groups"]:
            links = "".join(f'<li><a href="{u}">{icon("arrow")}{esc(g.get("labels", {}).get(u, title_of(u)))}</a></li>' for u in g["urls"])
            head = f'<a href="{g["href"]}">{g["title"]}</a>' if g.get("href") else g["title"]
            cols += f'<div class="lg-col"><h3><span class="card-icon">{icon(g["icon"])}</span>{head}</h3><ul>{links}</ul></div>'
        return f'<section class="sec linkgrid-sec {b.get("cls","")}"><div class="wrap">{h2(b)}{lead(b)}<div class="lg-grid">{cols}</div></div></section>'
    if t == "promo":
        return (f'<section class="promo"><div class="wrap"><div class="promo-card">{img_frame(b["image"], "4/3", "promo-img", src=b.get("image_src"), fit="cover", credit=b.get("image_credit"), pos=b.get("image_pos", "50% 60%"))}'
                f'<div class="promo-body"><h2><span class="hl">{b["h2_hl"]}</span> {b["h2"]}</h2><p>{b["text"]}</p>'
                f'<div class="btn-group small"><a class="btn btn-primary" href="{b.get("href","/contact/")}">{b.get("button","Get Pre-Approved")}{icon("arrow")}</a>'
                f'<a class="btn btn-secondary" href="{b.get("href2","/heat-pump-rebates/")}">{b.get("button2","How the rebate works")}</a></div></div></div></div></section>')
    if t == "stats":
        items = "".join(f'<li><strong>{i["value"]}</strong><span>{i["label"]}</span></li>' for i in b["items"])
        return f'<section class="sec stats"><div class="wrap"><ul>{items}</ul></div></section>'
    if t == "html":
        return b["html"]
    if t == "why":
        return why_block()
    if t == "areas":
        return areas_block()
    if t == "brands":
        return brands_block()
    if t == "reviews":
        return reviews_block()
    if t == "faq":
        return faq_block(b["items"], b.get("h2", "Frequently asked questions"))
    if t == "form":
        return form_block(b)
    raise ValueError(f"unknown block {t}")

def money_block(b):
    cols = b.get("items") or [
        {"icon": "dollar", "title": "Guaranteed pricing", "text": "Your quote is your final price. No surprise extras on the agreed scope of work."},
        {"icon": "leaf", "title": "Rebates up to $7,500", "text": 'Cold-climate heat pumps may qualify through the <a href="/heat-pump-rebates/">Home Renovation Savings Program</a>. We confirm eligibility and file the paperwork.'},
        {"icon": "clock", "title": "0% financing", "text": '<a href="/financing/">Interest-free for 3, 6 or 9 months</a>, or open loans from 2.99% on approved credit.'},
        {"icon": "shield", "title": "Up to 12 years parts and labour", "text": '<a href="/warranty/">Extended warranty</a> on select systems when registered.'},
    ]
    items = "".join(f'<li><span class="card-icon">{icon(c["icon"])}</span><h3>{c["title"]}</h3><p>{c["text"]}</p></li>' for c in cols)
    items += fill_cta(len(cols), (4, 2), "li", "Want the real number for your home?", "A guaranteed quote takes one visit. Rebate and financing options come with it.")
    return f'<section class="sec money"><div class="wrap">{h2(b, "What it costs, and how we keep it lower")}{lead(b)}<ul class="money-grid">{items}</ul></div></section>'

def why_block():
    items = [
        ("shield", "20+ years in Ontario homes", "We've installed through more January cold snaps and July heat waves than we can count. That experience shows up in the sizing, the ductwork and the little details."),
        ("star", "Voted Best Company 2019 to 2021", "HomeStars Verified. Our reviews come from real Ontario homeowners and business owners."),
        ("check", "Authorized Midea, Lennox, Kepler and Rinnai dealer", "Factory-backed equipment, factory-backed warranties, and techs trained on the gear we install."),
        ("dollar", "Guaranteed final pricing", "The number on your quote is the number on your invoice. We may also beat comparable reputable quotes by up to 10%."),
        ("leaf", "Rebate paperwork handled", "Pre-approval, heat-loss calculation and documentation for the Home Renovation Savings Program. You just sign."),
        ("wrench", "Licensed, certified crews", "TSSA-certified gas technicians, licensed refrigeration techs and ESA-licensed electrical work on every job."),
    ]
    lis = "".join(f'<li><span class="card-icon">{icon(i)}</span><h3>{t}</h3><p>{d}</p></li>' for i, t, d in items)
    lis += fill_cta(len(items), (4, 2), "li", "Ready when you are", "Call us or send the form. Quotes are free, guaranteed and come with your rebate estimate.")
    return f'<section class="sec why" id="why-ehi"><div class="wrap"><h2>Why Ontario homes and businesses choose EHI Heating &amp; Cooling</h2><ul class="why-grid">{lis}</ul></div></section>'

def areas_block():
    cols = "".join(f'<div class="area-col"><h3>{icon("pin")}{g}</h3><ul>' + "".join(f'<li>{c}</li>' for c in cities) + '</ul></div>' for g, cities in AREA_GROUPS)
    return (f'<section class="sec areas-sec"><div class="wrap"><div class="areas-head"><div><h2>HVAC service across Ontario</h2>'
            f'<p class="lead">We\'re a service-area business. Our crews come to your home or business, from the GTA to Northern Ontario. Don\'t see your town? Call, we probably cover it.</p></div>'
            f'{cta_buttons("Check My Area", small=True)}</div>'
            f'<div class="area-cols">{cols}</div><p><a class="more" href="/service-areas/">See all service areas{icon("arrow")}</a></p></div></section>')

def brands_block():
    bl = [("Midea", "/brands/midea-heat-pumps/", "midea"), ("Lennox", "/brands/lennox-furnaces/", "lennox"), ("Kepler", "/brands/kepler-heat-pumps/", "kepler"), ("Rinnai", "/brands/rinnai-tankless-water-heaters/", "rinnai")]
    items = "".join(brand_logo_card(n, u, f) for n, u, f in bl)
    return f'<section class="sec brands-sec"><div class="wrap"><h2>Brands we\'re authorized to sell, install and service</h2><ul class="brand-grid">{items}</ul></div></section>'

def map_iframe(h=380):
    return (f'<div class="map-wrap"><iframe src="{MAP_EMBED}" width="100%" height="{h}" style="border:0" loading="lazy" allowfullscreen '
            f'referrerpolicy="no-referrer-when-downgrade" title="Map showing EHI Heating and Cooling (Efficient Home Improvements) in Whitchurch-Stouffville, Ontario"></iframe></div>')

def gbp_block(b=None):
    b = b or {}
    hours = "".join(f'<li><span>{d}</span><span>8:00 am to 8:00 pm</span></li>' for d in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]) + '<li><span>Sunday</span><span>10:00 am to 5:00 pm</span></li>'
    rating = (f'<p class="gbp-rating"><span class="stars" aria-hidden="true">{icon("star")*5}</span><strong>{GBP_RATING[0]}</strong>&nbsp;on Google · <a href="{GBP_REVIEWS_URL}" target="_blank" rel="noopener">Read reviews</a> · <a href="{GBP_WRITE_REVIEW_URL}" target="_blank" rel="noopener">Write a review</a></p>') if GBP_RATING else \
             f'<p class="gbp-rating"><span class="stars" aria-hidden="true">{icon("star")*5}</span>Rated on Google. <a href="{GBP_URL}" target="_blank" rel="noopener">Read our Google reviews</a></p>'
    return f'''<section class="sec gbp-sec"><div class="wrap">
  <h2>{b.get("h2", "Find EHI Heating &amp; Cooling on Google")}</h2>
  <p class="lead">{b.get("lead", "Verified business listing, office location and hours. We come to your home or business anywhere in our Ontario service area.")}</p>
  <div class="gbp-grid">
    <div class="gbp-info">
      <h3>{esc(LEGAL)} <span class="small">(EHI Heating &amp; Cooling)</span></h3>
      {rating}
      <ul class="gbp-list">
        <li>{icon("phone")}<span><strong>Phone</strong><br><a href="tel:{PHONE_TEL}">{PHONE}</a></span></li>
        <li>{icon("chat")}<span><strong>Email</strong><br><a href="mailto:{EMAIL}">{EMAIL}</a></span></li>
        <li>{icon("truck")}<span><strong>Service area</strong><br>All of Ontario. <a href="/service-areas/">See the cities we serve</a></span></li>
      </ul>
      <h4>{icon("clock")} Hours</h4>
      <ul class="gbp-hours">{hours}</ul>
      <p class="small">Emergency service available outside these hours.</p>
      <ul class="gbp-list gbp-office">
        <li>{icon("pin")}<span><strong>Office</strong><br>{ADDRESS["street"]}, {ADDRESS["city"]}, {ADDRESS["region"]} {ADDRESS["postal"]}</span></li>
      </ul>
      <div class="btn-group small">
        <a class="btn btn-primary" href="{DIRECTIONS_URL}" target="_blank" rel="noopener">Get Directions{icon("arrow")}</a>
        <a class="btn btn-secondary" href="{GBP_URL}" target="_blank" rel="noopener">View on Google Maps</a>
      </div>
    </div>
    {map_iframe(b.get("height", 520))}
  </div>
</div></section>'''

import importlib.util as _ilu
def _load_gallery():
    path = os.path.join(ROOT, "data", "gallery.py")
    spec = _ilu.spec_from_file_location("ehi_gallery", path); m = _ilu.module_from_spec(spec); spec.loader.exec_module(m)
    return m.P, m.GALLERY
GALLERY_PHOTOS, SERVICE_GALLERIES = _load_gallery()

GALLERY_ALLOC = {}

def allocate_galleries(pages):
    """Hand out job photos to every service gallery: least-used first across the whole site,
    counting photos already used in page sections, and never repeating a photo within a page."""
    usage = {k: 0 for k in GALLERY_PHOTOS}
    per_page = {}
    for pg in pages:
        txt = repr(pg)
        used = {k for k in GALLERY_PHOTOS if f"/assets/img/work/{k}.webp" in txt}
        per_page[pg["url"]] = used
        for k in used: usage[k] += 1
    order = [pg["url"] for pg in pages if pg["url"] in SERVICE_GALLERIES]
    for url in order:
        heading, spec = SERVICE_GALLERIES[url]
        chosen = []
        for cat, n in spec:
            pool = [k for k, (c, _) in GALLERY_PHOTOS.items() if c == cat and k not in per_page[url] and k not in chosen
                    and os.path.exists(os.path.join(ROOT, "assets", "img", "work", k + ".webp"))]
            pool.sort(key=lambda k: (usage[k], list(GALLERY_PHOTOS).index(k)))
            for k in pool[:n]:
                chosen.append(k); usage[k] += 1
        GALLERY_ALLOC[url] = chosen
    return usage

def service_gallery(url):
    g = SERVICE_GALLERIES.get(url)
    keys = GALLERY_ALLOC.get(url, [])
    if not g or not keys:
        return ""
    heading = g[0]
    arrow = icon("arrow")
    cards = "".join(
        f'<figure class="sg-card"><button type="button" class="sg-open" data-full="/assets/img/work/{k}.webp" data-alt="{esc(GALLERY_PHOTOS[k][1])}" aria-label="Enlarge photo: {esc(GALLERY_PHOTOS[k][1])}">'
        f'<img src="/assets/img/work/{k}.webp" alt="{esc(GALLERY_PHOTOS[k][1])}" loading="lazy" decoding="async"><span class="sg-zoom" aria-hidden="true">{icon("arrow")}</span></button>'
        f'<figcaption>{esc(GALLERY_PHOTOS[k][1])}</figcaption></figure>' for k in keys)
    nav = (f'<div class="sg-nav"><button class="sg-prev" type="button" aria-label="Previous photos">{arrow}</button>'
           f'<button class="sg-next" type="button" aria-label="Next photos">{arrow}</button></div>') if len(keys) > 4 else ""
    return (f'<section class="sec gallery-strip"><div class="wrap"><div class="sg-head"><div><p class="sg-kicker">Our work · {len(keys)} photos</p><h2>{esc(heading)}</h2>'
            f'<p class="lead">Real jobs by our licensed crews in Ontario homes. Tap a photo to see it full size.</p></div>'
            f'<div class="sg-actions">{nav}<a class="more" href="/our-work/">See all our work{arrow}</a></div></div>'
            f'<div class="sg-rail" data-gallery><div class="sg-track count-{len(keys)}">{cards}</div></div></div></section>')

def partners_strip():
    logos = ""
    for name, file in [("Midea", "midea"), ("Lennox", "lennox"), ("Kepler", "kepler"), ("Rinnai", "rinnai")]:
        path = os.path.join(ROOT, "assets", "img", f"{file}.webp")
        logos += (f'<li class="p-{file}"><img src="/assets/img/{file}.webp" alt="{name}" loading="lazy" width="160" height="56"></li>' if os.path.exists(path)
                  else f'<li class="p-{file}"><span class="wordmark">{name}</span></li>')
    return (f'<section class="partners" aria-label="Our brand partners"><div class="wrap">'
            f'<h2 class="partners-label"><span>Our Brand Partners</span></h2>'
            f'<ul class="partners-logos">{logos}</ul></div></section>')

def brand_logo_card(name, url, file):
    path = os.path.join(ROOT, "assets", "img", f"{file}.webp")
    if os.path.exists(path):
        lg = f'<span class="brand-logo"><img src="/assets/img/{file}.webp" alt="{name} logo" loading="lazy" width="200" height="70"></span>'
    else:
        lg = f'<span class="brand-logo wordmark" role="img" aria-label="{name} logo">{name}</span>'
    return f'<li><a href="{url}">{lg}<span>Authorized {name} dealer</span></a></li>'

def load_reviews():
    path = os.path.join(ROOT, "data", "reviews.json")
    try:
        return [r for r in json.load(open(path, encoding="utf-8")).get("reviews", []) if r.get("text")]
    except (OSError, ValueError):
        return []

def google_g():
    return ('<svg class="g-logo" viewBox="0 0 48 48" aria-hidden="true"><path fill="#EA4335" d="M24 9.5c3.5 0 6.6 1.2 9 3.6l6.7-6.7C35.6 2.4 30.2 0 24 0 14.6 0 6.6 5.4 2.7 13.3l7.8 6C12.4 13.7 17.7 9.5 24 9.5z"/>'
            '<path fill="#4285F4" d="M46.5 24.5c0-1.6-.1-3.1-.4-4.5H24v8.5h12.7c-.6 3-2.3 5.5-4.8 7.2l7.5 5.8c4.4-4 7.1-10 7.1-17z"/>'
            '<path fill="#FBBC05" d="M10.5 28.7c-.5-1.4-.8-3-.8-4.7s.3-3.2.8-4.7l-7.8-6C1 16.6 0 20.2 0 24s1 7.4 2.7 10.7l7.8-6z"/>'
            '<path fill="#34A853" d="M24 48c6.5 0 11.9-2.1 15.9-5.8l-7.5-5.8c-2.1 1.4-4.8 2.3-8.4 2.3-6.3 0-11.6-4.2-13.5-10l-7.8 6C6.6 42.6 14.6 48 24 48z"/></svg>')

def reviews_block():
    """Google rating panel plus real reviews from data/reviews.json (never placeholder text)."""
    rating, count = GBP_RATING if GBP_RATING else ("", "")
    stars = icon("star") * 5
    panel = (f'<div class="g-panel">{google_g()}<div class="g-score"><strong>{rating}</strong><span class="stars" aria-hidden="true">{stars}</span>'
             f'<span class="g-count">Google rating from verified customers</span></div>'
             f'<div class="btn-group small"><a class="btn btn-primary" href="{GBP_REVIEWS_URL}" target="_blank" rel="noopener">Read our Google reviews{icon("arrow")}</a>'
             f'<a class="btn btn-secondary" href="{GBP_WRITE_REVIEW_URL}" target="_blank" rel="noopener">Write a review</a></div></div>')
    revs = [r for r in load_reviews() if not r.get("reviews_page_only")]
    cards = "".join(review_card(r, i, "rv-slide") for i, r in enumerate(revs[:12]))
    grid = (f'<div class="rv-carousel" data-carousel><button class="rv-nav prev" type="button" aria-label="Previous reviews">{icon("arrow")}</button>'
            f'<div class="rv-track" tabindex="0">{cards}</div><button class="rv-nav next" type="button" aria-label="Next reviews">{icon("arrow")}</button></div>') if cards else ""
    return (f'<section class="sec reviews-sec"><div class="wrap"><h2>What our customers say</h2>'
            f'<p class="lead">Rated {rating} on Google and voted Best Company 2019, 2020 and 2021 on HomeStars.</p>{panel}{grid}'
            f'<p><a class="more" href="{GBP_REVIEWS_URL}" target="_blank" rel="noopener">See all our Google reviews{icon("arrow")}</a></p></div></section>')

AVATAR_COLOURS = ["#138A36", "#0B5FA8", "#C8322B", "#7B4BB7", "#E07B00", "#0E7A6F"]

def review_card(r, i, cls="review"):
    n = max(1, min(5, int(r.get("stars", 5))))
    name = r.get("name", "Google reviewer")
    initial = esc(name[:1].upper())
    when = esc(r.get("date", ""))
    meta = " · ".join(esc(x) for x in [r.get("city"), r.get("service")] if x)
    return (f'<article class="{cls}"><header class="rv-head"><span class="rv-avatar" style="background:{AVATAR_COLOURS[i % len(AVATAR_COLOURS)]}">{initial}</span>'
            f'<span class="rv-who"><strong>{esc(name)}</strong><span>{when}</span></span>{google_g()}</header>'
            f'<p class="stars" aria-label="{n} star rating">{icon("star")*n}</p><blockquote>{esc(r["text"])}</blockquote>'
            + (f'<p class="meta">{meta}</p>' if meta else "") + '</article>')

def g_reviews_block(b):
    rating = GBP_RATING[0] if GBP_RATING else ""
    summary = (f'<aside class="g-summary"><img src="/assets/img/ehi-icon.png" alt="EHI Heating and Cooling" width="56" height="56">'
               f'<a class="g-name" href="{GBP_REVIEWS_URL}" target="_blank" rel="noopener">EHI Heating &amp; Cooling (Efficient Home Improvements)</a>'
               f'<p class="g-rate"><strong>{rating}</strong><span class="stars" aria-hidden="true">{icon("star")*5}</span></p>'
               f'<p class="g-powered">Powered by {google_g()} Google</p>'
               f'<a class="btn btn-primary" href="{GBP_WRITE_REVIEW_URL}" target="_blank" rel="noopener">Review us on Google</a>'
               f'<a class="more" href="{GBP_REVIEWS_URL}" target="_blank" rel="noopener">Read all reviews{icon("arrow")}</a></aside>')
    revs = [r for r in load_reviews() if not r.get("best")] or load_reviews()
    if revs:
        cards = "".join(review_card(r, i, "rv-slide") for i, r in enumerate(revs[:12]))
        right = (f'<div class="rv-carousel" data-carousel><button class="rv-nav prev" type="button" aria-label="Previous reviews">{icon("arrow")}</button>'
                 f'<div class="rv-track" tabindex="0">{cards}</div><button class="rv-nav next" type="button" aria-label="Next reviews">{icon("arrow")}</button></div>')
    else:
        right = f'<div class="rv-live">{map_iframe(380)}</div>'
    return f'<section class="sec g-reviews-sec"><div class="wrap"><h2 class="center">{b.get("h2","Latest Reviews on Google")}</h2><div class="g-reviews">{summary}{right}</div></div></section>'

def testimonials_block(b):
    revs = [r for r in load_reviews() if r.get("best")] or load_reviews()
    if not revs:
        return ""
    cards = "".join(review_card(r, i, "testimonial") for i, r in enumerate(revs))
    return f'<section class="sec testimonials-sec"><div class="wrap"><h2 class="center">{b.get("h2","All-Time Best Reviews From Our Customers")}</h2><div class="testimonial-grid">{cards}</div></div></section>'

def faq_block(items, heading="Frequently asked questions"):
    lis = "".join(f'<details class="faq"><summary><h3>{q}</h3></summary><div class="faq-a">{a if a.strip().startswith("<") else "<p>"+a+"</p>"}</div></details>' for q, a in items)
    return f'<section class="sec faq-sec" id="faq"><div class="wrap narrow"><h2>{heading}</h2>{lis}</div></section>'

def related_block(urls):
    if not urls: return ""
    cards = "".join(f'<a class="card rel" href="{u}"><h3>{esc(title_of(u))}</h3><p>{esc(blurb_of(u))}</p><span class="more">View service{icon("arrow")}</span></a>' for u in urls)
    cards += fill_cta(len(urls), (4, 2), "div", "Need something else?", "If you don't see it here, call us. We'll point you to the right service or the right person.")
    return f'<section class="sec related"><div class="wrap"><h2>Related services</h2><div class="cards">{cards}</div></div></section>'

import hashlib
GA_ID = "G-V5HRT0TJDR"
GTAG = f'''<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());

  gtag('config', '{GA_ID}');
</script>'''
# cache-busting versions: change whenever the file content changes
ASSET_V = {k: hashlib.md5(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", f)).read().encode()).hexdigest()[:8]
           for k, f in (("js", "js/main.js"), ("css", "css/style.css"))}

SERVICE_OPTIONS = ["Heat pump installation", "Furnace installation or replacement", "AC installation or replacement", "Ductless mini-split",
                   "Tankless water heater", "Repair (furnace, AC or heat pump)", "Emergency, no heat or no cooling", "Maintenance / tune-up",
                   "Humidifier, HRV/ERV or thermostat", "Rebate eligibility check", "Commercial HVAC (office, retail, warehouse, multi-unit)", "Something else"]

SERVICE_PREFIXES = ("/services/", "/furnace/", "/ac/", "/heat-pump/", "/water-heater/")
def preselect_for(url):
    rules = [("/services/emergency-hvac/", "Emergency, no heat or no cooling"), ("repair-maintenance", "Repair (furnace, AC or heat pump)"), ("/repair/", "Repair (furnace, AC or heat pump)"),
             ("/services/humidifiers/", "Humidifier, HRV/ERV or thermostat"), ("/services/hrv-erv/", "Humidifier, HRV/ERV or thermostat"), ("/services/thermostats/", "Humidifier, HRV/ERV or thermostat"),
             ("/water-heater/", "Tankless water heater"), ("ductless", "Ductless mini-split"), ("/heat-pump", "Heat pump installation"), ("/furnace/", "Furnace installation or replacement"), ("/ac/", "AC installation or replacement")]
    for k, v in rules:
        if k in url: return v
    return None

def form_block(b=None, compact=False, preselect=None):
    b = b or {}
    opts = "".join(f'<option{" selected" if o == preselect else ""}>{o}</option>' for o in SERVICE_OPTIONS)
    cls = "quote-form compact" if compact else "quote-form"
    return f'''<form class="{cls}" action="/api/quote.php" method="post" data-quote-form novalidate>
  <h3>{b.get("h3","Get your free guaranteed quote")}</h3>
  <p class="form-sub">{b.get("sub","We reply fast during business hours. No pressure, no spam.")}</p>
  <div class="f-row"><label>Name<input type="text" name="name" autocomplete="name" required></label>
  <label>Phone<input type="tel" name="phone" autocomplete="tel" inputmode="tel" required></label></div>
  <div class="f-row"><label>Email<input type="email" name="email" autocomplete="email"></label>
  <label>City<input type="text" name="city" autocomplete="address-level2" placeholder="e.g. Markham" required></label></div>
  <label>What do you need?<select name="service">{opts}</select></label>
  <label>Tell us a bit more (optional)<textarea name="message" rows="3" placeholder="e.g. 15-year-old furnace, 2,000 sq ft, want to look at a heat pump and the rebate"></textarea></label>
  <input type="text" name="company" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
  <input type="hidden" name="page" value="">
  <button class="btn btn-primary btn-block" type="submit">{b.get("button","Request My Free Quote")}{icon("arrow")}</button>
  <p class="form-note">Or call <a href="tel:{PHONE_TEL}">{PHONE}</a>. By submitting you agree to our <a href="/privacy-policy/">privacy policy</a>.</p>
  <p class="form-ok" hidden role="status">Thanks, we got it. We'll be in touch shortly.</p>
  <p class="form-err" hidden role="alert"></p>
</form>'''

# ---------------------------------------------------------------- page
def photo_hero(page):
    pts = "".join(f'<li>{icon("check")}{p}</li>' for p in page.get("hero_points", []))
    rating = GBP_RATING[0] if GBP_RATING else ""
    badge = (f'<a class="hh-badge" href="{GBP_REVIEWS_URL}" target="_blank" rel="noopener">{google_g()}'
             f'<span><strong>{rating}</strong><span class="stars" aria-hidden="true">{icon("star")*5}</span><small>Google rating</small></span></a>') if rating else ""
    return f'''<section class="hero home-hero">
  <div class="wrap hh-grid">
    <div class="hero-copy">
      <p class="kicker">{page.get("kicker","")}</p>
      <h1><span class="l1">{page["h1_line1"]}</span> <span class="l2">{page["h1_line2"]}</span></h1>
      <p class="sub">{page["intro"]}</p>
      <div class="btn-group"><a class="btn btn-call big" href="tel:{PHONE_TEL}">{icon("phone")}Call Today: {PHONE}</a><a class="btn btn-primary big" href="/contact/">Get a Free Quote{icon("arrow")}</a></div>
      <ul class="hero-points two">{pts}</ul>
    </div>
    <div class="hh-visual">
      <picture><source media="(max-width:767px)" srcset="/assets/img/ehi-team-mobile.webp"><img class="hh-photo" src="{page["hero_photo"]}" alt="{esc(page.get("hero_photo_alt","The EHI Heating and Cooling team"))}" width="1800" height="982" fetchpriority="high"></picture>
      {badge}
    </div>
  </div>
</section>'''

def hero(page):
    if page.get("hero_photo"): return photo_hero(page)
    pts = "".join(f'<li>{icon("check")}{p}</li>' for p in page.get("hero_points", []))
    eyebrow = f'<p class="eyebrow">{page["eyebrow"]}</p>' if page.get("eyebrow") else ""
    for b in ("midea", "lennox", "rinnai", "kepler"):
        if page["url"].startswith(f"/brands/{b}") and os.path.exists(os.path.join(ROOT, "assets", "img", f"{b}.webp")):
            eyebrow = f'<img class="hero-brand" src="/assets/img/{b}.webp" alt="{b.title()} logo" width="180" height="60">' + eyebrow
    is_service = page["url"].startswith(SERVICE_PREFIXES) and page["url"] != "/services/"
    use_form = page.get("hero_form", is_service)
    right = form_block({"h3": page.get("form_h3", "Get your free guaranteed quote"), "sub": page.get("form_sub", "Same-day reply in most cases. No pressure, no spam.")}, compact=True, preselect=preselect_for(page["url"])) if use_form else img_frame(page.get("hero_image", "Hero photo"), "4/3", "hero-img", src=page.get("hero_img"), fit=page.get("hero_img_fit", "contain"), credit=page.get("hero_img_credit"), eager=True, pos=page.get("hero_img_pos", "50% 55%"))
    cls = page.get("hero_cls", "svc-hero" if is_service else ("page-hero" if page["url"] != "/" else ""))
    return f'''<section class="hero {cls}"><div class="wrap hero-grid">
  <div class="hero-copy">{eyebrow}<h1>{page["h1"]}</h1>{f'<p class="tagline">{page["tagline"]}</p>' if page.get("tagline") else ""}{page["intro"]}
    <ul class="hero-points">{pts}</ul>{cta_buttons(page.get("cta_primary","Get a Free Quote"))}
    <p class="hero-trust">{icon("star")} Voted Best Company 2019 to 2021 · Authorized Midea, Lennox, Kepler &amp; Rinnai dealer · 20+ years</p>
  </div>
  <div class="hero-side">{right}</div>
</div></section>'''

def local_business_ld():
    return {
        "@type": "HVACBusiness", "@id": SITE + "/#organization", "name": BRAND, "alternateName": LEGAL,
        "url": SITE + "/", "logo": SITE + "/assets/img/ehi-logo.webp", "image": SITE + "/assets/img/ehi-logo.webp",
        "telephone": PHONE_TEL, "email": EMAIL, "priceRange": "$$",
        "address": {"@type": "PostalAddress", "streetAddress": ADDRESS["street"], "addressLocality": ADDRESS["city"],
                    "addressRegion": ADDRESS["region"], "postalCode": ADDRESS["postal"], "addressCountry": "CA"},
        "areaServed": [{"@type": "City", "name": a + ", ON"} for a in AREAS] + [{"@type": "State", "name": "Ontario"}],
        "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], "opens": "08:00", "closes": "20:00"},
                                      {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Sunday"], "opens": "10:00", "closes": "17:00"}],
        "brand": [{"@type": "Brand", "name": n} for n in ["Midea", "Lennox", "Kepler", "Rinnai"]],
        "knowsAbout": ["Cold climate heat pumps", "Furnace installation", "Air conditioning", "Ductless mini-splits", "Tankless water heaters", "Ontario heat pump rebates", "Commercial HVAC"],
        "description": "Residential and commercial HVAC contractor in Ontario: heat pumps, furnaces, air conditioning, ductless, tankless water heaters, rebates and financing.",
        "sameAs": [GBP_URL],
        "hasMap": GBP_URL,
        "geo": {"@type": "GeoCoordinates", "latitude": GBP_LAT, "longitude": GBP_LNG},
    }

VARIANT_TYPES = {"problems": 0, "cards": 1, "checklist": 2, "steps": 0, "table": 1, "money": 2, "why": 1, "faq": 2, "split": 0, "linkgrid": 1}
def page_seed(url):
    return sum((i + 1) * ord(c) for i, c in enumerate(url))

DARK = {"problems": {2}, "checklist": {2}, "steps": {2}, "money": {1}, "why": {0, 2}, "cta": {0, 1, 2}}

def pick_variant(btype, page, prev_dark):
    if page["url"] == "/" or btype not in VARIANT_TYPES or page.get("no_variants"):
        return 0
    v = (page_seed(page["url"]) + VARIANT_TYPES[btype] * 7 + len(btype)) % 3
    if prev_dark:
        for k in range(3):
            cand = (v + k) % 3
            if cand not in DARK.get(btype, set()):
                return cand
    return v

def with_variant(html_out, btype, page, prev_dark=False):
    """Tag a section with v0/v1/v2 so pages mix section designs. Homepage stays v0. Never stacks two dark bands."""
    if btype == "cta":
        if prev_dark:
            return html_out.replace('class="sec cta-band"', 'class="sec cta-band cta-light"', 1), False
        return html_out, True
    v = pick_variant(btype, page, prev_dark)
    return html_out.replace('class="sec ', f'class="sec v{v} ', 1), (v in DARK.get(btype, set()))

def render(page):
    url = page["url"]
    canonical = SITE + url
    crumbs_html, crumbs_ld = breadcrumbs(url)
    article = page.get("layout") == "article"
    if article:
        body = (f'<article class="legal"><div class="wrap narrow"><header class="legal-head"><h1>{page["h1"]}</h1>'
                f'<p class="legal-meta">{page.get("meta_line", "Last updated " + datetime.date.today().strftime("%B %Y"))}</p>{page["intro"]}</header>'
                + "".join(b["html"] for b in page.get("blocks", []) if b["type"] == "text") + '</div></article>')
        blocks = []
    elif page.get("banner"):
        body = (f'<section class="banner-hero"><div class="wrap"><h1>{page["h1"]}</h1><p>{page["intro"]}</p>'
                f'{cta_buttons(page.get("cta_primary","Get a Free Quote"))}</div></section>')
        blocks = list(page.get("blocks", []))
    else:
        body = hero(page) if page.get("h1") else ""
        blocks = list(page.get("blocks", []))
    has_brand_grid = any(b.get("type") == "brands" for b in page.get("blocks", []))
    strip = "" if page.get("no_partners") or not page.get("h1") or article or has_brand_grid or page.get("banner") else partners_strip()
    if strip and blocks and blocks[0].get("type") == "promo":
        body += render_block(blocks.pop(0), page)
    body += strip
    prev_dark = False
    gal = service_gallery(page["url"]) if not page.get("no_gallery") else ""
    mid = len(blocks) // 2
    for i, b in enumerate(blocks):
        if gal and i == mid:
            body += gal; prev_dark = False
        out, prev_dark = with_variant(render_block(b, page), b["type"], page, prev_dark)
        body += out
    if page["url"].startswith(SERVICE_PREFIXES) and page["url"] != "/services/" and not page.get("no_gbp"):
        body += gbp_block({"h2": "Serving Ontario from our Stouffville office", "lead": "Find us on Google, get directions, or check our hours. Our crews travel to your home or business across the province."})
    if page.get("faqs"):
        body += with_variant(faq_block(page["faqs"], page.get("faq_h2", "Frequently asked questions")), "faq", page)[0]
    body += related_block(page.get("related", []))

    graph = [local_business_ld()]
    graph.append({"@type": "WebPage", "@id": canonical + "#webpage", "url": canonical, "name": page["title"],
                  "description": page["description"], "isPartOf": {"@id": SITE + "/#website"}, "inLanguage": "en-CA",
                  "dateModified": TODAY, "about": {"@id": SITE + "/#organization"}})
    graph.append({"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": BRAND, "publisher": {"@id": SITE + "/#organization"}})
    if crumbs_ld: graph.append(crumbs_ld)
    if page.get("service"):
        s = page["service"]
        graph.append({"@type": "Service", "name": s["name"], "serviceType": s.get("type", s["name"]), "provider": {"@id": SITE + "/#organization"},
                      "areaServed": {"@type": "State", "name": "Ontario"}, "url": canonical, "description": page["description"],
                      **({"offers": {"@type": "Offer", "priceCurrency": "CAD", "price": s["from_price"], "priceSpecification": {"@type": "PriceSpecification", "minPrice": s["from_price"], "priceCurrency": "CAD"}, "description": "Installed price starting from, varies by size and installation"}} if s.get("from_price") else {})})
    if page.get("faqs"):
        graph.append({"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": re.sub("<[^>]+>", "", q), "acceptedAnswer": {"@type": "Answer", "text": re.sub("<[^>]+>", "", a)}} for q, a in page["faqs"]]})
    for extra in page.get("extra_ld", []):
        graph.append(extra)
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)

    return f'''<!DOCTYPE html>
<html lang="en-CA">
<head>
<meta charset="utf-8">
{GTAG}
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(page["title"])}</title>
<meta name="description" content="{esc(page["description"])}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="{page.get("robots","index, follow, max-image-preview:large")}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{esc(BRAND)}">
<meta property="og:title" content="{esc(page["title"])}">
<meta property="og:description" content="{esc(page["description"])}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE}/assets/img/ehi-logo.webp">
<meta property="og:locale" content="en_CA">
<meta name="twitter:card" content="summary_large_image">
<meta name="geo.region" content="CA-ON">
<meta name="geo.placename" content="Ontario">
<meta name="theme-color" content="#0B5FA8">
<link rel="icon" href="/assets/img/ehi-icon.png" type="image/png">
<link rel="apple-touch-icon" href="/assets/img/ehi-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap">
<link rel="stylesheet" href="/assets/css/style.css?v={ASSET_V['css']}">
<script type="application/ld+json">{ld}</script>
</head>
<body class="{page.get("body_cls","")}">
{header()}
{crumbs_html}
<main id="main">
{body}
</main>
{footer(show_cta=not page.get('layout') == 'article')}
</body>
</html>'''

# ---------------------------------------------------------------- lint
BANNED = ["meticulous", "navigating", "complexities", "realm", "bespoke", "tailored", "towards", "underpins", "ever changing", "ever-evolving",
          "the world of", "not only", "seeking more than just", "designed to enhance", "it's not merely", "it’s not merely", "our suite", "it is advisable",
          "daunting", "in the heart of", "when it comes to", "in the realm of", "amongst", "unlock the secrets", "unveil the secrets", "robust",
          "elevate", "seamless", "leverage", "delve", "cutting-edge", "state-of-the-art", "game-changer", "look no further", "rest assured",
          "top-notch", "hassle-free", "in conclusion", "furthermore", "moreover", "additionally"]
LIMIT3 = ["unique", "ensure", "utmost"]

def lint(url, html_out):
    text = re.sub(r"<script.*?</script>", "", html_out, flags=re.S)
    text = re.sub(r"<blockquote>.*?</blockquote>", "", text, flags=re.S)  # customer reviews stay verbatim
    text = re.sub(r"<[^>]+>", " ", text)
    # strip shared chrome noise is overkill; chrome is lint-clean by construction
    probs = []
    if "—" in text or "–" in text: probs.append("dash")
    low = text.lower()
    for w in BANNED:
        if re.search(r"\b" + re.escape(w) + r"\b", low): probs.append(f"banned:{w}")
    for w in LIMIT3:
        n = len(re.findall(r"\b" + w + r"\b", low))
        if n >= 3: probs.append(f"{w}x{n}")
    n_ex = text.count("!")
    if n_ex > 1: probs.append(f"exclaim:{n_ex}")
    return probs

# ---------------------------------------------------------------- main
def load_pages():
    pages = []
    for f in sorted(glob.glob(os.path.join(ROOT, "content", "*.py"))):
        spec = importlib.util.spec_from_file_location(os.path.basename(f)[:-3], f)
        m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
        if hasattr(m, "PAGE"): pages.append(m.PAGE)
        if hasattr(m, "PAGES"): pages.extend(m.PAGES)
    return pages

# Old efficienthomeimprovements.ca (GoDaddy builder) URLs. The new site is HVAC only,
# so the non-HVAC pages (doors and windows, renovations, decks, insulation) go to the homepage.
OLD_REDIRECTS = [
    ("about-us", "/about-ehi/"), ("contact-us-1", "/contact/"), ("rebates", "/heat-pump-rebates/"),
    ("payment-plans", "/financing/"), ("tankless-water-heaters", "/water-heater/"),
    ("heating-&-cooling", "/services/"), ("commercial", "/"),
    ("luxury-doors-&-windows", "/"), ("home-renovations", "/"), ("custom-design-decks", "/"), ("insulation/air-sealing", "/"),
]
HTACCESS = "\n".join([
    "ErrorDocument 404 /404.html", "Options -Indexes", "RewriteEngine On",
    "# One address: https://efficienthomeimprovements.ca (the temporary Hostinger address is left alone)",
    r"RewriteCond %{HTTP_HOST} ^www\.efficienthomeimprovements\.ca$ [NC]",
    "RewriteRule ^(.*)$ https://efficienthomeimprovements.ca/$1 [R=301,L]",
    r"RewriteCond %{HTTP_HOST} ^efficienthomeimprovements\.ca$ [NC]",
    "RewriteCond %{HTTPS} !=on",
    "RewriteCond %{HTTP:X-Forwarded-Proto} !https",
    "RewriteRule ^(.*)$ https://efficienthomeimprovements.ca/$1 [R=301,L]",
    "# Old site URLs",
] + [f"RewriteRule ^{re.escape(a).replace(chr(92)+'-', '-')}/?$ {b} [NC,L,R=301]" for a, b in OLD_REDIRECTS] + [""])

def main():
    if os.path.exists(OUT): shutil.rmtree(OUT)
    os.makedirs(OUT)
    shutil.copytree(os.path.join(ROOT, "assets"), os.path.join(OUT, "assets"))
    pages = load_pages()
    photo_usage = allocate_galleries(pages)
    urls = []
    issues = {}
    for p in pages:
        url = p["url"]
        if url not in REG: print("WARN not in registry:", url)
        out = render(p)
        d = os.path.join(OUT, url.strip("/"))
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as fh: fh.write(out)
        if p.get("robots", "").startswith("noindex") is False or "noindex" not in p.get("robots", ""):
            urls.append((url, p.get("priority", "0.7")))
        pr = lint(url, out)
        if pr: issues[url] = pr
        tl = len(p["title"]); dl = len(p["description"])
        if tl > 62 or dl > 158: print(f"META  {url}: title {tl} chars, description {dl} chars")
    # sitemap
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u, pr in urls:
        sm.append(f"<url><loc>{SITE}{u}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority></url>")
    sm.append("</urlset>")
    open(os.path.join(OUT, "sitemap.xml"), "w").write("\n".join(sm))
    open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
    shutil.copytree(os.path.join(ROOT, "server"), OUT, dirs_exist_ok=True)
    open(os.path.join(OUT, ".htaccess"), "w").write(HTACCESS)
    # thank-you page (non-JS form fallback, conversion tracking target)
    os.makedirs(os.path.join(OUT, "thank-you"), exist_ok=True)
    open(os.path.join(OUT, "thank-you", "index.html"), "w", encoding="utf-8").write(render({
        "url": "/thank-you/", "title": "Thanks, We Got Your Request", "description": "Your quote request is in. We reply fast during business hours.",
        "robots": "noindex, follow", "h1": "Thanks, we got your request", "intro": f"<p>We'll call you back shortly during business hours. Need help sooner? Call <a href=\"tel:{PHONE_TEL}\">{PHONE}</a>.</p>",
        "hero_points": [], "hero_image": "The EHI Heating and Cooling team in front of two EHI service vans", "hero_img": "/assets/img/ehi-team.webp", "hero_img_fit": "cover", "hero_img_pos": "50% 40%",
        "blocks": [{"type": "cards", "items": [{"title": t, "text": b, "link": u} for u, (t, b) in REG.items() if u in ("/heat-pump-rebates/", "/financing/", "/reviews/", "/our-work/")]}]}))
    # 404
    open(os.path.join(OUT, "404.html"), "w", encoding="utf-8").write(render({
        "url": "/404/", "title": "Page Not Found", "description": "That page moved or never existed. Find HVAC services, rebates and contact info here.",
        "robots": "noindex, follow", "h1": "Hmm, that page isn't here", "intro": "<p>The link may be old, or the page moved. Here's where most people are headed.</p>",
        "hero_points": [], "hero_image": "The EHI Heating and Cooling team in front of two EHI service vans", "hero_img": "/assets/img/ehi-team.webp", "hero_img_fit": "cover", "hero_img_pos": "50% 40%",
        "blocks": [{"type": "cards", "items": [{"title": t, "text": b, "link": u} for u, (t, b) in REG.items() if u in ("/heat-pump/", "/furnace/", "/ac/", "/services/emergency-hvac/", "/heat-pump-rebates/", "/contact/")]}]}))
    print(f"Built {len(pages)} pages -> {OUT}")
    reused = sorted(((v, k) for k, v in photo_usage.items() if v > 1), reverse=True)
    print(f"Job photos: {len(photo_usage)} in library, {sum(1 for v in photo_usage.values() if v)} used, {len(reused)} appear on more than one page")
    missing = [u for u in REG if u not in {p['url'] for p in pages} and u not in ("/privacy-policy/", "/terms/")]
    if missing: print("MISSING pages:", missing)
    for u, pr in issues.items(): print("LINT", u, pr)

if __name__ == "__main__":
    main()
