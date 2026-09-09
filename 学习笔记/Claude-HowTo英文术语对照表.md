# Claude-HowTo 英文术语对照表（小白版）

- **日期**：2026-09-09
- **用途**：读这个仓库的教程时，看到英文概念词不用再一个个查。先读第 1 章"词根拼装课"学会猜词，后面 6 章按场景查。
- **配套阅读**：[H-hooks 答疑](H-hooks/Hooks答疑-从事件匹配器到stdin-JSON逐行拆format-code脚本.md)、[G-mcp 答疑](G-mcp/MCP完全答疑-从授权安全到数据库文件系统与PDF流水线Agent.md)、[F-memory 答疑](F-memory/记忆体系完全答疑-从CLAUDE-md到L0-L3记忆流水线.md)

---

## 这份表怎么用

**两个标记先认识：**

- 🔒 = **协议词**：给机器读的"暗号"——事件名、JSON key、命令名、环境变量。它们的中文意思**只用来帮你理解，真正写配置、敲命令时必须原样写英文**，翻成中文就坏了。
- 其余普通概念词（agent、session、commit 这类）：日常说话直接用中文或英文都行，但看英文教程时要能对上号。

**一个例子说明 🔒 多重要：**

```json
{
  "hooks": {                          // 🔒 hooks：必须写英文
    "PostToolUse": [                  // 🔒 事件名：必须写英文
      { "matcher": "Write|Edit" }     // 🔒 matcher：必须写英文
    ]
  }
}
```

`PostToolUse` 你心里要知道它是"工具用完之后"，但配置文件里写"工具用完之后"，Claude Code 就不认了。

**词条长这样：**

> **英文** ｜ 中文叫法 ｜ 大白话 ｜ 在仓库哪里见过

高频词讲得细（有类比、有例子），低频词一句话带过，不注水。

---

# 第 1 章：词根拼装课 ⭐ 最重要

英文技术词看起来一大堆，其实大部分是**积木拼出来的**。比如：

> `Post`（之后）+ `Tool`（工具）+ `Use`（使用）+ `Failure`（失败）
> = **PostToolUseFailure** = "工具调用失败之后"那个事件

记住 20 来个词根，以后看到生词**先拆再猜**，十有八九能懂。

## 1.1 表"时间位置"的词根

| 词根 | 意思 | 像什么 | 拼出来的词 |
|---|---|---|---|
| `Pre-` | 在……**之前** | 饭前（pre-dinner） | 🔒 `PreToolUse`（用工具之前） |
| `Post-` | 在……**之后** | 饭后（post-dinner） | 🔒 `PostToolUse`（用工具之后）、`PostToolUseFailure`（工具失败之后）、`PostToolBatch`（一批工具之后） |

> 记住这一对，你就理解了 hooks 里最重要的两个事件：**Pre 是"拦在前面"，Post 是"跟在后面收拾"**。

## 1.2 表"核心事物"的词根

| 词根 | 意思 | 大白话 | 拼出来的词 |
|---|---|---|---|
| `Tool` | 工具 | Claude 干活用的"手"：读写文件、跑命令都是工具 | 🔒 `PreToolUse`、`tool_input`（工具的输入）、`tool_result`（工具的结果）、`mcp_tool` |
| `Use` | 使用、调用 | 真的动手用了一下 | `PreToolUse`、`PostToolUse` |
| `Prompt` | 提示词 | 你发给 AI 的那句话 | 🔒 `UserPromptSubmit`（用户提交了提示词）、`UserPromptExpansion`（提示词被展开） |
| `Session` | 会话 | 从打开 Claude Code 到关闭，**一整次聊天/开会** | 🔒 `SessionStart`、`SessionEnd`、环境变量 `CLAUDE_CODE_SESSION_ID`（这次会话的编号） |
| `Task` | 任务 | 一件被派出去、需要时间完成的活 | 🔒 `TaskCreated`（任务创建了）、`TaskCompleted`（任务完成了）、后台任务目录 `~/.claude/tasks/` |
| `Message` | 消息 | 屏幕上的一条对话 | 🔒 `MessageDisplay`（消息显示出来时） |
| `Permission` | 许可、权限 | "这件事准不准干"的批准 | 🔒 `PermissionRequest`（请求批准）、`PermissionDenied`（批准被拒） |
| `Notification` | 通知 | 弹给你看的提醒（像手机推送） | 🔒 `Notification` 事件 |
| `Directory` | 目录 | 就是"文件夹"的学名 | 🔒 `DirectoryAdded`（新文件夹被加进来了） |
| `Cwd` | 当前工作目录 | **c**urrent **w**orking **d**irectory 的缩写，"你现在站在哪个文件夹里" | 🔒 `CwdChanged`（当前目录变了） |
| `Worktree` | 工作树 | git 给同一份代码开的"分身工位"，详见第 4 章 | 🔒 `WorktreeCreate`、`WorktreeRemove` |
| `Batch` | 一批 | 好几个动作攒成一批 | 🔒 `PostToolBatch`（一批工具跑完之后） |

## 1.3 表"动作/状态变化"的词根

| 词根 | 意思 | 拼出来的词 |
|---|---|---|
| `Start` / `End` | 开始 / 结束 | 🔒 `SessionStart` / `SessionEnd` |
| `Stop` | 停下 | 🔒 `Stop`（Claude 这轮回答干完了）、`SubagentStop`（子代理干完了） |
| `Create` / `Remove` | 创建 / 移除、删除 | 🔒 `WorktreeCreate` / `WorktreeRemove` |
| `Added` / `Changed` / `Completed` | 被添加 / 被改变 / 完成了 | 🔒 `DirectoryAdded`、`CwdChanged`、`TaskCompleted` |
| `Submit` | 提交、交上去 | 🔒 `UserPromptSubmit`（你把那句话发出去的瞬间） |
| `Expansion` | 展开、扩充 | 🔒 `UserPromptExpansion`（你的话被系统补充加工后再送给 AI） |
| `Request` / `Denied` | 请求 / 被拒绝 | 🔒 `PermissionRequest` / `PermissionDenied` |
| `Display` | 显示、上屏 | 🔒 `MessageDisplay` |
| `Failure` | 失败 | 🔒 `PostToolUseFailure` |
| `Load` | 加载 | 🔒 `InstructionsLoaded`（指令文件被读取进来了） |

