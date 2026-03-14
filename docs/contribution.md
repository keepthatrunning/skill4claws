# 贡献指南

感谢你想为 OpenClaw Skills Hub 贡献！

---

## 📝 如何提交新 Skill

### 1. Fork 仓库

点击 GitHub 上的 "Fork" 按钮

### 2. 创建分支

```bash
git checkout -b add-skill-<skill-name>
```

### 3. 创建 Skill 文件

```bash
mkdir skills/<skill-name>
cp docs/skill-template.md skills/<skill-name>/SKILL.md
# 编辑 SKILL.md
```

### 4. 更新索引

编辑 `index.json`，添加你的 skill：

```json
{
  "id": "<skill-name>",
  "name": "<Skill 名称>",
  "description": "<描述>",
  "version": "1.0.0",
  "path": "skills/<skill-name>/SKILL.md",
  "tags": ["tag1", "tag2"],
  "author": "<你的名字>",
  "date": "<YYYY-MM-DD>",
  "signals": ["signal1", "signal2"]
}
```

### 5. 提交更改

```bash
git add .
git commit -m "Add skill: <skill-name>"
git push origin add-skill-<skill-name>
```

### 6. 创建 Pull Request

在 GitHub 上创建 PR，等待审核

---

## ✅ 审核标准

- [ ] 遵循 SKILL.md 模板格式
- [ ] 内容清晰、完整
- [ ] 包含实用示例
- [ ] 列出常见问题
- [ ] 更新 index.json

---

## 🔧 维护者指南

### 更新 Skill

```bash
# 编辑 skill
git add skills/<skill-name>/SKILL.md
# 更新版本号
# 更新 index.json
git commit -m "Update skill: <skill-name> to v1.1.0"
git push
```

### 发布新版本

```bash
# 打标签
git tag -a v1.1.0 -m "Release v1.1.0"
git push origin v1.1.0
```

---

## 📞 联系

有问题？联系维护者：egg小姐
