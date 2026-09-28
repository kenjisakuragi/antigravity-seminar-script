# -*- coding: utf-8 -*-
"""
_collect_final.py — 説明会で使う動画だけを、1つのフォルダに集める。

  python _collect_final.py

Canvaに上げるとき、フォルダを3つ行き来しなくて済むように。
**流す順に番号を振る**ので、そのまま並び順として使える。

元は消さない。コピーするだけ。
"""
import os
import shutil
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
Z = os.path.join(HERE, "zoom0803")
TIGHT = os.path.join(HERE, "_tight")     # 間詰め＋字幕焼きが済んだもの
OUT = os.path.join(HERE, "_説明会で使う動画")

# 2026/8/4 更新：字幕を大きくし、上の注記を外した版（*_大字幕.mp4）に切り替え

# (番号, 入れる場所, 元ファイル, 話し手, 中身)
USE = [
    ("01", "10ページ直後", f"{TIGHT}/A2_言い訳にしてきた_完成.mp4",
     "あかりんさん", "言い訳にしてきた"),
    ("02", "16ページ直後", f"{TIGHT}/Y5_敷居が高かった_完成.mp4",
     "Yamakaさん", "敷居が高かった（声のみ）"),
    ("03", "24ページ直後1", f"{TIGHT}/Y4_画像が出てきた瞬間_完成.mp4",
     "ユキチさん", "画像が出てきた瞬間"),
    ("04", "24ページ直後2", f"{TIGHT}/A6_私にもできるんだ_完成.mp4",
     "あかりんさん", "私にもできるんだ"),
    ("05", "29ページ直後", f"{TIGHT}/Z4_死ぬまでに一枚_完成.mp4",
     "ゆずさん", "死ぬまでに一枚（顔ぼかし）"),
    ("06", "36ページ直後", f"{TIGHT}/Z7_自動化の部門を作った_完成.mp4",
     "ゆずさん", "自動化の部門を作った（顔ぼかし）"),
    ("07", "45ページ直後", f"{TIGHT}/A3_ワードプレスで挫折_完成.mp4",
     "あかりんさん", "ワードプレスで挫折"),
    ("08", "51ページ直後", f"{TIGHT}/S8_人との繋がり_完成.mp4",
     "しのさん", "人との繋がり"),
    ("09", "60ページ", f"{TIGHT}/S2_32年前と同じ熱_完成.mp4",
     "しのさん", "32年前と同じ熱"),
    ("10", "61ページ", f"{TIGHT}/S1_できんわと思った_完成.mp4",
     "しのさん", "できんわと思った"),
    ("11", "67ページ直後1", f"{TIGHT}/Y7_はまれてよかった_完成.mp4",
     "ユキチさん", "はまれてよかった"),
    ("12", "67ページ直後2", f"{TIGHT}/Y8b_一緒にやろうよ_完成.mp4",
     "ユキチさん", "一緒にやろうよ"),
    ("13", "68ページ直前1", f"{TIGHT}/S7_行動するのみ_完成.mp4",
     "しのさん", "行動するのみ"),
    ("14", "68ページ直前2", f"{TIGHT}/A8c_大丈夫だよ_完成.mp4",
     "あかりんさん", "大丈夫だよ"),
]

# 時間に余裕があれば使うもの
SPARE = [
    ("予備1", f"{TIGHT}/Z1_思ってるよりずっとすごい_完成.mp4",
     "ゆずさん", "思ってるよりずっとすごい（69ページあたり）"),
    ("予備2", f"{TIGHT}/Z5_考えるのをやめて感じる_完成.mp4",
     "ゆずさん", "考えるのをやめて感じる（18〜22ページ）"),
    ("予備3", f"{TIGHT}/Y7_一人だと続かない_完成.mp4",
     "Yamakaさん", "一人だと続かない（特典③の説明）"),
]


def main():
    # ⚠️ フォルダごと消すと、中に置いた「はじめにお読みください.md」まで消える（実際消した）。
    #    消すのは動画だけにする。
    os.makedirs(os.path.join(OUT, "予備"), exist_ok=True)
    for d in (OUT, os.path.join(OUT, "予備")):
        for f in os.listdir(d):
            if f.lower().endswith(".mp4"):
                os.remove(os.path.join(d, f))

    total = 0.0
    missing = []
    for no, where, src, who, what in USE:
        if not os.path.exists(src):
            missing.append(src); continue
        name = f"{no}_{where}_{who}_{what}.mp4"
        dst = os.path.join(OUT, name)
        shutil.copy2(src, dst)
        mb = os.path.getsize(dst) / 1e6
        total += mb
        print(f"  {name}   {mb:.1f}MB")

    print()
    for no, src, who, what in SPARE:
        if not os.path.exists(src):
            missing.append(src); continue
        name = f"{no}_{who}_{what}.mp4"
        dst = os.path.join(OUT, "予備", name)
        shutil.copy2(src, dst)
        print(f"  予備/{name}")

    if missing:
        print("\n判定: ❌ 見つからないファイルがあります")
        for m in missing:
            print("   ", m)
        return 1

    print(f"\n判定: OK  本編14本（{total:.0f}MB）＋予備3本 → {os.path.basename(OUT)}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
