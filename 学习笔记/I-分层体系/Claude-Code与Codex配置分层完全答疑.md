# Claude Code / Codex 配置分层体系完全答疑

- **日期**：2026-09-09
- **分支**：study-notes
- **学习起因**：学 command / skill / hook / MCP / subagent / plugin 时反复问"放哪"，本质是同一个问题的不同切面——配置分层体系；同时调研 Codex CLI 的配置分层与 MCP 支持
- **配套阅读**：[英文术语对照表](../Claude-HowTo英文术语对照表.md)（词根课）、[H-hooks 答疑](../H-hooks/Hooks答疑-从事件匹配器到stdin-JSON逐行拆format-code脚本.md)、[G-mcp 答疑](../G-mcp/MCP完全答疑-从授权安全到数据库文件系统与PDF流水线Agent.md)

---

## 先建心智模型：四层抽屉柜

Claude Code 和 Codex 都是"配置可以分好几层放"的工具。想象一个**四层抽屉柜**，每层属于不同的人/不同的作用域，从上到下优先级递减：

```
第1层（最高，覆盖下面所有层）
  managed policy / managed-settings.json
  ——公司 / 团队管理员强制执行，你改不了

第2层
  .claude/settings.local.json（Claude Code）
  ——你个人对这个项目的临时偏好，通常不提交 git

第3层
  .claude/settings.json（Claude Code）
  或 .codex/config.toml（Codex）
  ——这个项目所有人共用，需要提交 git

第4层（最低，被上面所有层覆盖）
  ~/.claude/settings.json（Claude Code 用户级）
  或 ~/.codex/config.toml（Codex 用户级）
  ——你这个用户所有项目都生效
```

**记法**："上压下"——第1层 managed 最大，第2层 .local 高于项目级，项目级高于用户级。

---

## Part 1：Claude Code 配置分层

### 1.1 settings.json 的四层（优先级从高到低）

| 优先级 | 文件 | 路径 | 通常谁放 | 是否提交 git |
|---|---|---|---|---|
| 1（最高） | managed-settings.json / managed-settings.d/ | 系统级（如 `/etc/claude/managed-settings.json`，企业 IT 管控） | 公司 / 团队管理员 | ❌ 强制管控 |
| 2 | .claude/settings.local.json | 项目根目录下 | 你个人的项目覆盖 | ❌ 不提交 |
| 3 | .claude/settings.json | 项目根目录下 | 团队共用 | ✅ 提交 |
| 4（最低） | ~/.claude/settings.json | 你用户目录 | 你所有项目 | ✅ 提交 |

> ⚠️ 容易搞反的点：`.local.json` 不是"放本地文件"的意思，而是"这个项目的本地覆盖"，**优先级反而比项目级 `.settings.json` 更高**。它放在项目里但不提交（因为是 .local 后缀）。

**文件示例**（项目级 settings.json 的一部分）：

```json
{
  "hooks": { "PostToolUse": [...] },
  "mcpServers": { "github": { "command": "...", "args": [...] } }
}
```

### 1.2 managed settings 补充规则

- `managed-settings.d/` 目录下的 `.json` 文件会在基础 `managed-settings.json` **之后按文件名字母顺序合并**
- 合并规则：标量覆盖、数组拼接并去重、**对象深度合并**
- permission rules（allow / ask / deny）跨 scope **合并**，不是简单替换
- `allow` / `deny` 规则里的路径仍按**任意深度**理解（不受 hook `if` 的 v2.1.214 收窄影响）

### 1.3 各能力放哪：一张总表

| 东西 | 用户级（~） | 项目级（.claude/） | 本地覆盖（.local.json） | 说明 |
|---|---|---|---|---|
| settings 配置 | `~/.claude/settings.json` | `.claude/settings.json` | `.claude/settings.local.json` | 三层叠加优先级 |
| hooks 脚本 | `~/.claude/hooks/` | `.claude/hooks/` | — | 脚本本体放这里，配置写在 settings.json 的 hooks 段 |
| skills | `~/.claude/skills/<名>/SKILL.md` | `.claude/skills/<名>/SKILL.md` | — | 拷到哪层归哪层用 |
| commands | `~/.claude/commands/` | `.claude/commands/` | — | 命令文件放这里 |
| agents / subagents | `~/.claude/agents/` | `.claude/agents/` | — | 可嵌套，**近的覆盖远的**（monorepo 场景） |
| MCP servers | `~/.claude/settings.json` 的 mcpServers 段 | `.mcp.json`（需 git trust） | `~/.claude.json` 的 mcpServers 段 | `--scope local` 写 ~/.claude.json，`--scope project` 写 `.mcp.json` |
| CLAUDE.md | — | `./CLAUDE.md`（项目根，提交） | `./CLAUDE.local.md`（不提交） | 向上查找，深层子目录的 CLAUDE.md 按需加载 |
| plugin | — | `.claude-plugin/`（安装目录） | — | plugin 本体一般放项目里或用户 home 下 |
| statusline scripts | `~/.claude/settings.json` 的 statusline 段 | `.claude/settings.json` | — | |

