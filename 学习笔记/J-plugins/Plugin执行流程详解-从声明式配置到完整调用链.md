---
date: 2026-09-10
branch: study-notes
learning-origin: 用户学完07-plugins后，对documentation plugin的执行流程存在多处理解障碍，问题涉及：为什么agent/command写得这么简单（PPT大纲类比）、MCP配置为何只有几行、完整调用链的触发机制、agents之间如何流转
---

# Plugin 执行流程详解——讲明白

## 问题地图

用户共提出 4 个核心问题，已合并整理如下：

1. **为什么 agent/command 写得这么简单？** —— ✅ 类比PPT大纲基本正确
2. **MCP 配置为什么只有几行？** —— 🟡 知道是声明，但不理解这几行实际做了什么
3. **完整调用链的具体触发机制** —— ❌ 不清楚 Claude 在哪个时间点读哪个文件
4. **agents 之间怎么流转** —— ❌ 不理解 code-commentator/example-generator 的触发时机

补充问题：
5. 为什么 documentation plugin 没有 `.js` / `.py` 文件？

---

## 核心前提：Plugin 文件是"声明"，不是"程序"

Plugin 目录下**所有文件**，都是"声明"（配置），不是"程序"（代码）。

| | 声明 | 程序 |
|---|---|---|
| 本质 | 描述"是什么"和"要做什么" | 描述"怎么做" |
| 执行者 | Claude 读取后自己推理执行方式 | 计算机会逐行执行 |
| 例子 | "我叫 documentation，我有 4 个命令" | `for i in files: read(i)` |

Plugin 目录下没有 `if/else`、没有循环、没有函数调用——只有"我叫啥"、"我能干啥"、"我需要啥工具"。

---

## 问题一：为什么 agent/command 写得这么简单？

**类比：PPT 大纲完全正确。**

Command 文件里的步骤列表，就是给 Claude 的"执行提纲"。Claude 看到这几行字后，分两步走：

1. **读取**这几行字
2. **用内置推理能力**把每一步翻译成具体操作，然后调用工具执行

举例：`generate-api-docs.md` 第 3 步写的是"按模块整理"。Claude 读到这四个字，自己知道怎么拆模块、用什么结构、放在哪里——不需要你写出来。

**Agent 文件也是一个道理。**

`api-documenter.md` 里写：

```yaml
name: api-documenter
description: API 文档专家
tools: Read, Write, Grep
```

这就是一个"专家名片"。Claude 看到这个名片，知道：
- 遇到 API 文档任务 → 派这个专家
- 这个专家能用什么工具 → Read、Write、Grep
- 不需要写"怎么写文档" → Claude 内置了写文档的能力

**类比：** 就像一份会议议程，只需要写"第一项：财务汇报；第二项：散会"。主持人和参会者看到议程，自己知道怎么主持、怎么发言、怎么控时。议程不需要写"怎么开场、怎么过渡"。

---

## 问题二：MCP 配置到底做了什么？

看这个文件：

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-github"],
      "env": { "GITHUB_TOKEN": "${GITHUB_TOKEN}" }
    }
  }
}
```

**这是声明，不是安装程序。**

它的意思是："这个 plugin 需要一个叫 `github` 的 MCP server，Claude 帮我调用 `npx @modelcontextprotocol/server-github` 来启动它。"

`npx` 后面跟的这个 `@modelcontextprotocol/server-github` 是一个**现成的 npm 包**，网上有人已经写好了，Claude 只需要调用它就行。

### 两种 MCP 的区别

| 类型 | 形式 | 什么时候可用 |
|---|---|---|
| 全局 MCP | 装在电脑本地，通过 Claude 设置文件配置 | 每次启动 Claude 都可用 |
| 插件 MCP | 放在 plugin 的 `mcp/` 目录下，声明式配置 | 只有这个 plugin 被激活时才可用 |

Plugin 的 MCP 配置就是一个**依赖声明**——安装 plugin 时 Claude 会把这些声明加载进来，需要时调用。

**不需要另外写 `.js` 或 `.py` 文件**，因为调用的那个 npm 包已经有人写好了，Claude 只是通过这几句声明去找到它。

---

## 问题三：完整调用链的具体触发机制

以 `/generate-api-docs` 为例，一步一步说清楚 Claude 在哪个时间点读了哪个文件：

### Step 0：安装时（已发生，不需要操作）
Claude 读取 `plugin.json`，把整个 documentation plugin 的所有声明加载到内存——包括有哪些 commands、有哪些 agents、有哪些 MCP。

### Step 1：你输入 `/generate-api-docs`
Claude 收到命令，开始查："我认识 `/generate-api-docs` 吗？"

### Step 2：Claude 查到这个命令属于 documentation plugin
它去读 `documentation/.claude-plugin/plugin.json`，确认"对，这是一个 plugin，叫 documentation，我知道它里面有什么"。

### Step 3：Claude 读命令文件
它读 `documentation/commands/generate-api-docs.md`，确认是这个名字，然后读正文，知道要做 6 步。

### Step 4：开始执行第 1 步——"扫描 API endpoints"
这是一个模糊指令。Claude 需要判断"用什么工具扫"。

它看到：
- 有 `api-documenter` agent（tools 里包含 Read、Grep）
- 有 GitHub MCP（plugin 的 mcp 目录里有）
- 当前在一个代码仓库里

Claude 自己决定：用 Read/Grep 工具扫当前代码库。如果代码在 GitHub 上，GitHub MCP 提供支持。

### Step 5：第 2-3 步 spawn agent
第 2 步"提取函数签名和注释"、第 3 步"按模块整理"——这件事正好适合 `api-documenter`。

Claude 决定 spawn 这个 subagent，把任务给它。`api-documenter` 读到自己的定义，知道可以用 Read、Write、Grep，于是开始执行。

### Step 6：第 4-6 步写文档
`api-documenter` 用 Write 工具写 Markdown 文件。

第 6 步"补示例"——Claude 看到这三个字，判断当前文档缺不缺示例。如果缺，就调用 `example-generator`；如果代码注释差，就调用 `code-commentator`。这是**动态判断**，不是"写死在第几步里"。

### Step 7：模板的使用
在"生成文档"这一步，Claude 会先读一下 `templates/` 下的模板（比如 `api-endpoint.md`），看看格式要求，然后按这个格式填充内容。

---

## 问题四：agents 之间怎么流转？

**不是"跳转"，是"调度"。**

Claude 是大脑，agents 是被派出去干活的专业人员：

```
你输入 /generate-api-docs
         ↓
