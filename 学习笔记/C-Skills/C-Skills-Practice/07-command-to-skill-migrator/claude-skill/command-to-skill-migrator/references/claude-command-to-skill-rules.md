# Claude Command 转 Skill 规则

## 路径映射

```text
.claude/commands/example.md
    ↓
.claude/skills/example/SKILL.md
```

Skill 名称由目标目录和 `name` 共同表达，应保持一致、使用小写连字符。

## Frontmatter / 元数据

| Command 内容 | Skill 处理 |
|---|---|
| `name` | 保留或规范为目标 Skill 名称 |
| `description` | 重写为“做什么＋什么时候用” |
| `argument-hint` | 仍需参数提示时保留 |
| `allowed-tools` | 逐项核对，不扩大 |
| 高风险操作 | 增加 `disable-model-invocation: true` |
| PowerShell 动态命令 | 确有需要时设置相应 shell |

## 正文与动态内容

- `$ARGUMENTS`：检查全部参数是否仍按预期传入。
- `$0`、`$1`：检查位置参数和空参数处理。
- `@path`：确认引用相对路径和文件大小。
- ``!`command` ``：确认执行时机、权限、shell 和敏感输出。
- 资源拆分后，`SKILL.md` 必须说明何时读取。

## Bash 与 PowerShell

不要根据用户打开的终端窗口机械转换。

### 默认保留 Bash

- 原 Command 已工作；
- 只使用通用 Git、Python、Node 等外部程序；
- 没有 PowerShell 专属语法；
- Git Bash 可用。

### 考虑 PowerShell

- 使用 `Get-ChildItem`、`Copy-Item`、`Select-String`、`Test-Path` 或 `$env:`；
- Windows 环境没有 Git Bash；
- 工作流依赖 PowerShell 对象管道或 `.ps1` 脚本。

## 安全

- 不删除源 Command；
- 不把 `git push`、发布或删除权限顺便加进去；
- 高风险动作采用手动调用；
- 迁移和提交是两个独立任务；
- 动态 shell 输出中可能包含敏感内容时必须提醒。
