#!/usr/bin/env python3
"""Draw entry.png for news-image-20261127: one broadsheet page, 1024x1024.

Flat-vector newspaper, drawn from scratch with PIL. No network, no clock,
no randomness: the same run always writes the same bytes.
"""
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

PAPER = (247, 242, 231)
INK = (28, 28, 34)
NAVY = (22, 35, 63)
NAVY2 = (30, 58, 95)
RED = (176, 35, 24)
GOLD = (201, 162, 39)
GRAY = (107, 114, 128)
CARD = (255, 253, 246)
LINE = (180, 172, 150)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)   # noqa: E731
F_SERIF = lambda s: font("DejaVuSerif.ttf", s)          # noqa: E731
F_SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)     # noqa: E731
F_SANS = lambda s: font("DejaVuSans.ttf", s)            # noqa: E731


def text_w(draw, text, fnt):
    return draw.textlength(text, font=fnt)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if text_w(draw, trial, fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, max_w, fill, leading=None):
    lines = wrap(draw, text, fnt, max_w)
    step = leading if leading is not None else int(fnt.size * 1.18)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += step
    return y


def pill(draw, x, y, w, h, text, fnt, bg, fg):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=h // 2, fill=bg)
    tw = text_w(draw, text, fnt)
    draw.text((x + (w - tw) / 2, y + (h - fnt.size) / 2 - 1), text,
              font=fnt, fill=fg)


def tag_pill(draw, x, y, label):
    """Certainty tag; returns its width."""
    colors = {"REPORTED": ((201, 162, 39), (20, 20, 20)),
              "OFFICIAL": ((22, 35, 63), (255, 255, 255)),
              "CLAIM": ((176, 35, 24), (255, 255, 255)),
              "FORECAST": ((107, 33, 168), (255, 255, 255))}
    bg, fg = colors[label]
    fnt = F_SANS_B(9)
    w = int(text_w(draw, label, fnt)) + 12
    draw.rounded_rectangle([x, y, x + w, y + 14], radius=7, fill=bg)
    draw.text((x + 6, y + 2), label, font=fnt, fill=fg)
    return w


# ---------------------------------------------------------------- data
HEROES = [
    {"n": 1, "place": "KUWAIT CITY", "kicker": "DRONE STRIKE",
     "scene": "kuwait",
     "head": "Kuwait blames Iran as drone kills two Italians",
     "deck": "Two technicians die at an air-defence site; Tehran denies it.",
     "src": "Reuters · BBC", "tag": "REPORTED"},
    {"n": 2, "place": "NEW YORK", "kicker": "STORM",
     "scene": "storm",
     "head": "Thanksgiving storm cuts power to 800,000",
     "deck": "Winds to 70 mph flood the East Coast; 1,700 flights delayed.",
     "src": "Reuters · poweroutage.us", "tag": "REPORTED"},
    {"n": 3, "place": "GAZA CITY", "kicker": "STRIKES",
     "scene": "gaza",
     "head": "Israeli strikes kill 10 in Gaza",
     "deck": "Hamas weighs its reply after a third night of raids.",
     "src": "Reuters", "tag": "REPORTED"},
]

