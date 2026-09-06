# Subagent 实战入门：理清 Command、Skill、Agent 与自动调用

你现在的理解已经抓住了大约七成。真正让你感觉“每个点都懂，但串不起来”的原因，是这些东西都可能表现成 Markdown 文件，却分别属于不同维度。

最关键的纠正是：

> Command、Skill、Subagent 不是“初级 → 中级 → 高级”的三级升级关系。  
> 它们分别是“怎么触发”“怎么做”“谁来做”。

## 一张表先把关系串起来

| 概念 | 可以理解成 | 主要回答的问题 |
|---|---|---|
| Command / 自定义命令 | 一个按钮、一张任务单 | 我什么时候主动启动它？ |
| Skill | SOP、工作手册、工具包 | 这类事情应该按什么流程做？ |
| Subagent | 被临时派出去的专业员工 | 谁用独立上下文完成这个子任务？ |
| Main Agent | 项目负责人 | 谁理解总目标、拆任务、汇总结果？ |
| Tool / MCP | 员工能使用的软件、数据库和外部系统 | 它能实际操作什么？ |
| Hook | 自动感应器、流水线触发器 | 发生某个事件后，是否必须自动执行？ |
| `AGENTS.md` / `CLAUDE.md` | 团队制度、项目说明书 | 整个项目长期遵守什么规则？ |
| Plugin | 安装包 | 怎么把 Skill、Agent、工具等一起分发？ |
| Agent Team | 一个可以相互沟通的项目小组 | 多个 Agent 怎样长期协作？ |

所以更准确的组合是：

```text
你提出目标
   ↓
主 Agent 理解并拆任务
   ├─ 调用 Skill：告诉自己或 Subagent“按什么方法做”
   ├─ 调用工具：真正读取文件、跑测试、生成 PPT
   ├─ 委派 Subagent：让另一个独立上下文承担子任务
   └─ 汇总结果并决定下一步
```

## 一、为什么它们看起来都是 MD 文件，却不是同一种东西

文件格式只是“包装形式”，不能用扩展名判断它是什么。

例如在 Claude Code 中：

```text
.claude/
├── commands/
│   └── review.md             # 一个手动调用的命令
├── skills/
│   └── ppt-generator/
│       ├── SKILL.md          # 一套 PPT 工作流程
│       ├── templates/
│       └── scripts/
└── agents/
    └── presentation-reviewer.md  # 一个专业子代理定义
```

虽然里面都有 Markdown，但身份不同：

- `commands/review.md`：你输入命令后执行。
- `skills/ppt-generator/SKILL.md`：模型在需要制作 PPT 时读取的方法说明。
- `agents/presentation-reviewer.md`：创建一个独立 Agent 时使用的角色与权限配置。

因此你的“简单的是 Command，复杂后变 Skill，再复杂变 Agent”只对了一部分：

- 一个短命令变复杂后，确实经常适合重构为 Skill。
- 但 Skill 再复杂，也不会自动“升级成 Agent”。
- Agent 可以调用 Skill；Skill 也可以指示主 Agent 委派 Subagent。
- 它们是可以组合的不同零件。

比如：

> “制作一份产品发布会 PPT”

可以这样完成：

- 主 Agent：理解演讲目的、观众和时长。
- 研究 Subagent：整理产品数据和证据。
- 内容 Subagent：设计叙事结构。
- `presentation` Skill：规定如何生成和检查 PPT。
- PPT 工具：真正创建 `.pptx`。
- 审阅 Subagent：检查错字、结构和视觉问题。
- 主 Agent：汇总并交付最终文件。

这里不是“PPT Skill 变成了 PPT Agent”，而是“PPT Agent 使用了 PPT Skill”。

## 二、Subagent 究竟是什么

Subagent 不是那个 Markdown 文件本身。

Markdown 或 TOML 文件只是它的“岗位说明书”。真正运行时的 Subagent 通常包含：

```text
模型
+ 独立上下文
+ 当前子任务
+ 专门的角色指令
+ 可用工具
+ 权限边界
+ 可发现的 Skills
= 一个正在工作的 Subagent
```

所以“Agent 是一个文件夹”这个理解需要调整。

更准确地说：

- Agent 是运行中的助手实例。
- Agent 定义通常是一个配置文件。
- Skill 通常是一个文件夹，因为它可能带脚本、模板和参考资料。
- Python、Node、Git、数据库 CLI 是计算机或项目环境中的依赖，不需要塞进 Agent 文件夹。
- Agent 文件只要写明需要哪些依赖、怎么使用、缺少时怎么办。

