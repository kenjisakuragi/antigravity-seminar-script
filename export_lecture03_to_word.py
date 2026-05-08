# -*- coding: utf-8 -*-
"""
export_lecture03_to_word.py — 第3回講義読み原稿をWord形式に変換
"""
import sys, os, re

try:
    from docx import Document
    from docx.shared import Inches, Pt, Cm, RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "python-docx"])
    from docx import Document
    from docx.shared import Inches, Pt, Cm, RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MD_PATH = os.path.join(SCRIPT_DIR, "lecture_script_03.md")
OUT_PATH = os.path.join(SCRIPT_DIR, "セミナー読み原稿_第3回_v3.docx")

with open(MD_PATH, "r", encoding="utf-8") as f:
    lines = f.readlines()

doc = Document()

style = doc.styles['Normal']
style.font.name = 'メイリオ'
style.font.size = Pt(11)
style.paragraph_format.line_spacing = 1.5

for i in range(1, 4):
    h = doc.styles[f'Heading {i}']
    h.font.name = 'メイリオ'
    h.font.color.rgb = RGBColor(0x0E, 0xA5, 0xE9)

# 表紙
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.add_run("\n\n\n").font.size = Pt(14)

p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run("AI副業セミナー 第3回")
run.font.size = Pt(28); run.font.bold = True
run.font.color.rgb = RGBColor(0x0E, 0xA5, 0xE9)

p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run("AI動画② キャラクターが喋る！世界に届ける日")
run.font.size = Pt(18); run.font.bold = True
run.font.color.rgb = RGBColor(0x60, 0x60, 0x60)

p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.add_run("\n読み原稿（120分バージョン）").font.size = Pt(22)

doc.add_page_break()

# 凡例
doc.add_heading("記号凡例", level=1)
legend = [
    ("【間 ○秒】", "指定秒数の沈黙を取る"),
    ("【スライド切替】", "次のスライドに進む合図"),
    ("【実演開始】〜【実演終了】", "デモンストレーション区間"),
    ("【声のトーン：↑】", "テンションを上げて話す"),
    ("【声のトーン：↓】", "落ち着いた声で話す"),
    ("【ゆっくり】", "重要ポイント、ゆっくり読む"),
    ("📌", "特に強調して読む箇所"),
    ("※", "補足説明（読み飛ばし可）"),
]
table = doc.add_table(rows=len(legend)+1, cols=2)
table.style = 'Light Grid Accent 1'
table.rows[0].cells[0].text = "記号"
table.rows[0].cells[1].text = "意味"
for cell in table.rows[0].cells:
    for par in cell.paragraphs:
        for run in par.runs:
            run.font.bold = True
for i, (sym, desc) in enumerate(legend, 1):
    table.rows[i].cells[0].text = sym
    table.rows[i].cells[1].text = desc
doc.add_page_break()

def add_para(doc, text, is_stage=False):
    p = doc.add_paragraph()
    if is_stage:
        p.paragraph_format.left_indent = Cm(1)
        run = p.add_run(text)
        run.font.size = Pt(9)
        run.font.color.rgb = RGBColor(0x00, 0x80, 0x00)
        run.font.italic = True
        return
    parts = re.split(r'(\*\*[^*]+\*\*)', text)
    for part in parts:
        if part.startswith('**') and part.endswith('**'):
            r = p.add_run(part[2:-2]); r.font.bold = True
        else:
            p.add_run(part)

def add_code_line(doc, text):
    """コードブロック内の行をグレー背景・Courier Newで出力する"""
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(1.5)
    run = p.add_run(text if text else " ")
    run.font.name = 'Courier New'
    run.font.size = Pt(9)
    run.font.color.rgb = RGBColor(0x20, 0x20, 0x20)

# テーブル行（|始まり）は集めてWordテーブルに変換するか、そのままテキストで出力
in_code_block = False

for line in lines:
    line = line.rstrip('\r\n')
    stripped = line.strip()

    # コードブロック開始・終了の検出
    if stripped.startswith('```'):
        in_code_block = not in_code_block
        if in_code_block:
            # コードブロック開始：区切り線を引く
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Cm(1.5)
            r = p.add_run("▼ プロンプト例 ─────────────────────")
            r.font.size = Pt(8)
            r.font.color.rgb = RGBColor(0x60, 0x60, 0x60)
        else:
            # コードブロック終了：区切り線を引く
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Cm(1.5)
            r = p.add_run("─────────────────────────────────")
            r.font.size = Pt(8)
            r.font.color.rgb = RGBColor(0x60, 0x60, 0x60)
        continue

    if in_code_block:
        add_code_line(doc, stripped)
        continue

    if not stripped or stripped == '---': continue
    if stripped.startswith('# ━'): continue
    if line.startswith('# '):
        doc.add_heading(line.lstrip('# ').strip(), level=1); continue
    if line.startswith('## '):
        doc.add_heading(line.lstrip('# ').strip(), level=2); continue
    if line.startswith('### '):
        doc.add_heading(line.lstrip('# ').strip(), level=3); continue
    if line.startswith('> '):
        p = doc.add_paragraph(line[2:].strip())
        p.paragraph_format.left_indent = Cm(1.5)
        if p.runs: p.runs[0].font.italic = True; p.runs[0].font.color.rgb = RGBColor(0x60,0x60,0x60)
        continue
    # テーブル行（| で始まる行）は視覚的に区別できるよう等幅で出力
    if stripped.startswith('|'):
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(0.5)
        run = p.add_run(stripped)
        run.font.size = Pt(9)
        run.font.name = 'Courier New'
        continue
    is_stage = (
        stripped.startswith('【') and any(k in stripped for k in ['スライド切替','間','声のトーン','ゆっくり','優しく','実演'])
        or stripped.startswith('※') or stripped.startswith('・「') or stripped.startswith('→ ')
    )
    add_para(doc, stripped, is_stage)

doc.save(OUT_PATH)
print(f"完了！ Word形式で保存: {OUT_PATH}")