CARDS = [
    {"n": 4, "place": "USA", "kicker": "ECONOMY", "scene": "sale",
     "head": "Black Friday opens: $12.9bn day ahead",
     "deck": "Adobe sees a record $12.9bn online.",
     "src": "Adobe", "tag": "FORECAST"},
    {"n": 5, "place": "PYONGYANG", "kicker": "DEFENCE", "scene": "missile",
     "head": "Kim vows a bigger nuclear arsenal",
     "deck": "Kim calls for more warheads on a tour of nuclear plants.",
     "src": "KCNA · Reuters", "tag": "REPORTED"},
    {"n": 6, "place": "BRUSSELS", "kicker": "POLITICS", "scene": "eu",
     "head": "EU leaders split over €45bn Ukraine loan",
     "deck": "Summit ends with no deal on the budget or the Kyiv loan.",
     "src": "Reuters", "tag": "REPORTED"},
    {"n": 7, "place": "WELLINGTON", "kicker": "POLITICS", "scene": "ballot",
     "head": "NZ final count lands today",
     "deck": "400,000 special votes decide a coalition one seat short.",
     "src": "Electoral Commission", "tag": "OFFICIAL"},
    {"n": 8, "place": "LONDON", "kicker": "MIGRATION", "scene": "chart",
     "head": "UK net migration at lowest since 1997",
     "deck": "Net arrivals fall to 77,000, down from 204,000.",
     "src": "ONS", "tag": "OFFICIAL"},
    {"n": 9, "place": "PARIS", "kicker": "TRIAL", "scene": "court",
     "head": "Depardieu to stand trial over 2018 rape",
     "deck": "A Paris court orders the actor to face trial.",
     "src": "AP", "tag": "REPORTED"},
    {"n": 10, "place": "IBIZA", "kicker": "DISASTER", "scene": "tanker",
     "head": "Tanker capsizes off Ibiza",
     "deck": "7,000 tonnes of diesel at risk; one crew member dies.",
     "src": "BBC", "tag": "REPORTED"},
    {"n": 11, "place": "LONDON", "kicker": "STRIKE", "scene": "tube",
     "head": "Tube drivers begin eight days of strikes",
     "deck": "Drivers walk out for the first of eight winter strike days.",
     "src": "Reuters", "tag": "REPORTED"},
    {"n": 12, "place": "GENEVA", "kicker": "CHESS", "scene": "chess",
     "head": "Gukesh, Sindarov draw Game 3, 1.5–1.5",
     "deck": "A 60-move marathon leaves the match level at the rest day.",
     "src": "Chess.com", "tag": "REPORTED"},
    {"n": 13, "place": "HONG KONG", "kicker": "ANNIVERSARY", "scene": "tower",
     "head": "Hong Kong marks tower-fire anniversary",
     "deck": "Flowers and prayers for 168 dead.",
     "src": "AP", "tag": "REPORTED"},
    {"n": 14, "place": "GIZA", "kicker": "DISASTER", "scene": "fire",
     "head": "31 dead, 20 hurt in Giza tanker fire",
     "deck": "A tanker overturns and explodes; the driver is arrested.",
     "src": "AP", "tag": "REPORTED"},
    {"n": 15, "place": "BANGKOK", "kicker": "DISASTER", "scene": "blast",
     "head": "Nine hurt in Bangkok refinery blast",
     "deck": "Three critical after an explosion at an oil facility.",
     "src": "AP", "tag": "REPORTED"},
]

ALSO = [
    (16, "Kyiv", "Zelenskyy warns of grid attack"),
    (17, "Berlin", "Germany arrests two Iraqis over synagogue plot"),
    (18, "Karachi", "Building collapse kills 3"),
    (19, "Belgrade", "Serbia calls early vote for 27 December"),
    (20, "Washington", "US clears $622m F-16 kit sale to Ukraine"),
    (21, "Riyadh", "Saudi Arabia intercepts two Houthi missiles"),
    (22, "Brasilia", "Brazil names bank chief finance minister"),
    (23, "Kinshasa", "DR Congo Ebola cases pass 12,000"),
    (24, "Kyiv", "Russian ballistic missiles hit Kyiv"),
    (25, "Wellington", "NZ coalition one seat short of majority"),
    (26, "Worldwide", "Amazon workers strike in 20 countries"),
    (27, "Moscow", "Kushner and Witkoff put peace plan to Putin"),
    (28, "Seoul", "KOSPI opens higher as chip stocks steady"),
    (29, "Beijing", "Beijing threatens countermeasures on tariffs"),
    (30, "Washington", "Trump calls pre-election GDP figure 'fake'"),
    (31, "Nairobi", "Twice-yearly HIV injection reaches Africa cheaper"),
    (32, "Canberra", "Australia orders gas exporters to keep a fifth"),
    (33, "Jazan", "Fire at Saudi refinery kills a Nepali worker"),
    (34, "Washington", "Vance: Huang needs no pardon"),
    (35, "Khartoum", "Sudanese return to a ruined capital"),
    (36, "Hanoi", "Vietnam races for a US trade deal"),
    (37, "Paris", "Le Pen attacks EU budget deal"),
    (38, "Christchurch", "India chase first series win in Test"),
]

