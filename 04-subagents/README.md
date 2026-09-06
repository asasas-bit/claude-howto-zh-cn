<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../resources/logos/claude-howto-logo-dark.svg">
  <img alt="Claude How To" src="../resources/logos/claude-howto-logo.svg">
</picture>

# Subagents 指南

subagents 是 Claude Code 里做复杂任务拆分的关键能力。你可以把它理解成“主 Claude 把某个子任务交给一个更专业、上下文更独立的助手去做”。

---

## subagents 是什么

subagent 具备这些特点：

- 有自己的角色定位
- 有自己的上下文窗口
- 可以限制可用工具
- 可以使用单独的 system prompt
- 适合做任务拆分和专业分工

它不是简单的“再开一个对话”，而是 Claude Code 的正式能力机制。

---

## 什么时候值得用 subagents

非常适合：

- 大型代码审查
- 安全审查
- 测试策略分析
- 文档生成
- 调试与根因定位
- 多条线并行处理
- 性能瓶颈定位与优化

不太适合：

- 单文件的小改动
- 简单解释性问题
- 只需要几步就能完成的轻任务

---

## subagents 的核心价值

| 价值 | 说明 |
|------|------|
| 上下文隔离 | 避免主对话被复杂细节污染 |
| 专业分工 | 不同 agent 做不同任务 |
| 工具隔离 | 可以限制某个 agent 能做什么 |
| 可复用 | 适合团队共享常用角色 |

---

## 文件放哪里

| 类型 | 路径 | 作用域 |
|------|------|--------|
| 项目级 | `.claude/agents/` | 当前项目 |
| 用户级 | `~/.claude/agents/` | 所有项目 |
| plugin 自带 | plugin 的 `agents/` 目录 | 随 plugin 启用 |

---

## agent 定义优先级

上游这次修正了一个容易写反的点：当同名 agent 同时出现在多个位置时，优先级是：

1. CLI 临时定义：`--agents`
2. 项目级：`.claude/agents/`
3. 用户级：`~/.claude/agents/`

也就是说：

- `--agents` 只影响当前 session，优先级最高
- 项目级 agent 会覆盖同名用户级 agent
- 用户级 agent 适合放个人长期习惯，不适合压过项目团队约定

如果你在团队项目里发现“明明本机有一个同名 agent，但项目里表现不一样”，优先检查 `.claude/agents/` 是否覆盖了它。

### 嵌套 `.claude/agents/`：最近目录优先

从 `v2.1.178+` 起，如果 monorepo 里多个嵌套 `.claude/agents/` 都定义了同名 agent，Claude Code 会优先使用离当前工作目录最近的定义。

这条规则也适用于嵌套 workflow 和 output-style 定义。对中国用户来说，一个实用判断是：你在哪个 package / 子目录里启动 Claude Code，就先看离那里最近的 `.claude/`。

这里的 `.claude/agents/`、workflow、output-style 都是路径或能力标识，不要为了中文化改名。

---

## 文件格式长什么样

subagent 文件通常是：

1. YAML frontmatter
2. 后面跟 Markdown 形式的 system prompt

一个典型结构如下：

```yaml
---
name: code-reviewer
description: Review recent changes for quality issues
tools: Read, Grep, Glob, Bash
model: inherit
---
```

---

## 常用 frontmatter 字段

- `name`
- `description`
- `tools`
- `model`
- `effort`
- `permissionMode`
- `skills`
- `mcpServers`
- `background`
- `memory`
- `isolation`
- `maxTurns`
- `color`

如果你是做中文本地化，这些字段要保真；可以翻译的是下面真正给人看的 system prompt 正文。

从 `v2.1.218+` 起，agent `name` 不能包含 `:`；这个字符保留给 plugin namespace。不要为了中英文分组自行加入冒号。

project agent frontmatter 里的 `hooks` 只有在 agent 文件所在目录通过 workspace trust 后才运行。未信任项目不会借 agent hook 绕过这层安全边界。

`background: true` 的含义也发生了变化：从 `v2.1.198+` 起，subagents 默认就在后台运行；显式写 `true` 是强制它始终后台运行，并阻止 inline execution。

`effort` 可写 `low`、`medium`、`high`、`xhigh` 或 `max`，实际可用范围取决于模型。`permissionMode` 才是覆盖 subagent 权限模式的 frontmatter 字段；从 `v2.1.212+` 起，Task tool 调用参数里的 `mode` 已弃用并会被忽略，未写 `permissionMode` 时 subagent 继承父 session 的权限模式。