> **小规律**：事件名用过去分词（Added/Changed/Completed/Denied）表示"这件事**已经发生了**"——这类事件都是在动作完成后通知你。

## 1.4 高频修饰词

| 词 | 意思 | 大白话 / 例子 |
|---|---|---|
| `background` | 后台 | 不用你盯着、自己在后面跑。如"后台任务"background task |
| `scope` | 范围 | 管多大一片：只管这个项目，还是所有项目 |
| `mode` | 模式 | 同一款软件的不同"工作档位"，如自动模式、规划模式 |
| `allow` / `deny` / `ask` / `defer` 🔒 | 放行 / 拒绝 / 先问我 / 暂缓 | hook 和权限系统里的四种决定；优先级 **deny > defer > ask > allow**（拒绝最大） |
| `source` | 来源 | 这事是怎么引起来的。如 SessionStart 的来源有 `startup`（刚启动）、`resume`（恢复旧会话）、`fork`（分叉复制） |

## 1.5 拼装实战：自己拆四个词

读完前面的表，试着拆：

| 事件名 🔒 | 拆积木 | 意思是 |
|---|---|---|
| `PostToolUseFailure` | Post + Tool + Use + Failure | 一次工具调用**失败之后**触发 |
| `UserPromptExpansion` | User + Prompt + Expansion | 用户的提示词被**展开/加工**时触发 |
| `CwdChanged` | Cwd + Changed | **当前工作目录变了**时触发 |
| `WorktreeRemove` | Worktree + Remove | 一个 git 工作树**被移除**时触发 |

能猜出这四个，词根这一关就算过了。完整事件清单在第 3 章。

---

# 第 2 章：Claude Code 核心概念

**本章全家福**：agent、subagent、Agent Teams、prompt、system prompt、session、context、context window、compaction、token、skill、hook、plugin、MCP、checkpoint、slash command、workflow、memory、CLAUDE.md、frontmatter、workspace、cwd、model、effort、mode、REPL/TUI/headless、tool、task、instruction、manifest、marketplace、namespace、alias、status line、background/scheduled task、Monitor、progressive disclosure、fallback、artifact

先讲 12 个最核心的（这几个懂了，整个体系就通了），其余列表速查。

## 2.1 十二个核心概念（细讲）

### agent ｜ 代理、智能体

**大白话**：能"自己看情况决定下一步干什么"的 AI 程序。普通程序你点一下它动一下；agent 你给个目标，它自己拆步骤、调工具、干完再汇报。Claude Code 本身就是一个 agent。
**类比**：普通程序是**自动售货机**（按按钮出饮料），agent 是**新来的员工**（你说"把这事办了"，他自己想办法）。

### subagent ｜ 子代理

**大白话**：主 agent（你正在聊天的这个 Claude）**临时雇来的专员**。主 Claude 干不过来或需要独立上下文时，派一个子代理去查资料、做分析，干完把结论交回来，过程不占你这边的聊天版面。
**出处**：[04-subagents](../04-subagents/README.md)；详见 [E-Subagents 完全指南](E-Subagents/Subagent完全指南.md)。
**别混**：agent 是泛指，subagent 特指"被主 agent 派出去的那个"。

### prompt ｜ 提示词

**大白话**：你输入给 AI 的**任何一句话/一段指令**。你现在每天对 Claude Code 说的话就是 prompt。
- `system prompt`（系统提示）：**你看不见、但每次都在**的那段底层指令，规定 AI 的身份和规矩。Claude Code 的系统提示由产品写死；subagent 的系统提示来自它的 agent 文件。
- 🔒 `UserPromptSubmit`：hooks 事件，"用户把 prompt 交出去"的瞬间。

### session ｜ 会话

**大白话**：从你启动 Claude Code 到退出，**一整次连续对话**就是一个 session。关掉再开 = 新 session；用 `/resume` 恢复旧对话 = 续上旧 session。
**类比**：session 是"一次会议"，会议结束（退出）就散会；下次开会是新的 session。

### context ｜ 上下文

**大白话**：AI 在回答这一句时，**眼前能看到的全部材料**：你说过的话、它之前的回答、读进来的文件、工具返回的结果。它不像人有长期记忆——**没在 context 里的东西，它这一轮就"看不见"**。
- `context window`（上下文窗口）：一次能装进"眼前"的材料总量上限，按 token 算。窗口装满了，最早的内容会被挤出去。
- `compaction`（压缩）：对话太长时，系统自动把前面的内容**总结成摘要**腾出空间。仓库里叫"上下文压缩"。

**session / context / memory 三者别混：**

| 词 | 比喻 | 生命周期 |
|---|---|---|
| session 会话 | 一次会议 | 从开到关 |
| context 上下文 | 会议桌上摊着的材料 | 装满会被压缩/挤走 |
| memory 记忆 | 员工的笔记本，**会后还在** | 跨会话长期保留（见 [02-memory](../02-memory/README.md)） |

### token ｜ 词元

**大白话**：AI 切割文字的**最小计费/计量小块**。一个英文单词大约 1 个 token，一个汉字常被切成 1～2 个。它既是"字数单位"也是"计费单位"还是"窗口容量单位"。不用纠结精确切法，知道"token 数 ≈ 文字量、也 ≈ 花费"即可。

### skill ｜ 技能（保留英文 skill）

**大白话**：一份**打包好的"操作手册"**：把一套成熟做法（什么时候用、分几步、配套模板）写成文件，AI 遇到对应场景自己翻出来照着做。你在这个仓库里建的 `git-safe-submit`、`讲明白` 都是 skill 或 command。
**出处**：[03-skills](../03-skills/README.md)。

### hook ｜ 钩子（保留英文 hook）

**大白话**：**自动触发的机关**。你不用喊，只要预设的事件发生（工具调用前后、会话开始结束……），它就自动执行脚本。像门上的自动门感应器，或办公室的自动质检岗。
**出处**：[06-hooks](../06-hooks/README.md)，入门拆细看 [H-hooks 答疑](H-hooks/Hooks答疑-从事件匹配器到stdin-JSON逐行拆format-code脚本.md)。

