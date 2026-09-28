# -*- coding: utf-8 -*-
"""
_make_invites.py — 期・プランごとに、別々の招待リンクを作る。

  python _make_invites.py --list     # いまある招待を見るだけ（作らない）
  python _make_invites.py            # 下の INVITES を、足りないぶんだけ作る

■ なぜ分けるか
  Discordは「どの招待リンクから何人入ったか」だけを数える。**誰がどのプランか**は
  リンクを分けておかないと、あとから分からない。
  2期生は1年プランと生涯プランがあるので、入口を2本に分ける。

■ どのリンクが何なのかは、Discord側には残らない
  作成理由（reason）は監査ログに残るが、招待一覧には出てこない。
  そこで **_invites.json に対応表を持つ**。この台帳が本体だと思って扱うこと。

■ 設定
  期限なし・回数無制限。会員サイトとステップメールに載せて配るため。
  ⚠️ リンクを知っている人は誰でも入れる。**受講者以外に渡らない場所にだけ**貼ること。
  漏れたら、Discordの「サーバー設定 → 招待」から、その1本だけ取り消せる。
  分けてあるので、1本消しても他のプランの方には影響しない。
"""
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HERE = os.path.dirname(os.path.abspath(__file__))
LEDGER = os.path.join(HERE, "_invites.json")
LIST_ONLY = "--list" in sys.argv

# 作るリンク（キー＝台帳の名前）
INVITES = {
    "2期生_1年プラン": "2期生・1年プランの方の入口（2026/8 説明会）",
    "2期生_生涯プラン": "2期生・生涯プランの方の入口（2026/8 説明会）",
}


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


def load():
    if os.path.exists(LEDGER):
        return json.load(open(LEDGER, encoding="utf-8"))
    return {}


def save(d):
    json.dump(d, open(LEDGER, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


@client.event
async def on_ready():
    try:
        gid = env("DISCORD_GUILD_ID")
        g = client.get_guild(int(gid)) if gid else (client.guilds[0] if client.guilds else None)
        if g is None:
            print("❌ サーバーが見つかりません")
            return
        print(f"サーバー：{g.name}\n")

        invites = await g.invites()
        alive = {i.url: i for i in invites}
        led = load()

        print(f"■ いまある招待 {len(invites)}本")
        rev = {v: k for k, v in led.items()}
        for i in invites:
            age = "期限なし" if i.max_age == 0 else f"{i.max_age}秒"
            use = "無制限" if i.max_uses == 0 else f"{i.max_uses}回まで"
            name = rev.get(i.url, "（台帳になし）")
            print(f"  {i.url}  #{getattr(i.channel,'name','?')}  {age}／{use}／使用 {i.uses}回  ← {name}")

        if LIST_ONLY:
            return

        ch = (discord.utils.get(g.text_channels, name="ようこそ")
              or discord.utils.get(g.text_channels, name="一般")
              or g.system_channel
              or (g.text_channels[0] if g.text_channels else None))
        if ch is None:
            print("❌ 招待を作れるチャンネルがありません")
            return

        print()
        for key, reason in INVITES.items():
            if key in led and led[key] in alive:
                print(f"  ⏭ {key}：すでにあります {led[key]}")
                continue
            inv = await ch.create_invite(max_age=0, max_uses=0, unique=True, reason=reason)
            led[key] = inv.url
            print(f"  ✅ {key}：作りました {inv.url}")
        save(led)

        print(f"\n入口チャンネル：#{ch.name}／期限なし／回数無制限")
        print(f"対応表：{os.path.basename(LEDGER)}")
    finally:
        await client.close()


client.run(env("DISCORD_BOT_TOKEN"), log_handler=None)
