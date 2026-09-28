# -*- coding: utf-8 -*-
"""
_captions.py — クリップから、字幕の下書き（caps json）を作る。

  python _captions.py <クリップ.mp4> <出力.json>
  python _captions.py clips_akarin/*.mp4          # まとめて（caps_<名前>.json に出す）

■ なぜ通しのSRTを使わないか
  通し書き起こしのSRTは、時刻が2秒刻みで粗く、無音でも引き伸ばされる。
  焼き込むと字がずれて見えるので、クリップ単位で単語ごとの時刻を取り直す。

■ 出てくるのは「下書き」
  文言は話し言葉のままなので、**必ず手で直す**。
  読んで意味が通る形に。ただし、言っていないことは足さない。

■ 分け方
  1枚あたり全角24文字くらい、最長4秒。長い文は、句読点で切る。
  無音が2秒以上あいたら、そこで必ず切る（間は字幕を出さない）。
"""
import glob
import json
import os
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))

MAX_CHARS = 24
MAX_SEC = 4.2
BREAK_AT = "、。？！"

_model = None


def model():
    global _model
    if _model is None:
        from faster_whisper import WhisperModel
        _model = WhisperModel("medium", device="cpu", compute_type="int8")
    return _model


def words_of(clip):
    import imageio_ffmpeg
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    # 同時に2つ動かしても壊れないよう、クリップごとに別名にする
    # （固定名にしていたら、先に終わったほうが後続の作業ファイルを消した）
    tag = os.path.splitext(os.path.basename(clip))[0]
    wav = os.path.join(HERE, f"_cap_{tag}.wav")
    subprocess.run([ff, "-y", "-hide_banner", "-loglevel", "error",
                    "-i", clip, "-vn", "-ac", "1", "-ar", "16000", wav], check=True)
    segs, _ = model().transcribe(wav, language="ja", word_timestamps=True,
                                 vad_filter=False, beam_size=5)
    out = []
    for s in segs:
        for w in (s.words or []):
            out.append((w.start, w.end, w.word))
    os.remove(wav)
    return out


def pack(words):
    """単語を、読める大きさの字幕に詰めていく。"""
    caps, cur = [], None
    for st, en, w in words:
        w = w.strip()
        if not w:
            continue
        if cur is None:
            cur = {"in": st, "out": en, "words": [w]}
            continue
        gap = st - cur["out"]
        joined = "".join(cur["words"])
        too_long = len(joined) >= MAX_CHARS or (en - cur["in"]) > MAX_SEC
        # 2秒以上の間は、必ず切る（考えている間に字幕を残さない）
        if gap >= 2.0 or too_long:
            caps.append(cur)
            cur = {"in": st, "out": en, "words": [w]}
            continue
        cur["words"].append(w)
        cur["out"] = en
        # 句読点まで来ていて、そこそこ長ければ、いったん切る
        if w and w[-1] in BREAK_AT and len(joined) + len(w) >= MAX_CHARS * 0.6:
            caps.append(cur)
            cur = None
    if cur:
        caps.append(cur)

    for c in caps:
        c["text"] = fold(c.pop("words"))
        c["in"] = round(c["in"], 2)
        c["out"] = round(c["out"] + 0.25, 2)   # 語尾が切れないよう、少し伸ばす
    return caps


def fold(words):
    """単語のまとまりを、1〜2行に折る。
    　 **単語の途中では絶対に折らない。** 文字数で機械的に割ると
    　 「触ってみたこ／とは」のような読めない改行になる。"""
    lines, cur = [], ""
    for w in words:
        # 句読点まで来ていて、そこそこ長ければ、そこで行を変える
        if cur and (len(cur) + len(w) > 17 or
                    (cur[-1] in BREAK_AT and len(cur) >= 10)):
            lines.append(cur)
            cur = w
        else:
            cur += w
    if cur:
        lines.append(cur)
    # 3行以上になったら、2行に詰め直す（字幕は2行まで）
    while len(lines) > 2:
        i = min(range(len(lines) - 1),
                key=lambda k: len(lines[k]) + len(lines[k + 1]))
        lines[i:i + 2] = [lines[i] + lines[i + 1]]
    return "\n".join(lines)


def main():
    args = sys.argv[1:]
    if len(args) == 2 and args[1].endswith(".json"):
        pairs = [(args[0], args[1])]
    else:
        pairs = []
        for c in args:
            base = os.path.splitext(os.path.basename(c))[0]
            pairs.append((c, os.path.join(HERE, f"caps_{base}.json")))

    for clip, out in pairs:
        if os.path.exists(out):
            print(f"  {os.path.basename(out)} 済み（消せば作り直します）")
            continue
        caps = pack(words_of(clip))
        json.dump(caps, open(out, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
        print(f"  {os.path.basename(out)}  字幕{len(caps)}枚")
    print("\n判定: ✅ 下書きができました。文言は手で直してください")
    return 0


if __name__ == "__main__":
    sys.exit(main())
