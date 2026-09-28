# -*- coding: utf-8 -*-
"""
_tighten2.py — 間を詰めて、字幕の時刻も一緒にずらす。

  python _tighten2.py <クリップ.mp4> <字幕.json> <出力.mp4> <出力字幕.json>

■ なにをするか
  話していない区間（無音）を短くする。頭とお尻も切る。
  そのぶん**字幕の時刻を、同じだけ前に詰める**。

■ なぜ字幕を作り直さないか
  取り除くのは「区間」だけなので、**どの時刻がどこへ動くかは計算で出せる**。
  作り直すと、せっかく人の手で直した文がまた壊れる。

■ 加減
  1.2秒より長い間は 0.45秒に。頭とお尻は 0.25秒だけ残す。
  ゼロにすると詰まりすぎて、聞いていて息が苦しくなる。

■ 判定
  音の大きさを50msごとに測り、いちばん大きい音の4%を超えたら「話している」。
"""
import json
import os
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))

SR = 8000
STEP = 0.05
GAP_MAX = 1.2       # これより長い間は詰める
GAP_KEEP = 0.45     # 詰めたあとに残す長さ
EDGE_KEEP = 0.25    # 頭とお尻に残す長さ


def voiced(path):
    import numpy as np
    import imageio_ffmpeg
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    r = subprocess.run([ff, "-v", "error", "-i", path, "-ac", "1", "-ar", str(SR),
                        "-f", "s16le", "-"], capture_output=True, stdin=subprocess.DEVNULL)
    a = np.frombuffer(r.stdout, dtype=np.int16).astype(float) / 32768
    n = int(SR * STEP)
    m = len(a) // n
    e = np.sqrt((a[:m * n].reshape(m, n) ** 2).mean(axis=1))
    return e > max(0.006, e.max() * 0.04), m * STEP


def keep_ranges(on, dur):
    """残す区間（元の時刻）を返す。"""
    import numpy as np
    idx = np.flatnonzero(on)
    if len(idx) == 0:
        return [(0.0, dur)]
    segs = []
    start = max(0.0, idx[0] * STEP - EDGE_KEEP)
    prev = idx[0]
    for i in idx[1:]:
        gap = (i - prev) * STEP
        if gap > GAP_MAX:
            segs.append((start, (prev + 1) * STEP + GAP_KEEP / 2))
            start = i * STEP - GAP_KEEP / 2
        prev = i
    segs.append((start, min(dur, (prev + 1) * STEP + EDGE_KEEP)))
    return [(round(a, 3), round(b, 3)) for a, b in segs if b - a > 0.1]


def remap(t, segs):
    """元の時刻を、詰めたあとの時刻に置きかえる。"""
    acc = 0.0
    for a, b in segs:
        if t < a:
            return acc
        if t <= b:
            return acc + (t - a)
        acc += b - a
    return acc


def main():
    clip, capj, out, capout = sys.argv[1:5]
    import imageio_ffmpeg
    ff = imageio_ffmpeg.get_ffmpeg_exe()

    on, dur = voiced(clip)
    segs = keep_ranges(on, dur)
    new_dur = sum(b - a for a, b in segs)
    if new_dur > dur - 0.6:
        print(f"  詰めるところがありません（{dur:.1f}秒）。そのまま使います")
        return 2

    # 残す区間だけをつないで1本にする
    v = "".join(f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS[v{i}];"
                f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS[a{i}];"
                for i, (a, b) in enumerate(segs))
    cat = "".join(f"[v{i}][a{i}]" for i in range(len(segs)))
    fc = v + cat + f"concat=n={len(segs)}:v=1:a=1[vo][ao]"
    subprocess.run([ff, "-y", "-v", "error", "-i", clip, "-filter_complex", fc,
                    "-map", "[vo]", "-map", "[ao]",
                    "-c:v", "libx264", "-preset", "medium", "-crf", "20",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", out],
                   check=True, stdin=subprocess.DEVNULL)

    caps = json.load(open(capj, encoding="utf-8"))
    for c in caps:
        c["in"] = round(remap(c["in"], segs), 2)
        c["out"] = round(remap(c["out"], segs), 2)
    caps = [c for c in caps if c["out"] - c["in"] > 0.4]
    json.dump(caps, open(capout, "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)

    print(f"  {dur:.1f}秒 → {new_dur:.1f}秒（{dur-new_dur:.1f}秒短縮）／字幕{len(caps)}枚")
    return 0


if __name__ == "__main__":
    sys.exit(main())
