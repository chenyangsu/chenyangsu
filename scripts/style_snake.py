"""Frame Platane/snk's snake in a card that matches the hero, with real contribution stats.

Run: GITHUB_TOKEN=... python3 scripts/style_snake.py <snk dark svg> <output svg>
The input must be snk's output with the github-dark palette; the card is dark in both themes.
"""
import datetime
import json
import os
import re
import sys
import urllib.request

from build import BAR, BG, GOLD, INK, INK2, LINE, MUTED
from svgkit import Svg

USER = "chenyangsu"
W, H = 1000, 316
CELL, GRID_Y = 16, 150  # snk's grid pitch; where snk's y = 0 lands in the card


def calendar():
    query = ('{user(login:"%s"){contributionsCollection{contributionCalendar{totalContributions '
             'weeks{firstDay contributionDays{date contributionCount}}}}}}' % USER)
    req = urllib.request.Request("https://api.github.com/graphql", data=json.dumps({"query": query}).encode(),
                                 headers={"Authorization": f"bearer {os.environ['GITHUB_TOKEN']}"})
    data = json.load(urllib.request.urlopen(req))
    return data["data"]["user"]["contributionsCollection"]["contributionCalendar"]


def streaks(days):
    """Longest run of days with contributions, and the run ending today (or yesterday, as GitHub counts it)."""
    counts = [d["contributionCount"] for d in days]
    longest = run = 0
    for c in counts:
        run = run + 1 if c else 0
        longest = max(longest, run)
    if counts and counts[-1] == 0:
        counts = counts[:-1]
    current = 0
    for c in reversed(counts):
        if not c:
            break
        current += 1
    return longest, current


def main(src, dst):
    cal = calendar()
    weeks = cal["weeks"]
    days = [d for w in weeks for d in w["contributionDays"]]
    longest, current = streaks(days)
    snk = open(src).read()
    m = re.match(r'<svg viewBox="([-\d. ]+)" width="(\d+)" height="(\d+)"[^>]*>(.*)</svg>\s*$', snk, re.S)
    viewbox, sw, sh, inner = m.groups()
    vx, vy = (float(v) for v in viewbox.split()[:2])
    palette = dict(re.findall(r"--(c[0-4]):(#[0-9a-f]{6})", inner))
    n_cols = len({x for x in re.findall(r'<rect class="c[^"]*" x="([\d.]+)"', inner)})
    assert n_cols == len(weeks), f"snake grid has {n_cols} columns, calendar has {len(weeks)} weeks"

    # centre the grid: cells start at x = 2 in snk and are 12 px wide on a 16 px pitch
    GL = (W - (n_cols * CELL - 4)) / 2  # left edge of the first column
    GR = GL + n_cols * CELL - 4  # right edge of the last column
    GRID_X = GL - 2
    total = cal["totalContributions"]
    s = Svg(W, H, f"{total:,} GitHub contributions in the last year, longest streak {longest} days, current streak "
                  f"{current} days, drawn as a contribution graph that a snake eats.")
    # snk draws the snake at the end of its file; tint the head bright and fade the tail, add a glow,
    # round the progress bar away (the card carries its own legend)
    s.css.append(".s{filter:url(#glow)}.s.s0{fill:#ffd66e}.s.s1{fill:%s}.s.s2{fill:#c98f2a;opacity:.85}"
                 ".s.s3{fill:#a8741f;opacity:.7}.u{display:none}" % GOLD)
    s.add('<defs><filter id="glow" x="-100%" y="-100%" width="300%" height="300%">'
          '<feGaussianBlur stdDeviation="3.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="b"/>'
          '<feMergeNode in="SourceGraphic"/></feMerge></filter></defs>')
    s.add(f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="12" fill="{BG}" stroke="{LINE}"/>')
    s.add(f'<path d="M12.5 .5h{W - 25}a12 12 0 0 1 12 12v27.5H.5V12.5a12 12 0 0 1 12-12z" fill="{BAR}"/>')
    s.add(f'<rect x="1" y="40" width="{W - 2}" height="1" fill="{LINE}"/>')
    s.text(24, 25, "~/chenyangsu/contributions", "Plex Mono", "500", 13, INK2)
    s.text(W - 24, 25, "last 12 months", "Plex Mono", "400", 13, MUTED, anchor="end")

    # stats line
    w = s.text(GL, 92, f"{total:,}", "Geist", "700", 30, INK, tracking=-0.6)
    s.text(GL + w + 12, 92, "contributions in the last year", "Plex Mono", "400", 14, INK2)
    s.text(GR, 92, f"longest streak {longest}d · current {current}d", "Plex Mono", "400", 13, MUTED,
           anchor="end")

    # month labels at the first week of each month, weekday labels on the left (as on GitHub)
    last_col = -9
    for i, wk in enumerate(weeks):
        first = datetime.date.fromisoformat(wk["firstDay"])
        prev = datetime.date.fromisoformat(weeks[i - 1]["firstDay"]) if i else None
        if (prev is None or first.month != prev.month) and i - last_col >= 3:
            s.text(GL + i * CELL, GRID_Y - 10, first.strftime("%b"), "Plex Mono", "400", 11.5, MUTED)
            last_col = i
    for row, name in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        s.text(GL - 8, GRID_Y + 2 + row * CELL + 10, name, "Plex Mono", "400", 11, MUTED, anchor="end")

    # the snake and its grid
    s.add(f'<svg x="{GRID_X + vx:.1f}" y="{GRID_Y + vy:.1f}" width="{sw}" height="{sh}" viewBox="{viewbox}" '
          f'overflow="visible">{inner}</svg>')

    # legend
    lx, ly = GR, H - 26
    w = s.text(lx, ly, "more", "Plex Mono", "400", 11.5, MUTED, anchor="end")
    x = lx - w - 8 - 5 * 15
    for k in range(5):
        s.add(f'<rect x="{x + k * 15}" y="{ly - 10}" width="11" height="11" rx="2" fill="{palette[f"c{k}"]}"/>')
    s.text(x - 8, ly, "less", "Plex Mono", "400", 11.5, MUTED, anchor="end")
    s.text(GL, ly, f"{datetime.date.fromisoformat(days[0]['date']):%-d %b %Y} – "
                       f"{datetime.date.fromisoformat(days[-1]['date']):%-d %b %Y}", "Plex Mono", "400", 11.5, MUTED)
    open(dst, "w").write(s.render())


if __name__ == "__main__":
    main(*sys.argv[1:3])