Claude 分析任务 → 发现第 1-3 步需要扫描和提取 → spawn api-documenter
         ↓
api-documenter 干完回来报告
         ↓
Claude 检查结果 → 发现注释不够好 → spawn code-commentator
         ↓
Claude 检查结果 → 发现缺示例 → spawn example-generator
         ↓
所有子任务完成，汇总给你
```

**关键点：`code-commentator` 和 `example-generator` 不在命令文件里被显式调用。**

它们的触发条件是：Claude 根据实际情况自己判断——如果发现注释差就调注释专家，如果发现缺示例就调示例专家。

这就像一个项目经理，看到报告里图表不清楚，自己决定"让数据分析师重新做个图"，不需要你提前写"在第几步让数据分析师做图"。

---

## 问题五：为什么没有 `.js` / `.py` 文件？

因为 documentation plugin 所有的能力都是**声明式**的：

- Command = "步骤列表"，Claude 自己按步骤执行
- Agent = "专家定义"，Claude 自己判断派谁
- MCP = "外部工具声明"，Claude 调用现成的 npx 包

如果要做更复杂的逻辑（比如"先检查文件是否存在，不存在就跳过，存在才执行"这样的条件判断），才会需要 `.js` 或 `.py` 文件。

但 documentation plugin 场景下，Claude 的内置推理能力已经足够处理这些步骤，所以不需要写代码。

---

## 完整流程图

```
你输入 /generate-api-docs
         ↓
┌─────────────────────────────────────┐
│ Claude 查 → 属于 documentation plugin │
└─────────────────────────────────────┘
         ↓
┌─────────────────────────────────────┐
│ 读 plugin.json → 确认插件存在         │
└─────────────────────────────────────┘
         ↓
┌─────────────────────────────────────┐
│ 读 commands/generate-api-docs.md     │
│ → 知道要做这 6 步                     │
└─────────────────────────────────────┘
         ↓
第 1 步 "扫描 endpoints"
Claude 用 Read/Grep 自己干（或用 GitHub MCP）
         ↓
第 2-3 步 "提取签名、整理模块"
Claude 判断 → spawn api-documenter
         ↓
第 4 步 "生成 Markdown"
api-documenter 用 Write 工具写
         ↓
第 5-6 步 "补 schema、补示例"
Claude 动态判断 → 是否 spawn
  code-commentator / example-generator
         ↓
Templates 被参考（生成文档前读格式）
         ↓
最终文档输出给你
```

---

## 串成一条线

Plugin 的所有文件都是"声明"。Claude 安装 plugin 时把这些声明全部加载到内存，实际执行时根据用户输入动态决定调用哪些能力。

当你输入 `/generate-api-docs`：Claude 先确认这个命令属于哪个 plugin → 读命令文件知道要做哪几步 → 每一步由 Claude 自己判断用什么工具、要不要 spawn 专家 agents → agents 是被"派出去干活的专业人员"，不是写死在步骤里的。

**心智模型：** Plugin 就像一份完整的"能力清单"，Claude 是执行者，清单上写了"你能调哪些人、用哪些工具、按什么顺序"，但具体怎么干，由 Claude 自己推理决定。

---

## 自测问题

1. Plugin 文件是"程序"还是"声明"？两者的核心区别是什么？
2. 当你输入 `/generate-api-docs`，Claude **第一步**读的是哪个文件？
3. `"command": "npx"` 在 MCP 配置里是什么意思？
4. `api-documenter` 是在命令文件里被"显式调用"的吗？如果不是，是谁决定的？
5. Templates 在哪一步被参考？
