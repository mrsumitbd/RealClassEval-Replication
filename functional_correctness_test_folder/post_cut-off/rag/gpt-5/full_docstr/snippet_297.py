import json
import os
import uuid
import webbrowser
from pathlib import Path
from datetime import datetime


class MASVisualizer:
    '''Utility for visualizing Multi-Agent System interactions'''

    def __init__(self, output_dir=None):
        '''
        Initialize the MAS visualizer.
        Args:
            output_dir: Directory to save visualization HTML files
        '''
        if output_dir is None:
            output_dir = Path.cwd() / "mas_visualizations"
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_html(self, visualization_data, title=None):
        '''
        Generate HTML for visualizing agent interactions using D3.js.
        Args:
            visualization_data: Dictionary with nodes and links data
            title: Optional title for the visualization
        Returns:
            HTML string
        '''
        if not isinstance(visualization_data, dict):
            raise TypeError(
                "visualization_data must be a dict with 'nodes' and 'links' keys.")
        nodes = visualization_data.get("nodes", [])
        links = visualization_data.get("links", [])

        # Sanity fallback
        if not isinstance(nodes, list) or not isinstance(links, list):
            raise ValueError(
                "visualization_data must contain 'nodes' and 'links' lists.")

        # Default title
        if not title:
            title = "Multi-Agent System Visualization"

        # Ensure nodes have ids
        for i, n in enumerate(nodes):
            if "id" not in n:
                n["id"] = n.get("name", n.get("label", f"node-{i}"))

        # Stringify data for embedding
        graph_json = json.dumps({"nodes": nodes, "links": links})

        # HTML with embedded D3 visualization
        html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<title>{title}</title>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<script src="https://cdn.jsdelivr.net/npm/d3@7"></script>
