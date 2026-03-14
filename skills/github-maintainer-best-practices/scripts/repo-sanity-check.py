#!/usr/bin/env python3
"""
仓库健康检查脚本
全面的仓库结构和内容检查
"""

import os
import sys
import subprocess
from pathlib import Path

# 必须存在的文件
REQUIRED_FILES = [
    'README.md',
    'LICENSE',
    '.gitignore',
]

# 建议存在的文件
RECOMMENDED_FILES = [
    'CHANGELOG.md',
    'CONTRIBUTING.md',
]

# 禁止存在的敏感目录
FORBIDDEN_DIRS = [
    'browser',
    'credentials',
    'cron',
    'devices',
    'extensions',
    'feishu',
    'identity',
    'logs',
    'media',
    'memory',
    'subagents',
    'workspace',
]

# 禁止存在的敏感文件
FORBIDDEN_FILES = [
    '.coze',
    'openclaw.json',
    'openclaw.json.bak',
    'update-check.json',
]

def check_required_files():
    """检查必需文件"""
    print("1️⃣  检查必需文件...")
    missing = []
    for file in REQUIRED_FILES:
        if not os.path.exists(file):
            missing.append(file)
    
    if missing:
        print(f"   ❌ 缺少必需文件: {', '.join(missing)}")
        return False
    else:
        print("   ✅ 所有必需文件存在")
        return True

def check_recommended_files():
    """检查推荐文件"""
    print("\n2️⃣  检查推荐文件...")
    missing = []
    for file in RECOMMENDED_FILES:
        if not os.path.exists(file):
            missing.append(file)
    
    if missing:
        print(f"   ⚠️  缺少推荐文件: {', '.join(missing)}")
    else:
        print("   ✅ 所有推荐文件存在")
    return True

def check_forbidden_items():
    """检查禁止的文件和目录"""
    print("\n3️⃣  检查敏感文件/目录...")
    violations = []
    
    # 检查禁止的目录
    for dir_name in FORBIDDEN_DIRS:
        if os.path.isdir(dir_name):
            violations.append(f"目录: {dir_name}/")
    
    # 检查禁止的文件
    for file_name in FORBIDDEN_FILES:
        if os.path.exists(file_name):
            violations.append(f"文件: {file_name}")
    
    # 检查根目录下的 scripts (除非是项目脚本)
    if os.path.isdir('scripts'):
        # 检查是否包含非项目脚本
        non_project_scripts = []
        for item in os.listdir('scripts'):
            if item.endswith('.js') and 'evomap' in item.lower():
                non_project_scripts.append(item)
        if non_project_scripts:
            violations.append(f"scripts/ 包含工作脚本: {', '.join(non_project_scripts)}")
    
    if violations:
        print("   ❌ 检测到敏感文件/目录:")
        for v in violations:
            print(f"      - {v}")
        print("\n   💡 解决方法:")
        print("      git rm -r --cached <path>")
        print("      echo '<path>/' >> .gitignore")
        return False
    else:
        print("   ✅ 未检测到敏感文件/目录")
        return True

def check_gitignore():
    """检查 .gitignore 配置"""
    print("\n4️⃣  检查 .gitignore 配置...")
    
    if not os.path.exists('.gitignore'):
        print("   ❌ .gitignore 不存在")
        return False
    
    with open('.gitignore', 'r') as f:
        content = f.read()
    
    required_patterns = [
        ('browser/', '浏览器数据'),
        ('credentials/', '凭证文件'),
        ('logs/', '日志文件'),
        ('.env', '环境变量'),
        ('node_modules/', '依赖目录'),
    ]
    
    missing = []
    for pattern, desc in required_patterns:
        if pattern not in content:
            missing.append((pattern, desc))
    
    if missing:
        print("   ⚠️  .gitignore 缺少以下规则:")
        for pattern, desc in missing:
            print(f"      - {pattern} ({desc})")
        return False
    else:
        print("   ✅ .gitignore 配置完整")
        return True

def check_large_files():
    """检查大文件"""
    print("\n5️⃣  检查大文件 (>10MB)...")
    
    try:
        result = subprocess.run(
            ['git', 'ls-files'],
            capture_output=True,
            text=True
        )
        files = result.stdout.strip().split('\n')
        
        large_files = []
        for file in files:
            if not file:
                continue
            try:
                size = os.path.getsize(file)
                if size > 10 * 1024 * 1024:  # 10MB
                    large_files.append((file, size))
            except OSError:
                pass
        
        if large_files:
            print("   ⚠️  检测到大文件:")
            for file, size in large_files:
                print(f"      - {file} ({size/1024/1024:.2f} MB)")
            return False
        else:
            print("   ✅ 未检测到大文件")
            return True
    except Exception as e:
        print(f"   ⚠️  无法检查大文件: {e}")
        return True

def check_repo_structure():
    """检查仓库结构"""
    print("\n6️⃣  检查仓库结构...")
    
    items = []
    for item in os.listdir('.'):
        if item.startswith('.') and item != '.gitignore':
            continue
        if item == '.git':
            continue
        items.append(item)
    
    print("   根目录内容:")
    for item in sorted(items):
        if os.path.isdir(item):
            print(f"      📁 {item}/")
        else:
            print(f"      📄 {item}")
    
    return True

def generate_report():
    """生成检查报告"""
    print("\n" + "=" * 50)
    print("📊 仓库健康检查报告")
    print("=" * 50)
    
    checks = [
        ("必需文件", check_required_files),
        ("推荐文件", check_recommended_files),
        ("敏感文件", check_forbidden_items),
        (".gitignore", check_gitignore),
        ("大文件", check_large_files),
        ("仓库结构", check_repo_structure),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ 检查 '{name}' 时出错: {e}")
            results.append((name, False))
    
    print("\n" + "=" * 50)
    print("📋 检查结果汇总")
    print("=" * 50)
    
    all_passed = True
    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"   {status} - {name}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("✅ 所有检查通过！仓库状态健康。")
        return 0
    else:
        print("❌ 部分检查未通过，请修复上述问题。")
        print("\n💡 如需重建干净仓库:")
        print("   1. 创建新目录")
        print("   2. 仅复制必要文件 (skills/, docs/, README.md, LICENSE)")
        print("   3. 创建正确的 .gitignore")
        print("   4. git init && git add . && git commit")
        print("   5. git push origin main --force")
        return 1

def main():
    print("🔍 GitHub 仓库健康检查")
    print("=" * 50)
    print()
    
    # 检查是否在 git 仓库中
    if not os.path.exists('.git'):
        print("❌ 当前目录不是 git 仓库")
        return 1
    
    return generate_report()

if __name__ == '__main__':
    sys.exit(main())
