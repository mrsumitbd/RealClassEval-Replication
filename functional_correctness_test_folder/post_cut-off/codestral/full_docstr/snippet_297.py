
import json
import os
import webbrowser
from datetime import datetime


class MASVisualizer:
    '''Utility for visualizing Multi-Agent System interactions'''

    def __init__(self, output_dir=None):
        '''
        Initialize the MAS visualizer.
        Args:
            output_dir: Directory to save visualization HTML files
        '''
        self.output_dir = output_dir if output_dir else 'visualizations'
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
        nodes = visualization_data.get('nodes', [])
        links = visualization_data.get('links', [])

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{title if title else 'MAS Visualization'}</title>
            <script src="https://d3js.org/d3.v7.min.js"></script>
            <style>
                .node {{
                    stroke: #fff;
                    stroke-width: 1.5px;
                }}

                .link {{
                    stroke: #999;
                    stroke-opacity: 0.6;
                }}
            </style>
        </head>
        <body>
            <h1>{title if title else 'MAS Visualization'}</h1>
            <svg width="800" height="600"></svg>
            <script>
                const nodes = {json.dumps(nodes)};
                const links = {json.dumps(links)};

                const svg = d3.select("svg");

                const link = svg.append("g")
                    .selectAll("line")
                    .data(links)
                    .join("line")
                    .attr("class", "link")
                    .attr("stroke-width", d => Math.sqrt(d.value));

                const node = svg.append("g")
                    .selectAll("circle")
                    .data(nodes)
                    .join("circle")
                    .attr("class", "node")
                    .attr("r", 5)
                    .attr("fill", d => d.color);

                const simulation = d3.forceSimulation(nodes)
                    .force("link", d3.forceLink(links).id(d => d.id))
                    .force("charge", d3.forceManyBody().strength(-100))
                    .force("center", d3.forceCenter(400, 300));

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
        with open(visualization_file, 'r') as f:
            visualization_data = json.load(f)

        title = os.path.splitext(os.path.basename(visualization_file))[0]
        html = self.generate_html(visualization_data, title)

        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            output_file = os.path.join(
                self.output_dir, f"visualization_{timestamp}.html")

        with open(output_file, 'w') as f:
            f.write(html)

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

        for visualization_file in visualization_files:
            html_file = self.visualize(visualization_file)
            html_files.append(html_file)

        return html_files