<style>
  html, body {{
    margin: 0;
    padding: 0;
    height: 100%;
    background: #0f172a; /* slate-900 */
    color: #e2e8f0; /* slate-200 */
    font-family: system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Cantarell, Noto Sans, Helvetica, Arial, Apple Color Emoji, Segoe UI Emoji;
  }}
  .container {{
    display: flex;
    flex-direction: column;
    height: 100%;
  }}
  header {{
    padding: 12px 16px;
    border-bottom: 1px solid #1f2937; /* gray-800 */
    background: #0b1220;
  }}
  header h1 {{
    font-size: 18px;
    margin: 0;
    font-weight: 600;
  }}
  #viz {{
    flex: 1 1 auto;
    position: relative;
  }}
  svg {{
    width: 100%;
    height: 100%;
    display: block;
    background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0));
  }}
  .link {{
    stroke: #94a3b8; /* slate-400 */
    stroke-opacity: 0.4;
  }}
  .link.weight-2 {{ stroke-width: 2; }}
  .link.weight-3 {{ stroke-width: 3; }}
  .link.weight-4 {{ stroke-width: 4; }}
  .node circle {{
    stroke: #0f172a;
    stroke-width: 1.5px;
    cursor: pointer;
  }}
  .node text {{
    font-size: 11px;
    pointer-events: none;
    fill: #cbd5e1; /* slate-300 */
    text-shadow:
      -1px -1px 0 #0f172a,
       1px -1px 0 #0f172a,
      -1px  1px 0 #0f172a,
       1px  1px 0 #0f172a;
  }}
  .tooltip {{
    position: absolute;
    pointer-events: none;
    background: rgba(15, 23, 42, 0.95);
    color: #e2e8f0;
    border: 1px solid #1f2937;
    border-radius: 6px;
    padding: 8px 10px;
    font-size: 12px;
    max-width: 320px;
    z-index: 10;
    opacity: 0;
    transition: opacity 0.12s ease-in-out;
    box-shadow: 0 6px 24px rgba(0,0,0,0.35);
  }}
  .legend {{
    position: absolute;
    right: 12px;
    top: 12px;
    background: rgba(2,6,23,0.7);
    border: 1px solid #1f2937;
    border-radius: 6px;
    padding: 8px 10px;
    backdrop-filter: blur(3px);
  }}
  .legend h3 {{
    margin: 0 0 6px 0;
    font-size: 12px;
    color: #94a3b8;
    font-weight: 600;
  }}
  .legend-item {{
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 12px;
    color: #cbd5e1;
    margin: 2px 0;
  }}
  .legend-swatch {{
    width: 12px;
    height: 12px;
    border-radius: 50%;
    border: 1px solid #0f172a;
    display: inline-block;
  }}
  .controls {{
    position: absolute;
    left: 12px;
    top: 12px;
    display: flex;
    gap: 8px;
  }}
  .btn {{
    padding: 6px 10px;
    font-size: 12px;
    border: 1px solid #1f2937;
    background: #0b1220;
    color: #cbd5e1;
    border-radius: 6px;
    cursor: pointer;
  }}
  .btn:hover {{ border-color: #475569; }}
  .watermark {{
    position: absolute;
    bottom: 8px;
    right: 12px;
    font-size: 11px;
    color: #64748b;
    user-select: none;
  }}
</style>
</head>
<body>
<div class="container">
  <header>
    <h1>{title}</h1>
  </header>
  <div id="viz">
    <div class="controls">
      <button id="resetZoom" class="btn">Reset view</button>
      <button id="toggleLabels" class="btn">Toggle labels</button>
    </div>
    <div id="legend" class="legend" style="display:none;">
      <h3>Groups</h3>
      <div id="legendItems"></div>
    </div>
    <div id="tooltip" class="tooltip"></div>
    <div class="watermark">MAS Visualizer</div>
  </div>
</div>
<script>
  const graph = {graph_json};

  // Basic normalization
  graph.nodes = (graph.nodes || []).map((n, i) => {{
    return {{
      ...n,
      id: n.id ?? n.name ?? n.label ?? `node-${{i}}`,
      label: n.label ?? n.name ?? n.id ?? `Node ${{i}}`,
      group: n.group ?? n.type ?? 'default',
      size: +n.size || 6
    }};
  }});
  graph.links = (graph.links || []).map((l, i) => {{
    return {{
      ...l,
      source: l.source,
      target: l.target,
      weight: +l.weight || 1,
      label: l.label || l.type || ''
    }};
  }});

  const container = d3.select("#viz");
  const tooltip = d3.select("#tooltip");

  const svg = container.append("svg");
  const defs = svg.append("defs");

  // Arrowhead marker
  defs.append("marker")
      .attr("id", "arrow")
      .attr("viewBox", "0 -5 10 10")
      .attr("refX", 18)
      .attr("refY", 0)
      .attr("markerWidth", 6)
      .attr("markerHeight", 6)
      .attr("orient", "auto")
    .append("path")
      .attr("d", "M0,-5L10,0L0,5")
      .attr("fill", "#94a3b8")
      .attr("opacity", 0.65);

  const gZoom = svg.append("g");
  const linkGroup = gZoom.append("g").attr("stroke-linecap", "round");
  const nodeGroup = gZoom.append("g");
  const labelGroup = gZoom.append("g");

  // Color scale by group
  const groups = Array.from(new Set(graph.nodes.map(d => d.group)));
  const palette = d3.schemeTableau10 ?? d3.schemeCategory10;
  const color = d3.scaleOrdinal(palette).domain(groups);

  // Legend
  const legend = d3.select("#legend");
  const legendItems = d3.select("#legendItems");
  if (groups.length > 0) {{
    legend.style("display", "block");
    legendItems.selectAll(".legend-item")
      .data(groups)
      .enter()
      .append("div")
      .attr("class", "legend-item")
      .html(d => `<span class="legend-swatch" style="background:${{color(d)}}"></span> ${{d}}`);
  }}

  // Zoom/pan
  const zoom = d3.zoom().scaleExtent([0.1, 4]).on("zoom", (event) => {{
    gZoom.attr("transform", event.transform);
  }});
  svg.call(zoom);

  // Reset zoom
  d3.select("#resetZoom").on("click", () => {{
    svg.transition().duration(350).call(zoom.transform, d3.zoomIdentity);
  }});

  // Links
  const link = linkGroup
    .selectAll("line")
    .data(graph.links)
    .enter()
    .append("line")
    .attr("class", d => "link weight-" + Math.min(4, Math.max(1, Math.round(d.weight))))
    .attr("stroke-width", d => Math.min(4, Math.max(1, d.weight)))
    .attr("marker-end", "url(#arrow)");

  // Nodes
  const node = nodeGroup
    .selectAll("g")
    .data(graph.nodes)
    .enter()
    .append("g")
    .attr("class", "node")
    .call(d3.drag()
      .on("start", dragstarted)
      .on("drag", dragged)
      .on("end", dragended));

  node.append("circle")
    .attr("r", d => Math.max(4, Math.min(18, d.size)))
    .attr("fill", d => color(d.group));

  // Labels
  const label = labelGroup
    .selectAll("text")
    .data(graph.nodes)
    .enter()
    .append("text")
    .attr("dy", "-0.9em")
    .attr("text-anchor", "middle")
    .text(d => d.label);

  let labelsVisible = true;
  d3.select("#toggleLabels").on("click", () => {{
    labelsVisible = !labelsVisible;
    label.style("display", labelsVisible ? null : "none");
  }});

  // Tooltips
  node.on("mouseenter", (event, d) => {{
    const entries = Object.entries(d).filter(([k]) => !['vx','vy','x','y','index'].includes(k));
    const html = `
      <div><strong>${{d.label}}</strong></div>
      <div style="margin-top:6px;">
        ${{
          entries.map(([k, v]) => `<div><span style="color:#94a3b8">${{k}}:</span> ${{String(v)}}</div>`).join("")
        }}
      </div>
    `;
    tooltip.html(html)
      .style("opacity", 1);
  }}).on("mousemove", (event) => {{
    const [x, y] = d3.pointer(event, container.node());
    tooltip.style("left", (x + 16) + "px")
           .style("top", (y + 16) + "px");
  }}).on("mouseleave", () => {{
    tooltip.style("opacity", 0);
  }});

  // Simulation
  const simulation = d3.forceSimulation(graph.nodes)
    .force("link", d3.forceLink(graph.links).id(d => d.id).distance(d => 40 + Math.min(200, (d.weight || 1) * 10)))
    .force("charge", d3.forceManyBody().strength(-180))
    .force("center", d3.forceCenter(0, 0))
    .force("collision", d3.forceCollide().radius(d => Math.max(10, d.size + 6)));

  simulation.on("tick", () => {{
    link
      .attr("x1", d => d.source.x)
      .attr("y1", d => d.source.y)
      .attr("x2", d => d.target.x)
      .attr("y2", d => d.target.y);

    node.attr("transform", d => `translate(${{d.x}}, ${{d.y}})`);
    label.attr("transform", d => `translate(${{d.x}}, ${{d.y}})`);
  }});

  // Responsive resize
  function resize() {{
    const rect = container.node().getBoundingClientRect();
    const width = rect.width;
    const height = rect.height;
    svg.attr("width", width).attr("height", height);
  }}
  window.addEventListener("resize", resize);
  resize();

  function dragstarted(event, d) {{
    if (!event.active) simulation.alphaTarget(0.3).restart();
    d.fx = d.x; d.fy = d.y;
  }}
  function dragged(event, d) {{
    d.fx = event.x; d.fy = event.y;
  }}
  function dragended(event, d) {{
    if (!event.active) simulation.alphaTarget(0);
    d.fx = null; d.fy = null;
  }}
</script>
</body>
</html>
"""
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
        vpath = Path(visualization_file)
        if not vpath.exists() or not vpath.is_file():
            raise FileNotFoundError(f"Visualization file not found: {vpath}")

        with vpath.open("r", encoding="utf-8") as f:
            data = json.load(f)

        title = f"MAS Visualization - {vpath.stem}"
        html = self.generate_html(data, title=title)

        if output_file:
            out_path = Path(output_file)
        else:
            out_name = f"{vpath.stem}.html"
            out_path = self.output_dir / out_name

        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(html, encoding="utf-8")

        if open_browser:
            webbrowser.open(f"file://{out_path.resolve()}")

        return str(out_path)

    def visualize_from_agent_system(self, agent_system, problem_id=None):
        '''
        Generate visualizations for all visualization files from an agent system.
        Args:
            agent_system: AgentSystem instance
            problem_id: Optional problem ID to filter by
        Returns:
            List of paths to generated HTML files
        '''
        html_paths = []

        # 1) If system can directly provide data dicts
        data_lists = []
        for meth in ("get_visualization_data", "get_visualizations", "visualization_data"):
            try:
                attr = getattr(agent_system, meth, None)
                if callable(attr):
                    result = attr(
                        problem_id) if problem_id is not None else attr()
                    if isinstance(result, list) and all(isinstance(x, dict) for x in result):
                        data_lists.extend(result)
                elif isinstance(attr, list) and all(isinstance(x, dict) for x in attr):
                    data_lists.extend(attr)
            except Exception:
                pass

        # Save any in-memory visualizations first
        for i, data in enumerate(data_lists):
            stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            base = f"agent_system_{problem_id or 'all'}_{stamp}_{i}"
            out_path = self.output_dir / f"{base}.html"
            html = self.generate_html(
                data, title=f"MAS Visualization - {base}")
            out_path.write_text(html, encoding="utf-8")
            html_paths.append(str(out_path))

        # 2) Collect files from known attributes/dirs
        candidate_dirs = set()
        attr_names = [
            "visualization_dir", "visualizations_dir",
            "output_dir", "outputs_dir",
            "log_dir", "logs_dir",
            "run_dir", "runs_dir",
            "work_dir", "workspace",
            "root_dir", "project_dir",
        ]

        for name in attr_names:
            try:
                val = getattr(agent_system, name, None)
                if val:
                    p = Path(val)
                    if p.exists() and p.is_dir():
                        candidate_dirs.add(p)
            except Exception:
                pass

        for meth in ("get_output_dir", "get_visualization_dir", "artifacts_dir"):
            try:
                fn = getattr(agent_system, meth, None)
                if callable(fn):
                    p = Path(fn())
                    if p.exists() and p.is_dir():
                        candidate_dirs.add(p)
            except Exception:
                pass

        # If agent_system itself is a path
        if isinstance(agent_system, (str, Path)):
            p = Path(agent_system)
            if p.exists():
                if p.is_file():
                    candidate_dirs.add(p.parent)
                else:
                    candidate_dirs.add(p)

        # 3) Gather visualization JSON files
        json_files = set()
        patterns = [
            "**/*visualization*.json",
            "**/*viz*.json",
            "**/*interactions*.json",
            "**/*graph*.json",
            "**/*.viz.json",
        ]

        for d in candidate_dirs:
            for pat in patterns:
                for f in d.rglob(pat):
                    if f.is_file():
                        json_files.add(f)

        # 4) If system can directly provide file paths
        for meth in ("get_visualization_files", "get_visualization_paths"):
            try:
                fn = getattr(agent_system, meth, None)
                if callable(fn):
                    res = fn(problem_id) if problem_id is not None else fn()
                    if isinstance(res, (list, tuple)):
                        for p in res:
                            pp = Path(p)
                            if pp.exists() and pp.is_file():
                                json_files.add(pp)
            except Exception:
                pass

        # Filter by problem_id if provided
        if problem_id is not None:
            json_files = {p for p in json_files if str(problem_id) in str(p)}

        # 5) Generate visualizations for files
        for f in sorted(json_files):
            try:
                out_name = f"{f.stem}-{uuid.uuid4().hex[:6]}.html"
                out_path = self.output_dir / out_name
                html_path = self.visualize(
                    f, output_file=out_path, open_browser=False)
                html_paths.append(html_path)
            except Exception:
                # Skip problematic files silently
                continue

        return html_paths
