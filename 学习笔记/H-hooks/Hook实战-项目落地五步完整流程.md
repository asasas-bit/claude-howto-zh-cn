# Hook 实战：项目落地五步完整流程

- **日期**：2026-09-09
- **分支**：study-notes
- **学习起因**：在「Hooks 答疑」解决了原理问题之后，进一步梳理「在一个真实项目里从 0 到跑通」的落地步骤；结合 `logs/file-changes.log` 练手钩子的完整闭环实测

---

## 先弄清楚两件事再动手

hook 永远由**两半**组成，缺一不可：

| 半 | 是什么 | 写在哪 |
|---|---|---|
| ① 触发器配置 | "什么事件发生、动哪个脚本" | `settings.json` 里 |
| ② 动作脚本 | "触发后具体干什么" | 一个 `.sh` 文件 |

很多人学 hook 卡住，就是只盯着脚本看，不知道它的"原材料"（输入数据）是从哪来的——**Claude Code 通过 stdin 喂给它一段 JSON**，脚本开场必须先把这段 JSON 读进来。这件事搞清楚了，后面就顺了。

---

## 五步流程

### 第 1 步：想清楚这个 hook 要解决什么问题

先问自己三句话：

- **我想在什么时候动手？**（工具跑之前 / 跑完之后 / 会话结束时）
- **我盯哪类操作？**（写文件、跑命令、读文件、提交 prompt）
- **我想要什么结果？**（自动补救 / 直接拦住 / 通知一声 / 记一笔）

这三个答案一出来，事件名、matcher、脚本逻辑就基本定了。

常见场景速查：

| 场景 | 事件 | matcher | 脚本干什么 |
|---|---|---|---|
| 提交前跑测试，不通过就拦 | `PreToolUse` | `Bash`（脚本内判断 `git commit`） | 跑 `npm test`，exit 2 阻断 |
| 写完文件自动格式化 | `PostToolUse` | `Write\|Edit` | 调 prettier/black |
| 追踪 Claude 改了哪些文件 | `PostToolUse` | `Write\|Edit` | 记日志 |
| 会话结束时问一句"今天学了啥" | `SessionEnd` | `*` | 读 `/dev/tty` 交互，写入进度文件 |
| 拦截高危命令 | `PreToolUse` | `Bash`（脚本内判断 `rm -rf` 等） | exit 2 阻断 |

---

### 第 2 步：选一个零依赖场景，从简单版开始写脚本

hook 脚本不需要任何外部依赖，只要四步就能跑：

```bash
INPUT=$(cat)                    # ① 读 stdin 的 JSON
FILE_PATH=$(echo "$INPUT" | sed -n 's/.*"file_path"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -1)  # ② 抠出关键字段
[ -z "$FILE_PATH" ] && exit 0   # ③ 守卫：没我的事就安静下班
TOOL_NAME=$(echo "$INPUT" | sed -n 's/.*"tool_name"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -1)
echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$TOOL_NAME] $FILE_PATH" >> "$LOG_DIR/file-changes.log"  # ④ 干活
exit 0                          # ⑤ 收工：exit 0 = 放行，exit 2 = 硬拦
```

这个骨架能应付**所有**基于文件的 hook 场景。换功能只换最后一行，配置一动不动。

> **sed 那行为什么像天书？** 它就是在 JSON 里找到 `"file_path": "xxx"`，把 `xxx` 抠出来。`\(` 和 `\)` 是"抓包"，把引号里的内容记住；`\1` 是把抓到的内容吐出来。相当于"从快递单上抠出收件地址那一栏"。

---

### 第 3 步：先手动喂 JSON 测，不要等 Claude 触发

养成习惯：写完脚本不依赖 Claude，自己构造 JSON 先测通。这是排查"hook 为啥没反应"最快的一招。

```bash
# 模拟 Write 工具的输入
echo '{"tool_name":"Write","tool_input":{"file_path":"test.py"}}' \
  | bash .claude/hooks/write-logger.sh

# 模拟 Edit 工具的输入
echo '{"tool_name":"Edit","tool_input":{"file_path":"test.py"}}' \
  | bash .claude/hooks/write-logger.sh

# 验证结果
cat logs/file-changes.log
```

