<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../resources/logos/claude-howto-logo-dark.svg">
  <img alt="Claude How To" src="../resources/logos/claude-howto-logo.svg">
</picture>

# Memory 指南

memory 是 Claude Code 中最容易被低估的一项能力。很多人觉得自己只是“加了个 `CLAUDE.md`”，实际上它影响的是 Claude 在每次进入项目时会自动带上的长期上下文。

---

## memory 是什么

Claude Code 的 memory 主要依赖文件系统中的 `CLAUDE.md` 体系。你可以把它理解成：

- 项目规则入口
- 团队约定入口
- 个人偏好入口
- 某个目录下的局部规则入口

它和“当前对话里的临时上下文”不同，memory 更像是长期生效的规则层。

---

## 什么时候最该先配 memory

以下情况非常值得先配 `CLAUDE.md`：

- 你每次都要重复告诉 Claude 代码风格
- 团队里有固定约定，例如测试要求、命名规范、Git 流程
- 项目目录复杂，希望 Claude 一进来就知道哪些目录干什么
- 你想把一部分项目知识长期保存下来，而不是每次重新解释

---

## 高价值命令

| 命令 / 写法 | 用途 |
|-------------|------|
| `/init` | 初始化项目 memory |
| `/memory` | 查看或编辑 memory |
| 自然语言告诉 Claude“记住这条规则” | 让 Claude 帮你更新合适的 memory |
| `@README.md` | 在 `CLAUDE.md` 中引用外部文档 |

---

## April 2026 这批 memory 更新，最值得知道什么

- `/init` 的增强交互模式，推荐写法从 `CLAUDE_CODE_NEW_INIT=true` 逐步统一到了 `CLAUDE_CODE_NEW_INIT=1`
- `CLAUDE.local.md` 现在已经是官方文档里明确支持的个人项目记忆，不再只是“可能还能用的旧特性”
- auto memory 在会话开始时会加载 `MEMORY.md` 的前 200 行，**或者前 25KB**，以先到者为准
- auto memory 默认开启，可用 `autoMemoryEnabled`、`/memory` 或 `CLAUDE_CODE_DISABLE_AUTO_MEMORY` 控制
- subagents 也可以拥有自己的 auto memory，适合长期复杂项目
- 旧教程里常见的 `# ...` inline memory 快捷写法已经停用；现在请改用 `/memory` 或直接用自然语言让 Claude 记住

如果你是中国用户，这几条很重要，因为网上很多旧教程还停留在更早的说法。

---

## 最快上手方式

### 方法 1：直接复制项目模板

```bash
cp 02-memory/project-CLAUDE.md ./CLAUDE.md
```

### 方法 2：让 Claude 帮你初始化

```bash
CLAUDE_CODE_NEW_INIT=1 claude
/init
```

这通常适合新项目起步时使用。

### 方法 3：直接打开 `/memory` 编辑

```bash
/memory
```

这会直接打开 memory 文件，让你手工改最稳。

从 `v2.1.216+` 起，如果系统用 GUI editor 打开文件，当前 session 不会一直等到编辑器关闭，你可以并行继续工作；Vim 等 terminal editor 仍会占用终端，直到退出编辑器。

### 方法 4：直接用自然语言告诉 Claude 要记住什么

```text
记住：这个项目提交前总是先跑测试。
请加到 memory：优先用 async/await，不要堆 promise chain。
```

Claude 会根据你的描述，把内容写进合适的 `CLAUDE.md`。

> 旧资料里如果还在教你用 `# Always run tests before commit` 这种前缀写法，可以直接把它视为历史写法。现在请改用 `/memory` 或自然语言更新 memory。

---

## 用 `@` 导入外部文档

`CLAUDE.md` 支持用 `@path/to/file` 引用已有文档，避免把同一份项目说明复制多遍：

```markdown
项目概览见 @README.md
架构约定见 @docs/architecture.md
个人补充说明见 @~/.claude/my-project-instructions.md
```

- 相对路径以包含这条 import 的文件为基准，不是以启动 Claude Code 的工作目录为基准。
- import 可以递归，但最多允许 **4 hops**。
- 第一次导入外部位置时会弹出 approval dialog，确认来源后再继续。
- Markdown code span 和 code block 里的 `@path` 只是示例，不会被执行为 import。
- import 只是在文件层面拆分内容，加载时仍会占用上下文；真正想按任务减小加载量，应使用带 `paths` frontmatter 的 `.claude/rules/*.md` 或按需 skill。

### 已有 `AGENTS.md` 怎么办

`AGENTS.md` 是跨工具共享项目上下文的约定，不是 Claude Code 的 subagent 定义文件。Claude Code 不会自动读取它；需要复用时，在 `CLAUDE.md` 中写 `@AGENTS.md`，或把 `CLAUDE.md` 做成指向它的 symlink。真正的 subagent 定义仍放在 `.claude/agents/`。

