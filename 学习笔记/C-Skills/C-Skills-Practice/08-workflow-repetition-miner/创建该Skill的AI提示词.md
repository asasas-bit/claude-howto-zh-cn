# 创建 `workflow-repetition-miner` 的 AI 提示词

```text
请创建 Claude Code Skill：`workflow-repetition-miner`。

目标：从用户提供的聊天、笔记、日志或任务记录中提取反复出现的动作，判断哪些应沉淀为提示词、项目指导、Command、Skill、Script、Hook、MCP 或 Plugin，并为优先候选生成可执行规格。

需要包含：
- `SKILL.md`：证据索引、聚类、分类、排序、确认和规格生成；
- `references/carrier-decision-rubric.md`：载体选择和复杂度判断；
- `templates/workflow-candidate-catalog.md`：候选总表；
- `templates/candidate-spec.md`：单个候选五张卡、创建方法和测试。

要求：
1. 只分析用户提供或授权的来源；
2. 每个候选必须有重复证据；
3. 合并不同表达但本质相同的动作；
4. 区分“反复讨论一个知识点”和“反复执行一套动作”；
5. 先选择最小载体，不把所有内容做成 Skill；
6. 明确列出暂不值得沉淀的内容；
7. 输出价值、频率、稳定度、风险和优先级；
8. 未经用户确认不批量创建候选成品；
9. 高风险、事件触发和外部系统需求分别考虑 Hook、权限和 MCP；
10. 不提交、不推送、不访问未授权私人数据。

先输出需求卡和目录设计，再创建。完成后用一段混合聊天记录测试分类。不安装，不提交。
```

