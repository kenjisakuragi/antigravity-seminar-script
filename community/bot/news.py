# -*- coding: utf-8 -*-
"""
news.py — 毎朝、注目のAIニュースを #aiニュース に投稿する。

⚠️ いちばん大事な決めごと：**AIに「今日のニュースを探して」と頼まない**

　 それをやると、存在しないニュースを、それらしく書きます。
　 日付も社名も金額も、平気で作ります。AIは自分が最近を知らないことを知りません。
　 受講生は40〜60代で、書いてあることを信じてくださる方です。
　 嘘のニュースを1回出したら、AIさくらぎ全体の信用が終わります。

　 ですので役割を分けます。
　   ニュースを見つける … RSS（機械）。嘘をつけない
　   やさしく書き直す   … AI。文章だけ担当

　 AIには**RSSで実際に取れた記事だけ**を渡し、
　 「渡した記事に書いていないことは一文字も書かない」と縛ります。
　 出典URLもRSSの実物をそのまま貼り、AIには作らせません。

使い方
　 本番　  ai_support_bot.py から setup(client) で呼ばれる（morning.py と同じ）
　 お試し  python news.py --dry 3     … 直近3日ぶんの投稿案を、画面に出すだけ

前提：ai_support_bot.py から呼ばれる（同じbotユーザー・同じ接続）。
"""
import os
import re
import io
import sys
import json
import hashlib
import datetime as dt
import urllib.request
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime

HERE = os.path.dirname(os.path.abspath(__file__))
# 記録は**コードとは別の場所**に置く。
# setup.sh は入れ直しのたびにコード一式を消して置き直すので、
# コードと同じ場所に置くと**記録ごと消える**（実際に消えて、栞が二重投稿された）。
STATE_DIR = os.environ.get("RAKURAKU_STATE_DIR", HERE)
os.makedirs(STATE_DIR, exist_ok=True)
STATE_PATH = os.path.join(STATE_DIR, "_news_state.json")

JST = dt.timezone(dt.timedelta(hours=9))


def now_jst() -> dt.datetime:
    return dt.datetime.now(JST)


# ═══════════════════════════════════════════════════════════
# 設定（運用で変えるのは、ここだけ）
# ═══════════════════════════════════════════════════════════

CHANNEL_KEYS = ["aiニュース", "AIニュース", "ニュース"]   # チャンネル名の部分一致
POST_HOUR = 8                 # 投稿時刻（朝のあいさつ6:30と1時間半あける）
POST_MIN = 0
CATCHUP_UNTIL = 10            # 出遅れても、この時刻まではその日ぶんを出す
PICK = 3                      # 何本えらぶか
LOOKBACK_HOURS = 36           # 何時間前までの記事を対象にするか
SEEN_KEEP_DAYS = 30           # 一度出した記事を、何日おぼえておくか

# ⚠️ 下書きモード。True のあいだは、投稿せずに桜木さんへDMするだけ。
DRAFT_MODE = False
OWNER_ID = 0                  # 下書きの送り先（0なら、サーバーの持ち主へ）

# ── 集める先（2026-09-11 に実際につないで確認済み） ──
# 形式が2種類あることに注意。RDF側は名前空間を指定しないと0件に見える。
FEEDS = [
    # (名前, URL, AI専門か)
    ("ITmedia AI＋",     "https://rss.itmedia.co.jp/rss/2.0/aiplus.xml",                      True),
    ("AI Watch",         "https://ai.watch.impress.co.jp/data/rss/1.0/aiw/feed.rdf",          True),
    ("ITmedia NEWS",     "https://rss.itmedia.co.jp/rss/2.0/news_bursts.xml",                 False),
    ("ASCII.jp",         "https://ascii.jp/rss.xml",                                          False),
    ("CNET Japan",       "https://japan.cnet.com/rss/index.rdf",                              False),
    ("Impress Watch",    "https://www.watch.impress.co.jp/data/rss/1.0/ipw/feed.rdf",         False),
    ("ギズモード",        "https://www.gizmodo.jp/index.xml",                                  False),
]

