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
    ("stack()", "Python · R · PyTorch · vLLM · Claude API"),
    ("training()", "PhD & MSc, McGill · RL at Mila"),
    ("path()", "Kaohsiung → Vancouver → Montréal → Stanford"),
]
VERDICT = f"{len(ROWS)}/{len(ROWS)} checks · graded on end state"

LINKS = ["website", "blog", "scholar", "orcid", "linkedin", "x", "bluesky"]

# The three class cards: (tag, title, class, colour, sprite, flavour text, abilities)
CLASSES = [
    ("MAIN CLASS", "Agents & Evals", "Artificer", BLUE, "robot",
     "Builds agents that query databases, read papers and act in clinical records.",
     ["Tool-calling agents", "Outcome-graded evals", "Bootstrapped CIs"]),
    ("SUBCLASS", "Human Genetics", "Alchemist", GREEN, "helix",
     "Turns GWAS and plasma proteomics into ranked drug targets.",
     ["Mendelian randomization", "Colocalization", "Multi-ancestry pQTL"]),
    ("SIDE QUEST", "Teaching & Service", "Sage", GOLD, "book",
     "Teaches AI for multi-omics data and Mendelian randomization workshops.",
     ["Lectures & workshops", "Peer review", "Open teaching notebooks"]),
]

# 16x16 pixel sprites; one character per pixel, "." is empty
SPRITES = {
    "robot": [
        "......kyyk......",
        "......kyyk......",
        ".......kk.......",
        "..kkkkkkkkkkkk..",
        ".kbbbbbbbbbbbbk.",
        "kbbkkkkkkkkkkbbk",
        "kbbkddddddddkbbk",
        "kBbkdccddccdkbBk",
        "kBbkdccddccdkbBk",
        "kbbkddddddddkbbk",
        "kbbkkkkkkkkkkbbk",
        ".kbbbbbbbbbbbbk.",
        ".kbbbwwwwwwbbbk.",
        "..kBBBBBBBBBBk..",
        "...kkkkkkkkkk...",
        "....kk....kk....",
    ],
    "book": [
        "................",
        "................",
        ".kkkkk....kkkkk.",
        "kwwwwwkkkkwwwwwk",
        "kwllllwkkwllllwk",
        "kwwwwwwkkwwwwwwk",
        "kwlllwwkkwllllwk",
        "kwwwwwwkkwwwwwwk",
        "kwllllwkkwlllwwk",
        "kwwwwwwkkwwwwwwk",
        "kwlllwwkkwllllwk",
        "kwwwwwwkkwwwwwwk",
        "kooooookkooroook",
        ".kkkkkkkkkkrkkk.",
        "...........r....",
        "..........r.r...",
    ],
}
PIXEL = {"k": "#05080c", "y": GOLD, "b": BLUE, "B": "#3b78c9", "d": "#0b1a2e", "c": "#7ee8ff", "w": "#f0f3f6",
         "l": "#9aa7b6", "o": "#b7791f", "r": "#ff6b6b", "g": GREEN, "G": "#2f9e44", "p": "#ff8fb1", "P": "#c4547a"}


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


def helix():
    """A 16x16 DNA double helix: two 2-px strands, gold/cyan base pairs across each lobe."""
    a = [7, 9, 11, 12, 12, 11, 9, 7, 5, 3, 2, 2, 3, 5, 7, 9]  # left edge of strand g per row
    grid = [["."] * 16 for _ in range(16)]
    for y, xa in enumerate(a):
        xb = 14 - xa
        if y in (2, 5, 9, 12):
            lo, hi = min(xa, xb) + 2, max(xa, xb)
            for x in range(lo, hi):
                grid[y][x] = "y" if x < (lo + hi) / 2 else "c"
        # at each crossing the strands take turns being in front
        order = (("p", xb), ("g", xa)) if y in (6, 7, 8) else (("g", xa), ("p", xb))
        for c, x in order:
            grid[y][x] = grid[y][x + 1] = c
    return ["".join(r) for r in grid]


def sprite(s, x, y, rows, px):
    """Draw a pixel sprite, merging horizontal runs of one colour into single rects."""
    for j, row in enumerate(rows):
        i = 0
        while i < len(row):
            c = row[i]
            n = 1
            while i + n < len(row) and row[i + n] == c:
                n += 1
            if c != ".":
                s.add(f'<rect x="{x + i * px}" y="{y + j * px}" width="{n * px}" height="{px}" fill="{PIXEL[c]}"/>')
            i += n


def wrap(text, family, weight, size, maxw):
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if cur and width(trial, family, weight, size) > maxw:
            lines.append(cur)
            cur = word
        else:
            cur = trial
    return lines + [cur]


