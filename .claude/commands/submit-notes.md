---
name: submit-notes
allowed-tools: Bash(git status:*), Bash(git diff:*), Bash(git log:*), Bash(git branch:*), Bash(git remote:*), Bash(git add:*), Bash(git commit:*), Bash(git push:*)
argument-hint: [可选补充说明]
description: 把学习笔记按主题自动分组、起好中文 commit 名，确认后一次提交并推送到你的 GitHub
---

# Submit Notes / 提交并推送学习笔记

## 上下文（自动读取，仅供你分析用，不要在这一步做任何写操作）

- 当前分支：!`git branch --show-current`
- 工作区状态：!`git status -s`
- 最近提交：!`git log --oneline -5`
- 远程配置：!`git remote -v`

## 你的任务

把用户的学习笔记和个人配置**按主题分成多个 commit**，起好 conventional 风格的中文提交名，**等用户确认一次后，连续完成提交和推送**。

**在用户明确说"确认 / OK / 提交 / go"之前，不允许执行任何 `git add`、`git commit`、`git push`。**

---

### 第 1 步：状态检查（有问题就停下）

1. 如果 `git status -s` **没有任何输出**，告诉用户"✅ 工作区是干净的，没有要提交的笔记"，然后结束，不要继续后面的步骤。
2. 如果处于 detached HEAD（`git branch --show-current` 输出为空），或者状态里出现未解决的合并冲突（`UU`、`AA`、`DD` 等标记），停下来让用户先处理，不要贸然提交。
3. 如果当前分支是 `main`，提示用户："你现在在 main 分支上；笔记通常提交到 study-notes。确认要在 main 上提交并推送吗？"等用户明确确认再继续。

### 第 2 步：分析改动并按主题分组

**默认把未跟踪的新文件（状态里的 `??`）也包含进来**——学习笔记基本都是新文件，这是本命令和 `/git-safe-submit` 的关键区别。

纳入范围（用户自己的内容）：

- `学习笔记/` 下的所有笔记、日报
- `.claude/commands/`、`.claude/skills/`、`.claude/agents/` 下用户自建的内容

**特别检查**：如果发现上游核心文件也被改动了（`01-*`～`10-*` 教程目录、`scripts/`、`.github/`、根目录的 `README.md` / `CHANGELOG.md` 等），把它们**单独列出来**并提示：

> 以下文件不属于你的笔记，是上游教程或仓库配置：
> <文件列表>
> 确认要一起提交吗？还是先排除？

用户没有明确说包含，就不要把这些文件放进计划。

**分组规则**：

- 同一主题的文件放一组：同一目录的同一批笔记；配套的"命令 + 讲解副本"算同一主题（例如 `.claude/commands/xxx.md` 和 `学习笔记/D-command/xxx.md` 合为一组）
- 日报（`学习笔记/Z-日报/`）每篇单独一组；同一天同主题的内容可合并
- 拿不准某个文件归属哪组时，宁可在计划里标出来问用户，不要硬凑

**每组生成提交信息**：

- 格式：`<type>(<scope>): <中文一行概括>`
  - `type`：笔记和文档用 `docs`，新命令/新技能用 `feat`，修错用 `fix`，杂项维护用 `chore`
  - `scope`：笔记用 `study-notes`，命令用 `commands`
  - 概括：准确说清这组内容学了什么、加了什么；不编造、不写空话
- 内容较多时，加 1-3 行正文补充说明
- 如果用户传了参数 `$ARGUMENTS`，把这段补充说明融进相关 commit 的正文
- 每条 commit 消息末尾加一行 trailer：`Co-Authored-By: Claude Code <noreply@anthropic.com>`

### 第 3 步：展示完整计划，等一次确认

用下面的格式展示：

```
📋 提交计划（共 <N> 个 commit，完成后推送到 origin/<branch>）
─────────────────────────────────

第 1 个 commit：
  📝 <type>(<scope>): <消息>
  📂 <文件列表>

第 2 个 commit：
  📝 ...
  📂 ...

🌿 当前分支：<branch>
⬆️ 最后一步：git push origin <branch>
```

然后**停下来**，问用户：

> 以上是提交+推送计划，需要我：
> - ✅ **确认执行**（回复"确认 / OK / 提交 / go"，我会连续完成提交和推送）
> - ✏️ **修改**（告诉我哪个 commit 的消息或分组要调整）
> - ❌ **取消**（回复"取消 / 不了"）

**不要主动执行任何写操作，等用户回复。**

### 第 4 步：执行（只有用户确认后才走到这里）

1. 按计划**逐组**执行：`git add <这组文件>` → `git commit -m "<消息>"`，每组完成后把结果报给用户看
2. 全部 commit 完成后，执行：`git push origin <当前分支>`
3. 最后给一个总结：

```
✅ 已提交并推送
   <N> 个 commit：
     <sha> <消息>
     <sha> <消息>
   分支：<branch> → origin/<branch>
```

#### 如果推送失败

- **立即停下来**，把报错原样告诉用户
- **绝对不要 force push**（`--force`、`--force-with-lease` 都不行），也不要自作主张换别的方式推
- 最常见的原因是远端有了新内容：提示用户可以先运行 `/sync-upstream`（或手动 `git pull`）把远端内容合进来，再重新提交，由用户决定下一步

---

## 注意事项

- 这个命令管 **⬆️ 上传你的笔记**；追上游更新（⬇️ 拉取合并）用 `/sync-upstream`，两个是一对
- 通用的单次安全提交（默认不含新文件、提交完不推送）用 `/git-safe-submit`
- commit 消息里的 `type`、`scope`、文件路径、git 命令都是英文标识，不要中文化；概括描述用中文
- 永远不要跳过 git hooks（不要用 `--no-verify`）
- 任何一步出现意料之外的提示（登录失败、权限问题、hook 报错），停下告诉用户，不要自己绕过去
