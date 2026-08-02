# -*- coding: utf-8 -*-
"""
make_tools_knowledge.py — tool_registry.py から、botの知識ファイルを生成する。

なぜ：
　講義動画では、細かい画面操作を扱わない方針にした（陳腐化するため）。
　そのぶん「分からない → サポートAIに聞く」が、受講生の主な逃げ道になる。
　つまり bot が各ツールを答えられないと、この導線は機能しない。

運用：
　ツールの情報が変わったら v2_videos/tool_registry.py を直して、これを実行 →
　Discordで「!reload」。動画もスライドも作り直さない。

実行：
　python make_tools_knowledge.py
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(REPO, "v2_videos"))

from tool_registry import TOOLS, LAST_VERIFIED, GENERIC_STEPS  # noqa: E402

OUT = os.path.join(HERE, "knowledge", "tools_ai_video.md")

ORDER = [
    ("まず無料で試す", ["capcut", "canva", "myedit", "vidnoz"]),
    ("日本語で、もう一歩すすめたい", ["dreamina"]),
    ("顔出しなしで、話す動画", ["heygen"]),
    ("【上級】英語でもいいから、もっと安く量産したい", ["atlas"]),
]

lines = [
    "# AI動画コースで紹介しているツール",
    f"（最終確認日：{LAST_VERIFIED}）",
    "",
    "## 答えるときの前提",
    "- 講義動画では、**ボタンの場所や金額は、あえて説明していません**。画面がよく変わるためです。",
    "- なので「動画で言っていた画面と違う」という質問は、よくあります。**受講生のミスではありません**。",
    "  まず、そう伝えて安心させてから、下の『大きな流れ』に沿って案内してください。",
    "- 具体的な金額を聞かれたら、断定せずに「最新ツールシート」か公式ページをご案内する。",
    "- 画面の細部が分からないときは、無理に推測しない。Discordの質問チャンネルへ、やわらかくつなぐ。",
    "",
    "## どのツールでも共通の「大きな流れ」",
]
for i, st in enumerate(GENERIC_STEPS, 1):
    lines.append(f"{i}. {st['main']} — {st['note']}")
lines += [
    "",
    "この5つの順番は、サービスが変わっても、まず変わりません。",
    "「いま何番目で止まっていますか？」と聞くと、切り分けやすいです。",
    "",
    "---",
    "",
]

for section, keys in ORDER:
    lines.append(f"## {section}")
    lines.append("")
    for k in keys:
        d = TOOLS[k]
        lines.append(f"### {d['name']}")
        lines.append(f"- できること：{d['stable_what']}")
        lines.append(f"- 使うもの：{d['device']}")
        lines.append(f"- お金のかたち：{d['cost_type']}")
        if d.get("cost_hint"):
            lines.append(f"- 目安：{d['cost_hint']}")
        if d.get("must_say"):
            lines.append(f"- **必ず伝えること**：{d['must_say']}")
        lines.append(f"- 公式：{d['url']}")
        lines.append("")

lines += [
    "---",
    "",
    "## よくある質問",
    "",
    "**Q. 動画と画面が違います**",
    "A. サービス側が変わっただけで、受講生のせいではない、とまず伝える。"
    "そのうえで「大きな流れ」の何番目かを一緒に確認する。",
    "",
    "**Q. おしゃべりAI（ChatGPTなど）で動画は作れますか**",
    "A. 基本的に作れない。動画は動画用のサービスを使う、と案内する。",
    "",
    "**Q. 無料のままで大丈夫ですか**",
    "A. 個人で楽しむ範囲なら、無料でじゅうぶん。"
    "ただし副業＝お仕事として使うなら、有料プランに切りかえれば商用にも使える、と伝える。",
    "",
    "**Q. 透かしを消したい**",
    "A. 有料プランに切りかえると消える。金額は変わりやすいので公式で確認をご案内。",
    "",
    "**Q. どれを使えばいいですか**",
    "A. まず無料（CapCut／Canva）。もう一歩なら Dreamina。話す動画なら HeyGen。"
    "全部やる必要はない、気になった1つから、と伝える。",
]

with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")

print(f"作成しました：{OUT}")
