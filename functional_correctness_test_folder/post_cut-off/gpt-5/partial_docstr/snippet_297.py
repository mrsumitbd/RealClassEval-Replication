import os
import json
import webbrowser
import tempfile
import datetime
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Union


class MASVisualizer:
    '''Utility for visualizing Multi-Agent System interactions'''

    def __init__(self, output_dir=None):
        self.output_dir = Path(
            output_dir) if output_dir else Path.cwd() / "mas_visualizations"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_html(self, visualization_data, title=None):
        def safe_json(data: Any) -> str:
            try:
                return json.dumps(data, ensure_ascii=False, indent=2)
            except Exception:
                return json.dumps(str(data))

        title_text = title or "MAS Visualization"
        data_json = safe_json(visualization_data)

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>{title_text}</title>
<style>
  :root {{
    --bg: #0f1117;
    --panel: #151821;
    --text: #e6e6e6;
    --muted: #a0a4af;
    --accent: #5cc8ff;
    --accent-2: #7ee787;
    --border: #2a2f3a;
    --warn: #ffcc6a;
    --error: #ff7b72;
  }}
  * {{ box-sizing: border-box; }}
  html, body {{ margin: 0; padding: 0; background: var(--bg); color: var(--text); font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Cantarell, Noto Sans, Ubuntu, Arial, "Apple Color Emoji", "Segoe UI Emoji"; }}
  header {{
    position: sticky; top: 0; z-index: 10;
    background: linear-gradient(180deg, rgba(21,24,33,0.98), rgba(21,24,33,0.92));
    border-bottom: 1px solid var(--border);
    padding: 12px 16px;
    display: flex; align-items: center; gap: 12px; flex-wrap: wrap;
  }}
  h1 {{ font-size: 18px; margin: 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
  .meta {{ color: var(--muted); font-size: 12px; }}
  .container {{ display: grid; grid-template-columns: 360px 1fr; gap: 12px; padding: 12px; }}
  .panel {{ background: var(--panel); border: 1px solid var(--border); border-radius: 10px; overflow: hidden; }}
  .panel header {{ position: initial; background: transparent; border: none; padding: 10px 12px; }}
  .panel h2 {{ font-size: 14px; margin: 0; color: var(--accent); }}
  .content {{ padding: 12px; max-height: 65vh; overflow: auto; }}
  .tree ul {{ list-style: none; padding-left: 16px; margin: 0; }}
  .tree li {{ margin: 2px 0; }}
  .key {{ color: var(--accent-2); }}
  .type {{ color: var(--muted); font-size: 11px; }}
  details > summary {{ cursor: pointer; user-select: none; }}
  code, pre {{ font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, "Liberation Mono", monospace; }}
  pre {{ background: #0a0c10; color: #d8dee9; border: 1px solid var(--border); border-radius: 8px; padding: 10px; overflow: auto; }}
  .toolbar {{ display: flex; gap: 8px; flex-wrap: wrap; align-items: center; }}
  .toolbar input, .toolbar select {{ background: #0a0c10; color: var(--text); border: 1px solid var(--border); border-radius: 6px; padding: 6px 8px; }}
  .toolbar button {{ background: #0a0c10; color: var(--text); border: 1px solid var(--border); border-radius: 6px; padding: 6px 10px; cursor: pointer; }}
  .toolbar button:hover {{ border-color: var(--accent); color: var(--accent); }}
  .msg-list {{ display: grid; gap: 8px; }}
  .msg {{ border: 1px solid var(--border); border-radius: 10px; padding: 10px; background: #0a0c10; }}
  .msg .head {{ display: flex; justify-content: space-between; gap: 8px; font-size: 12px; color: var(--muted); }}
  .msg .route {{ color: var(--accent-2); font-weight: 600; }}
  .msg .ts {{ color: var(--muted); }}
  .msg .body {{ white-space: pre-wrap; margin-top: 6px; }}
  .pill {{ display: inline-block; padding: 2px 6px; border-radius: 999px; background: #111621; border: 1px solid var(--border); font-size: 11px; color: var(--muted); }}
  .grid {{ display: grid; gap: 12px; }}
  .section-title {{ font-size: 12px; color: var(--muted); margin: 0 0 6px 0; text-transform: uppercase; letter-spacing: 0.06em; }}
  .empty {{ color: var(--muted); font-style: italic; }}
  @media (max-width: 900px) {{
    .container {{ grid-template-columns: 1fr; }}
  }}
</style>
</head>
<body>
<header>
  <h1>{title_text}</h1>
  <span class="meta" id="meta"></span>
  <div class="toolbar" style="margin-left:auto">
    <input id="search" type="search" placeholder="Search messages..." />
    <select id="agentFilter"><option value="">All agents</option></select>
    <button id="expandAll">Expand all</button>
    <button id="collapseAll">Collapse all</button>
    <button id="downloadJson">Download JSON</button>
  </div>
</header>

<div class="container">
  <div class="panel">
    <header><h2>Data Explorer</h2></header>
    <div class="content">
      <div id="dataTree" class="tree"></div>
    </div>
  </div>
  <div class="panel">
    <header><h2>Messages</h2></header>
    <div class="content grid">
      <div>
        <div class="section-title">Timeline</div>
        <div id="messages" class="msg-list"></div>
      </div>
      <div>
        <div class="section-title">Raw JSON</div>
        <pre id="raw"></pre>
      </div>
    </div>
  </div>
</div>

<script>
  const DATA = {data_json};

  function byPath(obj, path) {{
    return path.split('.').reduce((acc, k) => acc && acc[k], obj);
  }}

  function formatTS(ts) {{
    try {{
      if (ts == null) return '';
      if (typeof ts === 'number') {{
        const d = new Date(ts * (ts > 1e12 ? 1 : 1000));
        return d.toISOString();
      }}
      const d = new Date(ts);
      if (!isNaN(d.getTime())) return d.toISOString();
    }} catch (_) {{}}
    return String(ts);
  }}

  function createTree(container, data, key='root') {{
    const ul = document.createElement('ul');
    function walk(val, k) {{
      const li = document.createElement('li');
      const type = Object.prototype.toString.call(val).slice(8,-1);
      if (val && typeof val === 'object') {{
        const details = document.createElement('details');
        const summary = document.createElement('summary');
        summary.innerHTML = `<span class="key">${{k}}</span> <span class="type">(${{type}})</span>`;
        details.appendChild(summary);
        const inner = document.createElement('ul');
        if (Array.isArray(val)) {{
          val.forEach((v, i) => inner.appendChild(walk(v, i)));
        }} else {{
          Object.keys(val).sort().forEach(childKey => {{
            inner.appendChild(walk(val[childKey], childKey));
          }});
        }}
        details.appendChild(inner);
        li.appendChild(details);
      }} else {{
        li.innerHTML = `<span class="key">${{k}}</span>: <code>${{String(val)}}</code> <span class="type">(${{type}})</span>`;
      }}
      return li;
    }}
    ul.appendChild(walk(data, key));
    container.innerHTML = '';
    container.appendChild(ul);
  }}

  function uniqueAgents(messages) {{
    const set = new Set();
    messages.forEach(m => {{
      if (m.sender) set.add(m.sender);
      if (m.receiver) set.add(m.receiver);
      if (m.agent) set.add(m.agent);
    }});
    return Array.from(set).sort();
  }}

  function renderMessages(messages) {{
    const list = document.getElementById('messages');
    const q = document.getElementById('search').value.toLowerCase().trim();
    const filter = document.getElementById('agentFilter').value;

    const filtered = messages.filter(m => {{
      let ok = true;
      if (filter) {{
        ok = (m.sender === filter || m.receiver === filter || m.agent === filter);
      }}
      if (ok && q) {{
        const blob = JSON.stringify(m).toLowerCase();
        ok = blob.includes(q);
      }}
      return ok;
    }});

    list.innerHTML = '';
    if (!filtered.length) {{
      const p = document.createElement('div');
      p.className = 'empty';
      p.textContent = 'No messages to display';
      list.appendChild(p);
      return;
    }}

    filtered
      .slice()
      .sort((a,b) => {{
        const ta = a.timestamp ?? a.ts ?? a.time ?? 0;
        const tb = b.timestamp ?? b.ts ?? b.time ?? 0;
        return (new Date(ta)) - (new Date(tb));
      }})
      .forEach(m => {{
        const div = document.createElement('div');
        div.className = 'msg';

        const route = m.sender || m.agent || 'unknown';
        const dest = m.receiver ? ` → ${m.receiver}` : '';
        const label = m.type ? ` · ${m.type}` : '';
        const ts = formatTS(m.timestamp ?? m.ts ?? m.time);

        const metaPills = [];
        ['conversation_id','thread_id','round','step','phase'].forEach(k => {{
          if (m[k] !== undefined) metaPills.push(`<span class="pill">${{k}}: ${{m[k]}}<\/span>`);
        }});

        const body = (m.content !== undefined) ? m.content
                    : (m.message !== undefined) ? m.message
                    : (m.data !== undefined) ? JSON.stringify(m.data, null, 2)
                    : '';

        div.innerHTML = `
          <div class="head">
            <div class="route"><span>${{route}}</span>${{dest}}${{label}}</div>
            <div class="ts">${{ts}}</div>
          </div>
          <div class="meta" style="display:flex;gap:6px;flex-wrap:wrap;margin-top:4px;">${{metaPills.join(' ')}}</div>
          <div class="body">${{(typeof body === 'string') ? body.replace(/[&<>]/g, s => ({{'&':'&amp;','<':'&lt;','>':'&gt;'}}[s])) : '<pre>'+JSON.stringify(body,null,2)+'</pre>'}}</div>
        `;
        list.appendChild(div);
      }});
  }}

  function download(filename, text) {{
    const a = document.createElement('a');
    a.setAttribute('href', 'data:application/json;charset=utf-8,' + encodeURIComponent(text));
    a.setAttribute('download', filename);
    a.style.display = 'none';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  }}

  function init() {{
    const meta = document.getElementById('meta');
    const raw = document.getElementById('raw');
    const dataTree = document.getElementById('dataTree');

    const messages = (Array.isArray(DATA) ? DATA : (DATA.messages || DATA.interactions || DATA.events || [])) || [];
    const agents = (Array.isArray(DATA?.agents) ? DATA.agents : uniqueAgents(messages));

    meta.textContent = `Records: ${'{'}${'}'}.replace('', messages.length)  + (agents?.length ? ' · Agents: ' + agents.length : '')`;

    raw.textContent = JSON.stringify(DATA, null, 2);
    createTree(dataTree, DATA, 'data');

    const agentFilter = document.getElementById('agentFilter');
    agents.forEach(a => {{
      const opt = document.createElement('option');
      opt.value = a;
      opt.textContent = a;
      agentFilter.appendChild(opt);
    }});
    agentFilter.addEventListener('change', () => renderMessages(messages));
    document.getElementById('search').addEventListener('input', () => renderMessages(messages));
    document.getElementById('downloadJson').addEventListener('click', () => download('visualization.json', JSON.stringify(DATA, null, 2)));
    document.getElementById('expandAll').addEventListener('click', () => document.querySelectorAll('details').forEach(d => d.open = true));
    document.getElementById('collapseAll').addEventListener('click', () => document.querySelectorAll('details').forEach(d => d.open = false));

    renderMessages(messages);
  }}

  document.addEventListener('DOMContentLoaded', init);
</script>

</body>
</html>"""
        return html

    def visualize(self, visualization_file, output_file=None, open_browser=True):
        '''
        Generate an HTML visualization from a visualization data file and open in browser.
        Args:
            visualization_file: Path to the visualization data JSON file
            output_file: Optional path to save the HTML output
            open_browser: Whether to open the visualization in a browser (default: True)
        Returns:
            Path to the generated HTML file
        '''
        in_path = Path(visualization_file)
        if not in_path.exists() or not in_path.is_file():
            raise FileNotFoundError(f"Visualization file not found: {in_path}")

        try:
            with in_path.open('r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(
                f"Invalid JSON in visualization file {in_path}: {e}") from e

        title = f"MAS Visualization - {in_path.stem}"
        html = self.generate_html(data, title=title)

        if output_file:
            out_path = Path(output_file)
            out_path.parent.mkdir(parents=True, exist_ok=True)
        else:
            timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
            safe_stem = re.sub(r'[^a-zA-Z0-9._-]+', '_', in_path.stem)
            out_path = self.output_dir / f"{safe_stem}-{timestamp}.html"

        with out_path.open('w', encoding='utf-8') as f:
            f.write(html)

        if open_browser:
            try:
                webbrowser.open_new_tab(out_path.as_uri())
            except Exception:
                pass

        return str(out_path.resolve())

    def visualize_from_agent_system(self, agent_system, problem_id=None):
        '''
        Generate visualizations for all visualization files from an agent system.
        Args:
            agent_system: AgentSystem instance
            problem_id: Optional problem ID to filter by
        Returns:
            List of paths to generated HTML files
        '''
        files: List[Path] = []

        def filter_by_problem(paths: List[Path]) -> List[Path]:
            if problem_id is None:
                return paths
            pid = str(problem_id)
            return [p for p in paths if pid in p.name or pid in str(p.parent)]

        if hasattr(agent_system, "get_visualization_files") and callable(getattr(agent_system, "get_visualization_files")):
            try:
                result = agent_system.get_visualization_files(
                    problem_id=problem_id)  # type: ignore
                files = [Path(p) for p in (result or []) if p]
            except TypeError:
                result = agent_system.get_visualization_files()  # type: ignore
                files = [Path(p) for p in (result or []) if p]
        elif hasattr(agent_system, "visualization_files"):
            cand = getattr(agent_system, "visualization_files")
            if isinstance(cand, (list, tuple)):
                files = [Path(p) for p in cand if p]
        else:
            search_dirs: List[Path] = []
            for attr in ("output_dir", "outputs_dir", "run_dir", "runs_dir", "log_dir", "logs_dir", "work_dir", "artifact_dir"):
                if hasattr(agent_system, attr):
                    d = getattr(agent_system, attr)
                    if d:
                        search_dirs.append(Path(d))
            if not search_dirs:
                search_dirs.append(Path.cwd())

            patterns = [
                "**/*.visualization.json",
                "**/*.viz.json",
                "**/*_visualization.json",
                "**/*-visualization.json",
                "**/*visualization*.json",
                "**/*mas*viz*.json",
            ]
            found: List[Path] = []
            for d in search_dirs:
                if not d.exists():
                    continue
                for pat in patterns:
                    found.extend(d.glob(pat))
            files = list({p.resolve() for p in found})

            files = filter_by_problem(files)

        if problem_id is not None and files:
            files = [p for p in files if str(
                problem_id) in p.name or str(problem_id) in str(p.parent)]

        files = [p for p in files if p.exists() and p.suffix.lower()
                 == ".json"]

        outputs: List[str] = []
        for fp in sorted(files):
            try:
                out = self.visualize(fp, open_browser=False)
                outputs.append(out)
            except Exception:
                continue

        if outputs:
            try:
                webbrowser.open_new_tab(Path(outputs[-1]).as_uri())
            except Exception:
                pass

        return outputs
