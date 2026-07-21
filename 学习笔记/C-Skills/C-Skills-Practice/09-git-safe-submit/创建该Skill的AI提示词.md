# 创建 `git-safe-submit` 的 AI 提示词

```text
请把现有 `01-slash-commands/commit.md` 改造为一个最小 Claude Code Skill：`git-safe-submit`。

要求：
1. 只创建一个 `SKILL.md`，不添加无用途的模板、参考资料或脚本；
2. 保留 `$ARGUMENTS` 作为可选提交信息；
3. 保留 `Bash(git ...)`，因为正文使用通用 Git 命令；
4. 补齐 status、diff、branch、log、add 和 commit 的 Bash 权限；
5. 设置 `disable-model-invocation: true`，只允许用户手动调用；
6. 创建 commit 前检查敏感文件和不相关改动；
7. 只暂存本次相关文件，不默认 `git add .`；
8. 不执行 push，不绕过 hooks，不修改 Git 配置；
9. 创建后检查最近 commit 和剩余状态；
10. 不删除或覆盖源 Command；
11. 不在当前仓库真实执行 commit，只做文件和规则校验。

创建前先说明为什么保留 Bash，以及为什么这个 Skill 不需要其他资源。创建后给出三类测试和手动安装命令。不安装，不提交。
```

