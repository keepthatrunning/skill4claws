#!/usr/bin/env python3
"""
导出关键词到飞书多维表格
"""

import sqlite3
import sys
import json
import requests

def export_to_bitable(db_path, app_token, table_id, feishu_app_id=None, feishu_app_secret=None):
    """将关键词导出到飞书多维表格"""
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 获取所有关键词
    cursor.execute('''
        SELECT keyword, search_volume, competition, cpc, category, intent, tags
        FROM keywords
        ORDER BY search_volume DESC
    ''')
    
    keywords = cursor.fetchall()
    print(f"📊 找到 {len(keywords)} 个关键词")
    
    # 准备记录
    records = []
    for row in keywords:
        keyword, volume, comp, cpc, category, intent, tags = row
        records.append({
            "fields": {
                "关键词": keyword,
                "搜索量": volume or 0,
                "竞争度": round(comp or 0, 2),
                "CPC": round(cpc or 0, 2),
                "分类": category or "",
                "意图": intent or "",
                "标签": tags or ""
            }
        })
    
    conn.close()
    
    # 批量创建记录 (使用 OpenClaw 工具调用)
    print(f"📝 准备导出 {len(records)} 条记录到多维表格")
    print(f"   App Token: {app_token}")
    print(f"   Table ID: {table_id}")
    
    # 这里需要通过 OpenClaw 工具调用
    # feishu_bitable_app_table_record batch_create
    print("\n💡 请使用 OpenClaw 工具完成导出:")
    print(f"   feishu_bitable_app_table_record batch_create")
    print(f"   - app_token: {app_token}")
    print(f"   - table_id: {table_id}")
    print(f"   - records: {len(records)} 条")
    
    return records

def main():
    if len(sys.argv) < 4:
        print("用法: python export_bitable.py <db_path> <app_token> <table_id>")
        print("示例: python export_bitable.py ./keywords.db bascQHzYax1f1MsJ7GJcABCDEF tblXxXxXxXxXxXx")
        sys.exit(1)
    
    db_path = sys.argv[1]
    app_token = sys.argv[2]
    table_id = sys.argv[3]
    
    export_to_bitable(db_path, app_token, table_id)

if __name__ == "__main__":
    main()
