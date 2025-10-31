
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
        if output_dir is not None:
            os.makedirs(output_dir, exist_ok=True)

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
        template_str = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>{{ title }}</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                h1 { color: #333; }
                .summary { background-color: #f5f5f5; padding: 15px; border-radius: 5px; margin-bottom: 20px; }
                .results-table { width: 100%; border-collapse: collapse; margin-top: 20px; }
                .results-table th, .results-table td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                .results-table th { background-color: #f2f2f2; }
                .results-table tr:nth-child(even) { background-color: #f9f9f9; }
                .problem-link { color: #0066cc; text-decoration: none; }
                .problem-link:hover { text-decoration: underline; }
            </style>
        </head>
        <body>
            <h1>{{ title }}</h1>
            <div class="summary">
                <h2>Benchmark Summary</h2>
                <pre>{{ summary_json }}</pre>
            </div>
            <h2>Problem Results</h2>
            <table class="results-table">
                <thead>
                    <tr>
                        <th>Problem ID</th>
                        <th>Status</th>
                        <th>Score</th>
                        <th>Details</th>
                    </tr>
                </thead>
                <tbody>
                    {% for result in results_data %}
                    <tr>
                        <td>
                            {% if problem_visualizations and result.problem_id in problem_visualizations %}
                                <a class="problem-link" href="{{ problem_visualizations[result.problem_id] }}">{{ result.problem_id }}</a>
                            {% else %}
                                {{ result.problem_id }}
                            {% endif %}
                        </td>
                        <td>{{ result.status }}</td>
                        <td>{{ result.score }}</td>
                        <td>{{ result.details }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </body>
        </html>
        """
        template = jinja2.Template(template_str)
        summary_json = json.dumps(summary_data, indent=2)
        title = title or "Benchmark Results Visualization"
        return template.render(
            title=title,
            summary_json=summary_json,
            results_data=results_data,
            problem_visualizations=problem_visualizations or {}
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
            visualizations_dir = Path(visualizations_dir)
            for viz_file in visualizations_dir.glob('*.html'):
                problem_id = viz_file.stem
                problem_visualizations[problem_id] = str(
                    viz_file.relative_to(visualizations_dir))

        html_content = self.generate_summary_html(
            summary_data,
            results_data,
            problem_visualizations,
            title=f"Benchmark Results: {Path(summary_file).stem}"
        )

        if output_file is None:
            if self.output_dir is None:
                output_file = Path(summary_file).with_suffix('.html')
            else:
                output_file = Path(self.output_dir) / \
                    f"{Path(summary_file).stem}.html"

        with open(output_file, 'w') as f:
            f.write(html_content)

        return str(output_file)
