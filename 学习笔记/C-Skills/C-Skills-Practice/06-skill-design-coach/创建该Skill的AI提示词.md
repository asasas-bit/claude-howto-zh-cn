# 创建 `skill-design-coach` 的 AI 提示词

```text
请创建 Claude Code Skill：`skill-design-coach`。

目标：帮助不会从零设计 Skill 的用户，通过五张需求卡和四道闸门，把模糊想法转化成最小可用、可解释、可测试的 Skill。

创建前先输出需求理解和目录设计，不修改文件。需要包含：

- `SKILL.md`：访谈、载体判断、结构设计、确认、创建、解释、测试和迭代；
- `templates/five-cards.md`：触发、输入、流程、输出、边界与验收；
- `templates/test-matrix.md`：应该触发、不应触发、边界测试；
- `references/resource-selection-guide.md`：Prompt、Skill、Script、Hook、MCP 和 Plugin 的选择规则。

行为要求：
1. 优先从项目发现事实，只询问真正的偏好和取舍；
2. 一次只问最重要的问题；
3. 五张卡未清楚前不创建；
4. 先给最小结构，每个可选目录必须说明存在理由；
5. 未经用户确认不进入文件创建；
6. 高风险操作单独确认；
7. 创建后逐项解释设计决策；
8. 至少设计三类测试；
9. 不自动提交或推送；
10. 不创建 README、CHANGELOG 或空目录。

完成后静态校验所有资源引用，并给出 Codex 迁移说明。不安装，不提交。
```

