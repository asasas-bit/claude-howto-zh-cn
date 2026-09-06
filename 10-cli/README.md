<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../resources/logos/claude-howto-logo-dark.svg">
  <img alt="Claude How To" src="../resources/logos/claude-howto-logo.svg">
</picture>

# CLI 指南

Claude Code 的 CLI 是最核心的使用入口。
很多功能看起来像“对话式能力”，但真正要高效使用、做自动化、接入脚本或 CI/CD，最后都绕不开 CLI。

---

## 最常用的命令

| 命令 | 用途 |
|------|------|
| `claude` | 打开交互模式 |
| `claude "query"` | 带初始问题进入 REPL |
| `claude -p "query"` | print mode，一次执行后退出 |
| `claude -c` | 继续最近一次会话 |
| `claude -r "session"` | 恢复指定 session |
| `claude mcp` | 管理 MCP |
| `claude agents` | 打开 Agent View，多 session 管理界面 |
| `claude agents --json` | 以 JSON 输出 Agent View session 列表，适合脚本、状态栏和 session picker |
| `claude plugin` | 管理 plugins |
| `claude remote-control` | 启动远程控制 |
| `claude auth status` | 查看登录状态 |
| `claude project purge [path]` | 清理某个项目的本地 Claude Code 状态，先用 `--dry-run` 预览 |
| `claude plugin prune` | 清理无主的自动安装 plugin 依赖 |
| `claude ultrareview [target]` | 在无头模式里运行 `/ultrareview`，适合 CI / PR gate |
| `claude auto-mode reset [--yes]` | 恢复 Auto Mode 默认配置；`--yes` 跳过确认（`v2.1.212+`） |

如果你是新手，先熟悉 `claude`、`claude -p`、`claude -c`、`claude -r` 就已经很有价值。

## 登录状态与 exit code

`claude auth status` 不只给人看，也适合脚本判断认证状态：已登录时 exit code 为 `0`，未登录时为 `1`。在 CI/CD 中先检查这个返回值，可以比等到正式请求失败更早发现凭证问题。

---

## 交互模式 vs print mode

### 交互模式

适合：

- 连续问答
- 多轮上下文
- 现场探索
- 需要边改边聊

```bash
claude
claude "explain this project"
```

### print mode（输出模式）

适合：

- 一次性任务
- shell 脚本
- CI/CD
- 通过 pipe 处理输入
- 结构化输出

```bash
claude -p "what does this function do?"
cat error.log | claude -p "explain this error"
```

### 一个实用判断标准

- 你要连续来回对话：交互模式
- 你要“给一条明确任务，然后退出”：print mode

---

## 新手最该掌握的 flags

| flag | 用途 |
|------|------|
| `-p, --print` | 进入 print mode |
| `-c, --continue` | 继续最近一次会话 |
| `-r, --resume` | 恢复指定 session |
| `-n, --name` | 给 session 起名 |
| `-w, --worktree` | 在 worktree 中启动 |
| `--model` | 指定模型 |
| `--effort` | 指定思考强度；Opus 5 默认 `high`，支持 `low` 到 `max` |
| `--permission-mode` | 指定权限模式 |
| `--permission-mode auto` | 直接以 Auto Mode 启动；替代已经移除的 `--enable-auto-mode` |
| `--bare` | 以最小模式启动 |
| `--safe-mode` | 禁用 CLAUDE.md、plugins、skills、hooks、MCP servers，用于隔离配置问题 |
| `--add-dir` | 加额外目录到工作上下文 |
| `--tmux` | 给 worktree / 多任务场景创建 tmux 会话 |
| `--exclude-dynamic-system-prompt-sections` | 排除系统提示中的动态段落，帮助 prompt cache 更稳定命中 |
| `--ax-screen-reader` | 使用适合 screen reader 的纯文本渲染模式（`v2.1.208+`） |
| `--forward-subagent-text` | 在 stream-json 中转发 subagent 文本；`v2.1.219+` 包含深度 2+ 的嵌套 subagents，并按触发它的 `Agent` `tool_use` ID 关联 |