### 1.4 CLAUDE.md / 记忆文件分层（02-memory 体系）

| 文件 | 位置 | 提交？ | 作用 |
|---|---|---|---|
| `CLAUDE.md` | 项目根目录 | ✅ | 项目守则，提交后团队共享 |
| `CLAUDE.local.md` | 同目录，在 `CLAUDE.md` 之后拼接 | ❌ | 你个人的项目偏好，不提交 |
| `MEMORY.md` | 用户根 `~/.claude/MEMORY.md` | ❌ | 自动记忆索引，L0 |
| `memory/` | 用户根 `~/.claude/memory/` | ❌ | L1～L3 记忆文件 |

**拼接规则**：所有文件**拼接**进上下文，不覆盖；同目录 `CLAUDE.local.md` 接在 `CLAUDE.md` 之后。更深层子目录的 CLAUDE.md 在 Claude 读取该子目录时**按需加载**（渐进披露）。

### 1.5 agents 的嵌套规则（monorepo 特别说明）

```
monorepo/
├── packages/
│   ├── a/
│   │   └── .claude/agents/reviewer.md   ← 最近的，优先级最高
│   └── b/
│       └── .claude/agents/reviewer.md
└── .claude/agents/reviewer.md             ← 较远的，被覆盖
```

从 `v2.1.178+`，同名的 agent 文件**离当前工作目录近的会覆盖远的**。

### 1.6 MCP 的 scope 三层（05-mcp 体系）

| scope | 路径 | 提交？ | 说明 |
|---|---|---|---|
| `local`（默认） | `~/.claude.json` 里的 mcpServers | ❌ | 只在当前项目用，不进 git |
| `project` | 仓库根 `.mcp.json` | ✅ | 团队共享，首次使用需 `codex trust` / `git trust` |
| `user` | `~/.claude/settings.json` 的 mcpServers | ✅ | 所有项目生效 |

> 注意：`.mcp.json` 里定义的 project MCP **仍需要用户信任**才能启动。未信任 workspace 即使在 settings.json 里批准了 project MCP，`claude mcp list` 也会显示 `⏸ Pending approval`。

---

## Part 2：Codex CLI 配置分层

### 2.1 配置文件体系（与 Claude Code 对照着看）

| 文件 | 位置 | 作用 | 是否提交 |
|---|---|---|---|
| `~/.codex/config.toml` | 用户 home | 用户级全局配置，所有项目生效 | ✅（是配置文件本身） |
| `~/.codex/auth.json` | 用户 home | 存 API key 或 ChatGPT token | ❌ **绝对不要提交** |
| `.codex/config.toml` | 仓库根（需 `codex trust`） | 项目级配置，团队共享 | ✅ |
| `/etc/codex/config.toml` | 系统级（Unix） | 系统级配置（一般用户碰不到） | ❌ |

**配置优先级**（从上到下递减）：

```
CLI flags（--model、-c key=value）
        ↓
Profile（--profile <name> 或 ~/.codex/<name>.config.toml）
        ↓
Project config（.codex/config.toml 从项目根走到 CWD）
        ↓
User config（~/.codex/config.toml）
        ↓
System config（/etc/codex/config.toml）
        ↓
内置默认值
```

> 注意：项目级 `.codex/config.toml` **不能覆盖**安全敏感的 key：`openai_base_url`、`model_provider`、`model_providers`、`notify`、`profile`、`profiles`。

**CODEX_HOME 环境变量**：可重定向整个 `~/.codex` 目录到别处（类似 Claude Code 的 `$CLAUDE_PROJECT_DIR` 但反过来）。

### 2.2 AGENTS.md 机制（对应 Claude Code 的 CLAUDE.md）

| 文件 | 位置 | 说明 |
|---|---|---|
| `~/.codex/AGENTS.md` | 用户 home | 全局 fallback，所有项目的兜底说明 |
| `AGENTS.md` | 仓库根 | 项目守则，提交 git |
| `AGENTS.override.md` | 同目录，在同名 AGENTS.md 基础上局部替代 | **本机临时覆盖，不提交**（类似 Claude Code 的 CLAUDE.local.md，但文件名不同） |
| 子目录 `AGENTS.md` | 各层子目录 | 从仓库根向 CWD 方向**全部合并**，冲突时靠近 CWD 的胜出 |

