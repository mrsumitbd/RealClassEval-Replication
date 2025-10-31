
import os
import json
import datetime
from pathlib import Path
from html import escape


class BenchmarkVisualizer:
    '''Utility for visualizing benchmark results and agent interactions across multiple problems'''

    def __init__(self, output_dir=None):
        '''
        Initialize the benchmark visualizer.
        Args:
            output_dir: Directory to save visualization HTML files
        '''
        self.output_dir = output_dir
        if self.output_dir:
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
        html.append(
            f'<title>{escape(title) if title else "Benchmark Summary"}</title>')
        html.append('''
        <style>
        body { font-family: Arial, sans-serif; margin: 2em; }
        h1, h2 { color: #2c3e50; }
        table { border-collapse: collapse; width: 100%; margin-bottom: 2em; }
        th, td { border: 1px solid #ccc; padding: 8px; text-align: left; }
        th { background: #f4f4f4; }
        tr:nth-child(even) { background: #fafafa; }
        a { color: #2980b9; text-decoration: none; }
        a:hover { text-decoration: underline; }
        .summary-table { width: auto; margin-bottom: 2em; }
        </style>
        ''')
        html.append('</head>')
        html.append('<body>')

        # Title
        html.append(
            f'<h1>{escape(title) if title else "Benchmark Summary"}</h1>')

        # Summary Table
        html.append('<h2>Summary</h2>')
        html.append('<table class="summary-table">')
        for k, v in summary_data.items():
            html.append(
                f'<tr><th>{escape(str(k))}</th><td>{escape(str(v))}</td></tr>')
        html.append('</table>')

        # Results Table
        html.append('<h2>Problem Results</h2>')
        if results_data and isinstance(results_data, list) and len(results_data) > 0:
            # Collect all keys for table header
            all_keys = set()
            for res in results_data:
                all_keys.update(res.keys())
            all_keys = list(sorted(all_keys))
            html.append('<table>')
            html.append(
                '<tr>' + ''.join(f'<th>{escape(str(k))}</th>' for k in all_keys) + '<th>Visualization</th></tr>')
            for res in results_data:
                html.append('<tr>')
                for k in all_keys:
                    val = res.get(k, "")
                    html.append(f'<td>{escape(str(val))}</td>')
                # Visualization link
                problem_id = res.get('problem_id') or res.get(
                    'id') or res.get('name')
                vis_link = ''
                if problem_id and problem_id in problem_visualizations:
                    vis_path = problem_visualizations[problem_id]
                    vis_link = f'<a href="{escape(vis_path)}" target="_blank">View</a>'
                html.append(f'<td>{vis_link}</td>')
                html.append('</tr>')
            html.append('</table>')
        else:
            html.append('<p>No problem results available.</p>')

        # Footer
        html.append(
            f'<footer><small>Generated on {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</small></footer>')
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
        # Load summary data
        with open(summary_file, 'r', encoding='utf-8') as f:
            summary_data = json.load(f)

        # Load results data
        results_data = []
        if results_file:
            with open(results_file, 'r', encoding='utf-8') as f:
                results_data = json.load(f)
        else:
            # Try to get from summary_data
            if isinstance(summary_data, dict):
                for k in ['results', 'problems', 'problem_results']:
                    if k in summary_data and isinstance(summary_data[k], list):
                        results_data = summary_data[k]
                        break

        # Map problem_id to visualization file
        problem_visualizations = {}
        if visualizations_dir:
            vis_dir = Path(visualizations_dir)
            if vis_dir.exists() and vis_dir.is_dir():
                for file in vis_dir.iterdir():
                    if file.suffix.lower() in {'.html', '.htm'}:
                        # Try to extract problem_id from filename
                        problem_id = file.stem
                        problem_visualizations[problem_id] = str(
                            file.resolve())
                # Try to match by id in results_data
                for res in results_data:
                    pid = res.get('problem_id') or res.get(
                        'id') or res.get('name')
                    if pid and pid not in problem_visualizations:
                        # Try to find a file with this id
                        for ext in ['.html', '.htm']:
                            candidate = vis_dir / (str(pid) + ext)
                            if candidate.exists():
                                problem_visualizations[pid] = str(
                                    candidate.resolve())
                                break

        # Title
        title = summary_data.get('name') or summary_data.get(
            'title') or "Benchmark Summary"

        # Generate HTML
        html = self.generate_summary_html(
            summary_data=summary_data,
            results_data=results_data,
            problem_visualizations=problem_visualizations,
            title=title
        )

        # Determine output file path
        if output_file:
            out_path = Path(output_file)
        else:
            base = Path(summary_file).stem
            out_dir = Path(self.output_dir) if self.output_dir else Path('.')
            out_path = out_dir / f"{base}_visualization.html"

        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(html)

        return str(out_path.resolve())
