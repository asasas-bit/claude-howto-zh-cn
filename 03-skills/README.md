<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../resources/logos/claude-howto-logo-dark.svg">
  <img alt="Claude How To" src="../resources/logos/claude-howto-logo.svg">
</picture>

# Skills 指南

skills 是 Claude Code 里最值得认真掌握的能力之一。它们让 Claude 不再只是“每次重新听你描述要求”，而是能在合适场景下自动拿出一套固定工作流、模板和最佳实践。

---

## skills 是什么

你可以把 skill 理解成：

- 一个带 frontmatter 的 `SKILL.md`
- 可附带脚本、模板、参考资料
- 会被 Claude 自动发现和按需加载
- 更适合长期复用的工作流能力

和普通 prompt 相比，skills 更稳定、更易复用，也更适合团队共享。

---

## skills 为什么重要

当你开始频繁做这些事时，skills 的价值就非常明显：

- 代码审查
- 文档生成
- 代码重构
- 品牌语气统一
- 项目初始化或规范生成

如果每次都靠你手打一大段提示词，既累，也不稳定。skill 的目标就是把这部分沉淀下来。

---

## 一个 skill 的基本结构

```text
skill-name/
├── SKILL.md
├── templates/
├── scripts/
└── references/
```

### `SKILL.md` 负责什么

- 定义 skill 名称
- 说明 skill 在什么情况下应该触发
- 告诉 Claude 该怎么做

### 其他目录负责什么

- `templates/`：输出模板
- `scripts/`：辅助脚本
- `references/`：参考规则或背景知识

---

## 当前 skills 更新，最值得知道什么

- skill description 的预算更紧了：默认只占上下文窗口的 **1%**，fallback 约 **8,000 字符**
- 即使装了很多 skills，**skill 名称会保留**，description 则会被裁短
- 如果你希望某个 skill 只在某些路径下自动触发，可以在 frontmatter 里加 `paths`
- 写 description 时要把“最关键的使用场景”放前面，否则容易在预算裁剪时丢失重点
- `effort` 可用值需要看模型能力；Opus 5、Sonnet 5、Opus 4.8、Opus 4.7 支持 `low` / `medium` / `high` / `xhigh` / `max`，除 Opus 4.7 默认 `xhigh` 外，其余默认 `high`
- skill 内容里可以使用 `${CLAUDE_EFFORT}` 获取当前 effort level，适合根据思考强度分支执行不同流程
- `/skills` 交互菜单支持直接输入过滤，装了很多 skills 时更容易定位
- Claude Code 现在内置一组 bundled skills，其中 `/run`、`/verify`、`/run-skill-generator` 很适合做“代码真的跑起来了吗”的端到端验证
- `/reload-skills` 可以在不重启 session 的情况下重新扫描 skill 目录；`SessionStart` hook 也可以通过返回 `reloadSkills: true` 触发同样行为
- skill frontmatter 现在可以写 `disallowed-tools`，用于在 skill 生效期间移除某些工具权限
- `/simplify` 在 `v2.1.154+` 后重新成为独立的清理型命令；`/code-review` 继续负责正确性缺陷审查
- `/code-review` 和 `/verify` 从 `v2.1.215+` 起只会在用户显式调用时运行；`/deep-research` 从 `v2.1.218+` 起也只允许显式调用
- `/code-review` 从 `v2.1.218+` 起在后台 subagent 中运行，不占满主对话，叠加 slash-skills 时仍以组合后的请求为审查目标
- `context: fork` skills 从 `v2.1.218+` 起默认 `background: true`；需要前台运行时写 `background: false`
- frontmatter boolean 从 `v2.1.218+` 起除 `true` / `false` 外，也接受不区分大小写的 `yes` / `no`、`on` / `off`、`1` / `0`
- 如果你写了 `context: fork` 的 skill，建议升级到 `v2.1.145+`；上游修复了少数场景下可能无限重新调用的问题

---

## progressive disclosure 是什么意思

skills 的一个核心优点是按需加载，而不是一上来把所有内容都塞进上下文里。

简单理解：

1. Claude 先只知道有哪些 skills，以及它们大概干什么
2. 真正需要某个 skill 时，再读取 `SKILL.md`
3. 只有在需要时，才进一步读模板、脚本或参考资料

这意味着你可以装很多 skills，而不会一开始就把上下文塞爆。

上游这次还顺手把技能加载流程图的分层写得更清楚了。现在更推荐这样理解：

- 第 1 层：先看 skill 名称和 description
- 第 2 层：真正命中时再读 `SKILL.md`
- 第 3 层：只有确实需要时，才继续读 `templates/`、`scripts/`、`references/`

这个分层对中文用户特别重要，因为它能解释一个常见疑问：

- 为什么我装了很多 skills，但 Claude 不会一上来全读？

答案就是：Claude 默认按层加载，而不是整包吞下。

---

## skill 类型、位置与优先级

