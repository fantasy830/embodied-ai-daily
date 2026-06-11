#!/usr/bin/env python3
"""Generate daily HTML report for embodied AI papers."""
import json, sys, os
from datetime import datetime, timedelta

# Load papers from stdin or file
papers_json = sys.stdin.read()
papers = json.loads(papers_json)

date_str = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
date_display = (datetime.now() - timedelta(days=1)).strftime('%Y年%m月%d日')

# Direction metadata
dir_meta = {
    'perception':  {'name': '具身感知与场景理解', 'icon': '👁️', 'color': 'i', 'bar_class': 'bf-i'},
    'planning':    {'name': '具身决策与规划',     'icon': '🧠', 'color': 'p', 'bar_class': 'bf-p'},
    'manipulation':{'name': '具身控制与操作',     'icon': '🦾', 'color': 'n', 'bar_class': 'bf-n'},
    'rl':          {'name': '强化学习与世界模型',  'icon': '🎯', 'color': 'a', 'bar_class': 'bf-a'},
    'vla':         {'name': '具身智能体与大模型',  'icon': '🤖', 'color': 'c', 'bar_class': 'bf-c'},
    'simulation':  {'name': '仿真、数据与平台',    'icon': '🖥️', 'color': 'r', 'bar_class': 'bf-r'},
    'hri':         {'name': '人机交互与社会智能',  'icon': '🤝', 'color': 'purple', 'bar_class': 'bf-p'},
}

# Compute direction counts (each paper can be in multiple directions, count per direction)
dir_counts = {k: 0 for k in dir_meta}
for p in papers:
    for d in p['directions']:
        dir_counts[d] += 1

total_papers = len(papers)
dir_count = sum(1 for v in dir_counts.values() if v > 0)

# Group papers by direction for table display
dir_papers = {k: [] for k in dir_meta}
for p in papers:
    for d in p['directions']:
        dir_papers[d].append(p)

# Top 5 per direction for cards
max_bar = max(dir_counts.values()) if dir_counts else 1

def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')

def trunc(s, n=80):
    return s[:n] + ('...' if len(s) > n else '')

# Build bar chart items
bar_items = []
for key in ['perception', 'planning', 'manipulation', 'rl', 'vla', 'simulation', 'hri']:
    meta = dir_meta[key]
    count = dir_counts[key]
    pct = (count / max_bar * 100) if max_bar > 0 else 0
    bar_items.append(f'''<div class="bar-item">
      <span class="bar-label">{meta['icon']} {meta['name']}</span>
      <div class="bar-track"><div class="bar-fill {meta['bar_class']}" style="width:{pct}%"></div></div>
      <span class="bar-count">{count}</span>
    </div>''')

bar_html = '\n'.join(bar_items)

# Build paper cards (top 2 per direction)
paper_cards = []
for key in ['vla', 'manipulation', 'rl', 'planning', 'simulation', 'hri', 'perception']:
    meta = dir_meta[key]
    ps = dir_papers[key][:3]
    if not ps:
        continue
    paper_cards.append(f'<div class="dir-section"><div class="dir-section-title">{meta["icon"]} {meta["name"]} <span class="dir-count-badge">{len(dir_papers[key])}篇</span></div>')
    for p in ps:
        # Truncate summary
        s = p['summary'][:250]
        dirs = ', '.join([dir_meta[d]['name'] for d in p['directions']])
        paper_cards.append(f'''<div class="paper-card">
      <div class="paper-card-top bc-{meta['color']}"></div>
      <div class="paper-card-body">
        <div class="paper-num">{p['id']} · {p['cat']} · {p['published']}</div>
        <h4>{esc(p['title'])}</h4>
        <div class="paper-meta">{esc(p['authors'])}</div>
        <p class="paper-summary">{esc(s)}</p>
        <div class="paper-dirs"><span class="ptag pt-{meta['color']}">{esc(dirs)}</span></div>
        <a class="plink" href="https://arxiv.org/abs/{p['id']}" target="_blank">📄 arXiv</a>
      </div>
    </div>''')
    paper_cards.append('</div>')
paper_cards_html = '\n'.join(paper_cards)

