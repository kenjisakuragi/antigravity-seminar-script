# -*- coding: utf-8 -*-
"""\npace.py — 一人ひとりの進み具合を覚えて、その人に合った声かけをする。\n\n■ 何をするか（2026-08-23・桜木さんのご指示）\n1. 受講生ひとりずつの「いま何週目か」を覚える\n2. 毎週月曜、**その人に合わせた一言**をDMで送る\n3. 栞に書かれた内容を読んで、**次の一歩**を添える\n\n■ ⚠️ いちばん大事な設計判断：なぜ「DM」なのか\n\nご指示は「月曜にメンションで、生徒それぞれに声がけ」でした。\nただ——**進み具合を含んだ声かけを、公開チャンネルでやってはいけません。**\n\nたとえば栞チャンネルに、こう並んだとします。\n「@Aさん 今週は M2-3 ですね」\n「@Bさん まずは B1-1 から、1本だけ」\nAさんは先へ進んでいて、Bさんはまだ入り口——**それが、全員に見えます。**\n\nBさんは、次の週から来なくなります。**これは推測ではなく、この層で必ず起きます。**\n\nなので、こう分けました。\n\n| どこ | 何を | 誰に見えるか |\n|---|---|---|\n| **栞チャンネル** | 全員へのメンション＋共通の一言 | 全員（進み具合は**含めない**） |\n| **DM** | その人の進み具合に合わせた一歩 | 本人だけ |\n\n「声をかけられた」感覚は公開のメンションで作り、\n「私に合っている」感覚はDMで作る。**両方あって、はじめて効きます。**\n\n→ どうしても公開でやりたい場合は PUBLIC_DETAIL = True にしてください。\nただし、上のリスクを承知のうえで。\n\n■ ⚠️ 進み方のルール（ここが肝）\n**日数では進めません。書いた週だけ、1つ進みます。**\n\n日数で進めると、2週休んだ人に「第5週です」と届きます。\nこれはステップメールと同じ失敗で、追いつけない人を切り捨てます。\n書かなかった週は、**同じ週のまま**。だから、いつ戻ってきても続きになります。\n\n■ ⚠️ 追いかけない\n4週つづけて反応が無い方には、**声かけを止めます**。\n「見ていないことが記録されている」——これは、想像以上に重い。\n止める設計が無い見守りは、ただの督促になります。\n"""
import datetime as dt
import json
import os
import random

import discord
from discord.ext import tasks

HERE = os.path.dirname(os.path.abspath(__file__))
STATE_DIR = os.environ.get("RAKURAKU_STATE_DIR", HERE)
os.makedirs(STATE_DIR, exist_ok=True)
STATE_PATH = os.path.join(STATE_DIR, "_pace_state.json")

# ===== 設定 =====
POST_WEEKDAY = 0          # 月曜
POST_HOUR = 7             # 朝7時（栞の投稿と同じ時刻）
CATCHUP_UNTIL = 21        # 出遅れても、月曜のこの時刻までは送る
GIVE_UP_WEEKS = 4         # 何週サイレントで、声かけを止めるか
DELIVER = "public"        # "public"＝栞チャンネルにまとめて投稿 ／ "dm"＝個別DM
MAX_PER_POST = 8          # 1投稿に載せる人数（Discordの2000字制限に収める）

# ⚠️ 2026-08-23：DMから「公開」に変えました（桜木さんのご判断）。
#    当初はDMにしていました。進み具合が見えると後ろの方が来なくなる、と考えたからです。
#    ただ、これは考えすぎでした。
#    **栞チャンネルでは、そもそも全員の書き込みが見えています。**
#    そこへ助言だけをDMに隠すと、コミュニティではなく個別指導になります。
#    他の人の質問と答えが見えることが、Discordに置いている意味なので、公開にします。
#
#    ⚠️ 公開にするぶん、次の3つは絶対に出さないこと。
#      ・週番号（「第5週です」）… 入った時期が違う人が置いていかれる
#      ・人数（「今週は5人が書きました」）… 書かなかった人が減点に感じる
#      ・比較（「みなさん進んでいます」）

FOOTER = ("やってみたこと、ここに一行どうぞ。\n"
          "「今週はお休み」でも、まったく問題ありません🌸")