| 类型 | 路径 | 适合什么 |
|------|------|----------|
| 个人级 | `~/.claude/skills/<skill-name>/SKILL.md` | 个人工作流 |
| 项目级 | `.claude/skills/<skill-name>/SKILL.md` | 团队共享 |
| plugin 自带 | `<plugin>/skills/...` | 和 plugin 一起分发 |

同名 skill 的优先级按 **Enterprise > Project > Personal** 理解；项目 skill 默认覆盖个人同名 skill。plugin 提供的 skill 带 namespace，避免和普通 skill 名称冲突。`skillOverrides` 用来调整 skill 的可见性和调用行为，见后文。

---

## 本目录里的示例 skills

| skill | 位置 | 用途 |
|-------|------|------|
| `code-review-specialist` | `03-skills/code-review-specialist/` | 代码审查；保留 `-specialist` 后缀，避免遮蔽 Claude Code 内置 `/code-review` |
| `brand-voice` | `03-skills/brand-voice/` | 文案风格统一 |
| `doc-generator` | `03-skills/doc-generator/` | 文档生成 |
| `refactor` | `03-skills/refactor/` | 结构化重构 |
| `claude-md` | `03-skills/claude-md/` | 生成或调整 `CLAUDE.md` |

---

## Claude Code 自带的 bundled skills

这些 skills 随 Claude Code 一起提供，不需要从本仓库复制安装。它们依然通过 slash command 形式调用，所以名称不要翻译：

| skill | 适合什么时候用 |
|-------|----------------|
| `/batch` | 同一类改动要批量作用到很多文件时 |
| `/claude-api` | 项目里用到 Anthropic / Claude API 或 SDK，需要加载参考资料时 |
| `/dataviz` | 需要设计图表、dashboard 或校验调色板时（`v2.1.198+`） |
| `/debug` | 当前 session 出错，需要读取 debug log 定位原因时 |
| `/deep-research <topic>` | 需要深入研究指定主题时；`v2.1.218+` 起必须显式调用 |
| `/fewer-permission-prompts` | 想减少反复弹出的只读权限确认时 |
| `/loop` | 需要按固定间隔重复执行一个 prompt 时 |
| `/run` | 改完后要启动项目，确认应用真实跑起来时 |
| `/run-skill-generator` | 第一次让 Claude 学会这个项目该怎么 `/run` / `/verify` 时 |
| `/code-review [effort]` | 想让 Claude 审查当前 diff 的正确性缺陷时；`v2.1.215+` 起必须显式调用，`v2.1.218+` 起在后台 subagent 中运行 |
| `/simplify` | 想做复用、简化、效率和抽象层级相关的清理型审查，并让 Claude 应用修复时 |
| `/verify` | 不只跑测试，还要构建、运行并观察修复是否真的生效时；`v2.1.215+` 起必须显式调用 |

对中文用户来说，`/verify` 的价值很高：它把“测试通过”和“用户实际能用”分开看，能减少本地看似成功、线上或真实应用仍出错的问题。

### 动态值与项目目录

skill body 和 `allowed-tools` 都可以使用 `${CLAUDE_PROJECT_DIR}`，它会在运行时解析为项目根目录的绝对路径（`v2.1.196+`）。常用动态值还包括 `$ARGUMENTS`、`$0`、`${CLAUDE_SESSION_ID}`、`${CLAUDE_SKILL_DIR}` 和 `${CLAUDE_EFFORT}`。

### 叠加多个 skills

从 `v2.1.199+` 起，一次调用可以连续写多个位于开头的 slash-skills，例如：

```text
/code-review /fix-issue 123
```

Claude Code 会加载第一个 skill，再加载最多 5 个额外 skill，并把后面的参数传给每一个。`v2.1.202+` 起，同一个 skill 重复出现时会去重，不会把相同内容重复塞进上下文。

---

## 如何安装

### 安装到个人目录

```bash
mkdir -p ~/.claude/skills
cp -r 03-skills/code-review-specialist ~/.claude/skills/
```

### 安装到项目目录

```bash
mkdir -p .claude/skills
cp -r 03-skills/code-review-specialist .claude/skills/
```

> 注意：本仓库的示例 skill 叫 `code-review-specialist`。如果你把它改回 `code-review`，它可能会遮蔽新版 Claude Code 自带的 `/code-review`，导致你以为在用内置审查命令，实际触发的是本地 skill。

---

## `SKILL.md` 里哪些不能翻

这点是本地化时最容易翻坏的地方。下面这些字段要保留原样：

- `name`
- `description`
- `effort`
- `shell`
- `paths`
- `allowed-tools`
- `disallowed-tools`
- `context`
- `agent`
- `background`
- `reloadSkills`
- `${CLAUDE_EFFORT}`
- `${CLAUDE_PROJECT_DIR}`

同时，skill 名称本身也不要擅自中文化改名。

### `paths` 是什么

这是新版里很实用的一个 frontmatter 字段，用来限制 skill 只在某些目录或文件模式下触发，例如：

