# -*- coding: utf-8 -*-
"""
export_lecture02_to_word.py — 第2回講義読み原稿をWord形式に変換
"""
import sys, os, re

# python-docxのインストール確認
try:
    from docx import Document
    from docx.shared import Inches, Pt, Cm, RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.enum.style import WD_STYLE_TYPE
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "python-docx"])
    from docx import Document
    from docx.shared import Inches, Pt, Cm, RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.enum.style import WD_STYLE_TYPE

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MD_PATH = os.path.join(SCRIPT_DIR, "lecture_script_02.md")
OUT_PATH = os.path.join(SCRIPT_DIR, "セミナー読み原稿_第2回_v3.docx")

# ── マークダウン読み込み ──
with open(MD_PATH, "r", encoding="utf-8") as f:
    lines = f.readlines()

# ── Word ドキュメント作成 ──
doc = Document()

# ── スタイル設定 ──
style = doc.styles['Normal']
font = style.font
font.name = 'メイリオ'
font.size = Pt(11)
style.paragraph_format.line_spacing = 1.5

# Heading styles
for i in range(1, 4):
    h_style = doc.styles[f'Heading {i}']
    h_style.font.name = 'メイリオ'
    h_style.font.color.rgb = RGBColor(0x1A, 0x1A, 0x2E)

# ── 表紙 ──
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run("\n\n\n")
run.font.size = Pt(14)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run("AI副業セミナー 第2回")
run.font.size = Pt(28)
run.font.bold = True
run.font.color.rgb = RGBColor(0x25, 0x63, 0xEB)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run("AI動画① 台本も画像もAIにおまかせ")
run.font.size = Pt(18)
run.font.bold = True
run.font.color.rgb = RGBColor(0x60, 0x60, 0x60)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run("\n読み原稿（120分バージョン）")
run.font.size = Pt(22)
run.font.bold = True

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run("\n\n\n※ 本原稿は seminar_script_policy.md の方針に基づいて作成")
run.font.size = Pt(10)
run.font.color.rgb = RGBColor(0x99, 0x99, 0x99)

doc.add_page_break()

# ── 記号凡例ページ ──
doc.add_heading("記号凡例", level=1)
legend_items = [
    ("【間 ○秒】", "指定秒数の沈黙を取る"),
    ("【スライド切替】", "次のスライドに進む合図"),
    ("【実演開始】〜【実演終了】", "デモンストレーション区間"),
    ("【声のトーン：↑】", "テンションを上げて話す"),
    ("【声のトーン：↓】", "落ち着いた声で話す"),
    ("【ゆっくり】", "重要ポイント、ゆっくり読む"),
    ("📌", "特に強調して読む箇所"),
    ("※", "補足説明（読み飛ばし可）"),
]
table = doc.add_table(rows=len(legend_items) + 1, cols=2)
table.style = 'Light Grid Accent 1'
# Header
table.rows[0].cells[0].text = "記号"
table.rows[0].cells[1].text = "意味"
for cell in table.rows[0].cells:
    for par in cell.paragraphs:
        for run in par.runs:
            run.font.bold = True
# Data
for i, (sym, desc) in enumerate(legend_items, 1):
    table.rows[i].cells[0].text = sym
    table.rows[i].cells[1].text = desc

doc.add_page_break()

# ── 本文変換 ──
def add_styled_paragraph(doc, text, is_stage_direction=False):
    """テキストを解析してスタイル付きパラグラフを追加"""
    p = doc.add_paragraph()
    
    if is_stage_direction:
        p.paragraph_format.left_indent = Cm(1)
        run = p.add_run(text)
        run.font.size = Pt(9)
        run.font.color.rgb = RGBColor(0x00, 0x80, 0x00)
        run.font.italic = True
        return
    
    # **bold** パターンを処理
    parts = re.split(r'(\*\*[^*]+\*\*)', text)
    for part in parts:
        if part.startswith('**') and part.endswith('**'):
            run = p.add_run(part[2:-2])
            run.font.bold = True
        else:
            run = p.add_run(part)
    
    return p

for line in lines:
    line = line.rstrip('\r\n')
    
    # 空行
    if not line.strip():
        continue
    
    # セパレータ (---) をスキップ
    if line.strip() == '---':
        continue
    
    # ━ セクション区切り
    if line.startswith('# ━'):
        continue
    
    # H1
    if line.startswith('# 第') or line.startswith('# 補足') or line.startswith('# 原稿') or line.startswith('# 概要') or line.startswith('# オープニング') or line.startswith('# セクション') or line.startswith('# クロージング') or line.startswith('# 講義'):
        # Just use bold paragraph for fake H1 instead of page break if not matching specific start
        title = line.lstrip('# ').strip()
        doc.add_heading(title, level=1)
        continue
    
    # H2 (## スライドタイトル)
    if line.startswith('## '):
        title = line.lstrip('# ').strip()
        doc.add_heading(title, level=2)
        continue
        
    # H3 (### サブタイトル)
    if line.startswith('### '):
        title = line.lstrip('# ').strip()
        doc.add_heading(title, level=3)
        continue
    
    # > 引用（凡例など）
    if line.startswith('> '):
        p = doc.add_paragraph(line[2:].strip())
        p.paragraph_format.left_indent = Cm(1.5)
        p.runs[0].font.italic = True
        p.runs[0].font.color.rgb = RGBColor(0x60, 0x60, 0x60)
        continue
    
    # 演出指示（【〜】で始まる行）
    stripped = line.strip()
    if stripped.startswith('【') and ('スライド切替' in stripped or '間' in stripped 
                                      or '声のトーン' in stripped or 'ゆっくり' in stripped
                                      or '優しく' in stripped
                                      or '実演' in stripped or 'カウントダウン' in stripped
                                      or 'リアルタイム' in stripped):
        add_styled_paragraph(doc, stripped, is_stage_direction=True)
        continue
    
    # ※ 補足コメント（緑色）
    if stripped.startswith('※') or stripped.startswith('・「') or stripped.startswith('→ '):
        add_styled_paragraph(doc, stripped, is_stage_direction=True)
        continue
    
    # 普通のテキスト
    add_styled_paragraph(doc, stripped)

# ── 保存 ──
doc.save(OUT_PATH)
print(f"完了！ Word形式で保存: {OUT_PATH}")
