"""Where the speech actually stops, so a cut never lands mid-word.

    python media/find_pauses.py <file.mp4>
"""
import re, subprocess, sys
from pathlib import Path

def pauses(path, noise="-32dB", minlen=0.28):
    out = subprocess.run(["ffmpeg", "-nostdin", "-i", str(path), "-af",
                          "silencedetect=noise=%s:d=%s" % (noise, minlen), "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", out)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", out)]
    return list(zip(starts, ends + [None] * (len(starts) - len(ends))))

if __name__ == "__main__":
    for s, e in pauses(Path(sys.argv[1])):
        print("  pause %7.2f -> %s" % (s, "%.2f" % e if e else "end"))
