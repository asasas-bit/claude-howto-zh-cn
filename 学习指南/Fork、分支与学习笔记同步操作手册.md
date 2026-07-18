# Fork、分支与学习笔记同步操作手册

> 适用于当前仓库 `claude-howto-zh-cn`。
> 用途：忘记怎样保存笔记、上传 GitHub 或同步原作者时，直接打开这篇照着操作。

---

## 一、先记住最重要的一句话

这个仓库里真正需要合在一起的，只有两类内容：

```text
原作者的项目更新 + 我自己的学习笔记
```

`Fork` 不是第三类内容。它只是这个仓库在**我自己的 GitHub 账号中保存的一份副本**。

当前采用的管理方式是：

- `main`：接收原作者更新，不放个人笔记。
- `study-notes`：保存个人笔记，也接收 `main` 带来的原作者更新。
- `学习指南/`：在 `study-notes` 中保存我的 Markdown 学习笔记。

---

## 二、当前仓库中的名称分别代表什么

### 1. `upstream`：原作者的 GitHub 仓库

```text
https://github.com/lhfer/claude-howto-zh-cn.git
```

它是原作者发布更新的地方。我通常只从这里获取更新，不向这里上传。

可以把它理解为：

```text
upstream = 原作者
```

### 2. `origin`：我自己的 GitHub Fork

```text
https://github.com/asasas-bit/claude-howto-zh-cn.git
```

我执行 `git push` 时，内容上传到这里。

可以把它理解为：

```text
origin = 我的 GitHub 仓库
```

### 3. 本地仓库：电脑里的这个文件夹

```text
D:\cc\claude-howto-zh-cn
```

我在 VSCode 中看到和修改的文件，都在本地仓库中。只有经过 `commit` 和 `push`，修改才会保存到我的 GitHub Fork。

### 4. `main`：同步原作者的分支

`main` 尽量保持干净，只用来接收原作者更新。

不要在 `main` 中写个人学习笔记。这样以后同步原作者时不容易混乱。

### 5. `study-notes`：我的学习分支

我自己的学习笔记放在这个分支中。

只要执行下面的命令后显示 `study-notes`：

```powershell
git branch --show-current
```

就可以直接在 `学习指南/` 或 `学习笔记/` 中新建或修改 Markdown 文件。

---

## 三、分支不是文件夹

这是最容易混淆的地方。

`study-notes` 不是电脑中的一个文件夹。它是**整个仓库的一套版本记录**。

```text
仓库
├── main 分支：原作者内容
└── study-notes 分支：原作者内容 + 我的学习笔记
```

`学习指南/` 和 `学习笔记/` 才是真正的文件夹。为了以后查找方便，建议这样区分：

| 文件夹 | 保存内容 |
| --- | --- |
| `学习指南/` | Git、Fork、分支等可以反复查阅的操作手册 |
| `学习笔记/` | 课程学习、项目阅读和动手实践产生的日常笔记 |

```text
claude-howto-zh-cn/
├── 学习指南/
│   ├── 从0建立Fork学习循环.md
│   └── Fork、分支与学习笔记同步操作手册.md
└── 学习笔记/
    ├── 00-学习计划.md
    └── 以后新建的其他笔记.md
```

当我位于 `study-notes` 分支时，在这两个目录中创建文件并提交，这些文件就属于 `study-notes`。

切换到 `main` 后，这些已经提交到 `study-notes` 的个人笔记通常不会显示，因为它们不属于 `main`。

### Git 不跟踪空文件夹

如果刚刚新建的 `学习笔记/` 还是空的，Git 和 VSCode 通常不会显示任何状态标记。这不是出错，而是因为 Git 只跟踪文件，不单独跟踪空文件夹。

因此，空的 `学习笔记/`：

- 不会显示 `U`。
- 不能单独执行提交。
- 不会出现在 GitHub 中。

等里面出现第一篇真实文件，例如：

```text
学习笔记/00-学习计划.md
```

这个文件显示 `U` 后，再执行 `git add`、`git commit` 和 `git push`，`学习笔记/` 才会随文件一起出现在 GitHub 中。

---

## 四、整套关系图

```text
原作者 GitHub
upstream/main
      │
      │ git fetch upstream
      │ git merge --ff-only upstream/main
      ▼
本地 main
      │
      │ git push origin main
      ▼
我的 GitHub Fork
origin/main


本地 main
      │
      │ 在 study-notes 中执行 git merge main
      ▼
本地 study-notes
（原作者内容 + 我的学习笔记）
      │
      │ git push
      ▼
我的 GitHub Fork
origin/study-notes
```

因此，最终我的 Fork 中会有两个分支：

