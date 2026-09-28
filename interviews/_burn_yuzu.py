# -*- coding: utf-8 -*-
import glob, os, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(HERE, "zoom0803")
for c in sorted(glob.glob(os.path.join(D, "clips_yuzu", "*.mp4"))):
    if "字幕入り" in c: continue
    tag = os.path.splitext(os.path.basename(c))[0]
    out = os.path.join(D, "clips_yuzu", tag + "_字幕入り.mp4")
    subprocess.run([sys.executable, os.path.join(HERE, "_burn.py"), c,
                    os.path.join(D, f"caps_{tag}.json"), out, "ゆずさん"],
                   stdin=subprocess.DEVNULL, capture_output=True)
    ok = os.path.exists(out)
    print(("  ✅ " if ok else "  ❌ ") + tag + (f"  {os.path.getsize(out)/1e6:.1f}MB" if ok else ""))