---

## 一些真正常用的例子

### 查看项目

```bash
claude "explain this project"
```

### 处理日志

```bash
cat error.log | claude -p "explain this error"
```

### 继续最近一次工作

```bash
claude -c
```

### 恢复命名会话

```bash
claude -r "auth-refactor" "finish this task"
```

### 用于自动化

```bash
claude -p "Run tests and summarize failures" --permission-mode dontAsk
```

### 批量处理文件

批处理通常用 shell loop 配合 print mode，每个文件独立调用一次：

```bash
for file in *.md; do
  claude -p "summarize: $(cat "$file")" > "${file%.md}.json"
done
```

文件名、引号和输出路径要按当前 shell 调整；不要假设存在一个通用的 `--batch *.md` flag。

---

## 模型与配置

CLI 常见会和这些配置一起使用：

- `--model`
- `--fallback-model`
- `--effort`
- `--settings`
- `--append-system-prompt`
- `--append-subagent-system-prompt`

示例：

```bash
claude --model opus "design a caching strategy"
claude -p --fallback-model sonnet "summarize this diff"
claude --append-system-prompt "Always explain tradeoffs" "review this plan"
claude -p --append-subagent-system-prompt "Cite sources" "review this project"
```

如果你要长期使用 Claude Code，把模型、权限、输出格式这些参数理解清楚，会直接影响效率和成本。

### 这轮 CLI / 平台更新里值得知道的变化

- **Sonnet 5**（`claude-sonnet-5`）提供原生 1M context window，并按订阅档位成为 Pro / Team Standard / Enterprise seats 的默认模型
- **Claude Opus 5**（`claude-opus-5`）提供 1M context window，并成为 Max、Team Premium、Enterprise pay-as-you-go、Anthropic API、Claude Platform on AWS、Bedrock 和 Vertex AI 的默认 Opus 模型；Microsoft Foundry 的 `opus` alias 仍解析为 Opus 4.6
- 组织管理员设置默认模型时，`/model` 会标注 `Org default`（或 `Role default`，`v2.1.196+`）
- `--append-subagent-system-prompt` 可在非交互 / print mode 中给每个 subagent 的 system prompt 追加内容（`v2.1.205+`）
- Opus 5 默认 effort 是 `high`，支持 `low` 到 `max`；Sonnet 5 与 Opus 4.8 也支持全部五档，Opus 4.7 默认 `xhigh`
- `/model` 现在默认保存为后续 session 默认值；如果只想作用于当前 session，选中后按 `s`
- Fast Mode 从 `v2.1.219+` 起只适用于 Opus 5 和 Opus 4.8；Opus 4.6 / 4.7 不再是 Fast Mode 目标，`CLAUDE_CODE_OPUS_4_6_FAST_MODE_OVERRIDE` 仍是 no-op
- 新增 `/reload-skills` 和 `/workflows`，分别用于重扫 skills 和查看 dynamic workflows
- 新增 `claude plugin init <name>`，可在 `.claude/skills` 中脚手架本地 plugin
- 从 `v2.1.207` 起，Bedrock / Vertex AI / Microsoft Foundry 上受支持模型的 Auto Mode 不再需要 `CLAUDE_CODE_ENABLE_AUTO_MODE=1`；该变量仅为历史兼容而保留，当前不产生效果
- `--enable-auto-mode` 已在 `v2.1.111` 移除；需要直接进入 Auto Mode 时使用 `--permission-mode auto`
- Auto Mode 面向所有 plans，但仍受模型和 provider 资格限制；Team / Enterprise 默认可用，管理员可在 managed settings 中把 `permissions.disableAutoMode` 设为 `"disable"`
- `v2.1.212+` 可用 `claude auto-mode reset [--yes]` 恢复 Auto Mode 默认配置
- `workflowSizeGuideline` 控制 dynamic workflow 建议规模；默认 medium，目标少于 15 个 agents，它不是并发硬上限
- `--max-budget-usd` 从 `v2.1.217+` 起达到预算上限时会停止已经运行的后台 subagents，并拒绝继续 spawn
- `--settings` 读取的文件从 `v2.1.214+` 起不得超过 2 MiB
- `--ax-screen-reader`、`CLAUDE_AX_SCREEN_READER=1` 或 `"axScreenReader": true` 可以启用纯文本 screen reader 渲染模式
- `EnterWorktree` 可以在同一 session 中切换 Claude 管理的 worktree
- `/cd <path>` 可以在保留 prompt cache 的情况下切换当前 session 工作目录
- `--safe-mode` / `CLAUDE_CODE_SAFE_MODE=1` 适合排查 CLAUDE.md、plugins、skills、hooks、MCP 带来的配置问题
- `fallbackModel` 最多可以配置三个 fallback models；`--fallback-model` 从 `v2.1.166+` 起也适用于交互式 session
- `claude-fable-5` 出现在上游模型表里，作为模型 ID 时不要翻译
- Windows 侧正在逐步拿到更专门的 PowerShell tool
- 主题里新增了更贴近终端外观的 Auto 模式
- 只读型 Bash / Glob 调用的权限提示比以前更安静
- `ANTHROPIC_BASE_URL` 指向兼容网关时，`/model` 不再默认自动发现远端模型；现在需要显式设置 `CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY=1`
- `claude auth login` 在浏览器 callback 打不回 localhost 时，可以把 OAuth code 粘回终端继续登录
- `/doctor` 在 `v2.1.178+` 改成 flat tree 布局，状态图标更清晰
- `/bug` 在 `v2.1.178+` 必须填写描述后才能提交
- `/review <pr>` 在 `v2.1.186+` 起用于审查 GitHub PR，并复用 `/code-review medium` 的 review engine；当前本地 diff 仍用 `/code-review [effort]`
- `claude mcp login <name>` / `claude mcp logout <name>` 可直接处理 MCP server 登录状态，`--no-browser` 适合 SSH 或 headless session
- `!` bash 命令输出会自动发给 Claude 并触发回复；如果只想把输出放进上下文，把 `respondToBashCommands` 设为 `false`
- Opus 5 的 cybersecurity classifier 命中后会在 Opus 4.8 上重跑；biology classifier 命中后直接拒绝，不走 fallback

