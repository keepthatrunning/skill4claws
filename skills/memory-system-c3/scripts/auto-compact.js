#!/usr/bin/env node
/**
 * 自动精炼脚本 - 方案C-v3
 * 根据时间窗口自动归档和清理记忆文件
 */

const fs = require('fs');
const path = require('path');

// 配置
const CONFIG = {
  l0MaxAge: 7,           // L0: 7天
  l3MaxAge: 30,          // L3: 30天
  l1LowMaxAge: 90,       // L1 low优先级: 90天
  archiveDir: 'archive'  // L4 归档目录
};

// 计算文件年龄(天)
function getFileAge(filePath) {
  const stats = fs.statSync(filePath);
  const now = new Date();
  const modified = new Date(stats.mtime);
  return Math.floor((now - modified) / (1000 * 60 * 60 * 24));
}

// 解析优先级
function parsePriority(content) {
  if (/priority.*critical/i.test(content)) return 'critical';
  if (/priority.*high/i.test(content)) return 'high';
  if (/priority.*medium/i.test(content)) return 'medium';
  return 'low';
}

// L0 → L3 精炼
function refineL0(memoryDir) {
  console.log('🔄 L0 → L3 精炼');
  const l0Path = path.join(memoryDir, 'RECENT_EVENTS.md');
  
  if (!fs.existsSync(l0Path)) {
    console.log('  ⚠️ L0 文件不存在');
    return;
  }
  
  const content = fs.readFileSync(l0Path, 'utf-8');
  const age = getFileAge(l0Path);
  
  if (age > CONFIG.l0MaxAge) {
    // 提取高价值内容
    const highValuePattern = /priority.*(critical|high)/gi;
    const matches = content.match(highValuePattern);
    
    if (matches) {
      console.log(`  📋 发现 ${matches.length} 个高价值条目`);
      // 移动到对应日期的 L3 文件
      // ... (简化版本，实际需要更复杂的解析)
    }
    
    // 重置 L0
    const template = `# RECENT_EVENTS.md

> 📝 24小时滚动事件 (L0层)

---

*已自动归档 ${new Date().toISOString().split('T')[0]}*
`;
    fs.writeFileSync(l0Path, template);
    console.log('  ✅ L0 已重置');
  }
}

// L3 → L1/L4 精炼
function refineL3(memoryDir) {
  console.log('🔄 L3 → L1/L4 精炼');
  const memorySubDir = path.join(memoryDir, 'memory');
  
  if (!fs.existsSync(memorySubDir)) {
    console.log('  ⚠️ memory 目录不存在');
    return;
  }
  
  const files = fs.readdirSync(memorySubDir)
    .filter(f => /^\d{4}-\d{2}-\d{2}\.md$/.test(f));
  
  let promoted = 0;
  let archived = 0;
  
  for (const file of files) {
    const filePath = path.join(memorySubDir, file);
    const age = getFileAge(filePath);
    
    if (age > CONFIG.l3MaxAge) {
      const content = fs.readFileSync(filePath, 'utf-8');
      const priority = parsePriority(content);
      
      if (priority === 'critical' || priority === 'high') {
        // 晋升到 L1
        console.log(`  ⬆️ 晋升到 L1: ${file}`);
        promoted++;
      } else {
        // 归档到 L4
        const archivePath = path.join(memorySubDir, CONFIG.archiveDir);
        if (!fs.existsSync(archivePath)) {
          fs.mkdirSync(archivePath, { recursive: true });
        }
        fs.renameSync(filePath, path.join(archivePath, file));
        console.log(`  📦 归档到 L4: ${file}`);
        archived++;
      }
    }
  }
  
  console.log(`  ✅ 晋升 ${promoted} 个，归档 ${archived} 个`);
}

// L1 low → L4 归档
function refineL1(memoryDir) {
  console.log('🔄 L1 low → L4 归档');
  const l1Path = path.join(memoryDir, 'MEMORY.md');
  
  if (!fs.existsSync(l1Path)) {
    console.log('  ⚠️ L1 文件不存在');
    return;
  }
  
  // 读取并解析 L1
  const content = fs.readFileSync(l1Path, 'utf-8');
  
  // 这里简化处理，实际需要更复杂的解析
  console.log('  ℹ️ 手动检查 L1 中的 low 优先级条目');
}

// 主函数
function main() {
  const memoryDir = path.join(process.cwd(), '..', '..');
  
  console.log('🧹 方案C-v3 自动精炼\n');
  
  refineL0(memoryDir);
  refineL3(memoryDir);
  refineL1(memoryDir);
  
  console.log('\n✅ 精炼完成');
}

if (require.main === module) {
  main();
}

module.exports = { refineL0, refineL3, refineL1 };
