"""Draw the profile hero and link buttons into assets/. Run: python3 scripts/build.py (needs fonttools).

Every fact drawn here is taken from chenyangsu.github.io; edit ROWS or LINKS, rerun, commit the SVGs.
"""
import html
from pathlib import Path

import icons
from svgkit import Svg, width

ASSETS = Path(__file__).resolve().parent.parent / "assets"

BG, BAR, LINE = "#0b0f15", "#10161e", "#222a35"
INK, INK2, MUTED = "#f0f3f6", "#c9d1d9", "#7d8590"
BLUE, GREEN, GOLD = "#79b0ff", "#56d364", "#e3b341"

NAME, NAME_TC, TAGLINE = "Chen-Yang Su", "蘇震洋", "Evals · Agents · AI for Science"
NAME_FONT = ("Geist", "700", -1.2)  # family, weight, letter-spacing at 52 px
NAME_TC_FONT = ("Sans TC", "500")
ROLE = ("Postdoctoral Scholar, Stanford", "Biomedical Data Science")
COMMAND = "evals run --subject chen-yang-su"
ROWS = [  # (call, result) printed by the trace; a tuple result wraps onto extra lines
    ("focus()", "AI agents for science · outcome-graded evals"),
    ("domain()", "human genetics · proteomics · drug targets"),
    ("writing()", "essays on luck, rejection and ambition"),
    ("training()", "PhD & MSc, McGill · RL at Mila"),
    ("path()", ("Kaohsiung → Arlington → Bellevue → Victoria", "→ Vancouver → Montréal → Palo Alto")),
]
VERDICT = f"{len(ROWS)}/{len(ROWS)} checks · graded on end state"


def lines(result):
    return (result,) if isinstance(result, str) else result


# typed at the cursor once the trace has finished, one after another, forever
QUOTES = [  # Silicon Valley founders, each with a documented source
    ("Make something people want.", "Paul Graham"),
    ("Stay hungry. Stay foolish.", "Steve Jobs"),
    ("It's time to build.", "Marc Andreessen"),
    ("Do things that don't scale.", "Paul Graham"),
    ("The biggest risk is not taking any risk.", "Mark Zuckerberg"),
    ("Real artists ship.", "Steve Jobs"),
    ("Only the paranoid survive.", "Andy Grove"),
    ("Live in the future, then build what's missing.", "Paul Graham"),
    ("Competition is for losers.", "Peter Thiel"),
]
QUOTE_START = 3.6  # seconds, once the PASS line is in
TYPE, HOLD, ERASE, GAP = 0.05, 2.8, 0.016, 0.5  # per character, pause, per character, pause


