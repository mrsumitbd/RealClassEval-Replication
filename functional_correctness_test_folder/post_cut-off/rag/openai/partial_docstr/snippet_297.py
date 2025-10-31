
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
    #  HTML generation
    # --------------------------------------------------------------------- #
    def generate_html(
        self,
        visualization_data: Dict[str, Any],
        title: Optional[str] = None,
    ) -> str:
        """
        Generate an HTML string that visualizes agent interactions using
        D3.js.

        Parameters
        ----------
        visualization_data : dict
            Dictionary with ``nodes`` and ``links`` keys. Each node is a
            dictionary with at least an ``id`` field. Each link is a
            dictionary with ``source`` and ``target`` fields that refer to
            node ids.
        title : str | None
            Optional title for the visualization. If omitted a generic title
            is used.

        Returns
        -------
        str
            Complete HTML document as a string.
        """
        # Basic D3 force‑directed graph template
        d3_template = """
<!DOCTYPE html>
<meta charset="utf-8">
<title>{title}</title>
<style>
    .link {{ stroke: #999; stroke-opacity: 0.6; }}
    .node {{ stroke: #fff; stroke-width: 1.5px; }}
</style>
<body>
<script src="https://d3js.org/d3.v7.min.js"></script>
<script>
const data = {data};

const width = 960;
const height = 600;

const svg = d3.select("body").append("svg")
    .attr("width", width)
    .attr("height", height);

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
    .attr("fill", d => d.group ? d3.schemeCategory10[d.group % 10] : "#69b3a2")
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
</html>
"""
        # Ensure the data contains the required keys
        if "nodes" not in visualization_data or "links" not in visualization_data:
            raise ValueError(
                "visualization_data must contain 'nodes' and 'links' keys")

        # Convert data to JSON string with indentation for readability
        data_json = json.dumps(visualization_data, indent=2)

        # Use provided title or a default one
        title_str = title or "MAS Interaction Graph"

        return d3_template.format(title=title_str, data=data_json)

    # --------------------------------------------------------------------- #
    #  File handling & browser opening
    # --------------------------------------------------------------------- #
    def visualize(
        self,
        visualization_file: Union[str, pathlib.Path],
        output_file: Optional[Union[str, pathlib.Path]] = None,
        open_browser: bool = True,
    ) -> pathlib.Path:
        """
        Generate an HTML visualization from a JSON data file and optionally
        open it in a web browser.

        Parameters
        ----------
        visualization_file : str | pathlib.Path
            Path to the JSON file containing the visualization data.
        output_file : str | pathlib.Path | None
            Path to write the generated HTML file. If omitted a file with the
            same stem and ``.html`` extension is created in ``output_dir``.
        open_browser : bool
            If ``True`` the resulting HTML file is opened in the default
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

        html_str = self.generate_html(data)

        if output_file is None:
            output_file = self.output_dir / f"{vis_path.stem}.html"
        else:
            output_file = pathlib.Path(output_file)

        output_file.parent.mkdir(parents=True, exist_ok=True)
        with output_file.open("w", encoding="utf-8") as f:
            f.write(html_str)

        if open_browser:
            webbrowser.open_new_tab(output_file.as_uri())

        return output_file

    # --------------------------------------------------------------------- #
    #  Convenience for agent systems
    # --------------------------------------------------------------------- #
    def visualize_from_agent_system(
        self,
        agent_system: Any,
        problem_id: Optional[Any] = None,
    ) -> List[pathlib.Path]:
        """
        Generate visualizations for all visualization files associated with
        an agent system.

        Parameters
        ----------
        agent_system : object
            An object that provides access to visualization JSON files. It
            should expose either a ``visualization_files`` attribute (iterable
            of paths) or a ``get_visualization_files`` method that accepts an
            optional ``problem_id`` argument.
        problem_id : Any, optional
            If the agent system supports filtering by problem ID, this value
            is passed to the ``get_visualization_files`` method.

        Returns
        -------
        list[pathlib.Path]
            Paths to the generated HTML files.
        """
        # Determine the list of JSON files
        if hasattr(agent_system, "get_visualization_files"):
            vis_files = agent_system.get_visualization_files(
                problem_id=problem_id)
        elif hasattr(agent_system, "visualization_files"):
            vis_files = agent_system.visualization_files
        else:
            raise AttributeError(
                "agent_system must provide 'visualization_files' or "
                "'get_visualization_files(problem_id)'"
            )

        if not isinstance(vis_files, Iterable):
            raise TypeError(
                "visualization_files must be an iterable of file paths")

        generated_files: List[pathlib.Path] = []
        for vis_file