CHANNEL_KEYS = ["今週の栞", "栞"]

# ⚠️ 記憶は「栞」だけでは足りません（2026-08-24に判明）。
#    30日間の書き込み数を数えたところ——
#      おはようチャレンジ 117件 ／ 一般 33 ／ 作品ギャラリー 32 ／ 1期生ラウンジ 29
#      質問ひろば 19 ／ 栞 16 ／ できた報告 11
#    **栞は7分の1しかありません。** 栞だけ見ていると、その方が
#    毎朝どこで何をしているかを、まるごと見落とします。
#
#    ⚠️ ただし「記憶する」と「返事をする」は別。
#    　 ここに増やしても、返事が増えるわけではありません。
MEMORY_CHANNELS = [
    "栞", "おはよう", "できた報告", "できたこと",
    "ギャラリー", "質問ひろば", "ビジョンボード", "自己紹介",
]
STUDENT_ROLES = ["受講生", "1期生", "2期生"]
EXCLUDE_ROLES = ["運営", "認定講師"]

JST = dt.timezone(dt.timedelta(hours=9))


def now_jst():
    return dt.datetime.now(JST)


def today_jst():
    return now_jst().date()


def iso_week(d):
    y, w, _ = d.isocalendar()
    return f"{y}-W{w:02d}"


# ===== 学習計画（機械が読む版） =====
# ⚠️ 人が読む版は knowledge/plan_2ki.md ／ plan_1ki.md にあります。
#    直すときは、**両方**直してください。片方だけだと、botと案内がずれます。
PLAN_2KI = [
    ("まず、AIに慣れる", "AIに話しかけて、答えが返ってくる",
     ["W0-1 キャンパスの使い方", "B1-1 AIって、なに？", "B1-2 ChatGPTを始める",
      "B1-3 まず、話しかけてみる", "B1-4 声で話す・写真を見せる"],
     "AIに「今日の献立を3つ教えて」と聞いてみる。それだけ"),
    ("頼み方で、答えが変わる", "欲しい答えに近づける",
     ["B1-5 無料と有料、どう違う？", "B1-6 安全に、かしこく使う",
      "B2-1 頼み方で、答えが変わる", "B2-2 「〇〇して」を、足すコツ",
      "B2-6 よく使う「魔法の一言」集"],
     "同じ質問を、頼み方を変えて2回してみる"),
    ("どんな稼ぎ方があるか、知る", "5つの道を、名前で言える",
     ["M0-1 このスクールの歩き方", "M0-2 AI副業の全体像",
      "M0-3 この3ヶ月で、起きること", "M0-4 3つのAIの始め方", "M0-6 最初の1週間"],
     "まだ決めなくて大丈夫。見るだけ"),
    ("場所を、決める", "自分の「場所」を1つ選べる",
     ["M0-5 プロンプトの基本", "気になる道の第1回（M1-1／M2-1／M3-1／M4-1／M5-1／M6-1）"],
     "ココナラかKindleを、5分だけのぞいて、★の数を見る"),
    ("選んだ道を、深く（前半）", "手を動かしはじめる",
     ["選んだ道の M◯-1 〜 M◯-3"], "1つ、作りはじめる"),
    ("選んだ道を、深く（後半）", "1つ、完成させる",
     ["選んだ道の M◯-4 〜 M◯-6"], "完成品を1つ。人に見せられなくてよい"),
    ("「出す」準備", "出すのが怖くなくなる",
     ["M8-1 はじめて、売るということ", "M8-2 値段を、どう考えるか",
      "M8-3 どこで、売るか", "M8-4 買う方に、先に伝えること"],
     "値段だけ、決めてみる"),
    ("出してみる", "世に出す",
     ["（出す準備：説明文・写真・値段）"], "出す。売れなくて当たり前。「出せた」で100点"),
    ("続く形にする", "手を止めても、止まらない形",
     ["C1-1 道具を、作れるAI", "C2-1 毎朝、ことばが届く", "C2-4 毎朝、自動で動かす"],
     "1つだけ、自動にしてみる"),
    ("暮らしにも使う", "毎日がラクになる",
     ["K1-1 献立に、もう悩まない", "K2-1 あの一通が、書けない",
      "K9-1 スマホの困った、AIに聞く"], "暮らしのことを、1つAIに頼む"),
    ("心を整える", "続けるための土台",
     ["S1-1 未来を、描いてみる", "S2-1 ことばが、自分をつくる",
      "S8-1 AIが、あなたの人生コーチになる"], "自分のための音声を、1本作る"),
    ("ふりかえり", "次の3ヶ月を、自分で決められる",
     ["（3ヶ月で作ったものを、並べてみる）"], "できるようになったことを、3つ書き出す"),
]

