# Claude Code：手动创建 `git-safe-submit` Skill

> 目标：把仓库中的 `01-slash-commands/commit.md` 手动转换成一个仅供当前项目使用的 Claude Code Skill。

## 一、这次要做成什么

源文件：

```text
01-slash-commands/commit.md
```

目标文件：

```text
.claude/skills/git-safe-submit/SKILL.md
```

完成后的目录结构：

```text
claude-howto-zh-cn/
├── 01-slash-commands/
│   └── commit.md
└── .claude/
    └── skills/
        └── git-safe-submit/
            └── SKILL.md
```

这里有三个要点：

1. `git-safe-submit` 是 Skill 名称，也是文件夹名称。
2. Skill 的主文件必须叫 `SKILL.md`，不能继续叫 `commit.md`。
3. 它放在项目的 `.claude/skills/` 下，所以只对当前项目生效。

## 二、关于 PowerShell 和 Bash 的选择

本教程在 **PowerShell 终端**中操作，但 Skill 内继续使用：

```yaml
allowed-tools: Bash(git ...)
```

不改成 `PowerShell(git ...)`，也不添加：

```yaml
shell: powershell
```

原因是这个 Skill 使用的都是通用 Git 命令：

```text
git status
git diff
git add
git commit
git branch
git log
```

它们在 Git Bash 和 PowerShell 中都能使用。只要当前电脑上的 Claude Code 可以使用 Bash 工具，原来的写法就不受你使用 PowerShell 终端的影响。

PowerShell 中的：

```powershell
cp
```

是 `Copy-Item` 的别名，所以简单复制文件时可以直接使用，不必改成长命令。

## 三、开始前先确认位置

打开 PowerShell，进入教程仓库：

```powershell
cd D:\cc\claude-howto-zh-cn
```

查看当前所在位置：

```powershell
pwd
```

确认源文件存在：

```powershell
Test-Path .\01-slash-commands\commit.md
```

如果返回：

```text
True
```

说明位置正确，可以继续。

如果返回 `False`，先不要继续复制，检查是否进入了正确的项目目录。

## 四、创建 Skill 文件夹

执行：

```powershell
mkdir .\.claude\skills\git-safe-submit -Force
```

这条命令会创建：

```text
.claude\skills\git-safe-submit
```

`-Force` 的作用是：上级目录不存在时一并创建；目录已经存在时也不报错。

## 五、复制原来的命令文件

执行：

```powershell
cp .\01-slash-commands\commit.md .\.claude\skills\git-safe-submit\SKILL.md
```

这条命令的意思是：

- 从 `01-slash-commands` 中读取 `commit.md`；
- 复制到新建的 Skill 文件夹；
- 复制后的文件改名为 `SKILL.md`；
- 原来的 `commit.md` 仍然保留，不会被删除。

确认复制成功：

```powershell
Test-Path .\.claude\skills\git-safe-submit\SKILL.md
```

返回 `True` 即表示复制成功。

## 六、修改 `SKILL.md`

可以使用记事本打开：

```powershell
notepad .\.claude\skills\git-safe-submit\SKILL.md
```

如果平时使用 VS Code，也可以执行：

```powershell
code .\.claude\skills\git-safe-submit\SKILL.md
```

把文件开头两个 `---` 之间的内容替换为：

```yaml
---
name: git-safe-submit
description: 基于当前改动创建一次本地 Git commit；仅在用户明确要求提交时使用，不执行 git push
argument-hint: "[message]"
disable-model-invocation: true
allowed-tools: Bash(git add *) Bash(git status *) Bash(git commit *) Bash(git diff *) Bash(git branch *) Bash(git log *)
---
```

下面原有的 Markdown 正文继续保留。

建议在“你的任务”下面再补充一句：

```markdown
只创建本地 commit，不执行 git push。提交前检查改动，不要提交密码、密钥或其他敏感信息。
```

### 这些字段分别是什么意思

| 字段 | 作用 |
|---|---|
| `name` | Skill 的名称 |
| `description` | 告诉 Claude 这个 Skill 做什么、什么时候使用 |
| `argument-hint` | 提示这个 Skill 可以接收一条提交信息 |
| `disable-model-invocation` | 禁止 Claude 自己主动调用，只允许用户手动调用 |
| `allowed-tools` | 预先允许该 Skill 使用的 Bash Git 命令 |

这里故意不加入：

```yaml
shell: powershell
```

因为当前 Skill 没有使用 PowerShell 专属命令，没有必要增加额外配置。

## 七、检查文件内容

保存后回到 PowerShell，查看文件前 20 行：

```powershell
Get-Content .\.claude\skills\git-safe-submit\SKILL.md -TotalCount 20
```

