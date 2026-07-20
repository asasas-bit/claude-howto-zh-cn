# Commands 与 Skills：从快捷命令到可复用工作流

> 学习日期：2026-07-19  
> 适用对象：刚开始使用 Claude Code 和 Codex，希望把重复提示词或工作步骤保存下来的人

## 一、先说结论：我的理解哪些是对的

我的核心理解是对的：

> Command 和 Skill 都能把重复使用的提示词、检查清单和工作步骤保存下来，以后不用每次重新描述。

但是要补上几个重要边界：

1. 不是任意位置的 Markdown 文件都会自动变成命令。
2. 文件必须放在当前工具能够识别的特定目录，并遵守对应结构。
3. Claude Code 和 Codex 的目录及调用方式不同，不能直接混用。
4. Command 和 Skill 有重叠，但 Skill 的能力范围更大。
5. Command 或 Skill 通常是“给 AI 的工作说明”，不是保证按固定字节执行的传统程序。
6. `allowed-tools` 是 Claude Code 的权限字段，不是给 Codex 通用的写法。
7. 有提交、推送、部署、删除等副作用的流程，不能因为封装以后就省略确认和安全检查。

## 二、先纠正一个词：是 Command，不是 Comment

- `command`：命令
- `comment`：注释、评论

这个知识点讨论的是：

- Slash Command
- Custom Command
- Skill

以后看到 `.claude/commands/`，应读作“Claude 的命令目录”，不是 comments。

## 三、`01-slash-commands` 里的文件现在是什么

本仓库的 [01-slash-commands](../01-slash-commands/README.md) 中有：

```text
01-slash-commands/
├── optimize.md
├── pr.md
├── push-all.md
├── doc-refactor.md
├── commit.md
└── ...
```

这些文件目前是“可供安装的示例模板”，不是仅仅放在 `01-slash-commands` 目录里就已经成为当前项目的命令。

要让 Claude Code 把它们识别成命令，需要复制到 Claude Code 认识的位置，例如：

```text
项目根目录/
└── .claude/
    └── commands/
        └── optimize.md
```

这时文件名 `optimize.md` 去掉扩展名，就会形成：

```text
/optimize
```

所以更准确的说法是：

> 放在 `.claude/commands/` 里的 Markdown 文件，可以被 Claude Code 注册成自定义 Slash Command。

而不是：

> 只要随便写一个 Markdown 文件，它就会自动变成命令。

## 四、Command 本质上是什么

Command 可以理解成：

> 一份由我主动触发的、已经保存好的提示词或工作流程。

例如 [optimize.md](../01-slash-commands/optimize.md) 规定 Claude 要检查：

- 性能瓶颈
- 内存泄漏
- 算法改进
- 缓存机会
- 并发问题

以后输入 `/optimize`，相当于把这份完整要求重新交给 Claude。

但是它和 PowerShell 中的 `cp`、`git status` 不完全一样。

| 类型 | 例子 | 特点 |
|---|---|---|
| 传统终端命令 | `git status`、`cp` | 程序按确定的参数执行 |
| Slash Command | `/optimize`、`/pr` | 加载一份提示词，让 AI 理解并组织执行 |
| Skill | 代码审查、文章工作流 | 加载一套说明，还可以带脚本、模板和参考资料 |

因此，`/push-all` 并不是一个写死的 shell alias。它加载的是一套工作要求，Claude 仍然会结合当前仓库状态作出判断、调用工具并汇报结果。

## 五、一个 Command 文件里通常有什么

以 Claude Code 为例：

```markdown
---
description: 暂存全部改动、提交并推送到远端
allowed-tools: Bash(git status:*), Bash(git diff:*), Bash(git commit:*), Bash(git push:*)
---

# 全量提交并推送

1. 先查看状态和 diff
2. 检查密钥、大文件和构建产物
3. 向用户展示摘要并等待确认
4. 创建提交
5. 推送到远程仓库
6. 返回 commit hash 和分支
```

可以分成两部分。

### 1. Frontmatter

位于两个 `---` 之间，用来提供元数据和行为控制。

常见字段包括：

