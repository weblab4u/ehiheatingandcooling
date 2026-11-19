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
    if slug in LIVE: return f"/{slug}/{kind}/"
    if slug in SKIP: return f"/{slug}/{'heat-pump-installation' if kind == 'heat-pump' else 'furnace-repair'}/"
    return None

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

    blocks = V("order",
        [snapshot, problems, table, place_b, sizing_b, cost, steps, equip, incl],
        [snapshot, table, problems, sizing_b, place_b, steps, cost, incl, equip],
        [problems, snapshot, table, sizing_b, cost, place_b, steps, equip, incl]) + [{"type": "money"}]

    title = fit([f"Heat Pump Installation {n} | Rebates & Sizing", f"Heat Pump Installation {n} | Cold Climate", f"Heat Pumps {n} | Install & Rebates", f"Heat Pumps {n}"], 60)
    desc = fit([f"Cold-climate heat pumps for {n} homes, sized for the {t} design day. Up to $7,500 back for electric, oil or propane homes. Free written quote.",
                f"Cold-climate heat pumps for {n}, sized for {t}. Up to $7,500 back for electric, oil or propane homes. Free written quote.",
                f"Heat pumps for {n}, sized for {t}. Up to $7,500 back for electric, oil or propane homes. Free quote."], 155)
    near = [u for u in (nearby_link(x, "heat-pump") for x in c["nearby"]) if u]
    return {
     "url": f"/{s}/heat-pump/", "city_service": s, "priority": "0.7", "heating": True,
     "title": title, "description": desc, "eyebrow": f"Heat Pumps · {n}", "h1": f"Heat Pump Installation in {n}",
     "tagline": V("tag", f"Sized for {N} {t} design day, rebate filed before install", f"Built for {t}, raised above the snow, rebate paperwork done for you", f"The right size for {t}, with your rebate filed first"),
     "intro": "<p>" + V("intro",
        f"Before you put a heat pump on a {n} house, you want two answers: will it keep you warm on the coldest night, and what does it cost after the rebate. Here are both, worked out with {N} own Building Code numbers, plus which setup suits the way your home is heated now.",
        f"Thinking about a heat pump for your {n} home this winter? Below are the numbers it has to meet, what it costs before and after the rebate, and which setup fits the way you heat today. No guesswork, just {N} own Building Code data.",
        f"A heat pump only works as well as its sizing. For {n} that means {t} on the coldest design day, so that is where we start. Here is how we size it, where the outdoor unit goes, what you pay and what you get back.") + "</p>",
     "hero_points": [f"Sized from a heat-loss calculation at {N} {t} design temperature",
                     "Cold-climate Midea and Kepler models rated to -30°C" + (", with full backup for colder nights" if below else ""),
                     "Up to $7,500 back for homes heated by electricity, oil or propane", "Rebate pre-approval filed before install day"],
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

    blocks = [checks_b] + V("order",
        [snapshot, problems, table, sizing_b, cost, replace, equip, visit],
        [problems, snapshot, table, cost, sizing_b, visit, replace, equip],
        [problems, table, snapshot, sizing_b, replace, cost, visit, equip]) + [{"type": "money"}]

    title = fit([f"Furnace Repair & Installation {n} | No Heat Help", f"Furnace Repair & Installation {n}", f"Furnace Repair {n} | No Heat Help", f"Furnaces {n}"], 60)
    desc = fit([f"No heat in {n}? TSSA-certified techs repair furnaces evenings and weekends. New 96% AFUE furnaces from $3,300 installed. Written price first.",
                f"No heat in {n}? Furnace repair evenings and weekends, new 96% AFUE furnaces from $3,300 installed. Written price first.",
                f"Furnace repair and new furnaces in {n} from $3,300 installed. Written price first."], 155)
    near = [u for u in (nearby_link(x, "furnace") for x in c["nearby"]) if u]
    return {
     "url": f"/{s}/furnace/", "city_service": s, "priority": "0.7", "heating": True,
     "title": title, "description": desc, "eyebrow": f"Furnaces · {n}", "h1": f"Furnace Repair and Installation in {n}",
     "tagline": V("tag", f"No heat at {t}? Here is what to check, and what we do next", f"No heat in {n}? Five checks first, then a straight answer", "Your furnace stopped. Here is the fastest way back to heat"),
     "intro": "<p>" + V("intro",
        f"If your furnace has stopped, you need two things: a few checks you can do in the next five minutes, and a technician who gives you a straight repair or replace answer. This page has both, plus what a new furnace costs and how we size one for {N} {t} design temperature.",
        f"No heat in {n}? Start with the five checks below; one of them fixes it more often than you would think. If not, we diagnose it, price it in writing and tell you honestly whether to repair or replace.",
        f"A furnace that quits in a {n} winter needs a quick, honest answer. Here is what to check yourself first, what the common faults mean, what repair and replacement cost, and how we size a new furnace for {t}.") + "</p>",
     "hero_points": ["TSSA-certified gas technicians, every major furnace brand", "Emergency furnace repair evenings, weekends and holidays",
                     "Written price before any part comes off the truck", "New 96% to 97% AFUE furnaces from $3,300 installed"],
     "hero_image": f"Technician repairing a high-efficiency gas furnace in a {n} basement",
     "service": {"name": f"Furnace Repair and Installation in {n}", "type": "Furnace repair and replacement", "area": n},
     "blocks": blocks,
     "faqs": [
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

PAGES = []
for _c in CITIES:
    if _c["slug"] in LIVE:
        PAGES += [heat_pump_page(_c), furnace_page(_c)]
