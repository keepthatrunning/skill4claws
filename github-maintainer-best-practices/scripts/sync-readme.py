#!/usr/bin/env python3
"""
README 自动同步脚本
扫描 skills/ 目录，自动更新 README.md 的技能列表
"""

import os
import re
import json
from datetime import datetime
from pathlib import Path

def parse_skill_metadata(skill_path):
    """解析 SKILL.md 的元数据"""
    skill_file = os.path.join(skill_path, 'SKILL.md')
    if not os.path.exists(skill_file):
        return None
    
    with open(skill_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 解析 frontmatter
    metadata = {}
    
    # 提取 name
    name_match = re.search(r'^name:\s*(.+)$', content, re.MULTILINE)
    if name_match:
        metadata['name'] = name_match.group(1).strip()
    
    # 提取 description (支持多行)
    desc_match = re.search(r'^description:\s*\|\s*\n((?:\s+.+\n?)+)', content, re.MULTILINE)
    if desc_match:
        desc_lines = desc_match.group(1).strip().split('\n')
        metadata['description'] = ' '.join(line.strip() for line in desc_lines if line.strip())
    else:
        desc_match = re.search(r'^description:\s*(.+)$', content, re.MULTILINE)
        if desc_match:
            metadata['description'] = desc_match.group(1).strip()
    
    # 提取 version
    version_match = re.search(r'^version:\s*(.+)$', content, re.MULTILINE)
    if version_match:
        metadata['version'] = version_match.group(1).strip()
    else:
        metadata['version'] = '1.0.0'
    
    # 提取 tags
    tags_match = re.search(r'^tags:\s*\[(.+?)\]', content, re.MULTILINE)
    if tags_match:
        metadata['tags'] = [t.strip().strip('"\'') for t in tags_match.group(1).split(',')]
    else:
        metadata['tags'] = []
    
    return metadata

def get_all_skills(skills_dir='skills'):
    """获取所有技能信息"""
    skills = []
    if not os.path.exists(skills_dir):
        return skills
    
    for item in os.listdir(skills_dir):
        skill_path = os.path.join(skills_dir, item)
        if os.path.isdir(skill_path):
            metadata = parse_skill_metadata(skill_path)
            if metadata:
                metadata['dir'] = item
                skills.append(metadata)
    
    return sorted(skills, key=lambda x: x['name'])

def categorize_skills(skills):
    """按类别分组技能"""
    categories = {
        'core': {'name': '🧠 核心系统', 'skills': []},
        'devops': {'name': '🔧 开发规范', 'skills': []},
        'tools': {'name': '🎨 工具集成', 'skills': []},
        'marketing': {'name': '📈 营销与分析', 'skills': []},
        'evomap': {'name': '🎯 EvoMap 集成', 'skills': []},
        'other': {'name': '🛠️ 其他工具', 'skills': []}
    }
    
    for skill in skills:
        tags = [t.lower() for t in skill.get('tags', [])]
        name = skill['name'].lower()
        
        if 'memory' in tags or 'evomap' in name and 'sop' in name:
            categories['core']['skills'].append(skill)
        elif 'github' in tags or 'skill' in name and 'creator' in name:
            categories['devops']['skills'].append(skill)
        elif any(t in ['image', 'voice', 'search', 'ai'] for t in tags):
            categories['tools']['skills'].append(skill)
        elif 'seo' in tags or 'keyword' in name:
            categories['marketing']['skills'].append(skill)
        elif 'evomap' in tags or 'a2a' in tags:
            categories['evomap']['skills'].append(skill)
        else:
            categories['other']['skills'].append(skill)
    
    # 过滤空分类
    return {k: v for k, v in categories.items() if v['skills']}

def generate_skill_table(skills):
    """生成技能表格 Markdown"""
    lines = ['| Skill | 描述 | 版本 | 标签 |', '|-------|------|------|------|']
    
    for skill in skills:
        name = skill['name']
        desc = skill.get('description', '')[:50] + '...' if len(skill.get('description', '')) > 50 else skill.get('description', '')
        version = skill.get('version', '1.0.0')
        tags = ', '.join(f'`{t}`' for t in skill.get('tags', [])[:3])
        dir_name = skill['dir']
        
        lines.append(f"| [{name}](./skills/{dir_name}/) | {desc} | {version} | {tags} |")
    
    return '\n'.join(lines)

def update_readme(readme_path='README.md', skills_dir='skills'):
    """更新 README.md"""
    skills = get_all_skills(skills_dir)
    categories = categorize_skills(skills)
    
    if not os.path.exists(readme_path):
        print(f"❌ {readme_path} 不存在")
        return False
    
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 更新统计信息
    content = re.sub(
        r'\*\*总 Skills\*\*\s*\|\s*\d+',
        f'**总 Skills** | {len(skills)}',
        content
    )
    
    # 更新最后更新日期
    today = datetime.now().strftime('%Y-%m-%d')
    content = re.sub(
        r'\*\*最后更新\*\*\s*\|\s*\d{4}-\d{2}-\d{2}',
        f'**最后更新** | {today}',
        content
    )
    
    # 更新版本号
    content = re.sub(
        r'\*更新时间: \d{4}-\d{2}-\d+ \| 版本: v[\d.]+\*',
        f'*更新时间: {today} | 版本: v2.0.0*',
        content
    )
    
    print(f"📊 发现 {len(skills)} 个 skills")
    print(f"📅 更新日期: {today}")
    
    # 保存更新后的 README
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ README.md 已更新")
    return True

def main():
    print("🔄 README 自动同步脚本\n")
    
    # 检查是否在 git 仓库中
    if not os.path.exists('.git'):
        print("⚠️  当前目录不是 git 仓库，请在项目根目录运行")
        return
    
    # 更新 README
    if update_readme():
        print("\n📋 更新摘要:")
        print("  - 技能数量统计已更新")
        print("  - 最后更新日期已更新")
        print("\n💡 如需完全重新生成技能列表，请手动编辑 README.md")
        print("   或使用 --regenerate 参数 (开发中)")
    else:
        print("❌ 更新失败")

if __name__ == '__main__':
    main()
