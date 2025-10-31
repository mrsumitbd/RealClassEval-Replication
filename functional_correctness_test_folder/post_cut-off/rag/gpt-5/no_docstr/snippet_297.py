import json
import os
import webbrowser
from pathlib import Path
from typing import Any, Dict, List, Optional


class MASVisualizer:
    """Utility for visualizing Multi-Agent System interactions"""

    def __init__(self, output_dir: Optional[str] = None):
        """
        Initialize the MAS visualizer.
        Args:
            output_dir: Directory to save visualization HTML files
        """
        self.output_dir = Path(output_dir or "mas_visualizations").resolve()
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _normalize_visualization_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        nodes = data.get("nodes") or data.get(
            "agents") or data.get("vertices") or []
        links = data.get("links") or data.get(
            "edges") or data.get("connections") or []

        norm_nodes = []
        for idx, n in enumerate(nodes):
            if isinstance(n, dict):
                nid = n.get("id") or n.get(
                    "name") or n.get("label") or str(idx)
                n = {**n, "id": nid}
            else:
                n = {"id": str(n)}
            norm_nodes.append(n)

        def norm_link(l):
            if isinstance(l, dict):
                s = l.get("source") or l.get(
                    "from") or l.get("src") or l.get("u")
                t = l.get("target") or l.get(
                    "to") or l.get("dst") or l.get("v")
                out = dict(l)
                out["source"] = s
                out["target"] = t
                return out
            if isinstance(l, (list, tuple)) and len(l) >= 2:
                return {"source": l[0], "target": l[1]}
            return l

        norm_links = [norm_link(l) for l in links]
        return {"nodes": norm_nodes, "links": norm_links, "metadata": data.get("metadata", {}), "problem_id": data.get("problem_id")}

    def generate_html(self, visualization_data: Dict[str, Any], title: Optional[str] = None) -> str:
        """
        Generate HTML for visualizing agent interactions using D3.js.
        Args:
            visualization_data: Dictionary with nodes and links data
            title: Optional title for the visualization
        Returns:
            HTML string
        """
        norm = self._normalize_visualization_data(visualization_data)
        nodes = norm["nodes"]
        links = norm["links"]
        md = norm.get("metadata") or {}
        problem_id = norm.get("problem_id")

        if not title:
            title = "MAS Interaction Graph"
            if problem_id is not None:
                title += f" - Problem {problem_id}"

        data_json = json.dumps(
            {"nodes": nodes, "links": links, "metadata": md}, ensure_ascii=False)

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>{title}</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/d3/7.9.0/d3.min.js" integrity="sha512-S1Wqk1e4IdMYBPm9JYNW6KMxq8rPxmLwYJd8FJXwsgGI7mYJqd9qSCuWkYB3aHfM/1gq6eE7Tv2eS8URWJpQ/Q==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>
<style>
  :root {{
    --bg: #0b1020;
    --panel: #12193a;
    --text: #e5e7ef;
    --muted: #98a2b3;
    --link: #7aa2ff;
    --node-stroke: rgba(255,255,255,0.6);
  }}
  html, body {{
    margin: 0;
    height: 100%;
    background: var(--bg);
    color: var(--text);
    font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Cantarell, Noto Sans, Helvetica Neue, Arial, "Apple Color Emoji", "Segoe UI Emoji";
  }}
  .container {{
    display: grid;
    grid-template-rows: auto 1fr;
    height: 100%;
  }}
  header {{
    padding: 12px 16px;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    background: linear-gradient(180deg, rgba(255,255,255,0.04), rgba(255,255,255,0));
    display: flex;
    align-items: baseline;
    gap: 12px;
  }}
  h1 {{
    font-size: 16px;
    margin: 0;
  }}
  .meta {{
    color: var(--muted);
    font-size: 13px;
  }}
  #graph {{
    width: 100%;
    height: 100%;
    position: relative;
  }}
  .tooltip {{
    position: absolute;
    pointer-events: none;
    background: rgba(12, 17, 36, 0.92);
    color: var(--text);
    border: 1px solid rgba(255,255,255,0.12);
    padding: 6px 8px;
    border-radius: 6px;
    font-size: 12px;
    line-height: 1.3;
    opacity: 0;
    transform: translate(8px, 8px);
    transition: opacity 120ms ease-out;
    z-index: 10;
    white-space: pre-line;
    max-width: 300px;
  }}
  .legend {{
    position: absolute;
    right: 10px;
    bottom: 10px;
    background: rgba(12, 17, 36, 0.85);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 8px;
    padding: 8px 10px;
    font-size: 12px;
  }}
  .legend-item {{
    display: flex;
    align-items: center;
    gap: 8px;
    margin: 3px 0;
    color: var(--muted);
  }}
  .legend-swatch {{
    width: 10px;
    height: 10px;
    border-radius: 50%;
    border: 1px solid rgba(0,0,0,0.2);
    flex: 0 0 auto;
  }}
  .node-label {{
    fill: var(--text);
    font-size: 11px;
    paint-order: stroke;
    stroke: rgba(0,0,0,0.8);
    stroke-width: 2px;
    pointer-events: none;
  }}
  .link {{
    stroke: rgba(122, 162, 255, 0.5);
    stroke-width: 1.5px;
  }}
  .link:hover {{
    stroke: rgba(122, 162, 255, 0.9);
  }}
  .node {{
    stroke: var(--node-stroke);
    stroke-width: 1px;
    cursor: grab;
  }}
  .node:active {{
    cursor: grabbing;
  }}
  .controls {{
    margin-left: auto;
    display: flex;
    align-items: center;
    gap: 8px;
  }}
  .btn {{
    background: var(--panel);
    color: var(--text);
    border: 1px solid rgba(255,255,255,0.1);
    padding: 6px 10px;
    border-radius: 8px;
    font-size: 12px;
    cursor: pointer;
  }}
  .btn:hover {{
    border-color: rgba(255,255,255,0.2);
  }}
