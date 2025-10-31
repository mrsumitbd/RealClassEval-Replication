
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
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

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
            <title>{{ title }}</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                h1 { color: #333; }
                .summary { background-color: #f5f5f5; padding: 15px; border-radius: 5px; margin-bottom: 20px; }
                .results-table { width: 100%; border-collapse: collapse; }
                .results-table th, .results-table td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                .results-table tr:nth-child(even) { background-color: #f2f2f2; }
                .results-table th { background-color: #4CAF50; color: white; }
                .visualization-link { color: #0066cc; text-decoration: none; }
                .visualization-link:hover { text-decoration: underline; }
            </style>
        </head>
        <body>
            <h1>{{ title }}</h1>
            
            <div class="summary">
                <h2>Benchmark Summary</h2>
                <p><strong>Total Problems:</strong> {{ summary.total_problems }}</p>
                <p><strong>Solved:</strong> {{ summary.solved }}</p>
                <p><strong>Success Rate:</strong> {{ summary.success_rate }}%</p>
                <p><strong>Average Score:</strong> {{ summary.avg_score }}</p>
                <p><strong>Average Time:</strong> {{ summary.avg_time }}s</p>
            </div>
            
            <h2>Problem Results</h2>
            <table class="results-table">
                <thead>
                    <tr>
                        <th>Problem ID</th>
                        <th>Status</th>
                        <th>Score</th>
                        <th>Time (s)</th>
                        <th>Visualization</th>
                    </tr>
                </thead>
                <tbody>
                    {% for result in results %}
                    <tr>
                        <td>{{ result.problem_id }}</td>
                        <td>{{ result.status }}</td>
                        <td>{{ result.score }}</td>
                        <td>{{ result.time }}</td>
                        <td>
                            {% if visualizations and result.problem_id in visualizations %}
                                <a class="visualization-link" href="{{ visualizations[result.problem_id] }}">View</a>
                            {% else %}
                                N/A
                            {% endif %}
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </body>
        </html>
        """
        template = Template(template_str)
        return template.render(
            title=title or "Benchmark Results",
            summary=summary_data,
            results=results_data,
            visualizations=problem_visualizations or {}
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
                    problem_id = filename.split('.')[0]
                    problem_visualizations[problem_id] = os.path.join(
                        visualizations_dir, filename)

        html_content = self.generate_summary_html(
            summary_data,
            results_data,
            problem_visualizations,
            title=f"Benchmark Results: {os.path.basename(summary_file)}"
        )

        if not output_file:
            if self.output_dir:
                output_file = os.path.join(
                    self.output_dir, "benchmark_results.html")
            else:
                output_file = "benchmark_results.html"

        with open(output_file, 'w') as f:
            f.write(html_content)

        return output_file
