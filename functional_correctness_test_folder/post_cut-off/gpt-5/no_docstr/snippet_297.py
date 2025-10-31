import os
import json
import webbrowser
import tempfile
import datetime
import inspect
from pathlib import Path


class MASVisualizer:

    def __init__(self, output_dir=None):
        self.output_dir = Path(output_dir) if output_dir else Path(
            tempfile.gettempdir()) / "mas_visualizations"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _default_json(self, obj):
        try:
            if hasattr(obj, "to_dict") and callable(obj.to_dict):
                return obj.to_dict()
            if hasattr(obj, "__dict__"):
                return obj.__dict__
            return repr(obj)
        except Exception:
            return repr(obj)

    def _serialize(self, data):
        if isinstance(data, str):
            try:
                json.loads(data)
                return data
            except Exception:
                pass
        return json.dumps(data, default=self._default_json, ensure_ascii=False, indent=2)

    def _timestamped_filename(self, stem="visualization", suffix=".html"):
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        return self.output_dir / f"{stem}_{ts}{suffix}"

    def generate_html(self, visualization_data, title=None):
        title = title or "MAS Visualization"
        json_text = self._serialize(visualization_data)

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title}</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  :root {{
    --bg: #0f172a;
    --panel: #111827;
    --text: #e5e7eb;
    --muted: #9ca3af;
    --accent: #38bdf8;
    --border: #1f2937;
    --highlight: #0ea5e9;
  }}
  html, body {{
    height: 100%;
    margin: 0;
    background: var(--bg);
    color: var(--text);
    font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, "Apple Color Emoji","Segoe UI Emoji";
  }}
  .wrap {{
    display: grid;
    grid-template-rows: auto 1fr;
    height: 100%;
  }}
  header {{
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 16px 20px;
    border-bottom: 1px solid var(--border);
    background: linear-gradient(180deg, rgba(255,255,255,0.03), transparent);
  }}
  header h1 {{
    margin: 0;
    font-size: 18px;
    font-weight: 600;
    letter-spacing: .3px;
  }}
  .badge {{
    font-size: 12px;
    padding: 3px 8px;
    border: 1px solid var(--border);
    border-radius: 999px;
    color: var(--muted);
  }}
  main {{
    display: grid;
    grid-template-columns: 320px 1fr;
    height: 100%;
    min-height: 0;
  }}
  .sidebar {{
    border-right: 1px solid var(--border);
    padding: 14px;
    overflow: auto;
  }}
  .content {{
    padding: 14px;
    overflow: auto;
  }}
  .panel {{
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 12px;
    margin-bottom: 12px;
  }}
  .panel h3 {{
    margin: 0 0 6px 0;
    font-size: 13px;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: .6px;
  }}
  .btn {{
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 8px 10px;
    border: 1px solid var(--border);
    border-radius: 8px;
    color: var(--text);
    background: rgba(255,255,255,0.02);
    cursor: pointer;
    user-select: none;
  }}
  .btn:hover {{
    border-color: var(--highlight);
  }}
  .toolbar {{
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
  }}
  .search {{
    display: flex;
    gap: 8px;
    align-items: center;
    background: rgba(255,255,255,0.02);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 4px 8px;
  }}
  .search input {{
    background: transparent;
    border: none;
    color: var(--text);
    outline: none;
    width: 100%;
  }}
  pre, code {{
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
    font-size: 12px;
    line-height: 1.5;
  }}
  .json-view {{
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 12px;
  }}
  .kv {{
    display: grid;
    grid-template-columns: 120px 1fr;
    gap: 10px;
  }}
  .muted {{ color: var(--muted); }}
  .accent {{ color: var(--accent); }}
  .counter {{
    font-variant-numeric: tabular-nums;
    padding: 2px 6px;
    background: rgba(56,189,248,0.08);
    border: 1px solid rgba(56,189,248,0.25);
    border-radius: 6px;
  }}
  .split {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
  }}
  @media (max-width: 960px) {{
    main {{ grid-template-columns: 1fr; }}
    .split {{ grid-template-columns: 1fr; }}
  }}
