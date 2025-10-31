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
        html.append("<!DOCTYPE html>")
        html.append("<html lang='en'>")
        html.append("<head>")
        html.append("<meta charset='UTF-8'>")
        html.append(
            "<meta name='viewport' content='width=device-width, initial-scale=1.0'>")
        html.append(f"<title>{title or 'Benchmark Summary'}</title>")
        html.append("""
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            h1, h2 { color: #333; }
            table { border-collapse: collapse; width: 100%; margin-bottom: 30px; }
            th, td { border: 1px solid #aaa; padding: 8px 12px; text-align: left; }
            th { background: #f0f0f0; }
            tr:hover { background: #f9f9f9; }
            .summary-table { width: auto; margin-bottom: 40px; }
            .problem-link { text-decoration: none; color: #1a0dab; }
            .problem-link:hover { text-decoration: underline; }
        </style>
        """)
        html.append("</head>")
        html.append("<body>")
        html.append(f"<h1>{title or 'Benchmark Summary'}</h1>")

        # Summary Table
        html.append("<h2>Benchmark Info</h2>")
        html.append("<table class='summary-table'>")
        for k, v in summary_data.items():
            if isinstance(v, (dict, list)):
                v = json.dumps(v)
            html.append(f"<tr><th>{k}</th><td>{v}</td></tr>")
        html.append("</table>")

        # Results Table
        html.append("<h2>Problem Results</h2>")
        if results_data:
            html.append("<table>")
            # Table header
            header_keys = []
            if isinstance(results_data, list) and results_data:
                # Find all keys used in any result
                all_keys = set()
                for r in results_data:
                    all_keys.update(r.keys())
                header_keys = sorted(all_keys)
            html.append("<tr>")
            for key in header_keys:
                html.append(f"<th>{key}</th>")
            if problem_visualizations:
                html.append("<th>Visualization</th>")
            html.append("</tr>")
            # Table rows
            for result in results_data:
                html.append("<tr>")
                for key in header_keys:
                    val = result.get(key, "")
                    html.append(f"<td>{val}</td>")
                if problem_visualizations:
                    problem_id = result.get("problem_id") or result.get(
                        "id") or result.get("problem") or ""
                    vis_path = problem_visualizations.get(problem_id)
                    if vis_path:
                        html.append(
                            f"<td><a class='problem-link' href='{vis_path}' target='_blank'>View</a></td>")
                    else:
                        html.append("<td></td>")
                html.append("</tr>")
            html.append("</table>")
        else:
            html.append("<p>No results data available.</p>")

        # List of all problem visualizations (if any not in results)
        if problem_visualizations:
            html.append("<h2>All Problem Visualizations</h2>")
            html.append("<ul>")
            for pid, vis_path in problem_visualizations.items():
                html.append(
                    f"<li><a class='problem-link' href='{vis_path}' target='_blank'>{pid}</a></li>")
            html.append("</ul>")

        html.append(
            f"<footer><hr><small>Generated on {datetime.datetime.now().isoformat()}</small></footer>")
        html.append("</body></html>")
        return "\n".join(html)

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
        results_data = []
        if results_file:
            with open(results_file, "r", encoding="utf-8") as f:
                results_data = json.load(f)
        elif "results" in summary_data:
            results_data = summary_data["results"]

        # Find problem visualizations
        problem_visualizations = {}
        if visualizations_dir and os.path.isdir(visualizations_dir):
            for fname in os.listdir(visualizations_dir):
                if fname.endswith(".html"):
                    # Try to extract problem id from filename
                    problem_id = fname
                    for prefix in ["problem_", "prob_", ""]:
                        if fname.startswith(prefix):
                            problem_id = fname[len(prefix):]
                            break
                    problem_id = os.path.splitext(problem_id)[0]
                    rel_path = os.path.relpath(os.path.join(
                        visualizations_dir, fname), self.output_dir)
                    problem_visualizations[problem_id] = rel_path

        # Try to get a title
        title = summary_data.get("benchmark_name") or summary_data.get(
            "name") or "Benchmark Summary"

        html = self.generate_summary_html(
            summary_data=summary_data,
            results_data=results_data,
            problem_visualizations=problem_visualizations,
            title=title
        )

        # Determine output file
        if output_file is None:
            base = Path(summary_file).stem
            output_file = os.path.join(
                self.output_dir, f"{base}_visualization.html")
        else:
            output_file = os.path.abspath(output_file)

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html)

        return output_file
