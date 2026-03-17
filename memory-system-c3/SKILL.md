---
name: memory-system-c3
description: |
  Hybrid Tiered Memory System v3 (方案C-v3) - 五层智能记忆架构
  包含智能去重、自动精炼、标签推断的完整 AI 记忆管理方案
version: 2.0.0
author: egg小姐
date: 2026-03-14
tags: [memory, management, tiered, smart-dedup, auto-compaction, workflow, automation]
---

# 方案C-v3: 智能分层记忆系统

> 🧠 五层架构 + 智能去重 + 自动精炼 + 标签推断
> 
> 解决 AI Agent 跨会话记忆丢失、文件膨胀、内容重复问题

---

## 🎯 核心特性

| 特性 | 说明 | 收益 |
|------|------|------|
| **五层架构** | L0-L4 分层存储，职责分离 | 结构化、易维护 |
| **智能去重** | 相似度>85%触发合并更新 | 减少60%冗余 |
| **自动精炼** | 时间窗口触发内容降级 | 自动归档、永不丢失 |
| **标签推断** | 基于关键词自动补全 type | 降低维护成本 |
| **优先级衰减** | low 优先级90天后自动归档 | 保持记忆新鲜 |

---

## 🏗️ 五层架构

```
workspace/
├── RECENT_EVENTS.md      ← L0: 24h滚动事件（最轻量）
├── MEMORY.md             ← L1: 长期精华记忆（标签化）⭐
└── memory/
    ├── index.md          ← L2: 活跃任务快照
    ├── 2026-03-11.md     ← L3: 详细记忆包（按日）
    └── archive/          ← L4: 历史归档（压缩）
```

### 各层职责

| 层级 | 文件 | 用途 | 保留时间 | 读取频率 |
|------|------|------|----------|----------|
| **L0** | `RECENT_EVENTS.md` | 24h滚动事件 | 7天 | 每次会话 |
| **L1** | `MEMORY.md` | 长期精华记忆 | 90天(low) | 每次会话 |
| **L2** | `memory/index.md` | 活跃任务索引 | 持续 | 每次会话 |
| **L3** | `memory/YYYYMMDD.md` | 详细日志 | 30天 | 按需 |
| **L4** | `memory/archive/` | 历史归档 | 永久 | 几乎不读 |

---

## 🏷️ 标签系统

### Type 标签

| 标签 | 含义 | 关键词模式 |
|------|------|------------|
| `preference` | 用户偏好 | 偏好/喜欢/习惯/风格 |
| `fact` | 客观事实 | 数据/统计/记录 |
| `task_state` | 任务状态 | 任务/项目/todo/进行中 |
| `decision` | 重要决策 | 决定/选择/方案/策略 |
| `insight` | 洞察/教训 | 发现/教训/经验/洞察 |
| `workflow` | 工作流程 | 流程/步骤/规则/SOP |

### Priority 优先级

| 优先级 | 说明 | 处理策略 |
|--------|------|----------|
| `critical` | 关键，必须记住 | 永不降级 |
| `high` | 重要，优先记住 | 90天后检查 |
| `medium` | 一般重要 | 60天后考虑归档 |
| `low` | 低优先级 | 90天后自动归档到 L4 |

---

## 🆕 v2.0.0 新特性

自动化脚本套件，告别手动维护：

| 脚本 | 功能 | 使用场景 |
|------|------|----------|
| `smart-dedup.js` | 智能去重 | 检查并合并相似度>85%的重复条目 |
| `tag-infer.js` | 标签推断 | 自动为缺失 type 的条目补全标签 |
| `auto-compact.js` | 自动精炼 | 按时间窗口归档和清理记忆文件 |
| `heartbeat-check.sh` | 心跳检查 | 整合所有维护任务的一站式脚本 |

### 快速使用

```bash
# 进入 skill 目录
cd skills/memory-system-c3

# 执行完整心跳检查
bash scripts/heartbeat-check.sh

# 单独执行某功能
node scripts/smart-dedup.js
node scripts/tag-infer.js
node scripts/auto-compact.js
```

---

## 🚀 快速开始

### 第一步：创建目录结构

```bash
mkdir -p workspace/memory/archive
touch workspace/RECENT_EVENTS.md
touch workspace/MEMORY.md
touch workspace/memory/index.md
```

### 第二步：初始化 MEMORY.md (L1)

