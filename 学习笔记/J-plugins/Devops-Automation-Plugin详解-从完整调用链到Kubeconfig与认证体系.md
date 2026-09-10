---
date: 2026-09-10
branch: study-notes
learning-origin: 用户在学习07-plugins过程中，先学了documentation plugin的执行流程答疑，又学了devops-automation plugin。过程中提出多个问题：hooks触发机制、AI如何推理匹配agents、MCP env里的KUBECONFIG是什么、kubeconfig文件从哪来、和GitHub TOKEN的区别、为什么AI知道什么时候调用什么
---

# Devops Automation Plugin 详解——从完整调用链到 Kubeconfig 与认证体系

## 问题地图

用户在学习过程中共提出以下问题，已按主题分类：

### A. 执行流程类
1. **完整的 /deploy 调用链是如何一步步工作的？** —— ✅ 看懂了流程，但想确认细节
2. **为什么读到"构建应用"就知道调用 deployment-specialist？** —— ❌ 不理解 AI 推理匹配机制
3. **为什么读到"health checks"就知道调用 post-deploy.js？** —— ❌ 同上
4. **AI 怎么知道"看到这句话就调那个东西"？** —— ❌ 核心困惑：智能匹配 vs 程序写死

### B. MCP 与认证类
5. **MCP 里的 `env` / `KUBECONFIG` 是什么？不填能用吗？** —— 🟡 知道有 env，但不知道干什么
6. **KUBECONFIG 里装的是什么？是 token 还是文件路径？** —— 🟡
7. **MCP 需要提前安装吗？还是用到时自动调用？** —— 🟡
8. **kubeconfig 文件从哪来？是登录 MCP 之后去弄的吗？** —— ❌ 完全不知道从哪来
9. **Kubernetes 需要 token 吗？和 GitHub TOKEN 有什么区别？** —— 🟡

### C. Agent 描述精准度类
10. **agent description 要写精准才能匹配，这个道理懂了，但想知道具体怎么才算精准** —— 🟡
11. **这和"你让员工倒水，他要知道杯子在哪水在哪"是一个道理** —— ✅ 类比理解正确

---

## 一、Devops Automation Plugin 全貌

### 与 Documentation Plugin 对比

| 维度 | Documentation Plugin | Devops Automation Plugin |
|---|---|---|
| 核心功能 | 文档生成与维护 | 部署、回滚、监控、incident 响应 |
| Commands | 4 个 | 4 个 |
| Agents | 3 个（文档专家/注释专家/示例专家） | 3 个（部署专家/事故指挥官/告警分析师） |
| Tools | Read, Write, Grep | **Read, Write, Bash, Grep** |
| MCP | GitHub | **Kubernetes** |
| Hooks | ❌ 没有 | ✅ **有**（pre-deploy.js + post-deploy.js） |
| Templates | ✅ 有 | ❌ 没有 |

**Devops 与 Documentation 的本质区别：Devops 要执行真实操作（部署、kubectl 命令），所以需要 Bash 工具；操作真实集群，所以需要 Kubernetes MCP；操作不可逆，所以需要 hooks 做安全 guardrail。**

---

## 二、Plugin 的文件结构

```
devops-automation/
├── .claude-plugin/
│   └── plugin.json                    ← 插件简历（名字、版本、描述）
├── commands/
│   ├── deploy.md                      ← /deploy 命令（6 步）
│   ├── rollback.md                    ← /rollback 命令（5 步）
│   ├── status.md                      ← /status 命令（6 步）
│   └── incident.md                    ← /incident 命令（7 步）
├── agents/
│   ├── deployment-specialist.md       ← 部署专家
│   ├── incident-commander.md          ← 事故指挥官
│   └── alert-analyzer.md              ← 告警分析师
├── mcp/
│   └── kubernetes-config.json         ← Kubernetes MCP 配置
└── hooks/
    ├── pre-deploy.js                  ← 部署前 hook（Node.js 程序）
    └── post-deploy.js                 ← 部署后 hook（Node.js 程序）
```

---

## 三、Commands——四类 Devops 操作

### /deploy（部署）

```yaml
---
name: Deploy
description: 部署到生产或预发布环境
---

执行部署流程：

1. 运行 pre-deployment checks
2. 构建应用
3. 执行测试
4. 部署到目标环境
5. 做 health checks
6. 通知团队
```

### /rollback（回滚）

```yaml
---
name: Rollback
description: 回滚到之前的稳定版本
---

1. 确认目标版本
2. 检查回滚目标是否健康
3. 执行回滚
4. 做 health checks
5. 通知团队
```

### /status（状态检查）

```yaml
---
name: System Status
description: 查看整体系统健康状态
---

1. 查询 pod 状态
2. 检查数据库连接
3. 监控 API 响应时间
4. 查看错误率
5. 检查资源使用
6. 输出整体健康判断
```