# AI専門でない媒体から拾うときに、**これを含むものだけ**残す
KEEP_WORDS = [
    "AI", "ＡＩ", "生成AI", "ChatGPT", "Gemini", "Claude", "Copilot", "OpenAI",
    "Anthropic", "画像生成", "動画生成", "音声合成", "文字起こし", "自動化",
    "エージェント", "チャットボット", "機械学習", "ディープラーニング",
]

# ⚠️ **こちらのほうが大事。** 資金調達と株価の話が毎日並ぶと、
# 　 「自分には関係ない部屋」になって、誰も見に来なくなります。
DROP_WORDS = [
    "株価", "時価総額", "資金調達", "シリーズA", "シリーズB", "ラウンド",
    "半導体", "データセンター", "決算", "IPO", "上場", "買収", "出資",
    "論文", "ベンチマーク", "パラメータ", "SDK", "API仕様", "脆弱性",
    "求人", "採用情報", "セミナー開催", "ウェビナー", "カンファレンス開催",
    # ⚠️ プロ向けの道具。受講生は触りません（2026-09-11 お試しで混ざったため追加）
    "Premiere", "After Effects", "DaVinci", "Unity", "Unreal", "Blender",
    "オンプレ", "SaaS基盤", "基幹システム", "開発者向け", "エンタープライズ",
    "GPU", "サーバー向け", "ゲノム", "研究グループ",
]

# 投稿の直前に、機械でかける語句チェック。
# ⚠️ ひとつでも入っていたら**投稿しない**。桜木さんへDMで知らせる。
BANNED = [
    "必ず", "確実に", "誰でも稼げ", "儲かります", "稼げます", "絶対に",
    "乗り遅れ", "手遅れ", "今すぐ買", "保証します",
]

HEADER = "おはようございます。今日のAIニュースです☀️"
FOOTER = "———\n🤖 自動投稿です。気になるものがあれば #質問ひろば でどうぞ🌸"

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36")


# ═══════════════════════════════════════════════════════════
# ① 集める
# ═══════════════════════════════════════════════════════════

RDF = "{http://purl.org/rss/1.0/}"
ATOM = "{http://www.w3.org/2005/Atom}"
DC = "{http://purl.org/dc/elements/1.1/}"


def _text(el, *names):
    for n in names:
        v = el.findtext(n)
        if v:
            return v.strip()
    return ""


def _when(el) -> dt.datetime | None:
    """記事の日時。媒体ごとに書き方が違うので、順に試す。"""
    raw = _text(el, "pubDate", f"{DC}date", "published", f"{ATOM}published",
                "updated", f"{ATOM}updated")
    if not raw:
        return None
    try:
        return parsedate_to_datetime(raw).astimezone(JST)
    except Exception:
        pass
    try:
        return dt.datetime.fromisoformat(raw.replace("Z", "+00:00")).astimezone(JST)
    except Exception:
        return None


def fetch_all(timeout=20) -> list[dict]:
    """全媒体から記事を集める。1媒体が落ちても、全体は止めない。"""
    out = []
    for name, url, is_ai in FEEDS:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            root = ET.fromstring(urllib.request.urlopen(req, timeout=timeout).read())
            items = (root.findall(".//item") or root.findall(f".//{RDF}item")
                     or root.findall(f".//{ATOM}entry"))
            for it in items:
                title = _text(it, "title", f"{RDF}title", f"{ATOM}title")
                link = _text(it, "link", f"{RDF}link")
                if not link:                       # Atomは属性側
                    a = it.find(f"{ATOM}link")
                    link = a.get("href") if a is not None else ""
                desc = _text(it, "description", f"{RDF}description",
                             "summary", f"{ATOM}summary")
                if not (title and link):
                    continue
                out.append({"media": name, "ai": is_ai, "title": title,
                            "url": link, "desc": re.sub("<[^>]+>", "", desc)[:300],
                            "at": _when(it)})
        except Exception as e:
            print(f"  ⚠️ {name} が取れませんでした（{type(e).__name__}）。とばします")
    return out


