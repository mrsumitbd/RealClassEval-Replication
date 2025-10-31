
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

    def _escape_html(self, text: str) -> str:
        """Simple HTML escaping."""
        return (
            text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&#39;")
        )

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
            "<!DOCTYPE html>",
            "<html lang='en'>",
            "<head>",
            f"<meta charset='utf-8'>",
            f"<title>{self._escape_html(title)}</title>",
            "<style>",
            "body{font-family:Arial,Helvetica,sans-serif;margin:20px;}",
            "h1{color:#333;}",
            "table{border-collapse:collapse;width:100%;margin-top:20px;}",
            "th,td{border:1px solid #ddd;padding:8px;text-align:left;}",
            "th{background:#f2f2f2;}",
            "a{color:#0066cc;text-decoration:none;}",
            "a:hover{text-decoration:underline;}",
            "</style>",
            "</head>",
            "<body>",
            f"<h1>{self._escape_html(title)}</h1>",
        ]

        # Summary section
        html_parts.append("<h2>Summary</h2>")
        html_parts.append("<table>")
        for key, value in summary_data.items():
            html_parts.append(
                f"<tr><th>{self._escape_html(str(key))}</th>"
                f"<td>{self._escape_html(str(value))}</td></tr>"
            )
        html_parts.append("</table>")

        # Problems section
        html_parts.append("<h2>Problems</h2>")
        html_parts.append(
            "<table>"
            "<tr>"
            "<th>Problem ID</th>"
            "<th>Name</th>"
            "<th>Status</th>"
            "<th>Score</th>"
            "<th>Visualization</th>"
            "</tr>"
        )
        for prob in results_data:
            prob_id = str(prob.get("problem_id", ""))
            name = str(prob.get("name", ""))
            status = str(prob.get("status", ""))
            score = str(prob.get("score", ""))
            viz_link = ""
            if problem_visualizations and prob_id in problem_visualizations:
                viz_path = problem_visualizations[prob_id]
                viz_link = f"<a href='{self._escape_html(viz_path)}' target='_blank'>View</a>"
            html_parts.append(
                f"<tr>"
                f"<td>{self._escape_html(prob_id)}</td>"
                f"<td>{self._escape_html(name)}</td>"
                f"<td>{self._escape_html(status)}</td>"
                f"<td>{self._escape_html(score)}</td>"
                f"<td>{viz_link}</td>"
                f"</tr>"
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
        # Load summary
        with open(summary_file, "r", encoding="utf-8") as f:
            summary_data = json.load(f)

        # Load results
        results_data = []
        if results_file:
            with open(results_file, "r", encoding="utf-8") as f:
                results_data = json.load(f)

        # Build problem visualizations mapping
        problem_visualizations = {}
        if visualizations_dir:
            viz_dir = Path(visualizations_dir)
            if viz_dir.is_dir():
                for file in viz_dir.iterdir():
                    if file.is_file() and file.suffix.lower() in {".html", ".htm"}:
                        # Assume filename format: <problem_id>_viz.html
                        name_parts = file.stem.split("_")
                        if name_parts:
                            prob_id = name_parts[0]
                            problem_visualizations[prob_id] = str(
                                file.relative_to(self.output_dir))

        # Determine output file path
        if not output_file:
            output_file = self.output_dir / "benchmark_summary.html"
        else:
            output_file = Path(output_file)
            output_file.parent.mkdir(parents=True, exist_ok=True)

        # Generate HTML
        html_content = self.generate_summary_html(
            summary_data=summary_data,
            results_data=results_data,
            problem_visualizations=problem_visualizations,
            title=summary_data.get("title") or "Benchmark Summary",
        )

        # Write to file
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html_content)

        return output_file
