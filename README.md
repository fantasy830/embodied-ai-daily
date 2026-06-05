# 具身智能周报 (Embodied AI Weekly)

[![Weekly Deploy](https://github.com/fantasy830/embodied-ai-weekly/actions/workflows/weekly-archive.yml/badge.svg)](https://github.com/fantasy830/embodied-ai-weekly/actions/workflows/weekly-archive.yml)

📊 每周自动追踪具身智能领域前沿动态，覆盖 arXiv 论文、GitHub 热门仓库。

## 🌐 在线访问

- **最新周报**: https://fantasy830.github.io/embodied-ai-weekly/latest/
- **历史归档**: https://fantasy830.github.io/embodied-ai-weekly/archive/

## 📁 目录结构

```
.
├── YYYY-W{NN}/            # 每周周报（独立目录）
│   └── index.html         # 完整 HTML 报告
├── latest/                # 最新周报入口
│   └── index.html         # 自动重定向到当前周
├── archive/               # 历史归档
│   └── index.html         # 归档索引页
├── .github/workflows/     # Actions 自动部署
└── README.md
```

## 🔄 自动化流程

```
每周三 22:00 (CST)
    ↓
Hermes Agent 按 embodied-ai-weekly skill 执行:
  ① 搜索 arXiv API (6方向, 过去7天论文)
  ② 搜索 GitHub API (新增 & 热门仓库)
  ③ 生成综合 HTML 报告 (暗色主题 + Chart.js 统计)
  ④ git push → GitHub Actions 自动部署
    ↓
https://fantasy830.github.io/embodied-ai-weekly/
```

## 📊 数据来源

| 来源 | 说明 |
|------|------|
| arXiv API | cs.RO/cs.CV 等分类，按 6 个研究方向检索 |
| GitHub API | 具身智能 / VLA / 机器人操控 相关仓库 |

## 🛠 技术栈

- **Agent**: Hermes Agent + `embodied-ai-weekly` skill
- **部署**: GitHub Actions + GitHub Pages
- **前端**: 纯 HTML/CSS + Chart.js（暗色主题，自适应）

## 🙏 致谢

工作流设计参考 [jessy-huang/embodied-ai-weekly](https://github.com/jessy-huang/embodied-ai-weekly)

## 📄 License

MIT
