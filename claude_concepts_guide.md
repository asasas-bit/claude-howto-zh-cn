# Claude Code 概念总览

这个文件用于把仓库里最容易混淆的几个核心概念放在一起解释。

## 1. Slash Commands（快捷命令）

用户主动输入的快捷命令，适合显式触发某个动作。

`/fork [prompt]` 会复制当前对话为独立后台 session，结果不回传；`/subtask <task>` 会启动继承对话的 forked subagent，并在完成后回传结果；`/branch [name]` 则让你本人切换到对话副本。三者当前不是 alias。关闭 agent view 时，`/subtask` 不可用，`/fork` 保留旧的 forked-subagent 行为。无参数 `/resume` 会打开历史 session picker。

## 2. Memory（记忆）

Memory 包含两套互补机制：人维护的 `CLAUDE.md` 指令，以及 Claude 自己维护的 auto memory。Managed、User、Project、Local 四类 CLAUDE.md 会按范围**拼接**进上下文，不是严格覆盖链；`.claude/rules/*.md` 与 auto memory 是独立的相关机制。

`@path/to/file` 可以从 CLAUDE.md 导入外部文档，递归最大深度为 4 hops；相对路径以包含 import 的文件为基准。

auto memory 默认开启，可通过 `autoMemoryEnabled`、`/memory` 或 `CLAUDE_CODE_DISABLE_AUTO_MEMORY` 控制。单个 `CLAUDE.md` 当前建议目标控制在 200 行以内；import 不节省上下文，按路径内容应放到 `.claude/rules/*.md`。Claude Code 不会自动读取 `AGENTS.md`，需要时从 `CLAUDE.md` 导入或使用 symlink；subagent 定义仍放 `.claude/agents/`。

## 3. Skills（技能）

可复用、可自动触发的能力，适合沉淀稳定工作流。

同名 skill 的来源优先级是 Enterprise > Project > Personal；plugin skills 使用 namespace。`skillOverrides` 调整可见性和调用行为。

截至 `v2.1.220`，特别值得关注这些 bundled skills、plugin 和排障入口：

- `/run`：启动当前项目，确认改动能真实运行
- `/verify`：构建、运行并观察应用，确认修复不是只停留在测试通过；`v2.1.215+` 起仅显式调用
- `/run-skill-generator`：为项目生成专属 run / verify skill
- `/deep-research <topic>`：深入研究指定主题；`v2.1.218+` 起仅显式调用
- `/code-review [effort]`：审查当前 diff 的正确性缺陷；`v2.1.215+` 起仅显式调用，`v2.1.218+` 起在后台 subagent 中运行
- `/simplify`：清理型审查，关注复用、简化、效率和抽象层级，并应用修复
- `/dataviz`：图表和 dashboard 设计指导，附带可运行的调色板校验器
- `${CLAUDE_PROJECT_DIR}`：在 skill body 和 `allowed-tools` 中引用项目根目录绝对路径
- 一次调用可叠加最多 6 个开头的 slash-skills，重复 skill 内容会去重
- `context: fork` skills 从 `v2.1.218+` 起默认 `background: true`；设为 `false` 才在前台运行
- `/reload-skills`：重新扫描 skill 目录，不需要重启当前 session
- `disableBundledSkills` / `CLAUDE_CODE_DISABLE_BUNDLED_SKILLS=1`：隐藏内置 skills、workflows 和 commands
- `claude plugin init <name>`：在 `.claude/skills` 中脚手架本地 plugin，放在该目录的 plugin 会自动加载
- `/plugin list --enabled` / `--disabled`：按启用状态查看 installed plugins
- `/doctor`：诊断安装、配置和 plugin 健康状态；`v2.1.178+` 起界面是 flat tree 布局
- `/bug`：提交反馈；`v2.1.178+` 起必须填写描述
- `/review <pr>`：审查 GitHub PR；`v2.1.186+` 起复用 `/code-review medium` 的 review engine，本地 diff 仍用 `/code-review [effort]`

## 4. Subagents（子代理）

用于复杂任务拆分和专业分工的子代理。

