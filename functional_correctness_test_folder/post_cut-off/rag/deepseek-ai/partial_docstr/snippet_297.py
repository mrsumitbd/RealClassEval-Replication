
import json
import os
import webbrowser
from pathlib import Path


class MASVisualizer:
    '''Utility for visualizing Multi-Agent System interactions'''

    def __init__(self, output_dir=None):
        '''
        Initialize the MAS visualizer.
        Args:
            output_dir: Directory to save visualization HTML files
        '''
        self.output_dir = output_dir if output_dir else os.getcwd()
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)

    def generate_html(self, visualization_data, title=None):
        '''
        Generate HTML for visualizing agent interactions using D3.js.
        Args:
            visualization_data: Dictionary with nodes and links data
            title: Optional title for the visualization
        Returns:
            HTML string
        '''
        nodes = visualization_data.get('nodes', [])
        links = visualization_data.get('links', [])
        title = title or 'Multi-Agent System Visualization'

        html_template = f"""
<!DOCTYPE html>
<html>
<head>
    <title>{title}</title>
    <script src="https://d3js.org/d3.v7.min.js"></script>
    <style>
        .node circle {{ fill: #999; stroke: #fff; stroke-width: 1.5px; }}
        .node text {{ font: 10px sans-serif; pointer-events: none; }}
        .link {{ stroke: #999; stroke-opacity: 0.6; }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    <div id="graph"></div>
    <script>
        const data = {{
            nodes: {json.dumps(nodes)},
            links: {json.dumps(links)}
        }};

        const width = 800, height = 600;

        const svg = d3.select("#graph").append("svg")
            .attr("width", width)
            .attr("height", height);

        const simulation = d3.forceSimulation(data.nodes)
            .force("link", d3.forceLink(data.links).id(d => d.id).distance(100))
            .force("charge", d3.forceManyBody().strength(-300))
            .force("center", d3.forceCenter(width / 2, height / 2));

        const link = svg.append("g")
            .selectAll("line")
            .data(data.links)
            .enter().append("line")
            .attr("class", "link");

        const node = svg.append("g")
            .selectAll("g")
            .data(data.nodes)
            .enter().append("g");

        node.append("circle")
            .attr("r", 10)
            .attr("fill", d => d.color || "#999");

        node.append("text")
            .attr("dy", -15)
            .text(d => d.id);

        simulation.on("tick", () => {{
            link
                .attr("x1", d => d.source.x)
                .attr("y1", d => d.source.y)
                .attr("x2", d => d.target.x)
                .attr("y2", d => d.target.y);

            node
                .attr("transform", d => `translate(${{d.x}},${{d.y}})`);
        }});
    </script>
</body>
</html>
"""
        return html_template

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
        with open(visualization_file, 'r') as f:
            visualization_data = json.load(f)

        title = Path(visualization_file).stem.replace('_', ' ').title()
        html_content = self.generate_html(visualization_data, title)

        if not output_file:
            output_file = os.path.join(
                self.output_dir, f"{Path(visualization_file).stem}.html")

        with open(output_file, 'w') as f:
            f.write(html_content)

        if open_browser:
            webbrowser.open(f'file://{os.path.abspath(output_file)}')

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
        visualization_files = agent_system.get_visualization_files(problem_id)
        output_files = []

        for vis_file in visualization_files:
            output_file = self.visualize(vis_file, open_browser=False)
            output_files.append(output_file)

        return output_files
