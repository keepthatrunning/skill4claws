# 数据库结构文档

## 表结构说明

### keywords (关键词主表)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键，自增 |
| keyword | TEXT | 关键词文本，唯一 |
| search_volume | INTEGER | 月搜索量 |
| competition | REAL | 竞争度 (0-1) |
| cpc | REAL | 单次点击成本 |
| category | TEXT | 分类 |
| intent | TEXT | 搜索意图 (信息型/导航型/交易型/商业型) |
| priority | INTEGER | 优先级 (1-10) |
| status | TEXT | 状态 (active/paused/archived) |
| created_at | TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | 更新时间 |

### tags (标签表)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键，自增 |
| name | TEXT | 标签名称，唯一 |

### keyword_tags (关键词-标签关联表)

| 字段 | 类型 | 说明 |
|------|------|------|
| keyword_id | INTEGER | 关键词ID |
| tag_id | INTEGER | 标签ID |

### rankings (排名历史表)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键，自增 |
| keyword_id | INTEGER | 关键词ID |
| position | INTEGER | 排名位置 |
| date | DATE | 日期 |
| url | TEXT | 排名URL |

### volume_history (搜索量历史表)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键，自增 |
| keyword_id | INTEGER | 关键词ID |
| volume | INTEGER | 搜索量 |
| date | DATE | 日期 |
| source | TEXT | 数据来源 |

## 常用查询示例

### 按分类统计关键词
```sql
SELECT category, COUNT(*) as count, AVG(search_volume) as avg_volume
FROM keywords
GROUP BY category
ORDER BY count DESC;
```

### 查找高价值低竞争关键词
```sql
SELECT keyword, search_volume, competition, cpc
FROM keywords
WHERE search_volume > 1000 AND competition < 0.4
ORDER BY search_volume DESC;
```

### 按意图类型统计
```sql
SELECT intent, COUNT(*) as count, AVG(search_volume) as avg_volume
FROM keywords
GROUP BY intent;
```
