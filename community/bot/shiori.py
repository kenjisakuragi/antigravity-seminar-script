# -*- coding: utf-8 -*-
"""
shiori.py — 特典③「今週の栞」の、Discord側の運用を自動化する。

ステップメールが毎週1通「今週やること」を届ける。
受講生はそれを **Discordに一行だけ書く**。この一行を受けとめるのが、ここの仕事。

やること（3つだけ）
  1. 毎週月曜の朝、栞チャンネルに「今週の一行、どうぞ」の投稿をする
  2. 書いてくださった方に、**必ず**ひとこと返す（ChatGPTで短く。失敗したら定型文）
  3. 2週つづけて書いていない方にだけ、そっとDMを1通。**それ以上は追いかけない**

⚠️ ここは運用のルールが厳しい。コードを変える前に、下の「守ること」を読むこと。

守ること（プレッシャーをかけない設計）
  - 書いていない人のことを、**公開の場で言わない**（名指しも、ほのめかしも）
  - 「今週は◯人が書きました」のような **数を発表しない**（書かなかった人が減点に感じる）
  - 週番号を公開の投稿に出さない。**入会日は人によって違う**ので、
    「第5週です」と言うと、遅れて入った人が置いていかれた気持ちになる
  - DMは1回だけ。**返事がなくても、二度追わない**（同じ人へは最短6週あける）
  - 「お休みでも大丈夫」を、毎回どこかに置く

前提：ai_support_bot.py から呼ばれる（同じbotユーザー・同じ接続を使う）。
"""
import os
import json
import random
import datetime as dt

import discord
from discord.ext import tasks

HERE = os.path.dirname(os.path.abspath(__file__))
STATE_PATH = os.path.join(HERE, "_shiori_state.json")

# 時刻は**必ず日本時間**で見る。
# このPCは日本時間だが、レンタルサーバーはたいてい世界標準時（UTC）で動く。
# 素の now() のままサーバーに載せると、朝6:30の投稿が**日本の15:30**に出る。
JST = dt.timezone(dt.timedelta(hours=9))


def now_jst() -> dt.datetime:
    return dt.datetime.now(JST)


def today_jst() -> dt.date:
    return now_jst().date()


# ===== 設定 =====

CHANNEL_KEYS = ["今週の栞", "栞"]        # チャンネル名の部分一致
TARGET_ROLES = ["1期生", "2期生"]        # 沈黙チェックの対象（このロールを持つ人だけ）
EXCLUDE_ROLES = ["運営", "認定講師"]      # 運営側はDMの対象外

POST_WEEKDAY = 0        # 0=月曜
POST_HOUR = 7           # 朝7時（メールの配信時刻と揃える）
CATCHUP_UNTIL = 21      # 出遅れても、月曜のこの時刻までは、その週ぶんを投稿する
SILENT_WEEKS = 2        # 何週サイレントでDMするか
DM_COOLDOWN_WEEKS = 6   # 同じ人へ次にDMできるまで（追いかけない）
JOIN_GRACE_DAYS = 14    # 入って間もない人はDMしない

# 月曜の投稿。毎週まったく同じだと流れるので、少しだけ変える。
# ⚠️ どれも「週番号」と「人数」を含めないこと。
MONDAY_POSTS = [
    "おはようございます。新しい一週間ですね。\n"
    "今週の栞、メールに届いていますか。やってみたこと、一行でどうぞ。\n"
    "「今週はお休み」でも、もちろん大丈夫です🌸",

    "おはようございます。今週の栞が届いています。\n"
    "見た・作った・迷った——なんでも、一行だけ置いていってください。\n"
    "書かない週があっても、まったく問題ありません🌷",

    "おはようございます。月曜の朝です。\n"
    "今週やることは、ひとつだけ。できたら、ここに一行を。\n"
    "できなくても、大丈夫。またここにいます🍀",
]

# AIが使えない時の返し。単調にならないよう複数用意する。
FALLBACK_REPLIES = [
    "書いてくださって、ありがとうございます🌸 その一行が、いちばん大事です。",
    "受け取りました。ちゃんと進んでいますよ🌷",
    "ありがとうございます。ここに置いてくださるだけで、じゅうぶんです🍀",
    "うれしいです。今週も、あなたの速さで大丈夫ですよ🌸",
]

REPLY_PROMPT = """次は、受講生さんが「今週の栞」に書いてくださった一行です。

「{text}」

これに、40〜60代の女性にとどく、**1〜2文の短い返事**を書いてください。

- あたたかく、具体的に受け止める（何を書いてくれたかに触れる）
- 助言・指示・次の課題は出さない。**受け止めるだけ**
- 「すごい」の押し売りをしない。おおげさにしない
- 絵文字は最大1つ
- 「お休み」「できなかった」と書かれていたら、それを**そのまま肯定**する
- 前置き・説明は書かない。返事の本文だけを出力する
"""

# ===== 状態の保存 =====
# 追いかけないための記録なので、消えると「二度追い」が起きる。バックアップ対象。


def load_state() -> dict:
    if os.path.exists(STATE_PATH):
        try:
            return json.load(open(STATE_PATH, encoding="utf-8"))
        except Exception:
            pass
    return {"last_post": None, "last_entry": {}, "last_dm": {}}


