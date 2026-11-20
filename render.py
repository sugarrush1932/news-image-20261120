#!/usr/bin/env python3
"""Render the edition-20 front page: 'The World Today' for 20 November 2026.

Draws a dense cream-paper broadsheet (1024x1024) with Pillow: masthead,
stat strip, one lead story, a grid of illustrated panels, an ALSO ON briefs
block, a pinned world map beside a DATE CHECK box, a UTC timeline and a
footer. Run:  python3 render.py   # writes entry.png beside this file

All facts were checked against live reporting on 20 Nov 2026. Where an
outcome was not yet known at build time (COP31's final deal, Akvan's
landfall) the page says so instead of inventing one.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 227)
INK = (20, 20, 20)
RED = (166, 38, 31)
BLUE = (29, 78, 137)
TEAL = (15, 107, 92)
GOLD = (138, 109, 27)
TINT = (239, 231, 211)
PANEL = (250, 246, 236)
RULE = (20, 20, 20)
GREY = (90, 86, 76)

FD = "/usr/share/fonts/truetype/dejavu"
def font(name, size):
    return ImageFont.truetype(f"{FD}/{name}.ttf", size)

F_SERIF_B = lambda s: font("DejaVuSerif-Bold", s)
F_SERIF = lambda s: font("DejaVuSerif", s)
F_SANS_B = lambda s: font("DejaVuSans-Bold", s)
F_SANS = lambda s: font("DejaVuSans", s)

# ---------------------------------------------------------------- stories
# Panel: (kicker, headline, deck, icon, accent). Decks are short on purpose:
# grid panels are 236 px wide, so a deck gets two lines at ~32 chars each.
PANELS = [
    ("LAW · THE HAGUE", "MYANMAR GUILTY OF GENOCIDE",
     "The world court rules 9–6 that the 2017 crackdown on the Rohingya was genocide — the first state ever convicted. Safe return and reparations ordered.",
     "scales", RED),
    ("MARKETS · NEW YORK", "ANTHROPIC'S $81.3BN DEBUT",
     "Opens $111.50, closes $97.17, up 17% on $83.",
     "chart", BLUE),
    ("CLIMATE · ANTALYA", "COP31 CLOSING DAY, NO DEAL YET",
     "Draft cut 144→80 paras; fossil fuels deleted. No deal yet.",
     "globe", TEAL),
    ("WEATHER · INDIA", "CYCLONE AKVAN BEARS DOWN",
     "80,000 evacuated in Odisha as the storm nears landfall.",
     "storm", BLUE),
    ("SUMMIT · SHENZHEN", "TRUMP, XI, PUTIN MEET",
     "First three-way summit; no Ukraine deal.",
     "flags", RED),
    ("WAR · KYIV", "STRIKES HIT TWO EMBASSIES",
     "Strikes damage Austrian and Dutch embassies.",
     "bridge", INK),
    ("TECH · CALIFORNIA", "GEMINI TAKES OVER THE MAC",
     "Gemini now runs Mac apps for paying US subscribers.",
     "spark", TEAL),
    ("MARKETS · WORLD", "WALL STREET SLIDES 2%+",
     "Wall Street slides; Sensex jumps 1.21% to 83,022.",
     "down", RED),
    ("SPORT · WELLINGTON", "NICHOLLS 113* RESCUES NZ",
     "New Zealand 273 for 5 on day two of the first Test.",
     "cricket", TEAL),
    ("SPORT · JOHANNESBURG", "SOUTH AFRICA TOP OF THE WORLD",
     "Harmer 6 for 51 seals the series; SA top the Test table.",
     "trophy", GOLD),
    ("CLIMATE · SUVA", "FIJI DECLARES A DROUGHT DISASTER",
     "El Niño leaves taps dry; disaster declared.",
     "sun", GOLD),
    ("LAW · SEOUL", "EX-PM'S CONVICTION OVERTURNED",
     "Top court quashes Han Duck-soo's martial-law conviction.",
     "court", BLUE),
    ("MIDDLE EAST · GAZA", "TWO KILLED IN GAZA STRIKES",
     "Two killed in Israeli strikes; Hezbollah site hit.",
     "pin", RED),
]

BRIEFS = [
    ("APEC", "Xi urges deeper Asia-Pacific trade and tech cooperation in Shenzhen."),
    ("UKRAINE", "Kushner: Russia 'comfortable' with Article 5-style security guarantees."),
    ("UKRAINE", "Zelenskyy: NATO membership is Ukraine's best protection."),
    ("EUROPE", "Tusk heads to Berlin for Ukraine crisis talks with US envoys due."),
    ("EUROPE", "EU sanctions 143 more Russians — banks, oil firms, hackers."),
    ("EUROPE", "Five EU states plan a migrant return centre in Rwanda."),
    ("MIDDLE EAST", "Israel says it struck a Hezbollah weapons site in east Lebanon."),
    ("MIDDLE EAST", "Syria hails a historic UN resolution on post-war progress."),
    ("MIDDLE EAST", "Iran war costs pass $48bn, AP reports."),
    ("MIDDLE EAST", "US intelligence: Iran still holds at least 2,500 missiles."),
    ("MIDDLE EAST", "US and Venezuela sign a deal to restore military cooperation."),
    ("ASIA", "North Korea expanding uranium enrichment at Yongbyon, watchdog says."),
    ("ASIA", "Fire at Muhammad Yunus's ancestral home; arson suspected."),
    ("ASIA", "Modi meets the Prince and Princess of Wales in New Delhi."),
    ("ASIA", "Australia sanctions Israeli settlers over West Bank expansion."),
    ("ASIA", "LPG tanker that sank off Bulgaria was hit by projectiles, official says."),
    ("ASIA", "Japan's PM Takaichi seeks continued dialogue with China."),
    ("INDIA", "Defence deal worth ₹1,976 crore to upgrade the Navy's Barak system."),
    ("TECH", "Nvidia reports $115.8bn quarterly revenue, up 103% on the year."),
    ("TECH", "OpenAI ships GPT-6.2 Astra and Sol; Google launches Gemini 4 Neon."),
    ("TECH", "Meta's Muse agent passes 10m downloads in 40 days."),
    ("TECH", "IEA: AI data-centre emissions set to rise 70% by 2030."),
    ("ARCHAEOLOGY", "Gold artefacts unearthed at an ancient necropolis in Egypt."),
    ("DIPLOMACY", "UAE denounces Somalia's expulsion of its ambassador."),
    ("SPORT", "Dhoni retires from IPL playing; Bavuma out of the Bangladesh decider."),
    ("SPORT", "England beat Australia by 97 runs in the Hobart ODI decider."),
    ("SPORT", "Pakistan v Sri Lanka: Sri Lanka lead by 82 with one wicket left."),
    ("SPORT", "Women's Asian Hockey Champions Trophy opens today."),
]

STATS = [
    ("9–6", "ICJ vote: genocide"),
    ("$97.17", "ANT close, +17%"),
    ("$81.3bn", "record IPO"),
    ("80,000", "evacuated: Akvan"),
    ("144→80", "COP draft paras"),
    ("113*", "Nicholls, Wellington"),
]

# (label, event) — every timestamp is one actually reported, UTC unless noted.
TIMELINE = [
    ("19 NOV 16:50 GMT", "ANT first trade $111.50"),
    ("19 NOV 21:00 GMT", "ANT closes $97.17"),
    ("19 NOV, THE HAGUE", "ICJ: Myanmar guilty"),
    ("19 NOV 23:41 UTC", "COP31 draft drops fossils"),
    ("20 NOV 00:01 UTC", "Russian markets fall"),
    ("20 NOV 00:10 UTC", "Kyiv embassies hit"),
    ("20 NOV, MORNING IST", "Akvan landfall due"),
]

# (name, lon, lat) for the pinned map.
PINS = [
    ("The Hague", 4.5, 52.0), ("Shenzhen", 114.0, 22.5),
    ("Antalya", 30.7, 36.9), ("Odisha", 85.5, 20.0),
    ("Kyiv", 30.5, 50.4), ("Wellington", 174.8, -41.3),
    ("New York", -74.0, 40.7), ("Gaza", 34.5, 31.5),
    ("Cox's Bazar", 92.0, 21.4), ("Fiji", 178.0, -17.7),
    ("Seoul", 127.0, 37.5), ("Berlin", 13.4, 52.5),
]

# Coarse continent outlines (lon, lat), equirectangular, drawn small.
CONTINENTS = {
    "NA": [(-168, 66), (-140, 70), (-125, 72), (-110, 68), (-95, 69), (-85, 66),
           (-80, 73), (-65, 60), (-55, 47), (-65, 44), (-75, 35), (-80, 26),
           (-90, 21), (-97, 16), (-105, 20), (-117, 33), (-125, 40),
           (-125, 49), (-140, 60), (-158, 58), (-168, 66)],
    "SA": [(-80, 9), (-72, 12), (-62, 9), (-52, 5), (-50, 0), (-44, -3),
           (-35, -8), (-40, -20), (-48, -28), (-58, -35), (-65, -41),
           (-68, -52), (-73, -50), (-73, -37), (-70, -20), (-80, -5), (-80, 9)],
    "AF": [(-6, 35), (10, 37), (20, 32), (32, 31), (35, 28), (43, 12),
           (51, 11), (48, -1), (40, -10), (36, -18), (32, -29), (26, -34),
           (19, -35), (15, -27), (12, -18), (9, -1), (-8, 4), (-17, 15),
           (-17, 21), (-10, 31), (-6, 35)],
    "EU": [(-10, 37), (-9, 43), (-2, 44), (0, 46), (-2, 50), (3, 51),
           (8, 57), (10, 59), (18, 56), (21, 55), (24, 59), (28, 71),
           (32, 70), (40, 68), (40, 60), (30, 59), (28, 46), (23, 40),
           (19, 42), (12, 44), (8, 44), (3, 42), (0, 39), (-10, 37)],
    "AS": [(32, 70), (40, 68), (50, 69), (60, 69), (70, 72), (80, 73),
           (95, 76), (110, 74), (125, 73), (140, 72), (158, 70), (170, 67),
           (178, 65), (170, 60), (162, 56), (150, 59), (142, 50), (135, 43),
           (127, 40), (122, 31), (120, 22), (110, 20), (105, 9), (100, 6),
           (97, 16), (92, 21), (88, 22), (80, 13), (77, 8), (72, 20),
           (66, 25), (61, 25), (57, 27), (50, 29), (44, 29), (39, 21),
           (35, 28), (32, 31), (32, 70)],
    "OC": [(114, -22), (114, -35), (124, -33), (130, -32), (136, -35),
           (140, -38), (146, -39), (150, -37), (153, -27), (146, -19),
           (142, -11), (136, -12), (132, -11), (126, -14), (122, -17),
           (114, -22)],
}

# ---------------------------------------------------------------- helpers
def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns a list of lines that fit `width` px."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def text_block(draw, xy, lines, fnt, fill=INK, leading=None):
    x, y = xy
    lh = leading or int(fnt.size * 1.18)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y

def hline(draw, x0, x1, y, fill=RULE, width=2):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)

# ---------------------------------------------------------------- icons
def icon(draw, kind, box, accent):
    """Flat pictogram inside box (x0, y0, x1, y1)."""
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    w, h = x1 - x0, y1 - y0
    draw.rounded_rectangle(box, radius=6, fill=TINT, outline=accent, width=2)
    if kind == "scales":
        draw.line([(cx, y0 + 8), (cx, y1 - 8)], fill=accent, width=3)
        draw.line([(cx - 16, y0 + 14), (cx + 16, y0 + 14)], fill=accent, width=3)
        for dx in (-16, 16):
            draw.line([(cx + dx, y0 + 14), (cx + dx, y0 + 26)], fill=accent, width=2)
            draw.polygon([(cx + dx - 9, y0 + 26), (cx + dx + 9, y0 + 26),
                          (cx + dx, y0 + 36)], fill=accent)
        draw.ellipse([cx - 4, y0 + 5, cx + 4, y0 + 13], fill=accent)
    elif kind == "chart":
        bars = [10, 16, 13, 22, 28, 36]
        bw = (w - 16) // len(bars)
        for i, bh in enumerate(bars):
            bx = x0 + 8 + i * bw
            draw.rectangle([bx, y1 - 8 - bh, bx + bw - 3, y1 - 8], fill=accent)
        draw.line([(x0 + 8, y1 - 8 - 40), (x1 - 8, y1 - 8 - 40)],
                  fill=RED, width=2)
    elif kind == "globe":
        draw.ellipse([cx - 18, cy - 18, cx + 18, cy + 18], outline=accent, width=3)
        draw.ellipse([cx - 8, cy - 18, cx + 8, cy + 18], outline=accent, width=2)
        draw.line([(cx - 18, cy), (cx + 18, cy)], fill=accent, width=2)
        draw.arc([cx - 18, cy - 26, cx + 18, cy - 10], 200, 340, fill=GOLD, width=3)
    elif kind == "storm":
        for r in (6, 12, 18):
            draw.arc([cx - r, cy - r, cx + r, cy + r], 20, 300, fill=accent, width=3)
        draw.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=RED)
        for dx in (-14, 0, 14):
            draw.line([(cx + dx, y1 - 12), (cx + dx, y1 - 6)], fill=BLUE, width=2)
    elif kind == "flags":
        for i, col in enumerate((RED, BLUE, TEAL)):
            px = x0 + 12 + i * 16
            draw.line([(px, y0 + 10), (px, y1 - 8)], fill=INK, width=2)
            draw.polygon([(px, y0 + 10), (px + 13, y0 + 14), (px, y0 + 19)],
                         fill=col)
        draw.line([(x0 + 8, y1 - 8), (x1 - 8, y1 - 8)], fill=INK, width=2)
    elif kind == "bridge":
        draw.arc([x0 + 6, y0 + 14, x1 - 6, y1 - 6], 180, 360, fill=accent, width=3)
        draw.line([(x0 + 8, y0 + 22), (x1 - 8, y0 + 22)], fill=accent, width=2)
        for dx in (-12, 0, 12):
            draw.line([(cx + dx, y0 + 20), (cx + dx, y0 + 6)], fill=accent, width=2)
        draw.polygon([(x1 - 12, y0 + 2), (x1 - 4, y0 + 8), (x1 - 12, y0 + 14)],
                     fill=RED)
    elif kind == "spark":
        pts = [(cx, y0 + 6), (cx + 5, cy - 4), (cx + 16, cy - 4), (cx + 7, cy + 2),
               (cx + 11, cy + 14), (cx, cy + 7), (cx - 11, cy + 14),
               (cx - 7, cy + 2), (cx - 16, cy - 4), (cx - 5, cy - 4)]
        draw.polygon(pts, fill=GOLD)
        draw.rectangle([x0 + 10, y1 - 14, x1 - 10, y1 - 8], outline=accent, width=2)
    elif kind == "down":
        pts = [(x0 + 8, y0 + 12), (x0 + 20, y0 + 20), (x0 + 30, y0 + 16),
               (x1 - 10, y1 - 10)]
        draw.line(pts, fill=RED, width=3)
        draw.polygon([(x1 - 12, y1 - 12), (x1 - 6, y1 - 12), (x1 - 9, y1 - 4)],
                     fill=RED)
        draw.line([(x0 + 8, y1 - 8), (x1 - 8, y1 - 8)], fill=INK, width=2)
    elif kind == "cricket":
        draw.line([(cx - 12, y1 - 10), (cx + 8, y0 + 10)], fill=accent, width=5)
        draw.ellipse([cx + 8, y1 - 16, cx + 20, y1 - 4], fill=RED)
        draw.line([(x0 + 8, y1 - 8), (x1 - 8, y1 - 8)], fill=INK, width=2)
    elif kind == "trophy":
        draw.polygon([(cx - 10, y0 + 8), (cx + 10, y0 + 8), (cx + 7, y0 + 24),
                      (cx - 7, y0 + 24)], fill=GOLD)
        draw.arc([cx - 16, y0 + 8, cx - 4, y0 + 20], 90, 270, fill=GOLD, width=3)
        draw.arc([cx + 4, y0 + 8, cx + 16, y0 + 20], 270, 90, fill=GOLD, width=3)
        draw.line([(cx, y0 + 24), (cx, y0 + 32)], fill=GOLD, width=3)
        draw.line([(cx - 8, y0 + 32), (cx + 8, y0 + 32)], fill=GOLD, width=3)
    elif kind == "sun":
        import math
        draw.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=GOLD)
        for a in range(0, 360, 45):
            r1, r2 = 14, 19
            x1a = cx + r1 * math.cos(math.radians(a))
            y1a = cy + r1 * math.sin(math.radians(a))
            x2a = cx + r2 * math.cos(math.radians(a))
            y2a = cy + r2 * math.sin(math.radians(a))
            draw.line([(x1a, y1a), (x2a, y2a)], fill=GOLD, width=2)
        draw.line([(x0 + 8, y1 - 8), (x1 - 8, y1 - 8)], fill=TEAL, width=2)
    elif kind == "court":
        for i in range(3):
            px = x0 + 12 + i * 12
            draw.line([(px, y0 + 16), (px, y1 - 10)], fill=accent, width=3)
        draw.polygon([(x0 + 6, y0 + 16), (cx, y0 + 6), (x1 - 6, y0 + 16)],
                     fill=accent)
        draw.line([(x0 + 8, y1 - 10), (x1 - 8, y1 - 10)], fill=accent, width=3)
    elif kind == "pin":
        draw.ellipse([cx - 12, y0 + 6, cx + 12, y0 + 30], outline=accent, width=3)
        draw.ellipse([cx - 4, y0 + 12, cx + 4, y0 + 20], fill=accent)
        draw.polygon([(cx - 9, y0 + 26), (cx + 9, y0 + 26), (cx, y1 - 6)],
                     fill=accent)

# ---------------------------------------------------------------- layout
M = 28            # outer margin
CW = W - 2 * M    # content width = 968

def draw_masthead(d):
    d.text((M, 14), "ONE DAY — ONE PAGE — THE WHOLE WORLD",
           font=F_SANS_B(13), fill=RED)
    total = len(PANELS) + len(BRIEFS)
    d.text((W - M, 14), f"{total} STORIES — ALL FROM FRIDAY 20 NOVEMBER",
           font=F_SANS_B(13), fill=INK, anchor="ra")
    hline(d, M, W - M, 36, width=3)
    d.text((W // 2, 42), "Friday 20 November 2026", font=F_SERIF_B(56),
           fill=INK, anchor="ma")
    sub = ("Shenzhen summit · The World Court rules on the Rohingya · "
           "Anthropic's record debut · COP31's last day")
    d.text((W // 2, 106), sub, font=F_SERIF(16), fill=GREY, anchor="ma")
    hline(d, M, W - M, 128, fill=(199, 189, 169), width=1)
    return 134

def draw_stats(d, y):
    n = len(STATS)
    cw = CW / n
    for i, (num, lab) in enumerate(STATS):
        cx = M + cw * (i + 0.5)
        d.text((cx, y + 4), num, font=F_SERIF_B(22), fill=INK, anchor="ma")
        d.text((cx, y + 30), lab, font=F_SANS(10), fill=GREY, anchor="ma")
    hline(d, M, W - M, y + 52, fill=(199, 189, 169), width=1)
    return y + 56

def draw_lead(d, y):
    kicker, head, deck, kind, accent = PANELS[0]
    h = 112
    d.rectangle([M, y, W - M, y + h], fill=PANEL, outline=RULE, width=2)
    d.rectangle([M, y, M + 8, y + h], fill=RED)
    icon(d, kind, (M + 20, y + 14, M + 20 + 84, y + 14 + 84), accent)
    tx = M + 122
    d.text((tx, y + 10), kicker + "  —  LEAD", font=F_SANS_B(12), fill=RED)
    d.text((tx, y + 28), head, font=F_SERIF_B(30), fill=INK)
    lines = wrap(d, deck, F_SANS(14), W - M - tx - 16)
    text_block(d, (tx, y + 68), lines[:2], F_SANS(14), leading=18)
    return y + h + 8

def draw_panel(d, x0, y0, w, h, story):
    kicker, head, deck, kind, accent = story
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=PANEL, outline=RULE, width=1)
    d.rectangle([x0, y0, x0 + w, y0 + 3], fill=accent)
    icon(d, kind, (x0 + 8, y0 + 20, x0 + 8 + 44, y0 + 20 + 44), accent)
    tx = x0 + 60
    tw = w - 68
    d.text((tx, y0 + 6), kicker, font=F_SANS_B(10), fill=accent)
    lines = wrap(d, head, F_SERIF_B(14), tw)
    yy = text_block(d, (tx, y0 + 19), lines[:2], F_SERIF_B(14), leading=16)
    dlines = wrap(d, deck, F_SANS(11), tw)
    text_block(d, (tx, yy + 2), dlines[:2], F_SANS(11), leading=13)

def draw_grid(d, y):
    cols, rows = 4, 3
    gap = 8
    pw = (CW - gap * (cols - 1)) // cols
    ph = 96
    idx = 1
    for r in range(rows):
        for c in range(cols):
            x0 = M + c * (pw + gap)
            y0 = y + r * (ph + gap)
            draw_panel(d, x0, y0, pw, ph, PANELS[idx])
            idx += 1
    return y + rows * ph + (rows - 1) * gap + 8

def draw_briefs(d, y):
    d.text((M, y), "ALSO ON — THE REST OF THE DAY", font=F_SANS_B(14), fill=INK)
    d.text((W - M, y), f"{len(BRIEFS)} MORE STORIES", font=F_SANS_B(12),
           fill=RED, anchor="ra")
    hline(d, M, W - M, y + 20, width=2)
    y += 26
    colw = (CW - 24) // 2
    per = (len(BRIEFS) + 1) // 2
    for col in range(2):
        cx = M + col * (colw + 24)
        for i in range(per):
            j = col * per + i
            if j >= len(BRIEFS):
                break
            tag, txt = BRIEFS[j]
            yy = y + i * 12
            d.text((cx, yy), tag, font=F_SANS_B(10), fill=RED)
            tw = d.textlength(tag, font=F_SANS_B(10))
            # one line only: truncate with an ellipsis if it would overflow
            maxw = colw - tw - 8
            fnt = F_SANS(10)
            while txt and d.textlength(txt, font=fnt) > maxw:
                txt = txt[:-2]
            if txt != BRIEFS[j][1]:
                txt = txt.rstrip(" ,.;") + "…"
            d.text((cx + tw + 6, yy), txt, font=fnt, fill=INK)
    return y + per * 12 + 8

def draw_map(d, y, box_w):
    x0, x1 = M, M + box_w
    h = 112
    d.rectangle([x0, y, x1, y + h], fill=(223, 232, 238), outline=RULE, width=1)
    d.text((x0 + 8, y + 5), "WHERE IT HAPPENED", font=F_SANS_B(11), fill=INK)
    mx0, my0 = x0 + 8, y + 22
    mw, mh = box_w - 16, h - 44
    for gx in range(mx0, x1 - 8, 7):
        for gy in range(my0, y + h - 26, 7):
            d.point((gx, gy), fill=(190, 205, 214))
    def proj(lon, lat):
        px = mx0 + (lon + 180) / 360 * mw
        py = my0 + (90 - lat) / 180 * mh
        return px, py
    for pts in CONTINENTS.values():
        poly = [proj(lon, lat) for lon, lat in pts]
        d.polygon(poly, fill=(196, 178, 138), outline=(120, 105, 70))
    for i, (name, lon, lat) in enumerate(PINS, 1):
        px, py = proj(lon, lat)
        d.ellipse([px - 5, py - 5, px + 5, py + 5], fill=RED,
                  outline=(255, 255, 255), width=1)
        d.text((px + 1, py - 4), str(i), font=F_SANS_B(7),
               fill=(255, 255, 255), anchor="mm")
    names = " · ".join(f"{i + 1} {n}" for i, (n, _, _) in enumerate(PINS))
    lines = wrap(d, names, F_SANS(9), box_w - 16)
    text_block(d, (x0 + 8, y + h - 14), lines[:1], F_SANS(9), leading=11)
    return y + h

def draw_datecheck(d, y, x0, w):
    h = 112
    d.rectangle([x0, y, x0 + w, y + h], fill=INK, outline=RULE, width=1)
    d.text((x0 + 12, y + 8), "DATE CHECK", font=F_SANS_B(13), fill=(232, 196, 90))
    body = ("FRIDAY 20 NOVEMBER 2026 — World Children's Day. This page sums up "
            "the news of 20 November 2026. Events first reported late on 19 Nov "
            "(UTC) are 20 Nov in Asia-Pacific time. COP31 has no final deal yet "
            "and Akvan has not made landfall — both are pending, not done.")
    lines = wrap(d, body, F_SANS(11), w - 24)
    text_block(d, (x0 + 12, y + 30), lines, F_SANS(11),
               fill=(246, 241, 227), leading=14)
    return y + h

def draw_timeline(d, y):
    d.text((M, y), "THE DAY IN UTC", font=F_SANS_B(11), fill=INK)
    n = len(TIMELINE)
    step = CW / n
    axis_y = y + 24
    d.line([(M, axis_y), (W - M, axis_y)], fill=RULE, width=2)
    for i, (t, ev) in enumerate(TIMELINE):
        cx = M + step * (i + 0.5)
        d.ellipse([cx - 4, axis_y - 4, cx + 4, axis_y + 4], fill=RED)
        d.text((cx, y + 12), t, font=F_SANS_B(8), fill=INK, anchor="ma")
        lines = wrap(d, ev, F_SANS(9), int(step) - 8)
        text_block(d, (cx, axis_y + 8), lines[:1], F_SANS(9), leading=11)
    return y + 46

def draw_footer(d, y):
    hline(d, M, W - M, y, width=2)
    d.text((M, y + 6),
           "Sources: Reuters · AP · AFP · UN News · Nasdaq · IMD · IIMM · OHCHR · Compiled 07:30 WIB, 20 Nov 2026.",
           font=F_SANS(10), fill=GREY)
    d.text((W - M, y + 6), "THE WORLD TODAY · No. 20", font=F_SANS_B(10),
           fill=INK, anchor="ra")

# ---------------------------------------------------------------- main
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = draw_masthead(d)
    y = draw_stats(d, y)
    y = draw_lead(d, y)
    y = draw_grid(d, y)
    y = draw_briefs(d, y)
    map_w = 640
    y_map = draw_map(d, y, map_w)
    y_dc = draw_datecheck(d, y, M + map_w + 16, CW - map_w - 16)
    y = max(y_map, y_dc) + 6
    y = draw_timeline(d, y)
    draw_footer(d, y + 4)
    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)

if __name__ == "__main__":
    main()
