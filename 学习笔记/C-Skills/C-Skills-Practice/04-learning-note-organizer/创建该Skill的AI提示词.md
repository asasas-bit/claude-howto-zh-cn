# 创建 `learning-note-organizer` 的 AI 提示词

```text
请为 Claude Code 创建一个项目级 Skill，名称为 `learning-note-organizer`。

目标：把当前对话、用户材料和项目内相关教程整理成适合新手复习的 Markdown，并保存到用户指定的学习笔记目录。

先只读检查当前项目，不要立即创建。先输出五张需求卡和最小目录设计，说明每个资源为什么需要。确认需求已经清楚后再创建。

Skill 必须满足：

1. description 同时说明功能和触发场景；
2. 正文包含输入、流程、资源使用、输出、安全边界和验证；
3. 使用 `templates/learning-note-template.md` 统一输出骨架；
4. 使用 `references/writing-rules.md` 保存稳定的中文新手写作规则；
5. 使用 `scripts/validate-note.ps1` 只读校验 Markdown 标题和残留占位符；
6. 在 SKILL.md 中明确每个资源什么时候读取或执行；
7. 不覆盖已有文件；
8. 不写入密码、密钥或隐私；
9. 不执行 git commit 或 git push；
10. 保存后重新读取目标文件，并运行校验脚本；
11. 脚本必须在临时正常样例和错误样例上真实测试；
12. 不创建 README、安装说明或无用途的空目录。

创建完成后，请解释：
- 每个文件解决什么问题；
- 为什么这些内容不全写进 SKILL.md；
- V0.1 单文件版本怎样逐步演进到当前版本；
- 应该触发、不应触发和边界测试分别是什么；
- 如果迁移到 Codex，哪些 Claude 专属部分需要调整。

只创建 Skill 文件并验证，不安装到 `.claude/skills`，不提交 Git。
```

