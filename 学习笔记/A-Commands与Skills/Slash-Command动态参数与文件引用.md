# Slash Command 动态参数与文件引用（$ARGUMENTS / $0 / @path / !命令）

> **学习起因**：在 [`学习指南/Claude-Code知识体系全景表.md`](../../学习指南/Claude-Code知识体系全景表.md) 里看到一行知识点 "见到 `$ARGUMENTS`、`$0`、`@path` 时知道它们是动态输入或文件引用"，之前跳过没搞懂，回头补上。
>
> **本文风格**：先提问 → 通俗解释 → 用项目里的真实文件当例子 → 速查表 → 上手练习。

---

## 目录

- [一、这些符号到底是什么](#一这些符号到底是什么)
- [二、`$ARGUMENTS` — 用户传入的全部参数](#二arguments--用户传入的全部参数)
- [三、`$0` / `$1` / `$2` — 按位置拆开的单个参数](#三0--1--2--按位置拆开的单个参数)
- [四、`@path/to/file` — 把文件内容塞进上下文](#四pathtofile--把文件内容塞进上下文)
- [五、`` !`command` `` — 执行 bash 并把输出塞进来](#五command--执行-bash-并把输出塞进来)
- [六、`${CLAUDE_PROJECT_DIR}` 等 — 内置环境变量](#六claude_project_dir-等--内置环境变量)
- [七、速查表](#七速查表)
- [八、练手：一道读懂题](#八练手一道读懂题)
- [九、我做的练手命令：`/review-file`](#九我做的练手命令review-file)

---

## 一、这些符号到底是什么

它们都是 **slash command / skill 的 md 文件里的"占位符"**。你在文件里写它们的时候，它们**不代表自己**；等 Claude Code 真正加载这个命令的时候，会**在把内容喂给模型之前**，把这些占位符**替换成真实的值**。

打个比方：这就像 **Word 里的邮件合并**。你写一份邀请函模板：

```
亲爱的 <收件人姓名>，
请于 <日期> 参加聚会。
```

发信时软件自动把 `<收件人姓名>` 换成"张三"、`<日期>` 换成"2026-07-25"，最终收件人看到的是替换后的完整信件。

`$ARGUMENTS` / `$0` / `@path` 就是 Claude Code 的"邮件合并字段"。

---

## 二、`$ARGUMENTS` — 用户传入的全部参数

### 定义

**用户在斜杠命令后面敲的所有内容，会被整个塞到 `$ARGUMENTS` 里。**

### 拿我自己的 `/git-safe-submit` 举例

[`.claude/commands/git-safe-submit.md`](../../.claude/commands/git-safe-submit.md) 里有这么一行：

```markdown
- 如果用户传了参数 `$ARGUMENTS`，**直接用这个作为提交信息**，跳过自己生成
```

假设我在 Claude Code 里敲：

```
/git-safe-submit docs: 补充参数用法说明
```

Claude Code 会**在加载文件时**做替换：

```
用户传入的参数是: docs: 补充参数用法说明
```

模型看到"哦，用户明确给了 message，直接用这个 commit"。

### 如果用户什么都没传呢？

```
/git-safe-submit
```

`$ARGUMENTS` 就是**空字符串**。命令文件里已经写好了兜底逻辑："否则，请分析改动并生成一条符合 conventional commits 的提交信息" —— 这就是为什么这个命令**传不传参数都能用**。

### 关键点

- `$ARGUMENTS` = **全部**参数（一整段字符串，包括空格）
- 只在 `.claude/commands/*.md` 里生效，普通对话里写 `$ARGUMENTS` 没意义
- Anthropic 把它设计成 shell 环境变量的语法，方便老程序员上手

---

## 三、`$0` / `$1` / `$2` — 按位置拆开的单个参数

### 定义

如果你想**按位置**取参数，用 `$0`、`$1`、`$2`……

- `$0` = **第 1 个**参数（是的，从 0 开始数）
- `$1` = 第 2 个参数
- `$2` = 第 3 个参数

（不同版本 Claude Code 编号起点略有差异，有的从 `$1` 起。能用就行，不纠结。）

### 举例

假设写一个 `.claude/commands/翻译.md`：

```markdown
把下面这段 <$0> 翻译成 <$1>：

$ARGUMENTS
```

用户敲：

```
/翻译 英文 中文 Hello world, how are you?
```

Claude Code 替换后送给模型的内容是：

```
把下面这段 <英文> 翻译成 <中文>：

英文 中文 Hello world, how are you?
```

⚠️ 注意：`$ARGUMENTS` 是**全部**，不是"剩下的"。位置参数只是拆出来的**引用**，不会从原始参数里"消费"掉。

### 什么时候用哪个

| 场景 | 推荐 |
|---|---|
| 用户只传一段自由文本（比如 commit message） | `$ARGUMENTS` |
| 用户传固定几个字段（源语言、目标语言、内容） | `$0` / `$1` / `$2` |
| 想两者都有 | 同一个文件里混用没问题 |

**大部分情况下 `$ARGUMENTS` 就够了。**

---

## 四、`@path/to/file` — 把文件内容塞进上下文

### 定义

在 command / skill 的 body 里写 `@某个文件的相对路径`，Claude Code 会**把那个文件的完整内容读出来，一起送给模型**。

### 项目文档里的原话

[`01-slash-commands/README.md:141`](../../01-slash-commands/README.md) 说：

> 在 command 或 skill 的 prompt 里写 `@path/to/file`，可以把目标文件内容按需带入上下文。适合引用模板、需求文档或局部代码，不必把整份内容复制进 command 文件。

### 实际长什么样

假设写一个 `.claude/commands/审查文档风格.md`：

```markdown
请按 @LOCALIZATION-STYLE.md 里的规则，审查用户当前打开的文档。
```

Claude Code 加载时，会**把 `LOCALIZATION-STYLE.md` 整个文件内容拼进来**，最终送给模型的是：

```
请按 <LOCALIZATION-STYLE.md 的全部内容...> 里的规则，审查用户当前打开的文档。
```

### 好处

- **不用复制粘贴**：规则文件更新了，命令自动跟着更新
- **保持命令文件短小**：命令本身只写"用什么规则做什么事"，规则细节留在原文件

### 常见坑

- **`@` 后面必须是路径**，不能有空格
- **相对路径以项目根为基准**（不是命令文件所在目录）
- 文件太大也会全塞进去，占用 token —— 不要 `@` 一个 10 万行的文件

---

## 五、`` !`command` `` — 执行 bash 并把输出塞进来

### 你可能没意识到，`/git-safe-submit` 里已经用了这个

看 [`.claude/commands/git-safe-submit.md:12-15`](../../.claude/commands/git-safe-submit.md)：

```markdown
- 当前 git 状态：!`git status`
- 当前 diff：!`git diff HEAD`
- 当前分支：!`git branch --show-current`
- 最近提交：!`git log --oneline -10`
```

这个 `` !`command` `` 语法的意思是：**先在你电脑上跑这条 bash 命令，把输出替换到这里**。

### 加载过程

当我敲 `/git-safe-submit`，Claude Code 会：

1. 真的跑一次 `git status`，比如输出 `On branch study-notes\nnothing to commit...`
2. 把这段输出**贴到那一行**
3. 然后才把完整的文件送给模型

这就是为什么它每次都能"知道"当前的 git 状态 —— 不是模型猜的，是**真的执行了命令**。

### 受 `allowed-tools` 管控

命令文件顶部有：

```yaml
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*), Bash(git diff:*), Bash(git branch:*), Bash(git log:*)
```

所以只有 `git add / status / commit / diff / branch / log` 这几个前缀允许执行。写 `` !`rm -rf /` `` 是**不会被执行的**，会直接拒绝。**这是安全边界**。

---

## 六、`${CLAUDE_PROJECT_DIR}` 等 — 内置环境变量

`${大写名字}` 形式的是 Claude Code 内置的**环境变量**。常见的：

| 变量 | 意思 |
|---|---|
| `${CLAUDE_PROJECT_DIR}` | 当前项目的绝对路径（比如 `D:\cc\claude-howto-zh-cn`）|
| `${CLAUDE_SESSION_ID}` | 当前会话 ID |
| `${CLAUDE_SKILL_DIR}` | 当前 skill 的目录（只在 skill 里有意义）|
| `${CLAUDE_EFFORT}` | 当前会话的 effort 等级 |

**啥时候会用到？** 主要是需要跨平台写脚本、或者需要拿到绝对路径去做别的事。**日常写 command 基本用不到**，看到能认出来就够了。

---

## 七、速查表

| 符号 | 含义 | 我会在哪儿见到 |
|---|---|---|
| `$ARGUMENTS` | 用户跟在命令后的**全部**输入 | `/git-safe-submit` 里就用了 |
| `$0` / `$1` / `$2` | 按**位置**取的单个参数 | 需要拆参数的命令，比如翻译类 |
| `@path/to/file` | **注入文件内容**到 prompt | "按 X 文件的规则来做 Y" 这种命令 |
| `` !`command` `` | **执行 bash 命令**，把输出注入 | `/git-safe-submit` 里的 `` !`git status` `` |
| `${CLAUDE_PROJECT_DIR}` | 项目根目录**绝对路径** | 需要跨平台脚本时才用 |

---

## 八、练手：一道读懂题

能读懂下面这段 command 文件吗？

```markdown
---
name: review-file
argument-hint: [file-path]
description: 按项目风格审查某个文件
---

请按 @LOCALIZATION-STYLE.md 的规则，审查这个文件：

$ARGUMENTS

当前 git 分支：!`git branch --show-current`
```

**用户敲**：

```
/review-file 01-slash-commands/README.md
```

**最终喂给模型的是什么？** 脑子里跑一遍：

- `@LOCALIZATION-STYLE.md` → 被替换成那个文件的完整内容
- `$ARGUMENTS` → 被替换成 `01-slash-commands/README.md` 这一串字符
- `` !`git branch --show-current` `` → 真的跑 bash 命令，输出（比如 `study-notes`）被替换进去

送给模型的最终内容大概是：

```
请按 [LOCALIZATION-STYLE.md 的完整正文...] 的规则，审查这个文件：

01-slash-commands/README.md

当前 git 分支：study-notes
```

模型看到这个 prompt，就明白"哦，用户要我按那份风格规则审查 `01-slash-commands/README.md`，而且当前在 study-notes 分支"。

**能理清这个替换过程，就彻底学会这一节了。**

---

## 九、我做的练手命令：`/review-file`

真的动手做了一个 —— 见 [`.claude/commands/review-file.md`](../../.claude/commands/review-file.md)。

这个命令一次性用到了**四种占位符**：

- `$ARGUMENTS` —— 接收用户传入的文件路径
- `@LOCALIZATION-STYLE.md` —— 把项目风格规则塞进 prompt
- `` !`command` `` —— 读取当前分支、当前 git 状态
- `${CLAUDE_PROJECT_DIR}` —— 展示项目根路径

用法：

```
/review-file 01-slash-commands/README.md
```

Claude 会拿着"项目风格规则"审查我指定的这个文件，并给出反馈。

**动手做完 + 真正跑一次 = 印象最深**。这就是这一节的完整闭环。

---

## 相关笔记

- [Commands 与 Skills：从快捷命令到可复用工作流](./Commands与Skills-从快捷命令到可复用工作流.md)
- [Claude Code 手动创建 git-safe-submit Skill](./Claude-Code-手动创建git-safe-submit-Skill.md)
