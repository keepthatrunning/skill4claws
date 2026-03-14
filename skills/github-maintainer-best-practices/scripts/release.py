#!/usr/bin/env python3
"""
版本发布助手
自动化版本号更新、CHANGELOG维护、Git标签创建
"""

import subprocess
import re
import os
import sys
from datetime import datetime
from pathlib import Path

def get_current_version():
    """从package.json或setup.py获取当前版本"""
    # 尝试从package.json读取
    if os.path.exists('package.json'):
        with open('package.json', 'r') as f:
            content = f.read()
            match = re.search(r'"version":\s*"([^"]+)"', content)
            if match:
                return match.group(1)
    
    # 尝试从setup.py读取
    if os.path.exists('setup.py'):
        with open('setup.py', 'r') as f:
            content = f.read()
            match = re.search(r'version=[\'"]([^\'"]+)[\'"]', content)
            if match:
                return match.group(1)
    
    # 尝试从pyproject.toml读取
    if os.path.exists('pyproject.toml'):
        with open('pyproject.toml', 'r') as f:
            content = f.read()
            match = re.search(r'version\s*=\s*"([^"]+)"', content)
            if match:
                return match.group(1)
    
    return "0.0.0"

def bump_version(version, bump_type):
    """根据类型递增版本号"""
    parts = version.split('.')
    major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])
    
    if bump_type == 'major':
        major += 1
        minor = 0
        patch = 0
    elif bump_type == 'minor':
        minor += 1
        patch = 0
    else:  # patch
        patch += 1
    
    return f"{major}.{minor}.{patch}"

def update_package_json(new_version):
    """更新package.json中的版本号"""
    if not os.path.exists('package.json'):
        return False
    
    with open('package.json', 'r') as f:
        content = f.read()
    
    content = re.sub(
        r'("version":\s*")([^"]+)(")',
        f'\\g<1>{new_version}\\g<3>',
        content
    )
    
    with open('package.json', 'w') as f:
        f.write(content)
    
    return True

def update_setup_py(new_version):
    """更新setup.py中的版本号"""
    if not os.path.exists('setup.py'):
        return False
    
    with open('setup.py', 'r') as f:
        content = f.read()
    
    content = re.sub(
        r"(version=)['\"]([^'\"]+)['\"]",
        f"\\g<1>'{new_version}'",
        content
    )
    
    with open('setup.py', 'w') as f:
        f.write(content)
    
    return True

def update_changelog(new_version, bump_type):
    """更新CHANGELOG.md"""
    changelog_path = 'CHANGELOG.md'
    today = datetime.now().strftime('%Y-%m-%d')
    
    new_section = f"""## [{new_version}] - {today}

### Added
- 

### Changed
- 

### Fixed
- 

"""
    
    if os.path.exists(changelog_path):
        with open(changelog_path, 'r') as f:
            content = f.read()
        
        # 在Unreleased后插入新版本
        content = re.sub(
            r'(## \[Unreleased\]\n)',
            f'\\g<1>\n{new_section}',
            content
        )
        
        with open(changelog_path, 'w') as f:
            f.write(content)
    else:
        # 创建新的CHANGELOG
        content = f"""# Changelog

所有 notable changes 将记录在此文件。

格式基于 [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)，
版本号遵循 [Semantic Versioning](https://semver.org/lang/zh-CN/)。

## [Unreleased]

{new_section}"""
        
        with open(changelog_path, 'w') as f:
            f.write(content)
    
    return True

def create_git_tag(version):
    """创建Git标签"""
    tag_name = f"v{version}"
    subprocess.run(['git', 'tag', '-a', tag_name, '-m', f'Release {tag_name}'], check=True)
    return tag_name

def main():
    import argparse
    parser = argparse.ArgumentParser(description='版本发布助手')
    parser.add_argument('--type', choices=['patch', 'minor', 'major'], default='patch',
                       help='版本升级类型 (默认: patch)')
    parser.add_argument('--version', help='指定版本号 (覆盖自动计算)')
    parser.add_argument('--no-tag', action='store_true', help='不创建Git标签')
    
    args = parser.parse_args()
    
    # 检查git状态
    result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
    if result.stdout.strip():
        print("❌ 错误: 工作区有未提交的变更")
        print("请先提交或暂存当前变更")
        sys.exit(1)
    
    # 获取当前版本
    current = get_current_version()
    print(f"📦 当前版本: {current}")
    
    # 计算新版本
    if args.version:
        new_version = args.version
    else:
        new_version = bump_version(current, args.type)
    
    print(f"🆙 新版本: {new_version}")
    
    # 确认
    response = input(f"\n确认发布 v{new_version}? [Y/n]: ")
    if response.lower() not in ('', 'y', 'yes'):
        print("已取消")
        sys.exit(0)
    
    # 更新版本文件
    updated = False
    if update_package_json(new_version):
        print("✅ 已更新 package.json")
        updated = True
    if update_setup_py(new_version):
        print("✅ 已更新 setup.py")
        updated = True
    
    # 更新CHANGELOG
    if update_changelog(new_version, args.type):
        print("✅ 已更新 CHANGELOG.md")
    
    # 提交变更
    subprocess.run(['git', 'add', '-A'], check=True)
    subprocess.run(['git', 'commit', '-m', f'chore(release): bump version to {new_version}'], check=True)
    print(f"✅ 已提交版本更新")
    
    # 创建标签
    if not args.no_tag:
        tag = create_git_tag(new_version)
        print(f"✅ 已创建标签: {tag}")
    
    print(f"\n🎉 版本 {new_version} 发布准备完成!")
    print(f"   执行以下命令推送到远程:\n")
    print(f"   git push origin main")
    if not args.no_tag:
        print(f"   git push origin v{new_version}")

if __name__ == '__main__':
    main()
