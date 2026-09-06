# 课程测验题库（Lesson Quiz Question Bank）

每个 lesson 预置 10 道题。每题都包含：

- `category`
- `question`
- `options`
- `correct`
- `explanation`
- `review`

---

## Lesson 01：Slash Commands（快捷命令）

### Q1
- **Category**: conceptual
- **Question**: slash commands 在 Claude Code 中最适合做什么？
- **Options**: A) 存长期项目规则 | B) 显式触发某个快捷操作或工作流 | C) 替代所有 hooks | D) 替代所有 skills
- **Correct**: B
- **Explanation**: slash commands 更适合用户主动输入并显式触发某个动作，例如 `/optimize`、`/pr`。
- **Review**: 什么是 slash commands

### Q2
- **Category**: practical
- **Question**: 安装单个示例命令 `/optimize` 的正确方式是什么？
- **Options**: A) `cp 01-slash-commands/optimize.md .claude/commands/` | B) `cp 01-slash-commands/optimize.md .claude/skills/` | C) `mv optimize.md ~/.claude/` | D) `claude install optimize`
- **Correct**: A
- **Explanation**: 当前示例 command 安装到 `.claude/commands/`，即可通过 `/optimize` 使用。
- **Review**: 怎么安装

### Q3
- **Category**: conceptual
- **Question**: slash commands 和 skills 的一个核心区别是什么？
- **Options**: A) 前者自动触发，后者手动触发 | B) 前者更适合手动显式触发，后者更适合自动复用能力 | C) 二者完全无关 | D) skills 只能用于插件
- **Correct**: B
- **Explanation**: slash commands 偏用户主动触发；skills 偏 Claude 按描述自动调用。
- **Review**: slash commands 和 skills 的关系

### Q4
- **Category**: practical
- **Question**: 哪些内容在 command 文件里不应该被翻译？
- **Options**: A) 标题和段落说明 | B) 真实命令名、frontmatter key、代码块命令 | C) 所有内容都不能改 | D) 只有 Markdown 标题
- **Correct**: B
- **Explanation**: `description`、`allowed-tools`、`/optimize`、命令行片段等都属于高风险标识。
- **Review**: command 文件里哪些不能翻

### Q5
- **Category**: conceptual
- **Question**: 为什么新手适合先学 slash commands？
- **Options**: A) 因为它最复杂 | B) 因为必须先学完 hooks 才能用 | C) 因为安装简单、反馈快、回报高 | D) 因为它是唯一能运行的功能
- **Correct**: C
- **Explanation**: slash commands 是最快能获得收益的一类能力，能帮助新手建立信心。
- **Review**: Slash Commands 指南开头

### Q6
- **Category**: practical
- **Question**: 如果 command 文件放对了但不生效，首先应该检查什么？
- **Options**: A) GPU 驱动 | B) 路径、扩展名和 frontmatter 格式 | C) 数据库连接 | D) 浏览器缓存
- **Correct**: B
- **Explanation**: 最常见问题就是文件不在 `.claude/commands/`、不是 `.md` 或 frontmatter 格式损坏。
- **Review**: 常见坑

### Q7
- **Category**: conceptual
- **Question**: 什么时候应该把 command 升级成 skill？
- **Options**: A) 任何时候都不该升级 | B) 当它变成长期复用工作流，并需要模板、脚本或自动触发时 | C) 只有代码超过 500 行时 | D) 只有在 Windows 下
- **Correct**: B
- **Explanation**: 当一个 command 变得需要长期复用、附带资源或自动触发时，更适合转为 skill。
- **Review**: 什么时候该升级成 skill

### Q8
- **Category**: practical
- **Question**: `/pr` 这个示例 command 的重点是什么？
- **Options**: A) 管理 MCP | B) 准备 PR 前的检查、测试和摘要整理 | C) 部署到生产环境 | D) 配置 CLAUDE.md
- **Correct**: B
- **Explanation**: `/pr` 用于在发 PR 前整理改动、跑测试、生成摘要。
- **Review**: 本目录里的示例命令

### Q9
- **Category**: practical
- **Question**: 你想限制某个 skill 能使用哪些工具，应该在 frontmatter 里加哪个字段？
- **Options**: A) `tools: [Read, Grep]` | B) `allowed-tools: [Read, Grep]` | C) `permissions: [Read, Grep]` | D) `restrict-tools: [Read, Grep]`
- **Correct**: B
- **Explanation**: `SKILL.md` frontmatter 里的 `allowed-tools` 用来限制这个 command / skill 可以调用的工具范围。
- **Review**: command 文件里哪些不能翻

### Q10
- **Category**: conceptual
- **Question**: skill 里的 `@file` 语法主要用来做什么？
- **Options**: A) 导入另一个 skill | B) 引用文件并把文件内容带入 prompt | C) 创建 symlink | D) 设置文件权限
- **Correct**: B
- **Explanation**: `@path/to/file` 会把目标文件内容纳入 prompt，适合按需引入模板、上下文或参考资料。
- **Review**: 在 prompt 中引用文件

---

## Lesson 02：Memory（记忆）

### Q1
- **Category**: conceptual
- **Question**: memory 和当前会话上下文的核心区别是什么？
- **Options**: A) memory 只在本次会话有效 | B) memory 是长期规则层，会跨会话影响 Claude 的默认上下文 | C) 二者没有区别 | D) memory 只给人看，不影响 Claude
- **Correct**: B
- **Explanation**: `CLAUDE.md` 体系提供的是长期上下文，不是当前对话中的一次性说明。
- **Review**: memory 是什么

### Q2
- **Category**: practical
- **Question**: 最快安装项目级 memory 的方式是什么？
- **Options**: A) `cp 02-memory/project-CLAUDE.md ./CLAUDE.md` | B) `touch memory.md` | C) `claude --memory init` | D) `mv project-CLAUDE.md docs/`
- **Correct**: A
- **Explanation**: 直接复制项目模板到根目录的 `CLAUDE.md` 是最快方式。
- **Review**: 最快上手方式

