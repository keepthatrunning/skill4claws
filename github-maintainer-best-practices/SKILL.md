---
name: github-maintainer-best-practices
description: |
  GitHub仓库维护最佳实践 v2.2.0 - 开源项目规范化管理指南。
  涵盖代码与文档同步、README维护、版本号管理、提交规范、CHANGELOG维护、README自动同步、多AI协作冲突解决等完整工作流程。
  使用场景：(1) 更新代码后同步更新README，(2) 发布新版本时维护CHANGELOG和版本号，(3) 规范化Git提交信息，(4) 管理开源项目的文档一致性，(5) 建立项目维护的标准操作流程，(6) CI自动检查文档同步，(7) AI Agent自动README同步，(8) 多AI协作版本控制与冲突解决
version: 2.2.0
author: egg小姐
date: 2026-03-14
---

# GitHub 仓库维护最佳实践 v2.2.0

开源项目规范化管理的完整指南，确保代码与文档始终同步。

## 🆕 v2.2.0 新特性

| 特性 | 说明 |
|------|------|
| **CI 自动检查** | GitHub Actions 工作流自动检查文档同步 |
| **PR 模板** | 标准化的 PR 检查清单模板 |
| **版本验证** | 自动化版本号一致性检查 |
| **README 自动同步** | AI Agent 自动扫描仓库改动并同步更新 README |
| **多AI协作** | 版本冲突检测、锁定机制、分支策略、协作流程 |

### 快速设置 CI 检查

1. 复制模板到你的项目:
   ```bash
   cp templates/ci-check.yml .github/workflows/
   cp templates/pr-template.md .github/pull_request_template.md
   ```

2. 提交并启用:
   ```bash
   git add .github/
   git commit -m "ci: add documentation sync check"
   git push
   ```

3. 后续 PR 将自动检查文档同步状态

## 核心原则

### 1. 代码与文档同步法则

**黄金法则**: 任何代码变更都必须有对应的文档更新

```
代码变更
    ↓
影响评估 (API变更? 功能新增? 配置修改?)
    ↓
同步更新文档
    ├── README.md (如影响使用方式)
    ├── CHANGELOG.md (记录变更)
    ├── 版本号 (如为功能性更新)
    └── 相关引用文档
    ↓
提交时一并推送
```

### 2. README.md 维护清单

每次更新后检查：

- [ ] **功能列表** - 新增/修改的功能是否已描述
- [ ] **安装指南** - 依赖或安装步骤是否有变化
- [ ] **使用示例** - API或用法变更需更新示例代码
- [ ] **配置说明** - 新增配置项需补充文档
- [ ] **版本徽章** - 版本号是否已更新
- [ ] **最后更新日期** - 时间戳是否已刷新

### 2.5 AI Agent 自动 README 同步规则 ⭐ NEW

**规则**: 每次更新 GitHub 仓库或上传技能更新后，自动扫描仓库改动并同步更新 README

**触发条件**:
- 成功执行 `git push` 后
- 新增/修改/删除 skills 文件后
- 更新 GitHub Actions 工作流后

**自动扫描清单**:
```
推送完成
    ↓
扫描仓库改动
    ├── 新增 skills? → 更新 README 技能列表
    ├── 删除 skills? → 从 README 移除对应条目
    ├── 修改 skill 版本? → 更新 README 版本号
    ├── 新增 scripts? → 更新 README 脚本说明
    └── 修改 docs? → 更新 README 文档链接
    ↓
生成 README 更新摘要
    ↓
提交并推送 README 更新
```

**README 同步检查清单**:
- [ ] **技能数量** - 统计 skills/ 目录下的 skill 数量，更新 README 头部统计
- [ ] **技能列表** - 检查每个 skill 是否在 README 中有对应条目
- [ ] **版本号** - 同步 SKILL.md 中的 version 到 README
- [ ] **最后更新日期** - 更新为当前日期
- [ ] **新技能描述** - 为新技能生成简洁描述（基于 SKILL.md 的 description）
- [ ] **分类整理** - 确保技能按正确分类排列

**实施方式**:
```bash
# 方式1: 手动执行同步脚本
python scripts/sync-readme.py

# 方式2: 在 CI 中自动执行 (推荐)
# 添加到 .github/workflows/post-push-sync.yml
```

**同步脚本逻辑**:
1. 遍历 `skills/` 目录，读取每个 `SKILL.md` 的元数据
2. 对比 README.md 中的技能列表
3. 检测差异：新增、删除、版本变更
4. 自动更新 README.md 的对应部分
5. 生成提交：`docs: sync README with latest skills (auto-update)`
6. 自动推送更新

