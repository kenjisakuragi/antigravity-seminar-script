# -*- coding: utf-8 -*-
"""
_tighten.py — 長すぎる無音だけを詰める。ジェットカットはしない。

  python _tighten.py <入力.mp4> <出力.mp4> [<字幕.json> <詰めた後の字幕.json>]

■ 何をするか / しないか
  する  … 3秒を超える無音を、1.2秒まで詰める（機材のもたつき・相槌待ちの空白）
  しない… 語と語のあいだを詰める（ジェットカット）
          考えている間を消す（3秒以内の沈黙は、そのまま残す）

  卒業生の語りなので、細かく切ると「編集で意味を作った」ように見える。
  意味に触らず、空白だけを削る。

■ 字幕の時刻も一緒にずらす
  第3・第4引数に caps json を渡すと、詰めた分だけ時刻を繰り上げた json を書き出す。
"""
import json
import os
import re
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))

LONG = 3.0        # これより長い無音を詰める
KEEP = 1.2        # 詰めたあとに残す長さ
NOISE = "-32dB"   # 無音とみなす音量
MIN_SIL = 0.6     # silencedetect が無音と認める最短


def ffmpeg():
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


def duration(ff, path):
    r = subprocess.run([ff, "-hide_banner", "-i", path],
                       capture_output=True, text=True, errors="replace")
    m = re.search(r"Duration: (\d+):(\d+):([\d.]+)", r.stderr)
    return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))


def silences(ff, path):
    r = subprocess.run([ff, "-hide_banner", "-i", path, "-af",
                        f"silencedetect=noise={NOISE}:d={MIN_SIL}",
                        "-f", "null", "-"],
                       capture_output=True, text=True, errors="replace")
    out, start = [], None
    for line in r.stderr.splitlines():
        a = re.search(r"silence_start: ([\d.]+)", line)
        b = re.search(r"silence_end: ([\d.]+)", line)
        if a:
            start = float(a.group(1))
        elif b and start is not None:
            out.append((start, float(b.group(1))))
            start = None
    return out


def plan(sils, total):
    """残す区間と、時刻の対応表を作る。"""
    keeps, cuts = [], []
    at = 0.0
    for s, e in sils:
        if e - s <= LONG:
            continue
        # 無音の前半 KEEP/2 と後半 KEEP/2 だけ残し、真ん中を捨てる
        keeps.append((at, s + KEEP / 2))
        cuts.append((s + KEEP / 2, e - KEEP / 2))
        at = e - KEEP / 2
    keeps.append((at, total))
    return keeps, cuts


def remap(t, cuts):
    """元の時刻 → 詰めたあとの時刻。"""
    shift = 0.0
    for a, b in cuts:
        if t >= b:
            shift += b - a
        elif t > a:
            return a - shift          # 捨てた区間の中なら、その入口に寄せる
    return t - shift


def main():
    src, out = sys.argv[1], sys.argv[2]
    ff = ffmpeg()
    total = duration(ff, src)
    sils = silences(ff, src)
    keeps, cuts = plan(sils, total)

    print(f"全体 {total:.1f}秒 / 無音 {len(sils)}か所 "
          f"（うち{LONG}秒超 {len(cuts)}か所）")
    for a, b in cuts:
        print(f"  {a:6.2f}〜{b:6.2f} を詰めます（{b - a:.1f}秒ぶん）")
    if not cuts:
        print("判定: 詰めるところがありません")
        return 0

    # 区間ごとに切り出して、つなぐ
    parts, lst = [], os.path.join(HERE, "_t_list.txt")
    for i, (a, b) in enumerate(keeps):
        p = os.path.join(HERE, f"_t_{i:02d}.mp4")
        subprocess.run([ff, "-y", "-hide_banner", "-loglevel", "error",
                        "-ss", str(a), "-to", str(b), "-i", src,
                        "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
                        "-c:a", "aac", "-b:a", "128k", p], check=True)
        parts.append(p)
    with open(lst, "w", encoding="utf-8") as f:
        for p in parts:
            f.write("file '{}'\n".format(os.path.abspath(p).replace("\\", "/")))
    subprocess.run([ff, "-y", "-hide_banner", "-loglevel", "error",
                    "-f", "concat", "-safe", "0", "-i", lst,
                    "-c", "copy", out], check=True)
    for p in parts + [lst]:
        os.remove(p)

    if len(sys.argv) >= 5:
        caps = json.load(open(sys.argv[3], encoding="utf-8"))
        for c in caps:
            c["in"] = round(remap(c["in"], cuts), 2)
            c["out"] = round(remap(c["out"], cuts), 2)
        json.dump(caps, open(sys.argv[4], "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
        print(f"字幕の時刻も繰り上げました → {os.path.basename(sys.argv[4])}")

    saved = sum(b - a for a, b in cuts)
    print(f"判定: ✅ {total:.1f}秒 → {total - saved:.1f}秒（{saved:.1f}秒ぶん短く）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