</style>
</head>
<body>
<div class="wrap">
  <header>
    <h1>{title}</h1>
    <span class="badge">MAS Visualizer</span>
  </header>
  <main>
    <aside class="sidebar">
      <div class="panel">
        <h3>Overview</h3>
        <div class="kv">
          <div class="muted">Nodes</div>
          <div><span id="countNodes" class="counter">-</span></div>
          <div class="muted">Edges</div>
          <div><span id="countEdges" class="counter">-</span></div>
          <div class="muted">Messages</div>
          <div><span id="countMsgs" class="counter">-</span></div>
          <div class="muted">Agents</div>
          <div><span id="countAgents" class="counter">-</span></div>
        </div>
      </div>
      <div class="panel">
        <h3>Actions</h3>
        <div class="toolbar">
          <button class="btn" id="btnExpand">Expand all</button>
          <button class="btn" id="btnCollapse">Collapse all</button>
          <button class="btn" id="btnCopy">Copy JSON</button>
          <button class="btn" id="btnDownload">Download JSON</button>
        </div>
      </div>
      <div class="panel">
        <h3>Search</h3>
        <div class="search">
          <input type="text" id="searchInput" placeholder="Filter by key or value...">
        </div>
      </div>
    </aside>
    <section class="content">
      <div class="split">
        <div class="panel">
          <h3>Summary</h3>
          <div id="summary" class="muted">No summary available.</div>
        </div>
        <div class="panel">
          <h3>Schema</h3>
          <div id="schema" class="muted">No schema detected.</div>
        </div>
      </div>
      <div class="json-view" id="jsonView"></div>
    </section>
  </main>
</div>