### plugin ｜ 插件

**大白话**：把 commands、skills、agents、hooks、MCP 配置**整套打成一个包**，一次安装获得一整套能力，像给软件装"扩展包/DLC"。
**出处**：[07-plugins](../07-plugins/README.md)。

### MCP ｜ 外部工具协议（Model Context Protocol）

**大白话**：让 AI 接外部工具/数据的**统一插座标准**。没有 MCP，每接一个新工具都要单独改造；有了 MCP，数据库、文件系统、飞书等都做成同一种"插头"，插上就能用。
**类比**：USB 接口——设备千奇百怪，接口统一就都能插。
**出处**：[05-mcp](../05-mcp/README.md)，细讲见 [G-mcp 答疑](G-mcp/MCP完全答疑-从授权安全到数据库文件系统与PDF流水线Agent.md)。

### checkpoint ｜ 检查点

**大白话**：给工作状态拍的**存档快照**。改坏了可以退回到某个检查点，类似游戏存档、Word 的"恢复到以前版本"。
**出处**：[08-checkpoints](../08-checkpoints/README.md)。

### slash command ｜ 快捷命令

**大白话**：以 `/` 开头调用的**自定义口令**（如 `/submit-notes`、`/讲明白`）。背后是一个写好流程的 Markdown 文件，喊一声就按流程办。区别于 AI 自己判断时机的 skill：**command 是你主动喊的，skill 是它自动翻的**。
**出处**：[01-slash-commands](../01-slash-commands/README.md)。

## 2.2 一张表分清四兄弟：command / skill / subagent / hook

这是新手最容易混的，用"新员工"类比一次讲清：

| 东西 | 类比 | 什么时候动 | 仓库位置 |
|---|---|---|---|
| slash command | 你**喊口令**派活 | 你主动输入 `/xxx` | `.claude/commands/` |
| skill | 一本**操作手册**，他自己判断要不要翻 | 场景对上了自动加载 | `.claude/skills/` |
| subagent | 临时雇的**外包专员** | 主 agent 派他出去干一块独立的活 | `.claude/agents/` |
| hook | 办公室的**自动门禁/质检岗** | 对应事件一发生就自动触发，不用喊 | `settings.json` 的 hooks 段 + 脚本 |
| plugin | 以上东西的**整套打包** | 安装后整体生效 | 插件市场/目录 |

## 2.3 其余核心概念速查

| 英文 | 中文叫法 | 大白话 |
|---|---|---|
| Agent Teams | 代理团队 | 多个 subagent 组队、能互相通信协作的模式 |
| workflow / dynamic workflow | 工作流 / 动态工作流 | 把多步操作编排成固定流水线；"动态"指 AI 可以按情况决定派几个子任务 |
| memory / auto memory | 记忆 / 自动记忆 | 跨会话保留的笔记；自动记忆指 AI 自己维护的 MEMORY.md 索引和事实文件，见 [02-memory](../02-memory/README.md) |
| `CLAUDE.md` | （文件名不译） | 项目的"员工守则"，AI 每次开工自动读，见 [F-memory 答疑](F-memory/记忆体系完全答疑-从CLAUDE-md到L0-L3记忆流水线.md) |
| frontmatter 🔒 | 元数据头 / 前置字段 | 文件最顶部夹在两条 `---` 之间的 YAML 配置，如 `name:`、`description:`。给机器看，key 不能翻 |
| workspace | 工作区 | Claude Code 当前被授权工作的文件夹范围 |
| model / model ID | 模型 / 模型编号 | 背后是哪个大脑，如 `claude-opus-5`、`claude-sonnet-5`、`claude-haiku-4-5` |
| fallback / fallbackModel | 兜底 / 备用模型 | 主模型不可用时自动换用的备选 |
| effort / effort level | 思考强度 | AI 回答时"想多深"的档位（low/medium/high…），越高越慢越贵但通常越稳；hook 里能通过 🔒 `CLAUDE_EFFORT` 读到 |
| built-in command | 内建命令 | 软件自带的 `/config`、`/help` 这类命令，区别于你自己建的 |
| tool / tool call / tool_result | 工具 / 工具调用 / 工具结果 | AI 能执行的动作（读写文件、跑命令）；调用一次；动作返回的内容 |
| task | 任务 | 一件被派出、可能要跑一会儿的活（后台任务、定时任务都是它） |
| instruction | 指令 | 给 AI 的规矩和要求，比 prompt 更偏"长期守则"的味道 |
| manifest 🔒 | 清单文件 | 描述一个包"里面有什么"的总目文件，如插件的 `plugin.json` |
| marketplace | 市场 | 下载/分发插件的地方，类似应用商店 |
| namespace | 命名空间 | 给名字加"前缀分区"防止重名撞车，像同名的人加上公司名区分 |
| alias | 别名 | 给命令起的短外号，敲短名等于敲全名 |
| status line / statusline | 状态栏 | 终端最底下那行实时信息（分支、模型、用量等） |
| background task | 后台任务 | 在后面自己跑、完成了再通知你的任务，不用干等 |
| scheduled task | 定时任务 | 按时间计划自动跑的任务（如每隔 5 分钟） |
| Monitor（Tool） | 监控工具 | 盯着命令输出/日志，出现关键行就通知你的内置工具 |
| progressive disclosure | 按需加载 / 渐进披露 | skill 的设计原则：平时只给 AI 看摘要，需要时才读详细参考文件，省 context |
| TUI | 全屏终端界面 | **T**ext **U**ser **I**nterface：Claude Code 那种占满终端窗口的交互式界面 |
| REPL | 交互式命令行 | **R**ead-**E**val-**P**rint **L**oop：你输一句它回一句的循环，就是对话式终端 |
| CLI | 命令行界面 | **C**ommand-**L**ine **I**nterface：在黑窗口敲字操作软件的方式（对比图形界面点按钮） |
| headless | 无头模式 | 没有交互界面、由脚本/管道驱动跑完就退出的用法 |
| print mode | 输出模式 | 用 `claude -p "问题"` 让它答完就退出、结果可传给别的命令，不进交互界面 |
| planning mode | 规划模式 | 只让 AI 调研和写计划、不实际改文件的档位，批准计划后才动手 |
| output style | 输出风格 | `/config` 里选回答的呈现风格 |
| artifact | 制品 | AI 生成并发布的可交互网页/文档作品 |

