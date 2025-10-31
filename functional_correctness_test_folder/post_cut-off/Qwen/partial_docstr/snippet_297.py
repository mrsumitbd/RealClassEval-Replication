
import os
import json
import webbrowser
from jinja2 import Environment, FileSystemLoader


class MASVisualizer:
    '''Utility for visualizing Multi-Agent System interactions'''

    def __init__(self, output_dir=None):
        self.output_dir = output_dir or 'visualizations'
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        self.env = Environment(
            loader=FileSystemLoader(os.path.dirname(__file__)))

    def generate_html(self, visualization_data, title=None):
        template = self.env.get_template('template.html')
        html_content = template.render(
            data=visualization_data, title=title or 'MAS Visualization')
        return html_content

    def visualize(self, visualization_file, output_file=None, open_browser=True):
        with open(visualization_file, 'r') as file:
            visualization_data = json.load(file)
        html_content = self.generate_html(visualization_data)
        output_file = output_file or os.path.join(
            self.output_dir, 'visualization.html')
        with open(output_file, 'w') as file:
            file.write(html_content)
        if open_browser:
            webbrowser.open(f'file://{os.path.abspath(output_file)}')
        return output_file

    def visualize_from_agent_system(self, agent_system, problem_id=None):
        visualization_files = agent_system.get_visualization_files(problem_id)
        html_files = []
        for vis_file in visualization_files:
            html_file = self.visualize(vis_file, output_file=os.path.join(
                self.output_dir, f'{os.path.basename(vis_file)}.html'), open_browser=False)
            html_files.append(html_file)
        return html_files
