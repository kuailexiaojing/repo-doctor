# 🩺 repo-doctor

> 开源仓库健康诊断 CLI —— 一键检查你的项目是否"健康"，自动生成修复建议

[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-Apache--2.0-green)](LICENSE)

## 🎯 它解决什么问题？

很多开源项目缺少关键文件（LICENSE、README、CONTRIBUTING 等）、没有 CI 配置、
依赖过时或有安全风险。`repo-doctor` 帮你一键诊断，给出健康评分和修复建议，
让你的项目更规范、更可信、更容易吸引贡献者。

## ✨ 功能特点

- 📋 **关键文件检查** —— LICENSE、README、CONTRIBUTING、CHANGELOG、.gitignore 等
- 📖 **README 质量评分** —— 标题、安装说明、使用示例、许可证声明
- 🔒 **安全检查** —— 敏感文件是否被 .gitignore 排除
- ⚙️ **CI/CD 检查** —— 是否配置了 GitHub Actions 等
- 🧹 **代码规范检查** —— 是否有 formatter / linter 配置
- 🏥 **健康评分** —— 0-100 分，一目了然
- 🤖 **AI 修复建议** —— 可选接入 OpenAI API，生成智能修复方案
- 🔧 **自动修复** —— 一键生成缺失的模板文件

## 📦 安装

