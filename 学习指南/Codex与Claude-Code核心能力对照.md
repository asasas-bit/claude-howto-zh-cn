# Codex 与 Claude Code 核心能力对照

这份指南用于回答三个问题：

1. Claude Code 教程里的概念，在 Codex 中大致对应什么？
2. 哪些只是“目标相似”，不能直接照搬文件和配置？
3. 如果平时主要使用 Codex，应该怎样学习这个 Claude Code 仓库？

> 核对日期：2026-07-19。两款产品更新都很快，具体命令和配置字段应以当前版本的内建帮助与官方文档为准。

## 一、先记住最重要的结论

Codex 和 Claude Code 都可以：

- 阅读和修改项目文件
- 运行终端命令
- 遵守项目级长期说明
- 使用 Skills、Hooks、MCP 和 Subagents
- 进入非交互模式做脚本或 CI
- 通过权限和沙箱限制操作范围

但它们的文件名、目录、配置格式、命令入口和部分功能边界不同。

**可以迁移的是工作方法，不能直接照搬的是配置文件。**

例如：

- “给项目写员工手册”这个思路可以迁移
- Claude Code 的 `CLAUDE.md` 不能想当然地当作 Codex 默认项目说明
- “把流程做成 Skill”这个思路可以迁移
- `.claude/skills/` 不能直接当作 Codex 的项目 Skill 目录

## 二、核心能力总对照

| 关注点 | Claude Code | Codex | 是否一一对应 | 小白应该怎么理解 |
|---|---|---|---|---|
| 产品定位 | Anthropic 的终端型 coding agent，并延伸到桌面、Web 和远程能力 | OpenAI 的 coding agent，可用于 CLI、IDE、桌面/ChatGPT 和云端工作 | 大体对应 | 都能完成项目任务，但具体界面、模型和生态不同 |
| 终端入口 | `claude` | `codex` | 对应 | 进入交互式工作环境 |
| 一次性执行 | `claude -p "任务"` | `codex exec "任务"` | 对应 | 用于脚本、管道和 CI，不适合一边聊一边改 |
| 项目长期说明 | 项目根目录 `CLAUDE.md` | 项目根目录 `AGENTS.md` | 目标对应，文件不同 | 都像项目员工手册 |
| 全局长期说明 | 用户目录中的 Claude memory 配置 | `~/.codex/AGENTS.md` 或全局 guidance | 近似对应 | 放跨项目都适用的个人规则 |
| 目录级规则 | 不同目录下的 `CLAUDE.md` / memory 层级 | 根目录到当前目录之间的 `AGENTS.md`，近处规则更具体 | 近似对应 | 大规则放上层，特殊目录规则放近处 |
| 内建 slash commands | `/help`、`/model`、`/rewind` 等 | Codex 也有界面和 CLI 内建 slash commands | 部分对应 | 名称和行为不要凭另一款产品猜 |
| 自定义快捷流程 | `.claude/commands/*.md`，新工作流也常用 Skills | 主要使用 Skills、插件或当前产品提供的工作流入口 | 不完全对应 | 不要把 `.claude/commands` 复制给 Codex 就期待自动生效 |
| Skills | `.claude/skills/<name>/SKILL.md` | 项目 `.agents/skills/<name>/SKILL.md`，个人 `$HOME/.agents/skills` | 概念高度对应，路径不同 | 都是可复用的流程、说明、脚本和参考资料 |
| Skill 调用 | 可显式调用，也可按描述自动匹配 | 可在提示中显式指定；CLI/IDE 可通过 `/skills` 或 `$` 选择，也可自动匹配 | 高度对应 | `description` 都决定“什么时候该用” |
| Subagents | `.claude/agents/*.md` | 项目 `.codex/agents/*.toml`，个人 `~/.codex/agents/*.toml` | 概念对应，格式不同 | 都是专业分工，但定义文件不能互抄 |
| 内建 agent | Claude Code 有自己的内建 agent 和团队机制 | Codex 当前提供 `default`、`worker`、`explorer` 等内建 agent | 不一一对应 | 按任务需要选角色，不要硬做名称映射 |
| Hooks | 常见配置在 Claude settings，支持多类 handler 和生命周期事件 | `.codex/hooks.json` 或 `.codex/config.toml`；当前主要执行 command handler | 概念对应，成熟度和格式不同 | 都能在事件发生时自动检查，但可用类型不完全相同 |
| MCP | 通过 `claude mcp`、`.mcp.json` 或 settings 管理 | 通过 Codex 配置、插件或 connector/MCP 入口管理 | 协议对应，配置不同 | MCP 是共同标准，但两边客户端配置不是同一个文件 |
| 配置文件 | 主要是 JSON，例如 `settings.json` | 主要是 TOML，例如 `config.toml` | 不对应 | JSON 示例不能直接粘贴进 TOML |
| 权限控制 | permission modes、允许/禁止工具、沙箱等 | sandbox、approval、rules 和 managed policy 等 | 目标对应，模型不同 | 核心都是最小权限，但开关名称不同 |
| 规划模式 | planning mode、`/plan` 等 | Codex 也支持先规划再执行的协作方式和相应模式 | 近似对应 | 复杂任务先查清事实和风险，再授权修改 |
| 回退与恢复 | Checkpoints、`/rewind`、Git | 依赖 diff、Git、会话控制以及当前界面提供的恢复能力 | 不完全对应 | 不要假设 Codex 一定有与 `/rewind` 完全相同的语义 |
| 会话恢复 | continue、resume、命名会话等 | Codex 也有 thread/session 和 resume 工作流 | 近似对应 | 长任务要命名、总结和保留下一步 |
| 后台与长任务 | background tasks、monitor、scheduled tasks | 桌面/云端长任务、自动化和任务监控能力 | 部分对应 | 先定义结束条件，再交给后台运行 |
| Worktrees | Claude Code 高级工作流可使用 Git worktree | Codex 也支持 Git worktrees | 高度对应 | 用 Git 隔离并行修改，不是普通复制文件夹 |
| Plugins | 打包 commands、skills、hooks、MCP、agents 等 | 打包 Skills、工具、MCP、Hooks、资产和应用映射等 | 概念对应，manifest 不同 | 都是分发单位，不是初学者必修 |
| Windows 重点 | 要分清 PowerShell、Git Bash 和 WSL，部分本地 MCP 依赖 shell | 要分清 Windows sandbox、PowerShell、WSL 和路径格式 | 风险对应 | 教程中的 Bash 命令不能无脑复制到 PowerShell |