### Q3
- **Category**: conceptual
- **Question**: 哪类信息最适合写进 memory？
- **Options**: A) 高频且长期稳定的项目规则 | B) 临时一次性任务说明 | C) 实时数据库数据 | D) 聊天记录全文
- **Correct**: A
- **Explanation**: memory 应该存长期稳定、高价值、跨会话都适用的规则。
- **Review**: 写什么最有价值

### Q4
- **Category**: practical
- **Question**: 个人偏好通常更适合放在哪个文件？
- **Options**: A) `~/.claude/CLAUDE.md` | B) `README.md` | C) `package.json` | D) `.mcp.json`
- **Correct**: A
- **Explanation**: 个人级 memory 通常放在 `~/.claude/CLAUDE.md`。
- **Review**: 个人级 memory

### Q5
- **Category**: conceptual
- **Question**: 为什么不建议把一次性任务说明塞进 `CLAUDE.md`？
- **Options**: A) 因为 Claude 看不懂 | B) 因为这会污染长期规则层，让 memory 失去聚焦 | C) 因为文件会变只读 | D) 因为 Git 不支持
- **Correct**: B
- **Explanation**: 一次性任务更适合放在当前对话或单独文档，而不是长期自动加载的 memory。
- **Review**: 哪些内容不适合写进 memory

### Q6
- **Category**: practical
- **Question**: 对话中快速写入一条 memory 的常见方式是什么？
- **Options**: A) 使用 `/memory` 打开编辑器，或直接用自然语言让 Claude 记住 | B) 以 `#` 开头写一条规则 | C) `@memory` | D) `/save-context`
- **Correct**: A
- **Explanation**: 推荐方式是用 `/memory` 编辑 memory 文件，或直接说“记住：……”。`# your rule` 这种前缀写法已经停用，不应再作为新教程推荐。
- **Review**: 高价值命令

### Q7
- **Category**: conceptual
- **Question**: 项目级 memory 和个人级 memory 的一个重要区别是什么？
- **Options**: A) 前者更适合团队共享，后者更适合个人偏好 | B) 前者不能被 Claude 读取 | C) 后者必须提交到 Git | D) 二者路径完全相同
- **Correct**: A
- **Explanation**: 项目级适合团队规范，个人级适合个人风格与习惯。
- **Review**: 常见 memory 类型

### Q8
- **Category**: practical
- **Question**: 如果你在 Windows 上工作，memory 里特别值得补充什么？
- **Options**: A) 股票价格 | B) 路径规则、shell 差异和环境要求 | C) 天气预报 | D) 表情包
- **Correct**: B
- **Explanation**: 对中国用户和 Windows 用户来说，路径与 shell 差异是高频踩坑点。
- **Review**: 中国用户特别注意

### Q9
- **Category**: conceptual
- **Question**: 多个不同范围的 `CLAUDE.md` 同时加载时，Claude Code 如何处理它们？
- **Options**: A) 只保留范围最窄的一份 | B) 按 Managed、User、Project、Local 范围拼接进上下文，而不是严格覆盖 | C) 只保留最近修改的一份 | D) 全部转成 auto memory
- **Correct**: B
- **Explanation**: `CLAUDE.md` 文件会按范围拼接进上下文；auto memory 和 `.claude/rules/*.md` 是独立的相关机制，不能混成一条严格覆盖链。
- **Review**: 两套 memory 机制与 CLAUDE.md 加载顺序

### Q10
- **Category**: practical
- **Question**: 你同时跨两个仓库工作，希望 Claude 加载两个仓库里的 `CLAUDE.md`，应该用哪个 flag？
- **Options**: A) `--multi-repo` | B) `--add-dir /path/to/other` | C) `--include /path/to/other` | D) `--merge-context /path/to/other`
- **Correct**: B
- **Explanation**: `--add-dir` 会加载额外目录中的 `CLAUDE.md`，适合多仓库上下文。
- **Review**: 用 --add-dir 加载额外目录

---

## Lesson 03：Skills（技能）

### Q1
- **Category**: conceptual
- **Question**: skills 最核心的价值是什么？
- **Options**: A) 替代所有命令行 | B) 让稳定工作流可以被 Claude 复用和自动触发 | C) 只用于图片生成 | D) 只用于插件市场
- **Correct**: B
- **Explanation**: skills 的意义在于把流程、模板和实践沉淀为可复用能力。
- **Review**: skills 是什么

### Q2
- **Category**: practical
- **Question**: 一个 skill 的核心文件名是什么？
- **Options**: A) `README.md` | B) `SKILL.md` | C) `RULES.md` | D) `PROMPT.md`
- **Correct**: B
- **Explanation**: `SKILL.md` 是 skill 的主定义文件。
- **Review**: 一个 skill 的基本结构

### Q3
- **Category**: conceptual
- **Question**: progressive disclosure 的意义是什么？
- **Options**: A) 一开始把所有内容全塞进上下文 | B) 按需加载 metadata、instructions 和 resources | C) 让 skill 只能手动触发 | D) 让文件更短
- **Correct**: B
- **Explanation**: skills 的优势之一是按需加载，metadata 默认预算约占上下文窗口 1%，fallback 约 8,000 字符；真正命中后再加载 `SKILL.md` 和资源文件。
- **Review**: progressive disclosure 是什么意思

### Q4
- **Category**: practical
- **Question**: `SKILL.md` 里哪些字段最不能被中文化？
- **Options**: A) `name`、`description`、`effort`、`shell` 这些 key | B) 只有标题 | C) 只有第一行 | D) 都可以翻
- **Correct**: A
- **Explanation**: 这些 frontmatter key 会被系统解析，必须保真。
- **Review**: `SKILL.md` 里哪些不能翻

