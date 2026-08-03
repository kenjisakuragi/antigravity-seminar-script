#!/bin/bash
# setup.sh — シンVPSに、AIさくらぎを住まわせる。
#
#   bash /root/setup.sh
#
# 何度流しても大丈夫。すでにできているものは飛ばす。
# .env だけは人の手で書く（鍵はこのスクリプトに書かない）。
set -eu

APP=/opt/rakuraku-bot
USER_NAME=rakuraku

say() { echo ""; echo "==== $* ===="; }

say "1/6  必要なものを入れます"
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
apt-get install -y -qq python3 python3-venv tzdata >/dev/null
timedatectl set-timezone Asia/Tokyo || true

say "2/6  bot専用のユーザーを作ります"
# rootで動かさない。万一おかしくなっても、被害をここだけに閉じ込めるため
id "$USER_NAME" >/dev/null 2>&1 || useradd -m -s /bin/bash "$USER_NAME"
mkdir -p "$APP"

say "3/6  ファイルを置きます"
# 記録は別の場所（state/）に置く。ここは絶対に消さない
mkdir -p "$APP/state"
if [ -d /root/community ]; then
    rm -rf "$APP/community"
    cp -r /root/community "$APP/community"
    # 手元のPCの分は持ち込まない（キャッシュと、Windows用の証明書）
    find "$APP/community" -name '__pycache__' -type d -exec rm -rf {} + 2>/dev/null || true
else
    echo "  /root/community がありません。先に手元のPCから送ってください。"
    exit 1
fi
chown -R "$USER_NAME:$USER_NAME" "$APP"
# 旧版はコードと同じ場所に記録を置いていた。あれば拾って引っ越す
for f in _shiori_state.json _morning_state.json _usage.json; do
    if [ -f "$APP/community/bot/$f" ] && [ ! -f "$APP/state/$f" ]; then
        mv "$APP/community/bot/$f" "$APP/state/$f"
        echo "  記録を引っ越しました: $f"
    fi
done
chown -R "$USER_NAME:$USER_NAME" "$APP/state"

say "4/6  Pythonの支度をします"
[ -d "$APP/.venv" ] || sudo -u "$USER_NAME" python3 -m venv "$APP/.venv"
sudo -u "$USER_NAME" "$APP/.venv/bin/pip" install -q --upgrade pip
sudo -u "$USER_NAME" "$APP/.venv/bin/pip" install -q -r "$APP/community/bot/requirements.txt"

say "5/6  .env を確かめます"
if [ ! -f "$APP/.env" ]; then
    cat > "$APP/.env" <<'EOF'
DISCORD_BOT_TOKEN=ここにDiscordのトークン
OPENAI_API_KEY=ここにOpenAIのキー
EOF
    echo "  ひな型を作りました。中身をまだ書いていません。"
    echo "  → nano $APP/.env  で2行を書き換えてから、もう一度このスクリプトを流してください。"
    chown "$USER_NAME:$USER_NAME" "$APP/.env"
    chmod 600 "$APP/.env"
    exit 0
fi
if grep -q "ここに" "$APP/.env"; then
    echo "  .env がひな型のままです。"
    echo "  → nano $APP/.env  で2行を書き換えてから、もう一度流してください。"
    exit 1
fi
chown "$USER_NAME:$USER_NAME" "$APP/.env"
chmod 600 "$APP/.env"        # 本人以外は読めないように

say "6/6  常駐させます"
cp "$APP/community/deploy/rakuraku-bot.service" /etc/systemd/system/
cp "$APP/community/deploy/backup_state.sh" /usr/local/bin/
chmod +x /usr/local/bin/backup_state.sh
# 記録のバックアップを、毎朝3:30に。
# _shiori_state.json が消えると、同じ人に二度DMが飛ぶ。それを防ぐため
( crontab -l 2>/dev/null | grep -v backup_state.sh ; \
  echo "30 3 * * * /usr/local/bin/backup_state.sh" ) | crontab -
systemctl daemon-reload
systemctl enable rakuraku-bot >/dev/null 2>&1
# ⚠️ enable --now だけだと、すでに動いている時に**新しいコードが読み込まれない**。
# 入れ直しのために流すことがほとんどなので、必ず restart する
systemctl restart rakuraku-bot
sleep 8

echo ""
echo "========================================"
systemctl is-active --quiet rakuraku-bot \
  && echo "判定: ✅ 動いています" \
  || echo "判定: ❌ 起動できていません。journalctl -u rakuraku-bot -n 30 を見てください"
echo "========================================"
echo ""
journalctl -u rakuraku-bot -n 15 --no-pager || true