---

## 常见 memory 类型

### 项目级 memory

位置通常是：

- `./CLAUDE.md`
- 或 `.claude/CLAUDE.md`

适合放：

- 项目背景
- 目录结构
- 技术栈
- 代码规范
- 测试规则
- 提交和 PR 规范

### 个人级 memory

位置通常是：

- `~/.claude/CLAUDE.md`

适合放：

- 你的个人编码偏好
- 你习惯的回答风格
- 常用工具和命令约定

如果你希望“这个偏好只对当前项目有效，但又不想提交进 Git”，也可以考虑 `./CLAUDE.local.md`。

### 目录级 memory

适合大型项目或 monorepo，在局部目录下放更细粒度规则。目录中的 `CLAUDE.md` 会在访问该目录时补充根目录规则；多个文件会拼接，不是由子目录整份覆盖根目录。

---

## 两套 memory 机制与 CLAUDE.md 加载顺序

Claude Code 有两套互补机制：你维护的 `CLAUDE.md` 指令，以及 Claude 自己维护的 auto memory。两者都会在对话开始时加载，但不能混成一条“高层覆盖低层”的严格优先级链。

`CLAUDE.md` 文件按作用范围从宽到窄加载：

| 范围 | 位置 | 用途 |
|------|------|------|
| Managed policy | macOS `/Library/Application Support/ClaudeCode/CLAUDE.md`、Linux/WSL `/etc/claude-code/CLAUDE.md`、Windows `C:\Program Files\ClaudeCode\CLAUDE.md` | 组织统一指令 |
| User instructions | `~/.claude/CLAUDE.md` | 个人跨项目偏好 |
| Project instructions | `./CLAUDE.md` 或 `./.claude/CLAUDE.md` | 团队共享的项目约定 |
| Local instructions | `./CLAUDE.local.md` | 不提交到 Git 的个人项目偏好 |

这些文件会**拼接**进上下文，而不是由后一层把前一层整份覆盖。Claude Code 会从工作目录向上查找；同一目录中的 `CLAUDE.local.md` 接在 `CLAUDE.md` 后面。工作目录下更深层的文件则在 Claude 读取对应子目录时按需加载。

`.claude/rules/*.md` 是另一套相关的模块化规则机制，可以通过 `paths` frontmatter 按路径生效。auto memory 位于 `~/.claude/projects/<project>/memory/`，保存 Claude 自己整理的笔记，也不参与上面的 CLAUDE.md 拼接顺序。

组织还可以在 managed settings 中通过 `claudeMd` 写入托管指令；这个 key 放到用户或项目 settings 中不会生效。大型 monorepo 可以用 `claudeMdExcludes` 排除无关的 CLAUDE.md 文件，但不能排除 managed policy。

## 用 --add-dir 加载额外目录

monorepo 或多仓库协作时，可以让当前 session 同时读取额外目录中的 `CLAUDE.md`：

```bash
export CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1
claude --add-dir /path/to/other/project
```

`--add-dir` 和 `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD` 都是可执行标识，不要翻译。额外目录中的 CLAUDE.md 会和当前项目的 memory 一起加载，用于补充上下文。

---

## 写什么最有价值

新手最容易把 `CLAUDE.md` 写成“泛泛而谈的项目介绍”，这价值并不大。更推荐写这些：

- 哪些目录最重要
- 哪些规则最容易被忽略
- 提交前必须做什么
- 哪些工具是本项目默认用法
- 哪些文件不要乱动
- 测试和验证的最低标准

---

## 一个适合小白的最小模板

```md
# 项目记忆

## 项目概览
- 这是一个 TypeScript Web 应用。

## 开发规则
- 提交前先运行测试。
- 优先使用 async/await。
- API 变更必须同步更新文档。

## 重要路径
- `src/` 主要应用代码
- `tests/` 自动化测试
- `docs/` 文档
```

---

## 哪些内容不适合写进 memory

- 过长、每次都不一定相关的大段背景知识
- 会频繁变化的实时数据
- 明显更适合做成 skill 或 hook 的工作流细节
- 会影响运行的命令名或配置 key 的中文重命名

如果你发现某段内容更像“流程模板”，通常更适合去做 skill，而不是塞进 `CLAUDE.md`。

---

## 关于 auto memory，再多记两件事

### 0. 默认开启，但可以明确控制

auto memory 默认开启。可在 settings 中设置：

```json
{
  "autoMemoryEnabled": false
}
```

也可以在当前 session 用 `/memory` 切换。环境变量 `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` 会关闭 auto memory；设为 `0` 则会强制开启，即使 `--bare` 或 `autoMemoryEnabled: false` 原本会关闭它。这里的 key 和环境变量都不能翻译。

### 1. 启动时不是整份都加载

Claude Code 不会把整个 auto memory 目录一次性全塞进上下文。最先进入上下文的是 `MEMORY.md` 的前 200 行或前 25KB，其余 topic files 按需加载。

