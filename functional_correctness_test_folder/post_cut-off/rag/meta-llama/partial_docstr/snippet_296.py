
import json
import os
from jinja2 import Template
from workbench.utils.file_utils import read_json_file


class BenchmarkVisualizer:
    """Utility for visualizing benchmark results and agent interactions across multiple problems"""

    def __init__(self, output_dir=None):
        """
        Initialize the benchmark visualizer.

        Args:
            output_dir: Directory to save visualization HTML files
        """
        self.output_dir = output_dir
        self.template_dir = os.path.join(
            os.path.dirname(__file__), 'templates')
        with open(os.path.join(self.template_dir, 'benchmark_summary.html.j2'), 'r') as f:
            self.template = Template(f.read())

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
        if problem_visualizations is None:
            problem_visualizations = {}
        if title is None:
            title = 'Benchmark Summary'
        return self.template.render(summary_data=summary_data, results_data=results_data, problem_visualizations=problem_visualizations, title=title)

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
        summary_data = read_json_file(summary_file)
        if results_file:
            results_data = read_json_file(results_file)
        else:
            results_data = []
        if visualizations_dir:
            problem_visualizations = {os.path.splitext(f)[0]: os.path.join(
                visualizations_dir, f) for f in os.listdir(visualizations_dir) if f.endswith('.html')}
        else:
            problem_visualizations = {}
        html = self.generate_summary_html(
            summary_data, results_data, problem_visualizations)
        if output_file is None:
            if self.output_dir is None:
                raise ValueError(
                    'Either output_file or output_dir must be specified')
            output_file = os.path.join(
                self.output_dir, 'benchmark_summary.html')
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w') as f:
            f.write(html)
        return output_file
