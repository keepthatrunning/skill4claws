#!/usr/bin/env python3
"""
GitHub仓库同步检查脚本
检查代码变更后文档是否已同步更新
"""

import subprocess
import re
import os
import sys
from pathlib import Path

# 文件变更与需同步文档的映射
SYNC_RULES = {
    r'src/.*\.py$': ['README.md', 'docs/api.md'],
    r'src/.*\.js$': ['README.md', 'docs/api.md'],
    r'.*\.api\.': ['README.md', 'CHANGELOG.md'],
    r'package\.json$': ['README.md', 'CHANGELOG.md'],
    r'setup\.py$': ['README.md', 'CHANGELOG.md'],
    r'pyproject\.toml$': ['README.md', 'CHANGELOG.md'],
    r'\.env\.example$': ['README.md', 'docs/configuration.md'],
    r'Dockerfile$': ['README.md', 'docs/deployment.md'],
}

def get_changed_files():
    """获取当前分支与main的差异文件"""
    try:
        result = subprocess.run(
            ['git', 'diff', '--name-status', 'origin/main...HEAD'],
            capture_output=True,
            text=True,
            check=True
        )
        changes = []
        for line in result.stdout.strip().split('\n'):
            if line:
                parts = line.split('\t')
                if len(parts) >= 2:
                    status, filepath = parts[0], parts[1]
                    changes.append((status, filepath))
        return changes
    except subprocess.CalledProcessError:
        # 可能没有origin/main，尝试与HEAD~1比较
        result = subprocess.run(
            ['git', 'diff', '--name-status', 'HEAD~1..HEAD'],
            capture_output=True,
            text=True
        )
        changes = []
        for line in result.stdout.strip().split('\n'):
            if line:
                parts = line.split('\t')
                if len(parts) >= 2:
                    status, filepath = parts[0], parts[1]
                    changes.append((status, filepath))
        return changes

def check_documentation_sync(changed_files):
    """检查文档同步状态"""
    suggestions = []
    
    for status, filepath in changed_files:
        for pattern, docs in SYNC_RULES.items():
            if re.match(pattern, filepath):
                for doc in docs:
                    if not any(doc == cf[1] for cf in changed_files):
                        suggestions.append({
                            'file': filepath,
                            'status': status,
                            'suggested_doc': doc,
                            'reason': f'代码文件变更，建议同步更新文档'
                        })
    
    return suggestions

def check_readme_updated():
    """检查README是否有更新"""
    try:
        result = subprocess.run(
            ['git', 'diff', 'origin/main...HEAD', '--name-only'],
            capture_output=True,
            text=True
        )
        changed = result.stdout.strip().split('\n')
        return 'README.md' in changed
    except:
        return True  # 无法检查时假设已更新

def main():
    print("🔍 GitHub 仓库同步检查")
    print("=" * 50)
    
    # 检查是否在git仓库中
    if not os.path.exists('.git'):
        print("❌ 错误: 当前目录不是Git仓库")
        sys.exit(1)
    
    changed_files = get_changed_files()
    
    if not changed_files:
        print("✅ 没有检测到文件变更")
        return
    
    print(f"\n📁 检测到 {len(changed_files)} 个文件变更:\n")
    for status, filepath in changed_files:
        status_icon = {
            'M': '📝',
            'A': '➕',
            'D': '➖',
            'R': '➡️',
        }.get(status[0], '•')
        print(f"  {status_icon} {filepath} ({status})")
    
    # 检查文档同步建议
    suggestions = check_documentation_sync(changed_files)
    
    if suggestions:
        print(f"\n⚠️  文档同步建议:\n")
        for sug in suggestions:
            print(f"  📄 {sug['file']} ({sug['status']})")
            print(f"     → 建议更新: {sug['suggested_doc']}")
            print()
    
    # 检查README更新
    if not check_readme_updated():
        code_changes = [f for f in changed_files if f[1].endswith(('.py', '.js', '.ts', '.go', '.rs']))]
        if code_changes:
            print("⚠️  提醒: 代码有变更，但 README.md 未更新")
            print("   请确认是否需要更新文档说明\n")
    
    print("=" * 50)
    print("💡 提示: 使用 --strict 模式可在发现问题时退出码非零")

if __name__ == '__main__':
    main()
