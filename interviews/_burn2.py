# -*- coding: utf-8 -*-
"""
_burn2.py — 説明会用に、字幕を大きく焼き込む（本番版）。

  python _burn2.py <クリップ.mp4> <字幕.json> <出力.mp4> [話し手]

`_burn.py` との違い（2026/8/4・桜木さん指定）
  1. **字幕を大きく**（42 → 68）。会場のうしろの席・スマホ視聴でも読める大きさに
  2. **上の注記テロップを外した**（下の「⚠️」を必ず読むこと）
  3. **1280x720 に上げてから焼く**。元が640x360なので、そのまま焼くと字がにじむ。
     先に拡大してから字を描くと、**文字だけは鮮明**になる（映像の解像度は上がらない）
  4. 1行を短く（22文字 → 18文字）。大きくしたぶん、1行に入る量を減らす

⚠️ 注記を外したことについて
  「前身講座の卒業生の声です／個人の感想です。成果を保証するものではありません」を
  動画から外しました。**この一文は、景表法・ステマ規制のための表示**です。
  動画に入っていない以上、**スライド側か、桜木さんの口頭で必ず出してください。**
"""
import json
import os
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))

W, H = 1280, 720
FONT = "Meiryo"
SIZE = 68          # 大きく
MARGIN_V = 64
OUTLINE = 6        # 字が大きくなったぶん、縁取りも太く
BLUR = 3.0
NAME_SIZE = 34

HEAD = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: base,{FONT},{SIZE},&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,-1,0,0,0,100,100,0.8,0,1,{OUTLINE},0,2,50,50,{MARGIN_V},1
Style: name,{FONT},{NAME_SIZE},&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,-1,0,0,0,100,100,0.6,0,1,4,0,1,48,48,{MARGIN_V + 108},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

WIDTH = 18          # 1行あたりの全角文字数


def rewrap(t):
    """大きくしたぶん、1行を短くし直す。最大2行。"""
    t = t.replace("\n", "").strip()
    if len(t) <= WIDTH:
        return t
    for i in range(WIDTH, max(WIDTH - 7, 1), -1):
        if t[i - 1] in "、。？」―":
            return t[:i] + "\n" + t[i:]
    return t[:WIDTH] + "\n" + t[WIDTH:]


def stamp(t):
    h, m = int(t // 3600), int(t % 3600 // 60)
    return f"{h:d}:{m:02d}:{t % 60:05.2f}"


def build_ass(caps, path, dur, who=None):
    with open(path, "w", encoding="utf-8-sig") as f:
        f.write(HEAD)
        if who:
            f.write(f"Dialogue: 0,{stamp(0)},{stamp(dur)},name,,0,0,0,,"
                    f"{{\\blur1.6}}{who}\n")
        for c in caps:
            body = rewrap(c["text"]).replace("\n", r"\N")
            f.write(f"Dialogue: 0,{stamp(c['in'])},{stamp(c['out'])},base,,0,0,0,,"
                    f"{{\\blur{BLUR}}}{body}\n")


def duration(ff, path):
    import re
    r = subprocess.run([ff, "-hide_banner", "-i", path],
                       capture_output=True, text=True, errors="replace")
    m = re.search(r"Duration: (\d+):(\d+):([\d.]+)", r.stderr)
    return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))


def main():
    clip, capj, out = sys.argv[1:4]
    who = sys.argv[4] if len(sys.argv) > 4 else None
    caps = json.load(open(capj, encoding="utf-8"))

    import imageio_ffmpeg
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    ass = os.path.join(HERE, f"_tmp_{os.getpid()}.ass")
    build_ass(caps, ass, duration(ff, clip), who)
    p = ass.replace("\\", "/").replace(":", "\\:")
    # ★先に720pへ拡大してから字を描く。順序が逆だと字までぼやける
    vf = f"scale={W}:{H}:flags=lanczos,subtitles='{p}'"
    subprocess.run([ff, "-y", "-hide_banner", "-loglevel", "error",
                    "-i", clip, "-vf", vf,
                    "-c:v", "libx264", "-preset", "medium", "-crf", "19",
                    "-pix_fmt", "yuv420p", "-c:a", "copy", out], check=True)
    os.remove(ass)
    print(f"判定: ✅ 字幕 {len(caps)}枚 → {os.path.basename(out)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
