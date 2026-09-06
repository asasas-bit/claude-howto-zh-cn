<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../resources/logos/claude-howto-logo-dark.svg">
  <img alt="Claude How To" src="../resources/logos/claude-howto-logo.svg">
</picture>

# EPUB / 网站构建脚本与本地化校验脚本

这个目录现在主要包含三类脚本：

- `build_epub.py`：把仓库内的 Markdown 文档打包成 EPUB
- `build_website.py`：把同一套 Markdown 文档生成静态网站
- `validate_localization.py`：校验中文本土化过程中是否把可执行标识、链接或配置翻坏

---

## `build_epub.py`

用于把整个指南打包成 EPUB 电子书。

当前默认会优先使用仓库里的固定封面图：

`assets/cover/epub-cover-official.png`

如果这个文件存在，就直接作为 EPUB 封面；如果不存在，才回退到脚本自动生成封面。

### 功能

- 按目录结构组织章节
- 通过本地 `mmdc` CLI 把 Mermaid 图渲染成图片，不依赖网络服务
- 对重复 Mermaid 图做缓存，每个唯一图表只渲染一次
- 生成封面
- 处理内部 Markdown 链接
- 任一图表无法渲染时让构建失败，避免发布缺图 EPUB

### 依赖

- Python 3.10+
- [uv](https://github.com/astral-sh/uv)
- `PATH` 中可用的 [`mmdc`](https://github.com/mermaid-js/mermaid-cli)：`npm install -g @mermaid-js/mermaid-cli`

`mmdc` 依赖的 Chromium 在 arm64 开发机上没有可用构建，因此 EPUB 不再属于 pre-commit 门禁。macOS arm64 用户应让 GitHub Actions 的 EPUB 构建 jobs 完成这项验证。

### 快速开始

```bash
uv run scripts/build_epub.py
```

### 常见选项

```text
usage: build_epub.py [-h] [--root ROOT] [--output OUTPUT] [--verbose]
                     [--mmdc-path MMDC_PATH] [--lang {zh}]
                     [--puppeteer-config PUPPETEER_CONFIG]
```

```bash
# 查看详细日志
uv run scripts/build_epub.py --verbose

# 自定义输出位置
uv run scripts/build_epub.py --output ~/Desktop/claude-guide.epub

# 显式指定 mmdc
uv run scripts/build_epub.py --mmdc-path ./node_modules/.bin/mmdc

# 容器或 CI 中传入 Puppeteer 配置
uv run scripts/build_epub.py --puppeteer-config /tmp/puppeteer-ci.json
```

---

## `validate_localization.py`

用于在中文本土化过程中做“翻译后验活”，避免这些问题：

- 内部 Markdown 链接失效
- YAML frontmatter 被改坏
- JSON / YAML 无法解析
- shell 脚本语法损坏
- 关键命令名、字段名、环境变量名、plugin manifest 标识被误改

### 快速开始

```bash
uv run python scripts/validate_localization.py
```

### 它会检查什么

- Markdown 相对链接
- frontmatter 合法性
- `.json` / `.yml` / `.yaml` 语法
- `*.sh` 的 `bash -n`
- 关键 protected tokens

### 什么时候运行

- 每次大规模翻译或重写之后
- 每次修改 `SKILL.md`、subagent、slash command 或 plugin manifest 之后
- 每次准备提交前
- 每次同步上游变更后

---

## 本地开发

```bash
# 创建虚拟环境
uv venv

# 激活并安装依赖
source .venv/bin/activate
uv pip install -r scripts/requirements-dev.txt

# 运行全部测试
pytest scripts/tests/ -v

# 运行本地化校验
uv run python scripts/validate_localization.py

# 构建 EPUB（需要本机可用的 mmdc；arm64 请交给 CI）
uv run scripts/build_epub.py --lang zh
```

---

## 常见问题

**提示 `mmdc not found`**

先运行 `npm install -g @mermaid-js/mermaid-cli`，或通过 `--mmdc-path` 指向现有二进制。arm64 开发机建议直接查看 GitHub Actions 的 EPUB 构建 jobs。

**容器或 CI 中 Chromium sandbox 启动失败**

把 `{"args":["--no-sandbox","--disable-setuid-sandbox"]}` 写入 JSON 文件，再通过 `--puppeteer-config` 传给构建脚本。

**本地化校验失败**
优先检查：

- 是否把 `/optimize`、`/pr`、`claude -p` 这类命令改坏了
- 是否把 `allowed-tools`、`tools`、`model`、`env` 这类字段翻译掉了
- 是否删掉了 `GITHUB_TOKEN`、`mcpServers`、`license` 等受保护标识

**中文内容导致拼写检查报错**
仓库已对中文字符做了忽略处理；如果仍然报错，多半是英文术语或项目名新增了未收录词条。

---

## `build_website.py`

用于把同一套 Markdown 源文档生成一个适合直接部署的静态网站。

它和 `build_epub.py` 的关系可以简单理解为：

- EPUB：面向离线阅读 / 打包分发
- Website：面向浏览器访问 / GitHub Pages 部署

两者都把 `.md` 作为唯一内容源，改完 Markdown 后重新运行脚本即可。

### 功能

- 为每个 Markdown 页面生成对应 HTML
- 把内部 `.md` 链接自动重写成站点内的 `.html`
- 把脚本、JSON、配置等非 Markdown 文件链接重写成 GitHub 源码链接
- 自托管 Mermaid、Tailwind、Inter、JetBrains Mono 等前端资源，不依赖运行时 CDN
- 适合直接部署到 GitHub Pages

### 快速开始

```bash
# 生成根目录中文站点到 ./site/
uv run scripts/build_website.py

# 本地预览
python -m http.server --directory site 8080
```

然后浏览器打开 `http://localhost:8080`。

### 常见选项

```text
usage: build_website.py [-h] [--root ROOT] [--output OUTPUT]
                        [--lang {en,vi,zh,ja,uk}] [--repo-url REPO_URL]
                        [--branch BRANCH] [--verbose]
```

默认生成的“查看源码”和非 Markdown 文件链接指向中文仓库
`lhfer/claude-howto-zh-cn`；维护其他 fork 时可通过 `--repo-url` 覆盖。

### GitHub Pages 部署

仓库会额外提供 `.github/workflows/pages.yml`：

- 当 Markdown 或网站生成脚本变更时自动构建
- 把输出目录 `site/` 发布到 GitHub Pages

如果你要在自己的中文 fork 上启用它，需要在仓库设置里把 GitHub Pages 的 Source 切到 **GitHub Actions**。

### 依赖和缓存

网站构建依赖：

- `jinja2`
- `markdown`
- `beautifulsoup4`

首次构建时还会把 Tailwind CLI、Mermaid、字体文件下载到：

`scripts/.vendor-cache/`

这个目录已经加入 `.gitignore`，不会污染仓库提交历史。
