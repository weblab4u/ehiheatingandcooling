# Place names people type into Google that belong to one of our city pages (from Google Search Console, November 2026).
# Used by the city service pages ("Bowmanville, Clarington") and by tools/keyword_map.py to file each query under a page.
ALIASES = {
 "whitchurch-stouffville": "stouffville", "whitchurch stouffville": "stouffville", "clarington": "bowmanville", "halton hills": "georgetown",
 "nobleton": "king-city", "schomberg": "king-city", "bolton": "caledon", "gwillimbury": "east-gwillimbury", "new tecumseth": "alliston", "angus": "alliston",
 "kitchener": "kitchener-waterloo", "waterloo": "kitchener-waterloo", "trenton": "quinte-west", "st catharines": "st-catharines", "st. catharines": "st-catharines",
 "thorold": "st-catharines", "flamborough": "hamilton", "lasalle": "windsor", "amherstburg": "windsor", "belle river": "windsor", "brant": "brantford",
 "clarence-rockland": "orleans", "rockland": "orleans", "clarence": "orleans", "keswick": "georgina", "orleans": "orleans",
}
# The municipality to name on a city's service pages, when people search for it rather than the town.
DISPLAY = {"stouffville": "Whitchurch-Stouffville", "bowmanville": "Clarington", "courtice": "Clarington", "georgetown": "Halton Hills",
           "king-city": "Nobleton and King Township", "caledon": "Bolton", "alliston": "New Tecumseth", "quinte-west": "Trenton"}
# Named on the city page as part of the area we cover: municipalities that contain the town, and places already on our
# service-area list. Neighbouring towns that are not on the list are left off.
SERVED = {"stouffville": ["Whitchurch-Stouffville"], "bowmanville": ["Clarington"], "courtice": ["Clarington"], "georgetown": ["Halton Hills"],
          "king-city": ["King Township", "Nobleton"], "caledon": ["Bolton"], "alliston": ["New Tecumseth", "Angus"], "quinte-west": ["Trenton"],
          "st-catharines": ["Thorold"], "georgina": ["Keswick"], "brantford": ["Brant County"]}
