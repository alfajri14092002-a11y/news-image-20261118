#!/usr/bin/env python3
"""Build page.html for the 46-story front page (v4) from stories-v4.json.

Layout (1024x1024): masthead, 7-region strip, 3 hero drawn stories,
8 small drawn stories, 35 compact one-line stories in 3 columns,
DATE CHECK box, footer. Run: python3 build_page.py
"""
import html
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

CSS = """
  * { margin: 0; padding: 0; box-sizing: border-box; }
  html, body { width: 1024px; height: 1024px; overflow: hidden; }
  body {
    background: #f7f3ea; color: #141414;
    font-family: "Liberation Sans", "DejaVu Sans", sans-serif;
    -webkit-font-smoothing: antialiased;
  }
  .page { height: 1024px; padding: 10px 16px 8px; display: flex; flex-direction: column; }
  .serif { font-family: "Liberation Serif", "DejaVu Serif", serif; }
  .kicker { color: #b91c1c; font-weight: bold; letter-spacing: 1px; }

  .masthead { background: #10243e; color: #fff; display: flex; align-items: center; gap: 14px; padding: 8px 14px; }
  .datebox { background: #b91c1c; text-align: center; padding: 5px 11px 6px; line-height: 1; flex-shrink: 0; }
  .datebox .mon { font-size: 11px; font-weight: bold; letter-spacing: 2px; }
  .datebox .day { font-family: "Liberation Serif", "DejaVu Serif", serif; font-size: 32px; font-weight: bold; line-height: 1.05; }
  .datebox .yr { font-size: 9px; letter-spacing: 1px; }
  .titleblock { flex: 1; }
  .titleblock h1 { font-family: "Liberation Serif", "DejaVu Serif", serif; font-size: 36px; line-height: 1.02; }
  .titleblock .sub { color: #e8c15a; font-size: 12px; font-weight: bold; letter-spacing: 4px; margin-top: 3px; }
  .titleblock .tag { color: #cfd8e3; font-size: 11px; font-style: italic; margin-top: 3px; }
  .count { text-align: right; color: #e8c15a; font-size: 11px; font-weight: bold; line-height: 1.55; letter-spacing: 1px; flex-shrink: 0; }

  .regions { display: flex; justify-content: space-between; padding: 5px 4px 0; font-size: 10.5px; font-weight: bold; letter-spacing: 1px; color: #4a4238; }
  .regions b { color: #b91c1c; }

  .top3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 12px; margin-top: 8px; }
  .topstory { background: #fffdf6; border: 1px solid #d8d0bd; }
  .topstory .banner { height: 68px; width: 100%; display: block; }
  .topstory .body { padding: 6px 10px 7px; }
  .topstory .kicker .n { background: #b91c1c; color: #fff; padding: 1px 5px; margin-right: 4px; }
  .topstory h2 { font-family: "Liberation Serif", "DejaVu Serif", serif; font-size: 21px; line-height: 1.12; margin-top: 4px; }
  .topstory p { font-size: 12px; line-height: 1.35; color: #333; margin-top: 4px; }
  .topstory .kicker { font-size: 10px; }

  .drawn8 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-top: 8px; }
  .drawn { background: #fffdf6; border: 1px solid #d8d0bd; }
  .drawn .banner { height: 42px; width: 100%; display: block; }
  .drawn .body { padding: 5px 8px 6px; }
  .drawn .kicker .n { background: #b91c1c; color: #fff; padding: 1px 4px; margin-right: 4px; }
  .drawn .kicker { font-size: 9px; }
  .drawn h3 { font-family: "Liberation Serif", "DejaVu Serif", serif; font-size: 13.5px; line-height: 1.2; margin-top: 3px; }

  .rest { margin-top: 8px; border-top: 2px solid #141414; padding-top: 5px; }
  .rest h4 { color: #b91c1c; font-size: 11px; letter-spacing: 2px; }
  .cols { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1px 20px; margin-top: 3px; }
  .item { font-size: 11.5px; line-height: 1.25; padding: 1.2px 0; border-bottom: 1px solid #e3dcc9; }
  .item .n { color: #b91c1c; font-weight: bold; }
  .item b { font-weight: bold; }

  .datecheck { margin-top: 7px; background: #f3ead3; border: 1px solid #d8c98f; padding: 5px 10px; font-size: 11px; line-height: 1.35; }
  .datecheck b { color: #b91c1c; letter-spacing: 1px; }
  footer { margin-top: 6px; font-size: 10.5px; color: #6b6259; text-align: center; line-height: 1.4; }
"""