STATS = [
    ("800,000", "left without power by the storm"),
    ("2", "Italians killed in Kuwait"),
    ("7,000 t", "tonnes of diesel off Ibiza"),
    ("€45bn", "Ukraine loan splitting EU leaders"),
    ("77,000", "UK net migration at 28-year low"),
    ("$12.9bn", "Black Friday online forecast"),
]

UTC_SLOTS = [
    ("00:17", "Gaza strike kills 3"),
    ("00:25", "Serbia calls Dec vote"),
    ("00:34", "Kushner: swap 'shortly'"),
    ("01:00", "NZ count lands"),
    ("11:00", "Kuwait strike kills 2"),
    ("13:35", "Zelenskyy warns attack"),
]

REGIONS = [
    ("EUROPE 11", (30, 58, 95)),
    ("MIDDLE EAST 4", (176, 35, 24)),
    ("ASIA 7", (15, 118, 110)),
    ("AMERICAS 6", (22, 101, 52)),
    ("AFRICA 4", (194, 65, 12)),
    ("OCEANIA 4", (107, 33, 168)),
    ("WORLD 2", (75, 85, 99)),
]

# Map pins: story number -> (grid col, grid row) on a 60x22 world grid.
PINS = {1: (40, 7), 2: (10, 4), 3: (38, 8), 4: (13, 6), 5: (52, 5),
        6: (31, 2), 7: (55, 16), 8: (27, 2), 9: (29, 5), 10: (27, 5),
        11: (26, 4), 12: (31, 4), 13: (49, 7), 14: (36, 8), 15: (47, 8)}

MAP_ROWS = [
    "                                                          ",
    "    #########                                           ",
    "   ###########      ####   ##########################     ",
    "  ############     ###### ############################    ",
    "   ##########       ####  ###########################     ",
    "    ########         ##   ##########################      ",
    "     ######               ##################  #####       ",
    "      ####          #    #################     ###        ",
    "       ##         ####   ##############        ##         ",
    "       ###       ######   ############                    ",
    "        ##        ####    ##########                     ",
    "        ###        ##      ########                      ",
    "         ##        #       ######                         ",
    "         ###               #####              #          ",
    "          ##                ###              ###         ",
    "          #                 ##              #####        ",
    "                             #               ###          ",
    "                                              #          ",
    "                                                          ",
    "                                                          ",
    "                                                          ",
    "                                                          ",
]


# ---------------------------------------------------------------- scenes
def scene_kuwait(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 138, 62))
    d.rectangle([x, y + h * 0.55, x + w, y + h], fill=(146, 84, 32))
    d.ellipse([x + w - 52, y + 8, x + w - 12, y + 48], fill=(250, 214, 130))
    d.rectangle([x, y + h - 26, x + w, y + h - 18], fill=(90, 52, 20))
    # radar dish: half-disc + mast + feed arm
    cx, cy = x + 62, y + h - 26
    d.pieslice([cx - 34, cy - 62, cx + 34, cy + 6], 180, 360,
               fill=(60, 42, 28))
    d.line([cx, cy, cx, cy + 26], fill=(60, 42, 28), width=4)
    d.line([cx, cy, cx + 44, cy - 6], fill=(60, 42, 28), width=4)
    # drones
    for dx, dy in ((x + w - 150, y + 26), (x + w - 110, y + 44)):
        d.ellipse([dx, dy, dx + 26, dy + 8], fill=(40, 28, 20))
        d.line([dx - 6, dy + 4, dx + 32, dy + 4], fill=(40, 28, 20), width=3)
    d.ellipse([x + 120, y + h - 14, x + 128, y + h - 6], fill=(250, 214, 130))


