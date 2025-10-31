
import os
import json
import tempfile
import webbrowser
from datetime import datetime


class MASVisualizer:
    '''Utility for visualizing Multi-Agent System interactions'''

    D3_JS_CDN = "https://d3js.org/d3.v7.min.js"

    def __init__(self, output_dir=None):
        '''
        Initialize the MAS visualizer.
        Args:
            output_dir: Directory to save visualization HTML files
        '''
        if output_dir is None:
            output_dir = tempfile.gettempdir()
        self.output_dir = os.path.abspath(output_dir)
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
        nodes = json.dumps(visualization_data.get("nodes", []))
        links = json.dumps(visualization_data.get("links", []))
        html_title = title or "Multi-Agent System Visualization"
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>{html_title}</title>
    <script src="{self.D3_JS_CDN}"></script>
    <style>
        body {{ font-family: Arial, sans-serif; background: #f9f9f9; }}
        .link {{ stroke: #999; stroke-opacity: 0.6; }}
        .node circle {{ stroke: #fff; stroke-width: 1.5px; }}
        .node text {{ pointer-events: none; font-size: 12px; }}
        #graph {{ margin: 20px auto; display: block; background: #fff; border-radius: 8px; box-shadow: 0 2px 8px #ccc; }}
    </style>
</head>
<body>
    <h2 style="text-align:center;">{html_title}</h2>
    <svg id="graph" width="900" height="600"></svg>
    <script>
        const nodes = {nodes};
        const links = {links};

        const width = 900, height = 600;

        const svg = d3.select("#graph")
            .attr("width", width)
            .attr("height", height);

        const simulation = d3.forceSimulation(nodes)
            .force("link", d3.forceLink(links).id(d => d.id).distance(120))
            .force("charge", d3.forceManyBody().strength(-400))
            .force("center", d3.forceCenter(width / 2, height / 2));

        const link = svg.append("g")
            .attr("stroke", "#999")
            .attr("stroke-opacity", 0.6)
            .selectAll("line")
            .data(links)
            .join("line")
            .attr("stroke-width", d => Math.sqrt(d.value || 1));

        const node = svg.append("g")
            .attr("stroke", "#fff")
            .attr("stroke-width", 1.5)
            .selectAll("g")
            .data(nodes)
            .join("g")
            .call(drag(simulation));

        node.append("circle")
            .attr("r", 18)
            .attr("fill", d => d.color || "#1f77b4");

        node.append("text")
            .attr("x", 0)
            .attr("y", 5)
            .attr("text-anchor", "middle")
            .text(d => d.label || d.id);

        simulation.on("tick", () => {{
            link
                .attr("x1", d => d.source.x)
                .attr("y1", d => d.source.y)
                .attr("x2", d => d.target.x)
                .attr("y2", d => d.target.y);

            node.attr("transform", d => `translate(${{d.x}},${{d.y}})`);
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
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = os.path.join(
                self.output_dir, f"{base}_vis_{timestamp}.html")
        else:
            output_file = os.path.abspath(output_file)
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html)
        if open_browser:
            webbrowser.open(f"file://{output_file}")
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
        vis_files = []
        if hasattr(agent_system, "get_visualization_files"):
            files = agent_system.get_visualization_files(problem_id=problem_id)
        elif hasattr(agent_system, "visualization_files"):
            files = agent_system.visualization_files
            if problem_id is not None:
                files = [f for f in files if problem_id in os.path.basename(f)]
        else:
            raise AttributeError(
                "Agent system does not provide visualization files.")
        for vis_file in files:
            html_path = self.visualize(vis_file, open_browser=False)
            vis_files.append(html_path)
        return vis_files