def label_strip(label, y=70, h=12, fs=9):
    return (f'<rect x="0" y="{y}" width="300" height="{h}" fill="#b91c1c"/>'
            f'<text x="8" y="{y + h - 3}" fill="#fff" font-family="sans-serif" '
            f'font-size="{fs}" font-weight="bold" letter-spacing="1">{html.escape(label)}</text>')


def hero_svg(art, label):
    if art == "shenzhen":
        inner = """
        <rect width="300" height="82" fill="#0e2a4e"/>
        <g fill="#e8c15a">
          <rect x="18" y="42" width="16" height="40"/><rect x="40" y="30" width="14" height="52"/>
          <rect x="60" y="50" width="20" height="32"/><rect x="86" y="22" width="14" height="60"/>
          <rect x="106" y="38" width="18" height="44"/><rect x="130" y="48" width="12" height="34"/>
          <rect x="148" y="28" width="16" height="54"/><rect x="170" y="44" width="18" height="38"/>
          <rect x="194" y="34" width="13" height="48"/><rect x="213" y="52" width="20" height="30"/>
          <rect x="239" y="40" width="14" height="42"/><rect x="259" y="30" width="16" height="52"/>
        </g>
        <g fill="#fff"><circle cx="52" cy="14" r="2"/><circle cx="120" cy="10" r="1.6"/><circle cx="200" cy="16" r="2"/><circle cx="262" cy="12" r="1.6"/><circle cx="150" cy="8" r="1.4"/></g>"""
    elif art == "gulf":
        inner = """
        <rect width="300" height="82" fill="#123f3a"/>
        <g fill="none" stroke="#7fb8a8" stroke-width="1.5">
          <circle cx="150" cy="41" r="12"/><circle cx="150" cy="41" r="24"/><circle cx="150" cy="41" r="36"/>
        </g>
        <g fill="#e8c15a"><circle cx="150" cy="41" r="3.5"/><circle cx="118" cy="30" r="3"/><circle cx="182" cy="52" r="3"/><circle cx="132" cy="58" r="2.5"/><circle cx="172" cy="26" r="2.5"/></g>
        <g stroke="#e8c15a" stroke-width="1.5"><line x1="150" y1="41" x2="118" y2="30"/><line x1="150" y1="41" x2="182" y2="52"/></g>"""
    elif art == "voyager":
        inner = """
        <rect width="300" height="82" fill="#0b0b18"/>
        <g fill="#fff">
          <circle cx="30" cy="16" r="1.8"/><circle cx="70" cy="30" r="1.4"/><circle cx="110" cy="12" r="2"/><circle cx="160" cy="24" r="1.5"/>
          <circle cx="210" cy="14" r="1.8"/><circle cx="250" cy="28" r="1.4"/><circle cx="285" cy="12" r="2"/><circle cx="50" cy="52" r="1.4"/><circle cx="270" cy="52" r="1.5"/>
        </g>
        <g stroke="#e8c15a" stroke-width="1.5" fill="none"><path d="M40 62 L150 40 L262 22"/></g>
        <g fill="#e8c15a"><circle cx="262" cy="22" r="4"/><rect x="256" y="18" width="12" height="2.4" transform="rotate(-14 262 22)"/></g>
        <circle cx="40" cy="62" r="5" fill="#7fb8a8"/>"""
    else:
        raise ValueError(f"unknown hero art {art}")
    return ('<svg class="banner" viewBox="0 0 300 82" preserveAspectRatio="none">'
            + inner + label_strip(label, y=66, h=16, fs=10) + '</svg>')