def save_state(state: dict):
    json.dump(state, open(STATE_PATH, "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)


def iso_week(d: dt.date) -> str:
    y, w, _ = d.isocalendar()
    return f"{y}-W{w:02d}"


def weeks_between(a: str, b: str) -> int:
    """ISO週の文字列どうしの差。ざっくりでよい（月曜起点で数える）。"""
    def monday(s):
        y, w = s.split("-W")
        return dt.date.fromisocalendar(int(y), int(w), 1)
    return (monday(b) - monday(a)).days // 7


# ===== 本体 =====

class Shiori:
    def __init__(self, client, ask_ai, guild_id=None):
        self.client = client
        self.ask_ai = ask_ai      # ai_support_bot の関数をそのまま借りる
        self.guild_id = guild_id
        self.state = load_state()

    # ---- チャンネル判定 ----
    def is_shiori_channel(self, channel) -> bool:
        name = getattr(channel, "name", "") or ""
        return any(k in name for k in CHANNEL_KEYS)

    def find_channel(self):
        for g in self.client.guilds:
            if self.guild_id and g.id != self.guild_id:
                continue
            for ch in g.text_channels:
                if self.is_shiori_channel(ch):
                    return ch
        return None

    # ---- ① 月曜の投稿 ----
    async def post_monday(self, today: dt.date):
        ch = self.find_channel()
        if ch is None:
            print("栞チャンネルが見つかりません（名前に「栞」を含むチャンネルを作ってください）")
            return
        # 週の文字列を鍵にするので、同じ週に二度投稿することはない
        text = random.choice(MONDAY_POSTS)
        await ch.send(text)
        self.state["last_post"] = iso_week(today)
        save_state(self.state)
        print(f"栞：月曜の投稿をしました（{iso_week(today)}）")

    # ---- ② 書いてくれた人に返す ----
    async def on_entry(self, message):
        """栞チャンネルへの書き込みを受け取る。必ず1件返す。"""
        uid = str(message.author.id)
        self.state["last_entry"][uid] = iso_week(today_jst())
        save_state(self.state)

        text = (message.content or "").strip()
        if not text:
            return
        reply = None
        try:
            import asyncio
            async with message.channel.typing():
                reply = await asyncio.to_thread(
                    self.ask_ai, REPLY_PROMPT.format(text=text[:500]))
        except Exception as e:
            print("栞の返事づくりに失敗:", repr(e)[:200])
        # AIが長文やエスカレーション文を返した時は、定型に落とす。
        # ここは「短くあたたかく」が絶対条件なので、長い返事は事故と見なす。
        if not reply or len(reply) > 160 or "自動応答です" in reply:
            reply = random.choice(FALLBACK_REPLIES)
        await message.reply(reply, mention_author=False)

    # ---- ③ 2週サイレントの方へ、そっとDM ----
    def _dm_targets(self, today: dt.date):
        now_w = iso_week(today)
        out = []
        for g in self.client.guilds:
            if self.guild_id and g.id != self.guild_id:
                continue
            for m in g.members:
                if m.bot:
                    continue
                roles = [r.name for r in getattr(m, "roles", [])]
                if any(r in EXCLUDE_ROLES for r in roles):
                    continue
                if not any(r in roles for r in TARGET_ROLES):
                    continue
                # 入りたての方には送らない
                joined = getattr(m, "joined_at", None)
                if joined and (today - joined.date()).days < JOIN_GRACE_DAYS:
                    continue
                uid = str(m.id)
                last = self.state["last_entry"].get(uid)
                if last and weeks_between(last, now_w) < SILENT_WEEKS:
                    continue
                prev_dm = self.state["last_dm"].get(uid)
                if prev_dm and weeks_between(prev_dm, now_w) < DM_COOLDOWN_WEEKS:
                    continue          # 一度声をかけた人を、追いかけない
                out.append(m)
        return out

    async def send_quiet_dms(self, today: dt.date):
        now_w = iso_week(today)
        sent = 0
        for m in self._dm_targets(today):
            body = (
                f"{m.display_name} さん、こんにちは。らくらくAIキャンパスです。\n\n"
                "お変わりないですか。\n"
                "急かすつもりは、まったくありません。ご都合のいい時で大丈夫です。\n\n"
                "もし「どこから戻ればいいか分からない」ということでしたら、\n"
                "そのままこのメッセージに返信してくださっても大丈夫です。\n\n"
                "またお会いできるのを、楽しみにしています🌸"
            )
            try:
                await m.send(body)
                self.state["last_dm"][str(m.id)] = now_w
                sent += 1
            except discord.Forbidden:
                pass                    # DMを閉じている方。追わない
            except Exception as e:
                print("DM失敗:", m.display_name, repr(e)[:120])
        save_state(self.state)
        # ⚠️ 件数はログにだけ出す。Discordには**絶対に**出さない
        print(f"栞：そっとDM {sent}件（{now_w}）")


def setup(client, ask_ai, guild_id=None) -> Shiori:
    """ai_support_bot から呼ぶ。毎時見にいって、月曜の朝だけ動く。"""
    sh = Shiori(client, ask_ai, guild_id)

    @tasks.loop(minutes=30)
    async def beat():
        await client.wait_until_ready()
        now = now_jst()
        today = now.date()
        if sh.state.get("last_post") == iso_week(today):
            return                       # その週はもう投稿済み
        if now.weekday() != POST_WEEKDAY or now.hour < POST_HOUR:
            return
        # PCが寝ていて7時を逃しても、月曜のうちに開けば、その週ぶんを出す。
        # 火曜以降には持ち越さない（「今週の栞」なので、週の頭に出ないと意味がうすい）
        if now.hour >= CATCHUP_UNTIL:
            return
        await sh.post_monday(today)
        await sh.send_quiet_dms(today)

    beat.start()
    return sh
