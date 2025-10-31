
import json
import os
import pathlib
import webbrowser
from typing import Dict, List, Optional, Union


class MASVisualizer:
    '''Utility for visualizing Multi-Agent System interactions'''

    def __init__(self, output_dir: Optional[Union[str, pathlib.Path]] = None):
        '''
        Initialize the MAS visualizer.
        Args:
            output_dir: Directory to save visualization HTML files
        '''
        self.output_dir = pathlib.Path(
            output_dir) if output_dir else pathlib.Path.cwd()
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_html(self, visualization_data: Dict, title: Optional[str] = None) -> str:
        '''
        Generate HTML for visualizing agent interactions using D3.js.
        Args:
            visualization_data: Dictionary with nodes and links data
            title: Optional title for the visualization
        Returns:
            HTML string
        '''
        title = title or "MAS Interaction Visualization"
        data_json = json.dumps(visualization_data)

        html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title}</title>
<script src="https://d3js.org/d3.v7.min.js"></script>
<style>
    body {{ margin:0; font-family:Arial, sans-serif; }}
    .link {{ stroke: #999; stroke-opacity: 0.6; }}
    .node {{ stroke: #fff; stroke-width: 1.5px; }}
</style>
</head>
<body>
<svg width="960" height="600"></svg>
<script>
const data = {data_json};

const svg = d3.select("svg"),
      width = +svg.attr("width"),
      height = +svg.attr("height");

const simulation = d3.forceSimulation(data.nodes)
    .force("link", d3.forceLink(data.links).id(d => d.id).distance(120))
    .force("charge", d3.forceManyBody().strength(-300))
    .force("center", d3.forceCenter(width / 2, height / 2));

const link = svg.append("g")
    .attr("stroke", "#999")
    .attr("stroke-opacity", 0.6)
  .selectAll("line")
  .data(data.links)
  .enter().append("line")
    .attr("stroke-width", d => Math.sqrt(d.value));

const node = svg.append("g")
    .attr("stroke", "#fff")
    .attr("stroke-width", 1.5)
  .selectAll("circle")
  .data(data.nodes)
  .enter().append("circle")
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
</html>"""
        return html_template

    def visualize(
        self,
        visualization_file: Union[str, pathlib.Path],
        output_file: Optional[Union[str, pathlib.Path]] = None,
        open_browser: bool = True,
    ) -> pathlib.Path:
        '''
        Generate an HTML visualization from a visualization data file and open in browser.
        Args:
            visualization_file: Path to the visualization data JSON file
            output_file: Optional path to save the HTML output
            open_browser: Whether to open the visualization in a browser (default: True)
        Returns:
            Path to the generated HTML file
        '''
        vis_path = pathlib.Path(visualization_file)
        if not vis_path.is_file():
            raise FileNotFoundError(
                f"Visualization data file not found: {vis_path}")

        with vis_path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        title = vis_path.stem
        html_content = self.generate_html(data, title=title)

        if output_file is None:
            output_file = self.output_dir / f"{vis_path.stem}.html"
        else:
            output_file = pathlib.Path(output_file)

        output_file.parent.mkdir(parents=True, exist_ok=True)
        with output_file.open("w", encoding="utf-8") as f:
            f.write(html_content)

        if open_browser:
            webbrowser.open_new_tab(output_file.as_uri())

        return output_file

    def visualize_from_agent_system(
        self,
        agent_system: object,
        problem_id: Optional[str] = None,
    ) -> List[pathlib.Path]:
        '''
        Generate visualizations for all visualization files from an agent system.
        Args:
            agent_system: AgentSystem instance
            problem_id: Optional problem ID to filter by
        Returns:
            List of paths to generated HTML files
        '''
        # Attempt to retrieve visualization files from the agent system.
        # The agent system is expected to provide a method or attribute that
        # returns a list of JSON file paths.  We support a few common patterns.
        vis_files = []

        # Pattern 1: attribute `visualization_files`
        if hasattr(agent_system, "visualization_files"):
            vis_files = list(agent_system.visualization_files)

        # Pattern 2: method `get_visualization_files`
        elif hasattr(agent_system, "get_visualization_files"):
            vis_files = list(
                agent_system.get_visualization_files(problem_id=problem_id))

        # Pattern 3: attribute `output_dir` containing JSON files
        elif hasattr(agent_system, "output_dir"):
            out_dir = pathlib.Path(agent_system.output_dir)
            if out_dir.is_dir():
                vis_files = list(out_dir.glob("*.json"))

        # If still empty, raise an informative error
        if not vis_files:
            raise AttributeError(
                "Could not find visualization files in the provided agent system. "
                "Expected one of: `visualization_files`, `get_visualization_files()`, "
                "or `output_dir` containing JSON files."
            )

        generated_files = []
        for vis_file in vis_files:
            try:
                out_path = self.visualize(vis_file, open_browser=False)
                generated_files.append(out_path)
            except Exception as e:
                # Log the error and continue with the next file
                print(f"Failed to generate visualization for {vis_file}: {e}")

        # Optionally open the first generated file in the browser
        if generated_files:
            webbrowser.open_new_tab(generated_files[0].as_uri())

        return generated_files
