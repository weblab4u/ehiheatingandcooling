import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from build import form_block, icon, AREAS, AREA_GROUPS, PHONE, PHONE_TEL, EMAIL, ADDRESS, map_iframe, GBP_URL, DIRECTIONS_URL

CONTACT = {
 "url": "/contact/",
 "title": "Contact Us | Free, Guaranteed HVAC Quote in Ontario",
 "description": "Call 1-647-694-5845 or request a free guaranteed HVAC quote for heat pumps, furnaces, AC and tankless across Ontario. Open 7 days, emergency service.",
 "priority": "0.8",
 "eyebrow": "Contact / Get a Quote",
 "h1": "Get a Free, Guaranteed HVAC Quote",
 "intro": "<p>Homeowner or business, tell us what's going on and where you are. We'll ask a few questions, book an in-home or virtual assessment, and send a guaranteed quote with your rebate estimate and financing options. No pressure, no spam, no surprise extras later.</p>",
 "hero_points": ["Open 7 days: Mon to Sat 8 am to 8 pm, Sun 10 am to 5 pm", "Emergency service evenings, weekends and holidays", "Same-day quotes in most cases", "Serving the GTA to Northern Ontario"],
 "hero_form": True,
 "blocks": [
  {"type": "html", "html": f'''<section class="sec"><div class="wrap contact-grid">
   <div class="contact-card"><h2>Reach us directly</h2>
     <p>{icon("phone")}<span><strong>Phone:</strong> <a href="tel:{PHONE_TEL}">{PHONE}</a><br><span class="small">Call for no-heat and no-cooling emergencies.</span></span></p>
     <p>{icon("check")}<span><strong>Email:</strong> <a href="mailto:{EMAIL}">{EMAIL}</a></span></p>
     <p>{icon("pin")}<span><strong>Office:</strong> {ADDRESS["street"]}, {ADDRESS["city"]}, {ADDRESS["region"]} {ADDRESS["postal"]}<br><span class="small">Service-area business. We come to you; visits to the office by appointment.</span></span></p>
     <p>{icon("clock")}<span><strong>Hours:</strong> Monday to Saturday, 8:00 am to 8:00 pm. Sunday, 10:00 am to 5:00 pm<br><span class="small">Emergency service outside these hours.</span></span></p>
     <h3>What to have handy</h3><ul class="checklist"><li>{icon("check")}<span>Your heating fuel (gas, electric, propane, oil, wood)</span></li><li>{icon("check")}<span>Rough square footage and number of storeys</span></li><li>{icon("check")}<span>Age and brand of your current equipment (a photo of the label is perfect)</span></li><li>{icon("check")}<span>Any error codes or symptoms you've noticed</span></li></ul>
   </div>
   <div><h2>Find us on Google</h2><p class="lead">Rated 4.5 on Google. Get directions to our Stouffville office or open the listing.</p>{map_iframe(360)}<p class="btn-group small"><a class="btn btn-secondary" href="{DIRECTIONS_URL}" target="_blank" rel="noopener">Get Directions</a><a class="btn btn-secondary" href="{GBP_URL}" target="_blank" rel="noopener">View on Google Maps</a></p>
   </div></div></section>'''},
  {"type": "areas"},
 ],
 "faqs": [
  ("Is the quote really free?", "Yes. Assessments and quotes for new installations are free with no obligation. Diagnostic visits for repairs have a service fee that we tell you before booking and that goes toward the repair if you proceed."),
  ("How fast can you come out?", "For emergencies we aim for same-day service across our core service area. For installation quotes we usually book within a day or two."),
  ("Do you charge for travel outside the GTA?", "We serve a large part of Ontario and quote each job all-in. Any travel considerations are built into your guaranteed price, never added later."),
 ],
 "related": ["/services/emergency-hvac/", "/heat-pump-rebates/", "/financing/", "/service-areas/"],
}


