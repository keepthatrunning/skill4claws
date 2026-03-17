# 版本发布工作流程

## 发布前检查清单

- [ ] 所有测试通过
- [ ] 代码审查完成
- [ ] 文档已同步更新
- [ ] CHANGELOG 已更新
- [ ] 版本号已确定

## 标准发布流程

### 1. 准备阶段

```bash
# 确保在主分支且工作区干净
git checkout main
git pull origin main
git status  # 应该为空
```

### 2. 版本号决策

根据变更类型选择版本号递增方式：

| 变更类型 | 版本变化 | 示例 |
|----------|----------|------|
| Bug修复 | 修订号+1 | 1.0.0 → 1.0.1 |
| 功能新增 | 次版本+1 | 1.0.0 → 1.1.0 |
| 破坏性变更 | 主版本+1 | 1.0.0 → 2.0.0 |

### 3. 执行发布

使用 release.py 脚本自动化：

```bash
# 补丁版本
python scripts/release.py --type patch

# 次要版本
python scripts/release.py --type minor

# 主要版本
python scripts/release.py --type major

# 指定版本号
python scripts/release.py --version 2.0.0
```

### 4. 推送发布

```bash
# 推送代码
git push origin main

# 推送标签
git push origin v1.1.0
```

### 5. GitHub Release (可选)

创建 GitHub Release 页面：

```bash
# 使用 gh CLI
gh release create v1.1.0 \
  --title "Release v1.1.0" \
  --notes-file CHANGELOG.md
```

## 紧急修复流程 (Hotfix)

```bash
# 1. 从最新标签创建修复分支
git checkout -b hotfix/critical-bug v1.0.0

# 2. 修复问题
# ... 编写修复代码 ...

# 3. 更新版本号 (补丁版本)
python scripts/release.py --type patch

# 4. 推送并合并回main
git push origin hotfix/critical-bug
# 创建PR合并到main

# 5. 发布后合并回开发分支
git checkout develop
git merge main
```
