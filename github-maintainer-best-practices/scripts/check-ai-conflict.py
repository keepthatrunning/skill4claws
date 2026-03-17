#!/usr/bin/env python3
"""
AI协作冲突检测脚本
检查是否有其他AI正在编辑或最近更新了指定skill
"""

import os
import sys
import subprocess
import re
from datetime import datetime, timedelta

def get_recent_commits(skill_path, hours=2):
    """获取最近N小时的提交记录"""
    try:
        result = subprocess.run(
            ['git', 'log', '--since=f{hours} hours ago', '--oneline', '--', skill_path],
            capture_output=True,
            text=True,
            cwd=os.getcwd()
        )
        return result.stdout.strip().split('\n') if result.stdout.strip() else []
    except Exception as e:
        print(f"⚠️  获取提交记录失败: {e}")
        return []

def check_lock_file(skill_name):
    """检查是否有锁文件"""
    lock_file = f".lock/{skill_name}.lock"
    if os.path.exists(lock_file):
        with open(lock_file, 'r') as f:
            content = f.read().strip()
        return content
    return None

def parse_author_from_commit(commit_msg):
    """从提交信息中解析作者"""
    # 匹配 [author] 或 author: xxx 格式
    patterns = [
        r'\[(\w+)\]',           # [egg]
        r'by\s+(\w+)',          # by egg
        r'author[:\s]+(\w+)',   # author: egg
    ]
    for pattern in patterns:
        match = re.search(pattern, commit_msg, re.IGNORECASE)
        if match:
            return match.group(1)
    return "unknown"

def check_conflicts(skill_path):
    """检查潜在的冲突"""
    skill_name = os.path.basename(skill_path)
    
    print(f"🔍 检查 skill: {skill_name}")
    print("=" * 50)
    
    # 1. 检查锁文件
    lock = check_lock_file(skill_name)
    if lock:
        print(f"🚧 发现锁文件: {lock}")
        print("   请等待对方完成编辑后再进行修改")
        return 1
    
    # 2. 检查最近提交
    commits = get_recent_commits(skill_path)
    if commits:
        print(f"📜 发现最近 {len(commits)} 个提交:")
        for commit in commits[:5]:  # 只显示最近5个
            author = parse_author_from_commit(commit)
            print(f"   - {commit} [by {author}]")
        
        if len(commits) > 5:
            print(f"   ... 还有 {len(commits) - 5} 个提交")
    
    # 3. 检查本地修改
    try:
        result = subprocess.run(
            ['git', 'status', '--short', '--', skill_path],
            capture_output=True,
            text=True
        )
        if result.stdout.strip():
            print(f"⚠️  本地有未提交的修改:")
            for line in result.stdout.strip().split('\n'):
                print(f"   {line}")
    except Exception as e:
        pass
    
    # 4. 检查远程更新
    try:
        subprocess.run(['git', 'fetch', 'origin'], capture_output=True)
        result = subprocess.run(
            ['git', 'log', 'HEAD..origin/main', '--oneline', '--', skill_path],
            capture_output=True,
            text=True
        )
        if result.stdout.strip():
            commits_ahead = result.stdout.strip().split('\n')
            print(f"📥 远程有 {len(commits_ahead)} 个新提交未拉取:")
            for commit in commits_ahead[:3]:
                print(f"   - {commit}")
            print("   请先执行: git pull origin main")
            return 1
    except Exception as e:
        pass
    
    print("\n✅ 检查通过，可以安全地进行修改")
    return 0

def main():
    if len(sys.argv) < 2:
        print("用法: python check-ai-conflict.py <skill-path>")
        print("示例: python check-ai-conflict.py skills/memory-system-c3")
        sys.exit(1)
    
    skill_path = sys.argv[1]
    exit_code = check_conflicts(skill_path)
    sys.exit(exit_code)

if __name__ == '__main__':
    main()
