#!/usr/bin/env python3
"""Generate AD WIKI dashboard.html.

Reads YAML front-matter from every wiki/**/*.md, plus inventories raw/, and
emits a self-contained HTML dashboard at AD WIKI/dashboard.html.

Usage:
    python3 code/scripts/build_dashboard.py
"""
from __future__ import annotations

import html
import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]  # AD WIKI/
WIKI = ROOT / "wiki"
RAW = ROOT / "raw"
OUTPUT = ROOT / "dashboard.html"

FM_RE = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)


def parse_front_matter(text: str) -> dict:
    m = FM_RE.match(text)
    if not m:
        return {}
    fm = {}
    for line in m.group(1).splitlines():
        if ":" not in line or line.startswith(" ") or line.startswith("-"):
            continue
        key, _, val = line.partition(":")
        fm[key.strip()] = val.strip().strip("\"'")
    return fm


def collect_pages():
    pages_by_section = {}
    for md in sorted(WIKI.rglob("*.md")):
        rel = md.relative_to(ROOT)
        parts = rel.parts
        if len(parts) < 3:
            continue
        section = parts[1]
        if section == "deliverables" and len(parts) >= 4:
            section = f"deliverables/{parts[2]}"
        text = md.read_text(encoding="utf-8")
        fm = parse_front_matter(text)
        title = fm.get("title") or md.stem.replace("_", " ")
        status = fm.get("status", "settled")
        pages_by_section.setdefault(section, []).append({
            "path": str(rel).replace("\\", "/"),
            "title": title,
            "status": status,
            "stem": md.stem,
        })
    return pages_by_section


def inventory_raw():
    if not RAW.exists():
        return {}
    inv = {}
    for sub in sorted(RAW.iterdir()):
        if not sub.is_dir():
            continue
        files = [f for f in sub.rglob("*") if f.is_file() and f.name != ".DS_Store"]
        if not files:
            continue
        inv[sub.name] = {
            "count": len(files),
            "size_human": human_size(sum(f.stat().st_size for f in files)),
        }
    return inv


def human_size(n: int) -> str:
    for unit in ["B", "KB", "MB", "GB"]:
        if n < 1024:
            return f"{n:.1f} {unit}" if unit != "B" else f"{n} {unit}"
        n /= 1024
    return f"{n:.1f} TB"


# Hardcoded narrative content — kept here so the generator is self-contained.
PROJECT_PITCH = (
    "智能手套（EDA + PPG + IMU + 麦克风）+ 多智能体系统，"
    "实时监测 AD 患者状态、判断疾病阶段（SCD→MCI→轻度→中度→重度），"
    "并配合非药物干预。"
)

CORE_ASSETS = [
    {
        "name": "专家知识库设计",
        "desc": "5 目录 / 7 段格式 / 医生可编辑的临床手册式 KB，已和临床团队对齐",
        "link": "wiki/synthesis/expert_kb_report.md",
        "tag": "已就绪",
    },
    {
        "name": "OpenNeuro 合成数据源",
        "desc": "用于 v1 合成数据校准（IMU 退化幅度、量表分布、SCD 早期建模等）",
        "link": "wiki/methods/synthetic_data_review.md",
        "tag": "待登记数据集 ID",
    },
    {
        "name": "Clinical advisor consultation",
        "desc": "26-question structured interview with senior clinician (private — see internal repo)",
        "link": "#",
        "tag": "私有",
    },
    {
        "name": "S01–S04 baseline",
        "desc": "4 健康受试者 × 12 任务，30 min 协议；S03/S04 完整，S02 部分 HR 异常",
        "link": "wiki/datasets/baseline_4.8.md",
        "tag": "已就绪",
    },
]

OPEN_QUESTIONS = [
    ("#1", "合成数据 v0 是否合理", "wiki/methods/synthetic_data_review.md", "open_question"),
    ("#2", "中文社区 BPSD 流行率与信号", "wiki/synthesis/what_we_dont_know.md", "open_question"),
    ("#3", "Agent 桩→实现的差距 (8/9 stub)", "wiki/agents/_architecture.md", "open_question"),
    ("#4", "可穿戴 × 临床数据未交叉", "wiki/synthesis/what_we_dont_know.md", "open_question"),
    ("#5", "硬件还没造出来", "wiki/synthesis/what_we_dont_know.md", "open_question"),
]

