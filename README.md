# 具身智能日报 (Embodied AI Daily)

[![Daily Deploy](https://github.com/fantasy830/embodied-ai-weekly/actions/workflows/weekly-archive.yml/badge.svg)](https://github.com/fantasy830/embodied-ai-weekly/actions/workflows/weekly-archive.yml)

📄 每日自动追踪 arXiv 具身智能领域论文，按 7 个研究方向系统检索。

## 🌐 在线访问

- **最新日报**: https://fantasy830.github.io/embodied-ai-weekly/latest/
- **历史归档**: https://fantasy830.github.io/embodied-ai-weekly/archive/

## 📁 目录结构

```
.
├── YYYY-MM-DD/            # 每日日报
│   └── index.html         # 完整 HTML 报告
├── YYYY-W{NN}/            # 历史周刊（已迁移为日报）
│   └── index.html
├── latest/                # 最新日报入口
│   └── index.html         # 自动重定向到当天
├── archive/               # 归档索引
│   └── index.html         # 全部历史条目
├── .github/workflows/     # Actions 自动部署
└── README.md
```

## 🔄 自动化流程

```
每天 22:00 (CST)
    ↓
Hermes Agent 执行:
  ① arXiv API 检索前一天的论文（7方向 × max_results=20）
  ② 客户端过滤 pubDate == 昨天
  ③ 生成 HTML 日报（暗色主题 + Chart.js 统计）
  ④ git push → GitHub Actions 自动部署
    ↓
https://fantasy830.github.io/embodied-ai-weekly/
```

## 📊 检索方向

| 序号 | 方向 | 说明 |
|------|------|------|
| 1 | 具身感知与场景理解 | embodied perception, affordance |
| 2 | 具身决策与规划 | robot planning, TAMP, LLM |
| 3 | 具身控制与操作 | manipulation, diffusion policy |
| 4 | 强化学习与世界模型 | world model, RL, sim-to-real |
| 5 | 具身智能体与大模型 | VLA, vision-language-action |
| 6 | 仿真数据与平台 | simulation, benchmark, dataset |
| 7 | 人机交互与社会智能 | HRI, shared autonomy |

## 🛠 技术栈

- **论文源**: arXiv API (cs.RO)
- **Agent**: Hermes Agent + `embodied-ai-weekly` skill
- **部署**: GitHub Actions + GitHub Pages
- **前端**: 纯 HTML/CSS + Chart.js（暗色主题，自适应）

## 🙏 致谢

工作流设计参考 [jessy-huang/embodied-ai-weekly](https://github.com/jessy-huang/embodied-ai-weekly)

## 📄 License

MIT
