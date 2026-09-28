import os, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
JOBS = [
 (f"{HERE}/clips_yukichi/Y8b_一緒にやろうよ.mp4", f"{HERE}/caps_Y8b.json", "ユキチさん", "Y8b_一緒にやろうよ"),
 (f"{HERE}/clips_akarin/A8c_間詰め.mp4",          f"{HERE}/caps_A8c.json", "あかりんさん", "A8c_間詰め"),
]
for src, capj, who, tag in JOBS:
    out = os.path.join(os.path.dirname(src), tag + "_大字幕.mp4")
    r = subprocess.run([sys.executable, os.path.join(HERE, "_burn2.py"), src, capj, out, who],
                       stdin=subprocess.DEVNULL, capture_output=True, text=True, errors="replace")
    print(("  ✅ " if os.path.exists(out) else "  ❌ ") + tag, r.stderr[-200:] if not os.path.exists(out) else "")