# ═══════════════════════════════════════════════════════════
# ② 機械でふるいにかける（AIに渡す前に、ここで9割落とす）
# ═══════════════════════════════════════════════════════════

def _key(url: str) -> str:
    """同じ記事かどうかの目印。追跡用のパラメータは外す。"""
    u = url.split("?")[0].split("#")[0].rstrip("/")
    return hashlib.sha1(u.encode()).hexdigest()[:16]


def sift(arts: list[dict], seen: set[str], until: dt.datetime,
         hours: int = LOOKBACK_HOURS, per_media: int = 5) -> list[dict]:
    """時間・重複・話題で絞る。"""
    since = until - dt.timedelta(hours=hours)
    got, keys, count = [], set(), {}
    for a in arts:
        if a["at"] is None or not (since <= a["at"] <= until):
            continue
        k = _key(a["url"])
        if k in keys or k in seen:                 # 重複と、前に出したもの
            continue
        text = a["title"] + " " + a["desc"]
        if any(w in text for w in DROP_WORDS):     # ⚠️ ここがいちばん効く
            continue
        if not a["ai"] and not any(w in text for w in KEEP_WORDS):
            continue                               # AI専門以外は、AIの話だけ
        if count.get(a["media"], 0) >= per_media:
            continue
        keys.add(k)
        count[a["media"]] = count.get(a["media"], 0) + 1
        a["key"] = k
        got.append(a)
    got.sort(key=lambda x: (not x["ai"], -x["at"].timestamp()))
    return got


# ═══════════════════════════════════════════════════════════
# ③ AIが選んで、やさしく書く
# ═══════════════════════════════════════════════════════════

SYSTEM = """あなたは「らくらくAIキャンパス」の、やさしいAIサポート係です。
受講生は40〜60代の女性が中心で、AIやパソコンが得意でない方も多くいます。

渡された記事の一覧から、受講生にとって注目すべきものを選び、やさしく紹介してください。

【選ぶ物差し】ひとつだけです。
「これを読んだ受講生が、今日または今週、自分で何かできるようになるか」

  ◎ 選ぶ：新しい機能が使えるようになった／無料や安くなった／日本語に対応した／
  　　　　スマホでできるようになった／仕事や暮らしの変わり方／世の中の空気が変わる話
  ✗ 選ばない：研究や論文／資金調達や株価／海外だけの話／開発者向けの技術の話／
  　　　　　　企業どうしの提携／細かい仕様変更

⚠️ **受講生が実際に手を出せるもの**を優先してください。
　 ChatGPT・Gemini・スマホのアプリ・無料で試せるもの が、いちばん喜ばれます。
　 動画編集ソフトや業務システムなど、**仕事で使う人しか触らない道具**は選ばないでください。

⚠️ 不安な話題（犯罪・なりすまし・仕事が減る等）は、**1日に1本まで**。
　 選ぶときは、必ず「だから、こうしておくと安心です」と**備えの話に着地**させてください。
　 着地できないなら、選ばないでください。朝いちばんに不安だけ残すのは、いちばん避けたいことです。

【書き方】
- 1本につき、次の3行だけ。
    ① 見出し（20字以内。記事の見出しを、やさしいことばに直す）
    　 → これで、何ができるようになるか（1行・40字以内）
    　 URL（渡されたものを、そのまま）
- 横文字・専門用語はかみくだく（「マルチモーダル」→「写真も音も、まとめて扱える」）
- 断定しない。「〜のようです」「〜と発表されました」
- あおらない。「もう乗り遅れます」のような書き方はしない
- 「稼げる」「儲かる」「必ず」は、絶対に書かない

【守ること】
⚠️ 渡された記事に書いていないことは、一文字も書かないでください。
⚠️ URLは渡されたものをそのまま使ってください。作らないでください。
⚠️ ちょうどよい記事が少ない日は、少ない本数で構いません。無理に埋めないでください。
⚠️ ひとつもふさわしい記事がない日は、「なし」とだけ答えてください。

【出す形】前置きも、あとがきも、書かないでください。本文だけを次の形で。
① 見出し
　 → 何ができるようになるか
　 URL

② 見出し
　 → 何ができるようになるか
　 URL
"""