```yaml
paths: "src/api/**/*.ts"
```

如果你已经开始做团队级 skills，这个字段很值得用。

## 控制 skill 的调用方式

常见 frontmatter 控制项：

- `disable-model-invocation: true`：禁止模型自动调用，但仍允许用户从 `/` 菜单手动触发
- `user-invocable: false`：不在用户可调用列表中展示，保留给模型按场景调用
- `context: fork`：在 forked context 中运行，可配合 `agent` 指定 subagent；`v2.1.218+` 默认后台运行
- `background: false`：只对 `context: fork` 有意义；显式改为前台运行

这些 key 会直接影响加载和调用行为，说明可以中文化，key 不能翻译。

boolean 字段可以写 `true` / `false`，`v2.1.218+` 也接受不区分大小写的 `yes` / `no`、`on` / `off`、`1` / `0`。团队项目仍建议统一一种写法，减少审阅歧义。

---

## skills 和 slash commands 的区别

### 更适合用 skill 的情况

- 你希望 Claude 自动判断什么时候该触发
- 你需要附带模板、脚本、参考资料
- 这是一个长期工作流，而不是一次性快捷命令

### 更适合用 slash command 的情况

- 你希望自己手动明确触发
- 它更像一个短促的操作入口
- 你希望用户一眼知道“我要输入哪个命令”

---

## 如何写出更好用的 skill

- `description` 要具体，不要空泛
- 一个 skill 聚焦一类问题，别做成“大杂烩”
- 如果依赖脚本或模板，放进 skill 目录，不要散落各处
- 优先写“什么时候触发”和“输出长什么样”

---

## 常见坑

### 1. description 写得太泛

Claude 就不知道什么时候该用它，或者会误触发。

### 2. 把 skill 写成一大段散文

推荐写成结构化说明，让 Claude 更容易执行。

### 3. 把 frontmatter key 翻译掉

这会直接让 skill 无法正确解析。

### 4. description 把重点写在后面

现在 description 预算更紧，Claude 可能先看到的是前半句。最该写在前面的，是“什么时候调用它”。

---

## 中国用户特别注意

- skill 里如果调用 shell 脚本，先确认本机 shell 环境。
- 如果脚本依赖 `python`、`node`、`uv`、`npm`，建议在 skill 说明里提前写明。
- Windows 用户优先考虑 PowerShell / Git Bash / WSL 差异。

---

## 新增的安全护栏：禁用 skill 里的 shell 替换

skill 里支持 ``!`command` `` 这种写法：Claude 在真正读取 skill 前，会先执行 shell 命令，把输出拼进 prompt。

这很强，但在更敏感的环境里也会带来风险。上游现在给了一个更明确的总开关：

```json
{
  "disableSkillShellExecution": true
}
```

开启后：

- ``!`command` `` 不再执行
- 会被当作普通文本保留
- skill 还能继续用，但少了一层 shell 注入面

如果你是在团队、CI 或更受控的环境里推广 skills，这个设置很值得知道。

### 隐藏内置 skills：`disableBundledSkills`

从 `v2.1.169+` 开始，可以用 `disableBundledSkills` 隐藏 Claude Code 自带的 bundled skills、workflows 和 commands：

```json
{
  "disableBundledSkills": true
}
```

等价的环境变量写法是：

```bash
export CLAUDE_CODE_DISABLE_BUNDLED_SKILLS=1
```

它适合两类场景：一是团队想让模型只看项目自己沉淀的 skills；二是你在排查“为什么 Claude 总想调用某个内置能力”。这个 key 和环境变量都不要翻译。

---

## `skillOverrides`：控制 skill 可见性

从 `v2.1.129+` 开始，可以用 `skillOverrides` 隐藏或收缩某个 skill 的展示信息，而不修改它自己的 `SKILL.md`。`/skills` 菜单会把选择写入 `.claude/settings.local.json`：

```json
{
  "skillOverrides": {
    "legacy-context": "name-only",
    "deploy": "off"
  }
}
```

每个 skill 名对应一种状态：

- `"on"`：向 Claude 展示名称和 description，也出现在 `/` 菜单
- `"name-only"`：只向 Claude 展示名称，仍出现在 `/` 菜单
- `"user-invocable-only"`：不向 Claude 展示，但仍允许用户从 `/` 菜单手动调用
- `"off"`：不向 Claude 展示，也不出现在 `/` 菜单

未出现在 `skillOverrides` 中的 skill 按 `"on"` 处理。plugin skills 不受这个设置影响，应通过 `/plugin` 管理。来源冲突仍遵循 Enterprise > Project > Personal。

---

## 推荐下一步

- 想让任务分工更专业：看 [04-subagents](../04-subagents/)
- 想在工具调用前后做自动动作：看 [06-hooks](../06-hooks/)
- 想继续用中文规范扩写：看 [LOCALIZATION-STYLE.md](../LOCALIZATION-STYLE.md)