## 三、最核心的五组区别

### 1. `CLAUDE.md` 与 `AGENTS.md`

| 项目 | Claude Code | Codex |
|---|---|---|
| 推荐文件 | `CLAUDE.md` | `AGENTS.md` |
| 核心用途 | 项目背景、规范、命令、禁止事项 | 仓库约定、命令、验证方式、审查要求 |
| 全局位置 | Claude 用户级 memory 位置 | `~/.codex/AGENTS.md` |
| 项目位置 | 通常放项目根目录，也可分层 | 从 Git 根目录向当前目录查找 |
| 覆盖思路 | 更具体的上下文和当前提示优先 | 靠近当前目录的说明更具体 |

Codex 官方说明：Codex 在开始工作前读取 `AGENTS.md`，并从项目根目录向当前目录组合规则。  
参考：[Custom instructions with AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)

**迁移方法**：

1. 保留项目定位、常用命令、禁止事项、验收要求
2. 不照搬 Claude Code 专属命令和路径
3. 为 Codex 另写 `AGENTS.md`
4. 如果两款工具都使用，可让两份文件表达同一套项目原则，但分别使用各自语法

### 2. `.claude/commands` 与 Codex Skills

Claude Code 的自定义 command 更像“人工按下的提示词按钮”：

```text
.claude/commands/optimize.md → /optimize
```

Codex 中想保存可复用流程，优先考虑 Skill：

```text
.agents/skills/optimize/
└── SKILL.md
```

