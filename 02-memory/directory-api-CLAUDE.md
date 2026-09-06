# API 模块规则

这个文件用于补充根目录 `CLAUDE.md`，作用范围是 `/src/api/` 下的内容。两者会拼接加载，不是整份覆盖关系。

## API 专属规范

### 请求校验

- 使用 Zod 做 schema validation
- 所有输入都必须校验
- 校验失败返回 400
- 错误信息尽量提供字段级细节

### 鉴权

- 所有 endpoint 默认需要 JWT token
- token 放在 `Authorization` header
- token 默认 24 小时过期
- 实现 refresh token 机制

### 响应格式

所有成功响应统一遵循下面的结构：

```json
{
  "success": true,
  "data": { /* actual data */ },
  "timestamp": "2025-11-06T10:30:00Z",
  "version": "1.0"
}
```

错误响应：

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "User message",
    "details": { /* field errors */ }
  },
  "timestamp": "2025-11-06T10:30:00Z"
}
```

### 分页

- 使用 cursor-based pagination
- 返回 `hasMore`
- 单页最大 100
- 默认每页 20

### 限流

- 登录用户每小时 1000 次
- 公共接口每小时 100 次
- 超限返回 429
- 包含 `retry-after` header

### 缓存

- 使用 Redis 做 session caching
- 默认缓存 5 分钟
- 写操作后主动失效
- cache key 带资源类型标签
