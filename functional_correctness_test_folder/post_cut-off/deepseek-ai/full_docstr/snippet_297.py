
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
        self.output_dir = output_dir
        if output_dir is not None:
            os.makedirs(output_dir, exist_ok=True)

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

        html_template = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{title if title else 'MAS Visualization'}</title>
    <script src="https://d3js.org/d3.v7.min.js"></script>
    <style>
        .node circle {{
            stroke: #fff;
            stroke-width: 1.5px;
        }}
        .link {{
            stroke: #999;
            stroke-opacity: 0.6;
        }}
        text {{
            font-family: sans-serif;
            font-size: 10px;
        }}
    </style>
</head>
<body>
    <h1>{title if title else 'Multi-Agent System Visualization'}</h1>
    <svg width="800" height="600"></svg>
    <script>
        const data = {{
            nodes: {json.dumps(nodes)},
            links: {json.dumps(links)}
        }};

        const svg = d3.select("svg"),
              width = +svg.attr("width"),
              height = +svg.attr("height");

        const simulation = d3.forceSimulation(data.nodes)
            .force("link", d3.forceLink(data.links).id(d => d.id).distance(100))
            .force("charge", d3.forceManyBody().strength(-300))
            .force("center", d3.forceCenter(width / 2, height / 2));

        const link = svg.append("g")
            .attr("class", "links")
            .selectAll("line")
            .data(data.links)
            .enter().append("line")
            .attr("class", "link")
            .attr("stroke-width", d => Math.sqrt(d.value));

        const node = svg.append("g")
            .attr("class", "nodes")
            .selectAll("g")
            .data(data.nodes)
            .enter().append("g");

        node.append("circle")
            .attr("r", 10)
            .attr("fill", d => d.color || "#69b3a2");

        node.append("text")
            .text(d => d.id)
            .attr("x", 12)
            .attr("y", 3);

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

        html_content = self.generate_html(visualization_data)

        if output_file is None:
            if self.output_dir is not None:
                output_file = os.path.join(self.output_dir, Path(
                    visualization_file).stem + '.html')
            else:
                output_file = Path(visualization_file).stem + '.html'

        with open(output_file, 'w') as f:
            f.write(html_content)

        if open_browser:
            webbrowser.open('file://' + os.path.abspath(output_file))

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
        html_files = []
        for vis_file in agent_system.get_visualization_files(problem_id):
            output_file = os.path.join(self.output_dir, Path(
                vis_file).stem + '.html') if self.output_dir else None
            html_file = self.visualize(
                vis_file, output_file=output_file, open_browser=False)
            html_files.append(html_file)
        return html_files