### Q5
- **Category**: conceptual
- **Question**: skills 和 slash commands 的一个重要区别是什么？
- **Options**: A) skills 更偏自动复用，slash commands 更偏手动显式触发 | B) slash commands 可以自动触发，skills 不行 | C) 二者完全相同 | D) skills 不能附带脚本
- **Correct**: A
- **Explanation**: skills 适合长期复用和自动调用；slash commands 更适合手动入口。
- **Review**: skills 和 slash commands 的区别

### Q6
- **Category**: practical
- **Question**: 将 `code-review` 安装到个人 skills 目录的正确方式是什么？
- **Options**: A) `cp -r 03-skills/code-review ~/.claude/skills/` | B) `mv code-review ~/.claude/` | C) `claude install skill code-review` | D) `cp SKILL.md CLAUDE.md`
- **Correct**: A
- **Explanation**: 个人级 skill 安装到 `~/.claude/skills/`。
- **Review**: 如何安装

### Q7
- **Category**: conceptual
- **Question**: skills 什么时候最值得使用？
- **Options**: A) 当某个流程经常重复出现，而且希望 Claude 在合适场景自动帮你做 | B) 只在第一次使用 Claude 时 | C) 只在设计 logo 时 | D) 只在没有代码时
- **Correct**: A
- **Explanation**: 高频、稳定、可复用的工作流最适合 skill 化。
- **Review**: skills 为什么重要

### Q8
- **Category**: practical
- **Question**: 如果 script 依赖 `python` 或 `node`，在 skill 文档里最好补什么？
- **Options**: A) 股票代码 | B) shell / 环境变量 / 运行依赖说明 | C) 作者邮箱 | D) 社交媒体链接
- **Correct**: B
- **Explanation**: 这能显著减少中国用户和 Windows 用户的实际踩坑。
- **Review**: 中国用户特别注意

### Q9
- **Category**: conceptual
- **Question**: Claude 查找 skills 时的优先级顺序是什么？
- **Options**: A) User > Project > Enterprise | B) Enterprise > Personal > Project（plugin skill 使用 namespace） | C) Project > User > Enterprise | D) 按字母顺序
- **Correct**: B
- **Explanation**: skill 优先级是 Enterprise > Personal > Project；plugin skill 会带 namespace，避免和普通 skill 名称冲突。
- **Review**: skill 类型、位置与优先级

### Q10
- **Category**: practical
- **Question**: 如果你想阻止 Claude 自动调用某个 skill，但仍允许用户手动使用，应该怎么做？
- **Options**: A) 设置 `user-invocable: false` | B) 设置 `disable-model-invocation: true` | C) 删除 `description` 字段 | D) 设置 `auto-invoke: false`
- **Correct**: B
- **Explanation**: `disable-model-invocation: true` 会阻止模型自动触发，但保留用户通过 `/` 菜单手动调用的能力。
- **Review**: 控制 skill 的调用方式

---

## Lesson 04：Subagents（子代理）

### Q1
- **Category**: conceptual
- **Question**: subagents 最适合解决什么问题？
- **Options**: A) 复杂任务拆分与专业分工 | B) 替代 Git | C) 存长期规则 | D) 生成 favicon
- **Correct**: A
- **Explanation**: subagents 的核心优势是分工、隔离和上下文拆分。
- **Review**: subagents 是什么

### Q2
- **Category**: practical
- **Question**: 同名 agent 同时出现在 CLI、项目级和用户级时，优先级顺序是什么？
- **Options**: A) CLI > 项目级 > 用户级 | B) CLI > 用户级 > 项目级 | C) 用户级 > 项目级 > CLI | D) 三者没有优先级
- **Correct**: A
- **Explanation**: 新版口径是 `--agents` 临时定义最高，其次是 `.claude/agents/` 项目级，最后才是 `~/.claude/agents/` 用户级。
- **Review**: agent 定义优先级

### Q3
- **Category**: conceptual
- **Question**: subagent 为什么能减少主对话污染？
- **Options**: A) 因为它有自己独立的上下文窗口 | B) 因为它不会读文件 | C) 因为它不能返回结果 | D) 因为它只能运行一次
- **Correct**: A
- **Explanation**: subagents 通过独立上下文隔离细节，避免主会话被复杂内容淹没。
- **Review**: subagents 的核心价值

### Q4
- **Category**: practical
- **Question**: 以下哪个字段属于 subagent frontmatter，且不应翻译？
- **Options**: A) `tools` | B) `模型` | C) `用途说明` | D) `附加提示词说明`
- **Correct**: A
- **Explanation**: `name`、`description`、`tools`、`model` 等字段都属于 frontmatter 协议部分。
- **Review**: frontmatter 里这些字段不要翻

### Q5
- **Category**: conceptual
- **Question**: 什么情况下不建议拆 subagents？
- **Options**: A) 任务很小且耦合很高 | B) 任务复杂且多线程 | C) 需要不同角色并行分析 | D) 需要工具隔离
- **Correct**: A
- **Explanation**: 小任务或高度耦合任务强拆 subagents，反而增加复杂度。
- **Review**: 如何决定要不要拆成 subagents

### Q6
- **Category**: practical
- **Question**: `code-reviewer` 这类 subagent 最适合什么时候使用？
- **Options**: A) 在代码改动后做结构化审查 | B) 初始化 npm | C) 改 favicon 颜色 | D) 改 Git 用户名
- **Correct**: A
- **Explanation**: `code-reviewer` 就是典型的审查型 subagent。
- **Review**: 本目录里的示例 subagents

