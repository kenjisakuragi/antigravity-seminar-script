# -*- coding: utf-8 -*-
"""
usage.py — AIさくらぎが使ったAPI費用を、自分で記録して見張る。

なぜ自前でやるか
  OpenAIの請求APIは**管理者用の鍵（sk-admin-）**が要る。
  botが持っている普通の鍵では 403 で読めない（実際に試して確認）。
  なので、呼んだそばから自分で数えて、日ごとにためておく。

記録するもの（`_usage.json`）
  日付ごとに { 入力トークン, キャッシュ入力, 出力トークン, 呼んだ回数 }
  ⚠️ 質問の中身は**一切保存しない**。数だけ。

見方
  Discordで `!cost` と打つ（運営・認定講師のみ）。今月と今週の概算が返る。

見張り
  1ヶ月の見込みが THRESHOLD_USD を超えたら、桜木さんにDMで1回だけ知らせる。
  超えっぱなしのあいだ何度も言わないよう、月に1回に抑える。
"""
import os
import json
import datetime as dt

HERE = os.path.dirname(os.path.abspath(__file__))
# 記録は**コードとは別の場所**に置く。
# setup.sh は入れ直しのたびにコード一式を消して置き直すので、
# コードと同じ場所に置くと**記録ごと消える**（実際に消えて、栞が二重投稿された）。
STATE_DIR = os.environ.get("RAKURAKU_STATE_DIR", HERE)
os.makedirs(STATE_DIR, exist_ok=True)
PATH = os.path.join(STATE_DIR, "_usage.json")

JST = dt.timezone(dt.timedelta(hours=9))

# 1Mトークンあたりのドル単価（2026/8/3 時点・公式の料金表より）
# モデルを変えたら、ここも直すこと。
PRICES = {
    "gpt-5.4-mini": {"in": 0.75, "cached": 0.075, "out": 4.50},
    "gpt-5.4-nano": {"in": 0.20, "cached": 0.02, "out": 1.25},
}

USD_JPY = 155          # 概算用。厳密な請求額ではない
THRESHOLD_USD = 20.0   # 1ヶ月の見込みがこれを超えたら知らせる


def _load() -> dict:
    if os.path.exists(PATH):
        try:
            return json.load(open(PATH, encoding="utf-8"))
        except Exception:
            pass
    return {"days": {}, "alerted_month": None}


