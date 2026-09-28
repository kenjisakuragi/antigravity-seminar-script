# -*- coding: utf-8 -*-
"""Yamakaさんの2本は、カードに名前が出ているので、左下の名前は付けない。"""
import os, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__)); Z = os.path.join(HERE, "zoom0803")
for tag in ("Y5_敷居が高かった", "Y7_一人だと続かない"):
    src = os.path.join(Z, "clips_yamaka", tag + ".mp4")
    out = os.path.join(Z, "clips_yamaka", tag + "_大字幕.mp4")
    subprocess.run([sys.executable, os.path.join(HERE, "_burn2.py"),
                    src, os.path.join(Z, f"caps_{tag}.json"), out],
                   stdin=subprocess.DEVNULL, capture_output=True)
    print(("  ✅ " if os.path.exists(out) else "  ❌ ") + tag)
