
import os
import json
import shutil
from datetime import datetime
from pathlib import Path


class BenchmarkVisualizer:

    def __init__(self, output_dir=None):
        if output_dir is not None:
            self.output_dir = Path(output_dir)
            self.output_dir.mkdir(parents=True, exist_ok=True)
        else:
            self.output_dir = None

    def generate_summary_html(self, summary_data, results_data, problem_visualizations=None, title=None):
        html = []
        html.append("<!DOCTYPE html>")
        html.append("<html lang='en'>")
        html.append("<head>")
        html.append("<meta charset='UTF-8'>")
        html.append(
            "<meta name='viewport' content='width=device-width, initial-scale=1.0'>")
        html.append(f"<title>{title or 'Benchmark Summary'}</title>")
        html.append("""
        <style>
        body { font-family: Arial, sans-serif; margin: 2em; }
        h1, h2, h3 { color: #333; }
        table { border-collapse: collapse; width: 100%; margin-bottom: 2em; }
        th, td { border: 1px solid #ccc; padding: 8px; text-align: left; }
        th { background: #f0f0f0; }
        .visualization { margin-bottom: 2em; }
        </style>
        """)
        html.append("</head>")
        html.append("<body>")
        html.append(f"<h1>{title or 'Benchmark Summary'}</h1>")

        # Summary Table
        html.append("<h2>Summary</h2>")
        html.append("<table>")
        html.append("<tbody>")
        for k, v in summary_data.items():
            html.append(f"<tr><th>{k}</th><td>{v}</td></tr>")
        html.append("</tbody>")
        html.append("</table>")

        # Results Table
        if results_data:
            html.append("<h2>Results</h2>")
            html.append("<table>")
            # Header
            if isinstance(results_data, list) and results_data:
                header = results_data[0].keys()
                html.append("<thead><tr>")
                for h in header:
                    html.append(f"<th>{h}</th>")
                html.append("</tr></thead>")
                html.append("<tbody>")
                for row in results_data:
                    html.append("<tr>")
                    for h in header:
                        html.append(f"<td>{row.get(h, '')}</td>")
                    html.append("</tr>")
                html.append("</tbody>")
            elif isinstance(results_data, dict):
                html.append("<tbody>")
                for k, v in results_data.items():
                    html.append(f"<tr><th>{k}</th><td>{v}</td></tr>")
                html.append("</tbody>")
            html.append("</table>")

        # Problem Visualizations
        if problem_visualizations:
            html.append("<h2>Problem Visualizations</h2>")
            for problem, vis_path in problem_visualizations.items():
                html.append(f"<div class='visualization'><h3>{problem}</h3>")
                ext = os.path.splitext(vis_path)[1].lower()
                if ext in ['.png', '.jpg', '.jpeg', '.gif', '.svg']:
                    html.append(
                        f"<img src='{vis_path}' alt='{problem}' style='max-width:100%;'>")
                elif ext in ['.html', '.htm']:
                    html.append(
                        f"<iframe src='{vis_path}' width='100%' height='400'></iframe>")
                else:
                    html.append(f"<a href='{vis_path}'>{vis_path}</a>")
                html.append("</div>")

        html.append(
            f"<footer><small>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</small></footer>")
        html.append("</body></html>")
        return "\n".join(html)

    def visualize_benchmark(self, summary_file, results_file=None, visualizations_dir=None, output_file=None):
        # Load summary
        with open(summary_file, "r", encoding="utf-8") as f:
            summary_data = json.load(f)

        # Load results
        results_data = None
        if results_file:
            with open(results_file, "r", encoding="utf-8") as f:
                results_data = json.load(f)

        # Collect visualizations
        problem_visualizations = None
        if visualizations_dir:
            vis_dir = Path(visualizations_dir)
            if vis_dir.exists() and vis_dir.is_dir():
                problem_visualizations = {}
                for file in vis_dir.iterdir():
                    if file.is_file():
                        problem_name = file.stem
                        problem_visualizations[problem_name] = file.name

        # Copy visualizations to output_dir if needed
        vis_map = None
        if problem_visualizations and self.output_dir:
            vis_map = {}
            out_vis_dir = self.output_dir / "visualizations"
            out_vis_dir.mkdir(exist_ok=True)
            for problem, vis_file in problem_visualizations.items():
                src_path = Path(visualizations_dir) / vis_file
                dst_path = out_vis_dir / vis_file
                shutil.copy2(src_path, dst_path)
                vis_map[problem] = f"visualizations/{vis_file}"
        elif problem_visualizations:
            vis_map = {k: os.path.join(visualizations_dir, v)
                       for k, v in problem_visualizations.items()}

        # Generate HTML
        title = summary_data.get("title") or "Benchmark Summary"
        html = self.generate_summary_html(
            summary_data, results_data, vis_map, title=title)

        # Write output
        if output_file:
            out_path = Path(output_file)
            if self.output_dir:
                out_path = self.output_dir / out_path.name
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(html)
            return str(out_path)
        elif self.output_dir:
            out_path = self.output_dir / "benchmark_summary.html"
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(html)
            return str(out_path)
        else:
            return html