def _save(d: dict):
    json.dump(d, open(PATH, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def record(model: str, usage) -> None:
    """1回呼ぶたびに数える。usage は OpenAI の response.usage。"""
    if usage is None:
        return
    cached = 0
    det = getattr(usage, "prompt_tokens_details", None)
    if det is not None:
        cached = getattr(det, "cached_tokens", 0) or 0
    pin = (getattr(usage, "prompt_tokens", 0) or 0) - cached
    out = getattr(usage, "completion_tokens", 0) or 0

    d = _load()
    key = dt.datetime.now(JST).date().isoformat()
    row = d["days"].setdefault(key, {"in": 0, "cached": 0, "out": 0, "calls": 0, "model": model})
    row["in"] += pin
    row["cached"] += cached
    row["out"] += out
    row["calls"] += 1
    row["model"] = model
    # 古い日は落とす（100日ぶんあれば十分）
    if len(d["days"]) > 100:
        for k in sorted(d["days"])[:-100]:
            d["days"].pop(k, None)
    _save(d)


def _cost(row: dict) -> float:
    p = PRICES.get(row.get("model", ""), PRICES["gpt-5.4-mini"])
    return (row["in"] * p["in"] + row["cached"] * p["cached"] + row["out"] * p["out"]) / 1_000_000


def summary() -> dict:
    """今月・今週・今日の概算をまとめる。"""
    d = _load()
    today = dt.datetime.now(JST).date()
    monday = today - dt.timedelta(days=today.weekday())
    month = today.strftime("%Y-%m")

    acc = {"month": 0.0, "week": 0.0, "today": 0.0,
           "month_calls": 0, "week_calls": 0, "today_calls": 0}
    for k, row in d["days"].items():
        c = _cost(row)
        day = dt.date.fromisoformat(k)
        if k.startswith(month):
            acc["month"] += c; acc["month_calls"] += row["calls"]
        if day >= monday:
            acc["week"] += c; acc["week_calls"] += row["calls"]
        if day == today:
            acc["today"] += c; acc["today_calls"] += row["calls"]

    # 今月の見込み＝いまのペースが月末まで続いたら
    dim = (today.replace(day=28) + dt.timedelta(days=4)).replace(day=1) - dt.timedelta(days=1)
    acc["forecast"] = acc["month"] / today.day * dim.day if today.day else 0.0
    acc["model"] = next((r.get("model") for r in reversed(list(d["days"].values()))),
                        "gpt-5.4-mini")
    return acc


def report() -> str:
    """Discordに出す文面。"""
    s = summary()
    def y(u): return f"約{u * USD_JPY:,.0f}円（${u:.2f}）"
    return (
        f"**AIさくらぎの利用状況**（モデル：{s['model']}）\n"
        f"```\n"
        f"今日   {y(s['today']):<24} {s['today_calls']:>4}回\n"
        f"今週   {y(s['week']):<24} {s['week_calls']:>4}回\n"
        f"今月   {y(s['month']):<24} {s['month_calls']:>4}回\n"
        f"月末見込み {y(s['forecast'])}\n"
        f"```\n"
        f"※ 1ドル{USD_JPY}円で計算した概算です。正確な請求額はOpenAIの画面をご確認ください。"
    )


def over_threshold() -> str | None:
    """見込みがしきい値を超えていたら、知らせる文面を返す。月1回だけ。"""
    s = summary()
    if s["forecast"] < THRESHOLD_USD:
        return None
    d = _load()
    month = dt.datetime.now(JST).date().strftime("%Y-%m")
    if d.get("alerted_month") == month:
        return None                      # 今月はもう言った。何度も言わない
    d["alerted_month"] = month
    _save(d)
    return (
        f"⚠️ **AIさくらぎの費用が、いつもより多めです**\n\n"
        f"今月の見込み：約{s['forecast'] * USD_JPY:,.0f}円"
        f"（${s['forecast']:.2f}）／{s['month_calls']}回\n\n"
        f"質問が増えているだけなら、いいことです。\n"
        f"抑えたい場合は、モデルを `gpt-5.4-nano` に下げる手があります（費用は約1/4）。\n"
        f"`!cost` で、いつでも内訳を見られます。"
    )


# ────────────────────────────────────────────────
# 1日の上限（2026-09-27 追加）
#
# なぜ足したか
#   それまでの見張りは「月の見込みが $20 を超えたらDMする」だけだった。
#   問題が2つあった。
#     ① 知らせるだけで、**止めない**。DMが届くころには使い終わっている
#     ② 判定が月単位なので、1日で暴走しても月の見込みが超えるまで気づかない
#   実績は9月で月92円（1日4.2円）。$20 はその33倍で、見張りとして働いていなかった。
#
#   なので「その日ぶんを使い切ったら、もう呼ばない」という硬い止め方を入れる。
#   上限は環境変数で変えられる。既定は1日100円（実績の約24倍＝十分な余裕）。
# ────────────────────────────────────────────────

DAILY_LIMIT_JPY = float(os.environ.get("RAKURAKU_DAILY_LIMIT_JPY", "100"))
DAILY_LIMIT_USD = DAILY_LIMIT_JPY / USD_JPY


def today_cost() -> float:
    """今日ぶんの概算（ドル）。"""
    d = _load()
    key = dt.datetime.now(JST).date().isoformat()
    row = d["days"].get(key)
    return _cost(row) if row else 0.0


def over_daily_limit() -> bool:
    """今日ぶんを使い切ったか。ask_ai はこれを見て、呼ぶ前に引き返す。"""
    return today_cost() >= DAILY_LIMIT_USD


def daily_alert() -> str | None:
    """上限に達した日、**1日1回だけ**知らせる文面を返す。

    over_threshold（月）とは別枠。こちらは「もう止めました」の報告なので、
    黙っていると桜木さんが気づけない。だが何度も言うと読まれなくなる。
    """
    if not over_daily_limit():
        return None
    d = _load()
    key = dt.datetime.now(JST).date().isoformat()
    if d.get("alerted_day") == key:
        return None                      # 今日はもう言った
    d["alerted_day"] = key
    _save(d)
    c = today_cost()
    return (
        f"🛑 **AIさくらぎを、今日はここで止めました**\n\n"
        f"今日ぶん：約{c * USD_JPY:,.0f}円（${c:.2f}）\n"
        f"1日の上限：約{DAILY_LIMIT_JPY:,.0f}円\n\n"
        f"質問には「明日また聞いてくださいね」とお返ししています。\n"
        f"日付が変わればひとりでに戻ります。**何もしなくて大丈夫です**。\n\n"
        f"急いで上げたいときは、サーバーの `RAKURAKU_DAILY_LIMIT_JPY` を\n"
        f"書き換えて入れ直してください。`!cost` で内訳が見られます。"
    )


# 上限に達した日に、受講生へお返しする文面。
# ここで会話を終わらせず、**人にパスする**のが大事。
# 「もう答えません」で切ると、聞きにくい空気がそのまま残る。
DAILY_LIMIT_REPLY = (
    "申し訳ありません。今日はここまでにさせてください🙏\n"
    "日付が変わりましたら、また聞いてくださいね🌸\n\n"
    "お急ぎのときは、そのままチャンネルに書いてください。桜木が直接お答えします。"
)