</style>
</head>
<body>
<div class="container">
  <header>
    <h1>{title}</h1>
    <div class="meta" id="meta"></div>
    <div class="controls">
      <button class="btn" id="reset">Reset View</button>
      <button class="btn" id="toggle-labels">Toggle Labels</button>
    </div>
  </header>
  <div id="graph"></div>
</div>

<script>
  const data = {data_json};

  const metaEl = document.getElementById('meta');
  metaEl.textContent = `Nodes: ${len(nodes)} • Links: ${len(links)}`;

  const container = document.getElementById('graph');
  const tooltip = document.createElement('div');
  tooltip.className = 'tooltip';
  container.appendChild(tooltip);

  function size() {{
    const r = container.getBoundingClientRect();
    return [r.width, r.height];
  }}

  let [width, height] = size();

  const svg = d3.select('#graph')
    .append('svg')
    .attr('width', width)
    .attr('height', height);

  const defs = svg.append('defs');
  defs.append('marker')
    .attr('id', 'arrow')
    .attr('viewBox', '0 0 10 10')
    .attr('refX', 14)
    .attr('refY', 5)
    .attr('markerWidth', 6)
    .attr('markerHeight', 6)
    .attr('orient', 'auto-start-reverse')
    .append('path')
    .attr('d', 'M 0 0 L 10 5 L 0 10 z')
    .attr('fill', 'rgba(122, 162, 255, 0.9)');

  const g = svg.append('g');

  const zoom = d3.zoom()
    .scaleExtent([0.1, 4])
    .on('zoom', (event) => {{
      g.attr('transform', event.transform);
    }});

  svg.call(zoom);

  document.getElementById('reset').addEventListener('click', () => {{
    svg.transition().duration(300).call(zoom.transform, d3.zoomIdentity);
  }});

  let showLabels = true;
  document.getElementById('toggle-labels').addEventListener('click', () => {{
    showLabels = !showLabels;
    nodeLabels.style('display', showLabels ? null : 'none');
  }});

  const color = d3.scaleOrdinal(d3.schemeTableau10);

  const link = g.append('g')
    .attr('stroke-linecap', 'round')
    .selectAll('line')
    .data(data.links)
    .join('line')
    .attr('class', 'link')
    .attr('marker-end', 'url(#arrow)');

  const node = g.append('g')
    .selectAll('circle')
    .data(data.nodes)
    .join('circle')
      .attr('class', 'node')
      .attr('r', d => Math.max(4, Math.min(18, d.size || d.radius || 8)))
      .attr('fill', d => color(d.group ?? d.type ?? d.role ?? 'default'))
      .on('mouseover', (event, d) => {{
        const parts = [];
        const id = d.id ?? '(unnamed)';
        parts.push(`id: ${'{'}id{'}'}`);
        const label = d.label ?? d.name;
        if (label && label !== id) parts.push(`label: ${'{'}label{'}'}`);
        if (d.group !== undefined) parts.push(`group: ${'{'}d.group{'}'}`);
        if (d.type !== undefined) parts.push(`type: ${'{'}d.type{'}'}`);
        if (d.role !== undefined) parts.push(`role: ${'{'}d.role{'}'}`);
        tooltip.textContent = parts.join('\\n');
        tooltip.style.opacity = 1;
      }})
      .on('mousemove', (event) => {{
        tooltip.style.left = (event.offsetX + 12) + 'px';
        tooltip.style.top = (event.offsetY + 12) + 'px';
      }})
      .on('mouseout', () => {{
        tooltip.style.opacity = 0;
      }})
      .call(d3.drag()
        .on('start', dragstarted)
        .on('drag', dragged)
        .on('end', dragended)
      );

  const nodeLabels = g.append('g')
    .selectAll('text')
    .data(data.nodes)
    .join('text')
      .attr('class', 'node-label')
      .attr('dy', -12)
      .attr('text-anchor', 'middle')
      .text(d => d.label ?? d.name ?? d.id);

  const simulation = d3.forceSimulation(data.nodes)
    .force('link', d3.forceLink(data.links).id(d => d.id).distance(70).strength(0.2))
    .force('charge', d3.forceManyBody().strength(-280))
    .force('collide', d3.forceCollide().radius(d => Math.max(10, d.size || d.radius || 8) + 4))
    .force('center', d3.forceCenter(width / 2, height / 2))
    .on('tick', ticked);

  function ticked() {{
    link
      .attr('x1', d => d.source.x)
      .attr('y1', d => d.source.y)
      .attr('x2', d => d.target.x)
      .attr('y2', d => d.target.y);

    node
      .attr('cx', d => d.x)
      .attr('cy', d => d.y);

    nodeLabels
      .attr('x', d => d.x)
      .attr('y', d => d.y);
  }}

  function dragstarted(event, d) {{
    if (!event.active) simulation.alphaTarget(0.3).restart();
    d.fx = d.x;
    d.fy = d.y;
  }}

  function dragged(event, d) {{
    d.fx = event.x;
    d.fy = event.y;
  }}

  function dragended(event, d) {{
    if (!event.active) simulation.alphaTarget(0);
    d.fx = null;
    d.fy = null;
  }}

  const legendGroups = Array.from(new Set(data.nodes.map(n => n.group ?? n.type ?? n.role).filter(v => v !== undefined)));
  if (legendGroups.length) {{
    const legend = d3.select('#graph').append('div').attr('class', 'legend');
    legend.append('div').style('font-weight', '600').style('margin-bottom', '6px').text('Groups');
    const items = legend.selectAll('.legend-item').data(legendGroups).join('div').attr('class', 'legend-item');
    items.append('div').attr('class', 'legend-swatch').style('background', d => color(d));
    items.append('div').text(d => d);
  }}

  const resizeObserver = new ResizeObserver(entries => {{
    for (const entry of entries) {{
      if (entry.target === container) {{
        const [w, h] = size();
        width = w; height = h;
        svg.attr('width', width).attr('height', height);
        simulation.force('center', d3.forceCenter(width / 2, height / 2)).alpha(0.1).restart();
      }}
    }}
  }});
  resizeObserver.observe(container);
