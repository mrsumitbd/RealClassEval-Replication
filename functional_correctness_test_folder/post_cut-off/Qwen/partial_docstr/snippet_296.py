
import os
import json
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
        self.env = Environment(
            loader=FileSystemLoader(os.path.dirname(__file__)))

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
            title=title or "Benchmark Summary",
            summary_data=summary_data,
            results_data=results_data,
            problem_visualizations=problem_visualizations or {}
        )

    def visualize_benchmark(self, summary_file, results_file=None, visualizations_dir=None, output_file=None):
        with open(summary_file, 'r') as f:
            summary_data = json.load(f)

        results_data = []
        if results_file:
            with open(results_file, 'r') as f:
                results_data = json.load(f)

        problem_visualizations = {}
        if visualizations_dir:
            for problem_id in summary_data.get('problem_ids', []):
                vis_file = os.path.join(
                    visualizations_dir, f"{problem_id}.html")
                if os.path.exists(vis_file):
                    problem_visualizations[problem_id] = vis_file

        html_content = self.generate_summary_html(
            summary_data, results_data, problem_visualizations)

        if output_file:
            with open(output_file, 'w') as f:
                f.write(html_content)
        else:
            print(html_content)
