"""news-image-20261126: one image summing up Thursday 26 November 2026.

Layout: masthead, one dominant lead (Houthi strike on the Ras Tanura
refinery, Brent over $94), two illustrated stories (Hormuz mines, Gaza
strike), a Trade & Markets band, and a two-column Day in Brief.
Everything is drawn from scratch with the stdlib raster engine in
render.py; the program writes /output/entry.png (or $MAKEFUN_OUTPUT_DIR)
and nothing else. Deterministic: no network, no clock, no randomness.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from render import Page, write_png

W, H = 1024, 1024
PAPER = b"\xf6\xf1\xe3"
INK = b"\x19\x19\x19"
RED = b"\xb3\x20\x2c"
NAVY = b"\x17\x32\x4e"
GOLD = b"\xc8\x9b\x3c"
TEAL = b"\x1f\x6f\x6b"
GREY = b"\x6b\x66\x5c"
SKY = b"\x27\x4a\x6b"
SEA = b"\x2e\x6b\x8a"
ORANGE = b"\xe8\x6a\x1a"
FLAME = b"\xf5\xc5\x1e"
SMOKE = b"\x9a\x94\x88"
WHITE = b"\xff\xff\xff"


# ------------------------------------------------------------- scenes
def refinery_scene(pg, x, y, w, h):
    """Night refinery under attack: towers, flame, smoke, price arrow."""
    pg.box(x, y, w, h, SKY)
    pg.stipple(x, y, w, 40, b"\x3a\x5c\x7d", step=6)
    # ground + towers
    pg.box(x, y + h - 46, w, 46, b"\x12\x24\x38")
    for tx, tw, th in ((x + 18, 34, 150), (x + 66, 26, 118),
                       (x + 104, 40, 168), (x + 158, 30, 132)):
        pg.box(tx, y + h - 46 - th, tw, th, b"\x2c\x44\x5c")
        pg.box(tx + 4, y + h - 46 - th - 10, tw - 8, 10, b"\x2c\x44\x5c")
    # flare stack + flame
    pg.box(x + w - 78, y + 58, 14, h - 104, b"\x2c\x44\x5c")
    pg.tri(x + w - 92, y + 62, x + w - 56, y + 62, x + w - 71, y + 18, FLAME)
    pg.tri(x + w - 84, y + 62, x + w - 58, y + 62, x + w - 71, y + 34, ORANGE)
    # smoke puffs
    for sx, sy, r in ((x + 60, y + 46, 16), (x + 92, y + 30, 20),
                      (x + 130, y + 48, 14), (x + 200, y + 26, 18)):
        pg.disc(sx, sy, r, SMOKE)
        pg.disc(sx + 8, sy + 6, r - 6, b"\xb0\xaa\x9e")
    # oil barrel + rising price arrow
    pg.box(x + w - 130, y + h - 78, 34, 32, b"\x8a\x2e\x1e")
    pg.box(x + w - 130, y + h - 84, 34, 6, b"\x8a\x2e\x1e")
    ax0, ay0 = x + 24, y + h - 60
    ax1, ay1 = x + w - 168, y + h - 158
    pg.seg(ax0, ay0, ax1, ay1, FLAME)
    pg.tri(ax1 - 16, ay1 + 2, ax1 + 8, ay1 + 2, ax1, ay1 - 14, FLAME)
    pg.put_text(x + 16, y + h - 34, "BRENT $94+", WHITE, 2)


def hormuz_scene(pg, x, y, w, h):
    """Two tankers on a strait, a spiked mine, one blast. Scene is h
    tall; all coordinates stay inside (x, y, w, h)."""
    pg.box(x, y, w, h, SKY)
    sea_top = y + h - 44
    pg.box(x, sea_top, w, 44, SEA)
    for wy in range(sea_top + 6, y + h, 12):
        pg.hrule(x + 8, wy, w - 16, b"\x7f\xb8\xc9", 2)
    # blast over tanker 1 (top-left of the scene)
    bx, by = x + 96, y + 26
    for dx, dy in ((-26, 0), (26, 0), (0, -20), (0, 16),
                   (-18, -14), (18, -14), (-18, 12), (18, 12)):
        pg.seg(bx, by, bx + dx, by + dy, FLAME)
    pg.disc(bx, by, 10, ORANGE)
    pg.disc(bx, by, 5, FLAME)
    # tanker 1 (left, listing)
    pg.box(x + 18, sea_top - 26, 150, 26, b"\x7a\x1f\x1a")
    pg.box(x + 30, sea_top - 42, 44, 16, WHITE)
    pg.seg(x + 18, sea_top + 2, x + 168, sea_top + 2, b"\x3a\x3a\x3a")
    # tanker 2 (right)
    pg.box(x + w - 170, sea_top - 22, 150, 22, b"\x3c\x3c\x3c")
    pg.box(x + w - 140, sea_top - 36, 36, 14, b"\xd8\xd2\xc2")
    # mine between them, half-submerged
    mx, my = x + w // 2, sea_top + 8
    pg.disc(mx, my, 12, INK)
    for dx, dy in ((-16, 0), (16, 0), (0, -16), (0, 16),
                   (-11, -11), (11, -11), (-11, 11), (11, 11)):
        pg.seg(mx, my, mx + dx, my + dy, INK)


def gaza_scene(pg, x, y, w, h):
    """City skyline at dusk with a blast column and falling debris.
    Building heights fit inside the scene."""
    pg.box(x, y, w, h, b"\x4a\x2e\x3a")
    pg.disc(x + w - 52, y + 30, 16, FLAME)
    base = y + h - 6
    for bx, bw, bh in ((x + 10, 52, 52), (x + 70, 44, 74),
                       (x + 122, 60, 46), (x + 190, 48, 66),
                       (x + 246, 56, 50), (x + 310, 46, 80),
                       (x + 364, 58, 58), (x + 430, 44, 48)):
        pg.box(bx, base - bh, bw, bh, b"\x24\x1a\x22")
        for wy in range(base - bh + 10, base - 6, 20):
            for wx in range(bx + 8, bx + bw - 8, 16):
                pg.box(wx, wy, 5, 6, FLAME)
    # blast column over the middle building
    cx = x + 152
    pg.tri(cx - 26, base - 46, cx + 26, base - 46, cx, y + 12, ORANGE)
    pg.tri(cx - 14, base - 46, cx + 14, base - 46, cx, y + 34, FLAME)
    pg.disc(cx - 34, y + 76, 9, SMOKE)
    pg.disc(cx + 40, y + 56, 11, SMOKE)
    pg.disc(cx + 18, y + 96, 7, SMOKE)


def bars(pg, x, y, w, h, vals, rgb):
    """Tiny vertical bar chart, values 0..100, baseline at bottom."""
    n = len(vals)
    bw = w // n
    for i, v in enumerate(vals):
        bh = max(2, h * v // 100)
        pg.box(x + i * bw + 2, y + h - bh, bw - 4, bh, rgb)


# -------------------------------------------------------------- build
def build():
    pg = Page(W, H, PAPER)

    # ---- masthead
    pg.box(0, 0, W, 10, RED)
    pg.put_center(W // 2, 26, "THE WORLD IN ONE DAY", INK, 4)
    pg.put_center(W // 2, 66, "THURSDAY 26 NOVEMBER 2026", RED, 2)
    pg.put_center(W // 2, 92, "THANKSGIVING DAY - 44 STORIES - SIX CONTINENTS",
                  GREY, 1)
    pg.hrule(28, 116, W - 56, INK, 3)
    pg.hrule(28, 122, W - 56, INK, 1)

    # ---- lead: refinery scene left, story right
    ly = 134
    pg.frame(28, ly, 420, 300, INK, 2)
    refinery_scene(pg, 30, ly + 2, 416, 296)
    tx = 472
    pg.put_text(tx, ly + 6, "ENERGY - MIDDLE EAST", RED, 2)
    pg.hrule(tx, ly + 30, 524, RED, 2)
    pg.put_text(tx, ly + 44, "HOUTHIS HIT", INK, 3)
    pg.put_text(tx, ly + 74, "SAUDI REFINERY", INK, 3)
    pg.put_text(tx, ly + 104, "AS BRENT TOPS $94", INK, 3)
    body_end = pg.flow(tx, ly + 142, 524,
                       "Yemen's Houthis claim strikes on the Ras Tanura refinery "
                       "and Riyadh's financial district, jolting oil markets and "
                       "raising fears of wider disruption to Gulf energy supplies.",
                       INK, 2, leading=20)
    pg.flow(tx, body_end + 8, 524,
            "Riyadh says its defences intercepted the attack; crude "
            "spiked as traders priced in the risk to the world's "
            "largest oil export terminal.", GREY, 1, leading=12)
    pg.box(tx, body_end + 40, 150, 2, GOLD)

    # ---- two illustrated stories
    cy = 452
    cw = 476
    for cx, scene, kick, head, body in (
        (28, hormuz_scene, "SHIPPING - GULF",
         "TANKERS HIT MINES IN STRAIT OF HORMUZ",
         "Two oil tankers strike naval mines in the world's busiest "
         "oil chokepoint as Gulf tensions climb."),
        (520, gaza_scene, "MIDDLE EAST - GAZA",
         "ISRAEL STRIKE IN GAZA STRAINS CEASEFIRE",
         "Israel kills a senior Hamas security official in Gaza; the "
         "fragile ceasefire comes under fresh strain."),
    ):
        pg.frame(cx, cy, cw, 252, INK, 2)
        scene(pg, cx + 2, cy + 2, cw - 4, 128)
        pg.put_text(cx + 12, cy + 142, kick, RED, 1)
        pg.flow(cx + 12, cy + 160, cw - 24, head, INK, 2, leading=19)
        pg.flow(cx + 12, cy + 204, cw - 24, body, GREY, 1, leading=12)

    # ---- trade & markets band
    my = 722
    pg.box(28, my, W - 56, 148, NAVY)
    pg.put_text(44, my + 12, "TRADE & MARKETS", GOLD, 2)
    pg.hrule(44, my + 36, W - 88, GOLD, 1)
    colw = (W - 88) // 3
    # tariffs
    cx = 44
    pg.put_text(cx, my + 48, "US TARIFFS: 14 PARTNERS", WHITE, 1)
    bars(pg, cx, my + 66, 150, 62, (55, 70, 85, 100, 90), ORANGE)
    pg.put_text(cx, my + 134, "UP TO 15% - CHINA, EU, JAPAN", WHITE, 1)
    # taiwan
    cx = 44 + colw
    pg.put_text(cx, my + 48, "TAIWAN SHARES TUMBLE", WHITE, 1)
    pg.seg(cx + 8, my + 72, cx + 140, my + 124, RED)
    pg.tri(cx + 128, my + 112, cx + 152, my + 112, cx + 140, my + 130, RED)
    pg.put_text(cx, my + 134, "TAIEX -1,927 PTS - DOLLAR PAST 33", WHITE, 1)
    # ai sell-off
    cx = 44 + 2 * colw
    pg.put_text(cx, my + 48, "AI SELL-OFF DEEPENS", WHITE, 1)
    pg.box(cx + 8, my + 72, 52, 52, INK)
    pg.put_text(cx + 16, my + 88, "AI", FLAME, 2)
    pg.seg(cx + 76, my + 76, cx + 150, my + 120, RED)
    pg.tri(cx + 138, my + 108, cx + 162, my + 108, cx + 150, my + 126, RED)
    pg.put_text(cx, my + 134, "NVIDIA ON DOWNGRADE WATCH", WHITE, 1)

    # ---- day in brief, two columns
    by = 888
    pg.put_text(28, by, "THE DAY IN BRIEF", RED, 2)
    pg.hrule(28, by + 24, W - 56, INK, 2)
    brief_left = [
        "MUMBAI MARKS 18 YEARS SINCE 26/11 ATTACKS; INDIA OBSERVES CONSTITUTION DAY",
        "PAKISTAN'S FIRST ASTRONAUT JOINS CHINA'S SHENZHOU-24 MISSION TO TIANGONG",
        "UKRAINE HITS RUSSIAN REFINERIES; PUTIN VOWS RETALIATION",
        "31 KILLED IN CAIRO FUEL-TANKER FIRE ON HIGHWAY",
    ]
    brief_right = [
        "NORTH KOREA EXPELS SWISS DIPLOMAT IN SANCTIONS ROW",
        "SOLOMON ISLANDS SIGNS HISTORIC SECURITY TREATY WITH AUSTRALIA",
        "AGE 15, SOORYAVANSHI SMASHES FASTEST LIST A DOUBLE CENTURY - 204 OFF 53",
        "100TH MACY'S THANKSGIVING DAY PARADE TAKES TO NEW YORK STREETS",
    ]
    yy = by + 36
    for col_x, items in ((28, brief_left), (520, brief_right)):
        y = yy
        for item in items:
            pg.put_text(col_x, y, chr(8226), RED, 1)
            y = pg.flow(col_x + 14, y, 452, item, INK, 1, leading=11)
            y += 2
    pg.hrule(28, 992, W - 56, INK, 1)
    pg.put_center(W // 2, 1000, "SOURCES: REUTERS - BBC - CNN - AFP - AP",
                  GREY, 1)
    return pg


def main():
    out = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out, exist_ok=True)
    pg = build()
    path = os.path.join(out, "entry.png")
    n = write_png(pg, path)
    print(f"wrote {path} ({n} bytes, {W}x{H})")


if __name__ == "__main__":
    main()
