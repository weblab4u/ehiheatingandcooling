# descriptive link text for each answer's "more" link
MORE = {"/ac/": "More on AC installation", "/ac/multi-zone-ductless-system/": "More on multi-zone ductless", "/ac/repair-maintenance/": "More on AC repair",
        "/furnace/": "More on furnace installation", "/furnace/repair-maintenance/": "More on furnace repair", "/heat-pump-rebates/": "More on heat pump rebates",
        "/heat-pump/cold-climate/": "More on cold-climate heat pumps", "/heat-pump/electric-air-handler-systems/": "More on all-electric heat pump systems",
        "/heat-pump/hybrid-furnace-systems/": "More on hybrid systems", "/services/hrv-erv/": "More on HRV and ERV", "/services/humidifiers/": "More on humidifiers",
        "/services/hvac-repair-maintenance/": "More on HVAC maintenance", "/water-heater/": "More on tankless water heaters"}
QA = [
 ("How much does a new furnace cost in Ontario?", "A new high-efficiency gas furnace installed by EHI starts at $3,300. Most homes land between $3,300 and $6,500 depending on BTU size, efficiency (96% or 97% AFUE), two-stage or variable-speed features and venting work. Your quote is guaranteed before install.", "/furnace/"),
 ("How much does a heat pump cost in Ontario after the rebate?", "Cold-climate heat pumps from EHI start at $5,500 installed. A typical central system runs $8,000 to $16,000 before rebates. With up to $7,500 from the Home Renovation Savings Program for electric, oil, propane or wood-heated homes, the net cost often lands in the same range as a furnace and AC replacement.", "/heat-pump-rebates/"),
 ("Should I repair or replace my furnace?", "If the furnace is under 12 years old and the repair is under about a third of replacement cost, repair it. If it's 15 or older, has a cracked heat exchanger, or needs a second major repair in two years, replace it. We give you both numbers.", "/furnace/repair-maintenance/"),
 ("Do heat pumps work in Ontario winters?", "Yes. Cold-climate heat pumps such as the Midea EVOX G3 and Kepler are rated to -30°C and keep most of their heating capacity at -15°C. In the coldest parts of the province we pair them with a gas furnace or electric backup.", "/heat-pump/cold-climate/"),
 ("What size AC do I need?", "AC size depends on a heat-gain calculation covering square footage, insulation, windows, orientation and occupancy. A rough rule for Ontario is 1 ton per 600 to 1,000 square feet, but oversizing causes short cycling and humidity problems, so we calculate rather than guess.", "/ac/"),
 ("Why is my AC blowing warm air?", "The usual causes are a low refrigerant charge from a leak, a failed capacitor or contactor on the outdoor unit, a frozen evaporator coil from a dirty filter, or a thermostat set to fan-only. A diagnostic visit pins it down and comes with a written repair quote.", "/ac/repair-maintenance/"),
 ("Is a tankless water heater worth it in Ontario?", "For most families, yes. A Rinnai condensing tankless unit delivers endless hot water at 0.97 to 0.98 UEF, frees up floor space and ends monthly tank rental fees. Installed from $3,300. Sizing accounts for Ontario's cold winter inlet water.", "/water-heater/"),
 ("How often should I service my furnace or heat pump?", "Once a year for a furnace or AC, and once a year for a heat pump (ideally fall). Annual service keeps efficiency up, catches small failures early and is usually required to keep extended warranties valid.", "/services/hvac-repair-maintenance/"),
 ("Do I need a home energy audit for the heat pump rebate?", "No. Under the Home Renovation Savings Program a heat pump is a single-upgrade rebate with no assessment required. You do need pre-approval before installation and equipment from NRCan's qualified list.", "/heat-pump-rebates/"),
 ("What's the difference between an HRV and an ERV?", "Both bring in fresh air while recovering heat from the stale air going out. An HRV transfers heat only; an ERV also transfers moisture, which helps keep humidity balanced. In most Ontario homes an HRV is the standard choice; ERVs suit very tight homes or humid regions.", "/services/hrv-erv/"),
 ("Can a ductless mini-split heat a whole house?", "A multi-zone ductless system with two to five indoor heads can heat and cool a whole house without ducts, with each room on its own control. Midea multi-zone systems run from 18,000 to 60,000 BTU.", "/ac/multi-zone-ductless-system/"),
 ("What humidity should my house be in winter?", "Aim for 30 to 40% relative humidity in an Ontario winter. Lower causes static, dry skin and cracked wood; higher causes condensation on windows. A whole-home humidifier with a humidistat holds the target automatically.", "/services/humidifiers/"),
]

