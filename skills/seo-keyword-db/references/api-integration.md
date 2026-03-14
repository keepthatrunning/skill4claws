# API集成指南

## 支持的API源

### Google Keyword Planner

需配置API密钥:
```bash
export GOOGLE_ADS_DEVELOPER_TOKEN="your_token"
export GOOGLE_ADS_CLIENT_ID="your_client_id"
export GOOGLE_ADS_CLIENT_SECRET="your_secret"
```

### SEMrush API

```bash
export SEMRUSH_API_KEY="your_api_key"
```

获取关键词数据:
```python
from semrush import SEMrushAPI

api = SEMrushAPI(api_key=os.getenv('SEMRUSH_API_KEY'))
data = api.get_keyword_data("seo tools", database="us")
```

### Ahrefs API

```bash
export AHREFS_API_TOKEN="your_token"
```

### 百度指数

需配置Cookie:
```bash
export BAIDU_INDEX_COOKIE="your_cookie"
```

## 数据同步策略

### 自动同步

建议每周同步一次搜索量数据:
```bash
# 添加到crontab
0 9 * * 1 python scripts/sync_volume.py --db ./keywords.db --source semrush
```

### 手动同步

```bash
python scripts/sync_volume.py --db ./keywords.db --source google --keywords-file update_list.txt
```

## 速率限制

| API | 免费额度 | 付费档位 |
|-----|----------|----------|
| SEMrush | 10 requests/month | $99/month |
| Ahrefs | 500 credits/month | $99/month |
| Google Ads | 15,000 units/day | 按用量计费 |
