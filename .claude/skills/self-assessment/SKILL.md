---
name: self-assessment
version: 2.3.0
description: Claude Code 中文自测与学习路径顾问。用于评估当前水平、识别短板、推荐学习顺序。Use when asked to "assess my level", "take the quiz", "find my level", "where should I start", "what should I learn next", "check my skills", "skill check", or similar Chinese requests.
---

# 自测与学习路径顾问（Self-Assessment & Learning Path Advisor）

这是一个完整的 Claude Code 交互式自测 skill，用来评估用户在 10 个能力域上的熟练度，并据此生成个性化学习路径。

## 参考文件

为节省上下文，较长的题目轮次、输出模板和按主题建议拆到了 `references/`：

- `references/deep-assessment-rounds.md`：Deep Assessment 的 5 轮题目与评分映射
- `references/output-templates.md`：Quick / Deep 结果和学习路径模板
- `references/topic-recommendations.md`：按主题、按得分给出的具体学习建议

执行时先按本文件确定流程；需要展示题目、生成最终报告或补齐主题建议时，再读取对应 reference。不要翻译或改名其中的路径、CLI flags、frontmatter key、JSON/YAML key。

## 使用说明

### Step 1: 先让用户选择评估模式

使用 AskUserQuestion 提供两个选项：

- **Quick Assessment**：用 2 道多选题检查 8 个能力项，约 2 分钟，用于快速判断 Beginner / Intermediate / Advanced
- **Deep Assessment**：5 轮问题，约 5 分钟，用于分别评估 10 个主题的掌握情况

如果用户选择 Quick Assessment，进入 Step 2A。
如果用户选择 Deep Assessment，进入 Step 2B。

---

### Step 2A：Quick Assessment（快速评估）

使用两个多选问题完成快速自测，每个问题最多 4 个选项。

**Question 1**（header: `基础`）
Prompt:
`第 1/2 部分：下面哪些 Claude Code 基础能力你已经具备？`

Options:
1. `启动 Claude Code 并对话` — 我会运行 `claude` 并进入对话
2. `创建或编辑 CLAUDE.md` — 我配置过项目或个人 memory
3. `使用过 3 个以上 slash commands` — 例如 `/help`、`/compact`、`/model`
4. `创建过 command 或 skill` — 写过 `SKILL.md` 或 `.claude/commands/`

**Question 2**（header: `进阶`）
Prompt:
`第 2/2 部分：下面哪些 Claude Code 进阶能力你已经具备？`

Options:
1. `配置过 MCP server` — 配置过 GitHub、数据库或其他外部数据源
2. `设置过 hooks` — 配置过 `~/.claude/settings.json` 里的 hooks
3. `创建或使用过 subagents` — 使用过 `.claude/agents/`
4. `使用过 print mode（claude -p）` — 用过非交互模式或 CI/CD 集成

**Quick 模式评分：**

- 0-2 项：Level 1 — Beginner
- 3-5 项：Level 2 — Intermediate
- 6-8 项：Level 3 — Advanced

进入 Step 3A 输出结果，并列出未勾选项作为短板。

---

### Step 2B：Deep Assessment（深度评估）

Deep 模式共 5 轮，每轮 1 个多选问题，每题最多 4 个选项，每轮覆盖 2 个主题。

完整题面也见 `references/deep-assessment-rounds.md`。如果本文件与 reference 有冲突，以本文件里的评分规则为准。

#### 第 1 轮：Slash Commands 与 Memory

Header: `命令`
Prompt:
`下面哪些操作你做过？请选择所有符合的选项。`

Options:
1. `创建过 slash command 或 skill` — 写过带 frontmatter 的 `SKILL.md` 或 `.claude/commands/` 文件
2. `在 command 中使用过动态上下文` — 用过 `$ARGUMENTS`、`$0`/`$1`、`!command`、`@file`
3. `同时配置过项目和个人 memory` — 同时配置过项目级和个人级 `CLAUDE.md`
4. `使用过 memory 层级功能` — 理解层级优先级、用过 `.claude/rules/`、path-specific rules 或 `@import`

