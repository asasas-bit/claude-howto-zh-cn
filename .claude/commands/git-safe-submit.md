---
name: git-safe-submit
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*), Bash(git diff:*), Bash(git branch:*), Bash(git log:*)
argument-hint: [message]
description: 分析当前改动、生成 commit 计划、等用户确认后再提交（不会自动 push）
---

# Git Safe Submit / 安全提交改动

## 上下文（自动读取，仅供你分析用，不要在这一步做任何写操作）

- 当前 git 状态：!`git status`
- 当前 diff：!`git diff HEAD`
- 当前分支：!`git branch --show-current`
- 最近提交：!`git log --oneline -10`

## 你的任务

严格按下面的三步走。**在用户明确说"确认 / OK / 提交 / 可以了 / go"之前，不允许执行任何 `git add` 或 `git commit`。**

---

### 第 1 步：预演（Dry Run）

不要执行任何写操作。用下面的格式把提交计划展示给用户看：

```
📋 提交预览
─────────────────────────────────

📂 将要提交的文件：
  M path/to/file1.md
  A path/to/file2.md
  D path/to/deleted.md
  ?? path/to/untracked.md   ← 未被 git 跟踪，默认不加入，除非用户明确要求

📝 建议的提交信息：
  <type>(<scope>): <一行简短描述>

  （如果改动比较复杂，可以加 1-3 行正文，说明改了什么、为什么改）

🌿 当前分支：<branch-name>
🎯 目标：本地 commit（不会 push）
```

生成提交信息时：

- 如果用户传了参数 `$ARGUMENTS`，**直接用这个作为提交信息**，跳过自己生成
- 否则按 conventional commits 生成：
  - `feat:` 新功能
  - `fix:` 修复 bug
  - `docs:` 文档改动
  - `refactor:` 重构
  - `test:` 新增或调整测试
  - `chore:` 杂项维护
- 提交信息要求：准确概括改动、简洁、不编造

### 第 2 步：等待确认

展示完预览后，**停下来**，问用户：

> 以上是提交计划，需要我：
> - ✅ **直接提交**（回复"确认 / OK / 提交 / go"）
> - ✏️ **修改提交信息**（告诉我新的 message）
> - ➕ **调整文件范围**（告诉我要包含或排除哪些文件）
> - ❌ **取消**（回复"取消 / 不了"）

**不要主动执行 git add / git commit。等用户回复。**

### 第 3 步：执行（只有在用户明确确认后才走到这一步）

用户确认后，按下面顺序执行，每一步都把命令和输出报给用户看：

1. `git add <上一步预览里列出的文件>`（默认不加 untracked 文件，除非用户明确要求）
2. `git status` — 让用户看一眼暂存区状态
3. `git commit -m "<确认后的提交信息>"`
4. `git log --oneline -1` — 显示刚生成的这次 commit

**绝对不要执行 `git push`。** 推送由用户手动决定。

执行完给一个简短总结：

```
✅ 已本地提交
   Commit: <sha> <message>
   分支：  <branch>

如需推送到远端，请手动执行：
   git push
```

---

## 注意事项

- 如果 `git status` 显示没有任何改动，直接告诉用户"当前工作区没有可提交的改动"，不要继续走后面的步骤
- 如果当前处于 detached HEAD 或者有未解决的 merge 冲突，先提示用户处理，不要贸然 commit
- 如果改动跨越多个不相关主题（例如同时改了文档 + 修了 bug + 加了新功能），**建议**用户拆成多次提交，但最终决定权在用户