**合并策略**：root → leaf 全路径拼接，不是"只取最近的"。可以用 `project_doc_fallback_filenames` 在每层声明备用文件名（如 `["TEAM_GUIDE.md", ".agents.md"]`）。总大小上限默认 32 KiB（`project_doc_max_bytes`）。

> ⚠️ **和 Claude Code 的关键区别**：Claude Code 用 `CLAUDE.local.md` 做本地覆盖，Codex 用 `AGENTS.override.md`（文件名不同，但定位相同）。另外 Codex 没有 L0-L3 分层记忆体系，只有单层 AGENTS.md。

### 2.3 自定义 prompts / slash commands（对应 Claude Code 的 commands）

| 文件 | 路径 | 说明 |
|---|---|---|
| 自定义 prompt | `~/.codex/prompts/*.md`（每个 .md 一个） | 放在 `~/.codex/prompts/` 目录里 |
| 调用方式 | `/prompts`（内置命令打开选择器）或 `/<prompt 名>` | — |
| 旧兼容路径 | `$CODEX_HOME/prompts/` | 仍可用 |

每个 prompt 文件是 Markdown（是否支持 YAML frontmatter 的 `name`/`description`/`argument-hint` 字段——**官方文档未明确确认**，第三方文档有提及，建议先当不支持处理）。

### 2.4 MCP servers 配置

| 配置位置 | 说明 |
|---|---|
| `~/.codex/config.toml` 的 `[mcp_servers.<name>]` 段 | 用户级，所有项目生效 |
| `.codex/config.toml` 的 `[mcp_servers.<name>]` 段 | 项目级，需 `codex trust`，提交 git |

Codex 用 **`[mcp_servers.<name>]`**（snake_case），不是 Claude Code 的 `[mcpServers]`。

**支持的 transport：**

| transport | 触发条件 | 配置字段 |
|---|---|---|
| stdio（本地进程） | 有 `command` 字段 | `command`、`args`、`env`、`cwd`、`startup_timeout_sec`、`tool_timeout_sec`、`enabled`、`enabled_tools`、`disabled_tools` |
| Streamable HTTP | 有 `url` 字段 | `url`、`bearer_token_env_var`、`http_headers` |
| SSE（Server-Sent Events） | 无原生支持 | 需用 `npx mcp-remote@latest` 包一层 stdio 桥 |

**管理子命令（对应 Claude Code 的 `claude mcp`）：**

```bash
codex mcp add <name>          # 添加 stdio 或 HTTP MCP
codex mcp list [--json]        # 列出已配置
codex mcp get <name> [--json]  # 查看详情
codex mcp remove <name>        # 移除
codex mcp login <name>         # OAuth 登录
codex mcp logout <name>         # 登出
```

> ⚠️ **注意**：`claude mcp add` 是 Claude Code 的命令，Codex 用的是 **`codex mcp add`**。两者是不同的 CLI，二进制名不同。

### 2.5 Approval / Sandbox 模式

**sandbox_mode（文件系统隔离）：**

| 值 | 含义 |
|---|---|
| `read-only`（默认） | 只读，不允许写入 |
| `workspace-write` | 允许写入当前工作区 |
| `danger-full-access` | 关闭沙箱，等同完全放权 |

**approval_policy（操作审批）：**

| 值 | 含义 |
|---|---|
| `untrusted` | 最保守，每次都问 |
| `on-request`（默认） | 必要时问 |
| `never` | 从不主动问 |

也支持细粒度 table 形式：`approval_policy = { granular = { sandbox_approval, rules, mcp_elicitations, request_permissions, skill_approval } }`。`on-failure` 已弃用，改用 `on-request`。

CLI flags：`--sandbox policy`（值同上）、`--approval-policy` 或 `-a`。

### 2.6 "connect7" 的结论

调研结论：**"connect7" 是 Context7 MCP（`@upstash/context7-mcp`）的拼写变形**，不是 Codex 自有的功能。搜索 "codex connect7" 的可信结果全部指向 Upstash 的 Context7 库文档查询 MCP server。

**Codex Connect 协议**：在 OpenAI 官方域名（openai.com、developers.openai.com、platform.openai.com）上**未找到名为 "Codex Connect" 的 CLI 子命令或协议层**。Codex CLI 原生支持 Streamable HTTP 远程 MCP server（概念上等价于"HTTP 暴露远端 MCP"），但没有名为 Connect 的独立协议层。

### 2.7 哪些文件应该提交 / 不提交

**应该提交：**
- 仓库根 `AGENTS.md`、`AGENTS.override.md`（如团队共用）
- `.codex/config.toml`（项目级，需 trust）
- 自定义 prompts（`~/.codex/prompts/` 或共享到项目里）

**绝对不要提交：**

