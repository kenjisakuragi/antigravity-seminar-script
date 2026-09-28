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
import waiting        # 「待ってから出る」
import feedback       # 答えの手ごたえ（リアクションだけ数える）

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

def ask_ai(question: str, context: str = "") -> str:
    """ChatGPTに聞く。失敗時はエスカレーション文。

    ⚠️ 2026-08-20 改修：**それまで会話の流れをまったく渡していなかった。**
    　　1問1答だったので、
    　　　・「それ、どうやるんですか？」の「それ」が分からない
    　　　・返信（リプライ）で聞かれても、何への返信か見えない
    　　　・相手が1期生なのか、今日入った2期生なのかも分からない
    　　という状態で、毎回ゼロから答えていた。
    　　文脈がずれて見えたのは、モデルのせいではなく、**渡していなかったから**。
    """
    user_content = (context + "\n\n" if context else "") + question
    # 今日ぶんの上限に達していたら、**呼ばない**。
    # 知らせるだけの見張りでは間に合わないので、ここで硬く止める。
    if usage.over_daily_limit():
        return usage.DAILY_LIMIT_REPLY

    try:
        resp = gpt.chat.completions.create(
            model=config.MODEL,
            max_completion_tokens=config.MAX_TOKENS,
            reasoning_effort=config.REASONING,
            messages=[{"role": "system", "content": SYSTEM},
                      {"role": "user", "content": user_content}],
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
import pace as pace_mod              # 一人ひとりの進み具合と、月曜の声かけ
import morning as morning_mod        # おはようチャレンジ（毎朝の投稿・スタンプ・返事）
import praise as praise_mod          # 今週の good job（毎週日曜、桜木さんへDM）
SHIORI = None
PACE = None
FEEDBACK = None
MORNING = None
PRAISE = None

def is_mentioned(message) -> bool:
    return client.user in message.mentions

def is_question_channel(message) -> bool:
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
    """Discordの2000字制限に合わせて分割送信。**最後のメッセージを返す。**

    返すのは、そこに 👍 🤔 のスタンプを付けるため（feedback.attach）。
    分割されたときは、最後の1通にだけ付ける。頭に付けると、読む前に押される。
    """
    text = (text + config.FOOTER)[:6000]
    last = None
    while text:
        last = await channel.send(text[:1900]); text = text[1900:]
    return last

def who_context(message) -> str:
    """その方の「これまで」を、AIに渡す文章にする。

    ⚠️ 同じ質問でも、はじめての方と、出品まで進んだ方とでは、返す答えが違う。
    　 「ChatGPTって何ですか」に、M8まで来た方が答えを求めているとは限らない。
    """
    if not PACE:
        return ""
    try:
        return PACE.profile_of(message.author)
    except Exception:
        return ""


async def build_context(message) -> str:
    """その場の「流れ」を集めて、AIに渡せる形にする。

    ■ なぜ要るか（2026-08-20）
      これが無かったので、botは毎回「はじめまして」の状態で答えていた。
      ・「それ、どこにありますか？」の“それ”が分からない
      ・返信で聞かれても、何への返信か見えない
      ・相手が1期生か、今日入った2期生かも分からない
      文脈がずれて見えた原因は、ここ。

    ■ 集めるもの（多すぎると高くなるので、この3つだけ）
      1. 話しかけてきた人（お名前・1期/2期・在籍の長さ）
      2. 返信元のメッセージ（あれば）
      3. 同じチャンネルの直前のやりとり（最大8件・30分以内）
    """
    lines = []

    # 1. 誰が話しているか
    a = message.author
    roles = [r.name for r in getattr(a, "roles", []) if r.name != "@everyone"]
    kigo = "2期生（今月入られたばかり）" if "2期生" in roles else            "1期生（3ヶ月の講座を終えた方）" if "1期生" in roles else "受講生"
    if "認定講師" in roles:
        kigo += "／認定講師"
    lines.append(f"【いま話しかけている人】{a.display_name} さん（{kigo}）")

    # 1-b. その方の「これまで」（栞・おはよう・ギャラリー等の書き込み）
    #      ⚠️ 同じ質問でも、はじめての方と、出品まで進んだ方とでは、返す答えが違う。
    #      　 ここが無いと、毎回「はじめての人」として答えることになる。
    prof = who_context(message)
    if prof:
        lines.append(prof)

    # 2. 返信元
    ref = getattr(message, "reference", None)
    if ref is not None:
        try:
            src = ref.resolved or await message.channel.fetch_message(ref.message_id)
            body = (src.content or "").strip().replace(chr(10), " ")[:300]
            if body:
                lines.append(f"【この発言への返信です】{src.author.display_name}: {body}")
        except Exception:
            pass

    # 3. 直前のやりとり
    try:
        import datetime
        since = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(minutes=30)
        hist = []
        async for m in message.channel.history(limit=12, before=message, after=since):
            body = (m.content or "").strip().replace(chr(10), " ")
            if not body:
                continue
            who = "AIさくらぎ" if m.author.id == (client.user.id if client.user else 0)                   else m.author.display_name
            hist.append(f"  {who}: {body[:200]}")
        if hist:
            hist.reverse()
            lines.append("【このチャンネルの、直前のやりとり（古い順）】")
            lines.extend(hist[-8:])
    except Exception as e:
        print("文脈の取得に失敗:", repr(e)[:120])

    lines.append("")
    lines.append("上の流れをふまえて、いちばん下の質問に答えてください。")
    lines.append("※「それ」「あれ」などは、流れの中の何を指すか読み取ってください。")
    lines.append("※すでに答えたことを、もう一度くり返さないでください。")
    lines.append("")
    lines.append("【質問】")
    return chr(10).join(lines)


async def answer_now(message):
    """実際に答える。呼ばれたとき／誰も答えなかったときだけ通る。"""
    question = clean_question(message)
    if not question:
        await message.channel.send("はい、なんでも聞いてくださいね🌸 どんなことでしょう？")
        return
    ctx = await build_context(message)
    async with message.channel.typing():
        # API呼び出しは同期なので別スレッドで
        answer = await asyncio.to_thread(ask_ai, question, ctx)
    sent = await send_long(message.channel, answer)
    # 「役に立ちましたか？」とは聞かない。押したい人だけ押せるよう、先に付けておく
    if sent is not None:
        await feedback.attach(sent)


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


@tasks.loop(hours=1)
async def watch_cost():
    """API費用を見張る。使いすぎの月だけ、1回だけ知らせる。
    毎回報告すると、そのうち読まれなくなるので、黙っているのが基本。"""
    await client.wait_until_ready()
    try:
        msg = usage.daily_alert()          # 今日ぶんを使い切って、止めた
        if msg:
            await notify_owner(msg)
        msg = usage.over_threshold()       # 月の見込みが多め
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
    global SHIORI, MORNING, PACE, PRAISE, FEEDBACK
    print(f"AIサポート稼働: {client.user}  （知識 {len(KNOWLEDGE)} 文字）")
    if SHIORI is None:
        SHIORI = shiori_mod.setup(client, ask_ai)
    if PACE is None:
        PACE = pace_mod.setup(client, ask_ai)
        print("ペースメーカー：月曜の声かけ（DM）を見張ります")
        print("今週の栞：月曜7時の投稿と、そっとDMを見張ります")
    if MORNING is None:
        MORNING = morning_mod.setup(client, ask_ai)
        print("おはようチャレンジ：毎朝6:30の投稿を見張ります")
    if PRAISE is None:
        PRAISE = praise_mod.setup(client)
        print("今週の good job：毎週日曜20時に、桜木さんへDMします")
    # 再起動で消えた「待ち」を拾い直す
    chans = [c for g in client.guilds for c in g.text_channels
             if any(k in c.name for k in config.AUTO_REPLY_CHANNELS)]
    if chans:
        asyncio.create_task(
            waiting.catch_up(client, chans, config.WAIT_MIN_QUESTION, answer_now))

    # 答えの手ごたえ（リアクションの受け口）。中身は保存しない
    global FEEDBACK
    if FEEDBACK is None:
        FEEDBACK = feedback.setup(client)

    if not watch_cost.is_running():
        watch_cost.start()
        print(f"API費用：1時間ごとに見張ります（1日 {usage.DAILY_LIMIT_JPY:,.0f}円で止めます）")

@client.event
async def on_message(message):
    global KNOWLEDGE, SYSTEM
    # 管理者コマンド：!cost（かかっているAPI費用）
    if message.content.strip() == "!cost" and is_admin(message):
        await message.channel.send(usage.report())
        return

    # 管理者コマンド：!fb（答えの手ごたえ。👍と🤔の数だけ）
    if message.content.strip() in ("!fb", "!feedback") and is_admin(message):
        await message.channel.send(feedback.report())
        return

    # 管理者コマンド：!praise（今週の good job の材料を、いますぐ取り寄せる）
    # ⚠️ 中身は件数を含むので、**チャンネルには出さずDMで返す**。
    #    ここを channel.send にすると、受講生に件数が見えます。絶対にしないこと。
    if message.content.strip() == "!praise" and is_admin(message):
        if PRAISE:
            await message.channel.send("今週ぶんを集めています。DMでお送りします🌸")
            try:
                await PRAISE.send(force=True)
            except Exception as e:
                await message.channel.send(f"うまく集められませんでした（{repr(e)[:80]}）")
        return

    # 管理者コマンド：!good お名前（全体に出した方を、覚えておく）
    # 次の週、同じ人ばかりが並ばないようにするためのものです。
    if message.content.strip().startswith("!good ") and is_admin(message):
        who = message.content.strip()[6:].strip()
        if PRAISE and who:
            PRAISE.record_pick(who)
            await message.channel.send(
                f"**{who}** さんを、今週の good job として覚えました🌸\n"
                f"次回の材料では、しばらく選ばれていない方を上に出します。")
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
        if PACE:
            # ⚠️ 記録だけ。返事は栞が担当する（二重返信を防ぐ）
            PACE.on_entry(message)
        return

    # おはようチャレンジも同じく、質問ではない。スタンプ＋（人によって）ひとこと
    if MORNING and not message.author.bot and MORNING.is_morning_channel(message.channel):
        await MORNING.on_post(message)
        return

    if message.author.bot:
        return

    # ⚠️ どのチャンネルでも、受講生の書き込みは**記憶にだけ**入れる。
    #    栞は7分の1しか書かれていない（おはよう117件 / 栞16件・30日）。
    #    栞だけ見ていると、その方の毎日をまるごと見落とす。
    #    ※ 返事はしない。週も進めない（週が進むのは栞に書いたときだけ）。
    if PACE:
        try:
            PACE.note_any(message)
        except Exception as e:
            print("記憶の保存に失敗:", repr(e)[:120])

    # ① 呼ばれたら、待たずに答える
    if is_mentioned(message):
        await answer_now(message)
        return

    # ② 呼ばれていない質問ひろばは、**しばらく待つ**。
    #    そのあいだに講師や仲間が答えていたら、botは黙る
    if is_question_channel(message):
        asyncio.create_task(
            waiting.maybe_answer_later(client, message,
                                       config.WAIT_MIN_QUESTION, answer_now))

if __name__ == "__main__":
    client.run(DISCORD_TOKEN)