当前版本从 `v2.1.219` 起默认允许 subagent 嵌套 spawn，默认深度为 3；设置 `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH=1` 可禁用嵌套。历史上，`v2.1.172` 到 `v2.1.216` 默认最多 5 层且不能配置，`v2.1.217` 到 `v2.1.218` 才短暂使用深度 1。要限制可 spawn 的对象，保留 `Agent(agent_type)` 语法，不要翻译成中文字段。

project agent 的 frontmatter hooks 只有在 agent 文件所在 workspace 通过 trust 后才运行；agent `name` 不能包含 `:`，因为该字符保留给 plugin namespace。

agent frontmatter 的 `color` 可写 `red`、`blue`、`green`、`yellow`、`purple`、`orange`、`pink` 或 `cyan`。

从 `v2.1.178+` 起，嵌套 `.claude/agents/` 里的同名 agent 会按“离当前工作目录最近者优先”加载；workflow 和 output-style 定义也遵循这个规则。

从 `v2.1.198+` 起，subagents 默认在后台运行，built-in `Explore` 会继承 session 模型（上限 Opus），extended thinking 也会继承。`CLAUDE_CODE_DISABLE_EXPLORE_PLAN_AGENTS=1` 可禁用 built-in Explore / Plan，`--append-subagent-system-prompt` 可在 print mode 中追加统一提示。

从 `v2.1.210+` 起，subagent 最终报告会扫描 instruction-shaped text；从 `v2.1.212+` 起，每个 session 默认最多 spawn 200 个 subagents，可用 `CLAUDE_CODE_MAX_SUBAGENTS_PER_SESSION` 调整，`/clear` 会重置预算。`v2.1.217+` 新增 `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`，默认最多同时运行 20 个。Task tool 的 `mode` 调用参数已弃用并被忽略，权限应通过 agent frontmatter 的 `permissionMode` 配置。

Agent Teams 的 teammate mode 也新增了 `--teammate-mode iterm2`，可把 teammate 放进 iTerm2 pane；该模式依赖 `it2` CLI。

## 5. MCP（外部工具协议）

让 Claude 连接外部工具和实时数据的协议。

从 `v2.1.186+` 起，`claude mcp login <name>` / `claude mcp logout <name>` 可以直接在 CLI 中处理 MCP server 登录状态；`--no-browser` 适合 SSH 或 headless session。

从 `v2.1.193+` 起，启动时会提示哪些 MCP server 仍需要认证；如果你用 `headersHelper` 提供动态认证头，遇到 HTTP 401 / 403 时会自动刷新。

从 `v2.1.203+` 起，MCP server 可通过 `roots/list` 获得启动目录和 `--add-dir` / `additionalDirectories`，目录变化时会收到 `notifications/roots/list_changed`。未信任 workspace 中的 project MCP 会保持 `Pending approval`，不能靠 `enableAllProjectMcpServers` 自动绕过。

从 `v2.1.212+` 起，MCP tool call 超过 2 分钟会自动转后台；`CLAUDE_CODE_MCP_AUTO_BACKGROUND_MS` 用于调整这个阈值，和无响应中止用的 `CLAUDE_CODE_MCP_TOOL_IDLE_TIMEOUT` 不是同一个设置。

从 `v2.1.219+` 起，`claude mcp list` 和 `/mcp` 会显示连接失败的 HTTP 状态与错误文本；配置值首尾空白会报警，headless stream-json init event 会通过 `mcp_server_errors` 暴露无效 `--mcp-config` server 的错误。

新增 MCP 时用 `--scope local|project|user`（短写 `-s`）控制保存范围，也可用 `claude mcp add-json`。JSON 中应显式保留 `type`；`streamable-http` 是 `http` 的 alias，凭证应从环境变量注入。

## 6. Hooks（钩子）

在特定事件上自动执行动作的机制。

从 `v2.1.172+` 起，hook handler 可以加 `if` 条件，用 `Edit(src/**)`、`Read(.env)`、`Bash(git push *)` 这类 permission-rule 语法按工具参数继续收窄匹配。

从 `v2.1.214+` 起，hook `if` 中的单段 `dir/**` 只匹配 `<cwd>/dir`；需要任意深度时写 `**/dir/**`。同一版本里，fork session 的 `SessionStart` source 改为 `"fork"`，不再报告 `"resume"`。

