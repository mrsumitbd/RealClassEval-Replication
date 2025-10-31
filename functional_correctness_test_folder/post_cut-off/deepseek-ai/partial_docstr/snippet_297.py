
import json
import os
import webbrowser
from pathlib import Path


class MASVisualizer:
    '''Utility for visualizing Multi-Agent System interactions'''

    def __init__(self, output_dir=None):
        self.output_dir = output_dir
        if output_dir is not None:
            os.makedirs(output_dir, exist_ok=True)

    def generate_html(self, visualization_data, title=None):
        if title is None:
            title = "Multi-Agent System Visualization"

        html_template = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{title}</title>
            <script src="https://d3js.org/d3.v7.min.js"></script>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .agent {{ margin-bottom: 15px; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }}
                .interaction {{ margin-left: 20px; padding: 5px; border-left: 2px solid #aaa; }}
            </style>
        </head>
        <body>
            <h1>{title}</h1>
            <div id="visualization"></div>
            <script>
                const data = {json.dumps(visualization_data)};
                const visualization = d3.select("#visualization");
                
                data.agents.forEach(agent => {{
                    const agentDiv = visualization.append("div").attr("class", "agent");
                    agentDiv.append("h3").text(agent.name);
                    
                    if (agent.interactions && agent.interactions.length > 0) {{
                        const interactionsDiv = agentDiv.append("div").attr("class", "interactions");
                        agent.interactions.forEach(interaction => {{
                            interactionsDiv.append("div")
                                .attr("class", "interaction")
                                .text(`${interaction.type} with ${interaction.with} (${interaction.timestamp})`);
                        }});
                    }}
                }});
            </script>
        </body>
        </html>
        """
        return html_template

    def visualize(self, visualization_file, output_file=None, open_browser=True):
        with open(visualization_file, 'r') as f:
            visualization_data = json.load(f)

        title = visualization_data.get(
            'title', 'Multi-Agent System Visualization')
        html_content = self.generate_html(visualization_data, title)

        if output_file is None:
            if self.output_dir is not None:
                output_file = os.path.join(
                    self.output_dir, f"visualization_{os.path.basename(visualization_file)}.html")
            else:
                output_file = f"visualization_{os.path.basename(visualization_file)}.html"

        with open(output_file, 'w') as f:
            f.write(html_content)

        if open_browser:
            webbrowser.open(f'file://{os.path.abspath(output_file)}')

        return output_file

    def visualize_from_agent_system(self, agent_system, problem_id=None):
        html_files = []
        for agent in agent_system.agents:
            if problem_id is None or agent.problem_id == problem_id:
                for viz_file in agent.visualization_files:
                    html_file = self.visualize(viz_file, open_browser=False)
                    html_files.append(html_file)
        return html_files