---

# 第 3 章：hooks 事件名与配置词（最密集的一章）

**本章全家福**：事件名 22 个（Setup、SessionStart、SessionEnd、UserPromptSubmit、UserPromptExpansion、PreToolUse、PostToolUse、PostToolUseFailure、PostToolBatch、Notification、MessageDisplay、Stop、SubagentStop、PermissionRequest、PermissionDenied、DirectoryAdded、TaskCreated、TaskCompleted、CwdChanged、WorktreeCreate、WorktreeRemove、InstructionsLoaded）+ 配置词（matcher、type、if、command、args、timeout、once、continueOnBlock）+ 协议词（stdin、stdout、stderr、exit code、payload、allow/deny/ask/defer、block、updatedInput、additionalContext、updatedToolOutput、hookSpecificOutput、reloadSkills、环境变量）

> 注：上游版本持续在增加事件（截至 v2.1.219 共 31 个），这里讲**你最该先掌握的**；完整清单以 [06-hooks/README.md](../06-hooks/README.md) 当前版本为准。

## 3.1 先看一张"事件时间轴"

把事件挂到一次对话的流程上，就一点都不乱了：

```text
启动 Claude Code
  │  ① Setup（一次性初始化）
  │  ② SessionStart（会话开始）
  │  ③ InstructionsLoaded（CLAUDE.md 等守则被读进来）
  ▼
你发一句话
  │  ④ UserPromptSubmit（你按了回车）
  │  ⑤ UserPromptExpansion（句子被展开加工）
  ▼
Claude 决定调一个工具（比如写文件）
  │  ⑥ PreToolUse        ── 动手前！能拦住
  │       （要批准时）PermissionRequest / PermissionDenied
  │  ▼ 工具真正执行
  │  ⑦ PostToolUse       ── 干完了，可收拾/记录
  │  ⑧ PostToolUseFailure ── 干失败了
  │  ⑨ PostToolBatch     ── 一批工具都干完了
  ▼
Claude 准备结束这轮回答
  │  ⑩ MessageDisplay（回答文字正在上屏）
  │  ⑪ Stop（这轮回答完了）；子代理干完是 SubagentStop
  ▼
（期间随时可能）Notification 通知、DirectoryAdded 加目录、
              TaskCreated/Completed 后台任务、CwdChanged 换目录、
              WorktreeCreate/Remove 工作树增删
  ▼
你退出 Claude Code
     ⑫ SessionEnd（整场会话结束，只触发一次）
```

**记忆法**：Pre 拦在动作前，Post 跟在动作后；Start/End 管整场会话，Stop 管单轮回答；其余都是"某件具体小事发生时"。

## 3.2 事件名逐个拆（全是 🔒，配置里照抄英文）

| 事件名 | 积木拆解 | 什么时候触发 | 典型用途 |
|---|---|---|---|
| `Setup` | 初始化 | 每个 session 的一次性准备阶段 | 装依赖、备环境 |
| `SessionStart` | Session+Start | 会话刚启动（来源 `source`：startup/resume/clear/compact/fork） | 打招呼、重扫 skills、设会话标题 |
| `SessionEnd` | Session+End | 整场会话结束时，只触发一次 | 写学习日志、收尾清理（如 session-end.sh） |
| `InstructionsLoaded` | Instructions+Loaded | CLAUDE.md 等守则文件被读进来时 | 检查守则内容 |
| `UserPromptSubmit` | User+Prompt+Submit | 你每次按下回车发送消息 | 校验 prompt、拦危险请求（validate-prompt.sh） |
| `UserPromptExpansion` | User+Prompt+Expansion | 你的话被系统展开/补充时 | 加工输入 |
| `PreToolUse` | Pre+Tool+Use | **每个工具动手之前** | 最常用：校验、拦截、改输入（pre-commit.sh） |
| `PostToolUse` | Post+Tool+Use | 每个工具干完之后 | 格式化、记录、脱敏（format-code.sh、log-bash.sh） |
| `PostToolUseFailure` | …+Failure | 工具调用失败之后 | 失败补救、报警 |
| `PostToolBatch` | …+Batch | 一批工具调用全部结束之后 | 批量收尾 |
| `Notification` | Notification | 需要通知你时（含子代理 `agent_needs_input` 要人补充、`agent_completed` 已完成） | 推送到手机/团队 |
| `MessageDisplay` | Message+Display | AI 的回答文字逐块显示时 | 改写展示内容 |
| `Stop` | Stop | Claude **这一轮回答**结束时（每轮都可能触发，区别于 SessionEnd） | 完成度兜底检查 |
| `SubagentStop` | Subagent+Stop | 一个子代理收工时 | 检查子代理产出 |
| `PermissionRequest` | Permission+Request | 有动作来请求批准时 | 自定义审批 |
| `PermissionDenied` | Permission+Denied | 批准被拒绝时 | 记录拒绝、给提示 |
| `DirectoryAdded` | Directory+Added | 用 `/add-dir` 等把新文件夹加入工作区时 | 对新目录做准备 |
| `TaskCreated` | Task+Created | 一个后台/定时任务被创建时 | 任务跟踪 |
| `TaskCompleted` | Task+Completed | 任务完成时 | 任务跟踪 |
| `CwdChanged` | Cwd+Changed | 你切换了当前工作目录时 | 跟随目录改行为 |
| `WorktreeCreate` | Worktree+Create | 新建了一个 git 工作树时 | 为分身工位装 hooks |
| `WorktreeRemove` | Worktree+Remove | 删除工作树时 | 清理 |

## 3.3 配置词（写在 settings.json 里的 key，全 🔒）

