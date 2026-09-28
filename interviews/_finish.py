# -*- coding: utf-8 -*-
"""
_finish.py — クリップを「間詰め → 字幕の時刻を繰り上げ → 焼き込み」の順で仕上げる。

  python interviews/_finish.py

■ 順序が大事
  字幕を焼いたあとに間詰めすると、映像だけ縮んで**字幕がずれる**。
  必ず、間詰めしてから焼く。

■ 間詰めの方針（_tighten.py と同じ）
  3秒を超える無音だけ、1.2秒に詰める。語と語のあいだは詰めない（ジェットカットはしない）。
  考えている間（3秒以内）は、そのまま残す。
"""
import json
import os
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable

# (クリップの場所, 素材名, 字幕json, 表示名)
JOBS = [
    ("clips_akarin", "A3_ワードプレスで挫折", "caps_A3_ワードプレスで挫折.json", "あかりんさん"),
    ("clips_akarin", "A5_いいねをもらえた", "caps_A5_いいねをもらえた.json", "あかりんさん"),
    ("clips_akarin", "A6_私にもできるんだ", "caps_A6_私にもできるんだ.json", "あかりんさん"),
    ("clips_yukichi", "Y4_画像が出てきた瞬間", "caps_Y4_画像が出てきた瞬間.json", "ユキチさん"),
    ("clips_yukichi", "Y5_写真集を作っている", "caps_Y5_写真集を作っている.json", "ユキチさん"),
    ("clips_yukichi", "Y7_はまれてよかった", "caps_Y7_はまれてよかった.json", "ユキチさん"),
    ("clips_yukichi", "Y8b_一緒にやろうよ", "caps_Y8b.json", "ユキチさん"),
]


def run(args):
    r = subprocess.run([PY] + args, cwd=HERE, capture_output=True,
                       text=True, errors="replace")
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def main():
    for folder, name, caps, who in JOBS:
        src = os.path.join(HERE, folder, name + ".mp4")
        tight = os.path.join(HERE, folder, name + "_間詰め.mp4")
        caps2 = os.path.join(HERE, "_t_" + caps)
        out = os.path.join(HERE, folder, name + "_字幕入り.mp4")

        if os.path.exists(caps2):
            os.remove(caps2)
        run([os.path.join(HERE, "_tighten.py"), src, tight,
             os.path.join(HERE, caps), caps2])
        # 判定は**ファイルができたかどうか**で行う。
        # 子プロセスの日本語出力は化けることがあり、文字列一致は当てにならない。
        cut = os.path.exists(caps2) and os.path.exists(tight)
        if not cut:
            tight, caps2 = src, os.path.join(HERE, caps)   # 詰める箇所なし
        print(f"  {name}  {'間を詰めました' if cut else '詰めるところなし'}")

        code, log2 = run([os.path.join(HERE, "_burn.py"), tight, caps2, out, who])
        print(f"    → {'✅ 焼き込みOK' if code == 0 else '❌ ' + log2[-200:]}")
        if cut and os.path.exists(caps2):
            os.remove(caps2)
    print("\n判定: ✅ 仕上げ完了")
    return 0


if __name__ == "__main__":
    sys.exit(main())
