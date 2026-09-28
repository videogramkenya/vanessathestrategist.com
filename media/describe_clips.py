"""Listen to each clip and write down what is in it, so Alex does not have to watch 14 minutes.

Pulls the audio out with ffmpeg, sends it to Gemini, and asks for: who is speaking, what they say,
whether it is a client speaking or Vanessa, and the two or three lines worth quoting on a website.

    python media/describe_clips.py
"""
import base64, json, os, subprocess, sys, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "media" / "source"
WORK = ROOT / "media" / "work"
OUT = ROOT / "media" / "clip_notes.json"
ENV = Path(r"C:\Users\HomePC\Documents\Agentic Workflows\Content OS\.env")
env = {}
for line in ENV.read_text(encoding="utf-8").splitlines():
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip()
KEY = env.get("GEMINI_API_KEY") or env["GOOGLE_AI_API_KEY"]
MODEL = "gemini-2.5-flash"

ASK = """This is the audio from a clip on Vanessa Wanjiku's Instagram. She runs Videogram Kenya and
sells marketing help to business owners in Nairobi: a one day Growth Strategy Day, team training
called Acquire and Close, and a four month build for property developers.

She wants to put real proof on her website. Tell me, in plain English:

1. WHO is talking. Vanessa herself, a client, several clients, or nobody (music only)?
2. WHAT is actually said, summarised in two or three sentences.
3. Is anyone praising her or describing a result they got? Quote their exact words if so.
4. Would this work as proof on a website for a stranger who has never heard of her? Answer
   STRONG, WEAK or NO, and say why in one line.

Keep the whole answer under 150 words. If there is no speech at all, say so in one line."""


def audio_of(mp4):
    wav = WORK / (mp4.stem + ".mp3")
    if not wav.exists():
        subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", str(mp4),
                        "-vn", "-ac", "1", "-ar", "16000", "-b:a", "48k", str(wav)], check=True)
    return wav


def ask_gemini(mp3):
    body = {"contents": [{"parts": [
        {"text": ASK},
        {"inline_data": {"mime_type": "audio/mp3", "data": base64.b64encode(mp3.read_bytes()).decode()}}]}]}
    req = urllib.request.Request(
        "https://generativelanguage.googleapis.com/v1beta/models/%s:generateContent?key=%s" % (MODEL, KEY),
        method="POST", data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        out = json.loads(r.read().decode())
    return "".join(p.get("text", "") for p in out["candidates"][0]["content"]["parts"]).strip()


WORK.mkdir(exist_ok=True)
notes = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {}
for mp4 in sorted(SRC.glob("*.mp4")):
    if mp4.name in notes:
        continue
    print("listening to", mp4.name, flush=True)
    try:
        notes[mp4.name] = ask_gemini(audio_of(mp4))
    except Exception as e:
        notes[mp4.name] = "(failed: %s)" % str(e)[:120]
    OUT.write_text(json.dumps(notes, ensure_ascii=False, indent=1), encoding="utf-8")
print("\n-> %s" % OUT)
