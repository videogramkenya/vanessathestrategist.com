"""Three written client quotes under the video testimonials on the home page.

Words from Vanessa's mock-up. Alex, 29 Sep 2026: these are real clients' words; no names.
Each is signed with the client's role and city only.

    python media/add_written_quotes.py
"""
import io
from pathlib import Path

INDEX = Path(__file__).resolve().parents[1] / "index.html"
s = io.open(INDEX, encoding="utf-8").read()
assert 'class="wquotes"' not in s, "already added"

QUOTES = [
    ("Vanessa doesn&rsquo;t just run your ads. She builds the whole system &mdash; the funnel, the follow-up, "
     "the handover to sales. We saw qualified leads within the first week.",
     "Property developer &middot; Nairobi"),
    ("The training she delivered to our team was the best investment we made this year. Practical, no fluff, "
     "and immediately applicable. Our team actually understood the full funnel.",
     "Marketing director &middot; Nairobi"),
    ("I came in with zero clarity on what was working in my marketing. I left with a 90-day plan, a tracking "
     "dashboard, and a team that finally understood what they were measuring.",
     "SME founder, beauty &middot; Nairobi"),
]

CSS = """
/* written client quotes under the videos, 29 Sep 2026 */
.wquotes{display:grid;grid-template-columns:repeat(3,1fr);gap:1.4rem;margin-top:2.6rem}
.wquote{margin:0;padding-top:1.1rem;border-top:2px solid var(--ink);display:flex;flex-direction:column;gap:1rem}
.wquote blockquote{margin:0;font-family:var(--dsp);font-size:clamp(1.02rem,1.4vw,1.15rem);font-weight:500;letter-spacing:-.01em;line-height:1.45;color:var(--ink)}
.wquote blockquote::before{content:"\\201C";display:block;font-size:2.6rem;font-weight:800;line-height:.8;color:var(--mag);margin-bottom:.2rem}
.wquote figcaption{margin-top:auto;font-family:var(--mno);font-size:.62rem;letter-spacing:.16em;text-transform:uppercase;color:var(--soft)}
@media(max-width:900px){.wquotes{grid-template-columns:1fr;gap:1.8rem}}
"""
end = s.find("</style>")
s = s[:end] + CSS + s[end:]

# straight after the video row in the "People who have sat in the room." section on the home page
home = s.find('<main id="page-home"')
t = s.find("<h2>People who have sat in the room.</h2>", home)
assert home < t < s.find("</main>", home), "testimonials not found on the home page"
proofs = s.find('<div class="proofs">', t)
proofs_end = s.find("\n  </div>", proofs) + len("\n  </div>")
block = "\n  <div class=\"wquotes\">\n%s\n  </div>" % "\n".join(
    '   <figure class="wquote"><blockquote>%s</blockquote><figcaption>%s</figcaption></figure>' % q for q in QUOTES)
s = s[:proofs_end] + block + s[proofs_end:]

io.open(INDEX, "w", encoding="utf-8", newline="").write(s)
print("added %d written quotes under the videos" % len(QUOTES))
