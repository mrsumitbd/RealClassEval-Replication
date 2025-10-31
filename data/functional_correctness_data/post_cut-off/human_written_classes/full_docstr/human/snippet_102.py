from ultralytics.utils.checks import IS_PYTHON_3_12, check_requirements, check_yolo
from pathlib import Path
import yaml
import os
from ultralytics.utils.downloads import safe_download
import shutil
import re

class RF100Benchmark:
    """Benchmark YOLO model performance across various formats for speed and accuracy."""

    def __init__(self):
        """Initialize the RF100Benchmark class for benchmarking YOLO model performance across various formats."""
        self.ds_names = []
        self.ds_cfg_list = []
        self.rf = None
        self.val_metrics = ['class', 'images', 'targets', 'precision', 'recall', 'map50', 'map95']

    def set_key(self, api_key):
        """
        Set Roboflow API key for processing.

        Args:
            api_key (str): The API key.

        Examples:
            Set the Roboflow API key for accessing datasets:
            >>> benchmark = RF100Benchmark()
            >>> benchmark.set_key("your_roboflow_api_key")
        """
        check_requirements('roboflow')
        from roboflow import Roboflow
        self.rf = Roboflow(api_key=api_key)

    def parse_dataset(self, ds_link_txt='datasets_links.txt'):
        """
        Parse dataset links and download datasets.

        Args:
            ds_link_txt (str): Path to the file containing dataset links.

        Examples:
            >>> benchmark = RF100Benchmark()
            >>> benchmark.set_key("api_key")
            >>> benchmark.parse_dataset("datasets_links.txt")
        """
        (shutil.rmtree('rf-100'), os.mkdir('rf-100')) if os.path.exists('rf-100') else os.mkdir('rf-100')
        os.chdir('rf-100')
        os.mkdir('ultralytics-benchmarks')
        safe_download('https://github.com/ultralytics/assets/releases/download/v0.0.0/datasets_links.txt')
        with open(ds_link_txt) as file:
            for line in file:
                try:
                    _, url, workspace, project, version = re.split('/+', line.strip())
                    self.ds_names.append(project)
                    proj_version = f'{project}-{version}'
                    if not Path(proj_version).exists():
                        self.rf.workspace(workspace).project(project).version(version).download('yolov8')
                    else:
                        print('Dataset already downloaded.')
                    self.ds_cfg_list.append(Path.cwd() / proj_version / 'data.yaml')
                except Exception:
                    continue
        return (self.ds_names, self.ds_cfg_list)

    @staticmethod
    def fix_yaml(path):
        """
        Fixes the train and validation paths in a given YAML file.

        Args:
            path (str): Path to the YAML file to be fixed.

        Examples:
            >>> RF100Benchmark.fix_yaml("path/to/data.yaml")
        """
        with open(path) as file:
            yaml_data = yaml.safe_load(file)
        yaml_data['train'] = 'train/images'
        yaml_data['val'] = 'valid/images'
        with open(path, 'w') as file:
            yaml.safe_dump(yaml_data, file)

    def evaluate(self, yaml_path, val_log_file, eval_log_file, list_ind):
        """
        Evaluate model performance on validation results.

        Args:
            yaml_path (str): Path to the YAML configuration file.
            val_log_file (str): Path to the validation log file.
            eval_log_file (str): Path to the evaluation log file.
            list_ind (int): Index of the current dataset in the list.

        Returns:
            (float): The mean average precision (mAP) value for the evaluated model.

        Examples:
            Evaluate a model on a specific dataset
            >>> benchmark = RF100Benchmark()
            >>> benchmark.evaluate("path/to/data.yaml", "path/to/val_log.txt", "path/to/eval_log.txt", 0)
        """
        skip_symbols = ['🚀', '⚠️', '💡', '❌']
        with open(yaml_path) as stream:
            class_names = yaml.safe_load(stream)['names']
        with open(val_log_file, encoding='utf-8') as f:
            lines = f.readlines()
            eval_lines = []
            for line in lines:
                if any((symbol in line for symbol in skip_symbols)):
                    continue
                entries = line.split(' ')
                entries = list(filter(lambda val: val != '', entries))
                entries = [e.strip('\n') for e in entries]
                eval_lines.extend(({'class': entries[0], 'images': entries[1], 'targets': entries[2], 'precision': entries[3], 'recall': entries[4], 'map50': entries[5], 'map95': entries[6]} for e in entries if e in class_names or (e == 'all' and '(AP)' not in entries and ('(AR)' not in entries))))
        map_val = 0.0
        if len(eval_lines) > 1:
            print("There's more dicts")
            for lst in eval_lines:
                if lst['class'] == 'all':
                    map_val = lst['map50']
        else:
            print("There's only one dict res")
            map_val = [res['map50'] for res in eval_lines][0]
        with open(eval_log_file, 'a') as f:
            f.write(f'{self.ds_names[list_ind]}: {map_val}\n')