
import os
import json
import matplotlib.pyplot as plt
from jinja2 import Environment, FileSystemLoader


class BenchmarkVisualizer:

    def __init__(self, output_dir=None):
        self.output_dir = output_dir or os.getcwd()
        self.env = Environment(loader=FileSystemLoader(
            os.path.join(os.path.dirname(__file__), 'templates')))

    def generate_summary_html(self, summary_data, results_data, problem_visualizations=None, title=None):
        template = self.env.get_template('summary_template.html')
        html_content = template.render(
            summary_data=summary_data,
            results_data=results_data,
            problem_visualizations=problem_visualizations,
            title=title
        )
        return html_content

    def visualize_benchmark(self, summary_file, results_file=None, visualizations_dir=None, output_file=None):
        with open(summary_file, 'r') as f:
            summary_data = json.load(f)

        if results_file:
            with open(results_file, 'r') as f:
                results_data = json.load(f)
        else:
            results_data = None

        problem_visualizations = []
        if visualizations_dir:
            for filename in os.listdir(visualizations_dir):
                if filename.endswith('.png'):
                    problem_visualizations.append(
                        os.path.join(visualizations_dir, filename))

        html_content = self.generate_summary_html(
            summary_data, results_data, problem_visualizations, title="Benchmark Results")

        output_file = output_file or os.path.join(
            self.output_dir, 'benchmark_results.html')
        with open(output_file, 'w') as f:
            f.write(html_content)

        return output_file
