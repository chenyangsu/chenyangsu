"""Helpers for hand-built SVGs: fetch fonts, subset and embed them, measure text."""
import base64
import html
import io
import re
import urllib.parse
import urllib.request
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont

FONT_DIR = Path(__file__).parent / ".fonts"

# SVG family name -> weight -> Google Fonts css2 family spec. All are SIL Open Font License.
FACES = {
    "Serif Display": {"700": "Source+Serif+4:opsz,wght@60,700"},
    "Serif TC": {"500": "Noto+Serif+TC:wght@500"},
    "Lato": {"400": "Lato:wght@400"},
    "Plex Mono": {"400": "IBM+Plex+Mono:wght@400", "500": "IBM+Plex+Mono:wght@500", "600": "IBM+Plex+Mono:wght@600"},
}
_cache = {}


def _path(family, weight):
    return FONT_DIR / f"{family.replace(' ', '')}-{weight}.ttf"


def _font(family, weight):
    p = _path(family, weight)
    if not p.exists():
        FONT_DIR.mkdir(exist_ok=True)
        spec = FACES[family][weight]
        if family == "Serif TC":  # the full CJK font is ~10 MB; ask Google for the three glyphs we draw
            spec += "&text=" + urllib.parse.quote("蘇震洋")
        css = urllib.request.urlopen(f"https://fonts.googleapis.com/css2?family={spec}").read().decode()
        url = re.search(r"url\((https://[^)]+)\)", css).group(1)
        p.write_bytes(urllib.request.urlopen(url).read())
    if p not in _cache:
        _cache[p] = TTFont(p)
    return _cache[p]


def width(text, family, weight, size, tracking=0.0):
    """Advance width of `text` in px (kerning ignored), plus letter-spacing per glyph."""
    font = _font(family, weight)
    cmap, hmtx, upem = font.getBestCmap(), font["hmtx"], font["head"].unitsPerEm
    missing = [ch for ch in text if ord(ch) not in cmap]
    if missing:
        raise ValueError(f"{family} {weight} has no glyph for {missing!r}")
    return sum(hmtx[cmap[ord(ch)]][0] for ch in text) * size / upem + tracking * len(text)


class Svg:
    """Collects elements and the characters drawn in each face; render() embeds only those glyphs."""

    def __init__(self, w, h, label):
        self.w, self.h, self.label = w, h, label
        self.parts, self.css = [], []
        self.used = {}

    def add(self, s):
        self.parts.append(s)

    def text(self, x, y, s, family, weight, size, fill, anchor="start", tracking=0.0):
        self.used.setdefault((family, weight), set()).update(s)
        ls = f' letter-spacing="{tracking}"' if tracking else ""
        # quoted family name: an unquoted "Serif ..." is parsed as the generic serif keyword
        self.add(f'<text x="{x:.1f}" y="{y:.1f}" font-family="&apos;{family}&apos;" font-weight="{weight}" '
                 f'font-size="{size}" fill="{fill}" text-anchor="{anchor}"{ls}>{html.escape(s)}</text>')
        return width(s, family, weight, size, tracking)

    def _fontfaces(self):
        rules = []
        for (family, weight), chars in sorted(self.used.items()):
            font = TTFont(_path(family, weight), recalcTimestamp=False)
            opts = subset.Options()
            opts.flavor = "woff"
            opts.name_IDs = []
            sub = subset.Subsetter(opts)
            sub.populate(text="".join(chars | {" "}))
            sub.subset(font)
            buf = io.BytesIO()
            font.save(buf)
            b64 = base64.b64encode(buf.getvalue()).decode()
            rules.append(f"@font-face{{font-family:'{family}';font-weight:{weight};"
                         f"src:url(data:font/woff;base64,{b64}) format('woff')}}")
        return "\n".join(rules)

    def render(self):
        label = html.escape(self.label)
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" width="{self.w}" '
                f'height="{self.h}" role="img" aria-label="{label}">\n<title>{label}</title>\n'
                f"<style>\n{self._fontfaces()}\n{''.join(self.css)}\n</style>\n" + "\n".join(self.parts) + "\n</svg>\n")
