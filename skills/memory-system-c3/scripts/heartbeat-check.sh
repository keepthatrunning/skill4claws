#!/bin/bash
#
# 心跳检查脚本 - 方案C-v3
# 整合所有维护任务
#

echo "🧹 方案C-v3 心跳检查 - $(date)"
echo "=========================================="

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 1. 智能去重
echo ""
echo "1️⃣ 执行智能去重..."
node "$SCRIPT_DIR/smart-dedup.js"

# 2. 标签推断
echo ""
echo "2️⃣ 执行标签推断..."
node "$SCRIPT_DIR/tag-infer.js"

# 3. 自动精炼 (仅在每月1日执行)
DAY=$(date +%d)
if [ "$DAY" = "01" ]; then
  echo ""
  echo "3️⃣ 执行自动精炼 (每月1日)..."
  node "$SCRIPT_DIR/auto-compact.js"
else
  echo ""
  echo "3️⃣ 跳过自动精炼 (仅在每月1日执行)"
fi

echo ""
echo "=========================================="
echo "✅ 心跳检查完成"
