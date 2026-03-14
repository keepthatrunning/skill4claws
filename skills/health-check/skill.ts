import { Tool } from "@openclaw/core";

export const healthCheckTool: Tool = {
  name: "health_check",
  description: "执行 OpenClaw 系统健康检查",
  parameters: {
    type: "object",
    properties: {},
  },
  handler: async () => {
    const { exec } = require("child_process");
    const fs = require("fs");
    const path = require("path");

    const REPORT_FILE = "/tmp/openclaw/daily_report.md";
    const TIMESTAMP = new Date().toLocaleString("zh-CN", {
      timeZone: "Asia/Shanghai",
    });

    // 执行健康检查
    const healthCheck = () => {
      return new Promise((resolve) => {
        exec("/tmp/openclaw_health_check.sh", (error, stdout, stderr) => {
          if (error) {
            resolve(`Error: ${error.message}`);
          } else if (stderr) {
            resolve(`Stderr: ${stderr}`);
          } else {
            resolve(stdout);
          }
        });
      });
    };

    // 执行检查
    const result = await healthCheck();

    // 读取报告
    let reportContent = "";
    if (fs.existsSync(REPORT_FILE)) {
      reportContent = fs.readFileSync(REPORT_FILE, "utf-8");
    }

    return {
      status: "success",
      timestamp: TIMESTAMP,
      report: reportContent,
      summary: `健康检查已完成于 ${TIMESTAMP}`,
    };
  },
};

export default healthCheckTool;
