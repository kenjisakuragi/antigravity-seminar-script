# -*- coding: utf-8 -*-
"""しのさんの9本に、字幕の下書きを作る（日本語パスをシェルに渡さないため）。"""
import glob, os, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
os.environ.setdefault("SSL_CERT_FILE", os.path.join(HERE, "_win_roots.pem"))
py = sys.executable
clips = sorted(glob.glob(os.path.join(HERE, "zoom0803", "clips_shino", "*.mp4")))
print(f"{len(clips)}本に字幕下書きを作ります")
for c in clips:
    tag = os.path.splitext(os.path.basename(c))[0]
    out = os.path.join(HERE, "zoom0803", f"caps_{tag}.json")
    if os.path.exists(out):
        print("  済:", tag); continue
    r = subprocess.run([py, os.path.join(HERE, "_captions.py"), c, out],
                       stdin=subprocess.DEVNULL, capture_output=True)
    print(("  OK " if os.path.exists(out) else "  NG ") + tag)
