# -*- coding: utf-8 -*-
"""
_make_invite_2ki.py — 2期生用の招待リンクを作る（1期生のものとは別にする）。

  python _make_invite_2ki.py --list     # いまある招待を見るだけ（作らない）
  python _make_invite_2ki.py            # 2期生用を1本作る（すでにあれば、それを使う）

■ なぜ期別に分けるか
  Discordは「どの招待リンクから何人入ったか」を数えてくれる。
  1期生と同じリンクを配ると、**2期生が何人入ったのか分からなくなる**。

■ 設定
  期限なし・回数無制限。会員サイトとステップメールに載せて配るため。
  ⚠️ リンクを知っている人は誰でも入れる。**受講者以外に渡らない場所にだけ**貼ること。
  漏れたときは、Discordの「サーバー設定 → 招待」から、その1本だけ取り消せる。
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HERE = os.path.dirname(os.path.abspath(__file__))
LABEL = "2期生の受け入れ（2026/8 説明会）"
LIST_ONLY = "--list" in sys.argv


def env(n):
    # ⚠️ ルートの .env を先に読む。community/.env のトークンは**古くて401になる**（8/8に確認）。
    #    直すのは桜木さんの判断（本番BotはシンVPS側の .env を使っているため、ここは触らない）。
    for path in (os.path.join(ROOT, ".env"), os.path.join(HERE, ".env")):
        if not os.path.exists(path):
            continue
        for l in open(path, encoding="utf-8"):
            if l.startswith(n + "="):
                v = l.split("=", 1)[1].strip().strip('"').strip("'")
                if v:
                    return v
    return None


import discord  # noqa: E402

client = discord.Client(intents=discord.Intents.default())


@client.event
async def on_ready():
    try:
        gid = env("DISCORD_GUILD_ID")
        g = client.get_guild(int(gid)) if gid else (client.guilds[0] if client.guilds else None)
        if g is None:
            print("❌ サーバーが見つかりません")
            return
        print(f"サーバー：{g.name}")

        invites = await g.invites()
        print(f"いまある招待：{len(invites)}本")
        for inv in invites:
            age = "期限なし" if inv.max_age == 0 else f"{inv.max_age}秒"
            use = "無制限" if inv.max_uses == 0 else f"{inv.max_uses}回まで"
            print(f"  {inv.url}  ch=#{getattr(inv.channel,'name','?')}  {age}／{use}／使用 {inv.uses}回")

        if LIST_ONLY:
            return

        # すでに2期生用があれば、それを使う（毎回増やさない）
        for inv in invites:
            if (inv.max_age == 0 and inv.max_uses == 0
                    and getattr(inv, "revoked", False) is False
                    and inv.uses == 0 and inv.inviter == client.user):
                pass  # 判別できないので、下の台帳ファイルで見る

        led = os.path.join(HERE, "_invite_2ki.txt")
        if os.path.exists(led):
            url = open(led, encoding="utf-8").read().strip()
            if any(i.url == url for i in invites):
                print(f"\n✅ 2期生用は、すでにあります：{url}")
                return

        # 1期生の期限なし招待は #一般 に付いている。同じ入口にそろえる。
        ch = (discord.utils.get(g.text_channels, name="ようこそ")
              or discord.utils.get(g.text_channels, name="一般")
              or g.system_channel
              or (g.text_channels[0] if g.text_channels else None))
        if ch is None:
            print("❌ 招待を作れるチャンネルがありません")
            return

        inv = await ch.create_invite(max_age=0, max_uses=0, unique=True, reason=LABEL)
        open(led, "w", encoding="utf-8").write(inv.url + "\n")
        print(f"\n✅ 2期生用を作りました：{inv.url}")
        print(f"   入口チャンネル：#{ch.name}／期限なし／回数無制限")
        print(f"   記録：{os.path.basename(led)}")
    finally:
        await client.close()


client.run(env("DISCORD_BOT_TOKEN"), log_handler=None)
