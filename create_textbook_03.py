# -*- coding: utf-8 -*-
"""
create_textbook_03.py — 第3回テキスト教材（受講者向け完全版）を Word 形式で生成
"""
import os
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(SCRIPT_DIR, "第3回_テキスト教材_完全版.docx")

BLUE   = RGBColor(0x0E, 0xA5, 0xE9)
ORANGE = RGBColor(0xEA, 0x58, 0x0C)
GRAY   = RGBColor(0x60, 0x60, 0x60)
DARK   = RGBColor(0x20, 0x20, 0x20)

doc = Document()

# ── ページマージン ──────────────────────────────
for section in doc.sections:
    section.top_margin    = Cm(2.0)
    section.bottom_margin = Cm(2.0)
    section.left_margin   = Cm(2.5)
    section.right_margin  = Cm(2.5)

# ── 基本スタイル ────────────────────────────────
normal = doc.styles['Normal']
normal.font.name = 'メイリオ'
normal.font.size = Pt(11)
normal.paragraph_format.line_spacing = 1.5

for lvl in range(1, 4):
    h = doc.styles[f'Heading {lvl}']
    h.font.name  = 'メイリオ'
    h.font.color.rgb = BLUE


# ── ユーティリティ ──────────────────────────────

def set_font(run, size=None, bold=False, color=None, name='メイリオ'):
    run.font.name = name
    if size:
        run.font.size = Pt(size)
    run.font.bold = bold
    if color:
        run.font.color.rgb = color

def center_para(text, size, bold=False, color=None):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(text)
    set_font(r, size=size, bold=bold, color=color)
    return p

def body(text, indent=None, orange_words=None):
    """通常段落。orange_words リストにある語をオレンジ太字にする。"""
    p = doc.add_paragraph()
    if indent:
        p.paragraph_format.left_indent = Cm(indent)
    if not orange_words:
        r = p.add_run(text)
        set_font(r, size=11)
    else:
        import re
        pattern = '(' + '|'.join(re.escape(w) for w in orange_words) + ')'
        parts = re.split(pattern, text)
        for part in parts:
            r = p.add_run(part)
            if part in orange_words:
                set_font(r, size=11, bold=True, color=ORANGE)
            else:
                set_font(r, size=11)
    return p

def bullet(text, level=1, mark='●'):
    p = doc.add_paragraph()
    indent = Cm(0.8 * level)
    p.paragraph_format.left_indent  = indent
    p.paragraph_format.first_line_indent = Cm(-0.4)
    r = p.add_run(f'{mark} {text}')
    set_font(r, size=11)
    return p

def check_item(text):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.8)
    r = p.add_run(f'□ {text}')
    set_font(r, size=11)
    return p

def section_heading(text, level=1):
    h = doc.add_heading(text, level=level)
    for run in h.runs:
        run.font.name = 'メイリオ'
        run.font.color.rgb = BLUE
    return h

def add_code_block(lines_list, label='▼ プロンプト'):
    # ラベル行
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(1.5)
    r = p.add_run(f'{label} ─────────────────────────────')
    r.font.name  = 'Courier New'
    r.font.size  = Pt(8)
    r.font.color.rgb = GRAY

    for line in lines_list:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(1.5)
        r = p.add_run(line if line else ' ')
        r.font.name  = 'Courier New'
        r.font.size  = Pt(9)
        r.font.color.rgb = DARK

    # 終端線
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(1.5)
    r = p.add_run('─' * 40)
    r.font.name  = 'Courier New'
    r.font.size  = Pt(8)
    r.font.color.rgb = GRAY

def add_table_header(table, headers):
    row = table.rows[0]
    for i, h in enumerate(headers):
        cell = row.cells[i]
        cell.text = h
        for par in cell.paragraphs:
            for run in par.runs:
                run.font.bold = True
                run.font.name = 'メイリオ'
                run.font.size = Pt(10)
                run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        # ヘッダーセル背景をブルーに
        tc = cell._tc
        tcPr = tc.get_or_add_tcPr()
        shd = OxmlElement('w:shd')
        shd.set(qn('w:val'), 'clear')
        shd.set(qn('w:color'), 'auto')
        shd.set(qn('w:fill'), '0EA5E9')
        tcPr.append(shd)

