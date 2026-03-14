# Health Report Skill

查看 OpenClaw 系统健康检查报告和异常告警。

## 工具

- `view_health_report`: 查看健康检查报告
- `view_alerts`: 查看系统异常告警
- `run_health_check`: 立即执行系统健康检查

## 使用方法

在飞书中发送以下命令：

- "查看健康报告" - 查看完整的健康检查报告
- "查看告警" - 查看系统异常告警
- "执行健康检查" - 立即执行一次系统健康检查

## 定时检查

系统会在每天 8:00 和 20:00 自动执行健康检查，并更新报告。

## 报告位置

- 主报告：`/tmp/openclaw/reports/health_report.md`
- 告警文件：`/tmp/openclaw/reports/alerts.txt`
