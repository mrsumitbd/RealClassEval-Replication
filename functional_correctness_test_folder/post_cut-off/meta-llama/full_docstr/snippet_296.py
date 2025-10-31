
import json
import os
from jinja2 import Template


class BenchmarkVisualizer:
    '''Utility for visualizing benchmark results and agent interactions across multiple problems'''

    def __init__(self, output_dir=None):
        '''
        Initialize the benchmark visualizer.
        Args:
            output_dir: Directory to save visualization HTML files
        '''
        self.output_dir = output_dir
        self.template_dir = os.path.join(
            os.path.dirname(__file__), 'templates')
        with open(os.path.join(self.template_dir, 'benchmark_summary.html.j2'), 'r') as f:
            self.template = Template(f.read())

    def generate_summary_html(self, summary_data, results_data, problem_visualizations=None, title=None):
        '''
        Generate HTML for visualizing benchmark summary with links to problem visualizations.
        Args:
            summary_data: Dictionary with benchmark summary data
            results_data: List of problem results data
            problem_visualizations: Optional dictionary mapping problem_id to visualization file paths
            title: Optional title for the visualization
        Returns:
            HTML string
        '''
        return self.template.render(
            summary_data=summary_data,
            results_data=results_data,
            problem_visualizations=problem_visualizations,
            title=title
        )

    def visualize_benchmark(self, summary_file, results_file=None, visualizations_dir=None, output_file=None):
        '''
        Generate HTML visualization from benchmark summary file with links to problem visualizations.
        Args:
            summary_file: Path to the benchmark summary JSON file
            results_file: Optional path to the benchmark results JSON file
            visualizations_dir: Optional directory containing problem visualizations
            output_file: Optional path to save the HTML output
        Returns:
            Path to the generated HTML file
        '''
        with open(summary_file, 'r') as f:
            summary_data = json.load(f)

        if results_file:
            with open(results_file, 'r') as f:
                results_data = json.load(f)
        else:
            results_data = []

        problem_visualizations = None
        if visualizations_dir:
            problem_visualizations = {}
            for filename in os.listdir(visualizations_dir):
                if filename.endswith('.html'):
                    problem_id = os.path.splitext(filename)[0]
                    problem_visualizations[problem_id] = os.path.join(
                        visualizations_dir, filename)

        html = self.generate_summary_html(
            summary_data, results_data, problem_visualizations)

        if output_file is None:
            if self.output_dir is None:
                raise ValueError('Output directory must be specified')
            output_file = os.path.join(
                self.output_dir, 'benchmark_summary.html')

        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w') as f:
            f.write(html)

        return output_file
