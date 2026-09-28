# -*- coding: utf-8 -*-
"""説明会で使う14本＋予備3本を、_burn2.py（大きい字幕・上部注記なし）で焼き直す。"""
import os, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__)); Z = os.path.join(HERE, "zoom0803")
# (元クリップ, 字幕json, 話し手)
JOBS = [
 (f"{HERE}/clips_akarin/A2_言い訳にしてきた.mp4",       f"{HERE}/caps_A2_言い訳にしてきた.json",        "あかりんさん"),
 (f"{Z}/clips_yamaka/Y5_敷居が高かった.mp4",            f"{Z}/caps_Y5_敷居が高かった.json",            "Yamakaさん"),
 (f"{HERE}/clips_yukichi/Y4_画像が出てきた瞬間.mp4",    f"{HERE}/caps_Y4_画像が出てきた瞬間.json",     "ユキチさん"),
 (f"{HERE}/clips_akarin/A6_私にもできるんだ.mp4",       f"{HERE}/caps_A6_私にもできるんだ.json",       "あかりんさん"),
 (f"{Z}/clips_yuzu/Z4_死ぬまでに一枚.mp4",              f"{Z}/caps_Z4_死ぬまでに一枚.json",            "ゆずさん"),
 (f"{Z}/clips_yuzu/Z7_自動化の部門を作った.mp4",        f"{Z}/caps_Z7_自動化の部門を作った.json",      "ゆずさん"),
 (f"{HERE}/clips_akarin/A3_ワードプレスで挫折.mp4",     f"{HERE}/caps_A3_ワードプレスで挫折.json",     "あかりんさん"),
 (f"{Z}/clips_shino/S8_人との繋がり.mp4",               f"{Z}/caps_S8_人との繋がり.json",              "しのさん"),
 (f"{Z}/clips_shino/S2_32年前と同じ熱.mp4",             f"{Z}/caps_S2_32年前と同じ熱.json",            "しのさん"),
 (f"{Z}/clips_shino/S1_できんわと思った.mp4",           f"{Z}/caps_S1_できんわと思った.json",          "しのさん"),
 (f"{HERE}/clips_yukichi/Y7_はまれてよかった.mp4",      f"{HERE}/caps_Y7_はまれてよかった.json",       "ユキチさん"),
 (f"{HERE}/clips_yukichi/Y8b.mp4",                      f"{HERE}/caps_Y8b.json",                       "ユキチさん"),
 (f"{Z}/clips_shino/S7_行動するのみ.mp4",               f"{Z}/caps_S7_行動するのみ.json",              "しのさん"),
 (f"{HERE}/clips_akarin/A8c.mp4",                       f"{HERE}/caps_A8c.json",                       "あかりんさん"),
 (f"{Z}/clips_yuzu/Z1_思ってるよりずっとすごい.mp4",    f"{Z}/caps_Z1_思ってるよりずっとすごい.json",  "ゆずさん"),
 (f"{Z}/clips_yuzu/Z5_考えるのをやめて感じる.mp4",      f"{Z}/caps_Z5_考えるのをやめて感じる.json",    "ゆずさん"),
 (f"{Z}/clips_yamaka/Y7_一人だと続かない.mp4",          f"{Z}/caps_Y7_一人だと続かない.json",          "Yamakaさん"),
]
ng = []
for src, capj, who in JOBS:
    tag = os.path.splitext(os.path.basename(src))[0]
    if not os.path.exists(src) or not os.path.exists(capj):
        ng.append((tag, os.path.exists(src), os.path.exists(capj))); continue
    out = os.path.join(os.path.dirname(src), tag + "_大字幕.mp4")
    subprocess.run([sys.executable, os.path.join(HERE, "_burn2.py"), src, capj, out, who],
                   stdin=subprocess.DEVNULL, capture_output=True)
    print(("  ✅ " if os.path.exists(out) else "  ❌ ") + tag)
if ng:
    print("\n見つからない:", ng)
