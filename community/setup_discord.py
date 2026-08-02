# -*- coding: utf-8 -*-
"""
setup_discord.py — らくらくAIキャンパス Discordサーバー 自動構築スクリプト。

やること：
  - ロール（受講生 / レベル / 認定講師 / 運営）を作成
  - カテゴリ＋チャンネル（テキスト/ボイス）を、権限つきで作成
  - すべて「名前で存在チェック → なければ作成」の冪等運用（何度流してもOK）

前提：
  1) Discordでサーバー（ギルド）を作成済み
  2) Developer Portal で Bot アプリを作成 → Botをサーバーに招待済み（権限：管理者 が簡単）
  3) .env（このファイルと同じ階層 or 一つ上）に下記を記載
        DISCORD_BOT_TOKEN=xxxxx
        DISCORD_GUILD_ID=123456789012345678
  4) pip install discord.py python-dotenv

使い方：
    python setup_discord.py           # 開始セット（推奨・少数チャンネル）
    python setup_discord.py --full    # 拡張チャンネルも全部作成

※夜想メソッド系・21日チャレンジは含めない方針。
"""
import os, sys, asyncio
# Windowsコンソール(cp932)で絵文字printがクラッシュするのを防ぐ
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
try:
    import discord
except ImportError:
    print("discord.py が必要です:  pip install discord.py python-dotenv"); sys.exit(1)

# ---- .env 読み込み（同階層→一つ上の順に探す） ----
def load_env():
    here = os.path.dirname(os.path.abspath(__file__))
    for p in (os.path.join(here, ".env"), os.path.join(here, "..", ".env")):
        if os.path.exists(p):
            for line in open(p, encoding="utf-8"):
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip())
load_env()

TOKEN = os.environ.get("DISCORD_BOT_TOKEN", "")
GUILD_ID = int(os.environ.get("DISCORD_GUILD_ID", "0") or 0)
FULL = "--full" in sys.argv

if not TOKEN:
    print("DISCORD_BOT_TOKEN を .env に設定してください。"); sys.exit(1)

# ========================= 設計データ =========================
# ロール：上から強い順。color は 0xRRGGBB。
ROLES = [
    dict(name="運営",              color=0xA82F55, hoist=True,  admin=True),
    dict(name="認定講師",          color=0x7C5CD0, hoist=True,  mod=True),
    dict(name="✨ マスター",        color=0xE8C87A, hoist=False),
    dict(name="🌟 先輩",           color=0x9B7BE0, hoist=False),
    dict(name="🌸 実践者",         color=0xC9A9E8, hoist=False),
    dict(name="🌱 はじめの一歩",    color=0xB8D8B8, hoist=False),
    dict(name="受講生",            color=0x8AB4E8, hoist=False),  # 基本アクセス権
    # 興味タグ（自己申告・リアクションロールで付与する想定）
    dict(name="興味:AI基礎",       color=0x9AC4E8, hoist=False, tag=True),
    dict(name="興味:セルフケア",    color=0xC9B8F0, hoist=False, tag=True),
    dict(name="興味:副業",         color=0xE8C87A, hoist=False, tag=True),
    dict(name="興味:ライフハック",  color=0xB8D8A8, hoist=False, tag=True),
    dict(name="興味:自動化",       color=0x9FB0D8, hoist=False, tag=True),
]

# 権限プリセット：everyone は非公開、受講生に開放
# perms: "read_only"（受講生は閲覧のみ）/ "member"（受講生も投稿可）/ "voice"
# チャンネル：type text/voice、phase start/later
STRUCTURE = [
 ("🌸 はじめに", [
    dict(name="ようこそ",        type="text",  perms="read_only", phase="start",
         topic="サーバーの歩き方・ルール。まずはここを読んでね"),
    dict(name="自己紹介",        type="text",  perms="member",    phase="start",
         topic="お名前・地域・叶えたい願いを、1つ投稿してみましょう🌸"),
    dict(name="お知らせ",        type="text",  perms="read_only", phase="start",
         topic="運営からの大切なお知らせ（LINEにも届きます）"),
 ]),
 ("☀️ 毎日の習慣", [
    dict(name="おはようチャレンジ", type="text", perms="member", phase="start",
         topic="毎朝の一言。今日の気分・やりたいこと・感謝など"),
    dict(name="感謝ノート",       type="text",  perms="member",    phase="start",
         topic="今日よかったこと・ありがとうを3つ"),
    dict(name="できた報告",       type="text",  perms="member",    phase="start",
         topic="小さな「できた！」を、みんなで祝う場所🎉"),
 ]),
 ("🖼 作品・シェア", [
    dict(name="ビジョンボード",    type="text",  perms="member",    phase="start",
         topic="AIで作った理想の一枚をシェア"),
    dict(name="AI作品ギャラリー",  type="text",  perms="member",    phase="start",
         topic="画像・音声・カード・動画など、作った作品を自由に"),
    dict(name="オラクルカード",    type="text",  perms="member",    phase="later",
         topic="自作カード／今日引いたカード"),
    dict(name="副業チャレンジ",    type="text",  perms="member",    phase="later",
         topic="作った・出品した報告（※成果は人それぞれ。金額の断定はしない文化で）"),
 ]),
 ("💬 学びとサポート", [
    dict(name="質問ひろば",       type="text",  perms="member",    phase="start",
         topic="わからないことは気軽に。AIと講師が答えます（初歩的な質問も大歓迎）"),
    dict(name="講座のはなし",     type="text",  perms="member",    phase="later",
         topic="5つの部屋（基礎/セルフケア/副業/ライフハック/自動化）の話題"),
    dict(name="もくもく会",       type="voice", perms="voice",     phase="later",
         topic=None),
 ]),
 ("🌙 世界観", [
    dict(name="新月の願い-満月の手放し", type="text", perms="member", phase="later",
         topic="月のリズムに合わせて、願いを書く・手放す（月のリズム講座と連動）"),
    dict(name="雑談-お茶の間",    type="text",  perms="member",    phase="start",
         topic="なんでもおしゃべり。ゆるくどうぞ☕"),
 ]),
 ("🎤 イベント", [
    dict(name="グループ相談会",    type="voice", perms="voice",     phase="start",
         topic=None),
 ]),
]