Codex Skill 可以显式选择，也可以根据 `description` 自动匹配。  
参考：[Build skills](https://learn.chatgpt.com/docs/build-skills)

这并不表示两边完全相同：

- command 往往更短，由用户明确触发
- Skill 可以包含脚本、资料和模板
- Codex 和 Claude Code 的 Skill 路径也不同

### 3. Subagents 定义格式

Claude Code 示例通常使用：

```text
.claude/agents/reviewer.md
```

Codex 自定义 agent 使用：

```text
.codex/agents/reviewer.toml
```

Codex 当前要求自定义 agent 至少说明：

- `name`
- `description`
- `developer_instructions`

还可以按 agent 设置模型、推理强度、沙箱、MCP 和 Skills。Codex 官方也提醒，Subagents 会增加 token 和协调成本。  
参考：[Codex Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)

**共同原则**：角色要窄、输入输出要清楚、能并行才拆分。

### 4. Hooks 配置和能力边界

Claude Code 本仓库展示了 command、HTTP、MCP tool、prompt、agent 等多类 Hook。

Codex 的 Hook 可以放在：

```text
~/.codex/hooks.json
~/.codex/config.toml
<repo>/.codex/hooks.json
<repo>/.codex/config.toml
```

截至核对日期，Codex 官方文档说明当前真正运行的是 `command` handler；`prompt` 和 `agent` handler 即使被解析，也会跳过。项目本地 Hook 还涉及 trust review。  
参考：[Codex Hooks](https://learn.chatgpt.com/docs/hooks)

因此，看到 Claude Code Hook 示例时，应该迁移“触发时机和安全目标”，而不是复制 JSON 字段。

### 5. 非交互与自动化

| 目的 | Claude Code | Codex |
|---|---|---|
| 一次性运行 | `claude -p "任务"` | `codex exec "任务"` |
| 机器可读输出 | JSON / stream JSON 等输出格式 | `codex exec --json` 输出 JSONL |
| 结构化结果 | 通过相应输出和 schema 能力 | `--output-schema` |
| 权限原则 | 明确允许工具和 permission mode | 默认只读，按需设置 sandbox |
| 恢复 | `--continue` / `--resume` | `codex exec resume` |

Codex 官方建议自动化使用最小权限；`codex exec` 默认运行在只读 sandbox 中，需要修改时再显式允许 workspace write。  
参考：[Codex non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode)

## 四、哪些概念没有简单的一一对应

### Claude Code Checkpoint

Claude Code 的 checkpoint 和 `/rewind` 是具体产品能力。到了 Codex，不要只问“对应命令叫什么”，而要先明确目的：

- 想查看修改：看 diff
- 想恢复文件：使用 Git 或界面提供的撤销能力
- 想恢复会话：使用 session/thread 恢复
- 想尝试不同方案：先分支或创建 worktree

一个 Claude Code 名词，到了 Codex 可能需要几个不同工具共同完成。

### Claude Code Memory

Claude Code 的 `CLAUDE.md`、个人 memory、auto memory，不应简单等同于 Codex 的某一个文件。

在 Codex 中应按范围选择：

- 当前任务临时要求：写在本轮提示中
- 项目长期规则：`AGENTS.md`
- Codex 项目配置：`.codex/config.toml`
- 可复用流程：Skill
- 跨项目个人习惯：全局 guidance

### 自定义 Slash Command

两款产品都有 `/` 开头的内建交互命令，但“怎样创建自己的 `/xxx`”不是天然通用标准。学习这个仓库时，把重点放在：

- 为什么要复用提示词
- 何时人工触发
- 何时升级成 Skill

不要把某个产品的目录约定当成另一款产品的协议。

## 五、如果你主要使用 Codex，怎样学习本仓库

| 本仓库章节 | 在 Claude Code 中练什么 | 在 Codex 中迁移什么 |
|---|---|---|
| `01-slash-commands` | 安装并调用一个 command | 学会识别重复提示词，之后考虑 Codex Skill |
| `02-memory` | 编写和维护 `CLAUDE.md` | 编写和维护 `AGENTS.md` |
| `03-skills` | `.claude/skills` 和 `SKILL.md` | `.agents/skills` 和 `SKILL.md` |
| `04-subagents` | `.claude/agents/*.md` | `.codex/agents/*.toml` 与明确分工 |
| `05-mcp` | Claude Code MCP 配置 | 保留 server、工具、授权和最小权限思路，重写 Codex 配置 |
| `06-hooks` | Claude lifecycle hook | 保留触发场景，按 Codex 当前 Hook schema 重写 |
| `07-plugins` | Claude Code plugin 结构 | 学习“能力打包”的思路，再按 Codex plugin 结构实现 |
| `08-checkpoints` | `/rewind` 与 checkpoint | 使用 diff、Git、session 和 worktree 建立安全试错 |
| `09-advanced-features` | Claude 的 plan、权限、后台能力 | 对照 Codex 的 plan、sandbox、approval、长任务和 worktree |
| `10-cli` | `claude` 与 `claude -p` | 对照 `codex` 与 `codex exec` |

## 六、给小白的选择建议

### 当前任务只做一次

直接在提示词里说清楚，不要创建配置。

### 项目内每次都要遵守

- Claude Code：写进 `CLAUDE.md`
- Codex：写进 `AGENTS.md`

### 同一流程反复执行

两边都优先考虑 Skill；Claude Code 中短流程也可以使用自定义 command。

### 到特定时机必须自动检查

使用 Hook，但要分别按两款产品的配置格式编写。

### 需要实时访问外部系统

使用 MCP 或产品提供的 connector，并从只读、最小授权开始。

### 任务有多个真正独立的部分

使用 Subagents。只是任务很长但步骤相互依赖时，不一定适合并行。

## 七、最终记忆口诀

```text
项目规则：Claude 看 CLAUDE.md，Codex 看 AGENTS.md
复用流程：两边都能做 Skill，但目录不同
专业分工：两边都有 Subagents，但定义格式不同
外部连接：都能用 MCP，但客户端配置不同
自动检查：都有 Hooks，但支持类型和配置不同
脚本运行：Claude 用 claude -p，Codex 用 codex exec
安全原则：先只读、后写入；先小范围、后自动化
```

