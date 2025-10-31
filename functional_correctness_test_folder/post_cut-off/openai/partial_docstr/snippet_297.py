
import os
import json
import uuid
import datetime
import webbrowser
from pathlib import Path


class MASVisualizer:
    '''Utility for visualizing Multi-Agent System interactions'''

    def __init__(self, output_dir=None):
        """
        Parameters
        ----------
        output_dir : str or Path, optional
            Directory where generated HTML files will be stored.
            If None, a temporary directory under the current working directory
            named 'mas_visualizations_<timestamp>' will be created.
        """
        if output_dir is None:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            output_dir = Path.cwd() / f"mas_visualizations_{timestamp}"
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _html_template(self, title, data_json):
        """
        Simple HTML template embedding the JSON data.
        """
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title}</title>
<style>
body {{ font-family: Arial, sans-serif; margin: 20px; }}
pre {{ background: #f4f4f4; padding: 10px; border: 1px solid #ddd; }}
</style>
</head>
<body>
<h1>{title}</h1>
<pre id="data">{data_json}</pre>
<script>
/* Placeholder for future interactive visualizations */
console.log('Visualization data:', {data_json});
</script>
</body>
</html>"""

    def generate_html(self, visualization_data, title=None):
        """
        Generate an HTML file from the given visualization data.

        Parameters
        ----------
        visualization_data : dict
            Data to be visualized.
        title : str, optional
            Title of the visualization. If None, a UUID will be used.

        Returns
        -------
        Path
            Path to the generated HTML file.
        """
        if title is None:
            title = f"Visualization_{uuid.uuid4().hex[:8]}"
        data_json = json.dumps(visualization_data, indent=2)
        html_content = self._html_template(title, data_json)

        filename = f"{title.replace(' ', '_')}.html"
        file_path = self.output_dir / filename
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        return file_path

    def visualize(self, visualization_file, output_file=None, open_browser=True):
        """
        Generate an HTML visualization from a visualization data file and open in browser.

        Parameters
        ----------
        visualization_file : str or Path
            Path to the visualization data JSON file.
        output_file : str or Path, optional
            Optional path to save the HTML output. If None, a file will be created
            in the output directory with a name derived from the JSON file.
        open_browser : bool, default True
            Whether to open the visualization in a browser.

        Returns
        -------
        Path
            Path to the generated HTML file.
        """
        vis_path = Path(visualization_file)
        if not vis_path.is_file():
            raise FileNotFoundError(
                f"Visualization file not found: {vis_path}")

        with open(vis_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON in {vis_path}: {e}")

        title = vis_path.stem
        if output_file is None:
            output_file = self.output_dir / f"{title}.html"
        else:
            output_file = Path(output_file)

        # Ensure the output directory exists
        output_file.parent.mkdir(parents=True, exist_ok=True)

        # Generate HTML
        html_content = self._html_template(title, json.dumps(data, indent=2))
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html_content)

        if open_browser:
            webbrowser.open_new_tab(output_file.as_uri())

        return output_file

    def visualize_from_agent_system(self, agent_system, problem_id=None):
        """
        Generate visualizations for all visualization files from an agent system.

        Parameters
        ----------
        agent_system : object
            An instance that provides a method `get_visualization_files(problem_id=None)`
            returning an iterable of file paths (strings or Path objects).
        problem_id : str or int, optional
            Optional problem ID to filter by.

        Returns
        -------
        list[Path]
            List of paths to generated HTML files.
        """
        if not hasattr(agent_system, "get_visualization_files"):
            raise AttributeError(
                "agent_system must provide a 'get_visualization_files' method"
            )

        vis_files = agent_system.get_visualization_files(problem_id=problem_id)
        if not vis_files:
            return []

        generated_files = []
        for vis_file in vis_files:
            try:
                html_path = self.visualize(vis_file, open_browser=False)
                generated_files.append(html_path)
            except Exception as e:
                # Log the error and continue with next file
                print(f"Failed to visualize {vis_file}: {e}")

        return generated_files
