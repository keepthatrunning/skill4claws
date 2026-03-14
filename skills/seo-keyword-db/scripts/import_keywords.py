#!/usr/bin/env python3
"""
关键词导入脚本
支持CSV和JSON格式
"""

import sqlite3
import csv
import json
import argparse
from datetime import datetime

def import_from_csv(db_path, csv_path, auto_categorize=False, tags=None):
    """从CSV导入关键词"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    imported = 0
    skipped = 0
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                cursor.execute('''
                    INSERT OR IGNORE INTO keywords 
                    (keyword, search_volume, competition, cpc, category, intent)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    row.get('keyword', '').strip(),
                    int(row.get('search_volume', 0) or 0),
                    float(row.get('competition', 0) or 0),
                    float(row.get('cpc', 0) or 0),
                    row.get('category', ''),
                    row.get('intent', '')
                ))
                if cursor.rowcount > 0:
                    imported += 1
                else:
                    skipped += 1
            except Exception as e:
                print(f"⚠️ 跳过行: {row.get('keyword', 'N/A')} - {e}")
                skipped += 1
    
    conn.commit()
    conn.close()
    
    print(f"✅ 导入完成: {imported} 个关键词")
    if skipped > 0:
        print(f"⏭️  跳过: {skipped} 个（重复或无效）")

def import_from_json(db_path, json_path):
    """从JSON导入关键词"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    keywords = data.get('keywords', [])
    imported = 0
    skipped = 0
    
    for kw in keywords:
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO keywords 
                (keyword, search_volume, competition, cpc, category, intent, tags)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                kw.get('keyword', '').strip(),
                int(kw.get('search_volume', 0) or 0),
                float(kw.get('competition', 0) or 0),
                float(kw.get('cpc', 0) or 0),
                kw.get('category', ''),
                kw.get('intent', ''),
                ','.join(kw.get('tags', []))
            ))
            if cursor.rowcount > 0:
                imported += 1
            else:
                skipped += 1
        except Exception as e:
            print(f"⚠️ 跳过: {kw.get('keyword', 'N/A')} - {e}")
            skipped += 1
    
    conn.commit()
    conn.close()
    
    print(f"✅ 导入完成: {imported} 个关键词")
    if skipped > 0:
        print(f"⏭️  跳过: {skipped} 个（重复或无效）")

def main():
    parser = argparse.ArgumentParser(description='导入关键词到数据库')
    parser.add_argument('--file', required=True, help='要导入的文件路径')
    parser.add_argument('--db', default='./keywords.db', help='数据库路径')
    parser.add_argument('--format', choices=['csv', 'json'], 
                       help='文件格式（自动检测）')
    parser.add_argument('--auto-categorize', action='store_true',
                       help='自动分类关键词')
    parser.add_argument('--tags', help='添加标签（逗号分隔）')
    
    args = parser.parse_args()
    
    # 自动检测格式
    file_format = args.format
    if not file_format:
        if args.file.endswith('.json'):
            file_format = 'json'
        else:
            file_format = 'csv'
    
    if file_format == 'csv':
        import_from_csv(args.db, args.file, args.auto_categorize, args.tags)
    else:
        import_from_json(args.db, args.file)

if __name__ == '__main__':
    main()
