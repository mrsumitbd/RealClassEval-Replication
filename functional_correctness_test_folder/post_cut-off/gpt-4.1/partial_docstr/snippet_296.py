
import os
import json
import html
from datetime import datetime


class BenchmarkVisualizer:
    '''Utility for visualizing benchmark results and agent interactions across multiple problems'''

    def __init__(self, output_dir=None):
        '''
        Initialize the benchmark visualizer.
        Args:
            output_dir: Directory to save visualization HTML files
        '''
        self.output_dir = output_dir
        if self.output_dir is not None:
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
        if problem_visualizations is None:
            problem_visualizations = {}

        html_parts = []
        html_parts.append("<!DOCTYPE html>")
        html_parts.append("<html lang='en'>")
        html_parts.append("<head>")
        html_parts.append("<meta charset='UTF-8'>")
        html_parts.append(
            "<meta name='viewport' content='width=device-width, initial-scale=1.0'>")
        html_parts.append(
            f"<title>{html.escape(title) if title else 'Benchmark Summary'}</title>")
        html_parts.append("""
        <style>
            body { font-family: Arial, sans-serif; margin: 2em; }
            table { border-collapse: collapse; width: 100%; margin-bottom: 2em; }
            th, td { border: 1px solid #ccc; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; }
            tr:hover { background-color: #f9f9f9; }
            .summary-table { width: auto; margin-bottom: 2em; }
            .title { font-size: 2em; margin-bottom: 0.5em; }
            .timestamp { color: #888; font-size: 0.9em; }
        </style>
        """)
        html_parts.append("</head>")
        html_parts.append("<body>")

        if title:
            html_parts.append(f"<div class='title'>{html.escape(title)}</div>")
        html_parts.append(
            f"<div class='timestamp'>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>")

        # Summary Table
        html_parts.append("<h2>Benchmark Summary</h2>")
        html_parts.append("<table class='summary-table'>")
        for k, v in summary_data.items():
            html_parts.append(
                f"<tr><th>{html.escape(str(k))}</th><td>{html.escape(str(v))}</td></tr>")
        html_parts.append("</table>")

        # Results Table
        html_parts.append("<h2>Problem Results</h2>")
        if results_data:
            # Collect all keys for table header
            all_keys = set()
            for result in results_data:
                all_keys.update(result.keys())
            all_keys = list(sorted(all_keys))
            if 'problem_id' in all_keys:
                all_keys.remove('problem_id')
                all_keys = ['problem_id'] + all_keys

            html_parts.append("<table>")
            # Header
            html_parts.append("<tr>")
            for key in all_keys:
                html_parts.append(f"<th>{html.escape(str(key))}</th>")
            if problem_visualizations:
                html_parts.append("<th>Visualization</th>")
            html_parts.append("</tr>")
            # Rows
            for result in results_data:
                html_parts.append("<tr>")
                for key in all_keys:
                    val = result.get(key, "")
                    html_parts.append(f"<td>{html.escape(str(val))}</td>")
                if problem_visualizations:
                    pid = result.get('problem_id')
                    vis_path = problem_visualizations.get(pid)
                    if vis_path:
                        html_parts.append(
                            f"<td><a href='{html.escape(vis_path)}' target='_blank'>View</a></td>")
                    else:
                        html_parts.append("<td></td>")
                html_parts.append("</tr>")
            html_parts.append("</table>")
        else:
            html_parts.append("<p>No problem results available.</p>")

        html_parts.append("</body></html>")
        return "\n".join(html_parts)

    def visualize_benchmark(self, summary_file, results_file=None, visualizations_dir=None, output_file=None):
        '''
        Visualize the benchmark by generating an HTML summary.
        Args:
            summary_file: Path to JSON file with summary_data
            results_file: Path to JSON file with results_data (list of dicts)
            visualizations_dir: Directory containing per-problem visualization HTML files (named by problem_id)
            output_file: Path to save the generated HTML file (if None, uses output_dir/benchmark_summary.html)
        '''
        # Load summary_data
        with open(summary_file, 'r', encoding='utf-8') as f:
            summary_data = json.load(f)

        # Load results_data
        results_data = []
        if results_file:
            with open(results_file, 'r', encoding='utf-8') as f:
                results_data = json.load(f)

        # Map problem_id to visualization file path
        problem_visualizations = {}
        if visualizations_dir and os.path.isdir(visualizations_dir):
            for fname in os.listdir(visualizations_dir):
                if fname.endswith('.html'):
                    problem_id = os.path.splitext(fname)[0]
                    rel_path = os.path.relpath(os.path.join(visualizations_dir, fname),
                                               os.path.dirname(output_file) if output_file else self.output_dir or '.')
                    problem_visualizations[problem_id] = rel_path

        # Title
        title = summary_data.get('benchmark_name', 'Benchmark Summary')

        # Generate HTML
        html_str = self.generate_summary_html(
            summary_data=summary_data,
            results_data=results_data,
            problem_visualizations=problem_visualizations if problem_visualizations else None,
            title=title
        )

        # Output file
        if output_file is None:
            if self.output_dir:
                output_file = os.path.join(
                    self.output_dir, 'benchmark_summary.html')
            else:
                output_file = 'benchmark_summary.html'

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_str)
