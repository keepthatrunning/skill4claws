#!/usr/bin/env python3
"""
关键词分析报告生成器
"""

import sqlite3
import argparse
from datetime import datetime

def generate_analysis(db_path, output_path, min_volume=0, max_competition=1.0):
    """生成关键词分析报告"""
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 基础统计
    cursor.execute('SELECT COUNT(*) FROM keywords')
    total_keywords = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM keywords WHERE status = "active"')
    active_keywords = cursor.fetchone()[0]
    
    # 按类别统计
    cursor.execute('''
        SELECT category, COUNT(*) as count, AVG(search_volume) as avg_volume
        FROM keywords 
        WHERE category IS NOT NULL
        GROUP BY category
        ORDER BY count DESC
    ''')
    categories = cursor.fetchall()
    
    # 按意图统计
    cursor.execute('''
        SELECT intent, COUNT(*) as count
        FROM keywords 
        WHERE intent IS NOT NULL
        GROUP BY intent
    ''')
    intents = cursor.fetchall()
    
    # 高价值关键词（高搜索量，低竞争）
    cursor.execute('''
        SELECT keyword, search_volume, competition, cpc, category
        FROM keywords
        WHERE search_volume >= ? AND competition <= ? AND status = 'active'
        ORDER BY (search_volume * (1 - competition)) DESC
        LIMIT 20
    ''', (min_volume, max_competition))
    opportunities = cursor.fetchall()
    
    # 生成HTML报告
    html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>SEO关键词分析报告</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 40px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
        h1 {{ color: #1a1a1a; border-bottom: 3px solid #3370ff; padding-bottom: 10px; }}
        h2 {{ color: #333; margin-top: 30px; }}
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }}
        .stat-card {{ background: #f8f9fa; padding: 20px; border-radius: 8px; border-left: 4px solid #3370ff; }}
        .stat-value {{ font-size: 32px; font-weight: bold; color: #3370ff; }}
        .stat-label {{ color: #666; margin-top: 5px; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #e8e8e8; }}
        th {{ background: #f8f9fa; font-weight: 600; color: #333; }}
        tr:hover {{ background: #f8f9fa; }}
        .opportunity {{ background: #e6f7ff; }}
        .badge {{ padding: 4px 12px; border-radius: 12px; font-size: 12px; font-weight: 500; }}
        .badge-info {{ background: #e6f7ff; color: #1890ff; }}
        .badge-success {{ background: #f6ffed; color: #52c41a; }}
        .badge-warning {{ background: #fff7e6; color: #fa8c16; }}
        .timestamp {{ color: #999; font-size: 14px; margin-top: 40px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🎯 SEO关键词分析报告</h1>
        <p class="timestamp">生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-value">{total_keywords}</div>
                <div class="stat-label">关键词总数</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{active_keywords}</div>
                <div class="stat-label">活跃关键词</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{len(categories)}</div>
                <div class="stat-label">分类数量</div>
            </div>
        </div>
        
        <h2>📊 分类分布</h2>
        <table>
            <tr>
                <th>分类</th>
                <th>关键词数量</th>
                <th>平均搜索量</th>
            </tr>
'''
    
    for cat in categories:
        html_content += f'''
            <tr>
                <td>{cat[0] or '未分类'}</td>
                <td>{cat[1]}</td>
                <td>{int(cat[2] or 0):,}</td>
            </tr>
'''
    
    html_content += f'''
        </table>
        
        <h2>🎯 搜索意图分布</h2>
        <table>
            <tr>
                <th>意图类型</th>
                <th>关键词数量</th>
            </tr>
'''
    
    for intent in intents:
        html_content += f'''
            <tr>
                <td>{intent[0] or '未标注'}</td>
                <td>{intent[1]}</td>
            </tr>
'''
    
    html_content += f'''
        </table>
        
        <h2>💎 高价值机会关键词</h2>
        <p>筛选条件: 最小搜索量 {min_volume:,}, 最大竞争度 {max_competition}</p>
        <table>
            <tr>
                <th>关键词</th>
                <th>搜索量</th>
                <th>竞争度</th>
                <th>CPC</th>
                <th>分类</th>
            </tr>
'''
    
    for opp in opportunities:
        html_content += f'''
            <tr class="opportunity">
                <td><strong>{opp[0]}</strong></td>
                <td>{opp[1]:,}</td>
                <td>{opp[2]:.2f}</td>
                <td>${opp[3]:.2f}</td>
                <td>{opp[4] or '未分类'}</td>
            </tr>
'''
    
    html_content += f'''
        </table>
        
        <div class="timestamp">
            <p>Generated by SEO关键词库 | 方案C-v3 智能分析</p>
        </div>
    </div>
</body>
</html>
'''
    
    conn.close()
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ 分析报告已生成: {output_path}")
    print(f"📊 包含 {total_keywords} 个关键词的分析")
    print(f"💎 发现 {len(opportunities)} 个高价值机会")

def main():
    parser = argparse.ArgumentParser(description='生成关键词分析报告')
    parser.add_argument('--db', default='./keywords.db', help='数据库路径')
    parser.add_argument('--output', default='report.html', help='输出文件路径')
    parser.add_argument('--min-volume', type=int, default=0, help='最小搜索量')
    parser.add_argument('--max-competition', type=float, default=1.0, help='最大竞争度')
    
    args = parser.parse_args()
    generate_analysis(args.db, args.output, args.min_volume, args.max_competition)

if __name__ == '__main__':
    main()