### Q7
- **Category**: conceptual
- **Question**: subagent 的工具权限为什么重要？
- **Options**: A) 因为不同 agent 需要不同能力边界和安全范围 | B) 因为工具越多越好 | C) 因为工具只影响 UI | D) 因为工具会决定字体大小
- **Correct**: A
- **Explanation**: 工具权限既影响功能，也影响安全性和任务边界。
- **Review**: subagents 的核心价值

### Q8
- **Category**: practical
- **Question**: Windows 用户在使用依赖 shell 的 subagent 时，最该先确认什么？
- **Options**: A) GPU 型号 | B) 当前到底在 PowerShell、Git Bash 还是 WSL 中运行 | C) 显示器刷新率 | D) 本机壁纸
- **Correct**: B
- **Explanation**: 路径、shell 语法和命令兼容性都会受运行环境影响。
- **Review**: 中国用户特别注意

### Q9
- **Category**: conceptual
- **Question**: subagent 支持哪些 `permissionMode` 值？
- **Options**: A) 旧式权限词：read, write, admin | B) `default`、`acceptEdits`、`bypassPermissions`、`plan`、`dontAsk`、`auto` | C) 安全等级词：safe, normal, dangerous | D) 访问范围词：restricted, standard, elevated
- **Correct**: B
- **Explanation**: subagent 支持 `default`、`acceptEdits`、`bypassPermissions`、`plan`、`dontAsk`、`auto`；它们分别控制提示、自动接受编辑、跳过检查、只读计划、默认拒绝和自动分类。
- **Review**: 常用 frontmatter 字段

### Q10
- **Category**: practical
- **Question**: 如果某个 subagent 上次运行返回了 `agentId`，要怎样继续这个 subagent？
- **Options**: A) 使用 `/resume agent-id` | B) 调用 Task tool 时传入带 `agentId` 的 `resume` 参数 | C) 使用 `claude -r agent-id` | D) subagent 不能继续
- **Correct**: B
- **Explanation**: 可恢复的 subagent 通过 Task tool 的 `resume` 参数带上之前返回的 `agentId`，从而保留上下文继续执行。
- **Review**: 恢复已有 subagent

---

## Lesson 05：MCP（外部工具协议）

### Q1
- **Category**: conceptual
- **Question**: MCP 的核心价值是什么？
- **Options**: A) 提供长期项目规则 | B) 让 Claude 接入外部工具和实时数据 | C) 取代 CLI | D) 取代所有 plugins
- **Correct**: B
- **Explanation**: MCP 是 Claude 访问外部系统和实时数据的标准协议。
- **Review**: MCP 解决什么问题

### Q2
- **Category**: practical
- **Question**: 试用 GitHub MCP 示例前，最常见需要先准备什么？
- **Options**: A) `GITHUB_TOKEN` | B) `AWS_SECRET` | C) `JAVA_HOME` | D) `DISPLAY`
- **Correct**: A
- **Explanation**: GitHub MCP 通常首先依赖可用的 `GITHUB_TOKEN`。
- **Review**: 直接复制示例配置

### Q3
- **Category**: conceptual
- **Question**: MCP 和 memory 的一个重要区别是什么？
- **Options**: A) memory 更适合实时外部数据 | B) MCP 更适合实时外部数据，memory 更适合长期规则 | C) 二者完全一样 | D) MCP 只能存文档
- **Correct**: B
- **Explanation**: memory 适合长期稳定规则；MCP 适合实时和外部数据接入。
- **Review**: MCP 解决什么问题

### Q4
- **Category**: practical
- **Question**: 下面哪个 JSON key 在 MCP 配置里绝对不能翻译？
- **Options**: A) `mcpServers` | B) “用途” | C) “说明” | D) “备注”
- **Correct**: A
- **Explanation**: `mcpServers` 属于协议字段，翻译会直接破坏配置。
- **Review**: 哪些内容不能翻

### Q5
- **Category**: conceptual
- **Question**: 为什么中国用户在第一次用 MCP 时更容易遇到安装问题？
- **Options**: A) 因为 MCP 只能在美国用 | B) 因为常依赖 `npx`、外部 API、GitHub 和网络环境 | C) 因为 MCP 需要专用键盘 | D) 因为 JSON 不能保存中文
- **Correct**: B
- **Explanation**: 首次安装或连通性往往受 npm、代理、证书和 GitHub 网络影响。
- **Review**: 中国用户特别注意

### Q6
- **Category**: practical
- **Question**: 如果想一次挂多个服务，应该参考哪个示例？
- **Options**: A) `multi-mcp.json` | B) `README.md` | C) `favicon-32.svg` | D) `personal-CLAUDE.md`
- **Correct**: A
- **Explanation**: 多服务组合对应 `05-mcp/multi-mcp.json`。
- **Review**: 本目录里的示例配置

### Q7
- **Category**: conceptual
- **Question**: 为什么不建议一上来接很多 MCP 服务？
- **Options**: A) 因为只能接一个 | B) 因为排障和权限问题会叠加，推荐先跑通最核心的一个 | C) 因为 Git 会坏 | D) 因为 Claude 不支持
- **Correct**: B
- **Explanation**: 推荐先跑通 GitHub 或 filesystem，再逐步扩展。
- **Review**: 常见坑

### Q8
- **Category**: practical
- **Question**: Windows 原生环境运行 `npx` MCP server 时，文档建议优先关注什么？
- **Options**: A) `cmd /c` 风格与 shell 差异 | B) 鼠标 DPI | C) 壁纸分辨率 | D) Git commit message
- **Correct**: A
- **Explanation**: Windows shell 兼容性是 MCP 配置中非常常见的差异点。
- **Review**: 中国用户特别注意

### Q9
- **Category**: conceptual
- **Question**: managed config 里 `allowedMcpServers` 和 `deniedMcpServers` 同时匹配一个 server 时，谁优先？
- **Options**: A) allow 规则优先 | B) deny 规则优先 | C) 最后配置的规则优先 | D) 两者独立生效
- **Correct**: B
- **Explanation**: 在 managed MCP configuration 中，deny rules 始终优先于 allow rules。
- **Review**: 托管 MCP 配置