def fill_table_row(table, row_idx, values, bold_first=False):
    row = table.rows[row_idx]
    for i, v in enumerate(values):
        cell = row.cells[i]
        cell.text = v
        for par in cell.paragraphs:
            for run in par.runs:
                run.font.name = 'メイリオ'
                run.font.size = Pt(10)
                if bold_first and i == 0:
                    run.font.bold = True

def step_item(num, text):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.4)
    r_num = p.add_run(f'STEP {num}　')
    set_font(r_num, size=11, bold=True, color=ORANGE)
    r_txt = p.add_run(text)
    set_font(r_txt, size=11)
    return p

def orange_bold(text):
    """インライン用ではなく段落としてオレンジ強調"""
    p = doc.add_paragraph()
    r = p.add_run(text)
    set_font(r, size=12, bold=True, color=ORANGE)
    return p


# ══════════════════════════════════════════════
# 1. 表 紙
# ══════════════════════════════════════════════
doc.add_paragraph('\n\n')
center_para('らくらくAI副業キャンパス', 14, color=GRAY)
doc.add_paragraph()
center_para('AI副業セミナー 第3回', 32, bold=True, color=BLUE)
doc.add_paragraph()
center_para('AI動画②　キャラクターが喋る！世界に届ける日', 18, bold=True, color=GRAY)
doc.add_paragraph()
center_para('受講者テキスト教材　完全版', 22, bold=True)
doc.add_paragraph()
center_para('2026年5月4日', 14, color=GRAY)

doc.add_page_break()


# ══════════════════════════════════════════════
# 2. 本日のゴールと全体の流れ
# ══════════════════════════════════════════════
section_heading('本日のゴールと全体の流れ', level=1)

section_heading('本日の3大ゴール', level=2)

goals = [
    ('ゴール①', '音声生成ができる', 'Google AI Studio で日本語音声を生成し、WAVファイルを手元に保存できる'),
    ('ゴール②', '動画が完成する',   'キャラクターが喋る動画（または字幕動画）を1本完成させる'),
    ('ゴール③', 'YouTubeに公開できる', 'タイトル・説明文・サムネイルを設定し、1本目の動画を公開する'),
]
for tag, title, desc in goals:
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.5)
    r1 = p.add_run(f'{tag}　')
    set_font(r1, size=12, bold=True, color=ORANGE)
    r2 = p.add_run(f'{title}\n')
    set_font(r2, size=12, bold=True)
    r3 = p.add_run(f'    {desc}')
    set_font(r3, size=10, color=GRAY)

doc.add_paragraph()
section_heading('タイムライン', level=2)

timeline = [
    ('00:00〜10:00', '導入・前回の復習',           'テキスト教材（本書）'),
    ('10:00〜30:00', 'PART 1: 音声生成ハンズオン', 'Google AI Studio'),
    ('30:00〜50:00', 'PART 2A: リップシンク動画',   'KLING AI'),
    ('30:00〜50:00', 'PART 2B: 字幕動画（代替）',   'CapCut'),
    ('50:00〜80:00', 'PART 3: YouTube 公開ガイド',  'YouTube Studio / Canva'),
    ('80:00〜100:00', '自由作業＋質問タイム',        '各自のツール'),
    ('100:00〜120:00', '発表・フィードバック',       'Discord'),
]
table = doc.add_table(rows=len(timeline)+1, cols=3)
table.style = 'Light Grid Accent 1'
add_table_header(table, ['時間', '内容', '使うツール'])
for i, (t, c, tool) in enumerate(timeline, 1):
    fill_table_row(table, i, [t, c, tool])

doc.add_page_break()


