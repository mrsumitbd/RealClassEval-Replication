
import json
import os
import html
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
        problem_visualizations = problem_visualizations or {}

        # Basic CSS
        css = """
        <style>
        body {font-family: Arial, sans-serif; margin: 20px;}
        h1 {color: #333;}
        table {border-collapse: collapse; width: 100%; margin-bottom: 20px;}
        th, td {border: 1px solid #ddd; padding: 8px; text-align: left;}
        th {background-color: #f2f2f2;}
        tr:hover {background-color: #f5f5f5;}
        a {text-decoration: none; color: #0066cc;}
        a:hover {text-decoration: underline;}
        </style>
        """

        # Summary section
        summary_rows = ""
        for key, value in summary_data.items():
            summary_rows += f"<tr><th>{html.escape(str(key))}</th><td>{html.escape(str(value))}</td></tr>"

        summary_table = f"""
        <h2>Overall Summary</h2>
        <table>
            {summary_rows}
        </table>
        """

        # Results section
        results_rows = ""
        for result in results_data:
            problem_id = result.get("problem_id", "unknown")
            name = result.get("name", problem_id)
            score = result.get("score", "N/A")
            link = ""
            if problem_id in problem_visualizations:
                link = f'<a href="{html.escape(problem_visualizations[problem_id])}" target="_blank">View</a>'
            results_rows += f"""
            <tr>
                <td>{html.escape(str(problem_id))}</td>
                <td>{html.escape(str(name))}</td>
                <td>{html.escape(str(score))}</td>
                <td>{link}</td>
            </tr>
            """

        results_table = f"""
        <h2>Problem Results</h2>
        <table>
            <tr><th>Problem ID</th><th>Name</th><th>Score</th><th>Visualization</th></tr>
            {results_rows}
        </table>
        """

        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>{html.escape(title)}</title>
            {css}
        </head>
        <body>
            <h1>{html.escape(title)}</h1>
            {summary_table}
            {results_table}
        </body>
        </html>
        """
        return html_content

    def visualize_benchmark(
        self,
        summary_file: str,
        results_file: Optional[str] = None,
        visualizations_dir: Optional[str] = None,
        output_file: Optional[str] = None,
    ) -> str:
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
        if results_file and os.path.exists(results_file):
            with open(results_file, "r", encoding="utf-8") as f:
                results_data = json.load(f)

        # Map problem_id to visualization file
        problem_visualizations = {}
        if visualizations_dir and os.path.isdir(visualizations_dir):
            for fname in os.listdir(visualizations_dir):
                if fname.lower().endswith(".html"):
                    # Assume filename format: <problem_id>.html or similar
                    problem_id = os.path.splitext(fname)[0]
                    problem_visualizations[problem_id] = os.path.join(
                        visualizations_dir, fname)

        # Generate HTML
        html_str = self.generate_summary_html(
            summary_data=summary_data,
            results_data=results_data,
            problem_visualizations=problem_visualizations,
            title=summary_data.get("title", "Benchmark Summary"),
        )

        # Determine output path
        if not output_file:
            base_name = Path(summary_file).stem
            output_file = self.output_dir / f"{base_name}_summary.html"
        else:
            output_file = Path(output_file)

        # Ensure directory exists
        output_file.parent.mkdir(parents=True, exist_ok=True)

        # Write file
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html_str)

        return str(output_file)