看到日志里多了对应行，说明脚本本身没问题。这一步通了，再挂配置。

---

### 第 4 步：把触发器挂进 settings.json

触发器配置是一个 JSON 块，放在 `hooks` 字段下。放在哪张配置文件里，取决于"给谁用"：

| 场景 | 配置写哪 | 进不进 git |
|---|---|---|
| 只给我自己练手 | `.claude/settings.local.json` | 不进（已被 .gitignore 忽略） |
| 团队共享，同事 clone 下来就有 | `.claude/settings.json` | 两个都提交 |
| 所有项目全局生效 | `~/.claude/settings.json` | 跟仓库无关 |

一个具体配置示例（就是我们这次装的）：

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR/.claude/hooks/write-logger.sh\"",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

逐字段说明——**这些 key 一个字都不能改，是协议**：

- `PostToolUse`：事件名，"工具执行完之后"触发
- `"Write|Edit"`：matcher（正则），只盯 Write 和 Edit 工具
- `type: "command"`：跑本地 shell 命令
- `"$CLAUDE_PROJECT_DIR/..."`：项目根目录变量，换电脑也不废
- `timeout: 10`：10 秒没跑完就杀掉，防止脚本卡死把 Claude 也卡住

> **为什么用 PostToolUse 而不是 PreToolUse？** 我们在文件**写完之后**才记录——文件还没落地，你记录的是空气。事件选前还是选后，就看你想"拦在动作前"还是"跟在动作后收拾/记录"。

---

### 第 5 步：重启会话，真实触发，看结果落地

配置改完后，当前会话有时能热加载，稳妥起见：

1. 新开一个 Claude Code 会话（或者在当前会话里让它写/改一个文件）
2. 查看日志有没有新行

这一步是**完整的闭环验证**：配置 → 事件触发 → 脚本执行 → 结果落地。跑通之后，将来改脚本逻辑、换触发工具，都照着这个闭环重跑一遍。

---

## 补充：hook 怎么"回话"给 Claude

脚本跑完后，用两种方式告诉 Claude 结果：

| 退出码 | 含义 | 场景 |
|---|---|---|
| `exit 0` | 成功/放行 | 日常干活、不拦 |
| `exit 2` | **硬阻断**（必须同时向 stderr 写原因） | `echo "危险！" >&2; exit 2` |
| stdout 输出 JSON | 不拦，但给 Claude 递小纸条 | `{"hookSpecificOutput":{"additionalContext":"..."}}` |

> ⚠️ **最容易踩的坑**：`exit 1` 在 hook 协议里**不等于阻断**。很多人写 `exit 1` 想拦住危险操作，结果命令还是执行了——只有 `exit 2` 才是真正的阻断。

---

## 五步全流程回顾

```
① 想清楚：事件（前/后）+ matcher（盯哪个工具）+ 想要什么结果
② 写脚本：开场读 stdin → 守卫判断 → 干活 → exit 0/2
③ 先手动喂 JSON 测通，不等 Claude
④ 挂配置进 settings.json（选对文件：local / 项目 / 全局）
⑤ 重启会话，真实触发，看结果落地
```

跑通第一个 hook（哪怕只是记日志）之后，换成格式化、补拦截、加通知，都只是**换脚本里最后几行**的事，配置不用动。

---

## 本次实战成果

在 `claude-howto-zh-cn` 项目里实际落地了一套文件追踪 hook：

- 脚本：[.claude/hooks/write-logger.sh](../../.claude/hooks/write-logger.sh)
- 日志：[logs/file-changes.log](../../logs/file-changes.log)（不进 git）
- 说明：[logs/README.md](../../logs/README.md)
- 配置：`.claude/settings.local.json` 里的 `hooks` 段

实测完整闭环：Write → 自动记日志 → Edit → 再次自动记日志，Write/Edit 均可区分。
