# -*- coding: utf-8 -*-
"""
add_new_slides.py  — 既存PPTXに3枚の新規スライドを追加するスクリプト
  1. 本日限定ボーナス特典
  2. 30日間全額返金保証
  3. 1日150円でスタート（分割払い日割り）
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "Google_Slide_generator"))

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
import copy

# ── 既存PPTXを開く ──
SRC = os.path.join(os.path.dirname(__file__), "AI副業セミナー_v3.pptx")
prs = Presentation(SRC)
SW = prs.slide_width   # slide width
SH = prs.slide_height  # slide height

# ── デザイン定数 ──
DARK1 = RGBColor(0x0F, 0x17, 0x2A)
DARK2 = RGBColor(0x1E, 0x29, 0x3B)
ACCENT1 = RGBColor(0x25, 0x63, 0xEB)
ACCENT2 = RGBColor(0x7C, 0x3A, 0xED)
GOLD = RGBColor(0xFF, 0xD7, 0x00)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
RED = RGBColor(0xDC, 0x26, 0x26)
GREEN = RGBColor(0x10, 0xB9, 0x81)

def add_blank_slide(prs):
    """空白レイアウトのスライドを追加"""
    layout = prs.slide_layouts[6]  # blank layout
    return prs.slides.add_slide(layout)

def set_bg_dark(slide):
    """ダーク背景を設定"""
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = DARK1

def set_bg_gradient(slide, c1_hex="0F172A", c2_hex="1E293B"):
    """グラデーション背景"""
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor.from_string(c1_hex)

def add_text(slide, left, top, width, height, text, font_size=18,
             color=WHITE, bold=False, align=PP_ALIGN.LEFT):
    """テキストボックスを追加"""
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.color.rgb = color
    p.font.bold = bold
    p.alignment = align
    return txBox

def add_rounded_rect(slide, left, top, width, height, fill_color):
    """角丸矩形を追加"""
    from pptx.enum.shapes import MSO_SHAPE
    shape = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        left, top, width, height
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    shape.line.fill.background()
    return shape

# ═══════════════════════════════════════
# スライド1: 本日限定ボーナス特典
# ═══════════════════════════════════════
slide1 = add_blank_slide(prs)
set_bg_dark(slide1)

# タイトル
add_text(slide1, Inches(0.5), Inches(0.3), Inches(12), Inches(0.8),
         "🎁 本日限定ボーナス特典", 36, GOLD, True, PP_ALIGN.CENTER)

# サブタイトル
add_text(slide1, Inches(1), Inches(1.3), Inches(11), Inches(0.6),
         "今日のWEBセミナー中にお申し込みの方だけ", 20, WHITE, False, PP_ALIGN.CENTER)

# メインカード
card1 = add_rounded_rect(slide1, Inches(1.5), Inches(2.2), Inches(10), Inches(2.5),
                          RGBColor(0x1E, 0x40, 0x7A))
add_text(slide1, Inches(2), Inches(2.5), Inches(9), Inches(0.7),
         "『秘蔵プロンプト集 — 収益化特化版 50選』", 28, GOLD, True, PP_ALIGN.CENTER)
add_text(slide1, Inches(2), Inches(3.3), Inches(9), Inches(0.5),
         "（非公開PDF）", 18, WHITE, False, PP_ALIGN.CENTER)
add_text(slide1, Inches(2), Inches(4.0), Inches(9), Inches(0.5),
         "スクール内でも配布していない、実際に収益を出しているプロンプト集", 16, RGBColor(0xA0, 0xAE, 0xC0), False, PP_ALIGN.CENTER)

# 警告バー
warn_bar = add_rounded_rect(slide1, Inches(2), Inches(5.2), Inches(9), Inches(0.8),
                             RGBColor(0xDC, 0x26, 0x26))
add_text(slide1, Inches(2.5), Inches(5.3), Inches(8), Inches(0.6),
         "⚠️ 明日以降のお申し込みでは手に入りません。今日だけです。", 20, WHITE, True, PP_ALIGN.CENTER)

# フッター
add_text(slide1, Inches(0.5), Inches(6.5), Inches(12), Inches(0.5),
         "WEBセミナー限定価格 ¥98,000（本日23:59まで）", 14, RGBColor(0x60, 0x70, 0x80), False, PP_ALIGN.CENTER)


# ═══════════════════════════════════════
# スライド2: 30日間全額返金保証
# ═══════════════════════════════════════
slide2 = add_blank_slide(prs)
set_bg_dark(slide2)

# タイトル
add_text(slide2, Inches(0.5), Inches(0.3), Inches(12), Inches(0.8),
         "🛡️ 30日間 全額返金保証", 36, GREEN, True, PP_ALIGN.CENTER)

# メインメッセージ
add_text(slide2, Inches(1), Inches(1.5), Inches(11), Inches(0.8),
         "30日間しっかり取り組んでみてください。\nそれでも「自分には合わなかった」場合は、全額お返しします。",
         22, WHITE, False, PP_ALIGN.CENTER)

# カード: 理由
reason_card = add_rounded_rect(slide2, Inches(2), Inches(2.8), Inches(9), Inches(1.2),
                                RGBColor(0x06, 0x4E, 0x3B))
add_text(slide2, Inches(2.5), Inches(2.9), Inches(8), Inches(0.5),
         "なぜこんな保証ができるのか？", 18, RGBColor(0x6E, 0xE7, 0xB7), True, PP_ALIGN.CENTER)
add_text(slide2, Inches(2.5), Inches(3.4), Inches(8), Inches(0.5),
         "それだけ、このカリキュラムに自信があるからです。", 22, WHITE, True, PP_ALIGN.CENTER)

# 実績
add_text(slide2, Inches(1.5), Inches(4.5), Inches(10), Inches(0.6),
         "過去の受講生で返金を申請された方はほとんどいません。", 18, RGBColor(0xA0, 0xAE, 0xC0), False, PP_ALIGN.CENTER)

# 結論カード
conclusion = add_rounded_rect(slide2, Inches(3), Inches(5.3), Inches(7), Inches(1.0),
                               RGBColor(0x25, 0x63, 0xEB))
add_text(slide2, Inches(3.5), Inches(5.4), Inches(6), Inches(0.8),
         "📌 リスクはゼロ。得られるものは無限大。", 24, WHITE, True, PP_ALIGN.CENTER)

# フッター
add_text(slide2, Inches(0.5), Inches(6.5), Inches(12), Inches(0.5),
         "WEBセミナー限定価格 ¥98,000（本日23:59まで）", 14, RGBColor(0x60, 0x70, 0x80), False, PP_ALIGN.CENTER)


# ═══════════════════════════════════════
# スライド3: 1日150円でスタート
# ═══════════════════════════════════════
slide3 = add_blank_slide(prs)
set_bg_dark(slide3)

# タイトル
add_text(slide3, Inches(0.5), Inches(0.3), Inches(12), Inches(0.8),
         "💳 1日たった150円で、人生が変わる", 34, WHITE, True, PP_ALIGN.CENTER)

# 大きな価格表示
price_card = add_rounded_rect(slide3, Inches(2.5), Inches(1.5), Inches(8), Inches(2.0),
                               RGBColor(0x25, 0x63, 0xEB))
add_text(slide3, Inches(3), Inches(1.6), Inches(7), Inches(0.5),
         "24回分割払いなら", 20, RGBColor(0xBF, 0xDB, 0xFE), False, PP_ALIGN.CENTER)
add_text(slide3, Inches(3), Inches(2.1), Inches(7), Inches(0.8),
         "月々 約4,500円", 40, GOLD, True, PP_ALIGN.CENTER)
add_text(slide3, Inches(3), Inches(2.9), Inches(7), Inches(0.5),
         "＝ 1日 約150円（コンビニコーヒー1杯分）", 18, WHITE, False, PP_ALIGN.CENTER)

# 比較リスト
comparisons = [
    ("☕ コンビニコーヒー1杯", "150円/日"),
    ("📱 サブスク動画サービス", "約50円/日"),
    ("🎓 AI副業スクール", "150円/日 → 月10万円の可能性"),
]
y_pos = 4.0
for icon_text, price_text in comparisons:
    add_text(slide3, Inches(2), Inches(y_pos), Inches(5), Inches(0.45),
             icon_text, 18, WHITE, False, PP_ALIGN.LEFT)
    add_text(slide3, Inches(7), Inches(y_pos), Inches(4), Inches(0.45),
             price_text, 18, GOLD if "10万" in price_text else RGBColor(0xA0, 0xAE, 0xC0),
             "10万" in price_text, PP_ALIGN.RIGHT)
    y_pos += 0.55

# 結論
add_text(slide3, Inches(1), Inches(5.8), Inches(11), Inches(0.6),
         "コーヒー1杯ガマンするだけで、人生が変わるかもしれない。", 22, WHITE, True, PP_ALIGN.CENTER)

# フッター
add_text(slide3, Inches(0.5), Inches(6.5), Inches(12), Inches(0.5),
         "WEBセミナー限定価格 ¥98,000（本日23:59まで）", 14, RGBColor(0x60, 0x70, 0x80), False, PP_ALIGN.CENTER)


# ── 保存 ──
OUT = os.path.join(os.path.dirname(__file__), "AI副業セミナー_v4.pptx")
prs.save(OUT)
print(f"完了！ 新スライド3枚を追加して保存: {OUT}")
print(f"  スライド総数: {len(prs.slides)}")
