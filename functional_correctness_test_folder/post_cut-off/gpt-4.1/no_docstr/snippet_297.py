
import os
import json
import webbrowser
import tempfile
from datetime import datetime


class MASVisualizer:

    def __init__(self, output_dir=None):
        if output_dir is None:
            output_dir = tempfile.gettempdir()
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def generate_html(self, visualization_data, title=None):
        if title is None:
            title = "MAS Visualization"
        data_json = json.dumps(visualization_data)
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{title}</title>
    <script src="https://cdn.jsdelivr.net/npm/vega@5"></script>
    <script src="https://cdn.jsdelivr.net/npm/vega-lite@5"></script>
    <script src="https://cdn.jsdelivr.net/npm/vega-embed@6"></script>
</head>
<body>
    <h2>{title}</h2>
    <div id="vis"></div>
    <script type="text/javascript">
        const spec = {data_json};
        vegaEmbed('#vis', spec);
    </script>
</body>
</html>
"""
        return html

    def visualize(self, visualization_file, output_file=None, open_browser=True):
        with open(visualization_file, 'r', encoding='utf-8') as f:
            visualization_data = json.load(f)
        title = visualization_data.get('title', 'MAS Visualization')
        html = self.generate_html(visualization_data, title=title)
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = os.path.join(
                self.output_dir, f"mas_visualization_{timestamp}.html")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
        if open_browser:
            webbrowser.open('file://' + os.path.abspath(output_file))
        return output_file

    def visualize_from_agent_system(self, agent_system, problem_id=None):
        # Assume agent_system has a method to_vega_lite_spec(problem_id)
        if hasattr(agent_system, 'to_vega_lite_spec'):
            spec = agent_system.to_vega_lite_spec(problem_id)
        elif hasattr(agent_system, 'to_dict'):
            spec = agent_system.to_dict()
        else:
            raise ValueError(
                "agent_system must have a to_vega_lite_spec or to_dict method")
        # Save spec to a temp file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        vis_file = os.path.join(
            self.output_dir, f"mas_visdata_{timestamp}.json")
        with open(vis_file, 'w', encoding='utf-8') as f:
            json.dump(spec, f)
        return self.visualize(vis_file)
