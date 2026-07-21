---
name: git-safe-submit
description: 检查当前 Git 改动，只暂存本次相关文件，并创建一次安全的本地 commit。仅在用户明确调用或明确要求使用该 Skill 提交时使用；不执行 git push。
argument-hint: "[message]"
disable-model-invocation: true
allowed-tools: Bash(git add *) Bash(git status *) Bash(git commit *) Bash(git diff *) Bash(git branch *) Bash(git log *)
---

# Git Safe Submit / 安全本地提交

## 当前上下文

- Git 状态：!`git status --short`
- 当前分支：!`git branch --show-current`
- 当前改动：!`git diff HEAD`
- 最近提交：!`git log --oneline -10`

## 执行流程

1. 确认当前目录是 Git 仓库，并说明当前分支。
2. 阅读已暂存、未暂存和未跟踪文件，识别本次提交范围。
3. 检查密码、密钥、令牌、本地配置和明显不相关文件。
4. 如果范围不清楚或包含多个独立主题，先向用户确认或建议拆分。
5. 只对本次相关的明确文件执行 `git add <path>`；不要使用 `git add .`。
6. 再次运行 `git diff --cached`，确认将要提交的内容。
7. 用户通过参数提供 message 时使用 `$ARGUMENTS`；否则根据已暂存改动生成 Conventional Commit 信息。
8. 执行一次 `git commit`，不绕过 hooks。
9. 运行 `git log -1 --oneline` 和 `git status --short` 验证结果。

## 提交信息

优先使用：

- `feat:` 新功能
- `fix:` 修复问题
- `docs:` 文档改动
- `refactor:` 重构
- `test:` 测试改动
- `chore:` 维护工作

信息必须准确、简洁，不编造未发生的内容。

## 安全边界

- 不执行 `git push`。
- 不执行 `git add .`。
- 不使用 `--no-verify`。
- 不修改 Git 配置。
- 不提交敏感信息。
- 不把不相关改动塞进同一个 commit。
- 如果 commit 失败，报告原因，不用破坏性命令绕过。

## 完成汇报

报告 commit hash、提交信息、包含的文件、剩余未提交改动，并明确说明尚未推送。
