#!/usr/bin/env bash
# SessionEnd hook: prompt for the modules studied in this session, then append
# a record to ~/.claude-howto-progress.json.

set -euo pipefail

PROGRESS_FILE="$HOME/.claude-howto-progress.json"

# 只在 claude-howto 仓库里运行，避免全局安装后影响其他项目。
if [[ "${CLAUDE_PROJECT_DIR:-}" != *"claude-howto"* ]] && [[ "$PWD" != *"claude-howto"* ]]; then
  exit 0
fi

# hooks 的 stdin 用来接收 JSON payload，交互输入必须显式走 /dev/tty。
if [ ! -r /dev/tty ]; then
  exit 0
fi

if [ ! -f "$PROGRESS_FILE" ]; then
  printf '{"sessions":[]}\n' > "$PROGRESS_FILE"
fi

DATE=$(date +"%Y-%m-%d")
TIME=$(date +"%H:%M")

printf '\n'
printf 'Claude Code 学习会话结束\n'
printf '%s %s\n' "$DATE" "$TIME"
printf '\n'
printf '这次学了哪些模块？例如 06,07；直接回车表示跳过。\n'
printf '01=Slash  02=Memory  03=Skills  04=Subagents  05=MCP\n'
printf '06=Hooks  07=Plugins 08=Checkpoints 09=Advanced 10=CLI\n'
printf '> '
read -r INPUT </dev/tty

if [ -z "$INPUT" ] || [ "$INPUT" = "skip" ]; then
  printf '已跳过，本次不记录。\n\n'
  exit 0
fi

printf '备注？可直接回车跳过：'
read -r NOTES </dev/tty

python3 - "$PROGRESS_FILE" "$INPUT" "$NOTES" <<'PYEOF'
from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

path = Path(sys.argv[1])
raw_modules = sys.argv[2]
notes = sys.argv[3]

module_map = {
    "01": "01-slash-commands",
    "02": "02-memory",
    "03": "03-skills",
    "04": "04-subagents",
    "05": "05-mcp",
    "06": "06-hooks",
    "07": "07-plugins",
    "08": "08-checkpoints",
    "09": "09-advanced-features",
    "10": "10-cli",
}

modules = [
    module_map.get(part.strip(), part.strip())
    for part in raw_modules.split(",")
    if part.strip()
]

try:
    data = json.loads(path.read_text(encoding="utf-8"))
except (OSError, json.JSONDecodeError):
    data = {"sessions": []}

now = datetime.now()
data.setdefault("sessions", []).append(
    {
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M"),
        "modules": modules,
        "notes": notes,
    }
)

path.write_text(
    json.dumps(data, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)
PYEOF

printf '\n已保存到 %s\n' "$PROGRESS_FILE"
if [ -n "$NOTES" ]; then
  printf '备注：%s\n' "$NOTES"
fi
printf '\n'

exit 0
