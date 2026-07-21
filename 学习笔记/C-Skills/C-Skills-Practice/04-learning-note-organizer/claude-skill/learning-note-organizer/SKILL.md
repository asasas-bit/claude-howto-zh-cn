---
name: learning-note-organizer
description: 将 AI 工具学习过程中的对话、零散理解和项目资料整理成适合新手复习的 Markdown 学习笔记。用户要求整理学习笔记、沉淀知识点、把当前讨论保存为 Markdown，或维护学习笔记目录时使用。
argument-hint: "[topic-or-source]"
---

# Learning Note Organizer / 学习笔记整理器

## 输入

使用用户提供的主题、当前对话、文件或目录作为主要材料。缺少文件名时，根据主题生成清楚、稳定、不含“最终版”等时效词的名称。

优先从项目中发现目标目录、已有命名和相关教程。只有多个合理选择会明显改变结果时才询问用户。

## 执行流程

1. 明确用户真正要理解的主题和当前水平。
2. 读取与主题直接相关的项目材料，不扩展到无关内容。
3. 读取 `${CLAUDE_SKILL_DIR}/references/writing-rules.md`。
4. 读取 `${CLAUDE_SKILL_DIR}/templates/learning-note-template.md`，按需保留适用章节。
5. 先诊断用户已有理解，再组织结论、原理、步骤、例子和误区。
6. 检查目标目录和同名文件；不得静默覆盖。
7. 保存 Markdown 后重新读取，确认路径、标题和关键内容。
8. 运行校验：

   ```powershell
   powershell -NoProfile -ExecutionPolicy Bypass -File "${CLAUDE_SKILL_DIR}/scripts/validate-note.ps1" -Path "目标文件绝对路径"
   ```

9. 向用户报告文件路径、主要内容和验证结果。

## 输出要求

- 先给一句话结论，再展开解释。
- 第一次出现英文术语时补充中文含义。
- 使用必要的表格、例子和命令，但不为了形式增加无关内容。
- 区分用户原有理解、纠正内容和新增知识。
- 命令必须符合用户实际终端环境。
- 聊天回复只汇报结果，不重复粘贴整篇笔记。

## 安全边界

- 不写入密码、密钥、令牌、账号或其他敏感信息。
- 不静默覆盖已有文件。
- 不修改与笔记无关的文件。
- 不执行 `git commit` 或 `git push`。
- 校验失败时先修正笔记，再报告完成。