### settings.json 里新增的几个 key

这些不是 CLI flag，也不是环境变量，而是放在 `~/.claude/settings.json`、`.claude/settings.json` 或托管 settings 里的配置 key。key 名保持英文，说明文字可以中文化。

| key | 用途 |
|-----|------|
| `wheelScrollAccelerationEnabled` | 从 `v2.1.174+` 起可设为 `false`，关闭全屏 renderer 里的鼠标滚轮加速 |
| `footerLinksRegexes` | 从 `v2.1.176+` 起可配置正则数组，把匹配到的链接显示成 footer badges |
| `language` | 设置 Claude Code 偏好的回复语言和语音听写语言；从 `v2.1.176+` 起，自动生成的 session title 也会按这个语言固定 |
| `respondToBashCommands` | 从 `v2.1.186+` 起控制 `!` bash 命令输出后是否自动让 Claude 回复；默认 `true`，设为 `false` 可回到只进上下文的旧行为 |
| `permissions.disableAutoMode` | 在 managed settings 中设为 `"disable"`，关闭 Team / Enterprise 默认可用的 Auto Mode |
| `axScreenReader` | 设为 `true` 后启用纯文本 screen reader 渲染模式（`v2.1.208+`） |
| `sandbox.filesystem.disabled` | 跳过 filesystem isolation，但继续执行 network isolation；仅 user / managed settings 或 `--settings` 可设置（`v2.1.216+`） |
| `sandbox.network.strictAllowlist` | sandboxed command 访问非 allowlist host 时直接拒绝，不弹权限询问（`v2.1.219+`） |
| `emojiCompletionEnabled` | 控制 prompt 输入框里的 emoji shortcode 自动补全（`v2.1.217+`） |
| `workflowSizeGuideline` | dynamic workflow 的建议规模；默认 medium，目标少于 15 个 agents（`v2.1.219+`） |