<script>
  const rawData = {json_text};

  function computeCounts(data) {{
    const counts = {{nodes: 0, edges: 0, messages: 0, agents: 0}};
    try {{
      const walk = (obj) => {{
        if (Array.isArray(obj)) {{
          for (const item of obj) walk(item);
        }} else if (obj && typeof obj === 'object') {{
          const keys = Object.keys(obj).map(k => k.toLowerCase());
          if (keys.includes('nodes')) counts.nodes += (obj.nodes?.length || 0);
          if (keys.includes('edges')) counts.edges += (obj.edges?.length || 0);
          if (keys.includes('messages')) counts.messages += (obj.messages?.length || 0);
          if (keys.includes('agents')) counts.agents += (obj.agents?.length || 0);
          for (const k in obj) walk(obj[k]);
        }}
      }};
      walk(data);
    }} catch(e) {{}}
    return counts;
  }}

  function summarize(data) {{
    try {{
      const topKeys = Object.keys(data || {{}}).slice(0, 12);
      const parts = [];
      if (topKeys.length) parts.push('Top-level keys: ' + topKeys.map(k => '`' + k + '`').join(', '));
      const counts = computeCounts(data);
      const cparts = [];
      if (counts.agents) cparts.push(counts.agents + ' agent(s)');
      if (counts.nodes) cparts.push(counts.nodes + ' node(s)');
      if (counts.edges) cparts.push(counts.edges + ' edge(s)');
      if (counts.messages) cparts.push(counts.messages + ' message(s)');
      if (cparts.length) parts.push('Detected: ' + cparts.join(', '));
      return parts.length ? parts.join(' • ') : 'No obvious structure detected.';
    }} catch(e) {{
      return 'Unable to compute summary.';
    }}
  }}

  function schemaOf(obj, depth=0) {{
    if (depth > 4) return '...';
    if (obj === null) return 'null';
    const t = typeof obj;
    if (t !== 'object') return t;
    if (Array.isArray(obj)) {{
      if (!obj.length) return 'array';
      return 'array<' + schemaOf(obj[0], depth+1) + '>';
    }}
    const keys = Object.keys(obj).slice(0, 8);
    const parts = keys.map(k => k + ':' + schemaOf(obj[k], depth+1));
    return '{{' + parts.join(', ') + (Object.keys(obj).length > 8 ? ', ...' : '') + '}}';
  }}

  function escapeHtml(s) {{
    return String(s)
      .replaceAll('&', '&amp;')
      .replaceAll('<', '&lt;')
      .replaceAll('>', '&gt;');
  }}

  function renderJsonTree(container, data) {{
    container.innerHTML = '';
    const root = document.createElement('div');
    root.style.fontFamily = 'inherit';
    root.style.fontSize = '12px';

    const createNode = (key, value, level=0) => {{
      const node = document.createElement('div');
      node.style.marginLeft = (level ? 12 : 0) + 'px';
      node.style.borderLeft = level ? '1px dashed rgba(255,255,255,0.06)' : 'none';
      node.style.paddingLeft = level ? '8px' : '0';

      const header = document.createElement('div');
      header.style.display = 'flex';
      header.style.alignItems = 'center';
      header.style.gap = '6px';
      header.style.cursor = (typeof value === 'object' && value !== null) ? 'pointer' : 'default';
      header.style.padding = '2px 0';

      const caret = document.createElement('span');
      caret.textContent = (typeof value === 'object' && value !== null) ? '▾' : '•';
      caret.style.color = 'var(--muted)';
      caret.style.width = '12px';

      const k = document.createElement('span');
      k.innerHTML = '<span class="muted">"' + escapeHtml(key) + '"</span>:';

      const v = document.createElement('span');
      v.className = 'accent';

      const child = document.createElement('div');
      child.style.display = 'block';

      if (value === null || typeof value !== 'object') {{
        v.textContent = JSON.stringify(value);
      }} else if (Array.isArray(value)) {{
        v.textContent = 'Array(' + value.length + ')';
        for (let i=0;i<value.length;i++) {{
          child.appendChild(createNode(i, value[i], level+1));
        }}
      }} else {{
        v.textContent = 'Object';
        Object.keys(value).forEach((kk) => {{
          child.appendChild(createNode(kk, value[kk], level+1));
        }});
      }}

      header.appendChild(caret);
      header.appendChild(k);
      header.appendChild(v);
      node.appendChild(header);
      node.appendChild(child);

      if (typeof value === 'object' && value !== null) {{
        header.addEventListener('click', () => {{
          const hidden = child.style.display === 'none';
          child.style.display = hidden ? 'block' : 'none';
          caret.textContent = hidden ? '▾' : '▸';
        }});
      }}

      return node;
    }};

    if (data && typeof data === 'object') {{
      if (Array.isArray(data)) {{
        container.appendChild(createNode('root', data, 0));
      }} else {{
        Object.keys(data).forEach(k => container.appendChild(createNode(k, data[k], 0)));
      }}
    }} else {{
      container.textContent = JSON.stringify(data);
    }}
  }}

  function expandCollapseAll(container, expand=true) {{
    container.querySelectorAll('div').forEach(el => {{
      if (el.children && el.children.length >= 2) {{
        const child = el.children[1];
        if (child && child.style !== undefined) {{
          child.style.display = expand ? 'block' : 'none';
        }}
      }}
    }});
    container.querySelectorAll('span').forEach(el => {{
      if (el.textContent === '▾' || el.textContent === '▸') {{
        el.textContent = expand ? '▾' : '▸';
      }}
    }});
  }}

  function filterJson(container, data, query) {{
    if (!query) {{
      renderJsonTree(container, data);
      return;
    }}
    const q = query.toLowerCase();
    const filterObj = (obj) => {{
      if (obj === null || typeof obj !== 'object') return obj;
      if (Array.isArray(obj)) {{
        return obj.map(filterObj).filter(x => x !== undefined);
      }}
      const out = {{}};
      for (const k in obj) {{
        const v = obj[k];
        const ks = String(k).toLowerCase();
        const vs = (typeof v === 'object') ? '' : String(v).toLowerCase();
        if (ks.includes(q) || vs.includes(q)) {{
          out[k] = v;
        }} else if (typeof v === 'object' && v !== null) {{
          const nested = filterObj(v);
          if (nested && ((Array.isArray(nested) && nested.length) || (typeof nested === 'object' && Object.keys(nested).length))) {{
            out[k] = nested;
          }}
        }}
      }}
      if (!Object.keys(out).length) return undefined;
      return out;
    }};
    const filtered = filterObj(data);
    renderJsonTree(container, filtered ?? {{}});
  }}

  const container = document.getElementById('jsonView');
  const summaryEl = document.getElementById('summary');
  const schemaEl = document.getElementById('schema');
  const counts = computeCounts(rawData);
  document.getElementById('countNodes').textContent = counts.nodes;
  document.getElementById('countEdges').textContent = counts.edges;
  document.getElementById('countMsgs').textContent = counts.messages;
  document.getElementById('countAgents').textContent = counts.agents;

  summaryEl.innerHTML = summarize(rawData);
  schemaEl.innerHTML = escapeHtml(schemaOf(rawData));

  renderJsonTree(container, rawData);

  document.getElementById('btnExpand').addEventListener('click', () => expandCollapseAll(container, true));
  document.getElementById('btnCollapse').addEventListener('click', () => expandCollapseAll(container, false));
  document.getElementById('btnCopy').addEventListener('click', async () => {{
    try {{
      await navigator.clipboard.writeText(JSON.stringify(rawData, null, 2));
    }} catch(e) {{
      const ta = document.createElement('textarea');
      ta.value = JSON.stringify(rawData, null, 2);
      document.body.appendChild(ta);
      ta.select();
      document.execCommand('copy');
      document.body.removeChild(ta);
    }}
  }});
  document.getElementById('btnDownload').addEventListener('click', () => {{
    const a = document.createElement('a');
    a.href = URL.createObjectURL(new Blob([JSON.stringify(rawData, null, 2)], {{type: 'application/json'}}));
    a.download = 'visualization.json';
    a.click();
  }});
  document.getElementById('searchInput').addEventListener('input', (e) => {{
    filterJson(container, rawData, e.target.value);
  }});
