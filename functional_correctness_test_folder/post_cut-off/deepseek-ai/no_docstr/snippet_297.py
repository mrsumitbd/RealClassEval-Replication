
import os
import webbrowser
from pathlib import Path


class MASVisualizer:

    def __init__(self, output_dir=None):
        self.output_dir = output_dir
        if output_dir is not None:
            os.makedirs(output_dir, exist_ok=True)

    def generate_html(self, visualization_data, title=None):
        html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>{title}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        .visualization {{
            border: 1px solid #ddd;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 5px;
            background-color: #f9f9f9;
        }}
        h1 {{
            color: #333;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{title}</h1>
        <div class="visualization">
            {content}
        </div>
    </div>
</body>
</html>
        """
        content = str(visualization_data)
        title = title or "MAS Visualization"
        return html_template.format(title=title, content=content)

    def visualize(self, visualization_file, output_file=None, open_browser=True):
        if output_file is None:
            if self.output_dir is not None:
                output_file = os.path.join(
                    self.output_dir, "visualization.html")
            else:
                output_file = "visualization.html"

        with open(visualization_file, 'r') as f:
            content = f.read()

        html = self.generate_html(content)

        with open(output_file, 'w') as f:
            f.write(html)

        if open_browser:
            webbrowser.open(f'file://{Path(output_file).absolute()}')

        return output_file

    def visualize_from_agent_system(self, agent_system, problem_id=None):
        if problem_id is not None:
            title = f"Agent System Visualization - Problem {problem_id}"
        else:
            title = "Agent System Visualization"

        visualization_data = str(agent_system)
        html = self.generate_html(visualization_data, title)

        if self.output_dir is not None:
            output_file = os.path.join(
                self.output_dir, f"agent_system_{problem_id or 'default'}.html")
        else:
            output_file = f"agent_system_{problem_id or 'default'}.html"

        with open(output_file, 'w') as f:
            f.write(html)

        webbrowser.open(f'file://{Path(output_file).absolute()}')

        return output_file