示例：

```json
{
  "wheelScrollAccelerationEnabled": false,
  "language": "french",
  "footerLinksRegexes": [".*jira\\.example\\.com/.*"],
  "respondToBashCommands": false
}
```

---

## 这轮 CLI 更新里，最值得你知道的一个新 flag

```bash
claude --tmux
```

它适合：

- 你已经开始频繁用 worktrees
- 想把多个任务分屏展示
- 想为更复杂的多终端协作留出界面空间

如果你还处在基础阶段，不必先学它；但当你开始并行做多条任务线时，它会很有用。

---

## 项目状态清理：`claude project purge`

`claude project purge` 用来删除某个项目在本机留下的 Claude Code 状态，例如 transcripts、tasks、debug logs、file-edit history、prompt history，以及 `~/.claude.json` 中的项目记录。

先预览，不落盘删除：

```bash
claude project purge ~/work/repo --dry-run
```

确认后清理指定项目：

```bash
claude project purge ~/work/repo --yes
```

逐个确认所有项目：

```bash
claude project purge --all --interactive
```

这个命令清的是 Claude Code 本地状态，不是你的 Git 仓库源码。即便如此，也建议先跑 `--dry-run` 看清楚会删什么。

---

## 工具与权限相关 flags

下面这些参数非常重要，但也是最容易被误用的一组：

- `--permission-mode`
- `--dangerously-skip-permissions`
- `--allowedTools`
- `--disallowedTools`
- `--tools`

这里还有一个这轮修掉的老坑值得知道：

- 从 `v2.1.132+` 起，`--permission-mode` 在 `--continue` / `--resume` 场景下也会真正生效
- 旧版本里你即使恢复 session 时重新带了 `--permission-mode plan`，也可能悄悄降回别的模式

### 实用例子

```bash
# 只做只读分析
claude --permission-mode plan "review this codebase"

# 非交互测试摘要
claude -p "Run tests" --permission-mode dontAsk

# 限制工具范围
claude -p --tools "Read,Grep,Glob" "find all TODO comments"
```

### permission rule 可以按参数匹配

从 `v2.1.178+` 起，permission rules 除了 `Tool` 或 `Tool(pattern)`，还可以用 `Tool(param:value)` 形式按工具输入参数继续细化匹配，并支持通配。

这和你已经熟悉的 `Bash(...)`、`Read(...)` 是同一类安全边界，只是匹配粒度更细。例子：

```text
Bash(npm run test *)
Read(./.env.*)
Tool(param:value)
```

真实项目里不要凭空猜参数名，先查当前版本的 permissions / settings reference。这里的 `Tool(param:value)`、`Bash(...)`、`Read(...)` 都是规则语法，不能翻译。

从 `v2.1.214+` 起还有三项 permission hardening：Docker / Podman 使用 `--url`、`--connection`、`--identity` 等 daemon redirect flag 时会要求确认；`file` 命令使用 `-m` / `--magic-file` 或 `-f` / `--files-from` 时会要求确认；超过 10,000 字符的 Bash 命令无论 allow rule 如何都会提示确认。

---

## 输出与格式

如果你要把 Claude Code 接进脚本或程序，最值得关注的是：

- `--output-format`
- `--json-schema`
- `--include-partial-messages`
- `--max-budget-usd`

### 常见使用方式

```bash
# 默认文本输出
claude -p "explain this code"

# JSON 输出
claude -p --output-format json "list all functions in main.py"

# 用 schema 约束结构
claude -p --json-schema '{"type":"object"}' "return structured analysis"

# 设置 print mode 预算；v2.1.217+ 达到上限时也会停止后台 subagents
claude -p --max-budget-usd 5.00 "analyze this repository"
```

如果你的下游还要接 `jq`、Python、Node 或 CI job，结构化输出会非常有用。