SECTION_LABELS = {
    "entities": ("实体 Entities", "谁 / 什么"),
    "concepts": ("概念 Concepts", "领域知识：分期 / BPSD / 传感器原理"),
    "methods": ("方法 Methods", "数据管道 / 预处理 / 合成数据 / 推理模式"),
    "agents": ("智能体 Agents", "7 专科 + 1 协调"),
    "synthesis": ("综合 Synthesis", "横切论述与开放问题"),
    "datasets": ("数据集 Datasets", "raw 数据的说明页"),
    "meetings": ("会议 Meetings", "按日期"),
    "deliverables/funding": ("交付：申请书 Funding", "IIT / NHS / 政府 one-pager"),
    "deliverables/ethics": ("交付：伦理 Ethics", "Imperial portal + 4 个表单"),
    "deliverables/talks": ("交付：讲稿 Talks", "2026-03-26 三个讲稿"),
}

SECTION_ORDER = list(SECTION_LABELS.keys())

STATUS_BADGE = {
    "settled": ("settled", "#16a34a"),
    "draft": ("draft", "#ca8a04"),
    "working_hypothesis": ("working hypothesis", "#ea580c"),
    "open_question": ("open question", "#dc2626"),
    "future": ("future", "#94a3b8"),
    "doc": ("doc", "#64748b"),
}


