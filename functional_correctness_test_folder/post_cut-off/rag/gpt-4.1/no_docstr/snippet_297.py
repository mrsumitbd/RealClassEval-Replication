import os
import json
import tempfile
import webbrowser


class MASVisualizer:
    '''Utility for visualizing Multi-Agent System interactions'''

    def __init__(self, output_dir=None):
        '''
        Initialize the MAS visualizer.
        Args:
            output_dir: Directory to save visualization HTML files
        '''
        self.output_dir = output_dir or tempfile.gettempdir()
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
        nodes = visualization_data.get("nodes", [])
        links = visualization_data.get("links", [])
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{title or "Multi-Agent System Visualization"}</title>
  <style>
    body {{ font-family: Arial, sans-serif; background: #f8f8f8; }}
    .link {{ stroke: #999; stroke-opacity: 0.6; }}
    .node circle {{ stroke: #fff; stroke-width: 1.5px; }}
    .node text {{ pointer-events: none; font-size: 12px; }}
    .tooltip {{
      position: absolute;
      text-align: left;
      padding: 8px;
      font: 12px sans-serif;
      background: #fff;
      border: 1px solid #aaa;
      border-radius: 4px;
      pointer-events: none;
      box-shadow: 2px 2px 8px #aaa;
      z-index: 10;
    }}
  </style>
</head>
<body>
  <h2>{title or "Multi-Agent System Visualization"}</h2>
  <svg width="900" height="600"></svg>
  <script src="https://d3js.org/d3.v7.min.js"></script>
  <script>
    const graph = {json.dumps({"nodes": nodes, "links": links})};

    const svg = d3.select("svg"),
          width = +svg.attr("width"),
          height = +svg.attr("height");

    const color = d3.scaleOrdinal(d3.schemeCategory10);

    const simulation = d3.forceSimulation(graph.nodes)
        .force("link", d3.forceLink(graph.links).id(d => d.id).distance(120))
        .force("charge", d3.forceManyBody().strength(-400))
        .force("center", d3.forceCenter(width / 2, height / 2));

    const link = svg.append("g")
        .attr("stroke", "#999")
        .attr("stroke-opacity", 0.6)
      .selectAll("line")
      .data(graph.links)
      .join("line")
        .attr("stroke-width", d => Math.sqrt(d.value || 1));

    const node = svg.append("g")
        .attr("stroke", "#fff")
        .attr("stroke-width", 1.5)
      .selectAll("g")
      .data(graph.nodes)
      .join("g")
        .call(drag(simulation));

    node.append("circle")
        .attr("r", 18)
        .attr("fill", d => color(d.group || 0));

    node.append("text")
        .attr("x", 0)
        .attr("y", 5)
        .attr("text-anchor", "middle")
        .text(d => d.label || d.id);

    // Tooltip
    const tooltip = d3.select("body").append("div")
        .attr("class", "tooltip")
        .style("opacity", 0);

    node.on("mouseover", function(event, d) {{
        tooltip.transition().duration(200).style("opacity", .95);
        tooltip.html("<b>" + (d.label || d.id) + "</b><br/>" + (d.info || ""))
            .style("left", (event.pageX + 10) + "px")
            .style("top", (event.pageY - 28) + "px");
    }})
    .on("mouseout", function() {{
        tooltip.transition().duration(300).style("opacity", 0);
    }});

    simulation.on("tick", () => {{
      link
          .attr("x1", d => d.source.x)
          .attr("y1", d => d.source.y)
          .attr("x2", d => d.target.x)
          .attr("y2", d => d.target.y);

      node
          .attr("transform", d => `translate(${{d.x}},${{d.y}})`);
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
        with open(visualization_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        title = data.get("title", None)
        html = self.generate_html(data, title=title)
        if output_file is None:
            base = os.path.splitext(os.path.basename(visualization_file))[0]
            output_file = os.path.join(
                self.output_dir, f"{base}_visualization.html")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html)
        if open_browser:
            webbrowser.open(f"file://{os.path.abspath(output_file)}")
        return output_file

    def visualize_from_agent_system(self, agent_system, problem_id=None):
        '''
        Generate visualizations for all visualization files from an agent system.
        Args:
            agent_system: AgentSystem instance
            problem_id: Optional problem ID to filter by
        Returns:
            List of paths to generated HTML files
        '''
        visualization_files = []
        if hasattr(agent_system, "get_visualization_files"):
            files = agent_system.get_visualization_files(problem_id=problem_id)
        elif hasattr(agent_system, "visualization_files"):
            files = agent_system.visualization_files
            if problem_id is not None:
                files = [f for f in files if problem_id in os.path.basename(f)]
        else:
            raise ValueError(
                "Agent system does not provide visualization files.")
        output_files = []
        for vis_file in files:
            output_file = self.visualize(vis_file, open_browser=False)
            output_files.append(output_file)
        return output_files