# Build full table
table_rows = []
for i, p in enumerate(papers, 1):
    dirs = ', '.join([dir_meta[d]['name'] for d in p['directions']])
    first_dir = p['directions'][0]
    meta = dir_meta[first_dir]
    title_short = trunc(p['title'], 60)
    summary_short = trunc(p['summary'], 80)
    table_rows.append(f'''<tr>
        <td>{i}</td>
        <td class="td-title">{esc(title_short)}</td>
        <td class="td-dir hide-m"><span class="ptag pt-{meta['color']}">{esc(dirs)}</span></td>
        <td class="td-val hide-m">{esc(summary_short)}</td>
        <td class="td-link"><a href="https://arxiv.org/abs/{p['id']}" target="_blank">→ arXiv</a></td>
      </tr>''')
table_html = '\n'.join(table_rows)

html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>具身智能日报 · {date_str}</title>
  <style>
    :root {{
      --bg: #0B0E14; --bg2: #10141E; --card: #141824; --card2: #1A1F2E;
      --border: #1E2537; --border2: #252D40;
      --indigo: #6366F1; --indigo-l: #818CF8;
      --cyan: #06B6D4; --cyan-l: #67E8F9;
      --neon: #10B981; --neon-l: #6EE7B7;
      --amber: #F59E0B; --amber-l: #FCD34D;
      --rose: #F43F5E; --purple: #A855F7; --purple-l: #D8B4FE;
      --text: #E2E8F0; --text-2: #94A3B8; --text-3: #64748B;
    }}
    * {{ margin:0; padding:0; box-sizing:border-box; }}
    body {{ background:var(--bg); color:var(--text); font-family:-apple-system,'Segoe UI','PingFang SC','Hiragino Sans GB',sans-serif; line-height:1.6; }}
    a {{ color:var(--cyan-l); text-decoration:none; }}
    a:hover {{ text-decoration:underline; }}

    @keyframes pulse {{ 0%,100%{{ opacity:.6; transform:scale(1) }} 50%{{ opacity:1; transform:scale(1.05) }} }}
    @keyframes fadeUp {{ from{{ opacity:0; transform:translateY(20px) }} to{{ opacity:1; transform:translateY(0) }} }}

    .wrap {{ max-width:1100px; margin:0 auto; padding:0 20px; }}

    /* Hero */
    header {{ position:relative; overflow:hidden; padding:60px 20px 40px; text-align:center; }}
    .hero-orb {{ position:absolute; border-radius:50%; filter:blur(80px); pointer-events:none; }}
    .orb-1 {{ width:600px; height:600px; top:-200px; left:-150px; background:radial-gradient(circle,rgba(99,102,241,.18),transparent 70%); animation:pulse 8s ease-in-out infinite; }}
    .orb-2 {{ width:500px; height:500px; top:-100px; right:-100px; background:radial-gradient(circle,rgba(6,182,212,.15),transparent 70%); animation:pulse 6s ease-in-out infinite 2s; }}
    .vol-badge {{ display:inline-block; background:var(--card); border:1px solid var(--border); border-radius:20px; padding:6px 16px; font-size:13px; color:var(--text-2); margin-bottom:20px; }}
    h1 {{ font-size:2.2em; font-weight:700; background:linear-gradient(135deg,var(--cyan-l),var(--indigo-l),var(--purple-l)); -webkit-background-clip:text; -webkit-text-fill-color:transparent; margin:10px 0; }}
    .subtitle {{ color:var(--text-2); font-size:1.05em; margin:10px 0 20px; }}
    .date-row {{ display:flex; justify-content:center; gap:12px; flex-wrap:wrap; }}
    .date-chip {{ background:var(--card); border:1px solid var(--border); border-radius:20px; padding:6px 14px; font-size:13px; color:var(--text-2); }}
    .date-chip span {{ color:var(--cyan-l); }}

    /* Stats */
    .stats-grid {{ display:grid; grid-template-columns:repeat(3,1fr); gap:16px; margin:30px 0; }}
    .stat-card {{ background:var(--card); border:1px solid var(--border); border-radius:12px; padding:24px 20px; text-align:center; transition:border-color .3s; }}
    .stat-card:hover {{ border-color:var(--indigo); }}
    .stat-val {{ font-size:2.4em; font-weight:700; }}
    .stat-label {{ color:var(--text-2); font-size:14px; margin:4px 0; }}
    .stat-badge {{ display:inline-block; font-size:12px; border-radius:10px; padding:2px 10px; margin-top:6px; }}
    .sv-i {{ color:var(--indigo-l); }} .sv-n {{ color:var(--neon-l); }} .sv-c {{ color:var(--cyan-l); }}
    .sb-up {{ background:rgba(99,102,241,.15); color:var(--indigo-l); }}

    /* Chart */
    .chart-section {{ background:var(--card); border:1px solid var(--border); border-radius:12px; padding:24px; margin:30px 0; }}
    .chart-title {{ font-size:1.1em; font-weight:600; color:var(--text); margin-bottom:16px; }}
    .bar-list {{ display:flex; flex-direction:column; gap:10px; }}
    .bar-item {{ display:flex; align-items:center; gap:12px; }}
    .bar-label {{ width:160px; font-size:14px; color:var(--text-2); text-align:right; flex-shrink:0; }}
    .bar-track {{ flex:1; height:22px; background:var(--card2); border-radius:6px; overflow:hidden; }}
    .bar-fill {{ height:100%; border-radius:6px; transition:width 1s ease; }}
    .bf-i {{ background:linear-gradient(90deg,var(--indigo),var(--indigo-l)); }}
    .bf-c {{ background:linear-gradient(90deg,var(--cyan),var(--cyan-l)); }}
    .bf-n {{ background:linear-gradient(90deg,var(--neon),var(--neon-l)); }}
    .bf-a {{ background:linear-gradient(90deg,var(--amber),var(--amber-l)); }}
    .bf-r {{ background:linear-gradient(90deg,var(--rose),var(--rose)/*.7*/); }}
    .bf-p {{ background:linear-gradient(90deg,var(--purple),var(--purple-l)); }}
    .bar-count {{ width:36px; font-weight:700; color:var(--text); font-size:14px; text-align:left; }}

    /* Paper cards */
    .dir-section {{ margin:24px 0; }}
    .dir-section-title {{ font-size:1.15em; font-weight:600; color:var(--text); padding:8px 0; border-bottom:1px solid var(--border); margin-bottom:12px; }}
    .dir-count-badge {{ font-size:12px; background:var(--card2); border-radius:10px; padding:2px 10px; color:var(--text-2); }}
    .paper-card {{ background:var(--card); border:1px solid var(--border); border-radius:12px; overflow:hidden; margin-bottom:12px; animation:fadeUp .5s ease; }}
    .paper-card-top {{ height:4px; }}
    .bc-i {{ background:var(--indigo); }} .bc-c {{ background:var(--cyan); }} .bc-n {{ background:var(--neon); }}
    .bc-a {{ background:var(--amber); }} .bc-r {{ background:var(--rose); }} .bc-p {{ background:var(--purple); }}
    .bc-purple {{ background:var(--purple); }}
    .paper-card-body {{ padding:16px 20px; }}
    .paper-num {{ font-size:11px; color:var(--text-3); margin-bottom:4px; }}
    .paper-card-body h4 {{ font-size:1em; color:var(--text); margin:6px 0; line-height:1.4; }}
    .paper-meta {{ font-size:12px; color:var(--text-3); margin:4px 0; }}
    .paper-summary {{ font-size:13px; color:var(--text-2); margin:8px 0; line-height:1.5; }}
    .paper-dirs {{ margin:8px 0; }}
    .ptag {{ display:inline-block; font-size:11px; border-radius:8px; padding:2px 10px; margin:2px 4px 2px 0; }}
    .pt-i {{ background:rgba(99,102,241,.15); color:var(--indigo-l); }}
    .pt-c {{ background:rgba(6,182,212,.15); color:var(--cyan-l); }}
    .pt-n {{ background:rgba(16,185,129,.15); color:var(--neon-l); }}
    .pt-a {{ background:rgba(245,158,11,.15); color:var(--amber-l); }}
    .pt-r {{ background:rgba(244,63,94,.15); color:var(--rose); }}
    .pt-p {{ background:rgba(168,85,247,.15); color:var(--purple-l); }}
    .pt-purple {{ background:rgba(168,85,247,.15); color:var(--purple-l); }}
    .plink {{ display:inline-block; font-size:13px; color:var(--cyan-l); margin-top:6px; }}

    /* Full table */
    .table-section {{ background:var(--card); border:1px solid var(--border); border-radius:12px; overflow:hidden; margin:30px 0; }}
    .table-header {{ display:flex; align-items:center; justify-content:space-between; padding:16px 20px; border-bottom:1px solid var(--border); }}
    .table-header h3 {{ font-size:1.05em; }}
    .table-badge {{ font-size:12px; background:var(--card2); border-radius:10px; padding:4px 12px; color:var(--text-2); }}
    .table-toggle {{ font-size:13px; color:var(--cyan-l); cursor:pointer; background:none; border:none; }}
    table {{ width:100%; border-collapse:collapse; }}
    th {{ text-align:left; padding:12px 16px; font-size:12px; color:var(--text-3); text-transform:uppercase; letter-spacing:.5px; border-bottom:1px solid var(--border); }}
    td {{ padding:10px 16px; font-size:13px; border-bottom:1px solid var(--border2); }}
    tr:hover {{ background:var(--card2); }}
    .td-title {{ color:var(--text); max-width:300px; }}
    .td-dir {{ white-space:nowrap; }}
    .td-val {{ color:var(--text-2); max-width:250px; font-size:12px; }}
    .td-link a {{ color:var(--cyan-l); font-size:12px; white-space:nowrap; }}
    .table-body {{ max-height:500px; overflow-y:auto; }}
    .table-body.expanded {{ max-height:none; }}

    /* Footer */
    footer {{ text-align:center; padding:40px 20px; color:var(--text-3); font-size:13px; border-top:1px solid var(--border); margin-top:40px; }}
    footer strong {{ color:var(--text-2); }}

    @media (max-width:900px) {{ .stats-grid {{ grid-template-columns:repeat(2,1fr); }} .bar-label {{ width:100px; font-size:12px; }} }}
    @media (max-width:600px) {{ .stats-grid {{ grid-template-columns:1fr; }} .bar-label {{ width:80px; font-size:11px; }} .hide-m {{ display:none; }} h1 {{ font-size:1.5em; }} }}
  </style>
