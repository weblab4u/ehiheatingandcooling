# City heat pump and furnace pages: /<city>/heat-pump/ and /<city>/furnace/
# Built from each city's verified facts (data/cities.py) and its Ontario Building Code SB-1 climate data
# (data/climate.py), so every number on a page is that city's own. Cities that already have
# /<city>/heat-pump-installation/ and /<city>/furnace-repair/ are skipped. Batches go live in order.
# Every passage has several independently written versions; each city gets its own mix (V picks by city),
# so pages read differently, not as one template with the name swapped. Facts never vary, only wording.
# Image blocks carry a "shot" brief: the photo to take on a real job. Until then a library photo stands in
# (allocated by build.py), and build.py lists every slot in image-slots.csv.
import os, zlib, importlib.util
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def _load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, "data", name + ".py"))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

CITIES = _load("cities").CITIES
_cl = _load("climate"); CLIMATE, TOR_HDD = _cl.CLIMATE, _cl.TORONTO_HDD
SKIP = {"toronto", "mississauga", "brampton", "vaughan", "markham", "oshawa", "hamilton", "barrie", "ottawa"}
LIVE_BATCHES = {1}
LIVE = {c["slug"] for c in CITIES if c["slug"] not in SKIP and c.get("batch", 1) in LIVE_BATCHES}
LIVE_TANKLESS = {c["slug"] for c in CITIES if c.get("batch", 1) in LIVE_BATCHES}      # no city had a tankless page, so every city gets one
RINNAI = {"garage": "/assets/img/brands/rinnai-rx-garage-install.webp", "unit": "/assets/img/brands/rinnai-rx-tankless.webp", "sink": "/assets/img/brands/rinnai-hot-water-sink.webp"}
ENBRIDGE_EMERGENCY = "1-866-763-5427"
FURNACE_PHOTOS = ["midea-gas-furnace-installed", "midea-furnace-room-pvc-venting", "furnace-coil-utility-room"]      # stand-ins for furnace slots
COMMISSION_PHOTOS = ["heat-pump-commissioning-gauges", "midea-cold-climate-heat-pump-commissioning"]

def chooser(slug):
    """V(key, a, b, ...) picks one version for this city, the same every build."""
    return lambda key, *opts: opts[zlib.crc32((slug + key).encode()) % len(opts)]

def fit(options, limit):
    for o in options:
        if len(o) <= limit: return o
    return options[-1]

def band(d):
    t = d["dt"]
    return "mild" if t >= -18 else "gta" if t >= -22 else "cold" if t >= -26 else "severe"

def snow_class(d):
    return "heavy" if d["snow"] >= 2.5 else "moderate" if d["snow"] >= 1.8 else "light"

def deg(t): return f"{t}°C"
def poss(n): return n + "'" if n.endswith("s") else n + "'s"

def hdd_line(d):
    pct = round((d["hdd"] / TOR_HDD - 1) * 100)
    if pct >= 5: return f"about {pct}% more heating over a winter than downtown Toronto"
    if pct <= -5: return f"about {-pct}% less heating over a winter than downtown Toronto"
    return "about the same heating load over a winter as downtown Toronto"

def dt_source(n, d):
    if d["listed"]:
        return f"the Ontario Building Code (SB-1) January design temperature for {n}"
    src = list(dict.fromkeys(d["src"]))
    return (f"the colder of the Building Code figures for nearby {src[0]} and {src[1]}, since SB-1 has no separate entry for {n}"
            if len(src) > 1 else f"the Building Code figure for nearby {src[0]}, since SB-1 has no separate entry for {n}")

def off_gas(c): return "propane" in c["housing"] or "oil" in c["housing"]
def hoods(c, k=3):
    h = c["neighbourhoods"][:k]
    return ", ".join(h[:-1]) + " and " + h[-1] if len(h) > 1 else h[0]
def cap(x): return x[:1].upper() + x[1:]

def nearby_link(slug, kind):
    """Same-service page for a nearby city: the new page if live, the older service page for the big cities, else nothing."""
    if kind == "tankless-water-heater": return f"/{slug}/{kind}/" if slug in LIVE_TANKLESS else None
    if slug in LIVE: return f"/{slug}/{kind}/"
    if slug in SKIP: return f"/{slug}/{'heat-pump-installation' if kind == 'heat-pump' else 'furnace-repair'}/"
    return None

def part(anchor, jump, icon, kicker, h2, lead):
    return {"type": "part", "anchor": anchor, "jump": jump, "icon": icon, "kicker": kicker, "h2": h2, "lead": lead}

def checklist(items): return '<ul class="checklist">' + "".join(f"<li>{i}</li>" for i in items) + "</ul>"

