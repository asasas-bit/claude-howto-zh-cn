---
name: review-file
allowed-tools: Bash(git branch:*), Bash(git status:*), Bash(git log:*)
argument-hint: <file-path>
description: 按项目本地化风格审查指定的文件（一次性练手：$ARGUMENTS + @path + !command + ${CLAUDE_PROJECT_DIR}）
---

/ 这个command的命令，是一个纠正翻译的命令。是针对这个Claude-howto-zh-cn，因为考虑到翻译过程中，会把一些【占位符】（eg：$ARGUMENTS、$0/$1、@path/to/file、!`command`、${CLAUDE_PROJECT_DIR}等翻译成中文，导致占位符失效，所以加了一个这个审核命令。

/ 这个是在学习【占位符】的时候，AI给加上的一个command命令，但实际上自己用不到，因为不用翻译，但感觉挺好，就保留了。

/ 其实也挺有参考意义，比如自己翻译内容的时候，就可以借鉴这种写法。

# Review File / 审查指定文件（练手命令）

> 这个命令是学习"slash command 占位符"时做的练手作品。同时用到 4 种动态注入方式，
> 详见笔记：[学习笔记/A-Commands与Skills/Slash-Command动态参数与文件引用.md](../../学习笔记/A-Commands与Skills/Slash-Command动态参数与文件引用.md)

## 项目上下文（会被 Claude Code 自动替换后再送给模型）

- 项目根目录：`${CLAUDE_PROJECT_DIR}`
- 当前分支：!`git branch --show-current`
- 当前 git 状态摘要：!`git status --short`
- 最近 3 次提交：!`git log --oneline -3`

## 项目本地化风格规则

以下内容会由 Claude Code 在加载时把 `LOCALIZATION-STYLE.md` 整个文件塞进来：

@LOCALIZATION-STYLE.md

## 用户想审查的文件

用户传入的参数（应该是一个仓库内的相对路径）：

```
$ARGUMENTS
```

## 你的任务

按上面这份**项目本地化风格规则**，审查用户指定的这个文件。审查时请遵守下面几点：

1. **先确认文件是否存在**。如果 `$ARGUMENTS` 为空，或者路径对不上任何文件，直接告诉用户"请传入一个仓库内的文件相对路径"，然后停下，不要瞎猜。
2. **只读，不改**。这个命令是审查性质的，不要执行 Edit / Write。审查完把发现的问题列出来即可，用户会决定是否修改。
3. **按下面这个格式输出**：

```
📄 审查目标：<文件相对路径>
🌿 当前分支：<从上面读到的分支>

──────────────────────────────
🔎 发现的问题（按严重程度排序）

1. [严重] xxxxxx
   - 位置：第 12 行
   - 说明：违反了 LOCALIZATION-STYLE 里 "不要翻译 CLI flags" 的规定
   - 建议：把 "命令行参数" 改回 "CLI flags"

2. [一般] xxxxxx
   ...

──────────────────────────────
✅ 做得好的地方（可选，1-3 条）

- 术语保留恰当
- 中文表达自然，不生硬

──────────────────────────────
📌 总体判断

<一句话结论：可以合并 / 需要小改 / 需要大改>
```

4. 如果文件**没有**明显问题，直接给出简短的通过说明，不要硬凑问题。
5. 只关注**本地化风格**层面的问题（术语保留、翻译腔、frontmatter key 未被误翻等），不要越界去评审代码逻辑或文档结构。

## 学习提示（这段可以由 Claude 忽略，是给我自己看的）

这个命令刻意在一个文件里同时用了：

- `$ARGUMENTS` → 接文件路径
- `@LOCALIZATION-STYLE.md` → 注入规则文件全文
- `` !`git branch --show-current` `` 等 → 执行 bash 命令注入 git 状态
- `${CLAUDE_PROJECT_DIR}` → 内置环境变量

跑一次这个命令，看看它输出的判断结果是否合理，就能验证"这些占位符真的被替换了"。
