import os
from typing import List, Union, Dict, Any

class Tracking:
    """A unified tracking interface for logging experiment data to multiple backends.

    This class provides a centralized way to log experiment metrics, parameters, and artifacts
    to various tracking backends including WandB, MLflow, SwanLab, TensorBoard, and console.

    Attributes:
        supported_backend: List of supported tracking backends.
        logger: Dictionary of initialized logger instances for each backend.
    """
    supported_backend = ['wandb', 'mlflow', 'swanlab', 'vemlp_wandb', 'tensorboard', 'console', 'clearml']

    def __init__(self, project_name, experiment_name, default_backend: Union[str, List[str]]='console', config=None):
        if isinstance(default_backend, str):
            default_backend = [default_backend]
        for backend in default_backend:
            if backend == 'tracking':
                import warnings
                warnings.warn('`tracking` logger is deprecated. use `wandb` instead.', DeprecationWarning, stacklevel=2)
            else:
                assert backend in self.supported_backend, f'{backend} is not supported'
        self.logger = {}
        if 'tracking' in default_backend or 'wandb' in default_backend:
            import wandb
            settings = None
            if config['trainer'].get('wandb_proxy', None):
                settings = wandb.Settings(https_proxy=config['trainer']['wandb_proxy'])
            wandb.init(project=project_name, name=experiment_name, config=config, settings=settings)
            self.logger['wandb'] = wandb
        if 'mlflow' in default_backend:
            import os
            import mlflow
            MLFLOW_TRACKING_URI = os.environ.get('MLFLOW_TRACKING_URI', None)
            if MLFLOW_TRACKING_URI:
                mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
            experiment = mlflow.set_experiment(project_name)
            mlflow.start_run(experiment_id=experiment.experiment_id, run_name=experiment_name)
            mlflow.log_params(_compute_mlflow_params_from_objects(config))
            self.logger['mlflow'] = _MlflowLoggingAdapter()
        if 'swanlab' in default_backend:
            import os
            import swanlab
            SWANLAB_API_KEY = os.environ.get('SWANLAB_API_KEY', None)
            SWANLAB_LOG_DIR = os.environ.get('SWANLAB_LOG_DIR', 'swanlog')
            SWANLAB_MODE = os.environ.get('SWANLAB_MODE', 'cloud')
            if SWANLAB_API_KEY:
                swanlab.login(SWANLAB_API_KEY)
            if config is None:
                config = {}
            swanlab.init(project=project_name, experiment_name=experiment_name, config={'FRAMEWORK': 'siirl', **config}, logdir=SWANLAB_LOG_DIR, mode=SWANLAB_MODE)
            self.logger['swanlab'] = swanlab
        if 'vemlp_wandb' in default_backend:
            import os
            import volcengine_ml_platform
            from volcengine_ml_platform import wandb as vemlp_wandb
            volcengine_ml_platform.init(ak=os.environ['VOLC_ACCESS_KEY_ID'], sk=os.environ['VOLC_SECRET_ACCESS_KEY'], region=os.environ['MLP_TRACKING_REGION'])
            vemlp_wandb.init(project=project_name, name=experiment_name, config=config, sync_tensorboard=True)
            self.logger['vemlp_wandb'] = vemlp_wandb
        if 'tensorboard' in default_backend:
            self.logger['tensorboard'] = _TensorboardAdapter()
        if 'console' in default_backend:
            from siirl.utils.logger.aggregate_logger import LocalLogger
            self.console_logger = LocalLogger(print_to_console=True)
            self.logger['console'] = self.console_logger
        if 'clearml' in default_backend:
            self.logger['clearml'] = ClearMLLogger(project_name, experiment_name, config)

    def log(self, data, step, backend=None):
        for default_backend, logger_instance in self.logger.items():
            if backend is None or default_backend in backend:
                logger_instance.log(data=data, step=step)

    def __del__(self):
        if 'wandb' in self.logger:
            self.logger['wandb'].finish(exit_code=0)
        if 'swanlab' in self.logger:
            self.logger['swanlab'].finish()
        if 'vemlp_wandb' in self.logger:
            self.logger['vemlp_wandb'].finish(exit_code=0)
        if 'tensorboard' in self.logger:
            self.logger['tensorboard'].finish()
        if 'clearnml' in self.logger:
            self.logger['clearnml'].finish()