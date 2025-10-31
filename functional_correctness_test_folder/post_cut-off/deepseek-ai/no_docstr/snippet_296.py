
import os
import json
from jinja2 import Template


class BenchmarkVisualizer:

    def __init__(self, output_dir=None):
        self.output_dir = output_dir
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def generate_summary_html(self, summary_data, results_data, problem_visualizations=None, title=None):
        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>{{ title }}</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                h1 { color: #333; }
                table { border-collapse: collapse; width: 100%; margin-bottom: 20px; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background-color: #f2f2f2; }
                img { max-width: 100%; height: auto; }
            </style>
        </head>
        <body>
            <h1>{{ title }}</h1>
            <h2>Summary</h2>
            <table>
                <tr>
                    {% for key in summary_data.keys() %}
                    <th>{{ key }}</th>
                    {% endfor %}
                </tr>
                <tr>
                    {% for value in summary_data.values() %}
                    <td>{{ value }}</td>
                    {% endfor %}
                </tr>
            </table>
            
            <h2>Results</h2>
            <table>
                <tr>
                    {% for key in results_data[0].keys() %}
                    <th>{{ key }}</th>
                    {% endfor %}
                </tr>
                {% for row in results_data %}
                <tr>
                    {% for value in row.values() %}
                    <td>{{ value }}</td>
                    {% endfor %}
                </tr>
                {% endfor %}
            </table>
            
            {% if problem_visualizations %}
            <h2>Visualizations</h2>
            {% for problem, img_path in problem_visualizations.items() %}
            <div>
                <h3>{{ problem }}</h3>
                <img src="{{ img_path }}" alt="{{ problem }} visualization">
            </div>
            {% endfor %}
            {% endif %}
        </body>
        </html>
        """
        template = Template(html_template)
        return template.render(
            title=title or "Benchmark Summary",
            summary_data=summary_data,
            results_data=results_data,
            problem_visualizations=problem_visualizations or {}
        )

    def visualize_benchmark(self, summary_file, results_file=None, visualizations_dir=None, output_file=None):
        with open(summary_file, 'r') as f:
            summary_data = json.load(f)

        results_data = []
        if results_file:
            with open(results_file, 'r') as f:
                results_data = json.load(f)

        problem_visualizations = None
        if visualizations_dir and os.path.exists(visualizations_dir):
            problem_visualizations = {}
            for img_file in os.listdir(visualizations_dir):
                if img_file.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                    problem = os.path.splitext(img_file)[0]
                    problem_visualizations[problem] = os.path.join(
                        visualizations_dir, img_file)

        html_content = self.generate_summary_html(
            summary_data, results_data, problem_visualizations
        )

        if not output_file:
            output_file = os.path.join(
                self.output_dir, "benchmark_summary.html") if self.output_dir else "benchmark_summary.html"

        with open(output_file, 'w') as f:
            f.write(html_content)

        return output_file
