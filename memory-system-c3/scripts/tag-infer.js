#!/usr/bin/env node
/**
 * 标签推断脚本 - 方案C-v3
 * 基于关键词自动补全缺失的 type 标签
 */

const fs = require('fs');
const path = require('path');

// 关键词模式
const TYPE_PATTERNS = {
  preference: /偏好|喜欢|习惯|风格|prefer|like|habit|style/i,
  decision: /决定|选择|方案|策略|decision|choose|strategy/i,
  insight: /发现|教训|经验|洞察|insight|lesson|discovery/i,
  task_state: /任务|项目|todo|进行中|task|project|in.?progress/i,
  workflow: /流程|步骤|规则|SOP|检查清单|workflow|process|checklist/i,
  fact: /数据|统计|记录|fact|data|statistic/i
};

// 推断类型
function inferType(content) {
  const types = [];
  
  for (const [type, pattern] of Object.entries(TYPE_PATTERNS)) {
    if (pattern.test(content)) {
      types.push(type);
    }
  }
  
  return types.length > 0 ? types : ['fact'];
}

// 处理文件
function processFile(filePath) {
  console.log(`🏷️ 处理: ${filePath}`);
  
  if (!fs.existsSync(filePath)) {
    console.log('  ⚠️ 文件不存在');
    return 0;
  }
  
  let content = fs.readFileSync(filePath, 'utf-8');
  let updatedCount = 0;
  
  // 查找缺失 type 的条目
  const entryPattern = /(### .+?\n)(- \*\*类型\*\*: )?([^\n]*)/g;
  
  content = content.replace(entryPattern, (match, header, typePrefix, existingType) => {
    if (!typePrefix || !existingType.trim()) {
      const inferredTypes = inferType(match);
      updatedCount++;
      console.log(`  ✨ 推断类型: ${inferredTypes.join(', ')}`);
      return `${header}- **类型**: ${inferredTypes.join(', ')}\n`;
    }
    return match;
  });
  
  fs.writeFileSync(filePath, content);
  console.log(`  ✅ 更新 ${updatedCount} 个条目`);
  
  return updatedCount;
}

// 主函数
function main() {
  const memoryDir = path.join(process.cwd(), '..', '..');
  const files = [
    path.join(memoryDir, 'RECENT_EVENTS.md'),
    path.join(memoryDir, 'MEMORY.md'),
    path.join(memoryDir, 'memory', 'index.md')
  ];
  
  console.log('🏷️ 方案C-v3 标签推断\n');
  
  let totalUpdated = 0;
  for (const file of files) {
    totalUpdated += processFile(file);
  }
  
  console.log(`\n📊 总计: 更新 ${totalUpdated} 个条目`);
}

if (require.main === module) {
  main();
}

module.exports = { inferType, processFile };
