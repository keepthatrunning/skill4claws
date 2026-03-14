#!/usr/bin/env python3
"""
仓库提交前检查脚本
检测敏感文件和大文件，防止泄露
"""

import os
import sys
import subprocess

# 敏感文件/目录模式
SENSITIVE_PATTERNS = [
    # 工作目录
    r'^browser/',
    r'^credentials/',
    r'^cron/',
    r'^devices/',
    r'^extensions/',
    r'^feishu/',
    r'^identity/',
    r'^logs/',
    r'^media/',
    r'^memory/',
    r'^scripts/$',  # 根目录 scripts，但保留项目脚本
    r'^subagents/',
    r'^workspace/',
    
    # 敏感文件
    r'\.coze$',
    r'^openclaw\.json',
    r'^update-check\.json',
    r'\.key$',
    r'\.pem$',
    r'\.env$',
    r'\.env\.local$',
    r'credentials\.json$',
    
    # 缓存/临时文件
    r'\.log$',
    r'\.tmp$',
    r'\.cache$',
    r'__pycache__/',
    
    # 大文件扩展名 (需要 LFS)
    r'\.mp4$',
    r'\.mov$',
    r'\.avi$',
    r'\.psd$',
    r'\.ai$',
]

# 允许的项目级脚本 (相对于仓库根目录)
ALLOWED_SCRIPTS = [
    'scripts/check-sync.py',
    'scripts/release.py',
    'scripts/sync-readme.py',
    'scripts/check-ai-conflict.py',
    'scripts/notify-ai-update.py',
    'scripts/repo-sanity-check.py',
    'scripts/pre-commit-check.py',
]

# 大文件阈值 (10MB)
LARGE_FILE_THRESHOLD = 10 * 1024 * 1024

def get_staged_files():
    """获取已暂存的文件列表"""
    try:
        result = subprocess.run(
            ['git', 'diff', '--cached', '--name-only', '--diff-filter=ACMR'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip().split('\n') if result.stdout.strip() else []
    except subprocess.CalledProcessError:
        return []

def check_sensitive_files(files):
    """检查敏感文件"""
    import re
    violations = []
    
    for file in files:
        for pattern in SENSITIVE_PATTERNS:
            if re.search(pattern, file):
                # 检查是否在允许列表中
                if file.startswith('scripts/'):
                    if file not in ALLOWED_SCRIPTS:
                        violations.append((file, pattern))
                else:
                    violations.append((file, pattern))
                break
    
    return violations

def check_large_files(files):
    """检查大文件"""
    large_files = []
    
    for file in files:
        if not os.path.exists(file):
            continue
        
        try:
            size = os.path.getsize(file)
            if size > LARGE_FILE_THRESHOLD:
                large_files.append((file, size))
        except OSError:
            pass
    
    return large_files

def check_gitignore():
    """检查 .gitignore 是否存在"""
    if not os.path.exists('.gitignore'):
        return False, "❌ .gitignore 文件不存在"
    
    with open('.gitignore', 'r') as f:
        content = f.read()
    
    required_patterns = [
        'browser/',
        'credentials/',
        'logs/',
        '.env',
    ]
    
    missing = []
    for pattern in required_patterns:
        if pattern not in content:
            missing.append(pattern)
    
    if missing:
        return False, f"⚠️  .gitignore 缺少关键规则: {', '.join(missing)}"
    
    return True, "✅ .gitignore 配置正确"

def main():
    print("🔍 执行仓库提交前检查...\n")
    
    has_error = False
    
    # 1. 检查 .gitignore
    print("1️⃣  检查 .gitignore 配置...")
    ok, msg = check_gitignore()
    print(f"   {msg}")
    if not ok:
        has_error = True
    print()
    
    # 2. 获取已暂存文件
    print("2️⃣  检查已暂存文件...")
    staged_files = get_staged_files()
    
    if not staged_files:
        print("   ⚠️  没有已暂存的文件")
        return 0
    
    print(f"   发现 {len(staged_files)} 个已暂存文件")
    print()
    
    # 3. 检查敏感文件
    print("3️⃣  检查敏感文件...")
    sensitive = check_sensitive_files(staged_files)
    
    if sensitive:
        print("   ❌ 检测到敏感文件/目录:")
        for file, pattern in sensitive:
            print(f"      - {file} (匹配: {pattern})")
        print("\n   💡 解决方法:")
        print("      1. 添加到 .gitignore")
        print("      2. 从暂存区移除: git reset HEAD <file>")
        print("      3. 如需保留，检查是否误判")
        has_error = True
    else:
        print("   ✅ 未检测到敏感文件")
    print()
    
    # 4. 检查大文件
    print("4️⃣  检查大文件 (>10MB)...")
    large = check_large_files(staged_files)
    
    if large:
        print("   ⚠️  检测到大文件:")
        for file, size in large:
            size_mb = size / (1024 * 1024)
            print(f"      - {file} ({size_mb:.2f} MB)")
        print("\n   💡 建议:")
        print("      1. 使用 Git LFS 管理大文件")
        print("      2. 从提交中移除: git reset HEAD <file>")
        print("      3. 压缩或分割文件")
        has_error = True
    else:
        print("   ✅ 未检测到大文件")
    print()
    
    # 5. 总结
    print("=" * 50)
    if has_error:
        print("❌ 检查未通过，请修复上述问题后再提交")
        print("\n如需强制提交，使用: git commit --no-verify")
        return 1
    else:
        print("✅ 所有检查通过，可以安全提交")
        return 0

if __name__ == '__main__':
    sys.exit(main())
