"""Timestamped words for the four clips worth using, so the cut lands on the sentence.

    python media/transcribe_clips.py
"""
import base64, json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC, WORK = ROOT / "media" / "source", ROOT / "media" / "work"
OUT = ROOT / "media" / "clip_transcripts.json"
ENV = Path(r"C:\Users\HomePC\Documents\Agentic Workflows\Content OS\.env")
env = {}
for line in ENV.read_text(encoding="utf-8").splitlines():
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
        k, v = line.split("=", 1); env[k.strip()] = v.strip()
KEY = env.get("GEMINI_API_KEY") or env["GOOGLE_AI_API_KEY"]

CLIPS = ["if_these_testimonials_from_cohort_7_don_t_inspire_you_to_tak.mp4",
         "growing_business_owners_assemble_let_me_plug_you_there_s_a_l.mp4",
         "a_powerful_reminder_that_scaling_isn_t_just_about_systems_it.mp4",
         "this_year_i_intend_to_lock_in_and_see_what_this_little_busin.mp4"]

ASK = """Transcribe this audio with timestamps. One line per sentence, in this exact shape:

[mm:ss - mm:ss] SPEAKER: what they said

SPEAKER is "Vanessa" when it is the business owner who runs the training, or "Client" (Client 1,
Client 2 if there are several) for anyone praising her. Write "MUSIC" for stretches with no speech.
Transcribe the words exactly as spoken. Do not summarise."""


def ask(mp3):
    body = {"contents": [{"parts": [
        {"text": ASK},
        {"inline_data": {"mime_type": "audio/mp3", "data": base64.b64encode(mp3.read_bytes()).decode()}}]}]}
    import urllib.request
    req = urllib.request.Request(
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=" + KEY,
        method="POST", data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        out = json.loads(r.read().decode())
    return "".join(p.get("text", "") for p in out["candidates"][0]["content"]["parts"]).strip()


res = {}
for name in CLIPS:
    mp3 = WORK / (Path(name).stem + ".mp3")
    print("transcribing", name, flush=True)
    res[name] = ask(mp3)
OUT.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
for k, v in res.items():
    print("\n" + "=" * 70 + "\n" + k + "\n" + v)
