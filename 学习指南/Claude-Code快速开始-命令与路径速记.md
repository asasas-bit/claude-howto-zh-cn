# Claude Code 快速开始：命令与路径速记

> 用途：复习“15 分钟快速开始”涉及的目录、复制命令、slash command、项目 memory 和 skill。
>
> 本指南默认使用 **Windows PowerShell 简写**：用 `mkdir` 创建目录，用 `cp` 复制文件。
> `cp` 在 PowerShell 中是 `Copy-Item` 的别名，不需要改写成长命令。

## 1. 先分清两个目录

```text
教程仓库：D:\cc\claude-howto-zh-cn
实际项目：D:\Projects\my-app
```

- 教程仓库：存放示例和模板。
- 实际项目：真正使用 Claude Code 工作的项目。
- 操作本质：把教程仓库里的模板复制到实际项目或个人配置目录。

## 2. 当前目录与路径

- **当前目录**：终端现在所在的位置。
- **绝对路径**：从盘符开始的完整地址，如 `D:\cc\claude-howto-zh-cn\01-slash-commands\optimize.md`。
- **相对路径**：从当前目录开始找，如 `01-slash-commands\optimize.md`。
- 相对路径不会搜索整台电脑；它只从当前目录出发查找，所以其他位置有同名文件夹也不影响。

PowerShell 常用检查命令：

```powershell
Get-Location                       # 查看当前目录，也可写 pwd
Set-Location "D:\某个目录"         # 进入目录，也可写 cd
Get-ChildItem                     # 查看目录内容，也可写 ls
Test-Path "D:\某个文件或目录"      # 检查路径是否存在
```

## 3. 创建 `.claude\commands` 目录

PowerShell 推荐写法：

```powershell
mkdir D:\Projects\my-app\.claude\commands -Force
```

- `mkdir`：创建目录。
- `D:\Projects\my-app`：示例项目地址，要换成自己的实际项目地址。
- `-Force`：目录已经存在时继续执行，不把它当成错误。
- 正确目录名是 `.claude\commands`，不是 `.cloud\comments`。

如果终端已经位于实际项目根目录，也可以使用相对路径：

```powershell
mkdir .\.claude\commands -Force
```

结果：

```text
my-app
└─ .claude
   └─ commands
```

## 4. 复制 slash command

命令结构：

```text
cp  源地址  目标地址
```

- `cp` 是 copy，即复制。
- 源地址表示“复制谁”。
- 目标地址表示“复制到哪里”。

假设终端当前位于教程仓库根目录：

```powershell
cp .\01-slash-commands\optimize.md D:\Projects\my-app\.claude\commands\
```

也可以把源地址和目标地址都写成 Windows 完整路径：

```powershell
cp D:\cc\claude-howto-zh-cn\01-slash-commands\optimize.md D:\Projects\my-app\.claude\commands\
```

- 上面两种都是 PowerShell 写法。
- `cp` 是 `Copy-Item` 的简写，作用相同。
- 如果路径中有空格，就给完整路径加双引号。
- 目标位置以 `\` 结尾时，文件会保持原名 `optimize.md`。

复制结果：

```text
my-app
└─ .claude
   └─ commands
      └─ optimize.md
```

## 5. `/optimize` 是什么

- Claude Code 会识别项目里的 `.claude\commands\*.md`。
- `optimize.md` 对应自定义命令 `/optimize`。
- `/help`、`/init` 一般是内置命令；`/optimize` 是通过 Markdown 文件添加的自定义命令。
- `optimize.md` 中保存的是一段可重复使用的提示词或工作流程。

使用方法：

```powershell
Set-Location "D:\Projects\my-app"
claude
```

进入 Claude Code 对话界面后输入：

```text
/optimize
```

这表示：加载 `.claude\commands\optimize.md` 中的内容并按其要求执行。

## 6. 添加项目级 memory

假设终端当前位于教程仓库根目录，PowerShell 写法是：

```powershell
cp .\02-memory\project-CLAUDE.md D:\Projects\my-app\CLAUDE.md
```

含义：把教程里的 `project-CLAUDE.md` 模板复制到项目根目录，并改名为 `CLAUDE.md`。

`CLAUDE.md` 可以记录：

- 项目用途与技术栈；
- 启动、构建、测试命令；
- 代码规范；
- 禁止修改的内容；
- Claude Code 在项目中应遵守的长期要求。

它更像“项目长期说明书”，不是自动保存全部聊天的日记。模板复制后要按项目实际情况修改。如果项目已经存在 `CLAUDE.md`，不要直接覆盖，应先合并内容。

> Claude Code 主要使用 `CLAUDE.md`；Codex 项目通常使用 `AGENTS.md`，不要混淆。

## 7. `~` 与用户主目录

- `~` 表示当前用户的主目录。
- 在本机通常类似 `C:\Users\11488`。
- `~/.claude/skills` 对应 `C:\Users\11488\.claude\skills`。

PowerShell 中可使用：

```powershell
$env:USERPROFILE
```

查看实际地址。

## 8. 安装全局 skill

PowerShell 推荐写法：

```powershell
mkdir "$env:USERPROFILE\.claude\skills" -Force
cp -Recurse .\03-skills\code-review-specialist "$env:USERPROFILE\.claude\skills\"
```

- `-Recurse` 表示递归复制整个文件夹及其全部内容。
- 这条 `cp` 命令要求终端当前位于教程仓库根目录。
- skill 安装到个人目录后，可供多个项目使用。

## 9. 三种能力放在哪里

| 能力 | 存放位置 | 作用范围 |
|---|---|---|
| Slash command | `项目\.claude\commands\optimize.md` | 当前项目 |
| 项目 memory | `项目\CLAUDE.md` | 当前项目 |
| Skill | `用户主目录\.claude\skills\...` | 多个项目 |

## 10. 一句话记忆

```text
mkdir = 创建目录
cp = 在 PowerShell 中复制文件
cp -Recurse = 在 PowerShell 中复制整个文件夹
相对路径 = 从当前目录开始找
绝对路径 = 从盘符开始写完整地址
.claude\commands\optimize.md = Claude Code 中的 /optimize
CLAUDE.md = 当前项目的长期说明书
~ = 当前用户的主目录
```
