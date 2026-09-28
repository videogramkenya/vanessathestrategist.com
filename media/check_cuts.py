"""Listen to each finished cut and prove no word is chopped at either end.

Whisper reads the cut itself. A first word that starts at 0.00, or a last word that ends right on
the final frame, means the cut landed inside speech. 28 Sep 2026.

    python media/check_cuts.py
"""
import json, subprocess
from pathlib import Path
import whisper

ROOT = Path(__file__).resolve().parents[1]
CUT = ROOT / "media" / "cut"
model = whisper.load_model("small")
for mp4 in sorted(CUT.glob("*.mp4")):
    mp3 = mp4.with_suffix(".mp3")
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", str(mp4), "-vn", "-ac", "1",
                    "-ar", "16000", "-b:a", "48k", str(mp3)], check=True)
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                "-of", "csv=p=0", str(mp4)], capture_output=True, text=True).stdout)
    r = model.transcribe(str(mp3), word_timestamps=True, language="en")
    words = [w for seg in r["segments"] for w in seg["words"]]
    mp3.unlink()
    if not words:
        print("%-24s NO SPEECH" % mp4.name); continue
    first, last = words[0], words[-1]
    head = " ".join(w["word"].strip() for w in words[:7])
    tail = " ".join(w["word"].strip() for w in words[-7:])
    start_ok = first["start"] > 0.12
    end_ok = (dur - last["end"]) > 0.12
    print("%-24s %4.1fs  starts clean: %-5s  ends clean: %-5s" % (mp4.name, dur, start_ok, end_ok))
    print("     opens: %s" % head)
    print("     ends : %s   (%.2fs of quiet after)" % (tail, dur - last["end"]))
