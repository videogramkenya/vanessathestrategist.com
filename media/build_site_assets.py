"""Turn the cut clips and chosen photos into files the website can serve.

Videos are already cut and compressed. This adds a still for each one (what you see before you
press play, so nothing downloads until someone clicks) and shrinks the photos for the web.

    python media/build_site_assets.py
"""
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CUT, SRC = ROOT / "media" / "cut", ROOT / "media" / "source"
OUT = ROOT / "proof"
OUT.mkdir(exist_ok=True)

# still frame time per clip, chosen where the person is looking at the camera
POSTER_AT = {"michelle_founder.mp4": 2.0, "social_insider.mp4": 3.0, "ads_like_a_pro.mp4": 12.0,
             "not_what_i_expected.mp4": 3.0, "ads_made_sense.mp4": 2.0}
PHOTOS = {
    "kss_team.jpg": "last_week_we_finally_graduated_the_kss_internal_team_after_f.jpg",
    "kss_terrence.jpg": "last_week_we_finally_graduated_the_kss_internal_team_after_f_1.jpg",
    "kss_daniel.jpg": "last_week_we_finally_graduated_the_kss_internal_team_after_f_3.jpg",
    "muzi_launch.jpg": "saturday_was_a_big_one_we_officially_launched_muzi_salama_an.jpg",
    "muzi_team.jpg": "saturday_was_a_big_one_we_officially_launched_muzi_salama_an_2.jpg",
}

for name, at in POSTER_AT.items():
    src = CUT / name
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-ss", str(at), "-i", str(src),
                    "-frames:v", "1", "-vf", "scale='min(720,iw)':-2", "-q:v", "4",
                    str(OUT / (src.stem + ".jpg"))], check=True)
    (OUT / name).write_bytes(src.read_bytes())

for out, src in PHOTOS.items():
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", str(SRC / src),
                    "-vf", "scale='min(1400,iw)':-2", "-q:v", "6", str(OUT / out)], check=True)

total = 0
for f in sorted(OUT.iterdir()):
    total += f.stat().st_size
    print("%-28s %6.0f KB" % (f.name, f.stat().st_size / 1024))
print("total %.1f MB (only the stills and photos load with the page)" % (total / 1e6))