---

## workspace 与多目录

如果你需要让 Claude 同时看多个目录，可以用：

```bash
claude --add-dir ../frontend ../backend ../shared "find all API endpoints"
```

这对 monorepo、前后端分仓或跨目录排查问题特别有帮助。

---

## MCP 与 plugin 相关 CLI

你不只会在文档里看到：

- `claude mcp`
- `claude mcp serve`
- `claude mcp login <name>`
- `claude mcp logout <name>`
- `claude plugin`
- `claude plugin init <name>`
- `claude plugin prune`
- `claude plugin uninstall <name> --prune`

你实际使用中也经常会碰到它们。

### 典型场景

```bash
claude mcp
claude mcp serve
claude mcp login github
claude mcp login github --no-browser
claude mcp logout github
claude plugin init my-plugin
claude plugin install my-plugin
claude plugin prune
```

如果你要做自动化、集成第三方系统或团队分发，这些命令迟早会用到。

---

## `--agents` 与 agent 优先级

CLI 也可以在当前 session 临时定义 agents：

```bash
claude --agents "$(cat agents.json)" "review the auth module"
```

当同名 agent 同时出现在多个位置时，优先级要按新版口径记：

1. `--agents`：当前 session 临时定义
2. `.claude/agents/`：当前项目
3. `~/.claude/agents/`：用户级默认配置