ANSWERS = {
 "url": "/answers/",
 "title": "HVAC Questions Answered for Ontario Homeowners",
 "description": "Straight answers to the heating, cooling, heat pump, rebate and water heater questions Ontario homeowners ask most. Costs, sizing, repair or replace.",
 "priority": "0.7",
 "eyebrow": "Your Questions Answered",
 "h1": "Your HVAC Questions, Answered by People Who Install This Stuff",
 "intro": "<p>These are the questions we get on the phone, at kitchen tables and in the furnace room. Short, honest answers, with a link to the page that goes deeper. If yours isn't here, call us. We'll answer it and probably add it to the list.</p>",
 "hero_points": ["Written by licensed Ontario HVAC technicians", "Costs quoted are real EHI starting prices", "Updated as programs and equipment change", "No sales pitch, just answers"],
 "hero_image": "The EHI Heating And Cooling team in front of two EHI service vans", "hero_img": "/assets/img/ehi-team.webp", "hero_img_fit": "cover", "hero_img_pos": "50% 40%",
 "blocks": [
  {"type": "html", "html": '<section class="sec"><div class="wrap narrow answers"><dl>' + "".join(f'<dt>{q}</dt><dd>{a} <a class="more" href="{u}">{MORE.get(u, "More on this topic")}</a></dd>' for q, a, u in QA) + '</dl></div></section>'},
  {"type": "cta", "h2": "Still have a question?", "text": "Call 1-647-694-5845 or send us the form. We answer HVAC questions seven days a week."},
  {"type": "why"},
 ],
 "faqs": [(q, a) for q, a, u in QA],
 "faq_h2": "Quick reference",
 "related": ["/services/", "/heat-pump-rebates/", "/blog/", "/contact/"],
}

POSTS = [
 ("Ontario Heat Pump Rebate 2026: Eligibility, Amounts and How to Apply", "The plain-language guide to the Home Renovation Savings Program for homeowners who've just left the government site more confused than when they arrived.", "/heat-pump-rebates/"),
 ("Hybrid Heat Pump vs Furnace Replacement: What an Enbridge Gas Home Should Choose", "Run the numbers on a dual-fuel system versus a straight furnace swap, with real Ontario gas and hydro rates.", "/heat-pump/hybrid-furnace-systems/"),
 ("Furnace Not Heating? 7 Things to Check Before You Call", "Thermostat, breaker, filter, condensate, furnace switch, gas valve, error codes. Five minutes that might save a service call.", "/furnace/repair-maintenance/"),
 ("Replacing Electric Baseboards with a Heat Pump: Costs and Savings in Ontario", "Why baseboard and propane homes get the biggest rebate and the biggest bill savings, and what an air handler system actually involves.", "/heat-pump/electric-air-handler-systems/"),
 ("Tankless vs Tank Water Heater: Ending the Rental in Ontario", "What a Rinnai tankless costs, what it saves, and what to know about cold inlet water and gas line sizing.", "/water-heater/"),
]

BLOG = {
 "url": "/blog/",
 "title": "HVAC Blog for Ontario Homeowners | Heating & Cooling Guides",
 "description": "Guides on heat pumps, furnaces, AC, rebates and water heaters written for Ontario homes by licensed HVAC technicians. Practical, local and current.",
 "priority": "0.5",
 "eyebrow": "Blog",
 "h1": "Heating and Cooling Guides for Ontario Homes",
 "intro": "<p>Rebate rules change, equipment changes, and Ontario winters don't get any shorter. Our blog keeps you current on what matters for your home, written by the people who do the installs. Posts below are planned; the first ones publish soon.</p>",
 "hero_points": ["Written by licensed EHI technicians", "Ontario-specific: rebates, utilities, climate", "No recycled generic advice", "New guides added regularly"],
 "hero_image": "Midea ductless head above a window in a bright bedroom, installed by EHI", "hero_img": "/assets/img/work/midea-wall-head-bright-room.webp", "hero_img_fit": "cover", "hero_img_pos": "50% 28%", "hero_img_credit": "EHI install",
 "blocks": [
  {"type": "blog_index", "h2": "Guides and recent posts", "planned": POSTS},
  {"type": "cta", "h2": "Rather just talk to someone?", "text": "Our comfort advisors answer the questions these posts cover, seven days a week."},
 ],
 "faqs": [],
 "related": ["/answers/", "/heat-pump-rebates/", "/services/"],
}

PAGES = [ANSWERS, BLOG]
