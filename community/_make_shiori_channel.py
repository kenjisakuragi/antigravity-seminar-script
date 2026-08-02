# -*- coding: utf-8 -*-
"""
_make_shiori_channel.py — 特典③「今週の栞」を置く部屋を作る。

  python community/_make_shiori_channel.py --plan   # 何をするか見るだけ
  python community/_make_shiori_channel.py          # 実際に作る

■ なぜ専用の部屋にするか
  「できた報告」に混ぜると、**作れた人の投稿だけが並ぶ**。
  栞は「今週はお休み」も置いていい場所なので、そこと分ける必要がある。

■ 部屋の名前
  bot（community/bot/shiori.py）は、名前に「栞」を含むチャンネルを探す。
  名前を変えるときは、あちらの CHANNEL_KEYS も合わせること。

■ 何度流しても大丈夫。すでにあれば飛ばす。
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

NAME = "📖今週の栞"
CAT = "💬 学びとサポート"
WHO = "受講生"
TOPIC = ("今週の栞に、一行だけ置いていく場所です。"
         "「今週はお休み」でも大丈夫。書かない週があっても、何も起きません。")

# 部屋を作ったら、最初に置いておく一言（空の部屋は書きこみにくい）
FIRST_POST = (
    "この部屋のことを、少しだけ。\n\n"
    "毎週月曜の朝、メールで「今週の栞」が届きます。\n"
    "200本の中から、**今週やることが1つだけ**。それだけです。\n\n"
    "やってみたら、ここに**一行だけ**置いていってください。\n"
    "「見ました」でも、「作ってみた」でも、「今週はお休み」でも。\n\n"
    "書いてくださったら、必ず、誰かがお返事します。\n"
    "書かない週があっても、何も起きません。急ぎませんので、あなたの速さで🌸"
)


def env(name):
    for line in open(os.path.join(ROOT, ".env"), encoding="utf-8"):
        if line.startswith(name + "="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    return None


def main():
    plan = "--plan" in sys.argv
    token, gid = env("DISCORD_BOT_TOKEN"), env("DISCORD_GUILD_ID")
    import discord
    intents = discord.Intents.default()
    intents.members = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        try:
            g = client.get_guild(int(gid))
            print(f"サーバー：{g.name}\n")
            names = {r.name: r for r in g.roles}
            chans = {c.name: c for c in g.channels}
            cats = {c.name: c for c in g.categories}

            if NAME in chans:
                print(f"  チャンネル {NAME} … すでにあります")
            elif plan:
                print(f"  チャンネル {NAME} … 作ります（{CAT} の中／{WHO}だけ見られる）")
            else:
                gate = names.get(WHO)
                if gate is None:
                    print(f"  ❌ ロール「{WHO}」がありません")
                    return
                ow = {
                    g.default_role: discord.PermissionOverwrite(view_channel=False),
                    gate: discord.PermissionOverwrite(view_channel=True,
                                                      send_messages=True),
                }
                for extra in ("運営", "認定講師"):
                    if extra in names:
                        ow[names[extra]] = discord.PermissionOverwrite(
                            view_channel=True, send_messages=True)
                c = await g.create_text_channel(
                    NAME, category=cats.get(CAT), topic=TOPIC, overwrites=ow)
                await c.send(FIRST_POST)
                print(f"  チャンネル {c.name} ✅（説明の一言も置きました）")

            print("\n判定: " + ("✅ これを作ります（--plan なので、まだ作っていません）"
                                if plan else "✅ できました"))
        finally:
            await client.close()

    client.run(token, log_handler=None)
    return 0


if __name__ == "__main__":
    sys.exit(main())
