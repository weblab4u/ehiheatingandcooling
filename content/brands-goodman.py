# Goodman product pages under the Goodman main page (/brands/goodman/, in brands-main.py):
# /brands/goodman/furnaces/ and /brands/goodman/heat-pumps/, ordered installation, replacement, repair and maintenance.
# Specs from Goodman spec sheets: SS-GCVC96 11/23 (GMVC96 is the upflow version), SS-GMEC96, SS-GSXH5 07/22, SS-GSZH5 05/22.

def part(anchor, jump, icon, kicker, h2, lead):
    return {"type": "part", "anchor": anchor, "jump": jump, "icon": icon, "kicker": kicker, "h2": h2, "lead": lead}

FURNACES = {
 "url": "/brands/goodman/furnaces/", "priority": "0.8",
 "title": "Goodman Furnace Installation Ontario | GMVC96 & GMEC96",
 "description": "Goodman GMVC96 and GMEC96 furnace installation in Ontario by an authorized Goodman dealer. Up to 96% AFUE, from $3,300 installed. Replacement and repair too.",
 "eyebrow": "Goodman GMVC96 · GMEC96",
 "h1": "Goodman Furnace Installation, Replacement and Repair in Ontario",
 "tagline": "Two-stage Goodman furnaces at up to 96% AFUE, sized for your home",
 "intro": "<p>Want a Goodman furnace installed by an authorized Goodman dealer? We install the GMVC96 and GMEC96 two-stage gas furnaces across Ontario, size them from a heat-loss calculation, and register the warranty inside Goodman's 60-day window. Replacing an old furnace or need a repair? Use the quick links below.</p>",
 "hero_points": ["Goodman GMVC96 and GMEC96, two-stage, up to 96% AFUE", "40,000 to 120,000 BTU/h input, sized from your heat loss", "From $3,300 installed, guaranteed written quote", "Warranty registered online within Goodman's 60-day window"],
 "hero_image": "Gas furnace with a matched coil and supply plenum installed by EHI in an Ontario utility room",
 "hero_img": "/assets/img/work/furnace-coil-utility-room.webp", "hero_img_fit": "cover", "hero_img_credit": "EHI install",
 "service": {"name": "Goodman Furnace Installation", "type": "Gas furnace installation", "from_price": "3300"},
 "blocks": [
  part("installation", "Installation", "install", "Installation", "Goodman furnace installation", "Which Goodman furnace fits your home, what is included and what it costs."),
  {"type": "table", "h2": "Goodman furnaces we install", "headers": ["Model", "Staging and blower", "Efficiency", "Sizes"], "rows": [
    ["Goodman GMVC96", "Two-stage gas valve, variable-speed ECM blower", "Up to 96% AFUE", "40,000 to 120,000 BTU/h input"],
    ["Goodman GMEC96", "Two-stage gas valve, multi-speed ECM blower", "Up to 96% AFUE", "40,000 to 120,000 BTU/h input"]],
   "note": "Goodman furnace prices in Ontario start at $3,300 installed, with a guaranteed written quote. Your final price depends on size, venting, gas line and condensate work."},
  {"type": "cards", "h2": "GMVC96 or GMEC96?", "no_fill": True, "items": [
    {"icon": "furnace", "title": "GMVC96: quiet, even heat", "text": "Two-stage heat runs on low most of the winter and the variable-speed blower ramps up gently. The better partner for central air or a heat pump, because it moves air smoothly at every speed."},
    {"icon": "dollar", "title": "GMEC96: two-stage on a tighter budget", "text": "The same 96% AFUE and two-stage burner with a multi-speed ECM blower. A sensible upgrade from an old 80% furnace without the top-tier price."}]},
  {"type": "problems", "h2": "Problems a new Goodman furnace solves", "items": [
    {"problem": "An old 80% furnace burning through gas", "solution": "An 80% furnace sends a fifth of the heat up the chimney. A Goodman at up to 96% AFUE keeps almost all of it, and on an Ontario winter gas bill that difference shows every month."},
    {"problem": "The house swings from too hot to too cold", "solution": "Single-stage furnaces blast at full fire, then shut off. Goodman's two-stage gas valve runs on low for long, steady cycles that hold the temperature where you set it."},
    {"problem": "A loud blower every time the heat comes on", "solution": "The GMVC96's variable-speed blower starts slowly and runs quietly at low speed, so you hear far less of it than an older single-speed blower."}]},
  {"type": "checklist", "h2": "What is included in a Goodman furnace installation", "items": [
    "Heat-loss calculation to pick the right Goodman size", "Removal and disposal of your old furnace", "PVC intake and exhaust venting and a condensate drain",
    "Gas connection, leak test and combustion check by TSSA-certified gas technicians", "Filter rack, thermostat setup and a walk-through of your new system",
    "Goodman warranty registration online within the 60-day window, and permits where required"]},
  part("replacement", "Replacement", "clock", "Replacement", "Replacing a furnace with a Goodman", "When a repair still makes sense, and when replacing is the better money."),
  {"type": "table", "h2": "Repair or replace your furnace?", "lead": "We price both in writing and tell you which we would choose.", "headers": ["What we find", "Usually", "Why"], "rows": [
    ["Flame sensor, ignitor, capacitor or pressure switch", "Repair", "Low-cost parts on a furnace with life left"],
    ["Inducer or blower motor on a furnace under 12 years old", "Repair", "The rest of the furnace is still sound"],
    ["Control board or blower motor on a furnace over 15 years old", "Usually replace", "A big repair on an old furnace is often the first of several"],
    ["Cracked heat exchanger", "Replace", "A carbon monoxide risk, and rarely worth fixing"],
    ["Mid-efficiency (80%) furnace with repeated calls", "Replace", "A Goodman at up to 96% AFUE cuts gas use and resets the warranty"]],
   "note": "Our rule of thumb: under about 12 years old and the repair is under a third of a new furnace, repair it."},
  {"type": "steps", "h2": "How a Goodman furnace replacement goes", "cta": "Get My Goodman Price", "items": [
    {"title": "Diagnosis and two prices", "text": "We confirm the fault and give you the repair and replacement prices in writing."},
    {"title": "Sizing", "text": "A heat-loss calculation picks the GMVC96 or GMEC96 size, not the old furnace's label."},
    {"title": "Install day", "text": "Old furnace out, Goodman in, venting, gas and condensate done to code. Usually one day."},
    {"title": "Start-up and registration", "text": "Combustion and carbon monoxide checks, thermostat setup, and the warranty registered online."}]},
  part("repair", "Repair & Maintenance", "wrench", "Repair and maintenance", "Goodman furnace repair and maintenance", "We service Goodman furnaces of any age, whoever installed them."),
  {"type": "problems", "h2": "Goodman furnace problems we fix", "items": [
    {"problem": "Clicks and tries to light, then shuts off", "solution": "Usually a dirty flame sensor, a failing hot surface ignitor or a pressure switch that will not close. Common parts, often fixed on the first visit, priced in writing first."},
    {"problem": "Blower runs but the air is cold", "solution": "The furnace has locked out after failed ignition or tripped a limit switch from a blocked filter. We find the cause rather than resetting it and leaving."},
    {"problem": "A flashing status light", "solution": "Goodman furnaces flash a fault code on the control board. We read it, confirm it with meter readings and fix the actual fault."},
    {"problem": "Shuts down after snow or wind", "solution": "Blocked intake or exhaust pipes outside. Clear them by hand; if they keep getting buried, we raise them above the snow line."}]},
  {"type": "checklist", "h2": "What a Goodman furnace tune-up includes", "lead": "Once a year, ideally in the fall. See <a href='/furnace/repair-maintenance/'>furnace repair and maintenance</a> for more.", "items": [
    "Flame sensor cleaned and ignitor tested", "Burners, inducer and blower checked", "Condensate trap and drain cleared", "Venting checked inside and out",
    "Gas pressure and combustion tested", "Carbon monoxide check and a fresh filter"]},
  {"type": "money"}, {"type": "why"}, {"type": "areas"}],
 "faqs": [
  ('Do you do Goodman furnace repair in Toronto, Mississauga, Oakville and Milton?', 'Yes. We repair Goodman furnaces across the GTA, including Toronto, Mississauga, Oakville and Milton, and the rest of our Ontario service area. You get a diagnosis and a written price before any work.'),
  ("How much does a Goodman furnace cost installed?", "Our gas furnace installs start from $3,300, and the price for a Goodman furnace depends on the size, the model and the installation needs, such as venting, condensate drain and gas line work. You get a written, guaranteed quote with the exact model number before any work starts."),
  ("What is the difference between the Goodman GMVC96 and GMEC96?", "Both are two-stage Goodman gas furnaces at up to 96% AFUE with 40,000 to 120,000 BTU/h inputs. The GMVC96 has a variable-speed ECM blower that ramps airflow smoothly and works well with central air or a heat pump, while the GMEC96 uses a multi-speed ECM blower and usually costs less."),
  ("What warranty comes with a Goodman furnace?", "Goodman's better furnaces carry a heat exchanger limited warranty for as long as you own your home, plus 10-year unit replacement and 10-year parts limited warranties, when registered online within 60 days of installation. We register it for you."),
  ("Do you repair Goodman furnaces you did not install?", "Yes. We repair and maintain Goodman furnaces no matter who installed them, with a diagnosis and a written price before any work."),
  ("Can a Goodman furnace work with a heat pump?", "Yes. A Goodman furnace, especially the variable-speed GMVC96, pairs with a heat pump as a hybrid system: the heat pump heats most of the year and the furnace covers the coldest days.")],
 "related": ["/brands/goodman/", "/brands/goodman/heat-pumps/", "/furnace/", "/furnace/high-efficiency/", "/furnace/repair-maintenance/", "/financing/"],
}

