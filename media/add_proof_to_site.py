"""Put the client proof into the site: clips on the home page, matching proof on each service page.

Nothing plays by itself. Each clip shows a still picture until somebody presses play, so the page
still loads in a moment and the 8MB of video is only fetched by people who actually want it.

    python media/add_proof_to_site.py            # dry run, says what it would change
    python media/add_proof_to_site.py --confirm
"""
import io, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "index.html"

CSS = """
/* client proof: clips and photos, added 28 Sep 2026 */
.proofs{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:1.4rem;margin-top:2.2rem}
.proof{margin:0}
.proof video{width:100%;aspect-ratio:9/16;object-fit:cover;border-radius:3px;background:#000;display:block}
.proof.wide video{aspect-ratio:16/9}
.proof figcaption{margin-top:.7rem;font-size:.82rem;line-height:1.45;opacity:.78}
.proof figcaption b{display:block;opacity:1;font-weight:600}
.shots{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:1rem;margin-top:2rem}
.shots figure{margin:0}
.shots img{width:100%;height:100%;aspect-ratio:4/5;object-fit:cover;border-radius:3px;display:block}
.shots figcaption{margin-top:.6rem;font-size:.8rem;opacity:.75}
@media(max-width:640px){.proofs{grid-template-columns:1fr 1fr;gap:.9rem}.proof figcaption{font-size:.75rem}}
"""


def clip(name, who, what):
    return ('<figure class="proof"><video controls preload="none" playsinline '
            'poster="proof/%s.jpg" src="proof/%s.mp4"></video>'
            '<figcaption><b>%s</b>%s</figcaption></figure>' % (name, name, who, what))


def shot(name, alt, cap):
    return ('<figure><img loading="lazy" src="proof/%s.jpg" alt="%s"><figcaption>%s</figcaption></figure>'
            % (name, alt, cap))


HOME = """<section>
 <div class="wrap">
  <p class="kick">In their words</p>
  <h2>People who have sat in the room.</h2>
  <p class="lead">Nothing here is written by me. Press play on any of them.</p>
  <div class="proofs">
  %s
  %s
  %s
  </div>
 </div>
</section>

""" % (
    clip("michelle_founder", "Ayuma Michelle, founder",
         "&ldquo;For the first time, I actually find that there&rsquo;s value for money in investing in anything social media.&rdquo;"),
    clip("social_insider", "The Social Insider, brand strategist",
         "&ldquo;Ads were such a monster, but Vanessa simplified it.&rdquo;"),
    clip("ads_like_a_pro", "Business owner, after ads training",
         "&ldquo;She sat down with me and trained me how to actually run ads like a pro.&rdquo;"),
)

BT = """<div class="shots">
  %s
  %s
 </div>
 <p class="small" style="margin-top:1rem">Launch day at Muzi Salama, a residential development in Nairobi.</p>

 """ % (shot("muzi_launch", "The Muzi Salama launch", "Muzi Salama launch, Nairobi"),
        shot("muzi_team", "The team at the Muzi Salama launch", "On site with the team"))

AC = """<div class="shots">
  %s
  %s
  %s
 </div>
 <p class="small" style="margin-top:1rem">The KSS team, after four Acquire &amp; Close sessions with their own accounts and their own pipeline.</p>
 <div class="proofs" style="margin-top:1.8rem">
  %s
 </div>

 """ % (shot("kss_team", "The KSS team with their certificates", "Acquire &amp; Close, graduation day"),
        shot("kss_terrence", "Vanessa handing over a certificate", "Certificates, not slides"),
        shot("kss_daniel", "Another team member receiving a certificate", "Four sessions, one team"),
        clip("not_what_i_expected", "A business owner, on the day",
             "&ldquo;Not what I was expecting, in a good way. Very engaging, extremely practical.&rdquo;"))

SD = """<div class="proofs">
  %s
  %s
 </div>

 """ % (clip("ads_made_sense", "Business owner, Meta Money Masterclass",
             "&ldquo;For the first time, ads actually made sense. We built ads practically, step by step.&rdquo;"),
       clip("not_what_i_expected", "A business owner, on the day",
            "&ldquo;Not what I was expecting, in a good way. Very engaging, extremely practical.&rdquo;"))

s = io.open(PAGE, encoding="utf-8").read()
assert "class=\"proofs\"" not in s, "refusing: the proof is already in the page"

edits = [
    ("the stylesheet", "\n/* objections */", CSS + "\n/* objections */"),
    ("the home page, after the flagship case",
     '<section>\n <div class="wrap">\n  <p class="kick">Say it out loud</p>', HOME +
     '<section>\n <div class="wrap">\n  <p class="kick">Say it out loud</p>'),
    ("the Build & Transfer page", '  <div class="ctabox" style="margin-top:2.8rem">\n   <h2>Tell me about the development.</h2>',
     " " + BT + ' <div class="ctabox" style="margin-top:2.8rem">\n   <h2>Tell me about the development.</h2>'),
    ("the Acquire & Close page", '  <div class="ctabox" style="margin-top:2.8rem">\n   <h2>Tell me what your team sells.</h2>',
     " " + AC + ' <div class="ctabox" style="margin-top:2.8rem">\n   <h2>Tell me what your team sells.</h2>'),
    ("the Strategy Day page", '  <div class="ctabox" style="margin-top:2.8rem">\n   <h2>One day. Then you know where your next sale comes from.</h2>',
     " " + SD + ' <div class="ctabox" style="margin-top:2.8rem">\n   <h2>One day. Then you know where your next sale comes from.</h2>'),
]
for label, old, new in edits:
    n = s.count(old)
    assert n == 1, "anchor for %s found %d times" % (label, n)
    s = s.replace(old, new)
    print("ready:", label)

if "--confirm" not in sys.argv:
    print("\ndry run. add --confirm to write index.html")
    raise SystemExit(0)
io.open(PAGE, "w", encoding="utf-8", newline="").write(s)
print("\nwritten. index.html is now %.2f MB" % (PAGE.stat().st_size / 1e6))
