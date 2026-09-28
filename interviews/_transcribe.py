# -*- coding: utf-8 -*-
"""
_transcribe.py — インタビュー動画から、時刻つきの書き起こしを作る。

  python _transcribe.py "<動画ファイル>" <出力名>

出力（interviews/ の下）
  <出力名>.txt   … [00:01:23] 本文  の形。使いどころを探すのに使う
  <出力名>.srt   … 字幕ファイル。あとで動画に焼くとき用

■ なぜローカルで文字起こしするか
  この録画はZoomクラウドではなく手元のファイルなので、Zoom側の書き起こしが無い。
  faster-whisper（CPU）で起こす。22分の音声で、20〜40分ほどかかる。

■ 個人情報
  卒業生の語りが入る。ここで作る書き起こしは社外に出さない。
  公開に使うのは、許諾を取った引用だけ。
"""
import os
import re
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))


def hhmmss(t, comma=False):
    h, m = int(t // 3600), int(t % 3600 // 60)
    s = t % 60
    return (f"{h:02d}:{m:02d}:{s:06.3f}".replace(".", ",")
            if comma else f"{h:02d}:{m:02d}:{int(s):02d}")


def main():
    src, name = sys.argv[1], sys.argv[2]
    wav = os.path.join(HERE, name + ".wav")

    if not os.path.exists(wav):
        import imageio_ffmpeg
        ff = imageio_ffmpeg.get_ffmpeg_exe()
        print("音声を取り出します…", flush=True)
        subprocess.run([ff, "-y", "-hide_banner", "-loglevel", "error",
                        "-i", src, "-vn", "-ac", "1", "-ar", "16000", wav],
                       check=True)

    # 途中でPCを切っても、続きから再開できるようにする。
    # すでに書けている .txt の最後の時刻を読み、そこから先だけ起こす。
    tp = os.path.join(HERE, name + ".txt")
    done_until, n = 0.0, 0
    if os.path.exists(tp):
        for l in open(tp, encoding="utf-8"):
            m = re.match(r"\[(\d+):(\d+):(\d+)\]", l)
            if m:
                done_until = (int(m.group(1)) * 3600 + int(m.group(2)) * 60
                              + int(m.group(3)))
                n += 1
        if n:
            print(f"前回の続きから：{hhmmss(done_until)} まで済み（{n}行）", flush=True)

    from faster_whisper import WhisperModel
    # 日本語なので small では取りこぼす。medium で起こす。
    print("書き起こし中（音声1分あたり1〜3分かかります）…", flush=True)
    model = WhisperModel("medium", device="cpu", compute_type="int8")
    segs, info = model.transcribe(wav, language="ja", vad_filter=True,
                                 beam_size=5,
                                 clip_timestamps=[done_until] if done_until else None)

    mode = "a" if n else "w"
    txt = open(tp, mode, encoding="utf-8")
    srt = open(os.path.join(HERE, name + ".srt"), mode, encoding="utf-8")
    for s in segs:
        n += 1
        line = s.text.strip()
        txt.write(f"[{hhmmss(s.start)}] {line}\n")
        txt.flush()
        srt.write(f"{n}\n{hhmmss(s.start, True)} --> {hhmmss(s.end, True)}\n"
                  f"{line}\n\n")
        if n % 20 == 0:
            print(f"  {hhmmss(s.start)} まで", flush=True)
    txt.close()
    srt.close()
    print(f"判定: ✅ {n}行  → {name}.txt / {name}.srt")
    return 0


if __name__ == "__main__":
    sys.exit(main())