### /incident（事故响应）

```yaml
---
name: Incident Response
description: 用结构化流程处理生产事故
---

1. 创建 incident 记录
2. 判断严重级别和影响面
3. 通知 on-call
4. 收集诊断信息
5. 协调处置
6. 记录解决方案
7. 安排 post-mortem
```

---

## 四、三个 Agents——有 Bash 才能执行命令

| Agent | name | description | tools |
|---|---|---|---|
| 部署专家 | `deployment-specialist` | 负责部署流程与回滚操作 | Read, Write, **Bash**, Grep |
| 事故指挥官 | `incident-commander` | 负责 incident 响应协调 | Read, Write, **Bash**, Grep |
| 告警分析师 | `alert-analyzer` | 分析监控告警和系统指标 | Read, Grep, **Bash** |

**关键：三个 agents 都有 Bash 工具。**

Bash 让它们可以执行 `kubectl`、`docker`、`curl`、`./deploy.sh` 等命令——没有 Bash，就只能读读写写，无法操作真实的部署和集群。

---

## 五、MCP 配置——两种认证方式

### Kubernetes MCP

```json
{
  "mcpServers": {
    "kubernetes": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-kubernetes"],
      "env": {
        "KUBECONFIG": "${KUBECONFIG}"
      }
    }
  }
}
```

### GitHub MCP（对比）

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

### 两种认证方式对比

| | Kubernetes MCP | GitHub MCP |
|---|---|---|
| env 里的东西 | `KUBECONFIG`（文件路径） | `GITHUB_TOKEN`（令牌字符串） |
| 本质 | kubeconfig 文件的路径 | 一串加密字符串 |
| 文件里有什么 | 集群地址 + 用户名 + 证书/私钥 | token 值 |
| 类比 | 身份证（证明你是谁） | 临时门禁卡（卡号即通行证） |
| 从哪来 | 从 Kubernetes 集群来（下载或本地生成） | 从 GitHub 网站生成 |
| 默认路径 | `~/.kube/config` | 无默认，需环境变量 |

**核心理解：MCP 需要什么"通行证"，取决于它要连的那个系统用什么方式认证。**

---

## 六、Hooks——安全 Guardrail

### 什么是 Hook？

**Hook = 在某个动作"之前"或"之后"自动运行的脚本。**

| 文件 | 触发时机 | 作用 |
|---|---|---|
| `pre-deploy.js` | 部署前（第 1 步） | 检查 kubectl 是否安装、集群是否可连 |
| `post-deploy.js` | 部署后（第 5 步之后） | 等待 pod 就绪、跑 smoke tests |

### pre-deploy.js（部署前检查）

```javascript
#!/usr/bin/env node

async function preDeploy() {
  console.log('Running pre-deployment checks...');

  const { execSync } = require('child_process');

  // 检查 kubectl 是否安装
  try {
    execSync('which kubectl', { stdio: 'pipe' });
  } catch (error) {
    console.error('❌ kubectl not found. Please install Kubernetes CLI.');
    process.exit(1);
  }

  // 检查是否连接到集群
  try {
    execSync('kubectl cluster-info', { stdio: 'pipe' });
  } catch (error) {
    console.error('❌ Not connected to Kubernetes cluster');
    process.exit(1);
  }

  console.log('✅ Pre-deployment checks passed');
}

preDeploy().catch(error => {
  console.error('Pre-deploy hook failed:', error);
  process.exit(1);
});
```

### post-deploy.js（部署后检查）

```javascript
#!/usr/bin/env node

async function postDeploy() {
  console.log('Running post-deployment tasks...');

  const { execSync } = require('child_process');

  // 等待 pod 就绪
  console.log('Waiting for pods to be ready...');
  try {
    execSync('kubectl wait --for=condition=ready pod -l app=myapp --timeout=300s', {
      stdio: 'inherit'
    });
  } catch (error) {
    console.error('❌ Pods failed to become ready');
    process.exit(1);
  }

  console.log('Running smoke tests...');
  console.log('✅ Post-deployment tasks complete');
}
```

**这是真正的 Node.js 程序，不是声明。** 有 if/else、有条件判断、有 `process.exit(1)` 失败退出。

---

## 七、完整调用链——以 /deploy 为例

