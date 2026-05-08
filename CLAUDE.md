# らくらくAI副業キャンパス — セミナー制作リポジトリ

## プロジェクト概要
AI副業スクール「らくらくAI副業キャンパス」の受講者向け教材・スライド・読み原稿を管理するリポジトリ。

## ディレクトリ構成

```
seminar_script/
├── lecture_script_0N.md      # 第N回 講師読み原稿（原稿ソース）
├── create_textbook_0N.py     # 第N回 受講者テキスト教材 Word 生成スクリプト
├── export_lecture0N_to_word.py  # 第N回 読み原稿 Word 生成スクリプト
├── generate_session0N.py     # 第N回 PowerPoint スライド生成スクリプト
├── curriculum_*.md           # カリキュラム設計ドキュメント
├── handoff_to_claude_code.md # Claude Code への作業引き継ぎ指示書
└── CLAUDE.md                 # このファイル
```

## Python 実行環境

```powershell
$py = 'C:\Users\yanagi\.gemini\antigravity\playground\ecliptic-expanse\.venv\Scripts\python.exe'
& $py <script_name>.py
```

依存パッケージ：`python-docx`（インストール済み）、`python-pptx`（インストール済み）

## 出力ファイル命名規則

| 種別 | ファイル名パターン |
|------|--------------------|
| 受講者テキスト教材（Word） | `第N回_テキスト教材_完全版.docx` |
| 講師読み原稿（Word） | `セミナー読み原稿_第N回_vX.docx` |
| スライド（PowerPoint） | `講義0N_タイトル_vX.pptx` |

## デザイン仕様（共通）

- フォント：メイリオ
- 見出し色：RGB(14, 165, 233) — ライトブルー
- 強調色：RGB(234, 88, 12) — オレンジ
- コードブロック：Courier New 9pt、左インデント 1.5cm

## カリキュラム進捗

| 回 | テーマ | 状態 |
|----|--------|------|
| 第1回 | はじめの一歩・AI副業の全体像 | 完了 |
| 第2回 | AI動画① 静止画→動画化 | 完了 |
| 第3回 | AI動画② キャラクターが喋る・YouTube公開 | 完了 |
| 第4回以降 | AI音楽・Kindle・ブログ・画像販売… | 準備中 |

## 新しい回を作成するときの手順

1. `lecture_script_0N.md` で講義原稿を執筆
2. `create_textbook_0N.py` でテキスト教材 Word を生成
3. `export_lecture0N_to_word.py` で読み原稿 Word を生成
4. `generate_session0N.py` でスライドを生成
