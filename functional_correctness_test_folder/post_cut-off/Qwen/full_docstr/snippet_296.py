
import os
import json
from jinja2 import Template


class BenchmarkVisualizer:
    '''Utility for visualizing benchmark results and agent interactions across multiple problems'''

    def __init__(self, output_dir=None):
        '''
        Initialize the benchmark visualizer.
        Args:
            output_dir: Directory to save visualization HTML files
        '''
        self.output_dir = output_dir or 'visualizations'
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

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
        problem_visualizations = problem_visualizations or {}
        title = title or "Benchmark Summary"

        template_str = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{{ title }}</title>
            <style>
                body { font-family: Arial, sans-serif; }
                table { width: 100%; border-collapse: collapse; }
                th, td { border: 1px solid #ddd; padding: 8px; }
                th { background-color: #f2f2f2; }
                tr:hover { background-color: #f1f1f1; }
            </style>
        </head>
        <body>
            <h1>{{ title }}</h1>
            <h2>Summary</h2>
            <pre>{{ summary_data | tojson(indent=4) }}</pre>
            <h2>Results</h2>
            <table>
                <tr>
                    <th>Problem ID</th>
                    <th>Details</th>
                    <th>Visualization</th>
                </tr>
                {% for result in results_data %}
                <tr>
                    <td>{{ result.problem_id }}</td>
                    <td><pre>{{ result | tojson(indent=4) }}</pre></td>
                    <td>
                        {% if problem_visualizations[result.problem_id] %}
                        <a href="{{ problem_visualizations[result.problem_id] }}">View</a>
                        {% else %}
                        N/A
                        {% endif %}
                    </td>
                </tr>
                {% endfor %}
            </table>
        </body>
        </html>
        """
        template = Template(template_str)
        return template.render(summary_data=summary_data, results_data=results_data, problem_visualizations=problem_visualizations, title=title)

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
            for problem_id in [result.get('problem_id') for result in results_data]:
                visualization_file = os.path.join(
                    visualizations_dir, f"{problem_id}.html")
                if os.path.exists(visualization_file):
                    problem_visualizations[problem_id] = os.path.basename(
                        visualization_file)

        html_content = self.generate_summary_html(
            summary_data, results_data, problem_visualizations)

        output_file = output_file or os.path.join(
            self.output_dir, 'benchmark_summary.html')
        with open(output_file, 'w') as f:
            f.write(html_content)

        return output_file