```
你输入 /deploy
         ↓
┌─────────────────────────────────────────────┐
│ Claude 读 plugin.json                        │
│ → 确认是 devops-automation 插件              │
└─────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────┐
│ 读 commands/deploy.md                       │
│ → 知道要做这 6 步                           │
└─────────────────────────────────────────────┘
         ↓
第 1 步："运行 pre-deployment checks"
         ↓
    ⬇️ Claude 推理：
    "这是部署前的检查"
    → 我有一个 hook 叫 pre-deploy.js（专门干这事）
    → 调用 pre-deploy.js（Node.js 程序）
    → 如果 kubectl 没装或集群连不上 → process.exit(1) → 部署终止
         ↓
第 2 步："构建应用"
         ↓
    ⬇️ Claude 推理：
    "构建应用"是部署流程的子步骤
    → deployment-specialist 的 description："负责部署流程与回滚操作"
    → 匹配 → 调用 deployment-specialist
    → 它用 Bash 工具执行构建命令（docker build 等）
         ↓
第 3 步："执行测试"
         ↓
    ⬇️ Claude 推理：
    "测试"也是部署流程的一部分
    → 还是 deployment-specialist
    → 它用 Bash 工具执行测试命令
         ↓
第 4 步："部署到目标环境"
         ↓
    ⬇️ Claude 推理：
    "部署"是核心操作
    → deployment-specialist + Kubernetes MCP
    → 它用 Bash 调用 kubectl，结合 Kubernetes MCP 操作集群
         ↓
第 5 步："做 health checks"
         ↓
    ⬇️ Claude 推理：
    "health checks" = 部署后确认服务健康
    → post-deploy.js 专门干这个（部署后运行）
    → 调用 post-deploy.js（等待 pod 就绪、smoke tests）
         ↓
第 6 步："通知团队"
         ↓
    Claude 用 Write 工具写通知、发消息
```

---

## 八、AI 推理匹配机制——核心答疑

### 问题：为什么读到"构建应用"就知道调用 deployment-specialist？

**不是"自动关联"，是"AI 推理出来的"。**

```
Command 第 2 步："构建应用"
         ↓
Claude 读 deployment-specialist 的 description：
"负责部署流程与回滚操作"
         ↓
Claude 推理：
"构建应用"是部署流程中的一个步骤
deployment-specialist 负责部署流程
意思对上了
         ↓
匹配 → 调用它
```

### 问题：为什么读到"health checks"就知道调用 post-deploy.js？

```
Command 第 5 步："做 health checks"
         ↓
Claude 看到 hooks/ 目录里有 post-deploy.js
"post-deploy" = "部署之后"
         ↓
Claude 推理：
"health checks"是部署后要确认健康
post-deploy.js = 部署之后自动运行的脚本
意思对上了
         ↓
匹配 → 调用它
```

### 问题：这是智能匹配，和程序写死的区别是什么？

| | 程序（if/else） | AI 推理匹配 |
|---|---|---|
| 匹配方式 | `if (步骤 == "构建应用") { 调 deployment-specialist }` | 理解"构建应用"的意思 → 找最相关的 agent |
| 依赖 | 程序员把所有情况都想到并写出来 | 程序员只需要写清楚 agent 负责什么 |
| 灵活性 | 只能处理写好的情况 | 能处理没写到的、模糊的情况 |

**类比：就像"衣服价格"。**

客户问："这件衣服多少钱？"

你的大脑不是查表找到"衣服价格"对应"查数据库"——你是**理解了这个问题的意思**，然后自己决定：
- 先想：这说的是哪件衣服？
- 如果有图片就看图片
- 如果没有可能要问客户
- 然后去查
- 最后报价格

AI 读 Plugin 是一样的——不是查表，是**理解意思后匹配**。

---

## 九、Agent Description 为什么要写精准？

**Description 写得越精准，AI 匹配越准。**

| 写法 | description | 效果 |
|---|---|---|
| ❌ 差 | `tools: Bash` | 只说了能用什么工具，但没说干什么 |
| ✅ 好 | `负责部署流程与回滚操作` | 说清楚了干什么，AI 知道什么时候派这个专家 |

**类比：你指挥员工。**

- ❌ "你负责工作" → 员工不知道干什么
- ✅ "你负责倒茶" → 员工知道倒茶要用杯子、烧水、倒水

Plugin 的 agent description 就是在告诉 AI：**"你负责什么"**。

---

## 十、MCP 需要提前安装吗？

**不需要提前手动安装。**

```
/deploy
         ↓
第 4 步需要 Kubernetes 能力
         ↓
Claude 读 mcp/kubernetes-config.json
看到："command": "npx", "args": ["@modelcontextprotocol/server-kubernetes"]
         ↓
Claude 执行：npx @modelcontextprotocol/server-kubernetes
         ↓
npx 自动下载这个包（如果本地没有缓存）
启动 MCP server
         ↓
Claude 通过 MCP 连接 Kubernetes 集群
```

**安装 plugin = 把 plugin 的声明文件加载进来（commands、agents、mcp 配置）。**
**MCP server 本身 = 用到时通过 npx 自动下载和启动。**

---

## 十一、Kubeconfig 文件从哪来？

### kubeconfig 不是什么？

- **不是 token**（GitHub 用 token，Kubernetes 不用 token）
- **不是 MCP 提供的**（MCP 只是 Claude 和集群之间的电话机）
- **不是需要注册什么账号才能拿到的**