Scoring:
- 1-2 映射到 Slash Commands（0-2）
- 3-4 映射到 Memory（0-2）

#### 第 2 轮：Skills 与 Hooks

Header: `自动化`

Options:
1. `安装并使用过自动触发的 skill` — 使用过会按 `description` 自动触发的 skill
2. `控制过 skill 调用方式` — 用过 `disable-model-invocation`、`user-invocable` 或 `context: fork`
3. `设置过 PreToolUse 或 PostToolUse hook` — 配置过常见 hook
4. `使用过进阶 hook 功能` — 用过 prompt hooks、component-scoped hooks、HTTP hooks、custom JSON output

Scoring:
- 1-2 映射到 Skills（0-2）
- 3-4 映射到 Hooks（0-2）

#### 第 3 轮：MCP 与 Subagents

Header: `集成`

Options:
1. `连接过 MCP server 并使用其工具`
2. `使用过进阶 MCP 功能` — project-scope `.mcp.json`、OAuth、Tool Search、`claude mcp serve`
3. `创建或配置过自定义 subagents`
4. `使用过进阶 subagent 功能` — worktree 隔离、persistent memory、background tasks、agent allowlists、agent teams

Scoring:
- 1-2 映射到 MCP（0-2）
- 3-4 映射到 Subagents（0-2）

#### 第 4 轮：Checkpoints 与 Advanced Features

Header: `高级`

Options:
1. `用 checkpoints 做过安全试验`
2. `使用过 planning mode 或 extended thinking`
3. `配置过 permission modes`
4. `使用过 remote / desktop / web 功能`

Scoring:
- 1 映射到 Checkpoints（0-1）
- 2-4 映射到 Advanced Features（0-2，最多记 2 分）

#### 第 5 轮：Plugins 与 CLI

Header: `综合`

Options:
1. `安装或创建过 plugin`
2. `使用过 plugin 进阶功能` — plugin hooks、plugin MCP、LSP、`--plugin-dir`
3. `在脚本或 CI/CD 中使用过 print mode`
4. `使用过进阶 CLI 功能` — `-c/-r`、`--agents`、`--json-schema`、`--fallback-model`、`--from-pr`

Scoring:
- 1-2 映射到 Plugins（0-2）
- 3-4 映射到 CLI（0-2）

进入 Step 3B 输出结果。

---

### Step 3A: Quick 模式结果输出

输出必须包含：

可直接使用 `references/output-templates.md` 中的 Quick Assessment 结果模板。

```markdown
## Claude Code 自测结果

### 你的等级：Level 1 / Level 2 / Level 3

你勾选了 **N/8** 项。

[一句鼓励性的总结]

### 你的能力概览

| 能力领域 | 状态 |
|------|--------|
| 基础 CLI 与对话 | [已掌握 / 有短板] |
| CLAUDE.md 与 Memory | [已掌握 / 有短板] |
| Slash Commands | [已掌握 / 有短板] |
| Custom Commands 与 Skills | [已掌握 / 有短板] |
| MCP | [已掌握 / 有短板] |
| Hooks | [已掌握 / 有短板] |
| Subagents | [已掌握 / 有短板] |
| Print Mode 与 CI/CD | [已掌握 / 有短板] |

### 主要短板

[对每个未勾选项，给一行说明 + 对应教程链接]

### 个性化学习路径

[按 Step 4 生成]
```

---

### Step 3B: Deep 模式结果输出

Deep 模式要输出完整结果：

可直接使用 `references/output-templates.md` 中的 Deep Assessment 结果模板。

