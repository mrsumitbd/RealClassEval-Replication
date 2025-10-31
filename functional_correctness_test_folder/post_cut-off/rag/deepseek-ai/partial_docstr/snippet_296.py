
import json
import os
from pathlib import Path
import jinja2


class BenchmarkVisualizer:
    '''Utility for visualizing benchmark results and agent interactions across multiple problems'''

    def __init__(self, output_dir=None):
        '''
        Initialize the benchmark visualizer.
        Args:
            output_dir: Directory to save visualization HTML files
        '''
        self.output_dir = output_dir
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        # Set up Jinja2 environment for HTML templates
        self.template_env = jinja2.Environment(
            loader=jinja2.PackageLoader(__name__, 'templates'),
            autoescape=jinja2.select_autoescape(['html', 'xml'])
        )

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
        if title is None:
            title = "Benchmark Results Summary"

        if problem_visualizations is None:
            problem_visualizations = {}

        template = self.template_env.get_template('benchmark_summary.html')
        return template.render(
            title=title,
            summary=summary_data,
            results=results_data,
            visualizations=problem_visualizations
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
        with open(summary_file) as f:
            summary_data = json.load(f)

        results_data = []
        if results_file:
            with open(results_file) as f:
                results_data = json.load(f)

        problem_visualizations = {}
        if visualizations_dir:
            visualizations_dir = Path(visualizations_dir)
            for viz_file in visualizations_dir.glob('*.html'):
                problem_id = viz_file.stem
                problem_visualizations[problem_id] = str(
                    viz_file.relative_to(visualizations_dir))

        html_content = self.generate_summary_html(
            summary_data,
            results_data,
            problem_visualizations,
            title=f"Benchmark Results: {summary_data.get('benchmark_name', '')}"
        )

        if output_file is None:
            if self.output_dir:
                output_file = os.path.join(
                    self.output_dir, 'benchmark_summary.html')
            else:
                output_file = 'benchmark_summary.html'

        with open(output_file, 'w') as f:
            f.write(html_content)

        return output_file