# ---------------------------------------------------------------- heat pump page
def heat_pump_page(c):
    s, n = c["slug"], c["name"]; d = CLIMATE[s]; b = band(d); sc = snow_class(d); t = deg(d["dt"]); V = chooser(s + "/hp")
    below = d["dt"] < -30; N = poss(n)

    keep_warm = {
     "mild": V("kw",
        f"Yes, when it is sized right. {n} is designed for {t} in January, comfortably inside what a cold-climate heat pump handles. We size it so the heat pump carries the house on its own through almost all of the winter, and backup heat only steps in during defrost and the odd colder night.",
        f"For a {n} winter, comfortably. The Building Code designs {n} for {t}, and cold-climate units keep producing heat far below that. Sized from a proper heat-loss calculation, the heat pump does nearly all of your heating, with a small backup for defrost cycles and rare cold snaps.",
        f"{t} is the coldest temperature {n} homes are designed for, and it sits well inside a cold-climate heat pump's range. The real question is sizing. Get that right and the heat pump heats the house on its own most of the winter; backup heat covers defrost and the occasional colder night."),
     "gta": V("kw",
        f"A cold-climate unit keeps heating well below {t}, but its output drops as the air gets colder while your house loses more heat. We run a heat-loss calculation for your home at {t}, find the balance point where the two meet, and size backup heat for the hours below it. In a {n} winter that is a small share of the season.",
        f"Yes, with the right size and a plan for the coldest hours. As it gets colder outside, the heat pump's output falls and your heat loss rises. We calculate both at {t}, find where they cross, and size backup heat to cover the few hours a {n} winter spends below that point.",
        f"It keeps heating at {t} and below. What changes in the cold is how much heat it can deliver, so we check its real output at {t} against your home's heat loss. The gap, if there is one, is covered by backup heat that only runs in the coldest stretches of a {n} winter."),
     "cold": V("kw",
        f"It will still be heating at {t}, but by then a cold-climate unit delivers noticeably less than its rated output. So we size from your home's heat loss at {t} and pair the heat pump with real backup: your furnace in a hybrid setup, or electric heat strips in an air handler. The heat pump does the work on the many milder days, and you never sit in a cold house waiting for it.",
        f"At {t} a cold-climate heat pump is still producing heat, just less of it. So in {n} we never size it to work alone on the design day. It pairs with a backup that can carry the load, your furnace or electric heat strips, and the heat pump handles the many winter days that are milder than that.",
        f"Yes, as part of a system built for {t}. The heat pump does most of the heating through the season; on the coldest days its output falls short of what a {n} house loses, so a furnace or electric heat strips make up the difference automatically. You do not notice the switch, you just stay warm."),
     "severe": (V("kw",
        f"{N} design temperature is {t}, colder than the -30°C the units we install are rated to. That is not a reason to skip a heat pump. It means we design the system as a pair: the heat pump carries the house through fall, spring and the milder part of winter, and a backup sized to heat the whole house alone takes over in the deep cold.",
        f"On its own, no, and anyone who says otherwise is not being straight with you. {n} is designed for {t}, below the -30°C rating of the units we install. Paired with a backup that can heat the whole house by itself, yes: the heat pump runs whenever it is mild enough and the backup takes the coldest days.")
        if below else V("kw",
        f"At {t} a cold-climate unit is near the bottom of its range, so we never count on it alone in {n}. We design a pair: the heat pump carries the house through fall, spring and the milder part of winter, and a backup sized to heat the whole house on its own covers the deep cold.",
        f"Not on its own at {t}. That is close to the limit of the units we install, so a {n} system always includes a backup big enough to heat the house by itself. The heat pump earns its keep on the many days warmer than that, which is most of the heating season.")),
    }[b]

    fuel = ({"problem": V("fuel-h", "You heat with propane or oil and the delivery bills keep coming", "Propane or oil, and you are tired of watching the tank gauge", "Your home is off the gas line"),
             "solution": V("fuel",
                f"This is where a heat pump pays back fastest in {n}. Homes heated by propane or oil sit in the top Home Renovation Savings tier, up to $7,500 based on heat pump size, and every hour the heat pump runs is fuel you do not buy. Keep the existing furnace as backup in a hybrid, or go all-electric with an <a href='/heat-pump/electric-air-handler-systems/'>electric air handler</a> if you want the tank gone.",
                f"Then you are in the top rebate tier: up to $7,500 for homes heated by propane or oil, based on heat pump size. The heat pump takes over most of your heating, so deliveries drop. You can keep the furnace as backup, or go all-electric with an <a href='/heat-pump/electric-air-handler-systems/'>electric air handler</a> and take the tank out.")}
            if off_gas(c) else
            {"problem": V("fuel-h", f"You are on {c['gas']} and the furnace still works", "Your gas furnace is fine, so why add a heat pump?", "You do not want to give up gas heat"),
             "solution": V("fuel",
                f"You do not have to rip it out. A cold-climate heat pump on top of your furnace becomes a <a href='/heat-pump/hybrid-furnace-systems/'>hybrid system</a>: the heat pump heats and cools most of the year and the furnace takes over below the balance point. Gas-heated homes commonly get up to $2,000 back, and the heat pump replaces your air conditioner at the same time.",
                f"You keep it. The heat pump goes on the same ductwork and becomes your air conditioner and your main heat for most of the season, and the furnace only fires when it gets properly cold. That is a <a href='/heat-pump/hybrid-furnace-systems/'>hybrid system</a>. Gas-heated homes commonly qualify for up to $2,000 back.",
                f"No need to. In a <a href='/heat-pump/hybrid-furnace-systems/'>hybrid setup</a> the furnace stays as your cold-weather heat and the heat pump handles the milder days and all of your cooling. For a home on {c['gas']}, the Ontario rebate is commonly up to $2,000.")})

    baseboard = {"problem": V("bb-h", "Electric baseboards and a hydro bill that climbs every January", "You heat with baseboards and the hydro bill hurts", "Baseboard heat in every room"),
                 "solution": V("bb",
                    "Baseboards turn one unit of electricity into one unit of heat. A cold-climate heat pump moves two to three units of heat per unit of electricity in mild weather. Homes heated by electricity get the top rebate tier, up to $7,500, and a <a href='/ac/multi-zone-ductless-system/'>multi-zone ductless system</a> heats and cools each room without adding ducts.",
                    "A baseboard heater gives you one unit of heat for each unit of electricity. A heat pump gives two to three in mild weather, so the same hydro buys you a lot more heat. Electrically heated homes are in the top rebate tier, up to $7,500, and <a href='/ac/ductless-mini-split/'>ductless heads</a> need no ductwork. The baseboards stay as backup.",
                    "Keep the baseboards as backup and let <a href='/ac/multi-zone-ductless-system/'>ductless heads</a> do most of the work. In mild weather a heat pump delivers two to three times the heat per unit of electricity that a baseboard does, it adds air conditioning, and homes heated by electricity get up to $7,500 back.")}

    ice = {"problem": V("ice-h", "Ice and snow on the outdoor unit", "Is it normal for the outdoor unit to frost up?", "Steam and frost on the unit in winter"),
           "solution": V("ice",
              f"A little frost on the coil is normal in a {n} winter: the unit melts it off in a defrost cycle and you may see steam. A solid block of ice, or snow packed against the coil, is not. It usually means the unit sits too low or under the roof drip line, and that is fixable.",
              f"Frost, yes. Every so often the unit reverses for a few minutes to melt it, and you see a cloud of steam. That is the defrost cycle. What is not normal is a block of ice building up around the unit, which in {n} almost always comes down to placement: too low, or under dripping eaves.",
              "Light frost that clears every so often is the defrost cycle doing its job, and the steam you see is the melt. Thick ice that stays, or snow drifted against the coil, means something is wrong with drainage or placement. Call us before it damages the fan.")}

    house = {"problem": V("house-h", f"Not sure a heat pump suits your kind of {n} home", f"Every {n} house is different. Which setup is yours?", "Will it work in an older or oddly shaped house?"),
             "solution": V("house",
                f"Homes in {n} range from {c['housing']}. Those need different setups: a ducted heat pump where there is a furnace and decent ductwork, ductless heads where there are no ducts or a cold addition, and an air handler where you are leaving propane, oil or an electric furnace. We look at your house first, then recommend one.",
                f"In {n} we see {c['housing']}. There is no single right answer for all of them. Ducted where the ductwork is sound, ductless for additions and homes without ducts, an air handler when you are leaving another fuel. The site visit decides it.")}

    winter = {"problem": V("win-h", "Can you install it in the middle of winter?", "Is winter a bad time to install?", "What if I need it before spring?"),
              "solution": V("win",
                 "Yes. Your existing heat stays on until the new system is running, and most single-system installs take one working day. Rebate pre-approval has to be in place before install day, so we file it first and book the install after.",
                 "Not at all. Your current heating runs right up until the new system is switched on, usually the same day. The one thing that cannot wait is the rebate pre-approval: it has to be granted before installation, so we file it before we book your date.",
                 f"Winter installs are routine for us. You keep your heat the whole time, most single systems in {n} go in within one working day, and we file your rebate pre-approval before the install date so a winter job does not cost you the rebate.")}

    order = [keep_warm and {"problem": V("kw-h", f"Will a heat pump keep my house warm at {t}?", f"Can a heat pump really handle {t}?", f"What happens on a {t} night?"), "solution": keep_warm},
             fuel, baseboard, ice, house, winter]
    items = order if b != "severe" else [order[0], order[1], order[5], order[3], order[2], order[4]]

    place = {
     "heavy": V("pl",
        f"{N} ground snow load is {d['snow']} kPa in the Building Code, heavy for Ontario. The outdoor unit goes on a tall stand or a wall bracket, out from under the roof edge so sliding snow and ice cannot land on it, and turned so drifts do not pile against the coil.",
        f"The Building Code puts {N} ground snow load at {d['snow']} kPa, among the heavier figures in the province. So the unit never sits on the ground here: it goes on a tall stand or bracket, clear of the eaves, facing away from the wind that builds drifts."),
     "moderate": V("pl",
        f"The Building Code puts {N} ground snow load at {d['snow']} kPa, so snow piles up here. We raise the outdoor unit on a stand above the usual snow line, keep it out of the roof drip line and leave room for defrost water to drain away instead of freezing into a block under the unit.",
        f"With a {d['snow']} kPa ground snow load in the Building Code, {n} gets enough snow to bury a unit sitting on a pad. We set it on a stand above the usual snow line, away from the drip line, with a clear path for defrost water to drain."),
     "light": V("pl",
        f"{n} gets less snow than most of Ontario (a {d['snow']} kPa ground snow load in the Building Code), but the unit still goes on a raised stand. During defrost it sheds water, and a unit sitting on a pad at grade freezes that water into an ice dam around its own base.",
        f"Snow is lighter in {n}, with a {d['snow']} kPa ground snow load in the Building Code. The bigger risk here is meltwater: the unit drains during every defrost cycle, so we raise it on a stand where that water runs off instead of freezing around the base."),
    }[sc]
    place_html = (f"<p>{place}</p><p>" + V("pl2",
        "We also check where the wind comes from, keep the unit away from bedroom windows (yours and your neighbour's), and run the line set in a cover along the wall.",
        "Then the practical stuff: keep it away from bedroom windows, yours and the neighbour's, mind the prevailing wind, and run the line set in a tidy cover.",
        "Noise and looks matter too. We keep the unit away from bedrooms on both sides of the fence and cover the line set where it runs along the wall.")
        + (f" In {hoods(c)}, that often means the side or rear yard rather than the front." if c["neighbourhoods"] else "") + "</p>"
        + checklist(V("pl3", ["Raised stand or wall bracket, never a pad at grade", "Out of the roof drip line and sliding snow", "Defrost water drains away from walkways", "Line set covered and sealed where it enters the house"],
                             ["Lifted above the snow line on a stand or bracket", "Clear of eaves, valleys and sliding snow", "A drainage path for defrost water", "Line set in a cover, sealed at the wall"])))

    sizing_html = (
        "<p>" + V("sz1",
            f"{n} is designed for <strong>{t}</strong> in January, which is {dt_source(n, d)}. One percent of January hours are colder still, at or below {deg(d['dt1'])}. Over a full season the Building Code counts <strong>{d['hdd']:,} heating degree days</strong> here, {hdd_line(d)}.",
            f"Your system is sized for <strong>{t}</strong>, {dt_source(n, d)}. In one percent of January hours it gets colder, down to {deg(d['dt1'])}. Across the season, {n} needs <strong>{d['hdd']:,} heating degree days</strong>, {hdd_line(d)}.")
        + "</p><p>" + V("sz2",
            f"Those numbers decide the system. We measure your walls, attic, windows and air leakage, calculate the heat loss at {t}, and check the heat pump's real output at that temperature, not the number on the box. ",
            f"From there we work on your house: walls, attic insulation, windows and air leakage give the heat loss at {t}. Then we look up the unit's actual output at that temperature in the manufacturer's data, because the capacity printed on the label is measured in much milder weather. ")
        + ("Then we size backup heat to carry the whole house on its own, because below -30°C the heat pump steps aside." if below else
           V("sz3", "Where the heat pump's output and your heat loss meet is the balance point. Below it, backup heat helps.",
                    "The temperature where those two lines cross is your balance point, and backup heat is sized for the hours below it."))
        + (f" Locally, {c['climate']}." if c.get("climate") else "") + "</p>"
        + checklist(V("sz4", ["Heat loss calculated room by room at your design temperature", f"Heat pump output checked at {t}, not just the nameplate", "Backup heat sized for the hours below the balance point", "Duct static pressure tested so the airflow matches the unit"],
                             [f"Room-by-room heat loss at {t}", "Real output at that temperature, from manufacturer data", "Backup sized to the balance point for your fuel", "Ductwork tested for airflow before we commit to a size"]))
        + "<p>" + V("sz5", "Oversizing is a common mistake: a unit that is too big short cycles and wears out early.",
                         "Bigger is not better. An oversized unit runs in short bursts, dehumidifies poorly in summer and wears out sooner.")
        + " Read how these units hold capacity in our <a href='/heat-pump/cold-climate/'>cold-climate heat pump guide</a>.</p>")

    snapshot = {"type": "snapshot", "h2": V("snap-h", f"Heat pump numbers for {n}", f"{N} heating numbers", f"The {n} figures we size from"),
       "lead": V("snap-l", "The figures we size your system from. They come from the Ontario Building Code, not a sales chart.",
                           "Official Ontario Building Code climate data for your area. Every quote starts here.",
                           "Before we talk equipment, these are the numbers your house has to meet."),
       "items": [
        {"icon": "snow", "label": "January design temperature", "value": t,
         "text": (f"SB-1 figure for {n}. Your heat pump and backup are sized to keep you warm at this temperature." if d["listed"]
                  else f"SB-1 has no separate entry for {n}. Nearby {' and '.join(dict.fromkeys(d['src']))} give {deg(d['dt_warm'])} to {t}; we size to the colder." if d["dt_warm"] != d["dt"]
                  else f"SB-1 figure for nearby {' and '.join(dict.fromkeys(d['src']))}, the closest listed to {n}. We size to it.")},
        {"icon": "flame", "label": "Heating degree days", "value": f"{d['hdd']:,}", "text": f"How much heating a season takes: {hdd_line(d)}."},
        {"icon": "house", "label": "Ground snow load", "value": f"{d['snow']} kPa",
         "text": {"heavy": "Heavy for Ontario. The outdoor unit goes on a tall stand or wall bracket.", "moderate": "Snow piles up. The unit sits on a stand above the snow line.",
                  "light": "Lighter snow, but the unit still goes on a stand so defrost water drains."}[sc]},
        {"icon": "rebate", "label": "Ontario rebate", "value": "Up to $7,500",
         "text": "For homes heated by electricity, oil or propane. Gas-heated homes commonly up to $2,000. Pre-approval before install."}]}
    problems = {"type": "problems", "h2": V("prob-h", f"Heat pump questions {n} homeowners ask us in winter", f"What {n} homeowners ask before switching to a heat pump", f"Your heat pump questions, answered for {n}"),
                "lead": V("prob-l", f"Straight answers, using {poss(n)} own numbers.", "Short answers to what people actually ask us on site visits.", f"No sales pitch, just what applies to a {n} house."),
                "items": items}
    off_row = ["Propane or oil furnace", "Central heat pump with an electric air handler, or a hybrid with your existing furnace", "Up to $7,500"]
    table = {"type": "table", "h2": V("tab-h", f"Which heat pump setup fits your {n} home", f"Pick your starting point: heat pump options in {n}", f"How you heat now decides your {n} heat pump"),
       "lead": V("tab-l", "Start with how your house is heated today. That decides the equipment and your rebate tier.", "Find your current heating in the left column. The middle column is what we usually recommend, and the right one is your Ontario rebate tier.",
                          "Your current fuel sets both the equipment and the rebate."),
       "headers": ["How you heat now", "What we usually install", "Ontario rebate"],
       "rows": ([off_row] if off_gas(c) else []) + [
        ["Gas furnace with ductwork", "Cold-climate heat pump on your furnace, with the furnace as backup (<a href='/heat-pump/hybrid-furnace-systems/'>hybrid</a>)", "Commonly up to $2,000"],
        ["Electric furnace", "Central heat pump with an <a href='/heat-pump/electric-air-handler-systems/'>electric air handler</a>", "Up to $7,500"],
        ["Electric baseboards, no ducts", "<a href='/ac/ductless-mini-split/'>Ductless</a> or <a href='/ac/multi-zone-ductless-system/'>multi-zone ductless</a> heads", "Up to $7,500"]] +
        ([] if off_gas(c) else [off_row]) + [["Boiler and radiators", "Ductless heads for the main rooms, with the boiler kept as backup", "Depends on your fuel"]],
       "note": "Rebates are from Ontario's Home Renovation Savings Program, based on heat pump size, and need pre-approval before installation. A separate federal rebate is expected to open in early 2027. See <a href='/heat-pump-rebates/'>how both work</a>."}
    place_b = {"type": "split", "h2": V("pl-h", f"Where your outdoor unit goes in {n}", f"Placing a heat pump for {n} snow", f"Keeping the outdoor unit clear of {n} winters"),
               "photo": "out", "reverse": True, "html": place_html,
               "shot": f"Outdoor heat pump on a raised stand or wall bracket beside a {n} home, with snow on the ground and the roof edge visible"}
    sizing_b = {"type": "split", "h2": V("sz-h", f"How we size a heat pump for {t}", f"Sizing for {poss(n)} {t} design day", f"The sizing math for a {n} home"),
                "photo": "sys", "photo_keys": COMMISSION_PHOTOS, "html": sizing_html,
                "shot": "Technician at the outdoor unit during commissioning, gauges connected, checking pressures and output"}
    cost = {"type": "cost_guide", "h2": V("cost-h", f"What a heat pump costs in {n}", f"Heat pump prices in {n}", f"{n} heat pump installation costs"), "keys": ["heat_pump_ducted", "ductless_single"],
            "lead": V("cost-l", "Starting prices before rebates. Your final price depends on the size we calculate, the indoor equipment, ductwork and the electrical work, and it is guaranteed in writing.",
                                "These are starting points before rebates. The written quote you get after the visit is the price you pay.",
                                "Size, indoor equipment, ductwork and electrical work set the final number. You get it in writing, guaranteed, before anything is ordered.")}
    steps = {"type": "steps", "h2": V("st-h", f"How a winter heat pump install works in {n}", f"From first call to first heat in {n}", f"Your {n} heat pump install, step by step"), "cta": "Book My Heat Pump Visit",
       "items": [
        {"title": V("s1t", "Home visit and heat loss", "We measure your house"), "text": V("s1", f"We measure the house, check the ducts and electrical panel, and calculate the heat loss at {t}.", f"A technician checks your ducts, panel and insulation and works out the heat loss at {t}.")},
        {"title": V("s2t", "Written price and pre-approval", "Your price, then the rebate"), "text": V("s2", "One guaranteed price with model numbers and your rebate estimate. We file pre-approval before booking install day.", "You get a fixed price with the exact models and your estimated rebate. Pre-approval goes in before we schedule the install.")},
        {"title": V("s3t", "Install day", "One day of work"), "text": V("s3", "Your current heat stays on. Most single systems are done in one working day, 240V circuit by an ESA-licensed electrician included.", "Most single systems take one working day, including the 240V circuit by an ESA-licensed electrician. Your old heat runs until the switchover.")},
        {"title": V("s4t", "Commissioning and handover", "Testing and paperwork"), "text": V("s4", "We test heating at today's outdoor temperature, set the backup switchover, register the warranty and file your rebate paperwork.", "We prove it heats at today's outdoor temperature, tune the backup switchover, then register your warranty and send in the rebate documents.")}]}
    equip = {"type": "equipment", "h2": V("eq-h", f"Cold-climate heat pumps we install in {n}", f"Heat pump models for {n} homes"), "groups": ["heat_pumps"],
             "lead": "Every model is on NRCan's qualified products list, the requirement for the Ontario rebate."}
    incl = {"type": "checklist", "h2": V("in-h", f"What is included in a {n} heat pump installation", f"Everything in your {n} heat pump quote"), "photo": "in",
            "shot": "Indoor side of a finished install: wall head or air handler with neat line set and condensate drain",
            "items": V("in", [f"Heat-loss sizing at {t} and a written, guaranteed price", "Outdoor unit on a raised stand or wall bracket, clear of snow and the drip line",
                              "Line set brazed, nitrogen pressure tested, vacuumed and covered", "Dedicated 240V circuit with the ESA notification filed",
                              "Indoor coil, air handler or wall heads with a condensate drain that will not freeze", "Backup heat set up and the switchover temperature tuned for your fuel",
                              "Thermostat setup, warranty registration and your rebate paperwork", "A walk-through of defrost cycles and what is normal in winter"],
                             [f"A heat-loss calculation for {t} and one fixed price", "Stand or bracket that lifts the unit above the snow", "Brazed, pressure-tested and vacuumed refrigerant lines in a cover",
                              "The 240V circuit, done and filed by an ESA-licensed electrician", "Air handler, coil or wall heads, with a freeze-proof condensate drain",
                              "Backup heat wired in and the changeover set for your fuel", "Warranty registration and every piece of rebate paperwork", "A handover so you know what defrost looks and sounds like"])}

    install = V("order",
        [snapshot, problems, table, place_b, sizing_b, cost, steps, equip, incl],
        [snapshot, table, problems, sizing_b, place_b, steps, cost, incl, equip],
        [snapshot, problems, table, sizing_b, cost, place_b, steps, equip, incl])

    rp_table = {"type": "table", "h2": V("rpt-h", "Repair it or replace it?", "Fix the old system, or replace it?"),
       "lead": V("rpt-l", "We price both in writing and tell you which we would pick. This is how we decide.", "You get both numbers. Here is the reasoning behind our recommendation."),
       "headers": ["What we find", "Usually", "Why"],
       "rows": [["Capacitor, contactor or fan motor", "Repair", V("rr1", "Common parts, and the system has years left", "Inexpensive parts on a system with life left")],
                ["Small refrigerant leak on a newer system", "Repair", V("rr2", "Find and fix the leak, then recharge", "Seal the leak and recharge to spec")],
                ["Compressor failure on a system over 10 years old", "Usually replace", V("rr3", "The compressor is the most expensive part, and the rest of the system is aging too", "A compressor on an older unit costs close to a new system")],
                ["Air conditioner still running on R-22 refrigerant", "Replace", V("rr4", "New R-22 has not been made or imported in Canada since 2020, so every recharge gets dearer", "R-22 supply in Canada is limited to recovered stock, so repairs keep getting more expensive")],
                ["Older heat pump that cannot keep up in winter", "Replace", V("rr5", "Older models lose capacity fast in the cold; cold-climate units are rated to -30°C", "Cold-climate models hold far more capacity at low temperatures")],
                ["Central AC 12 to 15 or more years old", "Replace with a heat pump", V("rr6", "Same footprint, adds winter heat, and qualifies for the rebate", "One outdoor unit for cooling and heating, plus the rebate")]],
       "note": "Our rule of thumb: if the system is under about 10 years old and the repair is under a third of a new one, repair it."}
    rp_split = {"type": "split", "h2": V("rps-h", f"Swapping an old AC or heat pump for a cold-climate unit in {n}", f"What replacing your system involves in {n}"), "photo": "out",
       "shot": "Old air conditioner condenser beside the new cold-climate heat pump on install day, before the old unit is hauled away",
       "html": "<p>" + V("rps1",
           "Most replacements we do start with an air conditioner that has reached the end of its life. A cold-climate heat pump goes in the same spot, cools just as well, and heats your home most of the winter.",
           "Replacing an aging air conditioner is the easiest time to switch. The heat pump sits where the AC was, does the cooling, and takes over most of your heating as well.")
           + "</p>" + checklist(V("rps2", ["Old refrigerant recovered by licensed techs and the unit hauled away", "Line set inspected; replaced when it is undersized, damaged or contaminated",
                                           "A stand or bracket that lifts the new unit above the snow", "Indoor coil matched to the new outdoor unit", "Electrical checked for the new unit's breaker and disconnect",
                                           "Rebate pre-approval filed before the old unit comes out"],
                                          ["Refrigerant recovered and the old unit taken away", "Line set reused only when it is sized and clean enough", "New unit raised above the snow line",
                                           "A matched indoor coil, not a mix and match", "Breaker and disconnect sized for the heat pump", "Pre-approval in place before removal day"]))
           + "<p>" + V("rps3", f"If your furnace is also old, we quote both together so the {n} system is designed as one.", "If the furnace is near the end too, we price both, so the new system works as one.") + "</p>"}

    rep_problems = {"type": "problems", "h2": V("rep-h", f"Heat pump problems we fix in {n}", f"When your {n} heat pump acts up"),
       "lead": V("rep-l", "What each symptom usually means. Call us with the symptom and we bring the right parts.", "Some of these are normal winter behaviour. Some need a technician. Here is how to tell."),
       "items": [
        {"problem": V("r1h", "It runs, but the house is getting cold", "Running, but not keeping up"),
         "solution": V("r1", "Check the thermostat mode and the filter first. If those are fine, the usual causes are a blocked or iced outdoor coil, backup heat that is not switching on, or low refrigerant. We test the charge and the controls and fix the cause.",
                             "First the easy checks: thermostat in Heat, clean filter, nothing piled against the outdoor unit. If it still falls behind, we test refrigerant pressures, the defrost controls and the backup heat switchover.")},
        {"problem": V("r2h", "The outdoor unit has turned into a block of ice", "Thick ice that will not clear"),
         "solution": V("r2", "A failed defrost sensor or control board, a fan that is not running, or meltwater that has nowhere to drain. Switch the thermostat to emergency or auxiliary heat so the house stays warm, and call us. Do not chip the ice off; it is easy to damage the coil.",
                             "Defrost is not working, or the meltwater is refreezing under the unit. Set the thermostat to emergency heat, leave the ice alone, and call us. We repair the defrost fault and fix the drainage or placement.")},
        {"problem": V("r3h", "Backup heat runs all the time and the hydro bill jumped", "Emergency heat is always on"),
         "solution": V("r3", "Usually a thermostat setting, a faulty outdoor sensor, low refrigerant or a heat pump that is too small for the house. Backup heat is expensive to run, so it is worth fixing quickly.",
                             "The heat pump is handing off too early or not running at all. We check the thermostat's changeover settings, the outdoor temperature sensor and the refrigerant charge.")},
        {"problem": V("r4h", "It blows cool air for a few minutes, then a whoosh", "Steam, a whoosh and a few minutes of cool air"),
         "solution": V("r4", "That is a normal defrost cycle. The unit reverses for a few minutes to melt frost off the outdoor coil. If it happens every few minutes or lasts much longer than usual, call us.",
                             "Normal. Every so often the heat pump defrosts its outdoor coil, and you hear the valve shift and see steam outside. Constant defrosting, or cold air for long stretches, is not normal.")},
        {"problem": V("r5h", "An error code is flashing", "A code on the thermostat or the unit"),
         "solution": V("r5", "Write it down or take a photo and call us. We read the code, confirm it with meter readings and price the repair before we start, whoever installed the system.",
                             "Send us a photo of the code. We confirm it with real measurements rather than guessing from the code alone, and we work on systems we did not install.")}]}
    maint = {"type": "checklist", "h2": V("mt-h", f"What a heat pump tune-up includes in {n}", "Your yearly heat pump service"),
       "lead": V("mt-l", "Once a year, ideally in the fall, so the system goes into winter clean and charged. Many manufacturers also require it for extended warranty coverage.", "A fall service catches the weak part before a January breakdown. See our <a href='/heat-pump/repair-maintenance/'>heat pump repair and maintenance</a> page for more."),
       "items": V("mt", ["Outdoor coil cleaned and the fan checked", "Refrigerant pressures tested against the manufacturer's numbers", "Defrost cycle tested", "Condensate drain cleared",
                         "Electrical connections tightened and the capacitor tested", "Backup heat and changeover temperature checked", "Filter replaced or cleaned", "Stand, bracket and snow clearance checked"],
                        ["Coil and fan cleaned and inspected", "Charge checked with gauges, not guessed", "A defrost cycle run and timed", "Drain lines flushed",
                         "Capacitor and contactor tested, terminals tightened", "Backup heat tested at the switchover", "A clean filter", "The unit's height and clearance for winter checked"])}

    blocks = ([part("installation", "Installation", "install", V("pk1", "Installation", "New heat pump"), V("ph1", f"Heat pump installation in {n}", f"Installing a heat pump in {n}"),
                    V("pl1", f"Sizing, placement, cost and rebates for a new cold-climate heat pump in {n}.", f"Everything you need to decide on a new heat pump for your {n} home."))]
              + install
              + [part("replacement", "Replacement", "clock", V("pk2", "Replacement", "Replacing a system"), V("ph2", f"Heat pump and AC replacement in {n}", f"Replacing an old heat pump or air conditioner in {n}"),
                      V("pl2", "When an older system is worth repairing, and when replacing it with a cold-climate heat pump makes more sense.", "How we decide between repair and replacement, and what a replacement involves.")),
                 rp_table, rp_split,
                 part("repair", "Repair & Maintenance", "wrench", V("pk3", "Repair and maintenance", "Service"), V("ph3", f"Heat pump repair and maintenance in {n}", f"Keeping your {n} heat pump running"),
                      V("pl3", "Winter problems, what is normal, and what a yearly tune-up covers.", "What to do when it acts up, and how to stop it happening.")),
                 rep_problems, maint, {"type": "money"}])

    title = fit([f"Heat Pump Installation & Replacement {n} | Repair", f"Heat Pump Installation & Replacement {n}", f"Heat Pump Installation {n} | Replacement", f"Heat Pump Installation {n}"], 60)
    desc = fit([f"Heat pump installation in {n}, sized for {t}, plus replacement and repair. Up to $7,500 back for electric, oil or propane homes. Free quote.",
                f"Heat pump installation in {n}, sized for {t}, plus replacement and repair. Up to $7,500 in rebates. Free quote.",
                f"Heat pump installation, replacement and repair in {n}. Up to $7,500 in rebates. Free quote."], 155)
    near = [u for u in (nearby_link(x, "heat-pump") for x in c["nearby"]) if u]
    return {
     "url": f"/{s}/heat-pump/", "city_service": s, "priority": "0.7", "heating": True,
     "title": title, "description": desc, "eyebrow": f"Heat Pumps · {n}", "h1": f"Heat Pump Installation, Replacement and Repair in {n}",
     "tagline": V("tag", f"Sized for {N} {t} design day, rebate filed before install", f"Built for {t}, raised above the snow, rebate paperwork done for you", f"The right size for {t}, with your rebate filed first"),
     "intro": "<p>" + V("intro",
        f"Before you put a heat pump on a {n} house, you want two answers: will it keep you warm on the coldest night, and what does it cost after the rebate. Here are both, worked out with {N} own Building Code numbers, plus which setup suits the way your home is heated now.",
        f"Thinking about a heat pump for your {n} home this winter? Below are the numbers it has to meet, what it costs before and after the rebate, and which setup fits the way you heat today. No guesswork, just {N} own Building Code data.",
        f"A heat pump only works as well as its sizing. For {n} that means {t} on the coldest design day, so that is where we start. Here is how we size it, where the outdoor unit goes, what you pay and what you get back.")
        + V("intro2", " Replacing an old AC or heat pump, or need a repair? Use the quick links below.", " Already have one that needs replacing or fixing? Jump straight there with the links below.") + "</p>",
     "hero_points": [f"Sized from a heat-loss calculation at {N} {t} design temperature",
                     "Cold-climate Midea and Kepler models rated to -30°C" + (", with full backup for colder nights" if below else ""),
                     "Up to $7,500 back for homes heated by electricity, oil or propane", "Old AC and heat pump replacement, repair and yearly tune-ups"],
     "hero_image": f"Cold-climate heat pump outdoor unit on a raised stand beside a {n} home in winter",
     "service": {"name": f"Heat Pump Installation in {n}", "type": "Cold-climate heat pump installation", "area": n},
     "blocks": blocks,
     "faqs": [
      (f"Will a heat pump work in {n} in January?",
       V("f1", f"Yes, a cold-climate heat pump keeps heating in a {n} January, and we size it from your home's heat loss at {t}, {dt_source(n, d)}. ",
               f"It does, as long as it is sized for {t}, {dt_source(n, d)}. ")
       + ("Because that is colder than the -30°C the units are rated to, we always pair it with backup heat sized to carry the house on its own." if below else
          V("f1b", "Backup heat, either your furnace or electric heat strips, covers the coldest hours below the balance point.", "On the coldest hours a furnace or electric heat strips back it up automatically."))),
      (f"How much does a heat pump cost in {n} after the rebate?",
       V("f2", f"Cold-climate heat pump installation in {n} starts at $5,500 before rebates, and the final price depends on size, ductwork and electrical work. Homes heated by electricity, oil or propane can get up to $7,500 back through the Home Renovation Savings Program, while gas-heated homes commonly get up to $2,000. Pre-approval must be in place before installation.",
               f"Installed prices in {n} start at $5,500 before rebates; your written quote depends on size, ductwork and the electrical work. The Ontario rebate is up to $7,500 for homes heated by electricity, oil or propane and commonly up to $2,000 for gas-heated homes, with pre-approval required before installation.")),
      (f"Should I keep my furnace when I add a heat pump in {n}?",
       (V("f3", f"In most {n} homes, yes. Keeping the furnace as backup in a hybrid system means the heat pump does the work on milder days and the furnace covers the deep cold. If you are on propane or oil and want to leave it behind, an electric air handler with heat strips is the all-electric option.",
                f"Usually, yes. In {n} the furnace makes a good cold-weather backup while the heat pump does most of the heating. If you would rather be done with propane or oil, an electric air handler with heat strips replaces it.") if off_gas(c) else
        V("f3", f"In most {n} homes on {c['gas']}, yes. A hybrid system lets the heat pump heat and cool most of the year while the furnace covers the coldest hours. If your furnace is near the end of its life, we quote the replacement at the same time.",
                f"Usually, yes. On {c['gas']}, a hybrid system keeps the furnace for the coldest hours and lets the heat pump handle the rest of the year, cooling included. If the furnace is old, we price a replacement alongside."))),
      (f"Where should the heat pump go on a {n} house?",
       V("f4", f"On a raised stand or wall bracket, out of the roof drip line, with room for defrost water to drain. {N} Building Code ground snow load is {d['snow']} kPa, so we set the height for your snow, keep the unit away from bedroom windows and run the line set in a cover.",
               f"Above the snow line, on a stand or bracket, clear of the eaves and away from bedrooms. With a {d['snow']} kPa ground snow load in {n}, height and drainage matter more than which side of the house it is on.")),
      (f"Should I repair or replace my old air conditioner or heat pump in {n}?",
       V("f6", "If it is under about 10 years old and the repair is under a third of a new system, repair it. If the compressor has failed on an older unit, or it runs on R-22 refrigerant, replacing it with a cold-climate heat pump usually makes more sense and qualifies for the rebate.",
               "Repair when the system is younger than about 10 years and the fix is modest. Replace when the compressor fails on an older unit or it still uses R-22. A cold-climate heat pump then cools, heats and qualifies for the rebate.")),
      (f"How often does a heat pump need servicing in {n}?",
       V("f7", f"Once a year, ideally in the fall before the {n} heating season. We clean the coil, check the refrigerant charge, test defrost and backup heat, and clear the condensate drain.",
               "Every year, best done in the fall. A tune-up covers the coil, charge, defrost cycle, drains, electrical parts and backup heat, and many manufacturers require it to keep extended warranties valid.")),
      (f"Can you install a heat pump in {n} during winter?",
       V("f5", f"Yes. Your current heat stays on until the new system is running, and most single-system installs in {n} take one working day. We file the rebate pre-approval first, then book the install date, so a winter install does not cost you the rebate.",
               f"Yes, winter installs are routine. You keep your existing heat until the switchover, most jobs in {n} take a day, and the rebate pre-approval is filed before we book the date."))],
     "related": [f"/{s}/furnace/", f"/{s}/", "/heat-pump/cold-climate/", "/heat-pump/hybrid-furnace-systems/", "/heat-pump-rebates/"] + near[:1],
    }

