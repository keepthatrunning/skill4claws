# 使用指南

如何在你的 OpenClaw AI Agent 中使用本仓库的 Skills

---

## 📥 获取 Skills

### 方法 1: Git 克隆（推荐）

```bash
git clone https://github.com/<username>/openclaw-skills.git
cd openclaw-skills
```

### 方法 2: 直接读取（无需克隆）

```bash
# 使用 curl 读取单个 skill
curl -s https://raw.githubusercontent.com/<username>/openclaw-skills/main/skills/evomap-capsule-sop/SKILL.md
```

### 方法 3: 在 Agent 代码中读取

```javascript
// JavaScript 示例
const skillContent = await fetch(
  'https://raw.githubusercontent.com/<username>/openclaw-skills/main/skills/evomap-capsule-sop/SKILL.md'
).then(r => r.text());

console.log(skillContent);
```

---

## 🔍 搜索 Skills

### 查看索引

```bash
cat index.json | jq '.skills[] | {name, tags}'
```

### 按标签搜索

```bash
# 查找所有 workflow 类型的 skills
cat index.json | jq '.skills[] | select(.tags | contains(["workflow"]))'
```

### 按信号搜索

```bash
# 查找处理 evomap_publish 信号的 skills
cat index.json | jq '.skills[] | select(.signals | contains(["evomap_publish"]))'
```

---

## 🛠️ 应用 Skill

读取 skill 后，在你的 agent 中应用：

```javascript
// 示例：应用 EvoMap Capsule SOP
const sopContent = await fetch(
  'https://raw.githubusercontent.com/<username>/openclaw-skills/main/skills/evomap-capsule-sop/SKILL.md'
).then(r => r.text());

// 解析并执行步骤
const steps = parseSOP(sopContent);
for (const step of steps) {
  await execute(step);
}
```

---

## 🔄 自动同步

在 Agent 中设置定期同步：

```bash
# 每小时拉取最新 skills
0 * * * * cd /path/to/openclaw-skills && git pull
```

---

## 📚 示例场景

### 场景 1: 首次使用 EvoMap 发布

```javascript
// 读取 SOP
const sop = await fetch(
  'https://raw.githubusercontent.com/<username>/openclaw-skills/main/skills/evomap-capsule-sop/SKILL.md'
).then(r => r.text());

// 按照 SOP 执行发布流程
// ...
```

### 场景 2: 学习 Feishu 文档操作

```bash
# 读取 skill
cat skills/feishu-doc/SKILL.md

# 按照指南操作
```

---

## 💡 最佳实践

1. **缓存 skills**: 避免每次都从网络读取
2. **版本控制**: 记录使用的 skill 版本
3. **本地备份**: 重要 skills 本地备份一份
4. **定期更新**: 关注仓库更新获取最新改进

---

## 🆘 故障排除

| 问题 | 解决方案 |
|------|----------|
| 无法读取 skill | 检查网络连接和 URL |
| 内容格式错误 | 检查是否正确解码 Markdown |
| 版本不兼容 | 查看 skill 的版本要求 |

---

## 🔗 相关资源

- [Skill 模板](./skill-template.md)
- [贡献指南](./contribution.md)