| 词 | 大白话 | 例子 |
|---|---|---|
| `matcher` | 匹配器：这条 hook 盯**哪个工具** | `"Write"` 只盯写文件；`"Edit\|Write"` 正则盯两个；`"Bash"` 盯命令；`"*"` 盯全部 |
| `type` | hook 类型：用什么方式执行 | 五种：`command`（跑本地脚本，最常用）、`http`（调网址）、`mcp_tool`（调 MCP 工具）、`prompt`（让模型判断）、`agent`（派子代理评估） |
| `if` | 二次收窄：matcher 选中工具后，再按**参数**过滤 | `if: "Edit(src/**)"` 只在改 src 目录时触发；`if: "Read(.env)"` 只在读 .env 时 |
| `command` | 要执行的 shell 命令/脚本路径 | `"$CLAUDE_PROJECT_DIR/.claude/hooks/x.sh"` |
| `args` | 参数数组形式：直接拉起程序、不经过 shell 解析 | 比 command 更不容易被特殊字符搞坏 |
| `timeout` | 超时秒数，到点强杀，防止脚本卡死拖垮 AI | `30` |
| `once` | 这次会话里是否只跑一次 | `true` |
| `continueOnBlock` | Post hook 阻断后，是否让 AI 看到理由**自己调整重试**，而不是直接终止 | `true` |
| `url` / `server` / `tool` | http 类型的网址；mcp_tool 类型的服务器名和工具名 | — |

## 3.4 输入输出协议词（hook 脚本怎么和 Claude Code 对话）

这组词是读懂所有示例脚本的钥匙，拆细一点（也可复习 [H-hooks 答疑](H-hooks/Hooks答疑-从事件匹配器到stdin-JSON逐行拆format-code脚本.md)）：

| 词 | 中文 | 大白话 |
|---|---|---|
| `stdin` | 标准输入 | **送菜窗口**：Claude Code 把一段 JSON 数据从这个窗口塞进脚本。脚本开场 `INPUT=$(cat)` 就是在收这个窗口的东西 |
| `stdout` | 标准输出 | **出菜窗口**：脚本正常回话的通道。hook 在这里吐 JSON 就能给 AI 递补充信息 |
| `stderr` | 标准错误 | **抱怨窗口**：脚本报错/写阻断理由走这里（`echo "理由" >&2`） |
| payload | 载荷 | 通过 stdin 送进来的**那段 JSON 本体**，装着文件路径、命令等字段 |
| `exit code` | 退出码 | 脚本收工时亮的"信号灯"。**0 = 一切正常放行；2 = 阻断**（理由必须写 stderr）；其他非零（如 1）只是脚本出错，**不拦**——这是头号大坑 |
| JSON | （格式名） | 最通用的结构化数据写法，"键: 值"成对，长这样 `{"file_path": "a.py"}` |
| `tool_input` 🔒 | 工具输入 | payload 里装"这次工具调用的参数"的字段，如命令文本、文件路径 |
| `file_path` 🔒 | 文件路径 | Write/Edit/Read 事件 payload 里的文件路径字段 |
| `user_prompt` 🔒 | 用户提示词 | UserPromptSubmit 事件 payload 里你发的那句话（旧字段名 `prompt`） |
| `prompt_id` 🔒 | 提示词编号 | 本次提问的 UUID，用来把日志串起来 |
| allow / deny / ask / defer 🔒 | 放行/拒绝/询问/暂缓 | PreToolUse 可以返回的四种 `permissionDecision`。冲突时 deny 最大 |
| block 🔒 | 阻断 | `"decision": "block"` = 硬拦住这次动作 |
| `updatedInput` 🔒 | 修改后的输入 | 放行但**偷偷改掉工具参数**（如改路径）后再执行 |
| `additionalContext` 🔒 | 附加上下文 | **不拦**，但给 AI 塞一张"小纸条"提醒它（validate-prompt.sh 就是这么干的） |
| `updatedToolOutput` 🔒 | 改写工具结果 | Post 阶段在 AI 看到结果前先加工：去颜色码、脱敏、压缩日志 |
| `hookSpecificOutput` 🔒 | hook 专用输出 | 装上面这些回话的外层信封，里面要写 `hookEventName` 标明是哪个事件 |
| `hookEventName` 🔒 | 事件名回标 | 告诉系统这份输出对应哪个事件，如 `"PostToolUse"` |
| `reloadSkills` 🔒 | 重扫技能 | SessionStart 时返回 `true`，效果等同 `/reload-skills` |
| `sessionTitle` 🔒 | 会话标题 | 给这次会话起个显示在界面上的名字 |
| `permissionDecisionReason` 🔒 | 决定的理由 | 解释为什么 allow/deny |

**两个常用环境变量（脚本运行时系统自动给的，🔒 名字照抄）：**

| 变量名 | 大白话 |
|---|---|
| `CLAUDE_PROJECT_DIR` | 当前项目根目录的绝对路径，脚本里靠它定位文件，别写死路径 |
| `CLAUDE_CODE_SESSION_ID` | 当前会话编号，用来把多条日志对到同一次会话 |
| `CLAUDE_EFFORT` | 当前思考强度档位，脚本可据此决定"高 effort 多检查、低 effort 少检查" |
| `COLUMNS` / `LINES` | 终端窗口的宽/高（列数、行数），状态栏脚本据此排版 |

---

# 第 4 章：Git / GitHub 术语

**本章全家福**：repository、commit、hash/SHA、branch、push、pull、merge、rebase、fork、remote、origin、upstream、worktree、tag、PR、clone、status、stage、diff、add、log、stash、checkout、reset、clean、amend、issue、OAuth、token、conventional commits

**总比喻**：git 是你代码的**档案柜+时光机**，GitHub 是放这个档案柜的**云端协作网站**。

## 4.1 核心词（细讲）

### repository（repo）｜ 仓库

一个被 git 管理的项目文件夹，所有代码和历史都在里面。你现在这个 `claude-howto-zh-cn` 就是一个仓库。

### commit ｜ 提交（名词：一次存档；动词：存档这个动作）

**大白话**：给某一刻的所有文件拍一张**快照**存进历史，附一句说明。历史就是一串 commit。
- `hash` / `SHA`：每个快照的唯一编号（如 `eab5c4c`），像快递单号，靠它精确找到某次提交。

