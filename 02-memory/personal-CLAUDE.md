# 我的开发偏好

## 关于我

- **经验水平**: 8 年全栈开发经验
- **偏好语言**: TypeScript、Python
- **沟通风格**: 直接、清晰、带例子
- **学习风格**: 喜欢图示和代码结合

## 代码偏好

### 错误处理

偏好显式错误处理，尽量使用清晰的 `try-catch` 和有意义的错误信息。
避免过于泛化的错误；排查时尽量保留日志上下文。

### 注释

注释优先解释 **WHY**，不要只是重复代码在做什么。
更适合解释业务逻辑或不明显的决策。

### 测试

偏好 TDD。
尽量先写测试，再实现。
测试关注行为，而不是实现细节。

### 架构

偏好模块化、低耦合设计。
重视可测试性和职责分离。

## 调试偏好

- `console.log` 建议带 `[DEBUG]` 前缀
- 日志包含函数名和关键变量
- 能给 stack trace 时尽量给
- 日志里尽量保留时间戳

## 沟通方式

- 复杂概念先给例子再讲理论
- 需要时提供 before / after 代码片段
- 长回答最后给一个简要总结

## 项目组织方式

我常用的项目结构：

```text
project/
  ├── src/
  │   ├── api/
  │   ├── services/
  │   ├── models/
  │   └── utils/
  ├── tests/
  ├── docs/
  └── docker/
```

## 工具链

- **IDE**: VS Code + vim keybindings
- **终端**: Zsh + Oh-My-Zsh
- **格式化**: Prettier（100 字符换行）
- **Lint 工具**: ESLint + airbnb config
- **测试框架**: Jest + React Testing Library
