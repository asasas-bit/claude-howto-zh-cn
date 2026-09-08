# Hooks 答疑：从事件、匹配器到 stdin JSON，逐行拆 format-code 脚本

- **日期**：2026-09-08
- **分支**：study-notes
- **学习起因**：用户问 hooks 怎么写，觉得 06-hooks 里的英文代码看不懂，要求挑一个案例拆开讲明白

---

我从 `06-hooks/` 的 10 个脚本里挑了 **[format-code.sh](../../06-hooks/format-code.sh)**（写完文件自动格式化）给你拆。理由是：它短（50 行）、骨架完整、没有吓人的正则，而且"自动格式化"这件事的价值一眼就能懂。`pre-commit.sh` 虽然是官方推荐第一例，但里面有一行 3 屏幕长的 git 匹配正则，入门看那个容易直接劝退。

---

## 一、先立心智模型：hook 到底是个啥？

你可以把 Claude Code 想成一个**新来的、干活特别快但需要你定规矩的员工**：

- **slash command** 是你**主动喊他**："去，把这事办了"
- **CLAUDE.md** 是贴在墙上的**员工守则**：他每次开工前自己读
- **hook** 是你装在办公室里的**自动门禁/自动质检岗**：你不用喊，**只要某件事发生，它就自动触发**

比如："Claude 每次写完一个文件，自动跑一遍格式化"——这就是一个 hook。

一个 hook 永远是**两半**组成的：

| 半 | 是什么 | 写在哪 |
|---|---|---|
| ① 触发器配置 | "什么事件发生时、动哪个脚本" | `settings.json` 里的 `hooks` 段 |
| ② 动作脚本 | "触发后具体干什么" | 一个 `.sh`（或 `.py`）脚本文件 |

很多人学 hooks 卡住，是因为只盯着脚本看，不知道**脚本的"饭"（输入数据）是 Claude Code 从 stdin 喂给它的**。这个讲完你就通了。

---

## 二、第一半：触发器配置长什么样

假设把 [format-code.sh](../../06-hooks/format-code.sh) 装到项目里，配置（放在 `.claude/settings.local.json` 里，个人练手用这个文件，不会被 git 提交）是：

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR/.claude/hooks/format-code.sh\"",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

逐字段翻译（**这些 key 一个字都不能翻、不能改**，它们是协议）：

- `hooks`：hook 配置的总入口
- `PostToolUse`：**事件名** = "工具执行完之后"。这是"什么时候触发"。常见的就四个：
  - `PreToolUse`：工具**动手前**（能拦住不让干）
  - `PostToolUse`：工具**干完后**（能补救、加工、记录）
  - `UserPromptSubmit`：你每次发消息时
  - `SessionStart` / `SessionEnd`：会话开始/结束
- `matcher`：**匹配哪个工具**。`"Write|Edit"` 是正则，意思是"写文件或改文件时"；`"Bash"` 就是只盯命令行；`"*"` 是全部
- `type: "command"`：hook 类型是"跑一条本地命令"（还有 http、prompt 等类型，新手先不管）
- `command`：要跑的脚本路径。`$CLAUDE_PROJECT_DIR` 是 Claude Code 自动给的变量=项目根目录，这样写不怕项目挪位置
- `timeout`：30 秒没跑完就杀掉，防止脚本卡死把 Claude 也卡住

**为什么选 PostToolUse 而不是 PreToolUse？** 因为格式化必须在文件**写完之后**做——文件还没落地，你格式化空气呢。事件选前还是选后，就看你想"拦在动作前"还是"跟在动作后收拾"。

---

## 三、关键中的关键：数据是怎么流进脚本的

Claude 写完一个文件，比如 `hello.py`，Claude Code 会在背后做这件事：

1. 准备一张"施工单"（一段 JSON），大致长这样：

```json
{
  "session_id": "abc123",
  "tool_name": "Write",
  "tool_input": {
    "file_path": "d:/cc/demo/hello.py",
    "content": "print( 1 )"
  }
}
```

2. 把这段 JSON 从脚本的 **stdin**（标准输入）喂进去——就像管道里灌水一样
3. 脚本干完活，用两种方式回话：
   - **退出码**（exit code）：0 = 放行；**2 = 阻断**（理由要写进 stderr）
   - **stdout 输出 JSON**：可以给 Claude 递补充信息（后面讲）

所以每个 hook 脚本的开场永远是同一招：**先把 stdin 里的 JSON 读进来**。

---

## 四、逐行拆 format-code.sh

