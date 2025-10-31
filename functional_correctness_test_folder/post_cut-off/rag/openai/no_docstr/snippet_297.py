
import json
import os
import pathlib
import webbrowser
from typing import Any, Dict, Iterable, List, Optional, Union


class MASVisualizer:
    """Utility for visualizing Multi‑Agent System interactions."""

    def __init__(self, output_dir: Optional[Union[str, pathlib.Path]] = None):
        """
        Initialize the MAS visualizer.

        Parameters
        ----------
        output_dir : str | pathlib.Path | None
            Directory to save visualization HTML files. If ``None`` the current
            working directory is used.
        """
        self.output_dir = pathlib.Path(output_dir or os.getcwd())
        self.output_dir.mkdir(parents=True, exist_ok=True)

    # --------------------------------------------------------------------- #
    #  Core rendering
    # --------------------------------------------------------------------- #
    def generate_html(
        self,
        visualization_data: Dict[str, Any],
        title: Optional[str] = None,
    ) -> str:
        """
        Generate an HTML string that visualizes agent interactions using D3.js.

        Parameters
        ----------
        visualization_data : dict
            Dictionary containing at least two keys: ``nodes`` and ``links``.
            ``nodes`` should be a list of dicts with at least an ``id`` field.
            ``links`` should be a list of dicts with ``source`` and ``target`` fields
            referencing node ids.
        title : str | None
            Optional title for the visualization. If omitted, the title will be
            ``"MAS Interaction Graph"``.

        Returns
        -------
        str
            A complete HTML document ready to be written to a file or served.
        """
        if not isinstance(visualization_data, dict):
            raise TypeError("visualization_data must be a dict")

        nodes = visualization_data.get("nodes")
        links = visualization_data.get("links")

        if nodes is None or links is None:
            raise ValueError(
                "visualization_data must contain 'nodes' and 'links' keys")

        # Escape JSON for embedding
        data_json = json.dumps({"nodes": nodes, "links": links})

        # Basic D3 force‑directed graph template
        html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title or "MAS Interaction Graph"}</title>
<script src="https://cdn.jsdelivr.net/npm/d3@7"></script>
<style>
    body {{ margin:0; font-family:Arial,Helvetica,sans-serif; }}
    .link {{ stroke: #999; stroke-opacity: 0.6; }}
    .node {{ stroke: #fff; stroke-width: 1.5px; }}
    text {{ pointer-events: none; font-size: 10px; }}
</style>
</head>
<body>
<svg width="100%" height="100%"></svg>
<script>
const data = {data_json};

const svg = d3.select("svg"),
      width = +svg.node().getBoundingClientRect().width,
      height = +svg.node().getBoundingClientRect().height;

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
    .attr("r", 8)
    .attr("fill", d => d.color || "#69b3a2")
    .call(drag(simulation));

node.append("title")
    .text(d => d.id);

const label = svg.append("g")
    .selectAll("text")
    .data(data.nodes)
    .join("text")
    .attr("dy", -10)
    .attr("text-anchor", "middle")
    .text(d => d.label || d.id);

simulation.on("tick", () => {{
    link
        .attr("x1", d => d.source.x)
        .attr("y1", d => d.source.y)
        .attr("x2", d => d.target.x)
        .attr("y2", d => d.target.y);

    node
        .attr("cx", d => d.x)
        .attr("cy", d => d.y);

    label
        .attr("x", d => d.x)
        .attr("y", d => d.y);
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
    #  File handling
    # --------------------------------------------------------------------- #
    def visualize(
        self,
        visualization_file: Union[str, pathlib.Path],
        output_file: Optional[Union[str, pathlib.Path]] = None,
        open_browser: bool = True,
    ) -> pathlib.Path:
        """
        Generate an HTML visualization from a JSON data file and optionally open it.

        Parameters
        ----------
        visualization_file : str | pathlib.Path
            Path to the JSON file containing the visualization data.
        output_file : str | pathlib.Path | None
            Path to write the generated HTML file. If omitted, the file will be
            written to ``self.output_dir`` with the same base name and a
            ``.html`` extension.
        open_browser : bool
            If ``True`` the resulting HTML file will be opened in the default
            web browser.

        Returns
        -------
        pathlib.Path
            Path to the generated HTML file.
        """
        vis_path = pathlib.Path(visualization_file)
        if not vis_path.is_file():
            raise FileNotFoundError(
                f"Visualization file not found: {vis_path}")

        with vis_path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        html = self.generate_html(data, title=vis_path.stem)

        if output_file is None:
            output_file = self.output_dir / f"{vis_path.stem}.html"
        else:
            output_file = pathlib.Path(output_file)

        output_file.parent.mkdir(parents=True, exist_ok=True)
        with output_file.open("w", encoding="utf-8") as f:
            f.write(html)

        if open_browser:
            webbrowser.open(f"file://{output_file.resolve()}")

        return output_file

    # --------------------------------------------------------------------- #
    #  Agent system integration
    # --------------------------------------------------------------------- #
    def visualize_from_agent_system(
        self,
        agent_system: Any,
        problem_id: Optional[str] = None,
    ) -> List[pathlib.Path]:
        """
        Generate visualizations for all visualization files associated with an
        agent system.

        Parameters
        ----------
        agent_system : Any
            An object representing an agent system. It must expose either a
            ``visualization_files`` attribute (iterable of file paths) or a
            ``get_visualization_files`` method that accepts an optional
            ``problem_id`` argument.
        problem_id : str | None
            Optional problem identifier to filter the visualization files