```markdown
# MEMORY.md - Long-Term Memory

> 🧠 长期精华记忆 (方案C-v3)

---

## 👤 User Profile

**Name**: 
**沟通风格**: 
**时区**: 

---

## 🎯 Key Preferences

| 偏好 | 类型 | 优先级 | 来源 | 更新策略 |
|------|------|--------|------|----------|

---

## 📊 Important Decisions

---

## 🔧 Work Patterns

### 记忆写入检查清单
- [ ] 智能去重检查 (重复则合并)
- [ ] 自动标签推断 (如缺失)
- [ ] 写入 RECENT_EVENTS.md (24h内重要事件)
- [ ] 更新当天 memory/YYYYMMDD.md (详细记录)
- [ ] 更新 memory/index.md (任务状态)
- [ ] 打标签: type + priority
- [ ] 触发自动精炼 (如满足条件)

---

## 🔗 Important Links

| 资源 | 链接 | 说明 |
|------|------|------|

---

*方案C-v3: 智能分层记忆系统*
```

### 第三步：初始化 index.md (L2)

```markdown
# Memory Index

> 📌 活跃任务快照与快速索引

---

## 🎯 Active Tasks

| Bundle ID | 任务 | 状态 | 优先级 | 日期 |
|-----------|------|------|--------|------|

---

## ✅ Completed Tasks

| Bundle ID | 任务 | 关键成果 | 优先级 | 日期 |
|-----------|------|----------|--------|------|

---

## 👤 User Preferences

| 偏好 | 类型 | 优先级 | 来源 | 更新策略 |
|------|------|--------|------|----------|

---

*方案C-v3 | 最后更新: YYYY-MM-DD*
```

### 第四步：初始化 RECENT_EVENTS.md (L0)

```markdown
# RECENT_EVENTS.md

> 📝 24小时滚动事件 (L0层)

---

## 今日重要事件 (YYYY-MM-DD)

### HH:MM - 事件标题
- **类型**: [system/task/insight]
- **优先级**: [critical/high/medium/low]
- **详情**: ...

---

## 归档记录

| 日期 | 归档文件 | 状态 |
|------|----------|------|

---

*超过24小时的事件将自动归档到 memory/YYYY-MM-DD.md*
```

---

## 🔧 核心算法

### 智能去重算法

```javascript
/**
 * 写入前检查重复
 * 相似度阈值: 85%
 * 合并策略: 保留更高优先级 + 更新时间戳 + 合并详细内容
 */
function writeWithDeduplication(entry) {
  const existing = findSimilarEntry(entry.content);
  
  if (existing && similarity(existing.content, entry.content) > 0.85) {
    // 🔥 合并更新
    existing.priority = max(existing.priority, entry.priority);
    existing.updatedAt = now();
    existing.content = mergeContent(existing.content, entry.content);
    return { action: "merged", id: existing.id };
  }
  
  // 新内容写入
  append(entry);
  return { action: "appended", id: entry.id };
}
```

### 标签自动推断

```javascript
/**
 * 基于关键词模式推断 type 标签
 */
function inferTypeTags(content) {
  const patterns = {
    preference: /偏好|喜欢|习惯|风格/,
    decision: /决定|选择|方案|策略/,
    insight: /发现|教训|经验|洞察/,
    task_state: /任务|项目|todo|进行中/,
    workflow: /流程|步骤|规则|SOP|检查清单/
  };
  
  const inferred = [];
  for (const [type, pattern] of Object.entries(patterns)) {
    if (pattern.test(content)) inferred.push(type);
  }
  
  return inferred.length > 0 ? inferred : ['fact'];
}
```

---

## 🔄 自动精炼规则

### 每日任务 (memory:maintain)

| 源 | 条件 | 动作 | 目标 |
|----|------|------|------|
| L0 | >7天 | 高价值→L3, 低价值→丢弃 | L3/memory/YYYYMMDD.md |
| L3 | 每日 | 智能去重扫描 | L3 文件 |
| 全部 | 缺失 type | 标签推断补全 | 对应文件 |

### 每月1日 (memory:compact)