从 `v2.1.178+` 起，permission rule 还可以用 `Tool(param:value)` 形式按工具输入参数匹配。这个语法本身不要翻译。

从 `v2.1.191+` 起，`matcher` 支持 `"Write,Edit"` 这类逗号列表；从 `v2.1.195+` 起，工具名匹配更精确，带连字符的 MCP tool name 不会再因为子串重叠误触发。

这轮同步移除了上一版里关于 `Stop` / `SubagentStop` 可读取 `background_tasks`、`session_crons` 的说明；当前官方 hooks reference 没有列出这两个字段，写 hook 时不要依赖它们。

`Notification` matcher 新增 `agent_needs_input` 和 `agent_completed`；hook 输入新增 `prompt_id`，可与 OpenTelemetry `prompt.id` 对齐。

从 `v2.1.219+` 起共有 31 个 hook 事件；新增的 `DirectoryAdded` 会在 `/add-dir` 或 SDK `register_repo_root` 注册新工作目录后触发。`MessageDisplay` 和 `DirectoryAdded` 都是事件名，不能翻译。

shell hook 要阻断工具调用，必须把理由写到 stderr 并 `exit 2`；`exit 1` 是非阻断错误。`PreToolUse.permissionDecision` 支持 `allow`、`deny`、`ask`、`defer`，冲突优先级为 deny > defer > ask > allow。

## 7. Plugins（插件）

把 commands、skills、MCP、hooks、subagents 打包成整套方案。

从 `v2.1.187+` 起，`/plugin` 会提示 unused plugins；从 `v2.1.195+` 起，plugin 的 `plugin.json` `name` 和 marketplace entry name 不一致时，enable / disable 仍能正确工作。

marketplace entry 还支持 `renames`、`displayName`、`defaultEnabled`；`first-party-plugins` 和 `healthcare` 是官方保留的 marketplace 名称。

社区 marketplace 是 `anthropics/claude-plugins-community`，先用 `/plugin marketplace add` 添加，再以 `<plugin-name>@claude-community` 安装。第三方条目虽固定 commit SHA 并经过自动筛查，仍需自行审查权限和依赖。

## 8. Checkpoints（检查点）

用于安全试错和回退。

从 `v2.1.191+` 起，`/clear` 不再是 `/rewind` 的硬边界。需要时可以回到 `/clear` 之前创建的 checkpoint。

从 `v2.1.216+` 起，`/rewind` 遇到 symlink 或 hard link 路径会跳过，不再沿链接恢复或删除真实目标，并会报告跳过数量。

`Summarize up to here` 可以压缩所选位置之前的对话，与 `Summarize from here` 组成双向定点压缩。

`fileCheckpointingEnabled` 默认 `true`，`CLAUDE_CODE_DISABLE_FILE_CHECKPOINTING` 可禁用文件快照；`cleanupPeriodDays` 控制保留天数，但文件快照最多只保留最近 100 个 checkpoints。

## 9. CLI（命令行）

Claude Code 的核心使用入口，也是自动化、脚本化和 CI/CD 的关键接口。

`claude agents --json` 可以把 Agent View 列表输出为机器可读 JSON，适合接状态栏、脚本巡检或自定义 session picker。

在 `claude agents` 视图里，`Ctrl+T` 可以固定后台 session。已固定的 session 空闲时会被优先保留，升级 Claude Code 时也会在原位重启，只有内存压力较大时才会在未固定 session 之后被清理。

`/usage` 的成本页现在会按 skills、subagents、plugins、MCP server 等类别拆分，排查“钱花在哪里”会更直观。

`v2.1.174+` 的 VSCode Account & usage 视图还会显示 cache miss、long-context cost、subagents，以及 per-skill / per-agent / per-plugin / per-MCP 归因。

`/workflows` 可以查看 dynamic workflows 的运行记录，适合大规模审查、迁移、全仓扫描这类需要多代理编排的任务。

从 `v2.1.219+` 起，dynamic workflows 默认采用 medium 指引，目标少于 15 个 agents。可在 `/config` 的 **Dynamic workflow size** 中调整，或设置 `workflowSizeGuideline`；它是建议，不是并发硬上限。

