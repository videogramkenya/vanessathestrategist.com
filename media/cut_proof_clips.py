"""Cut the four usable clips down to the part that is actually proof.

Each cut is one or two pieces joined, chosen from the timestamped transcript so the cut lands
between sentences. Compressed for the web: 720 tall, which is plenty on a phone.

    python media/cut_proof_clips.py
"""
import json, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC, OUT = ROOT / "media" / "source", ROOT / "media" / "cut"
OUT.mkdir(exist_ok=True)

COHORT = "if_these_testimonials_from_cohort_7_don_t_inspire_you_to_tak.mp4"
CUTS = [
    # Every boundary sits in a real gap between words, read off Whisper's word timings
    # (media/word_times.py). The first cut of these landed mid-word and ran into the next
    # speaker, which Alex heard straight away. 28 Sep 2026.
    ("michelle_founder.mp4", COHORT, [(0.00, 1.70), (17.35, 24.55), (24.90, 47.80)],
     "Ayuma Michelle, founder: her name, then 'for the first time there is value for money'"),
    ("social_insider.mp4", COHORT, [(97.70, 108.25), (113.90, 131.80)],
     "The Social Insider, brand strategist: 'best investment, best everything', ads were a monster, Vanessa simplified"),
    ("ads_like_a_pro.mp4", "growing_business_owners_assemble_let_me_plug_you_there_s_a_l.mp4",
     [(7.10, 37.35)], "client: 'that was also me', trained to run ads like a pro, a lot of new leads"),
    ("not_what_i_expected.mp4", "a_powerful_reminder_that_scaling_isn_t_just_about_systems_it.mp4",
     [(16.50, 39.60)], "client at the Strategy Day: 'not what I was expecting, in a good way', practical"),
    ("ads_made_sense.mp4", "this_year_i_intend_to_lock_in_and_see_what_this_little_busin.mp4",
     [(0.00, 16.60)], "client: 'for the first time ads actually made sense', built ads step by step"),
]


def piece(src, start, end, out):
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-ss", str(start), "-to", str(end),
                    "-i", str(src), "-vf", "scale=-2:720", "-c:v", "libx264", "-crf", "26",
                    "-preset", "veryfast", "-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart",
                    str(out)], check=True)


notes = {}
for name, src, spans, what in CUTS:
    parts = []
    for i, (a, b) in enumerate(spans):
        p = OUT / ("_tmp_%s_%d.mp4" % (Path(name).stem, i))
        piece(SRC / src, a, b, p)
        parts.append(p)
    final = OUT / name
    if len(parts) == 1:
        parts[0].replace(final)
    else:
        lst = OUT / ("_tmp_%s.txt" % Path(name).stem)
        lst.write_text("".join("file '%s'\n" % p.name for p in parts), encoding="utf-8")
        subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "concat", "-safe", "0",
                        "-i", str(lst), "-c", "copy", "-movflags", "+faststart", str(final)],
                       check=True, cwd=str(OUT))
        lst.unlink()
        for p in parts:
            p.unlink()
    secs = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                 "-of", "csv=p=0", str(final)], capture_output=True, text=True).stdout.strip())
    notes[name] = {"what": what, "seconds": round(secs, 1), "mb": round(final.stat().st_size / 1e6, 2)}
    print("%-24s %5.1fs  %5.2f MB  %s" % (name, secs, final.stat().st_size / 1e6, what))
(ROOT / "media" / "cut_notes.json").write_text(json.dumps(notes, indent=1), encoding="utf-8")
