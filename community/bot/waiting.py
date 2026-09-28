# -*- coding: utf-8 -*-
"""
waiting.py — 「待ってから出る」。

■ なぜ待つのか
  botが1分で答えると、認定講師と仲間が話す前に会話が終わる。
  特典③は「認定講師が、並んで歩きます」なので、**人が先に出ない設計は特典を壊す**。
  受講生から見ても「結局AIが答えるなら、講師って何？」になる。

■ どう待つか
  1. 呼ばれた（@メンション）ときは、待たずに即答する
  2. 呼ばれていないときは、決められた分だけ待つ
  3. 待っているあいだに**人が反応していたら、黙る**
  4. 誰も反応しなかったときだけ、そっと出る

  栞のメールにある「必ず誰かがお返事します」は、この形でも守られる。
  人が答えれば、それが「誰か」。誰も答えなければbotが出るので、無視は起きない。

■ 黙る条件（どれか1つでも当てはまれば、出ない）
  ・本人以外の**人**が、そのあとに発言している
  ・誰かがその投稿に**返信**している
  ・誰かが**スタンプ**を付けている（見たよ、の合図として扱う）
  ・本文が短すぎる（「ありがとう」等の相づち）
  ・そのチャンネルで、今日もう上限まで話した

■ 夜は待たない
  22時〜翌8時は即答。一人で困っている人を、朝まで放置しないため。

■ 再起動したら
  待っている途中の予定は消える。**起動時に取りこぼしを拾い直す**（catch_up）。
"""
import asyncio
import datetime as dt
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import config

JST = dt.timezone(dt.timedelta(hours=9))

# 今日そのチャンネルで何回話したか（{チャンネルID: [日付, 回数]}）
_spoken = {}
# 待っている最中のメッセージID（二重に予約しないため）
_pending = set()


def is_night(now=None) -> bool:
    h = (now or dt.datetime.now(JST)).hour
    return h >= config.NIGHT_FROM or h < config.NIGHT_TO


def too_short(text: str) -> bool:
    """答えなくてよい発言か。

    ⚠️ 2026-08-20：長さだけで切っていたので、
    　　「どこですか？」のような**短い追い質問まで捨てていた**。
    　　長さの線を下げたうえで、あいさつ・相づちは別に名指しで外す。
    """
    s = text.strip().rstrip("!！。．､、 ")
    if s in getattr(config, "IGNORE_EXACT", []):
        return True
    # 「？」で終わるなら、短くても質問。拾う
    if s.endswith(("?", "？")):
        return False
    return len(s) < config.MIN_LEN_TO_ANSWER


def _quota_left(channel) -> bool:
    today = dt.datetime.now(JST).date().isoformat()
    d, n = _spoken.get(channel.id, (today, 0))
    if d != today:
        d, n = today, 0
    return n < config.DAILY_LIMIT_PER_CHANNEL


def _count(channel):
    today = dt.datetime.now(JST).date().isoformat()
    d, n = _spoken.get(channel.id, (today, 0))
    if d != today:
        d, n = today, 0
    _spoken[channel.id] = (d, n + 1)


async def answered_by_human(client, message) -> bool:
    """その投稿のあとに、人が反応したか。"""
    # スタンプが付いていたら、誰かが見ている
    try:
        fresh = await message.channel.fetch_message(message.id)
        if any(r.count > 0 for r in fresh.reactions):
            return True
    except Exception:
        pass
    # そのあとに、本人でも bot でもない人が話していたら
    try:
        async for m in message.channel.history(after=message, limit=30):
            if m.author.bot:
                continue
            if m.author.id != message.author.id:
                return True
    except Exception:
        pass
    return False


async def maybe_answer_later(client, message, wait_min, respond):
    """待ってから、誰も答えていなければ respond(message) を呼ぶ。

    respond は「実際に返事をする」処理。呼び出し側から渡す。"""
    if message.id in _pending:
        return
    text = (message.content or "").strip()
    if too_short(text):
        return
    if not _quota_left(message.channel):
        print(f"  今日の上限に達したので黙ります（#{message.channel}）")
        return

    wait = 0 if is_night() else wait_min * 60
    if wait:
        _pending.add(message.id)
        try:
            await asyncio.sleep(wait)
            if await answered_by_human(client, message):
                print(f"  人が先に反応したので黙ります（#{message.channel}）")
                return
        finally:
            _pending.discard(message.id)

    if not _quota_left(message.channel):
        return
    _count(message.channel)
    await respond(message)


async def catch_up(client, channels, wait_min, respond, look_back_min=180):
    """再起動で消えた予定を拾い直す。
    待ち時間を過ぎていて、まだ誰も答えていないものだけ答える。"""
    now = dt.datetime.now(dt.timezone.utc)
    for ch in channels:
        try:
            async for m in ch.history(limit=40):
                age = (now - m.created_at).total_seconds() / 60
                if age > look_back_min:
                    break
                if m.author.bot or age < wait_min:
                    continue
                if too_short((m.content or "").strip()):
                    continue
                if await answered_by_human(client, m):
                    continue
                if not _quota_left(ch):
                    break
                _count(ch)
                print(f"  取りこぼしに答えます（#{ch} / {age:.0f}分前）")
                await respond(m)
        except Exception as e:
            print("拾い直しに失敗:", repr(e)[:160])