CSS = """
:root {
  --bg: #fafaf9;
  --card: #ffffff;
  --text: #1c1917;
  --muted: #57534e;
  --accent: #0f766e;
  --border: #e7e5e4;
}
* { box-sizing: border-box; }
body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Segoe UI", Helvetica, Arial, sans-serif;
  background: var(--bg);
  color: var(--text);
  line-height: 1.55;
}
.wrap { max-width: 1100px; margin: 0 auto; padding: 32px 24px 80px; }
header.hero {
  background: linear-gradient(135deg, #0f766e 0%, #115e59 100%);
  color: #f0fdfa;
  padding: 48px 24px;
  margin-bottom: 32px;
}
header.hero h1 { margin: 0 0 8px; font-size: 32px; letter-spacing: -0.02em; }
header.hero p { margin: 0; max-width: 800px; font-size: 16px; opacity: 0.9; }
header.hero .meta { font-size: 13px; opacity: 0.7; margin-top: 12px; }
h2 { font-size: 20px; margin: 40px 0 16px; letter-spacing: -0.01em; }
h2 .muted { color: var(--muted); font-weight: 400; font-size: 14px; margin-left: 8px; }
section { margin-bottom: 8px; }
.cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 16px;
}
.card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 18px;
  transition: transform 0.1s, box-shadow 0.1s;
}
.card:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.06); }
.card h3 { margin: 0 0 6px; font-size: 15px; }
.card p { margin: 0 0 12px; font-size: 13px; color: var(--muted); }
.card .tag {
  display: inline-block; font-size: 11px; padding: 2px 8px; border-radius: 999px;
  background: #f0fdfa; color: var(--accent); border: 1px solid #99f6e4;
}
.card a { color: var(--accent); text-decoration: none; font-size: 13px; font-weight: 500; }
.card a:hover { text-decoration: underline; }
.oq-list { list-style: none; padding: 0; margin: 0; }
.oq-list li {
  background: var(--card);
  border: 1px solid var(--border);
  border-left: 3px solid #dc2626;
  border-radius: 6px;
  padding: 12px 16px;
  margin-bottom: 8px;
  display: flex;
  align-items: center;
  gap: 12px;
}
.oq-list .oq-id { font-weight: 600; color: #dc2626; font-size: 13px; min-width: 28px; }
.oq-list a { color: var(--text); text-decoration: none; flex: 1; font-size: 14px; }
.oq-list a:hover { color: var(--accent); }
.section-block {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 8px;
  margin-bottom: 12px;
  overflow: hidden;
}
.section-block summary {
  padding: 12px 16px;
  cursor: pointer;
  font-weight: 600;
  font-size: 14px;
  list-style: none;
  display: flex;
  align-items: center;
  gap: 10px;
}
.section-block summary::-webkit-details-marker { display: none; }
.section-block summary::before {
  content: "▸";
  display: inline-block;
  transition: transform 0.15s;
  color: var(--muted);
}
.section-block[open] summary::before { transform: rotate(90deg); }
.section-block summary .desc {
  font-weight: 400; color: var(--muted); font-size: 12px; margin-left: auto;
}
.section-block .body { padding: 0 16px 12px; }
.page-row {
  display: flex; align-items: center; gap: 10px;
  padding: 6px 0;
  border-top: 1px solid #f5f5f4;
  font-size: 13px;
}
.page-row a { color: var(--text); text-decoration: none; flex: 1; }
.page-row a:hover { color: var(--accent); }
.page-row.future { opacity: 0.45; }
.page-row.future a { color: var(--muted); }
.page-row.future:hover { opacity: 0.8; }
.badge {
  display: inline-block;
  font-size: 10px;
  font-weight: 600;
  padding: 2px 7px;
  border-radius: 999px;
  color: white;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  white-space: nowrap;
}
.raw-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 10px;
}
.raw-cell {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 10px 14px;
}
.raw-cell .name { font-weight: 600; font-size: 13px; }
.raw-cell .stat { color: var(--muted); font-size: 12px; margin-top: 2px; }
footer {
  margin-top: 56px; padding-top: 16px; border-top: 1px solid var(--border);
  font-size: 12px; color: var(--muted); text-align: center;
}

/* === Modal / inline markdown viewer === */
#mdModal {
  position: fixed; inset: 0; background: rgba(0,0,0,0.5);
  display: none; align-items: stretch; justify-content: center;
  z-index: 1000; padding: 20px;
}
#mdModal.open { display: flex; }
#mdModal .panel {
  background: white; border-radius: 8px; width: min(900px, 100%);
  max-height: 100%; display: flex; flex-direction: column;
  box-shadow: 0 20px 60px rgba(0,0,0,0.3);
}
#mdModal header.bar {
  display: flex; align-items: center; gap: 12px;
  padding: 12px 18px; border-bottom: 1px solid var(--border);
  background: #fafaf9; border-radius: 8px 8px 0 0; margin: 0;
}
#mdModal header.bar .path { color: var(--muted); font-size: 12px; flex: 1; font-family: ui-monospace, monospace; }
#mdModal header.bar button {
  background: transparent; border: 1px solid var(--border);
  border-radius: 4px; padding: 4px 10px; cursor: pointer; font-size: 13px;
}
#mdModal header.bar button:hover { background: var(--bg); }
#mdContent {
  padding: 24px 32px; overflow-y: auto; flex: 1;
  font-size: 14px; line-height: 1.7;
}
#mdContent h1, #mdContent h2, #mdContent h3 { margin-top: 24px; }
#mdContent h1 { font-size: 22px; border-bottom: 1px solid var(--border); padding-bottom: 8px; }
#mdContent h2 { font-size: 18px; }
#mdContent h3 { font-size: 15px; }
#mdContent code { background: #f5f5f4; padding: 1px 6px; border-radius: 3px; font-size: 0.9em; }
#mdContent pre { background: #f5f5f4; padding: 12px; border-radius: 6px; overflow-x: auto; }
#mdContent pre code { background: transparent; padding: 0; }
#mdContent table { border-collapse: collapse; margin: 12px 0; }
#mdContent th, #mdContent td { border: 1px solid var(--border); padding: 6px 12px; text-align: left; }
#mdContent th { background: #fafaf9; }
#mdContent blockquote { border-left: 3px solid var(--accent); padding-left: 16px; color: var(--muted); margin: 16px 0; }
#mdContent a { color: var(--accent); }
#mdFront {
  background: #f0fdfa; border: 1px solid #99f6e4;
  border-radius: 6px; padding: 10px 14px; margin-bottom: 16px;
  font-size: 12px; color: #0f766e; font-family: ui-monospace, monospace;
  white-space: pre-wrap;
}
.notice {
  background: #fef3c7; border: 1px solid #fde68a; color: #92400e;
  padding: 10px 14px; border-radius: 6px; font-size: 13px; margin-bottom: 16px;
}
.recent-changes {
  background: var(--card); border: 1px solid var(--border);
  border-radius: 8px; overflow: hidden;
}
.commit-row {
  display: flex; align-items: baseline; gap: 12px;
  padding: 10px 16px; border-top: 1px solid #f5f5f4;
  font-size: 13px;
}
.commit-row:first-child { border-top: 0; }
.commit-row .commit-date {
  color: var(--muted); font-size: 11px; min-width: 80px;
  font-family: ui-monospace, monospace;
}
.commit-row .commit-msg { flex: 1; color: var(--text); }
.commit-row .commit-msg a { color: var(--accent); text-decoration: none; }
.commit-row .commit-msg a:hover { text-decoration: underline; }
.commit-row .commit-author { color: var(--muted); font-size: 11px; }
.commit-row .commit-bot {
  background: #fef3c7; color: #92400e; padding: 1px 6px;
  border-radius: 3px; font-size: 10px; font-weight: 600; margin-left: 6px;
}
.refresh-btn {
  background: transparent; border: 1px solid var(--border);
  border-radius: 4px; padding: 4px 10px; cursor: pointer;
  font-size: 12px; color: var(--muted); margin-left: 8px;
}
.refresh-btn:hover { background: var(--bg); color: var(--text); }
.arch {
  background: var(--card); border: 1px solid var(--border); border-radius: 8px;
  padding: 20px; overflow-x: auto;
}
.arch svg { display: block; margin: 0 auto; }
.legend { display: flex; flex-wrap: wrap; gap: 12px; font-size: 12px; color: var(--muted); margin-top: 8px; }
.legend span.swatch {
  display: inline-block; width: 12px; height: 12px; border-radius: 3px;
  margin-right: 6px; vertical-align: -2px;
}
"""


