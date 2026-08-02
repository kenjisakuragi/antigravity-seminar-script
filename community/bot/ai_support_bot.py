# -*- coding: utf-8 -*-
"""
ai_support_bot.py — らくらくAIキャンパス AI一次対応bot。

しくみ：
  - 「質問ひろば」チャンネル、または @メンション で質問を受ける
  - knowledge/*.md（講座・FAQ・プロンプト集）を"知識"としてChatGPTに渡し、やさしく回答
  - 健康/お金/法律の重い相談は専門家へ誘導（config.SAFETY）
  - 答えきれない時はエスカレーション文（＝講師が対応します）
  - 「!reload」で知識を読み直し（運営/認定講師のみ）

前提：
  - Botをサーバーに招待済み（setup_discord.py 済み）
  - Developer Portal → Bot → Privileged Gateway Intents →
    「MESSAGE CONTENT INTENT」と「SERVER MEMBERS INTENT」を ON（両方とも必須）
  - .env に OPENAI_API_KEY（ChatGPT用）と DISCORD_BOT_TOKEN
  - pip install discord.py openai python-dotenv
実行：  python community/bot/ai_support_bot.py
"""
import os, sys, glob, asyncio

try:
    import discord
    from discord.ext import tasks
except ImportError:
    print("discord.py が必要です: pip install discord.py"); sys.exit(1)
try:
    import openai
except ImportError:
    print("openai が必要です: pip install openai"); sys.exit(1)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import config
import usage          # API費用の記録・見張り

HERE = os.path.dirname(os.path.abspath(__file__))
KNOWLEDGE_DIR = os.path.join(HERE, "knowledge")

# このPCはTLSを覗く構成のため、素のままだと OpenAI への接続が証明書エラーで落ちる。
# 検証は切らない。Windowsの証明書ストアから書き出した束を使う。
_ROOTS = os.path.join(HERE, "..", "..", "interviews", "_win_roots.pem")
if not os.environ.get("SSL_CERT_FILE") and os.path.exists(_ROOTS):
    os.environ["SSL_CERT_FILE"] = os.path.abspath(_ROOTS)

# ---- .env（community/.env → repo直下/.env の順で探す） ----
def load_env():
    for p in (os.path.join(HERE, "..", ".env"), os.path.join(HERE, "..", "..", ".env")):
        if os.path.exists(p):
            for line in open(p, encoding="utf-8"):
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip())
load_env()

DISCORD_TOKEN = os.environ.get("DISCORD_BOT_TOKEN", "")
OPENAI_KEY = os.environ.get("OPENAI_API_KEY", "")
if not DISCORD_TOKEN:
    print("DISCORD_BOT_TOKEN を community/.env に設定してください。"); sys.exit(1)
if not OPENAI_KEY:
    print("OPENAI_API_KEY を .env に設定してください（ChatGPT用）。"); sys.exit(1)

gpt = openai.OpenAI(api_key=OPENAI_KEY)

# ---- 知識ベースの読み込み（起動時＆!reloadで再読込） ----
def load_knowledge() -> str:
    parts = []
    for path in sorted(glob.glob(os.path.join(KNOWLEDGE_DIR, "*.md"))):
        name = os.path.basename(path)
        try:
            text = open(path, encoding="utf-8").read().strip()
        except Exception as e:
            text = f"(読み込み失敗: {e})"
        parts.append(f"===== 資料: {name} =====\n{text}")
    return "\n\n".join(parts) if parts else "(知識ファイルがありません)"

KNOWLEDGE = load_knowledge()

def build_system() -> str:
    """system プロンプトを組み立てる。
    知識はいつも同じ文面なので、OpenAI側が自動でキャッシュしてくれる
    （長い前置きが同じなら安くなる）。こちらで指定することは何もない。"""
    body = (
        f"{config.PERSONA}\n\n{config.SAFETY}\n\n"
        "以下は、らくらくAIキャンパスの資料です。質問には、必ずこの資料の範囲で、"
        "受講生にやさしく答えてください。資料にないこと・分からないことは、正直に「分かりません」と述べ、"
        "無理に作り話をしないでください。\n\n"
        f"{KNOWLEDGE}"
    )
    return body

SYSTEM = build_system()

def ask_ai(question: str) -> str:
    """1問1答でChatGPTに聞く。失敗時はエスカレーション文。"""
    try:
        resp = gpt.chat.completions.create(
            model=config.MODEL,
            max_completion_tokens=config.MAX_TOKENS,
            reasoning_effort=config.REASONING,
            messages=[{"role": "system", "content": SYSTEM},
                      {"role": "user", "content": question}],
        )
        usage.record(config.MODEL, getattr(resp, "usage", None))
        text = (resp.choices[0].message.content or "").strip()
        return text or config.ESCALATION
    except openai.RateLimitError:
        return "ただいま混み合っています。少し待ってから、もう一度お願いします🙏"
    except Exception as e:
        print("ChatGPT error:", repr(e)[:200])
        return config.ESCALATION

# ---- Discord ----
intents = discord.Intents.default()
intents.message_content = True   # ← Developer PortalでMESSAGE CONTENT INTENTをONにする必要あり
intents.members = True           # ← 栞の「2週サイレント」を見るのに必要（SERVER MEMBERS INTENT）
client = discord.Client(intents=intents)

