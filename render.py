"""Renders entry.png: a one-page front of the world's news for Tuesday 17 November 2026.

Every item comes from Wikipedia's Portal:Current_events/2026_November_17 and names the
outlet that page cites. Run: python render.py  (needs Pillow and the Windows fonts below).
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
F = "C:/Windows/Fonts/"
def font(name, size): return ImageFont.truetype(F + name, size)

INK = (20, 20, 24)
GREY = (95, 95, 100)
PAPER = (250, 247, 240)
RULE = (40, 40, 40)
RED = (178, 28, 36)
REG = {
    "EUROPE": (31, 84, 160),
    "MIDDLE EAST": (178, 28, 36),
    "ASIA": (196, 110, 10),
    "AMERICAS": (24, 128, 72),
    "AFRICA": (128, 60, 150),
    "OCEANIA": (0, 128, 150),
}

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)


def wrap(text, f, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= width:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(x, y, text, f, width, fill=INK, lh=None):
    lh = lh or int(f.size * 1.18)
    for line in wrap(text, f, width):
        d.text((x, y), line, font=f, fill=fill)
        y += lh
    return y


# ---------- masthead ----------
d.rectangle([0, 0, W, 8], fill=INK)
d.text((24, 14), "THE WORLD IN ONE DAY", font=font("arialbd.ttf", 15), fill=RED)
d.text((W - 24, 14), "21 numbered stories · 6 continents · every item sourced", font=font("ariali.ttf", 15), fill=GREY, anchor="ra")
mast = font("georgiab.ttf", 50)
d.text((W // 2, 36), "Tuesday 17 November 2026", font=mast, fill=INK, anchor="ma")
d.line([24, 100, W - 24, 100], fill=RULE, width=3)
d.line([24, 104, W - 24, 104], fill=RULE, width=1)


# ---------- icons ----------
def icon_bridge(x, y, s):
    c = INK
    d.rectangle([x, y + s * 0.80, x + s, y + s], fill=(70, 120, 175))  # water
    for i in range(3):
        ax = x + i * s / 3
        d.arc([ax, y + s * 0.35, ax + s / 3, y + s * 1.05], 180, 360, fill=c, width=3)
    d.line([x, y + s * 0.38, x + s * 0.55, y + s * 0.38], fill=c, width=5)
    d.line([x + s * 0.72, y + s * 0.38, x + s, y + s * 0.38], fill=c, width=5)
    d.line([x + s * 0.55, y + s * 0.38, x + s * 0.62, y + s * 0.78], fill=RED, width=5)  # fallen span
    for k in range(3):  # flames
        fx = x + s * (0.2 + k * 0.3)
        d.polygon([(fx, y + s * 0.34), (fx + 6, y + s * 0.12), (fx + 12, y + s * 0.34)], fill=(230, 120, 20))


def icon_drone(x, y, s):
    cx, cy = x + s / 2, y + s / 2
    d.line([x + 8, y + 8, x + s - 8, y + s - 8], fill=INK, width=5)
    d.line([x + s - 8, y + 8, x + 8, y + s - 8], fill=INK, width=5)
    for px, py in [(x + 8, y + 8), (x + s - 8, y + 8), (x + 8, y + s - 8), (x + s - 8, y + s - 8)]:
        d.ellipse([px - 9, py - 4, px + 9, py + 4], outline=INK, width=2)
    d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=RED)


def icon_virus(x, y, s):
    cx, cy, r = x + s / 2, y + s / 2, s * 0.28
    import math
    for k in range(10):
        a = k * math.pi / 5
        ex, ey = cx + math.cos(a) * r * 1.6, cy + math.sin(a) * r * 1.6
        d.line([cx, cy, ex, ey], fill=REG["AMERICAS"], width=3)
        d.ellipse([ex - 4, ey - 4, ex + 4, ey + 4], fill=REG["AMERICAS"])
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=REG["AMERICAS"])
    d.ellipse([cx - r * 0.4, cy - r * 0.5, cx, cy - r * 0.1], fill=(150, 210, 170))


def icon_ballot(x, y, s):
    d.rectangle([x + 4, y + s * 0.42, x + s - 4, y + s - 4], fill=(31, 84, 160))
    d.rectangle([x + s * 0.3, y + s * 0.40, x + s * 0.7, y + s * 0.46], fill=INK)
    d.polygon([(x + s * 0.34, y + s * 0.42), (x + s * 0.40, y + 4), (x + s * 0.78, y + s * 0.10), (x + s * 0.68, y + s * 0.42)], fill="white", outline=INK)
    d.line([x + s * 0.48, y + s * 0.2, x + s * 0.55, y + s * 0.3, x + s * 0.68, y + s * 0.12], fill=(24, 128, 72), width=3)
    d.text((x + s / 2, y + s * 0.72), "AK", font=font("arialbd.ttf", 16), fill="white", anchor="mm")


def icon_door(x, y, s):  # resignation: a person leaving a door
    d.rectangle([x + 6, y + 4, x + s * 0.55, y + s - 4], outline=INK, width=3)
    d.polygon([(x + 6, y + 4), (x + s * 0.40, y + 12), (x + s * 0.40, y + s - 12), (x + 6, y + s - 4)], fill=(196, 110, 10))
    hx = x + s * 0.78
    d.ellipse([hx - 6, y + 10, hx + 6, y + 22], fill=INK)
    d.line([hx, y + 22, hx - 2, y + s * 0.62], fill=INK, width=4)
    d.line([hx - 2, y + s * 0.62, hx - 10, y + s - 6], fill=INK, width=4)
    d.line([hx - 2, y + s * 0.62, hx + 8, y + s - 6], fill=INK, width=4)
    d.line([hx, y + 30, hx + 10, y + 42], fill=INK, width=4)


def icon_plane(x, y, s):
    d.line([x + 6, y + s * 0.3, x + s - 6, y + s * 0.65], fill=INK, width=7)
    d.polygon([(x + s * 0.45, y + s * 0.47), (x + s * 0.30, y + s * 0.85), (x + s * 0.42, y + s * 0.85), (x + s * 0.60, y + s * 0.52)], fill=INK)
    d.polygon([(x + s * 0.50, y + s * 0.47), (x + s * 0.55, y + s * 0.15), (x + s * 0.65, y + s * 0.15), (x + s * 0.62, y + s * 0.52)], fill=INK)
    d.line([x + s * 0.8, y + s * 0.7, x + s * 0.95, y + s * 0.95], fill=RED, width=4)
    d.line([x + 4, y + s - 4, x + s - 4, y + s - 4], fill=GREY, width=2)


# ---------- numbered pins and the world map ----------
import json, os
PINS = []  # ((lon, lat), number, colour)
LAND = os.environ.get("LAND_GEOJSON", "land.json")  # Natural Earth 1:110m land (public domain), not committed


def badge(cx, cy, n, col, r=8):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col, outline="white", width=1)
    d.text((cx, cy), str(n), font=font("arialbd.ttf", 10 if n > 9 else 11), fill="white", anchor="mm")


MX0, MY0, MX1, MY1 = 652, 112, 1000, 256
LAT_TOP, LAT_BOT = 78, -50


def proj(lon, lat):
    return (MX0 + (lon + 180) / 360 * (MX1 - MX0), MY0 + (LAT_TOP - lat) / (LAT_TOP - LAT_BOT) * (MY1 - MY0))


def draw_map():
    d.rectangle([MX0, MY0, MX1, MY1], fill=(222, 233, 242))
    for feat in json.load(open(LAND, encoding="utf-8"))["features"]:
        g = feat["geometry"]
        polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
        for poly in polys:
            pts = [proj(lo, max(min(la, LAT_TOP), LAT_BOT)) for lo, la in poly[0]]
            if len(pts) > 2:
                d.polygon(pts, fill=(205, 198, 182), outline=(160, 150, 130))
    d.rectangle([MX0, MY0, MX1, MY1], outline=GREY, width=1)
    for (lon, lat), n, col in PINS:
        x, y = proj(lon, lat)
        badge(x, y, n, col, r=7)
    d.text((MX1 - 4, MY1 - 3), "numbers = stories", font=font("ariali.ttf", 10), fill=GREY, anchor="rd")


# ---------- lead story ----------
y0 = 114
icon_bridge(26, y0 + 22, 92)
badge(34, y0 + 8, 1, REG["EUROPE"])
PINS.append(((36.5, 45.3), 1, REG["EUROPE"]))
d.text((132, y0), "EUROPE · RUSSIA–UKRAINE WAR", font=font("arialbd.ttf", 13), fill=REG["EUROPE"])
yy = para(132, y0 + 18, "Ukrainian drones hit the Crimean Bridge for a second day; two killed, traffic shut again",
          font("georgiab.ttf", 25), 640 - 132, lh=29)
para(132, yy + 3, "Open-source analysts report that a road section damaged the day before has collapsed into the Kerch Strait.  (Reuters; Türkiye Today)",
     font("georgiai.ttf", 14), 640 - 132, fill=GREY, lh=17)
d.line([24, 264, W - 24, 264], fill=RULE, width=1)

# ---------- second tier: four boxes ----------
tier = [
    (icon_drone, "MIDDLE EAST · IRAN WAR", "US strikes Qeshm Island; Iran fires drones at Bahrain",
     "At least six US Air Force strikes on Qeshm; the IRGC says it shot down an MQ-9 Reaper. Bahrain intercepts IRGC drones aimed at Sheikh Isa Air Base.  (Reuters; AFP; Al Jazeera)"),
    (icon_virus, "AMERICAS · HEALTH", "Measles: US, Mexico and Bolivia lose elimination status",
     "The Pan American Health Organization revokes it; the US has had over 12 months of spread and 5,700+ cases in 2026.  (AFP; Al Jazeera)"),
    (icon_door, "ASIA · MONGOLIA", "Mongolia's president Khürelsükh announces resignation",
     "Three days after an ex-Ulaanbaatar mayor accused him of embezzling from a railway project. Parliament must accept it.  (AP)"),
    (icon_ballot, "AMERICAS · US ELECTIONS", "Democrat Mary Peltola projected to unseat Alaska senator Sullivan",
     "Two weeks after Election Day, the call widens the Democrats' Senate lead.  (AP)"),
]
bw = (W - 48 - 3 * 14) / 4
by = 276
TIER_LL = [(55.9, 26.8), (-99.1, 19.4), (106.9, 47.9), (-150.0, 63.0)]
for i, (ic, kick, head, body) in enumerate(tier):
    bx = 24 + i * (bw + 14)
    ic(bx, by, 58)
    region = kick.split(" · ")[0]
    badge(bx + 6, by + 6, i + 2, REG[region])
    PINS.append((TIER_LL[i], i + 2, REG[region]))
    d.text((bx + 66, by + 4), kick.split(" · ")[0], font=font("arialbd.ttf", 12), fill=REG[region])
    d.text((bx + 66, by + 20), kick.split(" · ")[1], font=font("arialbd.ttf", 12), fill=GREY)
    yy = para(bx, by + 66, head, font("georgiab.ttf", 19), bw, lh=22)
    para(bx, yy + 4, body, font("arial.ttf", 13), bw, fill=(55, 55, 60), lh=16)
    if i:
        d.line([bx - 7, by, bx - 7, by + 236], fill=(170, 170, 170), width=1)
d.line([24, 520, W - 24, 520], fill=RULE, width=2)

# ---------- briefs by region (numbered; the numbers match the map pins) ----------
briefs = {
    "MIDDLE EAST": [
        ("Gaza", "Israeli airstrikes kill five Palestinians, including a child.", "AA", (34.4, 31.4)),
        ("West Bank", "Settlers attack homes near Jericho, killing a woman, 72, and injuring ten.", "Al Jazeera", (35.4, 32.6)),
    ],
    "EUROPE": [
        ("Czechia", "Two trains collide in Prague; 46 people injured.", "BBC", (14.4, 50.1)),
        ("Greece / N. Macedonia", "Five arrested over an alleged Iran-linked plot to kill an Israeli executive in Athens.", "AP", (21.4, 41.0)),
        ("UK", "Britain sanctions eight West Bank settlement builders and the group Tzav 9.", "AP", (-1.5, 52.5)),
    ],
    "SOUTH ASIA": [
        ("Bangladesh", "Awami League office burned in Comilla; a worker who filmed BNP clashes is killed in Fatullah.", "TBS; Views Bangladesh", (91.2, 21.5)),
    ],
    "ASIA": [
        ("Russia", "Air Force An-12 crashes near Kemerovo; all 19 on board killed.", "AP; The Independent", (86.1, 55.3)),
        ("Bangladesh", "Banned Awami League activists storm and burn a police station in Tungipara, freeing detainees.", "The Daily Star", (88.0, 24.5)),
        ("Bangladesh", "Police and border guards use tear gas on garment workers striking for higher pay around Dhaka.", "The Business Standard", (91.5, 26.0)),
        ("Malaysia", "Macron's state visit seals a strategic partnership; limited rare-earth exports to France.", "Reuters", (101.7, 3.1)),
        ("China / Canada", "Xi and Carney agree new tariff cuts ahead of the APEC summit in Shenzhen.", "AFP", (114.1, 22.5)),
    ],
    "AMERICAS": [
        ("Costa Rica", "Journalist Camilo Rodríguez shot dead in Heredia, the first such killing in 25 years.", "Univisión", (-84.1, 10.0)),
        ("Haiti", "Hundreds march in support of Salvadoran troops fighting gangs.", "Al Jazeera", (-72.3, 18.5)),
        ("Tech", "Apple Pay, iCloud and the App Store go down; Apple blames an internal update, not an attack.", "Time", (-122.0, 37.3)),
    ],
    "AFRICA": [
        ("Guinea", "Court tries 1,000+ illegal gold miners; 22 ex-officials and 202 others jailed.", "DW", (-11.0, 10.5)),
    ],
    "OCEANIA": [
        ("Australia", "Racing NSW investigates after Melbourne Cup runner So You Are is found dead in a skip bin.", "Guardian Australia", (151.2, -33.9)),
    ],
}
COLOR = dict(REG, **{"SOUTH ASIA": REG["ASIA"]})
cols = [["MIDDLE EAST", "EUROPE", "SOUTH ASIA"], ["ASIA"], ["AMERICAS", "AFRICA", "OCEANIA"]]
cw = (W - 48 - 2 * 20) / 3
bf, bb, sf = font("arialbd.ttf", 14), font("arial.ttf", 14), font("ariali.ttf", 12)
IND = 22
num = 6
for ci, regions in enumerate(cols):
    x = 24 + ci * (cw + 20)
    y = 532
    for r in regions:
        d.rectangle([x, y, x + cw, y + 20], fill=COLOR[r])
        d.text((x + 6, y + 2), r, font=font("arialbd.ttf", 14), fill="white")
        y += 26
        for place, text, src, ll in briefs[r]:
            badge(x + 8, y + 8, num, COLOR[r])
            PINS.append((ll, num, COLOR[r]))
            num += 1
            first = place.upper() + " "
            lines = wrap(first + text, bb, cw - IND - 2)
            d.text((x + IND, y), first, font=bf, fill=COLOR[r])
            off = d.textlength(first, font=bf) + 3
            d.text((x + IND + off, y), lines[0][len(first):], font=bb, fill=INK)
            y += 17
            for ln in lines[1:]:
                d.text((x + IND, y), ln, font=bb, fill=INK)
                y += 17
            d.text((x + IND, y), "— " + src, font=sf, fill=GREY)
            y += 19
        y += 3
    if ci:
        d.line([x - 10, 532, x - 10, 978], fill=(170, 170, 170), width=1)

draw_map()

# ---------- footer ----------
d.line([24, 984, W - 24, 984], fill=RULE, width=1)
d.text((24, 992), "Events of Tuesday 17 November 2026, as reported that day. Sources named after each item.",
       font=font("ariali.ttf", 13), fill=GREY)
d.text((W - 24, 992), "17 · XI · 2026", font=font("georgiab.ttf", 15), fill=INK, anchor="ra")
d.rectangle([0, H - 8, W, H], fill=INK)

img.save("entry.png", optimize=True)
print("wrote entry.png")
