# AGENTS.md

本文档面向 AI 编程 Agent（如 Codex、Cursor、Copilot），提供项目上下文和操作规范。

## 项目概述

repo-doctor 是一个开源仓库健康诊断 CLI 工具，使用 Python 编写。

### 核心模块

- `src/repo_doctor/cli.py` — CLI 入口，定义所有命令（check / fix / ai-suggest）
- `src/repo_doctor/checker.py` — 检查引擎，执行各项健康检查
- `src/repo_doctor/reporter.py` — 报告生成，格式化输出（文本 / JSON）
- `src/repo_doctor/fixer.py` — 自动修复，生成缺失的模板文件
- `tests/` — 单元测试

### 技术栈

- Python 3.10+
- Click（CLI 框架）
- pytest（测试）
- black + isort + ruff（代码规范）
- GitHub Actions（CI）

## 构建与安装
