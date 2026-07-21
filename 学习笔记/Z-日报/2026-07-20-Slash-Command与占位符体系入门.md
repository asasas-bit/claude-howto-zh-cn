# 📅 2026-07-20 学习日报

🌿 分支：study-notes

---

## 🎯 今天主要学了这几件事

1. **自定义 slash command 从零到一**
   → 亲手写出了 `git-safe-submit`、`review-file`、`today` 三个命令，跑通了"预演→确认→执行"的安全交互套路。

2. **手动搭 Skill 的完整流程**
   → 把 `git-safe-submit` 也做成了 Skill，弄清楚了 frontmatter 里 `name` 字段的作用，以及 Skill 和 Command 的分工。

3. **占位符体系的全景梳理**
   → 一口气写了 700 多行的《占位符如何贯穿 Claude Code 全体系》，把 `$ARGUMENTS`、`!`bash``、`@file`、`{{var}}` 这些散落在各处的写法串成了一条线。

4. **学习笔记目录结构重组**
   → 把原本堆在根目录的 Commands/Skills 笔记归类进 `A-Commands与Skills/`，新开了 `B-占位符全景/`、`Z-日报/` 分区，长期看更好翻。

---

## 💡 关键收获（今天最值钱的三个知识点）

### slash command 的三段式安全模板
写 `git-safe-submit` 的时候悟到：所有涉及副作用的命令，最好都长这样——
**第 1 段用 `!`git status`` 之类的只读命令把现状注入 prompt**，
**第 2 段让 Claude 生成"我准备做 XX"的预演文案**，
**第 3 段必须等用户显式确认才执行**。
这套模板复用性极高，后面写 `today` 的时候直接套用（虽然 today 无副作用，但"先展示再动手"的节奏是一样的）。

### frontmatter 里 `name` 字段不是装饰
之前以为 Skill 的 `name` 只是给人看的，今天实测发现它其实是 Claude Code **识别和调用这个 Skill 的唯一凭据**——文件夹名可以随便叫，但 `name` 必须和你想让 Claude 记住的名字一致，否则 `/skill xxx` 根本调不到。这个坑踩过一次就不会再踩。

### 占位符是 Claude Code 的"胶水"
今天把 slash command 里的 `$ARGUMENTS`、`` !`cmd` `` bash 注入、`@path/file` 文件引用、Skill 里的 `{{variable}}` 全部对比着写了一遍，发现它们本质是**同一种思路的不同变体**：都是"先把外部信息塞进 prompt，再让 Claude 基于完整上下文回答"。理解了这一层，以后写 hooks、MCP 甚至 subagents 时对"数据怎么流"就有直觉了。

---

## ⚠️ 卡壳 & 待办

- `/today` 命令里 bash 注入 `git log --stat` 输出量比较大，之后可以试试用 `--oneline` + 单独 `--stat` 分开注入，看能不能压缩上下文。
- 明天想接着看 **hooks** 章节，正好把今天备忘的"Stop hook 自动生成日报"这个伏笔试着落地。
- 占位符那篇 723 行的笔记有点长，之后要拆成"入门 / 进阶 / 场景速查"三段，方便回头翻。

---

## 🌟 一句话自我肯定

从"看到 slash command 只会照抄"到今天自己写出 3 个能跑的命令、还顺手把学习笔记归了类，这一天很饱满 👏
