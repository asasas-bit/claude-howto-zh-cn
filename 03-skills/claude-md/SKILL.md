---
name: claude-md
description: 按最佳实践创建或更新 CLAUDE.md，帮助 AI agent 更快理解项目。Use when users want to create, update, audit, or improve a CLAUDE.md file.
---

# CLAUDE.md / 项目记忆整理

## 用户输入

```text
$ARGUMENTS
```

支持的意图：

- `create`
- `update`
- `audit`
- 指定某个路径下的 `CLAUDE.md`

## 核心原则

- `CLAUDE.md` 是 Claude Code 自动加载的长期项目上下文
- 内容要短、准、长期有效
- 不要把 lint / format 规则硬塞进去
- 不要把一次性任务说明塞进去
- 不要自动生成一堆无价值内容
- `AGENTS.md` 不会被 Claude Code 自动读取；需要共享时从 `CLAUDE.md` 导入 `@AGENTS.md` 或使用 symlink
- subagent 定义属于 `.claude/agents/`，不要把 `AGENTS.md` 当成 agent 配置

## 推荐结构

- Project Overview
- Tech Stack
- Project Structure
- Development Commands
- Critical Conventions
- Known Issues / Gotchas

## 执行流程

### create（创建）

1. 分析项目结构和技术栈
2. 草拟 `CLAUDE.md`
3. 给用户审阅
4. 确认后写入

### update（更新）

1. 读取现有 `CLAUDE.md`
2. 找出冗余、过时或不该存在的内容
3. 给出优化建议
4. 审阅后更新

### audit（审计）

1. 检查行数和结构
2. 识别 anti-patterns
3. 输出报告，不直接改文件

## 质量约束

- 目标控制在 200 行以内；更长内容拆到按路径生效的 rules 或按需 skills
- 面向所有会话都适用
- 文件引用可以减少重复维护，但不会减少加载上下文；需要按需加载时使用 rules 或 skills
- 命令必须真实可用