def small_svg(art, label):
    scenes = {
        "drones": """
        <rect width="300" height="48" fill="#1c2733"/>
        <g stroke="#7fb8a8" stroke-width="1" stroke-dasharray="3 3" fill="none">
          <path d="M20 12 L90 26"/><path d="M120 8 L190 24"/><path d="M210 14 L280 30"/>
        </g>
        <g fill="#e8c15a">
          <rect x="86" y="22" width="10" height="3"/><rect x="89" y="19" width="3" height="9"/>
          <rect x="186" y="20" width="10" height="3"/><rect x="189" y="17" width="3" height="9"/>
          <rect x="276" y="26" width="10" height="3"/><rect x="279" y="23" width="3" height="9"/>
        </g>
        <g fill="#b91c1c"><circle cx="91" cy="24" r="2"/><circle cx="191" cy="22" r="2"/><circle cx="281" cy="28" r="2"/></g>
        <g fill="#fff"><circle cx="40" cy="10" r="1.4"/><circle cx="150" cy="8" r="1.4"/><circle cx="250" cy="10" r="1.4"/></g>""",
        "cyclone": """
        <rect width="300" height="48" fill="#0f3d4a"/>
        <g fill="none" stroke="#7fb8a8" stroke-width="2">
          <path d="M150 24 m-4 0 a4 4 0 1 1 8 0 a4 4 0 1 1 -8 0"/>
          <path d="M150 24 m-10 0 a10 10 0 1 1 20 0 a10 10 0 1 1 -20 0"/>
          <path d="M150 24 m-17 0 a17 17 0 1 1 34 0 a17 17 0 1 1 -34 0"/>
        </g>
        <g stroke="#bfe3d8" stroke-width="1.2"><line x1="30" y1="8" x2="24" y2="20"/><line x1="60" y1="6" x2="54" y2="18"/><line x1="240" y1="8" x2="246" y2="20"/><line x1="270" y1="6" x2="276" y2="18"/></g>
        <circle cx="150" cy="24" r="2.5" fill="#e8c15a"/>""",
        "tanks": """
        <rect width="300" height="48" fill="#c9a86a"/>
        <circle cx="262" cy="12" r="7" fill="#e8c15a"/>
        <rect y="36" width="300" height="12" fill="#a9854e"/>
        <g fill="#5a4632">
          <rect x="40" y="26" width="52" height="10"/><rect x="58" y="19" width="18" height="8"/>
          <rect x="76" y="21" width="34" height="3"/>
          <rect x="180" y="28" width="44" height="9"/><rect x="194" y="22" width="15" height="7"/>
          <rect x="209" y="24" width="28" height="2.6"/>
        </g>
        <g fill="#3d2f1e"><circle cx="52" cy="38" r="2.4"/><circle cx="66" cy="38" r="2.4"/><circle cx="80" cy="38" r="2.4"/><circle cx="190" cy="39" r="2.2"/><circle cx="202" cy="39" r="2.2"/><circle cx="214" cy="39" r="2.2"/></g>""",
        "fed": """
        <rect width="300" height="48" fill="#10243e"/>
        <g fill="#e8e4d8">
          <rect x="40" y="16" width="10" height="22"/><rect x="36" y="13" width="18" height="3"/><rect x="36" y="38" width="18" height="3"/>
          <rect x="70" y="16" width="10" height="22"/><rect x="66" y="13" width="18" height="3"/><rect x="66" y="38" width="18" height="3"/>
          <rect x="100" y="16" width="10" height="22"/><rect x="96" y="13" width="18" height="3"/><rect x="96" y="38" width="18" height="3"/>
        </g>
        <g stroke="#e8c15a" stroke-width="2.5" fill="none"><path d="M150 36 L185 26 L215 28 L258 10"/></g>
        <polygon points="258,10 246,12 254,20" fill="#e8c15a"/>""",
        "eu": """
        <rect width="300" height="48" fill="#1e3a8a"/>
        <g fill="#e8c15a">
          <circle cx="150" cy="10" r="2.6"/><circle cx="166" cy="14" r="2.6"/><circle cx="172" cy="24" r="2.6"/>
          <circle cx="166" cy="34" r="2.6"/><circle cx="150" cy="38" r="2.6"/><circle cx="134" cy="34" r="2.6"/>
          <circle cx="128" cy="24" r="2.6"/><circle cx="134" cy="14" r="2.6"/>
        </g>
        <circle cx="150" cy="24" r="5" fill="none" stroke="#e8c15a" stroke-width="1.2"/>""",
        "ipo": """
        <rect width="300" height="48" fill="#0d2b1a"/>
        <g fill="#e8c15a">
          <rect x="40" y="30" width="16" height="10"/><rect x="66" y="24" width="16" height="16"/>
          <rect x="92" y="18" width="16" height="22"/><rect x="118" y="12" width="16" height="28"/>
        </g>
        <g stroke="#fff" stroke-width="2" fill="none"><path d="M40 30 L74 22 L100 16 L126 10 L160 6 L200 4"/></g>
        <polygon points="200,4 188,6 196,12" fill="#fff"/>""",
        "chip": """
        <rect width="300" height="48" fill="#0b0b18"/>
        <g stroke="#22c55e" stroke-width="1.5">
          <line x1="128" y1="24" x2="112" y2="24"/><line x1="128" y1="18" x2="112" y2="18"/><line x1="128" y1="30" x2="112" y2="30"/>
          <line x1="172" y1="24" x2="188" y2="24"/><line x1="172" y1="18" x2="188" y2="18"/><line x1="172" y1="30" x2="188" y2="30"/>
          <line x1="150" y1="8" x2="150" y2="2"/><line x1="142" y1="8" x2="142" y2="2"/><line x1="158" y1="8" x2="158" y2="2"/>
        </g>
        <rect x="128" y="8" width="44" height="32" fill="#14532d" stroke="#22c55e" stroke-width="1.5"/>
        <rect x="140" y="16" width="20" height="16" fill="#22c55e"/>""",
        "cop31": """
        <rect width="300" height="48" fill="#14532d"/>
        <circle cx="150" cy="24" r="16" fill="#7fb8a8"/>
        <g fill="none" stroke="#14532d" stroke-width="1.2">
          <ellipse cx="150" cy="24" rx="7" ry="16"/><path d="M134 24 h32"/><path d="M138 14 q12 10 24 0"/><path d="M138 34 q12 -10 24 0"/>
        </g>
        <g fill="#e8c15a"><path d="M52 34 q8 -14 16 0 q-8 4 -16 0"/><path d="M232 34 q8 -14 16 0 q-8 4 -16 0"/></g>""",
        "rocket": """
        <rect width="300" height="48" fill="#0b1e3a"/>
        <g fill="#fff"><circle cx="40" cy="10" r="1.4"/><circle cx="80" cy="16" r="1.2"/><circle cx="230" cy="10" r="1.4"/><circle cx="266" cy="18" r="1.2"/><circle cx="200" cy="8" r="1.2"/></g>
        <g fill="#e8e4d8"><path d="M150 6 L158 24 L150 30 L142 24 Z"/><rect x="142" y="24" width="16" height="6"/></g>
        <g fill="#e8c15a"><path d="M146 30 L150 42 L154 30 Z"/></g>
        <g stroke="#7fb8a8" stroke-width="1.2" fill="none"><path d="M150 42 q-4 4 0 6"/><path d="M150 42 q4 4 0 6"/></g>""",
        "train": """
        <rect width="300" height="48" fill="#26221c"/>
        <rect y="30" width="300" height="2.4" fill="#8a7f63"/>
        <g stroke="#8a7f63" stroke-width="1"><line x1="20" y1="30" x2="20" y2="36"/><line x1="60" y1="30" x2="60" y2="36"/><line x1="100" y1="30" x2="100" y2="36"/><line x1="140" y1="30" x2="140" y2="36"/><line x1="180" y1="30" x2="180" y2="36"/><line x1="220" y1="30" x2="220" y2="36"/><line x1="260" y1="30" x2="260" y2="36"/></g>
        <g fill="#b91c1c"><rect x="52" y="18" width="80" height="11" transform="rotate(-8 92 24)"/></g>
        <g fill="#26221c"><rect x="60" y="20" width="9" height="4" transform="rotate(-8 92 24)"/><rect x="78" y="20" width="9" height="4" transform="rotate(-8 92 24)"/><rect x="96" y="20" width="9" height="4" transform="rotate(-8 92 24)"/></g>
        <g fill="#e8e4d8"><rect x="150" y="16" width="96" height="13"/><rect x="158" y="19" width="10" height="5"/><rect x="174" y="19" width="10" height="5"/><rect x="190" y="19" width="10" height="5"/><rect x="206" y="19" width="10" height="5"/><rect x="222" y="19" width="10" height="5"/></g>""",
    }
    if art not in scenes:
        raise ValueError(f"unknown small art {art}")
    return ('<svg class="banner" viewBox="0 0 300 48" preserveAspectRatio="none">'
            + scenes[art] + label_strip(label, y=36, h=12, fs=8) + '</svg>')


