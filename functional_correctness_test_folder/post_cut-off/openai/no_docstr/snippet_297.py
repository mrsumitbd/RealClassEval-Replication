
import json
import os
import webbrowser
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Union


class MASVisualizer:
    """
    A simple visualizer for Multi‑Agent System (MAS) data.
    The visualizer can generate an HTML representation of a data structure
    (typically a list of dictionaries) and optionally open it in a web
    browser.  It also supports generating a visualisation directly from
    an agent system object that provides a ``get_visualization_data`` method.
    """

    def __init__(self, output_dir: Optional[Union[str, Path]] = None):
        """
        Parameters
        ----------
        output_dir : str or Path, optional
            Directory where generated HTML files will be stored.
            If ``None`` the current working directory is used.
        """
        self.output_dir = Path(output_dir) if output_dir else Path.cwd()
        self.output_dir.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------
    # Helper methods
    # ------------------------------------------------------------------
    @staticmethod
    def _ensure_list_of_dicts(data: Any) -> List[Dict[str, Any]]:
        """
        Normalise the input data to a list of dictionaries.
        """
        if isinstance(data, dict):
            # Convert a single dict to a list of one dict
            return [data]
        if isinstance(data, list):
            # Ensure each element is a dict
            if all(isinstance(item, dict) for item in data):
                return data
            # Try to convert each element to dict if possible
            return [dict(item) for item in data]
        # Fallback: try to interpret as iterable of key/value pairs
        if isinstance(data, Iterable):
            return [dict(item) for item in data]
        raise TypeError("Visualization data must be a dict or a list of dicts")

    @staticmethod
    def _html_escape(text: str) -> str:
        """
        Escape HTML special characters.
        """
        return (
            text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&#39;")
        )

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def generate_html(
        self,
        visualization_data: Union[Dict[str, Any], List[Dict[str, Any]]],
        title: Optional[str] = None,
    ) -> str:
        """
        Generate an HTML string from the provided visualization data.

        Parameters
        ----------
        visualization_data : dict or list of dicts
            The data to visualise.  Each dictionary represents a row.
        title : str, optional
            Title of the HTML page.  If omitted, a default title is used.

        Returns
        -------
        str
            The generated HTML content.
        """
        data = self._ensure_list_of_dicts(visualization_data)

        # Determine columns from the first row
        columns = set()
        for row in data:
            columns.update(row.keys())
        columns = sorted(columns)

        # Build HTML
        html_parts = [
            "<!DOCTYPE html>",
            "<html lang='en'>",
            "<head>",
            f"<meta charset='utf-8'>",
            f"<title>{self._html_escape(title or 'MAS Visualisation')}</title>",
            "<style>",
            "table {border-collapse: collapse; width: 100%;}",
            "th, td {border: 1px solid #ddd; padding: 8px;}",
            "th {background-color: #f2f2f2;}",
            "</style>",
            "</head>",
            "<body>",
            f"<h1>{self._html_escape(title or 'MAS Visualisation')}</h1>",
            "<table>",
            "<thead><tr>",
        ]

        # Header
        for col in columns:
            html_parts.append(f"<th>{self._html_escape(str(col))}</th>")
        html_parts.append("</tr></thead>")

        # Body
        html_parts.append("<tbody>")
        for row in data:
            html_parts.append("<tr>")
            for col in columns:
                value = row.get(col, "")
                html_parts.append(f"<td>{self._html_escape(str(value))}</td>")
            html_parts.append("</tr>")
        html_parts.append("</tbody>")

        # Close tags
        html_parts.extend(
            [
                "</table>",
                "</body>",
                "</html>",
            ]
        )

        return "\n".join(html_parts)

    def visualize(
        self,
        visualization_file: Union[str, Path, Dict[str, Any], List[Dict[str, Any]]],
        output_file: Optional[Union[str, Path]] = None,
        open_browser: bool = True,
    ) -> Path:
        """
        Generate an HTML visualisation from a file or data structure.

        Parameters
        ----------
        visualization_file : str, Path, dict or list of dicts
            Path to a JSON file containing the data, or the data itself.
        output_file : str or Path, optional
            Path where the HTML file will be written.  If omitted, the
            output file is derived from ``visualization_file``.
        open_browser : bool, default True
            If True, the generated HTML file is opened in the default web
            browser.

        Returns
        -------
        Path
            Path to the generated HTML file.
        """
        # Load data
        if isinstance(visualization_file, (str, Path)):
            path = Path(visualization_file)
            if not path.exists():
                raise FileNotFoundError(
                    f"Visualization file not found: {path}")
            with path.open("r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError as exc:
                    raise ValueError(f"Failed to parse JSON: {exc}") from exc
        else:
            data = visualization_file

        # Determine output file path
        if output_file is None:
            if isinstance(visualization_file, (str, Path)):
                base = Path(visualization_file).stem
                output_file = self.output_dir / f"{base}.html"
            else:
                output_file = self.output_dir / "visualisation.html"
        else:
            output_file = Path(output_file)

        # Ensure directory exists
        output_file.parent.mkdir(parents=True, exist_ok=True)

        # Generate HTML
        html_content = self.generate_html(data, title=output_file.stem)

        # Write to file
        with output_file.open("w", encoding="utf-8") as f:
            f.write(html_content)

        # Open in browser if requested
        if open_browser:
            webbrowser.open(f"file://{output_file.resolve()}")

        return output_file

    def visualize_from_agent_system(
        self,
        agent_system: Any,
        problem_id: Optional[Any] = None,
        output_file: Optional[Union[str, Path]] = None,
        open_browser: bool = True,
    ) -> Path:
        """
        Generate a visualisation directly from an agent system object.

        Parameters
        ----------
        agent_system : object
            The agent system instance.  It must provide a method
            ``get_visualization_data(problem_id)`` that returns data
            suitable for ``generate_html``.
        problem_id : any, optional
            Identifier of the problem to visualise.  Passed to
            ``agent_system.get_visualization_data``.
        output_file : str or Path, optional
            Path where the HTML file will be written
