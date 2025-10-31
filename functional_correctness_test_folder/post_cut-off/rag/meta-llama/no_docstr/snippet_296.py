
import json
import os
from jinja2 import Template
from pathlib import Path


class BenchmarkVisualizer:
    """Utility for visualizing benchmark results and agent interactions across multiple problems"""

    def __init__(self, output_dir=None):
        """
        Initialize the benchmark visualizer.

        Args:
            output_dir: Directory to save visualization HTML files
        """
        self.output_dir = output_dir
        self.template_dir = Path(__file__).parent / 'templates'
        with open(self.template_dir / 'benchmark_summary.html.j2', 'r') as f:
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
        return self.template.render(
            title=title,
            summary_data=summary_data,
            results_data=results_data,
            problem_visualizations=problem_visualizations
        )

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
            for file in os.listdir(visualizations_dir):
                if file.endswith('.html'):
                    problem_id = file[:-5]
                    problem_visualizations[problem_id] = os.path.join(
                        visualizations_dir, file)
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
