# -*- coding: utf-8 -*-
"""第4〜12回 一括パワポ生成"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "Google_Slide_generator"))
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from design_v2 import *
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
L_C1, L_C2 = "6366F1", "8B5CF6"
M2_C1, M2_C2 = "059669", "10B981"  # Month2 = グリーン系
M3_C1, M3_C2 = "D97706", "F59E0B"  # Month3 = ゴールド系

def dashboard(prs, title, rows, note, c1, c2):
    s = add_slide(prs)
    make_table_slide(s, title, ["収益源","ステータス","メモ"], rows, accent_c1=c1, accent_c2=c2, highlight_last=False, note=note)

def build_s04(prs):
    """第4回：AI音楽① 30秒で作曲する魔法"""
    c1, c2 = L_C1, L_C2
    s = add_slide(prs); make_title_slide(s, "AI音楽①\n30秒で作曲する魔法", "第4回｜2026年5月11日（月）19:00〜21:00", "らくらくAI副業キャンパス")
    s = add_slide(prs); make_cards_slide(s, "🎯 本日のゴール", [("🎵","Suno AIで\n楽曲を作れる","テキスト入力だけで\nプロ品質の曲を生成"),("🎧","狙い目ジャンルを\n理解する","稼ぎやすいジャンル\nBEST5を学ぶ"),("💰","音楽ビジネスの\n全体像を把握","印税の仕組みを\n理解する")], accent_c1=c1, accent_c2=c2)
    s = add_slide(prs); make_dark_summary(s, "前回の振り返り", ["✅ YouTube動画を完成＆公開した","✅ AI音声ナレーション＋AI動画編集をマスター","✅ 量産テンプレートで効率化"], sub="YouTube順調ですか？今日から第2の収益源です", c1=c1, c2=c2)
    s = add_slide(prs); make_section(s, 1, "AI音楽ビジネスの全体像\n〜 印税＝再生されるたびに自動入金 〜", "20:00 - 35:00", c1=c1, c2=c2)
    s = add_slide(prs); make_cards_slide(s, "AI音楽ビジネスとは？", [("🎵","Suno AI","テキスト入力だけで\nプロ品質の楽曲を\n30秒で自動生成"),("🌍","世界配信","Spotify/Apple Music等\n100以上のプラットフォームに\n一括配信"),("💰","印税収入","再生されるたびに\n自動で印税が発生\n= デジタル印税マシン")], accent_c1=c1, accent_c2=c2)
    s = add_slide(prs); make_table_slide(s, "AI音楽の収益事例", ["プラットフォーム","再生数/月","推定月収","備考"], [["YouTube Music","50万回","15〜20万円","BGMチャンネル"],["Spotify","30万回","10〜15万円","プレイリスト掲載"],["Apple Music","10万回","5〜8万円","ジャンル特化"],["合計","90万回","27.5万円","1チャンネルの実績"]], accent_c1=c1, accent_c2=c2, note="📌 音楽 × YouTube = 二重の収益源")
    s = add_slide(prs); make_section(s, 2, "Suno AI完全マスター\n〜 アカウント作成から実演まで 〜", "35:00 - 55:00", c1=c1, c2=c2)
    s = add_slide(prs); make_step_flow(s, "Suno AI 操作手順", [("1","アカウント作成","suno.com に\nアクセス\nGoogleログイン"),("2","基本操作","テーマを入力\nジャンルを選択\n生成ボタンを押す"),("3","スタイル指定","歌詞あり/インスト\nテンポ・雰囲気\nを指定"),("4","生成＆確認","30秒で完成！\nプレビュー再生\nダウンロード")], accent_c1=c1, accent_c2=c2)
    s = add_slide(prs); make_numbered_slide(s, "狙い目ジャンル BEST 5", [("1","Lo-Fi / チルホップ","作業用BGMとして安定需要。プレイリストに入りやすい"),("2","アンビエント / 瞑想","ヨガ・睡眠系で長時間再生。リピート率が高い"),("3","子守唄 / キッズ","育児層の安定ニーズ。競合が少ない穴場"),("4","J-POP カバー","日本語市場で圧倒的な検索ボリューム"),("5","ゲーム風BGM","ゲーム実況者の需要。サブスク安定収入")], accent_c1=c1, accent_c2=c2)
    s = add_slide(prs); make_emphasis(s, "【実演タイム】\n今から5曲をその場で作ります", "テキスト入力 → 30秒 → プロ品質の楽曲が完成\nみなさんの目の前でリアルタイム生成", gold=True)
    s = add_slide(prs); make_section(s, 3, "ハンズオン実践\n〜 自分の曲を作ろう 〜", "55:00 - 100:00", c1=c1, c2=c2)
    s = add_slide(prs); make_numbered_slide(s, "✋ ハンズオン", [("1","Suno AIで5曲を生成する","色々なジャンル・スタイルを試してみましょう"),("2","ベスト1曲をDiscordに投稿","仲間に聴いてもらって感想をもらいましょう")], accent_c1=c1, accent_c2=c2)
    s = add_slide(prs); make_numbered_slide(s, "📝 今週の課題", [("1","楽曲を合計15曲生成","量を作ってお気に入りを見つける。色々なジャンルを試す"),("2","ベスト3曲をDiscordに投稿","仲間からフィードバックをもらいましょう"),("3","YouTube動画は継続","動画もコツコツ公開し続けましょう")], accent_c1=c1, accent_c2=c2)
    dashboard(prs, "📊 収益源ダッシュボード — 第4回", [["① YouTube","✅ 稼働中","動画公開中"],["② AI音楽","🟡 準備中","楽曲生成中"],["③ Kindle","⬜ まだ","第6回"],["④ ブログ","⬜ まだ","第7回"],["⑤ 画像販売","⬜ まだ","第8回"],["⑥ ショート","⬜ まだ","第9回"],["⑦ スキル","⬜ まだ","第10回"]], "📌 来週はこの曲を世界100か国に配信！永久に印税が入ります", c1, c2)
    s = add_slide(prs); make_emphasis(s, "お疲れさまでした！\n来週は世界100か国に配信します 🌍", "📌 課題：15曲生成＋ベスト3をDiscord投稿\n📌 YouTube動画も継続\n📌 来週月曜19:00にお会いしましょう！")

def build_s05(prs):
    """第5回：AI音楽② 世界100か国に配信して印税生活"""
    c1, c2 = M2_C1, M2_C2
    s = add_slide(prs); make_title_slide(s, "AI音楽②\n世界100か国に配信して印税生活", "第5回｜2026年5月18日（月）19:00〜21:00", "らくらくAI副業キャンパス")
    s = add_slide(prs); make_cards_slide(s, "🎯 本日のゴール", [("📡","配信サービスに\n登録","TuneCore等で\nアーティスト登録完了"),("🎬","YouTube Musicに\n公開","音楽チャンネルを\n開設＆動画公開"),("💰","印税の仕組みを\n完成させる","配信したら永久に\n印税が入る状態")], accent_c1=c1, accent_c2=c2)
    s = add_slide(prs); make_section(s, 1, "配信サービスへの登録\n〜 世界100か国に届ける 〜", "20:00 - 45:00", c1=c1, c2=c2)
    s = add_slide(prs); make_step_flow(s, "音楽配信の手順", [("1","配信サービスに\n登録","TuneCore等に\nアカウント作成"),("2","アーティスト名を\n決める","Geminiに\n名前を提案\nしてもらう"),("3","ジャケ画像を\nAIで作成","Geminiや画像AIで\nアルバムアートを\n生成"),("4","楽曲を\nアップロード","メタデータ入力\n→ 配信開始\n→ 世界へ！")], accent_c1=c1, accent_c2=c2)
    s = add_slide(prs); make_section(s, 2, "YouTube Musicチャンネル\n〜 動画＋音楽の二重収益 〜", "45:00 - 60:00", c1=c1, c2=c2)
    s = add_slide(prs); make_cards_slide(s, "YouTube Music運営のポイント", [("🎵","音楽動画の作り方","ジャケ画像＋楽曲\n→ 動画化ツールで\n簡単に作成"),("📋","プレイリスト","ジャンル別に\nプレイリストを作成\n再生時間UP"),("📈","BGMチャンネル","「作業用BGM」として\n長時間再生を狙う\n再生数が安定")], accent_c1=c1, accent_c2=c2)
    s = add_slide(prs); make_emphasis(s, "📌 印税収入の最大化戦略\n月30曲ペースで積み上げる", "一度配信した曲は永久に働き続ける\n「デジタル印税マシン」の完成", gold=True)
    s = add_slide(prs); make_section(s, 3, "ハンズオン実践", "60:00 - 100:00", c1=c1, c2=c2)
    s = add_slide(prs); make_numbered_slide(s, "✋ ハンズオン", [("1","配信サービスに登録する","画面共有で一緒に進めます"),("2","ベスト3曲をアップロードする","メタデータも一緒に入力"),("3","ジャケ画像をAIで作成する","プロンプトテンプレートを使用"),("4","YouTube Music用に動画1本作成","ジャケ画像＋楽曲→動画化")], accent_c1=c1, accent_c2=c2)
    s = add_slide(prs); make_numbered_slide(s, "📝 今週の課題", [("1","配信登録を完了する","アップロードまで終わらせましょう"),("2","YouTube Musicに音楽動画3本","BGMチャンネルとして運営開始"),("3","YouTube動画・音楽ともに継続","両方の収益源を回し続ける")], accent_c1=c1, accent_c2=c2)
    dashboard(prs, "📊 収益源ダッシュボード — 第5回", [["① YouTube","✅ 稼働中","動画公開中"],["② AI音楽","✅ 稼働中","配信開始！"],["③ Kindle","⬜ まだ","来週！"],["④ ブログ","⬜ まだ","第7回"],["⑤ 画像販売","⬜ まだ","第8回"],["⑥ ショート","⬜ まだ","第9回"],["⑦ スキル","⬜ まだ","第10回"]], "📌 2つの収益源が動き始めました！来週は3つ目です", c1, c2)
    s = add_slide(prs); make_emphasis(s, "お疲れさまでした！\n2つの収益源が稼働中です 🎉", "📌 来週はAIに本を書いてもらいます\n📌 3つ目の収益源です！\n📌 来週月曜19:00にお会いしましょう！")

def build_s06(prs):
    """第6回：AIに本を書かせてAmazonで売る"""
    c1, c2 = M2_C1, M2_C2
    s = add_slide(prs); make_title_slide(s, "AIに本を書かせて\nAmazonで売る", "第6回｜2026年5月25日（月）19:00〜21:00", "らくらくAI副業キャンパス")
    s = add_slide(prs); make_cards_slide(s, "🎯 本日のゴール", [("📚","Kindle書籍の\n原稿を完成","Geminiで1万字を\n15分で生成"),("🎨","表紙を\nAIで作成","プロ品質の表紙\nデザインを生成"),("📤","KDPに\n出版する","Amazonに\n自分の本が並ぶ！")], accent_c1=c1, accent_c2=c2)
    s = add_slide(prs); make_section(s, 1, "Kindle出版で稼ぐ\n〜 印税70%・在庫ゼロ・永久販売 〜", "20:00 - 35:00", c1=c1, c2=c2)
    s = add_slide(prs); make_cards_slide(s, "Kindle出版のメリット", [("💰","印税70%","一般的な出版は10%\nKindleなら70%\n圧倒的な還元率"),("📦","在庫ゼロ","電子書籍だから\n在庫リスクなし\n初期投資もゼロ"),("♾️","永久販売","一度出版したら\nずっとAmazonで\n販売され続ける")], accent_c1=c1, accent_c2=c2)
    s = add_slide(prs); make_emphasis(s, "📌 YouTube台本10本分 ＝ 1冊の本\n一粒で二度おいしい戦略", "すでにGeminiで作った台本を再利用できます！", gold=True)
    s = add_slide(prs); make_section(s, 2, "Geminiで1冊書き上げる\n〜 実演します 〜", "35:00 - 55:00", c1=c1, c2=c2)
    s = add_slide(prs); make_step_flow(s, "Geminiで書籍を生成する5ステップ", [("1","章立て生成","「〇〇の本の\n章立てを作って」"),("2","各章の本文","「第1章の本文を\n2000字で書いて」"),("3","校正","「読みやすく\n校正して」"),("4","タイトル","「売れるタイトルを\n10案出して」"),("5","紹介文","「Amazonの\n紹介文を書いて」")], accent_c1=c1, accent_c2=c2)
    s = add_slide(prs); make_section(s, 3, "表紙デザイン＆出版手順", "55:00 - 70:00", c1=c1, c2=c2)
    s = add_slide(prs); make_step_flow(s, "KDP出版の手順", [("1","表紙をAIで\n作成","画像生成AIで\nプロ品質の\n表紙デザイン"),("2","KDPに登録","kdp.amazon.com\nにアカウント作成"),("3","原稿＆表紙\nアップロード","Word形式で\nアップロード"),("4","価格設定\n→出版！","250〜500円に設定\n→出版ボタン\n→Amazonに掲載！")], accent_c1=c1, accent_c2=c2)
    s = add_slide(prs); make_numbered_slide(s, "✋ ハンズオン", [("1","自分のジャンルで章立てを生成","Geminiにテーマを伝えて章構成を作る"),("2","第1章の本文を生成","プロンプトテンプレートで一気に生成"),("3","表紙1パターンを作成","AI画像生成で表紙をデザイン")], accent_c1=c1, accent_c2=c2)
    s = add_slide(prs); make_numbered_slide(s, "📝 今週の課題", [("1","全章の原稿を完成（1万字以上）","Geminiで各章を一気に生成しましょう"),("2","表紙を3パターン作成","ベストなデザインを選びましょう"),("3","KDPに登録＆出版する","Amazonに自分の本を出版！"),("4","YouTube・音楽は継続","全収益源を回し続けましょう")], accent_c1=c1, accent_c2=c2)
    dashboard(prs, "📊 収益源ダッシュボード — 第6回", [["① YouTube","✅ 稼働中",""],["② AI音楽","✅ 稼働中",""],["③ Kindle","✅ 稼働中","出版完了！"],["④ ブログ","⬜ まだ","来週！"],["⑤ 画像販売","⬜ まだ","第8回"],["⑥ ショート","⬜ まだ","第9回"],["⑦ スキル","⬜ まだ","第10回"]], "📌 3つの収益源が稼働！来週は4つ目です", c1, c2)
    s = add_slide(prs); make_emphasis(s, "お疲れさまでした！\nAmazonに自分の本が並んでますよ 📚", "📌 来週はAIブログ。寝てる間にアフィリ収入\n📌 4つ目の収益源です\n📌 来週月曜19:00にお会いしましょう！")

def build_s07(prs):
    """第7回：AIブログで寝てる間にアフィリ収入"""
    c1, c2 = M2_C1, M2_C2
    s = add_slide(prs); make_title_slide(s, "AIブログで\n寝てる間にアフィリ収入", "第7回｜2026年6月1日（月）19:00〜21:00", "らくらくAI副業キャンパス")
    s = add_slide(prs); make_cards_slide(s, "🎯 本日のゴール", [("📝","ブログを\n開設する","note or WordPress\nどちらかで開設"),("✍️","記事3本を\n公開する","Geminiで\nSEO記事を生成"),("💰","アフィリエイトを\n設定する","広告リンクを\n記事に挿入")], accent_c1=c1, accent_c2=c2)
    s = add_slide(prs); make_section(s, 1, "AIブログで稼ぐ仕組み\n〜 アフィリエイトとは 〜", "20:00 - 35:00", c1=c1, c2=c2)
    s = add_slide(prs); make_cards_slide(s, "ブログ収益の仕組み", [("📝","記事を書く","Geminiで\nSEO最適化された\n記事を自動生成"),("🔗","広告を貼る","ASP（A8.net等）\nの広告リンクを\n記事に挿入"),("💰","読者が購入","記事を読んだ人が\n商品を購入すると\n報酬が入る")], accent_c1=c1, accent_c2=c2)
    s = add_slide(prs); make_emphasis(s, "📌 YouTube台本 → ブログ記事に変換\nもう一粒おいしい戦略", "Geminiに「この台本をブログ記事に変換して」と指示するだけ", gold=True)
    s = add_slide(prs); make_section(s, 2, "GeminiでSEO記事を書く\n〜 検索で上位表示される技術 〜", "35:00 - 55:00", c1=c1, c2=c2)
    s = add_slide(prs); make_step_flow(s, "SEO記事作成の流れ", [("1","キーワード\n選定","Geminiに\n「検索されやすい\nキーワードを提案」"),("2","記事構成\n自動生成","「この KW で\n記事の構成を\n作って」"),("3","本文を\n一気に生成","「各見出しの\n本文を書いて」\n3,000字が10分"),("4","公開＆\nリンク挿入","記事を公開し\nアフィリリンクを\n挿入")], accent_c1=c1, accent_c2=c2)
    s = add_slide(prs); make_section(s, 3, "アフィリエイト設定", "55:00 - 70:00", c1=c1, c2=c2)
    s = add_slide(prs); make_step_flow(s, "アフィリエイト設定 3ステップ", [("1","ASPに登録","A8.net等に\nアカウント作成\n無料・審査なし"),("2","広告を選ぶ","自分の記事に\n合う広告を選択\nリンクを取得"),("3","記事に挿入","記事内に\n自然な形で\n広告リンクを配置")], accent_c1=c1, accent_c2=c2)
    s = add_slide(prs); make_numbered_slide(s, "✋ ハンズオン", [("1","ブログを開設する（note or WordPress）","画面共有で一緒に進めます"),("2","記事1本をGeminiで生成＆公開","テンプレートを使って記事を作成"),("3","アフィリリンクを挿入","A8.net等の広告を記事に挿入")], accent_c1=c1, accent_c2=c2)
    s = add_slide(prs); make_numbered_slide(s, "📝 今週の課題", [("1","ブログ記事3本を公開","SEOテンプレートで量産"),("2","YouTube台本1本をブログに変換","一粒二度おいしい戦略を実践"),("3","全収益源の継続","YouTube・音楽・Kindle・ブログ")], accent_c1=c1, accent_c2=c2)
    dashboard(prs, "📊 収益源ダッシュボード — 第7回", [["① YouTube","✅",""],["② AI音楽","✅",""],["③ Kindle","✅",""],["④ ブログ","✅ 稼働中","記事公開開始！"],["⑤ 画像販売","⬜ まだ","来週！"],["⑥ ショート","⬜ まだ","第9回"],["⑦ スキル","⬜ まだ","第10回"]], "📌 4つの収益源が稼働中！", c1, c2)
    s = add_slide(prs); make_emphasis(s, "お疲れさまでした！\n来週はAIで絵を描いて売ります 🎨", "📌 LINEスタンプやグッズ販売。5つ目の収益源です\n📌 来週月曜19:00にお会いしましょう！")

def build_s08(prs):
    """第8回：AIに描かせて売る — スタンプ＆グッズ販売"""
    c1, c2 = M2_C1, M2_C2
    s = add_slide(prs); make_title_slide(s, "AIに描かせて売る\nスタンプ＆グッズ販売", "第8回｜2026年6月8日（月）19:00〜21:00", "らくらくAI副業キャンパス")
    s = add_slide(prs); make_cards_slide(s, "🎯 本日のゴール", [("🎨","AI画像で稼ぐ\nルートを理解","LINEスタンプ\nストックフォト\nグッズ販売"),("✏️","作品を\n作成する","好きなルート1つで\n実際に制作"),("📤","販売を\n開始する","各プラットフォームに\n登録＆出品")], accent_c1=c1, accent_c2=c2)
    s = add_slide(prs); make_section(s, 1, "AI画像で稼ぐ4つのルート", "20:00 - 35:00", c1=c1, c2=c2)
    s = add_slide(prs); make_cards_slide(s, "AI画像で稼ぐ4つのルート", [("😀","LINEスタンプ","月1〜3万円\nキャラ40個を\n一気に生成"),("📸","ストックフォト","Adobe Stock/PIXTA\n素材画像を投稿\nダウンロード報酬"),("👕","グッズ販売","SUZURI連携\n画像→自動グッズ化\n在庫ゼロ販売"),("🖼️","制作代行","SNSアイコン等\n1件1,000〜5,000円\n即金性が高い")], accent_c1=c1, accent_c2=c2)
    s = add_slide(prs); make_section(s, 2, "LINEスタンプ制作", "35:00 - 50:00", c1=c1, c2=c2)
    s = add_slide(prs); make_step_flow(s, "LINEスタンプ制作の流れ", [("1","キャラを\nAIで作成","Geminiや画像AIで\nオリジナルキャラを\nデザイン"),("2","表情40個を\n一気に生成","プロンプトで\n表情バリエーション\nを一括生成"),("3","背景透過","無料ツールで\n背景を透過\n（remove.bg等）"),("4","LINE Creators\nMarketに申請","画像をアップ\n→ 審査\n→ 販売開始！")], accent_c1=c1, accent_c2=c2)
    s = add_slide(prs); make_section(s, 3, "ストックフォト＆グッズ販売", "50:00 - 70:00", c1=c1, c2=c2)
    s = add_slide(prs); make_cards_slide(s, "ストックフォト＆SUZURI", [("📸","売れる素材画像","風景・ビジネス・\n食べ物などの\nAI生成画像"),("👕","SUZURI連携","画像をアップ\n→自動でTシャツ\nマグカップ等に"),("💰","在庫ゼロ","注文が入ったら\n製造＆発送は\nSUZURIが代行")], accent_c1=c1, accent_c2=c2)
    s = add_slide(prs); make_numbered_slide(s, "✋ ハンズオン（好きなルート1つを選択）", [("A","LINEスタンプ：8種類のスタンプ画像を作成","キャラデザイン→表情バリエーション生成"),("B","ストックフォト：10枚の素材画像を投稿","売れやすいジャンルの画像を生成＆投稿"),("C","SUZURI：グッズ3種を作成","デザイン画像→アップロード→商品化")], accent_c1=c1, accent_c2=c2)
    s = add_slide(prs); make_numbered_slide(s, "📝 今週の課題", [("1","選んだルートで規定数を完成","スタンプ40個 / ストックフォト30枚 / グッズ10種"),("2","全収益源の継続","YouTube・音楽・Kindle・ブログ＋画像販売")], accent_c1=c1, accent_c2=c2)
    dashboard(prs, "📊 収益源ダッシュボード — 第8回", [["① YouTube","✅",""],["② AI音楽","✅",""],["③ Kindle","✅",""],["④ ブログ","✅",""],["⑤ 画像販売","✅ 稼働中","出品開始！"],["⑥ ショート","⬜ まだ","来週！"],["⑦ スキル","⬜ まだ","第10回"]], "📌 5つの収益源が動いてます！来月はさらに増やして全自動化", c1, c2)
    s = add_slide(prs); make_emphasis(s, "Month 2 完了！🎉\n5つの収益源が稼働中です", "📌 来月はさらに増やして全部を自動化します\n📌 来週月曜19:00にお会いしましょう！")

def build_s09(prs):
    """第9回：AIショート動画で一気にバズる"""
    c1, c2 = M3_C1, M3_C2
    s = add_slide(prs); make_title_slide(s, "AIショート動画で\n一気にバズる", "第9回｜2026年6月15日（月）19:00〜21:00", "らくらくAI副業キャンパス")
    s = add_slide(prs); make_cards_slide(s, "🎯 本日のゴール", [("📱","ショート動画を\n作れるようになる","60秒台本＋動画制作\nを完全マスター"),("🚀","3プラットフォームに\n同時投稿","TikTok / Reels\n/ Shorts 全対応"),("🔥","バズるフックを\n学ぶ","一気に万再生を\n狙うテクニック")], accent_c1=c1, accent_c2=c2)
    s = add_slide(prs); make_section(s, 1, "ショート動画で稼ぐ仕組み", "20:00 - 35:00", c1=c1, c2=c2)
    s = add_slide(prs); make_cards_slide(s, "3プラットフォームの収益", [("🎵","TikTok","再生ボーナス\nフォロワー0でも\nバズる可能性"),("📸","Instagram\nReels","ボーナス＋集客\nアフィリエイトへの\n導線として最強"),("🎬","YouTube\nShorts","広告収益＋\n通常動画への導線\n既存チャンネル活用")], accent_c1=c1, accent_c2=c2)
    s = add_slide(prs); make_section(s, 2, "AIでショート動画を量産", "35:00 - 55:00", c1=c1, c2=c2)
    s = add_slide(prs); make_numbered_slide(s, "バズるフック 5パターン", [("1","衝撃の事実","「99%の人が知らない〇〇」→ 好奇心を刺激"),("2","ビフォーアフター","「〇〇する前と後で…」→ 変化に引き込まれる"),("3","ランキング","「〇〇ベスト5」→ 最後まで見たくなる"),("4","あるある","「〇〇な人あるある」→ 共感でシェアされる"),("5","やってみた","「〇〇してみた結果…」→ 結果が気になる")], accent_c1=c1, accent_c2=c2)
    s = add_slide(prs); make_emphasis(s, "📌 1本作れば3か所で稼げる\nTikTok / Reels / Shorts 同時投稿", "ハッシュタグ戦略もGeminiで自動生成", gold=True)
    s = add_slide(prs); make_numbered_slide(s, "✋ ハンズオン", [("1","60秒台本をGeminiで3本生成","バズるフックテンプレートを使用"),("2","1本を動画化する","AI音声＋縦動画編集"),("3","3プラットフォームに投稿","TikTok / Reels / Shorts に同時投稿")], accent_c1=c1, accent_c2=c2)
    s = add_slide(prs); make_numbered_slide(s, "📝 今週の課題", [("1","ショート動画5本を作成＆3プラットフォーム投稿","計15投稿を目指しましょう"),("2","全収益源の継続","6つすべてを回し続ける")], accent_c1=c1, accent_c2=c2)
    dashboard(prs, "📊 収益源ダッシュボード — 第9回", [["① YouTube","✅",""],["② AI音楽","✅",""],["③ Kindle","✅",""],["④ ブログ","✅",""],["⑤ 画像","✅",""],["⑥ ショート","✅ 稼働中","3プラットフォーム！"],["⑦ スキル","⬜ まだ","来週！"]], "📌 6つの収益源！来週で全7つ完成です", c1, c2)
    s = add_slide(prs); make_emphasis(s, "お疲れさまでした！\n来週はAIスキルを商品にして売ります 💼", "📌 即金性が一番高い方法です\n📌 来週月曜19:00にお会いしましょう！")

def build_s10(prs):
    """第10回：あなたのAIスキルを「商品」にして売る"""
    c1, c2 = M3_C1, M3_C2
    s = add_slide(prs); make_title_slide(s, "あなたのAIスキルを\n「商品」にして売る", "第10回｜2026年6月22日（月）19:00〜21:00", "らくらくAI副業キャンパス")
    s = add_slide(prs); make_cards_slide(s, "🎯 本日のゴール", [("🛒","ココナラ等に\n出品する","サービスを作って\n即日出品完了"),("💼","ポートフォリオを\n作成","AIで作品集を\n自動生成"),("💰","即金で稼ぐ\n方法を学ぶ","受注→制作→納品\nの全フローを習得")], accent_c1=c1, accent_c2=c2)
    s = add_slide(prs); make_section(s, 1, "AIスキル販売で稼ぐ", "20:00 - 35:00", c1=c1, c2=c2)
    s = add_slide(prs); make_table_slide(s, "出品できるスキル一覧",["スキル","内容","単価"],[ ["AI動画制作代行","YouTube動画をAIで制作","1本 5,000〜20,000円"],["AI記事作成","ブログ・SEO記事を生成","1本 3,000〜10,000円"],["AI楽曲制作","オリジナル楽曲を生成","1曲 5,000〜15,000円"],["AI画像制作","アイコン・バナー等","1枚 1,000〜5,000円"],["AI書籍代筆","電子書籍の執筆代行","1冊 30,000〜50,000円"]],accent_c1=c1,accent_c2=c2,note="📌 すべて、この3ヶ月で身につけたスキルです")
    s = add_slide(prs); make_section(s, 2, "売れるサービスの作り方", "35:00 - 55:00", c1=c1, c2=c2)
    s = add_slide(prs); make_step_flow(s, "出品→受注→納品の流れ", [("1","サービスを\n作る","タイトル・説明文\nをGeminiで作成\n価格を設定"),("2","ポートフォリオ\nを作る","AIで作品サンプル\nを生成して掲載"),("3","受注＆制作","依頼が来たら\nAIで制作\n（30分〜1時間）"),("4","納品","完成品を納品\nお客様から評価\n→実績が積み上がる")], accent_c1=c1, accent_c2=c2)
    s = add_slide(prs); make_numbered_slide(s, "✋ ハンズオン", [("1","出品する商品を決める","自分が得意＆好きなスキルを選択"),("2","説明文をGeminiで作成","売れるサービス説明文テンプレートを使用"),("3","ポートフォリオ画像をAIで作成","作品サンプルを生成"),("4","出品を完了する","ココナラ等に即日出品！")], accent_c1=c1, accent_c2=c2)
    s = add_slide(prs); make_numbered_slide(s, "📝 今週の課題", [("1","2つ以上のサービスを出品","複数出品で受注チャンスUP"),("2","出品リンクをDiscordに投稿","仲間のサービスにもコメント"),("3","全収益源の継続","7つすべてを回す！")], accent_c1=c1, accent_c2=c2)
    dashboard(prs, "📊 収益源ダッシュボード — 第10回", [["① YouTube","✅",""],["② AI音楽","✅",""],["③ Kindle","✅",""],["④ ブログ","✅",""],["⑤ 画像","✅",""],["⑥ ショート","✅",""],["⑦ スキル","✅ 稼働中","全7つ完成！🎉"]], "📌 全7つの収益源が稼働中！🎉🎉🎉", c1, c2)
    s = add_slide(prs); make_emphasis(s, "🎉 全7つの収益源が稼働中！\n来週は全部を自動で回す仕組みを完成させます", "📌 来週月曜19:00にお会いしましょう！")

def build_s11(prs):
    """第11回：AIで「自動で稼ぐ仕組み」を完成させる"""
    c1, c2 = M3_C1, M3_C2
    s = add_slide(prs); make_title_slide(s, "AIで「自動で稼ぐ仕組み」\nを完成させる", "第11回｜2026年6月29日（月）19:00〜21:00", "らくらくAI副業キャンパス")
    s = add_slide(prs); make_cards_slide(s, "🎯 本日のゴール", [("🔄","クロスメディア\n変換をマスター","1コンテンツを\n5倍活用する技術"),("📋","量産ルーティンを\n完成させる","週3時間で\n全部回す仕組み"),("💰","チャンネル売却を\n理解する","毎月の収入＋\n売却益の二重構造")], accent_c1=c1, accent_c2=c2)
    s = add_slide(prs); make_section(s, 1, "クロスメディア変換テクニック\n〜 同じ労力で5倍稼ぐ 〜", "20:00 - 45:00", c1=c1, c2=c2)
    s = add_slide(prs); make_step_flow(s, "1本のYouTube台本から5展開", [("1","YouTube\n動画","元の台本で\nそのまま動画化"),("2","ブログ\n記事","Geminiで\n「ブログ記事に\n変換して」"),("3","Kindleの\n1章","書籍の1章分\nとして蓄積"),("4","ショート\n動画3本","「60秒に要約して」\n→3本量産"),("5","SNS\n投稿5本","「投稿用に\n5つに分割して」")], accent_c1=c1, accent_c2=c2)
    s = add_slide(prs); make_section(s, 2, "量産ルーティン\n〜 週3時間で全部回す 〜", "45:00 - 60:00", c1=c1, c2=c2)
    s = add_slide(prs); make_table_slide(s, "週3時間で全部回すタイムテーブル",["曜日","作業","時間"],[ ["月曜","ネタ出し（Geminiと相談）","30分"],["火曜","台本一括生成","30分"],["水曜","動画＆音楽の制作一括","60分"],["木曜","投稿＆クロスメディア変換","30分"],["金曜","音楽配信＆ブログ更新","30分"]],accent_c1=c1,accent_c2=c2,note="📌 合計3時間。残りの時間は自由に使えます")
    s = add_slide(prs); make_section(s, 3, "チャンネル売却＆今後の展望", "60:00 - 75:00", c1=c1, c2=c2)
    s = add_slide(prs); make_emphasis(s, "YouTubeチャンネルは「売れる」資産\n月収10万円 → 300〜500万円で売却", "ラッコM&Aで実際に売買されています\n毎月の収入 ＋ いつでも売れる資産", gold=True)
    s = add_slide(prs); make_numbered_slide(s, "✋ ハンズオン", [("1","過去コンテンツ1本をクロスメディア5展開","実際にGeminiで変換を実行"),("2","My量産テンプレートを完成させる","全収益源のプロンプト一式を整理"),("3","週間ルーティン表を作成する","自分の生活に合わせたスケジュール")], accent_c1=c1, accent_c2=c2)
    s = add_slide(prs); make_numbered_slide(s, "📝 今週の課題", [("1","「3ヶ月の成果レポート」を作成","全収益源の実績・学び・成長をまとめる"),("2","来週の発表準備（3〜4分）","何を話すか考えておきましょう"),("3","卒業への意気込みをDiscordに投稿","みんなで最終回を盛り上げましょう")], accent_c1=c1, accent_c2=c2)
    s = add_slide(prs); make_emphasis(s, "来週は最終回 🎓\nみなさんの成長を全員でお祝いしましょう", "📌 成果レポート＋発表準備をお忘れなく\n📌 来週月曜19:00、最後の講義です")

def build_s12(prs):
    """第12回：🎓 卒業 — 3ヶ月前のあなたへ"""
    c1, c2 = M3_C1, M3_C2
    s = add_slide(prs); make_title_slide(s, "🎓 卒業\n3ヶ月前のあなたへ", "第12回（最終回）｜2026年7月6日（月）19:00〜21:00", "らくらくAI副業キャンパス")
    s = add_slide(prs); make_emphasis(s, "3ヶ月前、AIを触ったこともなかったあなた。\n今のあなたを見てください。", "7つの収益源。クロスメディア変換。自動化ルーティン。\nすべて、あなたが手に入れたものです。", gold=True)
    s = add_slide(prs); make_cards_slide(s, "📋 本日の流れ", [("🎤","成果発表","一人ひとりの\n3ヶ月の成果を\n発表＆お祝い"),("🏆","表彰式","5つの賞で\n頑張りを\nたたえ合う"),("🗺️","半年後の\nロードマップ","卒業後の\n目標設定＆\n計画策定")], accent_c1=c1, accent_c2=c2)
    s = add_slide(prs); make_simple_slide(s, "🎤 成果発表のフォーマット", ["❶ 立ち上げた収益源の数","❷ 数字の成果（再生数・売上・楽曲数など）","❸ 一番大変だったこと","❹ 一番嬉しかったこと","","📌 一人3〜4分。講師が全員にコメントします"], accent_c1=c1, accent_c2=c2)
    s = add_slide(prs); make_emphasis(s, "成果発表タイム（前半）", "みなさんの番です。一人ずつ発表していきましょう！", gold=True)
    s = add_slide(prs); make_emphasis(s, "成果発表タイム（後半）", "残りの方の発表です。素晴らしい成果ですね！")
    s = add_slide(prs); make_cards_slide(s, "🏆 表彰式", [("🥇","最多コンテンツ賞","一番多くの\nコンテンツを\n制作した方"),("📈","伸び率No.1賞","最も成長した方\n数字の伸びが\n素晴らしい"),("⭐","ベスト\nポートフォリオ賞","質の高い\n作品集を\n作り上げた方")], accent_c1=c1, accent_c2=c2)
    s = add_slide(prs); make_cards_slide(s, "🏆 表彰式（続き）", [("👑","皆勤賞","全12回の講義に\nすべて参加\nした方"),("💬","ベストコメント賞","Discordで最も\n仲間を励まし\n助けた方")], accent_c1=c1, accent_c2=c2)
    s = add_slide(prs); make_section(s, 1, "半年後の自分へロードマップ", "50:00 - 65:00", c1=c1, c2=c2)
    s = add_slide(prs); make_dark_summary(s, "3ヶ月で手に入れたもの", ["✅ 収益源① YouTube動画（広告収入＋売却益）","✅ 収益源② AI音楽（ストリーミング印税）","✅ 収益源③ Kindle出版（電子書籍の印税）","✅ 収益源④ AIブログ（アフィリエイト収入）","✅ 収益源⑤ AI画像販売（スタンプ・グッズ）","✅ 収益源⑥ ショート動画（TikTok/Reels/Shorts）","✅ 収益源⑦ AIスキル販売（制作代行）"], sub="＋ クロスメディア変換 ＋ 週3時間の自動化ルーティン", c1=c1, c2=c2)
    s = add_slide(prs); make_cards_slide(s, "卒業後のサポート", [("💬","Discord\n無期限利用OK","卒業後もずっと\n仲間と繋がれます"),("📱","最新AIツール\n速報を継続配信","ツールが変わっても\n安心です"),("🎙️","月1ライブQ&A","いつでも質問\nできる場を\n用意しています")], accent_c1=c1, accent_c2=c2)
    s = add_slide(prs); make_section(s, 2, "ワーク：3ヶ月前の自分への手紙", "65:00 - 75:00", c1=c1, c2=c2)
    s = add_slide(prs); make_emphasis(s, "3ヶ月前の不安だった自分に\n何と声をかけますか？", "Discordに投稿してください\n講師が読み上げます", gold=True)
    s = add_slide(prs); make_section(s, 3, "講師からの最終メッセージ", "75:00 - 88:00", c1=c1, c2=c2)
    s = add_slide(prs); make_emphasis(s, "これは「終わり」ではなく\n「始まり」です。", "仕組みが回り続けるから\nスクールが終わっても収益は止まりません")
    s = add_slide(prs)
    bg_grad(s, DARK1, "162544")
    txt(s, Inches(1), Inches(1.0), Inches(11.3), Inches(1.2), "🎓 修了おめでとうございます", sz=40, clr=C_GOLD, bold=True, align=PP_ALIGN.CENTER)
    txt(s, Inches(1), Inches(3.0), Inches(11.3), Inches(1.0), "一緒に、走り続けましょう。", sz=28, clr=C_WHITE, bold=True, align=PP_ALIGN.CENTER)
    txt(s, Inches(1), Inches(5.0), Inches(11.3), Inches(0.8), "らくらくAI副業キャンパス 第1期生", sz=20, clr=C_GRAY, align=PP_ALIGN.CENTER)
    footer(s, c1, c2)

SESSIONS = [
    (build_s04, "講義04_AI音楽①.pptx"),
    (build_s05, "講義05_AI音楽②.pptx"),
    (build_s06, "講義06_Kindle出版.pptx"),
    (build_s07, "講義07_AIブログ.pptx"),
    (build_s08, "講義08_画像販売.pptx"),
    (build_s09, "講義09_ショート動画.pptx"),
    (build_s10, "講義10_スキル販売.pptx"),
    (build_s11, "講義11_自動化.pptx"),
    (build_s12, "講義12_卒業.pptx"),
]

if __name__ == "__main__":
    for fn, name in SESSIONS:
        prs = create_prs()
        print(f"生成中: {name}...")
        fn(prs)
        out = os.path.join(SCRIPT_DIR, name)
        prs.save(out)
        print(f"  → {len(prs.slides)}枚")
    print("\n全セッション生成完了！")