### Q10
- **Category**: practical
- **Question**: 在对话里引用 MCP resource 应该使用什么语法？
- **Options**: A) `/mcp resource-name` | B) `@server-name:protocol://resource/path` mention 语法 | C) `mcp.get("resource")` | D) resources 会自动加载
- **Correct**: B
- **Explanation**: MCP resources 通过 `@server-name:protocol://resource/path` 这类 mention 语法在对话中访问。
- **Review**: 用 @ 引用 MCP resources

---

## Lesson 06：Hooks（钩子）

### Q1
- **Category**: conceptual
- **Question**: hooks 最适合把什么事情自动化？
- **Options**: A) 每次都要手动重复检查的动作 | B) 所有写作任务 | C) 只做图片压缩 | D) 只管理 GitHub stars
- **Correct**: A
- **Explanation**: hooks 的核心价值是把重复检查、提醒和拦截变成事件驱动自动化。
- **Review**: hooks 是什么

### Q2
- **Category**: practical
- **Question**: 一个 hooks 配置里最外层的关键 JSON key 是什么？
- **Options**: A) `hooks` | B) `memory` | C) `plugins` | D) `agents`
- **Correct**: A
- **Explanation**: hooks 的配置结构从 `hooks` 这个 key 开始。
- **Review**: 基本结构

### Q3
- **Category**: conceptual
- **Question**: `PreToolUse` 和 `PostToolUse` 的主要区别是什么？
- **Options**: A) 一个在工具前，一个在工具后 | B) 一个只给图片用 | C) 一个是 CLI，一个是 MCP | D) 完全一样
- **Correct**: A
- **Explanation**: `PreToolUse` 适合拦截和校验；`PostToolUse` 适合验证与补充上下文。
- **Review**: 最常见的事件

### Q4
- **Category**: practical
- **Question**: 如果你想先体验 hooks 的价值，最推荐先试哪个示例？
- **Options**: A) `pre-commit.sh` | B) `favicon-32.svg` | C) `README.backup.md` | D) `project-CLAUDE.md`
- **Correct**: A
- **Explanation**: 提交前跑测试是最容易体会 hooks 价值的起步示例。
- **Review**: 一个高价值起步例子

### Q5
- **Category**: conceptual
- **Question**: 截至 Claude Code v2.1.119，hooks 支持哪五种类型？
- **Options**: A) `command`、`http`、`mcp_tool`、`prompt`、`agent` | B) `shell`、`json`、`yaml`、`plugin`、`web` | C) `pre`、`post`、`read`、`write`、`sync` | D) `sync`、`async`、`web`、`app`、`memory`
- **Correct**: A
- **Explanation**: 新版 hooks 已把 `mcp_tool` 明确列为 hook 类型，所以不能继续按“四种类型”的旧口径记。
- **Review**: 五种 hook 类型

### Q6
- **Category**: practical
- **Question**: hooks 配置里哪些字段最不能翻？
- **Options**: A) `hooks`、`matcher`、`type`、`command`、事件名 | B) 所有 Markdown 标题 | C) 只有注释 | D) 只有文件名
- **Correct**: A
- **Explanation**: 这些字段和事件名属于协议结构，翻译会直接损坏配置。
- **Review**: hooks 配置里哪些不能翻

### Q7
- **Category**: conceptual
- **Question**: 为什么“hook 做得太重”会影响使用体验？
- **Options**: A) 因为它会让每次触发都变慢 | B) 因为 hook 会自动删文件 | C) 因为 hook 会禁用 Claude | D) 因为 hook 会禁用 Git
- **Correct**: A
- **Explanation**: 高成本 hook 会让常规工作流变得拖沓，应该先从轻量检查做起。
- **Review**: 常见坑

### Q8
- **Category**: practical
- **Question**: Windows 用户使用 hooks 前，最重要的一个检查点是什么？
- **Options**: A) 当前 shell 是什么 | B) 鼠标速度 | C) 电池电量 | D) GitHub 头像
- **Correct**: A
- **Explanation**: PowerShell、Git Bash、WSL 的差异会直接影响脚本兼容性。
- **Review**: 中国用户特别注意

### Q9
- **Category**: conceptual
- **Question**: Claude Code 一共支持多少种 hook events？
- **Options**: A) 16 | B) 25 | C) 30 | D) 31
- **Correct**: D
- **Explanation**: 当前教程按 Claude Code `v2.1.219+` 的口径记录 31 个 hook 事件、5 种 hook 类型；新增事件是 `DirectoryAdded`，不要再沿用旧资料里的 25、28、29 或 30 个事件。
- **Review**: 常见事件

### Q10
- **Category**: practical
- **Question**: 如果你想排查某个 hook 为什么没有触发，最佳做法是什么？
- **Options**: A) 在 hook 脚本里加 print | B) 使用 `--debug` flag 和 `Ctrl+O` verbose mode | C) 查看系统日志 | D) hooks 没有调试工具
- **Correct**: B
- **Explanation**: `--debug` 和 `Ctrl+O` verbose mode 会展示 hook 执行细节，包括哪些 hook 被触发、输入和输出是什么。
- **Review**: debugging 和排错思路

---

## Lesson 07：Plugins（插件）

### Q1
- **Category**: conceptual
- **Question**: plugin 的核心价值是什么？
- **Options**: A) 把多项 Claude Code 能力打包成一套可安装方案 | B) 只用来放图片 | C) 只用来写 README | D) 只用来存 token
- **Correct**: A
- **Explanation**: plugin 用于分发整套工作流，而不是单一能力。
- **Review**: plugin 是什么

