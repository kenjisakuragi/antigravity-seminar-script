# -*- coding: utf-8 -*-
"""
feedback.py — AIさくらぎの答えが役に立ったかを、リアクションだけで集める。

■ なぜ作ったか（2026-09-28）
  いままで、botの答えが良かったのか外れたのかを知る手立てが無かった。
  `usage.py` は回数と費用しか残していない（これは正しい設計）。
  結果、「直したいが、どこを直せばいいか分からない」状態だった。

■ 何を保存するか — ここが設計の芯
  **質問も、回答も、一切保存しない。** 数だけ。
  保存するのは次の3つだけ。

    ・botが答えたメッセージのID（直近500件ぶん。中身は持たない）
    ・日ごとの 👍 と 🤔 の数
    ・日ごとの「答えた回数」

  中身を残せば改善は速くなる。が、受講生が書いたものを黙って溜めることになる。
  桜木さんの判断で**残さない**方を選んだ（2026-09-28）。
  だから分かるのは「どの回が外れたか」までで、「なぜ外れたか」は分からない。
  そこは、数字が出たあとにDiscordを直接見に行く。

■ どう動くか
  1. botが答えたら、その返信に 👍 と 🤔 を自分で付けておく
  2. 誰かが押したら、数える（押した人が誰かは記録しない）
  3. 取り消されたら、減らす
  4. `!fb` で、運営だけが内訳を見られる

■ 押してもらう文言について
  ⚠️ 「役に立ちましたか？」と毎回聞かない。聞かれると、押しづらくなる。
  　 スタンプが先に付いていて、押したい人だけ押す。これくらいがちょうどいい。
"""
import datetime as dt
import json
import os

GOOD = "👍"
HMM = "🤔"

HERE = os.path.dirname(os.path.abspath(__file__))
STATE_DIR = os.environ.get("RAKURAKU_STATE_DIR", HERE)
os.makedirs(STATE_DIR, exist_ok=True)
PATH = os.path.join(STATE_DIR, "_feedback_state.json")

KEEP_IDS = 500          # 覚えておくbot返信の数。古いものから落とす
JST = dt.timezone(dt.timedelta(hours=9))


def _today():
    return dt.datetime.now(JST).date().isoformat()


def _load() -> dict:
    if os.path.exists(PATH):
        try:
            d = json.load(open(PATH, encoding="utf-8"))
            d.setdefault("ids", [])
            d.setdefault("days", {})
            return d
        except Exception:
            pass
    return {"ids": [], "days": {}}


def _save(d: dict):
    json.dump(d, open(PATH, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def _row(d, key):
    return d["days"].setdefault(key, {"answered": 0, "good": 0, "hmm": 0})


def remember(message_id: int) -> None:
    """botが答えた、ということだけ覚える。中身は持たない。"""
    d = _load()
    d["ids"].append(int(message_id))
    if len(d["ids"]) > KEEP_IDS:
        d["ids"] = d["ids"][-KEEP_IDS:]
    _row(d, _today())["answered"] += 1
    _save(d)


def is_ours(message_id: int) -> bool:
    return int(message_id) in set(_load()["ids"])


def count(message_id: int, emoji: str, delta: int) -> bool:
    """押された／取り消されたを数える。数えたら True。"""
    if emoji not in (GOOD, HMM):
        return False
    d = _load()
    if int(message_id) not in set(d["ids"]):
        return False
    r = _row(d, _today())
    k = "good" if emoji == GOOD else "hmm"
    r[k] = max(0, r[k] + delta)
    _save(d)
    return True


def _sum(days):
    a = {"answered": 0, "good": 0, "hmm": 0}
    for r in days:
        for k in a:
            a[k] += r.get(k, 0)
    return a


def summary() -> dict:
    d = _load()
    today = dt.datetime.now(JST).date()
    monday = today - dt.timedelta(days=today.weekday())
    month = today.strftime("%Y-%m")

    week, mon, tod = [], [], []
    for k, r in d["days"].items():
        try:
            day = dt.date.fromisoformat(k)
        except Exception:
            continue
        if day >= monday:
            week.append(r)
        if k.startswith(month):
            mon.append(r)
        if day == today:
            tod.append(r)
    return {"today": _sum(tod), "week": _sum(week), "month": _sum(mon)}


def report() -> str:
    """Discordに出す文面。運営だけが見る。"""
    s = summary()

    def line(name, r):
        ans, g, h = r["answered"], r["good"], r["hmm"]
        total = g + h
        if ans == 0:
            return f"{name}　答えた回数 0"
        rate = f"{total / ans * 100:.0f}%" if ans else "—"
        mood = ""
        if total:
            mood = f"　うち 🤔 {h / total * 100:.0f}%"
        return (f"{name}　答え {ans:>3}回　👍 {g:>3}　🤔 {h:>3}"
                f"　（押された率 {rate}{mood}）")

    return (
        "**AIさくらぎの手ごたえ**\n"
        "```\n"
        f"{line('今日', s['today'])}\n"
        f"{line('今週', s['week'])}\n"
        f"{line('今月', s['month'])}\n"
        "```\n"
        "※ 押されない回のほうが多いのが普通です。**🤔 が付いた回だけ**、\n"
        "　 あとでチャンネルを見に行ってください。そこに直すところがあります。\n"
        "※ 質問と回答の中身は、保存していません。数だけです。"
    )


def setup(client):
    """ai_support_bot から呼ぶ。リアクションの受け口をつなぐ。"""

    @client.event
    async def on_raw_reaction_add(payload):
        try:
            if payload.user_id == client.user.id:
                return                      # bot が自分で付けた分は数えない
            count(payload.message_id, str(payload.emoji), +1)
        except Exception as e:
            print("リアクションの記録に失敗:", repr(e)[:120])

    @client.event
    async def on_raw_reaction_remove(payload):
        try:
            if payload.user_id == client.user.id:
                return
            count(payload.message_id, str(payload.emoji), -1)
        except Exception as e:
            print("リアクションの取り消しに失敗:", repr(e)[:120])

    print("手ごたえの記録：botの答えに 👍 🤔 を付けて、押された数だけ数えます")
    return True


async def attach(message):
    """botの返信に 👍 🤔 を付け、IDを覚える。失敗しても本体は止めない。"""
    try:
        remember(message.id)
        await message.add_reaction(GOOD)
        await message.add_reaction(HMM)
    except Exception as e:
        print("スタンプ付けに失敗:", repr(e)[:120])