</script>
</body>
</html>
"""
        return html

    def visualize(self, visualization_file: str, output_file: Optional[str] = None, open_browser: bool = True) -> str:
        """
        Generate an HTML visualization from a visualization data file and open in browser.
        Args:
            visualization_file: Path to the visualization data JSON file
            output_file: Optional path to save the HTML output
            open_browser: Whether to open the visualization in a browser (default: True)
        Returns:
            Path to the generated HTML file
        """
        vis_path = Path(visualization_file)
        if not vis_path.exists():
            raise FileNotFoundError(
                f"Visualization file not found: {visualization_file}")
        with vis_path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        title = data.get("title") or f"MAS Visualization - {vis_path.stem}"
        html = self.generate_html(data, title=title)

        if output_file:
            out_path = Path(output_file)
        else:
            out_path = self.output_dir / f"{vis_path.stem}.html"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(html, encoding="utf-8")

        if open_browser:
            webbrowser.open(out_path.as_uri())

        return str(out_path)

    def visualize_from_agent_system(self, agent_system: Any, problem_id: Optional[str] = None) -> List[str]:
        """
        Generate visualizations for all visualization files from an agent system.
        Args:
            agent_system: AgentSystem instance
            problem_id: Optional problem ID to filter by
        Returns:
            List of paths to generated HTML files
        """
        candidate_attrs = [
            "visualization_dir",
            "visualizations_dir",
            "output_dir",
            "out_dir",
            "workspace",
            "workspace_dir",
            "work_dir",
            "artifacts_dir",
            "artifacts_path",
            "log_dir",
            "logs_dir",
            "results_dir",
            "root_dir",
            "base_dir",
        ]
        roots: List[Path] = []
        for attr in candidate_attrs:
            p = getattr(agent_system, attr, None)
            if p:
                pp = Path(p)
                if pp.exists() and pp.is_dir():
                    roots.append(pp)

        if not roots:
            # Fallback: current working directory
            roots = [Path.cwd()]

        patterns = [
            "*.visualization.json",
            "*visualization*.json",
            "*.viz.json",
            "*_viz.json",
            "*_graph.json",
            "interactions.json",
            "mas_visualization.json",
        ]

        found: List[Path] = []
        seen = set()
        for root in roots:
            for pat in patterns:
                for p in root.rglob(pat):
                    if p.suffix.lower() == ".json" and p.is_file():
                        if p.resolve() not in seen:
                            seen.add(p.resolve())
                            found.append(p)

        def matches_problem(path: Path) -> bool:
            if problem_id is None:
                return True
            pid = str(problem_id)
            if pid in path.stem:
                return True
            try:
                with path.open("r", encoding="utf-8") as f:
                    d = json.load(f)
                if d.get("problem_id") is not None and str(d.get("problem_id")) == pid:
                    return True
                md = d.get("metadata") or {}
                if md.get("problem_id") is not None and str(md.get("problem_id")) == pid:
                    return True
            except Exception:
                return False
            return False

        filtered = [p for p in found if matches_problem(p)]
        outputs: List[str] = []
        for p in filtered:
            try:
                outputs.append(self.visualize(str(p), open_browser=False))
            except Exception:
                continue
        return outputs