# 1期生は「週」で進めない。3つのコースから選ぶ形（plan_1ki.md）。
PLAN_1KI_NOTE = (
    "1期生の方です。週ごとの計画ではなく、"
    "🅐深める／🅑教える／🅒広げる の3コースから選ぶ形になっています。"
)

# 公開チャンネルに出す、共通の一言（進み具合は含めない）
# ⚠️ この投稿は、栞の月曜投稿を**兼ねます**（shiori 側は PACE_ACTIVE で黙ります）。
#    なので「一行どうぞ」の呼びかけを、必ず含めること。
#    ⚠️ 週番号・人数・進み具合は、絶対に入れない。
# ⚠️ 栞の月曜投稿を兼ねます。「一行どうぞ」の呼びかけは FOOTER 側に置いています。
# ⚠️ 月曜は「投げかけ」だけにします（2026-08-23・桜木さんのご判断）。
#    以前は、こちらで一人ひとりの文面を作って並べていました。
#    ただ——**まだ誰も書いていない状態では、書き込みに沿った文が作れません。**
#    当たり障りのない一般論が並ぶだけで、「自分に向けて書かれている」感じが出ない。
#
#    そこで順番を逆にします。
#      月曜：**やったことを聞く**（全員に投げかける）
#      → 書いてくださったら、**その中身に反応する**（30分待って、誰も反応しなければ）
#
#    こうすると、返事は必ず**本物の書き込みに沿ったもの**になります。
#    そして公開なので、他の方の質問と答えが、そのまま全員の学びになります。
MONDAY_ASK = [
    "おはようございます。今週も始まりました。\n\n"
    "この1週間、やってみたことを**一行だけ**教えてください。\n\n"
    "　「動画を1本見た」\n"
    "　「AIに献立を聞いてみた」\n"
    "　「うまくいかなくて、やめた」\n"
    "　「今週は何もできなかった」\n\n"
    "どれでも構いません。書いてくださった方に、**次の一手を1つ**お返しします。",

    "おはようございます。月曜です。\n\n"
    "先週から今日までで、やってみたことはありますか。一行で構いません。\n\n"
    "「何もできなかった」も、そのまま書いてください。\n"
    "そこから、**5分で終わる次の一手**をお返しします。",

    "おはようございます。今週の1回目です。\n\n"
    "いま、どのあたりまで来ていますか。一行で教えてください。\n\n"
    "進んでいても、止まっていても構いません。\n"
    "いまの位置に合わせて、**次にやること**をお返しします。",
]

# ===== AI副業の全体像（5段） =====
# ⚠️ 返事のなかで「いまここ → 次ここ」を示すための地図。
#    グルコンで話した「場所 → 作業 → 代行」と、同じ骨格にしてあります。
#    講座の並びとも対応しているので、案内する動画がぶれません。
ROADMAP = """
【AI副業の全体像】5つの段があります。

　1. 選ぶ　　… どこでやるか決める（もう買われている場所を探す）　→ M0
　2. 作る　　… 1つ、完成させる　　　　　　　　　　　　　　　　 → M1〜M7
　3. 出す　　… 世に出す（売れなくてよい。出せたら100点）　　　　→ M8
　4. 直す　　… 売れない理由を直す（写真・タイトル・説明文）　　　→ M9
　5. 仕組みにする … 手を止めても止まらない形にする　　　　　　　 → C1〜C6

⚠️ 段は飛ばせます。すでに作れている方は 3 から、
　 出せている方は 4 から始めて構いません。順番は絶対ではありません。
"""

