import json
import os
import tempfile
import time
import webbrowser
from pathlib import Path
from typing import Any, Dict, List, Optional, Union


class MASVisualizer:
    '''Utility for visualizing Multi-Agent System interactions'''

    def __init__(self, output_dir=None):
        '''
        Initialize the MAS visualizer.
        Args:
            output_dir: Directory to save visualization HTML files
        '''
        if output_dir is None:
            output_dir = os.path.join(
                tempfile.gettempdir(), "mas_visualizations")
        self.output_dir = os.path.abspath(str(output_dir))
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_html(self, visualization_data, title=None):
        '''
        Generate HTML for visualizing agent interactions using D3.js.
        Args:
            visualization_data: Dictionary with nodes and links data
            title: Optional title for the visualization
        Returns:
            HTML string
        '''
        try:
            data_json = json.dumps(visualization_data)
        except Exception as e:
            raise ValueError(
                f"visualization_data must be JSON serializable: {e}")

        page_title = title or "Multi-Agent System Visualization"
        # Simple force-directed graph with zoom, pan, tooltips, and legend support
        html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{page_title}</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  html, body {{
    margin: 0; padding: 0; height: 100%; width: 100%; background: #0f172a; color: #e2e8f0; font-family: Arial, Helvetica, sans-serif;
  }}
  #container {{
    display: flex; flex-direction: column; height: 100%;
  }}
  header {{
    padding: 12px 16px; border-bottom: 1px solid #1f2a44; background: #111827;
  }}
  h1 {{
    margin: 0; font-size: 18px; font-weight: 600;
  }}
  #meta {{
    font-size: 12px; color: #94a3b8; margin-top: 4px;
  }}
  #graph {{
    flex: 1; position: relative;
  }}
  .tooltip {{
    position: absolute; padding: 6px 8px; background: rgba(17, 24, 39, 0.95);
    color: #e5e7eb; border: 1px solid #374151; border-radius: 6px; pointer-events: none;
    font-size: 12px; white-space: pre-wrap; max-width: 320px;
  }}
  .legend {{
    position: absolute; top: 12px; right: 12px; background: rgba(17, 24, 39, 0.85);
    padding: 8px 10px; border: 1px solid #374151; border-radius: 8px; font-size: 12px;
  }}
  .legend-item {{
    display: flex; align-items: center; margin: 4px 0;
  }}
  .legend-swatch {{
    width: 12px; height: 12px; border-radius: 50%; margin-right: 6px; border: 1px solid #111827;
  }}
  .link {{
    stroke: #64748b; stroke-opacity: 0.5;
  }}
  .node {{
    stroke: #0b1020; stroke-width: 1.5px;
  }}
  .node text {{
    font-size: 10px; fill: #e2e8f0; pointer-events: none;
  }}
  .status-bar {{
    position: absolute; left: 12px; bottom: 12px; font-size: 12px; color: #94a3b8;
    background: rgba(17, 24, 39, 0.85); padding: 6px 8px; border: 1px solid #374151; border-radius: 6px;
  }}
</style>
</head>
<body>
<div id="container">
  <header>
    <h1>{page_title}</h1>
    <div id="meta"></div>
  </header>
  <div id="graph"></div>
</div>