def quote_loop(s, x, baselines, size, cursor, one_line):
    """Type, hold and erase each quote at the cursor, looping forever. Uses SMIL (<animate>), which
    GitHub's image viewer runs: each character sits at a fixed x, and a clip rectangle widens one
    character at a time, so font hinting at small sizes cannot shift or hide characters.
    one_line: "quote — author" at baselines[0]; otherwise the author goes on a second line.
    cursor: (width, height, rise above the baseline)."""
    cw = width("M", "Plex Mono", "400", size)
    quotes = [[f"{q} — {a}"] if one_line else [q, f"— {a}"] for q, a in QUOTES]

    # frames: (time, quote index, characters shown on each line); each holds until the next
    frames, t = [(0.0, None, ())], 0.0
    for i, ls in enumerate(quotes):
        def shown(k):
            out = []
            for line in ls:
                out.append(min(k, len(line)))
                k -= out[-1]
            return tuple(out)
        n = sum(map(len, ls))
        frames += [(t + k * TYPE, i, shown(k)) for k in range(1, n + 1)]
        t += n * TYPE + HOLD
        frames += [(t + (n - k) * ERASE, i, shown(k)) for k in range(n - 1, -1, -1)]
        t += n * ERASE + GAP
    T = t

    def animate(attr, series):
        """series: [(time, value)]; keep only the frames where the value changes."""
        kept = [series[0]] + [b for a, b in zip(series, series[1:]) if b[1] != a[1]]
        return (f'<animate attributeName="{attr}" calcMode="discrete" begin="{QUOTE_START}s" dur="{T:.3f}s" '
                f'repeatCount="indefinite" keyTimes="{";".join(f"{tt / T:.5f}" for tt, _ in kept)}" '
                f'values="{";".join(str(v) for _, v in kept)}"/>')

    s.add('<g class="q">')
    for i, ls in enumerate(quotes):
        for j, line in enumerate(ls):
            cid = f"q{i}_{j}"
            series = [(tt, f"{(c[j] if qi == i else 0) * cw:.1f}") for tt, qi, c in frames]
            s.add(f'<clipPath id="{cid}"><rect x="{x}" y="{baselines[j] - size}" width="0" height="{size * 1.5}">'
                  f'{animate("width", series)}</rect></clipPath>')
            # quote in ink, author muted; on one line the author follows " — "
            parts = line.split(" — ") if one_line else [line]
            k = 0
            for n, part in enumerate(parts):
                text = (" — " if n else "") + part
                muted = n > 0 or text.startswith("— ")
                xs = " ".join(f"{x + (k + m) * cw:.1f}" for m in range(len(text)))
                s.chars("Plex Mono", "400", text)
                s.add(f'<text x="{xs}" y="{baselines[j]}" font-family="&apos;Plex Mono&apos;" font-weight="400" '
                      f'font-size="{size}" fill="{MUTED if muted else INK}" clip-path="url(#{cid})" xml:space="preserve">'
                      f'{html.escape(text)}</text>')
                k += len(text)
            assert x + len(line) * cw <= s.w - 18, f"quote too wide for the card: {line}"
    # the cursor rides at the end of the text being typed
    cwid, chgt, rise = cursor

    def at(c):
        active = max([j for j, k in enumerate(c) if k] or [0])
        return x + (c[active] if c else 0) * cw, baselines[active] - rise
    xs = [(tt, f"{at(c)[0]:.1f}") for tt, _, c in frames]
    ys = [(tt, f"{at(c)[1]:.1f}") for tt, _, c in frames]
    s.add(f'<rect class="cur" x="{x}" y="{baselines[0] - rise}" width="{cwid}" height="{chgt}" fill="{INK2}">'
          f'{animate("x", xs)}{animate("y", ys)}</rect>')
    s.add("</g>")
    # reduced motion: no typing, just the resting cursor
    s.add(f'<rect class="rm" x="{x}" y="{baselines[0] - rise}" width="{cwid}" height="{chgt}" fill="{INK2}"/>')

LINKS = {  # button -> its colour; order is the order in the README
    "website": "#39c5cf",
    "blog": GOLD,
    "linkedin": "#4c8dff",
    "x": INK,
    "bluesky": "#5cc8ff",
    "email": GREEN,
}