REPLY_PROMPT = """あなたは「AIさくらぎ」。らくらくAIキャンパスの、受講生を見守るサポート役です。\n「今週の栞」に書いてくださった内容へ、返事を書いてください。\n\n【今回、書いてくださったこと】\n{name}さん（{cohort}）：「{text}」\n\n【この方が、これまで書いてくださったこと（古い順）】\n{past}\n\n{roadmap}\n\n【参考：この方のいまのあたり】{theme}\n⚠️ これはあくまで参考です。**書かれた内容と合わなければ、無視してください。**\n\n【⚠️ 直前に、他の方へこう返しました】\n{recent}\n**これと似た助言は、絶対にしないでください。** 同じ言い回しも避けてください。\n\n━━━ ここからが、いちばん大事です ━━━\n\n**書かれた内容から、次の一手を決めてください。**\n週の計画からではありません。**その方が、いま何をしているか**から決めます。\n\n例：\n・「noteの記事が途中で止まっている」→ 書きかけの文章をAIに渡して整えてもらう手順\n・「毎朝6時に自動化できた」→ すでに上級。次は別の作業を自動化する、など\n・「アフィリエイト申請中」→ 申請の待ち時間にできること\n・「AI基礎を見始めます」→ その動画の、見どころを1つ\n・「何も進んでいない」→ **5分で終わる、いちばん小さいこと**を1つだけ\n\n**講座を案内するときは、システムプロンプトの「講座の目次」から、\n書かれた内容にいちばん近いものを選んでください。**\n（noteなら M5、動画なら M2、音楽なら M3、自動化なら C1〜C3、Kindleなら M4 …）\n\n⚠️ **部屋の名前を間違えないこと。記号で決まっています。**\n　 M番号 → 💰 収入の種の部屋　／　B番号 → 🧭 AI基礎の部屋\n　 S番号 → 🌙 なりたい私の部屋　／　K番号 → 🍀 暮らしが広がる部屋\n　 C番号 → ⚡ 仕組みが働く部屋\n　 （2026-08-24、M5-5を「暮らしが広がる部屋」と案内する誤りが実際に出ました。\n　 　 違う部屋を探しに行かせると、そこで止まります）\n\n⚠️ 1期生の方には、B1・B2などの基礎講座を案内しないでください。\n　 3ヶ月の講座を終えた方です。入学時の課題を出すのは失礼にあたります。\n\n【書き方】4〜5行。長いと読まれません。\n1) 書かれた中身に、具体的に触れて受け止める\n2) **いま全体像のどこにいて、次がどこか。1行だけ。**\n　 例「いまは『2. 作る』のなかほど。ここを抜けると『3. 出す』です」\n　 例「もう『5. 仕組みにする』に入っています。ここまで来た方は多くありません」\n　 ⚠️ 段の番号と名前は、上の地図のとおりに。勝手に作らない\n　 ⚠️ 「そうすれば稼げます」に転ばせない。**道筋であって、成果の約束ではない**\n3) 次の一手を1つだけ。**具体的に**（動画なら1本だけ／作業なら5分で終わる大きさ）\n4) **その一手が、どこへつながるか**を短く添える（「ここを抜けると、出す段です」など）\n5) 絵文字は最大1つ。前置きは書かない。返事の本文だけを出力する\n\n【トンマナ】\nこの方たちは「AI副業」に興味を持って申し込んだ方です。癒やしを求めて来たのではありません。\n- ❌ 「そっと」「受け取ります」「あなたのペースで」——情緒に寄りすぎ\n- ❌ 「稼げます」「収益が」——期待値が上がって、あとで落ちる\n- ✅ 実務的・具体的・無駄がない\n- やわらかさは言い方で出す（「〜してみませんか」）。世界観では出さない\n\n⚠️ **ここでは絶対にエスカレーションしないこと。**\n　 「お答えできません」「桜木が答えます」の類は返さない。\n　 栞は質問の場ではありません。**どんな内容でも、必ず次の一手を1つ出せます。**\n\n【絶対にしないこと】\n- 「遅れています」「まだですね」／他の方と比べる／週番号を出す／期限を切る\n- 収入や成果を約束する\n- 「できなかった」と書かれていたら、そのまま肯定する。次の一手はさらに小さく\n"""

