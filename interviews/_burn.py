# -*- coding: utf-8 -*-
"""
_burn.py — クリップに字幕を焼き込む。

  python _burn.py <クリップ.mp4> <字幕.json> <出力.mp4>

字幕.json の形（時刻は秒）
  [{"in":0.5, "out":7.9, "text":"1行目\n2行目"}, ...]

■ 見た目（桜木さん指定）
  白の太ゴシック（メイリオ Bold）＋黒のグロー。
  グローは、黒の太い縁取りに ぼかし を掛けて出す。
  くっきりした縁取りだけだと硬いので、ぼかしを少し入れて字を浮かせる。

■ 書き起こしのままにしない
  話し言葉は、読むと不自然になる。字幕は「読んで意味が通る形」に直す。
  ただし、言っていないことは足さない。
"""
import json
import os
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))

W, H = 1280, 720
FONT = "Meiryo"
SIZE = 42
MARGIN_V = 54
OUTLINE = 4        # 黒の縁取りの太さ
BLUR = 2.4         # 縁取りのぼかし＝グロー感

# 説明会で流すときに、画面に出したままにする注記（景表法・ステマ規制）
# 上の黒帯に置くので、映像は隠れない。
NOTE = ("前身講座（らくらくAI副業キャンパス）卒業生の声です　／　"
        "個人の感想です。成果を保証するものではありません")
NOTE_SIZE = 20

HEAD = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: base,{FONT},{SIZE},&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,-1,0,0,0,100,100,0.6,0,1,{OUTLINE},0,2,60,60,{MARGIN_V},1
Style: note,{FONT},{NOTE_SIZE},&H00C8C8C8,&H00C8C8C8,&H00000000,&H00000000,0,0,0,0,100,100,0.4,0,1,2,0,8,40,40,14,1
Style: name,{FONT},26,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,-1,0,0,0,100,100,0.6,0,1,3,0,1,56,56,{MARGIN_V + 62},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


def stamp(t):
    h, m = int(t // 3600), int(t % 3600 // 60)
    return f"{h:d}:{m:02d}:{t % 60:05.2f}"


def build_ass(caps, path, dur, who=None):
    with open(path, "w", encoding="utf-8-sig") as f:
        f.write(HEAD)
        # 注記は最初から最後まで出しっぱなし
        f.write(f"Dialogue: 0,{stamp(0)},{stamp(dur)},note,,0,0,0,,{NOTE}\n")
        if who:
            f.write(f"Dialogue: 0,{stamp(0)},{stamp(dur)},name,,0,0,0,,"
                    f"{{\\blur1.6}}{who}\n")
        for c in caps:
            body = c["text"].replace("\n", r"\N")
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
    who = sys.argv[4] if len(sys.argv) > 4 else None   # 話し手の表示名
    caps = json.load(open(capj, encoding="utf-8"))

    import imageio_ffmpeg
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    ass = os.path.join(HERE, "_tmp.ass")
    build_ass(caps, ass, duration(ff, clip), who)
    # subtitles フィルタに渡すパスは、コロンとバックスラッシュを逃がす必要がある
    p = ass.replace("\\", "/").replace(":", "\\:")
    subprocess.run([ff, "-y", "-hide_banner", "-loglevel", "error",
                    "-i", clip, "-vf", f"subtitles='{p}'",
                    "-c:v", "libx264", "-preset", "medium", "-crf", "19",
                    "-c:a", "copy", out], check=True)
    os.remove(ass)
    print(f"判定: ✅ 字幕 {len(caps)}枚を焼き込みました → {os.path.basename(out)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
