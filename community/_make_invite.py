# -*- coding: utf-8 -*-
"""_make_invite.py — 「ようこそ」チャンネルへの、期限なし招待リンクを作る。"""
import os, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def env(n):
    for l in open(os.path.join(ROOT, ".env"), encoding="utf-8"):
        if l.startswith(n + "="):
            return l.split("=", 1)[1].strip().strip('"').strip("'")

import discord
client = discord.Client(intents=discord.Intents.default())

@client.event
async def on_ready():
    try:
        g = client.get_guild(int(env("DISCORD_GUILD_ID")))
        ch = discord.utils.get(g.text_channels, name="ようこそ")
        if ch is None:
            print("❌ ようこそチャンネルが見つかりません"); return
        # 既存の期限なし招待があれば、それを使い回す
        for inv in await g.invites():
            if inv.max_age == 0 and inv.max_uses == 0:
                print(f"既存の招待リンク：{inv.url}"); return
        inv = await ch.create_invite(max_age=0, max_uses=0, unique=False,
                                     reason="1期生の受け入れ")
        print(f"作りました：{inv.url}")
    finally:
        await client.close()

client.run(env("DISCORD_BOT_TOKEN"), log_handler=None)
