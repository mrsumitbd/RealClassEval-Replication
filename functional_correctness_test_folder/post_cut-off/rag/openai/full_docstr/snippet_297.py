
import json
import os
import webbrowser
from pathlib import Path
from typing import List, Optional, Union


class MASVisualizer:
    """Utility for visualizing Multi-Agent System interactions."""

    def __init__(self, output_dir: Optional[Union[str, Path]] = None):
        """
        Initialize the MAS visualizer.

        Parameters
        ----------
        output_dir : str | Path | None
            Directory to save visualization HTML files. If None, a temporary
            directory named ``mas_visualizations`` will be created in the
            current working directory.
        """
        self.output_dir = Path(
            output_dir) if output_dir else Path.cwd() / "mas_visualizations"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    # --------------------------------------------------------------------- #
    #  Core rendering
    # --------------------------------------------------------------------- #
    def generate_html(self, visualization_data: dict, title: Optional[str] = None) -> str:
        """
        Generate HTML for visualizing agent interactions using D3.js.

        Parameters
        ----------
        visualization_data : dict
            Dictionary with ``nodes`` and ``links`` data. Example:
            {
                "nodes": [{"id": "A"}, {"id": "B"}],
                "links": [{"source": "A", "target": "B"}]
            }
        title : str | None
            Optional title for the visualization. Defaults to ``"MAS Visualization"``.

        Returns
        -------
        str
            Complete HTML document as a string.
        """
        title = title or "MAS Visualization"
        data_json = json.dumps(visualization_data, indent=2)

        # Minimal D3 force-directed graph example (v7)
        html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title}</title>
<script src="https://cdn.jsdelivr.net/npm/d3@7/dist/d3.min.js"></script>
<style>
    body {{ margin: 0; font-family: sans-serif; }}
    svg {{ width: 100vw; height: 100vh; }}
    .link {{ stroke: #999; stroke-opacity: 0.6; }}
    .node {{ stroke: #fff; stroke-width: 1.5px; }}
</style>
</head>
<body>
<script>
const data = {data_json};

const width = window.innerWidth;
const height = window.innerHeight;

const svg = d3.select("body").append("svg")
    .attr("viewBox", [0, 0, width, height]);

const simulation = d3.forceSimulation(data.nodes)
    .force("link", d3.forceLink(data.links).id(d => d.id).distance(120))
    .force("charge", d3.forceManyBody().strength(-300))
    .force("center", d3.forceCenter(width / 2, height / 2));

const link = svg.append("g")
    .attr("stroke", "#999")
    .attr("stroke-opacity", 0.6)
  .selectAll("line")
  .data(data.links)
  .join("line")
    .attr("stroke-width", 1.5);

const node = svg.append("g")
    .attr("stroke", "#fff")
    .attr("stroke-width", 1.5)
  .selectAll("circle")
  .data(data.nodes)
  .join("circle")
    .attr("r", 10)
    .attr("fill", d => d.color || "#69b3a2")
    .call(drag(simulation));

node.append("title")
    .text(d => d.id);

simulation.on("tick", () => {{
  link
      .attr("x1", d => d.source.x)
      .attr("y1", d => d.source.y)
      .attr("x2", d => d.target.x)
      .attr("y2", d => d.target.y);

  node
      .attr("cx", d => d.x)
      .attr("cy", d => d.y);
}});

function drag(simulation) {{
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

  return d3.drag()
      .on("start", dragstarted)
      .on("drag", dragged)
      .on("end", dragended);
}}
</script>
</body>
</html>"""
        return html_template

    # --------------------------------------------------------------------- #
    #  File handling & browser integration
    # --------------------------------------------------------------------- #
    def visualize(
        self,
        visualization_file: Union[str, Path],
        output_file: Optional[Union[str, Path]] = None,
        open_browser: bool = True,
    ) -> Path:
        """
        Generate an HTML visualization from a visualization data file and open in browser.

        Parameters
        ----------
        visualization_file : str | Path
            Path to the visualization data JSON file.
        output_file : str | Path | None
            Optional path to save the HTML output. If None, the file will be
            written to ``self.output_dir`` with the same base name and a
            ``.html`` extension.
        open_browser : bool
            Whether to open the visualization in a browser (default: True).

        Returns
        -------
        Path
            Path to the generated HTML file.
        """
        vis_path = Path(visualization_file)
        if not vis_path.is_file():
            raise FileNotFoundError(
                f"Visualization data file not found: {vis_path}")

        with vis_path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        # Determine output path
        if output_file:
            out_path = Path(output_file)
        else:
            out_path = self.output_dir / (vis_path.stem + ".html")

        # Ensure parent directory exists
        out_path.parent.mkdir(parents=True, exist_ok=True)

        # Generate HTML and write to file
        html_content = self.generate_html(data, title=vis_path.stem)
        out_path.write_text(html_content, encoding="utf-8")

        # Open in browser if requested
        if open_browser:
            webbrowser.open(f"file://{out_path.resolve()}")

        return out_path

    # --------------------------------------------------------------------- #
    #  Convenience for agent systems
    # --------------------------------------------------------------------- #
    def visualize_from_agent_system(
        self,
        agent_system,
        problem_id: Optional[str] = None,
    ) -> List[Path]:
        """
        Generate visualizations for all visualization files from an agent system.

        Parameters
        ----------
        agent_system : object
            An instance of an AgentSystem (or similar) that provides access to
