
import json
import os
import webbrowser
from datetime import datetime


class MASVisualizer:
    '''Utility for visualizing Multi-Agent System interactions'''

    def __init__(self, output_dir=None):
        self.output_dir = output_dir if output_dir else 'visualizations'
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_html(self, visualization_data, title=None):
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{title if title else 'MAS Visualization'}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .agent {{ margin: 10px; padding: 10px; border: 1px solid #ccc; border-radius: 5px; }}
                .message {{ margin: 5px; padding: 5px; background-color: #f0f0f0; border-radius: 3px; }}
            </style>
        </head>
        <body>
            <h1>{title if title else 'MAS Visualization'}</h1>
        """

        for agent in visualization_data['agents']:
            html_content += f"""
            <div class="agent">
                <h2>Agent: {agent['name']}</h2>
                <p>Type: {agent['type']}</p>
                <h3>Messages:</h3>
            """
            for message in agent['messages']:
                html_content += f"""
                <div class="message">
                    <p><strong>From:</strong> {message['from']}</p>
                    <p><strong>To:</strong> {message['to']}</p>
                    <p><strong>Content:</strong> {message['content']}</p>
                    <p><strong>Timestamp:</strong> {message['timestamp']}</p>
                </div>
                """
            html_content += "</div>"

        html_content += """
        </body>
        </html>
        """

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(
            self.output_dir, f"visualization_{timestamp}.html")

        with open(output_file, 'w') as f:
            f.write(html_content)

        return output_file

    def visualize(self, visualization_file, output_file=None, open_browser=True):
        '''
        Generate an HTML visualization from a visualization data file and open in browser.
        Args:
            visualization_file: Path to the visualization data JSON file
            output_file: Optional path to save the HTML output
            open_browser: Whether to open the visualization in a browser (default: True)
        Returns:
            Path to the generated HTML file
        '''
        with open(visualization_file, 'r') as f:
            visualization_data = json.load(f)

        title = visualization_data.get('title', None)
        html_file = self.generate_html(visualization_data, title)

        if output_file:
            os.rename(html_file, output_file)
            html_file = output_file

        if open_browser:
            webbrowser.open(f'file://{os.path.abspath(html_file)}')

        return html_file

    def visualize_from_agent_system(self, agent_system, problem_id=None):
        '''
        Generate visualizations for all visualization files from an agent system.
        Args:
            agent_system: AgentSystem instance
            problem_id: Optional problem ID to filter by
        Returns:
            List of paths to generated HTML files
        '''
        html_files = []

        for agent in agent_system.agents:
            for visualization_file in agent.visualization_files:
                if problem_id and visualization_file.problem_id != problem_id:
                    continue
                html_file = self.visualize(
                    visualization_file.path, open_browser=False)
                html_files.append(html_file)

        return html_files