# ══════════════════════════════════════════════
# 3. 使用ツール一覧
# ══════════════════════════════════════════════
section_heading('使用ツール一覧', level=1)

tools = [
    ('Google AI Studio', '音声生成（TTS）',         '無料',        'aistudio.google.com'),
    ('KLING AI',          'リップシンク動画',        '無料〜月1,500円', 'klingai.com'),
    ('CapCut',            '動画編集（無料ルート）',  '無料',        'capcut.com'),
    ('Canva',             'サムネイル作成',           '無料',        'canva.com'),
    ('Gemini',            'プロンプト生成・SEO文案', '無料',        'gemini.google.com'),
]
table = doc.add_table(rows=len(tools)+1, cols=4)
table.style = 'Light Grid Accent 1'
add_table_header(table, ['ツール', '用途', '料金', 'URL'])
for i, row_data in enumerate(tools, 1):
    fill_table_row(table, i, list(row_data), bold_first=True)

doc.add_page_break()


# ══════════════════════════════════════════════
# 4. PART 1: Google AI Studio 音声生成
# ══════════════════════════════════════════════
section_heading('PART 1　Google AI Studio 音声生成（全員共通）', level=1)

body('Google AI Studio の無料 TTS（テキスト読み上げ）機能を使い、キャラクターの音声ナレーションを生成します。')
doc.add_paragraph()

section_heading('手順（7ステップ）', level=2)

steps = [
    'aistudio.google.com にアクセス → Google アカウントでログイン',
    '左メニューから「Speech」をクリック',
    'モデル選択：Gemini 2.0 Flash（推奨・無料枠大）を選ぶ',
    'Voice を選択する（下の表を参考に）',
    'テキスト入力欄に演出プロンプト＋台本を貼り付ける',
    '「Run」ボタンをクリック → 生成完了まで待つ',
    '「…」→「Download」でWAVファイルを保存',
]
for i, s in enumerate(steps, 1):
    step_item(i, s)

doc.add_paragraph()
section_heading('Voice 選び方ガイド', level=2)

voices = [
    ('Puck / Charon',  '落ち着いた男性', '知的・神秘的・ナレーター系キャラ'),
    ('Kore / Leda',    '落ち着いた女性', 'お姉さん系・教育系・解説系キャラ'),
    ('Zephyr / Aoede', '明るく元気',     'かわいい・ポップ・VTuber系キャラ'),
    ('Fenrir',         '低め・渋い',     'ナレーション・シリアス・ドキュメント系'),
]
table = doc.add_table(rows=len(voices)+1, cols=3)
table.style = 'Light Grid Accent 1'
add_table_header(table, ['Voice名', '声の特徴', '向いているキャラクター'])
for i, row_data in enumerate(voices, 1):
    fill_table_row(table, i, list(row_data), bold_first=True)

doc.add_paragraph()
section_heading('コピペ用：演出プロンプトテンプレート', level=2)

add_code_block([
    '以下のテキストを読み上げてください。',
    '',
    '【話し方の指示】',
    '・落ち着いた、優しいトーンで',
    '・重要な部分は少しゆっくり、力を込めて読む',
    '・「、」の部分は0.5秒、「。」の部分は1秒の間をあける',
    '・聴き手に語りかけるような親しみのある話し方で',
    '',
    '【台本】',
    '（ここに台本テキストをコピペ）',
], label='▼ 演出プロンプト（Google AI Studio 用）')

doc.add_paragraph()
section_heading('品質向上のコツ', level=2)

tips = [
    '台本は 300 文字以下に分割すると音声が安定する',
    '句読点を適切に入れると間・イントネーションが自然になる',
    'Run を複数回実行して一番良いテイクを選ぶ',
]
for t in tips:
    bullet(t)

doc.add_page_break()


# ══════════════════════════════════════════════
# 5. PART 2A: KLING AI リップシンク（プレミアムルート）
# ══════════════════════════════════════════════
section_heading('PART 2A　KLING AI リップシンク（プレミアムルート）', level=1)

