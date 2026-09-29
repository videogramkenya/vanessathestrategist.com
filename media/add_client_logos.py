"""Swap the client names under the numbers for the brands' real logos.

The logos were found on each brand's own website or public profile (media/logos/logos.csv says
where each came from). Nothing is redrawn or recoloured. A brand with no logo yet, or where the
logo found may belong to a different business, keeps its name in her display font instead.
Web-sized copies go to clients/ so the page does not load 2,700px files.

    python media/add_client_logos.py
"""
import csv, io, re, shutil
from pathlib import Path
from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parents[1]
SRC, OUT = ROOT / "media" / "logos", ROOT / "clients"
INDEX = ROOT / "index.html"

# name only until Vanessa confirms: the logo found is a different business with the same name
NAME_ONLY = {"Welcome Home", "Winny Imports"}
# white or gold logos on a see-through background: they need a dark tile to show at all
DARK = {"Insmile Aesthetics", "Pritt Events", "Game Nights 254", "Imports by Rigi"}

GROUPS = [
    ("Real estate", ["IHS Kenya", "Welcome Home"]),
    ("Beauty &amp; wellness", ["Beauty Square", "Maya's Salon", "Carey Beauty College", "Joannak Cosmetics",
                               "Insmile Aesthetics", "Fahma Aesthetics", "Lerisque Africa"]),
    ("Fashion &amp; lifestyle", ["The Lip Tribe", "Jesus Girl Closet", "Bouchic", "Artistry by Njanja",
                                 "Glam by Julie", "Wan Styling"]),
    ("Automotive", ["Imports by Rigi", "Yohana Motors", "Black Carbon", "Winny Imports"]),
    ("Technology", ["Computer Pride", "Mophones", "Foresight Tech Group", "PTS Africa"]),
    ("Finance &amp; professional", ["ICPAK", "Binance", "Centonomy", "Fermentis"]),
    ("Education", ["Kenya School of Sales"]),
    ("Travel &amp; tourism", ["Safirii", "Savi Tours"]),
    ("Events &amp; entertainment", ["Pritt Events", "Glam Events Kenya", "Game Nights 254"]),
    ("Media &amp; content", ["Create with Ayan"]),
    ("Home &amp; interiors", ["Tanj Curtains"]),
]

files = {r["brand"]: r["file"] for r in csv.DictReader(io.open(SRC / "logos.csv", encoding="utf-8")) if r["file"]}


def trim(im, bg=(255, 255, 255)):
    """Cut the empty margin round a logo so it fills its tile: see-through edges, or plain white ones."""
    if im.mode == "RGBA":
        box = im.getchannel("A").point(lambda a: 255 if a > 8 else 0).getbbox()
    else:
        plain = Image.new("RGB", im.size, bg)
        box = ImageChops.difference(im, plain).convert("L").point(lambda v: 255 if v > 18 else 0).getbbox()
    return im.crop(box) if box else im


def edge_colour(im):
    """The logo's own background colour, if its four corners share one that is not white."""
    if im.mode != "RGB":
        return None
    w, h = im.size
    dx, dy = max(2, w // 16), max(2, h // 16)          # a little way in, past any thin frame
    px = [im.getpixel(c) for c in ((dx, dy), (w - dx, dy), (dx, h - dy), (w - dx, h - dy))]
    avg = tuple(sum(c[i] for c in px) // 4 for i in range(3))
    if max(abs(c[i] - avg[i]) for c in px for i in range(3)) > 24 or min(avg) > 235:
        return None
    return "#%02x%02x%02x" % avg


def web_copy(brand):
    src = SRC / files[brand]
    OUT.mkdir(exist_ok=True)
    if src.suffix == ".svg":
        shutil.copy(src, OUT / src.name)
        return "clients/" + src.name, None
    im = Image.open(src)
    im = im.convert("RGBA") if im.mode in ("RGBA", "LA", "P") else im.convert("RGB")
    if im.mode == "RGBA" and im.getchannel("A").getextrema()[0] == 255:
        im = im.convert("RGB")                       # fully opaque: treat as a flat image
    solid = edge_colour(im)
    if solid:
        # cut the logo's own empty background down to the mark; the tile carries that colour instead
        rgb = tuple(int(solid[i:i + 2], 16) for i in (1, 3, 5))
        w, h = im.size
        if max(abs(a - b) for a, b in zip(im.getpixel((1, 1)), rgb)) > 24:
            im = im.crop((w // 16, h // 16, w - w // 16, h - h // 16))   # a thin frame of another colour
        im = trim(im, rgb)
    else:
        im = trim(im)
    im.thumbnail((440, 176))                         # twice the tile size, sharp on phones
    name = src.stem + ".png" if im.mode == "RGBA" else src.stem + ".jpg"
    if im.mode == "RGBA":
        im.save(OUT / name, optimize=True)
    else:
        im.save(OUT / name, quality=88, optimize=True)
    return "clients/" + name, solid


def esc(t):
    return t.replace("&", "&amp;").replace("'", "&rsquo;").replace("&amp;amp;", "&amp;")


tiles_total = logos = 0
rows = []
for industry, brands in GROUPS:
    tiles = []
    for b in brands:
        tiles_total += 1
        label = esc(b)
        if b in files and b not in NAME_ONLY:
            logos += 1
            path, solid = web_copy(b)
            cls = "clogo dark" if b in DARK else "clogo solid" if solid else "clogo"
            style = ' style="background:%s;border-color:%s"' % (solid, solid) if solid else ""
            tiles.append('<li class="%s"%s><img src="%s" alt="%s" title="%s" loading="lazy" decoding="async"></li>'
                         % (cls, style, path, label, label))
        else:
            tiles.append('<li class="clogo cname">%s</li>' % label)
    rows.append('    <div class="cgroup"><p class="cind">%s</p><ul class="clogos">%s</ul></div>'
                % (industry, "".join(tiles)))

s = io.open(INDEX, encoding="utf-8").read()
m = re.search(r'(<div class="clients">\n)(.*?)(\n  </div>\n </div>\n</section>)', s, re.S)
assert m, "client block not found"
s = s[:m.start(2)] + "\n".join(rows) + s[m.end(2):]

CSS = """
/* the client names become their logos, 29 Sep 2026 */
.clogos{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:.6rem}
.clogo{width:150px;height:84px;display:flex;align-items:center;justify-content:center;padding:12px 16px;background:var(--paper);border:1px solid var(--rule);border-radius:10px}
.clogo img{max-width:100%;max-height:100%;width:auto;height:auto;object-fit:contain;display:block}
.clogo.dark{background:var(--ink);border-color:var(--ink)}
.clogo.solid{padding:10px 14px}
.clogo.cname{font-family:var(--dsp);font-weight:600;font-size:.95rem;letter-spacing:-.01em;line-height:1.2;color:var(--ink2);text-align:center;background:var(--wash)}
@media(max-width:760px){.clogos{gap:.5rem}.clogo{width:calc(50% - .25rem);height:76px}}
"""
if "/* the client names become their logos" not in s:
    end = s.find("</style>")
    s = s[:end] + CSS + s[end:]

io.open(INDEX, "w", encoding="utf-8", newline="").write(s)
print("%d brands: %d as logos, %d as names" % (tiles_total, logos, tiles_total - logos))
