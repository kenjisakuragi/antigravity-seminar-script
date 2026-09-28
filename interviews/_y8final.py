# -*- coding: utf-8 -*-
"""Y8b（たたみかけ用・決め台詞だけ）を切って、字幕まで焼く。"""
import json
import os
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = r"C:\Users\yanagi\Documents\Zoom\2026-07-30 21.01.17 ゆきちさん\ゆきちさん.mp4"
OUT = os.path.join(HERE, "clips_yukichi", "Y8b_一緒にやろうよ.mp4")
BURN = os.path.join(HERE, "clips_yukichi", "Y8b_字幕入り.mp4")

import imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe()

# 1257.0〜1266.0（9秒）。桜木さんの受けは入れない
subprocess.run([FF, "-y", "-hide_banner", "-loglevel", "error",
                "-ss", "1257.0", "-to", "1266.0", "-i", SRC,
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
                "-c:a", "aac", "-b:a", "128k", OUT], check=True)
print("切り出し Y8b（9秒）")

# 単語ごとの時刻を取って、切れ目を決める
wav = os.path.join(HERE, "_y8b.wav")
subprocess.run([FF, "-y", "-hide_banner", "-loglevel", "error",
                "-i", OUT, "-vn", "-ac", "1", "-ar", "16000", wav], check=True)
from faster_whisper import WhisperModel
m = WhisperModel("medium", device="cpu", compute_type="int8")
segs, _ = m.transcribe(wav, language="ja", word_timestamps=True,
                       vad_filter=False, beam_size=5)
words = [(w.start, w.end, w.word.strip()) for s in segs for w in (s.words or [])]
os.remove(wav)
for w in words:
    print(f"  {w[0]:5.2f} {w[1]:5.2f} {w[2]}")

# 「一緒に」が始まるところで2枚に分ける。
# whisperは「一」「緒」と1文字ずつに割ることがあるので、文字列一致に頼らない。
# 「ら」のあとに1秒以上あく → そこが句の切れ目、と見る。
cut = None
for a, b in zip(words, words[1:]):
    if b[0] - a[1] >= 0.8:
        cut = b[0]
        break
if cut is None:
    cut = words[len(words) // 2][0]
end = words[-1][1] if words else 8.0
start = words[0][0] if words else 0.5
caps = [
    {"in": round(start - 0.2, 2), "out": round(cut - 0.05, 2),
     "text": "気になるんだったら、"},
    {"in": round(cut - 0.05, 2), "out": round(end + 0.3, 2),
     "text": "一緒にやろうよ、っていう感じです"},
]
p = os.path.join(HERE, "caps_Y8b.json")
json.dump(caps, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("字幕:", json.dumps(caps, ensure_ascii=False))

subprocess.run([sys.executable, os.path.join(HERE, "_burn.py"), OUT, p, BURN],
               check=True)