正在阅读的 Claude Code 示例，例如 [`performance-optimizer.md`](../../04-subagents/performance-optimizer.md)，就是“岗位说明书”：负责什么、按什么流程分析、允许使用哪些工具、最后返回什么格式。

## 三、Subagent 什么时候会被调用

这是最关键的困惑。

答案是：

> 定义了 Subagent，不等于每次都会自动调用。

通常有四种调用方式。

### 1. 你明确要求调用——最可靠

例如直接对 Codex 或 Claude Code 说：

```text
这个功能实现完成后，请委派三个 Subagent：
1. 一个检查正确性和潜在 Bug；
2. 一个检查安全问题；
3. 一个检查测试遗漏。

三个 Agent 都只读检查，不要修改代码。
等它们全部完成后，由主 Agent 合并重复问题，并按严重程度汇报。
```

对于不懂技术的用户，这是最推荐的起点。你不需要知道该读哪些文件，也不需要自己操作 agent ID；只要说明：

- 要不要拆；
- 分成几个方向；
- 能不能修改；
- 是否并行；
- 最后怎么汇总。

当前 Codex 支持直接要求委派，也可以按照项目里的 `AGENTS.md` 或 Skill 指令进行委派；各个子线程的结果最后由主线程汇总。参见 [Codex Subagents 官方说明](https://learn.chatgpt.com/docs/agent-configuration/subagents)。

### 2. 主 Agent 根据 description 自己判断

例如：

```yaml
description: 在非简单功能实现完成后，检查正确性、安全风险和测试遗漏。
```

主 Agent 看到任务匹配时，可能选择这个 Subagent。

但 `description` 是“匹配信号”，不是定时器，也不是绝对保证。它写得越模糊，越难触发；即使写得很好，也不建议对关键质量流程完全依赖模型自行判断。

### 3. 写进项目规则，形成长期习惯

Codex 可以在项目根目录的 `AGENTS.md` 中写：

```md
## Subagent delegation

- 实现非简单功能前，先委派 explorer 梳理相关代码。
- 实现阶段只能有一个 Agent 修改同一区域代码。
- 实现完成后，委派只读 reviewer 检查正确性、安全性和测试遗漏。
- 等待所有审查结果，由主 Agent 去重并决定是否修复。
- 单文件文案修改、拼写修正和简单解释不使用 Subagent。
```

这样以后只需要说“按照需求实现这个功能”，Codex 就会把这套委派规则作为项目约定。

Codex 会从项目根目录向当前目录逐层读取 `AGENTS.md`，离当前工作目录越近的规则越具体。参见 [Codex `AGENTS.md` 官方说明](https://learn.chatgpt.com/docs/agent-configuration/agents-md)。

### 4. 用 Hook 做确定性的自动触发

如果要求是：

> 每次提交代码前必须跑测试；  
> 每次修改某类文件后必须执行安全检查。

这时只依靠 Agent 自己判断还不够，应该使用 Hook。

可以这样理解：

- Skill：模型判断“现在可能需要这套方法”。
- Subagent：模型判断“这部分适合交给另一个人”。
- Hook：事件一发生，系统就执行预设动作。

所以“写完功能后自动审查”有两个等级：

- 希望大多数时候审查：写进 `AGENTS.md`。
- 要求每次都不能漏：使用 Hook 或 CI 作为硬性门禁。

项目里 [`06-hooks/README.md`](../../06-hooks/README.md) 讲的就是后一种机制。

## 四、不懂技术时，实际应该怎么指挥

你不需要自己准确判断“该派哪个技术专家”。你可以让主 Agent 先负责拆分。

例如：

```text
先不要开始写代码。

请根据这份需求判断：
1. 哪些部分由主 Agent 完成；
2. 哪些部分适合交给 Subagent；
3. 哪些任务可以并行；
4. 哪些任务涉及文件修改，必须串行；
5. 每个 Subagent 的输入、权限和交付物是什么。

给我一份容易理解的分工方案，确认后再执行。
```

确认后再说：

```text
按照刚才的分工执行。主 Agent 继续负责整体方案和最终整合。
可以并行的只读分析交给 Subagent。
同一批代码只允许一个 Agent 修改。
实现结束后再启动独立审查。
```

一个比较稳的项目流程是：

```text
需求沟通
  ↓
形成规格说明
  ↓
主 Agent 拆分任务
  ↓
并行只读探索：代码结构、资料、安全风险
  ↓
主 Agent 或一个 Implementation Agent 实现
  ↓
并行审查：正确性、安全、测试、文档
  ↓
主 Agent 去重、判断、修复
  ↓
运行测试并交付
```

关键规则是：分析可以大胆并行，修改代码要谨慎并行。

## 五、Codex 和 Claude Code 能不能直接复制安装

### Claude Code

这个项目里的文件是按 Claude Code 格式写的。可以把：

```text
04-subagents/code-reviewer.md
```

复制到：

```text
.claude/agents/code-reviewer.md
```

项目级放 `.claude/agents/`，个人全局使用则放 `~/.claude/agents/`。具体见 [`04-subagents/README.md`](../../04-subagents/README.md)。

Skill 则复制整个文件夹，因为它可能包含：

```text
SKILL.md
scripts/
references/
templates/
```

只复制 `SKILL.md` 有时会漏掉它依赖的脚本和模板。

### Codex

Codex 的概念相似，但格式和目录不完全一样，不能把 Claude 的 Agent MD 原样复制过去。

当前 Codex 自定义 Agent 使用：

```text
项目级：.codex/agents/*.toml
个人级：~/.codex/agents/*.toml
```

例如：

```toml
name = "reviewer"
description = "在功能完成后检查正确性、安全风险和测试遗漏。"
sandbox_mode = "read-only"

developer_instructions = """
你是只读代码审查员。

优先检查：
1. 真实行为错误
2. 安全风险
3. 回归风险
4. 缺失测试

不要修改代码。
每条发现必须提供文件位置、证据、影响和建议。
如果没有实质问题，明确说明没有发现。
"""
```

Codex 的项目 Skill 当前放在：

```text
.agents/skills/<skill-name>/SKILL.md
```

个人 Skill 放在：

```text
~/.agents/skills/<skill-name>/SKILL.md
```

Skill 可以显式通过 `$skill-name` 调用，也可以根据 `description` 隐式匹配。参见 [Codex Skills 官方说明](https://learn.chatgpt.com/docs/build-skills)。

所以跨平台迁移时应该：

- Skill：通常较容易迁移，但仍要检查工具名称和路径。
- Subagent：保留角色思想，把 Claude YAML + Markdown 改写成 Codex TOML。
- Command：检查两个产品各自的命令机制，不要直接假设兼容。
- Shell 脚本：检查 PowerShell、Git Bash、WSL、macOS/Linux 的差异。

## 六、“Subagent 也能发现 Skills”怎么理解

你的理解基本正确。

例如项目里已经有一个复杂的 PPT Skill：

```text
.agents/skills/presentation/SKILL.md
```

又定义了一个：

```text
.codex/agents/report_planner.toml
```

不需要把整个 PPT Skill 再复制到 `report_planner` 的目录中。Subagent 运行时可以使用当前环境里可发现的 Skill。

但是，不建议只写一句“你负责汇报”，然后完全期待它自己找到并正确使用 PPT Skill。更稳定的写法是：

```toml
developer_instructions = """
你负责把项目资料整理成汇报方案。

需要生成演示文稿时，使用可用的 presentation skill。
你只负责内容结构、页面大纲和材料核对；
最终文件由主 Agent 整合和验收。
"""
```

也就是说：

- 公共 Skill 只安装一份。
- Agent 定义里说明什么时候应该使用它。
- 主 Agent 委派时还可以明确指定“使用 presentation skill”。
- Skill 是否能真正工作，仍取决于它需要的工具和依赖是否可用。

Agent 可以使用零个、一个或多个 Skill，但“由很多 Skill 组成”并不自动让它变成更高级的 Agent。

## 七、“恢复已有 Subagent”到底是什么意思

“领导把任务交给员工，员工最后只返回成果”这个比喻是对的。

但员工完成第一次任务以后，可能还保留着自己的工作笔记、已经读过的文件、分析思路和上下文。

第一次调用：

```text
主 Agent：
检查支付模块的安全问题。

Subagent A：
读取代码、分析流程，最后返回审查报告。
同时系统记录 agentId = abc123。
```

后来主 Agent 发现还需要追问：

```text
请继续确认你刚才发现的问题是否也影响退款接口。
```

如果创建一个全新的 Subagent，它需要重新读代码、重新理解前因后果。

如果把 `abc123` 传给 `resume`，系统恢复的是原来的 Subagent：

```text
原来的角色
+ 原来的上下文
+ 原来的分析记录
+ 新的追问
```

这就是“恢复已有 Subagent”。

它和恢复整个主会话不同：

- `agentId + resume`：恢复某个子代理的工作线程。
- `claude -r` 或主会话 `/resume`：恢复整个主会话。
- 主 Agent 收到的是 Subagent 的总结，但 Subagent 自己的详细上下文可以继续保留在线程里。

在 Codex 中，普通用户通常不必手动管理 ID。可以直接说：

```text
让刚才负责安全审查的那个 Subagent 继续检查退款流程。
```

或者通过 `/agent` 查看和切换子线程。底层仍然是“向同一个 Agent 线程发送后续任务”的思想。

## 八、“工具给太多会失去隔离价值”是什么意思

你说得对：工具再多，它仍然有独立上下文。因此“上下文隔离”还在。

但隔离不只有上下文隔离，还有权限隔离。

例如安全审查员只需要：

```text
读取文件
搜索代码
查看差异
```

如果同时给它：

```text
修改文件
删除文件
安装依赖
访问网络
推送 Git
读取外部数据库
```

会产生几个问题：

- 它本来只负责报告，却可能顺手修改代码。
- 多个 Agent 同时编辑同一文件，容易冲突。
- 它可能访问完成任务并不需要的数据。
- 错误操作的影响范围扩大。
- 它的行动边界变得和主 Agent 差不多，审查独立性也下降。

所以“给太多工具”不是让它变成了主 Agent，而是让“最小权限”和“职责边界”消失了。

一种好的划分是：

- `reviewer`：只读，只报告。
- `security-reviewer`：只读，不运行不可信代码。
- `test-runner`：读取并执行测试，一般不改业务代码。
- `implementation-agent`：允许写入项目文件。
- 主 Agent：决定是否接受发现、是否实施修复。

## 九、所说的“三级目录式嵌套”包含三个不同概念

这里很容易混在一起。

### 1. 文件规则分层

Codex 可以有：

```text
项目根目录/AGENTS.md
项目根目录/frontend/AGENTS.md
项目根目录/backend/AGENTS.md
```

这是“规则越来越具体”。离当前工作目录更近的说明覆盖更宽泛的说明。

### 2. Skill 的渐进式读取

```text
先看 Skill 名称和 description
    ↓
命中后读取 SKILL.md
    ↓
需要时再读 references、scripts、templates
```

这是为了减少上下文占用，不是一层 Agent 创建另一层 Agent。

### 3. Subagent 运行时嵌套

```text
主 Agent
  └─ 研究 Agent
       └─ 数据核对 Agent
            └─ 来源验证 Agent
```

这才是真正的 Agent 嵌套。

嵌套每增加一层，都会增加：

- Token 消耗；
- 等待时间；
- 权限传播问题；
- 信息总结损失；
- 重复劳动；
- 委派循环风险；
- 多人同时写文件的冲突。

所以“复杂任务可以嵌套”不等于“层数越多越专业”。对当前阶段，建议最多先用：

```text
主 Agent → 一层 Subagent
```

已经能覆盖绝大多数项目。第二层只在某个 Subagent 自己又面对一个明显可独立拆分的大任务时使用。

## 十、最适合你的起步配置

不要一开始把目录里的九个 Agent 全装进去。角色太多、边界重叠，主 Agent 反而更难选。

先准备两个就够了：

```text
1. explorer
   只读，负责理解项目、定位文件、解释影响范围。

2. reviewer
   只读，负责功能完成后的正确性、安全和测试检查。
```

实现工作暂时仍交给主 Agent。等真的频繁遇到性能问题、文档问题、数据库问题，再添加：

```text
performance-optimizer
documentation-writer
data-scientist
```

日常提示词可以固定成：

```text
先理解需求并形成规格。

如果任务涉及多个模块，先委派只读 explorer 梳理影响范围；
由主 Agent 负责最终方案和代码实现；
实现完成后，委派只读 reviewer 检查正确性、安全风险和测试遗漏；
主 Agent 汇总审查结果、处理必要修复并运行验证。

小型修改不需要委派。
不要让多个 Agent 同时修改同一批文件。
```

这就把脑海里零散的知识真正串起来了：

> `AGENTS.md` 规定长期分工；主 Agent 负责调度；Subagent 承担独立任务；Skill 提供专业做法；工具负责实际执行；Hook 保证不能遗漏的自动检查；Plugin 负责整套能力的安装和分发。

当前最需要掌握的不是“设计很多 Agent”，而是学会向主 Agent 说清楚三件事：

1. 哪些方向值得分开检查；
2. 哪些 Agent 只能读取，哪些可以修改；
3. 最终必须回到主 Agent 统一决策和验收。
