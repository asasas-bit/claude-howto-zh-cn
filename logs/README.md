# logs/

这个目录存放 Claude Code 在本项目工作时自动产生的本地日志。

## file-changes.log

- 由 hook 脚本 [.claude/hooks/write-logger.sh](../.claude/hooks/write-logger.sh) 自动写入
- 触发时机：Claude 每次用 **Write**（新建或整体覆盖文件）或 **Edit**（修改文件）工具之后
- 每行格式：`[年-月-日 时:分:秒] [工具名] 文件绝对路径`

示例：

```text
[2026-09-09 21:20:01] [Write] d:\cc\claude-howto-zh-cn\logs\README.md
[2026-09-09 21:21:33] [Edit]  d:\cc\claude-howto-zh-cn\CLAUDE.md
```

## 这个日志记什么、不记什么

- 只记录 **Claude 通过工具改动**的文件
- 你自己在编辑器里手动改的文件，Claude 看不到，不会出现在日志里
- 只记「什么时间动了哪个文件」，不记改动内容和原因

## 会进 git 吗

不会。仓库根目录 `.gitignore` 里已有 `*.log` 全局规则，`file-changes.log` 自动被忽略，
只留在你自己的机器上，每个 clone 仓库的人各记各的。这个 README 是说明文件，不受影响，会正常提交。

## 能删吗

能。`file-changes.log` 随时可删；下次 Claude 再改动文件时，hook 会自动重建。
想停用整个记录：从 `.claude/settings.local.json` 删掉 `hooks` 段即可。
