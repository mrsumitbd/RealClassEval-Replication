import subprocess
import torch
from ultralytics.utils.plotting import plot_tune_results
from ultralytics.utils import DEFAULT_CFG, LOGGER, callbacks, colorstr, remove_colorstr, yaml_print, yaml_save
import shutil
import numpy as np
from ultralytics.cfg import get_cfg, get_save_dir
import random
import time

class Tuner:
    """
    Class responsible for hyperparameter tuning of YOLO models.

    The class evolves YOLO model hyperparameters over a given number of iterations
    by mutating them according to the search space and retraining the model to evaluate their performance.

    Attributes:
        space (dict): Hyperparameter search space containing bounds and scaling factors for mutation.
        tune_dir (Path): Directory where evolution logs and results will be saved.
        tune_csv (Path): Path to the CSV file where evolution logs are saved.

    Methods:
        _mutate(hyp: dict) -> dict:
            Mutates the given hyperparameters within the bounds specified in `self.space`.

        __call__():
            Executes the hyperparameter evolution across multiple iterations.

    Example:
        Tune hyperparameters for YOLOv8n on COCO8 at imgsz=640 and epochs=30 for 300 tuning iterations.
        ```python
        from ultralytics import YOLO

        model = YOLO("yolo11n.pt")
        model.tune(data="coco8.yaml", epochs=10, iterations=300, optimizer="AdamW", plots=False, save=False, val=False)
        ```

        Tune with custom search space.
        ```python
        from ultralytics import YOLO

        model = YOLO("yolo11n.pt")
        model.tune(space={key1: val1, key2: val2})  # custom search space dictionary
        ```
    """

    def __init__(self, args=DEFAULT_CFG, _callbacks=None):
        """
        Initialize the Tuner with configurations.

        Args:
            args (dict, optional): Configuration for hyperparameter evolution.
        """
        self.space = args.pop('space', None) or {'lr0': (1e-05, 0.1), 'lrf': (0.0001, 0.1), 'momentum': (0.7, 0.98, 0.3), 'weight_decay': (0.0, 0.001), 'warmup_epochs': (0.0, 5.0), 'warmup_momentum': (0.0, 0.95), 'box': (1.0, 20.0), 'cls': (0.2, 4.0), 'dfl': (0.4, 6.0), 'hsv_h': (0.0, 0.1), 'hsv_s': (0.0, 0.9), 'hsv_v': (0.0, 0.9), 'degrees': (0.0, 45.0), 'translate': (0.0, 0.9), 'scale': (0.0, 0.95), 'shear': (0.0, 10.0), 'perspective': (0.0, 0.001), 'flipud': (0.0, 1.0), 'fliplr': (0.0, 1.0), 'bgr': (0.0, 1.0), 'mosaic': (0.0, 1.0), 'mixup': (0.0, 1.0), 'copy_paste': (0.0, 1.0)}
        self.args = get_cfg(overrides=args)
        self.tune_dir = get_save_dir(self.args, name=self.args.name or 'tune')
        self.args.name = None
        self.tune_csv = self.tune_dir / 'tune_results.csv'
        self.callbacks = _callbacks or callbacks.get_default_callbacks()
        self.prefix = colorstr('Tuner: ')
        callbacks.add_integration_callbacks(self)
        LOGGER.info(f"{self.prefix}Initialized Tuner instance with 'tune_dir={self.tune_dir}'\n{self.prefix}💡 Learn about tuning at https://docs.ultralytics.com/guides/hyperparameter-tuning")

    def _mutate(self, parent='single', n=5, mutation=0.8, sigma=0.2):
        """
        Mutates the hyperparameters based on bounds and scaling factors specified in `self.space`.

        Args:
            parent (str): Parent selection method: 'single' or 'weighted'.
            n (int): Number of parents to consider.
            mutation (float): Probability of a parameter mutation in any given iteration.
            sigma (float): Standard deviation for Gaussian random number generator.

        Returns:
            (dict): A dictionary containing mutated hyperparameters.
        """
        if self.tune_csv.exists():
            x = np.loadtxt(self.tune_csv, ndmin=2, delimiter=',', skiprows=1)
            fitness = x[:, 0]
            n = min(n, len(x))
            x = x[np.argsort(-fitness)][:n]
            w = x[:, 0] - x[:, 0].min() + 1e-06
            if parent == 'single' or len(x) == 1:
                x = x[random.choices(range(n), weights=w)[0]]
            elif parent == 'weighted':
                x = (x * w.reshape(n, 1)).sum(0) / w.sum()
            r = np.random
            r.seed(int(time.time()))
            g = np.array([v[2] if len(v) == 3 else 1.0 for v in self.space.values()])
            ng = len(self.space)
            v = np.ones(ng)
            while all(v == 1):
                v = (g * (r.random(ng) < mutation) * r.randn(ng) * r.random() * sigma + 1).clip(0.3, 3.0)
            hyp = {k: float(x[i + 1] * v[i]) for i, k in enumerate(self.space.keys())}
        else:
            hyp = {k: getattr(self.args, k) for k in self.space.keys()}
        for k, v in self.space.items():
            hyp[k] = max(hyp[k], v[0])
            hyp[k] = min(hyp[k], v[1])
            hyp[k] = round(hyp[k], 5)
        return hyp

    def __call__(self, model=None, iterations=10, cleanup=True):
        """
        Executes the hyperparameter evolution process when the Tuner instance is called.

        This method iterates through the number of iterations, performing the following steps in each iteration:
        1. Load the existing hyperparameters or initialize new ones.
        2. Mutate the hyperparameters using the `mutate` method.
        3. Train a YOLO model with the mutated hyperparameters.
        4. Log the fitness score and mutated hyperparameters to a CSV file.

        Args:
           model (Model): A pre-initialized YOLO model to be used for training.
           iterations (int): The number of generations to run the evolution for.
           cleanup (bool): Whether to delete iteration weights to reduce storage space used during tuning.

        Note:
           The method utilizes the `self.tune_csv` Path object to read and log hyperparameters and fitness scores.
           Ensure this path is set correctly in the Tuner instance.
        """
        t0 = time.time()
        best_save_dir, best_metrics = (None, None)
        (self.tune_dir / 'weights').mkdir(parents=True, exist_ok=True)
        for i in range(iterations):
            mutated_hyp = self._mutate()
            LOGGER.info(f'{self.prefix}Starting iteration {i + 1}/{iterations} with hyperparameters: {mutated_hyp}')
            metrics = {}
            train_args = {**vars(self.args), **mutated_hyp}
            save_dir = get_save_dir(get_cfg(train_args))
            weights_dir = save_dir / 'weights'
            try:
                cmd = ['yolo', 'train', *(f'{k}={v}' for k, v in train_args.items())]
                return_code = subprocess.run(' '.join(cmd), check=True, shell=True).returncode
                ckpt_file = weights_dir / ('best.pt' if (weights_dir / 'best.pt').exists() else 'last.pt')
                metrics = torch.load(ckpt_file)['train_metrics']
                assert return_code == 0, 'training failed'
            except Exception as e:
                LOGGER.warning(f'WARNING ❌️ training failure for hyperparameter tuning iteration {i + 1}\n{e}')
            fitness = metrics.get('fitness', 0.0)
            log_row = [round(fitness, 5)] + [mutated_hyp[k] for k in self.space.keys()]
            headers = '' if self.tune_csv.exists() else ','.join(['fitness'] + list(self.space.keys())) + '\n'
            with open(self.tune_csv, 'a') as f:
                f.write(headers + ','.join(map(str, log_row)) + '\n')
            x = np.loadtxt(self.tune_csv, ndmin=2, delimiter=',', skiprows=1)
            fitness = x[:, 0]
            best_idx = fitness.argmax()
            best_is_current = best_idx == i
            if best_is_current:
                best_save_dir = save_dir
                best_metrics = {k: round(v, 5) for k, v in metrics.items()}
                for ckpt in weights_dir.glob('*.pt'):
                    shutil.copy2(ckpt, self.tune_dir / 'weights')
            elif cleanup:
                shutil.rmtree(weights_dir, ignore_errors=True)
            plot_tune_results(self.tune_csv)
            header = f"{self.prefix}{i + 1}/{iterations} iterations complete ✅ ({time.time() - t0:.2f}s)\n{self.prefix}Results saved to {colorstr('bold', self.tune_dir)}\n{self.prefix}Best fitness={fitness[best_idx]} observed at iteration {best_idx + 1}\n{self.prefix}Best fitness metrics are {best_metrics}\n{self.prefix}Best fitness model is {best_save_dir}\n{self.prefix}Best fitness hyperparameters are printed below.\n"
            LOGGER.info('\n' + header)
            data = {k: float(x[best_idx, i + 1]) for i, k in enumerate(self.space.keys())}
            yaml_save(self.tune_dir / 'best_hyperparameters.yaml', data=data, header=remove_colorstr(header.replace(self.prefix, '# ')) + '\n')
            yaml_print(self.tune_dir / 'best_hyperparameters.yaml')