#!/usr/bin/env python3
"""Draw entry.png: a front page summing up the world's news of
Wednesday 18 November 2026, for the make.fun news-image-20261118 bounty.

The image is drawn, not photographed: every word is rendered with PIL so
the text stays crisp and legible, and nothing in it is invented. The six
stories are the day's most consequential ones, across regions and fields,
as reported on 18 November 2026. Layout is flow-based: each block is
measured before it is drawn, so nothing overlaps. Output is 1024x1024
PNG, under 1 MiB.
"""

import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W = H = 1024
PAPER = (247, 243, 234)
PANEL = (255, 253, 247)
INK = (20, 20, 20)
RED = (185, 28, 28)
MUTED = (96, 90, 80)

SERIF_DIRS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
]
SANS_DIRS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
]
SANS_BOLD_DIRS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
]


def pick(paths):
    for p in paths:
        if os.path.exists(p):
            return p
    raise FileNotFoundError(paths[0])


def font(paths, size):
    return ImageFont.truetype(pick(paths), size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x0, x1, y, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def globe(draw, cx, cy, r):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=3)
    draw.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=INK, width=2)
    draw.line([(cx - r, cy), (cx + r, cy)], fill=INK, width=2)
    draw.arc([cx - r, cy - r, cx + r, cy + r], start=200, end=340, fill=INK, width=2)


def story_lines(draw, w, headline, summary, head_size=28, sum_size=22):
    head = wrap(draw, headline, font(SERIF_DIRS, head_size), w)
    summ = wrap(draw, summary, font(SANS_DIRS, sum_size), w)
    return head, summ


def story_height(head, summ):
    return 26 + len(head) * 33 + 4 + len(summ) * 27


def draw_story(draw, x, y, w, kicker_text, head, summ):
    draw.text((x, y), kicker_text, font=font(SANS_BOLD_DIRS, 20), fill=RED)
    y += 26
    y = text_block(draw, x, y, head, font(SERIF_DIRS, 28), INK, 33)
    y = text_block(draw, x, y + 4, summ, font(SANS_DIRS, 22), INK, 27)
    return y


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 44  # margin

    # Masthead: globe, title, date.
    globe(d, W // 2, 52, 26)
    title = "WORLD NEWS"
    tf = font(SERIF_DIRS, 78)
    d.text(((W - d.textlength(title, font=tf)) / 2, 86), title, font=tf, fill=INK)
    date = "WEDNESDAY, 18 NOVEMBER 2026"
    df = font(SANS_BOLD_DIRS, 32)
    d.text(((W - d.textlength(date, font=df)) / 2, 172), date, font=df, fill=RED)
    rule(d, mx, W - mx, 216, width=4)
    rule(d, mx, W - mx, 223, width=1)

    y = 238

    # Lead story on a white panel. Measure first, then draw the panel.
    lead_head = wrap(d, "Xi and Putin meet in Shenzhen; Trump to join them Thursday",
                     font(SERIF_DIRS, 42), W - 2 * mx - 40)
    lead_sum = wrap(d, "China and Russia denounced protectionism and sanctions, "
                       "a day before a historic US\u2013China\u2013Russia trilateral on "
                       "arms, Ukraine and Iran.",
                    font(SANS_DIRS, 24), W - 2 * mx - 40)
    lead_h = 16 + 26 + len(lead_head) * 50 + 4 + len(lead_sum) * 30 + 16
    d.rectangle([mx, y, W - mx, y + lead_h], fill=PANEL, outline=INK, width=2)
    ly = y + 16
    d.text((mx + 20, ly), "APEC SUMMIT  •  SHENZHEN",
           font=font(SANS_BOLD_DIRS, 20), fill=RED)
    ly += 26
    ly = text_block(d, mx + 20, ly, lead_head, font(SERIF_DIRS, 42), INK, 50)
    text_block(d, mx + 20, ly + 4, lead_sum, font(SANS_DIRS, 24), INK, 30)
    y += lead_h + 14

    # Secondary stories, two per row. Each row's height is the taller cell.
    col_w = (W - 2 * mx - 28) // 2
    rows = [
        [("MIDDLE EAST  •  SECURITY",
          "Iran fires drones at US bases in the Gulf",
          "Bahrain and Kuwait engaged drones in the sharpest US\u2013Iran "
          "escalation in years."),
         ("UKRAINE  •  WAR",
          "Kerch Bridge partly collapses",
          "Drones and missiles brought down part of the span to Crimea.")],
        [("SPACE  •  SCIENCE",
          "Voyager 1 reaches one light-day from Earth",
          "16.1 billion miles out; its signals now take a full day each way."),
         ("UNITED STATES  •  HEALTH",
          "US loses measles-free status held since 2000",
          "Continuous spread for over a year; 5,412 cases in 2026, the most "
          "since 1991.")],
    ]
    for i, row in enumerate(rows):
        cells = [(k, *story_lines(d, col_w, h, s)) for k, h, s in row]
        row_h = max(story_height(head, summ) for _, head, summ in cells)
        draw_story(d, mx, y, col_w, cells[0][0], cells[0][1], cells[0][2])
        draw_story(d, mx + col_w + 28, y, col_w, cells[1][0], cells[1][1], cells[1][2])
        y += row_h
        if i == 0:
            y += 12
            rule(d, mx, W - mx, y, width=1)
            y += 14

    # In brief: markets plus two more of the day's stories.
    y += 8
    rule(d, mx, W - mx, y, width=1)
    y += 12
    d.text((mx, y), "IN BRIEF", font=font(SANS_BOLD_DIRS, 20), fill=RED)
    y += 26
    brief = [
        ("MARKETS", "Fed minutes point to more hikes; S&P 500 below its 200-day "
                    "average, Dow down 1.11%."),
        ("ALSO", "Nvidia posts record $115.8B quarter, shares fall  •  "
                 "Sanchez named NWSL MVP."),
    ]
    for label, text in brief:
        lines = wrap(d, f"{label} \u2014 {text}", font(SANS_DIRS, 22), W - 2 * mx)
        y = text_block(d, mx, y, lines, font(SANS_DIRS, 22), INK, 28)
        y += 4

    # Footer.
    rule(d, mx, W - mx, H - 44, width=1)
    ff = font(SANS_DIRS, 18)
    foot = "The day in world news  •  Wednesday, 18 November 2026  •  As reported that day"
    d.text(((W - d.textlength(foot, font=ff)) / 2, H - 34), foot, font=ff, fill=MUTED)

    assert y <= H - 56, f"layout overflow: content ends at y={y}"
    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG", optimize=True)
    size = os.path.getsize(out)
    print(f"wrote {out} {W}x{H} {size} bytes, content ends y={y}")
    assert size <= 1048576, "entry.png over the 1 MiB cap"


if __name__ == "__main__":
    main()