| GitHub 上的分支 | 保存的内容 |
| --- | --- |
| `origin/main` | 与原作者同步的项目内容 |
| `origin/study-notes` | 原作者项目内容和我的学习笔记 |

---

## 五、平时怎样新建、保存和上传学习笔记

### 第一步：确认自己在学习分支

```powershell
git branch --show-current
```

如果显示：

```text
study-notes
```

就可以继续。

如果显示 `main`，切换到学习分支：

```powershell
git switch study-notes
```

### 第二步：在对应目录中写内容

操作方法、长期速查内容放进 `学习指南/`：

```text
学习指南/我的新指南.md
```

课程、项目阅读和实践记录放进 `学习笔记/`：

```text
学习笔记/
├── 01-Claude-Code基础.md
├── 02-斜杠命令学习笔记.md
├── 03-Skills学习笔记.md
└── 问题与解决记录.md
```

### 第三步：查看发生了哪些变化

```powershell
git status
```

常见提示：

- VSCode 中的 `U` 与 `git status --short` 中的 `??` 都表示 `Untracked`：这是尚未执行 `git add` 的新文件。
- `Changes not staged`：文件修改了，但还没有加入暂存区。
- `Changes to be committed` 或 `A`：文件已经执行 `git add`，正在等待 `commit`。
- `working tree clean`：目前没有尚未提交的修改。

一个新文件的完整状态变化是：

```text
U 或 ?? → git add → A → git commit → 状态标记消失 → git push → 上传到 Fork
```

注意：`commit` 之后标记消失，只代表内容已经记录在本地分支；必须再执行 `git push`，内容才会上传到 GitHub。

### 第四步：把笔记加入暂存区

添加整个学习指南目录：

```powershell
git add 学习指南
```

添加整个学习笔记目录：

```powershell
git add 学习笔记
```

也可以只添加某一篇：

```powershell
git add "学习指南/我的新笔记.md"
```

如果两个目录同时有需要保存的内容，可以一次加入暂存区：

```powershell
git add 学习指南 学习笔记
```

检查即将提交的内容：

```powershell
git diff --staged
git status
```

### 第五步：在本地创建提交

```powershell
git commit -m "docs: 更新学习笔记"
```

`commit` 的含义是：

```text
把当前修改正式记录在本地 study-notes 分支中
```

只执行 `git add` 还不算提交，必须再执行 `git commit`。

### 第六步：上传到自己的 GitHub Fork

```powershell
git push
```

因为 `study-notes` 已经关联到 `origin/study-notes`，所以这里的 `git push` 相当于：

```text
本地 study-notes
        ↓
我的 GitHub Fork 中的 study-notes
```

它不会上传到原作者仓库，也不会自动进入 `main`。

### 平时保存笔记的固定命令

```powershell
git switch study-notes
git status
git add 学习指南
git diff --staged
git commit -m "docs: 更新学习笔记"
git push
```

---

## 六、原作者更新后，怎样同步到我的仓库

同步时按照固定顺序操作：

```text
先更新 main，再把 main 合并进 study-notes
```

### 同步前：先保存正在写的笔记

执行：

```powershell
git status
```

如果有尚未提交的笔记，先提交并推送：

```powershell
git add 学习指南
git commit -m "docs: 保存同步前的学习笔记"
git push
```

### 第一步：切换到 `main`

```powershell
git switch main
```

### 第二步：获取原作者的更新

```powershell
git fetch upstream
```

这一步只是把原作者的最新提交信息下载到本地，还不会修改当前文件。

### 第三步：更新本地 `main`

```powershell
git merge --ff-only upstream/main
```

现在原作者的更新进入了本地 `main`。

### 第四步：更新我的 Fork 中的 `main`

```powershell
git push origin main
```

现在下面三处的 `main` 基本一致：

```text
原作者 upstream/main
本地 main
我的 Fork origin/main
```

### 第五步：把原作者更新带入学习分支

```powershell
git switch study-notes
git merge main
```

这次合并的结果是：

```text
study-notes
= 原作者的最新项目内容
+ 我的学习笔记
```

### 第六步：上传更新后的学习分支

```powershell
git push
```

现在我的 Fork 中的 `origin/study-notes` 也同时拥有原作者最新内容和我的笔记。

### 同步作者的完整固定命令

确认自己的笔记已经提交后，执行：

```powershell
git switch main
git fetch upstream
git merge --ff-only upstream/main
git push origin main

git switch study-notes
git merge main
git push
```

---

## 七、五个容易混淆的问题

### 问题 1：我把文件夹复制进仓库，它会自动属于当前分支吗？

不会立即属于任何提交。

复制进来的文件最开始只是本地文件。必须依次执行：

```powershell
git add 学习指南
git commit -m "docs: 添加学习指南"
```

它才会正式记录在当前分支。

因此，在提交前一定先确认：

