"""Numbers, client names and the testimonials, straight under the hero on the home page.

Vanessa sent a mock-up (vanessa-homepage.html) with the content; her own site's look is kept.
Numbers are the mock-up's, plus "50 corporate teams trained" from the live site (Alex, 29 Sep 2026).
The old "Track record" block further down is replaced, not repeated, and the About page's
line is brought into line with the same numbers.
Client names are set as text in her fonts, not as drawn logos: the mock-up's logos were invented
lookalikes of real companies' marks, which reads as fake to anyone who knows the brand.
The video testimonials already on the page move up to sit after the names.

    python media/add_proofbar.py
"""
import io
from pathlib import Path

INDEX = Path(__file__).resolve().parents[1] / "index.html"
s = io.open(INDEX, encoding="utf-8").read()
assert 'class="clients"' not in s, "already added"

STATS = [("200+", "SME owners trained"), ("50", "corporate teams trained"), ("35+", "brands built"),
         ("50+", "masterclasses delivered"), ("7 yrs", "in live ad accounts"), ("9", "industries served")]
CLIENTS = [
    ("Real estate", ["IHS Kenya", "Welcome Home"]),
    ("Beauty &amp; wellness", ["Beauty Square", "Maya&rsquo;s Salon", "Carey Beauty College", "Joannak Cosmetics",
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


def swap(old, new):
    global s
    assert s.count(old) == 1, "anchor not found once: " + old[:60]
    s = s.replace(old, new)


# 1. styles: her existing numbers strip goes from four to six, and the client list is added
swap(".stats{display:grid;grid-template-columns:repeat(4,1fr);",
     ".stats{display:grid;grid-template-columns:repeat(6,1fr);")
swap(".s1 b{color:var(--mag)}.s2 b{color:var(--blue)}.s3 b{color:var(--tan)}.s4 b{color:var(--green)}",
     ".s1 b{color:var(--mag)}.s2 b{color:var(--blue)}.s3 b{color:var(--tan)}.s4 b{color:var(--green)}"
     ".s5 b{color:var(--mag)}.s6 b{color:var(--blue)}")
CSS = """
/* client names under the numbers, 29 Sep 2026 */
.clients{margin-top:2.6rem}
.cgroup{display:grid;grid-template-columns:minmax(150px,210px) 1fr;gap:1.2rem;padding:1rem 0;border-top:1px solid var(--rule)}
.cgroup:last-child{border-bottom:1px solid var(--rule)}
.cgroup p{margin:0}
.cgroup .cind{font-family:var(--mno);font-size:.66rem;letter-spacing:.16em;text-transform:uppercase;color:var(--faint);padding-top:.35rem}
.cgroup .cnames{font-family:var(--dsp);font-size:clamp(1.02rem,1.5vw,1.2rem);font-weight:600;letter-spacing:-.01em;color:var(--ink);line-height:1.5}
.cgroup .cnames i{font-style:normal;color:var(--rule2);margin:0 .5rem}
@media(max-width:1000px) and (min-width:761px){.stats{grid-template-columns:repeat(3,1fr)}.stat:nth-child(3n){border-right:0}.stat:nth-child(-n+3){border-bottom:1px solid var(--rule)}.stat:nth-child(4){padding-left:0}}
@media(max-width:760px){.cgroup{grid-template-columns:1fr;gap:.3rem}}
"""
end = s.find("</style>")
s = s[:end] + CSS + s[end:]

home = s.find('<main id="page-home"')
home_end = s.find("</main>", home)


def lift(marker):
    """Take a whole <section> on the home page out of the page and return it."""
    global s, home_end
    m = s.find(marker, home)
    assert home < m < home_end, "not found on the home page: " + marker
    a = s.rfind("<section", home, m)
    b = s.find("</section>", m) + len("</section>")
    block = s[a:b]
    s = s[:a] + s[b:].lstrip("\n")
    home_end = s.find("</main>", home)
    return block


# 2. the old track record block goes; the testimonials are lifted out to move up
lift("Track record &middot; last twelve months")
testimonials = lift("<h2>People who have sat in the room.</h2>")

# 3. the new block, then the testimonials, straight after the hero
stats_html = "\n".join('    <div class="stat s%d"><b>%s</b><span>%s</span></div>' % (i + 1, n, l)
                       for i, (n, l) in enumerate(STATS))
groups_html = "\n".join('    <div class="cgroup"><p class="cind">%s</p><p class="cnames">%s</p></div>'
                        % (ind, "<i>&middot;</i>".join(names)) for ind, names in CLIENTS)
SECTION = """
<section id="track-record">
 <div class="wrap">
  <p class="kick">Track record</p>
  <h2>35 brands across 9 industries.</h2>
  <p class="lead">Nairobi, Kenya and East Africa. Seven years inside live ad accounts.</p>
  <div class="stats">
%s
  </div>
  <div class="clients">
%s
  </div>
 </div>
</section>

%s
""" % (stats_html, groups_html, testimonials)
hero = s.find('<section class="hero">', home)
hero_end = s.find("</section>", hero) + len("</section>")
s = s[:hero_end] + "\n" + SECTION + s[hero_end:]

# 4. the About page says the same numbers
swap("<dt>Last twelve months</dt><dd>200+ SME owners trained &middot; 50 corporate teams &middot; 10 masterclasses hosted</dd>",
     "<dt>Track record</dt><dd>200+ SME owners trained &middot; 50 corporate teams &middot; 50+ masterclasses delivered &middot; 35+ brands across 9 industries</dd>")

io.open(INDEX, "w", encoding="utf-8", newline="").write(s)
print("added: %d numbers, %d client names in %d groups; testimonials moved under them"
      % (len(STATS), sum(len(n) for _, n in CLIENTS), len(CLIENTS)))
