# -*- coding: utf-8 -*-
"""
_make_note_strip.py — 動画ページの下に貼る「注記」の帯を作る。

  python _make_note_strip.py

■ なぜ画像にするか
  動画から注記テロップを外したので、**スライド側で出す必要がある**（景表法・ステマ規制）。
  14枚に手で打つと、打ち間違いと書式のバラつきが出る。
  1枚の画像にして、コピーして貼るほうが速くて確実。

■ 2種類つくる
  ・黒地版　… 動画ページ（背景が黒）に貼る
  ・白地版　… 明るいスライドに貼る場合の予備

  どちらも幅1920pxで、Canvaのスライド幅にそのまま合う。
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "_preview")

W, H = 1920, 92
TEXT = ("前身講座（らくらくAI副業キャンパス）卒業生の声です。"
        "　個人の感想であり、成果を保証するものではありません。")


def make(name, bg, fg):
    img = Image.new("RGBA", (W, H), bg)
    d = ImageDraw.Draw(img)
    f = ImageFont.truetype(r"C:\Windows\Fonts\meiryo.ttc", 30)
    d.text((W // 2, H // 2), TEXT, font=f, fill=fg, anchor="mm")
    p = os.path.join(OUT, name)
    img.save(p)
    print(f"  {name}  {W}x{H}")


def main():
    os.makedirs(OUT, exist_ok=True)
    # 黒地・白文字（動画ページ用）。背景は半透明にして、映像を完全には隠さない
    make("注記_黒地.png", (0, 0, 0, 205), (235, 235, 235, 255))
    # 白地・濃紺文字（明るいスライド用）
    make("注記_白地.png", (255, 255, 255, 235), (27, 27, 58, 255))
    print("\n判定: OK  _preview/ に2枚")
    print("  Canvaでは、動画ページの**いちばん下**に置いてください。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
