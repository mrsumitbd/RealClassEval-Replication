
import os
import webbrowser
import json
from datetime import datetime


class MASVisualizer:

    def __init__(self, output_dir=None):
        self.output_dir = output_dir if output_dir else os.path.join(
            os.getcwd(), 'mas_visualizations')
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def generate_html(self, visualization_data, title=None):
        if title is None:
            title = f'MAS Visualization {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
        html_content = '''
        <html>
            <head>
                <title>{title}</title>
                <style>
                    body {{ font-family: Arial, sans-serif; }}
                </style>
            </head>
            <body>
                <h1>{title}</h1>
                <div id="visualization"></div>
                <script src="https://cdn.jsdelivr.net/npm/vis-network@9.1.2/dist/vis-network.min.js"></script>
                <script>
                    var nodes = new vis.DataSet({nodes});
                    var edges = new vis.DataSet({edges});
                    var container = document.getElementById('visualization');
                    var data = {{ nodes: nodes, edges: edges }};
                    var options = {{}};
                    var network = new vis.Network(container, data, options);
                </script>
            </body>
        </html>
        '''.format(title=title, nodes=json.dumps(visualization_data['nodes']), edges=json.dumps(visualization_data['edges']))
        return html_content

    def visualize(self, visualization_file, output_file=None, open_browser=True):
        if not os.path.exists(visualization_file):
            raise FileNotFoundError(
                f'Visualization file {visualization_file} not found')
        with open(visualization_file, 'r') as f:
            visualization_data = json.load(f)
        if output_file is None:
            output_file = os.path.join(
                self.output_dir, f'visualization_{datetime.now().strftime("%Y%m%d%H%M%S")}.html')
        else:
            output_file = os.path.join(self.output_dir, output_file)
        html_content = self.generate_html(visualization_data)
        with open(output_file, 'w') as f:
            f.write(html_content)
        if open_browser:
            webbrowser.open('file://' + os.path.realpath(output_file))

    def visualize_from_agent_system(self, agent_system, problem_id=None):
        # Assuming agent_system has a method to generate visualization data
        visualization_data = agent_system.generate_visualization_data(
            problem_id)
        html_content = self.generate_html(visualization_data)
        output_file = os.path.join(self.output_dir, f'visualization_{problem_id}.html') if problem_id else os.path.join(
            self.output_dir, f'visualization_{datetime.now().strftime("%Y%m%d%H%M%S")}.html')
        with open(output_file, 'w') as f:
            f.write(html_content)
        webbrowser.open('file://' + os.path.realpath(output_file))