```gitignore
# ~/.codex/ 下推荐忽略：
auth.json           # API token/凭证
sessions/           # 会话存档
history.jsonl       # 跨会话 prompt 历史
logs/               # 日志

# 项目 ./.codex/ 下推荐忽略：
.codex/auth.json
.codex/*.key
.env
```

---

## Part 3：Claude Code ↔ Codex 概念对照表

| Claude Code | Codex CLI | 对应关系 |
|---|---|---|
| `CLAUDE.md` | `AGENTS.md` | 项目守则；Codex 从仓库根向 CWD 全部合并，Claude Code 拼接但不覆盖 |
| `CLAUDE.local.md` | `AGENTS.override.md` | 个人本地临时覆盖，不提交；**文件名不同** |
| `settings.json` 三层（user/project/local） | `config.toml` 多层（user/project/system + profile + CLI flags） | 思路相同：分层叠加、上压下 |
| managed-settings.json | `/etc/codex/config.toml`（系统级） | 企业管控层 |
| hooks（PreToolUse / PostToolUse 等 31 个事件） | **无等价物** | Codex 通过 approval_policy + sandbox_mode 在工具调用前拦截，没有事件驱动的用户脚本 hook |
| skills | **无确认等价物** | 第三方博客提到 Codex Skills，但官方文档未确认 |
| subagents | **无确认等价物**（CLI 层） | IDE/云端语境有多 agent 概念，CLI 未发现原生 subagent 子命令 |
| plugins / marketplace | **无等价物** | Codex 没有 plugin marketplace |
| MCP servers（`[mcpServers]`） | `[mcp_servers.<name>]`（snake_case） | 都支持 stdio + HTTP（SSE 需桥接）；管理命令不同（`claude mcp` vs `codex mcp`） |
| slash commands | `~/.codex/prompts/*.md` + `/prompts` | Codex 是"文件即命令"，不通过 frontmatter 注册 |
| memory（L0-L3 分层） | **无等价物** | Codex 只有单层 AGENTS.md，没有 L0-L3 记忆流水线 |
| permission modes（manual/acceptEdits/plan/dontAsk/bypassPermissions/auto） | `approval_policy`（untrusted/on-request/never）+ `sandbox_mode`（read-only/workspace-write/danger-full-access） | 思路不同：Claude Code 是档位名，Codex 是两个正交维度 |
| `~/.claude/` | `~/.codex/` | 用户配置 home 目录 |
| `.mcp.json` | `.codex/config.toml` | 项目级配置；Codex 用 toml 不走独立 json |

---

## Part 4：记忆口诀

### 口诀 1：优先级"上压下"

```
managed > .local > project > user
```
（managed 最高，.local 高于项目级）

### 口诀 2：各能力放哪

```
脚本放 .claude/hooks/
技能放 .claude/skills/
命令放 .claude/commands/
代理放 .claude/agents/
MCP 配置看 scope：
  local  → ~/.claude.json
  project → .mcp.json
CLAUDE.md 系：
  守则在 ./CLAUDE.md
  本地在 ./CLAUDE.local.md
```

### 口诀 3：Codex vs Claude Code 的关键区别

```
Codex 用 .codex/config.toml（不是 settings.json）
Codex 用 AGENTS.md（不是 CLAUDE.md）
Codex 用 AGENTS.override.md（不是 CLAUDE.local.md）
Codex MCP 用 [mcp_servers.<name>]（不是 [mcpServers]）
Codex 管 MCP 用 codex mcp（不是 claude mcp）
Codex 没有 hooks / skills / subagents / memory L0-L3
```

---

## Part 5：Windows Git Bash 实操注意事项

1. **路径写法**：Git Bash 用 Unix 风格路径，`$HOME` = `C:\Users\11488`。创建用户级目录时：
   ```bash
   mkdir -p ~/.claude/hooks
   chmod +x ~/.claude/hooks/*.sh
   ```

2. **CODEX_HOME / CLAUDE_PROJECT_DIR**：Windows Git Bash 里这两个环境变量通用，但写进配置文件时注意引号。

3. **MCP server Windows 路径**：`C:\path\to\server.exe` 在 config.toml 里要写成 `/c/path/to/server.exe` 或用 `cygpath` 转换。

4. **`codex trust` vs `git trust`**：Codex CLI 用 `codex trust` 命令信任项目，Claude Code 用 `git trust`。两者独立，各管各的。

---

## 待二次核对事项

- AGENTS.md / AGENTS.override.md 加载链的 OpenAI 官方原文（GitHub 主仓 docs/agents.md 因网络限制未直接命中）
- Codex 是否真的把 "skills" 作为一等公民（官方文档未明确）
- Codex 云端 agent（ChatGPT 网页端）是否能挂载 GitHub 仓库并读取 AGENTS.md（未确认）