</script>
</body>
</html>
"""
        return html

    def visualize(self, visualization_file, output_file=None, open_browser=True):
        if isinstance(visualization_file, (str, os.PathLike)) and os.path.exists(visualization_file):
            with open(visualization_file, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    f.seek(0)
                    txt = f.read()
                    try:
                        data = json.loads(txt)
                    except Exception:
                        data = {"raw": txt}
        else:
            data = visualization_file

        html = self.generate_html(data, title="MAS Visualization")
        out_path = Path(
            output_file) if output_file else self._timestamped_filename()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)
        if open_browser:
            webbrowser.open_new_tab(out_path.as_uri())
        return str(out_path)

    def visualize_from_agent_system(self, agent_system, problem_id=None):
        data = None

        if hasattr(agent_system, "get_visualization_data") and callable(agent_system.get_visualization_data):
            try:
                sig = inspect.signature(agent_system.get_visualization_data)
                if len(sig.parameters) >= 1 and problem_id is not None:
                    data = agent_system.get_visualization_data(problem_id)
                else:
                    data = agent_system.get_visualization_data()
            except Exception:
                pass

        if data is None and hasattr(agent_system, "visualization_data"):
            try:
                v = getattr(agent_system, "visualization_data")
                if problem_id is not None and isinstance(v, dict):
                    data = v.get(problem_id, v)
                else:
                    data = v
            except Exception:
                pass

        if data is None and hasattr(agent_system, "to_dict") and callable(agent_system.to_dict):
            try:
                v = agent_system.to_dict()
                if problem_id is not None and isinstance(v, dict):
                    data = v.get(problem_id, v)
                else:
                    data = v
            except Exception:
                pass

        if data is None and isinstance(agent_system, dict):
            data = agent_system.get(
                problem_id) if problem_id is not None else agent_system

        if data is None:
            raise ValueError(
                "Unable to extract visualization data from agent_system.")

        return self.visualize(data, open_browser=True)
