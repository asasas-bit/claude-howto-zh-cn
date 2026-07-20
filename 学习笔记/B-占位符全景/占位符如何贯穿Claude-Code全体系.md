# 占位符如何贯穿 Claude Code 全体系

> **学习起因**：在学 slash command 的 `$ARGUMENTS`、`@path`、`` !`command` `` 之后，
> 想搞清楚这个"占位符"到底跟 Claude Code 的其他能力（skills、subagents、MCP、hooks、plugins）有没有关联。
> 结论：**关联极大，占位符是这些高级能力的"共同地基"**。
>
> **本文风格**：先给顶层公式 → 再讲基础分类 → 然后重点讲占位符如何贯穿六大模块 → 每个模块用生活类比 + 具体例子讲透 → 最后给一句总结。

---

## 目录

- [一、顶层公式：所有占位符做的是同一件事](#一顶层公式所有占位符做的是同一件事)
- [二、四大类占位符（按数据来源分）](#二四大类占位符按数据来源分)
- [三、能力矩阵：我已经练过的命令用了哪些占位符](#三能力矩阵我已经练过的命令用了哪些占位符)
- [四、占位符如何贯穿六大高级能力（核心）](#四占位符如何贯穿六大高级能力核心)
  - [4.1 占位符 → Skills：一套语法，两种触发](#41-占位符--skills一套语法两种触发)
  - [4.2 占位符 → Subagents：分包干活的完整链路](#42-占位符--subagents分包干活的完整链路)
  - [4.3 占位符 → MCP：从"读本地"跃迁到"调外部"](#43-占位符--mcp从读本地跃迁到调外部)
  - [4.4 占位符 → Hooks：反过来的预处理（顿悟点）](#44-占位符--hooks反过来的预处理顿悟点)
  - [4.5 占位符 → Plugins：把上面全部打包分发](#45-占位符--plugins把上面全部打包分发)
- [五、一句话总结 & 学习顺序建议](#五一句话总结--学习顺序建议)
- [六、常见坑](#六常见坑)

---

## 一、顶层公式：所有占位符做的是同一件事

所有你在 Claude Code 里见到的占位符、`@`、`!`、`${...}`，本质上都在做**同一件事**：

> **在把 prompt 送给模型之前，"预处理"一下 —— 把动态值填进去，把外部内容拉进来，把命令输出塞进来。**

一旦你抓住这个"**预处理**"的概念，后面 hooks、MCP、subagents、plugins 里所有类似的东西，你都能一眼看穿它在干嘛。

---

## 二、四大类占位符（按数据来源分）

按"符号形状"分容易记混，按"**数据从哪儿来**"分记得最牢：

| 数据来自哪里 | 代表符号 | 例子 |
|---|---|---|
| 🧑 **用户的输入** | `$ARGUMENTS`、`$0`/`$1` | 你在 `/command` 后面敲的字 |
| 📁 **文件内容** | `@path/to/file` | `@LOCALIZATION-STYLE.md` |
| ⚙️ **shell 命令的输出** | `` !`command` `` | `` !`git status` `` |
| 🌍 **系统内置变量** | `${CLAUDE_PROJECT_DIR}` 等 | 项目路径、会话 ID |

**核心**：不管形式怎么变，它们都是"**从外部世界拿数据填进 prompt**"。

---

## 三、能力矩阵：我已经练过的命令用了哪些占位符

这张表把我做过的命令跟占位符能力对应起来：

| 命令 | 场景 | `$ARGUMENTS` | `@file` | `!command` | `${VAR}` |
|---|---|:---:|:---:|:---:|:---:|
| `/git-safe-submit` | 提交代码 | ✅ | ❌ | ✅✅✅ (5 次) | ❌ |
| `/review-file`（练手） | 审查文档 | ✅ | ✅ | ✅ | ✅ |
| `/today`（自动日报） | 学习日报 | ✅ | ❌ | ✅✅✅ (5 次) | ❌ |

规律：

- **`$ARGUMENTS` 几乎每个命令都有** —— 因为几乎所有命令都需要"接受用户的一些输入"
- **`!command` 用得多的是"需要读环境状态"的命令**（git 状态、日期、搜索结果）
- **`@file` 用得多的是"要按某份规则/模板做事"的命令**（贴入风格规范、参考文档）
- **`${VAR}` 用得最少**，主要在需要绝对路径、跨平台脚本时才用

**给自己的启示**：设计命令时先问"**我需要什么数据？**"，再决定用哪种占位符。**别为了用而用**。

---

## 四、占位符如何贯穿六大高级能力（核心）

这是最关键的部分。占位符不是孤立的知识，它是一条主线，串起 Claude Code 几乎所有高级能力：

```
        用户敲一句话
             ↓
    ┌─────────────────────┐
    │  Slash Command      │ ← 我现在在这
    │  占位符预处理        │
    └─────────────────────┘
             ↓
    ┌─────────────────────┐
    │  Skills             │ ← 同样的占位符，但"自动触发"
    │  frontmatter + body │
    └─────────────────────┘
             ↓
    ┌─────────────────────┐
    │  Subagents          │ ← 把预处理后的 prompt 派给独立 AI
    └─────────────────────┘
             ↓
    ┌─────────────────────┐
    │  MCP                │ ← 数据源从"本地"升级到"远程服务"
    └─────────────────────┘
             ↓
    ┌─────────────────────┐
    │  Hooks              │ ← 反过来：事件驱动的预处理
    └─────────────────────┘
             ↓
    ┌─────────────────────┐
    │  Plugins            │ ← 把上面全部打包分发
    └─────────────────────┘
```

下面挨个讲连线。

---

### 4.1 占位符 → Skills：一套语法，两种触发

#### 通俗类比：闹钟 vs 便利贴

- **Slash Command 就像一张贴在冰箱上的"便利贴"**  
  你路过看到 "该收快递了"，你**主动**做这件事。什么时候做？你决定。

- **Skill 就像手机上的"智能闹钟"**  
  它有一堆"什么时候响"的规则（比如"上班日早上 7 点、周末 8 点、天气坏了提前 15 分钟"）。你不用去按它，**它根据条件自己响**。

**关键点**：闹钟和便利贴写的内容可以一模一样（"该收快递了"），**区别只是谁来触发**。

Skill 和 slash command 就是这个关系 —— **写的内容基本一样，触发方式不同**：

- Slash command → 你输 `/xxx` 触发
- Skill → AI 看你说的话，觉得匹配 `description` 就自己触发

#### 具体例子对比：同样一件事，两种写法

**假设需求**：读取项目里的 `LOCALIZATION-STYLE.md`，让 AI 按里面的规则给一段话做本地化审查。

**写法 A：Slash Command**（在 `.claude/commands/audit.md`）

```markdown
---
name: audit
argument-hint: <要审查的文字>
description: 按项目本地化规则审查一段文字
---

请按以下规则审查用户的这段文字：

@LOCALIZATION-STYLE.md

用户要审查的内容：

$ARGUMENTS
```

**怎么用**：主动敲 `/audit 这里放要审查的中文...`

**写法 B：Skill**（在 `.claude/skills/localization-auditor/SKILL.md`）

```markdown
---
name: localization-auditor
description: 当用户想审查一段中文翻译是否符合项目本地化规则时使用。检查术语保留、frontmatter 未误翻等。
---

请按以下规则审查用户提供的中文文字：

@${CLAUDE_SKILL_DIR}/references/LOCALIZATION-STYLE.md

用户会自然语言告诉你要审查什么，你直接开始工作。
```

**怎么用**：直接说人话 —— "帮我看看这段翻译有没有踩坑：..."，AI 读到你的话，觉得匹配 description，**自动**加载这个 skill。

#### 三个 skill 独有的能力（slash command 没有）

**① `${CLAUDE_SKILL_DIR}` —— 引用 skill 自己带的资源**

Skill 是**一个目录**，可以带子文件（模板、规则、示例）：

```
.claude/skills/localization-auditor/
├── SKILL.md
├── references/
│   ├── LOCALIZATION-STYLE.md    ← skill 自带的规则文件
│   └── terms-whitelist.md
└── templates/
    └── report-template.md
```

在 SKILL.md 里可以写：

```markdown
@${CLAUDE_SKILL_DIR}/references/LOCALIZATION-STYLE.md
@${CLAUDE_SKILL_DIR}/templates/report-template.md
```

**这个能力 slash command 没有** —— slash command 是单文件，没自己的家。

**实用价值**：可以把一个 skill 打包成一个"完整的能力包"，包括规则、模板、示例，分享给同事，别人 `cp -r` 整个目录就能用，不依赖项目里其他文件。

**② `${CLAUDE_EFFORT}` —— 根据"思考力度"调策略**

Claude Code 有 `low / medium / high / max` 四档 effort。skill 里可以判断：

```markdown
当前思考力度：${CLAUDE_EFFORT}

- 如果是 low：只做最基本的检查，输出 3 条最重要的问题
- 如果是 high：做完整审查，包括边缘情况
```

**③ 多个 skill 可以叠加，占位符各自独立预处理**

多个 skill 同时激活时，每个 skill 里的占位符**各自独立预处理**，然后拼在一起交给 AI。

#### 什么时候选 skill 而不是 command？

| 你希望怎样触发？ | 选谁 |
|---|---|
| "我要主动做这件事，比如提交代码" | Slash Command |
| "遇到某类问题时希望 AI 自动帮我做" | Skill |
| "有一堆配套模板 / 参考文件要一起带走" | Skill（因为目录结构） |
| "只是一段 prompt 快捷方式" | Slash Command 更轻 |

**记住这个心智模型**：**"skill = slash command + 目录 + 自动触发"**。掌握 slash command，学 skill 就是"再加两个能力"，不是从零学。

---

### 4.2 占位符 → Subagents：分包干活的完整链路

#### 通俗类比：项目经理 vs 专家团队

想象你是**项目经理**，接了个大活儿。你能一个人干完吗？可以，但会很累，脑子里要同时装十几件事。

聪明的做法是**分包**：

> "小张，你负责审查代码质量；小李，你负责跑测试；小王，你负责写文档。"
>
> 每个人都是**独立的专家**，脑子里只装自己那部分事，做完汇报给你。

**Subagent 就是你能"雇佣的专家团队"**。你（主 Claude）是项目经理，你把某个专业任务派给一个专门的 subagent，它在**自己的独立上下文**里干活，干完把结果给你。

#### 关键洞察：占位符是"派活时的任务简报"

主 Claude → subagent 派活时，会传给它一份"任务简报"。**这份简报就是 subagent 的 prompt**，而这个 prompt **就是用占位符预处理出来的**。

#### 完整例子：一个 code-reviewer subagent

在 `.claude/agents/code-reviewer.md`：

```markdown
---
name: code-reviewer
description: 独立审查代码 diff，返回问题清单
---

你是一个专注、严格的代码审查员。

## 你要审查的 diff

!`git diff HEAD~1`

## 团队的编码规范

@CONVENTIONS.md

## 已知的高风险文件

@.risk-files.txt

## 你的任务

审查上面的 diff，按下面格式返回结果：

- 🔴 严重问题（可能引起 bug）
- 🟡 一般问题（风格或最佳实践）
- 🟢 良好实践（可选，鼓励）

不要修改任何文件，只审查。
```

#### 派活时发生了什么？逐步拆解

- **Step 1**：主对话说 "帮我审查一下最近的改动"
- **Step 2**：主 Claude 判断"这活适合派给 code-reviewer"，准备派活
- **Step 3**：**Claude Code 先做占位符预处理**：
  - `` !`git diff HEAD~1` `` → 真的跑 git 命令，输出 200 行 diff 内容
  - `@CONVENTIONS.md` → 读那个文件的完整内容
  - `@.risk-files.txt` → 读风险文件清单
- **Step 4**：预处理完的**完整 prompt**（大约 5000 字）传给 subagent，subagent 在**全新的上下文**里开工
- **Step 5**：subagent 干完活，只把**审查结果**（不到 500 字）返回给主 Claude。**它自己那 5000 字的上下文，主对话根本看不到**
- **Step 6**：主 Claude 把这个精简结果转达给用户

#### 为什么这个流程很关键？

**核心价值：上下文隔离**

主对话里，你可能已经聊了 20 轮，上下文很珍贵。如果主 Claude 自己审查代码，那 5000 字的 diff + 规范文件都会占用主上下文。

用 subagent 之后：

- 主对话只多了一句 "审查结果：X、Y、Z"
- 那些临时用的文件、diff、规范，都留在 subagent 的"独立房间"里，用完就丢

**类比**：就像给助理打电话说 "小王，帮我看一下这份 100 页的合同"。小王读完给你 3 句话总结，那 100 页你根本不用看。

#### 占位符在这里的价值

**写 subagent 定义时**，占位符让你可以：

1. **动态传入实时数据**（`!command`）—— 每次派活时的 git diff 都不一样
2. **注入长文档**（`@file`）—— 规范文件几千字，不用每次复制粘贴
3. **接受主 Claude 传入的参数**（`$ARGUMENTS`）—— 主 Claude 可以说 "只审查 auth 模块，忽略 test 目录"

**如果没有占位符**：就得**手动**在 subagent 定义里写死所有信息，那 subagent 就变成了一个"死板的、不能变化的助手"，几乎没用。

**结论**：**占位符让 subagent 从"静态模板"变成"动态智能体"**。

---

### 4.3 占位符 → MCP：从"读本地"跃迁到"调外部"

#### 通俗类比：家里的书柜 vs 图书馆的联网检索

**占位符的 `@file` 和 `!command`**，就像你**家里书柜上的书** —— 能读的东西，都在你这台电脑上（本地文件、本地能跑的命令）。

**MCP** 就像办了**图书馆的联网检索卡**：

- 可以查国家图书馆的书（GitHub API）
- 可以查医学数据库（PubMed）
- 可以查地图（Google Maps）
- 也可以自己建一个小图书馆让别人查（自建 MCP server）

**核心飞跃**：数据源从"你的电脑"扩展到"**任何有 API 的服务**"。

#### 具体对比：查 GitHub PR 状态

**问题**：想让 AI 帮忙回顾 "昨天提交的那个 PR 有没有人 review 了"。

**用占位符做**（能不能做？勉强）：

```markdown
GitHub PR 状态：!`gh pr view 123 --json state,reviews`
```

问题：

- 得先装 `gh` 命令行工具
- 得手动配 GitHub token
- 命令输出是 JSON 字符串，AI 得自己解析
- 换个仓库、换个 PR 号，命令都要重写
- 想查更复杂的东西（比如"我所有分配给我的 issue"），命令会写到怀疑人生

**用 MCP 做**：

配置一下 GitHub MCP server，然后直接说：

> "帮我看看昨天那个 PR 的 review 状态"

AI 通过 MCP 直接调用 GitHub API，**结构化返回**：

```json
{
  "number": 123,
  "state": "open",
  "reviews": [
    { "author": "alice", "state": "approved", "at": "2h ago" },
    { "author": "bob", "state": "changes_requested", "at": "30m ago" }
  ]
}
```

AI 拿到这个结构化数据，直接告诉你 "Alice 批准了，Bob 请求改动 —— 要不要看看 Bob 的意见？"

#### 关键区别：静态 vs 动态

**占位符**（`@file`、`!command`）：**静态注入**

- 命令跑起来的**那一瞬间**，值就被填死
- 之后 AI 就算想"再查一次"，也做不到（除非再跑一次命令）

**MCP**：**动态查询**

- AI 在对话过程中**随时可以问**
- 可以**来回多轮**：先查 PR 列表 → 挑一个感兴趣的 → 再查它的详情 → 再查评论 → ...
- 每一次查询都是**实时的**

**一句话概括**：

> **占位符是"临出发前塞进背包的东西"，MCP 是"随时能打电话问的顾问"。**

#### 底层其实是同一种思想

**都是"给 AI 补充外部世界的信息"。**

MCP 可以理解为：**"高级版的 `!command`"**。

| | `!command` | MCP |
|---|---|---|
| 触发时机 | 命令加载时一次 | AI 需要时随时 |
| 数据源 | 本地 shell | 任何 API |
| 数据格式 | 文本 | 结构化 JSON |
| 认证 | 命令自己搞（token 在环境变量） | MCP server 统一管理 |
| 交互 | 单向（跑完就完） | 双向（AI 可以带参数问） |

#### 什么时候升级到 MCP？

出现下面这些信号时，就该考虑 MCP：

- 你的 `` !`command` `` 越写越复杂，一行变三行变十行
- 要处理的数据是外部服务的（GitHub、Slack、Notion、公司内网 API）
- 一个命令要"来回多轮"才能完成（先列出所有 PR，再挑一个看详情）
- 想让**多个 skill / command 共享同一个数据源**（不想每个都重复写 gh 命令）

**结论**：占位符是"能自己动手就自己动手"的初级方案；MCP 是"跟外部服务打交道"的正式方案。**先学占位符，是为了后面轻松理解 MCP** —— 你已经理解"给 AI 补数据"这件事了，MCP 只是升级了数据源。

---

### 4.4 占位符 → Hooks：反过来的预处理（顿悟点）

#### 通俗类比：门口的摄像头 vs 手写的便条

前面的 slash command / skill 都是**主动去干一件事**：你按钮，机器动。

**Hooks 是反过来的：机器观察你的行为，看到某个事件发生了，自动跑一段代码**。就像：

- 家门口装了个摄像头（hook）
- 检测到有人**推门**（PreToolUse 事件）→ 自动播放"欢迎光临"（跑你写的脚本）
- 检测到有人**离开**（Stop 事件）→ 自动关灯（跑你写的脚本）

**你从"操作者"变成了"设置规则的人"**。规则设好，之后的事你不用管。

#### Claude Code 里有哪些"事件"？

先建立印象，最常用的几个：

| 事件名 | 什么时候触发 |
|---|---|
| `SessionStart` | 每次会话开始时 |
| `PreToolUse` | AI 即将调用某个工具时（比如 Bash、Edit） |
| `PostToolUse` | AI 刚调用完某个工具时 |
| `Stop` | 一次会话结束时 |
| `UserPromptSubmit` | 用户按下回车提交问题时 |

#### 占位符和 hooks 什么关系？

**这里就是那个"顿悟点"**：

> **占位符和 hooks 其实是同一件事的两面**，只是**触发方向**反过来。
>
> - **占位符**：在 prompt 里写"预处理指令"，触发时机是"这个命令被调用"
> - **Hooks**：在系统配置里写"预处理指令"，触发时机是"某个事件发生"

**都是"预处理"，都是"往 AI 眼前塞东西"，只是"什么时候塞"由谁决定。**

#### 完整例子：用 hooks 实现 `/today` 自动化

`/today` 命令里埋了个 TODO："以后要自动化"。方案 A 就是用 hooks 实现"每次会话结束自动跑 `/today`"。

在 `.claude/settings.json` 里加：

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "cd ${CLAUDE_PROJECT_DIR} && claude -p '/today' --output-format text"
          }
        ]
      }
    ]
  }
}
```

**看这条完整的"预处理连锁链"** —— 有点长但很关键：

1. **你聊完天关掉 Claude Code**（触发 `Stop` 事件）
2. **系统检查 hooks 配置**，看到 `Stop` 里有一条命令要跑
3. **系统对这条命令做占位符替换**：
   - `${CLAUDE_PROJECT_DIR}` → 替换成 `D:\cc\claude-howto-zh-cn`
4. **执行**：`cd D:\cc\... && claude -p '/today' --output-format text`
5. **一个新的 Claude 进程被拉起来**，读到 `/today` 命令
6. **Claude Code 对 `/today.md` 做占位符替换**：
   - `` !`date +%Y-%m-%d` `` → `2026-07-20`
   - `` !`git log --since="1 day ago" --oneline` `` → 今天的 commit
   - 等等
7. **完整的 prompt 送给模型**
8. **模型生成日报**
9. **`/today` 命令定义里"第二步：自动归档"被执行**，写入 `学习笔记/Z-日报/2026-07-20-xxx.md`
10. **进程结束，Claude Code 主会话彻底关闭**

**看到没**？一条链上**至少两次占位符替换**：

- 第一次：hooks 系统在 shell 命令上替换 `${CLAUDE_PROJECT_DIR}`
- 第二次：`/today` 命令加载时替换 `` !command ``

**这就是"占位符思想的外层封装"**。不是学了新东西，是学了同一件事在**更外层**的应用。

#### 反方向的例子：hooks 也能拦截

`PreToolUse` 是个特别重要的 hook —— 它在 AI 即将执行某个工具前触发，**你可以决定放不放行**。

假设你不想让 AI 意外 `git push`：

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PROJECT_DIR}/scripts/block_push.sh"
          }
        ]
      }
    ]
  }
}
```

`block_push.sh` 脚本读取 AI 即将跑的命令，检查是不是 `git push`，如果是就返回一个"拒绝"信号。

**这里同样用到 `${CLAUDE_PROJECT_DIR}` 占位符** —— hooks 和 slash command 用的是**同一套占位符系统**，学一次到处用。

#### 总结：hooks 是把占位符思想"外置化"

三句话记住 hooks：

1. **触发者从你变成了事件**：不再是你敲 `/xxx`，而是系统看到某件事发生
2. **动作可以"拦截"**：不只是"塞数据进 AI"，还可以"阻止 AI 做某事"
3. **占位符依然生效**：`${CLAUDE_PROJECT_DIR}` 等在 hooks 配置里照样能用

**学完占位符再学 hooks，就是"从主动预处理"到"自动预处理"的一次自然升级**。

---

### 4.5 占位符 → Plugins：把上面全部打包分发

#### 通俗类比：单菜谱 vs 整套厨房套装

之前学的 command / skill / hook / MCP，每一个都是**一张菜谱**。自己家里做，够用。

**Plugin 就是"整套厨房套装"**：

- 一堆菜谱（commands）
- 一堆预设料理规则（skills）
- 自动化炊具（hooks）
- 联网订菜功能（MCP 配置）
- 一份说明书告诉你怎么用（README）

**打包成一个盒子，分享给同事、朋友、开源社区**。别人拿到这个盒子，`git clone` 一下就有全套厨房。

#### Plugin 目录结构

一个典型的 plugin 长这样（参考 [07-plugins/devops-automation/](../../07-plugins/devops-automation/)）：

```
devops-automation/
├── README.md              说明书
├── commands/              slash commands
│   ├── deploy.md
│   ├── rollback.md
│   └── incident.md
├── agents/                subagents
│   ├── alert-analyzer.md
│   └── deployment-specialist.md
├── hooks/                 hooks 配置
│   └── hooks.json
└── (可能还有 MCP 配置)
```

#### 占位符在 plugin 里的表现

**跟自己写的时候一模一样。** 打开 `commands/deploy.md`：

```markdown
---
name: deploy
allowed-tools: Bash(kubectl:*), Bash(git:*)
---

# 部署脚本

当前项目：${CLAUDE_PROJECT_DIR}
最近提交：!`git log --oneline -5`
用户传入的环境：$ARGUMENTS
```

看到没？**跟你自己在 `.claude/commands/git-safe-submit.md` 写的东西完全同一个套路**。

#### 但 plugin 里的占位符有一个"路径解析"的小细节

Plugin 里如果用 `@file`，路径解析有讲究：

- **绝对相对项目根**：`@LOCALIZATION-STYLE.md` → 用户项目的根目录
- **相对 plugin 自己**：`@${CLAUDE_PLUGIN_DIR}/templates/report.md` → plugin 自己带的模板

**为什么要有这个区分**？因为 plugin 是**别人**给你的，plugin 自己带的模板和你自己项目里的文件**不能混**：

- Plugin 自带的东西（规则、模板）→ 用 `${CLAUDE_PLUGIN_DIR}`
- 用户项目里的东西（代码、配置）→ 用相对路径或 `${CLAUDE_PROJECT_DIR}`

这个跟 skill 里 `${CLAUDE_SKILL_DIR}` 是完全一样的思想 —— **每个"能力包"都要能引用自己的东西**。

#### Plugin 的价值：可复制的最佳实践

假设你花一周时间在自己项目里搭好了这一套：

- `/git-safe-submit`
- `/today`
- `/review-file`
- 加上几个 skill 和一个 pre-commit hook

**朋友问你**："你这套 Claude Code 配置真好用，能给我一份吗？"

**没有 plugin 时**：得说"你复制 `.claude/commands/` 里的 xxx 文件，再复制 `.claude/skills/` 里的 xxx 文件，然后打开 `.claude/settings.json` 找到 hooks 那一段..." —— 折腾半小时都不一定装对。

**有了 plugin**：push 到 GitHub 上。朋友一句：

```bash
claude plugin install github.com/你/你的插件
```

**装完立刻能用**。所有占位符、所有 hooks、所有 skill 都跟你本地一样。

#### 结论：plugin 不是新知识，是打包工艺

**关键洞察**：**plugin 里没有一个你没学过的东西**。

- 占位符 —— 一样
- 命令定义 —— 一样
- skill 定义 —— 一样
- hook 定义 —— 一样

**plugin 只是"把这些东西按约定的目录结构组织好，加个 README，就能分发"**。

**学到 plugin 时的心态**应该是："哦，就是给我之前学的东西加个'包装外壳'"，而不是"又一个大新知识"。

---

## 五、一句话总结 & 学习顺序建议

### 总图

```
占位符（基础语法）
    │
    ├─→ Slash Command  = 你主动触发的预处理
    ├─→ Skill          = 系统自动触发的预处理 + 可带目录
    ├─→ Subagent       = 预处理结果派给独立 AI
    ├─→ MCP            = 数据源从本地升级到远程服务
    ├─→ Hook           = 事件驱动的预处理
    └─→ Plugin         = 上面所有能力的打包分发
```

### 顶层心智模型

> **Claude Code 的所有"高级能力"，其实都是"预处理 + 数据注入"这个原始能力的不同封装形式。**
>
> **占位符是这个能力最原始、最基础的表达。**

- 学 slash command → 学的是**手动触发的预处理**
- 学 skill → 学的是**AI 自动触发的预处理**
- 学 subagent → 学的是**把预处理结果派给独立 AI**
- 学 MCP → 学的是**从远程服务获取动态数据**
- 学 hooks → 学的是**事件驱动的预处理**
- 学 plugin → 学的是**把上面全部打包分发**

**学好占位符，是学好后面所有能力的地基。**

### 推荐学习顺序

- **路 A（我推荐）**：`Slash Command` → `Skills` → `Hooks` → `Subagents` → `MCP` → `Plugins`
  - 理由：skill 跟 command 是"孪生兄弟"，占位符知识 90% 通用；hooks 才是"进阶跳跃"
- **路 B（学习最快）**：直接跳去学 hooks
  - 理由：hooks 把占位符思想"倒过来"用，理解了两边就完全打通了

---

## 六、常见坑

正因为占位符跨越这么多模块，**同一个坑可能在不同地方出现**。提前预警：

### 坑 1：`$ARGUMENTS` 在 skill 里的行为**微妙不同**

- **在 slash command 里**：`$ARGUMENTS` 是用户 `/cmd` 后面的字
- **在 skill 里**：`$ARGUMENTS` 通常是**空的**，因为 skill 是 AI 自动触发的，没有用户输入
  - 除非用户用 `/skills` 交互菜单手动传参

### 坑 2：`@file` 有大小限制

- 文件太大（几十 KB）会被截断或者拒绝
- 千万别 `@node_modules/xxx`
- 需要读大量数据时，用 subagent 或 MCP，不要用 `@`

### 坑 3：`!command` 有 `allowed-tools` 限制

- 你在 frontmatter 里没允许的命令，`!` 里也跑不了
- 但反过来，允许了不代表 100% 会跑 —— 用户可能会被弹窗问"要不要执行"

### 坑 4：hooks 里的占位符**替换时机不一样**

- slash command 的占位符 → **进入模型之前**替换
- hooks 里的占位符 → 由 **shell 或 Claude Code 自己**在执行时替换
- 大部分时候语法相同，但如果遇到"没被替换成正确的值"的问题，先想想是谁在做替换

---

## 相关笔记

- [Slash Command 动态参数与文件引用](../A-Commands与Skills/Slash-Command动态参数与文件引用.md) —— 占位符的基础语法（前置阅读）
- [Commands 与 Skills：从快捷命令到可复用工作流](../A-Commands与Skills/Commands与Skills-从快捷命令到可复用工作流.md)
- [Claude Code 手动创建 git-safe-submit Skill](../A-Commands与Skills/Claude-Code-手动创建git-safe-submit-Skill.md)

## 相关项目文档

- [01-slash-commands/README.md](../../01-slash-commands/README.md) —— slash command 官方教程
- [03-skills/README.md](../../03-skills/README.md) —— skills 官方教程
- [04-subagents/README.md](../../04-subagents/README.md) —— subagents 官方教程
- [05-mcp/README.md](../../05-mcp/README.md) —— MCP 官方教程
- [06-hooks/README.md](../../06-hooks/README.md) —— hooks 官方教程
- [07-plugins/README.md](../../07-plugins/README.md) —— plugins 官方教程
