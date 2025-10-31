
class MASVisualizer:
    '''Utility for visualizing Multi-Agent System interactions'''

    def __init__(self, output_dir=None):
        '''
        Initialize the MAS visualizer.
        Args:
            output_dir: Directory to save visualization HTML files
        '''
        self.output_dir = output_dir

    def generate_html(self, visualization_data, title=None):
        '''
        Generate HTML for visualizing agent interactions using D3.js.
        Args:
            visualization_data: Dictionary with nodes and links data
            title: Optional title for the visualization
        Returns:
            HTML string
        '''
        import json
        from jinja2 import Template

        template_str = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>{{ title }}</title>
            <script src="https://d3js.org/d3.v7.min.js"></script>
            <style>
                .node { stroke: #fff; stroke-width: 1.5px; }
                .link { stroke: #999; stroke-opacity: 0.6; }
            </style>
        </head>
        <body>
            <h1>{{ title }}</h1>
            <div id="graph"></div>
            <script>
                const data = {{ visualization_data|tojson }};
                const width = 960, height = 600;

                const svg = d3.select("#graph").append("svg")
                    .attr("width", width)
                    .attr("height", height);

                const simulation = d3.forceSimulation(data.nodes)
                    .force("link", d3.forceLink(data.links).id(d => d.id))
                    .force("charge", d3.forceManyBody().strength(-100))
                    .force("center", d3.forceCenter(width / 2, height / 2));

                const link = svg.append("g")
                    .selectAll("line")
                    .data(data.links)
                    .enter().append("line")
                    .attr("class", "link")
                    .attr("stroke-width", d => Math.sqrt(d.value));

                const node = svg.append("g")
                    .selectAll("circle")
                    .data(data.nodes)
                    .enter().append("circle")
                    .attr("class", "node")
                    .attr("r", 5)
                    .attr("fill", d => d.color || "#69b3a2");

                node.append("title")
                    .text(d => d.id);

                simulation.on("tick", () => {
                    link
                        .attr("x1", d => d.source.x)
                        .attr("y1", d => d.source.y)
                        .attr("x2", d => d.target.x)
                        .attr("y2", d => d.target.y);

                    node
                        .attr("cx", d => d.x)
                        .attr("cy", d => d.y);
                });
            </script>
        </body>
        </html>
        """
        template = Template(template_str)
        return template.render(title=title or "MAS Visualization", visualization_data=visualization_data)

    def visualize(self, visualization_file, output_file=None, open_browser=True):
        '''
        Generate an HTML visualization from a visualization data JSON file and open in browser.
        Args:
            visualization_file: Path to the visualization data JSON file
            output_file: Optional path to save the HTML output
            open_browser: Whether to open the visualization in a browser (default: True)
        Returns:
            Path to the generated HTML file
        '''
        import json
        import os
        import webbrowser

        with open(visualization_file, 'r') as f:
            visualization_data = json.load(f)

        html_content = self.generate_html(visualization_data)

        if output_file is None:
            if self.output_dir is not None:
                os.makedirs(self.output_dir, exist_ok=True)
                output_file = os.path.join(self.output_dir, os.path.basename(
                    visualization_file).replace('.json', '.html'))
            else:
                output_file = visualization_file.replace('.json', '.html')

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
        import os

        visualization_files = agent_system.get_visualization_files(problem_id)
        output_files = []

        for vis_file in visualization_files:
            output_file = os.path.join(self.output_dir, os.path.basename(
                vis_file).replace('.json', '.html')) if self.output_dir else None
            output_files.append(self.visualize(
                vis_file, output_file, open_browser=False))

        return output_files
