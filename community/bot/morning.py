# -*- coding: utf-8 -*-
"""
morning.py — 「おはようチャレンジ」の朝の担当。

やること（2つ）
  1. 毎朝きまった時刻に、あいさつ＋その日のひと言を投稿する
  2. 書いてくださった方に、応える

⚠️ 2の応え方を、わざと分けてある（理由は下）

  - **全員に、スタンプ（リアクション）**。これは必ず付く
  - **言葉では返さない**（2026/8/4 変更）

なぜ言葉で返さないか（2026/8/4・桜木さん指定）
  ここは**あいさつを交わす部屋**であって、質問の部屋ではない。
  botが返事をすると、受講生どうしが「〇〇さんおはよう」と言い合う余白が消える。
  スタンプなら「見てるよ」は伝わるし、じゃまにならない。
  ここはbotが主役の部屋ではない。

  ※ 質問されたときは、@メンションすれば今までどおり答える。

守ること（栞と同じ）
  - 「◯日連続ですね」「久しぶりですね」と**言わない**。数えていることを見せない
  - 書かなかった日のことに触れない
  - 「必ず〇〇できる」「引き寄せられます」の類は言わない（約束しない）

前提：ai_support_bot.py から呼ばれる（同じbotユーザー・同じ接続）。
"""
import os
import json
import random
import datetime as dt

from discord.ext import tasks

HERE = os.path.dirname(os.path.abspath(__file__))
# 記録は**コードとは別の場所**に置く。
# setup.sh は入れ直しのたびにコード一式を消して置き直すので、
# コードと同じ場所に置くと**記録ごと消える**（実際に消えて、栞が二重投稿された）。
STATE_DIR = os.environ.get("RAKURAKU_STATE_DIR", HERE)
os.makedirs(STATE_DIR, exist_ok=True)
STATE_PATH = os.path.join(STATE_DIR, "_morning_state.json")

# 時刻は**必ず日本時間**で見る。
# このPCは日本時間だが、レンタルサーバーはたいてい世界標準時（UTC）で動く。
# 素の now() のままサーバーに載せると、朝6:30の投稿が**日本の15:30**に出る。
JST = dt.timezone(dt.timedelta(hours=9))


def now_jst() -> dt.datetime:
    return dt.datetime.now(JST)


def today_jst() -> dt.date:
    return now_jst().date()


# ===== 設定 =====

CHANNEL_KEYS = ["おはよう"]      # チャンネル名の部分一致
POST_HOUR = 6                    # 朝の投稿時刻
POST_MIN = 30
CATCHUP_UNTIL = 10               # 出遅れても、この時刻まではその日ぶんを投稿する
REPLY_MIN_LEN = 20               # これ以上書いてくれたら、言葉で返す
STAMPS = ["☀️", "🌸", "🌷", "🍀", "🌱"]

# 豆知識の切り口。日付で順に回す。
# これが無いと、AIは毎日「今日も暑いですね」ばかり書く（実際そうなった）。
# AIの話と暮らしの話を**交互**に。AIばかりだと勉強くさくなり、暮らしばかりだと学校でなくなる。
TOPICS = [
    ("AI", "ChatGPTに話しかけるときの、ちょっとしたコツ"),
    ("暮らし", "台所やお茶の、小さな知恵"),
    ("AI", "AIが得意なこと・苦手なこと"),
    ("暮らし", "眠りや休み方の、小さな知恵"),
    ("AI", "スマホでAIを使うときの、便利な機能"),
    ("暮らし", "片づけや家事の、小さな知恵"),
    ("AI", "AIに聞くと、思いのほか役に立つこと"),
    ("暮らし", "からだをいたわる、小さな知恵"),
    ("AI", "AIの答えが物足りないときの、頼み直し方"),
    ("暮らし", "季節の楽しみ・旬のもの"),
    ("AI", "AIで作れるもの（絵・文章・音声）の話"),
    ("暮らし", "人とのやりとりが、少しラクになる工夫"),
    ("AI", "AIを使うときに、気をつけたいこと"),
    ("暮らし", "外に出る日の、小さな楽しみ"),
]