def scene_storm(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 38, 66))
    for cx, cy, cw in ((x + 20, y + 12, 120), (x + 130, y + 4, 150),
                       (x + 230, y + 18, 110)):
        d.ellipse([cx, cy, cx + cw, cy + 30], fill=(52, 66, 96))
        d.ellipse([cx + 20, cy - 8, cx + cw - 10, cy + 18], fill=(66, 82, 116))
    # lightning
    d.polygon([(x + 165, y + 30), (x + 185, y + 30), (x + 172, y + 62),
               (x + 188, y + 62), (x + 158, y + 104), (x + 170, y + 66),
               (x + 156, y + 66)], fill=(250, 204, 21))
    # rain
    for rx in range(x + 8, x + w - 4, 22):
        d.line([rx, y + h - 34, rx - 8, y + h - 12], fill=(140, 160, 200),
               width=2)
    # power pole, sagging line
    d.line([x + 26, y + h - 52, x + 26, y + h], fill=(16, 24, 44), width=5)
    d.line([x + 8, y + h - 48, x + 44, y + h - 48], fill=(16, 24, 44), width=4)
    d.arc([x + 44, y + h - 52, x + w - 10, y + h - 8], 200, 340,
          fill=(16, 24, 44), width=3)


def scene_gaza(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 196, 130))
    d.ellipse([x + w - 70, y + 10, x + w - 26, y + 54], fill=(250, 228, 170))
    # skyline
    base = y + h
    for bx, bw, bh in ((x + 6, 44, 52), (x + 56, 36, 72), (x + 98, 52, 46),
                       (x + 156, 40, 66), (x + 202, 46, 54), (x + 254, 38, 78),
                       (x + 298, 30, 58)):
        d.rectangle([bx, base - bh, bx + bw, base], fill=(74, 66, 58))
    # smoke columns
    for sx, sy in ((x + 74, y + 18), (x + 220, y + 10), (x + 300, y + 22)):
        d.ellipse([sx, sy, sx + 26, sy + 30], fill=(120, 112, 100))
        d.ellipse([sx + 6, sy - 14, sx + 28, sy + 12], fill=(140, 132, 120))
    d.rectangle([x, y + h - 8, x + w, y + h], fill=(60, 54, 48))


