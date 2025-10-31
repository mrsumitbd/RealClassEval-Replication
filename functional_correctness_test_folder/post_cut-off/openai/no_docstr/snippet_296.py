
import os
import json
import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional, Union


class BenchmarkVisualizer:
    """
    A simple visualizer for benchmark results. It can read summary and result data
    from JSON/CSV files, optionally embed problem‑specific visualizations, and
    generate an HTML report.
    """

    def __init__(self, output_dir: Optional[Union[str, Path]] = None):
        """
        Parameters
        ----------
        output_dir : str or Path, optional
            Directory where generated reports will be stored. If not provided,
            the current working directory is used.
        """
        self.output_dir = Path(output_dir) if output_dir else Path.cwd()
        self.output_dir.mkdir(parents=True, exist_ok=True)

    # --------------------------------------------------------------------- #
    # Helper methods
    # --------------------------------------------------------------------- #
    @staticmethod
    def _load_data(file_path: Union[str, Path]) -> pd.DataFrame:
        """
        Load data from a JSON or CSV file into a pandas DataFrame.
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        if path.suffix.lower() == ".json":
            with path.open("r", encoding="utf-8") as f:
                data = json.load(f)
            # If the JSON is a list of dicts, convert directly
            if isinstance(data, list):
                df = pd.DataFrame(data)
            else:
                # Assume a dict of dicts
                df = pd.DataFrame.from_dict(data, orient="index")
        elif path.suffix.lower() == ".csv":
            df = pd.read_csv(path)
        else:
            raise ValueError(f"Unsupported file format: {path.suffix}")
        return df

    @staticmethod
    def _group_visualizations(
        visualizations_dir: Union[str, Path]
    ) -> Dict[str, List[Path]]:
        """
        Group image files in a directory by problem name. The problem name is
        inferred from the file name up to the first underscore.
        """
        dir_path = Path(visualizations_dir)
        if not dir_path.is_dir():
            raise NotADirectoryError(f"Not a directory: {dir_path}")

        groups: Dict[str, List[Path]] = {}
        for img_path in dir_path.iterdir():
            if img_path.is_file() and img_path.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif"}:
                # Problem name is the part before the first underscore
                name_parts = img_path.stem.split("_", 1)
                problem_name = name_parts[0] if name_parts else img_path.stem
                groups.setdefault(problem_name, []).append(img_path)
        return groups

    # --------------------------------------------------------------------- #
    # Public API
    # --------------------------------------------------------------------- #
    def generate_summary_html(
        self,
        summary_data: Union[Dict, pd.DataFrame],
        results_data: Union[Dict, pd.DataFrame],
        problem_visualizations: Optional[Dict[str, List[Path]]] = None,
        title: Optional[str] = None,
    ) -> str:
        """
        Generate an HTML string summarizing benchmark results.

        Parameters
        ----------
        summary_data : dict or pd.DataFrame
            Summary statistics of the benchmark.
        results_data : dict or pd.DataFrame
            Detailed results of the benchmark.
        problem_visualizations : dict of str -> list of Path, optional
            Mapping from problem names to lists of image paths to embed.
        title : str, optional
            Title of the report.

        Returns
        -------
        str
            The generated HTML content.
        """
        # Convert to DataFrames if necessary
        if isinstance(summary_data, dict):
            summary_df = pd.DataFrame.from_dict(summary_data, orient="index")
        else:
            summary_df = summary_data

        if isinstance(results_data, dict):
            results_df = pd.DataFrame.from_dict(results_data, orient="index")
        else:
            results_df = results_data

        # Start building HTML
        html_parts = [
            "<!DOCTYPE html>",
            "<html lang='en'>",
            "<head>",
            "<meta charset='utf-8'>",
            f"<title>{title or 'Benchmark Report'}</title>",
            "<style>",
            "body {font-family: Arial, sans-serif; margin: 20px;}",
            "h1, h2 {color: #2c3e50;}",
            "table {border-collapse: collapse; width: 100%; margin-bottom: 20px;}",
            "th, td {border: 1px solid #ddd; padding: 8px; text-align: left;}",
            "th {background-color: #f2f2f2;}",
            ".image {margin: 10px 0;}",
            "</style>",
            "</head>",
            "<body>",
        ]

        # Title
        html_parts.append(f"<h1>{title or 'Benchmark Report'}</h1>")

        # Summary table
        html_parts.append("<h2>Summary</h2>")
        html_parts.append(summary_df.to_html(index=True, border=0))

        # Results table
        html_parts.append("<h2>Results</h2>")
        html_parts.append(results_df.to_html(index=True, border=0))

        # Problem visualizations
        if problem_visualizations:
            html_parts.append("<h2>Problem Visualizations</h2>")
            for problem, images in problem_visualizations.items():
                html_parts.append(f"<h3>{problem}</h3>")
                for img_path in images:
                    # Copy image to output directory if not already there
                    dest_path = self.output_dir / img_path.name
                    if not dest_path.exists():
                        try:
                            dest_path.write_bytes(img_path.read_bytes())
                        except Exception:
                            # Skip if cannot copy
                            continue
                    # Use relative path
                    rel_path = dest_path.name
                    html_parts.append(
                        f"<div class='image'><img src='{rel_path}' alt='{problem}' style='max-width:100%;'></div>"
                    )

        # Closing tags
        html_parts.extend(["</body>", "</html>"])

        return "\n".join(html_parts)

    def visualize_benchmark(
        self,
        summary_file: Union[str, Path],
        results_file: Optional[Union[str, Path]] = None,
        visualizations_dir: Optional[Union[str, Path]] = None,
        output_file: Optional[Union[str, Path]] = None,
    ) -> None:
        """
        Read benchmark data files, generate an HTML report, and write it to disk.

        Parameters
        ----------
        summary_file : str or Path
            Path to the summary data file (JSON or CSV).
        results_file : str or Path, optional
            Path to the results data file (JSON or CSV). If omitted, an empty
            DataFrame is used.
        visualizations_dir : str or Path, optional
            Directory containing problem‑specific visualization images.
        output_file : str or Path, optional
            Path where the generated HTML report will be written. If omitted,
            the file is named 'benchmark_report.html' in the output directory.
        """
        # Load data
        summary_df = self._load_data(summary_file)
        results_df = (
            self._load_data(results_file) if results_file else pd.DataFrame()
        )

        # Load visualizations
        problem_visualizations = (
            self._group_visual
