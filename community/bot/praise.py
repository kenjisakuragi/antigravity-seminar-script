# -*- coding: utf-8 -*-
"""
praise.py — 「今週の good job」の材料を、毎週日曜に桜木さんへDMする。

■ 何のためのものか（2026-08-25・認定講師 制度設計 v5）
  認定講師6名には、サブスクを無料にするかわりに
  「Discordで、気づいたときに一言」をお願いしています。

  ただ——**サブスク無料は、2ヶ月で「もらって当たり前」になります。**
  効きつづけるのは、**毎週ちゃんと見て、名前を呼ぶこと**のほうです。

  なので、毎週日曜の夜に、材料をお届けします。

■ ⚠️ いちばん大事な設計判断：件数を、全体に出さないこと

  実測すると、6名の投稿数はこうでした（直近30日・2026-08-25）。

      ゆず60 ／ a子55 ／ しの54 ／ Yamaka42 ／ ゆきち5 ／ のりえ5

  **上と下で11倍あります。**
  これを毎週ならべて全体に出すと、下のお二人は**毎週いちばん下に並びます。年52回。**
  ホメるつもりが、いちばんよく効く退会装置になります。

  しかも——のりえさんは「今週の栞」に3件書いておられます。
  栞は全部で28件しかないチャンネルなので、**実は主力**です。
  **総数で数えると、この方の貢献が消えます。**

  だから、こう分けます。

  | どこ | 何を |
  |---|---|
  | **このDM（桜木さんだけ）** | 件数も、引用候補も、ぜんぶ |
  | **全体（#認定講師・グルコン）** | **数字なし。よかった一言を、そのまま引用して褒める** |

■ ⚠️ 選ぶのは、桜木さんです
  botは**候補を並べるだけ**。AIに選ばせません。
  「今週、誰を引き上げたいか」——ここが、この仕組みでいちばん大事なところで、
  そこはAIには分かりません。

■ 使い方
  ・毎週日曜 20時ごろ、DMが届きます
  ・全体に出したら、`!good お名前` と打ってください（誰を選んだか、覚えます）
  ・`!praise` で、いつでも今週ぶんを取り寄せられます
"""
import datetime as dt
import json
import os
import re

import discord
from discord.ext import tasks

HERE = os.path.dirname(os.path.abspath(__file__))
STATE_DIR = os.environ.get("RAKURAKU_STATE_DIR", HERE)
os.makedirs(STATE_DIR, exist_ok=True)
STATE_PATH = os.path.join(STATE_DIR, "_praise_state.json")

# ===== 設定 =====
POST_WEEKDAY = 6          # 日曜
POST_HOUR = 20            # 20時台に送る
CATCHUP_UNTIL = 23        # 日曜のうちなら、遅れても送る
DAYS = 7                  # 何日ぶんを見るか
TEACHER_ROLES = ["認定講師", "1期生"]   # 認定講師ロールが無ければ1期生で代用
FETCH_PER_CHANNEL = 100   # 1チャンネルあたり、さかのぼる件数
NOT_PICKED_WEEKS = 4      # 何週えらばれていないと、印を付けるか
MIN_QUOTE_LEN = 12        # 引用候補にする、最短の文字数

# 材料にしないチャンネル（運営用・自動投稿）
SKIP_CHANNELS = ["お知らせ", "グルコン資料置場", "aiニュース", "ルール", "はじめに"]

JST = dt.timezone(dt.timedelta(hours=9))


def now_jst():
    return dt.datetime.now(JST)


def iso_week(d):
    y, w, _ = d.isocalendar()
    return f"{y}-W{w:02d}"


def load_state():
    if os.path.exists(STATE_PATH):
        try:
            return json.load(open(STATE_PATH, encoding="utf-8"))
        except Exception:
            pass
    return {"last_sent": None, "picked": {}}      # picked: 名前 -> [週, 週, …]