ARCH_SVG = """
<svg viewBox="0 0 880 520" width="100%" style="max-width: 880px;">
  <defs>
    <marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">
      <path d="M0,0 L10,5 L0,10 z" fill="#525252"/>
    </marker>
    <marker id="arrAccent" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">
      <path d="M0,0 L10,5 L0,10 z" fill="#0f766e"/>
    </marker>
  </defs>

  <!-- ========== 你（作者） ========== -->
  <rect x="40" y="20" width="180" height="60" rx="8" fill="#0f766e" stroke="#0f766e"/>
  <text x="130" y="48" font-size="14" font-weight="600" text-anchor="middle" fill="white">你</text>
  <text x="130" y="66" font-size="11" text-anchor="middle" fill="#ccfbf1">作者 / curator</text>

  <!-- ========== 1. 编辑 wiki ========== -->
  <rect x="280" y="20" width="240" height="60" rx="8" fill="#ecfdf5" stroke="#10b981" stroke-width="1.5"/>
  <text x="400" y="44" font-size="13" font-weight="600" text-anchor="middle" fill="#065f46">① 编辑 wiki/*.md</text>
  <text x="400" y="62" font-size="11" text-anchor="middle" fill="#064e3b">concepts / methods / agents / ...</text>
  <line x1="222" y1="50" x2="278" y2="50" stroke="#0f766e" stroke-width="2" marker-end="url(#arrAccent)"/>

  <!-- ========== 2. git push ========== -->
  <rect x="580" y="20" width="240" height="60" rx="8" fill="#fafaf9" stroke="#a8a29e" stroke-width="1.5"/>
  <text x="700" y="44" font-size="13" font-weight="600" text-anchor="middle" fill="#1c1917">② git push</text>
  <text x="700" y="62" font-size="11" text-anchor="middle" fill="#57534e">推到 GitHub main 分支</text>
  <line x1="522" y1="50" x2="578" y2="50" stroke="#525252" stroke-width="1.5" marker-end="url(#arr)"/>

  <!-- 下行箭头 push → Action -->
  <line x1="700" y1="82" x2="700" y2="118" stroke="#525252" stroke-width="1.5" marker-end="url(#arr)"/>

  <!-- ========== 3. GitHub Action ========== -->
  <rect x="500" y="120" width="320" height="80" rx="8" fill="#fef3c7" stroke="#ca8a04" stroke-width="1.5"/>
  <text x="660" y="146" font-size="13" font-weight="600" text-anchor="middle" fill="#713f12">③ GitHub Action 触发（约 10 秒）</text>
  <text x="660" y="166" font-size="11" text-anchor="middle" fill="#854d0e">.github/workflows/build.yml</text>
  <text x="660" y="184" font-size="11" text-anchor="middle" fill="#854d0e">↳ 跑 build_dashboard.py</text>

  <!-- 下行箭头 Action → dashboard -->
  <line x1="660" y1="202" x2="660" y2="238" stroke="#525252" stroke-width="1.5" marker-end="url(#arr)"/>

  <!-- ========== 4. dashboard.html 生成 ========== -->
  <rect x="500" y="240" width="320" height="80" rx="8" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.5"/>
  <text x="660" y="266" font-size="13" font-weight="600" text-anchor="middle" fill="#1e3a8a">④ 重新生成 dashboard.html</text>
  <text x="660" y="286" font-size="11" text-anchor="middle" fill="#1e40af">扫所有 wiki/*.md front-matter</text>
  <text x="660" y="304" font-size="11" text-anchor="middle" fill="#1e40af">按类别 + 状态徽章渲染</text>

  <!-- 下行箭头 dashboard → Pages -->
  <line x1="660" y1="322" x2="660" y2="358" stroke="#525252" stroke-width="1.5" marker-end="url(#arr)"/>

  <!-- ========== 5. Pages 部署 ========== -->
  <rect x="500" y="360" width="320" height="80" rx="8" fill="#f5f3ff" stroke="#8b5cf6" stroke-width="1.5"/>
  <text x="660" y="386" font-size="13" font-weight="600" text-anchor="middle" fill="#4c1d95">⑤ Pages 部署（约 30 秒）</text>
  <text x="660" y="406" font-size="11" text-anchor="middle" fill="#5b21b6">jewelina95.github.io/ad-wiki-pages</text>
  <text x="660" y="424" font-size="11" text-anchor="middle" fill="#5b21b6">.nojekyll → 原样发布所有 .md</text>

  <!-- 下行箭头 Pages → 浏览者 -->
  <line x1="660" y1="442" x2="660" y2="478" stroke="#525252" stroke-width="1.5" marker-end="url(#arr)"/>

  <!-- ========== 6. 浏览者 ========== -->
  <rect x="500" y="480" width="320" height="32" rx="8" fill="#0f766e" stroke="#0f766e"/>
  <text x="660" y="500" font-size="12" font-weight="600" text-anchor="middle" fill="white">⑥ 任何人打开 URL → 看到最新版</text>

  <!-- ========== 反向：浏览器 fetch commits ========== -->
  <path d="M 500 496 Q 350 496 350 350 Q 350 250 350 165" stroke="#0f766e" stroke-width="1.5" stroke-dasharray="4 4" fill="none" marker-end="url(#arrAccent)"/>
  <text x="220" y="320" font-size="11" fill="#0f766e">浏览器载入时</text>
  <text x="220" y="336" font-size="11" fill="#0f766e">fetch GitHub commits API</text>
  <text x="220" y="352" font-size="11" fill="#0f766e">→ 「最近修改」面板</text>

  <!-- ========== 左侧：raw 数据来源 ========== -->
  <rect x="40" y="120" width="180" height="320" rx="8" fill="#fff7ed" stroke="#fb923c" stroke-width="1.5"/>
  <text x="130" y="146" font-size="13" font-weight="600" text-anchor="middle" fill="#9a3412">raw/ — 私有素材</text>
  <text x="130" y="170" font-size="11" text-anchor="middle" fill="#7c2d12">论文 PDF</text>
  <text x="130" y="188" font-size="11" text-anchor="middle" fill="#7c2d12">采访记录</text>
  <text x="130" y="206" font-size="11" text-anchor="middle" fill="#7c2d12">临床 xlsx (脱敏)</text>
  <text x="130" y="224" font-size="11" text-anchor="middle" fill="#7c2d12">传感器 CSV</text>
  <text x="130" y="246" font-size="11" text-anchor="middle" fill="#7c2d12">━━━━━━━</text>
  <text x="130" y="270" font-size="10" text-anchor="middle" fill="#9a3412">仅在 private 仓</text>
  <text x="130" y="286" font-size="10" text-anchor="middle" fill="#9a3412">不上传公开 URL</text>

  <text x="130" y="330" font-size="13" font-weight="600" text-anchor="middle" fill="#065f46">wiki/ ← cite</text>
  <text x="130" y="354" font-size="10" text-anchor="middle" fill="#064e3b">每个 wiki 页有</text>
  <text x="130" y="370" font-size="10" text-anchor="middle" fill="#064e3b">YAML front-matter:</text>
  <text x="130" y="386" font-size="10" text-anchor="middle" fill="#064e3b">title / type / status</text>
  <text x="130" y="402" font-size="10" text-anchor="middle" fill="#064e3b">last_updated / sources</text>
  <text x="130" y="418" font-size="10" text-anchor="middle" fill="#064e3b">→ 决定 dashboard 显示</text>

  <!-- 横线 raw → wiki edit -->
  <line x1="130" y1="120" x2="130" y2="100" stroke="#a8a29e" stroke-width="1.5"/>
  <line x1="130" y1="100" x2="278" y2="50" stroke="#a8a29e" stroke-width="1.5" stroke-dasharray="3 3" marker-end="url(#arr)"/>
  <text x="160" y="95" font-size="10" fill="#78716c">ingest</text>
</svg>
"""


