# 创建 `command-to-skill-migrator` 的 AI 提示词

```text
请创建 Claude Code Skill：`command-to-skill-migrator`。

用途：分析现有 Slash Command Markdown，判断是否值得升级为 Skill，并在保留原行为和安全边界的前提下，提供手动 PowerShell 迁移步骤或实施迁移。

需要包含：
- `SKILL.md`：只读分析、必要性判断、方案确认、手动/实施模式、校验；
- `references/claude-command-to-skill-rules.md`：目录、frontmatter、参数、动态上下文、Bash/PowerShell 和安全映射；
- `templates/migration-report.md`：统一迁移报告。

要求：
1. 创建或修改前先读取源文件和项目约束；
2. 先判断是否真的需要迁移；
3. 不删除或覆盖源 Command；
4. 用户要求手动练习时，不替用户修改；
5. PowerShell 中安装步骤优先使用简单 `mkdir`、`cp`；
6. 不因用户外层终端是 PowerShell 就自动把 `Bash(git ...)` 改掉；
7. 只有出现 PowerShell 专属语法或环境确实不支持 Bash 时才建议转换；
8. 高风险操作默认加入 `disable-model-invocation: true`；
9. 不扩大 allowed-tools；
10. 不执行 commit 或 push；
11. 创建后检查目标路径、SKILL.md、资源引用和调用名称。

先输出五张需求卡与结构，再创建。不安装，不提交。
```