脚本全文在 [06-hooks/format-code.sh](../../06-hooks/format-code.sh)，我们一段一段来。

### 第 1 段：声明 + 读入

```bash
#!/bin/bash
# Auto-format code after writing
# Hook: PostToolUse (matcher: Write)

INPUT=$(cat)
```

- `#!/bin/bash`：告诉系统"用 bash 来跑我"。照抄即可
- `#` 开头是注释，给人看的，机器不执行
- **`INPUT=$(cat)`**：这是全篇最重要的一行。`cat` 会把 stdin 的内容全部读出来，`$(...)` 是"把命令的结果存进变量"。整句意思：**把 Claude Code 喂进来的那段 JSON 整个存进变量 `INPUT`**

### 第 2 段：从 JSON 里把文件路径"抠"出来

```bash
FILE_PATH=$(echo "$INPUT" | sed -n 's/.*"file_path"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -1)
```

这是最像天书的一行，拆开看其实就是"**从快递单上抠出收件地址那一栏**"：

- `echo "$INPUT"`：把 JSON 文本吐出来
- `|`：管道，把前面的输出传给后面
- `sed -n 's/旧/新/p'`：sed 是文本替换工具，`s/旧/新/` 是替换，`p` 表示"替换成功了才打印"，`-n` 配合 p 只打印匹配行
- 匹配规则 `.*"file_path"[[:space:]]*:[[:space:]]*"\([^"]*\)".*`：
  - `.*` = 随便什么字符
  - `"file_path"` = 找到这个栏位名
  - `[[:space:]]*:[[:space:]]*` = 冒号，前后允许有空格
  - `"\([^"]*\)"` = 引号里的内容；`\( \)` 是"**抓包**"，把这部分记住；`[^"]*` = 一串"不是引号的字符"（也就是路径本身）
  - 后面 `.*` = 剩下的全部
- `\1`：把刚才"抓包"抓到的那串内容吐出来
- `head -1`：只要第一个匹配

连起来：**在 JSON 里找到 `"file_path": "xxx"`，把 `xxx` 抠出来存进 `FILE_PATH`**。

> 补充：用 sed 抠 JSON 是个"土办法"，好处是 Windows Git Bash 里也一定有 sed，不依赖 jq。同目录 [pre-commit.sh](../../06-hooks/pre-commit.sh) 演示了更稳的写法：有 jq 用 jq，没有就用 python3 兜底。你初学照抄 sed 就行，文件路径里不会有引号，土办法完全够用。

### 第 3 段：守卫——没活就安静下班

```bash
if [ -z "$FILE_PATH" ] || [ ! -f "$FILE_PATH" ]; then
  exit 0
fi
```

- `-z "$FILE_PATH"`：变量是空的（没抠到路径）
- `! -f "$FILE_PATH"`：这个路径文件不存在
- 两种情况任一成立，就 `exit 0`（正常退出，啥也不拦）

这叫"守卫语句"：**不关我的事就赶紧安静走人，别添乱**。hook 会被非常频繁地触发，"没事不吭声"是基本修养。

### 第 4 段：按后缀分拣，各找各的格式化工具

```bash
case "$FILE_PATH" in
  *.js|*.jsx|*.ts|*.tsx)
    if command -v prettier &> /dev/null; then
      prettier --write "$FILE_PATH" 2>/dev/null
    fi
    ;;
  *.py)
    if command -v black &> /dev/null; then
      black "$FILE_PATH" 2>/dev/null
    fi
    ;;
  # …go / rust / java 同理…
esac

exit 0
```

- `case ... in` 就是"按模式分流"，像快递按省份分拣：`.js/.ts` 走 prettier 那条线，`.py` 走 black 那条线
- `command -v prettier`：检查电脑里**装没装** prettier，装了返回成功、没装返回失败
- `&> /dev/null`：把检查命令的输出丢进"黑洞"（`/dev/null`），我们只想知道成败，不想看它啰嗦
- 所以这句的意思是：**装了 prettier 就跑，没装就跳过，绝不报错**
- `2>/dev/null`：格式化工具自己的报错也丢黑洞，别刷屏
- 最后 `exit 0`：收工，放行

这个脚本的完整"人生轨迹"就是：

> 读 JSON → 抠出文件路径 → 没路径/文件不存在就下班 → 看后缀选格式化工具 → 装了工具就跑，没装就跳过 → 退出

---

## 五、另一半本事：hook 怎么"回话"给 Claude