### branch ｜ 分支

**大白话**：从主线岔出去的**平行世界/支线**，你在支线上随便改不影响主线。你现在笔记都提交在 `study-notes` 支线，主线是 `main`。

### push ｜ 推送

把本地的提交**上传到远端**（GitHub）。`git push origin study-notes` = 把 study-notes 支线推到 origin。

### pull ｜ 拉取

把远端的新内容**下载并合并**到本地。push/pull 是一对反方向（上传/下载）。

### merge ｜ 合并

把一条支线的改动**并回**另一条线（如 study-notes 合进 main）。

### rebase ｜ 变基

把你的一串提交"**搬家**"到另一个基点之后，让历史变成一条直线。和 merge 目的类似但会重写历史顺序，新手知道即可，别在公共分支上乱用。`git pull --rebase` = 拉取时用变基方式整合。

### fork ｜ 分叉（⚠️ 一个词两个意思）

1. **Git 语境**：在 GitHub 上把**别人的仓库整个复制一份到你自己账号**下，你改你的。你仓库就是从上游 fork 来的。
2. **Claude Code 语境**：`/fork` 表示**复制当前会话**开出一个平行对话。hooks 里 SessionStart 的 source `fork` 也是这个意思。

### remote ｜ 远端

远端仓库的**地址簿条目**，每条记录有名字和网址。`git remote -v` 就是查看地址簿。

### origin ｜ 起源（远端的默认名字）

**你自己的**那个云端仓库的标准名字。你机器上 `origin` = `github.com/asasas-bit/claude-howto-zh-cn`。

### upstream ｜ 上游

你 fork 的**原厂仓库**。你这里 `upstream` = 原作者的仓库。原厂更新后，用 `/sync-upstream` 把新东西同步下来——所以 **origin 是"你家的云"，upstream 是"原厂的云"**。详见 [UPSTREAM.md](../UPSTREAM.md) 和 [sync-upstream 笔记](D-command/sync-upstream.md)。

### worktree ｜ 工作树

**大白话**：同一个仓库的历史**共享**，但在不同文件夹里**同时打开多个分支**的"分身工位"。好处：A 文件夹干到一半不用收，去 B 文件夹开另一个分支修 bug，互不打架。hooks 的 `WorktreeCreate/Remove` 就是在这种分身工位增删时触发。

### PR（Pull Request）｜ 合并请求（GitHub 上简称 PR）

**大白话**：你在支线改完，发一张**"请求合并审批单"**给维护者：请把我的改动看一眼、批准、合进主线。不是命令 pull，而是协作流程。

### clone ｜ 克隆

把一个远端仓库**完整下载**到本地（含全部历史），第一次拿到项目用它。

### stage / staging（暂存区）｜ 暂存

**大白话**：寄快递前的**打包箱**。改动的文件先用 `git add` 放进打包箱（stage），`git commit` 只把箱子里的东西封箱存档。没 add 的改动不会进 commit。

### tag ｜ 标签

给某个 commit 贴的**里程碑书签**（如 `v2.1.220`），常用来标版本发布点。

## 4.2 其余 Git 词速查

| 词 | 大白话 |
|---|---|
| `status` | 查看当前状态：哪些文件改了、哪些已装箱 |
| `add` | 把改动放进暂存箱（`git add 文件名`） |
| `diff` | 查看"到底改了哪几行"的对比 |
| `log` | 查看提交历史（`git log --oneline` 简洁版） |
| `stash` | 把没改完的东西**临时塞抽屉**，让工作区变干净；以后再 `stash pop` 拿回来 |
| `checkout` | 切换到另一个分支，或恢复旧版本文件 |
| `reset` | 回退（`--hard` 会丢弃改动，危险） |
| `clean` | 清理没被 git 跟踪的散落文件（`-fd` 很猛，先看清） |
| `amend` | 修补最近一次提交（如补传一个漏掉的文件），会改写最后一个 commit |
| conflict | 合并时两边改了**同一行**，git 拿不准留谁的，要你手动裁决 |
| issue | GitHub 上的"意见箱/任务单"：提 bug、提需求用 |
| OAuth | 一种主流的**授权登录流程**（你用 GitHub 账号授权登录某工具，背后就是它） |
| token | 令牌：代替密码的**一串通行证字符**，如 `GITHUB_TOKEN`。泄露=别人能冒充你 |
| conventional commits | 约定式提交信息：`type(scope): 描述` 的格式。type 如 `feat`（新功能）、`fix`（修 bug）、`docs`（文档）、`refactor`（重构不改变功能）、`test`、`chore`（杂活）。你笔记里的 `docs(study-notes): …` 就是这种 |

---

# 第 5 章：终端与编程通用词

**本章全家福**：shell、bash、PowerShell、WSL、Git Bash、CLI、flag、argument、环境变量、PATH、JSON、YAML、glob、regex、script、pipe、stdin/stdout/stderr、protocol、server/client、API、API key、endpoint、webhook、timeout、process/exec、path/directory、npm/npx/uv/pip/node、jq/sed/grep/cat/head、chmod/mkdir、prettier/black/pytest/lint、cache/TTL、SDK、proxy/TLS、Markdown、symlink、monorepo、stream、headless、telemetry

## 5.1 终端环境这一族（Windows 用户先搞清这几个）

| 词 | 中文 | 大白话 |
|---|---|---|
| terminal | 终端 | 那个**敲字的黑窗口**本身 |
| shell | 壳（命令解释器） | 窗口里**真正听懂你命令的程序**。它有不同"方言" |
| bash | —（最常见的 shell 方言） | Linux/macOS 默认；仓库里 `.sh` 脚本大多按它写 |
| PowerShell | —（Windows 的 shell 方言） | Windows 自带，语法和 bash 不一样（如变量 `$env:NAME`） |
| WSL | Linux 子系统 | 在 Windows 里**内嵌一个真 Linux**，跑 Linux 工具用 |
| Git Bash | Git 自带的 bash | **装 Git for Windows 时附送的轻量 bash**，仓库脚本在 Windows 上主要靠它跑。你现在机器上就有 |
| CLI | 命令行界面 | 在黑窗口敲字操作软件（见第 2 章） |
| script | 脚本 | 把一串命令写进一个文件批量执行，如 `.sh`、`.py` |
| `shebang`（`#!/bin/bash`） | 释伴行 | 脚本第一行，声明"用哪个程序跑我"，照抄即可 |

