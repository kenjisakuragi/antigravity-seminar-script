# -*- coding: utf-8 -*-
"""
generate_upsell_slides.py
レッスン最後に使うアップセル案内スライドを生成
出力: アップセル案内スライド.pptx
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "Google_Slide_generator"))
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from design_v2 import *

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(SCRIPT_DIR, "アップセル案内スライド.pptx")

# カラー：ゴールド系（特別感）
C1 = "D97706"
C2 = "F59E0B"

def build(prs):

    # ─── 1. ブリッジスライド ───
    s = add_slide(prs)
    bg_grad(s, DARK1, "1a1a2e")
    txt(s, Inches(1), Inches(1.8), Inches(11.3), Inches(1.0),
        "🎉 今日もお疲れさまでした！", sz=32, clr=C_GOLD, bold=True, align=PP_ALIGN.CENTER)
    txt(s, Inches(1), Inches(3.2), Inches(11.3), Inches(1.2),
        "最後に、あなたの成長をさらに加速させる\n「次のステップ」をご案内します", sz=22, clr=C_WHITE, align=PP_ALIGN.CENTER)
    footer(s, C1, C2)

    # ─── 2. 「もし〜なら」問いかけ ───
    s = add_slide(prs)
    make_dark_summary(s, "こんなお悩み、ありませんか？", [
        "📈 動画を公開しているが、再生数がなかなか伸びない",
        "🤔 どの収益源に集中すればいいか分からない",
        "⏰ 一人でやっていると方向性を見失ってしまう",
        "💰 まだ収益が月1万円に届いていない",
    ], sub="→ それを解決するために、3つの選択肢があります", c1=C1, c2=C2)

    # ─── 3. 3つの選択肢カード ───
    s = add_slide(prs)
    make_cards_slide(s, "ステップアップの3つの選択肢", [
        ("🎯", "個別コンサル\nプレミアム", "月1回60分\nあなた専用の\n成長プランを作成\n月額 29,800円"),
        ("🚀", "収益化加速コース\n（バックエンド）", "全8回\n月収10万円を\n一緒に達成\n198,000円"),
        ("💬", "卒業生コミュニティ\n（メンバーシップ）", "月1回勉強会＋\n最新AIツール速報\n仲間と走り続ける\n月額 2,980円"),
    ], accent_c1=C1, accent_c2=C2)

    # ─── 4. 個別コンサル 詳細 ───
    s = add_slide(prs)
    make_numbered_slide(s, "🎯 個別コンサルティングプラン 詳細", [
        ("月1回", "60分 1on1 Zoom コンサル",
         "あなたのチャンネル・収益数字を直接見てアドバイス"),
        ("毎回", "「次の一手」を具体的に決める",
         "「何をいつやるか」まで落とし込んで終わる"),
        ("常時", "最新AIツールを厳選して提供",
         "AI業界の変化を、あなたのジャンルで使える形で共有"),
    ], accent_c1=C1, accent_c2=C2)

    s = add_slide(prs)
    bg_grad(s, DARK1, "1a1a2e")
    txt(s, Inches(1), Inches(1.0), Inches(11.3), Inches(0.8),
        "🎯 個別コンサル — 特別オファー", sz=28, clr=C_GOLD, bold=True, align=PP_ALIGN.CENTER)
    txt(s, Inches(2), Inches(2.2), Inches(9.3), Inches(0.8),
        "通常価格", sz=16, clr=C_GRAY, align=PP_ALIGN.CENTER)
    txt(s, Inches(2), Inches(2.9), Inches(9.3), Inches(0.9),
        "月額 29,800円", sz=24, clr=C_GRAY, align=PP_ALIGN.CENTER)
    txt(s, Inches(2), Inches(3.9), Inches(9.3), Inches(1.0),
        "初月トライアル価格", sz=16, clr=C_WHITE, bold=True, align=PP_ALIGN.CENTER)
    txt(s, Inches(2), Inches(4.8), Inches(9.3), Inches(1.2),
        "14,800円（半額）", sz=40, clr=C_GOLD, bold=True, align=PP_ALIGN.CENTER)
    txt(s, Inches(2), Inches(6.0), Inches(9.3), Inches(0.6),
        "定員 4名 ／ 満員の場合はキャンセル待ち", sz=14, clr=C_GRAY, align=PP_ALIGN.CENTER)
    footer(s, C1, C2)

    # ─── 5. 収益化加速コース 詳細 ───
    s = add_slide(prs)
    make_cards_slide(s, "🚀 AI副業 収益化加速コース", [
        ("📊", "STAGE 1\n分析と選択", "収益ダッシュボード\n作成\n集中すべき1つを\n数字で決める"),
        ("📈", "STAGE 2\n収益の深化", "YouTube SEO\nブログSEO\nAI音楽最大化"),
        ("🔄", "STAGE 3〜4\n自動化と完成", "外注化・高単価商品\n月収10万円の\n仕組みを完成"),
    ], accent_c1=C1, accent_c2=C2)

    s = add_slide(prs)
    make_table_slide(s, "🚀 収益化加速コース — 料金・内容", ["項目", "内容"],
        [
            ["全8回ライブ講義", "月2回 × 4ヶ月（Zoom）"],
            ["Discord サポート", "4ヶ月間 無制限"],
            ["特典①", "収益ダッシュボード（スプレッドシート）"],
            ["特典②", "外注化指示書テンプレート"],
            ["特典③", "月次収益シミュレーター（Excel）"],
            ["受講料（一括）", "198,000円"],
            ["受講料（分割）", "55,000円 × 4ヶ月"],
        ], accent_c1=C1, accent_c2=C2, note="📌 月収10万円達成で投資対効果 1.5倍以上")

    # ─── 6. コミュニティ 詳細 ───
    s = add_slide(prs)
    make_cards_slide(s, "💬 卒業生コミュニティ（月額 2,980円）", [
        ("📱", "最新AIツール\n速報", "月4回以上\nあなたのジャンルに\n使えるツールを配信"),
        ("🎙️", "月1回\n勉強会", "90分のライブ\nQ&A＋最新情報\n共有"),
        ("👥", "仲間との\n相互応援", "チャンネルを\n見合って\nコメントし合う"),
    ], accent_c1=C1, accent_c2=C2)

    # ─── 7. テンプレートパック ───
    s = add_slide(prs)
    make_dark_summary(s, "📦 AI副業プロンプト＆テンプレートパック", [
        "✅ YouTube台本・タイトル・説明文・タグ生成プロンプト",
        "✅ AI音声演出プロンプト（4タイプ）",
        "✅ Kindle書籍・表紙・説明文テンプレート",
        "✅ SEOブログ記事生成プロンプト",
        "✅ LINEスタンプ・ストックフォト生成プロンプト",
        "✅ cocnara サービス説明文・やり取りテンプレート",
    ], sub="全100点以上 → 7,980円（コピペするだけ）", c1=C1, c2=C2)

    # ─── 8. まとめ ── どれを選ぶ？ ───
    s = add_slide(prs)
    make_table_slide(s, "✨ あなたに合う選択はどれ？", ["こんな方に", "おすすめ", "価格"],
        [
            ["個別サポートが欲しい・成長を加速させたい", "個別コンサル", "初月 14,800円"],
            ["月収10万円を3〜6ヶ月で達成したい", "収益化加速コース", "198,000円"],
            ["仲間と継続して最新情報を得たい", "コミュニティ", "月額 2,980円"],
            ["まずプロンプトだけ欲しい", "テンプレートパック", "7,980円"],
        ], accent_c1=C1, accent_c2=C2, note="📌 迷ったらまずコミュニティ（月2,980円）から")

    # ─── 9. 申込・QR ───
    s = add_slide(prs)
    bg_grad(s, DARK1, "1a1a2e")
    txt(s, Inches(1), Inches(0.8), Inches(11.3), Inches(0.9),
        "📩 申込・お問い合わせ", sz=30, clr=C_GOLD, bold=True, align=PP_ALIGN.CENTER)
    txt(s, Inches(1.5), Inches(2.0), Inches(10.3), Inches(0.7),
        "① Discord の #アップグレード-相談 に「相談希望」と投稿", sz=18, clr=C_WHITE)
    txt(s, Inches(1.5), Inches(2.9), Inches(10.3), Inches(0.7),
        "② 講師に直接 DM でご連絡", sz=18, clr=C_WHITE)
    txt(s, Inches(1.5), Inches(3.8), Inches(10.3), Inches(0.7),
        "③ 申込フォームから直接お申込み → 〔URL〕", sz=18, clr=C_WHITE)
    txt(s, Inches(1), Inches(5.2), Inches(11.3), Inches(0.7),
        "何かご不明な点があればお気軽にどうぞ！", sz=16, clr=C_GRAY, align=PP_ALIGN.CENTER)
    footer(s, C1, C2)

    # ─── 10. クロージング ───
    s = add_slide(prs)
    bg_grad(s, DARK1, "162544")
    txt(s, Inches(1), Inches(1.5), Inches(11.3), Inches(1.2),
        "継続こそが最大の武器です。", sz=36, clr=C_GOLD, bold=True, align=PP_ALIGN.CENTER)
    txt(s, Inches(1), Inches(3.2), Inches(11.3), Inches(0.9),
        "一人で悩まず、一緒に前に進みましょう。", sz=22, clr=C_WHITE, align=PP_ALIGN.CENTER)
    txt(s, Inches(1), Inches(4.5), Inches(11.3), Inches(0.7),
        "らくらくAI副業キャンパス", sz=18, clr=C_GRAY, align=PP_ALIGN.CENTER)
    footer(s, C1, C2)


if __name__ == "__main__":
    prs = create_prs()
    build(prs)
    prs.save(OUT_PATH)
    print(f"完了！ {len(prs.slides)}枚 → {OUT_PATH}")
