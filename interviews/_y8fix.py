# -*- coding: utf-8 -*-
"""Y8の切り直し。決め台詞「一緒にやろうよ」が入るように、終点を伸ばす。

シェル経由で日本語のパスを渡すと文字化けするので、ここに直接書く。
"""
import os
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = r"C:\Users\yanagi\Documents\Zoom\2026-07-30 21.01.17 ゆきちさん\ゆきちさん.mp4"

import imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe()

JOBS = [
    # 文脈込み。質問 → 考える間 → 答え → 「一緒にやろうよ」まで
    ("Y8_一緒にやろうよ_長", 1178, 1272),
    # ★たたみかけ用。決め台詞だけ
    ("Y8a_一緒にやろうよ", 1250, 1270),
]


def main():
    print("元ファイル:", "あり" if os.path.exists(SRC) else "なし")
    if not os.path.exists(SRC):
        return 1
    outdir = os.path.join(HERE, "clips_yukichi")
    for name, a, b in JOBS:
        out = os.path.join(outdir, name + ".mp4")
        subprocess.run([FF, "-y", "-hide_banner", "-loglevel", "error",
                        "-ss", str(a), "-to", str(b), "-i", SRC,
                        "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
                        "-c:a", "aac", "-b:a", "128k", out], check=True)
        print(f"  切り出し {name}（{b - a}秒）")

    wav = os.path.join(HERE, "_y8a.wav")
    subprocess.run([FF, "-y", "-hide_banner", "-loglevel", "error",
                    "-i", os.path.join(outdir, "Y8a_一緒にやろうよ.mp4"),
                    "-vn", "-ac", "1", "-ar", "16000", wav], check=True)
    from faster_whisper import WhisperModel
    m = WhisperModel("medium", device="cpu", compute_type="int8")
    segs, _ = m.transcribe(wav, language="ja", word_timestamps=True,
                           vad_filter=False, beam_size=5)
    print("--- Y8a の中身:")
    for s in segs:
        print(f"{s.start:6.2f} {s.end:6.2f}  {s.text.strip()}")
    os.remove(wav)
    return 0


if __name__ == "__main__":
    sys.exit(main())
