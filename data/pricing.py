# Price guide used on city pages and cost FAQs. "from" figures are EHI's published starting prices.
# RANGES are typical installed ranges to be CONFIRMED BY EHI; until confirmed they stay None and pages
# show only the from-price with "quote". Fill in as ("low", "high") strings, e.g. ("3,300", "6,500").
FROM = {"furnace": "3,300", "heat_pump": "5,500", "tankless": "3,300"}
RANGES = {
 "furnace_repair": None,        # typical diagnostic + common repair
 "ac_repair": None,
 "furnace_install": None,
 "ac_install": None,
 "heat_pump_ducted": None,
 "ductless_single": None,       # one indoor head
 "tankless_install": None,
}
LABELS = {
 "furnace_repair": ("Furnace repair", "Diagnostic visit plus common parts such as ignitors, flame sensors and capacitors"),
 "ac_repair": ("AC repair", "Diagnostic visit plus common parts such as capacitors, contactors and refrigerant leak repair"),
 "furnace_install": ("High-efficiency furnace, installed", "Lennox ML296V or Midea MGH96, 96% to 97% AFUE, two-stage variable-speed"),
 "ac_install": ("Central air conditioner, installed", "Lennox or Midea, sized from a heat-gain calculation"),
 "heat_pump_ducted": ("Cold-climate heat pump, installed", "Midea EVOX G3 or Kepler, 2 to 5 ton, rated to -30°C"),
 "ductless_single": ("Ductless mini split, one zone", "Midea or Kepler wall unit with outdoor unit and line set"),
 "tankless_install": ("Rinnai tankless water heater, installed", "RX160iN or RX199iN condensing, with venting and gas line"),
}
def price_cell(key):
    r = RANGES.get(key)
    if r: return f"${r[0]} to ${r[1]}"
    if key == "furnace_install": return f"From ${FROM['furnace']}"
    if key in ("heat_pump_ducted",): return f"From ${FROM['heat_pump']}"
    if key == "tankless_install": return f"From ${FROM['tankless']}"
    return "Quote after diagnosis" if "repair" in key else "Written quote"

# Equipment we install: (model, type, key specs, warranty note). Used for "What we install in <City>" sections.
EQUIPMENT_IMG = {"Lennox ML296V": "lennox-ml296v-furnace", "Lennox EL297V": "lennox-el297v-furnace", "Midea EVOX G3": "midea-evox-g3-heat-pump",
                 "Kepler cold-climate": "kepler-luxe-heat-pump", "Midea ductless": "kepler-wall-mini-split", "Rinnai RX160iN": "rinnai-rx-tankless", "Rinnai RX199iN": "rinnai-rx-garage-install"}
EQUIPMENT = {
 "furnaces": [("Lennox ML296V", "Gas furnace", "96% AFUE, two-stage, variable-speed blower, 45,000 to 110,000 BTU", "20-year limited heat exchanger warranty"),
              ("Lennox EL297V", "Gas furnace", "97% AFUE, two-stage, variable-speed blower", "20-year limited heat exchanger warranty"),
              ("Midea MGH96", "Gas furnace", "96.5% AFUE, two-stage, variable-speed, 60,000 to 120,000 BTU", "Registered warranty, up to 12 years parts and labour on select systems")],
 "heat_pumps": [("Midea EVOX G3", "Cold-climate ducted heat pump", "2 to 5 ton, inverter, R-454B, ENERGY STAR cold climate, rated to -30°C", "Up to 12 years parts and labour on select systems"),
                ("Kepler cold-climate", "Ducted heat pump", "1.5 to 5 ton, rated to -30°C, quiet operation", "Registered warranty"),
                ("Midea ductless", "Single and multi-zone", "18,000 to 60,000 BTU outdoor units, wall-mounted heads", "Registered warranty")],
 "water_heaters": [("Rinnai RX160iN", "Condensing tankless", "0.97 UEF, up to about 9 GPM", "Rinnai warranty, extended coverage may be available"),
                   ("Rinnai RX199iN", "Condensing tankless", "0.98 UEF, up to about 11.1 GPM", "Rinnai warranty, extended coverage may be available")],
}
