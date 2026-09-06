<picture>
  <source media="(prefers-color-scheme: dark)" srcset="resources/logos/claude-howto-logo-dark.svg">
  <img alt="Claude How To" src="resources/logos/claude-howto-logo.svg">
</picture>

# 仓库内容总索引

这个文件用于帮助你快速知道仓库里有哪些内容、分在哪些目录、各自做什么。

## 目录总览

- `01-slash-commands/`：用户主动触发的命令示例
- `02-memory/`：`CLAUDE.md` 与 memory 示例
- `03-skills/`：可复用、自动触发的能力
- `04-subagents/`：分工协作的子代理
- `05-mcp/`：MCP 接入示例
- `06-hooks/`：事件驱动自动化
- `07-plugins/`：组合能力的 plugin 示例
- `08-checkpoints/`：checkpoint / rewind 说明
- `09-advanced-features/`：高级工作流
- `10-cli/`：CLI 参考

## 顶层文档

- `README.md`
- `LEARNING-ROADMAP.md`
- `QUICK_REFERENCE.md`
- `CATALOG.md`
- `CHANGELOG.md`
- `UPSTREAM.md`
- `LOCALIZATION-STYLE.md`

## 当前版本重点

本仓库已跟进 Claude Code `v2.1.220-r2` accuracy pass 及 `4f3fa85` 后续修复。除 Claude Opus 5（`claude-opus-5`）、subagent 默认深度为 3、`/fork` / `/subtask`、MCP scope 等内容外，当前还将中文 EPUB 改为 CI 中使用本地 `mmdc` 严格构建，并明确 5 种 hook 类型与 31 个 hook 事件属于不同分类轴。

## 资源与脚本

- `resources/`：品牌与视觉资源说明
- `scripts/`：EPUB 构建与本地化校验脚本