def render_status_badge(status: str) -> str:
    label, color = STATUS_BADGE.get(status, STATUS_BADGE["doc"])
    return f'<span class="badge" style="background:{color}">{label}</span>'


def render_pages_section(pages_by_section: dict) -> str:
    out = []
    for sec in SECTION_ORDER:
        pages = pages_by_section.get(sec, [])
        if not pages:
            continue
        label, desc = SECTION_LABELS[sec]
        out.append(f'<details class="section-block" {"open" if sec in ("synthesis","agents") else ""}>')
        out.append(f'<summary>{html.escape(label)} <span class="desc">{html.escape(desc)} · {len(pages)} 页</span></summary>')
        out.append('<div class="body">')
        for p in pages:
            row_cls = "page-row future" if p["status"] == "future" else "page-row"
            out.append(f'<div class="{row_cls}">')
            out.append(f'<a href="{html.escape(p["path"])}">{html.escape(p["title"])}</a>')
            out.append(render_status_badge(p["status"]))
            out.append('</div>')
        out.append('</div></details>')
    return "\n".join(out)


def render_assets() -> str:
    out = ['<div class="cards">']
    for a in CORE_ASSETS:
        out.append(f"""
<div class="card">
  <h3>{html.escape(a["name"])}</h3>
  <p>{html.escape(a["desc"])}</p>
  <span class="tag">{html.escape(a["tag"])}</span>
  <div style="margin-top:10px"><a href="{html.escape(a["link"])}">查看 →</a></div>
</div>""")
    out.append('</div>')
    return "\n".join(out)


