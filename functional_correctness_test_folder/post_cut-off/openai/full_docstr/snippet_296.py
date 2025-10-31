
import json
import os
from pathlib import Path
from typing import Dict, List, Optional


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
        summary_data: Dict,
        results_data: List[Dict],
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
        title = title or summary_data.get("title", "Benchmark Summary")
        html_parts = [
            "<!DOCTYPE html>",
            "<html lang='en'>",
            "<head>",
            f"<meta charset='utf-8'>",
            f"<title>{self._escape_html(title)}</title>",
            "<style>",
            "body {font-family: Arial, sans-serif; margin: 20px;}",
            "h1 {color: #333;}",
            "table {border-collapse: collapse; width: 100%; margin-top: 20px;}",
            "th, td {border: 1px solid #ddd; padding: 8px; text-align: left;}",
            "th {background-color: #f2f2f2;}",
            "a {color: #0066cc; text-decoration: none;}",
            "a:hover {text-decoration: underline;}",
            "</style>",
            "</head>",
            "<body>",
            f"<h1>{self._escape_html(title)}</h1>",
        ]

        # Summary section
        html_parts.append("<h2>Summary</h2>")
        html_parts.append("<table>")
        for key, value in summary_data.items():
            if key == "title":
                continue
            html_parts.append(
                f"<tr><th>{self._escape_html(str(key))}</th>"
                f"<td>{self._escape_html(str(value))}</td></tr>"
            )
        html_parts.append("</table>")

        # Results section
        html_parts.append("<h2>Problem Results</h2>")
        html_parts.append("<table>")
        if results_data:
            # Header
            headers = set()
            for res in results_data:
                headers.update(res.keys())
            headers = sorted(headers)
            html_parts.append(
                "<tr>" +
                "".join(
                    f"<th>{self._escape_html(h)}</th>" for h in headers) + "</tr>"
            )
            # Rows
            for res in results_data:
                html_parts.append("<tr>")
                for h in headers:
                    cell = res.get(h, "")
                    if h == "problem_id" and problem_visualizations:
                        vis_path = problem_visualizations.get(cell)
                        if vis_path:
                            cell = f'<a href="{self._escape_html(vis_path)}">{self._escape_html(str(cell))}</a>'
                    html_parts.append(
                        f"<td>{self._escape_html(str(cell))}</td>")
                html_parts.append("</tr>")
        else:
            html_parts.append("<tr><td>No results data available.</td></tr>")
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
                        # Assume filename without extension is problem_id
                        problem_id = file.stem
                        problem_visualizations[problem_id] = str(
                            file.resolve())
            else:
                raise FileNotFoundError(
                    f"Visualizations directory not found: {visualizations_dir}")

        html_content = self.generate_summary_html(
            summary_data=summary_data,
            results_data=results_data,
            problem_visualizations=problem_visualizations,
            title=summary_data.get("title"),
        )

        if not output_file:
            output_file = summary_path.with_suffix(".html")
        output_path = Path(output_file).resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with output_path.open("w", encoding="utf-8") as f:
            f.write(html_content)

        return output_path