# 定期ものは別ファイルに分けてある
import shiori as shiori_mod          # 今週の栞（月曜の投稿・返事・そっとDM）
import morning as morning_mod        # おはようチャレンジ（毎朝の投稿・スタンプ・返事）
SHIORI = None
MORNING = None

def should_answer(message) -> bool:
    if message.author.bot:
        return False
    if client.user in message.mentions:
        return True
    ch = getattr(message.channel, "name", "") or ""
    return any(key in ch for key in config.AUTO_REPLY_CHANNELS)

def clean_question(message) -> str:
    q = message.content or ""
    # メンション部分を除去
    if client.user:
        q = q.replace(f"<@{client.user.id}>", "").replace(f"<@!{client.user.id}>", "")
    return q.strip()

def is_admin(message) -> bool:
    roles = [r.name for r in getattr(message.author, "roles", [])]
    return any(r in config.ADMIN_ROLES for r in roles)

async def send_long(channel, text: str):
    """Discordの2000字制限に合わせて分割送信。"""
    text = (text + config.FOOTER)[:6000]
    while text:
        await channel.send(text[:1900]); text = text[1900:]

async def notify_owner(text: str):
    """桜木さん（サーバーの持ち主）にDMで知らせる。"""
    for g in client.guilds:
        if g.owner is None:
            continue
        try:
            await g.owner.send(text)
        except Exception as e:
            print("お知らせDMに失敗:", repr(e)[:160])
        return


@tasks.loop(hours=6)
async def watch_cost():
    """API費用を見張る。使いすぎの月だけ、1回だけ知らせる。
    毎回報告すると、そのうち読まれなくなるので、黙っているのが基本。"""
    await client.wait_until_ready()
    try:
        msg = usage.over_threshold()
        if msg:
            await notify_owner(msg)
    except Exception as e:
        print("費用の見張りで失敗:", repr(e)[:160])


async def forward_dm(message):
    """botに届いたDMを、桜木さん（サーバーの持ち主）に転送する。
    botは答えない。答えると、いちばん拾いたい声をbotが握りつぶすことになる。"""
    who = message.author
    body = (message.content or "").strip()
    for g in client.guilds:
        owner = g.owner
        if owner is None:
            continue
        try:
            await owner.send(
                f"📩 **{who.display_name}** さんから、AIさくらぎ宛にDMが届きました。\n"
                f"（botは返事をしていません。桜木さんからお願いします）\n\n"
                f"> {body[:1500] if body else '（本文なし）'}\n\n"
                f"返信するには　→　`@{who.name}` をDMで検索してください"
            )
        except Exception as e:
            print("DM転送に失敗:", repr(e)[:160])
        break
    # 送った本人にも、届いたことだけは伝える（無視されたと思わせない）
    try:
        await message.channel.send(
            "お返事ありがとうございます。しっかり受け取りました🌸\n"
            "こちらは自動でお返事する仕組みなので、桜木にそのままお渡ししますね。\n"
            "少しだけ、お時間をくださいね。"
        )
    except Exception:
        pass

@client.event
async def on_ready():
    global SHIORI, MORNING
    print(f"AIサポート稼働: {client.user}  （知識 {len(KNOWLEDGE)} 文字）")
    if SHIORI is None:
        SHIORI = shiori_mod.setup(client, ask_ai)
        print("今週の栞：月曜7時の投稿と、そっとDMを見張ります")
    if MORNING is None:
        MORNING = morning_mod.setup(client, ask_ai)
        print("おはようチャレンジ：毎朝6:30の投稿を見張ります")
    if not watch_cost.is_running():
        watch_cost.start()
        print("API費用：6時間ごとに見張ります（使いすぎの月だけ知らせます）")

@client.event
async def on_message(message):
    global KNOWLEDGE, SYSTEM
    # 管理者コマンド：!cost（かかっているAPI費用）
    if message.content.strip() == "!cost" and is_admin(message):
        await message.channel.send(usage.report())
        return

    # 管理者コマンド：!reload
        KNOWLEDGE = load_knowledge()
        SYSTEM = build_system()
        await message.channel.send(f"知識を読み直しました（{len(KNOWLEDGE)} 文字）✅")
        return

    # botへのDMは、AIに答えさせない。**人に渡す。**
    # 栞の「そっとDM」に返信してくる方は、事務的な質問ではなく
    # 「実は迷っている」ことが多い。ここをbotで完結させてはいけない。
    if isinstance(message.channel, discord.DMChannel) and not message.author.bot:
        await forward_dm(message)
        return

    # 栞チャンネルは「質問」ではないので、AI回答ではなく“受け止める返事”を返す
    if SHIORI and not message.author.bot and SHIORI.is_shiori_channel(message.channel):
        await SHIORI.on_entry(message)
        return

    # おはようチャレンジも同じく、質問ではない。スタンプ＋（人によって）ひとこと
    if MORNING and not message.author.bot and MORNING.is_morning_channel(message.channel):
        await MORNING.on_post(message)
        return

    if not should_answer(message):
        return
    question = clean_question(message)
    if not question:
        await message.channel.send("はい、なんでも聞いてくださいね🌸 どんなことでしょう？")
        return

    async with message.channel.typing():
        # API呼び出しは同期なので別スレッドで
        answer = await asyncio.to_thread(ask_ai, question)
    await send_long(message.channel, answer)

if __name__ == "__main__":
    client.run(DISCORD_TOKEN)
