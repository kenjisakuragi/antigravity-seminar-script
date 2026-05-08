# -*- coding: utf-8 -*-
from pptx import Presentation
import os
d = r"c:\Users\yanagi\antigravity\seminar_script"
fs = sorted([f for f in os.listdir(d) if f.endswith(".pptx") and "v2" not in f and "セミナー" not in f])
t = 0
for f in fs:
    n = len(Presentation(os.path.join(d, f)).slides)
    t += n
    print(f"{f:45s} {n:3d} slides")
print(f"\nTotal: {t} slides across {len(fs)} files")