### Q2
- **Category**: practical
- **Question**: plugin manifest 的标准位置是什么？
- **Options**: A) `.claude-plugin/plugin.json` | B) `plugin.yaml` | C) `README.md` | D) `.mcp.json`
- **Correct**: A
- **Explanation**: 当前示例与现代结构都使用 `.claude-plugin/plugin.json`。
- **Review**: 基本结构

### Q3
- **Category**: conceptual
- **Question**: 什么情况下特别适合做 plugin？
- **Options**: A) 只有一个简单 command 时 | B) 工作流需要团队统一分发时 | C) 只想做一篇博客时 | D) 只想改单个注释
- **Correct**: B
- **Explanation**: plugin 最适合做团队级、一键安装的整套能力分发。
- **Review**: 什么时候该做 plugin

### Q4
- **Category**: practical
- **Question**: `.claude-plugin/plugin.json` 里哪些 key 最不能翻？
- **Options**: A) `name`、`version`、`description`、`author`、`license` | B) 只有第一行 | C) 只有注释 | D) 都可以翻
- **Correct**: A
- **Explanation**: 这些 key 直接影响 manifest 解析和 plugin 识别。
- **Review**: plugin manifest 里哪些不能翻

### Q5
- **Category**: conceptual
- **Question**: 为什么不建议在工作流还没稳定时过早做 plugin？
- **Options**: A) 因为 plugin 不能改 | B) 因为打包会提高后续迭代成本 | C) 因为插件只能官方维护 | D) 因为 plugin 不能含 commands
- **Correct**: B
- **Explanation**: 先把单项能力跑顺，再打包更稳妥。
- **Review**: 什么时候该做 plugin

### Q6
- **Category**: practical
- **Question**: `pr-review` 这个示例 plugin 主要解决什么问题？
- **Options**: A) PR 审查流程 | B) Docker 镜像压缩 | C) 图片裁剪 | D) 字体管理
- **Correct**: A
- **Explanation**: `pr-review` 把安全、测试和性能审查整合到 PR review 流程中。
- **Review**: 本目录里的示例 plugins

### Q7
- **Category**: conceptual
- **Question**: plugin 里常见会一起打包哪些能力？
- **Options**: A) commands、skills、subagents、hooks、MCP | B) 只有 Markdown | C) 只有 shell | D) 只有 logo
- **Correct**: A
- **Explanation**: plugin 的价值就在于组合能力，而不是单文件。
- **Review**: plugin 是什么

### Q8
- **Category**: practical
- **Question**: 发布中文 plugin 时，README 里最值得额外说明什么？
- **Options**: A) 依赖的外部服务、token、CLI、Windows / WSL 支持情况 | B) 作者最喜欢的电影 | C) 键盘颜色 | D) 不需要额外说明
- **Correct**: A
- **Explanation**: 这直接决定中国用户能不能顺利安装和使用。
- **Review**: 中国用户特别注意

### Q9
- **Category**: conceptual
- **Question**: plugin 相比 standalone skills / hooks / MCP 的主要优势是什么？
- **Options**: A) plugin 更快 | B) 单命令安装、可版本化、可通过 marketplace 分发，并能把多组件打包在一起 | C) plugin 权限更高 | D) plugin 一定离线可用
- **Correct**: B
- **Explanation**: plugin 可以把多个组件打包成一个可安装、可版本化、可更新的方案，比手工配置 standalone components 更适合团队分发。
- **Review**: plugin 的价值到底在哪里

### Q10
- **Category**: practical
- **Question**: plugin 目录里的 hooks 配置通常放在哪里？
- **Options**: A) `.claude-plugin/hooks.json` | B) `hooks/hooks.json` | C) `plugin.json` 的 hooks section | D) `.claude/settings.json`
- **Correct**: B
- **Explanation**: plugin hooks 通常配置在 plugin 目录结构里的 `hooks/hooks.json`。
- **Review**: plugin hooks 放在哪里

---

## Lesson 08：Checkpoints（检查点）

### Q1
- **Category**: conceptual
- **Question**: checkpoints 最核心的价值是什么？
- **Options**: A) 帮你安全试错和回退 | B) 自动部署 | C) 存 API key | D) 替代 Git
- **Correct**: A
- **Explanation**: checkpoints 让你敢试，因为随时可以回退。
- **Review**: checkpoint 是什么

### Q2
- **Category**: practical
- **Question**: 打开 checkpoint / rewind 界面的两种常见方式是什么？
- **Options**: A) `Esc+Esc` 或 `/rewind` | B) `/checkpoint-save` 或 `Ctrl+R` | C) `Alt+P` 或 `/memory` | D) 只能重启 Claude
- **Correct**: A
- **Explanation**: 最常见方式就是双击 `Esc` 或使用 `/rewind`。
- **Review**: 怎么打开

### Q3
- **Category**: conceptual
- **Question**: 为什么 checkpoints 对新手尤其重要？
- **Options**: A) 因为能降低“怕改坏”的心理门槛 | B) 因为必须先开 checkpoint 才能聊天 | C) 因为只对新手开放 | D) 因为它能自动修 bug
- **Correct**: A
- **Explanation**: 它解决的是试错焦虑，而不只是回滚功能。
- **Review**: 为什么它重要

### Q4
- **Category**: practical
- **Question**: `Restore code` 和 `Restore conversation` 的一个关键区别是什么？
- **Options**: A) 前者主要回代码，后者主要回对话 | B) 二者完全一样 | C) 前者会删 Git 仓库 | D) 后者会清空系统设置
- **Correct**: A
- **Explanation**: rewind 不是只有一种回退方式，可以只退代码或只退对话。
- **Review**: rewind 时你会看到什么选项

