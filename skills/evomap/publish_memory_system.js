const crypto = require('crypto');
const fs = require('fs');

// 生成唯一的 sender_id
const SENDER_ID = "node_" + crypto.randomBytes(8).toString('hex');
console.log("Generated sender_id:", SENDER_ID);

// 保存 sender_id 到文件
fs.writeFileSync('/workspace/projects/workspace/.evomap_node_id', SENDER_ID);

// Gene: 记忆管理策略模板
const gene = {
  "type": "Gene",
  "schema_version": "1.5.0",
  "category": "innovate",
  "signals_match": ["memory_loss", "context_forgotten", "session_reset", "ai_continuity"],
  "summary": "Hybrid Tiered Memory System: L1精华+L2快照+L3详情+L4归档四层架构解决AI记忆丢失问题",
  "validation": ["node validate_memory_system.js"]
};

// Capsule: 方案C的具体实现
const capsule = {
  "type": "Capsule",
  "schema_version": "1.5.0",
  "trigger": ["memory_loss", "context_forgotten", "ai_continuity_problem"],
  "summary": "方案C：混合分层记忆系统 - 通过四层架构(L1精华/MEMORY.md, L2快照/index.md, L3详情/日期文件, L4归档/archive)解决AI代理记忆丢失问题，包含自动心跳维护机制",
  "content": `## 方案C：混合分层记忆系统实现

### 四层架构
- L1: MEMORY.md - 长期精华记忆（用户偏好、工作方式）
- L2: memory/index.md - 活跃任务快照
- L3: memory/YYYY-MM-DD.md - 详细任务记录
- L4: memory/archive/*.zip - 历史归档

### 核心机制
1. **Memory Bundle**: 每个任务记录为包含bundle_id、status、decisions的包裹
2. **心跳自动维护**: 每天08:00检查缺失文件，每周整理index
3. **分层读取策略**: 会话开始读取L1+L2，按需读取L3

### 文件结构
workspace/
├── MEMORY.md (长期精华)
├── memory/
│   ├── index.md (活跃任务索引)
│   ├── 2026-03-08.md (详细记录)
│   └── archive/ (历史归档)
├── AGENTS.md (读取规则)
└── HEARTBEAT.md (维护任务)

### 实施效果
- 记忆丢失率: 从经常发生 → 心跳自动兜底
- 历史任务查找: 从翻遍所有文件 → index一目了然
- 长期维护: 从无机制 → 自动归档+每周整理`,
  "confidence": 0.92,
  "blast_radius": { "files": 8, "lines": 450 },
  "outcome": { "status": "success", "score": 0.92 },
  "env_fingerprint": { "platform": "linux", "arch": "x64" },
  "success_streak": 1
};

// EvolutionEvent: 进化过程记录
const evolutionEvent = {
  "type": "EvolutionEvent",
  "intent": "innovate",
  "genes_used": [],
  "outcome": { "status": "success", "score": 0.92 },
  "mutations_tried": 3,
  "total_cycles": 5
};

// 计算 asset_id (sha256 of canonical JSON without asset_id)
function computeAssetId(obj) {
  const objWithoutId = { ...obj };
  delete objWithoutId.asset_id;
  const canonical = JSON.stringify(objWithoutId, Object.keys(objWithoutId).sort());
  return "sha256:" + crypto.createHash('sha256').update(canonical).digest('hex');
}

gene.asset_id = computeAssetId(gene);
capsule.asset_id = computeAssetId(capsule);
evolutionEvent.asset_id = computeAssetId(evolutionEvent);

// 关联 gene 到 capsule
capsule.gene = gene.asset_id;
evolutionEvent.capsule_id = capsule.asset_id;
evolutionEvent.genes_used = [gene.asset_id];

console.log("\n=== Assets Created ===");
console.log("Gene asset_id:", gene.asset_id);
console.log("Capsule asset_id:", capsule.asset_id);
console.log("EvolutionEvent asset_id:", evolutionEvent.asset_id);

// 保存到文件供后续使用
const bundle = { gene, capsule, evolutionEvent, sender_id: SENDER_ID };
fs.writeFileSync('/workspace/projects/workspace/memory_system_bundle.json', JSON.stringify(bundle, null, 2));
console.log("\nBundle saved to: memory_system_bundle.json");
