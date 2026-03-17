# 团队规范强制执行指南

## 为什么需要强制执行?

个人项目靠自觉，团队项目靠规范。强制执行确保：
- 代码与文档始终同步
- 提交历史清晰可读
- 新成员快速上手

## 方法1: PR模板

创建 `.github/pull_request_template.md`:

```markdown
## 描述
<!-- 描述变更内容 -->

## 类型
- [ ] Bug修复
- [ ] 新功能
- [ ] 文档更新
- [ ] 重构

## 检查清单
- [ ] 代码通过所有测试
- [ ] README已同步更新 (如需要)
- [ ] CHANGELOG已更新
- [ ] 版本号已更新 (如为功能性变更)

## 相关Issue
Fixes #(issue编号)
```

## 方法2: CI/CD检查

创建 `.github/workflows/checks.yml`:

```yaml
name: Checks

on: [pull_request]

jobs:
  docs-sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Check documentation sync
        run: python scripts/check-sync.py --strict
        
      - name: Verify README updated
        run: |
          if git diff --name-only origin/main | grep -q "^src/"; then
            if ! git diff --name-only origin/main | grep -q "README.md"; then
              echo "⚠️ 代码变更但未更新README"
              exit 1
            fi
          fi
```

## 方法3: Git Hooks

创建 `.git/hooks/pre-commit`:

```bash
#!/bin/bash
# 提交前检查

# 检查README是否随代码一起更新
if git diff --cached --name-only | grep -qE "\.(py|js|ts)$"; then
    if ! git diff --cached --name-only | grep -q "README.md"; then
        echo "⚠️  警告: 检测到代码变更但未更新README.md"
        echo "    请确认是否需要同步更新文档"
        echo ""
        read -p "仍要提交? [y/N] " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
fi

exit 0
```

记得给hook添加执行权限：
```bash
chmod +x .git/hooks/pre-commit
```

## 方法4: 代码审查清单

审查者检查项：

- [ ] **功能实现** - 代码是否正确实现了功能
- [ ] **测试覆盖** - 是否有对应的测试用例
- [ ] **文档同步** - README/API文档是否已更新
- [ ] **CHANGELOG** - 是否记录了变更
- [ ] **版本号** - 如需要，版本号是否已更新
- [ ] **兼容性** - 是否引入了破坏性变更

## 方法5: 自动化机器人

使用 GitHub Actions 自动评论：

```yaml
name: PR Comment
on:
  pull_request:
    types: [opened]

jobs:
  comment:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/github-script@v6
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `## 📋 PR 检查清单\n\n请确认已完成以下事项:\n\n- [ ] README.md 已同步更新\n- [ ] CHANGELOG.md 已更新\n- [ ] 版本号已更新 (如适用)\n- [ ] 测试已通过\n`
            })
```

## 渐进式推行建议

不要一次性引入所有强制执行措施，建议按阶段推行：

**第1周**: 引入PR模板 (最轻量)
**第2-3周**: 添加警告性质的CI检查
**第4周**: 启用强制性的pre-commit hook
**第5周起**: 全面CI强制执行

给团队适应时间，同时强调规范带来的长期收益。
