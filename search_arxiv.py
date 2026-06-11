#!/usr/bin/env python3
import urllib.request, xml.etree.ElementTree as ET, time, json, sys
from datetime import datetime, timedelta

yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
print(f'DEBUG: yesterday={yesterday}', file=sys.stderr)

directions = [
    ('perception', '具身感知', 'all:embodied+AND+all:perception+AND+cat:cs.RO'),
    ('planning', '决策规划', 'all:robot+AND+all:planning+AND+cat:cs.RO'),
    ('manipulation', '操控', 'all:robot+AND+all:manipulation+AND+cat:cs.RO'),
    ('rl', 'RL世界模型', 'all:robot+AND+all:reinforcement+AND+cat:cs.RO'),
    ('vla', 'VLA大模型', 'all:VLA+AND+cat:cs.RO'),
    ('simulation', '仿真平台', 'all:robot+AND+all:simulation+AND+cat:cs.RO'),
    ('hri', '人机交互', 'all:human-robot+AND+all:interaction+AND+cat:cs.RO'),
]

all_papers = {}

for idx, (key, name_cn, query) in enumerate(directions):
    url = f'https://export.arxiv.org/api/query?search_query={query}&sortBy=submittedDate&sortOrder=descending&max_results=20'
    print(f'[{idx+1}/7] Searching {name_cn}...', file=sys.stderr)
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'EmbodiedAI-Weekly/1.0'})
        resp = urllib.request.urlopen(req, timeout=30)
        xml_data = resp.read().decode('utf-8')
        root = ET.fromstring(xml_data)
        ns = {'atom': 'http://www.w3.org/2005/Atom', 'arxiv': 'http://arxiv.org/schemas/atom'}
        count = 0
        for entry in root.findall('atom:entry', ns):
            arxiv_id = entry.find('atom:id', ns).text.strip()
            if 'arxiv.org/abs/' in arxiv_id:
                arxiv_id = arxiv_id.split('arxiv.org/abs/')[-1]
            arxiv_id = arxiv_id.split('v')[0] if 'v' in arxiv_id else arxiv_id
            
            title = entry.find('atom:title', ns).text.strip().replace('\n', ' ')
            summary = entry.find('atom:summary', ns).text.strip().replace('\n', ' ')[:300]
            published = entry.find('atom:published', ns).text.strip()[:10]
            
            authors_el = entry.findall('atom:author', ns)
            authors = [a.find('atom:name', ns).text for a in authors_el]
            author_str = ', '.join(authors[:3]) + (' et al.' if len(authors) > 3 else '')
            
            primary_cat = entry.find('arxiv:primary_category', ns)
            cat = primary_cat.get('term') if primary_cat is not None else 'cs.RO'
            
            if published != yesterday:
                continue
            
            count += 1
            if arxiv_id not in all_papers:
                all_papers[arxiv_id] = {
                    'id': arxiv_id,
                    'title': title,
                    'summary': summary,
                    'authors': author_str,
                    'published': published,
                    'cat': cat,
                    'directions': [key]
                }
            else:
                if key not in all_papers[arxiv_id]['directions']:
                    all_papers[arxiv_id]['directions'].append(key)
        
        print(f'  -> {count} papers matched (total unique: {len(all_papers)})', file=sys.stderr)
    except Exception as e:
        print(f'  -> ERROR: {e}', file=sys.stderr)
    
    if idx < 6:
        time.sleep(5)

result = list(all_papers.values())
result.sort(key=lambda p: p['id'], reverse=True)
print(json.dumps(result, ensure_ascii=False, indent=2))
