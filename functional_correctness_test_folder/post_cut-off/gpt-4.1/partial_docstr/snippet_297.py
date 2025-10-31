
import os
import json
import tempfile
import webbrowser
from datetime import datetime


class MASVisualizer:
    '''Utility for visualizing Multi-Agent System interactions'''
    HTML_TEMPLATE = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>{title}</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; background: #f9f9f9; }}
            h1 {{ color: #333; }}
            .agent {{ margin-bottom: 20px; padding: 10px; background: #fff; border-radius: 8px; box-shadow: 0 2px 6px #eee; }}
            .step {{ margin-left: 20px; }}
            .message {{ color: #0074D9; }}
        </style>
    </head>
    <body>
        <h1>{title}</h1>
        <div id="visualization"></div>
        <script>
        var data = {data_json};
        function render() {{
            var container = document.getElementById('visualization');
            if (!data.agents) {{
                container.innerHTML = "<b>No agent data found.</b>";
                return;
            }}
            data.agents.forEach(function(agent) {{
                var div = document.createElement('div');
                div.className = 'agent';
                var h2 = document.createElement('h2');
                h2.textContent = "Agent: " + agent.name;
                div.appendChild(h2);
                if (agent.steps) {{
                    agent.steps.forEach(function(step, idx) {{
                        var stepDiv = document.createElement('div');
                        stepDiv.className = 'step';
                        stepDiv.innerHTML = "<b>Step " + (idx+1) + ":</b> " + step.action;
                        if (step.messages && step.messages.length > 0) {{
                            var msgList = document.createElement('ul');
                            step.messages.forEach(function(msg) {{
                                var li = document.createElement('li');
                                li.className = 'message';
                                li.textContent = msg;
                                msgList.appendChild(li);
                            }});
                            stepDiv.appendChild(msgList);
                        }}
                        div.appendChild(stepDiv);
                    }});
                }}
                container.appendChild(div);
            }});
        }}
        render();
        </script>
    </body>
    </html>
    """

    def __init__(self, output_dir=None):
        if output_dir is None:
            output_dir = tempfile.gettempdir()
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_html(self, visualization_data, title=None):
        if title is None:
            title = "Multi-Agent System Visualization"
        data_json = json.dumps(visualization_data, indent=2)
        html = self.HTML_TEMPLATE.format(title=title, data_json=data_json)
        return html

    def visualize(self, visualization_file, output_file=None, open_browser=True):
        with open(visualization_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        title = data.get('title', "Multi-Agent System Visualization")
        html = self.generate_html(data, title=title)
        if output_file is None:
            base = os.path.splitext(os.path.basename(visualization_file))[0]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = os.path.join(
                self.output_dir, f"{base}_{timestamp}.html")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
        if open_browser:
            webbrowser.open('file://' + os.path.abspath(output_file))
        return output_file

    def visualize_from_agent_system(self, agent_system, problem_id=None):
        '''
        Expects agent_system to have a method get_visualization_files(problem_id)
        which returns a list of JSON file paths.
        '''
        if not hasattr(agent_system, 'get_visualization_files'):
            raise AttributeError(
                "agent_system must have a get_visualization_files(problem_id) method")
        vis_files = agent_system.get_visualization_files(problem_id)
        html_files = []
        for vis_file in vis_files:
            html_file = self.visualize(vis_file, open_browser=False)
            html_files.append(html_file)
        return html_files
