<picture>
  <source media="(prefers-color-scheme: dark)" srcset="resources/logos/claude-howto-logo-dark.svg">
  <img alt="Claude How To" src="resources/logos/claude-howto-logo.svg">
</picture>

# Claude Code 速查卡（Quick Reference）

这份速查卡适合两种场景：

- 你已经知道大概原理，现在只想快速复制命令
- 你正在本土化或二次改写仓库，想快速确认哪些路径和标识不能动

---

## 🚀 安装命令速查

### Slash Commands（快捷命令）

```bash
# 安装全部示例 slash commands
cp 01-slash-commands/*.md .claude/commands/

# 安装单个命令
cp 01-slash-commands/optimize.md .claude/commands/
```

### Memory（记忆）

```bash
# 项目级 memory
cp 02-memory/project-CLAUDE.md ./CLAUDE.md

# 个人级 memory
cp 02-memory/personal-CLAUDE.md ~/.claude/CLAUDE.md
```

### Skills（技能）

```bash
# 个人 skills
cp -r 03-skills/code-review-specialist ~/.claude/skills/

# 项目 skills
cp -r 03-skills/code-review-specialist .claude/skills/
```

### Subagents（子代理）

```bash
# 安装全部 subagents
cp 04-subagents/*.md .claude/agents/

# 安装单个 subagent
cp 04-subagents/code-reviewer.md .claude/agents/
```

### MCP（外部工具协议）

```bash
# 先准备凭证
export GITHUB_TOKEN="your_token"
export DATABASE_URL="postgresql://..."

# 项目级 MCP 配置
cp 05-mcp/github-mcp.json .mcp.json
claude mcp add --scope project --transport http github https://api.github.com/mcp
claude mcp add-json events-server '{"type":"stdio","command":"npx","args":["@modelcontextprotocol/server-events"]}'

# CLI 登录 / 登出 MCP server
claude mcp login github
claude mcp login github --no-browser
claude mcp logout github
# v2.1.193+ 启动时会提示仍需认证的 MCP server；headersHelper 遇到 HTTP 401 / 403 会自动刷新

# 或者写进用户级配置 ~/.claude.json
```

### Hooks（钩子）

```bash
mkdir -p ~/.claude/hooks
cp 06-hooks/*.sh ~/.claude/hooks/
chmod +x ~/.claude/hooks/*.sh
```

### Plugins（插件）

```bash
/plugin install pr-review
/plugin install devops-automation
/plugin install documentation
/plugin list --enabled
/plugin list --disabled
claude plugin init my-plugin
```

### Checkpoints（检查点）

```bash
# checkpoints 默认自动创建
# fileCheckpointingEnabled 默认 true；只保留最近 100 个 checkpoints 的文件快照
# CLAUDE_CODE_DISABLE_FILE_CHECKPOINTING 可关闭文件快照
# v2.1.191+ 起 /rewind 可以跨过 /clear 回到更早 checkpoint
/rewind
```

### Advanced Features（高级功能）