body('キャラクター画像と音声を合成して「口が動く動画」を自動生成します。')
doc.add_paragraph()

section_heading('料金プラン', level=2)

plans = [
    ('無料',         '0円',      '毎日無料生成あり',      'まず試したい人'),
    ('ライト',       '月約1,500円', '660クレジット/月',   '週1〜2本ペースの人'),
    ('スタンダード', '月約3,900円', '3,000クレジット/月', '毎日作る本格派'),
]
table = doc.add_table(rows=len(plans)+1, cols=4)
table.style = 'Light Grid Accent 1'
add_table_header(table, ['プラン', '月額', 'クレジット', '向いている人'])
for i, row_data in enumerate(plans, 1):
    fill_table_row(table, i, list(row_data), bold_first=True)

doc.add_paragraph()
section_heading('手順（7ステップ）', level=2)

steps2a = [
    'klingai.com にアクセス → Google アカウントでログイン',
    '左メニューから「Lip Sync」を選択',
    'キャラクター画像をアップロード（推奨条件は下記参照）',
    '「Upload Local Dubbing」で WAV ファイルをアップロード（日本語は必ずこちら）',
    '波形を確認し、必要ならトリミングして長さを調整',
    '「Generate」ボタンをクリック（1〜5分待つ）',
    'プレビューを確認 → 「Download」で MP4 を保存',
]
for i, s in enumerate(steps2a, 1):
    step_item(i, s)

doc.add_paragraph()
section_heading('画像の推奨条件', level=2)

ok_items = ['顔が正面向き', '口元がはっきり見える', '解像度 512px 以上', '背景がシンプル']
ng_items = ['横顔・斜め顔', 'サングラス・マスク着用', '極端に小さい顔（画面の 30% 未満）']

body('✅ OK', orange_words=['✅ OK'])
for item in ok_items:
    bullet(f'✅ {item}', mark='')

body('❌ NG', orange_words=['❌ NG'])
for item in ng_items:
    bullet(f'❌ {item}', mark='')

doc.add_paragraph()
section_heading('品質向上のコツ', level=2)

tips2a = [
    '無音部分が長い WAV は事前にトリミングしておく',
    '1回で不自然なら画像を変えてリトライ（消費クレジットは変わらない）',
    '複数カットに分けて撮影し、後で CapCut でつなぐと自然な仕上がりに',
    '生成が重い時間帯は早朝・深夜が比較的スムーズ',
]
for t in tips2a:
    bullet(t)

doc.add_page_break()


# ══════════════════════════════════════════════
# 6. PART 2B: CapCut 動画編集（コスト重視ルート）
# ══════════════════════════════════════════════
section_heading('PART 2B　CapCut 動画編集（コスト重視ルート）', level=1)

body('費用ゼロでキャラクター画像＋音声の動画を作成します。KLING AI の代わりに字幕を自動生成して見やすく仕上げます。')
doc.add_paragraph()

section_heading('手順（5ステップ）', level=2)

steps2b = [
    'capcut.com にアクセス（スマホアプリ or PC ブラウザ版どちらでも可）',
    '背景画像と WAV 音声をプロジェクトにインポート',
    '「テキスト」→「自動字幕」を選択 → 言語「日本語」で字幕を自動生成',
    '著作権フリー BGM を追加（YouTube オーディオライブラリ推奨）',
    '「エクスポート」→ MP4 1080p で書き出し',
]
for i, s in enumerate(steps2b, 1):
    step_item(i, s)

doc.add_paragraph()
body('💡 字幕スタイルはフォント・色・位置をカスタマイズして、チャンネルのブランドカラーに統一すると効果的です。')

doc.add_page_break()


# ══════════════════════════════════════════════
# 7. PART 3: YouTube 公開 完全ガイド
# ══════════════════════════════════════════════
section_heading('PART 3　YouTube 公開 完全ガイド', level=1)