### Q5
- **Category**: conceptual
- **Question**: checkpoint 除了回退，还有什么价值？
- **Options**: A) 用于探索多个实现方案并比较 | B) 只能清缓存 | C) 只能导出图片 | D) 只能查版本号
- **Correct**: A
- **Explanation**: 它同样适合做方案对比和实验分支。
- **Review**: 一个很实用的工作流

### Q6
- **Category**: practical
- **Question**: 如果你想在中文化大改中安全尝试多个版本，checkpoint 有什么帮助？
- **Options**: A) 可以在误翻关键标识后快速回退 | B) 会自动提交到 GitHub | C) 会帮你写文案 | D) 会自动翻译所有字段
- **Correct**: A
- **Explanation**: 这类大范围替换最适合借助 checkpoint 做安全迭代。
- **Review**: 中国用户特别注意

### Q7
- **Category**: conceptual
- **Question**: 为什么 `Summarize from here` 对长会话很有用？
- **Options**: A) 因为它能压缩上下文负担 | B) 因为它会把代码删掉 | C) 因为它会关掉 hooks | D) 因为它会改模型
- **Correct**: A
- **Explanation**: 长会话中，用 summary 替代大段历史可以减少上下文压力。
- **Review**: 新手最容易忽略的点

### Q8
- **Category**: practical
- **Question**: 哪类任务最适合配合 checkpoints 使用？
- **Options**: A) 高风险重构或多方案试验 | B) 只看天气 | C) 只改桌面图标 | D) 单纯改用户名
- **Correct**: A
- **Explanation**: 高风险或多路线任务最能体现 checkpoint 的价值。
- **Review**: 常见使用场景

### Q9
- **Category**: conceptual
- **Question**: checkpoints 可以替代 git commit 吗？
- **Options**: A) 可以，它更强大 | B) 不可以，它们互补：checkpoints 是 session-scoped 且会过期，git 是永久且可共享的记录 | C) 小项目可以完全替代 | D) 只有单人开发时可以
- **Correct**: B
- **Explanation**: checkpoints 临时、按 session 生效且不能共享；git commits 才是长期、可审计、可协作的记录。实际工作里两者应该配合使用。
- **Review**: checkpoints 和 Git 怎么配合

### Q10
- **Category**: practical
- **Question**: 如果你想比较两个不同实现方案，推荐的 checkpoint workflow 是什么？
- **Options**: A) 开两个完全独立的 session | B) 在方案 A 前打 checkpoint，尝试 A，rewind 回去，再尝试 B，最后比较结果 | C) 只能用 git branch | D) 没有合适办法
- **Correct**: B
- **Explanation**: 常见 branching strategy 是在干净状态打 checkpoint，尝试方案 A 并记录结果，再 rewind 回同一 checkpoint 试方案 B。
- **Review**: 一个很实用的工作流

---

## Lesson 09：Advanced Features（高级功能）

### Q1
- **Category**: conceptual
- **Question**: planning mode 最适合什么任务？
- **Options**: A) 多文件复杂改动或高风险实现 | B) 一个小 typo | C) 只查一个命令拼写 | D) 只看 logo
- **Correct**: A
- **Explanation**: planning mode 适合复杂任务先规划再执行。
- **Review**: planning mode 什么时候该用

### Q2
- **Category**: practical
- **Question**: 进入 planning mode 的一个常见入口是什么？
- **Options**: A) `/plan ...` | B) `/memory` | C) `claude --logo` | D) `npm plan`
- **Correct**: A
- **Explanation**: `/plan` 是最常见入口之一。
- **Review**: planning mode 什么时候该用

### Q3
- **Category**: conceptual
- **Question**: permission modes 为什么重要？
- **Options**: A) 因为它决定 Claude 在本地能做多少事以及自动化边界 | B) 因为它决定 logo 颜色 | C) 因为它决定磁盘大小 | D) 因为它替代 Git
- **Correct**: A
- **Explanation**: 权限模式直接关系到风险控制和自动化强度。
- **Review**: permission modes 怎么理解

### Q4
- **Category**: practical
- **Question**: `claude -p` 在 advanced features 里最关键的意义是什么？
- **Options**: A) 进入脚本和 CI/CD 自动化场景 | B) 改桌面主题 | C) 删除 session | D) 生成 plugin market
- **Correct**: A
- **Explanation**: print mode 是 Claude Code 进入自动化的关键接口。
- **Review**: print mode 为什么重要

### Q5
- **Category**: conceptual
- **Question**: `ultrathink` 在 extended thinking 里更准确的作用是什么？
- **Options**: A) 为当前这一次回答触发更深推理，但不永久改变 session effort | B) 永久把当前 session 改成最高 effort | C) 只在 Opus 4.6 可用 | D) 等价于打开 verbose transcript
- **Correct**: A
- **Explanation**: `ultrathink` 更像给这一轮 prompt 加一个深度推理指令；如果要调整 session 级别思考强度，应使用 `/effort`。
- **Review**: extended thinking

### Q6
- **Category**: practical
- **Question**: 如果你在公司网络环境中使用远程或 web 功能，最该先确认什么？
- **Options**: A) 网络、代理和访问稳定性 | B) 鼠标颜色 | C) Git 提交模板 | D) 显示器亮度
- **Correct**: A
- **Explanation**: 远程、web、desktop 相关能力很依赖网络环境。
- **Review**: 中国用户特别注意

### Q7
- **Category**: conceptual
- **Question**: worktrees 和 sandboxing 分别更偏什么？
- **Options**: A) 前者偏并行分支隔离，后者偏安全限制 | B) 二者都是写博客 | C) 二者都是图像编辑 | D) 前者做音频，后者做视频
- **Correct**: A
- **Explanation**: worktrees 偏并行开发，sandboxing 偏权限与隔离。
- **Review**: worktrees 和 sandboxing

