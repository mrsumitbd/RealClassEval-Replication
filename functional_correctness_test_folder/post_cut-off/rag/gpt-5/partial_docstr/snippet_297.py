import json
import os
import re
import webbrowser
from pathlib import Path
from typing import Any, Dict, List, Optional, Union


class MASVisualizer:
    """Utility for visualizing Multi-Agent System interactions"""

    def __init__(self, output_dir: Optional[Union[str, Path]] = None):
        """
        Initialize the MAS visualizer.
        Args:
            output_dir: Directory to save visualization HTML files
        """
        if output_dir is None:
            output_dir = Path.cwd() / "mas_visualizations"
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_html(self, visualization_data: Dict[str, Any], title: Optional[str] = None) -> str:
        """
        Generate HTML for visualizing agent interactions using D3.js.
        Args:
            visualization_data: Dictionary with nodes and links data
            title: Optional title for the visualization
        Returns:
            HTML string
        """
        if not isinstance(visualization_data, dict):
            raise ValueError(
                "visualization_data must be a dictionary containing 'nodes' and 'links'")
        nodes = visualization_data.get("nodes")
        links = visualization_data.get("links")
        if nodes is None or links is None:
            raise ValueError(
                "visualization_data must include 'nodes' and 'links' keys")

        if title is None:
            title = visualization_data.get(
                "title", "Multi-Agent System Interactions")

        # Safely embed JSON inside a <script type="application/json"> tag
        json_text = json.dumps(visualization_data, ensure_ascii=False)
        json_text = json_text.replace("</script>", "<\\/script>")

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title}</title>
<meta name="viewport" content="width=device-width, initial-scale=1" />
<script src="https://d3js.org/d3.v7.min.js" integrity="sha384-3h0YgX0o1PJHk0uU4H0M8Hsz2QjNQ3oY+Z7m3pH8aEGhFGAJvPiQwXl4szVUut6M" crossorigin="anonymous"></script>
<style>
  :root {{
    --bg: #0f1419;
    --panel: #151a21;
    --text: #e6edf3;
    --muted: #9aa4ad;
    --link: #6ea8fe;
    --accent: #7ee787;
    --warn: #ffb86b;
    --danger: #ff7b72;
    --grid: #26303a;
  }}
  html, body {{
    height: 100%;
    margin: 0;
    background: var(--bg);
    color: var(--text);
    font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Cantarell, Noto Sans, Helvetica Neue, Arial, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", sans-serif;
  }}
  .container {{
    display: flex;
    flex-direction: column;
    height: 100%;
  }}
  header {{
    padding: 12px 16px;
    border-bottom: 1px solid var(--grid);
    background: var(--panel);
  }}
  header h1 {{
    font-size: 16px;
    margin: 0;
    font-weight: 600;
  }}
  #chart {{
    flex: 1;
    position: relative;
    overflow: hidden;
  }}
  svg {{
    width: 100%;
    height: 100%;
    display: block;
    background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.00));
  }}
  .link {{
    stroke: #7f8a96;
    stroke-opacity: 0.6;
  }}
  .link-label {{
    fill: var(--muted);
    font-size: 11px;
    pointer-events: none;
  }}
  .node circle {{
    stroke: #0b0f14;
    stroke-width: 1px;
    cursor: pointer;
  }}
  .node text {{
    font-size: 12px;
    fill: var(--text);
    paint-order: stroke;
    stroke: #0b0f14;
    stroke-width: 2px;
    stroke-linejoin: round;
  }}
  .legend {{
    position: absolute;
    top: 12px;
    right: 12px;
    background: rgba(21, 26, 33, 0.9);
    border: 1px solid var(--grid);
    border-radius: 8px;
    padding: 8px 10px;
    color: var(--text);
    max-width: 260px;
    font-size: 12px;
  }}
  .legend h3 {{
    margin: 0 0 6px 0;
    font-size: 12px;
    font-weight: 600;
    color: var(--muted);
  }}
  .legend-item {{
    display: flex;
    align-items: center;
    gap: 8px;
    margin: 3px 0;
  }}
  .legend-swatch {{
    width: 12px;
    height: 12px;
    border-radius: 50%;
    border: 1px solid rgba(0,0,0,0.4);
  }}
  .tooltip {{
    position: absolute;
    pointer-events: none;
    background: rgba(21, 26, 33, 0.95);
    border: 1px solid var(--grid);
    padding: 8px 10px;
    border-radius: 8px;
    font-size: 12px;
    color: var(--text);
    max-width: 360px;
    z-index: 3;
    display: none;
    box-shadow: 0 6px 22px rgba(0,0,0,0.35);
  }}
  .tooltip .title {{
    font-weight: 600;
    margin-bottom: 6px;
    color: var(--accent);
  }}
  .tooltip .kv {{
    display: grid;
    grid-template-columns: auto 1fr;
    gap: 4px 10px;
  }}
  .gridlines line {{
    stroke: var(--grid);
    stroke-width: 1;
  }}
  .gridlines path {{
    stroke-width: 0;
  }}