| 字段 | 大白话解释 |
|---|---|
| `name` | 展示名称；是否决定调用名要看文件所在位置 |
| `description` | 说明它做什么、什么时候适合使用 |
| `allowed-tools` | Claude Code 在本次调用中可以不再询问就使用的工具 |
| `disallowed-tools` | Skill 激活期间从可用工具中移除的工具 |
| `disable-model-invocation` | 只允许用户手动调用，不允许 Claude 自动决定调用 |
| `user-invocable` | 是否允许用户在 `/` 菜单中调用 |
| `argument-hint` | 提示调用时应输入什么参数 |
| `context: fork` | 在独立的 subagent 上下文中运行 |
| `paths` | 只在匹配的路径场景中自动启用 |
| `shell` | Skill 内动态 shell 内容使用 Bash 还是 PowerShell |

并不是每一个文件都需要写全这些字段。字段越多不代表越专业，应只写真正需要的控制项。

### 2. Markdown 正文

正文是 Claude 真正遵循的工作说明，可以包含：

- 目标
- 操作步骤
- 输入
- 输出格式
- 停止条件
- 风险检查
- 验收方式
- 参数占位符
- 对脚本、模板或参考文件的引用

## 六、`allowed-tools` 到底是什么意思

这个字段很容易被误解。

它不是：

> 安装了这些工具，或者强迫 Claude 一定要使用这些工具。

它更接近：

> 当这个 Claude Code Skill 或 Command 被调用时，列出的工具可以在当前 turn 内不再逐项询问权限。

例如：

```yaml
allowed-tools: Bash(git status:*), Bash(git diff:*)
```

表示允许匹配的只读 Git 检查。

如果再加入：

```yaml
Bash(git push:*)
```

风险就明显提高，因为推送会改变远程 GitHub 状态。

所以 `allowed-tools` 应遵守：

1. 权限尽量小
2. 只允许流程真正需要的命令
3. 读取和写入分开考虑
4. 对 push、deploy、delete、send 等操作保留人工确认
5. 不要复制自己看不懂的权限表达式

> `allowed-tools` 是 Claude Code 的扩展字段。制作 Codex Skill 时，不要直接假设它具有相同含义。

## 七、Command 和 Skill 到底是什么关系

### 过去可以这样理解

- Command：手动输入 `/name` 的单文件快捷提示词
- Skill：可以自动触发、带完整目录和附属资源的复用能力

### 现在的 Claude Code

Claude Code 官方已经明确说明：

> Custom Commands 已经并入 Skills。

以下两种写法都会创建 `/deploy`：

```text
.claude/commands/deploy.md
```

```text
.claude/skills/deploy/SKILL.md
```

旧的 `.claude/commands/` 文件仍然有效；但新建复杂复用能力时，官方更推荐 Skills，因为 Skill 可以：

- 附带脚本
- 附带模板
- 附带参考资料
- 根据 `description` 自动匹配
- 控制由用户还是 Claude 调用
- 在 subagent 上下文中运行
- 按需加载，减少长期上下文占用

如果同一个名称同时存在 Command 和 Skill，Claude Code 当前会优先使用 Skill。