### 3. 版本号管理 (SemVer)

遵循语义化版本规范：`主版本.次版本.修订号`

| 变更类型 | 版本号变化 | 示例 | 文档更新 |
|----------|------------|------|----------|
| Bug修复 | 修订号+1 | 1.0.0 → 1.0.1 | CHANGELOG |
| 功能新增 | 次版本+1 | 1.0.0 → 1.1.0 | README + CHANGELOG |
| 破坏性变更 | 主版本+1 | 1.0.0 → 2.0.0 | README + CHANGELOG + 迁移指南 |

### 4. 提交信息规范 (Conventional Commits)

```
<type>(<scope>): <subject>

<body>

<footer>
```

**类型 (type)**:
- `feat`: 新功能
- `fix`: Bug修复
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 重构
- `test`: 测试相关
- `chore`: 构建/工具变更

**示例**:
```
feat(api): add user authentication endpoint

- Add JWT token validation
- Add login/logout endpoints
- Update README with auth examples

Closes #123
```

### 3. 多AI协作版本控制策略 ⭐ NEW

**问题**: 多个AI同时更新同一个Skill时可能产生版本冲突

**解决方案**:

#### 3.1 更新前检查 (Pre-Update Check)

```bash
# 1. 拉取最新代码
git pull origin main

# 2. 检查是否有其他AI的未合并更新
git log --oneline --since="1 hour ago" -- skills/your-skill/

# 3. 如检测到他人更新，执行冲突评估
python scripts/check-ai-conflict.py skills/your-skill/
```

#### 3.2 版本号冲突检测

**规则**: 版本号采用 `主版本.次版本.修订号-AI标识.序号` 格式

```yaml
# 示例版本号
version: "2.1.0-egg.1"    # egg小姐的第1个修订
version: "2.1.0-egg.2"    # egg小姐的第2个修订
version: "2.1.0-other.1"  # 其他AI的第1个修订
```

**合并时**:
- 如修改不同文件 → 保留双方版本号，合并为 `2.1.0-merged`
- 如修改相同文件 → 协商确定最终版本号

#### 3.3 分支策略 (推荐)

```
main (受保护分支)
    ↓
feature/skill-name-ai-id (个人开发分支)
    ↓
PR → Code Review (自动/人工) → Merge to main
```

**AI协作流程**:
```
1. 创建个人分支
   git checkout -b feature/memory-system-c3-egg

2. 进行修改并提交
   git add .
   git commit -m "feat(memory-system-c3): add auto-compact script [egg]"

3. 推送到远程
   git push origin feature/memory-system-c3-egg

4. 创建 PR (Pull Request)
   - 使用 PR 模板
   - 说明修改内容
   - 标记相关AI进行Review

5. 等待CI检查通过
   - 文档同步检查
   - 版本号验证
   - 冲突检测

6. 合并到 main
   git checkout main
   git pull origin main
   git merge feature/memory-system-c3-egg
   git push origin main
```

#### 3.4 冲突解决优先级

| 优先级 | 判定标准 | 处理方式 |
|--------|----------|----------|
| **P0** | 修改完全冲突（同一文件的同一部分） | 双方协商，取最优方案 |
| **P1** | 修改部分重叠（同一文件的不同部分） | Git自动合并 + 人工验证 |
| **P2** | 修改独立（不同文件） | 自动合并，无需干预 |
| **P3** | 仅元数据变更（版本号、日期） | 取最新时间戳 |

#### 3.5 协作锁定机制 (可选)

**方式1: 文件锁 (File Lock)**
```bash
# 开始编辑前创建锁文件
echo "editing by egg at $(date)" > .lock/memory-system-c3.lock
git add .lock/memory-system-c3.lock
git commit -m "lock: memory-system-c3 [egg]"
git push

# 编辑完成后删除锁
git rm .lock/memory-system-c3.lock
git commit -m "unlock: memory-system-c3 [egg]"
git push
```

**方式2: 声明式锁定 (Declaration)**
```markdown
# 在 skill 的 README 顶部添加
> 🚧 **正在编辑**: egg小姐 | 开始时间: 2026-03-14 10:00 | 预计完成: 2小时
> 请勿在此期间修改此 skill，如需协作请 @egg
```

#### 3.6 更新后通知

```bash
# 推送后发送通知给其他AI
python scripts/notify-ai-update.py \
  --skill memory-system-c3 \
  --version 2.1.0 \
  --changes "add auto-compact script" \
  --author egg
```

### 5. CHANGELOG 维护

