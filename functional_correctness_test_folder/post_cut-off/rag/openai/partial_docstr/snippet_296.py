
import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Any


class BenchmarkVisualizer:
    '''Utility for visualizing benchmark results and agent interactions across multiple problems'''

    def __init__(self, output_dir: Optional[str] = None):
        '''
        Initialize the benchmark visualizer.
        Args:
            output_dir: Directory to save visualization HTML files
        '''
        self.output_dir = Path(output_dir) if output_dir else Path.cwd()
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_summary_html(
        self,
        summary_data: Dict[str, Any],
        results_data: List[Dict[str, Any]],
        problem_visualizations: Optional[Dict[str, str]] = None,
        title: Optional[str] = None,
    ) -> str:
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
        title = title or "Benchmark Summary"
        html_parts = [
            f"<html><head><title>{title}</title>",
            "<style>",
            "body{font-family:Arial,Helvetica,sans-serif;margin:20px;}",
            "table{border-collapse:collapse;width:100%;}",
            "th,td{border:1px solid #ddd;padding:8px;text-align:left;}",
            "th{background:#f2f2f2;}",
            "a{color:#0066cc;text-decoration:none;}",
            "a:hover{text-decoration:underline;}",
            "</style></head><body>",
            f"<h1>{title}</h1>",
        ]

        # Summary table
        html_parts.append("<h2>Overall Summary</h2>")
        html_parts.append("<table>")
        for key, value in summary_data.items():
            html_parts.append(f"<tr><th>{key}</th><td>{value}</td></tr>")
        html_parts.append("</table>")

        # Problem results table
        html_parts.append("<h2>Problem Results</h2>")
        html_parts.append("<table>")
        # Header
        headers = ["Problem ID", "Agent", "Score", "Status", "Link"]
        html_parts.append(
            "<tr>" + "".join(f"<th>{h}</th>" for h in headers) + "</tr>")

        for prob in results_data:
            prob_id = str(prob.get("problem_id", "N/A"))
            agent = prob.get("agent", "N/A")
            score = prob.get("score", "N/A")
            status = prob.get("status", "N/A")
            link = ""
            if problem_visualizations and prob_id in problem_visualizations:
                link = f'<a href="{problem_visualizations[prob_id]}" target="_blank">View</a>'
            html_parts.append(
                f"<tr><td>{prob_id}</td><td>{agent}</td><td>{score}</td>"
                f"<td>{status}</td><td>{link}</td></tr>"
            )
        html_parts.append("</table>")

        html_parts.append("</body></html>")
        return "\n".join(html_parts)

    def visualize_benchmark(
        self,
        summary_file: str,
        results_file: Optional[str] = None,
        visualizations_dir: Optional[str] = None,
        output_file: Optional[str] = None,
    ) -> Path:
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
        summary_path = Path(summary_file)
        if not summary_path.is_file():
            raise FileNotFoundError(f"Summary file not found: {summary_file}")

        with summary_path.open("r", encoding="utf-8") as f:
            summary_data = json.load(f)

        results_data = []
        if results_file:
            results_path = Path(results_file)
            if results_path.is_file():
                with results_path.open("r", encoding="utf-8") as f:
                    results_data = json.load(f)
            else:
                raise FileNotFoundError(
                    f"Results file not found: {results_file}")

        problem_visualizations = {}
        if visualizations_dir:
            vis_dir = Path(visualizations_dir)
            if vis_dir.is_dir():
                for file in vis_dir.iterdir():
                    if file.suffix.lower() in {".html", ".htm"}:
                        # Assume file name contains problem id, e.g., problem_123.html
                        name = file.stem
                        parts = name.split("_")
                        if len(parts) >= 2:
                            prob_id = parts[-1]
                            problem_visualizations[prob_id] = file.name

        title = summary_data.get("title", "Benchmark Summary")
        html_content = self.generate_summary_html(
            summary_data=summary_data,
            results_data=results_data,
            problem_visualizations=problem_visualizations,
            title=title,
        )

        output_path = Path(
            output_file) if output_file else self.output_dir / "benchmark_summary.html"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", encoding="utf-8") as f:
            f.write(html_content)

        return output_path
