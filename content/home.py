import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from build import form_block, icon

QUOTE_SECTION = (
 '<section class="sec" id="quote"><div class="wrap quote-split"><div>'
 '<h2>Get a free, guaranteed quote</h2>'
 '<p class="lead">Tell us what is going on and where you are. We will book an in-home or virtual assessment and send a written quote with your rebate estimate and financing options.</p>'
 '<ul class="checklist">'
 + "".join(f'<li>{icon("check")}<span>{x}</span></li>' for x in [
   "Same-day quotes in most cases, seven days a week",
   "Sized by heat-loss calculation, never by guesswork",
   "Price shown before and after the estimated rebate",
   "No pressure, no spam, no surprise extras on install day",
 ]) + '</ul></div>' + form_block() + '</div></section>')

PAGE = {
 "url": "/",
 "title": "HVAC Contractor Ontario | Heat Pumps, Furnaces, AC",
 "description": "Licensed Ontario HVAC contractor for homes and businesses. Heat pumps, furnaces, AC and tankless with guaranteed pricing and up to $7,500 in rebates.",
 "priority": "1.0",
 "hero_photo": "/assets/img/ehi-team.webp",
 "hero_photo_desktop": "/assets/img/ehi-team-hero.webp",
 "hero_photo_alt": "The EHI Heating And Cooling team standing in front of two EHI service vans outside an Ontario home",
 "kicker": "EHI Heating And Cooling - Serving Ontario For 20+ Years",
 "h1": "Heating and Cooling Done Right, Priced Once, Backed for Years",
 "h1_line1": "Heating &amp; Cooling Done Right",
 "h1_line2": "Priced Once. Backed for Years.",
 "intro": "Licensed HVAC contractor for homes and businesses, 20+ years of experience. Heat pumps, furnaces, AC and tankless water heaters, with guaranteed pricing and up to $7,500 in rebates.",
 "hero_points": [
   "Guaranteed final pricing",
   "0% financing for 3, 6 or 9 months",
   "Authorized Midea, Lennox, Kepler and Rinnai dealer",
   "Up to 12 years parts and labour warranty",
 ],
 "blocks": [
  {"type": "promo", "h2_hl": "Up to $7,500 in heat pump rebates:", "h2": "get pre-approved before the cold sets in", "image": "Midea cold-climate heat pump on a stand beside a deck fence, installed by EHI", "image_src": "/assets/img/work/midea-cold-climate-heat-pump-deck-fence.webp", "image_credit": "EHI install", "image_pos": "50% 62%",
   "text": "The Home Renovation Savings Program pays up to $7,500 toward a qualifying cold-climate heat pump, but only if pre-approval happens before install day. We check your eligibility, size the system and file everything. One call gets it started."},
  {"type": "stats", "items": [
    {"value": "20+", "label": "years serving Ontario homes"},
    {"value": "$7,500", "label": "max heat pump rebate we help you claim"},
    {"value": "4", "label": "brands we're authorized to install: Midea, Lennox, Kepler, Rinnai"},
    {"value": "12 yrs", "label": "parts and labour coverage on select systems"},
  ]},
  {"type": "linkgrid", "h2": "HVAC services for every season in Ontario", "lead": "Heating, cooling, hot water and air quality for homes and commercial properties. Pick the service you need, or call and we'll point you the right way.", "groups": [
    {"icon": "heatpump", "title": "Heat Pumps", "href": "/heat-pump/", "urls": ["/heat-pump/", "/heat-pump/cold-climate/", "/heat-pump/central/", "/heat-pump/hybrid-furnace-systems/", "/heat-pump/electric-air-handler-systems/", "/heat-pump/repair-maintenance/", "/heat-pump-rebates/"]},
    {"icon": "furnace", "title": "Furnaces", "href": "/furnace/", "urls": ["/furnace/", "/furnace/high-efficiency/", "/furnace/electric-air-handlers/", "/furnace/repair-maintenance/"]},
    {"icon": "ac", "title": "Air Conditioning", "href": "/ac/", "urls": ["/ac/", "/ac/ductless-mini-split/", "/ac/multi-zone-ductless-system/", "/ac/repair-maintenance/", "/ac/ductless-mini-split/repair/"]},
    {"icon": "tankless", "title": "Water Heaters", "href": "/water-heater/", "urls": ["/water-heater/", "/water-heater/repair-maintenance/"]},
    {"icon": "air", "title": "Air Quality & Controls", "href": "/services/", "urls": ["/services/humidifiers/", "/services/hrv-erv/", "/services/thermostats/"]},
    {"icon": "wrench", "title": "General HVAC", "href": "/services/", "urls": ["/services/hvac-installation-replacement/", "/services/hvac-repair-maintenance/", "/services/emergency-hvac/", "/contact/"], "labels": {"/contact/": "Commercial HVAC"}},
  ]},
  {"type": "html", "html": QUOTE_SECTION},
  {"type": "split", "h2": "The Ontario heat pump rebate, handled start to finish", "image": "Midea cold-climate heat pump on a raised stand with outdoor disconnect, installed by EHI", "image_src": "/assets/img/work/midea-cold-climate-heat-pump-stand-1.webp", "image_fit": "cover", "image_pos": "50% 62%", "image_credit": "EHI install", "html": "<p>The Home Renovation Savings Program pays up to $7,500 toward a qualifying cold-climate air-source heat pump. The catch: the equipment has to be on NRCan's qualified list, pre-approval has to happen before install day, and the paperwork has to be right.</p><p>That's our job. We confirm your eligibility, run the heat-loss calculation, submit pre-approval, install the system, and file the final documents. You sign, we chase.</p><ul class=\"checklist\"><li>Homes heated by electricity, oil, propane or wood: up to $7,500</li><li>Homes heated by Enbridge natural gas: a smaller tier, commonly up to $2,000</li><li>Smart thermostat: $100</li><li>No home energy audit needed for a heat pump on its own</li></ul><p><a class=\"more\" href=\"/heat-pump-rebates/\">Read the full Ontario heat pump rebate guide</a></p>"},
  {"type": "split", "reverse": True, "h2": "Commercial HVAC for Ontario businesses", "image": "Midea ductless head above a cabinet in a family room, installed by EHI", "image_src": "/assets/img/work/midea-wall-head-family-room.webp", "image_fit": "cover", "image_pos": "50% 50%", "image_credit": "EHI install", "html": "<p>Offices, retail units, restaurants, warehouses, clinics and multi-unit residential buildings need heating and cooling that doesn't quit on a Tuesday afternoon. We install and service rooftop units, split systems, ductless and multi-zone heat pumps, high-efficiency furnaces and commercial tankless hot water, and we keep the paperwork, scheduling and after-hours work tidy so your operation stays open.</p><ul class=\"checklist\"><li>Equipment sizing for occupancy, equipment loads and code ventilation requirements</li><li>Planned maintenance agreements with priority emergency response</li><li>Work scheduled around your hours, including evenings and weekends</li><li>TSSA, ESA and refrigeration-licensed crews, insured and WSIB covered</li></ul><p><a class=\"more\" href=\"/contact/\">Request a commercial quote</a></p>"},
  {"type": "problems", "h2": "What's going on in your building? We've seen it before.", "lead": "Pick the one that sounds like you. Each one has a fix, and most of them are cheaper than you'd think.", "items": [
    {"problem": "The furnace is 15+ years old and the repair bills are adding up", "solution": "At that age, a new 96% or 97% AFUE furnace from $3,300 usually beats another repair. Or skip gas altogether with a cold-climate heat pump and a rebate. We'll price both so you can decide. <a href=\"/furnace/\">Furnace replacement</a>"},
    {"problem": "The AC runs all day and the upstairs is still hot", "solution": "Usually an undersized or dying unit, a low refrigerant charge, or ductwork that can't move the air. We diagnose first and quote in writing. <a href=\"/ac/repair-maintenance/\">AC repair</a>"},
    {"problem": "Hydro or propane bills are out of control in winter", "solution": "A heat pump paired with an electric air handler or your existing furnace cuts heating cost sharply for electric, propane and oil homes, and those homes get the highest rebate tier. <a href=\"/heat-pump/\">Heat pump installation</a>"},
    {"problem": "No ductwork, and window units aren't cutting it", "solution": "A ductless mini-split heats and cools without ducts. Multi-zone systems handle the whole house. <a href=\"/ac/multi-zone-ductless-system/\">Multi-zone ductless</a>"},
    {"problem": "You're paying rental fees on a hot water tank that's always running out", "solution": "A Rinnai tankless water heater gives endless hot water, takes up a fraction of the space, and ends the rental. <a href=\"/water-heater/\">Tankless installation</a>"},
    {"problem": "Dry winter air, static shocks, cracking hardwood", "solution": "A whole-home humidifier on your furnace or air handler keeps the house at a comfortable 30 to 40% humidity. <a href=\"/services/humidifiers/\">Humidifiers</a>"},
  ]},
  {"type": "why"},
  {"type": "steps", "h2": "How working with EHI goes", "items": [
    {"title": "Call or send the form", "text": "Tell us the problem or the project. We'll ask a few questions about your home, heating fuel and ductwork."},
    {"title": "Free assessment and guaranteed quote", "text": "In person or virtual. You get options, honest sizing and a final price. No last-minute extras on the agreed scope."},
    {"title": "Rebate and financing sorted", "text": "We handle pre-approval and paperwork, and set up 0% financing if you want it."},
    {"title": "Install day", "text": "Licensed, certified crews. Most installs finish in one day. We test everything and walk you through it."},
    {"title": "Backed for years", "text": "Warranty registered, rebate filed, and we're one call away for maintenance or repairs."},
  ]},
  {"type": "reviews"},
  {"type": "gbp"},
  {"type": "areas"},
 ],
 "faqs": [
  ("What does EHI Heating And Cooling do?", "EHI Heating And Cooling (Efficient Home Improvements) is a licensed residential and commercial HVAC contractor in Ontario. We install, replace, repair and maintain heat pumps, gas furnaces, central air conditioners, ductless mini-splits, tankless water heaters, humidifiers, HRV/ERV ventilation and thermostats, and we help homeowners claim Ontario heat pump rebates. We also serve offices, retail units, warehouses and multi-unit buildings."),
  ("Which areas of Ontario do you serve?", "We serve Toronto and the GTA including Stouffville, Markham, Richmond Hill, Vaughan, Aurora, Newmarket, Brampton, Mississauga, Milton and Oakville, plus Durham Region, Barrie and Wasaga Beach, Hamilton, Kitchener-Waterloo, London, Sarnia, Kingston, Ottawa, Pembroke, North Bay, Sudbury and Timmins. See our <a href=\"/service-areas/\">service areas</a> page."),
  ("How much does a new HVAC system cost in Ontario?", "With EHI, gas furnaces start at $3,300 installed, cold-climate heat pumps at $5,500 and Rinnai tankless water heaters at $3,300. Final pricing depends on equipment size and installation requirements, and your quote is guaranteed before work starts. Rebates of up to $7,500 and 0% financing can bring the net cost down."),
  ("Are your technicians licensed?", "Yes. Gas work is done by TSSA-certified gas technicians, refrigerant work by licensed refrigeration technicians, and electrical connections by ESA-licensed electricians. EHI has been installing HVAC in Ontario homes for more than 20 years and was voted Best Company in 2019, 2020 and 2021."),
  ("Do you offer financing?", "Yes. We offer 0% interest financing for 3, 6 or 9 months, and open loans starting at 2.99% on approved credit. See our <a href=\"/financing/\">HVAC financing</a> page."),
  ("Can you help me get the Ontario heat pump rebate?", "Yes. We confirm eligibility, complete the pre-approval before installation, install equipment from NRCan's qualified list and submit the documentation to the Home Renovation Savings Program. Read our <a href=\"/heat-pump-rebates/\">rebate guide</a>."),
 ],
 "faq_h2": "Questions our customers ask us",
 "related": [],
}
