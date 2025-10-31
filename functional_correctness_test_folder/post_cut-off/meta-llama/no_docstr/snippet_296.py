
import os
import json
import pandas as pd
from jinja2 import Template


class BenchmarkVisualizer:

    def __init__(self, output_dir=None):
        self.output_dir = output_dir
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def generate_summary_html(self, summary_data, results_data, problem_visualizations=None, title=None):
        template = Template('''
        <html>
            <head>
                <title>{{ title }}</title>
            </head>
            <body>
                <h1>{{ title }}</h1>
                <h2>Summary</h2>
                <table>
                    {% for key, value in summary_data.items() %}
                    <tr>
                        <td>{{ key }}</td>
                        <td>{{ value }}</td>
                    </tr>
                    {% endfor %}
                </table>
                <h2>Results</h2>
                <table>
                    <tr>
                        {% for column in results_data.columns %}
                        <th>{{ column }}</th>
                        {% endfor %}
                    </tr>
                    {% for index, row in results_data.iterrows() %}
                    <tr>
                        {% for value in row %}
                        <td>{{ value }}</td>
                        {% endfor %}
                    </tr>
                    {% endfor %}
                </table>
                {% if problem_visualizations %}
                <h2>Visualizations</h2>
                {% for visualization in problem_visualizations %}
                <img src="{{ visualization }}" />
                {% endfor %}
                {% endif %}
            </body>
        </html>
        ''')
        if title is None:
            title = 'Benchmark Results'
        html = template.render(title=title, summary_data=summary_data, results_data=results_data.to_dict(
            orient='records'), problem_visualizations=problem_visualizations)
        return html

    def visualize_benchmark(self, summary_file, results_file=None, visualizations_dir=None, output_file=None):
        with open(summary_file, 'r') as f:
            summary_data = json.load(f)

        if results_file:
            results_data = pd.read_csv(results_file)
        else:
            results_data = pd.DataFrame()

        if visualizations_dir:
            problem_visualizations = [os.path.join(visualizations_dir, f) for f in os.listdir(
                visualizations_dir) if f.endswith('.png') or f.endswith('.jpg')]
        else:
            problem_visualizations = None

        html = self.generate_summary_html(
            summary_data, results_data, problem_visualizations)

        if output_file is None:
            output_file = 'benchmark_results.html'

        if self.output_dir:
            output_file = os.path.join(self.output_dir, output_file)

        with open(output_file, 'w') as f:
            f.write(html)
