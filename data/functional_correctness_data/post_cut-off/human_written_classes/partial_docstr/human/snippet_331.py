from typing import List, Optional
import json
from typing import List, Dict
import subprocess
from collections import defaultdict

class LogAnalyzer:

    def __init__(self):
        self.results: List[LogAnalysisResult] = []

    def run_analysis_command(self, commands: List[str]) -> None:
        """Run the analysis command for each log file."""
        for cmd in commands:
            try:
                subprocess.run(cmd.split(), check=True)
                self._process_output_file(cmd.split()[-1])
            except subprocess.CalledProcessError as e:
                print(f'Error running command: {cmd}')
                print(f'Error details: {e}')

    def _process_output_file(self, output_file: str) -> None:
        """Process the output file and store results."""
        try:
            with open(output_file, 'r') as f:
                data = json.load(f)
                result = LogAnalysisResult(experiment_design=data['Experiment Design'], execution_setup=data['Execution Setup'], implementation_alignment=data['Implementation Alignment'], conclusion_correctness=data['Conclusion Correctness'], explanations=data['Explanation'])
                self.results.append(result)
        except FileNotFoundError:
            print(f'Output file not found: {output_file}')
        except json.JSONDecodeError:
            print(f'Error decoding JSON from file: {output_file}')

    def generate_summary(self) -> Dict:
        """Generate a summary of all analyzed logs."""
        if not self.results:
            return {'error': 'No results to analyze'}
        total_logs = len(self.results)
        metrics = {'Experiment Design': defaultdict(int), 'Execution Setup': defaultdict(int), 'Implementation Alignment': defaultdict(int), 'Conclusion Correctness': defaultdict(int)}
        for result in self.results:
            metrics['Experiment Design'][result.experiment_design] += 1
            metrics['Execution Setup'][result.execution_setup] += 1
            metrics['Implementation Alignment'][result.implementation_alignment] += 1
            metrics['Conclusion Correctness'][result.conclusion_correctness] += 1
        summary = {'total_logs_analyzed': total_logs, 'metrics': {}}
        for metric, counts in metrics.items():
            summary['metrics'][metric] = {result: {'count': count, 'percentage': count / total_logs * 100} for result, count in counts.items()}
        return summary