## 5.2 命令的零件

| 词 | 大白话 | 例子 |
|---|---|---|
| command | 一整条命令 | `git push origin study-notes` |
| argument（参数） | 命令作用的**对象** | 上面的 `origin`、`study-notes` 是参数 |
| flag / option（开关/选项） | 以 `-` 或 `--` 开头的**调节项** | `git log --oneline -5` 里 `--oneline`、`-5`；`--model` 选模型 |
| environment variable（环境变量） | 系统级的"便签变量"，所有程序都能读 | `$CLAUDE_PROJECT_DIR`、`$HOME`（你的用户目录） |
| `PATH` | 可执行程序的**寻路名单** | 输入 `black` 时系统按 PATH 里的文件夹依次去找这个程序；"提示命令不存在"常是它没在 PATH 里 |
| pipe（管道 `\|`） | 把前一个命令的输出**灌给**后一个命令处理 | `echo "$JSON" \| sed ...` |
| path | 路径：文件/文件夹的地址，分绝对（从盘符写全）和相对（相对当前目录） | `../06-hooks/README.md` |
| wildcard / glob | 通配符文件匹配 | `*.py`=所有 py 文件；`src/**`=src 下所有层级；`?` 匹配单字符 |
| regex（正则表达式） | 描述文本规律的**迷你语言** | `Edit\|Write` 匹配两个词之一；`^git commit` 匹配以 git commit 开头 |

## 5.3 三个"窗口"（与第 3 章互链）

