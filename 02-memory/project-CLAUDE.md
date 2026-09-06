# 项目配置

## 项目概览

- **项目名称**: E-commerce Platform
- **技术栈**: Node.js, PostgreSQL, React 18, Docker
- **团队规模**: 5 名开发者
- **截止时间**: 2025 年 Q4

## 架构

@docs/architecture.md
@docs/api-standards.md
@docs/database-schema.md

## 开发规范

### 代码风格

- 使用 Prettier
- 使用 ESLint + airbnb config
- 最大行长 100
- 2 空格缩进

### 命名约定

- **文件**: kebab-case
- **类**: PascalCase
- **函数/变量**: camelCase
- **常量**: UPPER_SNAKE_CASE
- **数据库表**: snake_case

### Git 工作流

- 分支命名：`feature/description` 或 `fix/description`
- 提交信息遵循 conventional commits
- 合并前需要 PR
- 所有 CI/CD 检查必须通过
- 至少 1 个 approval

### 测试要求

- 最低 80% 覆盖率
- 关键路径必须有测试
- unit tests 使用 Jest
- E2E 用 Cypress
- 文件命名：`*.test.ts` 或 `*.spec.ts`

### API 规范

- 使用 RESTful endpoints
- JSON request / response
- 正确使用 HTTP status code
- API 统一带版本：`/api/v1/`
- 所有 endpoint 要有示例文档

### 数据库

- schema 变更必须走 migration
- 不允许硬编码凭证
- 使用 connection pooling
- 开发环境开启 query logging
- 定期备份

### 部署

- 基于 Docker 部署
- 使用 Kubernetes 编排
- 采用 blue-green deployment
- 失败自动回滚
- deploy 前先跑数据库迁移

## 常用命令

| 命令 | 用途 |
|---------|---------|
| `npm run dev` | 启动开发服务 |
| `npm test` | 运行测试 |
| `npm run lint` | 检查代码风格 |
| `npm run build` | 生产构建 |
| `npm run migrate` | 执行数据库迁移 |

## 团队联系人

- 技术负责人: Sarah Chen (`@sarah.chen`)
- 产品经理: Mike Johnson (`@mike.j`)
- DevOps: Alex Kim (`@alex.k`)

## 已知问题与临时方案

- PostgreSQL 连接池高峰期限制为 20
- 临时方案：实现 query queuing
- Safari 14 对 async generators 有兼容性问题
- 临时方案：使用 Babel transpiler

## 相关项目

- Analytics Dashboard: `/projects/analytics`
- Mobile App: `/projects/mobile`
- Admin Panel: `/projects/admin`