section_heading('事前確認：電話番号認証', level=2)
body('カスタムサムネイルを設定するには電話番号認証が必要です。')
bullet('YouTube Studio → 設定 → チャンネル → 機能の利用資格 → 電話番号を確認')
bullet('認証が完了していれば「カスタムサムネイルをアップロード」ボタンが表示されます')

doc.add_paragraph()

# STEP 1
section_heading('STEP 1　Gemini でタイトル・説明文・タグを準備', level=2)

body('動画をアップロードする前に Gemini で SEO テキストを用意しておくとスムーズです。')

doc.add_paragraph()
body('【タイトル生成プロンプト】')
add_code_block([
    'あなたはYouTubeのSEOの専門家です。',
    '以下のテーマの動画に、クリックしたくなるタイトルを5個提案してください。',
    '',
    '【テーマ】〇〇（←ここだけ変える）',
    '【条件】',
    '・30文字以内',
    '・「〇〇な人向け」「知らないと損」「実は〇〇だった」「〇選」などのパターンを活用',
    '・YouTube検索で上位に来そうなキーワードを含める',
], label='▼ タイトル生成（Gemini 用）')

doc.add_paragraph()
body('【説明文生成プロンプト】')
add_code_block([
    '以下のYouTube動画の説明文を書いてください。',
    '',
    '【動画タイトル】（←決定したタイトルを貼る）',
    '【動画の内容概要】（←台本の冒頭100文字を貼る）',
    '【条件】',
    '・冒頭の2行は「なぜこの動画を見るべきか」を書く',
    '・全体で300〜500文字',
    '・末尾にチャンネル登録のお願いを入れる',
    '・ハッシュタグを5個入れる',
], label='▼ 説明文生成（Gemini 用）')

doc.add_paragraph()
body('【タグ生成プロンプト】')
add_code_block([
    'この動画に最適なYouTubeタグを15個提案してください。',
    'ビッグキーワードとニッチキーワードを両方入れてください。',
    '',
    '【動画テーマ】（←テーマを書く）',
], label='▼ タグ生成（Gemini 用）')

doc.add_paragraph()

# STEP 2〜4
section_heading('STEP 2〜4　YouTube にログイン → 動画アップロード → 詳細入力', level=2)

step_details = [
    ('STEP 2', 'YouTube にログイン・チャンネルを確認する'),
    ('STEP 3', '画面右上のカメラ＋アイコン → 「動画をアップロード」をクリックし MP4 ファイルを選択'),
    ('STEP 4', '詳細情報を入力する（下記チェックリスト参照）'),
]
for tag, txt in step_details:
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.4)
    r1 = p.add_run(f'{tag}　')
    set_font(r1, size=11, bold=True, color=ORANGE)
    r2 = p.add_run(txt)
    set_font(r2, size=11)

doc.add_paragraph()
body('詳細入力のチェックリスト')
detail_checks = [
    'タイトル（100文字以内・重要キーワードを前半に入れる）',
    '説明文（冒頭2行が検索結果に表示されるので最重要）',
    '視聴者：「子供向けではない」を選択（重要！）',
    'タグ：「もっと見る」を開いて Gemini で生成したタグを入力',
    '言語：日本語 ／ カテゴリ：ハウツーとスタイル or 教育',
]
for c in detail_checks:
    check_item(c)

doc.add_paragraph()

# STEP 5: Canva サムネイル
section_heading('STEP 5　Canva でサムネイルを作成', level=2)

bullet('canva.com → 検索バーで「YouTube サムネイル」を検索 → テンプレートを選択')
bullet('推奨仕様：1280×720px ／ 16:9 ／ 2MB 以内 ／ PNG または JPG')

doc.add_paragraph()
body('サムネイル 3 原則')
thumb_rules = [
    '大きな文字（遠くから見ても読める文字サイズ）',
    '鮮やかな色（高コントラスト・目立つ配色）',
    'シンプルなデザイン（情報を詰め込みすぎない）',
]
for r in thumb_rules:
    bullet(r, mark='★')

