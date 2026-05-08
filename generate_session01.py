# -*- coding: utf-8 -*-
"""
generate_session01.py — 第1回講義パワポ生成
「はじめの一歩 — AIと友達になる日」
4/20（月）120分
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "Google_Slide_generator"))
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from design_v2 import *

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# ── 講義用カラー定義 ──
# Month 1 = ブルー〜パープル系
L_C1 = "6366F1"  # インディゴ
L_C2 = "8B5CF6"  # バイオレット
L_GOLD = "F59E0B"


def build_session01(prs):
    """第1回：はじめの一歩 — AIと友達になる日"""

    # ═══ 1. タイトルスライド ═══
    s = add_slide(prs)
    make_title_slide(s,
        "はじめの一歩\nAIと友達になる日",
        "第1回｜2026年4月20日（月）19:00〜21:00",
        "らくらくAI副業キャンパス")

    # ═══ 2. 本日のゴール ═══
    s = add_slide(prs)
    make_cards_slide(s, "🎯 本日のゴール", [
        ("🤖", "Geminiが\n使えるようになる", "Googleアカウントで\n基本操作を完全マスター"),
        ("🤝", "仲間と繋がる", "Discordで自己紹介\n同じ志を持つ仲間と出会う"),
        ("🗺️", "全体像を把握する", "3ヶ月で7つの収益源を\n手に入れるロードマップ"),
    ], accent_c1=L_C1, accent_c2=L_C2)

    # ═══ 3. 3ヶ月ロードマップ ═══
    s = add_slide(prs)
    make_step_flow(s, "3ヶ月ロードマップ｜全12回の旅", [
        ("M1", "AI基礎 × YouTube\n× 音楽", "第1〜4回\nAIの使い方を覚え\nYouTube＆音楽を\nスタート"),
        ("M2", "毎週「新しい\n稼ぎ方」が増える", "第5〜8回\nKindle・ブログ\n画像販売を追加"),
        ("M3", "仕組みの完成\n× 卒業", "第9〜12回\nショート動画・スキル販売\n全自動化＆卒業"),
    ], accent_c1=L_C1, accent_c2=L_C2)

    # ═══ 4. 12回の講義一覧 ═══
    s = add_slide(prs)
    make_table_slide(s, "全12回 講義スケジュール",
        ["回", "日付", "講義タイトル", "収益源"],
        [
            ["1", "4/20", "はじめの一歩 — AIと友達になる日", "—"],
            ["2", "4/27", "AI動画① 台本も画像もAIにおまかせ", "YouTube（準備）"],
            ["3", "5/4",  "AI動画② 動画を完成させて世界に届ける", "✅ YouTube"],
            ["4", "5/11", "AI音楽① 30秒で作曲する魔法", "AI音楽（準備）"],
            ["5", "5/18", "AI音楽② 世界100か国に配信", "✅ AI音楽"],
            ["6", "5/25", "AIに本を書かせてAmazonで売る", "✅ Kindle"],
        ],
        accent_c1=L_C1, accent_c2=L_C2, highlight_last=False,
        note="📌 全12回で7つの収益源が手に入ります")

    # ═══ 5. 12回の講義一覧（後半） ═══
    s = add_slide(prs)
    make_table_slide(s, "全12回 講義スケジュール（続き）",
        ["回", "日付", "講義タイトル", "収益源"],
        [
            ["7", "6/1",  "AIブログで寝てる間にアフィリ収入", "✅ ブログ"],
            ["8", "6/8",  "AIに描かせて売る — スタンプ＆グッズ", "✅ 画像販売"],
            ["9", "6/15", "AIショート動画で一気にバズる", "✅ TikTok等"],
            ["10", "6/22", "AIスキルを「商品」にして売る", "✅ スキル販売"],
            ["11", "6/29", "自動で稼ぐ仕組みを完成させる", "全自動化"],
            ["12", "7/6",  "🎓 卒業 — 3ヶ月前のあなたへ", "成果発表"],
        ],
        accent_c1=L_C1, accent_c2=L_C2, highlight_last=False,
        note="📌 毎週月曜19:00〜21:00のライブ講義＋週間課題")

    # ═══ 6. 講師自己紹介 ═══
    s = add_slide(prs)
    make_simple_slide(s, "講師自己紹介", [
        "11歳で『マーフィーの法則』に出会い、潜在意識の世界にハマる",
        "東京大学でAIを専門に研究",
        "副業開始 → 最初の3ヶ月は1円も稼げず…",
        "「AI × 自動化」の仕組みに気づいて、人生が変わった",
        "現在：副業の収入が本業を超える",
        "📌 今日から3ヶ月間、一緒に走ります！",
    ], accent_c1=L_C1, accent_c2=L_C2)

    # ═══ 7. 講義のルール ═══
    s = add_slide(prs)
    make_cards_slide(s, "📋 講義のルール", [
        ("📺", "画面共有で\n一緒に進みます", "操作手順は「指差し確認」\nレベルで丁寧に解説\n置いていきません"),
        ("💬", "Discordで\n質問OK", "わからないことは\nいつでも質問\n仲間も助けてくれます"),
        ("📝", "毎週の課題で\n定着", "講義の学びを\n実践で身につける\n次回に成果シェア"),
    ], accent_c1=L_C1, accent_c2=L_C2)

    # ═══ 8. Discordの使い方 ═══
    s = add_slide(prs)
    make_step_flow(s, "Discord — 仲間と繋がる場所", [
        ("1", "アプリを\nインストール", "スマホでもPCでもOK\nApp Store / Google Play\nまたはブラウザ版"),
        ("2", "招待リンクから\n参加", "講義後にリンクを\nお送りします\nクリックするだけ"),
        ("3", "自己紹介を\n投稿", "名前・動機・意気込みを\n#自己紹介 チャンネルに\n投稿しましょう"),
    ], accent_c1=L_C1, accent_c2=L_C2)

    # ═══ 9. セクション仕切り：Gemini基礎 ═══
    s = add_slide(prs)
    make_section(s, 1, "Gemini基礎\n〜 AIと友達になろう 〜", "20:00 - 35:00",
                c1=L_C1, c2=L_C2)

    # ═══ 10. ChatGPTとは ═══
    s = add_slide(prs)
    make_cards_slide(s, "Geminiとは？", [
        ("🤖", "GoogleのAI\nアシスタント", "文章を書く、アイデアを出す\n質問に答える、相談に乗る\nGoogleが作った最新AI"),
        ("💬", "会話するだけで\n使える", "日本語で話しかけるだけ\n難しい操作は一切なし\nスマホでもPCでもOK"),
        ("🆓", "無料で\n始められる", "Googleアカウントだけで開始\nGmailがあればそのまま使える\n今日ここで一緒にやります"),
    ], accent_c1=L_C1, accent_c2=L_C2)

    # ═══ 11. アカウント作成ステップ ═══
    s = add_slide(prs)
    make_step_flow(s, "Gemini を始める（1分で完了）", [
        ("1", "サイトにアクセス", "gemini.google.com\nをブラウザで開く"),
        ("2", "Googleアカウントで\nログイン", "Gmailをお持ちなら\nそのままログインOK"),
        ("3", "Googleアカウントが\nない方", "accounts.google.com\nで無料作成（3分）"),
        ("4", "ログインしたら\n準備完了！", "画面が開いたら\nもうAIと話せます"),
    ], accent_c1=L_C1, accent_c2=L_C2)

    # ═══ 12. 初めてのプロンプト ═══
    s = add_slide(prs)
    make_emphasis(s, "初めてのプロンプト\n「こんにちは！私のことを覚えてね」",
                  "Geminiは、話しかけるだけで動きます\n難しいコマンドは一切不要です", gold=True)

    # ═══ 13. セクション仕切り：プロンプトの黄金パターン ═══
    s = add_slide(prs)
    make_section(s, 2, "プロンプトの黄金パターン\n〜 この3つだけで何でもできる 〜", "35:00 - 55:00",
                c1=L_C1, c2=L_C2)

    # ═══ 14. 黄金パターン3種 ═══
    s = add_slide(prs)
    make_cards_slide(s, "プロンプト 黄金の3パターン", [
        ("❶", "指示型", "「〇〇してください」\n\n例：自己紹介文を\n300文字で書いてください"),
        ("❷", "質問型", "「〇〇について教えて」\n\n例：AI副業の\nメリットを3つ教えて"),
        ("❸", "条件型", "「△△という条件で作って」\n\n例：40代女性向けに\n優しい文体で書いて"),
    ], accent_c1=L_C1, accent_c2=L_C2)

    # ═══ 15. 指示型の例 ═══
    s = add_slide(prs)
    make_faq(s,
        "指示型プロンプトの例",
        "✅「自己紹介文を300文字で書いてください」\n\n"
        "✅「今日の晩ごはんのレシピを3つ提案してください」\n\n"
        "✅「以下の文章を、小学生でもわかるように書き直してください」\n\n"
        "📌 ポイント：「〜してください」で終わる＝指示型\n（Geminiでそのまま使えます）")

    # ═══ 16. 質問型の例 ═══
    s = add_slide(prs)
    make_faq(s,
        "質問型プロンプトの例",
        "✅「AI副業のメリットを3つ教えてください」\n\n"
        "✅「YouTubeで稼ぐ仕組みを、簡単に説明してください」\n\n"
        "✅「40代から始められる副業を5つ挙げてください」\n\n"
        "📌 ポイント：「教えて」「説明して」＝質問型")

    # ═══ 17. 条件型の例 ═══
    s = add_slide(prs)
    make_faq(s,
        "条件型プロンプトの例",
        "✅「40代女性向けに、優しい文体で自己紹介文を書いて」\n\n"
        "✅「初心者にもわかるように、箇条書きで5つにまとめて」\n\n"
        "✅「スピリチュアル好きの人に響く、ブログのタイトルを10個作って」\n\n"
        "📌 ポイント：条件を加える＝精度が上がる！")

    # ═══ 18. 3パターンの組み合わせ ═══
    s = add_slide(prs)
    make_emphasis(s,
        "📌 この3パターンの組み合わせだけで\nAIは何でもやってくれます",
        "指示 × 質問 × 条件\n＝ 最強のプロンプト")

    # ═══ 19. セクション仕切り：AIでできること体験 ═══
    s = add_slide(prs)
    make_section(s, 3, "AIでできること体験\n〜 驚きの連続 〜", "55:00 - 70:00",
                c1=L_C1, c2=L_C2)

    # ═══ 20. AIでできること一覧 ═══
    s = add_slide(prs)
    make_cards_slide(s, "AIでできること — 驚きの5分間", [
        ("✍️", "文章作成", "ブログ記事\nメール文\n自己紹介"),
        ("💡", "アイデア出し", "ビジネスアイデア\n企画案\nネーミング"),
        ("🌍", "翻訳・要約", "英語⇔日本語\n長文の要約\n議事録作成"),
        ("🎯", "相談・分析", "悩み相談\nデータ分析\n意思決定サポート"),
    ], accent_c1=L_C1, accent_c2=L_C2)

    # ═══ 21. 実演タイム ═══
    s = add_slide(prs)
    make_emphasis(s, "【実演タイム】\nAIの驚きパワーを体験しましょう",
                  "文章作成 → アイデア出し → 翻訳 → 相談\nリアルタイムでお見せします", gold=True)

    # ═══ 22. セクション仕切り：ハンズオン ═══
    s = add_slide(prs)
    make_section(s, 4, "ハンズオン実践\n〜 手を動かしてみよう 〜", "70:00 - 100:00",
                c1=L_C1, c2=L_C2)

    # ═══ 23. ハンズオン ワーク内容 ═══
    s = add_slide(prs)
    make_numbered_slide(s, "✋ ハンズオン — 3つのワーク", [
        ("1", "プロフィール文を3パターン生成", "自分の自己紹介をGeminiに書いてもらいましょう。3パターン出してもらって、一番いいものを選びます"),
        ("2", "「私に合うAI副業は？」相談", "Geminiに「私は〇〇な人です。合うAI副業を教えて」と聞いてみましょう"),
        ("3", "Discordに投稿", "一番気に入った結果をDiscordの#ワーク投稿チャンネルに貼りましょう。仲間の投稿にもリアクション！"),
    ], accent_c1=L_C1, accent_c2=L_C2)

    # ═══ 24. ワーク①のプロンプト例 ═══
    s = add_slide(prs)
    bg_grad(s, DARK1, "162544")
    txt(s, Inches(1), Inches(0.5), Inches(11), Inches(0.7),
        "ワーク① プロフィール文生成のプロンプト例", sz=28, clr=C_GOLD, bold=True)
    card(s, Inches(1.2), Inches(1.5), Inches(10.9), Inches(4.5),
         grad=(DARK2, "2D3748"), radius=0.06, shadow=True,
         border=RGBColor(0x63, 0x66, 0xF1))
    multi_txt(s, Inches(1.8), Inches(1.8), Inches(10), Inches(4),
              [
                  "以下の条件で、私の自己紹介文を3パターン作ってください。",
                  "",
                  "【条件】",
                  "・名前：〇〇",
                  "・年齢：40代",
                  "・趣味：〇〇",
                  "・AI副業に興味を持ったきっかけ：〇〇",
                  "・文体：親しみやすく、温かい感じで",
                  "・文字数：各200文字程度",
              ], sz=16, clr=C_WHITE, align=PP_ALIGN.LEFT)
    txt(s, Inches(1.2), Inches(6.3), Inches(10.9), Inches(0.4),
        "📌 「条件」を具体的に書くほど、AIの回答が正確になります", sz=14, clr=C_GOLD)
    footer(s, L_C1, L_C2)

    # ═══ 25. ワーク②のプロンプト例 ═══
    s = add_slide(prs)
    bg_grad(s, DARK1, "162544")
    txt(s, Inches(1), Inches(0.5), Inches(11), Inches(0.7),
        "ワーク② AI副業相談のプロンプト例", sz=28, clr=C_GOLD, bold=True)
    card(s, Inches(1.2), Inches(1.5), Inches(10.9), Inches(4.5),
         grad=(DARK2, "2D3748"), radius=0.06, shadow=True,
         border=RGBColor(0x63, 0x66, 0xF1))
    multi_txt(s, Inches(1.8), Inches(1.8), Inches(10), Inches(4),
              [
                  "私に合うAI副業を3つ提案してください。",
                  "",
                  "【私の情報】",
                  "・年齢/性別：〇〇",
                  "・使える時間：1日〇〇分",
                  "・興味のあること：〇〇",
                  "・PCスキル：初心者 / 普通 / 得意",
                  "・目標月収：〇〇万円",
                  "",
                  "それぞれについて、理由とおすすめ度を教えてください。",
              ], sz=16, clr=C_WHITE, align=PP_ALIGN.LEFT)
    footer(s, L_C1, L_C2)

    # ═══ 26. スマホ版Geminiの設定 ═══
    s = add_slide(prs)
    make_step_flow(s, "📱 スマホ版Geminiの設定", [
        ("1", "アプリを\nダウンロード", "App Store（iPhone）\nGoogle Play（Android）\nで「Gemini」検索"),
        ("2", "Googleアカウントで\nログイン", "Gmailと同じアカウントで\nそのままログイン\n新規登録は不要"),
        ("3", "音声入力を\n試す", "マイクボタンを押して\n話しかけるだけ\n移動中もAIと会話OK"),
    ], accent_c1=L_C1, accent_c2=L_C2)

    # ═══ 27. 今週の課題 ═══
    s = add_slide(prs)
    make_numbered_slide(s, "📝 今週の課題", [
        ("1", "Geminiに10回以上話しかける", "何でもOK！料理のレシピ、旅行の計画、悩み相談…\nAIと仲良くなることが目的です"),
        ("2", "面白かった回答をDiscordに投稿", "#今週の課題 チャンネルに\nスクショまたはコピペで共有しましょう"),
        ("3", "仲間の投稿に「いいね」リアクション", "一人じゃない。仲間の頑張りを見て、自分も頑張れる\nリアクションは最高のモチベーション"),
    ], accent_c1=L_C1, accent_c2=L_C2)

    # ═══ 28. 収益源ダッシュボード ═══
    s = add_slide(prs)
    make_table_slide(s, "📊 収益源ダッシュボード — 第1回時点",
        ["収益源", "ステータス", "開始予定"],
        [
            ["① YouTube動画", "⬜ まだ", "第2〜3回で開始"],
            ["② AI音楽", "⬜ まだ", "第4〜5回で開始"],
            ["③ Kindle出版", "⬜ まだ", "第6回で開始"],
            ["④ AIブログ", "⬜ まだ", "第7回で開始"],
            ["⑤ 画像販売", "⬜ まだ", "第8回で開始"],
            ["⑥ ショート動画", "⬜ まだ", "第9回で開始"],
            ["⑦ スキル販売", "⬜ まだ", "第10回で開始"],
        ],
        accent_c1=L_C1, accent_c2=L_C2, highlight_last=False,
        note="📌 3ヶ月後、ここが全部✅になります。楽しみですね！")

    # ═══ 29. 来週の予告 ═══
    s = add_slide(prs)
    make_emphasis(s,
        "🎬 来週の予告\n「AI動画① 台本も画像もAIにおまかせ」",
        "来週から一気にYouTubeチャンネルを作ります！\n台本も画像も全部AIがやってくれます\nチャンネル開設の準備をしておいてくださいね",
        gold=True)

    # ═══ 30. エンディング ═══
    s = add_slide(prs)
    make_emphasis(s,
        "お疲れさまでした！\n今日からあなたはAIの友達です 🤝",
        "📌 Discordに自己紹介を投稿してくださいね\n📌 今週の課題：Geminiに10回話しかける\n📌 来週月曜19:00にお会いしましょう！")


# ═══════════════════════════════════════
# メイン実行
# ═══════════════════════════════════════
if __name__ == "__main__":
    prs = create_prs()
    print("第1回「はじめの一歩 — AIと友達になる日」を生成中...")
    build_session01(prs)

    out = os.path.join(SCRIPT_DIR, "講義01_はじめの一歩_v2.pptx")
    prs.save(out)
    print(f"\n完了！ スライド総数: {len(prs.slides)}")
    print(f"保存先: {out}")