GREETINGS = [
    "おはようございます！　今日も一日、はじまりましたね☀️",
    "おはようございます！　よく眠れましたか🌸",
    "おはようございます！　新しい一日です🌷",
    "おはようございます！　窓の外、いかがですか🍀",
    "おはようございます！　今日もこの部屋を開けておきますね🌱",
]

# 書き込みへの呼びかけ。**毎回「〜でも大丈夫」をセットにする**のが絶対条件。
INVITES = [
    "よかったら、今朝の調子をひとこと聞かせてください。\n"
    "「おはよう」だけでも、スタンプひとつでも、うれしいです。",

    "今日やってみたいこと、ひとつだけ書いてみませんか。\n"
    "「まだ決めてない」でも、ぜんぜん大丈夫です。",

    "上の話、やってみた方がいたら、ぜひ教えてください。\n"
    "読むだけの日があっても、もちろん大丈夫ですよ。",

    "「おはよう」の二文字だけでも、置いていってください。\n"
    "書かない日があっても、何も起きません。気楽にどうぞ。",

    "今日の気分、ひとことでどうぞ。\n"
    "「ねむい」でも「元気」でも。それだけで、じゅうぶんです。",
]

# その日の豆知識。AIに作らせるが、**必ずこの縛りの中で**。
HITOKOTO_PROMPT = """「おはようチャレンジ」という、朝のあいさつを書き合う部屋に置く、
**今日の豆知識**を書いてください。読むのは40〜60代の女性で、AIやパソコンが得意でない方が多いです。

今日のテーマは「**{topic}**」（{kind}の話）。

- **3〜4行、120字以内**。見出しは付けない
- **その場ですぐ試せること**を1つ。抽象的な心がけの話にしない
- 専門用語・横文字は使わない。使うなら、かならず言いかえる
- 明るく、軽やかに。ただし**大げさにしない**
- **約束しない。**「必ず○○できます」「引き寄せられます」の類は禁止
- 説教にしない。「〜しましょう」の号令より「〜すると、○○です」の形で
- 今日は{month}月{day}日
- 絵文字は使わない（部屋の他の場所で使うので、ここは文字だけ）
- 前置きは書かない。豆知識の本文だけを出力する

**最近使ったので、避けてほしい話：**
{recent}

例（AIの話）：
「AIに『小学生にもわかるように』と付けると、答えがぐっとやさしくなります。
むずかしい説明が返ってきたときは、そのまま『もっとやさしく』と打つだけでも大丈夫。
何度でも言い直せるので、遠慮はいりません。」

例（暮らしの話）：
「保冷剤は、冷凍庫の手前に立てて並べると、必要なときにすっと取り出せます。
袋にまとめて入れておくより、探す時間が減ります。
夏のあいだだけの置き方にしておくと、戻すのもかんたんです。」
"""

# AIが使えない朝の、備え。単調にならないよう多めに。
HITOKOTO_FALLBACK = [
    "AIに聞くときは、最後に「小学生にもわかるように」と付けてみてください。\n"
    "答えの雰囲気が、ずいぶんやわらかくなります。\n"
    "むずかしい返事が来たら、そのまま「もっとやさしく」と打てば大丈夫です。",

    "スマホのChatGPTには、マイクのボタンがあります。\n"
    "打つのが大変な日は、しゃべるだけで質問できます。\n"
    "言い間違えても、だいたい伝わります。気にしなくて大丈夫です。",

    "AIは、答えを一度で決めなくていい相手です。\n"
    "「もう3つ出して」「短くして」と、何度でも頼み直せます。\n"
    "遠慮する必要がないのが、いちばんの取り柄かもしれません。",

    "冷蔵庫にあるものを並べて「これで何が作れる？」と聞くと、献立が返ってきます。\n"
    "苦手な食材があれば「◯◯は抜きで」と足すだけ。\n"
    "思いつかない日の、ちいさな助けになります。",

    "予定の一番上に「休む」と書いておくのも、ひとつの手です。\n"
    "書いてあると、休んだときに罪悪感が減ります。\n"
    "手帳でも、スマホのメモでも大丈夫です。",
]