def scene_mini(d, key, x, y, w, h):
    """30px-tall flat icon strip for a card."""
    if key == "sale":
        d.rectangle([x, y, x + w, y + h], fill=(176, 35, 24))
        for i in range(5):
            d.polygon([(x + i * 50, y), (x + i * 50 + 25, y),
                       (x + i * 50 + 25, y + 12), (x + i * 50, y + 12)],
                      fill=(250, 250, 250) if i % 2 == 0 else (22, 35, 63))
        d.rectangle([x + 18, y + 16, x + 48, y + h - 2], fill=(250, 204, 21))
        d.rectangle([x + 58, y + 16, x + 88, y + h - 2], fill=(255, 255, 255))
        d.text((x + 100, y + 14), "SALE -50%", font=F_SANS_B(13),
               fill=(255, 255, 255))
    elif key == "missile":
        d.rectangle([x, y, x + w, y + h], fill=(24, 38, 66))
        d.ellipse([x + w - 34, y + 4, x + w - 14, y + 24], fill=(250, 214, 130))
        d.polygon([(x + 100, y + 2), (x + 108, y + 2), (x + 112, y + 22),
                   (x + 96, y + 22)], fill=(220, 220, 220))
        d.polygon([(x + 96, y + 2), (x + 104, y + 2), (x + 104, y + 10),
                   (x + 96, y + 10)], fill=(176, 35, 24))
        d.line([x + 96, y + 22, x + 148, y + 22], fill=(120, 130, 150), width=3)
        for sx in (x + 20, x + 44, x + 70, x + 170, x + 200):
            d.ellipse([sx, y + 6, sx + 3, y + 9], fill=(255, 255, 255))
    elif key == "eu":
        d.rectangle([x, y, x + w, y + h], fill=(30, 58, 95))
        cx, cy = x + w // 2, y + h // 2
        for k in range(12):
            import math
            a = math.pi * 2 * k / 12
            d.ellipse([cx + 52 * math.cos(a) - 3, cy + 10 * math.sin(a) - 3,
                       cx + 52 * math.cos(a) + 3, cy + 10 * math.sin(a) + 3],
                      fill=(250, 204, 21))
        d.rectangle([x + 14, y + 8, x + 44, y + h - 8], fill=(201, 162, 39))
        d.text((x + 18, y + 10), "€", font=F_SANS_B(12), fill=(22, 35, 63))
    elif key == "ballot":
        d.rectangle([x, y, x + w, y + h], fill=(15, 118, 110))
        d.rectangle([x + 90, y + 6, x + 150, y + h - 6], fill=(255, 255, 255))
        d.rectangle([x + 100, y + 2, x + 140, y + 8], fill=(22, 35, 63))
        d.line([x + 100, y + 12, x + 112, y + 22], fill=(22, 101, 52), width=4)
        d.line([x + 112, y + 22, x + 140, y + 6], fill=(22, 101, 52), width=4)
        d.text((x + 12, y + 8), "VOTE", font=F_SANS_B(12), fill=(255, 255, 255))
    elif key == "chart":
        d.rectangle([x, y, x + w, y + h], fill=(247, 242, 231))
        d.line([x + 8, y + h - 6, x + w - 8, y + h - 6], fill=INK, width=2)
        bars = [(20, 22), (48, 16), (76, 11)]
        for bx, bh in bars:
            d.rectangle([x + bx, y + h - 6 - bh, x + bx + 18, y + h - 6],
                        fill=(176, 35, 24))
        d.text((x + 108, y + 4), "77,000", font=F_SANS_B(13), fill=RED)
        d.text((x + 108, y + 16), "lowest since 1997", font=F_SANS(9),
               fill=INK)
    elif key == "court":
        d.rectangle([x, y, x + w, y + h], fill=(232, 220, 190))
        d.polygon([(x + 60, y + 2), (x + 180, y + 2), (x + 120, y + 12)],
                  fill=(120, 90, 50))
        for cx in (70, 100, 130, 160):
            d.rectangle([x + cx, y + 12, x + cx + 8, y + h - 4],
                        fill=(120, 90, 50))
        d.rectangle([x + 56, y + h - 4, x + 184, y + h], fill=(120, 90, 50))
        d.ellipse([x + w - 34, y + 6, x + w - 14, y + 26], fill=(250, 204, 21))
    elif key == "tanker":
        d.rectangle([x, y, x + w, y + h], fill=(30, 58, 95))
        d.polygon([(x + 60, y + 10), (x + 190, y + 10), (x + 180, y + 24),
                   (x + 70, y + 24)], fill=(176, 35, 24))
        d.rectangle([x + 60, y + 4, x + 90, y + 10], fill=(220, 220, 220))
        for wx in range(x + 6, x + w - 6, 26):
            d.arc([wx, y + h - 12, wx + 24, y + h + 2], 180, 360,
                  fill=(140, 180, 220), width=2)
    elif key == "tube":
        d.rectangle([x, y, x + w, y + h], fill=(176, 35, 24))
        d.rounded_rectangle([x + 70, y + 4, x + 180, y + h - 4], radius=8,
                            fill=(255, 255, 255))
        d.rectangle([x + 84, y + 8, x + 166, y + 16], fill=(22, 35, 63))
        d.ellipse([x + 118, y + 18, x + 132, y + h - 8], fill=(176, 35, 24))
        d.text((x + 12, y + 8), "8 DAYS", font=F_SANS_B(12),
               fill=(255, 255, 255))
    elif key == "chess":
        d.rectangle([x, y, x + w, y + h], fill=(247, 242, 231))
        for r in range(2):
            for c in range(8):
                if (r + c) % 2 == 0:
                    d.rectangle([x + 70 + c * 13, y + 2 + r * 13,
                                 x + 70 + c * 13 + 13, y + 2 + r * 13 + 13],
                                fill=(28, 28, 34))
        d.ellipse([x + 190, y + 6, x + 210, y + 26], fill=(176, 35, 24))
        d.text((x + 8, y + 8), "1.5–1.5", font=F_SANS_B(12), fill=INK)
    elif key == "tower":
        d.rectangle([x, y, x + w, y + h], fill=(24, 38, 66))
        for bx, bh in ((60, 22), (100, 26), (140, 20)):
            d.rectangle([x + bx, y + h - bh, x + bx + 30, y + h],
                        fill=(60, 66, 80))
            for wy in range(y + h - bh + 4, y + h - 2, 6):
                d.rectangle([x + bx + 5, wy, x + bx + 11, wy + 3],
                            fill=(250, 204, 21))
        d.ellipse([x + 200, y + 8, x + 208, y + 20], fill=(250, 180, 60))
        d.polygon([(x + 200, y + 8), (x + 204, y + 2), (x + 208, y + 8)],
                  fill=(250, 120, 40))
    elif key == "fire":
        d.rectangle([x, y, x + w, y + h], fill=(40, 40, 48))
        d.polygon([(x + 110, y + 26), (x + 122, y + 6), (x + 134, y + 26)],
                  fill=(250, 120, 40))
        d.polygon([(x + 118, y + 26), (x + 124, y + 14), (x + 130, y + 26)],
                  fill=(250, 204, 21))
        d.rectangle([x + 60, y + 18, x + 190, y + 26], fill=(120, 120, 130))
        d.ellipse([x + 66, y + 22, x + 74, y + 30], fill=(28, 28, 34))
        d.ellipse([x + 176, y + 22, x + 184, y + 30], fill=(28, 28, 34))
        d.text((x + 10, y + 8), "31 DEAD", font=F_SANS_B(12),
               fill=(255, 255, 255))
    elif key == "blast":
        d.rectangle([x, y, x + w, y + h], fill=(232, 196, 130))
        for tx in (70, 110, 150):
            d.rectangle([x + tx, y + 8, x + tx + 12, y + h - 4],
                        fill=(90, 80, 70))
            d.rectangle([x + tx - 3, y + 4, x + tx + 15, y + 8],
                        fill=(60, 54, 48))
        d.polygon([(x + 200, y + 15), (x + 206, y + 6), (x + 212, y + 15),
                   (x + 222, y + 15), (x + 214, y + 21), (x + 217, y + 29),
                   (x + 206, y + 24), (x + 195, y + 29), (x + 198, y + 21),
                   (x + 190, y + 15)], fill=(250, 120, 40))
        d.text((x + 8, y + 8), "BLAST", font=F_SANS_B(11), fill=(176, 35, 24))