`color` 控制任务列表和 transcript 中的 subagent 显示色，可写 `red`、`blue`、`green`、`yellow`、`purple`、`orange`、`pink` 或 `cyan`。这些枚举值是可执行标识，不要翻译。

---

## 本目录里的示例 subagents

| 名称 | 文件 | 用途 |
|------|------|------|
| `code-reviewer` | `code-reviewer.md` | 代码审查 |
| `clean-code-reviewer` | `clean-code-reviewer.md` | Clean Code 角度审查 |
| `test-engineer` | `test-engineer.md` | 测试覆盖与测试策略 |
| `documentation-writer` | `documentation-writer.md` | 文档生成 |
| `secure-reviewer` | `secure-reviewer.md` | 安全检查 |
| `implementation-agent` | `implementation-agent.md` | 功能实现 |
| `debugger` | `debugger.md` | 错误调试与根因定位 |
| `data-scientist` | `data-scientist.md` | 数据分析与 SQL 任务 |
| `performance-optimizer` | `performance-optimizer.md` | Profiling、性能瓶颈定位与优化 |

---

## 如何安装

`v2.1.198+` 起，`/agents` 不再打开交互式创建向导。推荐直接告诉 Claude“创建一个负责安全审查的 subagent”，让它生成 `.claude/agents/<name>.md`；也可以手动编辑这个路径中的 Markdown 文件。

```bash
mkdir -p .claude/agents
cp 04-subagents/*.md .claude/agents/
```

或者安装单个：

```bash
cp 04-subagents/code-reviewer.md .claude/agents/
```

安装后可以用 `ls .claude/agents/` 检查文件，也可以直接询问 Claude 当前 session 可用哪些 subagents。

## 恢复已有 subagent

可恢复的 subagent 会返回 `agentId`。后续调用 Task tool 时，把这个值传给 `resume` 参数，就能保留原上下文继续执行；不要把它误写成主 session 的 `claude -r`。

---

## 新增角色：`performance-optimizer`

这是上游 2026 年 4 月新增的一个示例 subagent，适合这些情况：

- API 延迟明显偏高
- SQL 查询越来越慢
- 某段算法或脚本 CPU / 内存占用异常
- 你已经知道“有性能问题”，但还没确认瓶颈到底在哪里

它强调的不是“先拍脑袋优化”，而是：

1. 先量化基线
2. 再找热点
3. 一次只做一个高收益改动
4. 做完重新测

如果你在团队里已经开始让 Claude 参与优化任务，这个角色很值得保留。

---

## subagents 和 Agent Teams 怎么区分

- `subagents`：主 Claude 委派一个边界清晰的子任务，等它把结果带回来
- `Agent Teams`：多个 Claude Code 实例协作，彼此有独立上下文窗口，还能直接通信

对绝大多数中国小白用户来说，先掌握 subagents 就足够了。
`Agent Teams` 依然是实验性能力，更适合复杂协作场景，细节放在 [09-advanced-features](../09-advanced-features/) 里看。

### Agent Teams 的 iTerm2 显示模式

从 `v2.1.186+` 起，teammate mode 可以使用 `--teammate-mode iterm2`，让 teammate 分别进入独立的 iTerm2 pane。它依赖 `it2` CLI；如果你用 `--teammate-mode auto` 但本机找不到 `it2`，新版会给出提示。

这里的 `--teammate-mode iterm2`、`--teammate-mode auto`、`it2` 都是命令或工具标识，不要翻译。

---

## 如何决定要不要拆成 subagents

### 这轮上游要补的一点：subagent 也会发现同一套 skills

从 `v2.1.133+` 开始，subagent 不再只看自己内嵌的那一小组能力。
它会像主 session 一样，通过 Skill tool 发现：

- 项目级 skills
- 用户级 skills
- plugin 提供的 skills

这对“skill + subagent” 组合工作流很重要。
如果你以前感觉主 Claude 会用某个 skill，但一委派给 subagent 就像“忘了这项能力”，新版应该按统一目录发现逻辑来理解。

### subagent 嵌套现在默认深度为 3

从 `v2.1.219` 起，subagent 默认可以继续 spawn 子 subagent，默认深度为 3。设置 `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH=1` 会禁用嵌套；设为其他正整数则覆盖最大深度。

历史口径要分三段看：`v2.1.172` 到 `v2.1.216` 默认最多 5 层且不能配置；`v2.1.217` 到 `v2.1.218` 默认深度为 1，也就是嵌套关闭；`v2.1.219` 再把默认值改为 3。复杂任务可以利用嵌套分工，但仍要结合并发、权限和成本边界控制。

