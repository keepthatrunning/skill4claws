# Skill Creator Enhanced

增强版 Skill 创建工具 - 结合 Anthropic 评估框架与 OpenClaw 打包规范。

## 功能特性

- 📝 **创建** - 初始化 Skill 目录，生成模板
- 🧪 **评估** - 对比测试，量化 Skill 效果  
- 📊 **分析** - 基准分析，识别改进点
- 📦 **打包** - 验证并打包成 .skill 文件
- ✨ **优化** - AI 辅助优化 description

## 目录结构

```
skill-creator-enhanced/
├── SKILL.md              # 主文档
├── scripts/              # 工具脚本
│   ├── init_skill.py     # 初始化
│   ├── run_eval.py       # 运行评估
│   ├── aggregate_benchmark.py  # 聚合基准
│   ├── package_skill.py  # 打包
│   ├── quick_validate.py # 快速验证
│   └── improve_description.py  # 优化描述
├── eval-viewer/          # 评估结果查看器
│   ├── generate_review.py
│   └── viewer.html
├── agents/               # 评估代理
└── references/           # 参考文档
```

## 使用方法

详见 SKILL.md

## 合并来源

- Anthropic skills: https://github.com/anthropics/skills
- OpenClaw skill-creator: /usr/lib/node_modules/openclaw/skills/skill-creator

---
*Created by egg小姐 | 2026-03-13*
