
import json
import webbrowser
import os
from jinja2 import Template
from pathlib import Path


class MASVisualizer:
    """Utility for visualizing Multi-Agent System interactions"""

    def __init__(self, output_dir=None):
        """Initialize the MAS visualizer.

        Args:
            output_dir: Directory to save visualization HTML files
        """
        self.output_dir = output_dir or os.getcwd()
        os.makedirs(self.output_dir, exist_ok=True)
        self.template = self._load_template()

    def _load_template(self):
        """Load the HTML template for visualization"""
        template_path = Path(__file__).parent / \
            'mas_visualization_template.html'
        with open(template_path, 'r') as file:
            return Template(file.read())

    def generate_html(self, visualization_data, title=None):
        """Generate HTML for visualizing agent interactions using D3.js.

        Args:
            visualization_data: Dictionary with nodes and links data
            title: Optional title for the visualization
        Returns:
            HTML string
        """
        return self.template.render(data=visualization_data, title=title)

    def visualize(self, visualization_file, output_file=None, open_browser=True):
        """Generate an HTML visualization from a visualization data file and open in browser.

        Args:
            visualization_file: Path to the visualization data JSON file
            output_file: Optional path to save the HTML output
            open_browser: Whether to open the visualization in a browser (default: True)
        Returns:
            Path to the generated HTML file
        """
        with open(visualization_file, 'r') as file:
            visualization_data = json.load(file)

        if output_file is None:
            output_file = os.path.join(
                self.output_dir, f'{os.path.basename(visualization_file)}.html')

        title = os.path.basename(visualization_file)
        html = self.generate_html(visualization_data, title)

        with open(output_file, 'w') as file:
            file.write(html)

        if open_browser:
            webbrowser.open('file://' + os.path.realpath(output_file))

        return output_file

    def visualize_from_agent_system(self, agent_system, problem_id=None):
        """Generate visualizations for all visualization files from an agent system.

        Args:
            agent_system: AgentSystem instance
            problem_id: Optional problem ID to filter by
        Returns:
            List of paths to generated HTML files
        """
        visualization_files = agent_system.get_visualization_files(problem_id)
        return [self.visualize(file, open_browser=False) for file in visualization_files]
