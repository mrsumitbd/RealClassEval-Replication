
import os
import webbrowser
import json


class MASVisualizer:

    def __init__(self, output_dir=None):
        self.output_dir = output_dir if output_dir else 'output'
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def generate_html(self, visualization_data, title=None):
        title = title if title else "MAS Visualization"
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{title}</title>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                #visualization {{ width: 100%; height: 600px; border: 1px solid #ccc; }}
            </style>
        </head>
        <body>
            <h1>{title}</h1>
            <div id="visualization">
                <pre>{json.dumps(visualization_data, indent=4)}</pre>
            </div>
        </body>
        </html>
        """
        return html_content

    def visualize(self, visualization_file, output_file=None, open_browser=True):
        if not output_file:
            output_file = os.path.join(self.output_dir, 'visualization.html')
        with open(output_file, 'w') as f:
            f.write(visualization_file)
        if open_browser:
            webbrowser.open(f'file://{os.path.abspath(output_file)}')

    def visualize_from_agent_system(self, agent_system, problem_id=None):
        visualization_data = agent_system.get_visualization_data(problem_id)
        html_content = self.generate_html(
            visualization_data, title=f"Agent System Visualization - Problem {problem_id}" if problem_id else "Agent System Visualization")
        self.visualize(html_content)
