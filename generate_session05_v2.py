# -*- coding: utf-8 -*-
"""
generate_session05_v2.py
第5回「AI音楽② 世界100か国に配信して印税生活」— 充実版（30枚）
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "Google_Slide_generator"))
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from design_v2 import *

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(SCRIPT_DIR, "講義05_AI音楽②_v2.pptx")

C1, C2 = "059669", "10B981"   # グリーン

def dashboard(prs, title, rows, note):
    s = add_slide(prs)
    make_table_slide(s, title, ["収益源","ステータス","メモ"], rows,
                     accent_c1=C1, accent_c2=C2, highlight_last=False, note=note)

def build(prs):

    # ──────────────────────────────
    # 1. タイトル
    # ──────────────────────────────
    s = add_slide(prs)
    make_title_slide(s,
        "AI音楽②\n世界100か国に配信して印税生活",
        "第5回｜2026年5月18日（月）19:00〜21:00",
        "らくらくAI副業キャンパス")

    # ──────────────────────────────
    # 2. 本日のゴール
    # ──────────────────────────────
    s = add_slide(prs)
    make_cards_slide(s, "本日のゴール", [
        ("📡", "配信サービスに\n登録完了する", "TuneCore等で\nアーティスト登録＆\n楽曲アップロード"),
        ("🎬", "YouTube Music\nを公開する", "BGMチャンネルを開設\n音楽動画1本を公開\nプレイリスト作成"),
        ("♾️", "印税マシンを\n動かし始める", "一度配信したら\n永久に印税が入る\n仕組みを完成させる"),
    ], accent_c1=C1, accent_c2=C2)

    # ──────────────────────────────
    # 3. 前回の振り返り
    # ──────────────────────────────
    s = add_slide(prs)
    make_dark_summary(s, "前回の振り返り", [
        "✅ Suno AI で楽曲を15曲生成した",
        "✅ ジャンルの方向性（Lo-Fi / アンビエント / キッズ etc.）が決まった",
        "✅ ベスト3曲を Discord に投稿してフィードバックをもらった",
        "✅ YouTube 動画も継続して投稿中",
    ], sub="今日はこの曲を「世界に届ける」作業をします。一緒にやりましょう！", c1=C1, c2=C2)

    # ──────────────────────────────
    # 4. 今日のロードマップ
    # ──────────────────────────────
    s = add_slide(prs)
    make_step_flow(s, "今日の90分ロードマップ", [
        ("1", "配信サービス\n徹底解説\n（25分）", "TuneCore vs 比較\n登録手順を一緒に\nステップバイステップ"),
        ("2", "ジャケット画像\n＆メタデータ\n（20分）", "AI でカバーアートを作成\n検索で見つかるための\nメタデータ入力方法"),
        ("3", "YouTube Music\n戦略\n（20分）", "BGMチャンネルの\n設計・運営方法\nプレイリスト戦略"),
        ("4", "ハンズオン\n実践\n（25分）", "配信登録・\nYouTube Music\n動画を実際に作成"),
    ], accent_c1=C1, accent_c2=C2)

    # ──────────────────────────────
    # 5. セクション1
    # ──────────────────────────────
    s = add_slide(prs)
    make_section(s, 1, "配信サービス徹底解説\n〜 TuneCore で世界100か国に届ける 〜", "19:10 - 19:35", c1=C1, c2=C2)

    # ──────────────────────────────
    # 6. 配信サービス比較
    # ──────────────────────────────
    s = add_slide(prs)
    make_table_slide(s, "主要配信サービス 比較表（どれを選ぶ？）",
        ["サービス", "年会費", "取り分", "おすすめ理由"],
        [
            ["TuneCore Japan", "約1,650円/曲", "100%",  "日本語サポートあり・初心者に最適"],
            ["DistroKid",      "月22ドル〜",   "100%",  "曲数無制限・最速配信（24〜48時間）"],
            ["CD Baby",        "曲ごと9ドル〜", "91%",  "1回払い・長期保有向き"],
            ["BandLab",        "無料",         "100%",  "完全無料・副業の入門として試しやすい"],
        ],
        accent_c1=C1, accent_c2=C2,
        note="📌 初心者には TuneCore Japan（日本語）か DistroKid（曲数無制限）がおすすめ")

    # ──────────────────────────────
    # 7. TuneCore 登録 ステップ詳細
    # ──────────────────────────────
    s = add_slide(prs)
    make_step_flow(s, "TuneCore Japan 登録ステップ（全員一緒にやります）", [
        ("1", "tunecore.co.jp\nにアクセス", "「無料会員登録」\nメールアドレス\n＋パスワードを設定"),
        ("2", "アーティスト\n名を登録", "本名でなくOK\nYouTube チャンネル名\nに合わせると統一感UP"),
        ("3", "楽曲を\nアップロード", "WAV 形式（44.1kHz\n/16bit推奨）\nMP3より音質が高い"),
        ("4", "配信先\nプラットフォームを\n選択", "「すべて選択」で\nSpotify/Apple Music\n等100か国以上に配信"),
    ], accent_c1=C1, accent_c2=C2)

    # ──────────────────────────────
    # 8. アーティスト名の付け方（戦略）
    # ──────────────────────────────
    s = add_slide(prs)
    bg_white(s)
    txt(s, Inches(1), Inches(0.4), Inches(11), Inches(0.65),
        "アーティスト名の付け方（検索されやすくするために）", sz=28, clr=C_BLACK, bold=True)
    gbar(s, Inches(1), Inches(1.05), Inches(2.5), Inches(0.04), C1, C2)

    tips = [
        ("英語名を選ぶ",
         "Spotify / Apple Music で日本語名は検索されにくい。英語名を推奨",
         "OK 例：「Chilly Moon」「Sakura Sleep Music」"),
        ("ジャンルを連想させる名前",
         "アーティスト名だけで何の音楽か伝わると、アルゴリズムが推薦しやすくなる",
         "OK 例：「Lo-Fi Cafe」「Mindful Waves」「Pixel Sound Lab」"),
        ("YouTube チャンネル名と統一",
         "SNS / YouTube / 配信すべて同じ名前にすると検索で一括ヒットする",
         "例：YouTube「Sakura Sleep Music」= Spotify「Sakura Sleep Music」"),
        ("ユニーク性を確認",
         "Spotify で検索して同名アーティストがいないかチェックする",
         "かぶっていると検索流入が分散されてしまう"),
    ]
    for i, (title, desc, example) in enumerate(tips):
        y = Inches(1.4) + i * Inches(1.35)
        card(s, Inches(1.0), y, Inches(11.3), Inches(1.15), fill="F0FDF4", shadow=True)
        txt(s, Inches(1.3), y + Inches(0.1), Inches(9), Inches(0.4),
            f"✅ {title}", sz=14, clr=RGBColor(0x05, 0x96, 0x69), bold=True)
        txt(s, Inches(1.3), y + Inches(0.55), Inches(9), Inches(0.35),
            desc, sz=12, clr=C_DGRAY)
        txt(s, Inches(1.3), y + Inches(0.85), Inches(9), Inches(0.25),
            example, sz=11, clr=RGBColor(0x6B, 0x72, 0x80))
    footer(s, C1, C2)

    # ──────────────────────────────
    # 9. メタデータ入力（重要！）
    # ──────────────────────────────
    s = add_slide(prs)
    bg_white(s)
    txt(s, Inches(1), Inches(0.4), Inches(11), Inches(0.65),
        "メタデータ入力（検索で見つけてもらうための設定）", sz=28, clr=C_BLACK, bold=True)
    gbar(s, Inches(1), Inches(1.05), Inches(2.5), Inches(0.04), C1, C2)

    meta_items = [
        ("曲名（Title）", "英語が基本。「Lo-Fi Morning Study」のように使用シーンをタイトルに入れる"),
        ("アルバム名",     "「Peaceful Study Collection Vol.1」など。シリーズ化すると次作が売りやすい"),
        ("ジャンル",       "「Lo-Fi」「Ambient」「New Age」など正確に選択。複数選べる場合は必ず複数選ぶ"),
        ("リリース日",     "1〜2週間先に設定。日付が近いほどNewリリースとして推薦されやすい"),
        ("著作権表示",     "「Composed by（アーティスト名）」を正確に記入。空欄は NG"),
        ("UPC / ISRC",    "TuneCore が自動発行してくれる。いじらなくて OK"),
    ]
    for i, (field, desc) in enumerate(meta_items):
        y = Inches(1.4) + i * Inches(0.95)
        card(s, Inches(1.0), y, Inches(2.8), Inches(0.72), grad=(C1, C2), shadow=False)
        txt(s, Inches(1.1), y + Inches(0.17), Inches(2.6), Inches(0.42),
            field, sz=13, clr=C_WHITE, bold=True)
        txt(s, Inches(4.1), y + Inches(0.17), Inches(8.2), Inches(0.5),
            desc, sz=12, clr=C_DGRAY)
    footer(s, C1, C2)

    # ──────────────────────────────
    # 10. セクション2（ジャケット）
    # ──────────────────────────────
    s = add_slide(prs)
    make_section(s, 2, "ジャケット画像をAIで作る\n〜 プロ品質のアートワーク in 5分 〜", "19:35 - 19:55", c1=C1, c2=C2)

    # ──────────────────────────────
    # 11. ジャケット規格
    # ──────────────────────────────
    s = add_slide(prs)
    make_dark_summary(s, "ジャケット画像の規格（これを守らないと配信できない！）", [
        "✅ サイズ：3000 × 3000 px（正方形）",
        "✅ ファイル形式：JPG または PNG",
        "✅ ファイルサイズ：10MB 以下",
        "✅ 解像度：72〜300 dpi",
        "❌ テキスト禁止：アーティスト名・曲名を画像に入れない（一部配信サービス）",
        "❌ 他者の著作物・商標：映画キャラ・有名ブランドロゴなどは使用禁止",
    ], sub="規格外の画像はアップロード時にエラーになります。事前に確認しましょう", c1=C1, c2=C2)

    # ──────────────────────────────
    # 12. ジャケット生成プロンプト集
    # ──────────────────────────────
    s = add_slide(prs)
    bg_white(s)
    txt(s, Inches(1), Inches(0.4), Inches(11), Inches(0.65),
        "ジャケット画像 AI生成プロンプト例（Gemini / Ideogram 使用）", sz=26, clr=C_BLACK, bold=True)
    gbar(s, Inches(1), Inches(1.05), Inches(2.5), Inches(0.04), C1, C2)

    covers = [
        ("Lo-Fi / チルホップ",
         "A cozy cafe window at night with rain, soft warm lighting, cassette tape aesthetic, square format, no text"),
        ("アンビエント / 瞑想",
         "Peaceful Japanese zen garden with morning mist, soft pastel colors, abstract and minimal, 3000x3000px"),
        ("子守唄 / キッズ",
         "Cute watercolor illustration of a sleeping baby under starry sky, gentle moon and clouds, pastel pink"),
        ("ゲームBGM",
         "Retro pixel art landscape of a fantasy adventure, 16-bit style, vibrant colors, square album art"),
        ("J-POP インスト",
         "Cherry blossom petals falling on a quiet street, soft bokeh, warm sunset, cinematic photography style"),
    ]
    for i, (genre, prompt) in enumerate(covers):
        y = Inches(1.35) + i * Inches(1.1)
        card(s, Inches(1.0), y, Inches(2.5), Inches(0.85), grad=(C1, C2), shadow=False)
        txt(s, Inches(1.05), y + Inches(0.2), Inches(2.4), Inches(0.5),
            genre, sz=11, clr=C_WHITE, bold=True, align=PP_ALIGN.CENTER)
        card(s, Inches(3.8), y, Inches(8.5), Inches(0.85), fill="F0FDF4", shadow=False)
        txt(s, Inches(4.0), y + Inches(0.18), Inches(8.0), Inches(0.55),
            prompt, sz=11, clr=C_DGRAY)
    footer(s, C1, C2)

    # ──────────────────────────────
    # 13. セクション3（YouTube Music）
    # ──────────────────────────────
    s = add_slide(prs)
    make_section(s, 3, "YouTube Music 戦略\n〜 BGMチャンネルで二重に稼ぐ 〜", "19:55 - 20:15", c1=C1, c2=C2)

    # ──────────────────────────────
    # 14. YouTube Music とは
    # ──────────────────────────────
    s = add_slide(prs)
    make_cards_slide(s, "通常の YouTube と YouTube Music の違い", [
        ("🎬", "通常の YouTube\nチャンネル", "動画コンテンツ中心\n広告収益（CPM高め）\n視聴者がアクティブに見る"),
        ("🎵", "YouTube Music\nBGMチャンネル", "音楽・BGM中心\nバックグラウンド再生\n長時間 × 多回数が特徴"),
        ("✨", "両方やれば\n二重収益！", "同じ楽曲を\n通常動画でもYT Musicでも\n配信できる"),
    ], accent_c1=C1, accent_c2=C2)

    # ──────────────────────────────
    # 15. BGMチャンネルの設計
    # ──────────────────────────────
    s = add_slide(prs)
    bg_white(s)
    txt(s, Inches(1), Inches(0.4), Inches(11), Inches(0.65),
        "BGMチャンネルの設計方法（コンセプトから運営まで）", sz=28, clr=C_BLACK, bold=True)
    gbar(s, Inches(1), Inches(1.05), Inches(2.5), Inches(0.04), C1, C2)

    design_items = [
        ("チャンネルコンセプト",
         "「誰のための・何のための BGM チャンネル」を1行で決める",
         "例：「集中したいすべての人への、Lo-Fi 作業 BGM チャンネル」"),
        ("チャンネルアート",
         "Canva の「YouTube チャンネルアート」テンプレートで5分で作成できる",
         "横長バナー（2560×1440px）＋プロフィールアイコン（800×800px）"),
        ("動画フォーマット",
         "「ジャケット画像 + 楽曲」をループ動画にして1〜2時間の長尺動画を作る",
         "長尺ほど1再生あたりの視聴時間が伸び、アルゴリズムに評価される"),
        ("投稿頻度",
         "週2〜3本がベスト。動画が増えれば増えるほど「おすすめ」に表示される確率UP",
         "最初の1ヶ月は量産優先。質は徐々に上げればOK"),
    ]
    for i, (title, desc, example) in enumerate(design_items):
        y = Inches(1.4) + i * Inches(1.35)
        card(s, Inches(1.0), y, Inches(11.3), Inches(1.15), fill="F0FDF4", shadow=True)
        txt(s, Inches(1.3), y + Inches(0.1), Inches(9), Inches(0.4),
            f"● {title}", sz=14, clr=RGBColor(0x05, 0x96, 0x69), bold=True)
        txt(s, Inches(1.3), y + Inches(0.55), Inches(9.5), Inches(0.35),
            desc, sz=12, clr=C_DGRAY)
        txt(s, Inches(1.3), y + Inches(0.87), Inches(9.5), Inches(0.25),
            example, sz=11, clr=RGBColor(0x6B, 0x72, 0x80))
    footer(s, C1, C2)

    # ──────────────────────────────
    # 16. 音楽動画の作り方（Step by Step）
    # ──────────────────────────────
    s = add_slide(prs)
    make_step_flow(s, "YouTube Music 動画の作り方（CapCut 使用・無料）", [
        ("1", "CapCut を開く\n新規プロジェクト", "capcut.com\nまたはスマホアプリ\nを起動"),
        ("2", "ジャケット画像\nをインポート", "3000×3000px の\nアートワーク画像を\nキャンバスに配置"),
        ("3", "楽曲ファイル\nを追加", "Suno AI で\nダウンロードした\nMP3/WAVをインポート"),
        ("4", "長さを調整\n→ エクスポート", "ループ再生で\n30〜60分に設定\n1080p で書き出し"),
    ], accent_c1=C1, accent_c2=C2)

    # ──────────────────────────────
    # 17. プレイリスト戦略
    # ──────────────────────────────
    s = add_slide(prs)
    bg_white(s)
    txt(s, Inches(1), Inches(0.4), Inches(11), Inches(0.65),
        "Spotify プレイリスト戦略（再生数を10倍にする方法）", sz=28, clr=C_BLACK, bold=True)
    gbar(s, Inches(1), Inches(1.05), Inches(2.5), Inches(0.04), C1, C2)

    playlist_items = [
        ("ピッチング（公式プレイリスト）",
         "Spotify for Artists に登録 → 楽曲リリース前に「ピッチ」機能で審査を申請",
         "採用されると一気に数万〜数十万再生に到達できる"),
        ("インディペンデント・プレイリスト",
         "Lo-Fi / アンビエント 専門のプレイリストキュレーターに直接コンタクトを取る",
         "Instagram や Twitter でキュレーターを探して楽曲を提案するDMを送る"),
        ("自分でプレイリストを作る",
         "自分の曲を含む「勉強用BGM」「眠れる音楽」などのテーマプレイリストを作成・公開",
         "自分でフォロワーを増やしながら楽曲露出を高める地道な方法"),
        ("プレイリスト掲載効果",
         "1つのプレイリストに掲載されると、関連プレイリストにも自動で推薦されやすくなる",
         "スノーボール効果で再生数が自然と増えていく"),
    ]
    for i, (title, desc, tip) in enumerate(playlist_items):
        y = Inches(1.4) + i * Inches(1.35)
        card(s, Inches(1.0), y, Inches(11.3), Inches(1.15), fill="F0FDF4", shadow=True)
        txt(s, Inches(1.3), y + Inches(0.1), Inches(9.5), Inches(0.42),
            f"● {title}", sz=14, clr=RGBColor(0x05, 0x96, 0x69), bold=True)
        txt(s, Inches(1.3), y + Inches(0.55), Inches(9.5), Inches(0.35),
            desc, sz=12, clr=C_DGRAY)
        txt(s, Inches(1.3), y + Inches(0.87), Inches(9.5), Inches(0.25),
            f"→ {tip}", sz=11, clr=RGBColor(0x6B, 0x72, 0x80))
    footer(s, C1, C2)

    # ──────────────────────────────
    # 18. 印税収入の長期シミュレーション
    # ──────────────────────────────
    s = add_slide(prs)
    make_table_slide(s, "印税収入の成長シミュレーション（月30曲ペースの場合）",
        ["経過月", "総曲数", "月間総再生数（目安）", "月収目安"],
        [
            ["1ヶ月後",   "30曲",  "  1〜3万回",  " 3,000〜1万円"],
            ["3ヶ月後",   "90曲",  " 5〜15万回",  "2〜5万円"],
            ["6ヶ月後",  "180曲",  "15〜50万回",  "5〜15万円"],
            ["12ヶ月後", "360曲",  "50〜150万回", "15〜50万円"],
            ["24ヶ月後", "700曲+", "100万回超",   "30万円〜"],
        ],
        accent_c1=C1, accent_c2=C2,
        note="📌 曲数は「永久に消えない資産」。一度配信したら削除しない限りずっと稼ぎ続けます")

    # ──────────────────────────────
    # 19. 強調スライド（印税マシン）
    # ──────────────────────────────
    s = add_slide(prs)
    make_emphasis(s,
        "配信した曲は「永久に働き続けるデジタル印税マシン」",
        "1曲あたりの収益は小さくても\n「曲数 × 時間 × プラットフォーム数」で\n複利的に積み上がっていきます",
        gold=True)

    # ──────────────────────────────
    # 20. セクション4（ハンズオン）
    # ──────────────────────────────
    s = add_slide(prs)
    make_section(s, 4, "ハンズオン実践\n〜 今日、配信を始めよう！ 〜", "20:15 - 20:40", c1=C1, c2=C2)

    # ──────────────────────────────
    # 21. ハンズオン手順
    # ──────────────────────────────
    s = add_slide(prs)
    make_numbered_slide(s, "ハンズオン 手順", [
        ("STEP 1", "TuneCore Japan（または DistroKid）に登録する",
         "tunecore.co.jp / distrokid.com → アカウント作成 → アーティスト名登録"),
        ("STEP 2", "ジャケット画像を AI で作成する",
         "Gemini または Ideogram でコピペ用プロンプトを使ってジャケットを生成 → 3000×3000px にリサイズ"),
        ("STEP 3", "ベスト3曲をアップロードする",
         "WAV ファイル ＋ ジャケット画像 ＋ メタデータを入力 → 配信先「すべて選択」"),
        ("STEP 4", "YouTube Music 用の動画を1本作成する",
         "CapCut でジャケット画像 + 楽曲 → ループ動画（30分）→ 1080p でエクスポート"),
        ("STEP 5", "YouTube に「BGMチャンネル」として動画を公開",
         "タイトル例：「【作業用BGM】Lo-Fi Morning Study Mix 30min」"),
    ], accent_c1=C1, accent_c2=C2)

    # ──────────────────────────────
    # 22. 今週の課題
    # ──────────────────────────────
    s = add_slide(prs)
    make_numbered_slide(s, "今週の課題", [
        ("課題①", "配信サービスへの登録を完了する",
         "TuneCore または DistroKid でアカウント作成 ＋ 3曲以上をアップロード"),
        ("課題②", "YouTube Music に動画を3本公開する",
         "CapCut で楽曲 × ジャケット画像の動画を作成 → BGMチャンネルで公開"),
        ("課題③", "Suno AI で追加10曲を生成する",
         "配信曲は「永久資産」。量産を止めないことが最大の戦略"),
        ("課題④", "YouTube 動画 ＆ 全収益源を継続する",
         "YouTube 動画は止めないこと。2つの収益源を同時に回し続ける"),
    ], accent_c1=C1, accent_c2=C2)

    # ──────────────────────────────
    # 23. よくある質問 Q&A
    # ──────────────────────────────
    s = add_slide(prs)
    make_dark_summary(s, "よくある質問 Q&A", [
        "Q: 配信から収益が入るまでどのくらいかかる？",
        "→ 配信開始から1〜2ヶ月後。TuneCore の支払いは月次払い（最低出金額あり）",
        "Q: 無料の BandLab でも OK？",
        "→ まず試す分には OK。本格的に稼ぐには TuneCore / DistroKid を推奨",
        "Q: 楽曲を削除したら印税はどうなる？",
        "→ 配信停止 = 収益ゼロ。基本的に削除しないことが鉄則",
    ], sub="他の疑問は Discord の #質問箱 へ！質問は全員の学びになります", c1=C1, c2=C2)

    # ──────────────────────────────
    # 24. トラブルシューティング
    # ──────────────────────────────
    s = add_slide(prs)
    make_table_slide(s, "配信でよくあるトラブルと解決策",
        ["問題", "原因", "解決策"],
        [
            ["ジャケットでエラー",         "サイズ・形式の不一致",        "3000×3000px / JPG で再作成"],
            ["配信が遅い",               "レビュー期間（5〜7営業日）",   "早めに申請。DistroKid なら24h"],
            ["Spotify に表示されない",    "反映に時間がかかる",          "配信後2週間待ってから確認"],
            ["収益が0円のまま",           "再生数が少ない",              "プレイリストにピッチング + 動画投稿増加"],
            ["別アーティストと名前が被る", "名前調査不足",               "Spotify で事前確認してリネーム"],
        ],
        accent_c1=C1, accent_c2=C2,
        note="📌 焦らず、正確に設定することが最短への道です")

    # ──────────────────────────────
    # 25. 収益源ダッシュボード
    # ──────────────────────────────
    dashboard(prs, "収益源ダッシュボード — 第5回終了時点",
        [
            ["① YouTube動画",  "✅ 稼働中",   "継続投稿中"],
            ["② AI音楽",       "✅ 稼働中",   "配信スタート！"],
            ["③ Kindle出版",   "⬜ まだ",     "来週（5/25）"],
            ["④ AIブログ",     "⬜ まだ",     "第7回（6/1）"],
            ["⑤ 画像販売",     "⬜ まだ",     "第8回（6/8）"],
            ["⑥ ショート動画", "⬜ まだ",     "第9回（6/15）"],
            ["⑦ スキル販売",   "⬜ まだ",     "第10回（6/22）"],
        ],
        "📌 2つの収益源が稼働中！来週は3つ目「Kindle出版」を始めます")

    # ──────────────────────────────
    # 26. 次回予告
    # ──────────────────────────────
    s = add_slide(prs)
    make_dark_summary(s, "来週（第6回）の予告：AIに本を書かせてAmazonで売る", [
        "📚 印税70%・在庫ゼロ・永久販売の Kindle 出版",
        "🤖 Gemini で1万字の本を15分で書く実演",
        "🎨 AI 画像で表紙デザインを作成",
        "📤 KDP（Kindle Direct Publishing）に出版",
        "💡 今週の台本 = そのまま本の原稿になります！",
    ], sub="YouTube台本 10本分 ＝ 1冊の本。一粒で二度おいしい戦略です", c1=C1, c2=C2)

    # ──────────────────────────────
    # 27. クロージング
    # ──────────────────────────────
    s = add_slide(prs)
    make_emphasis(s,
        "お疲れさまでした！2つの収益源が稼働中です 🎉",
        "📌 来週はAIに本を書いてもらいます\n"
        "📌 3つ目の収益源がスタートします！\n"
        "📌 来週月曜 19:00 にお会いしましょう！")


if __name__ == "__main__":
    prs = create_prs()
    print("第5回（v2）を生成中...")
    build(prs)
    prs.save(OUT_PATH)
    print(f"完了！ {len(prs.slides)} 枚 -> {OUT_PATH}")
