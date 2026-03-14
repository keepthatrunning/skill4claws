# SEO关键词库 (SEO Keyword Database)

AI Agent Skill for SEO keyword management, analysis and optimization.

## 功能特性

- 📊 **关键词管理**: 创建、导入、分类、标签化管理
- 📈 **数据分析**: 搜索量追踪、竞争度分析、排名监控
- 🔍 **机会发现**: 自动识别高价值低竞争关键词
- 📑 **报告生成**: HTML可视化报告、飞书多维表格导出
- 🔗 **API集成**: 支持SEMrush、Ahrefs、Google Keyword Planner

## 快速开始

### 安装

```bash
# 克隆到OpenClaw skills目录
cd /workspace/projects/workspace/skills
git clone https://github.com/yourusername/seo-keyword-db.git
```

### 初始化数据库

```bash
cd seo-keyword-db
python scripts/init_db.py --name "我的关键词库" --path ./keywords.db
```

### 导入关键词

```bash
# 从CSV导入
python scripts/import_keywords.py --file keywords.csv --db ./keywords.db

# 从JSON导入
python scripts/import_keywords.py --file keywords.json --db ./keywords.db --format json
```

### 生成分析报告

```bash
python scripts/analyze.py --db ./keywords.db --output report.html
```

## 数据结构

- **keywords**: 关键词主表
- **tags**: 标签表
- **keyword_tags**: 关键词-标签关联
- **rankings**: 排名历史
- **volume_history**: 搜索量历史

详见 [references/schema.md](references/schema.md)

## API集成

支持接入:
- Google Keyword Planner
- SEMrush API
- Ahrefs API
- 百度指数

配置方法见 [references/api-integration.md](references/api-integration.md)

## 作为OpenClaw Skill使用

当用户提到以下场景时，本Skill将自动激活:
- SEO关键词管理
- 关键词数据分析
- 生成SEO报告
- 关键词导入/导出

## 目录结构

```
seo-keyword-db/
├── SKILL.md                    # Skill主文档
├── scripts/
│   ├── init_db.py             # 初始化数据库
│   ├── import_keywords.py     # 导入关键词
│   └── analyze.py             # 分析报告生成
└── references/
    ├── schema.md              # 数据库结构
    ├── api-integration.md     # API集成指南
    └── examples.md            # 示例数据
```

## 许可证

MIT License

## 贡献

欢迎提交Issue和PR！

---

*Powered by OpenClaw | 方案C-v3 智能记忆系统*
