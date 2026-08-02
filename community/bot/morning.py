# -*- coding: utf-8 -*-
"""
morning.py — 「おはようチャレンジ」の朝の担当。

やること（2つ）
  1. 毎朝きまった時刻に、あいさつ＋その日のひと言を投稿する
  2. 書いてくださった方に、応える

⚠️ 2の応え方を、わざと分けてある（理由は下）

  - **全員に、スタンプ（リアクション）**。これは必ず付く
  - **言葉で返すのは、一部の方だけ**
      ・その日、いちばん最初に書いた方（部屋の口火を切ってくれた人）
      ・ひとこと添えて書いた方（20字以上＝「おはよう」だけではない人）

なぜ全員に言葉を返さないか
  30人が「おはようございます」と書く部屋で、botが30回返事をすると、
  **人の会話が埋まる**。受講生どうしが「〇〇さんおはよう」と言い合う余白が消える。
  スタンプなら「見てるよ」は伝わるし、じゃまにならない。
  ここはbotが主役の部屋ではない。

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
STATE_PATH = os.path.join(HERE, "_morning_state.json")

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

# 「ひと言」の切り口。日付で順に回す。
# これが無いと、AIは毎日「今日も暑いですね」ばかり書く（実際そうなった）。
TOPICS = [
    "台所・お茶", "手を動かすこと", "眠り・休むこと", "音・静けさ",
    "窓の外・空", "予定を減らすこと", "昨日の自分をねぎらう", "人と話すこと",
    "食べること", "からだの調子", "小さくできたこと", "毎日でなくていいこと",
    "散歩・出かけること", "季節のうつりかわり",
]

GREETINGS = [
    "おはようございます。今日も、ここから。",
    "おはようございます。よく眠れましたか。",
    "おはようございます。新しい一日ですね。",
    "おはようございます。窓を、少し開けてみませんか。",
    "おはようございます。今日はどんな日にしましょう。",
]

# その日のひと言。AIに作らせるが、**必ずこの縛りの中で**。
HITOKOTO_PROMPT = """「おはようチャレンジ」という、朝のあいさつを書き合う部屋に置く、
**その日のひと言**を1つ書いてください。読むのは40〜60代の女性です。

- **1〜2文、45字以内**
- 押しつけがましくない。「〜しましょう」の号令にしない
- **約束しない。**「必ず良いことが起きます」「引き寄せられます」の類は禁止
- 説教くさくしない。今日を少しだけ軽くする、それだけ
- 今日は{month}月{day}日。**天気や気温の話は、なるべく避ける**（毎日それになってしまうため）
- 今日の切り口は「**{topic}**」。ここから、ゆるく1つ
- 絵文字は使わない
- 前置きは書かない。ひと言の本文だけを出力する

**最近使ったので、避けてほしい言い回し：**
{recent}

例：
「やることの確認より、まず一杯のお茶から。」
「今日やらなくていいことを、ひとつ決めておくと、ラクです。」
"""

# AIが使えない朝の、備え。単調にならないよう多めに。
HITOKOTO_FALLBACK = [
    "予定の一番上に、休むことを書いておくのも、ありです。",
    "今日やらなくていいことを、ひとつ決めておくと、ラクになります。",
    "うまくいかない日は、うまくいかないままで、じゅうぶんです。",
    "がんばった日も、そうでない日も、同じだけ一日です。",
    "誰かと比べる材料は、朝いちばんに捨ててしまいましょう。",
    "できたことを、ひとつだけ、数えてみる。それで十分です。",
    "急がなくて大丈夫。今日も、あなたの速さで。",
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
            topic = TOPICS[today.toordinal() % len(TOPICS)]
            t = self.ask_ai(HITOKOTO_PROMPT.format(
                month=today.month, day=today.day,
                topic=topic, recent=recent_txt))
        except Exception as e:
            print("ひと言づくりに失敗:", repr(e)[:160])
            t = None
        # 長い・空・約束くさいものは使わない
        if not t or len(t) > 60 or any(w in t for w in ("必ず", "引き寄せ", "叶いま")):
            t = random.choice(HITOKOTO_FALLBACK)
        self.state["recent"] = (recent + [t])[-7:]
        return t

    async def post_morning(self, today: dt.date):
        ch = self.find_channel()
        if ch is None:
            print("おはようチャレンジのチャンネルが見つかりません")
            return
        body = f"{random.choice(GREETINGS)}\n\n{self.hitokoto(today)}"
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

        text = (message.content or "").strip()
        first = self.state.get("first_of_day") != today
        if first:
            self.state["first_of_day"] = today
            save_state(self.state)

        # 言葉を返すのは、口火を切った方と、ひとこと添えてくれた方だけ
        if not first and len(text) < REPLY_MIN_LEN:
            return
        if not text:
            return

        reply = None
        try:
            reply = await asyncio.to_thread(
                self.ask_ai, REPLY_PROMPT.format(text=text[:400]))
        except Exception as e:
            print("おはようの返事づくりに失敗:", repr(e)[:160])
        if not reply or len(reply) > 120 or "自動応答です" in reply:
            return          # 失敗したら黙る。スタンプは付いているので、それで足りる
        await message.reply(reply, mention_author=False)


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