REPLY_PROMPT = """次は、朝のあいさつの部屋に書かれた一言です。

「{text}」

これに、**1文だけ**の短い返事を書いてください。読むのは40〜60代の女性です。

- あたたかく、書かれた中身に触れる
- **助言・提案・励ましの押し売りをしない**
- 「毎日えらいですね」「久しぶりですね」は**禁止**（続いた日数や、間があいたことに触れない）
- **自然な日本語で。**（例：「孫さん」ではなく「お孫さん」。おかしな敬称をつけない）
- 絵文字は最大1つ
- 前置きは書かない。返事の本文だけを出力する
"""


def load_state() -> dict:
    if os.path.exists(STATE_PATH):
        try:
            return json.load(open(STATE_PATH, encoding="utf-8"))
        except Exception:
            pass
    return {"last_post": None, "first_of_day": None, "recent": []}


def save_state(state: dict):
    json.dump(state, open(STATE_PATH, "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)


class Morning:
    def __init__(self, client, ask_ai, guild_id=None):
        self.client = client
        self.ask_ai = ask_ai
        self.guild_id = guild_id
        self.state = load_state()

    def is_morning_channel(self, channel) -> bool:
        name = getattr(channel, "name", "") or ""
        return any(k in name for k in CHANNEL_KEYS)

    def find_channel(self):
        for g in self.client.guilds:
            if self.guild_id and g.id != self.guild_id:
                continue
            for ch in g.text_channels:
                if self.is_morning_channel(ch):
                    return ch
        return None

    # ---- ① 朝の投稿 ----
    def hitokoto(self, today: dt.date) -> str:
        # 直近1週間ぶんを渡して、似た言い回しが続かないようにする
        recent = self.state.get("recent") or []
        recent_txt = "\n".join("・" + r for r in recent) if recent else "（まだありません）"
        try:
            kind, topic = TOPICS[today.toordinal() % len(TOPICS)]
            t = self.ask_ai(HITOKOTO_PROMPT.format(
                month=today.month, day=today.day,
                kind=kind, topic=topic, recent=recent_txt))
        except Exception as e:
            print("豆知識づくりに失敗:", repr(e)[:160])
            t = None
        # 長い・空・約束くさいものは使わない
        if not t or len(t) > 200 or any(w in t for w in ("必ず", "引き寄せ", "叶いま")):
            t = random.choice(HITOKOTO_FALLBACK)
        self.state["recent"] = (recent + [t])[-7:]
        return t

    async def post_morning(self, today: dt.date):
        ch = self.find_channel()
        if ch is None:
            print("おはようチャレンジのチャンネルが見つかりません")
            return
        # あいさつ → 豆知識 → 呼びかけ の3段。
        # 呼びかけは**必ず最後**に置く。豆知識で終わると、読んで満足して閉じてしまう
        body = (f"{random.choice(GREETINGS)}\n\n"
                f"**今日の豆知識**\n{self.hitokoto(today)}\n\n"
                f"{random.choice(INVITES)}")
        await ch.send(body)
        self.state["last_post"] = today.isoformat()
        self.state["first_of_day"] = None      # その日の「最初の1人」枠を空ける
        save_state(self.state)
        print(f"おはよう：投稿しました（{today}）")

    # ---- ② 書いてくれた方に応える ----
    async def on_post(self, message):
        import asyncio
        today = today_jst().isoformat()

        # スタンプは、全員に
        try:
            await message.add_reaction(random.choice(STAMPS))
        except Exception:
            pass

        # 言葉では返さない。スタンプだけ（上の「なぜ」を参照）
        first = self.state.get("first_of_day") != today
        if first:
            self.state["first_of_day"] = today
            save_state(self.state)


def setup(client, ask_ai, guild_id=None) -> Morning:
    mo = Morning(client, ask_ai, guild_id)

    @tasks.loop(minutes=15)
    async def beat():
        await client.wait_until_ready()
        now = now_jst()
        today = now.date()
        if mo.state.get("last_post") == today.isoformat():
            return                      # その日はもう投稿済み
        # PCが寝ていて6:30を逃しても、朝のうちに開けば、その日ぶんを出す。
        # ただし昼を回ったら出さない（夕方に「おはようございます」は、かえって寂しい）
        if now.hour * 60 + now.minute < POST_HOUR * 60 + POST_MIN:
            return
        if now.hour >= CATCHUP_UNTIL:
            return
        await mo.post_morning(today)

    beat.start()
    return mo
