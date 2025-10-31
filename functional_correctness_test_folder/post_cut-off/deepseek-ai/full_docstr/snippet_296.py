
import json
import os
from pathlib import Path


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
        if title is None:
            title = "Benchmark Results Summary"

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{title}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1 {{ color: #333; }}
                table {{ border-collapse: collapse; width: 100%; margin-bottom: 20px; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
                tr:nth-child(even) {{ background-color: #f9f9f9; }}
                a {{ color: #0066cc; text-decoration: none; }}
                a:hover {{ text-decoration: underline; }}
            </style>
        </head>
        <body>
            <h1>{title}</h1>
            <h2>Summary</h2>
            <table>
                <tr><th>Metric</th><th>Value</th></tr>
        """

        for key, value in summary_data.items():
            html += f"<tr><td>{key}</td><td>{value}</td></tr>"

        html += """
            </table>
            <h2>Problem Results</h2>
            <table>
                <tr>
                    <th>Problem ID</th>
                    <th>Status</th>
                    <th>Score</th>
                    <th>Details</th>
                </tr>
        """

        for result in results_data:
            problem_id = result.get('problem_id', 'N/A')
            status = result.get('status', 'N/A')
            score = result.get('score', 'N/A')
            details_link = ""

            if problem_visualizations and problem_id in problem_visualizations:
                details_link = f'<a href="{problem_visualizations[problem_id]}">View Details</a>'

            html += f"""
                <tr>
                    <td>{problem_id}</td>
                    <td>{status}</td>
                    <td>{score}</td>
                    <td>{details_link}</td>
                </tr>
            """

        html += """
            </table>
        </body>
        </html>
        """

        return html

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

        problem_visualizations = None
        if visualizations_dir:
            problem_visualizations = {}
            for file in os.listdir(visualizations_dir):
                if file.endswith('.html'):
                    problem_id = os.path.splitext(file)[0]
                    problem_visualizations[problem_id] = os.path.join(
                        visualizations_dir, file)

        html = self.generate_summary_html(
            summary_data, results_data, problem_visualizations)

        if output_file is None:
            if self.output_dir is None:
                output_file = "benchmark_summary.html"
            else:
                output_file = os.path.join(
                    self.output_dir, "benchmark_summary.html")

        with open(output_file, 'w') as f:
            f.write(html)

        return output_file