def notched(x, y, w, h, n=6):
    """Rectangle path with stepped pixel corners."""
    return (f"M{x + 2 * n} {y}H{x + w - 2 * n}V{y + n}H{x + w - n}V{y + 2 * n}H{x + w}V{y + h - 2 * n}"
            f"H{x + w - n}V{y + h - n}H{x + w - 2 * n}V{y + h}H{x + 2 * n}V{y + h - n}H{x + n}"
            f"V{y + h - 2 * n}H{x}V{y + 2 * n}H{x + n}V{y + n}H{x + 2 * n}Z")


def sparkle(s, x, y, px, colour):
    s.add(f'<rect x="{x - px / 2}" y="{y - 1.5 * px}" width="{px}" height="{3 * px}" fill="{colour}"/>')
    s.add(f'<rect x="{x - 1.5 * px}" y="{y - px / 2}" width="{3 * px}" height="{px}" fill="{colour}"/>')


def party():
    W, H, GAP, SHADOW = 306, 478, 31, 6
    s = Svg(1000, H + SHADOW + 2, "Three character classes: main class Agents and Evals (Artificer), subclass Human "
                                  "Genetics (Alchemist), side quest Teaching and Service (Sage).")
    s.css.append(".bob{animation:bob 2.4s ease-in-out infinite}@keyframes bob{50%{transform:translateY(-5px)}}"
                 ".tw{animation:tw 1.8s steps(2) infinite}@keyframes tw{50%{opacity:.25}}"
                 "@media (prefers-reduced-motion:reduce){.bob,.tw{animation:none}}")
    for k, (tag, title, cls, colour, art, flavour, abilities) in enumerate(CLASSES):
        x = 1 + k * (W + GAP)
        cx = x + W / 2
        s.add(f'<path d="{notched(x + SHADOW, 1 + SHADOW, W, H)}" fill="#000" opacity=".35"/>')
        s.add(f'<path d="{notched(x, 1, W, H)}" fill="#121a24" stroke="{colour}" stroke-width="3"/>')
        s.add(f'<path d="{notched(x + 8, 9, W - 16, H - 16, 4)}" fill="none" stroke="{colour}" stroke-opacity=".3"/>')
        # tag ribbon
        tw = width(tag, "Plex Mono", "600", 13, 1.5) + 24
        s.add(f'<rect x="{cx - tw / 2:.1f}" y="22" width="{tw:.1f}" height="24" fill="{colour}"/>')
        s.text(cx, 39, tag, "Plex Mono", "600", 13, "#0b0f15", anchor="middle", tracking=1.5)
        # sprite on a glow, gently bobbing, with twinkling sparkles
        s.add(f'<circle cx="{cx}" cy="124" r="62" fill="{colour}" opacity=".10"/>')
        s.add(f'<circle cx="{cx}" cy="124" r="44" fill="{colour}" opacity=".10"/>')
        s.add(f'<rect x="{cx - 36}" y="186" width="72" height="6" fill="#000" opacity=".35"/>')
        s.add(f'<g class="bob" style="animation-delay:{k * 0.4}s">')
        sprite(s, cx - 48, 72, helix() if art == "helix" else SPRITES[art], 6)
        s.add("</g>")
        for i, (dx, dy) in enumerate(((-92, 84), (86, 70), (98, 150), (-84, 160))):
            s.add(f'<g class="tw" style="animation-delay:{(i + k) * 0.45:.2f}s">')
            sparkle(s, cx + dx, dy, 3 if i % 2 else 4, colour if i % 2 else "#f0f3f6")
            s.add("</g>")
        # name plate
        s.text(cx, 232, title, "Pixel", "700", 25, INK, anchor="middle")
        s.text(cx, 256, f"class · {cls}", "Plex Mono", "500", 13.5, colour, anchor="middle")
        for i in range(0, W - 48, 10):
            s.add(f'<rect x="{x + 24 + i}" y="272" width="5" height="2" fill="{colour}" opacity=".45"/>')
        # flavour text
        y = 300
        for line in wrap(flavour, "Plex Mono", "400", 13.5, W - 56):
            s.text(x + 24, y, line, "Plex Mono", "400", 13.5, INK2)
            y += 20
        # abilities
        y += 14
        s.text(x + 24, y, "ABILITIES", "Plex Mono", "600", 12, MUTED, tracking=1.5)
        for a in abilities:
            y += 25
            s.add(f'<path d="M{x + 30} {y - 10}l5 5-5 5-5-5z" fill="{colour}"/>')
            aw = s.text(x + 44, y, a, "Plex Mono", "500", 13.5, INK)
            assert 44 + aw <= W - 24, f"ability too wide: {a}"
        assert y <= H - 18, f"{title} card overflows: {y}"
    (ASSETS / "classes.svg").write_text(s.render())


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
    party()
    for name in LINKS:
        link_button(name)
    for f in sorted(ASSETS.rglob("*.svg")):
        print(f"{f.relative_to(ASSETS.parent)}  {f.stat().st_size / 1024:.1f} KB")