如果你要限制某个 subagent 能 spawn 哪些子 agent，使用 `Agent(agent_type)` 这种权限限制语法。这里的 `Agent(agent_type)`、`CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH` 都是可执行标识，不要翻译成中文字段。

### `v2.1.198+` 的默认后台运行和模型继承

- subagents 默认在后台运行，主对话可以继续工作，完成后会收到通知
- built-in `Explore` 不再固定使用 Haiku，而是继承当前 session 模型，上限为 Opus；想控制成本可在自定义 agent 中写 `model: haiku`
- subagents 和 context compaction 会继承当前 session 的 extended thinking 设置，没有单独的 per-subagent thinking 字段

另外还有两个控制入口：

- `CLAUDE_CODE_DISABLE_EXPLORE_PLAN_AGENTS=1`：禁用 built-in `Explore` 和 `Plan` agents
- `--append-subagent-system-prompt "<text>"`：在非交互 / print mode 中给每个 subagent 的 system prompt 追加内容（`v2.1.205+`）

### 推荐拆

- 任务本身可以天然分工
- 某个子任务需要单独工具权限
- 某个子任务需要更专门的 system prompt
- 你希望并行推进多个分析方向

### 不推荐拆

- 任务太小
- 子任务之间高度耦合、必须反复共享细节
- 你自己还没想清楚主任务是什么

---

## 常见坑

### 1. subagent 角色太模糊

如果 description 太空，Claude 就不知道什么时候该委派给它。

### 2. 工具给太多或太少

- 给太多：失去隔离价值
- 给太少：agent 做不了事

### 3. 直接把中文翻译写进字段名

像 `tools`、`model`、`name` 这些不能翻。

---

## 中国用户特别注意

- 如果 subagent 需要调用 shell，先确认 shell 环境。
- 如果某个 agent 依赖 Git、Python、Node、数据库 CLI 等工具，最好在正文里写清依赖。
- Windows 环境下尤其要提前确认路径和命令兼容性。

### `subagent_type` 现在不怕大小写和分隔符写错

从 `v2.1.140` 开始，`subagent_type` 的匹配会忽略大小写和分隔符形式：

- `code-reviewer`
- `Code Reviewer`
- `code_reviewer`

---

## main-thread agent 这轮更新最值得知道什么

上游最近把一个容易忽略的点写清楚了：

- 当 agent 是通过 `claude --agent <name>` 这种方式，直接作为主线程 agent 启动时
- 一些 frontmatter 字段现在会真正生效

尤其值得注意的是：

- `mcpServers`
- `permissionMode`
- `tools` / `disallowedTools`

这意味着你不能再把 agent frontmatter 简单理解成“只是描述信息”。<br>
在主线程用法下，它已经更接近真正的行为配置。

## forked subagents（fork 上下文子代理）

上游也把 `context: fork` 的定位讲得更清楚了：

- 默认 subagent 更像“新开一个干净上下文”
- `context: fork` 则会继承父上下文

它特别适合：

- 探索另一种实现路线
- 保留当前推理链再分叉
- 长任务里做 A/B 方案对比

如果你的目标是“保留主线上下文，再开一条支线试试”，就该优先考虑 forked subagents。

## subagent 输出安全扫描与 session 限额

从 `v2.1.210+` 起，Claude Code 会扫描每个 subagent 的最终报告，识别伪造的 `<system-reminder>`、`Human:` / `Assistant:` 对话或权限绕过提示等 instruction-shaped text。命中后，系统会转义或插入标记；父 session 应把它当作需要转述的发现，而不是待执行的指令。该扫描默认开启，没有公开的关闭入口，引用真实安全 flag 时也可能出现宁可多报的 false positive。

从 `v2.1.212+` 起，每个 session 默认最多 spawn **200** 个 subagents，防止委派循环失控。可用 `CLAUDE_CODE_MAX_SUBAGENTS_PER_SESSION` 调整；执行 `/clear` 会重置这项预算。

当前还有两层独立限制：

- `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`：同一时间最多运行多少个 subagents，默认 `20`
- `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`：允许嵌套 spawn 的最大深度；`v2.1.219+` 默认 `3`，设为 `1` 可禁用嵌套

```bash
export CLAUDE_CODE_MAX_SUBAGENTS_PER_SESSION=200
export CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS=20
export CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH=1  # 禁用嵌套；不设置时默认深度为 3
```

---

## 推荐下一步

- 想让 Claude 连接外部系统：看 [05-mcp](../05-mcp/)
- 想做自动检查和自动触发：看 [06-hooks](../06-hooks/)
- 想打包成团队工作流：看 [07-plugins](../07-plugins/)
