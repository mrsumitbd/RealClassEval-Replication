import os
import json
import datetime
from pathlib import Path


class BenchmarkVisualizer:
    '''Utility for visualizing benchmark results and agent interactions across multiple problems'''

    def __init__(self, output_dir=None):
        '''
        Initialize the benchmark visualizer.
        Args:
            output_dir: Directory to save visualization HTML files
        '''
        self.output_dir = output_dir or os.getcwd()
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

        html = []
        html.append('<!DOCTYPE html>')
        html.append('<html lang="en">')
        html.append('<head>')
        html.append('<meta charset="UTF-8">')
        html.append(
            '<meta name="viewport" content="width=device-width, initial-scale=1.0">')
        html.append(f'<title>{title or "Benchmark Summary"}</title>')
        html.append('''
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f9f9f9; }
            h1 { color: #333; }
            table { border-collapse: collapse; width: 100%; margin-bottom: 30px; }
            th, td { border: 1px solid #bbb; padding: 8px 12px; text-align: left; }
            th { background: #eee; }
            tr:nth-child(even) { background: #f5f5f5; }
            a { color: #1a0dab; text-decoration: none; }
            a:hover { text-decoration: underline; }
            .summary-table { width: 60%; margin-bottom: 40px; }
        </style>
        ''')
        html.append('</head>')
        html.append('<body>')
        html.append(f'<h1>{title or "Benchmark Summary"}</h1>')

        # Summary Table
        html.append('<h2>Benchmark Info</h2>')
        html.append('<table class="summary-table">')
        for k, v in summary_data.items():
            if isinstance(v, (dict, list)):
                continue
            html.append(f'<tr><th>{k}</th><td>{v}</td></tr>')
        html.append('</table>')

        # Aggregate stats if present
        if 'aggregate' in summary_data and isinstance(summary_data['aggregate'], dict):
            html.append('<h2>Aggregate Results</h2>')
            html.append('<table class="summary-table">')
            for k, v in summary_data['aggregate'].items():
                html.append(f'<tr><th>{k}</th><td>{v}</td></tr>')
            html.append('</table>')

        # Results Table
        html.append('<h2>Problem Results</h2>')
        html.append('<table>')
        # Table header
        if results_data and isinstance(results_data, list):
            first_row = results_data[0]
            columns = list(first_row.keys())
            if 'problem_id' not in columns:
                columns.insert(0, 'problem_id')
            html.append('<tr>')
            for col in columns:
                html.append(f'<th>{col}</th>')
            html.append('<th>Visualization</th>')
            html.append('</tr>')
            # Table rows
            for row in results_data:
                html.append('<tr>')
                for col in columns:
                    val = row.get(col, '')
                    html.append(f'<td>{val}</td>')
                problem_id = row.get('problem_id', None)
                vis_link = ''
                if problem_id and problem_id in problem_visualizations:
                    vis_path = problem_visualizations[problem_id]
                    vis_link = f'<a href="{vis_path}" target="_blank">View</a>'
                html.append(f'<td>{vis_link}</td>')
                html.append('</tr>')
        html.append('</table>')

        html.append('<hr>')
        html.append(
            f'<div style="color:#888;font-size:12px;">Generated on {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</div>')
        html.append('</body></html>')
        return '\n'.join(html)

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
        # Load summary
        with open(summary_file, 'r', encoding='utf-8') as f:
            summary_data = json.load(f)

        # Load results
        if results_file:
            with open(results_file, 'r', encoding='utf-8') as f:
                results_data = json.load(f)
        else:
            # Try to get from summary_data
            results_data = summary_data.get('results', [])
            if not isinstance(results_data, list):
                results_data = []

        # Map problem_id to visualization file
        problem_visualizations = {}
        if visualizations_dir:
            vis_dir = Path(visualizations_dir)
            for row in results_data:
                problem_id = row.get('problem_id')
                if not problem_id:
                    continue
                # Try to find a file for this problem_id
                for ext in ['.html', '.htm']:
                    vis_file = vis_dir / f"{problem_id}{ext}"
                    if vis_file.exists():
                        problem_visualizations[problem_id] = os.path.relpath(str(
                            vis_file), start=os.path.dirname(output_file) if output_file else self.output_dir)
                        break

        # Title
        title = summary_data.get('benchmark_name') or summary_data.get(
            'name') or "Benchmark Summary"

        # Generate HTML
        html = self.generate_summary_html(
            summary_data, results_data, problem_visualizations, title=title)

        # Output file
        if output_file is None:
            base = os.path.splitext(os.path.basename(summary_file))[0]
            output_file = os.path.join(self.output_dir, f"{base}_summary.html")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
        return output_file