```powershell
git branch --show-current
```

### 问题 2：执行 `git push` 后，笔记会到哪里？

如果当前位于 `study-notes`，而且它跟踪的是 `origin/study-notes`，那么：

```powershell
git push
```

会把笔记上传到：

```text
我的 Fork → study-notes 分支
```

不会上传给原作者。

可以用下面的命令检查跟踪关系：

```powershell
git branch -vv
```

正确关系应类似：

```text
main         [origin/main]
study-notes  [origin/study-notes]
```

### 问题 3：作者更新、我的 Fork 和笔记是不是三套更新？

不是。

只有两类内容：

1. 原作者的项目更新。
2. 我的学习笔记。

我的 Fork 只是 GitHub 上的存放位置，其中：

```text
origin/main        保存原作者更新
origin/study-notes 保存原作者更新 + 我的学习笔记
```

### 问题 4：为什么新建了 `学习笔记/`，却一直没有显示 `U`？

因为它是空文件夹。

`U` 表示 `Untracked`，只会标记尚未被 Git 跟踪的**文件**。Git 不单独跟踪空文件夹，所以一个空的 `学习笔记/` 不会显示 `U`，也不能提交。

先在里面创建一篇实际文件：

```text
学习笔记/00-学习计划.md
```

随后这个 Markdown 文件就会显示 `U`。提交时执行：

```powershell
git add 学习笔记
git status
git commit -m "docs: 添加第一篇学习笔记"
git push
```

### 问题 5：`学习指南/` 和 `学习笔记/` 同时有修改，怎样一起提交？

一次 `git add` 可以接收多个文件或目录。确认当前分支为 `study-notes` 后执行：

```powershell
git add 学习指南 学习笔记
git status
git diff --staged
git commit -m "docs: 更新学习指南和学习笔记"
git push
```

这会产生一个提交，同时包含两个目录中已经暂存的修改。`git status` 和 `git diff --staged` 用于在提交前确认没有误加其他文件。

---

## 八、如果忘记自己做到哪一步

先不要继续输入 `commit`、`push` 或 `merge`，执行这三个检查：

```powershell
git branch --show-current
git status
git branch -vv
```

它们分别回答：

| 命令 | 回答的问题 |
| --- | --- |
| `git branch --show-current` | 我现在在哪个分支？ |
| `git status` | 哪些文件改了？是否已经 add 或 commit？ |
| `git branch -vv` | 本地分支对应 GitHub 上的哪个分支？ |

还可以检查两个远程仓库：

```powershell
git remote -v
```

当前应当看到：

```text
origin   → asasas-bit/claude-howto-zh-cn
upstream → lhfer/claude-howto-zh-cn
```

---

## 九、遇到合并冲突怎么办

当原作者和我修改了同一个文件的同一位置，执行：

```powershell
git merge main
```

可能产生冲突。

先查看冲突文件：

```powershell
git status
```

如果知道怎样处理，可以在 VSCode 中选择保留哪部分内容，处理完成后执行：

```powershell
git add 冲突文件
git commit -m "merge: 解决上游更新冲突"
git push
```

如果暂时不知道如何处理，不要随便删除内容，可以取消本次合并：

```powershell
git merge --abort
```

取消后再查资料或寻求帮助。

不要在不清楚后果时使用：

```text
git reset --hard
git push --force
```

这些命令可能造成内容丢失。

---

## 十、最短速查表

### 写完笔记，上传到我的 Fork

```powershell
git switch study-notes
git add 学习笔记
git commit -m "docs: 更新学习笔记"
git push
```

### 两个目录同时有修改

```powershell
git switch study-notes
git add 学习指南 学习笔记
git status
git diff --staged
git commit -m "docs: 更新学习指南和学习笔记"
git push
```

### 获取原作者更新，并合并到笔记分支

```powershell
git switch main
git fetch upstream
git merge --ff-only upstream/main
git push origin main
git switch study-notes
git merge main
git push
```

### 不确定当前状态

```powershell
git branch --show-current
git status
git branch -vv
git remote -v
```

---

## 十一、以后只遵守这五条规则

1. 写笔记前，确认当前分支是 `study-notes`。
2. 操作手册放进 `学习指南/`，日常学习记录放进 `学习笔记/`。
3. `git add`、`git commit`、`git push` 分别代表准备、记录、上传，缺一不可。
4. 同步作者时，先更新 `main`，再把 `main` 合并进 `study-notes`。
5. 不把 `study-notes` 反向合并到 `main`。

最终形成的循环是：

```text
在 study-notes 写笔记
        ↓
commit
        ↓
push 到我的 Fork
        ↓
原作者有更新时，先更新 main
        ↓
把 main 合并进 study-notes
        ↓
继续学习和写笔记
```
