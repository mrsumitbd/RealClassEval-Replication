
import json
import os
from datetime import datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from IPython.display import HTML, display


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
        title = title or f"Benchmark Summary - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

        # Create summary table
        summary_table = pd.DataFrame([summary_data]).T.reset_index()
        summary_table.columns = ['Metric', 'Value']

        # Create results table
        results_df = pd.DataFrame(results_data)
        if problem_visualizations:
            results_df['Visualization'] = results_df['problem_id'].apply(
                lambda x: f'<a href="{problem_visualizations.get(x, "")}" target="_blank">View</a>' if x in problem_visualizations else ''
            )

        # Create HTML
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
                .container {{ display: flex; flex-wrap: wrap; }}
                .summary {{ flex: 1; min-width: 300px; margin-right: 20px; }}
                .results {{ flex: 2; min-width: 500px; }}
            </style>
        </head>
        <body>
            <h1>{title}</h1>
            <div class="container">
                <div class="summary">
                    <h2>Benchmark Summary</h2>
                    {summary_table.to_html(index=False, escape=False)}
                </div>
                <div class="results">
                    <h2>Problem Results</h2>
                    {results_df.to_html(index=False, escape=False)}
                </div>
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
        # Load data
        with open(summary_file, 'r') as f:
            summary_data = json.load(f)

        results_data = []
        if results_file:
            with open(results_file, 'r') as f:
                results_data = json.load(f)

        # Get problem visualizations if directory is provided
        problem_visualizations = {}
        if visualizations_dir:
            for filename in os.listdir(visualizations_dir):
                if filename.endswith('.html'):
                    problem_id = filename.replace('.html', '')
                    problem_visualizations[problem_id] = os.path.join(
                        visualizations_dir, filename)

        # Generate HTML
        html = self.generate_summary_html(
            summary_data, results_data, problem_visualizations)

        # Save to file if output_file is provided
        if output_file:
            output_path = os.path.join(self.output_dir, output_file)
            with open(output_path, 'w') as f:
                f.write(html)
            return output_path

        # Display in notebook if no output_file provided
        display(HTML(html))
        return None
