<picture>
  <source media="(prefers-color-scheme: dark)" srcset="resources/logos/claude-howto-logo-dark.svg">
  <img alt="Claude How To" src="resources/logos/claude-howto-logo.svg">
</picture>

# Claude Code 功能总表（Feature Catalog）

> 适合“先建立全局地图，再进入某个模块”的读者。

**快速导航**：
[Slash Commands](#slash-commands快捷命令) | [Permission Modes](#permission-modes权限模式) | [Subagents](#subagents子代理) | [Skills](#skills技能) | [Plugins](#plugins插件) | [MCP](#mcp外部工具协议) | [Hooks](#hooks钩子) | [Memory](#memory记忆) | [新功能提示](#新功能提示)

---

## 总览

| 类别 | 内建能力 | 仓库示例 | 适合先学吗 | 入口 |
|------|----------|----------|------------|------|
| Slash Commands | 60+ | 8 | 非常适合 | [01-slash-commands/](01-slash-commands/) |
| Memory | 2 套机制 | 3 | 非常适合 | [02-memory/](02-memory/) |
| Skills | bundled skills + 示例 | 多个 | 适合进阶 | [03-skills/](03-skills/) |
| Subagents | 6 个内建 | 多个 | 适合进阶 | [04-subagents/](04-subagents/) |
| MCP | 1 个内建生态入口 + 示例 | 多个 | 适合集成场景 | [05-mcp/](05-mcp/) |
| Hooks | 31 个事件 | 11 | 适合自动化 | [06-hooks/](06-hooks/) |
| Plugins | - | 3 | 适合团队级方案 | [07-plugins/](07-plugins/) |
| Checkpoints | 内建 | 示例文档 | 新手必学 | [08-checkpoints/](08-checkpoints/) |
| Advanced Features | 多项 | 示例文档 | 高阶再学 | [09-advanced-features/](09-advanced-features/) |
| CLI | 内建 | 参考文档 | 全阶段都用得到 | [10-cli/](10-cli/) |

---

## Slash Commands（快捷命令）

slash commands 是用户在 Claude Code 里主动输入的快捷操作，例如 `/help`、`/model`、`/rewind`。这也是新手最容易立刻感受到收益的能力。

### 常见内建命令

| 命令 | 用途 |
|------|------|
| `/help` | 查看帮助 |
| `/clear` | 清空当前对话 |
| `/config` | 查看或编辑配置 |
| `/agents` | 查看可用 agents |
| `/skills` | 查看可用 skills |
| `/hooks` | 查看 hooks |
| `/mcp` | 查看或管理 MCP servers |
| `/plugin` | 管理 plugins |
| `/doctor` | 诊断安装、配置和 plugin 健康；`v2.1.178+` 起是 flat tree 布局 |
| `/feedback` / `/bug` | 提交反馈；`/bug` 从 `v2.1.178+` 起必须填写描述 |
| `/plan` | 进入 planning mode |
| `/proactive` | `/loop` 的别名 |
| `/recap` | 返回旧 session 时快速回顾上下文 |
| `/rewind` | 回退到 checkpoint |
| `/resume` | 恢复之前的 session；无参数时打开历史 session picker |
| `/team-onboarding` | 根据当前项目配置生成新人上手说明 |
| `/tui` | 切换全屏 TUI 模式 |
| `/focus` | 切换 focus view |
| `/undo` | `/rewind` 的别名 |
| `/ultraplan` | 把计划起草交给浏览器里的云端会话 |
| `/ultrareview` | 云端多代理代码审查 |
| `/fewer-permission-prompts` | 分析调用记录并建议 allowlist |
| `/reload-skills` | 重新扫描 skill 目录，不需要重启 session |
| `/workflows` | 查看正在运行和已完成的 dynamic workflows |
| `/usage` | 查看 plan 用量、限流状态和成本；`v2.1.149+` 起成本视图会按 skills、subagents、plugins、MCP server 等类别拆分，`v2.1.174+` 的 VSCode Account & usage 视图还会显示 cache miss、long-context cost、subagents 以及 per-skill / per-agent / per-plugin / per-MCP 归因 |
| `/usage-credits` | 配置额外用量额度；`/extra-usage` 仍可作为 alias（别名）使用 |
| `/review <pr>` | 审查 GitHub PR；`v2.1.186+` 起复用 `/code-review medium` 的 review engine，本地 diff 仍用 `/code-review` |
| `/fork [prompt]` | 复制当前对话为独立后台 session，不回传结果 |
| `/subtask <task>` | 启动继承对话的 forked subagent，完成后回传结果 |
| `/branch [name]` | 切换到当前对话的副本并保留原对话 |

### 仓库里的示例命令

| 命令 | 文件 | 典型用途 |
|------|------|----------|
| `/optimize` | `01-slash-commands/optimize.md` | 性能分析 |
| `/pr` | `01-slash-commands/pr.md` | PR 准备流程 |
| `/generate-api-docs` | `01-slash-commands/generate-api-docs.md` | API 文档生成 |
| `/commit` | `01-slash-commands/commit.md` | 带上下文的提交说明 |
| `/push-all` | `01-slash-commands/push-all.md` | stage + commit + push |
| `/doc-refactor` | `01-slash-commands/doc-refactor.md` | 文档重构 |
| `/setup-ci-cd` | `01-slash-commands/setup-ci-cd.md` | CI/CD 初始化 |
| `/unit-test-expand` | `01-slash-commands/unit-test-expand.md` | 测试补全 |

**适合先学的原因**：复制文件就能用，反馈快，挫败感低。

---

## Permission Modes（权限模式）

permission modes 决定 Claude Code 在使用工具时需要多大授权。

| 模式 | 说明 | 适合什么时候 |
|------|------|--------------|
| `manual` | 大多数风险操作前询问 | 日常交互；`v2.1.200+` 从 `default` 改名，旧名仍是 alias |
| `acceptEdits` | 自动接受文件编辑，其他操作仍可能询问 | 较信任的本地编辑 |
| `plan` | 只读分析，不做修改 | 方案设计、代码阅读 |
| `dontAsk` | 只运行预先批准的工具，其余自动拒绝 | 无法交互且已明确 allowlist 的脚本 |
| `bypassPermissions` | 跳过权限检查 | 可信、受控的自动化环境 |
| `auto` | 所有动作经过后台 safety classifier 检查 | 高自动化流程（需要谨慎） |

中国用户在刚上手时，优先理解 `manual`、`acceptEdits`、`plan`、`dontAsk` 这四个就足够了。旧教程里的 `default` 仍能执行，但新文档优先写 `manual`。

从 `v2.1.183+` 起，Auto Mode 还带有内置 intent-based protection，会默认拦住 `git reset --hard`、`git clean -fd`、`git commit --amend`、`terraform destroy` 这类高风险动作，除非你在当前 session 明确要求。

从 `v2.1.193+` 起，`autoMode.classifyAllShell` 可以让所有 Bash / PowerShell 命令都走 Auto Mode 分类器；拒绝原因会显示在 transcript、toast 和 `/permissions` 的 recently-denied 列表。

从 `v2.1.219+` 的当前口径看，Auto Mode 面向所有 plans，但仍要求符合条件的模型和 provider。Team / Enterprise 默认可用，管理员可在 managed settings 中把 `permissions.disableAutoMode` 设为 `"disable"` 来关闭。`CLAUDE_CODE_ENABLE_AUTO_MODE` 仅为兼容保留，不再决定是否启用。

---

## Subagents（子代理）

subagents 是专门负责某类任务的子代理。它们适合复杂任务拆分，比如“一个做代码审查，一个做测试，一个做文档”。

当前版本从 `v2.1.219` 起默认允许 subagent 嵌套 spawn，默认深度为 3；设置 `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH=1` 才会禁用嵌套。历史上，`v2.1.172` 到 `v2.1.216` 默认最多 5 层且不能配置，`v2.1.217` 到 `v2.1.218` 才短暂改为深度 1。可用 `Agent(agent_type)` 限制可 spawn 对象；这些标识不要翻译或改名。

从 `v2.1.178+` 起，嵌套 `.claude/agents/` 的同名 agent 采用最近目录优先；workflow 和 output-style 定义也遵循同样规则。

从 `v2.1.210+` 起，subagent 最终报告会扫描 instruction-shaped text；从 `v2.1.212+` 起，每个 session 默认最多 spawn 200 个 subagents，可用 `CLAUDE_CODE_MAX_SUBAGENTS_PER_SESSION` 调整，`/clear` 会重置预算。`v2.1.217+` 还可用 `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS` 控制同时运行数量，默认 20。

### 常见内建 subagents

| 名称 | 典型用途 |
|------|----------|
| `general-purpose` | 通用复杂任务 |
| `Plan` | 方案设计 |
| `Explore` | 快速搜索与理解代码 |
| `Bash` | 终端命令执行 |

### 仓库里的示例 subagents

| 名称 | 文件 | 用途 |
|------|------|------|
| `code-reviewer` | `04-subagents/code-reviewer.md` | 代码质量审查 |
| `test-engineer` | `04-subagents/test-engineer.md` | 测试策略 |
| `documentation-writer` | `04-subagents/documentation-writer.md` | 文档撰写 |
| `secure-reviewer` | `04-subagents/secure-reviewer.md` | 安全审查 |
| `implementation-agent` | `04-subagents/implementation-agent.md` | 实现任务 |
| `debugger` | `04-subagents/debugger.md` | 根因分析 |
| `data-scientist` | `04-subagents/data-scientist.md` | 数据与 SQL 分析 |
| `performance-optimizer` | `04-subagents/performance-optimizer.md` | Profiling 与性能优化 |

---

## Skills（技能）

skills 是 Claude Code 会根据描述自动触发的复用能力。它们往往比单个 slash command 更适合长期维护的工作流。

### 仓库里的示例 skills

| 名称 | 文件夹 | 典型用途 |
|------|--------|----------|
| `code-review-specialist` | `03-skills/code-review-specialist/` | 代码审查；使用 `-specialist` 后缀是为了避免遮蔽 Claude Code 内置 `/code-review` |
| `brand-voice` | `03-skills/brand-voice/` | 文案语气统一 |
| `doc-generator` | `03-skills/doc-generator/` | 文档生成 |
| `refactor` | `03-skills/refactor/` | 结构化重构 |

### Claude Code 自带 bundled skills

这些是 Claude Code 自带的 skills，不需要从本仓库复制安装：

| 名称 | 典型用途 |
|------|----------|
| `/batch` | 跨大量文件批量执行同一类修改 |
| `/claude-api` | 加载 Claude API / SDK 参考 |
| `/debug` | 读取 debug log 并排查当前 session 问题 |
| `/fewer-permission-prompts` | 扫描调用记录并建议更合理的 allowlist |
| `/loop` | 按间隔重复执行 prompt |
| `/run` | 启动当前项目，实际看改动是否跑起来 |
| `/run-skill-generator` | 为项目生成 `/run` / `/verify` 所需的运行技能 |
| `/deep-research <topic>` | 深入研究指定主题；`v2.1.218+` 起仅显式调用 |
| `/code-review [effort]` | 审查当前 diff 的正确性缺陷，可传入 `/code-review high`；`v2.1.215+` 起仅显式调用，`v2.1.218+` 起在后台 subagent 中运行 |
| `/simplify` | 做复用、简化、效率和抽象层级相关的清理型审查，并应用修复；不负责找 bug |
| `/verify` | 构建、运行并观察应用，确认修复真的有效；`v2.1.215+` 起仅显式调用 |

### skill 结构

```text
.claude/skills/skill-name/
├── SKILL.md
├── scripts/
└── templates/
```

### 高风险提醒

`SKILL.md` 里的 frontmatter 是可执行配置的一部分，不要翻译这些字段：

- `name`
- `description`
- `effort`
- `context`
- `background`
- `shell`

---

## Plugins（插件）

plugins 适合“把整套方案打包给团队用”。它们通常会组合多个能力：

- slash commands
- skills
- subagents
- MCP
- hooks

### 仓库里的示例 plugins

| 名称 | 位置 | 用途 |
|------|------|------|
| `pr-review` | `07-plugins/pr-review/` | PR 审查工作流 |
| `documentation` | `07-plugins/documentation/` | 文档生成与同步 |
| `devops-automation` | `07-plugins/devops-automation/` | 部署、监控与事故处理 |

### plugin 结构

```text
plugin-name/
├── .claude-plugin/plugin.json
├── commands/
├── agents/
├── hooks/
├── mcp/
└── scripts/
```

`.claude-plugin/plugin.json` 是 manifest，`name`、`version`、`description`、`license` 这些 key 不要翻。

从 `v2.1.157` 起，可以用 `claude plugin init <name>` 在 `.claude/skills` 中创建本地 plugin；该目录下的 plugin 会自动加载，不需要 marketplace。

从 `v2.1.172+` 起，`/plugin` marketplace 浏览界面支持搜索栏，适合团队 marketplace 规模变大后快速过滤 plugin。

从 `v2.1.179+` 起，remote session 里的 plugin loading performance 有改进。

从 `v2.1.187+` 起，`/plugin` 会提示 unused plugins；从 `v2.1.195+` 起，plugin 的 `plugin.json` `name` 和 marketplace entry name 不一致时，enable / disable 也能正确处理。

---

## MCP（外部工具协议）

MCP（Model Context Protocol）用于让 Claude Code 连接外部工具、服务和实时数据。

### 仓库里的典型 MCP 配置

| 文件 | 用途 |
|------|------|
| `05-mcp/github-mcp.json` | GitHub 集成 |
| `05-mcp/database-mcp.json` | 数据库访问 |
| `05-mcp/filesystem-mcp.json` | 文件系统访问 |
| `05-mcp/multi-mcp.json` | 多服务组合 |

### 中国用户常见卡点

- `npx` 首次安装 MCP server 时很慢
- GitHub Token 没权限或没导出
- Windows / WSL 环境下 shell 和路径行为不同
- `v2.1.193+` 起，启动时会提示仍需认证的 MCP server；`headersHelper` 遇到 HTTP 401 / 403 会自动刷新动态认证头

### 高风险提醒

以下内容不要翻：

- `mcpServers`
- server 名称，例如 `github`
- 环境变量名，例如 `GITHUB_TOKEN`
- 路径占位符和命令字段

---

## Hooks（钩子）

hooks 是事件驱动的自动化动作。适合这些场景：

- 调工具前做风险拦截
- 提交前跑测试
- 改完代码后自动格式化
- 结束前记录上下文

### 仓库里的示例 hooks

| 文件 | 用途 |
|------|------|
| `06-hooks/pre-commit.sh` | 提交前跑测试 |
| `06-hooks/format-code.sh` | 自动格式化 |
| `06-hooks/security-scan.sh` | 安全检查 |
| `06-hooks/pre-tool-check.sh` | Bash 高风险命令预检查 |
| `06-hooks/validate-prompt.sh` | prompt 校验 |
| `06-hooks/log-bash.sh` | Bash 日志记录 |
| `06-hooks/dependency-check.sh` | 依赖清单变更后的漏洞扫描 |

### hook 类型

- `command`
- `http`
- `mcp_tool`
- `prompt`
- `agent`

这些类型名同样不要翻成中文字段。

`v2.1.191+` 起，`matcher` 支持 `"Write,Edit"` 这类逗号列表；`v2.1.195+` 起，工具名匹配更精确，带连字符的 MCP tool name 不会再误触发其他工具。

---

## Memory（记忆）

memory 是 Claude Code 用来长期加载规则和上下文的机制。

### 本仓库里的 memory 示例

| 文件 | 用途 |
|------|------|
| `02-memory/project-CLAUDE.md` | 项目规则 |
| `02-memory/personal-CLAUDE.md` | 个人偏好 |
| `02-memory/directory-api-CLAUDE.md` | 目录级规则示例 |

### 新手最重要的理解

- `CLAUDE.md` 不是随便写笔记的地方，它更像项目规范和上下文入口。
- `CLAUDE.md` 指令与 auto memory 是两套互补机制；前者由人维护，后者由 Claude 维护。
- Managed、User、Project、Local 四类 CLAUDE.md 会按范围拼接进上下文，不是严格的覆盖链。
- `@path/to/file` import 最多递归 4 hops，相对路径以包含 import 的文件为基准。
- memory 很强，但它不替代 skills、hooks 和 slash commands。
- 旧教程里常见的 `# ...` 快捷写 memory 已经停用；现在请用 `/memory` 或自然语言更新。

---

## 新功能提示

这个仓库同步的是 Claude Code 较新的能力集，因此你会在文档里频繁看到这些内容：

- Auto Mode
- Monitor Tool
- `/tui`
- `/focus`
- `/recap`
- `/undo`
- `/proactive`
- `/ultrareview`
- `/fewer-permission-prompts`
- `/usage-credits`
- `/team-onboarding`
- `/ultraplan`
- `/goal`
- `/scroll-speed`
- `/run`
- `/verify`
- `/run-skill-generator`
- `/reload-skills`
- `/workflows`
- `/cd <path>`
- `/plugin list --enabled`
- `/plugin list --disabled`
- unused plugins 提示
- `--safe-mode`
- `CLAUDE_CODE_SAFE_MODE=1`
- `fallbackModel`
- `disableBundledSkills`
- `CLAUDE_CODE_DISABLE_BUNDLED_SKILLS=1`
- `hookSpecificOutput.additionalContext`
- hook `matcher` 逗号列表和精确匹配
- `CLAUDE_CODE_SESSION_ID`
- `claude-fable-5`
- `Agent(agent_type)` 限制 subagent 可 spawn 类型；`CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH` 默认值为 3，设为 `1` 可禁用嵌套
- `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS` 控制并发 subagents，默认 20
- hook handler 级 `if` 条件
- `/plugin` marketplace 搜索栏
- `enforceAvailableModels`
- `wheelScrollAccelerationEnabled`
- `footerLinksRegexes`
- `language`
- `/doctor` flat tree 布局
- `/bug` 必须填写描述
- `Tool(param:value)` permission rule 参数匹配
- 嵌套 `.claude/agents/` 最近目录优先
- remote session plugin loading performance 改进
- `/review <pr>` 审查 GitHub PR；本地 diff 审查仍用 `/code-review [effort]`
- `claude mcp login <name>` / `claude mcp logout <name>`，`--no-browser` 适合 SSH / headless session
- `--teammate-mode iterm2`，依赖 `it2` CLI
- `respondToBashCommands`
- `sandbox.credentials`
- `sandbox.allowAppleEvents`
- `/config key=value`
- `CLAUDE_CLIENT_PRESENCE_FILE`
- `CLAUDE_CODE_MAX_RETRIES`
- `CLAUDE_CODE_RETRY_WATCHDOG`
- `CLAUDE_CODE_MCP_TOOL_IDLE_TIMEOUT`
- `CLAUDE_CODE_DISABLE_MOUSE_CLICKS`
- `autoMode.classifyAllShell`
- `claude_code.assistant_response`
- `!` bash mode live file-path autocomplete
- `claude plugin init <name>`
- `CLAUDE_CODE_ENABLE_AUTO_MODE`（从 `v2.1.207` 起仅保留兼容性，不再产生效果）
- `permissions.disableAutoMode`（managed settings 中设为 `"disable"` 可关闭 Auto Mode）
- `claude auto-mode reset [--yes]`
- `/fork [prompt]`、`/subtask <task>` 与 `/branch [name]` 的不同行为
- `outputStyle` / `/config` Output style 与 `/statusline`
- `fileCheckpointingEnabled`、`CLAUDE_CODE_DISABLE_FILE_CHECKPOINTING` 与最近 100 个 checkpoints 上限
- `claude mcp add --scope` / `-s`、`claude mcp add-json` 与 `streamable-http`
- `CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION`
- `CLAUDE_CODE_MAX_SUBAGENTS_PER_SESSION`
- `CLAUDE_CODE_MCP_AUTO_BACKGROUND_MS`
- `--permission-mode auto`（替代已移除的 `--enable-auto-mode`）
- `sandbox.filesystem.disabled`
- `emojiCompletionEnabled`
- `CLAUDE_CODE_OTEL_CONTENT_MAX_LENGTH`
- `FORCE_HYPERLINK=0`
- `--ax-screen-reader`、`CLAUDE_AX_SCREEN_READER`、`axScreenReader`
- `EnterWorktree`
- dynamic workflows 触发关键词是 `ultracode`，裸词 `workflow` 不再触发
- `claude agents --json`
- `/model` 默认保存为后续 session 默认值；按 `s` 才只作用于当前 session
- Claude Opus 5（`claude-opus-5`、1M context）是默认 Opus 模型，默认 effort 为 `high`
- `/fast` 只适用于 Opus 5 和 Opus 4.8
- Sonnet 5（`claude-sonnet-5`）与 1M context window
- `manual` permission mode（原 `default`，旧名仍可用）
- `/dataviz` bundled skill
- `/deep-research` 仅显式调用；`/code-review` 在后台 subagent 中运行
- `context: fork` skills 默认 `background: true`；frontmatter boolean 也接受 `yes` / `no`、`on` / `off`、`1` / `0`
- `${CLAUDE_PROJECT_DIR}` 与一次调用叠加多个 skills
- subagents 默认后台运行、Explore 模型继承和 `--append-subagent-system-prompt`
- MCP `roots/list`、`Pending approval` trust gate
- `Summarize up to here`
- `askUserQuestionTimeout`、`enableArtifact`
- `CLAUDE_ENABLE_STREAM_WATCHDOG`
- `DirectoryAdded` hook 与 31 个 hook 事件
- `workflowSizeGuideline`（默认 medium，目标少于 15 个 agents）
- `sandbox.network.strictAllowlist`
- `mcp_server_errors` 与 `--forward-subagent-text`
- `claude agents` 里用 `Ctrl+T` 固定后台 session
- `/usage` 按 skills、subagents、plugins、MCP server 等类别拆分成本
- VSCode Account & usage 视图显示 cache miss、long-context cost、subagents 以及 per-skill / per-agent / per-plugin / per-MCP 归因
- GFM 任务清单复选框（`- [ ]` / `- [x]`）渲染
- `allowAllClaudeAiMcps`
- Voice Dictation
- Channels
- background tasks
- scheduled tasks
- worktrees
- web sessions
- remote control

如果你是初学者，不需要先掌握这些。按 [LEARNING-ROADMAP.md](LEARNING-ROADMAP.md) 的顺序往下学即可。

---

## 推荐阅读顺序

1. [README.md](README.md)
2. [LEARNING-ROADMAP.md](LEARNING-ROADMAP.md)
3. [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
4. [01-slash-commands/](01-slash-commands/)
5. [02-memory/](02-memory/)
6. [10-cli/](10-cli/)
