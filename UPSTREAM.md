# 上游与 Fork 说明

## 上游来源

- 上游仓库：[`luongnv89/claude-howto`](https://github.com/luongnv89/claude-howto)
- 上游分支：`main`
- 本地化基线 commit：`0ca8c37c81918458e063739425c4740ca92c2db2`
- 最近检查到的上游 commit：`4f3fa85d7ed0f0f77f0d8bba3f0b40ff10b2063b`
- 上游许可证：[MIT License](LICENSE)

## 本仓库性质

本仓库是一个 **非官方中文本土化 fork**，目标是面向中国小白用户重写 Claude Code 学习材料，同时尽量保持与上游结构、示例和运行行为兼容。

它不是：

- 官方 Anthropic 文档
- 上游仓库的逐字逐句翻译镜像
- 为中国平台完全重构后的独立产品

## 本仓库做了哪些调整

- 把首页、学习路线、Quick Reference、Catalog 等核心入口文档改成中文主线。
- 用“先讲用途，再讲安装，再讲示例和常见坑”的方式重写表达。
- 保留目录结构、文件路径、命令名、frontmatter key、JSON/YAML key、环境变量、CLI flags 等关键兼容元素。
- 增加中国用户常见障碍说明，例如 GitHub Token、`npm` / `npx` / `uv` / Python 环境、网络与代理、Windows / WSL 差异。
- 增加本地化校验脚本与 CI 护栏，避免翻译把示例和配置改坏。

## 本地化原则

1. **兼容性优先**
   任何会影响 Claude Code 运行、加载或复制执行的标识，默认不翻。

2. **中文表达优先**
   给人看的说明文字、学习路径、FAQ、对比表、导语等内容，以中文重写为主。

3. **术语保真**
   `skills`、`CLI`、`hooks`、`MCP`、`subagents` 这类高频术语保留英文，首次出现补中文解释。

4. **持续同步**
   本仓库默认采用“跟进上游版本 -> 判定受影响文件 -> 更新中文内容 -> 记录处理结果”的维护方式。

## 推荐同步流程

1. 获取上游新版本或新 commit。
2. 列出上游变更的文件范围。
3. 判断哪些文件影响本仓库的中文文档、示例或校验脚本。
4. 优先同步以下类型的变化：
   - 命令名、字段名、协议名、路径约定
   - 新增或废弃功能
   - 影响复制可运行性的示例变更
5. 更新中文文档后，运行：

```bash
uv run python scripts/validate_localization.py
```

6. 在提交说明或更新日志中记录：
   - 上游变更点
   - 本仓库采取了什么处理
   - 哪些内容暂时未同步

## 最近一次同步记录

### 上游同步 — 2026-08-06

- Reviewed upstream range: `b9a973b` → `4f3fa85`
- 重点上游变化：
  - EPUB 构建从 pre-commit 完全移到 CI，并为上游维护的语言增加矩阵构建；原因是本地 `mmdc` 依赖的 Chromium 在 arm64 没有可用构建
  - 文档把已经失效的 Kroki/httpx、网络重试、`--timeout` 与 `--max-concurrent` 说明改为本地 `mmdc`、`--mmdc-path`、`--lang` 和 `--puppeteer-config`
  - 修正 Ruff include / per-file-ignores 相对 `scripts/pyproject.toml` 的解析范围，将 pre-commit Ruff 升至 `v0.15.10`，并兼容 Ruff 0.16 稳定启用的 `PLR0917`
  - 删除已经不再使用的 `httpx` 与 `tenacity`，修正多语言根层文档逃逸到英文目录的相对链接，并区分 5 种 hook 类型与 31 个 hook 事件
- Chinese fork actions:
  - 发现中文 fork 仍保留旧 Kroki EPUB 实现，因此把本地 `mmdc` 渲染连同行为测试一起移植，而不是只删除依赖；保留中文封面、元数据、目录标题、图片嵌入和根目录主线
  - 中文 fork 不维护上游 `ja/vi/uk/zh` 目录，未复制无效语言矩阵；CI 只构建根目录中文版本，并显式传入 `--lang zh` 与 Chromium sandbox 配置
  - EPUB 不再进入 pre-commit，主 CI、自动化测试与标签发布统一使用严格门禁；`mmdc` 缺失、超时、解析失败或未产出图片都会让构建失败
  - 移除 `httpx`、`tenacity`，同步 Ruff 版本下限，修正 Ruff tests pattern、Bandit 配置路径与废弃的 `B113` 抑制
  - 去掉 workflow 中 Ruff、Bandit、mypy 与 Markdown lint 的 `continue-on-error`；Markdown lint 使用面向本仓库既有中文排版的显式规则，失败会真实影响提交状态
  - 修复 actionlint 发现的 runner 兼容性问题：按官方推荐升级到 `codecov-action@v5` 与 `setup-python@v7`
  - 在中文 Hooks 教程中明确“类型决定如何运行、事件决定何时运行”，不机械复制上游英文入口
  - 更新本地化回归护栏，禁止 Kroki、旧 CLI flags、死依赖与静默 CI 放行重新出现
  - 根目录继续以 `Claude Code 中文全面上手指南` 为默认入口，只维护 `origin/main`，不向 upstream 写入

### 上游同步 — 2026-08-05

- Reviewed upstream range: `343d6f0` → `b9a973b`
- Upstream head: `b9a973bf32bc28bdccb106012397e10235779bc3`
- 重点上游变化：
  - 上游发布 Claude Code `v2.1.220-r2` accuracy pass；版本号不变，集中修正教程事实与可执行示例
  - `/fork [prompt]` 现在创建独立后台 session，`/subtask <task>` 才是会回传结果的 forked subagent；真实命令是 `/fewer-permission-prompts`
  - Hook 阻断需要向 stderr 输出原因并 `exit 2`；`dependency-check.sh` 应从 stdin JSON 读取 `file_path`
  - MCP 示例需保留 `type`，数据库凭证改由 `${DATABASE_URL}` 注入；新增 scope、`add-json` 与 `streamable-http` 说明
  - Memory、skills、checkpoints、plugins、permission modes、Output Styles、Status Line 和安全 fallback 配置完成准确性修订
- Chinese fork actions:
  - 全量审阅上游 258 个变更文件，只吸收会影响中文主线、示例运行和当前事实的改动；不机械复制 metadata、多语言页脚或英文根 README
  - 修正 command / skill frontmatter、4 份 MCP JSON、Hook scripts、context tracker、9 个 plugin agents 和 `config-examples.json`
  - 把事实修订写入 01-10 核心教程、Catalog、Quick Reference、概念总览、资源索引和 Index
  - 保留文件名、路径、frontmatter key、JSON/YAML key、CLI flags、环境变量、slash command、skill / subagent / plugin 名称原文
  - 扩展 `scripts/validate_localization.py`，锁定 `v2.1.220-r2` 关键行为并禁止旧错误回归
  - 修复 `pre-commit.sh` 对所有 Bash 调用误跑测试、`session-end.sh` 提前退出的问题，新增 6 项 Hook 回归测试并通过 ShellCheck
  - 修复网站生成器与链接检查的仓库归属、链接检查 timeout 类型及模板空链接，移除指向上游 Discussions 的反馈入口；默认指向 `lhfer/claude-howto-zh-cn`
  - 修正 Ruff include 范围并清零 15 个 Python 文件的实际 format、lint、Bandit 与 mypy 检查
  - 根目录继续以 `Claude Code 中文全面上手指南` 为默认入口，只维护 `origin/main`，不向 upstream 写入

### 上游同步 — 2026-07-30

- Reviewed upstream range: `97fc961` → `343d6f0`
- 重点上游变化：
  - 教程覆盖更新到 Claude Code `v2.1.220`；`v2.1.219` 将 subagent 嵌套默认深度改为 3，`CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH=1` 用于禁用嵌套
  - Claude Opus 5（`claude-opus-5`、1M context）成为默认 Opus 模型，默认 effort 为 `high`；`/fast` 当前只适用于 Opus 5 和 Opus 4.8
  - `/deep-research` 改为仅显式调用，`/code-review` 改为后台 subagent；`context: fork` skills 默认 `background: true`
  - 新增 `DirectoryAdded`，hook 事件总数变为 31；project agent frontmatter hooks 受 workspace trust 约束
  - Auto Mode 对所有 plans 开放，但仍受组织策略、模型和 provider 资格限制；新增 `workflowSizeGuideline`、`sandbox.network.strictAllowlist` 和 classifier 行为
  - MCP 连接错误会显示 HTTP 状态与文本，配置值首尾空白会报警，headless stream-json init 暴露 `mcp_server_errors`
  - 上游 commit `5f36214` 撤回此前加入 README 的 Vexilo 社区资源
- Chinese fork actions:
  - 将上述行为本土化写入中文入口、skills、subagents、MCP、hooks、Advanced Features、CLI、Catalog、Quick Reference、概念总览和资源索引
  - 保留 `claude-opus-5`、`DirectoryAdded`、`workflowSizeGuideline`、`strictAllowlist`、`mcp_server_errors`、CLI flags、环境变量和 frontmatter key 原文
  - 将 Hooks 自测题与学习建议统一更新为 31 个事件，避免教程正文和自测数据互相矛盾
  - 复核 `doc-generator` 名称已经正确；上游 plugins、checkpoints、planning examples、Learning Roadmap 与 Style Guide 的其余变化仅涉及英文版本页脚、来源和兼容模型，中文精简版没有对应页脚，因此不机械引入英文元数据
  - 从当前资源索引移除 Vexilo，旧同步记录继续保留，准确反映先合入后撤回的上游历史
  - 扩展 `scripts/validate_localization.py`，阻止旧嵌套默认值、30 个 hooks、旧默认模型和已撤回资源回归
  - 上游 `ja/`、`vi/`、`uk/`、`zh/` 目录继续只作差异参考，不引入本中文主线
  - 不复制上游英文根 README，继续保持 `Claude Code 中文全面上手指南` 为默认入口
  - 更新 `README.md`、`UPSTREAM.md` 和 `CHANGELOG.md` 的最近同步记录

### 上游同步 — 2026-07-23

- Reviewed upstream range: `8f04517` → `97fc961`
- 重点上游变化：
  - 教程覆盖更新到 Claude Code `v2.1.217`；subagent 嵌套从默认最多 5 层改为默认关闭，并新增 `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS` 与 `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`
  - 删除已经在 `v2.1.111` 移除的 `--enable-auto-mode` 口径，改用 `--permission-mode auto`
  - hook `if` 的单段 `dir/**` 只匹配 `<cwd>/dir`，`SessionStart` 新增 `fork` 来源；`/rewind` 不再沿 symlink / hard link 恢复或删除文件
  - Memory 文件 frontmatter 新增自动维护的 `modified` 时间；GUI editor 打开 `/memory` 后不再阻塞 session
  - `config-examples.json` 删除虚构的 `planning.*`、`extendedThinking.*`、`headless.*`、`checkpoints.autoCheckpoint` 等字段，改用真实 `settings.json` schema
  - 新增 `sandbox.filesystem.disabled`、`emojiCompletionEnabled`、`FORCE_HYPERLINK`、`CLAUDE_CODE_OTEL_CONTENT_MAX_LENGTH`、`--settings` 2 MiB 上限与 permission hardening 说明
- Chinese fork actions:
  - 将上述变化本土化写入 slash commands、Memory、skills、subagents、hooks、checkpoints、Advanced Features、CLI、Catalog、Quick Reference、概念总览、资源索引和 Index
  - 保留 `defaultMode`、`fileCheckpointingEnabled`、hook event、CLI flag、环境变量、模型 ID 和 frontmatter key 原文；仅翻译 JSON 中给人看的 `name` / `description` 值
  - 对齐 `brand-voice` skill 的 `name` 与 `user-invocable`，统一 CLAUDE.md 长度建议，并加入 Vexilo 参考资源
  - 上游 `ja/`、`vi/`、`uk/`、`zh/` 目录仍只作为差异参考，不引入本中文主线；其中 `zh/06-hooks/README.md` 的 JSON 修复已核对，根目录对应示例本来就是有效 JSON
  - 扩展 `scripts/validate_localization.py`，阻止旧 Auto Mode flag、旧 subagent 默认嵌套规则和虚构配置字段回归
  - 不复制上游英文根 README，继续保持 `Claude Code 中文全面上手指南` 为默认入口
  - 更新 `README.md`、`UPSTREAM.md` 和 `CHANGELOG.md` 的最近同步记录

### 上游同步 — 2026-07-19

- Reviewed upstream range: `a645ffe` → `8f04517`
- 重点上游变化：
  - 教程覆盖更新到 Claude Code `v2.1.212`，修正已经停用的 `#` memory shortcut 说明
  - CLAUDE.md 改为按 Managed、User、Project、Local 范围拼接理解；auto memory 和 `.claude/rules/*.md` 属于独立机制，import 最大深度为 4 hops
  - 这批 session 变化后来在 `v2.1.220-r2` accuracy pass 中纠正：`/fork [prompt]` 创建独立后台 session，`/subtask <task>` 才委派会回传结果的 forked subagent，`/branch [name]` 切换到对话副本
  - subagent 输出在 `v2.1.210+` 增加 instruction-shaped text 扫描，`v2.1.212+` 默认限制每 session 200 次 spawn
  - MCP tool call 超过 2 分钟自动转后台；Auto Mode provider opt-in 在 `v2.1.207+` 已移除，并新增 reset 与 screen reader 入口
- Chinese fork actions:
  - 将行为变化本土化写入 slash commands、Memory、subagents、MCP、Advanced Features、CLI、Catalog、Quick Reference、概念总览、资源索引和 Index，不复制上游英文根 README
  - 保留 `/fork [prompt]`、`/subtask <task>`、`/branch [name]`、`managed-settings.d/`、`permissionMode`、`CLAUDE_CODE_MAX_SUBAGENTS_PER_SESSION`、`CLAUDE_CODE_MCP_AUTO_BACKGROUND_MS`、`disableAutoMode`、`--ax-screen-reader` 等标识原文
  - 删除当前教程中的“8 层覆盖链”、`/fork` 兼容别名和 `CLAUDE_CODE_ENABLE_AUTO_MODE=1` 仍需 opt-in 等过时说法
  - 上游 `ja/`、`vi/`、`uk/`、`zh/` 目录仅作为差异参考，不引入本中文主线；示例页脚的版本元数据变化通过本记录吸收，不改写无对应页脚的中文示例
  - 扩展 `scripts/validate_localization.py`，覆盖 `v2.1.212` 关键字段并阻止旧表述回归
  - 更新 `README.md`、`UPSTREAM.md` 和 `CHANGELOG.md` 的最近同步记录

### 上游同步 — 2026-07-12

- Reviewed upstream range: `0f3fe1d` → `a645ffe`
- 重点上游变化：
  - Claude Code 教程覆盖更新到 `v2.1.206`，新增 Sonnet 5（`claude-sonnet-5`）及其 1M context window 说明
  - 交互 permission mode 从 `default` 改名为 `manual`，旧名继续作为 alias
  - bundled skills 新增 `/dataviz`；`${CLAUDE_PROJECT_DIR}` 可用于 skill body / `allowed-tools`；一次调用可叠加最多 6 个开头的 skills
  - subagents 默认后台运行，Explore 继承 session 模型与 extended thinking，并新增禁用 built-in agents 和追加 system prompt 的入口
  - MCP 新增 `roots/list` / `notifications/roots/list_changed`，并收紧未信任 workspace 的 project MCP approval
  - hooks、marketplace、checkpoints、settings 和 CLI 增加新 matcher、字段、双向摘要和 streaming watchdog
- Chinese fork actions:
  - 将上述行为本土化写入 01、03-10 模块和中文入口文档，不复制上游英文根 README
  - 保留 `manual`、`claude-sonnet-5`、`/dataviz`、`${CLAUDE_PROJECT_DIR}`、`roots/list`、`renames`、`askUserQuestionTimeout`、`CLAUDE_ENABLE_STREAM_WATCHDOG` 等可执行标识原文
  - 复查上一轮 assessment 内容，修正 5 轮 / 19 分 / 30 个 hook 事件等语义错误，翻译用户可见题面和结果模板，并校验 Q9 / Q10 回看指针
  - 扩展 `scripts/validate_localization.py`，新增课程结构、跨文档事实、中文输出和本轮关键更新的语义一致性检查
  - 修复 EPUB 构建器对已嵌入 Mermaid 图片的重复本地查找，消除误报并保护电子书图像输出
  - 更新 `README.md`、`UPSTREAM.md` 和 `CHANGELOG.md` 的最近同步记录

### 上游同步 — 2026-07-11

- Reviewed upstream range: `ce10c70` → `0f3fe1d`
- 重点上游变化：
  - `docs(skills): improve lesson-quiz skill to asm-eval grade A`
  - `docs(skills): slim self-assessment skill for context efficiency`
  - `/lesson-quiz` 明确固定使用 10 道题，禁止题库缺失时临时编题，并新增结果报告模板
  - self-assessment 将 Deep Assessment 轮次、输出模板和主题建议拆到 `references/`，降低主 skill 的上下文占用
- Chinese fork actions:
  - 本地化更新 `.claude/skills/lesson-quiz/SKILL.md`，保持中文说明，同时保留 `allowed-tools`、`@file`、`disable-model-invocation`、`--add-dir`、`permissionMode`、`--debug`、`Ctrl+O` 等可执行标识原文
  - 补齐中文题库中每个 lesson 的 Q9 / Q10，使 10 题流程与数据源一致，不在运行时编造题目
  - 新增中文化的 `results-template.md`、`deep-assessment-rounds.md`、`output-templates.md`、`topic-recommendations.md`
  - 更新 self-assessment 主文件，让它按需读取新增 reference 文件
  - 不引入上游英文根 README，不改变 `Claude Code 中文全面上手指南` 的中文默认入口
  - 更新 `README.md`、`UPSTREAM.md` 和 `CHANGELOG.md` 的最近同步记录

### 上游同步 — 2026-07-02

- Reviewed upstream range: `d4243d9` → `ce10c70`
- 重点上游变化：
  - 上游修复 Pages workflow：`fix(pages): remove uv cache glob that broke on missing uv.lock`
  - `.github/workflows/pages.yml` 不再对 `astral-sh/setup-uv@v4` 启用 uv cache，避免仓库没有 `uv.lock` 时缓存 glob 触发构建失败
- Chinese fork actions:
  - 同步删除 `setup-uv` 的 `enable-cache` / `cache-dependency-glob` 配置
  - 保留中文 fork 已有的 `actions/configure-pages@v5` 和发布后首页验证步骤，继续检查线上页面包含 `Claude Code 中文全面上手指南`
  - 本轮只同步必要 workflow 行为变化，不改教程正文，不引入上游英文根 README
  - 更新 `README.md`、`UPSTREAM.md` 和 `CHANGELOG.md` 的最近同步记录

### 上游同步 — 2026-06-30

- Reviewed upstream range: `6b9ce64` → `d4243d9`
- 重点上游变化：
  - Claude Code 教程覆盖更新到 `v2.1.195`
  - MCP 增加启动认证提醒；需要登录的 server 不再只是静默不可用
  - `headersHelper` 在 MCP server 返回 HTTP 401 / 403 时会自动重新调用，用于刷新动态认证头
  - hook `matcher` 支持 `"Write,Edit"` 逗号列表，并在 `v2.1.195+` 起按更精确的工具名规则匹配
  - `/plugin` 界面会提示 unused plugins；plugin 的 `plugin.json` `name` 与 marketplace entry name 不一致时，enable / disable 仍可正确工作
  - `/clear` 不再是 `/rewind` 的硬边界，可以回到 `/clear` 之前的 checkpoint
  - `autoMode.classifyAllShell` 可让所有 Bash / PowerShell 命令都走 Auto Mode 分类器，拒绝原因会显示在 transcript、toast 和 `/permissions` 的 recently-denied 列表
  - OpenTelemetry 增加 `claude_code.assistant_response` log event，用于记录模型回复文本
  - `!` bash mode 支持 live file-path autocomplete
  - CLI 环境变量新增 `CLAUDE_CODE_DISABLE_MOUSE_CLICKS`
- Chinese fork actions:
  - 将 MCP、hooks、plugins、checkpoints、advanced features 和 CLI 新行为改写进中文主线文档
  - 保留 `headersHelper`、HTTP 401 / 403、`matcher`、`"Write,Edit"`、`plugin.json`、`autoMode.classifyAllShell`、Bash / PowerShell、`claude_code.assistant_response`、`CLAUDE_CODE_DISABLE_MOUSE_CLICKS` 等可执行标识原文
  - 同步 `CATALOG.md`、`QUICK_REFERENCE.md`、`resources.md`、`claude_concepts_guide.md`，让入口页也能看到 `v2.1.195` 新能力
  - 不引入上游英文根 README，不改变中文首页结构
  - 更新 `README.md`、`UPSTREAM.md` 和 `CHANGELOG.md` 的最近同步记录

### 上游同步 — 2026-06-26

- Reviewed upstream range: `8143e37` → `6b9ce64`
- 重点上游变化：
  - Claude Code 教程覆盖更新到 `v2.1.187`
  - `/review <pr>` 现在用于审查 GitHub PR，并复用 `/code-review medium` 的 review engine；本地工作区 diff 仍用 `/code-review`
  - settings 新增 / 补充 `attribution.sessionUrl` 与 `respondToBashCommands`
  - MCP CLI 新增 `claude mcp login <name>` / `claude mcp logout <name>`，并支持 `--no-browser`
  - Agent Teams 增加 `--teammate-mode iterm2`，依赖 `it2` CLI
  - Auto Mode 增加内置 intent-based protection，默认拦截一批破坏性命令
  - `!` bash 命令输出会自动发给 Claude 并触发回复，可用 `respondToBashCommands=false` 回到旧行为
  - sandbox 补充 `sandbox.credentials`、`sandbox.allowAppleEvents`
  - `/config key=value` 可直接设置单个配置项
  - CLI 环境变量新增或强调 `CLAUDE_CLIENT_PRESENCE_FILE`、`CLAUDE_CODE_MAX_RETRIES`、`CLAUDE_CODE_RETRY_WATCHDOG`、`CLAUDE_CODE_MCP_TOOL_IDLE_TIMEOUT`
- Chinese fork actions:
  - 将 slash command、memory settings、subagents、MCP、advanced features 与 CLI 变化改写进中文主线文档
  - 保留 `/review <pr>`、`/code-review medium`、`attribution.sessionUrl`、`respondToBashCommands`、`claude mcp login`、`--no-browser`、`--teammate-mode iterm2`、`it2`、`sandbox.credentials`、`/config key=value` 等可执行标识原文
  - 同步 `CATALOG.md`、`QUICK_REFERENCE.md`、`resources.md`、`claude_concepts_guide.md`，让入口页也能看到 `v2.1.187` 新能力
  - 不引入上游英文根 README，不改变中文首页结构
  - 更新 `README.md`、`UPSTREAM.md` 和 `CHANGELOG.md` 的最近同步记录

### 上游同步 — 2026-06-18

- Reviewed upstream range: `ae656f6` → `8143e37`
- 重点上游变化：
  - Claude Code 教程覆盖更新到 `v2.1.179`
  - `/doctor` 布局刷新为 flat tree，状态图标更清晰
  - `/bug` 现在必须填写描述后才能提交
  - 嵌套 `.claude/agents/`、workflow 和 output-style 定义采用“离当前工作目录最近者优先”规则
  - permission rules 支持 `Tool(param:value)` 形式，按工具输入参数继续细化匹配
  - remote session 里的 plugin loading performance 有改进
  - `scripts/build_website.py` 改为缓存 Markdown 源文本、复用 HTML 解析树和导航骨架，减少重复解析
  - `.github/workflows/pages.yml` 增加 uv cache 与 vendor assets cache
- Chinese fork actions:
  - 将影响真实使用的 slash command、subagent precedence、permission rule、plugin 和 CLI 说明同步进中文主线文档
  - 保留 `/doctor`、`/bug`、`.claude/agents/`、`Tool(param:value)`、`Bash(...)`、`Read(...)`、`scripts/.vendor-cache` 等可执行标识原文
  - 同步网站构建脚本性能优化，但不为中文化改名 Python 函数、YAML key 或 workflow action
  - 合入 Pages 缓存配置，同时保留本中文 fork 既有的发布后首页验证步骤
  - 不引入上游英文根 README，继续维护 `lhfer/claude-howto-zh-cn` 的中文默认入口
  - 更新 `README.md`、`UPSTREAM.md` 和 `CHANGELOG.md` 的最近同步记录

### 上游同步 — 2026-06-16

- Reviewed upstream range: `733c088` → `ae656f6`
- 重点上游变化：
  - Claude Code 教程覆盖更新到 `v2.1.176`
  - 从 `v2.1.172` 起，subagent 可以继续 spawn 子 subagent，最多嵌套 5 层；可用 `Agent(agent_type)` 限制可 spawn 的 subagent 类型
  - hooks 支持在 hook handler 上使用 `if` 条件，通过 permission-rule 语法按工具参数进一步过滤匹配
  - `/plugin` marketplace 浏览界面新增搜索栏，便于在大型 marketplace 中按名称或关键词过滤 plugin
  - 新增或更新 settings key：`enforceAvailableModels`、`wheelScrollAccelerationEnabled`、`footerLinksRegexes`、`language`
  - VSCode Account & usage 视图补充 cache miss、long-context cost、subagents 以及 per-skill / per-agent / per-plugin / per-MCP 归因
  - 上游新增 `.gitissue.yml`，并修正 `scripts/check_links.py` 对 `footerLinksRegexes` 正则示例的 URL 误报
- Chinese fork actions:
  - 将影响真实使用的 subagent、hook、plugin、settings、CLI 和 usage 说明同步进中文主线文档
  - 保留 `Agent(agent_type)`、`if`、`matcher`、`enforceAvailableModels`、`wheelScrollAccelerationEnabled`、`footerLinksRegexes`、`language` 等可执行标识原文
  - 本仓库当前没有上游 `scripts/check_links.py`，CI 使用 `.github/markdown-link-check-config.json`；因此未新增该脚本，仅确保中文文档中的 `footerLinksRegexes` 示例可由现有检查覆盖
  - 上游 `.gitissue.yml` 属于上游 PR traceability 配置，本中文 fork 不向上游开 PR，也不采用相同检查流程，因此未引入
  - 不引入上游英文根 README，继续维护 `lhfer/claude-howto-zh-cn` 的中文默认入口
  - 更新 `README.md`、`UPSTREAM.md` 和 `CHANGELOG.md` 的最近同步记录

### 上游同步 — 2026-06-12

- Reviewed upstream range: `fcdc088` → `733c088`
- 重点上游变化：
  - Claude Code 教程覆盖更新到 `v2.1.170`
  - `/cd <path>` 可在保留 prompt cache 的情况下切换 session 工作目录
  - `--safe-mode` / `CLAUDE_CODE_SAFE_MODE=1` 可禁用 CLAUDE.md、plugins、skills、hooks、MCP 等自定义项，用于隔离配置问题
  - `fallbackModel` 可配置最多三个 fallback models；`--fallback-model` 从 `v2.1.166` 起也适用于交互式 session
  - `disableBundledSkills` / `CLAUDE_CODE_DISABLE_BUNDLED_SKILLS=1` 可隐藏内置 skills、workflows 和 commands
  - `/plugin list --enabled` / `--disabled` 支持按启用状态查看 installed plugins
  - Stop / SubagentStop hook 可返回 `hookSpecificOutput.additionalContext` 给 Claude 追加上下文并继续当前 turn
  - stdio MCP servers 会收到 `CLAUDE_CODE_SESSION_ID`，包括 `--resume` 恢复的 session
  - CLI 模型表新增 `claude-fable-5`
- Chinese fork actions:
  - 将影响真实使用的 slash command、CLI flag、settings、environment variable、hook output、MCP session 和模型标识同步进中文主线文档
  - 保留 `/cd`、`--safe-mode`、`CLAUDE_CODE_SAFE_MODE`、`fallbackModel`、`disableBundledSkills`、`CLAUDE_CODE_DISABLE_BUNDLED_SKILLS`、`hookSpecificOutput.additionalContext`、`CLAUDE_CODE_SESSION_ID`、`claude-fable-5` 等可执行标识原文
  - 上游 `02-memory/README.md` 仅刷新页脚和来源链接，本中文 fork 不为此改写记忆正文
  - 不引入上游英文根 README，继续维护 `lhfer/claude-howto-zh-cn` 的中文默认入口
  - 更新 `README.md`、`UPSTREAM.md` 和 `CHANGELOG.md` 的最近同步记录

### 上游同步 — 2026-06-03

- Reviewed upstream range: `e30220c` → `fcdc088`
- 重点上游变化：
  - Claude Code 教程覆盖更新到 `v2.1.160`
  - `claude plugin init <name>` 可在 `.claude/skills` 中创建新 plugin；该目录下的 plugin 会自动加载，不需要 marketplace
  - Auto Mode 支持 Bedrock / Vertex / Foundry 上的 Opus 4.7 / 4.8，但需要显式设置 `CLAUDE_CODE_ENABLE_AUTO_MODE=1`
  - `EnterWorktree` 可以在同一 session 中切换 Claude 管理的 worktree；完成后的 worktree 保持 unlocked，便于 `git worktree remove` / `prune`
  - `acceptEdits` 对 shell 启动文件和可执行构建配置写入仍会提示确认
  - dynamic workflows 的触发关键词改为 `ultracode`，裸词 `workflow` 不再触发运行
  - `CLAUDE_CODE_OPUS_4_6_FAST_MODE_OVERRIDE` 在 `v2.1.160` 起为 no-op
  - 上游修正 `ja` / `uk` / `vi` 翻译里的 settings 优先级说明
- Chinese fork actions:
  - 将影响真实使用的 plugin、Auto Mode、worktree、permission mode 和 workflow 行为变化同步进中文主线文档
  - 保留 `claude plugin init <name>`、`CLAUDE_CODE_ENABLE_AUTO_MODE`、`EnterWorktree`、`acceptEdits`、`ultracode`、`git worktree remove`、`prune` 等可执行标识原文
  - 不引入上游英文根 README 或 `ja` / `uk` / `vi` 目录；这些语言目录的修正已审阅，中文根目录 settings 优先级说明已保持正确
  - 更新 `README.md`、`UPSTREAM.md` 和 `CHANGELOG.md` 的最近同步记录

### 上游同步 — 2026-06-01

- Reviewed upstream range: `c726139` → `e30220c`
- 重点上游变化：
  - Claude Code 教程覆盖更新到 `v2.1.156`，并切到 Claude Opus `4.8` 口径
  - `/model` 默认行为改为保存为后续 session 默认值；按 `s` 才只作用于当前 session
  - Opus 4.8 默认 effort 是 `high`；`xhigh` 支持 Opus 4.8 / 4.7，`max` 支持 Opus 4.8 / 4.7 / 4.6 和 Sonnet 4.6；Haiku 4.5 不支持 effort levels
  - Fast Mode 默认切到 Opus 4.8，`CLAUDE_CODE_OPUS_4_6_FAST_MODE_OVERRIDE` 已弃用并在 2026-06-01 移除
  - `/simplify` 在 `v2.1.154` 后重新成为独立的清理型命令；`/code-review` 继续用于正确性缺陷审查
  - 新增 `/reload-skills`、`/workflows`、dynamic workflows、skill `disallowed-tools`、SessionStart `reloadSkills` / `sessionTitle`
  - hooks 事件数更新为 30，新增 `MessageDisplay`；status-line 命令脚本会收到 `COLUMNS` 和 `LINES`
  - 修正 settings 优先级链：managed policy -> `.claude/settings.local.json` -> `.claude/settings.json` -> `~/.claude/settings.json`
- Chinese fork actions:
  - 将模型、命令、settings、skills、hooks 和 workflow 行为变化同步进中文主线文档
  - 保留 `/model`、`/effort`、`/reload-skills`、`/workflows`、`disallowed-tools`、`reloadSkills`、`sessionTitle`、`MessageDisplay`、`COLUMNS`、`LINES` 等可执行标识原文
  - 不引入上游英文根 README 或额外多语言目录改动，继续维护 `lhfer/claude-howto-zh-cn` 的中文默认入口
  - 更新 `README.md`、`UPSTREAM.md` 和 `CHANGELOG.md` 的最近同步记录

### 上游同步 — 2026-05-27

- Reviewed upstream range: `46941a3` → `c726139`
- 重点上游变化：
  - Claude Code 教程覆盖更新到 `v2.1.150`
  - 内置 `/simplify` 改名为 `/code-review`，旧名不再作为 alias（别名）使用
  - `/code-review` 支持 effort 参数，例如 `/code-review high`，并可用 `--comment` 写 GitHub PR 行内评论
  - `/usage` 成本视图按 skills、subagents、plugins、MCP server 等类别拆分
  - `claude agents` 视图支持 `Ctrl+T` 固定后台 session
  - Markdown 渲染支持 GFM 任务清单复选框（`- [ ]` / `- [x]`）
  - 新增托管设置：`allowAllClaudeAiMcps`
  - 上游将本地示例 `code-review` skill 改为 `code-review-specialist`，避免遮蔽新版内置 `/code-review`
  - 移除 Stop / SubagentStop `background_tasks`、`session_crons` 字段说明，因为它们未列入当前官方 hooks reference
- Chinese fork actions:
  - 将本仓库示例 skill 目录从 `03-skills/code-review/` 改名为 `03-skills/code-review-specialist/`
  - 更新 README、CHANGELOG、功能总表、速查卡、skills、hooks、MCP、CLI、advanced features 与概念总览中的中文说明
  - 保留 `/code-review`、`--comment`、`Ctrl+T`、`allowAllClaudeAiMcps`、`- [ ]`、`- [x]` 等可执行标识原文
  - 不引入上游 `ja/`、`uk/`、`vi/`、`zh/` 等额外多语言目录改动，继续维护根目录中文默认入口
  - 更新 `README.md`、`UPSTREAM.md` 和 `CHANGELOG.md` 的最近同步记录

### 上游同步 — 2026-05-23

- Reviewed upstream range: `7e369ee` → `46941a3`
- 重点上游变化：
  - 上游先修正 `uk/`、`vi/`、`zh/` 等多语言 root-level README 的 logo 相对路径
  - Claude Code 教程覆盖更新到 `v2.1.145`
  - `/extra-usage` 主名称改为 `/usage-credits`，旧名继续作为 alias（别名）可用
  - `/model` 选择默认只影响当前 session；选择后按 `d` 才会设置成后续 session 默认模型
  - 新增 bundled skills：`/run`、`/verify`、`/run-skill-generator`
  - Stop / SubagentStop hook 输入新增 `background_tasks` 和 `session_crons`
  - `claude agents` 增加 `--json`，方便脚本、状态栏和 session picker 读取
  - 修复 Bash 裸环境变量 allowlist 自动批准问题，`FOO=bar somecommand` 这类命令现在需要覆盖完整命令的 `Bash(...)` 权限规则
- Chinese fork actions:
  - 将影响真实使用、安全边界和自动化脚本的变化同步进中文主线文档
  - 保留 `/usage-credits`、`/run`、`/verify`、`background_tasks`、`session_crons`、`Bash(...)` 等可执行标识原文
  - 补充根级 `pyproject.toml` 的 `jinja2` 依赖，确保固定自动化测试命令能覆盖网站构建测试
  - 不引入上游 `uk/`、`vi/`、`zh/` 等额外多语言目录改动，继续维护根目录中文默认入口
  - 更新 `README.md`、`UPSTREAM.md` 和 `CHANGELOG.md` 的最近同步记录

### 上游同步 — 2026-05-20（补充）

- Reviewed upstream range: `30d5ad5` → `7e369ee`
- 重点上游变化：
  - 修正 `ja/`、`uk/`、`vi/`、`zh/` 多语言模块 README 的 logo 相对路径
  - 变更集中在多语言子目录，不涉及英文根主线文档内容
- Chinese fork actions:
  - 审阅后确认本中文 fork 采用根目录中文主线，现有根目录与模块 README 路径本身正确
  - 不引入上游其他语言子目录改动，避免在本 fork 中维护额外多语言树
  - 仅更新 `README.md`、`UPSTREAM.md` 和 `CHANGELOG.md` 的同步记录

### 上游同步 — 2026-05-20

- Reviewed upstream range: `3557d79` → `30d5ad5`
- 重点上游变化：
  - Claude Code 教程覆盖更新到 `v2.1.143`
  - 新增 `/goal`、`/scroll-speed`、`claude agents` Agent View、`claude plugin details`
  - hooks 增加 `args` exec 形式、`continueOnBlock`、`terminalSequence`、Stop hook block safety cap
  - plugins、Remote Control、`/schedule`、Windows PowerShell tool、Fast Mode 默认模型出现多项行为更新
  - MCP stdio server 现在自动带 `CLAUDE_PROJECT_DIR`
- Chinese fork actions:
  - 将会影响真实使用和自动化行为的变化同步到中文主线文档
  - 保留 `/goal`、`claude agents`、`continueOnBlock`、`CLAUDE_PROJECT_DIR`、`CLAUDE_CODE_OPUS_4_6_FAST_MODE_OVERRIDE` 等可执行标识原文
  - 不引入上游英文根 README 或其他语言目录改动，继续维护 `lhfer/claude-howto-zh-cn` 的中文默认入口
  - 更新 `README.md`、`UPSTREAM.md` 和 `CHANGELOG.md` 的最近同步记录

### 上游同步 — 2026-05-16

- Reviewed upstream range: `553a319` → `3557d79`
- 重点上游变化：
  - 新增 `scripts/build_website.py`，可从 Markdown 生成静态网站
  - 新增 `scripts/vendor_assets.py` 与 `scripts/website_templates/`，用于自托管 Tailwind、Mermaid、字体和页面模板
  - 新增 `scripts/tests/test_build_website.py`
  - 新增 `.github/workflows/pages.yml`，支持 GitHub Pages 自动构建与发布
  - `scripts/requirements.txt` / `scripts/pyproject.toml` 增加 `jinja2` 依赖，`.gitignore` 增加 `site/` 与 `scripts/.vendor-cache/`
- Chinese fork actions:
  - 将静态网站生成器、依赖、模板、测试和 Pages workflow 同步到中文仓库
  - 用中文补充 `scripts/README.md` 的网站构建与部署说明，保留 CLI、路径和模板文件名等可执行标识原文
  - 实际运行新加的网站构建测试，并在整套脚本测试中确认通过
  - 更新 `README.md`、`UPSTREAM.md` 和 `CHANGELOG.md` 的最近同步记录

### 上游同步 — 2026-05-12

- Reviewed upstream range: `b3571e8` → `553a319`
- 重点上游变化：
  - 新增 `scripts/check_markdown_rendering.py`，用于校验 Markdown 渲染正确性
  - 新增 `scripts/tests/test_check_markdown_rendering.py`
  - `.pre-commit-config.yaml` 增加 `markdown-rendering` 钩子
  - 文档侧修正 `` !`command` `` 相关渲染转义，避免 inline code 被错误解析
- Chinese fork actions:
  - 将 Markdown 渲染校验脚本、测试和 pre-commit 钩子同步到中文仓库
  - 保持中文文档主线不变，不引入上游 `ja/`、`vi/`、`zh/` 目录里的非根主线改动
  - 通过实际运行新校验器，确认当前中文 README 集合渲染检查通过
  - 更新 `README.md`、`UPSTREAM.md` 和 `CHANGELOG.md` 的最近同步记录

### 上游同步 — 2026-05-10

- Reviewed upstream range: `d4b5cf5` → `b3571e8`
- 重点上游变化：
  - Claude Code 教程覆盖更新到 `v2.1.138`
  - hooks 文档更新为 29 个事件，新增 `Setup` 事件，并把 `effort.level` / `CLAUDE_EFFORT` / `CLAUDE_CODE_SESSION_ID` 暴露给 hooks / Bash 子进程
  - advanced features 增补 `worktree.baseRef`、`autoMode.hard_deny`、plan mode 无条件阻止写入、`sandbox.bwrapPath` / `sandbox.socatPath`
  - MCP 修复 `/clear` 后 server 丢失与 OAuth refresh token 并发刷新问题
  - plugin command 现在支持 `/myplugin review` 这种空格写法，`plugin.json` 里的 `skills` 条目与默认 `skills/` 目录会合并发现
- Chinese fork actions:
  - 将会影响命令执行、权限理解或自动化行为的变化同步到中文主线文档
  - 保留 `Setup`、`worktree.baseRef`、`autoMode.hard_deny`、`CLAUDE_CODE_SESSION_ID`、`CLAUDE_CODE_DISABLE_ALTERNATE_SCREEN` 等可执行标识原文
  - 不引入上游英文根 README 或其他语言目录改动，继续维护 `lhfer/claude-howto-zh-cn` 的中文默认入口
  - 更新 `README.md`、`UPSTREAM.md` 和 `CHANGELOG.md` 的最近同步记录

### 上游同步 — 2026-05-07

- Reviewed upstream range: `9701bb7` → `d4b5cf5`
- 重点上游变化：
  - Claude Code 教程覆盖更新到 `v2.1.131`
  - 新增 `skillOverrides` 的更细粒度取值、`--plugin-url`、plugin `.zip` 加载、`disableRemoteControl`
  - `/mcp` 会显示每个 server 的工具数并标记 `0 tools`
  - gateway `/v1/models` 发现从默认开启改为显式 opt-in，需要 `CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY=1`
  - `/context` 不再把 ASCII 可视化写进对话上下文，`Ctrl+R` 默认搜索范围扩大到所有项目，`--channels` 支持 API key 认证
- Chinese fork actions:
  - 将会影响复制执行或配置理解的变更同步到中文主线文档
  - 保留 `skillOverrides`、`/mcp`、`--plugin-url`、`disableRemoteControl`、`CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY` 等可执行标识原文
  - 不引入上游英文根 README 或其他语言目录改动，继续维护 `lhfer/claude-howto-zh-cn` 的中文默认入口
  - 更新 `README.md`、`UPSTREAM.md` 和 `CHANGELOG.md` 的最近同步记录

### 上游同步 — 2026-05-03

- Reviewed upstream range: `f393805` → `9701bb7`
- 重点上游变化：
  - Claude Code 教程覆盖更新到 `v2.1.126`
  - 新增或补充 `claude project purge`、`claude plugin prune`、headless `claude ultrareview`、MCP `alwaysLoad`、hooks `updatedToolOutput`
  - 修正 memory 题库中已停用的 `# your rule` 快捷写法
  - 修正 extended thinking 题库和示例，避免把 `/think` 当成有效命令，并明确 `ultrathink` 与 `/effort` 的区别
  - 上游 `uk/`、`vi/` 本地化目录同步了 advanced features 说明
- Chinese fork actions:
  - 将会影响中文用户复制使用的命令、配置和题库说明同步到根目录中文主线
  - 保留 `project purge`、`plugin prune`、`alwaysLoad`、`updatedToolOutput`、`ultrathink`、`/effort` 等可执行标识原文
  - 不引入上游其他语言目录改动，继续维护 `lhfer/claude-howto-zh-cn` 的中文默认入口
  - 更新 `README.md`、`UPSTREAM.md` 和 `CHANGELOG.md` 的最近同步记录

### 上游同步 — 2026-05-01

- Reviewed upstream range: `3221229` → `f393805`
- 重点上游变化：
  - 新增完整 `ja/` 日文翻译目录
  - 英文 README 去掉硬编码 star / fork 数字，改成更稳妥的动态信任表述
  - 上游为日文目录补充对应 pre-commit / EPUB 构建支持
- Chinese fork actions:
  - 不引入 `ja/` 多语言目录，继续保持根目录中文主线
  - 中文 README 原本未使用上游硬编码 star / fork 指标，因此只更新同步记录
  - 不同步日文 EPUB / pre-commit 专项配置，避免为未维护目录增加无效检查
  - 保持中文默认入口和核心教程内容不变

### 上游同步 — 2026-04-28

- Reviewed upstream range: `a7a0ea2` → `3221229`
- 重点上游变化：
  - 新增 `06-hooks/session-end.sh`，用于在 `SessionEnd` 时记录学习进度
  - 新增 `local-progress/index.html`，提供浏览器本地学习进度面板
  - 修正 agent 定义优先级为 CLI → Project → User
  - 修正 lesson quiz 题库里的 skill metadata 预算、agent 优先级和 hooks 类型口径
  - 配置示例继续收敛到 Opus 4.7 / Sonnet 4.6
- Chinese fork actions:
  - 将新增 hook 和本地进度页面改写为中文用户可直接理解的版本
  - 保留 `SessionEnd`、`CLAUDE_PROJECT_DIR`、`localStorage`、CLI flags 等可执行标识
  - 更新中文 hooks、subagents、CLI、advanced features 与题库说明
  - 保留本仓库自有 `RELEASE_NOTES.md`，不照搬上游删除动作

### 上游同步 — 2026-04-26

- Reviewed upstream range: `eff5bd2` → `a7a0ea2`
- 重点上游变化：
  - skills 文档把加载流程图的命名讲得更清楚
  - plugins 文档新增 marketplace update / plugin update 区分，以及 auto-update 说明
  - advanced features 修正 effort level 的模型支持范围，明确 `xhigh` 仅属于 Opus 4.7
- Chinese fork actions:
  - 只同步会影响中文用户理解和使用的说明性变化
  - 在中文文档里补上 marketplace 更新与 plugin 更新的区别
  - 修正 effort level 支持范围的中文表述，避免误导
  - 保持中文根目录主线，不引入上游多语言目录结构

### 上游同步 — 2026-04-25

- Reviewed upstream range: `d17d515` → `eff5bd2`
- 重点上游变化：
  - 修复 `security-reviewer` agent 中无效的 `diff` 工具配置，改为 `bash`
  - 新增 `scripts/check_cross_references.py` 的 repo-root 边界处理
  - 新增 `scripts/tests/test_check_cross_references.py` 覆盖该脚本边界场景
  - 将 `scripts/requirements.txt` 固定到已验证版本
- Chinese fork actions:
  - 把 agent 工具修正同步到中文仓库
  - 引入交叉引用检查脚本和测试，并修正中文仓库现有断锚，确保脚本能本地通过
  - 固定脚本依赖版本，减少环境差异导致的校验波动
  - 保持中文根目录主线，不引入上游多语言目录结构

### 上游同步 — 2026-04-24

- Reviewed upstream range: `cf92e8e` → `d17d515`
- 重点上游变化：
  - 上游同步到 Claude Code `v2.1.119`
  - slash commands 补充 `/cost` / `/stats` / `/usage` 的新关系，以及 `/doctor`、`/theme`、`/btw` 的新版说明
  - hooks 补充 `mcp_tool`、28 个事件、`duration_ms`、PowerShell auto-approve
  - CLI / advanced features 补充 native binary、docs host 迁移、Opus 4.7 细节、Auto Mode 与 settings 新行为
  - skills / memory / subagents / checkpoints / plugins 文档补充一批配置与行为说明
- Chinese fork actions:
  - 只把影响中文用户理解和实际使用的变化同步到中文根目录主线
  - 保持中文默认入口，不采用上游英文 README 和多语言目录结构
  - 对新增配置和命令做中文解释，同时保留可执行标识原样
  - 本地化校验与测试通过后再推送到 origin/main

### 上游同步 — 2026-04-22

- Reviewed upstream range: `9c224ff` → `cf92e8e`
- 重点上游变化：
  - 上游同步到 Claude Code `v2.1.110` / `v2.1.112`
  - 新增或明确 `/tui`、`/focus`、`/recap`、`/undo`、`/proactive`、`/ultrareview`、`/fewer-permission-prompts`
  - advanced features 补充了 TUI、session recap、push notifications、Auto Mode 新访问方式
  - CLI / docs 切到 Opus 4.7，并引入 `xhigh` effort
  - plugins 章节新增 background monitors 说明
- Chinese fork actions:
  - 把本轮新增能力同步到中文根目录主线文档
  - 保留中文默认入口，不采用上游英文 README 和 `uk/` / `zh/` 目录结构
  - 更新本地化校验，拦截明显未翻译的英文标题和英文模板段落

### 上游同步 — 2026-04-14

- Reviewed upstream range: `561c6cb` → `9c224ff`
- 重点上游变化：
  - 上游把 `# ...` inline memory 快捷写法标记为 discontinued，推荐改用 `/memory` 或自然语言记忆请求
  - `05-mcp/README.md` 不再继续强调 `WebSocket transport`
  - 新增 `/team-onboarding` 命令说明，并扩充了 `/ultraplan` 的云端起草细节
  - `Monitor Tool` 被明确写进 advanced features，用于替代低效轮询
  - `06-hooks/pre-tool-check.sh` 修复了 block reason 输出和 `rm -rf /tmp/...` 误拦截问题
  - README 补充了乌克兰语入口，但这属于上游多语言分发层变化
- Chinese fork actions:
  - 更新中文 `memory` 文档，移除对 `# ...` 快捷写法的继续推荐
  - 删除中文 `MCP` 文档里已经过时的 `WebSocket transport` 说明
  - 在中文命令目录、Catalog、Quick Reference 中补上 `/team-onboarding`、`/ultraplan` 与 `Monitor Tool`
  - 同步 `pre-tool-check.sh` 的上游修复，并新增回归测试覆盖 block/warn 行为
  - 保持根目录中文主线结构，不引入上游 `uk/` 目录和 README 语言切换入口

### 上游同步 — 2026-04-08

- Reviewed upstream range: `0ca8c37` → `561c6cb`
- 重点上游变化：
  - 上游在 2026 年 4 月完成一轮更大的文档同步，并发布 `v2.3.0`
  - 新增 `CLAUDE.md`
  - 新增 `04-subagents/performance-optimizer.md`
  - 新增 `06-hooks/pre-tool-check.sh` 与 `06-hooks/dependency-check.sh`
  - 一批 hooks 脚本改为读取 stdin JSON，并补齐 Windows Git Bash 兼容性
  - 文档层面新增 / 修正了 `MCP Apps`、`/ultraplan`、Agent Teams、Channels、`cleanupPeriodDays` 等说明
  - 上游新增 `zh/`、`vi/` 多语言目录，并重构了部分 CI / release 流程
- Chinese fork actions:
  - 将与中文主线直接相关的新增能力和示例同步到根目录中文文档
  - 新增中文 `CLAUDE.md`，适配本仓库自己的校验和本地化工作流
  - 新增 `performance-optimizer` subagent，并更新 `CATALOG.md`
  - 同步高价值 hooks 脚本与新版协议行为
  - 在 `README.md` 中更新最近同步日期与本轮更新说明
  - 未采用上游 `zh/` / `vi/` 目录结构与 README 指标徽章，继续保持“中文主线在根目录”的 fork 结构
### 上游同步 — 2026-04-01

- Upstream range: `d41b335` → `0ca8c37`
- Affected files:
  - `06-hooks/README.md`
  - `06-hooks/auto-adapt-mode.py`
  - `09-advanced-features/README.md`
  - `09-advanced-features/setup-auto-mode-permissions.py`
  - `README.md`
- Chinese fork actions:
  - 删除旧的 `auto-adapt-mode` hook 文件，不再继续维护“动态记忆批准”方案
  - 新增 `09-advanced-features/setup-auto-mode-permissions.py`，同步上游的一次性权限种子脚本
  - 在中文 `Advanced Features` 和 `Hooks` 文档中补上新的使用方式、适用场景和安全边界
  - 在项目介绍中写明最近同步日期与本次上游更新内容
  - 上游新增的 Trending 徽章未直接照搬，因为它描述的是上游仓库状态，而不是当前中文 fork 的状态

## 建议记录模板

```md
## 上游同步 - YYYY-MM-DD

- Upstream range: <old>...<new>
- Affected files:
  - README.md
  - 05-mcp/README.md
- Chinese fork actions:
  - 同步了 MCP 章节新增字段说明
  - 保留了命令名与 JSON key 不变
  - 补充了中国用户的安装注意事项
```

## 额外说明

- 如果你未来将本仓库发布到自己的 GitHub 账号下，建议仓库名使用 `claude-howto-zh-cn`。
- 如果需要替换徽章、封面图、仓库 URL，请在保留来源声明的前提下调整。
- 如果某处翻译和可执行性冲突，**优先保留原始标识**，并在正文中补中文解释。
