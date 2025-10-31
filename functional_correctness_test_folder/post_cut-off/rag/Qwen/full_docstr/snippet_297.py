
import json
import webbrowser
import os
from jinja2 import Template


class MASVisualizer:
    '''Utility for visualizing Multi-Agent System interactions'''

    def __init__(self, output_dir=None):
        '''
        Initialize the MAS visualizer.
        Args:
            output_dir: Directory to save visualization HTML files
        '''
        self.output_dir = output_dir or 'visualizations'
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def generate_html(self, visualization_data, title=None):
        '''
        Generate HTML for visualizing agent interactions using D3.js.
        Args:
            visualization_data: Dictionary with nodes and links data
            title: Optional title for the visualization
        Returns:
            HTML string
        '''
        template_str = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{{ title }}</title>
            <style>
                .node {
                    stroke: #fff;
                    stroke-width: 1.5px;
                }
                .link {
                    stroke: #999;
                    stroke-opacity: 0.6;
                }
            </style>
        </head>
        <body>
            <h1>{{ title }}</h1>
            <svg width="800" height="600"></svg>
            <script src="https://d3js.org/d3.v7.min.js"></script>
            <script>
                const data = {{ data | tojson }};
                const svg = d3.select("svg"),
                    width = +svg.attr("width"),
                    height = +svg.attr("height");

                const simulation = d3.forceSimulation(data.nodes)
                    .force("link", d3.forceLink(data.links).id(d => d.id))
                    .force("charge", d3.forceManyBody())
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
                    .selectAll("circle")
                    .data(data.nodes)
                    .enter().append("circle")
                    .attr("class", "node")
                    .attr("r", 5)
                    .attr("fill", d => d.color)
                    .call(d3.drag()
                        .on("start", dragstarted)
                        .on("drag", dragged)
                        .on("end", dragended));

                node.append("title")
                    .text(d => d.id);

                simulation
                    .on("tick", ticked);

                function ticked() {
                    link
                        .attr("x1", d => d.source.x)
                        .attr("y1", d => d.source.y)
                        .attr("x2", d => d.target.x)
                        .attr("y2", d => d.target.y);

                    node
                        .attr("cx", d => d.x)
                        .attr("cy", d => d.y);
                }

                function dragstarted(event, d) {
                    if (!event.active) simulation.alphaTarget(0.3).restart();
                    d.fx = d.x;
                    d.fy = d.y;
                }

                function dragged(event, d) {
                    d.fx = event.x;
                    d.fy = event.y;
                }

                function dragended(event, d) {
                    if (!event.active) simulation.alphaTarget(0);
                    d.fx = null;
                    d.fy = null;
                }
            </script>
        </body>
        </html>
        """
        template = Template(template_str)
        return template.render(title=title or "MAS Visualization", data=visualization_data)

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
        output_file = output_file or os.path.join(
            self.output_dir, 'visualization.html')
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
        visualization_files = agent_system.get_visualization_files(
            problem_id=problem_id)
        html_files = []
        for vis_file in visualization_files:
            html_file = self.visualize(vis_file, open_browser=False)
            html_files.append(html_file)
        return html_files
