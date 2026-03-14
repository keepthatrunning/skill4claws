# GitHub 仓库维护最佳实践

> 🎯 确保代码与文档始终同步的完整指南

## 核心原则

**黄金法则**: 任何代码变更都必须有对应的文档更新

```
代码变更 → 影响评估 → 同步更新文档 → 一并提交
```

## 快速开始

### 安装

```bash
# 克隆到项目
git clone https://github.com/keepthatrunning/skill4claws.git
cd skill4claws/github-maintainer-best-practices

# 复制脚本到你的项目
cp scripts/*.py /你的项目/scripts/
```

### 日常使用

```bash
# 提交前检查文档同步状态
python scripts/check-sync.py

# 发布新版本
python scripts/release.py --type minor
```

## 功能特性

| 功能 | 说明 |
|------|------|
| 📋 同步检查 | 自动检测代码变更后需更新的文档 |
| 🏷️ 版本管理 | 自动化版本号更新和Git标签创建 |
| 📝 提交规范 | Conventional Commits 格式指南 |
| 📚 文档模板 | README/CHANGELOG 维护模板 |
| 🔒 团队强制 | CI/CD 和 Git Hooks 配置 |

## 目录结构

```
github-maintainer-best-practices/
├── SKILL.md                        # Skill主文档
├── README.md                       # 本文件
├── scripts/
│   ├── check-sync.py              # 同步检查脚本
│   └── release.py                 # 版本发布助手
└── references/
    ├── release-workflow.md        # 版本发布流程
    └── team-enforcement.md        # 团队规范强制执行
```

## 作为 OpenClaw Skill 使用

当用户提到以下场景时自动激活：
- 更新 GitHub 仓库
- 维护开源项目
- 版本发布管理
- 代码与文档同步
- 提交信息规范

## 贡献

欢迎提交 Issue 和 PR！

---

*Powered by OpenClaw | egg小姐 🥚*