```bash
# 进入规划模式
/plan Task description

# 把复杂规划交给云端会话起草
/ultraplan Task description

# 为新同事生成项目 onboarding guide
/team-onboarding

# 额外用量配置
/usage-credits       # `/extra-usage` 仍可作为兼容 alias（别名）
/usage               # v2.1.149+ 成本视图会按类别拆分
/deep-research topic # 深入研究主题；v2.1.218+ 起仅显式调用
/code-review high    # 正确性缺陷审查；v2.1.218+ 起在后台 subagent 中运行
/review <pr>         # 审查 GitHub PR；本地 diff 仍用 /code-review
/simplify            # 清理型审查并应用修复，不负责找 bug
/doctor              # 诊断安装、配置和 plugin 健康
/bug "描述问题"      # v2.1.178+ 必须填写描述
/reload-skills       # 重新扫描 skill 目录
/workflows           # 查看 dynamic workflows
/cd ../backend       # 切换工作目录并尽量保留 prompt cache
/plugin              # marketplace 浏览界面可用搜索栏过滤 plugin
ultracode            # 触发 dynamic workflows 的关键词，裸词 workflow 不再触发
/config thinking=false  # 直接设置单个配置项
/config                 # Output style 在这里切换；/output-style 已移除
/statusline             # 配置底部状态栏 command
!npm test            # v2.1.186+ 起输出会自动发给 Claude 并触发回复
!cat src/index.ts    # v2.1.193+ 起 ! bash mode 支持路径自动补全
claude auto-mode reset        # 恢复 Auto Mode 默认配置并请求确认
claude auto-mode reset --yes  # 跳过确认
# CLAUDE_CODE_ENABLE_AUTO_MODE 从 v2.1.207 起仅保留兼容性，不再产生效果
export CLAUDE_CODE_DISABLE_MOUSE_CLICKS=1  # 禁用 fullscreen mode 的 click / drag / hover
CLAUDE_CODE_SAFE_MODE=1 claude          # 禁用自定义项后排查配置问题
export CLAUDE_CODE_MCP_TOOL_IDLE_TIMEOUT=600
export CLAUDE_CODE_MCP_AUTO_BACKGROUND_MS=120000
export CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION=200
export CLAUDE_CODE_MAX_SUBAGENTS_PER_SESSION=200
export CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS=20
export CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH=1  # v2.1.219+ 设为 1 可禁用嵌套；默认深度 3
export CLAUDE_CODE_OTEL_CONTENT_MAX_LENGTH=61440
export FORCE_HYPERLINK=0
export CLAUDE_AX_SCREEN_READER=1
export CLAUDE_CODE_RETRY_WATCHDOG=1

# 常见 permission mode
claude --permission-mode manual
claude --permission-mode acceptEdits
claude --permission-mode plan
claude --permission-mode dontAsk  # 未预先批准的工具自动拒绝
claude --permission-mode bypassPermissions
claude --permission-mode auto  # 所有动作经过后台 safety classifier；替代已移除的 --enable-auto-mode
claude --safe-mode
claude --fallback-model sonnet
claude --ax-screen-reader

# session 常用命令
/resume                 # 无参数时打开历史 session picker
/rename "session-name"
/fork 尝试 OAuth 方案   # 复制成独立后台 session，不回传结果
/subtask 检查 flaky tests  # forked subagent 完成后回传结果
/branch try-oauth       # 切换到对话副本，原对话保留
claude -c
claude -r "session-name"
claude agents --json   # 机器可读的 Agent View 列表
claude -p --output-format stream-json --forward-subagent-text "query"  # 包含深度 2+ 的 subagent 输出
git worktree prune     # 清理已解锁且不再使用的 worktree

# settings.json 常见新增 key（key 名不要翻译）
# outputStyle / statusLine / switchModelsOnFlag
# wheelScrollAccelerationEnabled
# footerLinksRegexes
# language
# enforceAvailableModels
# sandbox.filesystem.disabled
# sandbox.network.strictAllowlist
# emojiCompletionEnabled
# workflowSizeGuideline

# permission rule 参数匹配示意（语法不要翻译）
# Tool(param:value)

# hook matcher 组合示意（matcher key 和工具名不要翻译）
# "matcher": "Write,Edit"

# Auto Mode 严格 shell 分类示意（settings key 不要翻译）
# "autoMode": { "classifyAllShell": true }
# Team / Enterprise 管理员关闭 Auto Mode："permissions": { "disableAutoMode": "disable" }
```

---

## 📋 功能速查表

| 能力 | 安装 / 所在位置 | 典型用法 | 备注 |
|------|------------------|----------|------|
| Slash Commands | `.claude/commands/*.md` | `/command-name` | 用户主动触发 |
| Memory | `./CLAUDE.md` / `~/.claude/CLAUDE.md` | 自动加载 | 长期规则和偏好 |
| Skills | `.claude/skills/*/SKILL.md` | 自动触发 | 可复用工作流 |
| Subagents | `.claude/agents/*.md` | 自动委派 / 显式调用 | 分工执行 |
| MCP | `.mcp.json` / `~/.claude.json` | `/mcp`、工具调用 | 实时外部能力 |
| Hooks | `~/.claude/hooks/*.sh` 等 | 事件触发 | 自动检查和自动化 |
| Plugins | `/plugin install` | 一次安装多能力 | 团队分发 |
| Checkpoints | 内建 | `Esc+Esc`、`/rewind` | 安全试错 |
| Planning Mode | 内建 | `/plan <task>` | 复杂任务规划 |
| Ultraplan | 内建 | `/ultraplan <task>` | 云端起草复杂计划 |
| Monitor Tool | 内建 | 监控后台命令 stdout 事件流 | 适合替代轮询 |
| Auto Mode Reset | 内建 | `claude auto-mode reset [--yes]` | 恢复默认自动权限规则 |
| Screen Reader Mode | 内建 | `--ax-screen-reader` | 纯文本渲染，便于辅助技术读取 |
| Print Mode | 内建 | `claude -p` | 脚本 / CI/CD |
| Run / Verify Skills | bundled skills | `/run`、`/verify`、`/run-skill-generator` | 启动项目并确认改动真实可用；`/verify` 从 `v2.1.215+` 起仅显式调用 |

