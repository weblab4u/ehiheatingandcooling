"""Draws one infographic per blog post into assets/img/infographics/.

Run:  python3 tools/make_infographics.py
Writes <slug>.webp (1620 px wide, for the full-size link) and <slug>-800.webp (page size).
Layout is in 1080-px logical units, drawn at 1.5x. Text is wrapped with the real Inter metrics,
so copy can change freely. Same copy rules as the site: no dashes, no banned words, no invented facts.
"""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT = os.path.join(ROOT, "assets/fonts/inter-latin.woff2")
OUT = os.path.join(ROOT, "assets/img/infographics")
S = 1.5                       # draw scale
W = 1080                      # logical width
PAD = 64

NAVY, BLUE, BLUE_DARK, BLUE_LIGHT = "#0B2540", "#0B5FA8", "#083F70", "#E8F2FB"
GREEN, GREEN_DARK, GREEN_LIGHT = "#128535", "#0E6B2A", "#E6F5EA"
TEXT, MUTED, LINE, SOFT = "#1E2A38", "#5A6B7C", "#E2E8EF", "#F5F8FB"
RED, RED_LIGHT = "#B42318", "#FDECEA"

_fonts = {}
def font(size, weight="Regular"):
    k = (size, weight)
    if k not in _fonts:
        f = ImageFont.truetype(FONT, round(size * S))
        f.set_variation_by_name(weight)
        _fonts[k] = f
    return _fonts[k]

