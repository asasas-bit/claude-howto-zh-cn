# 创建 `learning-session-retrospective` 的 AI 提示词

```text
请创建 Claude Code Skill：`learning-session-retrospective`。

用途：在用户明确结束或复盘学习会话时，根据当前对话和真实产物生成 Markdown 学习日报，保存到 `学习笔记/Z-日报`。

需要包含：
- `SKILL.md`：回顾目标、核对产物、提炼收获、记录卡点、生成一个下一步练习、保存和检查；
- `templates/daily-retrospective-template.md`：固定日报结构。

要求：
1. 设置 `disable-model-invocation: true`，避免普通对话自动生成日报；
2. 文件名使用 `YYYY-MM-DD-主题.md`；
3. 同名文件存在时不静默覆盖；
4. 只写会话中有证据的完成事项；
5. 不把长篇主题笔记复制进日报；
6. 下一步只保留一个主要练习；
7. 保存后重新读取；
8. 不 commit，不 push；
9. 不增加无用途脚本或参考目录。

先输出五张卡和结构，再创建。完成后提供三类测试。不安装，不提交。
```

