# -*- coding: utf-8 -*-
"""Discordの投稿を、期間を区切って読み出す（読み取り専用・何も投稿しない）。2026-09-14

  ENV_PATH=/opt/rakuraku-bot/community/.env python _read_discord_period.py 2026-08-24T21:30 2026-09-14T23:59 出力.json

  ・AIさくらぎ本体と同じ discord.py で、REST だけ使う（ゲートウェイには接続しない）
    → 動いているボット本体の接続とは干渉しない
  ・チャンネルとスレッドの投稿、リアクション数、返信数、添付の有無を集める
  ・結果は手元のJSONに書くだけ。外へは送らない
"""
import asyncio, datetime as dt, json, os, sys

import discord

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))

env = {}
ENV_PATH = os.environ.get("ENV_PATH") or os.path.join(HERE, ".env")
for ln in open(ENV_PATH, encoding="utf-8"):
    ln = ln.strip()
    if "=" in ln and not ln.startswith("#"):
        k, v = ln.split("=", 1)
        env[k.strip()] = v.strip().strip('"').strip("'")
TOKEN = env["DISCORD_BOT_TOKEN"]

JST = dt.timezone(dt.timedelta(hours=9))
since = dt.datetime.fromisoformat(sys.argv[1]).replace(tzinfo=JST)
until = dt.datetime.fromisoformat(sys.argv[2]).replace(tzinfo=JST)
OUT = sys.argv[3]


async def main():
    client = discord.Client(intents=discord.Intents.none())
    await client.login(TOKEN)                      # RESTのみ。gatewayには繋がない
    try:
        guilds = [g async for g in client.fetch_guilds(limit=10)]
        guild = await client.fetch_guild(guilds[0].id)
        chans = await guild.fetch_channels()
        texts = [c for c in chans if isinstance(c, (discord.TextChannel, discord.ForumChannel))]

        targets = []
        for c in texts:
            if isinstance(c, discord.TextChannel):
                targets.append((c, c.name, None))
        # スレッド（進行中＋アーカイブ済みの公開スレッド）
        seen = set()
        try:
            for t in await guild.active_threads():
                if t.id not in seen:
                    seen.add(t.id); targets.append((t, t.parent.name if t.parent else "?", t.name))
        except discord.HTTPException:
            pass
        for c in texts:
            try:
                async for t in c.archived_threads(limit=100):
                    if t.id not in seen:
                        seen.add(t.id); targets.append((t, c.name, t.name))
            except (discord.Forbidden, discord.HTTPException):
                pass

        msgs = []
        for ch, cname, tname in targets:
            try:
                async for m in ch.history(limit=None, after=since.astimezone(dt.timezone.utc),
                                          before=until.astimezone(dt.timezone.utc), oldest_first=True):
                    msgs.append({
                        "id": str(m.id), "channel": cname, "thread": tname, "channel_id": str(ch.id),
                        "time": m.created_at.astimezone(JST).strftime("%m/%d %H:%M"),
                        "author": m.author.display_name, "bot": m.author.bot,
                        "content": m.content,
                        "reactions": [(str(r.emoji), r.count) for r in m.reactions],
                        "attachments": len(m.attachments),
                        "reply_to": str(m.reference.message_id) if m.reference and m.reference.message_id else None,
                    })
            except (discord.Forbidden, discord.HTTPException):
                continue
    finally:
        await client.close()

    by_id = {m["id"]: m for m in msgs}
    for m in msgs:
        m["replies"] = 0
    for m in msgs:
        if m["reply_to"] in by_id:
            by_id[m["reply_to"]]["replies"] += 1

    json.dump({"guild": guild.name, "since": sys.argv[1], "until": sys.argv[2], "messages": msgs},
              open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    people = [m for m in msgs if not m["bot"]]
    print(f"読み出し：{len(msgs)}件（人の投稿 {len(people)}件・ボット {len(msgs)-len(people)}件）")
    per = {}
    for m in people:
        per[m["channel"]] = per.get(m["channel"], 0) + 1
    for k, v in sorted(per.items(), key=lambda x: -x[1]):
        print(f"  {v:4d}  #{k}")


asyncio.run(main())
