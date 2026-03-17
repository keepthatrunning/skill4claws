---
name: skill-creator-enhanced
description: |
  增强版 Skill 创建工具 v2.0.0 - 结合 Anthropic 评估框架与 OpenClaw 打包规范。
  提供完整的 Skill 生命周期管理：创建、评估、优化、打包、验证。
  使用场景：(1) 从0创建新 Skill，(2) 评估和优化现有 Skill，(3) 运行量化测试和基准分析，(4) 打包和验证 Skill 结构，(5) 优化 Skill 描述提升触发准确率，(6) 批量评估多个 Skills
version: 2.0.0
author: egg小姐
date: 2026-03-14
---

# Skill Creator Enhanced (增强版 Skill 创建工具)

结合 Anthropic 评估框架与 OpenClaw 打包规范的完整 Skill 创建解决方案。

## 核心功能

| 功能 | 说明 |
|------|------|
| 📝 **创建** | 初始化 Skill 目录结构，生成模板 |
| 🧪 **评估** | 运行对比测试，量化 Skill 效果 |
| 📊 **分析** | 基准分析，识别改进点 |
| 📦 **打包** | 验证并打包成 .skill 文件 |
| ✨ **优化** | AI 辅助优化 description |

## 快速开始

```bash
# 1. 初始化 Skill
python scripts/init_skill.py my-skill --path ./skills --resources scripts,references

# 2. 创建测试用例 (evals/evals.json)
# 3. 运行评估
python scripts/run_eval.py --skill ./skills/my-skill --evals ./evals/evals.json

# 4. 查看结果
python eval-viewer/generate_review.py ./my-skill-workspace/iteration-1 --skill-name "my-skill"

# 5. 打包
python scripts/package_skill.py ./skills/my-skill
```

## 评估框架

### 对比测试
- **有 Skill** vs **无 Skill** 的效果对比
- 量化指标：通过率、时间、token 消耗
- 可视化结果查看器

### 断言类型
- `contains` - 包含指定内容
- `exists` - 文件存在
- `regex` - 匹配正则
- `custom` - 自定义脚本

## 脚本工具

| 脚本 | 功能 |
|------|------|
| `init_skill.py` | 初始化 Skill 目录 |
| `run_eval.py` | 运行评估测试 |
| `aggregate_benchmark.py` | 聚合基准报告 |
| `package_skill.py` | 打包 Skill |
| `quick_validate.py` | 快速验证结构 |
| `improve_description.py` | 优化 description |

## 合并说明

此 Skill 合并了：
- **Anthropic skill-creator**: 评估框架、测试工具、查看器
- **OpenClaw skill-creator**: 打包规范、验证脚本、目录结构

---
*合并版本 | egg小姐 🥚*
