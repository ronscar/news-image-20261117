"""Generate entry.png for news-image-20261117.

Draws a newspaper front page summing up Tuesday 17 November 2026 world
news: six verified stories of that day, each with a tag, a headline, a
short factual deck and a simple pictogram. Pure Pillow drawing, no network,
no randomness, no model calls. Run: python3 gen.py  ->  entry.png (1024x1024)
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)      # warm newsprint
INK = (20, 28, 43)           # near-black navy
NAVY = (20, 36, 61)          # masthead band
AMBER = (242, 183, 5)        # date accent
CARD = (255, 255, 255)
MUTED = (90, 96, 110)
RULE = (203, 209, 219)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines fitting max_w pixels."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_bridge(d, x, y, s, c):
    # Deck, two arches, posts: the Kerch Bridge.
    d.line([(x, y + s * 0.55), (x + s, y + s * 0.55)], fill=c, width=5)
    d.arc([x + 2, y + s * 0.15, x + s * 0.5, y + s * 0.75], 180, 360, fill=c, width=5)
    d.arc([x + s * 0.5, y + s * 0.15, x + s - 2, y + s * 0.75], 180, 360, fill=c, width=5)
    d.line([(x + s * 0.5, y + s * 0.15), (x + s * 0.5, y + s * 0.55)], fill=c, width=4)
    d.line([(x + 4, y + s * 0.55), (x + 4, y + s * 0.85)], fill=c, width=4)
    d.line([(x + s - 4, y + s * 0.55), (x + s - 4, y + s * 0.85)], fill=c, width=4)


def draw_drone(d, x, y, s, c):
    # Quad-rotor drone seen from above.
    cx, cy = x + s / 2, y + s / 2
    r = s * 0.16
    for px, py in [(x + 6, y + 6), (x + s - 6, y + 6),
                   (x + 6, y + s - 6), (x + s - 6, y + s - 6)]:
        d.line([(cx, cy), (px, py)], fill=c, width=4)
        d.ellipse([px - r, py - r, px + r, py + r], outline=c, width=4)
    d.ellipse([cx - s * 0.16, cy - s * 0.13, cx + s * 0.16, cy + s * 0.13],
              fill=c)


def draw_aid(d, x, y, s, c):
    # Aid box with a cross.
    d.rectangle([x + 4, y + s * 0.2, x + s - 4, y + s * 0.85], outline=c, width=5)
    d.rectangle([x + s * 0.38, y + s * 0.32, x + s * 0.62, y + s * 0.73], fill=c)
    d.rectangle([x + s * 0.25, y + s * 0.45, x + s * 0.75, y + s * 0.60], fill=c)


def draw_globe(d, x, y, s, c):
    # Globe: circle, meridian ellipse, equator.
    d.ellipse([x + 4, y + 4, x + s - 4, y + s - 4], outline=c, width=5)
    d.ellipse([x + s * 0.28, y + 4, x + s * 0.72, y + s - 4], outline=c, width=4)
    d.line([(x + 4, y + s / 2), (x + s - 4, y + s / 2)], fill=c, width=4)


def draw_pin(d, x, y, s, c):
    # Map pin.
    d.ellipse([x + s * 0.22, y + 4, x + s * 0.78, y + s * 0.6], outline=c, width=5)
    d.polygon([(x + s * 0.30, y + s * 0.52), (x + s * 0.70, y + s * 0.52),
               (x + s * 0.5, y + s * 0.92)], fill=c)
    d.ellipse([x + s * 0.40, y + s * 0.18, x + s * 0.60, y + s * 0.38], fill=c)


def draw_chip(d, x, y, s, c):
    # Microchip: square, inner square, pins on four sides.
    d.rectangle([x + s * 0.22, y + s * 0.22, x + s * 0.78, y + s * 0.78],
                outline=c, width=5)
    d.rectangle([x + s * 0.40, y + s * 0.40, x + s * 0.60, y + s * 0.60], fill=c)
    for i in range(3):
        t = s * (0.32 + 0.18 * i)
        d.line([(x + t, y + 2), (x + t, y + s * 0.22)], fill=c, width=4)
        d.line([(x + t, y + s * 0.78), (x + t, y + s - 2)], fill=c, width=4)
        d.line([(x + 2, y + t), (x + s * 0.22, y + t)], fill=c, width=4)
        d.line([(x + s * 0.78, y + t), (x + s - 2, y + t)], fill=c, width=4)


# (tag, colour, headline lines, deck, icon drawer)
STORIES = [
    ("UKRAINE", (179, 38, 30),
     ["KERCH BRIDGE", "HIT AGAIN"],
     "Ukraine strikes the bridge to Crimea for a second day; a road span "
     "collapses into the strait.",
     draw_bridge),
    ("THE GULF", (194, 87, 11),
     ["DRONES TARGET", "US BASE IN BAHRAIN"],
     "Iranian drones hit a US radar site; Bahrain says all intercepted. "
     "Tankers hit mines near Hormuz.",
     draw_drone),
    ("GAZA", (15, 118, 110),
     ["WEST PRESSES ISRAEL", "ON GAZA AID"],
     "UK, Australia, Canada and Italy call the crisis catastrophic; the UN "
     "warns 1.7m remain displaced.",
     draw_aid),
    ("ASIA", (29, 78, 216),
     ["TRUMP OPENS ASIA", "TRIP IN MANILA"],
     "Quad summit opens his tour; Trump, Xi and Putin are set to meet in "
     "Shenzhen on Thursday.",
     draw_globe),
    ("EUROPE", (109, 40, 217),
     ["FIVE EU STATES PLAN", "RWANDA RETURN HUB"],
     "Austria, Denmark, Germany, Greece and the Netherlands would send "
     "rejected asylum seekers to Rwanda.",
     draw_pin),
    ("TECH & MARKETS", (21, 128, 61),
     ["US CLOSES CHIP-EXPORT", "LOOPHOLE"],
     "New rules target data centres renting computing power to China. "
     "Bitcoin holds below $65,000.",
     draw_chip),
]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead ----
    d.rectangle([0, 0, W, 148], fill=NAVY)
    d.text((W / 2, 52), "THE WORLD IN ONE DAY", font=font(BOLD, 58),
           fill=(255, 255, 255), anchor="mm")
    d.text((W / 2, 112), "T U E S D A Y   ·   1 7   N O V E M B E R   2 0 2 6",
           font=font(BOLD, 30), fill=AMBER, anchor="mm")

    # ---- Subhead ----
    sub = "Six stories that defined the day — from Kyiv to the Gulf, Manila to Brussels."
    d.text((W / 2, 178), sub, font=font(REG, 22), fill=MUTED, anchor="mm")
    d.line([(24, 200), (W - 24, 200)], fill=RULE, width=2)

    # ---- Story grid: 2 columns x 3 rows ----
    gx, gy, gap = 24, 214, 16
    pw = (W - 2 * gx - gap) // 2          # 480
    ph = 236
    tag_f = font(BOLD, 17)
    head_f = font(BOLD, 29)
    deck_f = font(REG, 19)

    for i, (tag, colour, headline, deck, icon) in enumerate(STORIES):
        col, row = i % 2, i // 2
        x = gx + col * (pw + gap)
        y = gy + row * (ph + gap)

        d.rectangle([x, y, x + pw, y + ph], fill=CARD)
        d.rectangle([x, y, x + pw, y + 6], fill=colour)
        d.line([(x, y + ph), (x + pw, y + ph)], fill=RULE, width=1)
        d.line([(x, y), (x, y + ph)], fill=RULE, width=1)
        d.line([(x + pw, y), (x + pw, y + ph)], fill=RULE, width=1)

        d.text((x + 20, y + 26), tag, font=tag_f, fill=colour, anchor="lm")
        hy = y + 48
        for line in headline:
            d.text((x + 20, hy), line, font=head_f, fill=INK, anchor="la")
            hy += 36

        # Icon box, bottom left; deck text beside it.
        iy = y + ph - 94
        tint = tuple(235 + (c - 235) // 4 for c in colour)
        d.rounded_rectangle([x + 20, iy, x + 96, iy + 76], radius=10,
                            fill=tint)
        icon(d, x + 28, iy + 8, 60, colour)
        lines = wrap(d, deck, deck_f, pw - 132)
        dy = iy + 2
        for line in lines[:3]:
            d.text((x + 112, dy), line, font=deck_f, fill=(52, 58, 72),
                   anchor="la")
            dy += 23

    # ---- Footer ----
    fy = gy + 3 * ph + 2 * gap + 22
    d.line([(24, fy - 12), (W - 24, fy - 12)], fill=RULE, width=2)
    d.text((W / 2, fy + 8),
           "All events reported on Tuesday 17 November 2026  ·  Sources: Reuters, CNN, AP, BBC",
           font=font(REG, 17), fill=MUTED, anchor="mm")

    img.save("entry.png", format="PNG", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
