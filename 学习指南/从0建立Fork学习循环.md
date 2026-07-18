# 从 0 建立 Fork 学习循环

> 适用场景：你准备学习 GitHub 上的一个开源仓库，希望把它 Fork 到自己的账号，使用 VSCode 在本地阅读和做笔记，把学习成果上传到自己的 GitHub；当原作者更新时，还能继续同步最新代码。

---

## 一、最终要建立的工作方式

整个学习循环由两套远程仓库和两个本地分支组成。

### 两个远程仓库

| 名称 | 指向哪里 | 主要用途 |
| --- | --- | --- |
| `origin` | 你自己 Fork 后的 GitHub 仓库 | 上传自己的学习笔记和修改 |
| `upstream` | 原作者的 GitHub 仓库 | 获取原作者后续更新 |

### 两个本地分支

| 分支 | 主要用途 |
| --- | --- |
| `main` | 保持和原作者的主分支一致，尽量不写个人笔记 |
| `study-notes` | 阅读代码、做实验和保存自己的学习笔记 |

整体流程如下：

```text
原作者仓库 upstream
        ↓ 获取更新
本地 main 分支
        ↓ 合并更新
本地 study-notes 分支
        ↓ 提交并推送
自己的 GitHub Fork（origin）
```

这样做的好处是：原作者的代码和自己的学习内容分开管理，后续同步更新时更加清晰。

---

## 二、开始前的准备

需要准备：

1. GitHub 账号。
2. 已安装 Git。
3. 已安装 VSCode。
4. 已在 VSCode 中打开一个准备存放仓库和学习指南的总文件夹。
5. 知道准备学习的原作者仓库地址。

在 VSCode 中选择：

```text
终端 → 新建终端
```

检查 Git 是否已安装：

```powershell
git --version
```

如果能够看到类似下面的版本号，说明 Git 已安装：

```text
git version 2.x.x
```

### 第一次使用 Git 时配置身份

执行：

```powershell
git config --global user.name "你的GitHub用户名"
git config --global user.email "你的GitHub邮箱"
```

例如：

```powershell
git config --global user.name "andy"
git config --global user.email "andy@example.com"
```

检查配置：

```powershell
git config --global user.name
git config --global user.email
```

这里的邮箱最好使用 GitHub 账号绑定的邮箱，或者 GitHub 提供的隐私邮箱。

---

## 三、在 GitHub 上 Fork 原作者仓库

Fork 只需要在第一次建立学习仓库时操作一次。

1. 使用浏览器打开原作者的 GitHub 仓库。
2. 点击页面右上角的 `Fork`。
3. 在 `Owner` 中选择你自己的 GitHub 账号。
4. 仓库名称一般保持原名称不变。
5. 可以保留 `Copy the main branch only`。
6. 点击 `Create fork`。

创建完成后，浏览器会进入你自己的仓库，地址通常类似：

```text
https://github.com/你的用户名/仓库名
```

页面左上方通常会显示：

```text
你的用户名 / 仓库名
forked from 原作者用户名 / 仓库名
```

看到 `forked from` 就说明 Fork 成功。

### Fork、Clone 和 Branch 的区别

- `Fork`：在 GitHub 上复制一份仓库到自己的账号。
- `Clone`：把 GitHub 仓库下载到本地，并保留完整 Git 历史。
- `Branch`：同一个仓库内的一条独立开发路线。
- 下载 ZIP：只下载普通文件，不包含完整 Git 历史和远程仓库关系，不适合本学习流程。

---

## 四、将自己的 Fork 克隆到当前目录下

进入自己 Fork 后的 GitHub 仓库页面：

1. 点击绿色的 `Code` 按钮。
2. 选择 `HTTPS`。
3. 复制仓库地址。

地址类似：

```text
https://github.com/你的用户名/仓库名.git
```

回到 VSCode 终端。当前目录中已经有 `学习指南` 文件夹，因此让 Git 在当前目录下新建一个仓库子文件夹：

```powershell
git clone https://github.com/你的用户名/仓库名.git
```

克隆完成后的目录结构类似：

```text
当前总文件夹/
├── 学习指南/
│   └── 从0建立Fork学习循环.md
└── 仓库名/
    ├── .git/
    └── 原项目文件……
```