# ========================= 実行 =========================
intents = discord.Intents.default()
client = discord.Client(intents=intents)

def overwrites_for(guild, role_map, preset):
    everyone = guild.default_role
    jukousei = role_map.get("受講生")
    koushi   = role_map.get("認定講師")
    unei     = role_map.get("運営")
    ow = {everyone: discord.PermissionOverwrite(view_channel=False)}
    if preset == "read_only":
        ow[jukousei] = discord.PermissionOverwrite(view_channel=True, send_messages=False, add_reactions=True)
        if koushi: ow[koushi] = discord.PermissionOverwrite(view_channel=True, send_messages=True)
        if unei:   ow[unei]   = discord.PermissionOverwrite(view_channel=True, send_messages=True)
    elif preset == "member":
        ow[jukousei] = discord.PermissionOverwrite(view_channel=True, send_messages=True, add_reactions=True)
    elif preset == "voice":
        ow[jukousei] = discord.PermissionOverwrite(view_channel=True, connect=True, speak=True)
    return ow

@client.event
async def on_ready():
    try:
        # ---- ギルド決定：IDがあればそれ、なければ自動検出 ----
        if GUILD_ID:
            guild = client.get_guild(GUILD_ID)
        else:
            guilds = list(client.guilds)
            if len(guilds) == 0:
                print("Botがどのサーバーにも参加していません。SETUP_GUIDE.md 手順3でBotを招待してください。")
                await client.close(); return
            elif len(guilds) > 1:
                print("Botが複数サーバーに参加しています。.env に DISCORD_GUILD_ID を設定してください：")
                for g in guilds: print(f"  - {g.name} : {g.id}")
                await client.close(); return
            guild = guilds[0]
        if guild is None:
            print("ギルドが見つかりません。DISCORD_GUILD_ID とBotの招待を確認してください。"); await client.close(); return
        print(f"サーバー: {guild.name}  （--full={FULL}）\n")

        # ---- ロール作成（冪等） ----
        existing_roles = {r.name: r for r in guild.roles}
        role_map = {}
        for spec in ROLES:
            name = spec["name"]
            if name in existing_roles:
                role_map[name] = existing_roles[name]; print(f"  role  ✓既存 {name}"); continue
            perms = discord.Permissions.none()
            if spec.get("admin"): perms = discord.Permissions(administrator=True)
            elif spec.get("mod"): perms = discord.Permissions(manage_messages=True, moderate_members=True,
                                                              mute_members=True, move_members=True)
            r = await guild.create_role(name=name, colour=discord.Colour(spec["color"]),
                                        hoist=spec.get("hoist", False), permissions=perms,
                                        mentionable=not spec.get("tag", False),
                                        reason="community setup")
            role_map[name] = r; print(f"  role  ＋作成 {name}")

        # ---- カテゴリ＋チャンネル作成（冪等） ----
        existing_cats = {c.name: c for c in guild.categories}
        for cat_name, channels in STRUCTURE:
            cat = existing_cats.get(cat_name)
            if cat is None:
                cat = await guild.create_category(cat_name, reason="community setup")
                print(f"\ncategory ＋作成 {cat_name}")
            else:
                print(f"\ncategory ✓既存 {cat_name}")
            existing_ch = {ch.name: ch for ch in cat.channels}
            for c in channels:
                if not FULL and c["phase"] != "start":
                    continue
                # Discordはチャンネル名を小文字・ハイフン化するので比較も緩く
                cname = c["name"]
                if any(cname == k or cname.replace(" ", "-") == k for k in existing_ch):
                    print(f"    ch  ✓既存 {cname}"); continue
                ow = overwrites_for(guild, role_map, c["perms"])
                try:
                    if c["type"] == "voice":
                        await guild.create_voice_channel(cname, category=cat, overwrites=ow, reason="setup")
                    else:
                        await guild.create_text_channel(cname, category=cat, overwrites=ow,
                                                        topic=c.get("topic"), reason="setup")
                    print(f"    ch  ＋作成 {cname}  [{c['type']}/{c['perms']}]")
                except discord.Forbidden:
                    print(f"    ch  ✗権限不足 {cname}（Botに『チャンネルの管理』権限が必要）")
                except Exception as e:
                    print(f"    ch  ✗失敗 {cname}: {e!r}")

        print("\n完了しました。次は AIサポートbot と 運用コンテンツ を用意します。")
    finally:
        await client.close()

if __name__ == "__main__":
    client.run(TOKEN)