def main():
    with open(os.path.join(HERE, "stories-v4.json"), encoding="utf-8") as f:
        data = json.load(f)
    stories = data["stories"]
    heroes = [s for s in stories if s.get("hero")]
    drawn = [s for s in stories if s.get("drawn")]
    rest = [s for s in stories if not s.get("hero") and not s.get("drawn")]
    assert len(heroes) == 3, f"need 3 heroes, got {len(heroes)}"
    assert len(drawn) == 8, f"need 8 drawn, got {len(drawn)}"
    assert len(rest) == 35, f"need 35 rest, got {len(rest)}"
    assert len(stories) == 46, f"need 46 stories, got {len(stories)}"

    order = heroes + drawn + rest
    for i, s in enumerate(order, 1):
        s["n"] = i

    regions = ["ASIA", "MIDDLE EAST", "EUROPE", "AFRICA", "NORTH AMERICA", "SOUTH AMERICA", "OCEANIA"]
    counts = {r: sum(1 for s in stories if s["region"] == r) for r in regions}
    assert all(counts[r] > 0 for r in regions), f"empty region: {counts}"
    assert sum(counts.values()) == 46
    region_strip = " &nbsp;&bull;&nbsp; ".join(
        f"{r.title()} <b>{counts[r]}</b>" for r in regions)

    e = html.escape

    hero_html = ""
    for s in heroes:
        hero_html += f"""
    <article class="topstory">
      {hero_svg(s["art"], s["label"])}
      <div class="body">
        <div class="kicker"><span class="n">{s["n"]}</span>{e(s["region"])} &bull; {e(s["topic"])}</div>
        <h2>{e(s["headline"])}</h2>
        <p>{e(s["summary"])}</p>
      </div>
    </article>"""

    drawn_html = ""
    for s in drawn:
        drawn_html += f"""
    <article class="drawn">
      {small_svg(s["art"], s["label"])}
      <div class="body">
        <div class="kicker"><span class="n">{s["n"]}</span>{e(s["region"])} &bull; {e(s["topic"])}</div>
        <h3>{e(s["headline"])}</h3>
      </div>
    </article>"""

    cols = [[], [], []]
    for i, s in enumerate(rest):
        cols[i % 3].append(s)
    cols_html = ""
    for col in cols:
        cols_html += "      <div>\n"
        for s in col:
            cols_html += (f'        <div class="item"><span class="n">{s["n"]}</span> '
                          f'<b>{e(s["lead"])}</b> {e(s["clause"])}</div>\n')
        cols_html += "      </div>\n"

    datecheck = data["datecheck"]
    footer_sources = data["sources"]

    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Wednesday 18 November 2026 — The Day in World News</title>