重点检查：

- 文件路径是否正确；
- 文件名是否为大写的 `SKILL.md`；
- `name` 是否为 `git-safe-submit`；
- 开头和结尾的 `---` 是否都存在；
- YAML 中是否保留了 `Bash(git ...)`；
- 正文是否仍然存在。

还可以查看 Git 识别到了哪些变化：

```powershell
git status --short
```

正常情况下会看到新增加的 `.claude/skills/git-safe-submit/SKILL.md`。

## 八、让 Claude Code 加载 Skill

仍然在项目根目录中启动 Claude Code：

```powershell
claude
```

进入 Claude Code 后，可以先输入：

```text
/skills
```

检查 Skill 列表中是否出现 `git-safe-submit`。

也可以直接输入：

```text
/git-safe-submit
```

如果是在 Claude Code 已经运行之后才创建的文件，可以先尝试：

```text
/reload-skills
```

如果当前版本没有这个命令，就退出 Claude Code，再在项目根目录重新执行：

```powershell
claude
```

## 九、第一次调用前先理解风险

这个 Skill 不是演示按钮，它会尝试创建真实的 Git commit。

第一次练习前，先在 PowerShell 中查看：

```powershell
git status
```

再查看具体改动：

```powershell
git diff
```

确认没有密码、密钥、账号配置或不想提交的文件之后，再调用 Skill。

不传参数时：

```text
/git-safe-submit
```

Claude 会根据当前改动生成提交信息。

传入提交信息时：

```text
/git-safe-submit "docs: add git safe submit skill"
```

Claude 会优先使用你提供的提交信息。

注意：安装 Skill 本身也会新增一个文件。如果在当前教程仓库中调用它，这个新 Skill 文件也可能成为本次提交内容的一部分。

## 十、执行后检查结果

退出 Claude Code，或者另外打开一个 PowerShell 窗口，执行：

```powershell
git status
```

查看最近一次提交：

```powershell
git log -1 --oneline
```

这个 Skill 只负责创建本地 commit，不会自动推送到 GitHub。

需要推送时，由你另外手动执行：

```powershell
git push
```

## 十一、常见问题

### 1. 我使用 PowerShell，为什么还能写 `Bash(git ...)`？

你打开 Claude Code 的外层终端和 Claude 内部调用的工具不是一回事。

在 PowerShell 中启动 Claude Code，不代表 Claude 只能使用 PowerShell 工具。如果电脑安装了 Git for Windows，Claude Code 通常可以继续使用 Bash 工具。

### 2. 为什么 `cp` 在 PowerShell 中可以使用？

因为 PowerShell 把 `cp` 设置成了 `Copy-Item` 的别名。

可以执行下面的命令查看：

```powershell
Get-Alias cp
```

对于本教程这种简单文件复制，直接使用 `cp 源文件 目标文件` 即可。

### 3. 什么时候才需要改成 PowerShell？

当 Skill 中出现下面这些 PowerShell 专属写法时，再考虑使用 PowerShell：

```powershell
Get-ChildItem
Copy-Item
Select-String
Test-Path
$env:NAME
```

当前 Skill 只有 Git 命令，所以没有必要修改。

### 4. 输入 `/git-safe-submit` 没有出现怎么办？

依次检查：

1. 当前终端是否位于项目根目录；
2. 路径是否为 `.claude/skills/git-safe-submit/SKILL.md`；
3. 文件名是否确实是 `SKILL.md`；
4. YAML 的两个 `---` 是否完整；
5. 重启一次 Claude Code。

### 5. `allowed-tools` 是不是表示只能用这些工具？

不是。它主要表示这些匹配的命令可以预先获得许可、减少确认提示。

没有列出的工具仍然遵守 Claude Code 的普通权限规则，并不一定完全不能使用。

## 十二、最短操作清单

熟悉以后，只需要记住下面几步：

```powershell
cd D:\cc\claude-howto-zh-cn
mkdir .\.claude\skills\git-safe-submit -Force
cp .\01-slash-commands\commit.md .\.claude\skills\git-safe-submit\SKILL.md
notepad .\.claude\skills\git-safe-submit\SKILL.md
Get-Content .\.claude\skills\git-safe-submit\SKILL.md -TotalCount 20
git status --short
claude
```

进入 Claude Code 后：

```text
/skills
/git-safe-submit
```

## 十三、一句话理解

这次操作的本质是：

> 把一个原来的 Slash Command Markdown 文件，复制到 Claude Code 规定的 Skill 目录中，改名为 `SKILL.md`，补充 Skill 元数据，然后通过 `/git-safe-submit` 手动调用。