def wrap(text, f, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if f.getlength(t) <= maxw * S or not cur:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

class Canvas:
    """Two passes: measure (draw=None) to get the height, then paint."""
    def __init__(self, height=None):
        self.h = height
        self.im = Image.new("RGB", (round(W * S), round(height * S)), "white") if height else None
        self.d = ImageDraw.Draw(self.im) if height else None
    def rect(self, x, y, w, h, fill, r=0, outline=None):
        if self.d: self.d.rounded_rectangle([x * S, y * S, (x + w) * S, (y + h) * S], radius=r * S, fill=fill, outline=outline, width=round(2 * S) if outline else 0)
    def circle(self, cx, cy, r, fill):
        if self.d: self.d.ellipse([(cx - r) * S, (cy - r) * S, (cx + r) * S, (cy + r) * S], fill=fill)
    def line(self, pts, fill, width):
        if self.d: self.d.line([(x * S, y * S) for x, y in pts], fill=fill, width=round(width * S), joint="curve")
    def text(self, x, y, s, size, weight="Regular", fill=TEXT, anchor="la"):
        if self.d: self.d.text((x * S, y * S), s, font=font(size, weight), fill=fill, anchor=anchor)
    def para(self, x, y, s, size, maxw, weight="Regular", fill=TEXT, lh=1.38):
        """Wrapped paragraph; returns the y below it."""
        for ln in wrap(s, font(size, weight), maxw):
            self.text(x, y, ln, size, weight, fill)
            y += size * lh
        return y
    def para_h(self, s, size, maxw, weight="Regular", lh=1.38):
        return len(wrap(s, font(size, weight), maxw)) * size * lh

# ---------------------------------------------------------------- icons (simple strokes)
def icon_check(c, cx, cy, r=17, bg=GREEN):
    c.circle(cx, cy, r, bg)
    c.line([(cx - r * .45, cy), (cx - r * .1, cy + r * .38), (cx + r * .5, cy - r * .35)], "white", 4)
def icon_x(c, cx, cy, r=17):
    c.circle(cx, cy, r, RED)
    k = r * .38
    c.line([(cx - k, cy - k), (cx + k, cy + k)], "white", 4)
    c.line([(cx - k, cy + k), (cx + k, cy - k)], "white", 4)
def badge_num(c, cx, cy, n, r=22, bg=BLUE):
    c.circle(cx, cy, r, bg)
    c.text(cx, cy + 1, str(n), 24, "Bold", "white", "mm")

# ---------------------------------------------------------------- blocks
def header(c, y, eyebrow, title, subtitle):
    inner = W - 2 * PAD
    h = 56 + 26 + 18 + c.para_h(title, 54, inner, "ExtraBold", 1.12) + 18 + c.para_h(subtitle, 26, inner, lh=1.42) + 56
    c.rect(0, y, W, h, NAVY)
    c.rect(0, y + h - 10, W, 10, GREEN)
    yy = y + 56
    c.text(PAD, yy, eyebrow.upper(), 20, "Bold", "#8FD3A3"); yy += 26 + 18
    yy = c.para(PAD, yy, title, 54, inner, "ExtraBold", "white", 1.12) + 18
    c.para(PAD, yy, subtitle, 26, inner, fill="#D6E2EE", lh=1.42)
    return y + h

def section_title(c, y, n, title):
    badge_num(c, PAD + 22, y + 22, n, bg=GREEN)
    c.text(PAD + 60, y + 22, title, 34, "Bold", NAVY, "lm")
    return y + 44 + 22

def cards(c, y, items, cols=2, accent=BLUE):
    gap, inner = 22, W - 2 * PAD
    cw = (inner - gap * (cols - 1)) / cols
    tw = cw - 2 * 26
    rows = [items[i:i + cols] for i in range(0, len(items), cols)]
    for row in rows:
        rh = max(26 + c.para_h(t, 26, tw, "Bold", 1.2) + 10 + c.para_h(b, 22, tw) + 24 for t, b in row)
        for i, (t, b) in enumerate(row):
            x = PAD + i * (cw + gap)
            c.rect(x, y, cw, rh, BLUE_LIGHT, 16)
            c.rect(x, y, 8, rh, accent, 0)
            yy = c.para(x + 26, y + 26, t, 26, tw, "Bold", BLUE_DARK, 1.2) + 10
            c.para(x + 26, yy, b, 22, tw, fill=TEXT)
        y += rh + gap
    return y - gap

def numbered(c, y, items):
    tw = W - 2 * PAD - 70
    for n, s in enumerate(items, 1):
        h = max(48, c.para_h(s, 26, tw, "SemiBold"))
        badge_num(c, PAD + 22, y + 18, n)
        c.para(PAD + 70, y + 2, s, 26, tw, "SemiBold", TEXT)
        y += h + 16
    return y - 16

def flags(c, y, items, bad=True):
    tw = W - 2 * PAD - 70
    for s in items:
        h = max(40, c.para_h(s, 25, tw))
        (icon_x if bad else icon_check)(c, PAD + 20, y + 16)
        c.para(PAD + 64, y + 1, s, 25, tw, fill=TEXT)
        y += h + 14
    return y - 14

def panel(c, y, items, fill, bad):
    """List inside a tinted panel."""
    h = 28 + (flags(Canvas(), 0, items, bad)) + 28
    c.rect(PAD - 16, y, W - 2 * PAD + 32, h, fill, 18)
    flags(c, y + 28, items, bad)
    return y + h

def timeline(c, y, steps):
    x0, tw = PAD + 22, W - 2 * PAD - 76
    top = y
    pos = []
    for t, b in steps:
        h = c.para_h(t, 27, tw, "Bold", 1.2) + 6 + c.para_h(b, 22, tw)
        pos.append((y, h)); y += h + 26
    c.line([(x0, top + 20), (x0, pos[-1][0] + 20)], LINE, 5)
    for n, ((t, b), (yy, h)) in enumerate(zip(steps, pos), 1):
        badge_num(c, x0, yy + 20, n, 22, GREEN if n == 4 else BLUE)
        y2 = c.para(PAD + 76, yy + 2, t, 27, tw, "Bold", NAVY, 1.2) + 6
        c.para(PAD + 76, y2, b, 22, tw, fill=MUTED)
    return y - 26

def table(c, y, head, rows):
    inner = W - 2 * PAD
    rh = 52
    c.rect(PAD, y, inner, rh, BLUE_DARK, 12)
    c.text(PAD + 24, y + rh / 2, head[0], 22, "Bold", "white", "lm")
    c.text(PAD + inner - 24, y + rh / 2, head[1], 22, "Bold", "white", "rm")
    y += rh
    for i, (a, b) in enumerate(rows):
        c.rect(PAD, y, inner, rh, SOFT if i % 2 == 0 else "white")
        c.text(PAD + 24, y + rh / 2, a, 24, "Medium", TEXT, "lm")
        c.text(PAD + inner - 24, y + rh / 2, b, 24, "Bold", NAVY, "rm")
        y += rh
    c.rect(PAD, y - rh * (len(rows) + 1), inner, rh * (len(rows) + 1), None, 12, LINE)
    return y

def callout(c, y, title, body, fill=GREEN_LIGHT, edge=GREEN, tcol=GREEN_DARK):
    tw = W - 2 * PAD - 56
    h = 28 + c.para_h(title, 27, tw, "Bold", 1.2) + 8 + c.para_h(body, 23, tw) + 26
    c.rect(PAD, y, W - 2 * PAD, h, fill, 16)
    c.rect(PAD, y, 8, h, edge)
    yy = c.para(PAD + 32, y + 28, title, 27, tw, "Bold", tcol, 1.2) + 8
    c.para(PAD + 32, yy, body, 23, tw, fill=TEXT)
    return y + h

def footer(c, y, note):
    inner = W - 2 * PAD
    h = 40 + 80 + 20 + c.para_h(note, 19, inner) + 36
    c.rect(0, y, W, h, SOFT)
    c.rect(0, y, W, 2, LINE)
    if c.im:
        logo = Image.open(os.path.join(ROOT, "assets/img/ehi-logo.webp")).convert("RGBA")
        lh = round(80 * S); logo = logo.resize((round(logo.width * lh / logo.height), lh), Image.LANCZOS)
        c.im.paste(logo, (round(PAD * S), round((y + 40) * S)), logo)
    c.text(W - PAD, y + 62, "efficienthomeimprovements.ca", 24, "Bold", NAVY, "rm")
    c.text(W - PAD, y + 98, "1-647-694-5845", 24, "SemiBold", GREEN_DARK, "rm")
    c.para(PAD, y + 40 + 80 + 20, note, 19, inner, fill=MUTED)
    return y + h

# ---------------------------------------------------------------- content
CREDS = [("TSSA registration", "Gas work: the company's fuels registration and the technician's gas certificate"),
         ("Refrigeration licence", "For anyone opening the refrigerant circuit on an AC or heat pump"),
         ("ECRA / ESA", "A licensed electrical contractor for the 240V circuit, with the ESA notification filed"),
         ("WSIB and insurance", "A WSIB clearance certificate and a liability insurance certificate")]

def city_doc(city, questions, red_flags, homes_title, homes):
    def build(c):
        y = header(c, 0, "Cheat sheet · take it to every quote", f"Hiring an HVAC company in {city}",
                   "Check the credentials, ask seven questions, and walk away from the red flags. Here's the whole guide on one page.")
        y = section_title(c, y + 52, 1, "Check 4 credentials before the visit")
        y = cards(c, y, CREDS)
        y = section_title(c, y + 52, 2, "Ask these 7 questions before you sign")
        y = numbered(c, y, questions)
        y = section_title(c, y + 52, 3, "Walk away if you see")
        y = panel(c, y, red_flags, RED_LIGHT, True)
        y = section_title(c, y + 52, 4, homes_title)
        y = panel(c, y, homes, GREEN_LIGHT, False)
        y = callout(c, y + 44, "The rebate rule that costs people money",
                    "Ontario's heat pump rebate needs pre-approval before installation. A company that installs first and sorts out the rebate later has cost you the rebate.",
                    BLUE_LIGHT, BLUE, BLUE_DARK)
        return footer(c, y + 52, f"From our guide: How to choose an HVAC company in {city}. General guidance, not legal advice. Program terms can change, so confirm eligibility before installation.")
    return build

def federal_doc(c):
    y = header(c, 0, "Ontario heat pump rebates · updated November 3, 2026", "Two heat pump rebates. One order of steps.",
               "Ontario's Home Renovation Savings Program and the federal National Heat Pump Rebate are separate programs. Here's how to protect both.")
    y = section_title(c, y + 52, 1, "Two separate programs")
    y = cards(c, y, [
        ("Ontario: Home Renovation Savings", "Up to $7,500 for homes heated by electricity, oil, propane or wood. Commonly up to $2,000 for Enbridge gas-heated homes. Pre-approval required before installation."),
        ("Federal: National Heat Pump Rebate", "$2,000, or up to $10,000 for income-qualified households. Installs from November 1, 2026 may qualify retroactively. Applications expected in early 2027."),
    ])
    y = section_title(c, y + 52, 2, "The order that protects both")
    y = timeline(c, y + 4, [
        ("Check your Ontario tier", "Your current heating fuel decides it."),
        ("Size the heat pump for the whole home", "From a heat-loss calculation, not a rule of thumb."),
        ("Pick a model that's on both lists", "NRCan's qualified products list for Ontario, and the federal eligible product list by AHRI number."),
        ("Get Ontario pre-approval", "Before anything is installed. Ontario's rebate can't look back."),
        ("Install with an HVAC contractor", "On or after November 1, 2026 for the federal retroactive window."),
        ("Keep your receipt", "Your name and address, the installer, make, model and AHRI number, number of units and total cost."),
        ("Apply federally when the portal opens", "Expected in early 2027. Receipts must be submitted within 6 months."),
    ])
    y = section_title(c, y + 52, 3, "Federal $10,000 tier: Ontario income cut-offs")
    y = table(c, y, ("Household size", "After-tax income at or below"),
              [("1 person", "$46,981"), ("2 people", "$92,884"), ("3 people", "$119,850"), ("4 people", "$146,217"), ("5 or more people", "$158,202")])
    c.para(PAD, y + 12, "2025 dollars, as published by the Government of Canada. Above the line, the federal rebate is $2,000.", 19, W - 2 * PAD, fill=MUTED)
    y = callout(c, y + 70, "No combined total is guaranteed",
                "Getting both depends on meeting each program's rules. Federal funding is subject to approval, and program details are still being finalized.",
                "#FFF6E5", "#B7791F", "#7A4E0B")
    return footer(c, y + 52, "Sources: Government of Canada, National Heat Pump Rebate page (checked November 3, 2026), and the Home Renovation Savings Program. Program terms can change, so confirm eligibility before installation.")

DOCS = {
 "national-heat-pump-rebate-ontario": federal_doc,
 "how-to-choose-an-hvac-company-in-toronto": city_doc("Toronto",
    ["Can I have the quote in writing with model numbers?", "Who will actually do the install?", "Which permits and notifications does this job need, and who files them?",
     "How did you size this?", "Who registers the warranty, and what are the terms?", "Will you handle the rebate pre-approval before installation?", "What happens if the price changes?"],
    ["A firm price over the phone without a visit", "“This price is only good today”", "No permit, or “you don't need one”", "The pitch keeps drifting to a rental",
     "Cash only, or a large deposit before any paperwork", "No model numbers on the quote", "Scare tactics during a repair call"],
    "What changes the answer in Toronto",
    ["Century semis and row houses", "Tight lots and laneways", "Post-war bungalows and split-levels", "Condo townhomes and low-rise condos"]),
 "how-to-choose-an-hvac-company-in-barrie": city_doc("Barrie",
    ["Will the quote list the exact model numbers?", "Who does the install?", "Who pulls the permits and books the ESA inspection?", "How will you size it?",
     "Who registers the warranty?", "Will you file the rebate pre-approval before installing?", "What happens if the price changes?"],
    ["A price over the phone without a visit", "“This price is only good today”", "No permit, no inspection, no mention of the ESA", "A hard push to rent instead of buy",
     "Cash only, or a deep discount for cash", "No model numbers on the quote", "No local track record you can check"],
    "What changes the answer in Barrie",
    ["Outdoor unit placement above snow and roof slide", "Sizing at Barrie's colder design temperature", "Defrost and drainage", "Vent terminations", "Housing stock", "Summer cooling still counts"]),
 "how-to-choose-an-hvac-company-in-hamilton": city_doc("Hamilton",
    ["Can I have the quote in writing with model numbers?", "Who does the install?", "Who files the permits and notifications?", "How did you size this?",
     "Who registers the warranty?", "Will you handle the rebate pre-approval?", "What happens if the price changes?"],
    ["A price over the phone without a visit", "“This price is only good today”", "No permit, no notification", "A hard push to rent instead of buy",
     "Cash only, or a large deposit before any paperwork", "No model numbers", "Nobody looked at the electrical panel"],
    "What changes the answer in Hamilton",
    ["Century brick homes in the lower city", "Post-war homes on the Mountain", "Newer builds in Stoney Creek, Ancaster, Binbrook and Waterdown", "Humidity below the escarpment"]),
 "how-to-choose-an-hvac-company-in-mississauga": city_doc("Mississauga",
    ["Can I have the quote in writing, with model numbers?", "Who actually does the install?", "Which permits does this job need, and who pulls them?", "How did you size it?",
     "Who registers the warranty, and what does the labour side cover?", "Will you handle rebate pre-approval before the install?", "What happens if the price changes?"],
    ["A firm price over the phone without a visit", "“This price is only good today”", "No permit, or “we don't bother with ESA for heat pumps”", "A push to rent instead of buy",
     "Cash only, or a big discount for cash", "No model numbers", "Condemning the furnace without showing you"],
    "What changes the answer in Mississauga",
    ["1960s and 1970s bungalows and backsplits", "1990s subdivisions", "Townhomes"]),
 "how-to-choose-an-hvac-company-in-ottawa": city_doc("Ottawa",
    ["Can I have the quote in writing, with model numbers?", "Who actually does the install?", "What permits or notifications are needed, and who files them?", "How did you size this system?",
     "Who registers the warranty, and what does it cover?", "Is my rebate pre-approved before install day?", "What happens if the price changes once you're in the house?"],
    ["A price over the phone with no site visit", "“Today only” pricing", "No permit, no ESA notification, or “you don't need one”", "A push toward a rental when you asked to buy",
     "Cash only, or a big discount for cash", "No model numbers on the quote", "A heat pump quote with no mention of backup heat or capacity at -15°C",
     "Running down the rebate program instead of explaining it"],
    "What changes the answer in Ottawa",
    ["Sizing has to be done for the cold", "Older homes inside the Greenbelt have their own problems", "The suburbs are reaching replacement age", "Snow is an installation detail"]),
}

def render(slug, build):
    h = build(Canvas())
    c = Canvas(h); build(c)
    os.makedirs(OUT, exist_ok=True)
    full = c.im
    full.save(os.path.join(OUT, f"{slug}.webp"), "WEBP", quality=82, method=6)
    small = full.resize((800, round(full.height * 800 / full.width)), Image.LANCZOS)
    small.save(os.path.join(OUT, f"{slug}-800.webp"), "WEBP", quality=82, method=6)
    print(f"{slug}: {full.width}x{full.height}")

if __name__ == "__main__":
    for slug, build in DOCS.items():
        render(slug, build)
