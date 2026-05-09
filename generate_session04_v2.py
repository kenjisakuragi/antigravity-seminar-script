# -*- coding: utf-8 -*-
"""
generate_session04_v2.py
第4回「AI音楽① 30秒で作曲する魔法」— 充実版（30枚）
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "Google_Slide_generator"))
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from design_v2 import *

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(SCRIPT_DIR, "講義04_AI音楽①_v2.pptx")

C1, C2 = "6366F1", "8B5CF6"   # インジゴ×パープル

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
        "AI音楽①\n30秒で作曲する魔法",
        "第4回｜2026年5月11日（月）19:00〜21:00",
        "らくらくAI副業キャンパス")

    # ──────────────────────────────
    # 2. 本日のゴール
    # ──────────────────────────────
    s = add_slide(prs)
    make_cards_slide(s, "本日のゴール", [
        ("🎵", "Suno AIで\n楽曲を作れる", "テキスト入力だけで\nプロ品質の曲を生成\n（音楽知識ゼロOK）"),
        ("🎯", "狙い目ジャンルを\n選べる", "稼ぎやすいジャンル\nBEST5を学び\n自分の方向性を決める"),
        ("💰", "印税ビジネスの\n仕組みを理解する", "再生されるたびに\n自動で入金される\n仕組みを把握"),
    ], accent_c1=C1, accent_c2=C2)

    # ──────────────────────────────
    # 3. 前回の振り返り
    # ──────────────────────────────
    s = add_slide(prs)
    make_dark_summary(s, "前回の振り返り", [
        "✅ YouTube チャンネルを開設し、動画を1本公開した",
        "✅ AI音声（Google AI Studio）でナレーションを生成した",
        "✅ KLING AI or CapCut でキャラクターが喋る動画を完成させた",
        "✅ YouTube に公開して Discord に URL を投稿した",
    ], sub="YouTube 順調ですか？今日から第2の収益源「AI音楽」をスタートします！", c1=C1, c2=C2)

    # ──────────────────────────────
    # 4. 今日のロードマップ
    # ──────────────────────────────
    s = add_slide(prs)
    make_step_flow(s, "今日の90分ロードマップ", [
        ("1", "AI音楽\nビジネス全体像\n（20分）", "仕組み・収益事例\n著作権ルールを理解"),
        ("2", "Suno AI\n完全マスター\n（35分）", "アカウント作成から\n曲の生成\nプロンプト技術"),
        ("3", "狙い目\nジャンル講座\n（15分）", "BEST5の解説と\n稼ぎ方の戦略"),
        ("4", "ハンズオン\n実践\n（20分）", "5曲を生成し\nDiscordに投稿"),
    ], accent_c1=C1, accent_c2=C2)

    # ──────────────────────────────
    # 5. セクション1
    # ──────────────────────────────
    s = add_slide(prs)
    make_section(s, 1, "AI音楽ビジネスの全体像\n〜 印税 = 再生されるたびに自動入金 〜", "19:10 - 19:30", c1=C1, c2=C2)

    # ──────────────────────────────
    # 6. AI音楽ビジネスとは？（概念）
    # ──────────────────────────────
    s = add_slide(prs)
    make_cards_slide(s, "「AIで音楽を作って稼ぐ」とは？", [
        ("🤖", "Suno AIで\n楽曲を作る", "テキストを打ち込むだけ\nで30秒でプロ品質の\n楽曲が完成。費用0円"),
        ("🌍", "配信サービスに\n登録する", "TuneCore等を通じて\nSpotify / Apple Music\n/ YouTube Music に配信"),
        ("💴", "再生されるたびに\n印税が入る", "1再生 = 0.3〜0.5円\n10万再生 = 3〜5万円\n寝てる間にも積み上がる"),
    ], accent_c1=C1, accent_c2=C2)

    # ──────────────────────────────
    # 7. 3段構造の収益モデル
    # ──────────────────────────────
    s = add_slide(prs)
    bg_white(s)
    txt(s, Inches(1), Inches(0.4), Inches(11), Inches(0.65),
        "AI音楽 収益の3段構造", sz=30, clr=C_BLACK, bold=True)
    gbar(s, Inches(1), Inches(1.05), Inches(2.5), Inches(0.04), C1, C2)

    layers = [
        ("C1", "ストリーミング印税",
         "Spotify / Apple Music / YouTube Music 等で再生されるたびに自動収益",
         "安定・継続・寝てても入る"),
        ("C2", "YouTube 動画収益",
         "BGMチャンネルとして楽曲を動画化 → 広告収益も追加",
         "二重取り可能"),
        ("C3", "スキル販売（BGM制作代行）",
         "YouTuber・ポッドキャスター向けに楽曲を受注制作",
         "即金性が高い・単価5,000〜15,000円"),
    ]
    colors = [("6366F1", "8B5CF6"), ("059669", "10B981"), ("D97706", "F59E0B")]
    for i, (tag, title, desc, badge) in enumerate(layers):
        y = Inches(1.4) + i * Inches(1.6)
        c = card(s, Inches(1), y, Inches(11.3), Inches(1.4), shadow=True,
                 grad=(colors[i][0], colors[i][1]))
        txt(s, Inches(1.4), y + Inches(0.1), Inches(6), Inches(0.5),
            title, sz=18, clr=C_WHITE, bold=True)
        txt(s, Inches(1.4), y + Inches(0.62), Inches(7.5), Inches(0.55),
            desc, sz=13, clr=C_LGRAY)
        card(s, Inches(9.3), y + Inches(0.3), Inches(2.6), Inches(0.55),
             fill="1E293B", shadow=False)
        txt(s, Inches(9.4), y + Inches(0.35), Inches(2.5), Inches(0.45),
            badge, sz=11, clr=C_GOLD, bold=True, align=PP_ALIGN.CENTER)
    footer(s, C1, C2)

    # ──────────────────────────────
    # 8. リアルな収益事例
    # ──────────────────────────────
    s = add_slide(prs)
    make_table_slide(s, "リアルな収益事例（実績ベース）",
        ["プラットフォーム", "月間再生数", "推定月収", "ポイント"],
        [
            ["Spotify",       "30万回",  "約12万円", "プレイリスト掲載が鍵"],
            ["Apple Music",   "10万回",  " 約5万円", "iPhone ユーザーが多い"],
            ["YouTube Music", "50万回",  "約8万円",  "BGM長時間再生が強い"],
            ["Amazon Music",  " 5万回",  " 約1.5万円", "加入者が増加中"],
            ["合計",          "95万回",  "約27万円", "1チャンネルの実績"],
        ],
        accent_c1=C1, accent_c2=C2,
        note="📌 10万円を超えるには「月30曲ペース × ジャンル戦略」が必要です")

    # ──────────────────────────────
    # 9. 印税の計算式（ハウツー）
    # ──────────────────────────────
    s = add_slide(prs)
    bg_white(s)
    txt(s, Inches(1), Inches(0.4), Inches(11), Inches(0.65),
        "印税収入の計算式（目標設定に使おう）", sz=30, clr=C_BLACK, bold=True)
    gbar(s, Inches(1), Inches(1.05), Inches(2.5), Inches(0.04), C1, C2)

    formula_lines = [
        ("1再生あたりの収益",   "約 0.3〜0.5円（Spotify基準）"),
        ("月収1万円を達成するには", "約 2〜3万再生 / 月"),
        ("月収10万円を達成するには", "約 20〜30万再生 / 月"),
        ("月収10万円の実現イメージ", "30曲 × 平均月1万再生 = 30万再生"),
    ]
    for i, (label, val) in enumerate(formula_lines):
        y = Inches(1.5) + i * Inches(1.2)
        card(s, Inches(1), y, Inches(5.3), Inches(0.85), fill="F0F5FF", shadow=True)
        txt(s, Inches(1.3), y + Inches(0.18), Inches(4.8), Inches(0.5),
            label, sz=14, clr=RGBColor(0x33,0x33,0x66))
        card(s, Inches(6.8), y, Inches(5.5), Inches(0.85), grad=(C1, C2), shadow=True)
        txt(s, Inches(7.0), y + Inches(0.18), Inches(5.0), Inches(0.5),
            val, sz=16, clr=C_WHITE, bold=True)
    footer(s, C1, C2)

    # ──────────────────────────────
    # 10. 著作権ルール（重要！）
    # ──────────────────────────────
    s = add_slide(prs)
    make_dark_summary(s, "著作権ルール（知らないと収益停止になる！）", [
        "✅ Suno AI で生成した楽曲の著作権は「あなた」にあります",
        "✅ 商用利用（販売・配信）は Suno AI の有料プランで可能",
        "✅ 他アーティストの曲に似せた生成は著作権侵害になるリスクあり",
        "❌ 無料プランで生成した楽曲の商業利用は利用規約違反",
        "❌ 他人の既存楽曲のメロディーをそのまま使うのは NG",
        "📌 必ずプロプラン（月額20ドル〜）に加入してから配信しましょう",
    ], sub="ルールを守れば安全に「合法的な印税マシン」が作れます", c1=C1, c2=C2)

    # ──────────────────────────────
    # 11. セクション2
    # ──────────────────────────────
    s = add_slide(prs)
    make_section(s, 2, "Suno AI 完全マスター\n〜 アカウント作成からプロ技術まで 〜", "19:30 - 20:05", c1=C1, c2=C2)

    # ──────────────────────────────
    # 12. Suno AI アカウント作成
    # ──────────────────────────────
    s = add_slide(prs)
    make_step_flow(s, "Suno AI アカウント作成（5分でできる）", [
        ("1", "suno.com に\nアクセス", "ブラウザで\nhttps://suno.com\nを開く"),
        ("2", "Sign Up\nをクリック", "Google アカウント\nで即ログイン可能\n（メール不要）"),
        ("3", "プラン選択", "まず無料プランで\n動作確認\n→ 後でProに切替"),
        ("4", "Pro プランに\nアップグレード", "月額 20 ドル\n商用利用に\n必須！"),
    ], accent_c1=C1, accent_c2=C2)

    # ──────────────────────────────
    # 13. Suno AI 操作画面の見方
    # ──────────────────────────────
    s = add_slide(prs)
    bg_white(s)
    txt(s, Inches(1), Inches(0.4), Inches(11), Inches(0.65),
        "Suno AI 操作画面の見方", sz=30, clr=C_BLACK, bold=True)
    gbar(s, Inches(1), Inches(1.05), Inches(2.5), Inches(0.04), C1, C2)

    ui_items = [
        ("🎵 Style of Music", "ジャンル・スタイルを自由記述（例：Lo-Fi, Chill, Japanese Pop）"),
        ("📝 Song Description", "楽曲の雰囲気・テーマを説明（例：peaceful morning coffee background）"),
        ("🎤 Lyrics（任意）",   "歌詞を自分で書く or Suno に任せる。インストは空欄でOK"),
        ("⏱️ Generate ボタン",  "クリックすると約30秒で2バージョンを自動生成"),
        ("⬇️ Download",        "生成後に「…」→ Download → MP3/WAVで保存"),
    ]
    for i, (k, v) in enumerate(ui_items):
        y = Inches(1.4) + i * Inches(1.0)
        card(s, Inches(1.0), y, Inches(3.5), Inches(0.75), fill="EEF2FF", shadow=False)
        txt(s, Inches(1.15), y + Inches(0.16), Inches(3.2), Inches(0.5),
            k, sz=13, clr=RGBColor(0x44,0x36,0xB6), bold=True)
        txt(s, Inches(5.0), y + Inches(0.18), Inches(7.3), Inches(0.5),
            v, sz=13, clr=C_DGRAY)
    footer(s, C1, C2)

    # ──────────────────────────────
    # 14. プロンプトの書き方 3段階
    # ──────────────────────────────
    s = add_slide(prs)
    bg_white(s)
    txt(s, Inches(1), Inches(0.4), Inches(11), Inches(0.65),
        "プロンプトの書き方 3段階（初級 → 中級 → 上級）", sz=28, clr=C_BLACK, bold=True)
    gbar(s, Inches(1), Inches(1.05), Inches(2.5), Inches(0.04), C1, C2)

    levels = [
        ("初級", "EEF2FF", "44 36 B6",
         "ジャンル名を1〜2語で入力するだけ",
         "例：「Lo-Fi」「J-POP」「Piano Ballad」"),
        ("中級", "F0FDF4", "16 63 4A",
         "ジャンル + 雰囲気 + 楽器 + テンポ",
         "例：「Lo-Fi Hip Hop, relaxing, piano and rain sounds, 70bpm」"),
        ("上級", "FFF7ED", "92 40 0E",
         "シーン + ターゲット + 楽曲構成 + 感情",
         "例：「Peaceful morning coffee shop ambient, for study, soft guitar and distant cafe noise,\ngentle and warm feeling, instrumental, no drums」"),
    ]
    for i, (lvl, bg, clr_rgb, rule, example) in enumerate(levels):
        y = Inches(1.4) + i * Inches(1.7)
        r, g, b = [int(x, 16) for x in clr_rgb.split()]
        card(s, Inches(1), y, Inches(11.3), Inches(1.55), fill=bg, shadow=True)
        card(s, Inches(1.1), y + Inches(0.1), Inches(1.2), Inches(0.4),
             grad=(C1, C2), shadow=False)
        txt(s, Inches(1.15), y + Inches(0.14), Inches(1.1), Inches(0.35),
            lvl, sz=13, clr=C_WHITE, bold=True, align=PP_ALIGN.CENTER)
        txt(s, Inches(2.5), y + Inches(0.12), Inches(9.5), Inches(0.45),
            rule, sz=14, clr=RGBColor(r, g, b), bold=True)
        txt(s, Inches(2.5), y + Inches(0.65), Inches(9.5), Inches(0.7),
            example, sz=12, clr=C_DGRAY)
    footer(s, C1, C2)

    # ──────────────────────────────
    # 15. コピペ用プロンプト集
    # ──────────────────────────────
    s = add_slide(prs)
    bg_white(s)
    txt(s, Inches(1), Inches(0.4), Inches(11), Inches(0.65),
        "コピペOK！ ジャンル別プロンプト例", sz=30, clr=C_BLACK, bold=True)
    gbar(s, Inches(1), Inches(1.05), Inches(2.5), Inches(0.04), C1, C2)

    prompts = [
        ("Lo-Fi / チルホップ",
         "Lo-Fi Hip Hop, relaxing study music, soft piano and vinyl crackle, 70bpm, instrumental"),
        ("アンビエント / 瞑想",
         "Meditation ambient, peaceful and healing, singing bowl and soft synth pads, slow tempo, no percussion"),
        ("子守唄 / キッズ",
         "Gentle lullaby, for babies and toddlers, music box and soft strings, sweet and warm, very slow tempo"),
        ("ゲーム風BGM",
         "8-bit chiptune adventure, retro video game style, upbeat and exciting, loopable, no vocals"),
        ("J-POP バラード",
         "Japanese Pop Ballad, emotional and bittersweet, piano and acoustic guitar, female vocal impression"),
    ]
    for i, (genre, prompt) in enumerate(prompts):
        y = Inches(1.35) + i * Inches(1.1)
        card(s, Inches(1.0), y, Inches(2.5), Inches(0.85), grad=(C1, C2), shadow=False)
        txt(s, Inches(1.05), y + Inches(0.2), Inches(2.4), Inches(0.5),
            genre, sz=11, clr=C_WHITE, bold=True, align=PP_ALIGN.CENTER)
        card(s, Inches(3.8), y, Inches(8.5), Inches(0.85), fill="F8F8FF", shadow=False)
        txt(s, Inches(4.0), y + Inches(0.18), Inches(8.0), Inches(0.55),
            prompt, sz=11, clr=C_DGRAY)
    footer(s, C1, C2)

    # ──────────────────────────────
    # 16. セクション3
    # ──────────────────────────────
    s = add_slide(prs)
    make_section(s, 3, "狙い目ジャンル BEST 5\n〜 稼ぎやすいジャンルと理由を解説 〜", "20:05 - 20:20", c1=C1, c2=C2)

    # ──────────────────────────────
    # 17. ジャンルBEST5（詳細）
    # ──────────────────────────────
    s = add_slide(prs)
    make_numbered_slide(s, "稼ぎやすいジャンル BEST 5", [
        ("1位", "Lo-Fi / チルホップ",
         "作業・勉強用BGMとして24時間再生される。プレイリストに載りやすく安定した再生数を稼ぐ"),
        ("2位", "アンビエント / 瞑想",
         "ヨガ・睡眠・瞑想コンテンツで長時間再生。1再生あたりの時間が長いため収益効率が高い"),
        ("3位", "子守唄 / キッズ",
         "子育てパパ・ママが毎日繰り返し再生する。競合が少なく参入しやすいブルーオーシャン"),
        ("4位", "J-POPインスト / カバー系",
         "日本語市場で圧倒的な検索数。季節イベント（クリスマス・卒業式）に乗せると爆発的に伸びる"),
        ("5位", "ゲームBGM / 8-bit",
         "ゲーム実況者が使うBGM需要。YouTuberがスキル販売で依頼を受けやすい"),
    ], accent_c1=C1, accent_c2=C2)

    # ──────────────────────────────
    # 18. ジャンル × 収益シミュレーション表
    # ──────────────────────────────
    s = add_slide(prs)
    make_table_slide(s, "ジャンル別 収益シミュレーション",
        ["ジャンル", "月間再生数（目安）", "月収目安", "達成しやすさ"],
        [
            ["Lo-Fi",      "5〜20万回",  "2〜8万円",  "★★★★☆"],
            ["アンビエント",  "3〜15万回",  "1〜6万円",  "★★★☆☆"],
            ["キッズ・子守唄", "5〜30万回",  "2〜10万円", "★★★★★"],
            ["J-POPカバー系", "10〜50万回", "4〜20万円", "★★★☆☆"],
            ["ゲームBGM",    "2〜10万回",  "1〜4万円",  "★★★★☆"],
        ],
        accent_c1=C1, accent_c2=C2,
        note="📌 キッズ・子守唄は競合が少なくて始めやすい「隠れたチャンス」")

    # ──────────────────────────────
    # 19. 品質を上げる3つのコツ
    # ──────────────────────────────
    s = add_slide(prs)
    make_cards_slide(s, "楽曲クオリティを上げる3つのコツ", [
        ("🔁", "2回生成して\n良い方を選ぶ", "Suno AIは1回の生成で\n2パターン作成\n必ず聴き比べる"),
        ("✂️", "長さを\nコントロールする", "「1分30秒以内」に\n指定すると\nストリーミング適性UP"),
        ("🎛️", "Extend機能で\n自然なループに", "生成後に Extend を使って\n冒頭部分をシームレスに\nループさせる"),
    ], accent_c1=C1, accent_c2=C2)

    # ──────────────────────────────
    # 20. よくある失敗とその対処法
    # ──────────────────────────────
    s = add_slide(prs)
    make_table_slide(s, "よくある失敗と対処法",
        ["失敗パターン", "原因", "対処法"],
        [
            ["歌詞が変な日本語になった",   "英語プロンプト × 日本語歌詞の混在", "歌詞欄を空欄にしてインスト生成"],
            ["テンポが速すぎる",          "テンポ指定がない",       "「80bpm」のように BPM を明記する"],
            ["毎回同じような曲になる",     "プロンプトが短すぎる",   "楽器・感情・シーンを3つ以上追加"],
            ["ダウンロードできない",       "無料プランの上限超過",   "翌日にリセットされるか Pro に移行"],
            ["BGMにボーカルが入る",       "Vocal プロンプトが混入", "「instrumental, no vocals」を必ず追記"],
        ],
        accent_c1=C1, accent_c2=C2,
        note="📌 失敗は資産。試行錯誤で自分だけのプロンプトパターンが見つかります")

    # ──────────────────────────────
    # 21. 実演タイム
    # ──────────────────────────────
    s = add_slide(prs)
    make_emphasis(s,
        "【実演タイム】今から5曲をその場で作ります",
        "テキスト入力 → 30秒 → プロ品質の楽曲が完成\nみなさんの目の前でリアルタイム生成",
        gold=True)

    # ──────────────────────────────
    # 22. セクション4（ハンズオン）
    # ──────────────────────────────
    s = add_slide(prs)
    make_section(s, 4, "ハンズオン実践\n〜 自分の5曲を今日作ろう 〜", "20:20 - 20:40", c1=C1, c2=C2)

    # ──────────────────────────────
    # 23. ハンズオン手順
    # ──────────────────────────────
    s = add_slide(prs)
    make_numbered_slide(s, "ハンズオン 手順", [
        ("STEP 1", "Suno AI にログインする",
         "suno.com にアクセス → Google アカウントでログイン → Pro プラン確認"),
        ("STEP 2", "まずは「Lo-Fi」で1曲作る",
         "プロンプト：「Lo-Fi Hip Hop, relaxing study music, piano and vinyl crackle, 70bpm, instrumental」"),
        ("STEP 3", "好きなジャンルで3曲作る",
         "コピペ用プロンプト集（前のスライド）から選んで試す。失敗を恐れずどんどん生成！"),
        ("STEP 4", "ベスト1曲を選ぶ",
         "生成した中で「これは良い！」と思った曲をDownloadしておく"),
        ("STEP 5", "Discord に投稿する",
         "#第4回-ai音楽① チャンネルにベスト曲を投稿 → 仲間に聴いてもらおう"),
    ], accent_c1=C1, accent_c2=C2)

    # ──────────────────────────────
    # 24. 今週の課題
    # ──────────────────────────────
    s = add_slide(prs)
    make_numbered_slide(s, "今週の課題", [
        ("課題①", "楽曲を合計15曲生成する",
         "Lo-Fi / アンビエント / キッズ など3ジャンル以上を試して自分の方向性を見つける"),
        ("課題②", "ベスト3曲を Discord に投稿",
         "仲間からフィードバックをもらって次週の配信候補を決める"),
        ("課題③", "YouTube 動画の投稿を継続",
         "第1の収益源（YouTube）も止めないこと。コンテンツは積み重ねが命です"),
        ("課題④（任意）", "Suno AI Pro プランに移行する",
         "来週の配信サービス登録に備えて商用利用ライセンスを準備しておこう"),
    ], accent_c1=C1, accent_c2=C2)

    # ──────────────────────────────
    # 25. 収益源ダッシュボード
    # ──────────────────────────────
    dashboard(prs, "収益源ダッシュボード — 第4回終了時点",
        [
            ["① YouTube動画",   "✅ 稼働中",    "継続投稿"],
            ["② AI音楽",        "🟡 仕込み中",  "15曲生成が課題"],
            ["③ Kindle出版",    "⬜ まだ",      "第6回（5/25）"],
            ["④ AIブログ",      "⬜ まだ",      "第7回（6/1）"],
            ["⑤ 画像販売",      "⬜ まだ",      "第8回（6/8）"],
            ["⑥ ショート動画",  "⬜ まだ",      "第9回（6/15）"],
            ["⑦ スキル販売",    "⬜ まだ",      "第10回（6/22）"],
        ],
        "📌 来週はこの曲を世界100か国に配信します。一度配信したら永久に印税が入ります！")

    # ──────────────────────────────
    # 26. Q&A よくある質問
    # ──────────────────────────────
    s = add_slide(prs)
    make_dark_summary(s, "よくある質問 Q&A", [
        "Q: 音楽の知識がゼロでも大丈夫？",
        "→ 大丈夫！テキストを打ち込むだけです。コード進行や楽譜の知識は一切不要",
        "Q: 無料プランで試せる？",
        "→ はい、まず無料で試して感触をつかんでから Pro に移行がおすすめ",
        "Q: 生成した曲はすぐ配信できる？",
        "→ Pro プランなら OK。無料プランで生成した曲の商業利用は利用規約違反なので注意",
    ], sub="他にも疑問があれば Discord の #質問箱 へ！", c1=C1, c2=C2)

    # ──────────────────────────────
    # 27. クロージング
    # ──────────────────────────────
    s = add_slide(prs)
    make_emphasis(s,
        "お疲れさまでした！来週は世界100か国に配信します 🌍",
        "📌 課題：15曲生成 ＋ ベスト3曲を Discord 投稿\n"
        "📌 YouTube 動画も継続\n"
        "📌 来週月曜 19:00 にお会いしましょう！")


if __name__ == "__main__":
    prs = create_prs()
    print("第4回（v2）を生成中...")
    build(prs)
    prs.save(OUT_PATH)
    print(f"完了！ {len(prs.slides)} 枚 -> {OUT_PATH}")