# ---------------------------------------------------------------- furnace page
def furnace_page(c):
    s, n = c["slug"], c["name"]; d = CLIMATE[s]; b = band(d); sc = snow_class(d); t = deg(d["dt"]); V = chooser(s + "/fu"); N = poss(n)

    vent_tip = {"heavy": f"After a {n} snowstorm, check these before anything else.", "moderate": f"After a heavy {n} snowfall, check them first.",
                "light": "Drifts against the wall and ice from the roof can still close them off."}[sc]
    checks = [
        {"title": "Thermostat", "text": V("c1", "Set it to Heat and a few degrees above the room temperature. If the screen is blank, change the batteries.",
                                               "Make sure it says Heat, not Cool or Off, and turn it up a few degrees. A blank screen usually means dead batteries.")},
        {"title": "Power", "text": V("c2", "The furnace switch, which looks like a light switch on or near the furnace, must be on, and the breaker must not be tripped.",
                                          "Find the switch that looks like a light switch near the furnace and make sure it is on. Then check the breaker panel.")},
        {"title": "Filter", "text": V("c3", "A grey, clogged filter overheats the furnace and it shuts itself off. Swap it and wait a few minutes.",
                                           "If the filter is grey and matted, the furnace overheats and shuts off to protect itself. Put in a clean one and give it a few minutes.")},
        {"title": "Vent pipes outside", "text": V("c4", "Snow or ice over the two white plastic pipes on the outside wall shuts a high-efficiency furnace down. Clear them by hand.",
                                                       "A high-efficiency furnace vents through two white plastic pipes on an outside wall. If snow or ice covers them, it stops. Clear them by hand.") + " " + vent_tip},
        {"title": "One restart, then call", "text": V("c5", "Turn the furnace switch off for 30 seconds and back on. If it tries to light and shuts down again, stop there and call us.",
                                                           "Switch it off, wait 30 seconds, switch it on. If it starts, then quits again, do not keep resetting it. Call us.")}]

    cold_risk = {"mild": f"Even in {n}, a house without heat drops fast on a cold night.",
                 "gta": f"On a {t} night in {n}, a house without heat cools quickly, and pipes on outside walls are the first at risk.",
                 "cold": f"At {t}, a {n} house without heat can get cold enough to freeze pipes overnight.",
                 "severe": f"At {t}, a {n} house without heat can freeze pipes within hours."}[b]

    P = {
     "light": {"problem": V("p1h", "It clicks and tries to light, then shuts off", "Click, a flicker, then nothing"),
               "solution": V("p1", "Usually a dirty flame sensor, a cracked ignitor or a pressure switch that does not close. These are common parts we carry, so the fix is often done on the first visit, priced in writing before we start.",
                                   "That pattern points to the flame sensor, the ignitor or the pressure switch. They are inexpensive parts we keep on hand, so it is often sorted on the first visit, with the price in writing first.")},
     "cold": {"problem": V("p2h", "It runs, but the air from the vents is cold", "Fan running, no heat"),
              "solution": V("p2", "The furnace has locked itself out after failed ignition, or the high-limit switch has tripped from a blocked filter or closed vents. We find which and why, because resetting it without fixing the cause just brings it back tonight.",
                                  "Either it has locked out after failing to light, or it overheated (often a blocked filter or closed vents) and shut the burners off. Resetting it buys an hour. Finding the cause fixes it.")},
     "vents": ({"problem": V("p3h", "It shuts down every time it snows or the wind picks up", "Every storm, the furnace quits"),
                "solution": V("p3", f"Blocked intake or exhaust pipes. {N} Building Code ground snow load is {d['snow']} kPa, and a termination set too low gets buried. We clear it, and if it keeps happening we raise the pipes above your snow line.",
                                    f"The vent pipes outside are getting buried or iced over. With a {d['snow']} kPa ground snow load in {n}, low terminations are a regular problem. Raising them above the snow line ends it.")}
               if sc != "light" else
               {"problem": V("p3h", "Water around the furnace and an error light", "A puddle under the furnace"),
                "solution": V("p3", "A high-efficiency furnace makes litres of water a day. When the condensate trap clogs or the drain line freezes, the furnace shuts down to protect itself. We clean the trap and reroute or heat-trace the line so it does not happen again.",
                                    "High-efficiency furnaces drain water as they run. A clogged trap or a frozen drain line backs it up and trips a safety switch. We clean the trap and fix the line so it stays clear.")}),
     "cycle": {"problem": V("p4h", "It turns on and off every few minutes", "Short bursts, all day long"),
               "solution": V("p4", "Short cycling. The usual causes are an oversized furnace, a clogged filter or a thermostat near a supply vent. Short cycling wears out ignitors and heat exchangers early, so we fix the cause rather than the symptom.",
                                   "That is short cycling, usually from an oversized furnace, a blocked filter or a thermostat sitting next to a supply vent. It is hard on ignitors and heat exchangers, so it is worth fixing properly.")},
     "rooms": {"problem": V("p5h", "Some rooms never warm up", "The back bedroom is always cold"),
               "solution": V("p5", "That is usually the ductwork, not the furnace: too few returns, leaky joints or closed dampers. We measure and balance it. For a cold addition or bonus room, a single <a href='/ac/ductless-mini-split/'>ductless head</a> often fixes it for less than a bigger furnace.",
                                   "Usually that is the ducts, not the furnace: missing returns, leaks or closed dampers. We measure and balance the system, and for an addition that never warms up, one <a href='/ac/ductless-mini-split/'>ductless head</a> is often the cheaper fix.")},
     "old": {"problem": V("p6h", f"An original furnace in an older {n} home", "The furnace is as old as the renovation"),
             "solution": V("p6", f"Homes in {n} range from {c['housing']}. The oldest furnaces in them are often mid-efficiency units venting into a chimney, or early high-efficiency models near the end of their life. We check the heat exchanger and venting closely, and if replacement is the honest answer, we size the new furnace to the house, not to the old label.",
                                 f"In {n} we work in {c['housing']}. Older furnaces there tend to be mid-efficiency units on a chimney or first-generation high-efficiency models. We inspect the heat exchanger and venting, and if it is time to replace, we size the new one for your house as it is now.")},
     "gas": {"problem": V("p7h", "You smell gas or your CO alarm goes off", "Gas smell or a carbon monoxide alarm"),
             "solution": V("p7", f"Leave the house now. From outside, call 911 or Enbridge Gas's 24-hour emergency line at {ENBRIDGE_EMERGENCY}. Once the utility clears the house, we find the source, test for carbon monoxide and make it safe.",
                                 f"Get everyone out first, then call 911 or Enbridge Gas at {ENBRIDGE_EMERGENCY} from outside. After the utility has made it safe, we find the cause, test for carbon monoxide and fix it.")}}
    items = [P["light"], P["cold"], P["vents"], P["cycle"], P["old"], P["rooms"], P["gas"]]
    if off_gas(c):
        items.insert(5, {"problem": V("p8h", "A propane or oil furnace and a fuel bill you dread", "Paying for propane or oil every month"),
                         "solution": V("p8", f"If the furnace is old, ask us to price a <a href='/{s}/heat-pump/'>cold-climate heat pump</a> alongside the repair. In homes heated by propane or oil the Ontario rebate is up to $7,500, and the heat pump cuts how much fuel you buy every winter.",
                                             f"When the repair is big, get a <a href='/{s}/heat-pump/'>heat pump price</a> next to it. Propane and oil homes get up to $7,500 back, and the furnace can stay as backup while the heat pump does most of the work.")})
    if b in ("cold", "severe"):
        items.insert(2, {"problem": V("p9h", "The furnace stopped and it is bitterly cold", f"No heat at {t}"),
                         "solution": cold_risk + " " + V("p9", "While you wait for us: keep doors closed, open the cabinet doors under sinks on outside walls, let a tap drip, and use space heaters only with clear space around them. Never heat the house with the oven or a barbecue.",
                                                          "Until we arrive: close off unused rooms, open the cabinets under sinks on outside walls, leave a tap dripping, and keep space heaters clear of anything that burns. Never use the oven, a barbecue or a generator indoors for heat.")})

    sizing_html = (
        "<p>" + V("fs1", f"A new furnace for a {n} home is sized for <strong>{t}</strong>, {dt_source(n, d)}. Over a season {n} needs {d['hdd']:,} heating degree days, {hdd_line(d)}.",
                         f"We size {n} furnaces for <strong>{t}</strong>, {dt_source(n, d)}. The heating season here adds up to {d['hdd']:,} degree days, {hdd_line(d)}.")
        + "</p><p>" + V("fs2", "Oversized furnaces are common in Ontario homes. A furnace that is too big heats the air near the thermostat, shuts off, and starts again a few minutes later. You get uneven rooms, more noise and a shorter life. We calculate your home's heat loss at the design temperature and pick the size from that, not from the old unit's label.",
                              "Matching the old furnace's size is the easy way to get it wrong, because many older furnaces were oversized. Too big means short runs, hot and cold rooms and extra wear. We calculate the heat loss at the design temperature and size from that.")
        + "</p>" + checklist(V("fs3", ["Heat loss calculated at your design temperature", "Two-stage or variable-speed so it runs low and quiet most of the winter", f"Intake and exhaust set above {N} snow line", "Condensate drain routed so it cannot freeze"],
                                      [f"Heat loss worked out for {t}", "Two-stage or variable-speed for long, quiet, even heat", "Vent pipes above the snow line", "A condensate drain that will not freeze"]))
        + "<p>" + V("fs4", f"Thinking about lower gas bills too? A <a href='/{s}/heat-pump/'>heat pump paired with your new furnace</a> heats most of the year and leaves the furnace for the cold snaps.",
                         f"Replacing anyway? Ask for a price on a <a href='/{s}/heat-pump/'>heat pump to pair with it</a>. It handles most of the season and your cooling, and the furnace covers the coldest days.") + "</p>")

    snapshot = {"type": "snapshot", "h2": V("snap-h", f"Furnace numbers for {n}", f"{N} furnace sizing numbers"),
       "lead": V("snap-l", "What we size and install to, from the Ontario Building Code.", "The Building Code figures behind every furnace we quote here."),
       "items": [
        {"icon": "snow", "label": "January design temperature", "value": t,
         "text": (f"SB-1 figure for {n}. A new furnace is sized for your home's heat loss at this temperature." if d["listed"]
                  else f"SB-1 has no separate entry for {n}, so we use nearby {' and '.join(dict.fromkeys(d['src']))}. A new furnace is sized for your heat loss at {t}.")},
        {"icon": "flame", "label": "Heating degree days", "value": f"{d['hdd']:,}", "text": cap(hdd_line(d)) + "."},
        {"icon": "house", "label": "Ground snow load", "value": f"{d['snow']} kPa",
         "text": {"heavy": "Vent pipes go well above grade, where drifts and roof snow cannot bury them.", "moderate": "Vent pipes go above the usual snow line so storms do not shut the furnace down.",
                  "light": "Less snow, but vents still sit clear of drifts and roof run-off."}[sc]},
        {"icon": "phone", "label": "Gas emergency", "value": ENBRIDGE_EMERGENCY, "text": f"{c['gas']} 24-hour line. Smell gas? Leave first, then call it or 911 from outside."}]}
    checks_b = {"type": "steps", "h2": "No heat right now? Check these 5 things first", "cta": "Book a Furnace Repair",
                "lead": f"Smell gas or hear a CO alarm? Skip the list, leave the house and call 911 or Enbridge Gas at {ENBRIDGE_EMERGENCY} from outside.", "items": checks}
    problems = {"type": "problems", "h2": V("prob-h", f"Furnace problems we fix in {n} winters", f"What we find when a {n} furnace stops", f"Common {n} furnace failures and the fix"),
                "lead": V("prob-l", "What each symptom usually means, and what we do about it.", "Match the symptom, then call us with it. It speeds up the repair.") + " " + cold_risk, "items": items}
    table = {"type": "table", "h2": V("rr-h", f"Repair or replace your {n} furnace?", f"Fix it or replace it? How we call it in {n}"),
       "lead": V("rr-l", "We give you both prices in writing and tell you which we would choose. This is how we decide.", "You always get both numbers in writing. This is the reasoning behind our recommendation."),
       "headers": ["What we find", "Usually", "Why"],
       "rows": [["Flame sensor, ignitor, capacitor or pressure switch", "Repair", V("r1", "Low-cost parts, and the furnace has years left", "Small parts, small bill, plenty of life left")],
                ["Inducer or blower motor on a furnace under 12 years old", "Repair", V("r2", "Worth fixing while the rest of the furnace is sound", "The rest of the furnace is still good")],
                ["Control board or blower motor on a furnace over 15 years old", "Usually replace", V("r3", "A big repair on an old furnace is often the first of several", "Old furnaces rarely stop at one big repair")],
                ["Cracked heat exchanger", "Replace", V("r4", "A carbon monoxide risk, and rarely worth the cost to fix", "A carbon monoxide hazard, and not economical to repair")],
                ["Mid-efficiency (80%) furnace with repeated calls", "Replace", V("r5", "A 96% to 97% AFUE furnace cuts gas use and resets the warranty", "A 96% to 97% AFUE model burns less gas and comes with a new warranty")],
                ["Rooms that never heat evenly", "Fix the ducts first", V("r6", "A new furnace on the same ducts gives the same cold rooms", "The ducts, not the furnace, are usually the cause")]],
       "note": "Our rule of thumb: if the furnace is under about 12 years old and the repair is under a third of a new furnace, repair it."}
    sizing_b = {"type": "split", "h2": V("fs-h", f"Sizing a new furnace for {n}", f"Getting the furnace size right for {t}"), "photo": "sys", "photo_keys": FURNACE_PHOTOS, "reverse": True, "html": sizing_html,
                "shot": f"New high-efficiency gas furnace installed in a {n} basement, PVC venting and condensate line visible"}
    cost = {"type": "cost_guide", "h2": V("cost-h", f"Furnace repair and replacement costs in {n}", f"What furnace work costs in {n}"), "keys": ["furnace_repair", "furnace_install"],
            "lead": V("cost-l", "Repairs are priced in writing after diagnosis. A new furnace is quoted from your heat loss, venting and gas line, and the price is guaranteed.",
                                "You see the repair price before we start. A replacement is quoted from your heat loss, venting and gas line, and that price does not move.")}
    replace = {"type": "steps", "h2": V("rp-h", f"When a {n} furnace needs replacing", f"Replacing a furnace in {n}: what happens"), "cta": "Get My Furnace Price",
       "items": [
        {"title": V("rp1t", "Diagnosis and two prices", "Two written prices"), "text": V("rp1", "We confirm the fault, then give you the repair price and the replacement price in writing.", "We pin down the fault and put both options, repair and replace, in writing.")},
        {"title": V("rp2t", "Sizing and model choice", "The right size"), "text": V("rp2", f"Heat loss at {t}, then a Lennox or Midea two-stage furnace sized to match, with model numbers on the quote.", f"We size from your heat loss at {t} and list the exact two-stage model on the quote.")},
        {"title": "Install day", "text": V("rp3", "Old furnace out, new one in, with venting, gas connection, condensate drain and filter rack done to code by TSSA-certified techs.", "TSSA-certified techs remove the old unit and install the new one, venting, gas, condensate drain and all, to code.")},
        {"title": V("rp4t", "Startup and safety checks", "Tested before we leave"), "text": V("rp4", "Combustion test, carbon monoxide check, thermostat setup and warranty registration before we leave.", "We run a combustion test and a CO check, set up the thermostat and register the warranty in your name.")}]}
    equip = {"type": "equipment", "h2": V("eq-h", f"Furnaces we install in {n}", f"High-efficiency furnaces for {n} homes"), "groups": ["furnaces"],
             "lead": "High-efficiency two-stage furnaces with long parts warranties when registered. We register them for you."}
    visit = {"type": "checklist", "h2": V("v-h", f"What a {n} furnace repair visit includes", f"Your {n} furnace repair visit"), "photo": "sys", "photo_keys": FURNACE_PHOTOS,
             "shot": "Technician with the furnace door off, testing the flame sensor or ignitor with a meter",
             "items": V("v", ["A TSSA-certified technician who reads the fault code and tests it with a meter", "A written price before any part is replaced",
                              "Common parts on the truck: ignitors, flame sensors, pressure switches, capacitors", "Carbon monoxide test at the furnace and the supply registers",
                              "Filter, vent pipes and condensate drain checked while we are there", "Honest repair or replace advice, with both prices in writing"],
                             ["A TSSA-certified gas technician", "Fault codes read and confirmed with meter readings", "The price in writing before any part goes in",
                              "Ignitors, flame sensors, pressure switches and capacitors carried on the truck", "A carbon monoxide test before we leave", "Vents, filter and condensate drain checked on every call"])}

    cost["keys"] = ["furnace_install"]
    cost["h2"] = V("ci-h", f"What a new furnace costs in {n}", f"Furnace installation prices in {n}")
    cost["lead"] = V("ci-l", "A new furnace is quoted from your heat loss, venting and gas line, and the price is guaranteed in writing.", "Your quote is built from the heat loss, venting and gas work, and the number does not move.")
    install_incl = {"type": "checklist", "h2": V("ii-h", f"What is included in a {n} furnace installation", f"Everything in your {n} furnace quote"),
       "items": V("ii", [f"Heat-loss sizing at {t} and a written, guaranteed price", "Removal and disposal of the old furnace", "PVC intake and exhaust venting set above the snow line",
                         "Gas connection and leak test by TSSA-certified gas technicians", "Condensate drain routed so it cannot freeze", "New filter rack and thermostat setup",
                         "Combustion test and carbon monoxide check at start-up", "Warranty registration in your name"],
                        [f"A heat-loss calculation for {t} and one fixed price", "The old furnace taken out and disposed of", "New venting, terminated above the snow line",
                         "Gas work and leak testing by TSSA-certified technicians", "A freeze-proof condensate drain", "Filter rack, thermostat and settings done",
                         "Start-up combustion and CO testing", "The manufacturer warranty registered for you"])}
    signs = {"type": "problems", "h2": V("sg-h", f"Signs your {n} furnace is due for replacement", "When replacing beats another repair"),
       "lead": V("sg-l", "One of these on its own is not a verdict. Two or three together usually are.", "If you recognise several of these, get a replacement price next to the next repair quote."),
       "items": [
        {"problem": V("g1h", "It is 15 years old or more", "Fifteen-plus years of service"), "solution": V("g1", "Furnaces in Ontario homes commonly last 15 to 20 years. Past 15, big repairs start to cost more than they are worth.", "At that age, each repair buys less time. We look at the heat exchanger, motors and controls and tell you honestly how much life is left.")},
        {"problem": V("g2h", "Repairs every winter", "Another call, another part"), "solution": V("g2", "When the same furnace needs a part every season, the money is better spent on a new one with a fresh warranty.", "Repeated repairs add up. Put the last two years of repair bills next to a replacement price and the choice is usually clear.")},
        {"problem": V("g3h", "Gas bills keep rising", "Higher bills for the same house"), "solution": V("g3", "An older 80% furnace sends a fifth of the heat up the vent. A 96% to 97% AFUE furnace keeps almost all of it.", "Older mid-efficiency furnaces waste far more heat up the vent than a 96% to 97% AFUE condensing model.")},
        {"problem": V("g4h", "Yellow, flickering flame or soot", "Soot marks or a lazy yellow flame"), "solution": V("g4", "That can mean incomplete combustion and a carbon monoxide risk. Test your CO alarm and call us to inspect it.", "Get it checked now. It can point to a combustion problem, and we test for carbon monoxide on the visit.")},
        {"problem": V("g5h", "A cracked heat exchanger", "The technician found a crack"), "solution": V("g5", "A cracked heat exchanger can leak combustion gases into the air you breathe. On most furnaces it means replacement.", "Replacing a heat exchanger rarely makes financial sense, and running a furnace with one cracked is a carbon monoxide risk.")}]}
    rep_cost = {"type": "cost_guide", "h2": V("cr-h", f"Furnace repair costs in {n}", f"What a {n} furnace repair costs"), "keys": ["furnace_repair"],
                "lead": V("cr-l", "Repairs are priced in writing after diagnosis, before any part goes in.", "We find the fault first, then you get the price in writing.")}
    blocks = ([part("installation", "Installation", "install", V("pk1", "Installation", "New furnace"), V("ph1", f"Furnace installation in {n}", f"Installing a new furnace in {n}"),
                    V("pl1", f"Sizing, models, cost and what is included in a new furnace for a {n} home.", f"How we size and install a high-efficiency furnace in {n}."))]
              + V("order", [snapshot, sizing_b, cost, equip, install_incl], [snapshot, cost, sizing_b, install_incl, equip], [sizing_b, snapshot, cost, install_incl, equip])
              + [part("replacement", "Replacement", "clock", V("pk2", "Replacement", "Replacing a furnace"), V("ph2", f"Furnace replacement in {n}", f"Replacing an old furnace in {n}"),
                      V("pl2", "How we decide between repair and replacement, and how a replacement goes.", "When it is time, and what happens on replacement day.")),
                 signs, table, replace,
                 part("repair", "Repair & Maintenance", "wrench", V("pk3", "Repair and maintenance", "No heat? Start here"), V("ph3", f"Furnace repair and maintenance in {n}", f"No heat in {n}? Furnace repair"),
                      V("pl3", "Checks to do right now, what each symptom means, and what a repair visit covers.", "Start with the five checks, then match your symptom below.")),
                 checks_b, problems, rep_cost, visit, {"type": "money"}])

    title = fit([f"Furnace Installation & Replacement {n} | Repair", f"Furnace Installation & Replacement {n}", f"Furnace Installation {n} | Replacement", f"Furnace Installation {n}"], 60)
    desc = fit([f"Furnace installation in {n} from $3,300: 96% AFUE, sized for {t}. Replacement priced in writing, and repair evenings and weekends.",
                f"Furnace installation in {n} from $3,300, sized for {t}. Replacement and repair evenings and weekends.",
                f"Furnace installation, replacement and repair in {n}. New furnaces from $3,300."], 155)
    near = [u for u in (nearby_link(x, "furnace") for x in c["nearby"]) if u]
    return {
     "url": f"/{s}/furnace/", "city_service": s, "priority": "0.7", "heating": True,
     "title": title, "description": desc, "eyebrow": f"Furnaces · {n}", "h1": f"Furnace Installation, Replacement and Repair in {n}",
     "tagline": V("tag", f"High-efficiency furnaces sized for {t}, and straight answers when one stops", f"New furnaces from $3,300, replacement priced honestly, repair when you need it", f"The right furnace for {t}, installed and backed in writing"),
     "intro": "<p>" + V("intro",
        f"Whether you are planning a new furnace or replacing one that has given up, the starting point is the same: the right size for {N} {t} design temperature and one written price. Here is how we do it, what it costs, and when a repair still makes sense.",
        f"A new furnace for a {n} home should be sized for {t}, quoted in writing and installed to code. This page covers installation first, then replacement, then repair.",
        f"Planning a furnace for your {n} home? Below are the sizing numbers, prices and what is included, followed by how we handle replacement and repair.")
        + " <a href='#repair'>No heat right now? Jump to the five checks.</a></p>",
     "hero_points": ["New 96% to 97% AFUE furnaces from $3,300 installed", f"Sized from a heat-loss calculation at {t}",
                     "Replacement priced in writing next to the repair", "Emergency repair evenings, weekends and holidays by TSSA-certified techs"],
     "hero_image": f"Technician repairing a high-efficiency gas furnace in a {n} basement",
     "service": {"name": f"Furnace Repair and Installation in {n}", "type": "Furnace repair and replacement", "area": n},
     "blocks": blocks,
     "faqs": [
      (f"How much does a new furnace cost in {n}?",
       V("q0", f"High-efficiency furnace installation in {n} starts at $3,300 installed for a 96% to 97% AFUE two-stage furnace. The final price depends on size, venting and gas line work, and you get it in writing, guaranteed, after the home visit.",
               f"New 96% to 97% AFUE furnaces in {n} start at $3,300 installed. Size, venting changes and gas work set the final number, which we guarantee in writing.")),
      (f"How much does furnace repair cost in {n}?",
       V("q1", f"Furnace repair in {n} is priced in writing after diagnosis, because it depends on the failed part. Flame sensors, ignitors and capacitors are at the low end, blower and inducer motors and control boards cost more. If replacement is the better choice, a new high-efficiency furnace starts at $3,300 installed.",
               f"It depends on the part, so we diagnose first and give you the price in writing. Sensors, ignitors and capacitors are inexpensive; motors and control boards cost more. A new high-efficiency furnace in {n} starts at $3,300 installed.")),
      (f"What size furnace does a {n} home need?",
       V("q2", f"It depends on your home's heat loss at {t}, {dt_source(n, d)}. We calculate it from your walls, attic, windows and air leakage. The right furnace is often smaller than the one you are replacing, because many older furnaces were oversized.",
               f"The size that matches your heat loss at {t}, {dt_source(n, d)}. We work it out from your insulation, windows and air leakage, and it is often smaller than the old furnace.")),
      (f"Do you do emergency furnace repair in {n}?",
       V("q3", f"Yes. We take no-heat calls from {n} evenings, weekends and holidays. Tell us the symptom and whether anyone vulnerable is in the home, and we will tell you honestly when a technician can be there.",
               f"Yes, evenings, weekends and holidays. Call with the symptom and let us know if anyone in the home is elderly, very young or unwell, and we will give you an honest arrival time.")),
      ((f"Why does my furnace stop working when it snows in {n}?" if sc != "light" else f"Why is there water around my furnace in {n}?"),
       (V("q4", f"Most often the two white plastic vent pipes outside are covered by snow or ice, and the furnace shuts down for safety. Clear them by hand. If they get buried regularly, they are set too low for {N} snow and we can raise them.",
                f"Snow or ice over the vent pipes outside. The furnace senses the blockage and shuts down. Clear them by hand, and if it keeps happening, the pipes need to sit higher for {N} snow.") if sc != "light" else
        V("q4", "High-efficiency furnaces produce water while they run. When the condensate trap clogs or the drain line freezes or cracks, water collects and the furnace shuts down. We clean the trap and fix the drain line so it stays clear all winter.",
                "It is condensate. High-efficiency furnaces drain water, and a clogged trap or a frozen or cracked drain line makes it pool. We clear the trap and fix the line."))),
      (f"Is it worth adding a heat pump when I replace my furnace in {n}?",
       V("q5", "Often, yes. A cold-climate heat pump paired with the new furnace heats most of the year and replaces your air conditioner, and the furnace takes over in the deep cold. Gas-heated homes commonly get up to $2,000 back, and homes on propane or oil up to $7,500, with pre-approval before installation.",
               f"For many {n} homes, yes. The heat pump becomes your air conditioner and your main heat for most of the year, with the new furnace as cold-weather backup. The rebate is commonly up to $2,000 for gas-heated homes and up to $7,500 for propane or oil, with pre-approval first."))],
     "related": [f"/{s}/heat-pump/", f"/{s}/", "/furnace/high-efficiency/", "/furnace/repair-maintenance/", "/services/emergency-hvac/"] + near[:1],
    }

