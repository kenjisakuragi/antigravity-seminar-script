# シンVPSに、botを載せる手順

**AIさくらぎ**（AIサポート＋今週の栞＋おはようチャレンジ）を、シンVPSで24時間動かす。

一度これをやれば、あとは**桜木さんが何もしなくても動き続けます**。
PCを閉じても、寝ていても、旅行に行っても止まりません。

---

## 先に：この構成でできること

| | |
|---|---|
| 質問への即答 | ○ 24時間 |
| 毎朝6:30の投稿 | ○ |
| 毎週月曜7:00の栞＋DM | ○ |
| 追加費用 | **0円**（契約済みのVPSを使うため） |
| 落ちたとき | **自動で起き上がる**（systemdが面倒を見る） |
| サーバー再起動後 | **自動で立ち上がる** |

---

## 桜木さんにやっていただくこと（2つだけ）

1. **シンVPSにSSHでつなげる状態にする**（コントロールパネルでOSを入れて、鍵かパスワードを用意）
2. **`.env` の中身をサーバーに貼る**（トークンとAPIキー。ここは人の手でお願いします）

あとは下のコマンドを順に流すだけです。**上から順に、1行ずつ**で大丈夫です。

---

## 0. 前提

- OSは **Ubuntu 24.04 LTS** を想定（シンVPSのコントロールパネルから選べます）
- SSHでログインできること

```bash
ssh root@<サーバーのIPアドレス>
```

---

## 1. 下ごしらえ

```bash
apt update && apt upgrade -y
apt install -y python3 python3-venv git
```

bot専用のユーザーを作る（rootで動かさない。事故ったときの被害を小さくするため）。

```bash
useradd -m -s /bin/bash rakuraku
mkdir -p /opt/rakuraku-bot
chown rakuraku:rakuraku /opt/rakuraku-bot
```

## 2. ファイルを置く

GitHubから取ってくる場合（リポジトリが private なら、途中でユーザー名とトークンを聞かれます）。

```bash
su - rakuraku
git clone https://github.com/kenjisakuragi/antigravity-seminar-script.git /opt/rakuraku-bot
```

※ GitHubを使わない場合は、`community/` フォルダごとをWinSCP等で
`/opt/rakuraku-bot/community/` に置いてください。それでも動きます。

## 3. Pythonの支度

```bash
cd /opt/rakuraku-bot
python3 -m venv .venv
.venv/bin/pip install -r community/bot/requirements.txt
```

## 4. 鍵を置く（★ここだけ桜木さんの手で）

```bash
nano /opt/rakuraku-bot/.env
```

エディタが開くので、この2行を貼る（値はご自身のものに）。

```
DISCORD_BOT_TOKEN=（Discordのbotトークン）
OPENAI_API_KEY=（OpenAIのAPIキー）
```

`Ctrl+O` → `Enter` で保存、`Ctrl+X` で閉じる。

**他人に読まれないようにします。**

```bash
chmod 600 /opt/rakuraku-bot/.env
exit          # rakurakuユーザーから抜けて、rootに戻る
```

## 5. 常駐させる

```bash
cp /opt/rakuraku-bot/community/deploy/rakuraku-bot.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable --now rakuraku-bot
```

動いているか見る。

```bash
systemctl status rakuraku-bot
journalctl -u rakuraku-bot -f
```

`AIサポート稼働: AIさくらぎ` と出れば成功です。`Ctrl+C` で見るのをやめられます。

## 6. 記録のバックアップ（やっておいてください）

```bash
cp /opt/rakuraku-bot/community/deploy/backup_state.sh /usr/local/bin/
chmod +x /usr/local/bin/backup_state.sh
crontab -e
```

いちばん下に1行足す。

```
30 3 * * * /usr/local/bin/backup_state.sh
```

**なぜ必要か。** `_shiori_state.json` には「誰にいつDMしたか」が入っています。
これが消えると、一度そっと声をかけた方に、**もう一度同じDMが飛びます**。
栞の設計でいちばんやってはいけないことなので、毎日とっておきます。

---

## ふだんの操作

| したいこと | コマンド |
|---|---|
| 動いているか見る | `systemctl status rakuraku-bot` |
| ログを見る | `journalctl -u rakuraku-bot -n 100` |
| 止める | `systemctl stop rakuraku-bot` |
| 動かす | `systemctl start rakuraku-bot` |
| 入れ直す | `systemctl restart rakuraku-bot` |

## 中身を直したとき（知識ファイルの編集など）

`knowledge/*.md` を直しただけなら、**Discordで `!reload` と打つだけ**で反映されます
（運営・認定講師のみ）。サーバーを触る必要はありません。

コード自体を直したときは、

```bash
su - rakuraku -c 'cd /opt/rakuraku-bot && git pull'
systemctl restart rakuraku-bot
```

---

## ⚠️ 注意

- **`.env` は絶対にGitに入れない**（`.gitignore` で除外済み）
- Discordトークンを人に見せてしまったら、Developer Portalで**リセット**する
- OpenAIのキーも同じ。漏れたら発行し直す
- シンVPSのファイアウォールは、**外から開ける必要がありません**。
  botは自分からDiscordにつなぎに行くだけなので、穴を開けないでください

## つまずいたら

| 症状 | 見るところ |
|---|---|
| `AIサポート稼働` が出ない | `.env` の中身。トークンの前後に空白やクォートが入っていないか |
| 起動はするが反応しない | Developer Portal の **MESSAGE CONTENT INTENT** と **SERVER MEMBERS INTENT** がONか |
| 朝の投稿が変な時刻に出る | `systemctl show rakuraku-bot | grep TZ` で `Asia/Tokyo` になっているか |
| すぐ落ちる | `journalctl -u rakuraku-bot -n 50` にエラーが出ています |
