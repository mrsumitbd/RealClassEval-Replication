
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
        title = title or summary_data.get("title", "Benchmark Summary")
        header = f"<h1>{title}</h1>"
        summary_table_rows = ""
        for key, value in summary_data.items():
            if key == "title":
                continue
            summary_table_rows += f"<tr><th>{key}</th><td>{value}</td></tr>"

        summary_table = f"""
        <table border="1" cellpadding="4" cellspacing="0">
            {summary_table_rows}
        </table>
        """

        results_rows = ""
        for result in results_data:
            problem_id = result.get("problem_id", "unknown")
            name = result.get("name", problem_id)
            score = result.get("score", "N/A")
            link = ""
            if problem_visualizations and problem_id in problem_visualizations:
                link = f'<a href="{problem_visualizations[problem_id]}">View</a>'
            results_rows += f"""
            <tr>
                <td>{problem_id}</td>
                <td>{name}</td>
                <td>{score}</td>
                <td>{link}</td>
            </tr>
            """

        results_table = f"""
        <h2>Problem Results</h2>
        <table border="1" cellpadding="4" cellspacing="0">
            <tr><th>Problem ID</th><th>Name</th><th>Score</th><th>Visualization</th></tr>
            {results_rows}
        </table>
        """

        html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>{title}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ text-align: left; }}
                th {{ background-color: #f2f2f2; }}
            </style>
        </head>
        <body>
            {header}
            {summary_table}
            {results_table}
        </body>
        </html>
        """
        return html

    def visualize_benchmark(
        self,
        summary_file: str,
        results_file: Optional[str] = None,
        visualizations_dir: Optional[str] = None,
        output_file: Optional[str] = None,
    ) -> None:
        '''
        Generate a benchmark summary HTML file linking to individual problem visualizations.
        Args:
            summary_file: Path to JSON file containing summary data
            results_file: Optional path to JSON file containing list of problem results
            visualizations_dir: Optional directory containing per-problem visualization files
            output_file: Optional path to write the generated HTML file
        '''
        # Load summary data
        try:
            with open(summary_file, "r", encoding="utf-8") as f:
                summary_data = json.load(f)
        except Exception as e:
            raise RuntimeError(
                f"Failed to load summary file '{summary_file}': {e}")

        # Load results data
        results_data = []
        if results_file:
            try:
                with open(results_file, "r", encoding="utf-8") as f:
                    results_data = json.load(f)
                    if not isinstance(results_data, list):
                        raise ValueError(
                            "Results file must contain a JSON list")
            except Exception as e:
                raise RuntimeError(
                    f"Failed to load results file '{results_file}': {e}")

        # Build mapping from problem_id to visualization file path
        problem_visualizations = {}
        if visualizations_dir:
            vis_dir = Path(visualizations_dir)
            if vis_dir.is_dir():
                for file in vis_dir.iterdir():
                    if file.is_file() and file.suffix.lower() in {".html", ".htm"}:
                        # Assume file name starts with problem_id
                        problem_id = file.stem.split("_")[0]
                        problem_visualizations[problem_id] = str(
                            file.resolve())

        # Determine output file path
        if not output_file:
            base_name = Path(summary_file).stem
            output_file = self.output_dir / f"{base_name}_summary.html"
        else:
            output_file = Path(output_file)

        # Generate HTML
        html_content = self.generate_summary_html(
            summary_data=summary_data,
            results_data=results_data,
            problem_visualizations=problem_visualizations,
            title=summary_data.get("title"),
        )

        # Write to file
        try:
            output_file.parent.mkdir(parents=True, exist_ok=True)
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(html_content)
        except Exception as e:
            raise RuntimeError(
                f"Failed to write output file '{output_file}': {e}")