# ---------------------------------------------------------------- tankless water heater page
def tankless_page(c):
    s, n = c["slug"], c["name"]; d = CLIMATE[s]; b = band(d); sc = snow_class(d); t = deg(d["dt"]); V = chooser(s + "/tl"); N = poss(n)
    north = b in ("cold", "severe")
    gasline = (f"Homes in {n} on propane can have the same Rinnai units in their propane versions." if off_gas(c) else f"Most {n} homes are on {c['gas']}; a few are on propane, and Rinnai makes both versions.")

    snapshot = {"type": "snapshot", "h2": V("snap-h", f"Tankless numbers for {n}", f"What a tankless has to handle in {n}"),
       "lead": V("snap-l", "Sizing and installation details that change from town to town.", "The local facts we plan a tankless install around."),
       "items": [
        {"icon": "water", "label": "Winter inlet water", "value": "Single digits °C",
         "text": V("in1", "Incoming water in an Ontario winter can drop into the single digits Celsius, so we size for the temperature rise in February, not July.", "Cold winter water means a bigger temperature rise, which cuts the flow a tankless can deliver. We size for it.")
                 + (" Wells up north run colder still." if north else "")},
        {"icon": "snow", "label": "January design temperature", "value": t, "text": f"Sets how we protect the unit and its venting from freezing in {n}."},
        {"icon": "house", "label": "Ground snow load", "value": f"{d['snow']} kPa", "text": "Vent terminations go above the snow line so drifts cannot shut the heater down."},
        {"icon": "dollar", "label": "Installed price", "value": "From $3,300", "text": "Rinnai RX160iN condensing, with a guaranteed written quote."}]}
    why = {"type": "problems", "h2": V("why-h", f"Why {n} homeowners switch to tankless", f"What a tankless fixes in a {n} home", f"Is tankless right for your {n} home?"),
       "lead": V("why-l", "The problems a tank cannot solve, and what changes when you go tankless.", "Short answers to the reasons people call us."),
       "items": [
        {"problem": V("w1h", "Running out of hot water", "The last shower is always cold"), "solution": V("w1", "A 40 or 50 gallon tank has a hard limit. A tankless heats water as it flows, up to about 9 GPM on the RX160iN and 11.1 GPM on the RX199iN, so a shower lasts as long as you want.",
                                                                                                      "A tank holds a fixed amount and then you wait. A tankless heats on demand, so back-to-back showers and a running dishwasher are not a problem when it is sized right.")},
        {"problem": V("w2h", "Paying a rental fee every month", "A rented tank you will never own"), "solution": V("w2", "A rented tank can cost more over fifteen years than buying a tankless outright. We install a Rinnai you own and help arrange the return of the rental unit. Check your rental agreement for any buyout or removal terms first.",
                                                                                                                 "Rental fees never end. A Rinnai you own replaces them, and we help you return the old tank. Read your rental contract for buyout or removal terms before we book.")},
        {"problem": V("w3h", "The tank is leaking or rusting at the base", "Rust and water around the tank"), "solution": V("w3", "That tank is near the end. A wall-mounted tankless has no tank to rust through, and we can usually replace a failing tank with a tankless in one visit.",
                                                                                                                       "Do not wait for the long weekend it lets go. A tankless has no tank to fail, and most swaps are done in a day.")},
        {"problem": V("w5h", f"Will a tankless suit my kind of {n} home?", f"Tankless in an older or newer {n} house"),
         "solution": V("w5", f"Homes in {n} range from {c['housing']}. The questions are the same in all of them: where the vent can exit, whether the gas line can feed the burner, and how many bathrooms run at once. We answer all three on the assessment.",
                             f"In {n} we see {c['housing']}. Older homes often need a new vent route because the tank used the chimney; newer ones may need a bigger gas line. Both go on the quote before you decide.")},
        {"problem": V("w4h", "No room in the basement", "The tank takes up a corner of the room"), "solution": V("w4", "A Rinnai is about the size of a suitcase and hangs on the wall, freeing the floor space a tank used.",
                                                                                                                  "The unit mounts on the wall, so the floor space the tank used is yours again.")}]}
    sizing_html = ("<p>" + V("sz1",
        "Tankless sizing is about temperature rise. To deliver a 49°C shower from 5°C winter water, the heater has to raise it about 44°C, and a tankless unit's flow rate falls as the required rise climbs. The GPM on the box is a best case at a small rise.",
        "What matters is how much the heater has to warm the water. From 5°C winter water to a 49°C shower is a rise of about 44°C, and the bigger the rise, the less flow any tankless can deliver. Brochure GPM figures assume much warmer water.")
        + (f" {n} homes on wells, and inlet water further north, can run colder still, so we size with a margin." if north else "") + "</p><p>"
        + V("sz2", "So we count what you run at once in February: a shower uses roughly 2 to 2.5 GPM, a kitchen tap about 1.5 and a washing machine about 2. Two showers and a dishwasher together is a job for the RX199iN; one shower and a tap is fine on the RX160iN.",
                   "We size from your real peak: about 2 to 2.5 GPM per shower, 1.5 for a kitchen tap, 2 for the washer. One shower plus a tap fits the RX160iN. Two showers and the dishwasher at once needs the RX199iN.")
        + "</p>" + checklist(V("sz3", ["Fixtures that run at the same time counted", "Winter inlet temperature checked", "Gas line and meter capacity checked for the burner", "Venting route planned above the snow line"],
                                      ["Your peak hot water use, fixture by fixture", "The temperature rise for February water", "Gas supply sized for up to 199,000 BTU", "A vent route clear of snow and windows"])))
    sizing_b = {"type": "split", "h2": V("sz-h", f"Sizing a tankless for {n} winter water", "How we pick the right Rinnai"), "html": sizing_html,
                "image": "Rinnai condensing tankless water heater mounted on a wall", "image_src": RINNAI["unit"], "image_fit": "contain",
                "shot": f"Finished Rinnai tankless on a basement wall in a {n} home: isolation valves, gas line and PVC venting visible"}
    video = {"type": "video", "h2": V("vid-h", "Watch a tankless installation", "See a tankless install"), "lead": "A 39-second look at a compact, wall-mounted tankless install by EHI.", "items": [("rD0_LoGYAmo", "")]}
    cost = {"type": "cost_guide", "h2": V("cost-h", f"What a tankless water heater costs in {n}", f"Tankless prices in {n}"), "keys": ["tankless_install"],
            "lead": V("cost-l", "The RX199iN, propane set-ups, gas line upsizing and recirculation add to the starting price. Your quote is guaranteed in writing.", "Starting price for the RX160iN. Bigger models, gas line work and recirculation are quoted on the visit."),
            "note": "Installed pricing depends on the model, venting route and gas line work, and every job gets a written, guaranteed quote. Financing runs 0% for 3, 6 or 9 months on approved credit."}
    equip = {"type": "equipment", "h2": V("eq-h", f"Rinnai tankless water heaters we install in {n}", f"Tankless models for {n} homes"), "groups": ["water_heaters"],
             "lead": V("eq-l", "Condensing units, natural gas or propane. We register the Rinnai warranty for you.", "Both run on natural gas or propane, and we register your warranty.")}
    steps = {"type": "steps", "h2": V("st-h", f"How a tankless install works in {n}", f"Your {n} tankless install, step by step"), "cta": "Book My Tankless Quote",
       "items": [
        {"title": V("s1t", "Assessment", "Home or video visit"), "text": V("s1", f"We count fixtures, check the gas line and meter, and walk the venting route, anywhere from {hoods(c)}. In-home or virtual, your choice.", f"Fixtures, gas supply and the vent route, checked in person or on a video call, across {n} including {hoods(c, 2)}.")},
        {"title": V("s2t", "Guaranteed quote", "One written price"), "text": V("s2", "Model, venting, gas work and any recirculation on one written quote.", "Everything on one quote, and that is the price you pay.")},
        {"title": "Install day", "text": V("s3", "Usually one day: old tank out, Rinnai in, gas and venting by TSSA-certified technicians.", "Most installs take a day, with TSSA-certified techs on the gas and venting.")},
        {"title": V("s4t", "Start-up and handover", "Ready to use"), "text": V("s4", "We set the temperature, show you the controls and isolation valves, and register your warranty.", "Temperature set, controls explained, warranty registered.")}]}
    incl = {"type": "checklist", "h2": V("in-h", f"What is included in a {n} tankless installation", f"Everything in your {n} tankless quote"),
       "image": "Rinnai tankless water heater installed in a garage", "image_src": RINNAI["garage"], "image_fit": "cover",
       "shot": f"Install day in a {n} home: old tank removed, new Rinnai on the wall, technician connecting the gas line",
       "items": V("in", ["Fixture count and winter inlet sizing, with a guaranteed quote", "Removal of the old tank and help returning a rental",
                         "Gas line sized for the burner, upsized where needed by TSSA-certified technicians", "Direct-vent PVC or polypropylene venting, terminated above the snow line",
                         "Condensate drain with a neutralizer, because condensing units make acidic condensate", "Isolation valves so the yearly descaling flush takes minutes",
                         "Start-up, temperature set and warranty registration"],
                        ["Sizing for your real winter use and one fixed price", "Old tank out, rental return arranged", "Gas supply checked and upsized if the burner needs it",
                         "New direct venting above the snow line", "A condensate neutralizer to protect your drains", "Service valves for easy descaling", "Start-up, settings and your Rinnai warranty registered"])}

    rp_table = {"type": "table", "h2": V("rp-h", "Repair it or replace it?", "Fix the water heater or replace it?"),
       "lead": V("rp-l", "We give you both prices and tell you which we would choose.", "Both options in writing, with our honest recommendation."),
       "headers": ["What we find", "Usually", "Why"],
       "rows": [["Tank leaking from the bottom", "Replace", V("r1", "A leaking tank cannot be repaired", "Once the tank itself leaks, it is done")],
                ["Rented tank, any age", "Replace with a tankless you own", V("r2", "Stops the rental fees for good", "No more monthly rental charge")],
                ["Tankless with scale and lukewarm water", "Descale and service", V("r3", "Scale is the most common tankless problem, and a flush usually fixes it", "A descaling flush restores the flow")],
                ["Tankless ignition or sensor fault", "Repair", V("r4", "Replaceable parts on a long-lived unit", "Fixable parts, plenty of life left")],
                ["Old tankless that has outlived its parts", "Replace", V("r5", "New condensing models are more efficient and come with a fresh warranty", "A new condensing unit and a new warranty")]]}
    rp_split = {"type": "split", "h2": V("rs-h", f"Replacing a tank with a tankless in {n}", "What changes when you replace a tank"), "reverse": True,
       "image": "Hot water running at a kitchen sink", "image_src": RINNAI["sink"], "image_fit": "cover",
       "shot": f"Before and after in a {n} basement: the old tank next to the new wall-mounted Rinnai",
       "html": "<p>" + V("rs1", "Three things change when a tank becomes a tankless, and the quote covers all of them.", "A tank-to-tankless swap is more than a one-for-one. Here is what the quote includes.") + "</p>"
               + checklist(V("rs2", ["Venting: the old chimney or B-vent is not used; a condensing Rinnai vents through PVC or polypropylene to an outside wall",
                                     "Gas: a 160,000 to 199,000 BTU burner often needs a larger gas line than a tank, and we check the meter too",
                                     "Space: the unit goes on the wall, often right where the tank was"],
                                    ["New venting through an outside wall in PVC or polypropylene, not the old chimney", "A gas line big enough for up to 199,000 BTU, checked back to the meter",
                                     "Wall mounting that frees the floor space"]))
               + f"<p>{gasline} See our <a href='/water-heater/'>tankless water heater guide</a> for the full details.</p>"}

    rep = {"type": "problems", "h2": V("rep-h", f"Tankless problems we fix in {n}", f"When your {n} tankless acts up"),
       "lead": V("rep-l", "What each symptom usually means and what we do about it.", "Match the symptom, then call us with it."),
       "items": [
        {"problem": V("p1h", "Lukewarm water when more than one tap runs", "Hot water fades with two showers"), "solution": V("p1", "Either scale has built up in the heat exchanger or the unit is too small for your peak use. A descaling flush fixes the first; resizing or adding a second unit fixes the second.",
                                                                                                                              "Usually scale, sometimes sizing. We flush the heat exchanger first, and if it still cannot keep up, we show you the numbers.")},
        {"problem": V("p2h", "Bursts of cold water in the shower", "Hot, then a cold blast, then hot"), "solution": V("p2", "That cold water sandwich happens when the unit stops and restarts between uses. A recirculation option or a setting change usually solves it.",
                                                                                                                   "It is the gap while the burner restarts. Recirculation or a small settings change fixes it in most homes.")},
        {"problem": V("p3h", "No hot water and an error code", "A code on the display, no hot water"), "solution": V("p3", "Take a photo of the code and call us. Common causes are ignition, gas supply, a blocked vent or a clogged inlet filter.",
                                                                                                                      "Send us the code. It usually points to ignition, gas supply, a vent blockage or the inlet filter, and we bring the right parts.")},
        ({"problem": V("p4h", "It stops after a snowstorm", "No hot water after heavy snow"), "solution": V("p4", f"Snow or ice over the vent outside. With a {d['snow']} kPa ground snow load in {n}, low terminations get buried. Clear it by hand, and if it keeps happening, we raise the vent.",
                                                                                                         f"The vent outside is blocked. {N} snow can bury a low termination, so clear it and ask us about raising it.")}
         if sc != "light" else
         {"problem": V("p4h", "Water dripping from the unit or the drain", "A drip under the heater"), "solution": V("p4", "Usually the condensate line or neutralizer is blocked. We clear it and check the connections.", "Most often a blocked condensate drain or neutralizer cartridge. Easy to fix.")}),
        {"problem": V("p5h", f"A power outage during a {t} cold snap", "The power is out and it is freezing"),
         "solution": V("p5", f"A tankless needs power for its freeze protection. If the house will be without power and heat in a {n} deep freeze, shut off the water and gas to the unit and drain it, or call us to do it.",
                             "Freeze protection runs on electricity. In a long outage in deep cold, shut off the water and gas to the heater and drain it, or call us.")}]}
    maint = {"type": "checklist", "h2": V("mt-h", f"Yearly tankless maintenance in {n}", "What a tankless service includes"),
       "lead": V("mt-l", "A yearly descaling flush keeps the flow up and the burner efficient. Homes with very hard water may need it more often.", "Once a year, or more often with hard water, keeps a tankless running like new."),
       "items": V("mt", ["Heat exchanger flushed with descaler through the isolation valves", "Inlet water filter cleaned", "Burner and flame checked", "Vent and air intake checked for blockages and snow",
                         "Condensate neutralizer checked", "Error history read and settings confirmed"],
                        ["Descaling flush of the heat exchanger", "Water inlet screen cleaned", "Combustion checked", "Venting inspected, inside and out", "Neutralizer cartridge checked", "Fault history and settings reviewed"])}

    install = V("order", [snapshot, why, sizing_b, video, cost, steps, equip, incl], [snapshot, sizing_b, why, cost, video, incl, steps, equip], [why, snapshot, video, sizing_b, cost, equip, steps, incl])
    blocks = ([part("installation", "Installation", "install", V("pk1", "Installation", "New tankless"), V("ph1", f"Tankless water heater installation in {n}", f"Installing a tankless water heater in {n}"),
                    V("pl1", "Sizing for winter water, cost, models and what the install includes.", f"How we size and install a Rinnai tankless in a {n} home."))]
              + install
              + [part("replacement", "Replacement", "clock", V("pk2", "Replacement", "Replacing a water heater"), V("ph2", f"Water heater replacement in {n}", f"Replacing a tank or tankless in {n}"),
                      V("pl2", "Replacing a leaking or rented tank, or an older tankless.", "When to replace, and what a tank-to-tankless swap involves.")),
                 rp_table, rp_split,
                 part("repair", "Repair & Maintenance", "wrench", V("pk3", "Repair and maintenance", "Service"), V("ph3", f"Tankless repair and maintenance in {n}", f"Keeping your {n} tankless running"),
                      V("pl3", "Common faults, what to do in a winter power outage, and yearly descaling.", "What to do when it acts up, and how to keep it from happening.")),
                 rep, maint, {"type": "money"}])

    title = fit([f"Tankless Water Heater Installation {n} | Rinnai", f"Tankless Water Heater Installation {n}", f"Tankless Water Heaters {n}"], 60)
    desc = fit([f"Tankless water heater installation in {n} from $3,300: Rinnai condensing, sized for winter water. Tank replacement and repair too. Free quote.",
                f"Tankless water heater installation in {n} from $3,300, plus tank replacement and repair. Free quote.",
                f"Tankless water heaters in {n} from $3,300 installed. Free quote."], 155)
    near = [u for u in (nearby_link(x, "tankless-water-heater") for x in c["nearby"]) if u]
    heat = [u for u in (f"/{s}/furnace/" if s in LIVE else (f"/{s}/furnace-repair/" if s in SKIP else None),) if u]
    return {
     "url": f"/{s}/tankless-water-heater/", "city_service": s, "priority": "0.6", "heating": True,
     "title": title, "description": desc, "eyebrow": f"Tankless Water Heaters · {n}", "h1": f"Tankless Water Heater Installation, Replacement and Repair in {n}",
     "tagline": V("tag", "Endless hot water, sized for February, priced in writing", "Rinnai tankless, sized for winter water and installed in a day", "Stop running out of hot water, and stop paying rent on a tank"),
     "intro": "<p>" + V("intro",
        f"A tankless water heater gives a {n} home hot water for as long as the taps run, as long as it is sized for winter inlet water. Here is how we size it, what it costs, and what a swap from a tank involves.",
        f"Tired of cold showers or a monthly rental fee? A Rinnai tankless fixes both, if it is sized for the cold water a {n} winter delivers. Installation first, then replacement and repair.",
        f"Thinking about tankless for your {n} home? Below: sizing for winter water, prices, the models we install, and what changes when you replace a tank.")
        + V("intro2", " Need a repair instead? Use the quick links below.", " Already have one that needs work? Jump to repair below.") + "</p>",
     "hero_points": ["Rinnai RX160iN and RX199iN condensing, 0.97 and 0.98 UEF", "From $3,300 installed, guaranteed written quote", "Old tank removed and rental return arranged", "Descaling, service and repair for tankless units"],
     "hero_image": f"Rinnai tankless water heater on a wall in a {n} home",
     "service": {"name": f"Tankless Water Heater Installation in {n}", "type": "Tankless water heater installation", "area": n},
     "blocks": blocks,
     "faqs": [
      (f"How much does a tankless water heater cost in {n}?",
       V("q1", f"Tankless water heater installation in {n} starts at $3,300 installed for a Rinnai RX160iN. The RX199iN, propane set-ups, gas line upsizing and recirculation add to that. You get a guaranteed written quote before any work.",
               f"From $3,300 installed in {n} for the RX160iN. A bigger RX199iN, gas line work, propane or recirculation is quoted on the visit, and the price is guaranteed.")),
      (f"What size tankless water heater does a {n} home need?",
       V("q2", "It depends on how many hot fixtures run at once and how cold your winter water gets. Most two-bathroom homes are fine on the RX160iN at up to about 9 GPM; three or more bathrooms, or a soaker tub, usually need the RX199iN at up to about 11.1 GPM.",
               "Count what runs at the same time in winter. One shower and a tap: the RX160iN. Two showers plus the dishwasher, or a big soaker tub: the RX199iN.")),
      (f"Can I replace a rented water tank with a tankless in {n}?",
       V("q3", f"Yes. We install a Rinnai you own and help arrange the return of the rental tank. Check your rental agreement for buyout or removal terms first, so there are no surprises.",
               f"Yes, and it is one of the most common jobs we do. You own the new unit, and we help with returning the rental. Read your rental contract's buyout or removal terms first.")),
      (f"Does a tankless water heater need a new gas line in {n}?",
       V("q4", f"Often. A 160,000 to 199,000 BTU burner can need a larger line than a tank used, so we check the line and meter on the assessment. {gasline}",
               f"Sometimes. Tankless burners draw far more gas than a tank, so we check the line back to the meter and include any upsizing in the quote. {gasline}")),
      (f"How often should a tankless be descaled in {n}?",
       V("q5", "Once a year for most homes, more often if your water is very hard. The isolation valves we install make the flush quick.",
               "Yearly is the usual rule, and more often with hard water. With service valves in place it is a short visit."))],
     "related": [f"/{s}/", "/water-heater/", "/brands/rinnai-tankless-water-heaters/", "/water-heater/repair-maintenance/"] + heat + near[:1],
    }

PAGES = []
for _c in CITIES:
    if _c["slug"] in LIVE:
        PAGES += [heat_pump_page(_c), furnace_page(_c)]
    if _c["slug"] in LIVE_TANKLESS:
        PAGES.append(tankless_page(_c))