所以 `--agents` 会覆盖项目级和用户级；项目级会覆盖用户级。
完整背景可以回看 [Subagents 指南](../04-subagents/README.md#agent-定义优先级)。

---

## session 管理

当你开始做稍复杂的工作后，session 管理会非常重要。

常见场景：

- 延续昨天的任务
- 给当前任务起名
- 从当前会话分叉出实验方案

常用命令和 flags：

- `/resume`（无参数时打开历史 session picker，并把选中项作为后台 session 恢复）
- `/rename`
- `/fork [prompt]`（复制成独立后台 session，之后不回传结果）
- `/subtask <task>`（委派给继承对话的 forked subagent，完成后回传结果）
- `/branch [name]`（切换到当前对话的副本，并保留原对话）
- `claude -c`
- `claude -r`

`/fork`、`/subtask` 与 `/branch` 当前不是 alias。`v2.1.212+` 中，`/fork` 与 `/subtask` 对调了旧角色；关闭 agent view 时，`/subtask` 不可用，`/fork` 保留 forked-subagent 行为。不命名 session，前期感觉没问题，后期会越来越难管理。

---

## CLI 和自动化的关系

当你要做这些事情时，CLI 会变得尤其重要：

- CI/CD
- shell 脚本
- 批处理
- JSON 输出
- 定时任务
- 后台任务编排

很多“高级能力”最后都会落回 CLI 参数和脚本调用层。

所以如果你真想把 Claude Code 用深，CLI 不是可选项，而是核心能力。

### 无头 `ultrareview`

`claude ultrareview [target]` 可以把 `/ultrareview` 放到脚本或 CI 里运行。

```bash
claude ultrareview 1234 --json > review.json
```

它会把审查结果输出到 stdout；成功退出码为 `0`，失败或发现阻断性问题时退出码为 `1`。
如果默认 30 分钟不够，可以加 `--timeout <minutes>`。

---

## 新增环境变量

这轮 CLI 相关更新里，下面这些环境变量对自动化、云厂商部署和模型行为排查比较有用：

| 环境变量 | 用途 |
|----------|------|
| `ANTHROPIC_BEDROCK_SERVICE_TIER` | 在 Bedrock 上选择服务档位：`default`、`flex` 或 `priority` |
| `AI_AGENT` | Claude Code 启动子进程时自动设置，方便外部 CLI（例如 `gh`）识别调用来源 |
| `CLAUDE_CODE_FORCE_SYNC_OUTPUT` | 在终端能力自动检测失误时强制同步输出，例如 Emacs `eat` |
| `CLAUDE_CODE_PACKAGE_MANAGER_AUTO_UPDATE` | 为 Homebrew / WinGet 安装启用后台升级 |
| `CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY` | 在设置了 `ANTHROPIC_BASE_URL` 时，显式开启 `/v1/models` 网关发现 |
| `CLAUDE_CODE_ENABLE_AUTO_MODE` | `v2.1.158` 到 `v2.1.206` 的 Auto Mode opt-in；从 `v2.1.207` 起仅为历史兼容而保留，不再产生效果 |
| `CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION` | 每个 session 的 WebSearch 调用上限，默认 200（`v2.1.212+`） |
| `CLAUDE_CODE_MAX_SUBAGENTS_PER_SESSION` | 每个 session 的 subagent spawn 上限，默认 200；`/clear` 会重置预算（`v2.1.212+`） |
| `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS` | 同时运行的 subagents 上限，默认 20（`v2.1.217+`） |
| `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH` | 允许 subagent 嵌套 spawn 的最大深度；`v2.1.219+` 默认 `3`，设为 `1` 可禁用嵌套 |
| `CLAUDE_CODE_MCP_AUTO_BACKGROUND_MS` | MCP tool call 自动转后台的阈值，默认 `120000` 毫秒（2 分钟，`v2.1.212+`） |
| `CLAUDE_AX_SCREEN_READER` | 设为 `1` 后启用纯文本 screen reader 渲染模式，等同于 `--ax-screen-reader` 或 `"axScreenReader": true` |
| `CLAUDE_CODE_SAFE_MODE` | 设为 `1` 后以 safe mode 启动，禁用 CLAUDE.md、plugins、skills、hooks、MCP servers |
| `CLAUDE_CODE_DISABLE_BUNDLED_SKILLS` | 设为 `1` 后隐藏内置 skills、workflows 和 commands |
| `CLAUDE_CODE_OPUS_4_6_FAST_MODE_OVERRIDE` | `v2.1.160` 起已经是 no-op；`v2.1.219+` 的 Fast Mode 只适用于 Opus 5 和 Opus 4.8 |
| `CLAUDE_CODE_DISABLE_ALTERNATE_SCREEN` | 设为 `1` 后，停留在普通终端滚动历史里，而不是 fullscreen alternate-screen 渲染 |
| `CLAUDE_CODE_SESSION_ID` | 每个 Bash tool 子进程都会带上这个 session UUID，可用来和 hooks / telemetry 对日志 |
| `CLAUDE_CODE_ENABLE_FEEDBACK_SURVEY_FOR_OTEL` | 在 OTEL 环境下重新打开 Anthropic 的会话质量问卷 |
| `CLAUDE_CODE_OTEL_CONTENT_MAX_LENGTH` | OpenTelemetry content attribute 的截断上限，默认 60 KB（`v2.1.214+`） |
| `FORCE_HYPERLINK` | 设为 `0` 后关闭 footer 中可点击的 PR badge 链接（`v2.1.217+`） |
| `CLAUDE_CLIENT_PRESENCE_FILE` | 指向一个本机 marker file，人在电脑前时抑制 mobile push notifications；变量名不是 `CLAUDE_CODE_CLIENT_PRESENCE_FILE` |
| `CLAUDE_CODE_MAX_RETRIES` | API retry 最大次数；`v2.1.186+` 起上限为 15 |
| `CLAUDE_CODE_RETRY_WATCHDOG` | 面向无人值守 session 的 retry 控制，比盲目提高 `CLAUDE_CODE_MAX_RETRIES` 更稳 |
| `CLAUDE_ENABLE_STREAM_WATCHDOG` | streaming idle watchdog 默认对所有 provider 开启；连续 5 分钟没有 stream event 会 abort / retry，设为 `0` 可禁用（`v2.1.196+`） |
| `CLAUDE_CODE_MCP_TOOL_IDLE_TIMEOUT` | 覆盖 remote MCP tool 5 分钟无响应 abort 的默认值 |
| `CLAUDE_CODE_DISABLE_MOUSE_CLICKS` | 设为 `1` 后禁用 fullscreen mode 里的 mouse click / drag / hover；wheel scroll 仍可用（`v2.1.195+`） |

这些名字属于可执行标识，不要翻译。

### Gateway model discovery 现在是显式 opt-in

这点和我们上次同步相比有一个重要变化：

- 旧口径：只要设置了 `ANTHROPIC_BASE_URL`，`/model` 就会从网关 `/v1/models` 拉模型列表
- 新口径：从 `v2.1.129` 起，必须再额外设置 `CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY=1`

如果不加这个环境变量，`/model` 会退回到内置静态模型列表。
这个改动是为了避免网关返回你理论上看得见、实际上没权限用的模型。

---

## 哪些内容绝对不能翻

如果你在本地化文档，这些内容必须保持英文原样：

- `claude`
- `claude -p`
- flags，例如 `--model`、`--permission-mode`
- 子命令，例如 `claude mcp`、`claude plugin`
- 输出格式名，例如 `json`

CLI 是最典型的“说明文本可以翻，命令本身不能翻”的内容。

---

## 中国用户特别注意

### 1. 网络环境

如果你在公司网络、代理或受控环境下使用 CLI，先确认：

- API 访问
- GitHub 连通性
- npm / uv / Python 依赖下载
- 证书与代理设置

### 2. Windows / WSL 差异

Windows 用户建议尽早确认自己使用的是：

- PowerShell
- Git Bash
- WSL

这会直接影响路径、命令行为和脚本兼容性。

新版 Claude Code 不再强制依赖 Git Bash；缺少 Git Bash 时可以走 PowerShell。
如果开启了 PowerShell tool，PowerShell 会成为主 shell，PowerShell 7 的检测也更完整。

### 3. 自动化不要一开始就开太猛

建议从这些低风险任务开始：

- 日志解释
- 测试摘要
- 结构化分析

不要一开始就上高权限全自动修改流程。

---

## 常见坑

### 1. 把 print mode 当普通聊天

`claude -p` 更适合一次性、明确输入输出的任务。

### 2. 不给 session 命名

短期还行，任务一多就会混乱。

### 3. 翻译 CLI flags

这会让用户复制命令后直接失败。

### 4. 没区分“能跑”和“适合自动化”

某个命令能跑，不代表它就适合直接放进 CI/CD。

---

## 故障排查

如果 CLI 行为不符合预期，优先排查：

1. 当前是不是该用交互模式，而不是 print mode
2. flags 是否拼对
3. 权限模式是否合适
4. 环境变量是否已导出
5. 当前 shell / 路径环境是否匹配

---

## 最佳实践

### `claude agents` 视图

从 `v2.1.139` 开始，`claude agents` 不只是列出 agents，而是打开一个多 session 管理界面。
从 `v2.1.145` 开始，可以加 `--json` 输出机器可读列表，方便你接到 tmux 状态栏、自定义 session picker 或自动巡检脚本里。
从 `v2.1.147` 开始，在 `claude agents` 视图里可以对某个 session 按 `Ctrl+T` 进行 pin。已固定的后台 session 空闲时会被优先保留，Claude Code 升级时会在原位重启，遇到内存压力时也会排在未固定 session 之后再被清理。注意这里的 `Ctrl+T` 只作用于 Agent View；主会话里的 `Ctrl+T` 仍是任务列表视图切换。

- 先熟练 `claude`、`claude -p`、`claude -c`、`claude -r`
- 自动化从小任务开始
- 所有 CLI 示例都保留英文原样
- 把 session 命名当成好习惯
- 中国用户优先排除网络与 shell 环境问题

---

## 推荐下一步

- 想更系统地看高级能力：看 [09-advanced-features](../09-advanced-features/)
- 想查安装与路径：看 [QUICK_REFERENCE.md](../QUICK_REFERENCE.md)
- 想结合 hooks / MCP / plugins：回看 [06-hooks](../06-hooks/)、[05-mcp](../05-mcp/)、[07-plugins](../07-plugins/)