HEAT_PUMPS = {
 "url": "/brands/goodman/heat-pumps/", "priority": "0.8",
 "title": "Goodman Heat Pump Installation Ontario | GSZH5",
 "description": "Goodman GSZH5 heat pump installation in Ontario by an authorized Goodman dealer. 1.5 to 5 ton, up to 15.2 SEER2. Hybrid setups, replacement and repair.",
 "eyebrow": "Goodman GSZH5 Heat Pump",
 "h1": "Goodman Heat Pump Installation, Replacement and Repair in Ontario",
 "tagline": "Heating and cooling from one outdoor unit, paired with your furnace",
 "intro": "<p>A Goodman GSZH5 heat pump cools like central air in summer and heats your home through the shoulder seasons and milder winter days. In an Ontario winter we pair it with a gas furnace as a hybrid, so the furnace takes over in the deep cold. If you want a heat pump to carry the house alone at -25°C, we will tell you honestly that a cold-climate model is the better choice.</p>",
 "hero_points": ["Goodman GSZH5, 1.5 to 5 ton", "Up to 15.2 SEER2 and 7.8 HSPF2, SmartShift defrost", "Best as a hybrid with a Goodman or existing gas furnace", "Warranty registered online within Goodman's 60-day window"],
 "hero_image": "Outdoor heat pump on a raised stand above the lawn",
 "hero_img": "/assets/img/work/heat-pump-outdoor-lawn.webp", "hero_img_fit": "cover", "hero_img_credit": "EHI install",
 "service": {"name": "Goodman Heat Pump Installation", "type": "Heat pump installation"},
 "blocks": [
  part("installation", "Installation", "install", "Installation", "Goodman heat pump installation", "Who the GSZH5 suits, how we set it up for Ontario winters, and what is included."),
  {"type": "table", "h2": "The Goodman heat pump we install", "headers": ["Model", "Compressor", "Efficiency", "Sizes"], "rows": [
    ["Goodman GSZH5", "Single-stage scroll, SmartShift defrost", "Up to 15.2 SEER2, 7.8 HSPF2", "1.5 to 5 ton"]],
   "note": "Ratings are Goodman's published maximums; your rating depends on the matched coil or furnace. Every quote lists the exact model numbers and is guaranteed."},
  {"type": "cards", "h2": "Who a Goodman heat pump is right for", "no_fill": True, "items": [
    {"icon": "furnace", "title": "Gas-heated homes going hybrid", "text": "Keep or replace your gas furnace and add the GSZH5. The heat pump handles cooling and the milder heating days, and the furnace takes over below the balance point.", "link": "/heat-pump/hybrid-furnace-systems/", "link_text": "Hybrid systems"},
    {"icon": "ac", "title": "Replacing an old central AC", "text": "The GSZH5 goes where the air conditioner was, cools just as well, and adds heat for spring and fall.", "link": "/ac/", "link_text": "AC replacement"},
    {"icon": "heatpump", "title": "Want a heat pump to do it all?", "text": "For all-electric homes or the biggest Ontario rebate, a cold-climate model rated to -30°C is the better fit. We quote Midea or Kepler side by side.", "link": "/heat-pump/cold-climate/", "link_text": "Cold-climate heat pumps"}]},
  {"type": "checklist", "h2": "What is included in a Goodman heat pump installation", "items": [
    "Heat-loss and heat-gain sizing and a written, guaranteed price", "Outdoor unit on a raised stand or bracket above the snow line", "Matched indoor coil and a new line set where needed",
    "Vacuum and refrigerant charge by licensed refrigeration technicians", "Electrical disconnect and circuit by licensed electrical work", "Hybrid thermostat set-up and the furnace switchover temperature tuned",
    "Goodman warranty registration online within the 60-day window"]},
  part("replacement", "Replacement", "clock", "Replacement", "Replacing an AC or heat pump with a Goodman", "When to replace, and what the swap involves."),
  {"type": "table", "h2": "Repair or replace your AC or heat pump?", "headers": ["What we find", "Usually", "Why"], "rows": [
    ["Capacitor, contactor or fan motor", "Repair", "Common parts on a system with life left"],
    ["Compressor failure on a system over 10 years old", "Usually replace", "The most expensive part, on an aging system"],
    ["Air conditioner still running on R-22", "Replace", "New R-22 has not been made or imported in Canada since 2020, so recharges keep getting dearer"],
    ["Central AC 12 to 15 or more years old", "Replace with a heat pump", "Same footprint, and it adds heating"]],
   "note": "Ontario's heat pump rebate applies only to models on NRCan's qualified products list; we check the exact Goodman model before you buy."},
  {"type": "steps", "h2": "How a Goodman heat pump replacement goes", "cta": "Get My Goodman Price", "items": [
    {"title": "Visit and sizing", "text": "We check the old system, ducts, coil and electrical, and size the GSZH5 for your home."},
    {"title": "Written price", "text": "Model numbers, coil, line set and electrical on one guaranteed quote."},
    {"title": "Install day", "text": "Old refrigerant recovered, old unit out, Goodman in, charged and tested. Usually one day."},
    {"title": "Hybrid set-up and registration", "text": "Switchover temperature tuned with your furnace, and the warranty registered online."}]},
  part("repair", "Repair & Maintenance", "wrench", "Repair and maintenance", "Goodman heat pump repair and maintenance", "What is normal in winter, what is not, and what a tune-up covers."),
  {"type": "problems", "h2": "Goodman heat pump problems we fix", "items": [
    {"problem": "Steam and a whoosh from the outdoor unit", "solution": "That is SmartShift defrost melting frost off the coil, and it is normal. If it happens every few minutes, or ice keeps building, call us."},
    {"problem": "It is not keeping the house warm", "solution": "Check the thermostat mode and filter first. Then it is usually the switchover temperature, low refrigerant or a defrost fault. We test all three."},
    {"problem": "Not cooling in summer", "solution": "Often a failed capacitor or contactor, a dirty coil or a refrigerant leak. We diagnose with gauges and price the repair before we start."},
    {"problem": "Ice that will not clear", "solution": "Switch to your furnace or emergency heat and leave the ice alone. We repair the defrost fault and fix any drainage problem under the unit."}]},
  {"type": "checklist", "h2": "What a Goodman heat pump tune-up includes", "lead": "Once a year. See <a href='/heat-pump/repair-maintenance/'>heat pump repair and maintenance</a> for more.", "items": [
    "Coil and fan cleaned", "Refrigerant pressures checked with gauges", "Defrost cycle tested", "Capacitor and contactor tested", "Hybrid switchover checked", "Clearance and stand height checked for winter"]},
  {"type": "money"}, {"type": "why"}, {"type": "areas"}],
 "faqs": [
  ("Is a Goodman heat pump good for Ontario winters?", "The GSZH5 heats well through fall, spring and milder winter days, and in an Ontario winter we pair it with a gas furnace that takes over in the deep cold. If you want a heat pump to heat the whole house on its own at -25°C or colder, a cold-climate model rated to -30°C is the better fit."),
  ("Is a Goodman heat pump eligible for the Ontario rebate?", "Only if the exact model and size is on NRCan's qualified products list, which the Home Renovation Savings Program requires. We check your Goodman model before you buy. If it is not listed and the rebate matters to you, we quote a cold-climate model that is."),
  ("Can a Goodman heat pump replace my air conditioner?", "Yes. The GSZH5 goes where your AC was, cools just as well and adds heating, using a matched indoor coil on your furnace."),
  ("Do I need to register my Goodman heat pump warranty?", "Yes. Goodman's longer limited warranties depend on online registration within 60 days of installation, and we register it for you as part of the install."),
  ("Do you repair Goodman heat pumps and ACs you did not install?", "Yes. We repair and maintain Goodman heat pumps and air conditioners whoever installed them, with a written price before any work.")],
 "related": ["/brands/goodman/", "/brands/goodman/furnaces/", "/heat-pump/hybrid-furnace-systems/", "/heat-pump/cold-climate/", "/heat-pump/repair-maintenance/", "/heat-pump-rebates/"],
}

PAGES = [FURNACES, HEAT_PUMPS]