def save_state(s):
    json.dump(s, open(STATE_PATH, "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)


def is_teacher(member) -> bool:
    roles = [r.name for r in getattr(member, "roles", [])]
    return any(r in TEACHER_ROLES for r in roles)


# ===== 引用候補の見つけ方 =====
# ⚠️ ここが、この仕組みの質を決めます。
#    「自分の報告」ではなく、**人に向けた一言**を拾いたい。
#    前者はご自身の記録。後者が、他の方を動かしているものです。
REACT_WORDS = [
    "さん", "ですね", "ください", "でしょうか", "わかります", "分かります",
    "私も", "わたしも", "おめでとう", "すごい", "素敵", "ナイス",
    "大丈夫", "できます", "やってみて", "ありがとう", "がんばって",
    "頑張って", "いいですね", "良いですね", "そこ", "参考",
]


def quote_score(msg, prev_author_id):
    """人に向けた一言ほど、高い点にする。0なら候補にしない。"""
    body = (msg.content or "").strip()
    if len(body) < MIN_QUOTE_LEN:
        return 0
    if body.startswith(("!", "/")):
        return 0
    score = 0
    if msg.reference is not None:            # 誰かの投稿への返信
        score += 5
    if msg.mentions:                          # 誰かへのメンション
        score += 4
    if prev_author_id and prev_author_id != msg.author.id:
        score += 2                            # 直前が別の人＝反応している可能性
    score += sum(1 for w in REACT_WORDS if w in body)
    return score


def clean(body, limit=110):
    body = re.sub(r"<@!?\d+>", "", body)      # メンションのIDを消す
    body = re.sub(r"https?://\S+", "（リンク）", body)
    body = " ".join(body.split())
    return body[:limit] + ("…" if len(body) > limit else "")


class Praise:
    def __init__(self, client, guild_id=None):
        self.client = client
        self.guild_id = guild_id
        self.state = load_state()

    def _guild(self):
        for g in self.client.guilds:
            if self.guild_id and g.id != self.guild_id:
                continue
            return g
        return None

    async def collect(self, days=DAYS):
        """直近◯日ぶんを集める。件数と、引用候補。"""
        g = self._guild()
        if g is None:
            return None
        since = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=days)

        teachers = {m.id: m.display_name for m in g.members
                    if not m.bot and is_teacher(m)}
        counts = {n: {} for n in teachers.values()}
        quotes = []

        for ch in g.text_channels:
            if any(k in ch.name for k in SKIP_CHANNELS):
                continue
            try:
                msgs = [m async for m in ch.history(limit=FETCH_PER_CHANNEL, after=since)]
            except (discord.Forbidden, discord.HTTPException):
                continue
            msgs.sort(key=lambda m: m.created_at)
            prev = None
            for m in msgs:
                if m.author.bot:
                    prev = None
                    continue
                if m.author.id in teachers:
                    nm = teachers[m.author.id]
                    counts[nm][ch.name] = counts[nm].get(ch.name, 0) + 1
                    s = quote_score(m, prev)
                    if s > 0:
                        quotes.append((s, nm, ch.name, clean(m.content or "")))
                prev = m.author.id

        quotes.sort(key=lambda x: -x[0])
        return {"teachers": sorted(teachers.values()), "counts": counts,
                "quotes": quotes}

    def _weeks_since_picked(self, name, this_week):
        got = self.state["picked"].get(name, [])
        if not got:
            return 99
        try:
            last = max(got)
            ly, lw = int(last[:4]), int(last[6:])
            ty, tw = int(this_week[:4]), int(this_week[6:])
            return (ty - ly) * 52 + (tw - lw)
        except Exception:
            return 99

    async def build_report(self):
        data = await self.collect()
        if data is None:
            return "サーバーが見つかりませんでした。"
        wk = iso_week(now_jst().date())
        counts, quotes = data["counts"], data["quotes"]

        L = ["🌸 **今週の good job ── 材料をお届けします**",
             f"（{DAYS}日ぶん／このDMは桜木さんだけに届いています）", ""]

        # ── ① まだ選ばれていない方（いちばん上に置く。ここを見てほしいので）
        waiting = [n for n in data["teachers"]
                   if self._weeks_since_picked(n, wk) >= NOT_PICKED_WEEKS
                   and sum(counts.get(n, {}).values()) > 0]
        if waiting:
            L += ["**▼ しばらく選ばれていない方**（書いてはくださっています）",
                  "　" + "／".join(waiting),
                  "　→ この中に良い一言があれば、**そちらを優先**してください。", ""]

        # ── ② 引用の候補
        L.append("**▼ 引用の候補**（人に向けた一言を、上から）")
        if not quotes:
            L.append("　今週は、拾えるものがありませんでした。")
        else:
            seen, shown = set(), 0
            for _, nm, ch, body in quotes:
                if nm in seen:                 # 同じ人ばかりにしない
                    continue
                seen.add(nm)
                mark = "　⭐" if nm in waiting else "　・"
                L.append(f"{mark} **{nm}**（#{ch}）")
                L.append(f"　　「{body}」")
                shown += 1
                if shown >= 5:
                    break
        L.append("")

        # ── ③ 件数（桜木さんの手元だけ）
        L.append("**▼ 今週の件数**　⚠️ **全体には出さないでください**")
        rows = sorted(counts.items(), key=lambda x: -sum(x[1].values()))
        for nm, ch in rows:
            tot = sum(ch.values())
            top = "、".join(f"{c}{n}" for c, n in
                            sorted(ch.items(), key=lambda x: -x[1])[:3])
            L.append(f"　{nm}　{tot}件　{top or '—'}")
        L += ["",
              "──────────",
              "全体に出したら、**`!good お名前`** と打ってください（次回の材料に反映します）。"]
        return "\n".join(L)

    async def send(self, force=False):
        g = self._guild()
        if g is None or g.owner is None:
            print("praise: 送り先が見つかりません")
            return False
        wk = iso_week(now_jst().date())
        if not force and self.state.get("last_sent") == wk:
            return False
        text = await self.build_report()
        for i in range(0, len(text), 1900):
            await g.owner.send(text[i:i + 1900])
        if not force:
            self.state["last_sent"] = wk
            save_state(self.state)
        return True

    def record_pick(self, name):
        """全体に出した方を覚える。次回、同じ人ばかりにならないように。"""
        wk = iso_week(now_jst().date())
        got = self.state["picked"].setdefault(name, [])
        if wk not in got:
            got.append(wk)
        self.state["picked"][name] = got[-12:]
        save_state(self.state)


def setup(client, guild_id=None) -> Praise:
    p = Praise(client, guild_id)

    @tasks.loop(minutes=20)
    async def beat():
        await client.wait_until_ready()
        now = now_jst()
        if now.weekday() != POST_WEEKDAY:
            return
        if not (POST_HOUR <= now.hour < CATCHUP_UNTIL):
            return
        try:
            await p.send()
        except Exception as e:
            print("praise: 週次レポートで失敗", repr(e)[:160])

    beat.start()
    return p
