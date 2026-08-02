# -*- coding: utf-8 -*-
"""
_setup_integration.py — 1期生を2期生サーバーに迎えるための、追加ぶんだけを作る。

  python community/_setup_integration.py --plan   # 何をするか見るだけ
  python community/_setup_integration.py          # 実際に作る

■ 方針（チャンネルは期で割らない）
  期ごとにチャンネルを二重化すると、工数が倍になり、会話が半分に薄まる。
  既存の「歩み」のロール（🌱→🌸→🌟→✨）に乗せて、追加は最小限にする。

■ 作るもの
  ロール　　：1期生 / 2期生（名前欄に表示。アクセス権は既存の「受講生」のまま）
  チャンネル：🌷 1期生ラウンジ（1期生だけ・同窓会。運営は回さない）
  　　　　　　🎓 先輩に聞く（全員・2期生が聞き、1期生が答える）

■ 何度流しても大丈夫
  すでにあるものは飛ばす。作りかけで落ちても、もう一度流せば続きから。
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

ROLES = [
    dict(name="1期生", color=0xE0A96D),
    dict(name="2期生", color=0x8AB4E8),
]

# name, カテゴリ, 誰が見られるか, 説明文
CHANNELS = [
    dict(name="🌷1期生ラウンジ", cat="🌙 世界観", who="1期生",
         topic="1期生だけの部屋です。同窓会のようなもの。無理に書かなくて大丈夫です。"),
    dict(name="🎓先輩に聞く", cat="💬 学びとサポート", who="受講生",
         topic="先に歩いた方に聞ける場所です。答える側の参加も大歓迎です。"),
]


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
            for spec in ROLES:
                if spec["name"] in names:
                    print(f"  ロール {spec['name']} … すでにあります")
                    continue
                if plan:
                    print(f"  ロール {spec['name']} … 作ります")
                    continue
                r = await g.create_role(name=spec["name"],
                                        colour=discord.Colour(spec["color"]),
                                        hoist=True, mentionable=True)
                names[r.name] = r
                print(f"  ロール {spec['name']} ✅")

            chans = {c.name: c for c in g.channels}
            cats = {c.name: c for c in g.categories}
            for spec in CHANNELS:
                if spec["name"] in chans:
                    print(f"  チャンネル {spec['name']} … すでにあります")
                    continue
                if plan:
                    print(f"  チャンネル {spec['name']} … 作ります"
                          f"（{spec['cat']} の中／{spec['who']}だけ見られる）")
                    continue
                gate = names.get(spec["who"])
                if gate is None:
                    print(f"  チャンネル {spec['name']} ❌ ロール「{spec['who']}」がありません")
                    continue
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
                    spec["name"], category=cats.get(spec["cat"]),
                    topic=spec["topic"], overwrites=ow)
                print(f"  チャンネル {c.name} ✅")

            print("\n判定: " + ("✅ これを作ります（--plan なので、まだ作っていません）"
                                if plan else "✅ 追加ぶんを作りました"))
            if not plan:
                print("\n次にやること（人の手が要ります）:")
                print("  1. 1期生に告知：これまでの投稿を新しい方も読めるようになります。"
                      "消したいものがあれば今のうちに")
                print("  2. サブスク継続者に「受講生」＋「1期生」を付ける")
                print("  3. 🎓先輩に聞く で、最初の数往復を作る（1期生の数名に個別に声かけ）")
                print("  4. 月1回、非継続者から「受講生」を外す日を決める")
        finally:
            await client.close()

    client.run(token, log_handler=None)
    return 0


if __name__ == "__main__":
    sys.exit(main())