def compose(gpt, model: str, arts: list[dict], pick: int = PICK,
            max_tokens: int = 900, usage_mod=None) -> str:
    """AIに選ばせて、書かせる。"""
    if not arts:
        return ""
    lines = []
    for i, a in enumerate(arts, 1):
        lines.append(f"[{i}] {a['title']}\n　媒体:{a['media']}　URL:{a['url']}\n"
                     f"　概要:{a['desc'][:160]}")
    user = (f"次の記事から、{pick}本えらんで紹介してください。\n\n" + "\n\n".join(lines))
    resp = gpt.chat.completions.create(
        model=model,
        max_completion_tokens=max_tokens,
        reasoning_effort="low",
        messages=[{"role": "system", "content": SYSTEM},
                  {"role": "user", "content": user}],
    )
    if usage_mod is not None:
        usage_mod.record(model, getattr(resp, "usage", None))
    return (resp.choices[0].message.content or "").strip()


def check(body: str, arts: list[dict]) -> str | None:
    """投稿してよいか、機械で確かめる。だめな理由を返す（問題なければ None）。"""
    if not body or body.strip() in ("なし", "none", "None"):
        return "ふさわしい記事がありませんでした"
    for w in BANNED:
        if w in body:
            return f"使ってはいけない言葉が入っています：「{w}」"
    urls = re.findall(r"https?://\S+", body)
    if not urls:
        return "出典URLが1つも入っていません"
    # ⚠️ 渡していないURLが混じっていないか。ここが「嘘のニュース」の最後の砦。
    allowed = {a["url"].split("?")[0].rstrip("/") for a in arts}
    for u in urls:
        if u.rstrip("。、）)").split("?")[0].rstrip("/") not in allowed:
            return f"渡していないURLが入っています：{u[:60]}"
    return None


def build(body: str) -> str:
    return f"{HEADER}\n\n{body}\n\n{FOOTER}"


# ═══════════════════════════════════════════════════════════
# 記録
# ═══════════════════════════════════════════════════════════

def load_state() -> dict:
    if os.path.exists(STATE_PATH):
        try:
            return json.load(open(STATE_PATH, encoding="utf-8"))
        except Exception:
            pass
    return {"last_post": None, "seen": {}}


