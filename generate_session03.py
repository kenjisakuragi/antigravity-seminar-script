# -*- coding: utf-8 -*-
"""第3回「AI動画② キャラクターが喋る！世界に届ける日」改訂版"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "Google_Slide_generator"))
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from design_v2 import *
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
L_C1, L_C2 = "0EA5E9", "0284C7"

def build(prs):
    # ─── タイトル ───
    s = add_slide(prs)
    make_title_slide(s, "AI動画②\nキャラクターが喋る！世界に届ける日", "第3回｜2026年5月4日（月）20:00〜22:00", "らくらくAI副業キャンパス")

    # ─── ゴール ───
    s = add_slide(prs)
    make_cards_slide(s, "🎯 本日のゴール", [
        ("🎙️", "AIで台本を\n読み上げる", "Google AI Studioで\n自然な音声を生成\n（テキスト貼るだけ）"),
        ("🎬", "キャラクターが\n喋る動画を完成", "KLING AIで\nリップシンク動画\nを作成！"),
        ("🌍", "YouTubeに\n公開する！", "今日が記念日\n世界に届く初めての1本"),
    ], accent_c1=L_C1, accent_c2=L_C2)

    # ─── 振り返り ───
    s = add_slide(prs)
    make_dark_summary(s, "前回の振り返り", [
        "✅ YouTubeチャンネルの土台を作った",
        "✅ Geminiで台本1本を完成させた",
        "✅ 背景画像 ＋ AIキャラクターを生成した",
    ], sub="今日は「台本・背景・キャラクター」をつなぎ合わせて動画にします！", c1=L_C1, c2=L_C2)

    # ─── 課題チェック ───
    s = add_slide(prs)
    make_cards_slide(s, "課題チェック｜素材、仕上がりましたか？", [
        ("📝", "台本は？", "タイトルの投票結果を\n発表！\nどれが人気だったか…"),
        ("🖼️", "背景画像は？", "皆さんの世界観を\n画面でシェア！\nどんな雰囲気になった？"),
        ("🎭", "キャラクターは？", "あなたの分身を\n見せてください！\nDiscordで大公開"),
    ], accent_c1=L_C1, accent_c2=L_C2)

    # ─── 今日のロードマップ ───
    s = add_slide(prs)
    make_step_flow(s, "今日のロードマップ｜動画完成までの流れ", [
        ("1", "Google AI Studio\nで音声生成", "台本を貼るだけで\n自然な声が完成\n（共通・全員）"),
        ("2A", "【プレミアム】\nKLING AIで\nリップシンク", "キャラが喋る\n本格動画が完成\n（月1,500円〜）"),
        ("2B", "【コスト重視】\n画像＋音声で\n動画合成", "CapCutで\n背景画像＋音声\n（無料で可能）"),
        ("3", "公開設定して\nYouTubeへ！", "タイトル・説明文も\nAIが作成\n今日が記念日🎉"),
    ], accent_c1=L_C1, accent_c2=L_C2)

    # ─── 2ルートの説明 ───
    s = add_slide(prs)
    make_comparison(s, "あなたはどちらのルートで進みますか？",
        "🎭 プレミアムルート", [
            "キャラクターが実際に口を動かして喋る",
            "圧倒的なWOW！ クオリティ",
            "KLING AI（月1,500円〜）を使用",
            "まずは1ヶ月お試しがおすすめ",
            "将来的なチャンネル差別化に最適",
        ],
        "💰 コスト重視ルート", [
            "背景画像＋AI音声＋テロップの組み合わせ",
            "完全無料で始められる",
            "CapCutで動画合成（スマホもOK）",
            "YouTubeに多い「ゆっくり解説」スタイル",
            "慣れてからプレミアムに移行もあり",
        ],
        l_c1="94A3B8", l_c2="64748B", r_c1=L_C1, r_c2=L_C2)

    # ══════════════════
    # Section 1：Google AI Studio 音声生成（共通）
    # ══════════════════
    s = add_slide(prs)
    make_section(s, 1, "Google AI Studio で音声生成\n〜 声を出さなくていいんです（共通） 〜", "20:00 - 45:00", c1=L_C1, c2=L_C2)

    s = add_slide(prs)
    make_emphasis(s, "WOW！ この声、AIが作ったものです",
        "「えっ、これ本当に人間じゃないの？」そう思うほど自然な声が、\n台本をコピペするだけで生成されます。\n\nGoogle AI Studioは、Geminiと同じGoogleが提供する\n高品質な音声生成ツールです。無料から使えます！", gold=True)

    s = add_slide(prs)
    make_cards_slide(s, "Google AI Studioとは？", [
        ("🌐", "Googleが提供\nする無料ツール", "Geminiの兄弟ツール\nGoogleアカウントで\n無料で使える"),
        ("🎤", "驚くほど自然な\n日本語音声", "感情表現も可能\n速さ・音程も調整\nできます"),
        ("🎭", "キャラ音声に\n最適", "先週作った\nキャラクターの「声」として\n使います"),
    ], accent_c1=L_C1, accent_c2=L_C2)

    s = add_slide(prs)
    make_step_flow(s, "Google AI Studio 音声生成 4ステップ", [
        ("1", "aistudio.google.com\nにアクセス", "Googleアカウントで\nログインするだけ\n（無料）"),
        ("2", "「音声生成」を\n選択", "左メニューから\n「Speech」を選ぶ"),
        ("3", "台本を\n貼り付ける", "Geminiで作った\n台本テキストを\nコピペ"),
        ("4", "声を選んで\n生成！", "声の種類・速さを\n選んでボタンを押す\n→ 音声ファイル完成"),
    ], accent_c1=L_C1, accent_c2=L_C2)

    s = add_slide(prs)
    make_cards_slide(s, "【解説】声のクオリティを上げる3つのコツ", [
        ("🐌", "速さを調整", "少しゆっくり目に設定\n（0.85〜0.9倍速）\n聴きやすさが段違い"),
        ("⏸️", "間（ま）を入れる", "台本の「、。」を増やすと\n自然な間ができて\nプロの語り口になる"),
        ("🎭", "キャラに合わせた\n声を選ぶ", "神秘的キャラ→落ち着いた声\nかわいいキャラ→明るい声\n世界観を合わせよう"),
    ], accent_c1=L_C1, accent_c2=L_C2)

    # ══════════════════
    # Section 2A：KLING AI（プレミアムルート）
    # ══════════════════
    s = add_slide(prs)
    make_section(s, 2, "【プレミアムルート】KLING AI でリップシンク\n〜 キャラクターが本当に喋り出す 〜", "45:00 - 70:00", c1=L_C1, c2=L_C2)

    s = add_slide(prs)
    make_emphasis(s, "WOW！ キャラクターが本当に喋り出します",
        "「リップシンク」とは、音声に合わせてキャラクターの口が動く技術のこと。\n\n先ほど作ったキャラクター画像 ＋ 音声ファイルをKLING AIに渡すだけで、\nキャラクターが実際に口を動かして台本を読んでくれます！", gold=True)

    s = add_slide(prs)
    make_cards_slide(s, "KLING AIとは？（料金も正直にお伝えします）", [
        ("⚡", "世界最高水準の\nAI動画生成AI", "中国発の動画生成AI\nリップシンク機能が\n特に優秀"),
        ("💰", "料金プラン", "無料：月36クレジット\n（動画数本分）\nライト：月約1,500円〜"),
        ("✅", "おすすめの\n始め方", "まず無料で試して\n良ければ1ヶ月だけ\nお試し契約がベスト"),
    ], accent_c1=L_C1, accent_c2=L_C2)

    s = add_slide(prs)
    make_emphasis(s, "1ヶ月お試しを提案します",
        "まずは無料枠（月36クレジット）で試してみてください。\n動画数本分は無料で作れます。\n\n「これは使える！」と感じたら、ライトプラン（月約1,500円）を1ヶ月だけ契約してみましょう。\n📌 1ヶ月で元を取れるか確かめてから、継続を判断するのがおすすめです", gold=True)

    s = add_slide(prs)
    make_step_flow(s, "KLING AI でリップシンク動画を作る 4ステップ", [
        ("1", "KLING AIに\nアクセス", "klingai.com に\nアクセスして\n無料登録"),
        ("2", "「AI Video」→\n「Lip Sync」を選択", "リップシンク機能を\n選んでクリック"),
        ("3", "キャラ画像＋\n音声をアップ", "先週作ったキャラ画像と\n今日作った音声ファイルを\nアップロード"),
        ("4", "生成！", "数分で\nキャラクターが喋る\n動画が完成🎉"),
    ], accent_c1=L_C1, accent_c2=L_C2)

    s = add_slide(prs)
    make_cards_slide(s, "【解説】リップシンク動画をさらに良くするコツ", [
        ("🖼️", "画像の解像度を\n上げる", "ぼやけた画像だと\n口の動きが不自然になる\n高解像度で生成しよう"),
        ("🎙️", "音声は明瞭に", "雑音のない\nクリアな音声が\nリップシンク精度を上げる"),
        ("⏱️", "最初は\n短い動画から", "30秒〜1分で\nまず試してから\n長い動画に挑戦"),
    ], accent_c1=L_C1, accent_c2=L_C2)

    # ══════════════════
    # Section 2B：コスト重視ルート
    # ══════════════════
    s = add_slide(prs)
    make_section(s, 3, "【コスト重視ルート】画像＋音声＋テロップ\n〜 無料でも十分プロ品質！ 〜", "45:00 - 70:00", c1=L_C1, c2=L_C2)

    s = add_slide(prs)
    make_emphasis(s, "コスト重視ルートも全然アリ！",
        "「ゆっくり解説」スタイルのYouTubeチャンネルで\n月数十万円を稼いでいるクリエイターはたくさんいます。\n\nリップシンクはなくても、世界観のある背景画像＋自然なAI音声＋見やすいテロップで\n十分魅力的な動画が作れます。", gold=True)

    s = add_slide(prs)
    make_step_flow(s, "CapCutで動画を仕上げる 5ステップ", [
        ("1", "素材を準備", "背景画像＋\nGoogle AI Studio音声\nをフォルダにまとめる"),
        ("2", "CapCutに\nインポート", "スマホ・PCどちらでも\nOK。無料で使えます"),
        ("3", "自動テロップを\n生成", "「自動テキスト」機能で\n音声から字幕が\nワンクリックで完成！"),
        ("4", "BGMと\n動きをつける", "著作権フリーBGM追加\n画像に「スライド」効果で\nプロ感アップ"),
        ("5", "書き出し→\n完成！", "MP4で書き出し\n→ YouTube用\n動画ファイル完成"),
    ], accent_c1=L_C1, accent_c2=L_C2)

    # ──────────────────
    # 2ルートの比較まとめ
    # ──────────────────
    s = add_slide(prs)
    make_comparison(s, "2ルートの比較まとめ",
        "🎭 プレミアムルート（KLING AI）",
        [
            "キャラクターが実際に口を動かす",
            "圧倒的な差別化・WOWクオリティ",
            "月1,500円〜（まず無料枠で試そう）",
            "動画1本あたりのコスト：数十円〜",
        ],
        "💰 コスト重視ルート（CapCut）",
        [
            "背景＋音声＋テロップのシンプル構成",
            "完全無料・今日すぐ始められる",
            "「ゆっくり解説」スタイルで実績あり",
            "慣れてからプレミアムに移行もOK",
        ],
        l_c1=L_C1, l_c2=L_C2, r_c1="16A34A", r_c2="15803D")

    # ══════════════════
    # Section 4：公開設定（共通）
    # ══════════════════
    s = add_slide(prs)
    make_section(s, 4, "公開設定の最適化\n〜 タイトルも説明文もAIが作ります（共通） 〜", "70:00 - 80:00", c1=L_C1, c2=L_C2)

    s = add_slide(prs)
    make_cards_slide(s, "YouTube公開設定（全部AIにおまかせ）", [
        ("📝", "タイトル", "Geminiに\n「クリックされやすい\nタイトルを5個」"),
        ("📋", "説明文", "Geminiに\n「この動画の内容で\n説明文を書いて」"),
        ("🏷️", "タグ", "Geminiに\n「関連検索キーワードを\n15個提案して」"),
    ], accent_c1=L_C1, accent_c2=L_C2)

    s = add_slide(prs)
    bg_grad(s, DARK1, "0C2340")
    txt(s, Inches(1), Inches(0.5), Inches(11), Inches(0.7),
        "タイトル生成プロンプト例（Geminiにコピペ）", sz=24, clr=C_GOLD, bold=True)
    card(s, Inches(1.2), Inches(1.4), Inches(10.9), Inches(5.0),
         grad=(DARK2, "0F3460"), radius=0.06, shadow=True, border=RGBColor(0x0E, 0xA5, 0xE9))
    multi_txt(s, Inches(1.8), Inches(1.7), Inches(10), Inches(4.5), [
        "以下の動画のタイトルを5つ提案してください。",
        "",
        "【動画の内容】",
        "・ジャンル：〇〇（例：スピリチュアル）",
        "・テーマ：〇〇（例：運気が上がる朝の習慣）",
        "",
        "【条件】",
        "・クリックしたくなるような興味を引くタイトル",
        "・30文字以内",
        "・「〇〇な人」「知らないと損」「実は〇〇だった」などのパターンを活用",
    ], sz=14, clr=C_WHITE, align=PP_ALIGN.LEFT)
    txt(s, Inches(1.2), Inches(6.6), Inches(10.9), Inches(0.4),
        "📌 タイトルがクリック率を決めます。何案も出してもらって一番良いものを選びましょう", sz=12, clr=C_GOLD)
    footer(s, L_C1, L_C2)

    s = add_slide(prs)
    make_emphasis(s, "【解説】サムネイルで再生数が10倍変わります",
        "YouTubeの視聴者は、サムネイルで「見るか見ないか」を0.3秒で判断します。\n\nCanvaで「タイトル文字 ＋ キャラクター画像 ＋ 背景画像」を組み合わせると\n無料でプロ品質のサムネイルが作れます。\n\n📌 大きな文字・鮮やかな色・シンプルなデザインが鉄則！", gold=False)

    # ══════════════════
    # Section 5：ハンズオン
    # ══════════════════
    s = add_slide(prs)
    make_section(s, 5, "ハンズオン実践\n〜 全員が1本、公開する！ 〜", "80:00 - 110:00", c1=L_C1, c2=L_C2)

    s = add_slide(prs)
    make_numbered_slide(s, "✋ ハンズオン — 今日のワーク（共通）", [
        ("1", "Google AI Studioで音声を生成する",
         "台本をコピペして、キャラに合った声を選び音声ファイルを作りましょう"),
        ("2A", "【プレミアム】KLING AIでリップシンク動画を作る",
         "キャラ画像＋音声をアップして、キャラが喋る動画を完成させよう"),
        ("2B", "【コスト重視】CapCutで画像＋音声＋テロップの動画を作る",
         "素材を合成して、テロップ・BGMをつけて動画を完成させよう"),
        ("3", "タイトル・説明文・タグをAIで作り、YouTube公開！",
         "Geminiにプロンプトを貼り付けて最高のタイトルを決め、公開ボタンを押そう"),
    ], accent_c1=L_C1, accent_c2=L_C2)

    s = add_slide(prs)
    make_emphasis(s, "困ったときの合言葉：「詰まったらすぐ教えて！」",
        "エラーが出ても、うまくできなくても、それは当たり前のことです。\n遠慮なくDiscordや画面共有で助けを求めてください。\n\n全員が公開するまで、私たちは絶対に待ちます！", gold=True)

    # ─── クロージング ───
    s = add_slide(prs)
    bg_grad(s, DARK1, "0C2340")
    txt(s, Inches(1), Inches(1.3), Inches(11.3), Inches(1.5),
        "🎉 おめでとうございます！\n今日からあなたはYouTuberです！", sz=32, clr=C_GOLD, bold=True, align=PP_ALIGN.CENTER)
    txt(s, Inches(1), Inches(3.2), Inches(11.3), Inches(1.5),
        "あなたのキャラクターが喋る動画が、今この瞬間、世界中で見られる状態になりました。\n3週間前まで、AIを触ったことすらなかったかもしれない。\nそれが今日、世界に向けて自分だけの作品を発信できるようになった。\n胸を張ってください！", sz=16, clr=C_WHITE, align=PP_ALIGN.CENTER)
    footer(s, L_C1, L_C2)

    s = add_slide(prs)
    make_numbered_slide(s, "📝 今週の課題", [
        ("1", "2本目の動画も完成＆公開する",
         "今日のやり方を使って、もう1本の台本も動画にしましょう。2本目は確実に速くなります"),
        ("2", "公開したURLをDiscordに投稿",
         "「私の動画、ここにあります！」と宣言しましょう。仲間みんなで見に行きます"),
        ("3", "仲間の動画にコメントする",
         "良かったところを1つ書くだけでOK。コメントされると本当に励みになります"),
    ], accent_c1=L_C1, accent_c2=L_C2)

    s = add_slide(prs)
    make_table_slide(s, "📊 収益源ダッシュボード — 第3回時点",
        ["収益源", "ステータス", "メモ"],
        [
            ["① YouTube動画", "✅ 稼働中！", "初公開おめでとうございます！"],
            ["② AI音楽", "⬜ 次回", "第5回でスタート！"],
            ["③ Kindle出版", "⬜ まだ", "第6回で開始"],
            ["④ AIブログ", "⬜ まだ", "第7回で開始"],
            ["⑤ 画像販売", "⬜ まだ", "第8回で開始"],
            ["⑥ ショート動画", "⬜ まだ", "第9回で開始"],
            ["⑦ スキル販売", "⬜ まだ", "第10回で開始"],
        ],
        accent_c1=L_C1, accent_c2=L_C2, highlight_last=False,
        note="📌 最初の収益源が動き始めました！これはあなたの財産です")

    s = add_slide(prs)
    make_emphasis(s, "🎵 来週の予告\n「AI音楽① 30秒で世界中に配信される楽曲を作る」",
        "音楽の知識はゼロでOK。\n「明るい感じの曲を作って」のたった1行で、\n本物の楽曲がSpotifyやYouTube Musicで配信されます！", gold=True)

    s = add_slide(prs)
    make_emphasis(s, "お疲れさまでした！\n動画は増えれば増えるほど、あなたの財産になります 📈",
        "📌 課題：2本目の動画を公開する\n📌 公開URLをDiscordに投稿して仲間に見てもらおう\n📌 来週月曜20:00にまたお会いしましょう！")

if __name__ == "__main__":
    prs = create_prs()
    print("第3回を生成中...")
    build(prs)
    out = os.path.join(SCRIPT_DIR, "講義03_AI動画②_v5.pptx")
    prs.save(out)
    print(f"完了！ スライド{len(prs.slides)}枚 → {out}")
