"""Word-by-word timings for a clip, so a cut can land in a real gap between words.

Uses Whisper locally, which is already installed. The small model is enough for clear speech and
runs on the laptop, so no audio leaves the machine.

    python media/word_times.py media/work/<name>.mp3
"""
import json, sys
from pathlib import Path
import whisper

path = Path(sys.argv[1])
out = path.with_suffix(".words.json")
if out.exists():
    words = json.loads(out.read_text(encoding="utf-8"))
else:
    model = whisper.load_model("small")
    r = model.transcribe(str(path), word_timestamps=True, language="en")
    words = [{"w": w["word"].strip(), "a": round(w["start"], 2), "b": round(w["end"], 2)}
             for seg in r["segments"] for w in seg["words"]]
    out.write_text(json.dumps(words, ensure_ascii=False), encoding="utf-8")
line, start = [], None
for i, w in enumerate(words):
    if start is None:
        start = w["a"]
    line.append(w["w"])
    gap = words[i + 1]["a"] - w["b"] if i + 1 < len(words) else 9
    if gap > 0.45 or len(line) > 22:
        print("[%6.2f - %6.2f] (gap %.2fs) %s" % (start, w["b"], gap, " ".join(line)))
        line, start = [], None