### kubeconfig 从哪来？

**从 Kubernetes 集群来。** 你总得有一个 Kubernetes 集群，才能连它吧？

| 来源 | 说明 | 获取方式 |
|---|---|---|
| Docker Desktop | 开启 K8s 功能就有 | 设置 → Kubernetes → 开启，自动生成 `~/.kube/config` |
| minikube | 本地迷你集群 | `minikube start` 自动生成 |
| 云服务商（DigitalOcean/AWS/GCP/Azure） | 云上集群 | 登录控制台 → 下载 kubeconfig 文件 |

### kubeconfig 文件长什么样？

```yaml
apiVersion: v1
kind: Config
clusters:
- cluster:
    certificate-authority-data: 很长一串证书
    server: https://111.222.333.444:6443   # 集群地址
  name: my-cluster
contexts:
- context:
    cluster: my-cluster
    user: my-user
  name: my-cluster
current-context: my-cluster
users:
- name: my-user
  user:
    client-certificate-data: 证书
    client-key-data: 私钥
```

里面没有密码，但有**证书和私钥**——证书证明身份，私钥做加密验证。

### 本质：两种认证方式的区别

```
你要进一栋楼：

Kubernetes（kubeconfig）：
  你有一张本地身份证（kubeconfig 文件）
  里面有照片（证书）、名字（用户名）、指纹（私钥）
  门禁读文件 → 验证身份 → 让你进

GitHub（TOKEN）：
  你有一张临时门禁卡号（ghp_xxx）
  卡号存在系统里，验卡号是否有效
  有效 → 让你进
```

---

## 十二、为什么 Devops 需要 Hooks，Documentation 不需要？

**Documentation 是"生成内容"，Claude 自己能判断内容质量。**

**Devops 是"执行操作"，一旦执行就可能造成不可逆后果。**

Deploy 操作如果中途失败：
- 代码可能已经部署上去了
- 数据库可能已经迁移了
- 状态可能已经变了

所以需要：
- **部署前**（pre-deploy.js）：检查环境是否 OK，不 OK 就停止，不让部署开始
- **部署后**（post-deploy.js）：检查是否真的成功了，成功了才通知团队

**Hooks 是安全 guardrail，不是用来做业务的。**

---

## 十三、Plugin 里哪些是"声明"，哪些是"程序"？

| 文件类型 | 类型 | 说明 |
|---|---|---|
| `plugin.json` | 声明 | 元数据，Claude 读它知道插件存在 |
| `commands/*.md` | 声明 | 步骤列表，Claude 按步骤推理执行 |
| `agents/*.md` | 声明 | 专家名片，Claude 动态调度 |
| `mcp/*.json` | 声明 | 外部依赖声明，Claude 按需调用 |
| `templates/*` | 声明 | 输出格式参考 |
| `hooks/*.js` | **程序** | 真正的 Node.js 代码，有 if/else、有退出逻辑 |

**只有 hook 的 `.js` 文件是真正的程序——写死了检查逻辑，失败就 `process.exit(1)`。**

Plugin 里其他所有文件都是"声明"。

---

## 串成一条线

Devops Automation Plugin 的执行分为两层：

**声明层**（command / agent / MCP）：
- 你描述"是什么"，Claude 推理"怎么做"
- Command 的步骤 + Agent 的 description → AI 动态匹配
- MCP 配置告诉 AI 需要什么外部能力

**程序层**（hook 的 .js 文件）：
- 写死的检查逻辑，失败就退出，不让部署继续
- 这是安全 guardrail，不是业务逻辑

**AI 的智能匹配机制：**
- 不是查表，不是 if/else
- 是理解"这句话的意思"去匹配"那个组件负责什么"
- Description 写得越精准，匹配越准

**两种 MCP 认证方式：**
- Kubernetes = kubeconfig 文件（证书认证）
- GitHub = TOKEN 字符串（令牌认证）

---

## 自测问题

1. `KUBECONFIG` 环境变量里装的是什么？是 token 还是文件路径？
2. 当你执行 `/deploy` 时，Kubernetes MCP server 是在**安装 plugin 时**就启动了，还是在**实际用到那一步时**才启动的？
3. Claude 读到"执行测试"调用了 `deployment-specialist`，这是因为**程序写死了**，还是因为 **AI 推理出来的**？
4. kubeconfig 文件是从 Kubernetes MCP 下载来的，还是从 Kubernetes 集群来的？
5. 如果你本地没有 `~/.kube/config` 文件，要连云服务商的 Kubernetes，kubeconfig 文件从哪来？
6. Plugin 里哪类文件是"程序"（真正的代码，有 if/else），哪类是"声明"？
7. 为什么 devops 需要 hooks，而 documentation 不需要？