HERO_SCENES = {"kuwait": scene_kuwait, "storm": scene_storm,
               "gaza": scene_gaza}


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 228, 238))
    d.rectangle([x, y, x + w, y + h], outline=LINE, width=1)
    rows = len(MAP_ROWS)
    cols = len(MAP_ROWS[0])
    cw, ch = w / cols, h / rows
    for r, row in enumerate(MAP_ROWS):
        for c, ch_ in enumerate(row):
            if ch_ == "#":
                px, py = x + c * cw + cw / 2, y + r * ch + ch / 2
                d.ellipse([px - 1.6, py - 1.6, px + 1.6, py + 1.6],
                          fill=(196, 178, 140))
    d.text((x + 6, y + h - 14), "ATLANTIC", font=F_SANS(8), fill=(90, 110, 130))
    d.text((x + 6, y + 4), "PACIFIC", font=F_SANS(8), fill=(90, 110, 130))
    for n, (gc, gr) in PINS.items():
        px = x + (gc + 0.5) * cw
        py = y + (gr + 0.5) * ch
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED,
                  outline=(255, 255, 255), width=1)
        fnt = F_SANS_B(8)
        t = str(n)
        d.text((px - text_w(d, t, fnt) / 2, py - 5), t, font=fnt,
               fill=(255, 255, 255))


