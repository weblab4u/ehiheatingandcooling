# 2027 rebate landing page: the new federal National Heat Pump Rebate and how it may sit alongside Ontario's Home Renovation
# Savings Program. Federal facts are from the two Government of Canada pages linked below, read 2026-11-19. Anything the
# government has not confirmed (combining with Ontario's program, exact approval of a model) is written as conditional.
import importlib.util as _u, os as _os
_s = _u.spec_from_file_location("ehi_climate_rb", _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))), "data", "climate.py"))
_m = _u.module_from_spec(_s); _s.loader.exec_module(_m); CL = _m.CLIMATE

FED = "https://www.canada.ca/en/environment-climate-change/campaigns/one-million-home-energy-retrofits.html"
NEWS = "https://www.canada.ca/en/environment-climate-change/news/2026/10/prime-minister-carney-announces-landmark-investment-to-retrofit-one-million-homes-cutting-energy-costs-and-emissions.html"
UPDATED = "November 19, 2026"
SKIP = {"toronto", "vaughan", "markham", "barrie", "ottawa"}        # these cities have /heat-pump-installation/ pages

NO_HP = {"thunder-bay", "kanata"}         # no city heat pump page built yet
def hp(s): return f"/{s}/heat-pump-installation/" if s in SKIP else f"/{s}/heat-pump/"
def a(s, name): return f"<a href='/{s}/'>{name}</a>"
def temps(*slugs):
    ts = sorted({CL[s]["dt"] for s in slugs})
    return f"{ts[0]}°C" if len(ts) == 1 else f"{ts[-1]}°C to {ts[0]}°C"

REGIONS = [
 ("Toronto, Markham, Richmond Hill, Vaughan and the GTA", ["toronto", "markham", "richmond-hill", "vaughan"],
  "Mostly gas-heated homes, so the Ontario amount is usually the lower tier. A hybrid heat pump with the furnace as backup is the common setup, and we compare running costs before you switch.",
  [("toronto", "Toronto"), ("markham", "Markham"), ("richmond-hill", "Richmond Hill"), ("vaughan", "Vaughan")]),
 ("Ottawa and surrounding areas", ["ottawa", "orleans", "kanata"],
  "Long, cold winters. Size the heat pump to carry most of the season and set the backup for the coldest nights. Older rural homes on oil or propane sit in Ontario's higher tier.",
  [("ottawa", "Ottawa"), ("orleans", "Orléans"), ("kanata", "Kanata")]),
 ("Barrie and Simcoe County", ["barrie", "innisfil", "orillia", "collingwood"],
  "Heavy snow belt. The outdoor unit goes on a tall stand or wall bracket. Many cottage-country and rural homes heat with propane or electric baseboards.",
  [("barrie", "Barrie"), ("innisfil", "Innisfil"), ("orillia", "Orillia"), ("collingwood", "Collingwood")]),
 ("Sudbury and North Bay", ["sudbury", "north-bay"],
  "Some of the coldest design days we size for. Cold-climate models with full backup heat, and plenty of oil, propane and electric homes in Ontario's higher tier.",
  [("sudbury", "Sudbury"), ("north-bay", "North Bay")]),
 ("Kingston", ["kingston"], "Lake-moderated but still cold. Older homes downtown often need ductless heads or duct changes to heat the whole house.", [("kingston", "Kingston")]),
 ("London", ["london"], "Milder than most of the province, so a well-sized heat pump carries more of the winter on its own.", [("london", "London")]),
 ("Windsor", ["windsor"], "The mildest design temperature on our list, and hot, humid summers where the heat pump's cooling matters as much as its heating.", [("windsor", "Windsor")]),
 ("Thunder Bay", ["thunder-bay"], "Deep, dry cold. A cold-climate unit with backup heat and a humidifier is the usual plan, and the rebate case is strongest for oil, propane and electric homes.", [("thunder-bay", "Thunder Bay")]),
]
region_rows = [[f"<strong>{r}</strong>", temps(*sl), note, " · ".join(a(s, n) for s, n in links)] for r, sl, note, links in REGIONS]

