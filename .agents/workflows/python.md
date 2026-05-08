---
description: How to run Python scripts in any project using the shared venv
---

# Python実行環境の使い方

## 環境情報

このワークスペースでは、以下の共有Python環境を使用します。

### Pythonパス
```
C:\Users\yanagi\.gemini\antigravity\playground\ecliptic-expanse\.venv\Scripts\python.exe
```

### PowerShellでの実行方法

```powershell
# 変数に格納して使用（推奨）
$py = 'C:\Users\yanagi\.gemini\antigravity\playground\ecliptic-expanse\.venv\Scripts\python.exe'

# スクリプトの実行
& $py script.py

# パッケージのインストール
& $py -m pip install パッケージ名

# ワンライナー実行
& $py -c "print('hello')"
```

## インストール済みパッケージ

// turbo-all

### パッケージの確認
```powershell
$py = 'C:\Users\yanagi\.gemini\antigravity\playground\ecliptic-expanse\.venv\Scripts\python.exe'
& $py -m pip list
```

### 主要パッケージ
- `python-pptx` — PowerPointファイルの生成・編集
- `pip` — パッケージ管理

### 新しいパッケージが必要な場合
```powershell
$py = 'C:\Users\yanagi\.gemini\antigravity\playground\ecliptic-expanse\.venv\Scripts\python.exe'
& $py -m pip install 必要なパッケージ名
```

## 注意事項

1. **PowerShellの`python`コマンドは使えません**  
   `python` はWindows Storeのスタブにリダイレクトされるため、必ず上記のフルパスを使ってください。

2. **`& $py` 構文を使う**  
   パスにスペースや特殊文字が含まれるため、`$py` 変数に格納してから `&` で実行してください。

3. **追加のパッケージインストール**  
   新しいパッケージが必要な場合は `& $py -m pip install パッケージ名` でインストールできます。

4. **エンコーディング**  
   日本語を含むスクリプトは `# -*- coding: utf-8 -*-` をファイル先頭に記述してください。
