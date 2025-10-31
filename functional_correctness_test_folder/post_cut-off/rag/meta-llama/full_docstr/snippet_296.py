
import json
import os
from jinja2 import Environment, FileSystemLoader
import pandas as pd
from workbench.utils.path_utils import validate_and_create_directory


class BenchmarkVisualizer:
    """Utility for visualizing benchmark results and agent interactions across multiple problems"""

    def __init__(self, output_dir=None):
        """
        Initialize the benchmark visualizer.

        Args:
            output_dir: Directory to save visualization HTML files
        """
        self.output_dir = output_dir
        if output_dir:
            validate_and_create_directory(output_dir)
        self.template_env = Environment(loader=FileSystemLoader(
            os.path.join(os.path.dirname(__file__), 'templates')))

    def generate_summary_html(self, summary_data, results_data, problem_visualizations=None, title=None):
        """
        Generate HTML for visualizing benchmark summary with links to problem visualizations.

        Args:
            summary_data: Dictionary with benchmark summary data
            results_data: List of problem results data
            problem_visualizations: Optional dictionary mapping problem_id to visualization file paths
            title: Optional title for the visualization
        Returns:
            HTML string
        """
        summary_df = pd.DataFrame(summary_data)
        results_df = pd.DataFrame(results_data)
        template = self.template_env.get_template('benchmark_summary.html')
        html = template.render(summary_df=summary_df, results_df=results_df,
                               problem_visualizations=problem_visualizations, title=title)
        return html

    def visualize_benchmark(self, summary_file, results_file=None, visualizations_dir=None, output_file=None):
        """
        Generate HTML visualization from benchmark summary file with links to problem visualizations.

        Args:
            summary_file: Path to the benchmark summary JSON file
            results_file: Optional path to the benchmark results JSON file
            visualizations_dir: Optional directory containing problem visualizations
            output_file: Optional path to save the HTML output
        Returns:
            Path to the generated HTML file
        """
        with open(summary_file, 'r') as f:
            summary_data = json.load(f)
        if results_file:
            with open(results_file, 'r') as f:
                results_data = json.load(f)
        else:
            results_data = []
        problem_visualizations = {}
        if visualizations_dir:
            for filename in os.listdir(visualizations_dir):
                if filename.endswith('.html'):
                    problem_id = filename[:-5]
                    problem_visualizations[problem_id] = os.path.join(
                        visualizations_dir, filename)
        title = os.path.basename(summary_file).split('.')[0]
        html = self.generate_summary_html(
            summary_data, results_data, problem_visualizations, title)
        if output_file is None:
            if self.output_dir:
                output_file = os.path.join(self.output_dir, f'{title}.html')
            else:
                output_file = f'{title}.html'
        with open(output_file, 'w') as f:
            f.write(html)
        return output_file
