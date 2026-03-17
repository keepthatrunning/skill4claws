# SEO关键词库示例数据

## 示例CSV格式

```csv
keyword,search_volume,competition,cpc,category,intent
seo tools,5400,0.65,3.2,工具,信息型
keyword research,3600,0.45,2.8,研究,信息型
content marketing,2900,0.55,4.1,营销,商业型
link building,2400,0.7,3.5,外链,交易型
on page seo,1800,0.4,2.5,优化,信息型
technical seo,1600,0.5,3.0,技术,信息型
seo audit,1400,0.6,2.9,工具,交易型
local seo,1200,0.55,3.8,本地,商业型
ecommerce seo,900,0.45,4.2,电商,商业型
seo strategy,800,0.35,2.1,策略,信息型
```

## 示例JSON格式

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
      "tags": ["SEO", "软件", "工具"]
    },
    {
      "keyword": "keyword research",
      "search_volume": 3600,
      "competition": 0.45,
      "cpc": 2.8,
      "category": "研究",
      "intent": "信息型",
      "tags": ["关键词", "研究"]
    },
    {
      "keyword": "content marketing",
      "search_volume": 2900,
      "competition": 0.55,
      "cpc": 4.1,
      "category": "营销",
      "intent": "商业型",
      "tags": ["内容", "营销"]
    }
  ]
}
```

## 搜索意图分类说明

| 意图类型 | 说明 | 示例关键词 |
|----------|------|------------|
| 信息型 | 用户寻求信息 | "什么是SEO", "如何优化网站" |
| 导航型 | 用户寻找特定网站 | "Google Search Console", "Ahrefs登录" |
| 商业型 | 用户比较产品/服务 | "最佳SEO工具", "SEO软件对比" |
| 交易型 | 用户准备购买 | "购买SEO工具", "SEO服务价格" |
