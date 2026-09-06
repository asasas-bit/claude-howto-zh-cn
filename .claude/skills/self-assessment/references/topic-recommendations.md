# 按主题给出的学习建议

当某个主题是短板时，按这里生成具体建议。路径相对于本文件所在目录（`.claude/skills/self-assessment/references/`）。

**Slash Commands（得分 0）**:
- 教程：[01-slash-commands/](../../../../01-slash-commands/)
- 重点关注：内置命令参考、创建第一个 `SKILL.md`、`$ARGUMENTS` 语法
- 关键练习：创建一个 `/optimize` command 并测试
- 完成标准：你能创建带 arguments 和 dynamic context 的 custom skill

**Slash Commands（得分 1，需要复习）**:
- 重点关注：通过反引号 `!command` 注入 dynamic context、`@file` references、`disable-model-invocation` 与 `user-invocable` 的调用控制差异
- 完成标准：你能创建一个会注入 live command output、并控制自身触发方式的 skill

**Memory（得分 0）**:
- 教程：[02-memory/](../../../../02-memory/)
- 重点关注：创建 `CLAUDE.md`、`/init` 和 `/memory` commands、长期规则与一次性上下文的边界
- 关键练习：创建一个写有编码规范的项目级 `CLAUDE.md`
- 完成标准：Claude 能跨 session 记住你的项目偏好

**Memory（得分 1，需要复习）**:
- 重点关注：8 层 hierarchy 与 priority order、带 path-specific rules 的 `.claude/rules/` 目录、`@import` syntax（max depth 5）、Auto Memory 的 `MEMORY.md`（200-line limit）
- 完成标准：你有按目录拆分的 modular rules，并理解完整层级

**Skills（得分 0）**:
- 教程：[03-skills/](../../../../03-skills/)
- 重点关注：`SKILL.md` format、通过 `description` 自动触发、progressive disclosure（三层加载）
- 关键练习：安装 `code-review` skill 并验证它会自动触发
- 完成标准：skill 能根据对话场景自动激活

**Skills（得分 1，需要复习）**:
- 重点关注：`context: fork` 搭配 `agent` field 让 skill 在 subagent 执行、`disable-model-invocation` 与 `user-invocable`、1% context budget、bundled resources（`scripts/`、`references/`、`assets/`）
- 完成标准：你能创建一个在 forked context 的 subagent 中运行的 skill

**Hooks（得分 0）**:
- 教程：[06-hooks/](../../../../06-hooks/)
- 重点关注：hooks 配置结构（`matcher` + hooks array）、`PreToolUse` / `PostToolUse` events、exit codes（0=success, 2=block）、JSON input/output format
- 关键练习：创建一个能校验 Bash commands 的 `PreToolUse` hook
- 完成标准：hook 能在执行前阻止危险命令

**Hooks（得分 1，需要复习）**:
- 重点关注：31 个 hook 事件、5 种 hook 类型（`command`、`http`、`mcp_tool`、`prompt`、`agent`）、`DirectoryAdded`、`SKILL.md` frontmatter 里的 component-scoped hooks、带 `allowedEnvVars` 的 HTTP hooks、`SessionStart` / `CwdChanged` / `FileChanged` 可用的 `CLAUDE_ENV_FILE`
- 完成标准：你能创建一个 prompt-based `Stop` hook，以及一个 skill 内的 component-scoped hook

**MCP（得分 0）**:
- 教程：[05-mcp/](../../../../05-mcp/)
- 重点关注：`claude mcp add` command、transport types（HTTP recommended）、GitHub MCP 配置、environment variable expansion
- 关键练习：添加 GitHub MCP server 并查询 PRs
- 完成标准：你能通过 MCP 查询外部服务的 live data

**MCP（得分 1，需要复习）**:
- 重点关注：project-scope `.mcp.json`（需要团队 approval）、OAuth 2.0 auth、带 `@server:resource` mentions 的 MCP resources、Tool Search（`ENABLE_TOOL_SEARCH`）、`claude mcp serve`、output limits（10k / 25k / 50k）
- 完成标准：你有 project `.mcp.json`，并理解 Tool Search auto mode

**Subagents（得分 0）**:
- 教程：[04-subagents/](../../../../04-subagents/)
- 重点关注：agent file format（`.claude/agents/*.md`）、built-in agents（`general-purpose`、`Plan`、`Explore`）、`tools` / `model` / `permissionMode` config
- 关键练习：创建一个 `code-reviewer` subagent 并测试 delegation
- 完成标准：Claude 能把 code review 委派给你的 custom agent

**Subagents（得分 1，需要复习）**:
- 重点关注：worktree isolation（`isolation: worktree`）、persistent agent memory（带 scopes 的 `memory` field）、background agents（`Ctrl+B` / `Ctrl+F`）、`Task(agent_name)` allowlists、agent teams（`--teammate-mode`）
- 完成标准：你有一个带 persistent memory、并运行在 worktree isolation 中的 subagent

**Checkpoints（得分 0）**:
- 教程：[08-checkpoints/](../../../../08-checkpoints/)
- 重点关注：`Esc+Esc` 和 `/rewind` 入口、6 种 rewind options（恢复代码与对话、只恢复对话、只恢复代码、向后或向前摘要、取消）、限制（bash filesystem ops 不被追踪）
- 关键练习：做一组实验性改动，然后 rewind 恢复
- 完成标准：你能放心实验，并知道如何回退

**Advanced Features（得分 0）**:
- 教程：[09-advanced-features/](../../../../09-advanced-features/)
- 重点关注：planning mode（`/plan` 或 `Shift+Tab`）、permission modes、extended thinking（`Alt+T` toggle）
- 关键练习：用 planning mode 设计一个功能，再执行实现
- 完成标准：你能在 planning 和 implementation 之间自然切换

**Advanced Features（得分 1，需要复习）**:
- 重点关注：remote control（`claude remote-control`）、web sessions（`claude --remote`）、desktop handoff（`/desktop`）、worktrees（`claude -w`）、task lists（`Ctrl+T`）、enterprise managed settings 的使用场景
- 完成标准：你能在 CLI、web 和 desktop 之间交接 session

**Plugins（得分 0）**:
- 教程：[07-plugins/](../../../../07-plugins/)
- 重点关注：plugin structure（`.claude-plugin/plugin.json`）、plugin 能打包什么（commands、agents、MCP、hooks、settings）、marketplace installation
- 关键练习：安装一个 plugin 并查看它包含哪些组件
- 完成标准：你知道什么时候该用 plugin，而不是 standalone components

**Plugins（得分 1，需要复习）**:
- 重点关注：创建 `plugin.json` manifest、plugin hooks（`hooks/hooks.json`）、LSP configuration（`.lsp.json`）、`${CLAUDE_PLUGIN_ROOT}` variable、`--plugin-dir` testing、marketplace publishing
- 完成标准：你能为团队创建并测试一个 plugin

**CLI（得分 0）**:
- 教程：[10-cli/](../../../../10-cli/)
- 重点关注：interactive vs print mode、`claude -p` with piping、`--output-format json`、session management（`-c` / `-r`）
- 关键练习：把文件 pipe 给 `claude -p` 并获得 JSON output
- 完成标准：你能在脚本中非交互式使用 Claude

**CLI（得分 1，需要复习）**:
- 重点关注：带 JSON config 的 `--agents` flag、`--json-schema` structured output、`--fallback-model`、`--from-pr`、`--strict-mcp-config`、for loops batch processing、`claude mcp serve`
- 完成标准：你有一个使用 Claude 并输出 structured JSON 的 CI/CD script
