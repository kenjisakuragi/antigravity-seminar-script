# -*- coding: utf-8 -*-
"""
make_course_index.py — 会員サイトの全レッスンを、botの知識ファイルに書き出す。

  python community/bot/make_course_index.py

■ なぜ要るか（2026-08-20）
  AIさくらぎは、**200本以上ある講座の中身を1本も知らなかった**。
  知識ファイルは6本・32KBで、そこに講座の目次が無い。
  だから「M2ってどこですか」「音楽の講座はどれ」に答えられず、
  毎回エスカレーション（＝桜木さんに投げる）になっていた。

  受講生の質問でいちばん多いのは、実は難しい相談ではなく
  **「あれ、どこにありますか」**。ここを潰すのが、いちばん効く。

■ やること
  UTAGE APIで 部屋（コース）→ グループ → レッスン を全部読み、
  knowledge/course_index.md に「目次」として書き出す。

■ ⚠️ 下書きのレッスンは載せない
  受講生に見えないものを案内すると、「開けません」という次の質問を生む。
"""
import json
import os
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
API = "https://api.utage-system.com/v1"
SITE = "UP7ySCyYwRqU"
OUT = os.path.join(HERE, "knowledge", "course_index.md")


def key():
    for line in open(os.path.join(ROOT, ".env"), encoding="utf-8"):
        if line.startswith("UTAGE_API_KEY="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise SystemExit("判定: NG  .env に UTAGE_API_KEY がありません")


K = key()


def get(path, **params):
    q = "&".join(f"{k}={v}" for k, v in params.items())
    url = f"{API}{path}" + (f"?{q}" if q else "")
    # WindowsのTLS失効確認が通らないので --ssl-no-revoke
    r = subprocess.run(["curl", "-sS", "--ssl-no-revoke",
                        "-H", f"Authorization: Bearer {K}", url],
                       capture_output=True, text=True, errors="replace")
    try:
        return json.loads(r.stdout)
    except Exception:
        print("  [warn] 読めませんでした:", url, r.stdout[:120])
        return {}


def main():
    courses = get(f"/member/sites/{SITE}/courses").get("data", [])
    if not courses:
        print("判定: NG  コースが取れませんでした")
        return 1

    lines = ["# 講座の目次（会員サイトの中身）", "",
             "受講生から「◯◯はどこにありますか」と聞かれたら、この目次から探して案内してください。",
             "部屋の名前と、レッスンの名前を、そのまま伝えるのがいちばん親切です。",
             "⚠️ ここに無いものは「まだ無い」と正直に答えてください。作り話をしないこと。", ""]
    total = 0

    for c in courses:
        cid, cname = c["id"], c["name"]
        lines += [f"## {cname}", ""]
        groups = get(f"/member/sites/{SITE}/courses/{cid}/lesson_groups").get("data", [])
        gmap = {g["id"]: g["name"] for g in groups}

        page, rows = 1, []
        while True:
            r = get(f"/member/sites/{SITE}/courses/{cid}/lessons",
                    page=page, per_page=100, is_published="true")
            d = r.get("data", [])
            rows += d
            if len(d) < 100:
                break
            page += 1

        cur = None
        for l in rows:
            g = gmap.get(l.get("lesson_group_id"), "")
            if g != cur:
                cur = g
                if g:
                    lines.append(f"### {g}")
            lines.append(f"- {l['name']}")
            total += 1
        lines.append("")
        print(f"  {cname}  {len(rows)}本")

    lines += ["---", f"※ 公開中のレッスン 合計 {total}本（この目次の作成時点）"]
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
    print(f"\n判定: OK  {os.path.relpath(OUT, ROOT)}  {total}本 / {os.path.getsize(OUT)/1024:.0f}KB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