<script src="https://cdn.jsdelivr.net/npm/d3@7/dist/d3.min.js"></script>
<script>
(function() {{
  const data = {data_json};

  const nodes = (data.nodes || []).map((d, i) => Object.assign({{id: d.id ?? i}}, d));
  const links = (data.links || []).map(l => Object.assign({{}}, l));

  const typeKey = "type";
  const groupKey = "group";
  const nodeTypes = new Set(nodes.map(n => n[typeKey]).filter(v => v !== undefined));
  const linkTypes = new Set(links.map(l => l[typeKey]).filter(v => v !== undefined));
  const groups = new Set(nodes.map(n => n[groupKey]).filter(v => v !== undefined));

  const width = window.innerWidth;
  const height = window.innerHeight - 60;

  const color = d3.scaleOrdinal()
    .domain(Array.from(groups.size ? groups : nodeTypes.size ? nodeTypes : ["default"]))
    .range(d3.schemeSet2);

  const linkColor = d3.scaleOrdinal()
    .domain(Array.from(linkTypes.size ? linkTypes : ["default"]))
    .range(d3.schemeSet3);

  const container = d3.select("#graph");
  container.selectAll("*").remove();

  const tooltip = container.append("div")
    .attr("class", "tooltip")
    .style("opacity", 0);

  const legend = container.append("div")
    .attr("class", "legend");

  const status = container.append("div")
    .attr("class", "status-bar")
    .text("Drag nodes to reposition. Scroll to zoom. Double-click background to reset view.");

  const svg = container.append("svg")
    .attr("width", "100%")
    .attr("height", height)
    .attr("viewBox", [0, 0, width, height])
    .style("display", "block");

  const zoom = d3.zoom()
    .scaleExtent([0.1, 8])
    .on("zoom", (event) => {{
      g.attr("transform", event.transform);
    }});
  svg.call(zoom);
  svg.on("dblclick.zoom", null);
  svg.on("dblclick", () => {{
    svg.transition().duration(400).call(zoom.transform, d3.zoomIdentity);
  }});

  const g = svg.append("g");

  const link = g.append("g")
    .attr("stroke-width", 1.2)
    .selectAll("line")
    .data(links)
    .join("line")
    .attr("class", "link")
    .attr("stroke", d => linkColor(d[typeKey] ?? "default"));

  const node = g.append("g")
    .selectAll("g")
    .data(nodes)
    .join("g")
    .attr("class", "node")
    .call(d3.drag()
      .on("start", (event, d) => {{
        if (!event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x; d.fy = d.y;
      }})
      .on("drag", (event, d) => {{
        d.fx = event.x; d.fy = event.y;
      }})
      .on("end", (event, d) => {{
        if (!event.active) simulation.alphaTarget(0);
        d.fx = null; d.fy = null;
      }}));

  node.append("circle")
    .attr("r", d => Math.max(4, Math.min(18, d.size ?? 8)))
    .attr("fill", d => color((d[groupKey] ?? d[typeKey] ?? "default")))
    .on("mouseover", (event, d) => {{
      const text = JSON.stringify(d, null, 2);
      tooltip.style("opacity", 1)
             .style("left", (event.offsetX + 12) + "px")
             .style("top", (event.offsetY + 12) + "px")
             .text(text);
    }})
    .on("mousemove", (event) => {{
      tooltip.style("left", (event.offsetX + 12) + "px")
             .style("top", (event.offsetY + 12) + "px");
    }})
    .on("mouseout", () => tooltip.style("opacity", 0));

  node.append("text")
    .attr("x", 10)
    .attr("y", 3)
    .text(d => d.label ?? d.name ?? d.id)
    .style("opacity", 0.9);

  const simulation = d3.forceSimulation(nodes)
    .force("link", d3.forceLink(links).id(d => d.id).distance(l => l.distance ?? 60).strength(l => l.strength ?? 0.3))
    .force("charge", d3.forceManyBody().strength(-160))
    .force("center", d3.forceCenter(width / 2, height / 2))
    .force("collide", d3.forceCollide().radius(d => Math.max(8, Math.min(24, (d.size ?? 8) + 6))).iterations(2));

  simulation.on("tick", () => {{
    link
      .attr("x1", d => d.source.x)
      .attr("y1", d => d.source.y)
      .attr("x2", d => d.target.x)
      .attr("y2", d => d.target.y);

    node.attr("transform", d => `translate(${d.x},${d.y})`);
  }});

  const meta = document.getElementById("meta");
  const info = {{}};
  info.nodes = nodes.length;
  info.links = links.length;
  if (groups.size) info.groups = Array.from(groups).join(", ");
  if (nodeTypes.size) info.nodeTypes = Array.from(nodeTypes).join(", ");
  if (linkTypes.size) info.linkTypes = Array.from(linkTypes).join(", ");
  meta.textContent = Object.entries(info).map(([k,v]) => `${{k}}: ${{v}}`).join("  |  ");

  function renderLegend() {{
    legend.selectAll("*").remove();
    const title = legend.append("div").text("Legend");
    if (groups.size || nodeTypes.size) {{
      const header = legend.append("div").style("margin-top", "6px").text("Nodes");
      const items = Array.from((groups.size ? groups : nodeTypes));
      const row = legend.selectAll(".legend-item.node").data(items).join("div").attr("class", "legend-item");
      row.append("div").attr("class", "legend-swatch")
                       .style("background", d => color(d ?? "default"));
      row.append("div").text(d => String(d ?? "default"));
    }}
    if (linkTypes.size) {{
      const header = legend.append("div").style("margin-top", "6px").text("Links");
      const row = legend.selectAll(".legend-item.link").data(Array.from(linkTypes)).join("div").attr("class", "legend-item");
      row.append("div").attr("class", "legend-swatch")
                       .style("background", d => linkColor(d ?? "default"));
      row.append("div").text(d => String(d ?? "default"));
    }}
  }}
  renderLegend();
}})();
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
        vis_path = Path(visualization_file)
        if not vis_path.exists():
            raise FileNotFoundError(
                f"Visualization file not found: {vis_path}")

        with vis_path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        title = data.get("title") or f"M.A.S Visualization - {vis_path.stem}"
        html = self.generate_html(data, title=title)

        if output_file is None:
            safe_name = vis_path.stem
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            outfile = Path(self.output_dir) / f"{safe_name}-{timestamp}.html"
        else:
            outfile = Path(output_file)
            if not outfile.parent.exists():
                outfile.parent.mkdir(parents=True, exist_ok=True)

        with outfile.open("w", encoding="utf-8") as f:
            f.write(html)

        if open_browser:
            webbrowser.open_new_tab(outfile.as_uri())

        return str(outfile)

    def visualize_from_agent_system(self, agent_system, problem_id=None):
        '''
        Generate visualizations for all visualization files from an agent system.
        Args:
            agent_system: AgentSystem instance
            problem_id: Optional problem ID to filter by
        Returns:
            List of paths to generated HTML files
        '''
        files: List[Union[str, Path]] = []

        getter_candidates = [
            "get_visualization_files",
            "get_visualizations",
            "visualization_files",
            "visualizations",
        ]

        found = False
        for name in getter_candidates:
            if hasattr(agent_system, name):
                attr = getattr(agent_system, name)
                if callable(attr):
                    try:
                        res = attr(
                            problem_id) if problem_id is not None else attr()
                    except TypeError:
                        res = attr()
                    if res:
                        files.extend(res if isinstance(
                            res, (list, tuple)) else [res])
                        found = True
                        break
                else:
                    if attr:
                        files.extend(attr if isinstance(
                            attr, (list, tuple)) else [attr])
                        found = True
                        break

        if not found:
            dirs_to_search = []
            for cand in ["output_dir", "log_dir", "artifact_dir", "results_dir", "workspace"]:
                if hasattr(agent_system, cand):
                    path = getattr(agent_system, cand)
                    if path:
                        dirs_to_search.append(Path(path))
            if not dirs_to_search:
                dirs_to_search.append(Path.cwd())

            patterns = ["*.viz.json", "*visualization.json",
                        "*.visualization.json", "visualization_*.json", "*_viz.json"]
            collected: List[Path] = []
            for base in dirs_to_search:
                if base and Path(base).exists():
                    for pattern in patterns:
                        collected.extend(base.rglob(pattern))

            if problem_id is not None:
                pid_str = str(problem_id)
                collected = [
                    p for p in collected if pid_str in p.name or pid_str in str(p.parent)]
            files.extend(sorted({str(p) for p in collected}))

        result_paths: List[str] = []
        for f in files:
            try:
                path = self.visualize(f, open_browser=False)
                result_paths.append(path)
            except Exception:
                continue

        if result_paths:
            try:
                webbrowser.open_new_tab(Path(result_paths[0]).as_uri())
            except Exception:
                pass

        return result_paths
