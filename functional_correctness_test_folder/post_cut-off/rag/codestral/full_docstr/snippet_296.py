
import json
import os
from datetime import datetime


class BenchmarkVisualizer:
    '''Utility for visualizing benchmark results and agent interactions across multiple problems'''

    def __init__(self, output_dir=None):
        '''
        Initialize the benchmark visualizer.
        Args:
            output_dir: Directory to save visualization HTML files
        '''
        self.output_dir = output_dir or 'benchmark_visualizations'
        os.makedirs(self.output_dir, exist_ok=True)

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
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{title or 'Benchmark Visualization'}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1 {{ color: #333; }}
                .summary {{ margin-bottom: 30px; }}
                .problem {{ margin-bottom: 20px; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }}
                .problem-title {{ font-weight: bold; margin-bottom: 5px; }}
                .problem-metrics {{ margin-left: 20px; }}
                .visualization-link {{ color: #0066cc; text-decoration: none; }}
                .visualization-link:hover {{ text-decoration: underline; }}
            </style>
        </head>
        <body>
            <h1>{title or 'Benchmark Visualization'}</h1>
            <div class="summary">
                <h2>Benchmark Summary</h2>
                <p>Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p>Total Problems: {len(results_data)}</p>
                <p>Average Score: {summary_data.get('average_score', 'N/A')}</p>
            </div>
            <div class="results">
                <h2>Problem Results</h2>
        """

        for problem in results_data:
            problem_id = problem.get('problem_id', 'unknown')
            html += f"""
                <div class="problem">
                    <div class="problem-title">Problem: {problem_id}</div>
                    <div class="problem-metrics">
                        <p>Score: {problem.get('score', 'N/A')}</p>
                        <p>Steps: {problem.get('steps', 'N/A')}</p>
                        <p>Time: {problem.get('time', 'N/A')} seconds</p>
            """

            if problem_visualizations and problem_id in problem_visualizations:
                html += f"""
                        <p>Visualization: <a href="{problem_visualizations[problem_id]}" class="visualization-link" target="_blank">View</a></p>
                """

            html += """
                    </div>
                </div>
            """

        html += """
            </div>
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

        problem_visualizations = {}
        if visualizations_dir:
            for filename in os.listdir(visualizations_dir):
                if filename.endswith('.html'):
                    problem_id = filename[:-5]  # Remove .html extension
                    problem_visualizations[problem_id] = os.path.join(
                        visualizations_dir, filename)

        html_content = self.generate_summary_html(
            summary_data=summary_data,
            results_data=results_data,
            problem_visualizations=problem_visualizations,
            title='Benchmark Visualization'
        )

        output_path = output_file or os.path.join(
            self.output_dir, 'benchmark_visualization.html')
        with open(output_path, 'w') as f:
            f.write(html_content)

        return output_path
