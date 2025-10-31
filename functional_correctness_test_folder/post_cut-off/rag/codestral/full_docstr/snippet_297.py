
import json
import os
import webbrowser
from typing import Dict, List, Optional, Union


class MASVisualizer:
    '''Utility for visualizing Multi-Agent System interactions'''

    def __init__(self, output_dir: Optional[str] = None):
        '''
        Initialize the MAS visualizer.
        Args:
            output_dir: Directory to save visualization HTML files
        '''
        self.output_dir = output_dir or 'visualizations'
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_html(self, visualization_data: Dict, title: Optional[str] = None) -> str:
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
            <title>{title or 'MAS Visualization'}</title>
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
                .node-label {{
                    font-size: 10px;
                    pointer-events: none;
                }}
                .link-label {{
                    font-size: 8px;
                    pointer-events: none;
                }}
            </style>
        </head>
        <body>
            <div id="visualization" style="width: 100%; height: 100vh;"></div>
            <script>
                const nodes = {json.dumps(nodes)};
                const links = {json.dumps(links)};

                const width = window.innerWidth;
                const height = window.innerHeight;

                const svg = d3.select("#visualization")
                    .append("svg")
                    .attr("width", width)
                    .attr("height", height);

                const simulation = d3.forceSimulation(nodes)
                    .force("link", d3.forceLink(links).id(d => d.id).distance(100))
                    .force("charge", d3.forceManyBody().strength(-300))
                    .force("center", d3.forceCenter(width / 2, height / 2));

                const link = svg.append("g")
                    .selectAll("line")
                    .data(links)
                    .enter()
                    .append("line")
                    .attr("class", "link")
                    .attr("stroke-width", d => d.weight || 1);

                const linkLabel = svg.append("g")
                    .selectAll("text")
                    .data(links)
                    .enter()
                    .append("text")
                    .attr("class", "link-label")
                    .text(d => d.label || "");

                const node = svg.append("g")
                    .selectAll("circle")
                    .data(nodes)
                    .enter()
                    .append("circle")
                    .attr("class", "node")
                    .attr("r", d => d.size || 10)
                    .attr("fill", d => d.color || "#69b3a2")
                    .call(d3.drag()
                        .on("start", dragstarted)
                        .on("drag", dragged)
                        .on("end", dragended));

                const nodeLabel = svg.append("g")
                    .selectAll("text")
                    .data(nodes)
                    .enter()
                    .append("text")
                    .attr("class", "node-label")
                    .text(d => d.label || d.id)
                    .attr("dx", 12)
                    .attr("dy", 4);

                simulation.on("tick", () => {{
                    link
                        .attr("x1", d => d.source.x)
                        .attr("y1", d => d.source.y)
                        .attr("x2", d => d.target.x)
                        .attr("y2", d => d.target.y);

                    linkLabel
                        .attr("x", d => (d.source.x + d.target.x) / 2)
                        .attr("y", d => (d.source.y + d.target.y) / 2);

                    node
                        .attr("cx", d => d.x)
                        .attr("cy", d => d.y);

                    nodeLabel
                        .attr("x", d => d.x)
                        .attr("y", d => d.y);
                }});

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
            </script>
        </body>
        </html>
        """
        return html_template

    def visualize(self, visualization_file: str, output_file: Optional[str] = None, open_browser: bool = True) -> str:
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

        html_content = self.generate_html(visualization_data, title=os.path.splitext(
            os.path.basename(visualization_file))[0])

        if not output_file:
            base_name = os.path.splitext(
                os.path.basename(visualization_file))[0]
            output_file = os.path.join(self.output_dir, f"{base_name}.html")

        with open(output_file, 'w') as f:
            f.write(html_content)

        if open_browser:
            webbrowser.open(f'file://{os.path.abspath(output_file)}')

        return output_file

    def visualize_from_agent_system(self, agent_system, problem_id: Optional[str] = None) -> List[str]:
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
