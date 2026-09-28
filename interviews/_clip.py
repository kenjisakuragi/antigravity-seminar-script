# -*- coding: utf-8 -*-
"""
_clip.py — インタビュー動画から、使いどころを切り出す。字幕も一緒に切る。

  python _clip.py <元動画> <SRT> <台帳.json> <出力フォルダ>

台帳（json）の形
  [{"name":"c1_1年前", "in":"00:02:19", "out":"00:04:10", "note":"..."} , ...]
  "join": ["c1_1年前","c2_言い訳"] を入れた項目は、他のクリップをつないだものを作る。

出力
  <name>.mp4  … 切り出した動画（再エンコード。切り口をきれいにするため）
  <name>.srt  … そのクリップだけの字幕（時刻を0起点に振り直したもの）

■ 字幕を焼き込まない理由
  焼き込むと直せない。SRTを別に出しておけば、文字を直したり、
  テロップの体裁を変えたりが、あとからできる。
"""
import json
import os
import re
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))


def secs(t):
    p = [float(x.replace(",", ".")) for x in t.split(":")]
    while len(p) < 3:
        p.insert(0, 0.0)
    return p[0] * 3600 + p[1] * 60 + p[2]


def stamp(t):
    h, m = int(t // 3600), int(t % 3600 // 60)
    return f"{h:02d}:{m:02d}:{t % 60:06.3f}".replace(".", ",")


def read_srt(path):
    out = []
    for blk in open(path, encoding="utf-8").read().split("\n\n"):
        lines = [l for l in blk.splitlines() if l.strip()]
        if len(lines) < 3:
            continue
        m = re.match(r"(\S+)\s*-->\s*(\S+)", lines[1])
        if not m:
            continue
        out.append((secs(m.group(1)), secs(m.group(2)), " ".join(lines[2:])))
    return out


def cut_srt(subs, a, b, path):
    n = 0
    with open(path, "w", encoding="utf-8") as f:
        for s, e, txt in subs:
            if e <= a or s >= b:
                continue
            n += 1
            f.write(f"{n}\n{stamp(max(s, a) - a)} --> {stamp(min(e, b) - a)}\n{txt}\n\n")
    return n


def main():
    src, srtp, ledger, outdir = sys.argv[1:5]
    os.makedirs(outdir, exist_ok=True)
    import imageio_ffmpeg
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    subs = read_srt(srtp)
    items = json.load(open(ledger, encoding="utf-8"))
    made = {}

    for it in items:
        out = os.path.abspath(os.path.join(outdir, it["name"] + ".mp4"))
        if "join" in it:
            lst = os.path.join(outdir, "_join.txt")
            with open(lst, "w", encoding="utf-8") as f:
                for n in it["join"]:
                    # concat のパスは、リストファイルの場所からの相対になる。
                    # 絶対パスで書かないと二重になって開けない。
                    f.write("file '{}'\n".format(made[n].replace("\\", "/")))
            subprocess.run([ff, "-y", "-hide_banner", "-loglevel", "error",
                            "-f", "concat", "-safe", "0", "-i", lst,
                            "-c", "copy", out], check=True)
            os.remove(lst)
            print(f"  {it['name']}  ({'＋'.join(it['join'])})")
            made[it["name"]] = out
            continue

        a, b = secs(it["in"]), secs(it["out"])
        if os.path.exists(out):          # 作り直しは、消してから
            made[it["name"]] = out
            print(f"  {it['name']}  済み")
            continue
        subprocess.run([ff, "-y", "-hide_banner", "-loglevel", "error",
                        "-ss", str(a), "-to", str(b), "-i", src,
                        "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
                        "-c:a", "aac", "-b:a", "128k", out], check=True)
        n = cut_srt(subs, a, b, os.path.join(outdir, it["name"] + ".srt"))
        made[it["name"]] = out
        print(f"  {it['name']}  {it['in']}〜{it['out']}  "
              f"（{b - a:.0f}秒・字幕{n}行）")

    print(f"\n判定: ✅ {len(made)}本  → {outdir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