从 `v2.1.214+` 起，auto memory 文件如果以 YAML frontmatter 开头，Claude Code 每次写入时会自动维护 ISO 8601 格式的 `modified` 字段。`modified` 是协议字段，不要翻译或手工改名。

### 2. 它不是手工 `CLAUDE.md` 的替代品

- `CLAUDE.md` 更适合明确规则
- auto memory 更适合 Claude 在长期使用中自己沉淀项目知识

二者搭配使用效果最好。

---

## 中国用户特别注意

- 如果你在 Windows 上工作，路径规则和 shell 说明最好明确写清楚。
- 如果项目依赖 `uv`、`npm`、`pnpm`、`bun` 等特定工具，也建议写入 memory。
- 如果项目所在团队有 GitHub、内网、代理、镜像源要求，也值得写在 memory 里。

---

## 这轮 settings 更新里，最值得知道什么

### 1. `/config` 现在会真正落盘

上游在 `v2.1.119` 明确了一个很关键的行为：

- 你在 `/config` 里改的设置
- 现在会写入 `~/.claude/settings.json`
- 并参与正常的 policy / local / project / user 优先级链

对中国用户来说，这意味着：

- `/config` 不再只是“当前会话临时切一下”
- 你改完之后，后续 session 很可能会继承这些设置
- 如果团队里有统一 managed policy，要注意最终谁覆盖谁

当前更准确的 settings 优先级顺序是：

1. managed policy / `managed-settings.json`
2. 命令行参数
3. `.claude/settings.local.json`（本地覆盖，通常不提交）
4. `.claude/settings.json`（项目级，通常提交）
5. `~/.claude/settings.json`（用户级偏好）

这点容易和旧资料混淆：本地项目覆盖项 `.claude/settings.local.json` 的优先级高于项目级 `.claude/settings.json`，也高于用户级 `~/.claude/settings.json`。

`managed-settings.d/` 是 managed settings 的 JSON drop-in 目录，不是 memory 层。它会在基础 `managed-settings.json` 之后按文件名字母顺序合并 `*.json`；普通标量覆盖、数组拼接并去重、对象深度合并。另一个例外是 permission rules：`allow` / `ask` / `deny` 会跨 scope 合并，而不是简单由高优先级整项替换。

### 2. `cleanupPeriodDays` 不只是管 checkpoints

以前很多人会把它理解成“checkpoint 保留几天”。<br>
现在更准确的理解是：它统一控制 4 类本地缓存的保留周期：

- checkpoints
- `~/.claude/tasks/`
- `~/.claude/shell-snapshots/`
- `~/.claude/backups/`

也就是说，你调这个值时，影响的不只是 rewind 历史，还包括任务、shell 快照和备份清理。

### 3. 几个设置项换了更明确的写法

上游现在更推荐这些新写法：

- `attribution.commit`
- `attribution.pr`
- `attribution.sessionUrl`
- `voice.enabled`
- `prUrlTemplate`

其中 `attribution.sessionUrl` 是 `v2.1.183+` 新增的细分项，用来在 web / Remote Control session 创建 commit 或 PR 时省略 `claude.ai` session 链接。它只是 settings key，不要翻译成中文字段。

如果你还在旧资料里看到：

- `includeCoAuthoredBy`
- `voiceEnabled`

把它们视为旧名字即可。新项目和新文档尽量按新版写。

---

## 常见坑

### 1. 以为 memory 越长越好

不是。memory 要优先放高价值、长期稳定、对 Claude 行为影响大的规则。当前官方建议把单个 `CLAUDE.md` 目标控制在 **200 行以内**；更长的文件仍会完整加载，但指令遵循度会下降。多步骤流程移到 skill，路径规则移到 `.claude/rules/*.md`，长参考资料放到 skill 的 `references/`。

对 Opus 5 和 Fable 5，不要机械堆叠“完成前再检查一次”这类泛化提醒，以免反复验证消耗回合；但项目真正依赖的验收条件仍应明确保留，例如“集成测试需要 Docker”。

### 2. 把项目规则和个人偏好全混在一起

推荐区分项目级和个人级，这样更方便团队协作。

### 3. 让 `CLAUDE.md` 和实际仓库脱节

如果项目目录或规范已经变了，要及时更新 memory，否则 Claude 会学到过期规则。

### 4. 还在把 `CLAUDE.local.md` 当“灰色特性”

现在不需要了。它已经是正式支持的个人项目记忆文件；唯一要注意的是把它加进 `.gitignore`。

---

## 推荐下一步

- 想做可复用工作流：看 [03-skills](../03-skills/)
- 想安全试错：看 [08-checkpoints](../08-checkpoints/)
- 想看完整学习顺序：看 [LEARNING-ROADMAP.md](../LEARNING-ROADMAP.md)
