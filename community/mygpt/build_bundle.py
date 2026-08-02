# -*- coding: utf-8 -*-
"""
build_bundle.py — マイGPTに読ませる知識ファイルを1箇所に集める。

なぜ：
　知識の正本は community/bot/knowledge/*.md（Discord botと共用）。
　マイGPTには手でアップロードするので、アップ対象をこのフォルダに揃えておく。
　→ 将来 Discord bot に移行するとき、知識を作り直さなくて済む。

使い方：
　1) 元ネタを更新（tool_registry.py を直したら make_tools_knowledge.py も実行）
　2) python build_bundle.py
　3) community/mygpt/knowledge/ の中身を、マイGPTの「知識」に入れ直す（全差し替え）
"""
import os
import shutil
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.abspath(os.path.join(HERE, "..", "bot", "knowledge"))
DST = os.path.join(HERE, "knowledge")

os.makedirs(DST, exist_ok=True)

# 既存を掃除（消し忘れで古い知識が残るのを防ぐ）
for f in os.listdir(DST):
    if f.endswith(".md"):
        os.remove(os.path.join(DST, f))

n = 0
for f in sorted(os.listdir(SRC)):
    if not f.endswith(".md"):
        continue
    shutil.copy2(os.path.join(SRC, f), os.path.join(DST, f))
    size = os.path.getsize(os.path.join(DST, f))
    print(f"  {f}  ({size:,} bytes)")
    n += 1

total = sum(os.path.getsize(os.path.join(DST, f)) for f in os.listdir(DST))
print(f"\n{n}ファイル / 合計 {total:,} bytes → {DST}")
print("この中身を、マイGPTの「知識」にアップロードしてください（古いものは削除してから）。")
