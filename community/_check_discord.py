# -*- coding: utf-8 -*-
"""
_check_discord.py — Botがサーバーに繋がるか、権限が足りているかを確かめる。

  python community/_check_discord.py

つなぐだけで、何も作りません。何も消しません。
トークンは表示しません（.env から読むだけ）。
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def env(name):
    for line in open(os.path.join(ROOT, ".env"), encoding="utf-8"):
        if line.startswith(name + "="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    return None


def main():
    token, gid = env("DISCORD_BOT_TOKEN"), env("DISCORD_GUILD_ID")
    if not token or not gid:
        print("判定: ❌ .env に DISCORD_BOT_TOKEN / DISCORD_GUILD_ID がありません")
        return 1
    print(f"トークン 読み込みOK（{len(token)}文字）／サーバーID {gid}")

    import discord
    intents = discord.Intents.default()
    intents.members = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        try:
            g = client.get_guild(int(gid))
            if g is None:
                print("判定: ❌ そのサーバーが見つかりません")
                print("   → Botがそのサーバーに招待されていない可能性があります")
                return
            me = g.me
            p = me.guild_permissions
            print(f"\nサーバー名：{g.name}")
            print(f"メンバー数：{g.member_count}")
            print(f"Bot名　　：{client.user}")
            print(f"\n権限：管理者={p.administrator} / ロール管理={p.manage_roles} / "
                  f"チャンネル管理={p.manage_channels}")

            print(f"\n既存のロール（{len(g.roles)}）:")
            for r in sorted(g.roles, key=lambda r: -r.position):
                if r.name != "@everyone":
                    print(f"  {r.name}（{len(r.members)}人）")

            print(f"\n既存のチャンネル（{len(g.channels)}）:")
            for c in sorted(g.channels, key=lambda c: (c.category.name if c.category else "", c.position)):
                if isinstance(c, discord.CategoryChannel):
                    print(f"  ■ {c.name}")
                else:
                    print(f"    {c.name}（{c.type}）")

            ok = p.administrator or (p.manage_roles and p.manage_channels)
            print(f"\n判定: {'✅ この権限で、ロールもチャンネルも作れます' if ok else '❌ 権限が足りません（ロール管理・チャンネル管理が必要）'}")
        finally:
            await client.close()

    try:
        client.run(token, log_handler=None)
    except Exception as e:
        print(f"判定: ❌ 接続できません: {type(e).__name__}: {e}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
