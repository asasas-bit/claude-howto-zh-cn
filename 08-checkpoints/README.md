<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../resources/logos/claude-howto-logo-dark.svg">
  <img alt="Claude How To" src="../resources/logos/claude-howto-logo.svg">
</picture>

# Checkpoints 与 Rewind 指南

checkpoints 是 Claude Code 新手最值得尽早掌握的安全机制之一。
它的意义很简单：**敢试，因为随时能回退。**

---

## checkpoint 是什么

可以把 checkpoint 理解成当前会话状态的快照，通常包括：

- 对话消息
- 文件改动
- 工具使用历史
- 会话上下文

当你需要回退时，就使用 `rewind` 返回到某个 checkpoint。

---

## 为什么它重要

很多人不敢放手让 Claude 改代码，不是因为能力不够，而是因为怕改坏。checkpoints 解决的就是这个心理门槛。

适合这些场景：

- 大胆试不同方案
- 复杂重构
- 出现错误后回滚
- 比较两个实现方向

---

## 怎么打开

### 键盘方式

按 `Esc` 两次。

### 命令方式

```text
/rewind
```

`/checkpoint` 也可以作为别名使用。

---

## rewind 时你会看到什么选项

常见有这些：

1. **Restore code and conversation**：代码和对话都回退
2. **Restore conversation**：只回退对话
3. **Restore code**：只回退代码
4. **Summarize from here**：从这一点开始压缩总结，释放上下文窗口
5. **Summarize up to here**：压缩所选位置之前的对话，保留这一点之后的消息；它和上一项组成双向、定点的上下文压缩
6. **Never mind**：取消

> 新版行为里还有一个很实用的小细节：
> 你在做 **Restore conversation** 或 **Summarize from here** 后，被选中位置的原始 prompt 会回到输入框里，方便你重新发送或改写。

> 从 `v2.1.191+` 起，`/clear` 不再是 `/rewind` 的硬边界。也就是说，即使你已经清空过当前对话，仍可以用 `/rewind` 回到 `/clear` 之前创建的 checkpoint，找回更早的代码或上下文。

---

## checkpoints 默认就有

Claude Code 会自动创建 checkpoints，所以你不需要手动先“存档”才能用。

这意味着你可以把它当作日常工作流的一部分，而不是紧急救火功能。

---

## 配置上要纠正一个常见旧说法

现在更准确的理解是：

- checkpoints 默认开启
- 不需要再单独配置 `autoCheckpoint: true`
- `fileCheckpointingEnabled`（`v2.1.119+`）控制是否在编辑前保存文件快照
- `/config` 中对应 **Rewind code (checkpoints)**

完整配置示例：

```json
{
  "fileCheckpointingEnabled": true,
  "cleanupPeriodDays": 30
}
```

`fileCheckpointingEnabled` 默认是 `true`；也可用 `CLAUDE_CODE_DISABLE_FILE_CHECKPOINTING` 禁用文件 checkpoint。`cleanupPeriodDays` 默认是 `30`，控制保留天数。Claude Code 只保存最近 **100 个 checkpoints** 的文件快照；即使仍在保留期内，更老的快照也会被丢弃。

### `cleanupPeriodDays` 现在影响的范围更大了

上游在 `v2.1.117` 明确了：它不再只是管 checkpoints。

现在它统一影响这几类本地缓存：

- checkpoints
- `~/.claude/tasks/`
- `~/.claude/shell-snapshots/`
- `~/.claude/backups/`

所以你改这个值时，实际上是在统一调本地保留周期，而不是单独调 rewind 历史。

---

## 一个很实用的工作流

```text
先让 Claude 改
→ 如果结果好，继续
→ 如果不满意，/rewind
→ 换一种实现路线
```

这在这些任务里尤其好用：

- UI 重构
- API 重构
- auth / permission 变更
- 大批量文档整理

---

## 新手最容易忽略的点

### 1. checkpoint 不只是“撤销”

它不只是救错，还可以帮助你探索多种实现方案。

### 2. rewind 不一定要连代码一起退

有时你只是想保留代码，但回退对话；或者相反。这个选择很有用。

### 3. 两种 summarize 很适合长会话

当上下文太长时，`Summarize from here` 可以压缩所选位置之后的内容，`Summarize up to here` 可以压缩之前的内容。两者都只调整会话上下文，不会改磁盘文件。

### 4. 以为 rewind 一定会改磁盘文件

不是。像 **Summarize from here** 这种选项，核心作用是压缩会话上下文，不会直接改你磁盘上的代码文件。

### 5. 忽略 symlink / hard link 的保护边界

从 `v2.1.216+` 起，`/rewind` 不会再沿着被跟踪路径上的 symlink 或 hard link 去恢复、覆盖或删除真实目标。遇到这类路径时会跳过，并报告跳过数量。这个保护能避免回退误伤链接指向的外部文件，但也意味着这些路径需要你手工核对。

---

## 常见使用场景

| 场景 | 建议做法 |
|------|----------|
| 试两种不同实现 | 做一次改动后 `/rewind` 回去重试 |
| 大型重构 | 每走一段就确认 checkpoint |
| Claude 改坏了 | 回到上一个稳定状态 |
| 会话太长 | 用 summary 压缩后继续 |

---

## 中国用户特别注意

如果你在本地化或改写示例文档时做大范围文本替换，checkpoints 也非常有用。
因为这类修改很容易“看起来都对，实际把命令名或字段名翻坏”，有 checkpoint 会安全很多。

## checkpoints 和 Git 怎么配合

checkpoints 只服务于当前 session，适合短期试错，而且会随清理周期过期；Git commit 是长期、可审计、可共享的历史。推荐先用 checkpoint 探索和回退，确定方案后再用 Git 固化结果，不要把 checkpoints 当成版本控制替代品。

---

## 推荐下一步

- 想学命令行和 print mode：看 [10-cli](../10-cli/)
- 想学更复杂的规划与权限控制：看 [09-advanced-features](../09-advanced-features/)
