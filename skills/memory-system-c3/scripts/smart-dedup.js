#!/usr/bin/env node
/**
 * 智能去重脚本 - 方案C-v3
 * 检查并合并重复的记忆条目
 */

const fs = require('fs');
const path = require('path');

// 相似度阈值
const SIMILARITY_THRESHOLD = 0.85;

// 计算文本相似度 (Jaccard 系数)
function calculateSimilarity(text1, text2) {
  const set1 = new Set(tokenize(text1));
  const set2 = new Set(tokenize(text2));
  
  const intersection = new Set([...set1].filter(x => set2.has(x)));
  const union = new Set([...set1, ...set2]);
  
  return intersection.size / union.size;
}

// 分词
function tokenize(text) {
  return text.toLowerCase()
    .replace(/[^\u4e00-\u9fa5a-z0-9]/g, ' ')
    .split(/\s+/)
    .filter(w => w.length > 1);
}

// 合并内容
function mergeContent(existing, newContent) {
  // 保留更详细的内容
  if (newContent.length > existing.length * 1.2) {
    return newContent + '\n\n[合并自: ' + existing.substring(0, 50) + '...]';
  }
  return existing;
}

// 检查并去重
function deduplicate(filePath) {
  console.log(`🔍 检查文件: ${filePath}`);
  
  if (!fs.existsSync(filePath)) {
    console.log(`  ⚠️ 文件不存在，跳过`);
    return { merged: 0, checked: 0 };
  }
  
  const content = fs.readFileSync(filePath, 'utf-8');
  const sections = content.split(/\n(?=#{1,3}\s)/);
  
  const entries = [];
  let mergeCount = 0;
  
  for (const section of sections) {
    if (!section.trim()) continue;
    
    // 查找相似条目
    let merged = false;
    for (const entry of entries) {
      const similarity = calculateSimilarity(entry.content, section);
      if (similarity > SIMILARITY_THRESHOLD) {
        console.log(`  🔀 发现相似条目 (相似度: ${(similarity * 100).toFixed(1)}%)`);
        // 合并更新
        entry.content = mergeContent(entry.content, section);
        entry.priority = Math.max(entry.priority || 1, extractPriority(section));
        entry.updatedAt = new Date().toISOString();
        mergeCount++;
        merged = true;
        break;
      }
    }
    
    if (!merged) {
      entries.push({
        content: section,
        priority: extractPriority(section),
        updatedAt: new Date().toISOString()
      });
    }
  }
  
  // 写回文件
  const newContent = entries.map(e => e.content).join('\n\n');
  fs.writeFileSync(filePath, newContent);
  
  console.log(`  ✅ 检查完成: ${sections.length} 个条目，合并 ${mergeCount} 个重复`);
  return { merged: mergeCount, checked: sections.length };
}

// 提取优先级
function extractPriority(content) {
  if (/priority.*critical|优先级.*critical/i.test(content)) return 3;
  if (/priority.*high|优先级.*high/i.test(content)) return 2;
  if (/priority.*medium|优先级.*medium/i.test(content)) return 1;
  return 0;
}

// 主函数
function main() {
  const memoryDir = path.join(process.cwd(), '..', '..');
  const files = [
    path.join(memoryDir, 'RECENT_EVENTS.md'),
    path.join(memoryDir, 'MEMORY.md'),
    path.join(memoryDir, 'memory', 'index.md')
  ];
  
  // 添加最近30天的 L3 文件
  const today = new Date();
  for (let i = 0; i < 30; i++) {
    const date = new Date(today);
    date.setDate(date.getDate() - i);
    const dateStr = date.toISOString().split('T')[0];
    files.push(path.join(memoryDir, 'memory', `${dateStr}.md`));
  }
  
  console.log('🧹 方案C-v3 智能去重\n');
  
  let totalMerged = 0;
  let totalChecked = 0;
  
  for (const file of files) {
    const result = deduplicate(file);
    totalMerged += result.merged;
    totalChecked += result.checked;
  }
  
  console.log(`\n📊 总计: 检查 ${totalChecked} 个条目，合并 ${totalMerged} 个重复`);
  
  if (totalMerged > 0) {
    console.log('💡 建议: 手动检查合并后的内容');
  }
}

if (require.main === module) {
  main();
}

module.exports = { deduplicate, calculateSimilarity };
