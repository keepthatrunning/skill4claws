#!/usr/bin/env python3
"""
SEO关键词库初始化脚本
创建SQLite数据库和表结构
"""

import sqlite3
import argparse
import os
from datetime import datetime

SCHEMA = '''
-- 关键词主表
CREATE TABLE IF NOT EXISTS keywords (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    keyword TEXT NOT NULL UNIQUE,
    search_volume INTEGER DEFAULT 0,
    competition REAL DEFAULT 0.0,
    cpc REAL DEFAULT 0.0,
    category TEXT,
    intent TEXT CHECK(intent IN ('信息型', '导航型', '交易型', '商业型')),
    priority INTEGER DEFAULT 5,
    status TEXT DEFAULT 'active' CHECK(status IN ('active', 'paused', 'archived')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 标签表
CREATE TABLE IF NOT EXISTS tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

-- 关键词-标签关联表
CREATE TABLE IF NOT EXISTS keyword_tags (
    keyword_id INTEGER,
    tag_id INTEGER,
    FOREIGN KEY (keyword_id) REFERENCES keywords(id),
    FOREIGN KEY (tag_id) REFERENCES tags(id),
    PRIMARY KEY (keyword_id, tag_id)
);

-- 排名历史表
CREATE TABLE IF NOT EXISTS rankings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    keyword_id INTEGER,
    position INTEGER,
    date DATE DEFAULT CURRENT_DATE,
    url TEXT,
    FOREIGN KEY (keyword_id) REFERENCES keywords(id)
);

-- 搜索量历史表
CREATE TABLE IF NOT EXISTS volume_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    keyword_id INTEGER,
    volume INTEGER,
    date DATE DEFAULT CURRENT_DATE,
    source TEXT,
    FOREIGN KEY (keyword_id) REFERENCES keywords(id)
);

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_keywords_category ON keywords(category);
CREATE INDEX IF NOT EXISTS idx_keywords_intent ON keywords(intent);
CREATE INDEX IF NOT EXISTS idx_keywords_status ON keywords(status);
CREATE INDEX IF NOT EXISTS idx_rankings_date ON rankings(date);
CREATE INDEX IF NOT EXISTS idx_volume_date ON volume_history(date);
'''

def init_database(db_path, name=None):
    """初始化关键词数据库"""
    
    # 确保目录存在
    os.makedirs(os.path.dirname(db_path) if os.path.dirname(db_path) else '.', exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 执行建表语句
    cursor.executescript(SCHEMA)
    
    # 创建元数据表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS metadata (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    ''')
    
    # 插入元数据
    cursor.execute('INSERT OR REPLACE INTO metadata VALUES (?, ?)', 
                   ('name', name or 'SEO关键词库'))
    cursor.execute('INSERT OR REPLACE INTO metadata VALUES (?, ?)', 
                   ('created_at', datetime.now().isoformat()))
    cursor.execute('INSERT OR REPLACE INTO metadata VALUES (?, ?)', 
                   ('version', '1.0.0'))
    
    conn.commit()
    conn.close()
    
    print(f"✅ 关键词库已创建: {db_path}")
    if name:
        print(f"📁 库名称: {name}")
    print(f"📊 包含表: keywords, tags, keyword_tags, rankings, volume_history")

def main():
    parser = argparse.ArgumentParser(description='初始化SEO关键词数据库')
    parser.add_argument('--name', help='关键词库名称')
    parser.add_argument('--path', default='./keywords.db', help='数据库文件路径')
    
    args = parser.parse_args()
    init_database(args.path, args.name)

if __name__ == '__main__':
    main()
