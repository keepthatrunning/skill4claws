#!/usr/bin/env python3
"""
AI更新通知脚本
推送更新后通知其他AI（通过评论、Webhook或其他方式）
"""

import os
import sys
import argparse
import json
from datetime import datetime

def generate_update_report(skill, version, changes, author):
    """生成更新报告"""
    report = {
        "type": "skill_update",
        "timestamp": datetime.now().isoformat(),
        "skill": skill,
        "version": version,
        "changes": changes,
        "author": author,
        "action_required": "review"  # review / merge / none
    }
    return report

def print_notification(report):
    """打印通知信息"""
    print("\n" + "=" * 60)
    print("📢 AI Skill 更新通知")
    print("=" * 60)
    print(f"\n📝 Skill: {report['skill']}")
    print(f"🔖 版本: {report['version']}")
    print(f"👤 作者: {report['author']}")
    print(f"🕐 时间: {report['timestamp']}")
    print(f"\n📋 变更内容:")
    print(f"   {report['changes']}")
    print(f"\n💡 建议操作:")
    print(f"   - 其他AI可拉取最新代码查看变更")
    print(f"   - 如有冲突请协商解决")
    print(f"   - 欢迎Review并提出改进建议")
    print("\n" + "=" * 60)

def save_notification(report, output_file='.ai-updates/last-update.json'):
    """保存通知到文件"""
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w') as f:
        json.dump(report, f, indent=2)
    print(f"\n💾 通知已保存: {output_file}")

def update_changelog(skill, version, changes, author):
    """自动更新 CHANGELOG"""
    changelog_path = 'CHANGELOG.md'
    if not os.path.exists(changelog_path):
        print(f"⚠️  {changelog_path} 不存在，跳过自动更新")
        return
    
    with open(changelog_path, 'r') as f:
        content = f.read()
    
    # 在 [Unreleased] 部分添加新条目
    new_entry = f"\n- **{skill}** v{version} - {changes} [by {author}]\n"
    
    if '## [Unreleased]' in content:
        content = content.replace(
            '## [Unreleased]',
            f'## [Unreleased]{new_entry}'
        )
    else:
        content = f'## [Unreleased]{new_entry}\n\n' + content
    
    with open(changelog_path, 'w') as f:
        f.write(content)
    
    print(f"✅ 已更新 {changelog_path}")

def main():
    parser = argparse.ArgumentParser(description='AI Skill 更新通知')
    parser.add_argument('--skill', required=True, help='Skill名称')
    parser.add_argument('--version', required=True, help='新版本号')
    parser.add_argument('--changes', required=True, help='变更描述')
    parser.add_argument('--author', required=True, help='作者标识')
    parser.add_argument('--save', action='store_true', help='保存到文件')
    parser.add_argument('--update-changelog', action='store_true', help='自动更新CHANGELOG')
    
    args = parser.parse_args()
    
    # 生成报告
    report = generate_update_report(args.skill, args.version, args.changes, args.author)
    
    # 打印通知
    print_notification(report)
    
    # 保存到文件
    if args.save:
        save_notification(report)
    
    # 更新CHANGELOG
    if args.update_changelog:
        update_changelog(args.skill, args.version, args.changes, args.author)
    
    print("\n📤 通知发送完成！")

if __name__ == '__main__':
    main()
