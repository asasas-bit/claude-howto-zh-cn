# 将焊枪项目作为 Codex 实战练习场

## 总体方案

- 当前仓库处于干净的 `master`，并与 `origin/master` 同步，适合从此处创建 `practice/codex-lab`。
- `master` 保持稳定，用于继续学习 HTML、CSS、JavaScript，未来的 React、Next.js 升级另开功能分支。
- `practice/codex-lab` 作为长期实验分支；实验成果不整体合并，只把真正有价值的功能通过独立提交或小 PR 合回 `master`。
- 暂时不先大规模改造项目。当前原生 HTML/CSS/JS 的复杂度正适合学习 AI 编程工具；项目功能随练习逐步丰富。
- `claude-howto-zh-cn` 继续作为教材和笔记仓库，不混入焊枪项目代码。该仓库目前已有未跟踪文档，暂不对其执行切分支或提交操作。

## 分支与文件安排

- 从 `master` 创建并推送 `practice/codex-lab`，设置对应远程跟踪分支。
- 在练习分支中添加：
  - 根目录 `AGENTS.md`：记录项目结构、学习目标、修改边界、验证方法和提交要求。Codex 会在任务开始前读取适用的 `AGENTS.md`。[Codex AGENTS.md 文档](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
  - `AI-learning/README.md`：记录每次练习的目标、提示词、结果、错误和复盘。
  - `.agents/skills/welding-course-check/SKILL.md`：第二阶段创建项目专属检查 Skill。
  - 后期再引入 `.codex/config.toml` 或 hooks，不在第一轮同时配置。
- 调整练习分支的 `.gitignore`：允许提交 `.agents/skills/**` 和后期需要的 `.codex` 项目配置，同时继续忽略个人配置、凭据和本地临时文件。Codex 官方支持从仓库的 `.agents/skills` 发现项目级 Skill。[Codex Skills 文档](https://learn.chatgpt.com/docs/build-skills)

## 分阶段练习

1. **基础闭环**
   - 建立 `practice/codex-lab`。
   - 编写最小 `AGENTS.md`。
   - 让 Codex 先检查项目、输出计划，再实施一个小功能。
   - 首个功能确定为“报价历史”：每次成功计算后在页面下方显示最近 5 条报价，并使用 `localStorage` 保存；提供清空历史按钮。
   - 完整练习 `status → diff → 浏览器验证 → commit → log → restore/revert`。

2. **Memory/项目指令**
   - 测试没有 `AGENTS.md` 与加入 `AGENTS.md` 后，Codex 对目录、注释风格、验证步骤的遵守差异。
   - 根级规则只放稳定约定；未来若某个学习目录需要特殊规则，再添加嵌套 `AGENTS.md`。
   - 不把 Claude 的 `CLAUDE.md` 原样复制过来，而是提炼内容后转换为 Codex 的项目指令。

3. **Skills**
   - 创建 `welding-course-check` Skill，自动检查相对资源路径、HTML/CSS/JS 是否同步、移动端显示、表单交互和学习文档是否需要更新。
   - 分别测试显式调用与根据描述自动触发。
   - 不直接复制 `.claude/commands/*.md`；把有价值的 Claude command 思路改写为 Codex Skill。

4. **Hooks、权限与高级能力**
   - Skill 稳定后，再增加只读检查型 hook，例如修改网页文件后提醒执行验证。
   - hook 第一版不得自动提交、推送、删除或重写文件；项目 hook 需要单独审查和信任。[Codex Hooks 文档](https://learn.chatgpt.com/docs/hooks)
   - 随后练习计划模式、代码审查、回退、worktree 和子代理；每项能力绑定一个真实的小需求，避免只抄配置。

5. **逐步丰富项目**
   - Vanilla JS 阶段依次加入报价历史、折扣规则、产品数据拆分、基础自动化测试和可访问性检查。
   - React 学习时从 `master` 另开 `feature/react-learning`，不在 `practice/codex-lab` 直接迁移框架。
   - Next.js 同样作为后续独立阶段，避免同时学习框架和 AI 工具配置。

## 验收标准

- 切回 `master` 后工作区与当前版本一致，练习内容不可污染稳定分支。
- `practice/codex-lab` 能独立运行全部现有页面。
- 报价历史在刷新后仍保留、最多显示 5 条、可以清空，原报价校验和重置功能不退化。
- 新会话能够根据 `AGENTS.md` 正确说出项目结构、修改边界与验证要求。
- `welding-course-check` 能被显式调用，并对故意制造的资源路径错误给出有效检查结果。
- 每个练习形成一个主题明确、可单独查看或撤销的提交。
- 有价值的产品功能可以单独合回 `master`，AI 实验配置默认保留在练习分支。

## 默认选择

- 采用“实验后择优合并”，不整体合并长期练习分支。
- 第一轮先完成分支、`AGENTS.md`、计划、修改、验证、提交和回退的基础闭环。
- 保留当前正式分支名 `master`，暂不为了命名习惯改成 `main`。
- 当前阶段不需要先把项目改成 React 或 Next.js。
