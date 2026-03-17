---
name: seo-keyword-db
description: |
  SEO关键词库管理工具 v1.1.0 - 用于创建、管理、分析和优化SEO关键词数据库。
  支持关键词分组、搜索量追踪、竞争度分析、关键词挖掘和报告生成。
  使用场景：(1) 批量导入/导出关键词数据，(2) 关键词分类与标签管理，(3) 搜索量和排名追踪，(4) 竞争对手关键词分析，(5) 生成SEO优化建议报告，(6) 导出到飞书多维表格
version: 1.1.0
author: egg小姐
date: 2026-03-14
---

# SEO关键词库 v1.1.0

管理和优化SEO关键词的完整工具集。

## 🆕 v1.1.0 新特性

- **飞书多维表格导出** - 一键导出关键词到飞书多维表格，便于团队协作

### 导出到飞书多维表格

```bash
# 导出关键词到多维表格
python scripts/export_bitable.py \
  --db ./keywords.db \
  --app-token bascQHzYax1f1MsJ7GJcABCDEF \
  --table-id tblXxXxXxXxXxXx
```

导出的字段包括：
- 关键词
- 搜索量
- 竞争度
- CPC
- 分类
- 意图
- 标签

## 快速开始

### 创建关键词库

```bash
# 初始化新的关键词库
python scripts/init_db.py --name "项目关键词库" --path ./keywords.db
```

### 导入关键词

```bash
# 从CSV导入
python scripts/import_keywords.py --file keywords.csv --db ./keywords.db

# 从JSON导入
python scripts/import_keywords.py --file keywords.json --db ./keywords.db --format json
```

### 关键词分析

```bash
# 分析关键词竞争度
python scripts/analyze.py --db ./keywords.db --output report.html
```

## 核心功能

### 1. 关键词管理

- **添加关键词**: 支持单个或批量添加
- **分类标签**: 按主题、意图、漏斗阶段分类
- **优先级排序**: 基于搜索量、竞争度、商业价值评分

### 2. 数据分析

- **搜索量追踪**: 记录历史搜索量变化
- **排名监控**: 追踪关键词在SERPs中的位置
- **竞争分析**: 评估关键词竞争强度

### 3. 报告生成

- **关键词分布报告**: 按类别统计
- **机会分析**: 低竞争高价值关键词推荐
- **趋势报告**: 搜索量变化趋势

## 数据格式

### CSV导入格式

```csv
keyword,search_volume,competition,cpc,category,intent
seo tools,5400,0.65,3.2,工具,信息型
keyword research,3600,0.45,2.8,研究,信息型
```

### JSON导入格式

```json
{
  "keywords": [
    {
      "keyword": "seo tools",
      "search_volume": 5400,
      "competition": 0.65,
      "cpc": 3.2,
      "category": "工具",
      "intent": "信息型",
      "tags": ["SEO", "软件"]
    }
  ]
}
```

## 使用示例

### 示例1: 批量导入并分类

```bash
python scripts/import_keywords.py \
  --file input.csv \
  --db ./keywords.db \
  --auto-categorize \
  --tags "核心词,长尾词"
```

### 示例2: 生成优化建议

```bash
python scripts/generate_suggestions.py \
  --db ./keywords.db \
  --min-volume 1000 \
  --max-competition 0.5 \
  --output opportunities.md
```

### 示例3: 导出到飞书多维表格

```bash
python scripts/export_feishu.py \
  --db ./keywords.db \
  --app-token YOUR_APP_TOKEN \
  --table-id YOUR_TABLE_ID
```

## 数据库结构

详见 [references/schema.md](references/schema.md)

## API集成

支持接入以下SEO数据源：
- Google Keyword Planner (需API密钥)
- SEMrush API
- Ahrefs API
- 百度指数

配置方法见 [references/api-integration.md](references/api-integration.md)

## 高级用法

### 关键词聚类

```bash
python scripts/cluster_keywords.py \
  --db ./keywords.db \
  --method semantic \
  --clusters 10
```

### 内容缺口分析

```bash
python scripts/content_gap.py \
  --db ./keywords.db \
  --competitor-urls urls.txt \
  --output gap_report.html
```
