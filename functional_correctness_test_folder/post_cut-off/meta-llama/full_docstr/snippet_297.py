
import json
import os
import webbrowser
from jinja2 import Template
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
        os.makedirs(self.output_dir, exist_ok=True)

        # Load the HTML template
        template_path = Path(__file__).parent / \
            'mas_visualization_template.html'
        if template_path.exists():
            with open(template_path, 'r') as f:
                self.template = Template(f.read())
        else:
            # Provide a default template if the file is not found
            default_template = '''
            <!DOCTYPE html>
            <html>
            <head>
                <title>{{ title }}</title>
                <script src="https://d3js.org/d3.v7.min.js"></script>
                <style>
                    /* Add some basic styling */
                    body {
                        font-family: Arial, sans-serif;
                    }
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
                <svg width="800" height="600"></svg>
                <script>
                    var nodes = {{ nodes | tojson }};
                    var links = {{ links | tojson }};
                    var svg = d3.select("svg");
                    var width = svg.attr("width");
                    var height = svg.attr("height");

                    var simulation = d3.forceSimulation()
                        .nodes(nodes)
                        .force("charge", d3.forceManyBody().strength(-100))
                        .force("link", d3.forceLink(links).id(function(d) { return d.id; }).distance(100))
                        .force("center", d3.forceCenter(width / 2, height / 2));

                    var link = svg.selectAll(".link")
                        .data(links)
                        .enter()
                        .append("line")
                        .attr("class", "link");

                    var node = svg.selectAll(".node")
                        .data(nodes)
                        .enter()
                        .append("circle")
                        .attr("class", "node")
                        .attr("r", 5);

                    simulation.on("tick", function() {
                        link.attr("x1", function(d) { return d.source.x; })
                            .attr("y1", function(d) { return d.source.y; })
                            .attr("x2", function(d) { return d.target.x; })
                            .attr("y2", function(d) { return d.target.y; });

                        node.attr("cx", function(d) { return d.x; })
                            .attr("cy", function(d) { return d.y; });
                    });
                </script>
            </body>
            </html>
            '''
            self.template = Template(default_template)

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

        html = self.template.render(title=title, nodes=nodes, links=links)
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
        with open(visualization_file, 'r') as f:
            visualization_data = json.load(f)

        html = self.generate_html(visualization_data)

        if output_file is None:
            output_file = os.path.join(self.output_dir, os.path.basename(
                visualization_file).split('.')[0] + '.html')

        with open(output_file, 'w') as f:
            f.write(html)

        if open_browser:
            webbrowser.open('file://' + os.path.realpath(output_file))

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
        for visualization_file in agent_system.get_visualization_files(problem_id):
            html_file = self.visualize(visualization_file, open_browser=False)
            html_files.append(html_file)

        return html_files