def hero():
    s = Svg(1000, 400, "Chen-Yang Su (蘇震洋). Evals, agents, AI for science. Postdoctoral Scholar, Stanford "
                       "Biomedical Data Science. Drawn as an agent evaluation trace over his profile, then the cursor "
                       "types short motivational quotes.")
    s.css.append(TRACE_CSS)
    s.add(f'<rect x="0.5" y="0.5" width="999" height="399" rx="12" fill="{BG}" stroke="{LINE}"/>')
    s.add(f'<path d="M12.5 .5h975a12 12 0 0 1 12 12v27.5H.5V12.5a12 12 0 0 1 12-12z" fill="{BAR}"/>')
    s.add(f'<rect x="1" y="40" width="998" height="1" fill="{LINE}"/>')
    s.text(24, 25, "~/chenyangsu", "Plex Mono", "500", 13, INK2)
    s.text(976, 25, "trial 1 of 1", "Plex Mono", "400", 13, MUTED, anchor="end")

    # identity, left
    fam, wt, tr = NAME_FONT
    name_size = min(52, 52 * 350 / width(NAME, fam, wt, 52, tr))  # wide faces shrink to stay left of the divider
    s.text(40, 158, NAME, fam, wt, round(name_size, 1), INK, tracking=tr)
    s.text(42, 200, NAME_TC, *NAME_TC_FONT, 26, MUTED)
    s.text(42, 242, TAGLINE, "Plex Mono", "500", 15, BLUE)
    s.text(42, 282, ROLE[0], "Lato", "400", 15.5, INK2)
    s.text(42, 305, ROLE[1], "Lato", "400", 15.5, INK2)
    s.add(f'<rect x="420" y="72" width="1" height="296" fill="{LINE}"/>')

    # trace, right: lines fade in one after another
    x0, y, step, wrap_h, size = 452, 96, 34, 21, 14
    xr = x0 + 18 + max(width(c, "Plex Mono", "500", size) for c, _ in ROWS) + 22
    right = max(xr + width(t, "Plex Mono", "400", size) for _, r in ROWS for t in lines(r))
    assert right <= 972, f"trace overflows the card: right edge {right:.0f}px"

    s.add('<g class="l" style="animation-delay:.2s">')
    w = s.text(x0, y, "$", "Plex Mono", "600", size, GREEN)
    s.text(x0 + w + 10, y, COMMAND, "Plex Mono", "400", size, INK)
    s.add("</g>")
    yy = y + 2
    for i, (call, result) in enumerate(ROWS):
        yy += step
        s.add(f'<g class="l" style="animation-delay:{0.7 + i * 0.45:.2f}s">')
        s.add(f'<circle cx="{x0 + 4.5}" cy="{yy - 4.5}" r="4" fill="{GOLD}"/>')
        s.text(x0 + 18, yy, call, "Plex Mono", "500", size, BLUE)
        for j, t in enumerate(lines(result)):
            s.text(xr, yy + j * wrap_h, t, "Plex Mono", "400", size, INK2)
        s.add("</g>")
        yy += (len(lines(result)) - 1) * wrap_h
    yy += step + 14
    assert yy + 22 + 18 <= 392, f"trace runs off the bottom of the card: {yy}"
    s.add(f'<g class="l" style="animation-delay:{0.9 + len(ROWS) * 0.45:.2f}s">')
    s.add(f'<rect x="{x0}" y="{yy - 17}" width="56" height="25" rx="4" fill="#12301c"/>')
    s.text(x0 + 28, yy, "PASS", "Plex Mono", "600", size, GREEN, anchor="middle")
    s.text(x0 + 70, yy, VERDICT, "Plex Mono", "400", size, MUTED)
    s.add("</g>")
    quote_loop(s, x0, [yy + 36], size, (9, 18, 14), one_line=True)
    (ASSETS / "hero.svg").write_text(s.render())


TRACE_CSS = (".l{opacity:0;animation:in .35s ease-out forwards}"
             "@keyframes in{from{opacity:0;transform:translateX(-6px)}to{opacity:1;transform:none}}"
             ".cur{animation:blink 1.1s steps(1) infinite}@keyframes blink{50%{opacity:0}}"
             ".rm{display:none}"
             "@media (prefers-reduced-motion:reduce){.l{animation:none;opacity:1}.q{display:none}.rm{display:inline}}")