def render_oqs() -> str:
    out = ['<ul class="oq-list">']
    for oid, label, link, status in OPEN_QUESTIONS:
        out.append(
            f'<li><span class="oq-id">{oid}</span>'
            f'<a href="{html.escape(link)}">{html.escape(label)}</a>'
            f'{render_status_badge(status)}</li>'
        )
    out.append('</ul>')
    return "\n".join(out)


def render_raw(inv: dict) -> str:
    out = ['<div class="raw-grid">']
    for name, data in inv.items():
        out.append(f"""
<div class="raw-cell">
  <div class="name">{html.escape(name)}</div>
  <div class="stat">{data["count"]} 个文件 · {data["size_human"]}</div>
</div>""")
    out.append('</div>')
    return "\n".join(out)


def main():
    pages_by_section = collect_pages()
    raw_inv = inventory_raw()
    total_pages = sum(len(v) for v in pages_by_section.values())

    today = date.today().isoformat()

    html_out = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AD WIKI · Dashboard</title>
<style>{CSS}</style>
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
</head>
<body>

<!-- Markdown modal -->
<div id="mdModal" onclick="if(event.target===this) closeModal()">
  <div class="panel">
    <header class="bar">
      <span class="path" id="mdPath"></span>
      <button onclick="window.open(document.getElementById('mdPath').textContent, '_blank')">在新标签打开 ↗</button>
      <button onclick="closeModal()">关闭 ✕</button>
    </header>
    <div id="mdContent"></div>
  </div>