def save_state(s: dict):
    # 古い記録は落とす
    limit = (now_jst().date() - dt.timedelta(days=SEEN_KEEP_DAYS)).isoformat()
    s["seen"] = {k: v for k, v in s.get("seen", {}).items() if v >= limit}
    json.dump(s, open(STATE_PATH, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


# ═══════════════════════════════════════════════════════════
# Discord とのつなぎ（ai_support_bot.py から呼ばれる）
# ═══════════════════════════════════════════════════════════

def setup(client, gpt, model, usage_mod):
    from discord.ext import tasks

    state = load_state()

    def find_channel():
        for g in client.guilds:
            for c in g.text_channels:
                if any(k.lower() in c.name.lower() for k in CHANNEL_KEYS):
                    return c
        return None

    async def run_once(today: dt.date) -> bool:
        arts = sift(fetch_all(), set(state.get("seen", {})), now_jst())
        if not arts:
            print("news: 対象の記事がありませんでした。今日は投稿しません")
            return False
        body = compose(gpt, model, arts, usage_mod=usage_mod)
        ng = check(body, arts)
        ch = find_channel()
        if ng:
            print(f"news: 投稿を見送りました（{ng}）")
            await notify_owner(f"⚠️ 今日のAIニュースは投稿を見送りました。\n理由：{ng}")
            return False
        text = build(body)
        if DRAFT_MODE:
            await notify_owner("【下書き】今日のAIニュースです。よければ、そのまま貼ってください。\n\n" + text)
        else:
            if ch is None:
                print("news: 投稿先のチャンネルが見つかりません")
                return False
            await ch.send(text)
        # 出した記事をおぼえる
        for u in re.findall(r"https?://\S+", body):
            state.setdefault("seen", {})[_key(u)] = today.isoformat()
        state["last_post"] = today.isoformat()
        save_state(state)
        return True

    async def notify_owner(msg: str):
        try:
            uid = OWNER_ID or (client.guilds[0].owner_id if client.guilds else 0)
            if uid:
                u = await client.fetch_user(uid)
                await u.send(msg[:1900])
        except Exception as e:
            print(f"news: DMを送れませんでした（{type(e).__name__}）")

    @tasks.loop(minutes=15)
    async def beat():
        await client.wait_until_ready()
        now = now_jst()
        today = now.date()
        if state.get("last_post") == today.isoformat():
            return                                    # その日はもう出した
        if now.hour * 60 + now.minute < POST_HOUR * 60 + POST_MIN:
            return
        if now.hour >= CATCHUP_UNTIL:
            return                                    # 昼を回ったら、その日は出さない
        await run_once(today)

    beat.start()
    return beat


# ═══════════════════════════════════════════════════════════
# お試し（python news.py --dry 3）
# ═══════════════════════════════════════════════════════════

def _dry(days: int):
    """直近◯日ぶんの投稿案を、実際のロジックで作って画面に出す。

    ⚠️ Discordには何も出しません。記録も残しません。
    """
    import openai

    # ⚠️ Windowsの画面は cp932。絵文字を出すと落ちるので、utf-8にしておく
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    roots = os.path.join(HERE, "..", "..", "interviews", "_win_roots.pem")
    if not os.environ.get("SSL_CERT_FILE") and os.path.exists(roots):
        os.environ["SSL_CERT_FILE"] = os.path.abspath(roots)
    for p in (os.path.join(HERE, "..", ".env"), os.path.join(HERE, "..", "..", ".env")):
        if os.path.exists(p):
            for line in open(p, encoding="utf-8"):
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip())
    key = os.environ.get("OPENAI_API_KEY", "")
    if not key:
        print("OPENAI_API_KEY がありません"); return
    gpt = openai.OpenAI(api_key=key)
    import config

    print("① 集めます …")
    arts = fetch_all()
    print(f"　 {len(arts)}本 集まりました\n")

    seen: set[str] = set()
    for d in range(days):
        until = now_jst() - dt.timedelta(days=d)
        day = until.date()
        print("=" * 66)
        print(f"■ {day.strftime('%m月%d日')} ぶん（{(until - dt.timedelta(hours=LOOKBACK_HOURS)).strftime('%m/%d %H:%M')} 〜 {until.strftime('%m/%d %H:%M')} の記事）")
        print("=" * 66)
        got = sift(arts, seen, until)
        print(f"② ふるいにかけた結果：{len(arts)}本 → **{len(got)}本**")
        if got:
            for a in got[:12]:
                print(f"　 ・[{a['media']}] {a['title'][:52]}")
            if len(got) > 12:
                print(f"　 …ほか{len(got) - 12}本")
        print()
        if not got:
            print("③ 対象なし → **投稿しません**\n")
            continue
        body = compose(gpt, config.MODEL, got, usage_mod=None)
        ng = check(body, got)
        print("③ でき上がった投稿：")
        print("-" * 66)
        if ng:
            print(f"⚠️ 投稿を見送ります（{ng}）")
            print(body)
        else:
            print(build(body))
        print("-" * 66 + "\n")
        for u in re.findall(r"https?://\S+", body):
            seen.add(_key(u))


if __name__ == "__main__":
    n = 3
    if "--dry" in sys.argv:
        i = sys.argv.index("--dry")
        if i + 1 < len(sys.argv):
            n = int(sys.argv[i + 1])
        _dry(n)
    else:
        print("使い方: python news.py --dry 3")