</head>
<body>
<header>
  <div class="hero-orb orb-1"></div>
  <div class="hero-orb orb-2"></div>
  <div class="vol-badge">🤖 Embodied AI Daily · {date_str}</div>
  <h1>具身智能日报</h1>
  <p class="subtitle">arXiv cs.RO 论文速览 · {date_display}</p>
  <div class="date-row">
    <div class="date-chip">📅 日期 <span>{date_str}</span></div>
    <div class="date-chip">🔬 来源 <span>arXiv cs.RO</span></div>
    <div class="date-chip">📊 覆盖 <span>{dir_count}/7 方向</span></div>
  </div>
</header>

<div class="wrap">
  <div class="stats-grid">
    <div class="stat-card">
      <div class="stat-val sv-i">{total_papers}</div>
      <div class="stat-label">arXiv 收录论文</div>
      <div class="stat-badge sb-up">{dir_count}/7 方向覆盖</div>
    </div>
    <div class="stat-card">
      <div class="stat-val sv-c">{dir_counts['vla']}</div>
      <div class="stat-label">VLA/大模型方向</div>
      <div class="stat-badge sb-up">最热方向</div>
    </div>
    <div class="stat-card">
      <div class="stat-val sv-n">{dir_counts['manipulation']}</div>
      <div class="stat-label">操控方向论文</div>
      <div class="stat-badge sb-up">论文最多</div>
    </div>
  </div>

  <div class="chart-section">
    <div class="chart-title">📊 各方向论文分布</div>
    <div class="bar-list">
      {bar_html}
    </div>
  </div>

  <div class="chart-section">
    <div class="chart-title">📄 各方向精选论文</div>
    {paper_cards_html}
  </div>

  <div class="table-section">
    <div class="table-header">
      <h3>📋 全部论文索引</h3>
      <span class="table-badge">共 {total_papers} 篇</span>
    </div>
    <div class="table-body" id="paperTable">
      <table>
        <thead>
          <tr><th>#</th><th>论文标题</th><th class="hide-m">方向</th><th class="hide-m">摘要</th><th>链接</th></tr>
        </thead>
        <tbody>{table_html}</tbody>
      </table>
    </div>
  </div>
</div>

<footer>
  <p><strong>🤖 具身智能日报</strong> · {date_str} · 数据来源：arXiv cs.RO</p>
  <p style="font-size:12px;margin-top:8px;">本报告由 AI Agent 自动生成 · 论文覆盖 {dir_count}/7 方向</p>
</footer>

<script>
document.querySelectorAll('.bar-fill').forEach(el=>{{ const w=el.style.width; el.style.width='0'; requestAnimationFrame(()=>setTimeout(()=>el.style.width=w,50)); }});
</script>
</body>
</html>'''

print(html)
