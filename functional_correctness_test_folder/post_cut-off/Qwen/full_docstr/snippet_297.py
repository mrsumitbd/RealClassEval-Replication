
import os
import json
import webbrowser
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
        <html>
        <head>
            <title>{{ title }}</title>
            <script src="https://d3js.org/d3.v6.min.js"></script>
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
            <script>
                var data = {{ data | tojson }};
                var width = 800;
                var height = 600;
                var svg = d3.select("body").append("svg")
                    .attr("width", width)
                    .attr("height", height);

                var simulation = d3.forceSimulation(data.nodes)
                    .force("link", d3.forceLink(data.links).id(function(d) { return d.id; }))
                    .force("charge", d3.forceManyBody())
                    .force("center", d3.forceCenter(width / 2, height / 2));

                var link = svg.append("g")
                    .attr("stroke", "#999")
                    .attr("stroke-opacity", 0.6)
                    .selectAll("line")
                    .data(data.links)
                    .enter().append("line")
                    .attr("stroke-width", function(d) { return Math.sqrt(d.value); });

                var node = svg.append("g")
                    .attr("stroke", "#fff")
                    .attr("stroke-width", 1.5)
                    .selectAll("circle")
                    .data(data.nodes)
                    .enter().append("circle")
                    .attr("r", 5)
                    .attr("fill", function(d) { return d.color; })
                    .call(d3.drag()
                        .on("start", dragstarted)
                        .on("drag", dragged)
                        .on("end", dragended));

                node.append("title")
                    .text(function(d) { return d.id; });

                simulation.on("tick", function() {
                    link
                        .attr("x1", function(d) { return d.source.x; })
                        .attr("y1", function(d) { return d.source.y; })
                        .attr("x2", function(d) { return d.target.x; })
                        .attr("y2", function(d) { return d.target.y; });

                    node
                        .attr("cx", function(d) { return d.x; })
                        .attr("cy", function(d) { return d.y; });
                });

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
        visualization_files = agent_system.get_visualization_files(problem_id)
        html_files = []
        for vis_file in visualization_files:
            html_file = self.visualize(vis_file, open_browser=False)
            html_files.append(html_file)
        return html_files
