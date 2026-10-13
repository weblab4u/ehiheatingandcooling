# Job photo library (assets/img/work/*.webp) and which service pages show which photos.
# Pages not listed here get no gallery (no matching job photos yet).
P = {
 # dark Midea cold-climate heat pumps
 "hp1": ("midea-cold-climate-heat-pump-stand-1", "Midea cold-climate heat pump on a raised stand with outdoor disconnect"),
 "hp2": ("midea-cold-climate-heat-pump-stand-2", "Midea cold-climate heat pump installed beside green siding"),
 "hp3": ("midea-cold-climate-heat-pump-stand-3", "Midea cold-climate heat pump on a galvanized stand"),
 "hp4": ("midea-cold-climate-heat-pump-lawn", "Midea cold-climate heat pump on a stand above the lawn"),
 "hp5": ("midea-cold-climate-heat-pump-fence", "Midea cold-climate heat pump beside a backyard fence"),
 "hp6": ("midea-cold-climate-heat-pump-commissioning", "Midea cold-climate heat pump with gauge hoses connected during commissioning"),
 "hp7": ("midea-cold-climate-heat-pump-backyard", "Front view of a Midea cold-climate heat pump in a backyard"),
 # white Midea outdoor units (ductless / heat pump)
 "wo1": ("midea-heat-pump-outdoor-siding", "Midea outdoor unit on a stand beside vinyl siding"),
 "wo2": ("midea-ductless-outdoor-stand", "Midea ductless outdoor unit with tidy line set and disconnect"),
 "wo3": ("midea-ductless-outdoor-brick-home", "Midea ductless outdoor unit beside a brick home with line set cover"),
 "wo4": ("midea-outdoor-unit-side-yard", "Midea outdoor unit on a raised stand in a side yard"),
 "wo5": ("midea-outdoor-unit-deck", "Midea outdoor unit on a stand next to a deck"),
 "wo6": ("midea-outdoor-unit-siding-stand", "Midea outdoor unit on a stand against siding"),
 "wo7": ("midea-outdoor-unit-evening", "Midea outdoor unit installed on a level stand"),
 "wo8": ("midea-outdoor-unit-disconnect", "Midea outdoor unit with a new outdoor disconnect"),
 # indoor wall heads
 "ih1": ("midea-wall-head-living-room", "Midea ductless wall head above framed photos in a living room"),
 "ih2": ("midea-wall-head-closeup", "Close-up of a Midea wall-mounted ductless head"),
 "ih3": ("midea-wall-head-accent-wall", "Midea ductless head on a dark feature wall"),
 "ih4": ("midea-wall-head-bright-room", "Midea ductless head above a window in a bright bedroom"),
 "ih5": ("midea-wall-head-cedar-cottage", "Midea ductless head on a cedar wall at a cottage"),
 "ih6": ("midea-wall-head-family-room", "Midea ductless head above a cabinet in a family room"),
 "ih7": ("midea-wall-head-grey-wall", "Midea ductless head mounted high on a grey wall"),
 "ih8": ("midea-wall-head-cedar-angle", "Midea ductless head in a cedar-panelled room"),
 "ih9": ("midea-wall-head-basement", "Midea ductless head heating and cooling a basement room"),
 "ih10": ("midea-wall-head-over-window", "Midea ductless head above a window in a finished room"),
 # furnaces
 "fu1": ("midea-gas-furnace-installed", "Midea two-stage gas furnace installed in a furnace room"),
 "fu2": ("midea-furnace-room-pvc-venting", "Gas furnace with PVC intake and exhaust venting"),
 "fu3": ("furnace-coil-utility-room", "Furnace with matched coil and supply plenum in a utility room"),
 # thermostats
 "th1": ("ecobee-smart-thermostat", "ecobee smart thermostat installed for heat pump control"),
 "th2": ("ecobee-thermostat-closeup", "Close-up of an ecobee smart thermostat screen"),
}

GALLERY = {
 "/heat-pump/": ("Recent heat pump installations", ["hp6", "hp1", "hp2", "wo1", "hp5", "wo8", "hp7", "th1"]),
 "/heat-pump/cold-climate/": ("Cold-climate heat pumps we've installed", ["hp3", "hp2", "hp5", "hp6", "hp7", "hp4", "hp1", "wo4"]),
 "/heat-pump/central/": ("Ducted heat pump installs", ["hp1", "fu3", "hp4", "hp7", "fu2", "hp3"]),
 "/heat-pump/hybrid-furnace-systems/": ("Hybrid furnace and heat pump installs", ["fu2", "hp2", "fu1", "th1", "hp5", "fu3", "hp3", "th2"]),
 "/heat-pump/electric-air-handler-systems/": ("Heat pump outdoor units we've installed", ["hp7", "hp6", "hp4", "wo8", "hp1", "wo5"]),
 "/heat-pump/repair-maintenance/": ("Heat pumps we install and service", ["hp4", "wo7", "hp5", "wo2", "hp2", "wo6"]),
 "/ac/": ("Recent cooling installs", ["wo5", "ih1", "wo3", "ih4", "wo4", "ih3", "wo8", "ih7"]),
 "/ac/repair-maintenance/": ("Cooling systems we install and service", ["wo2", "ih2", "wo6", "ih10", "wo1", "ih6"]),
 "/ac/ductless-mini-split/": ("Recent ductless mini-split installs", ["ih4", "wo2", "ih1", "ih5", "wo3", "ih3", "ih9", "wo4"]),
 "/ac/ductless-mini-split/repair/": ("Ductless systems we install and service", ["ih2", "wo7", "ih6", "ih8", "wo8", "ih10"]),
 "/ac/multi-zone-ductless-system/": ("Multi-room ductless installs", ["ih5", "ih1", "wo5", "ih4", "ih9", "ih3", "ih10", "wo3"]),
 "/furnace/": ("Recent furnace installations", ["fu2", "fu1", "fu3", "th1"]),
 "/furnace/high-efficiency/": ("High-efficiency furnaces we've installed", ["fu1", "fu2", "fu3", "th2"]),
 "/furnace/repair-maintenance/": ("Furnaces we install and service", ["fu3", "fu2", "fu1", "th1"]),
 "/services/thermostats/": ("Smart thermostats we've installed", ["th1", "th2"]),
 "/services/hvac-installation-replacement/": ("Recent HVAC installations", ["hp6", "fu2", "ih4", "wo3", "hp2", "fu1", "ih5", "th1"]),
 "/services/hvac-repair-maintenance/": ("Systems we install and service", ["fu1", "hp4", "wo2", "ih2", "fu3", "hp7"]),
 "/services/emergency-hvac/": ("Systems our crews keep running", ["fu2", "hp1", "wo1", "fu1", "hp5", "ih7"]),
}