PAGE = {
 "url": "/ontario-heat-pump-rebate-2027/",
 "title": "Ontario Heat Pump Rebates 2027 | Up to $10,000 Back",
 "description": "See Ontario heat pump rebates for 2027: the new federal rebate of $2,000 or up to $10,000, Ontario's up to $7,500, who qualifies and how to apply now.",
 "updated": "2026-11-19",
 "show_updated": True,
 "priority": "0.9",
 "eyebrow": "Heat Pump Rebates 2027",
 "h1": "Ontario Heat Pump Rebates 2027: New Federal Rebates Up to $10,000",
 "tagline": "The National Heat Pump Rebate, Ontario's program, and how to be ready before applications open",
 "intro": ("<p>The Government of Canada's new <strong>National Heat Pump Rebate</strong> pays <strong>$2,000</strong>, or <strong>up to $10,000</strong> for households below the median income, "
           "on an eligible cold-climate heat pump. Applications are expected to open in early 2027. Here is who qualifies, how it may sit alongside Ontario's rebate, and what to do now.</p>"
           f"<p class='hero-updated'>Last updated {UPDATED}. Federal applications are not open yet.</p>"),
 "hero_points": [
   "Federal: $2,000, or up to $10,000 if income-qualified",
   "Installs from November 1, 2026 may qualify retroactively",
   "Ontario: up to $7,500, pre-approval before install",
   "We size it, quote it and prepare your rebate paperwork",
 ],
 "hero_rebate_form": True,
 "cta_primary": "Check Your Heat Pump Rebate Eligibility", "cta_href": "#check",
 "service": {"name": "Heat Pump Installation with Rebate Assistance", "type": "Cold-climate heat pump installation and federal and Ontario rebate paperwork"},
 "blocks": [
  {"type": "text", "h2": "Where the federal rebate stands today", "html":
   f"<div class='callout'><p><strong>Status on {UPDATED}:</strong> the National Heat Pump Rebate has been announced but is <strong>not accepting applications yet</strong>. "
   "The Government of Canada says the online portal is expected to open in early 2027. Eligible heat pumps installed from November 1, 2026 may qualify retroactively once it opens, "
   "but no payments are made until the program launches and your application is approved.</p></div>"
   "<p>EHI Heating And Cooling is a licensed HVAC contractor. We are not a government agency and are not endorsed by the Government of Canada or Ontario. "
   "We install heat pumps, check them against each program's rules, and give you the paperwork the applications ask for.</p>"},
  {"type": "table", "h2": "What is the new federal heat pump rebate for 2027?", "lead": "The National Heat Pump Rebate is a $2 billion, eight-year Government of Canada program announced on October 8, 2026, aimed at up to 820,000 homeowners who install an eligible electric cold-climate air-source heat pump. These are the details published so far.",
   "headers": ["", "National Heat Pump Rebate (federal)"], "rows": [
    ["Rebate amount", "$2,000 for eligible households above the median income; up to $10,000 for households at or below it. The government says the actual amount also depends on the cost of the equipment installed."],
    ["Eligible equipment", "Electric cold-climate air-source heat pumps on the federal Eligible Products List, identified by AHRI number, bought from and installed by an HVAC contractor"],
    ["Energy audit", "None required before or after installation"],
    ["How you apply", "Online portal, expected to open in early 2027, asking for basic personal details and the heat pump you plan to buy"],
    ["Approval", "The government says it will confirm approval within 24 hours"],
    ["Payment", "After installation you upload receipts, and the government says payment will be approved within five days, paid by direct deposit"],
    ["Limit", "One rebate per household, even if you own more than one property"],
    ["Program window", "Expected to run from early 2027 to March 2034, with installs from November 1, 2026 eligible retroactively"],
   ], "note": f"Sources: <a href='{FED}' rel='noopener'>National Heat Pump Rebate, Government of Canada</a> and the <a href='{NEWS}' rel='noopener'>October 8, 2026 announcement</a>. The government says program parameters are still being finalized and may change."},
  {"type": "checklist", "h2": "Heat pump rebate eligibility in Ontario: who qualifies for the federal rebate", "lead": "Based on what the Government of Canada has published, you are likely to qualify if all of these are true. Final criteria are still being set.",
   "image": "Midea cold-climate heat pump installed by EHI on a raised stand beside green siding", "image_title": "Cold-climate heat pump installation with rebates in Ontario",
   "image_src": "/assets/img/work/midea-cold-climate-heat-pump-installation-raised-stand.webp", "image_fit": "cover", "image_credit": "EHI install",
   "items": [
    "You live in Canada and own the home. It does not have to be your main residence, so a rental property you own can count.",
    "The heat pump is on the federal Eligible Products List, matched by its AHRI number",
    "It was bought from and installed by an HVAC contractor",
    "No federal funding has already been paid for a heat pump at that address",
    "Your household has not already received this rebate for another property",
    "The home is heated today by electricity, natural gas, oil, propane, diesel, coal or wood. Planned and emergency replacements both count, and you do not have to remove the old system.",
   ]},
  {"type": "table", "h2": "Income limits for the $10,000 heat pump rebate in Ontario", "lead": "The higher federal amount is for households at or below the median after-tax income for their province and household size. These are the Ontario figures the government has published.",
   "headers": ["Household size", "Ontario after-tax household income at or below"], "rows": [
    ["1 person", "$46,981"], ["2 people", "$92,884"], ["3 people", "$119,850"], ["4 people", "$146,217"], ["5 or more people", "$158,202"]],
   "note": "In 2025 dollars, from Statistics Canada 2021 data adjusted for inflation. To work out your figure, take line 23600 of your 2025 tax return minus line 43500, and add your spouse's or common-law partner's figure worked out the same way. When applications open, you give your Social Insurance Number and the Canada Revenue Agency confirms your income and rebate level. Thresholds can change before launch."},
  {"type": "video", "h2": "How Ontario's heat pump rebate is worked out", "lead": "Dustin, owner of EHI, explains the Ontario side: why your heating fuel and the heat pump's size set the amount. The federal rebate is separate and explained on this page.", "items": [("iocuwNDiIW4", "")]},
  {"type": "text", "h2": "Can Ontario and federal heat pump rebates be combined?", "html":
   "<p>Possibly. Ontario's <a href='/heat-pump-rebates/'>Home Renovation Savings Program</a> and the federal National Heat Pump Rebate are separate programs with separate rules, product lists and applications. "
   "As of our last check, the federal program has <strong>not yet published its rules on combining</strong> with provincial rebates, so treat any combined figure as possible, not promised.</p>"
   "<p>Ontario's program pays by heat pump size and by how your home is heated today: about <strong>$1,250 per ton, up to $7,500</strong>, for homes heated by electricity, oil, propane or wood, and about <strong>$500 per ton, up to $2,000</strong>, for homes heated by Enbridge natural gas. "
   "Ontario requires <strong>pre-approval before installation</strong>. Install first and you lose the Ontario rebate, whatever happens with the federal one.</p>"},
  {"type": "table", "h2": "Federal and Ontario rebate examples for a 3-ton heat pump", "lead": "Examples only, assuming both programs approve the same qualifying 3-ton cold-climate heat pump and combining is allowed. Your amounts depend on your fuel, the system size and cost, your income and the rules on the day it is installed.",
   "headers": ["Your situation", "Ontario (estimate)", "Federal", "Potential total if both apply"], "rows": [
    ["Heated by electricity, oil or propane, income above the cut-off", "$3,750 (3 tons × $1,250)", "$2,000", "<strong>$5,750</strong>"],
    ["Heated by natural gas, income above the cut-off", "$1,500 (3 tons × $500)", "$2,000", "<strong>$3,500</strong>"],
    ["Income at or below the cut-off", "$3,750 or $1,500, by fuel", "Up to $10,000, set by equipment cost", "Depends on the federal amount approved"],
   ], "note": "Conditional estimates, not a quote or a guarantee. Stacking rules, equipment eligibility and amounts must be confirmed by each program. We check your home and exact model against both before you sign."},
  {"type": "cta", "h2": "Book your heat pump assessment", "text": "We measure your home's heat loss, size the right cold-climate system, and tell you which rebate tiers you are likely to fall in, with one guaranteed written price.", "primary": "Book Your Heat Pump Assessment", "href": "#check"},
  {"type": "cards", "h2": "Which heat pumps are eligible? Cold-climate, ducted and ductless", "lead": "The federal rebate is for electric cold-climate air-source heat pumps on its Eligible Products List, which the government says has over 100,000 options. It supports systems that can heat the whole home, so sizing matters as much as the model.",
   "fill_h": "Not sure which system fits?", "fill_text": "Tell us how you heat now and roughly how big the house is. We will suggest the setup and check it against both programs.", "items": [
    {"icon": "heatpump", "title": "Ducted cold-climate heat pumps", "text": "Replace the AC and carry most or all of the heating through your existing ducts. Midea EVOX G3 and Kepler models we install are on NRCan's list used by Ontario's program.", "link": "/heat-pump/cold-climate/"},
    {"icon": "ductless", "title": "Ductless and multi-zone heat pumps", "text": "For homes with baseboards or no ducts. A multi-zone system can heat the whole house; one wall head in one room may not meet the whole-home focus.", "link": "/ac/ductless-mini-split/"},
    {"icon": "furnace", "title": "Hybrid heat pump with a furnace", "text": "A heat pump on your gas furnace, with the furnace as backup on the coldest nights. Common in gas-heated GTA homes.", "link": "/heat-pump/hybrid-furnace-systems/"},
    {"icon": "heatpump", "title": "Heat pump with an electric air handler", "text": "All-electric ducted setup for homes leaving oil, propane or an electric furnace.", "link": "/heat-pump/electric-air-handler-systems/"},
   ]},
  {"type": "problems", "h2": "Heat pump rebates by how you heat today", "lead": "Your current fuel sets your Ontario tier and usually your savings. The federal rebate covers all of these fuels.", "items": [
    {"problem": "Heat pump rebates for electric baseboard heating", "solution": "Ontario's higher tier, up to $7,500, plus the federal amount if you qualify. Baseboard homes usually get <a href='/ac/multi-zone-ductless-system/'>multi-zone ductless</a> heads, with the baseboards kept as backup."},
    {"problem": "Propane to heat pump rebate in Ontario", "solution": "Propane homes are in Ontario's higher tier, and the Government of Canada puts average savings above $1,400 a year for oil, propane and electric resistance heat. A ducted heat pump with an electric air handler, or a hybrid, are the usual routes."},
    {"problem": "Oil furnace to heat pump rebate", "solution": "Oil-heated homes are in Ontario's higher tier and are covered by the federal rebate. The older federal oil-to-heat-pump program closed to new applicants in July 2026. Ask us about removing the oil tank at the same time."},
    {"problem": "Natural gas furnace", "solution": "Ontario's lower tier, about $500 per ton up to $2,000, and the federal rebate applies to gas-heated homes too. The government notes a heat pump may not lower bills in every gas-heated home, so we compare running costs before you decide."},
   ]},
  {"type": "steps", "h2": "How to apply for the federal heat pump rebate", "lead": "This is the process the Government of Canada has described for when the portal opens. We handle the contractor side.", "cta": "Get a Heat Pump Installation Quote", "href": "#check", "items": [
    {"title": "Choose an eligible system", "text": "We size your home and pick a model on the federal list, matched by AHRI number, with a guaranteed written price."},
    {"title": "Apply online", "text": "You apply in the federal portal with basic personal details and the heat pump you plan to buy. The government says approval comes within 24 hours."},
    {"title": "Install", "text": "We install and commission the system. If you also want Ontario's rebate, its pre-approval must be in place first."},
    {"title": "Submit receipts", "text": "You upload our receipt. The government says payment is approved within five days, paid by direct deposit."},
   ]},
  {"type": "checklist", "h2": "How to prepare before the federal rebate opens", "lead": "You do not have to wait to plan. If your furnace or AC is near the end of its life, these steps put you first in line.", "items": [
    "Find your 2025 tax return: line 23600 minus line 43500, for you and your spouse or partner, to see if you are under the income cut-off",
    "Book a heat-loss assessment so the system is sized to heat the whole home, which the government encourages",
    "Want Ontario's rebate too? Get its pre-approval before anything is installed",
    "Keep the receipt. It must show your name and address, the installer's name, the make, model and AHRI number, how many heat pumps, and the total project cost including ductwork and electrical work",
    "Receipts must be submitted within 6 months, according to the federal program",
    f"Sign up for official updates on the <a href='{FED}' rel='noopener'>Government of Canada page</a>, and ignore anyone who calls asking for your SIN or banking details",
   ]},
  {"type": "rebate_form", "h2": "Check your heat pump rebate eligibility", "lead": "Five quick answers and we call you back with your likely Ontario tier, whether the federal rebate is likely to apply, and a time for a sizing visit. Free, and no obligation.",
   "items": ["Your likely Ontario rebate tier by fuel and size", "Whether your household may fall under the federal income cut-off", "A heat pump sized for your home, with one written price", "Receipts with everything the federal application asks for"], "where": "rebate_section_form"},
  {"type": "table", "h2": "Heat pump rebate help across Ontario", "lead": "Same programs everywhere in Ontario, but the system that qualifies and pays off depends on your local winter. Design temperatures are from the Ontario Building Code (SB-1).",
   "headers": ["Area", "January design temperature", "What it means for a rebate heat pump", "Local pages"], "rows": region_rows},
  {"type": "table", "h2": "Key dates for the 2027 heat pump rebates", "headers": ["Date", "What happens"], "rows": [
    ["October 8, 2026", "National Heat Pump Rebate announced by the Government of Canada"],
    ["November 1, 2026", "Retroactive period starts: eligible installs from this date may qualify once applications open"],
    ["Early 2027", "Online application portal expected to open"],
    ["Within 6 months", "Receipts must be submitted, according to the federal program"],
    ["March 2034", "Program expected to close"],
   ], "note": "Ontario's Home Renovation Savings Program is a separate program with its own dates. As of our last check it was accepting heat pump applications with pre-approval."},
  {"type": "money"},
  {"type": "why"},
 ],
 "faqs": [
  ("What is the new federal heat pump rebate for 2027?", "The National Heat Pump Rebate is a Government of Canada program announced on October 8, 2026. It pays $2,000, or up to $10,000 for households below the median income, toward an eligible electric cold-climate air-source heat pump installed by an HVAC contractor. Applications are expected to open through an online portal in early 2027, and installs from November 1, 2026 may qualify retroactively."),
  ("Who qualifies for the $10,000 heat pump rebate?", "Homeowners whose after-tax household income is at or below the median for their province and household size can get up to $10,000. The exact amount also depends on the cost of the equipment. Households above the median can get $2,000. The home must be in Canada and owned by you, and the heat pump must be on the federal Eligible Products List."),
  ("What income qualifies for the federal heat pump rebate?", "In Ontario the published cut-offs for the higher rebate are $46,981 for one person, $92,884 for two, $119,850 for three, $146,217 for four and $158,202 for five or more, in after-tax household income. Use line 23600 minus line 43500 of your 2025 tax return, plus your spouse's or partner's. The Canada Revenue Agency verifies it using your SIN when you apply."),
  ("Can Ontario and federal heat pump rebates be combined?", "Possibly, but it is not confirmed. They are separate programs with separate rules, and the federal program has not yet published its rules on combining with provincial rebates. As an example only, a qualifying 3-ton heat pump in an electric, oil or propane-heated home could see about $3,750 from Ontario and $2,000 federally, a potential $5,750, if both programs approve it. Ontario still needs pre-approval before installation."),
  ("When does the new federal heat pump rebate start?", "The Government of Canada says the online application portal is expected to open in early 2027. Eligible heat pumps installed from November 1, 2026 may qualify retroactively once it opens. The program is expected to run until March 2034. It is not accepting applications yet."),
  ("Do I need an energy audit for the heat pump rebate?", "Not for the federal rebate: no energy audit is needed before or after installation. Ontario's Home Renovation Savings Program also does not need an assessment for a heat pump on its own, though one is required if you bundle insulation or window rebates."),
  ("Can I receive a rebate for a ductless heat pump?", "Ontario's program covers qualifying cold-climate ductless heat pumps. For the federal rebate, the model must be on the Eligible Products List, and the government says the program supports systems that can heat the whole home. A multi-zone ductless system sized for the house fits that; a single head in one room may not. We check before you buy."),
  ("Are Midea cold-climate heat pumps eligible?", "The Midea EVOX G3 and the Midea ductless models we install are on Natural Resources Canada's qualified list used by Ontario's program. The federal list identifies eligible systems by AHRI number, so we match your exact Midea outdoor and indoor combination against it before you commit. Eligibility is confirmed by the program, not by us."),
  ("Can landlords qualify for heat pump rebates?", "Yes for the federal rebate, within limits. The home does not have to be your main residence, so a rental you own can qualify, but only one rebate is available per household even if you own several properties. Rented or leased heat pumps may be eligible once the program launches, with details to come. Ontario's program has its own property rules, which we check for you."),
  ("How do I apply for the federal heat pump rebate?", "When the portal opens in early 2027, you apply online with basic personal details and the heat pump you plan to buy, and the government says approval comes within 24 hours. After installation you upload the contractor's receipt, and payment is approved within five days. If you install before launch, keep the receipt and apply once the portal opens."),
  ("Is there a heat pump rebate for seniors in Ontario?", "There is no separate seniors' heat pump rebate. Ontario's program is not income-tested, so seniors qualify under the same rules as everyone else. The federal rebate is income-based, so a retired household below the Ontario cut-off, for example $92,884 after tax for two people, may get up to $10,000 instead of $2,000."),
 ],
 "related": ["/heat-pump-rebates/", "/heat-pump/", "/heat-pump/cold-climate/", "/brands/midea/heat-pumps/", "/heat-pump/hybrid-furnace-systems/", "/ac/ductless-mini-split/", "/financing/", "/blog/national-heat-pump-rebate-ontario/"],
}
