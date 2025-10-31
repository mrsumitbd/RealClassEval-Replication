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
        problem_visualizations = problem_visualizations or {}
        title = title or "Benchmark Results"
        date_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Summary Table
        summary_rows = []
        for k, v in summary_data.items():
            summary_rows.append(
                f"<tr><th style='text-align:left'>{k}</th><td>{v}</td></tr>")
        summary_table = "<table border='1' style='border-collapse:collapse;margin-bottom:20px'>" + \
            "".join(summary_rows) + "</table>"

        # Results Table
        if results_data and isinstance(results_data, list):
            # Collect all keys for table header
            all_keys = set()
            for r in results_data:
                all_keys.update(r.keys())
            all_keys = sorted(all_keys)
            header = "".join([f"<th>{k}</th>" for k in all_keys])
            rows = []
            for r in results_data:
                row = []
                for k in all_keys:
                    val = r.get(k, "")
                    if k == "problem_id" and r.get("problem_id") in problem_visualizations:
                        vis_path = problem_visualizations[r["problem_id"]]
                        vis_link = f"<a href='{vis_path}' target='_blank'>{r['problem_id']}</a>"
                        row.append(f"<td>{vis_link}</td>")
                    else:
                        row.append(f"<td>{val}</td>")
                rows.append("<tr>" + "".join(row) + "</tr>")
            results_table = (
                "<table border='1' style='border-collapse:collapse'>"
                "<tr>" + header + "</tr>"
                + "".join(rows) +
                "</table>"
            )
        else:
            results_table = "<p>No results data available.</p>"

        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{title}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        h1 {{ margin-bottom: 0.2em; }}
        table {{ margin-bottom: 2em; }}
        th, td {{ padding: 0.4em 0.8em; }}
        th {{ background: #f0f0f0; }}
        tr:hover {{ background: #f9f9f9; }}
        a {{ color: #1a0dab; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    <div style="color: #888; font-size: 0.9em; margin-bottom: 1em;">Generated: {date_str}</div>
    <h2>Summary</h2>
    {summary_table}
    <h2>Problem Results</h2>
    {results_table}
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
        # Load summary
        with open(summary_file, "r", encoding="utf-8") as f:
            summary_data = json.load(f)

        # Load results
        if results_file:
            with open(results_file, "r", encoding="utf-8") as f:
                results_data = json.load(f)
        else:
            # Try to get from summary_data
            results_data = summary_data.get(
                "results") or summary_data.get("problems") or []

        # Map problem_id to visualization file
        problem_visualizations = {}
        if visualizations_dir:
            vis_dir = Path(visualizations_dir)
            for r in results_data:
                pid = r.get("problem_id")
                if not pid:
                    continue
                # Try to find a file for this problem
                for ext in [".html", ".htm"]:
                    vis_path = vis_dir / f"{pid}{ext}"
                    if vis_path.exists():
                        # Use relative path if output_file is in output_dir
                        problem_visualizations[pid] = os.path.relpath(
                            str(vis_path), os.path.dirname(output_file) if output_file else self.output_dir)
                        break

        # Title
        title = summary_data.get("benchmark_name") or summary_data.get(
            "name") or "Benchmark Results"

        # Generate HTML
        html = self.generate_summary_html(
            summary_data, results_data, problem_visualizations, title=title)

        # Output file
        if not output_file:
            base = os.path.splitext(os.path.basename(summary_file))[0]
            output_file = os.path.join(
                self.output_dir, f"{base}_visualization.html")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html)
        return output_file