def hero_mobile():
    """Portrait hero for phone widths: identity on top, each trace result under its call."""
    W, PAD, size = 380, 20, 12.5
    rows_h = sum(46 + 19 * (len(lines(r)) - 1) for _, r in ROWS)
    H = 262 + rows_h + 100
    s = Svg(W, H, "Chen-Yang Su (蘇震洋). Evals, agents, AI for science. Postdoctoral Scholar, Stanford "
                  "Biomedical Data Science. Drawn as an agent evaluation trace over his profile, then the cursor "
                       "types short motivational quotes.")
    s.css.append(TRACE_CSS)
    s.add(f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="12" fill="{BG}" stroke="{LINE}"/>')
    s.add(f'<path d="M12.5 .5h{W - 25}a12 12 0 0 1 12 12v23.5H.5V12.5a12 12 0 0 1 12-12z" fill="{BAR}"/>')
    s.add(f'<rect x="1" y="36" width="{W - 2}" height="1" fill="{LINE}"/>')
    s.text(PAD, 23, "~/chenyangsu", "Plex Mono", "500", 12, INK2)
    s.text(W - PAD, 23, "trial 1 of 1", "Plex Mono", "400", 12, MUTED, anchor="end")
    fam, wt, tr = NAME_FONT
    name_size = min(38, 38 * 262 / width(NAME, fam, wt, 38, tr))
    w = s.text(PAD - 1, 92, NAME, fam, wt, round(name_size, 1), INK, tracking=tr)
    s.text(PAD + w + 10, 91, NAME_TC, *NAME_TC_FONT, 20, MUTED)
    s.text(PAD, 124, TAGLINE, "Plex Mono", "500", 13.5, BLUE)
    s.text(PAD, 154, ROLE[0], "Lato", "400", 14.5, INK2)
    s.text(PAD, 175, ROLE[1], "Lato", "400", 14.5, INK2)
    s.add(f'<rect x="{PAD}" y="198" width="{W - 2 * PAD}" height="1" fill="{LINE}"/>')
    y = 232
    s.add('<g class="l" style="animation-delay:.2s">')
    w = s.text(PAD, y, "$", "Plex Mono", "600", size, GREEN)
    s.text(PAD + w + 8, y, COMMAND, "Plex Mono", "400", size, INK)
    s.add("</g>")
    yy = y + 30
    for i, (call, result) in enumerate(ROWS):
        s.add(f'<g class="l" style="animation-delay:{0.7 + i * 0.45:.2f}s">')
        s.add(f'<circle cx="{PAD + 4}" cy="{yy - 4}" r="3.5" fill="{GOLD}"/>')
        s.text(PAD + 16, yy, call, "Plex Mono", "500", size, BLUE)
        for j, t in enumerate(lines(result)):
            rw = s.text(PAD + 16, yy + 19 * (j + 1), t, "Plex Mono", "400", 12, INK2)
            assert PAD + 16 + rw <= W - PAD + 4, f"mobile trace overflows: {t}"
        s.add("</g>")
        yy += 46 + 19 * (len(lines(result)) - 1)
    yy += 4
    s.add(f'<g class="l" style="animation-delay:{0.9 + len(ROWS) * 0.45:.2f}s">')
    s.add(f'<rect x="{PAD}" y="{yy - 16}" width="50" height="23" rx="4" fill="#12301c"/>')
    s.text(PAD + 25, yy, "PASS", "Plex Mono", "600", size, GREEN, anchor="middle")
    s.text(PAD + 62, yy, VERDICT, "Plex Mono", "400", 12, MUTED)
    s.add("</g>")
    quote_loop(s, PAD, [yy + 31, yy + 50], 11.5, (8, 16, 12), one_line=False)
    (ASSETS / "hero-mobile.svg").write_text(s.render())


def link_button(name, colour):
    """A CLI flag drawn as a button, e.g. --blog, with its own colour and icon."""
    size, h, icon = 14, 32, 15
    w = 11 + icon + 8 + width("--" + name, "Plex Mono", "500", size) + 13
    s = Svg(round(w), h, name)
    s.add(f'<rect x="0.5" y="0.5" width="{round(w) - 1}" height="{h - 1}" rx="6" fill="{BG}"/>')
    s.add(f'<rect x="0.5" y="0.5" width="{round(w) - 1}" height="{h - 1}" rx="6" fill="{colour}" '
          f'fill-opacity=".08" stroke="{colour}" stroke-opacity=".55"/>')
    # icon, drawn from 24x24 artwork scaled to `icon` px
    k = icon / 24
    t = f'translate(11 {(h - icon) / 2}) scale({k:.4f})'
    if name in icons.FILLED:
        s.add(f'<path transform="{t}" d="{icons.FILLED[name]}" fill="{colour}"/>')
    elif name in icons.STROKED:
        s.add(f'<g transform="{t}" fill="none" stroke="{colour}" stroke-width="2.2" stroke-linecap="round" '
              f'stroke-linejoin="round">{icons.STROKED[name]}</g>')
    else:  # linkedin: an "in" badge
        s.add(f'<rect x="11" y="{(h - icon) / 2}" width="{icon}" height="{icon}" rx="3" fill="{colour}"/>')
        s.text(11 + icon / 2, h / 2 + 4, "in", "Geist", "700", 10.5, BG, anchor="middle")
    x = 11 + icon + 8
    dash = s.text(x, 21, "--", "Plex Mono", "500", size, MUTED)
    s.text(x + dash, 21, name, "Plex Mono", "500", size, colour)
    (ASSETS / "links" / f"{name}.svg").write_text(s.render())


if __name__ == "__main__":
    (ASSETS / "links").mkdir(parents=True, exist_ok=True)
    hero()
    hero_mobile()
    for name, colour in LINKS.items():
        link_button(name, colour)
    for f in sorted(ASSETS.rglob("*.svg")):
        print(f"{f.relative_to(ASSETS.parent)}  {f.stat().st_size / 1024:.1f} KB")