使用 [Keep a Changelog](https://keepachangelog.com/) 格式：

```markdown
## [Unreleased]

### Added
- 新增功能描述

### Changed
- 变更的功能描述

### Fixed
- 修复的Bug描述

## [1.0.0] - 2026-03-13

### Added
- 初始版本发布
- 核心功能实现
```

## 使用工作流程

### 场景1: 新增功能

```bash
# 1. 开发功能
git checkout -b feature/new-feature
# ... 编写代码 ...

# 2. 同步更新文档
# 更新 README.md - 添加功能描述和使用示例
# 更新 CHANGELOG.md - 在 [Unreleased] 下添加 ### Added

# 3. 检查版本号
# 如为功能新增，准备更新次版本号

# 4. 提交（代码+文档一起）
git add .
git commit -m "feat(scope): add new feature

- Implementation details
- Update README with examples
- Update CHANGELOG

Relates to #456"

# 5. 推送
git push origin feature/new-feature
```

### 场景2: 发布新版本

```bash
# 使用脚本自动处理版本发布
python scripts/release.py --version 1.1.0 --type minor
```

详见 [references/release-workflow.md](references/release-workflow.md)

### 场景3: 快速修复同步检查

```bash
# 在提交前自动检查文档同步状态
python scripts/check-sync.py
```

## 自动化工具

### check-sync.py - 同步检查脚本

检查代码变更后文档是否已更新：

```bash
# 检查当前分支与main的差异
python scripts/check-sync.py

# 输出示例:
# ⚠️  检测到以下变更可能需同步文档更新:
#    - src/api/auth.js (修改)
#      → 建议更新: README.md (API文档)
#    
#    - package.json (版本号变更)
#      → 建议更新: README.md (版本徽章)
```

### release.py - 版本发布助手

自动化版本发布流程：

```bash
# 发布补丁版本 (1.0.0 → 1.0.1)
python scripts/release.py --type patch

# 发布次要版本 (1.0.0 → 1.1.0)
python scripts/release.py --type minor

# 发布主要版本 (1.0.0 → 2.0.0)
python scripts/release.py --type major
```

### check-ai-conflict.py - AI冲突检测 ⭐ NEW

在编辑前检查是否有其他AI正在修改：

```bash
# 检查指定skill的冲突情况
python scripts/check-ai-conflict.py skills/memory-system-c3

# 输出示例:
# 🔍 检查 skill: memory-system-c3
# ==================================================
# 📜 发现最近 2 个提交:
#    - a1b2c3d feat: add auto-compact [by other-ai]
#    - e4f5g6h fix: typo in README [by egg]
# ⚠️  远程有 1 个新提交未拉取:
#    - i7j8k9l docs: update description [by another-ai]
#    请先执行: git pull origin main
```

### notify-ai-update.py - AI更新通知 ⭐ NEW

推送更新后通知其他AI：

```bash
# 发送更新通知
python scripts/notify-ai-update.py \
  --skill memory-system-c3 \
  --version 2.1.0 \
  --changes "add heartbeat-check script" \
  --author egg \
  --save \
  --update-changelog

# 输出:
# 📢 AI Skill 更新通知
# ==================================================
# 📝 Skill: memory-system-c3
# 🔖 版本: 2.1.0
# 👤 作者: egg
# 🕐 时间: 2026-03-14T10:30:00
# 📋 变更内容: add heartbeat-check script
# 💡 建议操作:
#    - 其他AI可拉取最新代码查看变更
#    - 如有冲突请协商解决
# ==================================================
```

## 项目结构最佳实践

```
project/
├── README.md              # 项目入口文档
├── CHANGELOG.md           # 变更日志
├── CONTRIBUTING.md        # 贡献指南
├── LICENSE                # 许可证
├── package.json / setup.py # 版本号定义
├── docs/                  # 详细文档
│   ├── api.md
│   ├── configuration.md
│   └── examples.md
└── scripts/               # 维护脚本
    ├── check-sync.py
    └── release.py
```

## 常见问题

### Q: 小型项目也需要这么严格吗?
**A**: 建议至少遵循"代码与README同步"原则。项目越小，文档越重要，因为用户没有时间去翻看源码。

### Q: 忘记更新文档就提交了怎么办?
**A**: 可以追加提交 (amend) 如果还没推送；如果已推送，补充一个 `docs:` 类型的提交专门更新文档。

### Q: 如何确保团队成员遵守规范?
**A**: 
1. 在 CONTRIBUTING.md 中明确规范
2. 使用 PR 模板强制检查清单
3. 在 CI 中添加自动化检查

详见 [references/team-enforcement.md](references/team-enforcement.md)