进入刚刚克隆的仓库目录：

```powershell
cd 仓库名
```

以后所有 `git status`、`git add`、`git commit` 和同步命令，都需要在这个仓库子文件夹中执行。

如果你希望自己指定子文件夹名称，也可以执行：

```powershell
git clone https://github.com/你的用户名/仓库名.git 我的学习仓库
cd 我的学习仓库
```

### 如果提示目标文件夹已经存在

如果出现：

```text
fatal: destination path '仓库名' already exists and is not an empty directory
```

说明当前目录下已经存在同名子文件夹。先检查其中内容：

```powershell
Get-ChildItem -Force .\仓库名
```

不要不加判断地删除文件。确认它是否已经是克隆好的仓库；如果不是，可以换一个新的目标文件夹名称进行克隆。

### 检查克隆是否成功

执行：

```powershell
git status
git remote -v
```

此时通常会看到：

```text
origin  https://github.com/你的用户名/仓库名.git (fetch)
origin  https://github.com/你的用户名/仓库名.git (push)
```

这里的 `origin` 必须是你自己的 GitHub 仓库，而不是原作者仓库。

---

## 五、关联原作者仓库

回到原作者的 GitHub 仓库页面，点击 `Code`，复制原作者仓库的 HTTPS 地址。

执行：

```powershell
git remote add upstream https://github.com/原作者用户名/仓库名.git
```

检查远程仓库：

```powershell
git remote -v
```

正确结果类似：

```text
origin    https://github.com/你的用户名/仓库名.git (fetch)
origin    https://github.com/你的用户名/仓库名.git (push)
upstream  https://github.com/原作者用户名/仓库名.git (fetch)
upstream  https://github.com/原作者用户名/仓库名.git (push)
```

记忆方式：

```text
origin   = 我的 GitHub 仓库
upstream = 原作者的 GitHub 仓库
```

### 如果不小心添加错了 upstream

先检查：

```powershell
git remote -v
```

修改地址：

```powershell
git remote set-url upstream https://github.com/正确的原作者用户名/仓库名.git
```

再次检查：

```powershell
git remote -v
```

---

## 六、确认主分支名称

执行：

```powershell
git branch --show-current
```

大多数新仓库会显示：

```text
main
```

部分旧仓库可能显示：

```text
master
```

本文后续统一使用 `main`。如果实际仓库使用 `master`，请把命令里的 `main` 全部替换成 `master`。

还可以通过下面的命令查看原作者仓库的默认分支：

```powershell
git remote show upstream
```

找到类似：

```text
HEAD branch: main
```

---

## 七、创建自己的学习分支

建议不要直接在 `main` 中写笔记。创建一个专门保存学习内容的分支：

```powershell
git switch -c study-notes
```

检查当前分支：

```powershell
git branch --show-current
```

应该显示：

```text
study-notes
```

第一次把这个分支上传到自己的 GitHub：

```powershell
git push -u origin study-notes
```

参数 `-u` 会把本地 `study-notes` 和 GitHub 上的同名分支关联起来。以后在这个分支上只需要执行：

```powershell
git push
```

---

## 八、组织学习笔记

建议在仓库内建立单独的笔记目录：

```text
notes/
```

例如：

```text
notes/
├── 00-学习计划.md
├── 01-项目介绍.md
├── 02-安装与运行.md
├── 03-目录结构.md
├── 04-源码阅读.md
└── 05-问题与解决记录.md
```

如果需要编写实验代码，也建议放在单独目录：

```text
experiments/
```

尽量避免随意修改原项目文件。如果确实需要修改，可以在笔记中记录：

- 修改了哪个文件。
- 为什么修改。
- 修改前后的现象。
- 如何恢复。

---

## 九、日常学习和上传笔记

### 1. 确认当前位于学习分支

每次开始学习时执行：

```powershell
git branch --show-current
```

如果不是 `study-notes`，执行：

```powershell
git switch study-notes
```

### 2. 查看文件变化

完成一段学习笔记后执行：

```powershell
git status
```

查看尚未暂存的具体修改：

```powershell
git diff
```

### 3. 将需要提交的文件加入暂存区

