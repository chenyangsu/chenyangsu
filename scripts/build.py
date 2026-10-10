"""Draw the profile hero and link buttons into assets/. Run: python3 scripts/build.py (needs fonttools).

Every fact drawn here is taken from chenyangsu.github.io; edit ROWS or LINKS, rerun, commit the SVGs.
"""
from pathlib import Path

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
ROWS = [  # (call, result) printed by the trace, one per line
    ("focus()", "AI agents for science · outcome-graded evals"),
    ("domain()", "human genetics · proteomics · drug targets"),
    ("writing()", "essays on luck, rejection and ambition"),
    ("training()", "PhD & MSc, McGill · RL at Mila"),
    ("path()", "Kaohsiung → Vancouver → Montréal → Palo Alto"),
]
VERDICT = f"{len(ROWS)}/{len(ROWS)} checks · graded on end state"

LINKS = ["website", "blog", "linkedin", "x", "bluesky", "email"]

def hero():
    s = Svg(1000, 400, "Chen-Yang Su (蘇震洋). Evals, agents, AI for science. Postdoctoral Scholar, Stanford "
                       "Biomedical Data Science. Drawn as an agent evaluation trace over his profile.")
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
    x0, y, step, size = 452, 96, 36, 14
    xr = x0 + 18 + max(width(c, "Plex Mono", "500", size) for c, _ in ROWS) + 22
    right = max(xr + width(r, "Plex Mono", "400", size) for _, r in ROWS)
    assert right <= 972, f"trace overflows the card: right edge {right:.0f}px"

    s.add('<g class="l" style="animation-delay:.2s">')
    w = s.text(x0, y, "$", "Plex Mono", "600", size, GREEN)
    s.text(x0 + w + 10, y, COMMAND, "Plex Mono", "400", size, INK)
    s.add("</g>")
    for i, (call, result) in enumerate(ROWS):
        yy = y + (i + 1) * step + 2
        s.add(f'<g class="l" style="animation-delay:{0.7 + i * 0.45:.2f}s">')
        s.add(f'<circle cx="{x0 + 4.5}" cy="{yy - 4.5}" r="4" fill="{GOLD}"/>')
        s.text(x0 + 18, yy, call, "Plex Mono", "500", size, BLUE)
        s.text(xr, yy, result, "Plex Mono", "400", size, INK2)
        s.add("</g>")
    yy = y + (len(ROWS) + 1) * step + 16
    s.add(f'<g class="l" style="animation-delay:{0.9 + len(ROWS) * 0.45:.2f}s">')
    s.add(f'<rect x="{x0}" y="{yy - 17}" width="56" height="25" rx="4" fill="#12301c"/>')
    s.text(x0 + 28, yy, "PASS", "Plex Mono", "600", size, GREEN, anchor="middle")
    s.text(x0 + 70, yy, VERDICT, "Plex Mono", "400", size, MUTED)
    s.add("</g>")
    s.add(f'<rect class="cur" x="{x0}" y="{yy + 22}" width="9" height="18" fill="{INK2}"/>')
    (ASSETS / "hero.svg").write_text(s.render())


TRACE_CSS = (".l{opacity:0;animation:in .35s ease-out forwards}"
             "@keyframes in{from{opacity:0;transform:translateX(-6px)}to{opacity:1;transform:none}}"
             ".cur{animation:blink 1.1s steps(1) infinite}@keyframes blink{50%{opacity:0}}"
             "@media (prefers-reduced-motion:reduce){.l{animation:none;opacity:1}.cur{animation:none}}")


def hero_mobile():
    """Portrait hero for phone widths: identity on top, each trace result under its call."""
    W, PAD, size = 380, 20, 12.5
    rows_h = len(ROWS) * 46
    H = 262 + rows_h + 78
    s = Svg(W, H, "Chen-Yang Su (蘇震洋). Evals, agents, AI for science. Postdoctoral Scholar, Stanford "
                  "Biomedical Data Science. Drawn as an agent evaluation trace over his profile.")
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
    for i, (call, result) in enumerate(ROWS):
        yy = y + 30 + i * 46
        s.add(f'<g class="l" style="animation-delay:{0.7 + i * 0.45:.2f}s">')
        s.add(f'<circle cx="{PAD + 4}" cy="{yy - 4}" r="3.5" fill="{GOLD}"/>')
        s.text(PAD + 16, yy, call, "Plex Mono", "500", size, BLUE)
        rw = s.text(PAD + 16, yy + 19, result, "Plex Mono", "400", 12, INK2)
        assert PAD + 16 + rw <= W - PAD + 4, f"mobile trace overflows: {result}"
        s.add("</g>")
    yy = y + 30 + len(ROWS) * 46 + 4
    s.add(f'<g class="l" style="animation-delay:{0.9 + len(ROWS) * 0.45:.2f}s">')
    s.add(f'<rect x="{PAD}" y="{yy - 16}" width="50" height="23" rx="4" fill="#12301c"/>')
    s.text(PAD + 25, yy, "PASS", "Plex Mono", "600", size, GREEN, anchor="middle")
    s.text(PAD + 62, yy, VERDICT, "Plex Mono", "400", 12, MUTED)
    s.add("</g>")
    s.add(f'<rect class="cur" x="{PAD}" y="{yy + 18}" width="8" height="16" fill="{INK2}"/>')
    (ASSETS / "hero-mobile.svg").write_text(s.render())


def link_button(name):
    """A CLI flag drawn as a button, e.g. --scholar; matches the hero's card."""
    size, pad, h = 14, 13, 32
    w = pad * 2 + width("--" + name, "Plex Mono", "500", size)
    s = Svg(round(w), h, name)
    s.add(f'<rect x="0.5" y="0.5" width="{round(w) - 1}" height="{h - 1}" rx="6" fill="{BG}" stroke="#30363d"/>')
    dash = s.text(pad, 21, "--", "Plex Mono", "500", size, MUTED)
    s.text(pad + dash, 21, name, "Plex Mono", "500", size, INK2)
    (ASSETS / "links" / f"{name}.svg").write_text(s.render())


if __name__ == "__main__":
    (ASSETS / "links").mkdir(parents=True, exist_ok=True)
    hero()
    hero_mobile()
    for name in LINKS:
        link_button(name)
    for f in sorted(ASSETS.rglob("*.svg")):
        print(f"{f.relative_to(ASSETS.parent)}  {f.stat().st_size / 1024:.1f} KB")
