# 贡献指南

感谢你对 repo-doctor 的关注！欢迎通过以下方式贡献：

## 报告 Bug

1. 在 [Issues](https://github.com/YOUR_USERNAME/repo-doctor/issues) 中搜索是否已有相关 Issue
2. 如果没有，创建新 Issue，包含：
   - 问题描述
   - 复现步骤
   - 期望行为 vs 实际行为
   - 运行环境（Python 版本、OS 等）

## 提交 PR

1. Fork 本仓库
2. 创建功能分支：`git checkout -b feat/your-feature`
3. 提交修改：遵循 `type(scope): subject` 格式
4. 确保测试通过：`pytest`
5. 确保代码规范：`black src tests && isort src tests && ruff check src tests`
6. 推送分支：`git push origin feat/your-feature`
7. 创建 Pull Request

## 开发环境