添加一个指定文件：

```powershell
git add notes/01-项目介绍.md
```

添加整个笔记目录：

```powershell
git add notes
```

如果还要添加实验目录：

```powershell
git add notes experiments
```

初学阶段建议明确指定目录或文件，不要习惯性地使用 `git add .`，避免把临时文件、账号配置或不需要的文件一起提交。

### 4. 检查即将提交的内容

```powershell
git diff --staged
```

同时再次检查：

```powershell
git status
```

### 5. 创建一次提交

```powershell
git commit -m "docs: 更新学习笔记"
```

可以根据内容写得更具体：

```powershell
git commit -m "docs: 添加项目目录结构笔记"
```

```powershell
git commit -m "docs: 补充本地运行问题记录"
```

### 6. 上传到自己的 GitHub

```powershell
git push
```

### 日常保存笔记的固定命令

```powershell
git switch study-notes
git status
git add notes
git diff --staged
git commit -m "docs: 更新学习笔记"
git push
```

如果 Git 提示：

```text
nothing to commit, working tree clean
```

表示当前没有新的修改需要提交，不是错误。

---

## 十、同步原作者的最新更新

建议每次开始一轮较长的学习之前同步一次。

### 同步前先检查自己的修改

```powershell
git status
```

如果有尚未提交的笔记，优先完成提交并上传：

```powershell
git add notes
git commit -m "docs: 保存同步前的学习笔记"
git push
```

### 1. 切换到主分支

```powershell
git switch main
```

### 2. 获取原作者的最新提交

```powershell
git fetch upstream
```

`fetch` 只负责获取最新提交记录，不会立即修改当前文件。

### 3. 将原作者更新合并到本地主分支

```powershell
git merge --ff-only upstream/main
```

`--ff-only` 可以避免在干净的主分支上产生不必要的合并提交。如果这条命令失败，通常说明本地 `main` 已经有自己额外的提交，需要先检查原因，不要直接强制覆盖。

### 4. 更新自己的 GitHub 主分支

```powershell
git push origin main
```

完成后，下面三处的主分支应基本一致：

```text
原作者 upstream/main
本地 main
自己的 GitHub origin/main
```

### 5. 将原作者更新带入学习分支

```powershell
git switch study-notes
git merge main
```

如果没有冲突，再上传：

```powershell
git push
```

### 完整同步命令

```powershell
git status
git switch main
git fetch upstream
git merge --ff-only upstream/main
git push origin main
git switch study-notes
git merge main
git push
```

---

## 十一、有未完成修改时怎样同步

最稳妥的方法是先提交。如果内容暂时不适合提交，可以使用 `stash` 临时收藏。

### 临时收藏当前修改

```powershell
git stash push -u -m "同步前临时保存学习内容"
```

其中 `-u` 表示同时收藏尚未被 Git 跟踪的新文件。

检查收藏列表：

```powershell
git stash list
```

然后执行正常同步：

```powershell
git switch main
git fetch upstream
git merge --ff-only upstream/main
git push origin main
git switch study-notes
git merge main
```

恢复刚才临时收藏的修改：

```powershell
git stash pop
```

检查：

```powershell
git status
```

确认无误后，再提交并上传。

---

## 十二、发生合并冲突时怎么处理

当原作者和你修改了同一个文件的同一位置，执行下面的命令时可能出现冲突：

```powershell
git merge main
```

先查看：

```powershell
git status
```

VSCode 会在冲突位置显示类似内容：

```text
<<<<<<< HEAD
这是学习分支中的内容
=======
这是 main 分支带来的内容
>>>>>>> main
```

可以使用 VSCode 提供的按钮：

- `Accept Current Change`：保留当前学习分支内容。
- `Accept Incoming Change`：保留合并进来的内容。
- `Accept Both Changes`：两部分都保留。
- `Compare Changes`：先对比再决定。

也可以直接手工编辑，最终删除这些冲突标记：

```text
<<<<<<<
=======
>>>>>>>
```

处理完成后：

```powershell
git add 冲突文件路径
git commit -m "merge: 解决上游更新冲突"
git push
```

### 不确定如何解决时取消本次合并

在尚未完成合并提交之前，可以执行：