DM_PROMPT = """あなたは「AIさくらぎ」。40〜60代の受講生を見守る、やさしいサポート役です。\n次の方へ、**月曜の朝に届く短いDM**を書いてください。\n\n【この方のこと】\n・お名前：{name}\n・今週のテーマ：{theme}\n・今週できるようになること：{goal}\n・今週の動画：{videos}\n・今週の一歩：{step}\n・最近この方が栞に書いてくださったこと：\n{entries}\n\n【書き方】\n- **4行以内**。長いと読まれません\n- まず、最近書いてくださったことに**具体的に触れて**受け止める\n- そのうえで、今週の一歩を**1つだけ**そっと置く（命令しない。「〜してみませんか」）\n- 動画は**多くても1本だけ**名前を出す。全部並べない\n- 絵文字は最大1つ\n- 前置き・説明は書かない。DMの本文だけを出力する\n\n【絶対にしないこと】\n- 「遅れています」「まだですね」など、進みの遅さに触れる\n- 他の方と比べる（「みなさん進んでいます」等）\n- 週番号を出す（「第5週です」等）\n- 課題として出す（「今週中に」等）\n- 収入や成果を約束する\n"""

FALLBACK_DM = [
    "おはようございます。今週も、あなたの速さで大丈夫ですよ🌸\n"
    "気が向いたら、動画を1本だけ。それで十分です。",
    "おはようございます。新しい一週間ですね🌷\n"
    "無理のない範囲で、1つだけ触ってみてください。",
]


# ===== 記録 =====
def load_state():
    if os.path.exists(STATE_PATH):
        try:
            return json.load(open(STATE_PATH, encoding="utf-8"))
        except Exception as e:
            print("pace: 記録が読めません", repr(e)[:120])
    return {"users": {}, "last_run": ""}


