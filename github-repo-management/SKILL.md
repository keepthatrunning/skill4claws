# GitHub 仓库管理规则 - identity-egg-v1.0

> 本文件记录 egg 在 GitHub 私有仓库的管理规则和最佳实践
> 仓库地址: https://github.com/keepthatrunning/identity-egg-v1.0
> 最后更新: 2026-03-17

---

## 🔴 Critical 规则（必须遵守）

### 1. Release 发布前必须确认
- **规则**: 任何 GitHub Release 的创建必须经过用户明确确认
- **触发场景**: 
  - 自动备份脚本生成 release
  - 手动创建 release
  - 通过 API 发布 release
- **确认流程**:
  1. 准备 release 内容（文件、版本号、说明）
  2. 向用户报告: "准备发布 release [版本号]，包含 [内容概述]，是否确认？"
  3. 获得明确确认后才执行
- **违规后果**: 可能导致未审核的内容对外发布

---

## 🟡 High 优先级规则

### 2. 备份文件保留策略
- **规则**: 所有历史备份文件永久保留，不得删除
- **原因**: 
  - 备份是 egg 的完整状态快照
  - 删除后无法恢复历史版本
  - 可能包含重要记忆或配置
- **例外情况**: 无（即使磁盘空间不足也需用户确认）

### 3. 强制推送需谨慎
- **规则**: 使用 `git push -f` 重写历史前必须确认影响范围
- **检查清单**:
  - [ ] 确认当前分支状态
  - [ ] 确认是否有其他协作者
  - [ ] 确认是否会影响 open PR
  - [ ] 向用户报告影响范围
  - [ ] 获得明确确认

---

## 🟢 Medium 优先级规则

### 4. 仓库结构规范
```
identity-egg-v1.0/
├── egg-backup-YYYYMMDD-HHMMSS.tar.gz    # 备份文件（根目录）
├── archive-YYYYMMDD-HHMMSS.tar.gz       # 归档文件（历史文件打包）
└── README.md                            # 仓库说明（可选）
```

- **备份文件**: 直接放在根目录，命名格式 `egg-backup-YYYYMMDD-HHMMSS.tar.gz`
- **归档文件**: 将零散文件打包，命名格式 `archive-YYYYMMDD-HHMMSS.tar.gz`
- **避免**: 散落的配置文件、未打包的目录

### 5. 备份内容规范

**必须包含:**
- MEMORY.md, RECENT_EVENTS.md（记忆系统）
- memory/ 目录（详细记忆文件）
- SOUL.md, AGENTS.md, IDENTITY.md（核心身份文件）
- TOOLS.md, USER.md（工具和用户信息）
- skills/ 目录（所有技能）
- HEARTBEAT.md（定时任务配置）

**排除项:**
- .git/ 目录
- node_modules/
- *.log 文件
- 临时文件

---

## 📋 操作流程

### 创建新备份
```bash
# 1. 打包（排除不需要的文件）
tar --exclude='.git' --exclude='node_modules' --exclude='*.log' \
    -czf egg-backup-$(date +%Y%m%d-%H%M%S).tar.gz workspace/

# 2. 确认文件大小合理
ls -lh egg-backup-*.tar.gz

# 3. 推送到仓库（先确认！）
```

### 整理仓库结构
1. 克隆仓库到临时目录
2. 识别需要保留的备份文件
3. 将其他文件打包为 archive-*.tar.gz
4. 清理零散文件
5. **确认后再推送**

---

## ⚠️ 常见错误

| 错误 | 后果 | 预防 |
|------|------|------|
| 未经确认发布 release | 可能泄露敏感信息 | 严格执行确认流程 |
| 删除旧备份 | 历史状态丢失 | 永不删除，只新增 |
| 强制推送未确认 | 协作冲突 | 检查影响范围 |
| 备份遗漏关键文件 | 恢复不完整 | 对照备份内容清单 |

---

## 🔗 相关资源

- 仓库地址: https://github.com/keepthatrunning/identity-egg-v1.0
- 当前备份列表:
  - egg-backup-20260313-142800.tar.gz (34 KB)
  - egg-backup-20260314-180100.tar.gz (8.3 MB)
  - archive-20260317-110800.tar.gz (3.0 MB)
- Release 列表: 保留所有历史 release

---

*本规则由 egg 维护，更新需记录变更日志*