参考：[Claude Code Skills 官方文档](https://code.claude.com/docs/en/skills)

## 八、Skill 的完整结构

最小 Skill：

```text
optimize/
└── SKILL.md
```

完整 Skill 可以是：

```text
optimize/
├── SKILL.md
├── scripts/
│   └── collect-metrics.ps1
├── references/
│   └── performance-checklist.md
├── examples/
│   └── expected-report.md
└── assets/
    └── report-template.md
```

各部分职责：

| 部分 | 用途 |
|---|---|
| `SKILL.md` | 入口、触发条件、工作步骤和资源导航 |
| `scripts/` | 执行确定性较强的机械操作 |
| `references/` | 领域知识、规范和详细说明 |
| `examples/` | 告诉 AI 理想输出长什么样 |
| `assets/` | 输出模板和其他素材 |

Skill 不是要求每次把所有文件都塞进上下文。它通常采用按需加载：

1. AI 先看到 Skill 名称和 `description`
2. 命中任务以后才读取 `SKILL.md`
3. 真正需要时再读取参考资料、模板或脚本

这叫 progressive disclosure，可以理解成“先看目录，再按需翻正文和附件”。

## 九、Command 不一定只做“一件小事”

一个 Command 最好有单一目标，但可以包含多个步骤。

例如 `/push-all` 的单一目标是：

> 安全地把这一批相关改动提交并推送。

为了完成这个目标，它可以依次：

1. 查看状态
2. 查看 diff
3. 检查敏感信息
4. 请求确认
5. 暂存
6. 提交
7. 推送
8. 验证远程结果

所以“一个 Command 做一件事”更准确的理解是：

> 一个 Command 聚焦一个明确结果，而不是只能执行一个终端命令。

## 十、Claude Code 中应该怎样选择

### 适合继续用 Command

满足大部分以下条件：

- 只需要一个 Markdown 文件
- 必须由我主动输入 `/name`
- 流程较短
- 不依赖模板、脚本或参考资料
- 已有 `.claude/commands/` 旧文件，运行稳定

例如：

- `/commit-message`
- `/summarize-diff`
- `/explain-error`
- `/doc-outline`

### 适合新建 Skill

满足任意一项即可优先考虑：

- 希望 Claude 在合适场景下自动选择
- 除了提示词，还需要脚本、模板或参考文档
- 多个项目或团队需要复用
- 需要路径匹配、参数、subagent 或调用控制
- 工作流较长，未来还会扩展
- 这是新创建的能力，而不是维护旧 Command

例如：

- 完整代码审查流程
- 微信公众号文章工作流
- 项目部署与验证
- 品牌语气统一
- 数据清洗和报告生成

### Claude Code 的简单建议

```text
已有的短 Command：可以继续用
新建的复用流程：优先做 Skill
有副作用的 Skill：禁止自动调用，只允许人工触发
```

对于提交、推送、部署等高风险 Skill，可以使用：

```yaml
disable-model-invocation: true
```

这样仍可手动输入 `/push-all`，但 Claude 不会因为觉得“代码看起来准备好了”就自动触发。

## 十一、Codex 中应该怎样选择

Codex 曾经有 Custom Prompts：

```text
~/.codex/prompts/example.md
```

它们可以作为 Slash Command 显式调用，但 Codex 当前官方手册已经把 Custom Prompts 标记为 deprecated，并建议新建复用能力时使用 Skills。

所以 Codex 的建议更简单：

```text
新的可复用工作流：使用 Skill
不要再把 Custom Prompt 当作首选方案
```

Codex 项目级 Skill：

```text
项目根目录/
└── .agents/
    └── skills/
        └── optimize/
            └── SKILL.md
```

Codex 个人级 Skill：

```text
$HOME/.agents/skills/optimize/SKILL.md
```

Codex 可以通过两种方式使用 Skill：

1. 显式调用：在 CLI/IDE 中打开 `/skills` 选择，或输入 `$` 提及 Skill
2. 隐式调用：任务匹配 `description` 时，由 Codex 自动选择

因此不能把 Claude Code 的方式直接说成：

> 无论 Codex 还是 Claude Code，都输入 `/文件名`。

正确区别是：

| 工具 | 推荐的显式调用 |
|---|---|
| Claude Code | `/skill-name` |
| Codex | `/skills` 中选择，或使用 `$skill-name` 提及 |

参考：[Codex Build Skills 官方文档](https://learn.chatgpt.com/docs/build-skills)

## 十二、Codex Skill 和 Claude Code Skill 能不能共用

二者都基于 `SKILL.md` 思路，工作步骤和参考资料通常可以复用，但不能保证一个目录直接原样通吃。

主要差异：

| 项目 | Claude Code | Codex |
|---|---|---|
| 项目目录 | `.claude/skills/` | `.agents/skills/` |
| 个人目录 | `~/.claude/skills/` | `$HOME/.agents/skills/` |
| 直接调用 | `/skill-name` | `/skills` 或 `$skill-name` |
| 最小元数据 | `description` 推荐，其他字段按需 | `name` 和 `description` |
| 工具权限 | 支持 `allowed-tools`、`disallowed-tools` | 由 Codex 权限、沙箱和配置管理，不直接照搬 Claude 字段 |
| 禁止自动调用 | `disable-model-invocation: true` | 可在 `agents/openai.yaml` 中设置 invocation policy |

Codex 中如果希望高风险 Skill 只能显式调用，可以添加：

```text
skill-name/
├── SKILL.md
└── agents/
    └── openai.yaml
```

`agents/openai.yaml`：

```yaml
policy:
  allow_implicit_invocation: false
```

这表示 Codex 不会仅凭任务描述自动触发，但仍可以显式选择该 Skill。

### 对我目前最实用的建议

我平时使用 Codex 更多，所以：

1. 新工作流先在真实项目的 `.agents/skills/` 中做 Codex Skill
2. 确实要用 Claude Code 时，再制作 `.claude/skills/` 版本
3. 工作步骤、模板和参考资料可以保持一致
4. 两边各自保留少量适配字段，不要强行让一份 frontmatter 通吃

## 十三、什么时候不要做 Command 或 Skill

### 只使用一次

直接在当前对话中说清楚即可，不要为了“显得高级”就封装。

### 只是项目长期事实

例如：

- 项目使用 PowerShell
- 测试命令是 `npm test`
- 不允许修改生产配置
- 文档面向中国小白

这类内容更适合：

| 工具 | 位置 |
|---|---|
| Claude Code | `CLAUDE.md` |
| Codex | `AGENTS.md` |

### 必须机械、确定地执行

如果任务要求每次得到完全确定的操作结果，应优先写脚本：

```text
Skill：负责判断什么时候执行、输入是什么、怎样解释结果
Script：负责确定地完成机械操作
```

### 必须在某个事件自动发生

例如“每次写文件后都格式化”，更适合 Hook，而不是等待用户调用 Command。

### 需要访问外部系统

如果缺少 GitHub、飞书、数据库或其他外部能力，应考虑 MCP 或 connector。Skill 可以说明怎样使用工具，但 Skill 本身不会凭空提供外部访问权限。

## 十四、用六个问题选择正确载体

| 问题 | 如果答案是“是” | 更适合 |
|---|---|---|
| 只在当前任务使用一次吗？ | 是 | 普通提示词 |
| 是项目长期规则或事实吗？ | 是 | `CLAUDE.md` / `AGENTS.md` |
| 是一套会重复执行的工作流程吗？ | 是 | Skill |
| 在 Claude Code 中很短且只想手动触发吗？ | 是 | Command 也可以 |
| 必须在某个事件自动发生吗？ | 是 | Hook |
| 必须执行确定性的机械操作吗？ | 是 | Script，由 Skill 或 Hook 调用 |
| 需要实时连接外部系统吗？ | 是 | MCP / connector |

## 十五、结合本仓库示例判断

| 示例 | 当前形式 | 更适合长期变成什么 | 原因 |
|---|---|---|---|
| `optimize.md` | Command | Skill | 可按性能审查需求自动匹配，也可能增加检查脚本和参考资料 |
| `doc-refactor.md` | Command | Skill | 可能需要文档模板、结构规范和示例 |
| `pr.md` | Command | 手动 Skill | 多步骤且会运行检查、暂存改动，应由用户控制触发 |
| `push-all.md` | 高风险 Command | 只允许显式调用的 Skill，或者继续保留 Command | 会 commit 和 push，不能让模型随意自动触发 |
| `commit.md` | Command | Command 或手动 Skill | 流程相对短，但有提交副作用 |

## 十六、把 Claude Command 升级为 Skill

以 `optimize.md` 为例，PowerShell 中可以先创建目录：

```powershell
mkdir .\.claude\skills\optimize -Force
```

然后复制为 `SKILL.md`：

```powershell
cp .\01-slash-commands\optimize.md .\.claude\skills\optimize\SKILL.md
```

最终结构：

```text
.claude/
└── skills/
    └── optimize/
        └── SKILL.md
```

调用：

```text
/optimize
```

不要同时保留同名 Command 和 Skill 来做测试，因为 Claude Code 会优先使用同名 Skill，容易让自己不知道实际运行的是哪一个。

## 十七、把相同思路做成 Codex Skill

PowerShell：

```powershell
mkdir .\.agents\skills\optimize -Force
cp .\01-slash-commands\optimize.md .\.agents\skills\optimize\SKILL.md
```

然后检查 `SKILL.md`：

```markdown
---
name: optimize
description: 分析代码中的性能、内存、算法、缓存和并发问题。用户要求性能审查或优化建议时使用。
---

# 性能优化审查

请按优先级检查：

1. 性能瓶颈
2. 内存问题
3. 算法和数据结构
4. 缓存机会
5. 并发风险

输出问题位置、严重级别、原因、修复建议和验证方法。
```

使用时：

- 打开 `/skills` 选择它
- 或输入 `$optimize`
- 也可以直接提出与 `description` 匹配的性能审查任务，让 Codex 自动选择

## 十八、设计一个好 Skill 的实用模板

```markdown
---
name: skill-name
description: 说明做什么、什么时候使用、什么时候不要使用。
---

# 目标

最终要得到什么。

# 输入

需要哪些文件、参数或上下文。

# 工作步骤

1. 先检查什么
2. 怎样处理
3. 什么时候停止
4. 什么时候必须询问用户

# 输出

结果采用什么格式。

# 验收

怎样证明任务完成。

# 安全边界

- 不允许修改什么
- 哪些操作需要确认
- 哪些风险必须先报告
```

Frontmatter 不应把所有可能字段都塞进去。真正重要的是：

- `description` 清楚
- 任务边界清楚
- 输入输出清楚
- 验收方式清楚
- 高风险操作有确认

## 十九、最容易犯的七个错误

### 1. 以为任意 `.md` 都会自动注册

必须放到对应工具识别的目录。

### 2. 把 Claude Code 目录复制给 Codex

`.claude/commands/` 和 `.claude/skills/` 不是 Codex 的项目 Skill 目录。

### 3. 以为两边都能直接 `/文件名`

Claude Code 可以直接 `/skill-name`；Codex 当前推荐 `/skills` 或 `$skill-name`。

### 4. 以为 `allowed-tools` 会安装工具

它是 Claude Code 的临时工具权限声明。

### 5. 把所有重复文字都做成 Skill

只用一次的要求继续放在普通提示词里；项目长期规则放进项目说明文件。

### 6. 高风险操作允许自动触发

commit、push、deploy、delete、send 等操作应限制为人工显式调用。

### 7. Skill 只有步骤，没有验收

如果没写怎样验证，AI 很容易“做了动作”就宣布完成。

## 二十、最终用一句话区分

```text
Command：我按下的提示词快捷按钮
Skill：AI 可以按需加载的可复用工作包
Script：机器确定执行的操作程序
Hook：在特定事件上自动启动的检查或动作
CLAUDE.md / AGENTS.md：项目长期员工手册
MCP / connector：连接外部系统的接口
```

## 二十一、给我当前阶段的选择建议

我现在不需要批量制作很多 Commands 或 Skills。

更合适的练习顺序是：

1. 先挑一个自己已经重复说过几次的真实任务
2. 把目标、输入、步骤、输出和验收写清楚
3. 因为平时主要使用 Codex，先做成项目级 Codex Skill
4. 先显式调用几次，确认流程稳定
5. 再决定是否允许自动匹配
6. 需要 Claude Code 时，再制作 Claude Skill 版本
7. 确实很短、只需手动触发时，Claude Code 中可以继续使用 Command

最终判断不是“哪个功能更新”，而是：

> 这份内容是一次性要求、长期规则、手动快捷入口，还是一套可复用工作流？

把这个问题答清楚，就知道应该使用普通提示词、项目说明、Command、Skill、Hook 还是 Script。

## 参考资料

- [本仓库 Slash Commands 指南](../01-slash-commands/README.md)
- [本仓库 Skills 指南](../03-skills/README.md)
- [Claude Code Skills 官方文档](https://code.claude.com/docs/en/skills)
- [Codex Build Skills 官方文档](https://learn.chatgpt.com/docs/build-skills)
- [Codex Custom Prompts 说明（已弃用）](https://learn.chatgpt.com/docs/custom-prompts)

