
import os
import json
from jinja2 import Template


class BenchmarkVisualizer:
    '''Utility for visualizing benchmark results and agent interactions across multiple problems'''

    def __init__(self, output_dir=None):
        '''
        Initialize the benchmark visualizer.
        Args:
            output_dir: Directory to save visualization HTML files
        '''
        self.output_dir = output_dir
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def generate_summary_html(self, summary_data, results_data, problem_visualizations=None, title=None):
        '''
        Generate HTML for visualizing benchmark summary with links to problem visualizations.
        Args:
            summary_data: Dictionary with benchmark summary data
            results_data: List of problem results data
            problem_visualizations: Optional dictionary mapping problem_id to visualization file paths
            title: Optional title for the visualization
        Returns:
            HTML string
        '''
        template = Template('''
        <html>
            <head>
                <title>{{ title }}</title>
            </head>
            <body>
                <h1>{{ title }}</h1>
                <h2>Summary</h2>
                <ul>
                {% for key, value in summary_data.items() %}
                    <li>{{ key }}: {{ value }}</li>
                {% endfor %}
                </ul>
                <h2>Problem Results</h2>
                <ul>
                {% for result in results_data %}
                    <li>
                        Problem {{ result.problem_id }}: 
                        {% if problem_visualizations and result.problem_id in problem_visualizations %}
                            <a href="{{ problem_visualizations[result.problem_id] }}">Visualization</a>
                        {% endif %}
                        <ul>
                        {% for key, value in result.items() %}
                            {% if key != 'problem_id' %}
                                <li>{{ key }}: {{ value }}</li>
                            {% endif %}
                        {% endfor %}
                        </ul>
                    </li>
                {% endfor %}
                </ul>
            </body>
        </html>
        ''')
        return template.render(
            title=title or 'Benchmark Visualization',
            summary_data=summary_data,
            results_data=results_data,
            problem_visualizations=problem_visualizations or {}
        )

    def visualize_benchmark(self, summary_file, results_file=None, visualizations_dir=None, output_file=None):
        with open(summary_file, 'r') as f:
            summary_data = json.load(f)

        if results_file:
            with open(results_file, 'r') as f:
                results_data = json.load(f)
        else:
            results_data = []

        problem_visualizations = None
        if visualizations_dir:
            problem_visualizations = {}
            for filename in os.listdir(visualizations_dir):
                problem_id = os.path.splitext(filename)[0]
                problem_visualizations[problem_id] = os.path.join(
                    visualizations_dir, filename)

        html = self.generate_summary_html(
            summary_data, results_data, problem_visualizations)

        if output_file:
            output_path = output_file
        elif self.output_dir:
            output_path = os.path.join(
                self.output_dir, 'benchmark_visualization.html')
        else:
            raise ValueError('Output file or directory must be specified')

        with open(output_path, 'w') as f:
            f.write(html)