</div>

<header class="hero">
  <div class="wrap" style="padding: 0;">
    <h1>AD WIKI</h1>
    <p>{html.escape(PROJECT_PITCH)}</p>
    <div class="meta">{total_pages} 个 wiki 页 · {len(raw_inv)} 个 raw 类别 · 构建于 {today}</div>
  </div>
</header>

<div class="wrap">

<section>
  <h2>核心资产 <span class="muted">你现在手上有的 4 样东西</span></h2>
  {render_assets()}
</section>

<section>
  <h2>最近修改 <span class="muted">从 GitHub 实时拉取（最新 10 条）</span>
    <button class="refresh-btn" onclick="loadRecentChanges()">刷新 ↻</button>
  </h2>
  <div id="recentChanges" class="recent-changes">
    <div style="padding:14px;color:var(--muted);font-size:13px">载入中…</div>
  </div>
</section>

<section>
  <h2>工作原理 <span class="muted">这个 wiki 是怎么运转的</span></h2>
  <div class="arch">
    {ARCH_SVG}
    <div class="legend">
      <span><span class="swatch" style="background:#10b981"></span>编辑 / wiki 策展</span>
      <span><span class="swatch" style="background:#fef3c7"></span>GitHub Action</span>
      <span><span class="swatch" style="background:#3b82f6"></span>dashboard 构建</span>
      <span><span class="swatch" style="background:#f5f3ff"></span>Pages 部署</span>
      <span><span class="swatch" style="background:#fff7ed"></span>raw 私有源</span>
    </div>
    <div style="font-size: 12px; color: var(--muted); margin-top: 12px; line-height: 1.6;">
      <strong>从 push 到看到结果约 1 分钟。</strong>
      工作流：你改 <code>wiki/*.md</code> → <code>git push</code> → GitHub Action（10s）扫所有 front-matter 重生成 <code>dashboard.html</code> → Pages 重新部署（30s）→ 公开 URL 立刻反映新内容。
      浏览器载入 dashboard 时反向 <code>fetch</code> GitHub commits API → 顶部「最近修改」面板始终显示最新 10 条。
    </div>
  </div>
</section>

<section>
  <h2>Wiki 页面 <span class="muted">{total_pages} 页 · 点击展开各类</span></h2>
  {render_pages_section(pages_by_section)}
</section>

<section>
  <h2>raw/ 清单 <span class="muted">不可变素材</span></h2>
  {render_raw(raw_inv)}
</section>

<section>
  <h2>开放问题 <span class="muted">不确定性 / 待解决</span></h2>
  {render_oqs()}
</section>

<section>
  <h2>治理文件 <span class="muted">顶层四个</span></h2>
  <div class="cards">
    <div class="card"><h3>README.md</h3><p>项目入口</p><a href="README.md">打开 →</a></div>
    <div class="card"><h3>index.md</h3><p>所有页面目录</p><a href="index.md">打开 →</a></div>
    <div class="card"><h3>log.md</h3><p>时间线日志</p><a href="log.md">打开 →</a></div>
    <div class="card"><h3>schema.md</h3><p>操作手册</p><a href="schema.md">打开 →</a></div>
  </div>
</section>

<footer>
  生成自 <code>code/scripts/build_dashboard.py</code> · {today}<br>
  重新生成: <code>python3 code/scripts/build_dashboard.py</code><br>
  启动浏览: <code>./view.sh</code>（自动开服务器 + 浏览器）
</footer>

</div>

<script>
const modal = document.getElementById('mdModal');
const mdPath = document.getElementById('mdPath');
const mdContent = document.getElementById('mdContent');

function closeModal() {{ modal.classList.remove('open'); }}
document.addEventListener('keydown', e => {{ if (e.key === 'Escape') closeModal(); }});

function parseFrontMatter(text) {{
  const m = text.match(/^---\\s*\\n([\\s\\S]*?)\\n---\\s*\\n?/);
  if (!m) return {{ fm: '', body: text }};
  return {{ fm: m[1], body: text.slice(m[0].length) }};
}}

async function loadMarkdown(path) {{
  modal.classList.add('open');
  mdPath.textContent = path;
  mdContent.innerHTML = '<p style="color:#999">载入中…</p>';
  try {{
    const r = await fetch(path);
    if (!r.ok) throw new Error('HTTP ' + r.status);
    const text = await r.text();
    const {{fm, body}} = parseFrontMatter(text);
    let html = '';
    if (fm) html += '<div id="mdFront">' + fm + '</div>';
    if (location.protocol === 'file:') {{
      html += '<div class="notice">⚠️ 用 file:// 协议打开，部分链接 + 图片可能 404。建议用 <code>./view.sh</code> 起本地服务。</div>';
    }}
    html += marked.parse(body);
    mdContent.innerHTML = html;
    mdContent.scrollTop = 0;
    // intercept internal .md links inside the modal
    mdContent.querySelectorAll('a[href$=".md"]').forEach(a => {{
      a.addEventListener('click', e => {{
        e.preventDefault();
        const href = a.getAttribute('href');
        const base = path.split('/').slice(0, -1).join('/');
        const resolved = new URL(href, location.origin + '/' + (base ? base + '/' : '')).pathname.replace(/^\\//, '');
        loadMarkdown(resolved);
      }});
    }});
  }} catch (err) {{
    mdContent.innerHTML = '<div class="notice">无法载入 <code>' + path + '</code>: ' + err.message +
      '。如果你直接双击打开了本文件（file://），请改用 <code>./view.sh</code>。</div>';
  }}
}}

// hook all .md links on the dashboard
document.querySelectorAll('a[href$=".md"]').forEach(a => {{
  a.addEventListener('click', e => {{
    e.preventDefault();
    loadMarkdown(a.getAttribute('href'));
  }});
}});

// === Recent changes (GitHub commits API) ===
async function loadRecentChanges() {{
  const container = document.getElementById('recentChanges');
  if (!container) return;
  container.innerHTML = '<div style="padding:14px;color:var(--muted);font-size:13px">载入中…</div>';
  try {{
    const r = await fetch('https://api.github.com/repos/Jewelina95/ad-wiki-pages/commits?per_page=10');
    if (!r.ok) throw new Error('HTTP ' + r.status);
    const commits = await r.json();
    if (!commits.length) {{
      container.innerHTML = '<div style="padding:14px;color:var(--muted);font-size:13px">暂无 commit</div>';
      return;
    }}
    const fmtDate = iso => {{
      const d = new Date(iso);
      const now = new Date();
      const diffH = (now - d) / 36e5;
      if (diffH < 1) return Math.max(1, Math.round(diffH * 60)) + ' 分钟前';
      if (diffH < 24) return Math.round(diffH) + ' 小时前';
      if (diffH < 24 * 7) return Math.round(diffH / 24) + ' 天前';
      return d.toISOString().slice(0, 10);
    }};
    container.innerHTML = commits.map(c => {{
      const msg = (c.commit.message || '').split('\\n')[0];
      const author = c.commit.author.name || '';
      const isBot = author.includes('github-actions') || author.includes('[bot]');
      const safeMsg = msg.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
      return `
        <div class="commit-row">
          <span class="commit-date">${{fmtDate(c.commit.author.date)}}</span>
          <span class="commit-msg">
            <a href="${{c.html_url}}" target="_blank" rel="noopener">${{safeMsg}}</a>
            ${{isBot ? '<span class="commit-bot">auto</span>' : ''}}
          </span>
          <span class="commit-author">${{author.replace('[bot]','')}}</span>
        </div>`;
    }}).join('');
  }} catch (err) {{
    container.innerHTML = '<div style="padding:14px;color:var(--muted);font-size:13px">' +
      '无法载入 GitHub commits: ' + err.message + '（可能 API 限流，每小时 60 次）</div>';
  }}
}}
loadRecentChanges();
</script>

</body>
</html>
"""
    OUTPUT.write_text(html_out, encoding="utf-8")
    print(f"Wrote {OUTPUT}  ({total_pages} wiki pages, {len(raw_inv)} raw categories)")


if __name__ == "__main__":
    main()
