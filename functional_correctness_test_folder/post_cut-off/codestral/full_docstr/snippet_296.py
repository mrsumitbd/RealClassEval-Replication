
import json
import os
from jinja2 import Environment, FileSystemLoader


class BenchmarkVisualizer:
    '''Utility for visualizing benchmark results and agent interactions across multiple problems'''

    def __init__(self, output_dir=None):
        '''
        Initialize the benchmark visualizer.
        Args:
            output_dir: Directory to save visualization HTML files
        '''
        self.output_dir = output_dir
        if self.output_dir and not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        self.env = Environment(loader=FileSystemLoader(
            os.path.join(os.path.dirname(__file__), 'templates')))

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
        template = self.env.get_template('summary_template.html')
        return template.render(
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

        results_data = []
        if results_file:
            with open(results_file, 'r') as f:
                results_data = json.load(f)

        problem_visualizations = {}
        if visualizations_dir:
            for filename in os.listdir(visualizations_dir):
                if filename.endswith('.html'):
                    problem_id = os.path.splitext(filename)[0]
                    problem_visualizations[problem_id] = os.path.join(
                        visualizations_dir, filename)

        html_content = self.generate_summary_html(
            summary_data, results_data, problem_visualizations)

        if not output_file:
            if self.output_dir:
                output_file = os.path.join(
                    self.output_dir, 'benchmark_summary.html')
            else:
                output_file = 'benchmark_summary.html'

        with open(output_file, 'w') as f:
            f.write(html_content)

        return output_file
