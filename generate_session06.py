# -*- coding: utf-8 -*-
"""第6回「文章生成で稼ぐ〜note販売 ＋ Kindle出版〜」単独生成スクリプト"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "Google_Slide_generator"))
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from design_v2 import *
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
C1, C2 = "059669", "10B981"   # Month2グリーン（既存と同系統）

def build(prs):
    # ─── タイトル ───
    s = add_slide(prs)
    make_title_slide(s, "文章生成で稼ぐ\nnote販売 ＋ Kindle出版",
                     "第6回｜2026年5月25日（月）20:00〜22:00", "らくらくAI副業キャンパス")

    # ─── ゴール ───
    s = add_slide(prs)
    make_cards_slide(s, "🎯 本日のゴール", [
        ("📝", "有料noteを\n1本公開する", "あなたの知識・体験を\n記事にして今日から\nすぐ販売開始！"),
        ("📚", "Kindle書籍の\n原稿を完成させる", "Geminiで1万字を\n15分で生成\n→Amazonで永久販売"),
        ("♻️", "一粒二度おいしい\n変換術を覚える", "台本→note→Kindle\n同じ素材で3回稼ぐ\n仕組みを作ろう"),
    ], accent_c1=C1, accent_c2=C2)

    # ─── 振り返り ───
    s = add_slide(prs)
    make_dark_summary(s, "前回の振り返り", [
        "✅ AI音楽をSpotify / YouTube Musicで世界配信した",
        "✅ 2つの収益源（YouTube＋音楽）が稼働中",
        "✅ 量産ルーティンを回し始めた",
    ], sub="今日から3つ目の収益源！「書く力」をAIで爆発的に強化します", c1=C1, c2=C2)

    # ─── 課題チェック ───
    s = add_slide(prs)
    make_cards_slide(s, "課題チェック｜楽曲できましたか？", [
        ("🎵", "15曲以上\n生成できた？", "お気に入りの曲を\nDiscordで紹介して\nもらいます！"),
        ("📡", "配信サービスに\n登録できた？", "配信状況を\n一緒に確認します"),
        ("📺", "YouTube動画も\n継続できた？", "動画は積み上げれば\n積み上げるほど\n財産になります"),
    ], accent_c1=C1, accent_c2=C2)

    # ══════════════════
    # Section 1：文章で稼ぐ全体像
    # ══════════════════
    s = add_slide(prs)
    make_section(s, 1, "文章生成で稼ぐ全体像\n〜 AIがライターになる時代 〜", "20:00 - 30:00", c1=C1, c2=C2)

    s = add_slide(prs)
    make_emphasis(s, "「文章が苦手」でも大丈夫。\nAIがプロのライターになってくれます",
        "あなたがやることは「テーマを決める」だけ。\n文章を考えたり、推敲したり、そんな作業はすべてAIに任せましょう。\n\n大切なのは「あなたがどんな経験・知識・興味を持っているか」。\nそれがそのままコンテンツになります。", gold=True)

    s = add_slide(prs)
    make_comparison(s, "note販売 vs Kindle出版｜どう違うの？",
        "📝 note販売",
        [
            "記事1本から今日すぐ販売できる",
            "100〜1,000円で手軽に購入してもらいやすい",
            "フォロワーと関係を作りながら販売",
            "「お試し無料 → 続きは有料」戦略が使える",
            "まずnoteで反応を見てからKindleへ展開",
        ],
        "📚 Kindle出版",
        [
            "印税70%・在庫ゼロ・永久販売",
            "1冊250〜500円で安定したロングテール収益",
            "Amazonというブランドの信頼感",
            "「著者」という肩書きで信頼度UP",
            "noteの記事10本分 = Kindle1冊に変換できる",
        ],
        l_c1="047857", l_c2="059669", r_c1="1D4ED8", r_c2="3B82F6")

    s = add_slide(prs)
    make_emphasis(s, "📌 一粒三度おいしい戦略\nYouTube台本 → note記事 → Kindle書籍",
        "Geminiで作ったYouTube台本をそのまま再利用！\n\n台本1本 → noteの有料記事（300円）\n台本10本 → Kindle書籍1冊（500円）\n\n同じ素材から3つの収益源を作れます。", gold=True)

    # ══════════════════
    # Section 2：note販売
    # ══════════════════
    s = add_slide(prs)
    make_section(s, 2, "note有料販売\n〜 今日から売れる仕組みを作ろう 〜", "30:00 - 55:00", c1=C1, c2=C2)

    s = add_slide(prs)
    make_cards_slide(s, "noteで稼ぐ3つのパターン", [
        ("📄", "有料単体記事", "1記事100〜500円\n「〇〇の完全ガイド」\n「〇〇の裏ワザ」"),
        ("📂", "有料マガジン", "月額300〜1,000円\n定期購読モデルで\n安定収入を作る"),
        ("🎁", "無料→有料の\n導線戦略", "最初の3割は無料\n「続きは有料で」\nコンバージョンUP"),
    ], accent_c1=C1, accent_c2=C2)

    s = add_slide(prs)
    make_numbered_slide(s, "売れるnoteの「型」｜4パターン", [
        ("1", "体験談型", "「私が〇〇をやってみた全記録」「〇〇で変わった私の話」\n→ 実体験の正直な記録が一番読まれる。あなただけの話を書く"),
        ("2", "まとめ型", "「〇〇を始めるために必要な5つのこと」「〇〇完全ガイド」\n→ 読者の「調べる手間」を省いてあげる記事は価値が高い"),
        ("3", "テンプレート型", "「〇〇で使えるプロンプト30選」「私が使っているテンプレート集」\n→ すぐ使えるものは価格に関わらず売れやすい"),
        ("4", "Q\u0026A型", "「〇〇について聞かれたことに全部答えます」\n→ よくある悩みに答える記事は検索で見つけてもらいやすい"),
    ], accent_c1=C1, accent_c2=C2)

    # note生成プロンプト
    s = add_slide(prs)
    bg_grad(s, DARK1, "052E16")
    txt(s, Inches(1), Inches(0.5), Inches(11), Inches(0.6),
        "note有料記事 生成プロンプト例（Geminiにコピペ）", sz=24, clr=C_GOLD, bold=True)
    card(s, Inches(1.2), Inches(1.3), Inches(10.9), Inches(5.2),
         grad=(DARK2, "064E3B"), radius=0.06, shadow=True, border=RGBColor(0x05, 0x96, 0x69))
    multi_txt(s, Inches(1.8), Inches(1.6), Inches(10), Inches(4.7), [
        "以下の条件でnote有料記事の本文を書いてください。",
        "",
        "【テーマ】〇〇（例：40代からのAI副業の始め方）",
        "【ターゲット読者】〇〇（例：副業未経験の40〜50代女性）",
        "【記事の型】体験談型 / まとめ型 / テンプレート型 / Q&A型",
        "【文字数】2,000〜3,000字",
        "【構成】",
        "  ① つかみ（読者の悩みに共感する冒頭）",
        "  ② 本編（3〜5つのポイント）",
        "  ③ まとめ＆行動を促す一言",
        "【口調】優しく、話しかけるような語り口",
    ], sz=14, clr=C_WHITE, align=PP_ALIGN.LEFT)
    txt(s, Inches(1.2), Inches(6.7), Inches(10.9), Inches(0.35),
        "📌 これをコピペして「〇〇」を変えるだけで記事完成！最後に価格を設定して公開しよう", sz=12, clr=C_GOLD)
    footer(s, C1, C2)

    s = add_slide(prs)
    make_step_flow(s, "note有料記事の公開手順", [
        ("1", "note.comに\nアカウント作成", "Googleアカウントで\n登録\n（無料）"),
        ("2", "Geminiで\n記事を生成", "プロンプトテンプレートで\n2,000字を\n一気に生成"),
        ("3", "有料設定を\nする", "「有料エリア」で\n後半に有料ラインを\n設定（100〜500円）"),
        ("4", "公開！", "Discordで\n「公開しました！」\nと報告しよう"),
    ], accent_c1=C1, accent_c2=C2)

    s = add_slide(prs)
    make_cards_slide(s, "【解説】noteで売れるための3つのコツ", [
        ("🎯", "タイトルで\n勝負が決まる", "「〇〇の完全ガイド」\n「知らないと損な〇〇」\nGeminiにタイトル案を10個出してもらおう"),
        ("🆓", "最初の3割を\n無料で見せる", "「続きが読みたい！」\nと思わせる展開を\n無料部分に入れよう"),
        ("🔗", "SNSやYouTubeに\nリンクを貼る", "Discordや動画の\n概要欄からnoteへ\n誘導しよう"),
    ], accent_c1=C1, accent_c2=C2)

    # ══════════════════
    # Section 3：Kindle出版
    # ══════════════════
    s = add_slide(prs)
    make_section(s, 3, "Kindle出版\n〜 AIに本を書かせてAmazonで永久販売 〜", "55:00 - 80:00", c1=C1, c2=C2)

    s = add_slide(prs)
    make_cards_slide(s, "Kindle出版の3大メリット", [
        ("💰", "印税70%", "一般出版は10%\nKindleなら70%\n圧倒的な還元率"),
        ("📦", "在庫ゼロ\n初期投資ゼロ", "電子書籍だから\n在庫リスクなし\n費用は0円"),
        ("♾️", "一度出版したら\n永久販売", "Amazonが売り続けて\nくれる完全な\nデジタル資産"),
    ], accent_c1=C1, accent_c2=C2)

    s = add_slide(prs)
    make_emphasis(s, "📌 noteの記事10本 ＝ Kindle1冊\n「書いたもの」を2度稼がせる",
        "すでにnoteで書いた記事を集めて、少し加筆するだけでKindle本が完成します。\n\n一度の努力から、noteでの販売収入 ＋ Kindleの印税収入\nという2つの流れを作れます。", gold=True)

    s = add_slide(prs)
    make_step_flow(s, "Geminiで書籍を生成する5ステップ", [
        ("1", "章立てを\n生成", "「〇〇の本の\n章立てを5章で\n作って」"),
        ("2", "各章の\n本文を生成", "「第1章を\n2,000字で\n書いて」"),
        ("3", "校正・\nリライト", "「読みやすく\n校正して。\n丁寧な語り口で」"),
        ("4", "タイトル＆\n紹介文", "「売れるタイトルを\n10案出して」\n「紹介文を書いて」"),
        ("5", "表紙を\nAIで生成", "画像AIで\nプロ品質の\n表紙デザイン"),
    ], accent_c1=C1, accent_c2=C2)

    # Kindleプロンプト
    s = add_slide(prs)
    bg_grad(s, DARK1, "052E16")
    txt(s, Inches(1), Inches(0.5), Inches(11), Inches(0.6),
        "Kindle書籍 生成プロンプト例", sz=24, clr=C_GOLD, bold=True)
    card(s, Inches(1.2), Inches(1.3), Inches(10.9), Inches(4.8),
         grad=(DARK2, "064E3B"), radius=0.06, shadow=True, border=RGBColor(0x05, 0x96, 0x69))
    multi_txt(s, Inches(1.8), Inches(1.6), Inches(10), Inches(4.3), [
        "【STEP 1：章立て】",
        "「〇〇をテーマにした入門書の章立てを5章構成で作って。",
        "  読者は〇〇（例：AI初心者の40〜50代女性）です。」",
        "",
        "【STEP 2：本文生成（各章に繰り返す）】",
        "「第〇章の本文を2,000字で書いて。",
        "  具体例や体験談を入れて、優しい語り口で書いてください。」",
        "",
        "【STEP 3：タイトル】",
        "「この本のKindleで売れそうなタイトルを10案出して。",
        "  サブタイトルも付けて。読者が思わず買いたくなるもの。」",
    ], sz=13, clr=C_WHITE, align=PP_ALIGN.LEFT)
    txt(s, Inches(1.2), Inches(6.3), Inches(10.9), Inches(0.5),
        "📌 1万字の原稿が15分で完成します。あとはKDP（Kindle Direct Publishing）にアップするだけ！", sz=12, clr=C_GOLD)
    footer(s, C1, C2)

    s = add_slide(prs)
    make_step_flow(s, "KDP出版の手順", [
        ("1", "KDPに\n登録", "kdp.amazon.com\nにアカウント作成\n（無料）"),
        ("2", "原稿＆表紙を\nアップロード", "Word形式の原稿と\nAI生成した表紙を\nアップ"),
        ("3", "価格設定", "250〜500円が\n売れやすい\n価格帯です"),
        ("4", "出版！", "Amazonに\n自分の本が\n並びます📚"),
    ], accent_c1=C1, accent_c2=C2)

    s = add_slide(prs)
    make_cards_slide(s, "【解説】売れるKindle本の3つのコツ", [
        ("📖", "テーマは\n「細く深く」", "「AI副業の本」より\n「40代女性が始める\nAI副業の本」の方が\nターゲットに刺さる"),
        ("⭐", "最初の10ページ\nが命", "Kindleは「試し読み」\nができる。冒頭10ページで\n「読み続けたい！」\nと思わせる"),
        ("🔄", "noteで\n反応を見てから", "人気の記事テーマを\nKindleにする\n「反応を見てから\n書く」が最強戦略"),
    ], accent_c1=C1, accent_c2=C2)

    # ══════════════════
    # Section 4：ハンズオン
    # ══════════════════
    s = add_slide(prs)
    make_section(s, 4, "ハンズオン実践\n〜 note公開 ＋ Kindle原稿の着手 〜", "80:00 - 110:00", c1=C1, c2=C2)

    s = add_slide(prs)
    make_numbered_slide(s, "✋ ハンズオン — 今日のワーク", [
        ("1", "有料note記事を1本公開する",
         "プロンプトテンプレートで記事生成 → 有料設定 → 公開！今日が販売デビューです"),
        ("2", "Kindle書籍の章立てを生成する",
         "Geminiに「章立てを作って」と指示。まずは設計図を完成させましょう"),
        ("3", "第1章の本文を生成する",
         "「第1章を2,000字で書いて」と指示するだけ。全体の20%が今日中に完成します"),
    ], accent_c1=C1, accent_c2=C2)

    s = add_slide(prs)
    make_emphasis(s, "「書けない」ではなく「Geminiに書かせる」",
        "あなたがやることは「テーマを伝える」「出てきた文章を読んで確認する」だけ。\n\n「もう少し優しい表現にして」「この部分をもっと詳しくして」と\n会話しながら整えていくのが正解です。\n\nAIはあなたのゴーストライターです。", gold=True)

    # ─── Closing ───
    s = add_slide(prs)
    make_numbered_slide(s, "📝 今週の課題", [
        ("1", "note有料記事を3本公開する",
         "1本公開できたら、テーマを変えてどんどん量産しましょう"),
        ("2", "Kindle書籍の原稿を全章完成させる（1万字以上）",
         "Geminiで各章を一気に生成。表紙もAI画像で作成しましょう"),
        ("3", "KDPに登録＆出版する",
         "Amazonに自分の本を出版！「著者」デビューの瞬間です"),
        ("4", "YouTube・音楽は引き続き継続",
         "全収益源を止めずに回し続けましょう"),
    ], accent_c1=C1, accent_c2=C2)

    s = add_slide(prs)
    make_table_slide(s, "📊 収益源ダッシュボード — 第6回時点",
        ["収益源", "ステータス", "メモ"],
        [
            ["① YouTube動画", "✅ 稼働中", "動画公開継続中"],
            ["② AI音楽", "✅ 稼働中", "世界配信中"],
            ["③ note販売", "✅ 稼働中！", "今日から販売開始🎉"],
            ["④ Kindle出版", "🟡 準備中", "今週中に出版！"],
            ["⑤ AIブログ", "⬜ まだ", "第7回で開始"],
            ["⑥ 画像販売", "⬜ まだ", "第8回で開始"],
            ["⑦ スキル販売", "⬜ まだ", "第10回で開始"],
        ],
        accent_c1=C1, accent_c2=C2, highlight_last=False,
        note="📌 今日からnoteの販売がスタート！来週には本がAmazonに並びます")

    s = add_slide(prs)
    make_emphasis(s, "✍️ 来週の予告\n「AIブログで寝てる間にアフィリ収入」",
        "来週はAIブログを開設して、寝ている間に稼ぐアフィリエイトの仕組みを作ります。\n書いたnoteの記事を、そのままブログにも転用できます！", gold=True)

    s = add_slide(prs)
    make_emphasis(s, "お疲れさまでした！\nあなたは今日から「著者」であり「販売者」です 📚",
        "📌 課題：note記事3本公開＋Kindle出版\n📌 note公開URLをDiscordにシェアして、仲間に読んでもらおう\n📌 来週月曜20:00にお会いしましょう！")


if __name__ == "__main__":
    prs = create_prs()
    print("第6回を生成中...")
    build(prs)
    out = os.path.join(SCRIPT_DIR, "講義06_文章生成で稼ぐ_v1.pptx")
    prs.save(out)
    print(f"完了！ スライド{len(prs.slides)}枚 → {out}")
