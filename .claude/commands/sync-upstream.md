---
name: sync-upstream
allowed-tools: Bash(git fetch:*), Bash(git merge:*), Bash(git log:*), Bash(git diff:*), Bash(git status:*), Bash(git branch:*), Bash(git remote:*), Bash(git push:*)
argument-hint: (无参数直接跑)
description: 拉取上游更新、展示新内容、确认后合并（推送前会停下让你确认）
---

# Sync Upstream / 同步上游更新

## 上下文（自动读取，仅供你分析用，不要在这一步做任何写操作）

- 当前分支：!`git branch --show-current`
- 当前状态：!`git status -sb | head -3`
- 远程配置：!`git remote -v`
- 上游最近提交：!`git log --oneline -3 upstream/main 2>/dev/null || echo "（尚未 fetch 过 upstream）"`
- 本地与上游差异：!`git log --oneline HEAD..upstream/main 2>/dev/null | head -10`

## 你的任务

按下面四步走。**在用户明确说"确认 / OK / 合并 / go"之前，不允许执行 `git merge` 或 `git push`。**

---

### 第 1 步：检查远程配置

先确认 `upstream` 远程存在（指向 `lhfer/claude-howto-zh-cn`）。如果不存在，提示用户添加：

```bash
git remote add upstream https://github.com/lhfer/claude-howto-zh-cn.git
```

> 添加后需要用户确认，不要自作主张去加。

### 第 2 步：拉取上游更新（fetch）

执行：

```bash
git fetch upstream
```

拉取后，展示上游新内容：

```bash
git log --oneline HEAD..upstream/main
```

- 如果**没有输出**（即没有任何新提交），告诉用户"✅ 上游没有新内容，本地已经是最新的"，然后结束，不要继续。
- 如果有新提交，**用简洁中文概括**每个 commit 讲了什么（版本号、主要变化），列给用户看。

### 第 3 步：展示合并计划，等待确认

把合并计划展示给用户，格式参考：

```
📋 合并预览
─────────────────────────────────

🆕 上游新增提交（<N> 个）：
  <sha> <message>
  <sha> <message>

🌿 当前分支：<branch-name>
🔀 合并目标：upstream/main → <branch-name>
```

然后**停下来**，问用户：

> 以上是要合并到 <branch-name> 的内容，需要我：
> - ✅ **直接合并**（回复"确认 / OK / 合并 / go"）
> - ❌ **取消**（回复"取消 / 不了"）

**不要主动执行 merge，等用户回复。**

### 第 4 步：执行合并（只有用户确认后才走）

用户确认后：

```bash
git merge upstream/main -m "merge: 同步上游更新"
```

每步都把命令和输出报给用户看。

#### 如果合并成功

给一个简短总结：

```
✅ 已合并上游更新
   分支：  <branch-name>
   新增：  <N> files changed, <X> insertions(+), <Y> deletions(-)
```

然后**询问是否推送**（不要自动 push）：

> 合并已完成。需要推送到 GitHub 吗？
> - ✅ **推送**（回复"推送 / push / go"）
> - ❌ **不推**（回复"不用 / 不推"）

用户确认推送后才执行：

```bash
git push origin <branch-name>
```

#### 如果合并有冲突

**立即停下来**，不要尝试自动解决：

1. 列出冲突文件：`git status`（显示 `both modified:` 的项）
2. 告诉用户冲突发生在哪些文件、大概是什么冲突
3. 提示用户手动解决冲突文件（编辑完保存后，执行 `git add <file>`）
4. 等用户解决完所有冲突、并确认后，再执行：

```bash
git add .
git commit -m "merge: 同步上游更新"
```

**在用户明确确认冲突已解决之前，不要 commit。**

---

## 注意事项

- 默认目标分支是当前所在分支（通常是 `study-notes`）。如果用户当前不在想要的分支上，先提示。
- **绝对不要自动 push**。推送必须等用户明确确认。
- 如果本地有未提交的改动，`git merge` 可能会被拒绝，先提示用户提交或 stash。
- 如果发现 `upstream` 指向的地址和 `lhfer/claude-howto-zh-cn` 不一致，先跟用户核对，不要贸然 merge。
