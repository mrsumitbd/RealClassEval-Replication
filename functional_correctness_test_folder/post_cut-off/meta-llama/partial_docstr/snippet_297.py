
import json
import os
import webbrowser
from jinja2 import Environment, FileSystemLoader
from pathlib import Path


class MASVisualizer:
    '''Utility for visualizing Multi-Agent System interactions'''

    def __init__(self, output_dir=None):
        self.output_dir = output_dir if output_dir else os.getcwd()
        self.template_env = Environment(
            loader=FileSystemLoader(Path(__file__).parent / 'templates'))
        self.template = self.template_env.get_template(
            'mas_visualization.html')

    def generate_html(self, visualization_data, title=None):
        html = self.template.render(
            visualization_data=visualization_data, title=title)
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
            output_file = os.path.splitext(visualization_file)[0] + '.html'

        output_file = os.path.join(
            self.output_dir, os.path.basename(output_file))

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
        visualization_files = agent_system.get_visualization_files(problem_id)
        html_files = []

        for visualization_file in visualization_files:
            html_file = self.visualize(visualization_file, open_browser=False)
            html_files.append(html_file)

        return html_files
