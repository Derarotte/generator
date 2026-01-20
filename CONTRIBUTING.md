# 贡献指南

感谢你对本项目的关注！本文档将帮助你了解如何参与项目开发。

## 参与方式

### 1. 报告问题

在 [GitHub Issues](https://github.com/Derarotte/generator/issues) 提交问题时，请包含：

- 问题描述
- 复现步骤
- 期望行为
- 实际行为
- 环境信息（OS、Python版本等）

### 2. 提交功能建议

创建 Issue 并添加 `enhancement` 标签，描述：

- 功能需求
- 使用场景
- 建议的实现方式

### 3. 提交代码

#### 步骤

1. Fork 仓库
2. 创建功能分支: `git checkout -b feature/your-feature`
3. 编写代码和测试
4. 提交: `git commit -m "feat: your feature"`
5. 推送: `git push origin feature/your-feature`
6. 创建 Pull Request

#### PR 要求

- 清晰的标题和描述
- 通过所有测试
- 遵循代码规范
- 必要时更新文档

### 4. 添加新模块

这是最受欢迎的贡献方式！

1. 阅读 [模块开发指南](./module-development.md)
2. 在 `templates/` 下创建模块目录
3. 编写 `module.yaml` 和模板文件
4. 测试生成的项目
5. 提交 PR

## 开发规范

详见 [开发者指南](./DEVELOPER.md)

## 行为准则

- 尊重他人
- 建设性讨论
- 接受反馈

## 许可证

提交代码即表示同意以 MIT 许可证开源。