format-code.sh 只演示了"闷头干活"。hook 还有三种回话方式，都在同目录别的例子里，你现在只需记这张表：

| 你想干嘛 | 怎么做 | 例子出处 |
|---|---|---|
| 没事/活干完了，放行 | `exit 0` | 所有脚本 |
| **硬拦住，不让干** | 理由写进 stderr（`echo "..." >&2`）+ **`exit 2`** | [pre-commit.sh:42-44](../../06-hooks/pre-commit.sh#L42-L44) |
| **不拦，但给 Claude 递小纸条**提醒它 | stdout 输出 JSON：`{"hookSpecificOutput":{...,"additionalContext":"..."}}` | [validate-prompt.sh:50](../../06-hooks/validate-prompt.sh#L50) |

⚠️ **最大的坑**：退出码里**只有 `exit 2` 是阻断**。有些人想拦危险命令，写了 `exit 1`，结果命令照样执行——因为 `exit 1` 在 hook 协议里只是"脚本自己出错了"，**不拦** Claude。这个坑 README 里专门强调过。

举个"硬拦"的实际样子（pre-commit.sh 的核心三行）：

```bash
if ! npm test; then
  echo "❌ 测试没过！提交被拦住。" >&2   # >&2 = 写进 stderr
  exit 2                                  # 2 = 阻断，git commit 不许执行
fi
```

"递小纸条"的样子（validate-prompt.sh 里：你说要重构，但项目里没有 tests 目录，它不拦你，只提醒 Claude 一句）：

```bash
printf '{"hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": "警告：用户要重构，但没有 tests 目录，请提醒他确认回滚方案。"}}'
```

Claude 会把这张纸条当额外背景读进去，然后自己决定怎么做。

---

## 六、你在 Windows 上，这几件事提前知道

1. **脚本靠 Git Bash 跑**。你机器上有 Git Bash（我这个会话里的 Bash 工具就是），`#!/bin/bash` 的脚本可以直接用，不用装 WSL
2. **脚本要可执行**。在 Git Bash 里 `chmod +x .claude/hooks/xxx.sh` 一下
3. **脚本里调用的工具必须在 PATH 里**。format-code.sh 调 `prettier`/`black`，你没装的话，`command -v` 检查会让它**静默跳过**——所以这个 hook 装完"看起来没反应"很可能只是你没装格式化工具，不是坏了
4. **路径用 `$CLAUDE_PROJECT_DIR`**，别写死，换项目/换电脑就废
5. **调试神器**：不用等 Claude 触发，你可以**手动喂 JSON 测脚本**：

```bash
echo '{"tool_input":{"file_path":"hello.py"}}' | bash .claude/hooks/format-code.sh
```

能跑通再装进 settings.json，这是排查"hook 为啥不生效"最快的办法。

---

## 七、建议你的第一个 hook：零依赖，立刻能看到效果

format-code.sh 依赖 prettier/black，新手装完没反馈容易怀疑人生。建议你先写一个**啥依赖都不要**的："Claude 每次写完文件，往日志里记一笔"。

新建 `.claude/hooks/write-logger.sh`：

```bash
#!/bin/bash
# 练手 hook：Claude 每次写/改文件，记一笔到日志
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | sed -n 's/.*"file_path"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -1)
[ -z "$FILE_PATH" ] && exit 0
echo "[$(date '+%H:%M:%S')] Claude 写了文件: $FILE_PATH" >> "$HOME/claude-hooks-debug.log"
exit 0
```

配置进 `.claude/settings.local.json`（把上一节那段 JSON 的 command 换成这个脚本路径，matcher 用 `Write|Edit`），然后让我随便写个文件，再跑：

```bash
cat ~/claude-hooks-debug.log
```

看到日志里多了一行，你就**亲手跑通了一个 hook 的完整闭环**。跑通之后再换 format-code.sh，只是把"记日志"换成"调格式化工具"而已，骨架一模一样。

---

## 八、自测题（用你自己的话答，答完我判）

1. 你想让 Claude 每次写完 `.py` 文件自动跑 `black`，事件该选 `PreToolUse` 还是 `PostToolUse`？matcher 写什么？
2. 你写了个 hook 想拦截 `rm -rf`，脚本里写的是 `echo "危险！" >&2; exit 1`，结果命令还是执行了。为什么？改成什么？
3. 你不想硬拦 Claude，但希望它每次提到"删库/生产部署"时，自动收到一句"请先确认备份"的提醒——该用 `exit 2` 还是 stdout JSON 的 `additionalContext`？