def save_state(st):
    json.dump(st, open(STATE_PATH, "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)


def fmt_history(entries, limit=10):
    """これまでの書き込みを、古い順に並べて渡す。

    ⚠️ **直前の1件だけに反応すると、返事が浅くなります。**
    　 「先週できなかったことが、今週できた」——この変化に触れられるかどうかが、
    　 見てもらえている感じの分かれ目になります。だから経過ごと渡します。
    """
    if not entries:
        return "（今回がはじめてです）"
    out = []
    for e in entries[-limit:]:
        if isinstance(e, dict):
            ch = e.get("c", "")
            out.append("・%s %s%s" % (
                e.get("d", ""), ("[" + ch + "] ") if ch else "", e.get("t", "")))
        else:
            out.append("・" + str(e))
    return chr(10).join(out)


class Pace:
    def __init__(self, client, ask_ai, guild_id=None):
        self.client = client
        self.ask_ai = ask_ai
        self.guild_id = guild_id
        self.state = load_state()

    # ---- 対象者 ----
    def _students(self):
        out = []
        for g in self.client.guilds:
            if self.guild_id and g.id != self.guild_id:
                continue
            for m in g.members:
                if m.bot:
                    continue
                roles = [r.name for r in m.roles]
                if any(r in EXCLUDE_ROLES for r in roles):
                    continue
                if not any(r in STUDENT_ROLES for r in roles):
                    continue
                cohort = "1ki" if "1期生" in roles else "2ki"
                out.append((m, cohort))
        return out

    def _rec(self, member, cohort):
        u = self.state["users"].setdefault(str(member.id), {})
        u.setdefault("name", member.display_name)
        u.setdefault("cohort", cohort)
        u.setdefault("week", 1)
        u.setdefault("entries", [])
        u.setdefault("last_entry_week", "")
        u.setdefault("silent", 0)
        u.setdefault("last_dm_week", "")
        u["name"] = member.display_name      # 表示名は変わるので毎回上書き
        u["cohort"] = cohort
        return u

    # ---- ① 栞に書かれたら、記録して1つ進める ----
    def on_entry(self, message):
        """⚠️ shiori.on_entry から呼ぶ。ここでは返事はしない（返事は栞の担当）。

        ⚠️ **受講生タグの方だけを記録する。**
        　 2026-08-24、桜木さんご自身の告知文が「2期生の書き込み」として
        　 記録される事故があった。shiori 側には受講生チェックを入れていたが、
        　 ai_support_bot は PACE.on_entry を**別に呼んでいる**ので、素通りしていた。
        　 呼び出し側に頼らず、ここでも必ず確かめる。
        """
        roles = [r.name for r in getattr(message.author, "roles", [])]
        if any(r in EXCLUDE_ROLES for r in roles):
            return
        if not any(r in STUDENT_ROLES for r in roles):
            return                       # 運営・スタッフ・桜木さんは記録しない

        uid = str(message.author.id)
        u = self.state["users"].setdefault(uid, {
            "name": message.author.display_name, "cohort": "2ki",
            "week": 1, "entries": [], "last_entry_week": "",
            "silent": 0, "last_dm_week": ""})
        wk = iso_week(today_jst())

        text = (message.content or "").strip()
        if text:
            ch = getattr(message.channel, "name", "")
            u["entries"] = (u.get("entries", []) +
                            [{"d": today_jst().isoformat(),
                              "c": ch[:16], "t": text[:140]}])[-16:]

        # **同じ週に何度書いても、進むのは1つだけ**
        if u.get("last_entry_week") != wk:
            u["week"] = min(u.get("week", 1) + 1, len(PLAN_2KI))
            u["last_entry_week"] = wk
        u["silent"] = 0
        save_state(self.state)

    # ---- ② 月曜の声かけ ----
    async def run_monday(self, today):
        """月曜は「やったことを聞く」だけ。人ごとの文面は作らない。"""
        wk = iso_week(today)
        if self.state.get("last_run") == wk:
            return
        ch = self._find_channel()
        if ch is None:
            print("pace: 栞チャンネルが見つかりません")
            return

        # 声をかける相手（4週サイレントの方は、そっと外す）
        mentions = []
        for member, cohort in self._students():
            u = self._rec(member, cohort)
            if u.get("last_entry_week") != prev_week(wk):
                u["silent"] = u.get("silent", 0) + 1
            if u["silent"] > GIVE_UP_WEEKS:
                continue
            mentions.append(member.mention)

        head = " ".join(mentions[:25])
        body = random.choice(MONDAY_ASK)
        await ch.send((head + "\n\n" + body)[:1990] if head else body[:1990])

        self.state["last_run"] = wk
        save_state(self.state)
        print("pace: 月曜の投げかけ %d名へ (%s)" % (len(mentions), wk))

    def note_any(self, message):
        """栞以外のチャンネルの書き込みも、記憶にだけ入れる。

        ⚠️ **週は進めません。** 週が進むのは、栞に書いたときだけ。
        　 おはようの挨拶で週が進むと、実際より先に行ってしまいます。
        """
        ch = getattr(message.channel, "name", "") or ""
        if not any(k in ch for k in MEMORY_CHANNELS):
            return
        roles = [r.name for r in getattr(message.author, "roles", [])]
        if any(r in EXCLUDE_ROLES for r in roles):
            return
        if not any(r in STUDENT_ROLES for r in roles):
            return
        text = (message.content or "").strip()
        if len(text) < 4:
            return                       # 「おはよう」だけは覚えない

        uid = str(message.author.id)
        u = self.state["users"].setdefault(uid, {
            "name": message.author.display_name, "cohort": "2ki",
            "week": 1, "entries": [], "last_entry_week": "",
            "silent": 0, "last_dm_week": ""})
        u["name"] = message.author.display_name
        u["entries"] = (u.get("entries", []) +
                        [{"d": today_jst().isoformat(),
                          "c": ch[:16], "t": text[:140]}])[-16:]
        save_state(self.state)

    def profile_of(self, member):
        """その方の「これまで」を、短い文章にして返す。

        ⚠️ 質問ひろばで答えるときに使う。同じ質問でも、
        　 はじめての方と、もう出品まで進んだ方とでは、返す答えが違うので。
        """
        u = self.state["users"].get(str(getattr(member, "id", "")), {})
        if not u:
            return ""
        i = max(1, min(u.get("week", 1), len(PLAN_2KI))) - 1
        theme = PLAN_2KI[i][0]
        return ("【この方について】\n・いまのあたり：" + theme +
                "\n・これまでの書き込み：\n" + fmt_history(u.get("entries", []), 8))

    # ---- 書いてくださったことに、返す ----
    async def build_reply(self, message):
        """栞への書き込みに、その人に合わせた返事を作る。

        ⚠️ shiori._reply から呼ばれる。**数分待って、誰も反応しなかったときだけ**。
        ⚠️ 週の計画は「参考」までにとどめる。**主役は、書かれた内容**。
        　 週を主役にすると、全員が同じ助言になる（2026-08-24に実際そうなった）。
        """
        uid = str(message.author.id)
        u = self.state["users"].get(uid, {})

        roles = [r.name for r in getattr(message.author, "roles", [])]
        is_1ki = "1期生" in roles
        cohort = "1期生・3ヶ月の講座を終えた方" if is_1ki else "2期生・今月から"

        # 参考として渡す「いまのあたり」。1期生には週の概念を使わない
        if is_1ki:
            theme = "（1期生。基礎は終えている。書かれた内容から判断すること）"
        else:
            i = max(1, min(u.get("week", 1), len(PLAN_2KI))) - 1
            theme = PLAN_2KI[i][0]

        # ⚠️ 直前に他の方へ返した助言を集めて、同じことを言わせない
        recent = await self._recent_replies(message)

        import asyncio
        return await asyncio.to_thread(self.ask_ai, REPLY_PROMPT.format(
            name=message.author.display_name,
            cohort=cohort,
            text=(message.content or "").strip()[:400],
            past=fmt_history(u.get("entries", [])[:-1]),
            theme=theme,
            roadmap=ROADMAP,
            recent=recent))

    async def _recent_replies(self, message, n=4):
        """このチャンネルで、直前に自分（bot）が返した助言を集める。

        ⚠️ これが無いと、同じ日に同じ助言を何人にも返してしまう。
        　 受講生から見ると「コピペで返された」に見える。いちばん冷める。
        """
        out = []
        try:
            me = self.client.user.id if self.client.user else 0
            async for m in message.channel.history(limit=30, before=message):
                if m.author.id != me:
                    continue
                body = (m.content or "").strip().replace(chr(10), " ")
                if len(body) < 20 or body.startswith("<@"):
                    continue          # 月曜の投げかけは除く
                out.append("・" + body[:120])
                if len(out) >= n:
                    break
        except Exception as ex:
            print("pace: 直前の返事を読めませんでした", repr(ex)[:120])
        return "\n".join(out) if out else "（まだありません）"

    def _find_channel(self):
        for g in self.client.guilds:
            if self.guild_id and g.id != self.guild_id:
                continue
            for ch in g.text_channels:
                if any(k in (ch.name or "") for k in CHANNEL_KEYS):
                    return ch
        return None


def prev_week(wk):
    y, w = wk.split("-W")
    d = dt.date.fromisocalendar(int(y), int(w), 1) - dt.timedelta(days=7)
    return iso_week(d)


def setup(client, ask_ai, guild_id=None):
    # ⚠️ 栞の月曜投稿と、そっとDMを、こちらに寄せる（二重投稿・二重DMを防ぐ）
    pace = Pace(client, ask_ai, guild_id)

    # ⚠️ 栞の月曜投稿・そっとDMを、こちらに寄せる（二重投稿・二重DMを防ぐ）
    #    さらに、書き込みへの返事も pace に作らせる（その人の週と過去の書き込みを使う）
    try:
        import shiori
        shiori.PACE_ACTIVE = True
        shiori.REPLY_HOOK = pace.build_reply
    except Exception as e:
        print("pace: 栞との調整に失敗", repr(e)[:120])

    # ⚠️ 30分だと、botを起動した時刻によって最大30分ずれる。
#    2026-08-24、7:00の投稿が7:18になった。10分にして、ずれを詰める。
    @tasks.loop(minutes=10)
    async def beat():
        now = now_jst()
        if now.weekday() != POST_WEEKDAY:
            return
        if not (POST_HOUR <= now.hour < CATCHUP_UNTIL):
            return
        try:
            await pace.run_monday(now.date())
        except Exception as e:
            print("pace: 月曜処理で失敗", repr(e)[:200])

    @beat.before_loop
    async def _wait():
        await client.wait_until_ready()

    beat.start()
    return pace