`v2.1.160` 起，dynamic workflows 的触发关键词是 `ultracode`；裸词 `workflow` 不再触发运行。

`/model` 的默认行为也要注意：`v2.1.153+` 起选择模型会保存为后续 session 默认值；如果只想作用于当前 session，选中后按 `s`。

`--safe-mode` / `CLAUDE_CODE_SAFE_MODE=1` 适合排查自定义配置问题；`fallbackModel` 适合给主模型不可用时准备有序 fallback。

`claude auto-mode reset [--yes]` 用于恢复 Auto Mode 默认配置。Auto Mode 面向所有 plans，但仍受模型和 provider 资格限制；Team / Enterprise 默认可用，管理员可在 managed settings 中把 `permissions.disableAutoMode` 设为 `"disable"`。`CLAUDE_CODE_ENABLE_AUTO_MODE` 从 `v2.1.207` 起仅保留兼容性且不再生效。

直接进入 Auto Mode 应使用 `--permission-mode auto`；`--enable-auto-mode` 已在 `v2.1.111` 移除。`--max-budget-usd` 从 `v2.1.217+` 起达到上限时也会停止后台 subagents，`--settings` 文件上限为 2 MiB。

`--ax-screen-reader`、`CLAUDE_AX_SCREEN_READER=1` 或 `"axScreenReader": true` 会启用适合 screen reader 的纯文本渲染模式。

`wheelScrollAccelerationEnabled`、`footerLinksRegexes`、`language`、`workflowSizeGuideline` 是 settings.json 里的 key，说明文字可以中文化，但 key 本身不要翻译。

`respondToBashCommands` 控制 `!` bash 命令输出后是否自动让 Claude 回复；默认 `true`，设为 `false` 可回到只把输出放进上下文的旧行为。

交互 permission mode 从 `v2.1.200+` 起显示为 `manual`，旧 `default` 仍是 alias。`askUserQuestionTimeout`、`enableArtifact`、`CLAUDE_ENABLE_STREAM_WATCHDOG`、Sonnet 5 的 `claude-sonnet-5` 和默认 Opus 模型 `claude-opus-5` 都已进入当前口径。Opus 5 是 1M context，默认 effort 为 `high`；`/fast` 只适用于 Opus 5 和 Opus 4.8。

Output Styles 通过 `/config` 或 `outputStyle` 设置；`/output-style` 已移除。`/statusline` 和 `statusLine` 可配置底部状态栏。`switchModelsOnFlag: false` 会在安全标记触发时暂停，让用户决定是否切换模型。

从 `v2.1.193+` 起，`!` bash mode 支持 live file-path autocomplete。`autoMode.classifyAllShell` 可以让所有 Bash / PowerShell 命令都过 Auto Mode 分类器，`claude_code.assistant_response` 可把模型回复文本写进 OpenTelemetry log event。

`CLAUDE_CLIENT_PRESENCE_FILE`、`CLAUDE_CODE_MAX_RETRIES`、`CLAUDE_CODE_RETRY_WATCHDOG`、`CLAUDE_CODE_MCP_TOOL_IDLE_TIMEOUT`、`CLAUDE_CODE_MCP_AUTO_BACKGROUND_MS`、`CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION`、`CLAUDE_CODE_MAX_SUBAGENTS_PER_SESSION`、`CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`、`CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`、`CLAUDE_CODE_OTEL_CONTENT_MAX_LENGTH`、`FORCE_HYPERLINK`、`CLAUDE_CODE_DISABLE_MOUSE_CLICKS` 是环境变量标识，不要翻译。`sandbox.credentials`、`sandbox.allowAppleEvents`、`sandbox.filesystem.disabled`、`sandbox.network.strictAllowlist`、`emojiCompletionEnabled`、`workflowSizeGuideline`、`autoMode.classifyAllShell` 和 `/config key=value` 属于配置 / 命令口径，也要保持原文。print mode 的 `--forward-subagent-text` 从 `v2.1.219+` 起也会转发深度 2 及更深的 subagent 文本。
