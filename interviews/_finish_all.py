# -*- coding: utf-8 -*-
"""
_finish_all.py — 説明会で使う14本を、間詰め→字幕焼きまで一気に仕上げる。

  python _finish_all.py

順番が大事：**間を詰めてから、字幕を焼く。**
逆にすると、詰めたぶんだけ字幕がずれる。
"""
import os, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__)); Z = os.path.join(HERE, "zoom0803")
TMP = os.path.join(HERE, "_tight"); os.makedirs(TMP, exist_ok=True)

# (元クリップ, 字幕json, 話し手, 出力名)
JOBS = [
 (f"{HERE}/clips_akarin/A2_言い訳にしてきた.mp4",    f"{HERE}/caps_A2_言い訳にしてきた.json",    "あかりんさん", "A2_言い訳にしてきた"),
 (f"{Z}/clips_yamaka/Y5_敷居が高かった.mp4",         f"{Z}/caps_Y5_敷居が高かった.json",         None,          "Y5_敷居が高かった"),
 (f"{HERE}/clips_yukichi/Y4_画像が出てきた瞬間.mp4", f"{HERE}/caps_Y4_画像が出てきた瞬間.json", "ユキチさん",  "Y4_画像が出てきた瞬間"),
 (f"{HERE}/clips_akarin/A6_私にもできるんだ.mp4",    f"{HERE}/caps_A6_私にもできるんだ.json",    "あかりんさん", "A6_私にもできるんだ"),
 (f"{Z}/clips_yuzu/Z4_死ぬまでに一枚.mp4",           f"{Z}/caps_Z4_死ぬまでに一枚.json",         "ゆずさん",    "Z4_死ぬまでに一枚"),
 (f"{Z}/clips_yuzu/Z7_自動化の部門を作った.mp4",     f"{Z}/caps_Z7_自動化の部門を作った.json",   "ゆずさん",    "Z7_自動化の部門を作った"),
 (f"{HERE}/clips_akarin/A3_ワードプレスで挫折.mp4",  f"{HERE}/caps_A3_ワードプレスで挫折.json",  "あかりんさん", "A3_ワードプレスで挫折"),
 (f"{Z}/clips_shino/S8_人との繋がり.mp4",            f"{Z}/caps_S8_人との繋がり.json",           "しのさん",    "S8_人との繋がり"),
 (f"{Z}/clips_shino/S2_32年前と同じ熱.mp4",          f"{Z}/caps_S2_32年前と同じ熱.json",         "しのさん",    "S2_32年前と同じ熱"),
 (f"{Z}/clips_shino/S1_できんわと思った.mp4",        f"{Z}/caps_S1_できんわと思った.json",       "しのさん",    "S1_できんわと思った"),
 (f"{HERE}/clips_yukichi/Y7_はまれてよかった.mp4",   f"{HERE}/caps_Y7_はまれてよかった.json",    "ユキチさん",  "Y7_はまれてよかった"),
 (f"{HERE}/clips_yukichi/Y8b_一緒にやろうよ.mp4",    f"{HERE}/caps_Y8b.json",                    "ユキチさん",  "Y8b_一緒にやろうよ"),
 (f"{Z}/clips_shino/S7_行動するのみ.mp4",            f"{Z}/caps_S7_行動するのみ.json",           "しのさん",    "S7_行動するのみ"),
 (f"{HERE}/clips_akarin/A8c_間詰め.mp4",             f"{HERE}/caps_A8c.json",                    "あかりんさん", "A8c_大丈夫だよ"),
 # 予備
 (f"{Z}/clips_yuzu/Z1_思ってるよりずっとすごい.mp4", f"{Z}/caps_Z1_思ってるよりずっとすごい.json","ゆずさん",   "Z1_思ってるよりずっとすごい"),
 (f"{Z}/clips_yuzu/Z5_考えるのをやめて感じる.mp4",   f"{Z}/caps_Z5_考えるのをやめて感じる.json", "ゆずさん",    "Z5_考えるのをやめて感じる"),
 (f"{Z}/clips_yamaka/Y7_一人だと続かない.mp4",       f"{Z}/caps_Y7_一人だと続かない.json",       None,          "Y7_一人だと続かない"),
]

for src, capj, who, name in JOBS:
    if not os.path.exists(src) or not os.path.exists(capj):
        print(f"  ❌ 元がない: {name}"); continue
    tc = os.path.join(TMP, name + ".mp4")
    tj = os.path.join(TMP, name + ".json")
    r = subprocess.run([sys.executable, os.path.join(HERE, "_tighten2.py"), src, capj, tc, tj],
                       stdin=subprocess.DEVNULL, capture_output=True, text=True, errors="replace")
    if r.returncode == 2 or not os.path.exists(tc):     # 詰めるところが無い
        tc, tj = src, capj
        note = "そのまま"
    else:
        note = r.stdout.strip().replace("\n", " ")
    out = os.path.join(TMP, name + "_完成.mp4")
    cmd = [sys.executable, os.path.join(HERE, "_burn2.py"), tc, tj, out]
    if who: cmd.append(who)
    subprocess.run(cmd, stdin=subprocess.DEVNULL, capture_output=True)
    print(f"  {'✅' if os.path.exists(out) else '❌'} {name:26s} {note}")