| 源 | 条件 | 动作 | 目标 |
|----|------|------|------|
| L3 | >30天 | high/critical→L1, 其他→L4 | MEMORY.md / L4 |
| L1 | low >90天 | 移入 archive | L4/memory/archive/ |
| L4 | 每季度 | 压缩存储 | L4/*.zip |

### 每周日 20:00 (memory:index)

- 将已完成任务移至 "Completed"
- 更新 User Preferences 区域
- 智能去重合并重复偏好

---

## 📝 写入流程

### 标准写入流程

```
1. 智能去重检查
   └── 重复? → 合并更新 → 结束
   └── 新内容 → 继续
       
2. 自动标签推断
   └── 缺失 type? → 补全标签
   
3. 写入 RECENT_EVENTS.md (L0)
   └── 24h内重要事件
   
4. 更新当天 memory/YYYYMMDD.md (L3)
   └── 详细记录
   
5. 更新 memory/index.md (L2)
   └── 任务状态
   
6. 触发自动精炼 (如满足条件)
```

### 写入示例

```javascript
// 示例：记录一个重要决策
const entry = {
  timestamp: "2026-03-11T21:00:00Z",
  type: "decision",
  priority: "high",
  title: "选择方案C-v3作为记忆系统",
  content: "经过对比，选择方案C-v3的五层架构...",
  tags: ["memory", "architecture", "decision"]
};

// 1. 检查重复
const result = writeWithDeduplication(entry);

// 2. 写入各层
if (result.action === "appended") {
  appendToL0(entry);        // RECENT_EVENTS.md
  appendToL3(entry);        // memory/2026-03-11.md
  updateL2(entry);          // memory/index.md
  
  // 3. 如果是关键决策，同时更新 L1
  if (entry.priority === "critical" || entry.priority === "high") {
    updateL1(entry);        // MEMORY.md
  }
}
```

---

## 🎭 读取流程

### 每次会话启动时

```
读取顺序:
1. SOUL.md            → 加载人设
2. USER.md            → 加载用户信息
3. RECENT_EVENTS.md   → L0: 24h内事件
4. MEMORY.md          → L1: 长期精华
5. memory/index.md    → L2: 活跃任务
6. memory/YYYYMMDD.md → L3: 当天详情 (按需)
```

---

## ⚙️ 心跳任务配置

### HEARTBEAT.md 示例

```markdown
# HEARTBEAT.md

## ⏰ Scheduled Tasks

### memory:maintain
| 属性 | 值 |
|------|-----|
| 触发条件 | 每天 08:00 |
| 动作 | 方案C-v3 智能记忆维护 |
| 子任务 | 1. 创建缺失文件<br>2. 智能去重<br>3. 标签推断<br>4. L0→L3 精炼 |

### memory:compact
| 属性 | 值 |
|------|-----|
| 触发条件 | 每月1日 08:00 |
| 动作 | L3→L1 晋升 + L1 low归档 |

## 🔕 Silence Windows
| 时间段 | 说明 |
|--------|------|
| 22:00 - 07:00 | 夜间休息，仅执行关键任务 |

## 📋 Checklist
- [ ] L0 文件检查
- [ ] 智能去重扫描
- [ ] Index 同步检查
```

---

## 🐛 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 文件膨胀 | 未执行自动精炼 | 检查 heartbeat 任务是否运行 |
| 内容重复 | 缺少去重检查 | 每次写入前调用 `writeWithDeduplication` |
| 标签混乱 | 未使用标签推断 | 启用 `inferTypeTags` 自动补全 |
| 记忆丢失 | 未正确分层 | 确保 L0→L3→L1 的晋升流程 |

---

## 📦 文件模板

### 每日记忆文件模板 (L3)

```markdown
# Memory Log - YYYY-MM-DD

> 📅 Daily Memory Log (L3层)

---

## 📝 Event Log

### HH:MM - 事件标题
- **Type**: [type]
- **Priority**: [priority]
- **Status**: [status]
- **Details**: ...

---

## ✅ Task Updates

---

## 💡 Insights & Notes

---

*方案C-v3 | Created: YYYY-MM-DD HH:MM*
```

---

## 🔗 相关资源

- **EvoMap**: 借鉴了 EvoMap 的自动精炼机制
- **方案C-v2**: 前身版本（四层层架构）
- **本仓库**: https://github.com/keepthatrunning/skill4claws

---

## 📄 许可证

MIT - 自由使用、修改、分发

---

*方案C-v3: 智能分层记忆系统 | 作者: egg小姐 | 版本: 1.0.0*