SERVICE_AREAS = {
 "url": "/service-areas/",
 "title": "HVAC Service Areas in Ontario | GTA to Northern Ontario",
 "description": "We install and service heat pumps, furnaces and AC across the GTA, Durham, Simcoe, Southwestern, Eastern and Northern Ontario. Find your city.",
 "priority": "0.7",
 "eyebrow": "Service Areas",
 "h1": "Where We Work: HVAC Service Across Ontario",
 "intro": "<p>EHI Heating And Cooling is based in Whitchurch-Stouffville and serves homeowners from Toronto to Timmins. We're a service-area business: our licensed crews come to your home for quotes, installations, repairs and maintenance. If your city isn't listed, call anyway. We cover a large part of Ontario and surrounding communities.</p>",
 "hero_points": ["Same guaranteed pricing in every city we serve", "Rebate eligibility confirmed for your address and utility", "Emergency service across the core GTA area", "Northern Ontario installs scheduled in efficient routes"],
 "hero_image": "Midea ductless head on a cedar wall at a cottage, installed by EHI", "hero_img": "/assets/img/work/midea-wall-head-cedar-cottage.webp", "hero_img_fit": "cover", "hero_img_pos": "50% 30%", "hero_img_credit": "EHI install",
 "blocks": [
  {"type": "area_dir", "h2": "Cities and regions we serve", "lead": "Pick your city for local HVAC services, typical costs, rebates and the neighbourhoods we cover. Every service page applies to every city below."},
  {"type": "text", "h2": "A note on rebates by location", "html": "<p>The Home Renovation Savings Program applies province-wide, but the rebate tier depends on your heating fuel and utility. Enbridge gas customers sit in one tier; homes on electricity, propane, oil or wood (common in cottage country and Northern Ontario) sit in the higher tier, up to $7,500. Some local hydro utilities add their own incentives. We check all of it for your address. See the <a href=\"/heat-pump-rebates/\">Ontario heat pump rebate guide</a>.</p><p>Northern homeowners: cold-climate heat pumps rated to -30°C, like the <a href=\"/brands/midea-heat-pumps/\">Midea EVOX G3</a> and <a href=\"/brands/kepler-heat-pumps/\">Kepler</a>, are built for Sudbury, North Bay and Timmins winters. We'll still recommend a backup heat source and size it properly for your design temperature.</p>"},
  {"type": "cards", "h2": "Most requested services by region", "items": [
    {"icon": "heatpump", "title": "GTA and York Region", "text": "Hybrid furnace + heat pump systems and central AC replacements in gas-heated homes.", "link": "/heat-pump/hybrid-furnace-systems/"},
    {"icon": "house", "title": "Cottage country and Northern Ontario", "text": "All-electric heat pump with air handler, and multi-zone ductless for homes on electric or propane heat.", "link": "/heat-pump/electric-air-handler-systems/"},
    {"icon": "furnace", "title": "Durham, Peel, Halton", "text": "High-efficiency furnace replacements and same-day furnace repair.", "link": "/furnace/"},
    {"icon": "tankless", "title": "Everywhere", "text": "Rinnai tankless water heaters to end tank rentals for good.", "link": "/water-heater/"},
  ]},
  {"type": "why"},
 ],
 "faqs": [
  ("Do you serve my city if it's not listed?", "Probably. We cover a large part of Ontario and the communities around the cities listed. Call 1-647-694-5845 and we'll confirm in a minute."),
  ("Is pricing different outside the GTA?", "Your quote is all-in and guaranteed wherever you are. We schedule longer-distance jobs efficiently so travel doesn't inflate your price."),
  ("Do you offer emergency service in Northern Ontario?", "We offer emergency repair across our core GTA area and schedule Northern Ontario service as quickly as routing allows. Call and we'll give you a straight answer on timing."),
 ],
 "related": ["/contact/", "/heat-pump-rebates/", "/services/", "/services/emergency-hvac/"],
}

PAGES = [CONTACT, SERVICE_AREAS]
