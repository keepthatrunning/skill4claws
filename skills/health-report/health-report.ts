/**
 * OpenClaw 健康报告查看技能
 * 支持通过飞书机器人查看健康检查报告和告警
 */

import { Tool } from "@openclaw/core";
import * as fs from "fs";
import * as path from "path";

const REPORT_DIR = "/tmp/openclaw/reports";
const MAIN_REPORT = path.join(REPORT_DIR, "health_report.md");
const ALERT_FILE = path.join(REPORT_DIR, "alerts.txt");

export const viewHealthReport: Tool = {
  name: "view_health_report",
  description: "查看 OpenClaw 健康检查报告",
  parameters: {
    type: "object",
    properties: {},
  },
  handler: async () => {
    try {
      if (!fs.existsSync(MAIN_REPORT)) {
        return {
          status: "not_found",
          message: "暂无健康检查报告，系统将在每天 8:00 和 20:00 自动生成报告。",
        };
      }

      // 读取报告（最多 5000 字符，避免过长）
      const reportContent = fs.readFileSync(MAIN_REPORT, "utf-8");

      // 如果报告过长，只返回最近的检查
      if (reportContent.length > 5000) {
        const lines = reportContent.split("\n");
        const recentLines = lines.slice(-100).join("\n");
        return {
          status: "success",
          message: "📊 **OpenClaw 健康检查报告（最近记录）**\n\n" + recentLines,
          fullReport: reportContent,
        };
      }

      return {
        status: "success",
        message: "📊 **OpenClaw 健康检查报告**\n\n" + reportContent,
      };
    } catch (error) {
      return {
        status: "error",
        message: `读取报告失败：${error.message}`,
      };
    }
  },
};

export const viewAlerts: Tool = {
  name: "view_alerts",
  description: "查看系统异常告警",
  parameters: {
    type: "object",
    properties: {},
  },
  handler: async () => {
    try {
      if (!fs.existsSync(ALERT_FILE)) {
        return {
          status: "no_alerts",
          message: "✅ 暂无异常告警，系统运行正常！",
        };
      }

      const alerts = fs.readFileSync(ALERT_FILE, "utf-8").trim();

      if (!alerts) {
        return {
          status: "no_alerts",
          message: "✅ 暂无异常告警，系统运行正常！",
        };
      }

      // 只显示最近的 20 条告警
      const alertLines = alerts.split("\n");
      const recentAlerts = alertLines.slice(-20).join("\n");

      return {
        status: "has_alerts",
        message: "🔔 **系统异常告警（最近20条）**\n\n" + recentAlerts,
        count: alertLines.length,
      };
    } catch (error) {
      return {
        status: "error",
        message: `读取告警失败：${error.message}`,
      };
    }
  },
};

export const runHealthCheck: Tool = {
  name: "run_health_check",
  description: "立即执行系统健康检查",
  parameters: {
    type: "object",
    properties: {},
  },
  handler: async () => {
    const { exec } = require("child_process");

    return new Promise((resolve) => {
      exec("/tmp/openclaw_health_check_v2.sh", (error, stdout, stderr) => {
        if (error) {
          resolve({
            status: "error",
            message: `执行检查失败：${error.message}`,
          });
        } else {
          const alertCount = parseInt(stdout.trim().split("\n").pop() || "0");
          const message = alertCount > 0
            ? `⚠️ 健康检查完成，检测到 ${alertCount} 个异常，请查看告警详情。`
            : `✅ 健康检查完成，系统运行正常！`;

          resolve({
            status: "success",
            message: message,
            alertCount: alertCount,
          });
        }
      });
    });
  },
};

export default {
  viewHealthReport,
  viewAlerts,
  runHealthCheck,
};