doc.add_paragraph()

# STEP 6〜7
section_heading('STEP 6〜7　サムネイルをアップロード → 公開', level=2)

p = doc.add_paragraph()
p.paragraph_format.left_indent = Cm(0.4)
r1 = p.add_run('STEP 6　')
set_font(r1, size=11, bold=True, color=ORANGE)
r2 = p.add_run('「カスタムサムネイルをアップロード」ボタンをクリック → Canva で作成した PNG/JPG を選択')
set_font(r2, size=11)

p = doc.add_paragraph()
p.paragraph_format.left_indent = Cm(0.4)
r1 = p.add_run('STEP 7　')
set_font(r1, size=11, bold=True, color=ORANGE)
r2 = p.add_run('著作権チェック画面を確認（「問題は見つかりません」ならOK）→ 公開設定「公開」→「公開」ボタン')
set_font(r2, size=11)

doc.add_paragraph()
bullet('公開後：URL をコピー → Discord の URL 投稿チャンネルに貼る', mark='📌')

doc.add_page_break()


# ══════════════════════════════════════════════
# 8. 著作権フリー BGM 入手ガイド
# ══════════════════════════════════════════════
section_heading('著作権フリー BGM 入手ガイド', level=1)

body('YouTube に公開する動画には必ず著作権フリーの BGM を使いましょう。')
doc.add_paragraph()

bgm_methods = [
    ('① YouTube オーディオライブラリ（最推奨）',
     'YouTube Studio → 左メニュー「オーディオライブラリ」\n「帰属表示が不要」で絞り込むと説明文への記載も不要'),
    ('② Pixabay Music',
     'pixabay.com/music — 無料・商用 OK・会員登録なしで使用可'),
    ('③ CapCut 内蔵 BGM',
     'CapCut 内の BGM から「著作権フリー」タグで絞り込む'),
]
for title, desc in bgm_methods:
    p = doc.add_paragraph()
    r = p.add_run(title)
    set_font(r, size=12, bold=True, color=BLUE)
    for line in desc.split('\n'):
        bullet(line)
    doc.add_paragraph()

doc.add_page_break()


# ══════════════════════════════════════════════
# 9. プロンプトテンプレート集（切り取り保存用）
# ══════════════════════════════════════════════
section_heading('プロンプトテンプレート集（切り取り保存用）', level=1)

body('このページをコピー・印刷して手元に置いておくと便利です。')
doc.add_paragraph()

# 演出プロンプト
section_heading('演出プロンプト（Google AI Studio 用）', level=2)
add_code_block([
    '以下のテキストを読み上げてください。',
    '',
    '【話し方の指示】',
    '・落ち着いた、優しいトーンで',
    '・重要な部分は少しゆっくり、力を込めて読む',
    '・「、」の部分は0.5秒、「。」の部分は1秒の間をあける',
    '・聴き手に語りかけるような親しみのある話し方で',
    '',
    '【台本】',
    '（ここに台本テキストをコピペ）',
], label='▼ 演出プロンプト')

doc.add_paragraph()

# タイトル生成
section_heading('タイトル生成プロンプト（Gemini 用）', level=2)
add_code_block([
    'あなたはYouTubeのSEOの専門家です。',
    '以下のテーマの動画に、クリックしたくなるタイトルを5個提案してください。',
    '',
    '【テーマ】〇〇（←ここだけ変える）',
    '【条件】',
    '・30文字以内',
    '・「〇〇な人向け」「知らないと損」「実は〇〇だった」「〇選」などのパターンを活用',
    '・YouTube検索で上位に来そうなキーワードを含める',
], label='▼ タイトル生成')

doc.add_paragraph()

