# -*- coding: utf-8 -*-
import glob, os, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(HERE, "zoom0803")
py = sys.executable
for c in sorted(glob.glob(os.path.join(D, "clips_yamaka", "*.mp4"))):
    if "字幕入り" in c: continue
    tag = os.path.splitext(os.path.basename(c))[0]
    capj = os.path.join(D, f"caps_{tag}.json")
    out = os.path.join(D, "clips_yamaka", tag + "_字幕入り.mp4")
    subprocess.run([py, os.path.join(HERE, "_burn.py"), c, capj, out, "Yamakaさん"],
                   stdin=subprocess.DEVNULL, capture_output=True)
    ok = os.path.exists(out)
    print(("  ✅ " if ok else "  ❌ ") + tag + (f"  {os.path.getsize(out)/1e6:.1f}MB" if ok else ""))