### Q8
- **Category**: practical
- **Question**: 对新手来说，学 advanced features 的更合理顺序是什么？
- **Options**: A) 优先 planning mode、permission modes、print mode、background tasks | B) 先学全部高级特性 | C) 只学 remote | D) 不用学 CLI
- **Correct**: A
- **Explanation**: 这是最容易直接产生价值的一条主线。
- **Review**: 最该先掌握哪几个

### Q9
- **Category**: conceptual
- **Question**: `dontAsk` 和 `bypassPermissions` 两种模式有什么区别？
- **Options**: A) 它们完全一样 | B) `dontAsk` 会自动拒绝未预先批准的请求；`bypassPermissions` 会跳过所有权限检查 | C) `dontAsk` 只用于文件，`bypassPermissions` 只用于命令 | D) `bypassPermissions` 更安全
- **Correct**: B
- **Explanation**: `dontAsk` 默认拒绝不匹配预批准规则的权限请求；`bypassPermissions` 则跳过安全检查，日常使用风险更高。
- **Review**: permission modes（权限模式）

### Q10
- **Category**: practical
- **Question**: 如何把当前 CLI session 交给 desktop app 继续查看？
- **Options**: A) 使用 `/export` command | B) 使用 `/desktop` command | C) 复制 session ID 到 app | D) CLI 和 desktop 之间不能交接 session
- **Correct**: B
- **Explanation**: `/desktop` 会把当前 CLI session 交给原生 desktop app，便于查看视觉 diff 或管理多个 session。
- **Review**: remote / web / desktop（远程 / Web / 桌面）

---

## Lesson 10：CLI（命令行）

### Q1
- **Category**: conceptual
- **Question**: Claude Code CLI 最核心的地位是什么？
- **Options**: A) 是最主要的使用入口，也是自动化基础 | B) 只是装饰功能 | C) 只能看版本号 | D) 只用于图片处理
- **Correct**: A
- **Explanation**: 很多能力最后都要落到 CLI 使用和自动化集成上。
- **Review**: CLI 指南开头

### Q2
- **Category**: practical
- **Question**: 下面哪个命令属于 print mode？
- **Options**: A) `claude -p "explain this error"` | B) `/memory` | C) `/plugin install` | D) `git status`
- **Correct**: A
- **Explanation**: `claude -p` 是 print mode 的常见入口。
- **Review**: 交互模式 vs print mode

### Q3
- **Category**: conceptual
- **Question**: 交互模式和 print mode 的一个关键差别是什么？
- **Options**: A) 前者偏多轮对话，后者偏一次性任务与脚本 | B) 二者完全相同 | C) print mode 不能输出文本 | D) 交互模式不能读文件
- **Correct**: A
- **Explanation**: 这是两种使用模式最核心的差别。
- **Review**: 交互模式 vs print mode

### Q4
- **Category**: practical
- **Question**: 哪个 flag 用于恢复指定 session？
- **Options**: A) `-r, --resume` | B) `--logo` | C) `--theme` | D) `--fast-open`
- **Correct**: A
- **Explanation**: `-r` / `--resume` 用于恢复指定 session。
- **Review**: 新手最该掌握的 flags

### Q5
- **Category**: conceptual
- **Question**: 为什么 CLI 文档里的命令和 flags 不能中文化？
- **Options**: A) 因为它们是可复制执行的真实接口 | B) 因为中文不好看 | C) 因为 Git 不支持中文 | D) 因为 README 不允许
- **Correct**: A
- **Explanation**: CLI 是最典型的“说明文本可以翻，但命令本身不能翻”的内容。
- **Review**: 哪些内容不能翻

### Q6
- **Category**: practical
- **Question**: 哪组 flags 更适合新手优先掌握？
- **Options**: A) `-p`、`-c`、`-r`、`--model`、`--permission-mode` | B) 只学 `--version` | C) 只学 `--logo` | D) 只学 `--color`
- **Correct**: A
- **Explanation**: 这些是最直接影响日常使用效率的一组 flags。
- **Review**: 新手最该掌握的 flags

### Q7
- **Category**: conceptual
- **Question**: CLI 为什么对自动化特别重要？
- **Options**: A) 因为脚本、CI/CD、批处理和结构化输出都依赖它 | B) 因为它会自动帮你写 README | C) 因为它会替代 memory | D) 因为它只能在浏览器里运行
- **Correct**: A
- **Explanation**: 自动化几乎都需要 CLI 入口。
- **Review**: CLI 和自动化的关系

### Q8
- **Category**: practical
- **Question**: Windows 用户使用 CLI 时，最值得先确认什么？
- **Options**: A) 当前是在 PowerShell、Git Bash 还是 WSL 中运行 | B) 键盘布局 | C) 显示器分辨率 | D) 手机型号
- **Correct**: A
- **Explanation**: 这直接关系到命令兼容性与路径行为。
- **Review**: 中国用户特别注意

### Q9
- **Category**: conceptual
- **Question**: 用户已登录时，`claude auth status` 返回什么 exit code？
- **Options**: A) 1 | B) 0 | C) 200 | D) 它不返回 exit code
- **Correct**: B
- **Explanation**: `claude auth status` 在已登录时返回 0，未登录时返回 1，因此适合脚本或 CI/CD 中做认证检查。
- **Review**: 登录状态与 exit code

### Q10
- **Category**: practical
- **Question**: 如果要用 Claude 批量处理多个文件，哪种方式更合适？
- **Options**: A) `claude --batch *.md` | B) 使用 shell for loop：`for file in *.md; do claude -p "summarize: $(cat $file)" > ${file%.md}.json; done` | C) `claude -p --files *.md "summarize all"` | D) Claude 不支持批处理
- **Correct**: B
- **Explanation**: 批处理通常用 shell loop 配合 print mode，一个文件一次独立调用，并可输出结构化结果。
- **Review**: 批量处理文件
