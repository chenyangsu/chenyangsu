"""Draw the profile hero and link buttons into assets/. Run: python3 scripts/build.py (needs fonttools).

Every fact drawn here is taken from chenyangsu.github.io; edit ROWS or LINKS, rerun, commit the SVGs.
"""
from pathlib import Path

from svgkit import Svg, width

ASSETS = Path(__file__).resolve().parent.parent / "assets"

BG, BAR, LINE = "#0b0f15", "#10161e", "#222a35"
INK, INK2, MUTED = "#f0f3f6", "#c9d1d9", "#7d8590"
BLUE, GREEN, GOLD = "#79b0ff", "#56d364", "#e3b341"

COMMAND = "evals run --subject chen-yang-su"
ROWS = [  # (call, result) printed by the trace, one per line
    ("focus()", "AI agents for science · outcome-graded evals"),
    ("domain()", "human genetics · proteomics · drug targets"),
    ("training()", "PhD & MSc, McGill · RL at Mila"),
    ("papers()", "55 · ICLR · NEJM · Nat Genet · Nat Commun"),
    ("path()", "Kaohsiung → Vancouver → Montréal → Stanford"),
]
VERDICT = f"{len(ROWS)}/{len(ROWS)} checks · graded on end state"

LINKS = ["website", "blog", "scholar", "orcid", "linkedin", "x", "bluesky"]


def hero():
    s = Svg(1000, 400, "Chen-Yang Su (蘇震洋). Evals, agents, AI for science. Postdoctoral Scholar, Stanford "
                       "Biomedical Data Science. Drawn as an agent evaluation trace over his profile.")
    s.css.append(
        ".l{opacity:0;animation:in .35s ease-out forwards}"
        "@keyframes in{from{opacity:0;transform:translateX(-6px)}to{opacity:1;transform:none}}"
        ".cur{animation:blink 1.1s steps(1) infinite}@keyframes blink{50%{opacity:0}}"
        "@media (prefers-reduced-motion:reduce){.l{animation:none;opacity:1}.cur{animation:none}}"
    )
    s.add(f'<rect x="0.5" y="0.5" width="999" height="399" rx="12" fill="{BG}" stroke="{LINE}"/>')
    s.add(f'<path d="M12.5 .5h975a12 12 0 0 1 12 12v27.5H.5V12.5a12 12 0 0 1 12-12z" fill="{BAR}"/>')
    s.add(f'<rect x="1" y="40" width="998" height="1" fill="{LINE}"/>')
    s.text(24, 25, "~/chenyangsu", "Plex Mono", "500", 13, INK2)
    s.text(976, 25, "trial 1 of 1", "Plex Mono", "400", 13, MUTED, anchor="end")

    # identity, left
    s.text(40, 128, "Chen-Yang Su", "Serif Display", "700", 52, INK, tracking=-0.5)
    s.text(42, 170, "蘇震洋", "Serif TC", "500", 26, MUTED)
    s.text(42, 212, "Evals · Agents · AI for Science", "Plex Mono", "500", 15, BLUE)
    s.text(42, 252, "Postdoctoral Scholar, Stanford", "Lato", "400", 15.5, INK2)
    s.text(42, 275, "Biomedical Data Science", "Lato", "400", 15.5, INK2)
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
    for name in LINKS:
        link_button(name)
    for f in sorted(ASSETS.rglob("*.svg")):
        print(f"{f.relative_to(ASSETS.parent)}  {f.stat().st_size / 1024:.1f} KB")