```markdown
## Claude Code 自测结果

### 整体等级：[Level 1 / Level 2 / Level 3]

**总分：N/19**

[一句鼓励性总结]

### 你的能力画像

| 功能领域 | 得分 | 掌握程度 | 状态 |
|-------------|-------|---------|--------|
| Slash Commands | N/2 | 未掌握 / 基础 / 熟练（None / Basic / Proficient） | 学习 / 复习 / 已掌握（Learn / Review / Mastered） |
| Memory | N/2 | 未掌握 / 基础 / 熟练（None / Basic / Proficient） | 学习 / 复习 / 已掌握（Learn / Review / Mastered） |
| Skills | N/2 | 未掌握 / 基础 / 熟练（None / Basic / Proficient） | 学习 / 复习 / 已掌握（Learn / Review / Mastered） |
| Hooks | N/2 | 未掌握 / 基础 / 熟练（None / Basic / Proficient） | 学习 / 复习 / 已掌握（Learn / Review / Mastered） |
| MCP | N/2 | 未掌握 / 基础 / 熟练（None / Basic / Proficient） | 学习 / 复习 / 已掌握（Learn / Review / Mastered） |
| Subagents | N/2 | 未掌握 / 基础 / 熟练（None / Basic / Proficient） | 学习 / 复习 / 已掌握（Learn / Review / Mastered） |
| Checkpoints | N/1 | 未掌握 / 熟练（None / Proficient） | 学习 / 已掌握（Learn / Mastered） |
| Advanced Features | N/2 | 未掌握 / 基础 / 熟练（None / Basic / Proficient） | 学习 / 复习 / 已掌握（Learn / Review / Mastered） |
| Plugins | N/2 | 未掌握 / 基础 / 熟练（None / Basic / Proficient） | 学习 / 复习 / 已掌握（Learn / Review / Mastered） |
| CLI | N/2 | 未掌握 / 基础 / 熟练（None / Basic / Proficient） | 学习 / 复习 / 已掌握（Learn / Review / Mastered） |
```

然后继续输出：

- **优势领域**：得分满分的主题
- **优先补齐短板**：得分 0 的主题，按依赖顺序排列
- **需要复习的领域**：得分 1 的主题
- **你的个性化学习路径**

Deep 模式总体等级：

- 0-6：Level 1
- 7-13：Level 2
- 14-19：Level 3

---

### Step 4: 生成个性化学习路径

不要简单重复通用路线，要按短板动态生成。

具体主题建议优先参考 `references/topic-recommendations.md`，但要根据用户实际勾选结果裁剪，不要把所有主题机械列出来。

规则：

1. 满分主题不再列为重点学习项
2. 按依赖顺序排学习路径：
   - Slash Commands → Skills
   - Memory → Subagents
   - Hooks 依赖 Slash Commands
   - Plugins 依赖 MCP、Skills、Hooks
   - Advanced Features 依赖前面大多数基础
3. 得分 1 的主题推荐“深入补课”
4. 按还没掌握的主题估算总时长
5. 路径分成 2-3 个 phase

输出格式：

```markdown
### 你的个性化学习路径

**预计时间**：约 N 小时

#### 阶段 1：[名称]（约 N 小时）

**[主题]** — [从零学习 / 深入补课]
- 教程：[链接]
- 重点关注：[章节]
- 关键练习：[一个练习]
- 完成标准：[成功条件]
```

---

### Step 5: 提供后续动作

结果给完后，再用 AskUserQuestion 让用户选择：

1. `从第一个短板开始`
2. `深入学习一个主题`
3. `搭建练习项目`
4. `重新评估`

如果用户选第一项：直接进入第一个短板主题的学习建议。
如果用户选第二项：让用户选一个主题并解释。
如果用户选第三项：根据短板组合一个练习项目。
如果用户选第四项：重新开始。

## 输出要求

- 全程使用中文
- 保留关键英文术语，例如 skills、MCP、CLI
- 不要空泛鼓励，要给可执行建议
- 教程引用优先指向仓库内对应 lesson