# 説明文生成
section_heading('説明文生成プロンプト（Gemini 用）', level=2)
add_code_block([
    '以下のYouTube動画の説明文を書いてください。',
    '',
    '【動画タイトル】（←決定したタイトルを貼る）',
    '【動画の内容概要】（←台本の冒頭100文字を貼る）',
    '【条件】',
    '・冒頭の2行は「なぜこの動画を見るべきか」を書く',
    '・全体で300〜500文字',
    '・末尾にチャンネル登録のお願いを入れる',
    '・ハッシュタグを5個入れる',
], label='▼ 説明文生成')

doc.add_paragraph()

# タグ生成
section_heading('タグ生成プロンプト（Gemini 用）', level=2)
add_code_block([
    'この動画に最適なYouTubeタグを15個提案してください。',
    'ビッグキーワードとニッチキーワードを両方入れてください。',
    '',
    '【動画テーマ】（←テーマを書く）',
], label='▼ タグ生成')

doc.add_paragraph()

# 台本生成
section_heading('台本生成プロンプト（次回以降の動画用）', level=2)
add_code_block([
    '以下の条件でYouTube動画の台本を作成してください。',
    '',
    '【ジャンル】〇〇',
    '【ターゲット】〇〇が気になっている初心者',
    '【動画の長さ】3〜5分（文字数: 900〜1500文字）',
    '【構成】',
    '①フック（最初の15秒で視聴者を引き込む）',
    '②本題（3つのポイントで説明）',
    '③まとめ（チャンネル登録を促す）',
    '【トーン】親しみやすく、わかりやすく',
], label='▼ 台本生成')

doc.add_page_break()


# ══════════════════════════════════════════════
# 10. 今週の課題チェックリスト
# ══════════════════════════════════════════════
section_heading('今週の課題チェックリスト', level=1)

body('セミナー終了後、1週間以内に全てにチェックを入れることを目標にしましょう！')
doc.add_paragraph()

tasks = [
    'Google AI Studio で音声を生成できた',
    'キャラクターが喋る動画（またはゆっくり解説動画）が完成した',
    'YouTube に 1 本公開した',
    '公開 URL を Discord に投稿した',
    '仲間の動画に「見ました！」とコメントした',
    '2 本目の動画も完成させた',
]
for t in tasks:
    check_item(t)

doc.add_paragraph()
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('継続こそが最大の武器です。まず 1 本、世界に届けましょう！')
set_font(r, size=13, bold=True, color=ORANGE)

doc.add_page_break()


# ══════════════════════════════════════════════
# 11. トラブルシューティング
# ══════════════════════════════════════════════
section_heading('トラブルシューティング', level=1)

body('困ったときはまずこの表を確認してください。')
doc.add_paragraph()

troubles = [
    ('カスタムサムネイルが設定できない',
     '電話番号認証が未完了',
     'YouTube Studio → 設定 → チャンネル → 機能の利用資格 で認証'),
    ('著作権警告が出た',
     'BGMに著作権あり',
     'YouTube オーディオライブラリの BGM に差し替え'),
    ('リップシンクが不自然',
     '画像が横顔 or 低解像度',
     '正面向き・512px 以上の画像を使用'),
    ('音声生成でエラーが出る',
     'テキストが長すぎる',
     '台本を 300 文字以下に分割して生成'),
    ('動画がアップロードできない',
     'ファイル形式の問題',
     'CapCut / KLING AI で MP4 形式に書き出し直す'),
    ('字幕の精度が低い',
     'CapCut の音声認識精度',
     '手動で誤字を修正、または句読点を増やして再生成'),
]
table = doc.add_table(rows=len(troubles)+1, cols=3)
table.style = 'Light Grid Accent 1'
add_table_header(table, ['問題', '原因', '解決策'])
for i, row_data in enumerate(troubles, 1):
    fill_table_row(table, i, list(row_data))

doc.add_paragraph()
body('それでも解決しない場合は Discord の #質問チャンネル に投稿してください。')


# ══════════════════════════════════════════════
# 保存
# ══════════════════════════════════════════════
doc.save(OUT_PATH)
print(f'完了！ → {OUT_PATH}')
