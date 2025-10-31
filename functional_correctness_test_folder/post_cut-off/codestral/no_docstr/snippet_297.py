
import os
import webbrowser
from jinja2 import Environment, FileSystemLoader


class MASVisualizer:

    def __init__(self, output_dir=None):
        self.output_dir = output_dir if output_dir else os.getcwd()
        self.env = Environment(loader=FileSystemLoader(
            os.path.join(os.path.dirname(__file__), 'templates')))

    def generate_html(self, visualization_data, title=None):
        template = self.env.get_template('visualization_template.html')
        html_content = template.render(data=visualization_data, title=title)
        return html_content

    def visualize(self, visualization_file, output_file=None, open_browser=True):
        if not output_file:
            output_file = os.path.join(self.output_dir, 'visualization.html')

        with open(output_file, 'w') as f:
            f.write(visualization_file)

        if open_browser:
            webbrowser.open('file://' + os.path.realpath(output_file))

    def visualize_from_agent_system(self, agent_system, problem_id=None):
        visualization_data = agent_system.get_visualization_data(problem_id)
        html_content = self.generate_html(
            visualization_data, title=f"Agent System Visualization - Problem {problem_id}")
        self.visualize(html_content)
