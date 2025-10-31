
import os
import json
from jinja2 import Environment, FileSystemLoader


class BenchmarkVisualizer:

    def __init__(self, output_dir=None):
        self.output_dir = output_dir or 'output'
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def generate_summary_html(self, summary_data, results_data, problem_visualizations=None, title=None):
        env = Environment(loader=FileSystemLoader('templates'))
        template = env.get_template('summary_template.html')
        html_content = template.render(
            title=title or "Benchmark Summary",
            summary_data=summary_data,
            results_data=results_data,
            problem_visualizations=problem_visualizations or {}
        )
        output_path = os.path.join(self.output_dir, 'summary.html')
        with open(output_path, 'w') as f:
            f.write(html_content)
        return output_path

    def visualize_benchmark(self, summary_file, results_file=None, visualizations_dir=None, output_file=None):
        with open(summary_file, 'r') as f:
            summary_data = json.load(f)

        results_data = {}
        if results_file:
            with open(results_file, 'r') as f:
                results_data = json.load(f)

        problem_visualizations = {}
        if visualizations_dir:
            for filename in os.listdir(visualizations_dir):
                if filename.endswith('.png'):
                    problem_id = filename.split('.')[0]
                    problem_visualizations[problem_id] = os.path.join(
                        visualizations_dir, filename)

        output_file = output_file or 'summary.html'
        return self.generate_summary_html(summary_data, results_data, problem_visualizations, title="Benchmark Results")
