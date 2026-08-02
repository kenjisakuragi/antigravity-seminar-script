#!/bin/bash
# botの記録ファイルを、毎日とっておく。
#
# なぜ要るか
#   _shiori_state.json には「誰にいつDMしたか」が入っている。
#   これが消えると、一度そっと声をかけた方に**もう一度同じDMが飛ぶ**。
#   いちばんやってはいけないことなので、壊れても戻せるようにしておく。
#
# 使い方（rootで1回だけ）
#   cp backup_state.sh /usr/local/bin/ && chmod +x /usr/local/bin/backup_state.sh
#   crontab -e で1行足す：
#     30 3 * * * /usr/local/bin/backup_state.sh
set -eu

SRC=/opt/rakuraku-bot/community/bot
DST=/opt/rakuraku-bot/_backup
KEEP=30                       # 30日ぶん持っておく

mkdir -p "$DST"
STAMP=$(date +%Y%m%d)

for f in _shiori_state.json _morning_state.json; do
    [ -f "$SRC/$f" ] && cp "$SRC/$f" "$DST/${STAMP}_${f}"
done

# 古いものを消す
find "$DST" -name '*_state.json' -mtime +$KEEP -delete

echo "$(date '+%F %T') backup ok"