</style>
</head>
<body>
  <div class="container">
    <header>
      <h1>{title}</h1>
    </header>
    <div id="chart"></div>
    <div class="legend" id="legend" aria-hidden="true"></div>
    <div class="tooltip" id="tooltip"></div>
  </div>

  <script id="graph-data" type="application/json">{json_text}</script>
  <script>
    (function() {{
      const raw = document.getElementById('graph-data').textContent;
      const data = JSON.parse(raw);
      const chartEl = document.getElementById('chart');
      const tooltip = document.getElementById('tooltip');
      const legendEl = document.getElementById('legend');

      const width = chartEl.clientWidth || 1024;
      const height = chartEl.clientHeight || 640;

      const colorScale = d3.scaleOrdinal(d3.schemeTableau10);
      const linkColor = d3.scaleOrdinal().domain(["message","request","response","coordination"]).range(["#6ea8fe","#ffb86b","#7ee787","#c4b5fd"]);

      // Extract groups/types for legend
      const groups = Array.from(new Set((data.nodes || []).map(n => n.group || n.type || 'default')));
      const legendItems = groups.map((g) => {{
        return {{name: String(g), color: colorScale(g)}};
      }});
      if (legendItems.length > 0) {{
        legendEl.innerHTML = '<h3>Agent Groups</h3>' + legendItems.map(li => `
          <div class="legend-item">
            <span class="legend-swatch" style="background:${{li.color}}"></span>
            <span>${{li.name}}</span>
          </div>
        `).join('');
        legendEl.setAttribute('aria-hidden', 'false');
      }}

      const svg = d3.select('#chart').append('svg')
        .attr('viewBox', [0, 0, width, height])
        .call(d3.zoom().on('zoom', (event) => {{
          g.attr('transform', event.transform);
        }}))
        .on('dblclick.zoom', null);

      // Background grid
      const grid = svg.append('g').attr('class', 'gridlines');
      const gridSize = 48;
      for (let x = 0; x <= width; x += gridSize) {{
        grid.append('line').attr('x1', x).attr('y1', 0).attr('x2', x).attr('y2', height);
      }}
      for (let y = 0; y <= height; y += gridSize) {{
        grid.append('line').attr('x1', 0).attr('y1', y).attr('x2', width).attr('y2', y);
      }}

      const defs = svg.append('defs');
      defs.append('marker')
        .attr('id', 'arrow')
        .attr('viewBox', '0 -5 10 10')
        .attr('refX', 18)
        .attr('refY', 0)
        .attr('markerWidth', 6)
        .attr('markerHeight', 6)
        .attr('orient', 'auto')
        .append('path')
        .attr('d', 'M0,-5L10,0L0,5')
        .attr('fill', '#7f8a96')
        .attr('opacity', 0.8);

      const g = svg.append('g');

      const radius = (d) => {{
        const sz = +d.size || +d.weight || 0;
        if (Number.isFinite(sz) && sz > 0) return 6 + Math.sqrt(sz);
        return 8;
      }};

      const linkWidth = (l) => {{
        const v = +l.value || +l.weight || 1;
        return Math.max(1, Math.min(6, Math.log2(v + 1) + 1));
      }};

      const links = (data.links || []).map(d => Object.assign({{}}, d));
      const nodes = (data.nodes || []).map(d => Object.assign({{}}, d));

      const link = g.append('g')
        .attr('stroke-linecap', 'round')
        .selectAll('line')
        .data(links)
        .join('line')
        .attr('class', 'link')
        .attr('stroke-width', d => linkWidth(d))
        .attr('stroke', d => linkColor(d.type || d.kind || 'default'))
        .attr('marker-end', 'url(#arrow)');

      const linkLabels = g.append('g')
        .selectAll('text')
        .data(links)
        .join('text')
        .attr('class', 'link-label')
        .attr('dy', -2)
        .text(d => d.label || d.type || '');

      const node = g.append('g')
        .attr('stroke-linecap', 'round')
        .selectAll('g')
        .data(nodes)
        .join('g')
        .attr('class', 'node')
        .call(d3.drag()
          .on('start', (event, d) => {{
            if (!event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x; d.fy = d.y;
          }})
          .on('drag', (event, d) => {{
            d.fx = event.x; d.fy = event.y;
          }})
          .on('end', (event, d) => {{
            if (!event.active) simulation.alphaTarget(0);
            d.fx = null; d.fy = null;
          }}));

      node.append('circle')
        .attr('r', d => radius(d))
        .attr('fill', d => d.color || colorScale(d.group || d.type || 'default'))
        .attr('opacity', 0.95);

      node.append('title').text(d => d.id || d.name || '');

      node.append('text')
        .attr('x', 12)
        .attr('y', 4)
        .text(d => d.label || d.name || d.id || '')
        .attr('fill', '#fff');

      const showTooltip = (html, x, y) => {{
        tooltip.innerHTML = html;
        tooltip.style.display = 'block';
        const pad = 10;
        const rect = tooltip.getBoundingClientRect();
        const left = Math.min(x + pad, window.innerWidth - rect.width - pad);
        const top = Math.min(y + pad, window.innerHeight - rect.height - pad);
        tooltip.style.left = left + 'px';
        tooltip.style.top = top + 'px';
      }};
      const hideTooltip = () => {{
        tooltip.style.display = 'none';
      }};

      node.on('mousemove', (event, d) => {{
        const props = Object.entries(d).filter(([k,_]) => !['index','x','y','vx','vy','fx','fy'].includes(k));
        const kv = props.map(([k,v]) => `<span style="color:var(--muted)">${{k}}</span><span>${{String(v)}}</span>`).join('');
        const html = `
          <div class="title">Agent: ${{d.label || d.name || d.id}}</div>
          <div class="kv">${{kv}}</div>
        `;
        showTooltip(html, event.clientX, event.clientY);
      }}).on('mouseleave', hideTooltip);

      link.on('mousemove', (event, d) => {{
        const props = Object.entries(d).filter(([k,_]) => !['index','x','y','vx','vy','fx','fy','source','target'].includes(k));
        const kv = props.map(([k,v]) => `<span style="color:var(--muted)">${{k}}</span><span>${{String(v)}}</span>`).join('');
        const label = d.label || d.type || 'link';
        const src = (typeof d.source === 'object' ? (d.source.label || d.source.name || d.source.id) : d.source);
        const tgt = (typeof d.target === 'object' ? (d.target.label || d.target.name || d.target.id) : d.target);
        const html = `
          <div class="title">Interaction: ${{label}}</div>
          <div class="kv">
            <span style="color:var(--muted)">source</span><span>${{src}}</span>
            <span style="color:var(--muted)">target</span><span>${{tgt}}</span>
            ${{kv}}
          </div>
        `;
        showTooltip(html, event.clientX, event.clientY);
      }}).on('mouseleave', hideTooltip);

      const simulation = d3.forceSimulation(nodes)
        .force('link', d3.forceLink(links).id(d => d.id).distance(d => 60 + (5 * Math.min(10, +d.value || +d.weight || 0))))
        .force('charge', d3.forceManyBody().strength(-240))
        .force('center', d3.forceCenter(width / 2, height / 2))
        .force('collide', d3.forceCollide().radius(d => radius(d) + 4).iterations(2));

      simulation.on('tick', () => {{
        link
          .attr('x1', d => d.source.x)
          .attr('y1', d => d.source.y)
          .attr('x2', d => d.target.x)
          .attr('y2', d => d.target.y);

        linkLabels
          .attr('x', d => (d.source.x + d.target.x) / 2)
          .attr('y', d => (d.source.y + d.target.y) / 2);

        node.attr('transform', d => `translate(${{d.x}}, ${{d.y}})`);
      }});

      // Resize observer for responsiveness
      const ro = new ResizeObserver(entries => {{
        for (const entry of entries) {{
          const w = entry.contentRect.width || width;
          const h = entry.contentRect.height || height;
          svg.attr('viewBox', [0, 0, w, h]);
          simulation.force('center', d3.forceCenter(w/2, h/2)).alpha(0.05).restart();
        }}
      }});
      ro.observe(chartEl);
    }})();
  </script>
</body>
</html>
"""
        return html

    def visualize(
        self,
        visualization_file: Union[str, Path, Dict[str, Any]],
        output_file: Optional[Union[str, Path]] = None,
        open_browser: bool = True,
    ) -> Path:
        """
        Generate an HTML visualization from a visualization data file and open in browser.
        Args:
            visualization_file: Path to the visualization data JSON file
            output_file: Optional path to save the HTML output
            open_browser: Whether to open the visualization in a browser (default: True)
        Returns:
            Path to the generated HTML file
        """
        data: Dict[str, Any]
        title = None

        if isinstance(visualization_file, (str, Path)) and Path(visualization_file).exists():
            vf_path = Path(visualization_file)
            with vf_path.open("r", encoding="utf-8") as f:
                data = json.load(f)
            title = data.get("title") or vf_path.stem
            if output_file is None:
                safe_stem = self._sanitize_filename(vf_path.stem)
                output_file = self.output_dir / f"{safe_stem}.html"
        elif isinstance(visualization_file, dict):
            data = visualization_file
            title = data.get("title")
            if output_file is None:
                output_file = self.output_dir / "visualization.html"
        else:
            raise FileNotFoundError(
                f"Visualization file not found: {visualization_file}")

        html = self.generate_html(data, title=title)
        out_path = Path(output_file)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(html, encoding="utf-8")

        if open_browser:
            webbrowser.open(out_path.as_uri())

        return out_path

    def visualize_from_agent_system(self, agent_system: Any, problem_id: Optional[Union[str, int]] = None) -> List[Path]:
        """
        Generate visualizations for all visualization files from an agent system.
        Args:
            agent_system: AgentSystem instance
            problem_id: Optional problem ID to filter by
        Returns:
            List of paths to generated HTML files
        """
        viz_files: List[Path] = []

        # Try to obtain visualization files via common hooks/attributes
        if hasattr(agent_system, "get_visualization_files") and callable(getattr(agent_system, "get_visualization_files")):
            files = agent_system.get_visualization_files(
                problem_id=problem_id)  # type: ignore[attr-defined]
            viz_files = [Path(p) for p in files]
        elif hasattr(agent_system, "visualization_files"):
            files = getattr(agent_system, "visualization_files")
            viz_files = [Path(p) for p in files]
        else:
            base_dirs = []
            candidates = ["visualizations", "viz",
                          "outputs", "logs", "runs", "out"]
            for attr in ["visualization_dir", "output_dir", "outputs_dir", "work_dir", "run_dir", "log_dir", "root_dir"]:
                d = getattr(agent_system, attr, None)
                if d:
                    base_dirs.append(Path(d))
            if not base_dirs:
                base_dirs.append(Path.cwd())

            discovered: List[Path] = []
            for base in base_dirs:
                for c in candidates:
                    dir_path = (
                        base / c) if not str(base).endswith(c) else base
                    if dir_path.exists() and dir_path.is_dir():
                        discovered.append(dir_path)

            if not discovered:
                discovered = base_dirs

            patterns = ["*.viz.json", "*visualization*.json",
                        "*viz*.json", "*.json"]
            seen = set()
            for root in discovered:
                for pat in patterns:
                    for p in root.rglob(pat):
                        if problem_id is not None and str(problem_id) not in p.name:
                            continue
                        if p.suffix.lower() == ".json" and p.is_file():
                            if p.resolve() not in seen:
                                seen.add(p.resolve())
                                viz_files.append(p)

            # Validate by checking content has nodes and links
            valid_files: List[Path] = []
            for p in viz_files:
                try:
                    with p.open("r", encoding="utf-8") as f:
                        data = json.load(f)
                    if isinstance(data, dict) and "nodes" in data and "links" in data:
                        valid_files.append(p)
                except Exception:
                    continue
            viz_files = valid_files

        generated: List[Path] = []
        for vf in viz_files:
            try:
                out_name = self._sanitize_filename(vf.stem) + ".html"
                out_path = self.output_dir / out_name
                generated.append(self.visualize(
                    vf, output_file=out_path, open_browser=False))
            except Exception:
                continue

        return generated

    @staticmethod
    def _sanitize_filename(name: str) -> str:
        name = name.strip().replace(" ", "_")
        name = re.sub(r"[^A-Za-z0-9_.-]", "_", name)
        name = re.sub(r"_+", "_", name)
        return name[:255] if name else "visualization"
