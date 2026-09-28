# -*- coding: utf-8 -*-
"""しのさんの9本に字幕を焼く（日本語パスをシェルに渡さないため、ここに書く）。"""
import glob, os, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, "zoom0803")
py = sys.executable
clips = sorted(glob.glob(os.path.join(D, "clips_shino", "*.mp4")))
clips = [c for c in clips if "字幕入り" not in c]
for c in clips:
    tag = os.path.splitext(os.path.basename(c))[0]
    capj = os.path.join(D, f"caps_{tag}.json")
    out = os.path.join(D, "clips_shino", tag + "_字幕入り.mp4")
    if not os.path.exists(capj):
        print("  字幕なし:", tag); continue
    subprocess.run([py, os.path.join(HERE, "_burn.py"), c, capj, out, "しのさん"],
                   stdin=subprocess.DEVNULL, capture_output=True)
    ok = os.path.exists(out)
    print(("  ✅ " if ok else "  ❌ ") + tag + (f"  {os.path.getsize(out)/1e6:.1f}MB" if ok else ""))
