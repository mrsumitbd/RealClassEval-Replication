
import os
import json
import base64
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

        # Set up Jinja2 environment for HTML templating
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
            title=title or 'Benchmark Summary'
        )

    def visualize_benchmark(self, summary_file, results_file=None, visualizations_dir=None, output_file=None):
        '''
        Generate and save benchmark visualization HTML files.
        Args:
            summary_file: Path to JSON file with benchmark summary data
            results_file: Optional path to JSON file with problem results data
            visualizations_dir: Optional directory containing problem visualization files
            output_file: Optional path to save the summary HTML file
        '''
        # Load summary data
        with open(summary_file, 'r') as f:
            summary_data = json.load(f)

        # Load results data if provided
        results_data = []
        if results_file:
            with open(results_file, 'r') as f:
                results_data = json.load(f)

        # Load problem visualizations if directory is provided
        problem_visualizations = {}
        if visualizations_dir:
            for filename in os.listdir(visualizations_dir):
                if filename.endswith('.html'):
                    problem_id = os.path.splitext(filename)[0]
                    problem_visualizations[problem_id] = os.path.join(
                        visualizations_dir, filename)

        # Generate summary HTML
        html_content = self.generate_summary_html(
            summary_data=summary_data,
            results_data=results_data,
            problem_visualizations=problem_visualizations
        )

        # Save HTML file if output directory is provided
        if self.output_dir:
            output_file = output_file or os.path.join(
                self.output_dir, 'benchmark_summary.html')
            with open(output_file, 'w') as f:
                f.write(html_content)

        return html_content
