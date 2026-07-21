---
name: command-to-skill-migrator
description: 分析 Claude Code Slash Command Markdown，判断是否值得升级为 Skill，并生成兼容、安全的迁移方案、手动 PowerShell 步骤或目标 Skill。用户要求把 command 转为 skill、迁移 `.claude/commands`、解释迁移差异或检查 Bash 与 PowerShell 兼容性时使用。
argument-hint: "[command-file-path]"
disable-model-invocation: true
---

# Command to Skill Migrator / Command 转 Skill 迁移器

开始时读取：

- `${CLAUDE_SKILL_DIR}/references/claude-command-to-skill-rules.md`
- `${CLAUDE_SKILL_DIR}/templates/migration-report.md`

## 第一阶段：只读分析

1. 读取源 Command、项目 `CLAUDE.md` 和相关教程。
2. 检查现有目标 Skill 和同名 Slash 入口，避免冲突。
3. 分析：名称、描述、参数、动态值、文件引用、shell 命令、工具权限、写入范围和风险。
4. 判断继续保留 Command、转换为单文件 Skill，还是需要带资源的 Skill。
5. 使用迁移报告输出结论。

未经用户确认，不创建或修改文件。

## 第二阶段：确认设计

锁定：

- 目标 Skill 名称；
- 项目级或个人级；
- 手动调用或允许模型发现；
- 保留 Bash 还是改用 PowerShell；
- 是否保留源 Command；
- 需要复制、重写或拆分的资源。

默认保留源 Command，默认不扩大工具权限。

## 第三阶段：按模式执行

### 手动教学模式

- 只做只读检查；
- 给出 PowerShell 命令；
- 简单复制优先使用 `cp`；
- 每一步说明目的、预期结果和检查方法；
- 不替用户修改。

### 直接实施模式

- 只在用户明确授权后创建目标 Skill；
- 保留用户已有修改；
- 迁移后检查目录、frontmatter、正文和所有资源引用；
- 不删除源文件；
- 不执行 commit 或 push。

## Shell 决策

- 外层 PowerShell 不等于 Skill 必须使用 PowerShell 工具。
- `git status`、`git diff`、`git add`、`git commit` 等通用 Git 命令原来使用 Bash 且可工作时，默认保留。
- 出现 `Get-ChildItem`、`Copy-Item`、`$env:` 等 PowerShell 专属语法时，才选择 PowerShell。
- 出现 `grep`、`find`、`export` 等 POSIX 专属语法时，保留 Bash 并说明依赖。

## 验收

- 目标目录名称与 Skill 名称一致；
- 主文件名为 `SKILL.md`；
- `description` 包含功能和触发场景；
- 参数和动态上下文没有静默丢失；
- 权限没有扩大；
- 高风险 Skill 只能手动调用；
- 源文件仍存在；
- 没有 commit 或 push。