`stdin` / `stdout` / `stderr` 在 [3.4 节](#34-输入输出协议词hook-脚本怎么和-claude-code-对话)讲透了：送菜窗口、出菜窗口、抱怨窗口。补充一个普通场景：你在终端敲 `python x.py`，键盘输入走 stdin，正常打印走 stdout，报错走 stderr。

## 5.4 数据格式与网络词

| 词 | 大白话 |
|---|---|
| JSON | 最通用的"键:值"数据格式，hook payload、API、配置文件到处都是 |
| YAML | 另一种更靠缩进、更适合人写的格式，frontmatter 和很多配置用它 |
| Markdown | 你笔记用的这种轻量排版格式（# 标题、`**粗体**`、表格） |
| Mermaid | Markdown 里画流程图的文本语法，本仓库 EPUB 构建会渲染它 |
| protocol | 协议：双方约定好的**对话规矩**。MCP 全称 Model Context Protocol 就是一种协议；hook 的 stdin JSON 也是协议 |
| server（服务器）/ client（客户端） | 提供服务的一方 / 发起请求使用服务的一方。餐厅后厨 vs 点餐的你 |
| API | 应用之间的**点菜窗口**：程序不通过界面、直接按约定向另一个程序要服务 |
| endpoint | 端点：API 的**具体窗口地址**（一个网址） |
| API key | 调用 API 的**钥匙串/通行证**，如 `ANTHROPIC_API_KEY`，保密 |
| webhook | 反向的 API：事件一发生，系统**主动 POST 一段数据到你给的网址**。hooks 的 `http` 类型就是它 |
| timeout | 超时：等多久还没回应就不等了 |
| header | HTTP 请求携带的附加信息（如认证信息） |
| host | 主机/域名，如 `github.com` |
| proxy | 代理：你和外网之间的中转站（公司网络常见） |
| TLS / 证书 | 加密传输用的"安全锁"及其身份证；证书过期/公司抓包会导致连接报错 |
| OAuth | 见第 4 章，授权登录流程 |
| rate limit | 速率限制：API 规定"每分钟最多调多少次"，超了临时拒绝 |
| cache / TTL | 缓存：为省事临时存一份结果；TTL（存活时间）=这份临时结果多久后过期失效 |
| SDK | 软件开发工具包：帮你方便调用某服务的现成代码库 |
| telemetry | 遥测：程序自动上报的使用数据（供开发者分析改进） |

## 5.5 进程与执行

| 词 | 大白话 |
|---|---|
| process（进程） | 一个正在运行的程序实例。脚本跑起来就是一个进程 |
| spawn | 生成、派出：主程序启动一个子进程/子任务（"spawn 一个 subagent"=派出一个子代理） |
| exec / `execve()` | 直接启动一个可执行程序，不经过 shell 解释；hook 的 `args` 形式就是为了直接 exec |
| background | 后台：进程在后面跑，终端不等它 |
| stream / streaming | 流：数据不一次性给完，而是像水流一样**一段段持续到达**（AI 逐字蹦回答就是流式输出）；`stream-json` 是边跑边吐 JSON |

## 5.6 常见命令与工具名（混个脸熟即可，用到再查）

| 名字 | 是什么 |
|---|---|
| `node` / `npm` / `npx` | Node.js 运行时 / 它的包管理器 / 不安装直接跑一次包里的命令 |
| `python` / `pip` / `uv` | Python 运行时 / 它的包管理器 / 更快的新派包管理+运行工具（本仓库用 `uv run`） |
| `pytest` | Python 的测试工具 |
| `cargo` / `go` / `make` | Rust / Go / C 系项目的构建工具 |
| `cat` / `head` / `tail` | 查看文件全部 / 开头几行 / 末尾几行；`tail -f` 持续盯新输出 |
| `grep` | 在文本里搜规律（regex） |
| `sed` | 流编辑器：做文本替换/抽取，hook 脚本用它从 JSON 里"抠"字段 |
| `jq` | 专门解析 JSON 的命令行工具，比 sed 抠 JSON 稳（有它优先用它） |
| `chmod +x` | 给脚本加"**可执行**"权限；新脚本在 macOS/Linux/Git Bash 里要先跑这个 |
| `mkdir -p` | 建文件夹（`-p` = 父文件夹不存在就一起建） |
| `cp` / `mv` / `rm` | 复制 / 移动（也用来改名）/ 删除（`rm -rf` 极危险，路径写错后果严重） |
| `prettier` / `black` / `gofmt` / `rustfmt` | JS/TS、Python、Go、Rust 的代码**格式化工具**（format-code.sh 的主角） |
| `lint` / `linter` | 代码"挑刺工具"：不运行代码，专查风格问题和可疑写法，如 `markdownlint` |
| `mmdc` | Mermaid 图渲染器（本仓库 EPUB 构建用它把流程图渲染成图片） |
| `tmux` | 终端"分屏/保活"工具，关掉窗口任务也不断 |
| symlink | 符号链接：文件的"快捷方式/别名指针"，指向另一个真实文件 |
| monorepo | 把多个项目/模块放进**同一个 git 仓库**一起管理的组织方式 |
| Markdown 之外：GFM | GitHub 风格的 Markdown（表格、任务列表等扩展） |

---

# 第 6 章：权限与安全

**本章全家福**：permission、permission rule、allowlist、approve、trust、credential、secret、scope、sandbox、permission mode（六种）、safety classifier、intent-based protection、audit、budget

| 词 | 中文 | 大白话 |
|---|---|---|
| permission | 权限、许可 | "这个动作准不准做"。读文件一般不问，删东西、推代码会先问你 |
| permission rule 🔒 | 权限规则 | 在 settings 里预先写好的规矩，格式 `工具名(参数模式)`，如 `Bash(git status:*)` 直接放行、`Read(.env)` 询问、`Bash(rm -rf*)` 拒绝 |
| allow / deny / ask 🔒 | 放行 / 拒绝 / 询问 | 规则的三种裁决：自动允许、永不允许、每次问我 |
| allowlist | 白名单 | 明确允许的清单（在名单里的不再弹窗） |
| approve / approval | 批准 | 你点"允许"这个动作 |
| trust / workspace trust | 信任 / 工作区信任 | 只有被你标记"信任"的文件夹，里面的 agents/hooks 才允许运行——防止打开来路不明的项目时被埋的自动脚本坑到 |
| credential | 凭证 | 证明"你是你"的东西：密码、密钥、令牌的统称 |
| secret | 秘密、密钥 | 不该外泄的敏感串（API key、密码、私钥）。`.env` 文件常装它们，别提交到 git |
| scope | 范围（一词两义） | ①配置作用范围：local（仅本机）/ project（项目共享）/ user（你所有项目）；②令牌权限范围：这把 token 能干哪些事 |
| sandbox | 沙箱 | 把程序关进"**隔离试玩箱**"：能碰哪些文件夹、能不能联网都受限，搞破坏也出不了箱子 |
| audit | 审计 | 事后翻看"谁在什么时候干了什么"的日志 |
| budget | 预算 | 花费上限，如 `--max-budget-usd` 限定最多花多少美元 |
| safety classifier | 安全分类器 | Auto Mode 里判断一条命令危不危险的模型。它抽风超时会导致写操作暂时无法自动放行（我们提交笔记时就遇到过） |
| intent-based protection | 基于意图的保护 | 不靠死板字符串，而是理解命令意图来拦截危险操作（如识别 `git reset --hard` 会丢改动） |

**六种 permission mode（权限档位）🔒：**

| 模式 | 大白话 |
|---|---|
| `default` / `manual` | 默认档：该问就问，逐个批准 |
| `acceptEdits` | 自动同意文件编辑，但危险命令仍问 |
| `plan` | 规划档：只调研写计划，不动手 |
| `dontAsk` | 不问（按既定规则处理，规则没覆盖的拒绝） |
| `bypassPermissions` | 绕过所有权限检查——**危险**，只在隔离环境用 |
| `auto` | 自动模式：AI 自己读情况+安全分类器判断，低风险放行高风险问你 |

---

# 第 7 章：其他高频工作词

| 英文 | 中文 | 大白话 |
|---|---|---|
| code review | 代码审查 | 改动写完后让人（或 AI）挑毛病：查 bug、查风格、查安全问题。`/code-review` 干这个 |
| refactor | 重构 | **不改变功能**，只把代码内部改得更清晰好维护 |
| debug / root cause | 排错 / 根因 | 找 bug；root cause = 毛病的**根本原因**（不是表面症状） |
| deploy / deployment | 部署 | 把改好的代码**发布上线**，让真实用户用到 |
| rollback | 回滚 | 上线后发现出事，**撤回到上一个好版本** |
| incident | 事故 | 线上出故障的事件 |
| monitor / monitoring / metrics | 监控 / 指标 | 持续盯着系统状态；metrics = 量化的健康数字 |
| onboarding | 上手引导 | 新人/新用户第一次熟悉工具的过程 |
| retrospective | 复盘 | 事后回顾总结（你的"学习复盘"就是这个词） |
| usage | 用量 | 你用了多少（token、次数、钱），`/usage` 查看 |
| cost | 花费 | 用量折算的钱 |
| fallback | 兜底 | 首选方案失败时的备选（见 2.3） |
| artifact | 制品 | 见 2.3，AI 发布的可交互作品 |
| voice | 语音 | 语音输入/输出功能 |
| channel | 渠道 | 消息接入的通道，如 Discord、Telegram、飞书 |
| push notification | 推送通知 | 发到你手机/桌面的通知（和 git push 无关，只是"推给你"） |
| attribution | 署名 | 标明"这是谁做的"。如提交信息末尾的 `Co-Authored-By` 就是给协作署名 |
| truncate | 截断 | 内容太长被砍短（skill 的 description 太长会被预算截断） |
| screen reader | 屏幕阅读器 | 视障用户听屏幕内容的辅助工具 |

---

## 以后怎么补充这份表

1. 读教程遇到表里没有的英文词，先**按第 1 章拆词根**猜，猜不出再查
2. 查明白后，按词条格式追加到对应章节的全家福和正文里
3. 发现某个 🔒 词在新版 Claude Code 里变了（事件增减、字段改名），以 [06-hooks/README.md](../06-hooks/README.md) 当前版本为准，回头改这里
4. 上游术语总源头：[LOCALIZATION-STYLE.md](../LOCALIZATION-STYLE.md) 规定了哪些词保留英文、建议中文怎么叫
