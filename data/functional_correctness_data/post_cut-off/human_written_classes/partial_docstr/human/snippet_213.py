import re
import os
import subprocess
from pathlib import Path
import glob

class OptimizerBenchmarkEnv:

    def __init__(self, fob_root=None):
        self.fob_root = Path(fob_root) if fob_root else Path(__file__).parent
        self.optimizers_dir = self.fob_root / 'pytorch_fob' / 'optimizers'
        self.tasks = ['mnist', 'classification_small', 'tabular']
        self.optimizer_name = None
        self.optimizer_dir = None

    def submit_optimizer(self, optimizer_code: str, optimizer_name: str, default_yaml: str=None):
        """
        Registers a new optimizer by writing its code and default config to the optimizers directory.
        optimizer_code: Python code for optimizer.py (must define configure_optimizers)
        optimizer_name: Name for the optimizer (used as folder name)
        default_yaml: Optional YAML string for default.yaml (otherwise uses a minimal template)
        """
        self.optimizer_name = optimizer_name
        self.optimizer_dir = self.optimizers_dir / optimizer_name
        os.makedirs(self.optimizer_dir, exist_ok=True)
        with open(self.optimizer_dir / 'optimizer.py', 'w') as f:
            f.write(optimizer_code)
        if default_yaml is None:
            default_yaml = f'optimizer:\n  name: {optimizer_name}\n  learning_rate: 1.e-3\n'
        with open(self.optimizer_dir / 'default.yaml', 'w') as f:
            f.write(default_yaml)
        with open(self.optimizer_dir / '__init__.py', 'w') as f:
            f.write('')
        print(f"Registered optimizer '{optimizer_name}' at {self.optimizer_dir}")

    def generate_experiment_yaml(self, yaml_path=None, seeds=[42], data_dir='examples/data', output_dir=None):
        """
        Generates an experiment YAML for the three tasks and the registered optimizer.
        yaml_path: where to write the YAML file (default: f"experiment_{optimizer_name}.yaml" in FOB root)
        seeds: list of seeds to use
        data_dir: directory for datasets
        output_dir: directory for outputs (default: outputs/experiment_{optimizer_name})
        """
        if self.optimizer_name is None:
            raise ValueError('No optimizer registered. Call submit_optimizer first.')
        if output_dir is None:
            output_dir = f'FOB/outputs/experiment_{self.optimizer_name}'
        if yaml_path is None:
            yaml_path = self.fob_root / f'experiment_{self.optimizer_name}.yaml'
        else:
            yaml_path = Path(yaml_path)
        yaml_content = f'\ntask:\n  - mnist\n  - classification_small\n  - tabular\nmax_epochs: 1\noptimizer:\n  - name: {self.optimizer_name}\nengine:\n  seed: {seeds}\n  data_dir: {data_dir}\n  output_dir: {output_dir}\n  train: true\n  test: true\n  plot: false\n'
        with open(yaml_path, 'w') as f:
            f.write(yaml_content)
        self.experiment_yaml_path = yaml_path
        print(f'Experiment YAML written to {yaml_path}')

    def run_benchmark(self):
        """
        Runs dataset setup and experiment using the generated YAML.
        """
        if not hasattr(self, 'experiment_yaml_path'):
            raise ValueError('No experiment YAML found. Call generate_experiment_yaml first.')
        print('Running dataset setup...')
        subprocess.run(['python3', '-m', 'pytorch_fob.dataset_setup', str(self.experiment_yaml_path)], check=True)
        print('Running experiment...')
        subprocess.run(['python3', '-m', 'pytorch_fob.run_experiment', str(self.experiment_yaml_path)], check=True)
        print('Benchmark run complete.')

    def get_reward(self, alpha=1.0, beta=1.0):
        """
        Computes a reward based on training time and final loss/accuracy.
        For classification tasks (mnist, classification_small), uses accuracy (maximize).
        For regression/tabular tasks, uses loss (minimize).
        - alpha: weight for time
        - beta: weight for loss/accuracy
        """
        import json
        import yaml
        with open(self.experiment_yaml_path, 'r') as f:
            config = yaml.safe_load(f)
        output_dir = config['engine']['output_dir']
        if not os.path.isabs(output_dir):
            output_dir = self.fob_root / output_dir
        total_time = 0.0
        reward = 0.0
        for task in self.tasks:
            pattern = os.path.join(output_dir, task, self.optimizer_name, '*', 'train_time.txt')
            files = glob.glob(str(pattern))
            if not files:
                print(f'Warning: No train_time.txt found for task {task}. Pattern: {pattern}')
                continue
            for file in files:
                with open(file, 'r') as f:
                    content = f.read()
                    match = re.search('([0-9]+\\.?[0-9]*)', content)
                    if match:
                        t = float(match.group(1))
                        total_time += t
                        print(f'{task}: {t} seconds (from {file})')
                scores_path = os.path.join(os.path.dirname(file), 'scores.json')
                metric_val = None
                metric_used = None
                if os.path.exists(scores_path):
                    with open(scores_path, 'r') as f:
                        scores = json.load(f)
                        if task in ['mnist', 'classification_small']:
                            for k in ['acc', 'test_acc', 'val_acc']:
                                for parent in ['test_final', 'test_best']:
                                    if parent in scores and isinstance(scores[parent], list) and (len(scores[parent]) > 0):
                                        if k in scores[parent][0]:
                                            metric_val = scores[parent][0][k]
                                            metric_used = k
                                            break
                                if metric_val is not None:
                                    break
                            if metric_val is not None:
                                print(f'{task}: {metric_used} = {metric_val} (maximize, from {scores_path})')
                                reward += beta * metric_val
                            else:
                                print(f'Warning: No suitable accuracy metric found in {scores_path} for {task}')
                        elif task == 'tabular':
                            for k in ['loss', 'test_loss', 'val_loss', 'test_rmse']:
                                for parent in ['test_final', 'test_best']:
                                    if parent in scores and isinstance(scores[parent], list) and (len(scores[parent]) > 0):
                                        if k in scores[parent][0]:
                                            metric_val = scores[parent][0][k]
                                            metric_used = k
                                            break
                                if metric_val is not None:
                                    break
                            if metric_val is not None:
                                print(f'{task}: {metric_used} = {metric_val} (minimize, from {scores_path})')
                                reward += -beta * metric_val
                            else:
                                print(f'Warning: No suitable loss metric found in {scores_path} for {task}')
                else:
                    print(f'Warning: scores.json not found for task {task} at {scores_path}')
        reward -= alpha * total_time
        print(f'Total training time: {total_time} seconds. Reward: {reward}')
        return reward