```powershell
git merge --abort
```

这会回到本次合并开始之前的状态。

不要在不清楚影响时使用：

```text
git reset --hard
git push --force
```

这些命令可能丢失本地修改或覆盖远程历史。

---

## 十三、GitHub 登录和推送验证

第一次执行：

```powershell
git push
```

GitHub 可能要求登录。按照 VSCode 或 Git Credential Manager 弹出的浏览器授权页面完成登录即可。

GitHub 已经不支持使用普通账号密码完成 HTTPS Git 推送。如果终端要求输入 Password，需要使用 Personal Access Token，而不是 GitHub 登录密码。一般优先使用 Git Credential Manager 的浏览器登录流程。

如果出现无权推送的错误，检查：

```powershell
git remote -v
```

确保 `origin` 指向的是你自己的 Fork，而不是原作者仓库。

---

## 十四、常用检查命令

### 查看当前状态

```powershell
git status
```

### 查看当前分支

```powershell
git branch --show-current
```

### 查看所有本地分支

```powershell
git branch
```

### 查看本地和远程分支

```powershell
git branch -a
```

### 查看远程仓库

```powershell
git remote -v
```

### 查看提交历史

```powershell
git log --oneline --graph --decorate --all
```

### 查看尚未暂存的修改

```powershell
git diff
```

### 查看已经暂存的修改

```powershell
git diff --staged
```

### 取消暂存，但保留文件修改

```powershell
git restore --staged 文件路径
```

例如：

```powershell
git restore --staged notes/01-项目介绍.md
```

---

## 十五、推荐的固定学习循环

### 第一次建立

```text
1. 在 GitHub 网页 Fork 原仓库
2. 在 VSCode 终端克隆自己的 Fork
3. 添加 upstream
4. 创建 study-notes
5. 将 study-notes 推送到自己的 GitHub
```

对应核心命令：

```powershell
git clone https://github.com/你的用户名/仓库名.git
cd 仓库名
git remote add upstream https://github.com/原作者用户名/仓库名.git
git remote -v
git switch -c study-notes
git push -u origin study-notes
```

### 每次开始学习前

```powershell
git status
git switch main
git fetch upstream
git merge --ff-only upstream/main
git push origin main
git switch study-notes
git merge main
```

### 学习过程中

```text
1. 阅读项目代码
2. 在 notes 中记录理解
3. 在 experiments 中保存必要的实验
4. 经常执行 git status 查看变化
```

### 每次学习结束后

```powershell
git status
git add notes
git diff --staged
git commit -m "docs: 更新学习笔记"
git push
```

如果还修改了实验目录：

```powershell
git add notes experiments
git diff --staged
git commit -m "study: 更新笔记和实验"
git push
```

---

## 十六、最终速查表

### 我现在在哪里？

```powershell
git branch --show-current
git status
```

### 上传自己的笔记

```powershell
git add notes
git commit -m "docs: 更新学习笔记"
git push
```

### 获取原作者更新

```powershell
git switch main
git fetch upstream
git merge --ff-only upstream/main
git push origin main
```

### 把更新合并进学习分支

```powershell
git switch study-notes
git merge main
git push
```

### 暂存未完成工作

```powershell
git stash push -u -m "临时保存"
```

### 恢复未完成工作

```powershell
git stash pop
```

### 合并冲突时取消操作

```powershell
git merge --abort
```

---

## 十七、重要原则

1. `origin` 始终指向自己的 Fork。
2. `upstream` 始终指向原作者仓库。
3. `main` 尽量只用于同步原作者代码。
4. 自己的笔记和实验放在 `study-notes`。
5. 同步前先执行 `git status`。
6. 切换分支前先提交修改，或者使用 `git stash`。
7. 提交前用 `git diff --staged` 检查内容。
8. 初学阶段不要随意使用强制推送。
9. 遇到冲突先理解双方内容，不要直接删除其中一方。
10. Git 提交要小而清楚，一次提交尽量只表达一类变化。

按照这套结构，你就可以持续完成：

```text
Fork → Clone → 学习 → 记录笔记 → Commit → Push
              ↑                              ↓
              └──── 同步原作者 upstream ────┘
```