# ---------------------------------------------------------------- layout
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W - 1, H - 1], outline=NAVY, width=3)

    # top band
    d.rectangle([0, 0, W, 30], fill=NAVY)
    d.text((10, 7), "THE WORLD IN ONE DAY", font=F_SANS_B(15), fill=GOLD)
    right = "38 STORIES · 7 REGIONS"
    d.text((W - 10 - text_w(d, right, F_SANS_B(13)), 8), right,
           font=F_SANS_B(13), fill=GOLD)

    # masthead
    title = "Friday 27 November 2026"
    tf = F_SERIF_B(62)
    d.text(((W - text_w(d, title, tf)) / 2, 36), title, font=tf, fill=NAVY)
    deck = ("Kuwait drone strike kills two Italians · Thanksgiving storm "
            "cuts power to 800,000 · Ten killed in Gaza")
    df = F_SERIF(18)
    d.text(((W - text_w(d, deck, df)) / 2, 104), deck, font=df, fill=RED)
    d.line([10, 126, W - 10, 126], fill=INK, width=2)

    # region tabs
    x = 10
    tab_w = (W - 20 - 6 * 6) / 7
    for label, color in REGIONS:
        pill(d, x, 132, tab_w, 20, label, F_SANS_B(11), color, (255, 255, 255))
        x += tab_w + 6

    # UTC strip
    d.text((10, 158), "THE DAY IN UTC", font=F_SANS_B(11), fill=RED)
    d.line([10, 176, W - 10, 176], fill=LINE, width=1)
    slot_w = (W - 20 - 118) / 6
    sx = 128
    for t, txt in UTC_SLOTS:
        d.text((sx, 158), t, font=F_SANS_B(11), fill=RED)
        draw_wrapped(d, sx, 172, txt, F_SANS(10), slot_w - 6, INK, leading=12)
        sx += slot_w
    d.line([10, 198, W - 10, 198], fill=LINE, width=1)

    # stats row: six big red numbers
    col_w = (W - 20) / 6
    for i, (num, label) in enumerate(STATS):
        cx = 10 + i * col_w
        nf = F_SANS_B(28)
        d.text((cx + (col_w - text_w(d, num, nf)) / 2, 204), num, font=nf,
               fill=RED)
        draw_wrapped(d, cx + 6, 236, label, F_SANS(9), col_w - 12, INK,
                     leading=11)
        if i:
            d.line([cx, 206, cx, 246], fill=LINE, width=1)
    d.line([10, 252, W - 10, 252], fill=INK, width=2)

    # three heroes
    hw, gap = 330, 9
    for i, hero in enumerate(HEROES):
        hx = 10 + i * (hw + gap)
        hy = 258
        d.rectangle([hx, hy, hx + hw, hy + 252], fill=CARD,
                    outline=LINE, width=1)
        HERO_SCENES[hero["scene"]](d, hx + 1, hy + 1, hw - 2, 108)
        d.ellipse([hx + hw - 26, hy + 116, hx + hw - 6, hy + 136], fill=RED,
                  outline=(255, 255, 255), width=1)
        nf = F_SANS_B(11)
        t = str(hero["n"])
        d.text((hx + hw - 16 - text_w(d, t, nf) / 2, hy + 121), t, font=nf,
               fill=(255, 255, 255))
        kx = hx + 8
        d.text((kx, hy + 116), hero["place"], font=F_SANS_B(11), fill=INK)
        d.text((kx + text_w(d, hero["place"], F_SANS_B(11)) + 8, hy + 116),
               hero["kicker"], font=F_SANS_B(11), fill=RED)
        y = draw_wrapped(d, kx, hy + 134, hero["head"], F_SERIF_B(24),
                         hw - 16, INK, leading=27)
        draw_wrapped(d, kx, y + 2, hero["deck"], F_SANS(12), hw - 16,
                     (60, 60, 66), leading=15)
        d.text((kx, hy + 252 - 18), hero["src"], font=F_SANS(9), fill=GRAY)
        tag_pill(d, hx + hw - 72, hy + 252 - 18, hero["tag"])

    # twelve cards: 4 columns x 3 rows
    cw, chh, cgap = 246, 84, 8
    for i, card in enumerate(CARDS):
        cx = 10 + (i % 4) * (cw + cgap)
        cy = 520 + (i // 4) * (chh + cgap)
        d.rectangle([cx, cy, cx + cw, cy + chh], fill=CARD, outline=LINE,
                    width=1)
        scene_mini(d, card["scene"], cx + 1, cy + 1, cw - 2, 30)
        d.ellipse([cx + cw - 22, cy + 4, cx + cw - 6, cy + 20], fill=RED,
                  outline=(255, 255, 255), width=1)
        nf = F_SANS_B(10)
        t = str(card["n"])
        d.text((cx + cw - 14 - text_w(d, t, nf) / 2, cy + 8), t, font=nf,
               fill=(255, 255, 255))
        d.text((cx + 6, cy + 34), card["place"], font=F_SANS_B(9), fill=INK)
        d.text((cx + 6 + text_w(d, card["place"], F_SANS_B(9)) + 6, cy + 34),
               card["kicker"], font=F_SANS_B(9), fill=RED)
        tag_pill(d, cx + cw - 62, cy + 32, card["tag"])
        draw_wrapped(d, cx + 6, cy + 48, card["head"], F_SANS_B(12), cw - 12,
                     INK, leading=13)

    # ALSO + map
    d.text((10, 792), "WHERE IT HAPPENED", font=F_SANS_B(11), fill=NAVY)
    d.text((172, 793), "pins = story numbers", font=F_SANS(9), fill=GRAY)
    d.text((348, 792), "ALSO ON FRIDAY 27 NOVEMBER",
           font=F_SANS_B(11), fill=NAVY)
    d.line([10, 806, W - 10, 806], fill=INK, width=1)
    draw_map(d, 10, 812, 322, 106)
    af = F_SANS(9)
    col1 = ALSO[:12]
    col2 = ALSO[12:]
    for col, ox in ((col1, 348), (col2, 688)):
        yy = 810
        for n, place, head in col:
            line = "%d  %s — %s" % (n, place, head)
            d.text((ox, yy), line, font=af, fill=INK)
            yy += 9

    # date check
    d.rectangle([10, 922, W - 10, 994], outline=RED, width=2)
    d.text((20, 928), "DATE CHECK", font=F_SANS_B(12), fill=RED)
    d.text((118, 928),
           "Every story here happened, or was first reported, on 27 November "
           "2026 (in any time zone).",
           font=F_SANS(11), fill=INK)
    draw_wrapped(d, 20, 946,
                 "LEFT OUT (other days): Macy's parade postponed, 26 Nov · "
                 "Trump tariffs on 14 partners, 26 Nov · 26/11 Mumbai "
                 "anniversary tributes, 26 Nov · Murmansk governor detained, "
                 "25 Nov · Houthi claim on Ras Tanura refinery, 25 Nov · "
                 "Steelers release Rodgers, 25 Nov.",
                 F_SANS(11), W - 40, INK, leading=14)

    # footer
    d.text((10, 1002),
           "Sources: Reuters · BBC · AP · AFP · KCNA · ONS · Chess.com · "
           "Electoral Commission · Adobe. Scenes are drawn illustrations, "
           "not photographs.",
           font=F_SANS(9), fill=GRAY)
    img.save(OUT, "PNG", optimize=True)
    return OUT


if __name__ == "__main__":
    print(build())