---

## 🧠 哪些标识不能翻

这部分最容易踩坑，单独列出来：

- `/optimize`、`/pr`、`/review-pr`
- `skills`、`hooks`、`MCP`、`CLI`
- `allowed-tools`、`tools`、`model`、`env`
- `GITHUB_TOKEN`、`DATABASE_URL`
- `.mcp.json`
- `claude -p`

想继续中文化仓库时，先看：

- [LOCALIZATION-STYLE.md](LOCALIZATION-STYLE.md)
- [UPSTREAM.md](UPSTREAM.md)

---

## 🎯 常见场景速查

### 代码审查

```bash
# 方法 1：slash command
cp 01-slash-commands/optimize.md .claude/commands/
# 使用：/optimize

# 方法 2：subagent
cp 04-subagents/code-reviewer.md .claude/agents/

# 方法 3：skill
cp -r 03-skills/code-review-specialist ~/.claude/skills/

# 方法 4：plugin
/plugin install pr-review
```

### 文档生成

```bash
cp 01-slash-commands/generate-api-docs.md .claude/commands/
cp 04-subagents/documentation-writer.md .claude/agents/
cp -r 03-skills/doc-generator ~/.claude/skills/
/plugin install documentation
```

### DevOps（运维自动化）

```bash
/plugin install devops-automation
# 常见命令：/deploy /rollback /status /incident
```

### 团队规范

```bash
cp 02-memory/project-CLAUDE.md ./CLAUDE.md
```

### 自动化与 Hooks

```bash
mkdir -p ~/.claude/hooks
cp 06-hooks/*.sh ~/.claude/hooks/
chmod +x ~/.claude/hooks/*.sh

# 常见例子
# - pre-commit.sh
# - format-code.sh
# - security-scan.sh
```

### 安全试错

```bash
# 修改前后都记得 checkpoint 可回退
/rewind
```

### CI/CD

```bash
claude -p "Run all tests and generate report"
claude -p "Run tests" --permission-mode dontAsk
```

---

## 🇨🇳 中国用户特别注意

### GitHub 访问和 Token

- 很多 MCP 示例、plugin 示例默认依赖 GitHub。
- 开始之前先确认你能访问 GitHub，并且 `GITHUB_TOKEN` 具备需要的 scope。

### `npm` / `npx` / `uv` 使用提醒

- 很多示例会用到 `npx` 安装 MCP server。
- Python 相关脚本和测试通常依赖 `uv`。
- 如果第一次安装很慢，优先检查网络、代理、包管理镜像和证书环境。

### Windows / WSL 使用提醒

- 如果你在 Windows 上，优先明确自己是在 PowerShell、Git Bash，还是 WSL 里操作。
- 部分 shell 脚本和路径写法默认更偏 Unix / macOS / Linux 风格。

### 翻译不要碰的地方

- frontmatter 字段名
- JSON key
- shell 命令
- 环境变量
- slash command / skill / plugin / subagent 的名称
- hook 输入字段和输出 key，例如 `effort.level`、`CLAUDE_EFFORT`、`hookSpecificOutput.updatedToolOutput`

---

## 🔗 常用入口

- [README.md](README.md)
- [LEARNING-ROADMAP.md](LEARNING-ROADMAP.md)
- [CATALOG.md](CATALOG.md)
- [01-slash-commands/](01-slash-commands/)
- [02-memory/](02-memory/)
- [03-skills/](03-skills/)
- [04-subagents/](04-subagents/)
- [05-mcp/](05-mcp/)
- [06-hooks/](06-hooks/)
- [07-plugins/](07-plugins/)
- [09-advanced-features/](09-advanced-features/)
- [10-cli/](10-cli/)