<style>{CSS}</style>
</head>
<body>
<div class="page">

  <header class="masthead">
    <div class="datebox">
      <div class="mon">NOV</div>
      <div class="day">18</div>
      <div class="yr">WED &bull; 2026</div>
    </div>
    <div class="titleblock">
      <h1>Wednesday 18 November 2026</h1>
      <div class="sub">THE DAY IN WORLD NEWS</div>
      <div class="tag">Everything on this page happened, or was first reported, on Wednesday 18 November 2026.</div>
    </div>
    <div class="count">46 STORIES<br>7 REGIONS<br>ONE PAGE</div>
  </header>

  <div class="regions">{region_strip}</div>

  <section class="top3">{hero_html}
  </section>

  <section class="drawn8">{drawn_html}
  </section>

  <section class="rest">
    <h4>THE REST OF THE DAY &mdash; 35 MORE STORIES</h4>
    <div class="cols">
{cols_html}    </div>
  </section>

  <div class="datecheck"><b>DATE CHECK</b> &mdash; {e(datecheck)}</div>
  <footer>All 46 stories happened, or were first reported, on Wednesday 18 November 2026; claims are attributed. Original drawings.<br>Sources: {e(footer_sources)}</footer>

</div>
</body>
</html>
"""
    out = os.path.join(HERE, "page.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(page)
    print(f"wrote {out}: {len(stories)} stories, regions {counts}")


if __name__ == "__main__":
    main()
