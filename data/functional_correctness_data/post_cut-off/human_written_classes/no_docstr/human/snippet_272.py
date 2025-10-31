from loguru import logger

class ClearMLLogger:

    def __init__(self, project_name: str, experiment_name: str, config):
        self.project_name = project_name
        self.experiment_name = experiment_name
        import clearml
        self._task: clearml.Task = clearml.Task.init(task_name=experiment_name, project_name=project_name, continue_last_task=True, output_uri=False)
        self._task.connect_configuration(config, name='Hyperparameters')

    def _get_logger(self):
        return self._task.get_logger()

    def log(self, data, step):
        import numpy as np
        import pandas as pd
        logger = self._get_logger()
        for k, v in data.items():
            title, series = k.split('/', 1)
            if isinstance(v, (int, float, np.floating, np.integer)):
                logger.report_scalar(title=title, series=series, value=v, iteration=step)
            elif isinstance(v, pd.DataFrame):
                logger.report_table(title=title, series=series, table_plot=v, iteration=step)
            else:
                logger.warning(f'''Trainer is attempting to log a value of "{v}" of type {type(v)} for key "{k}". This invocation of ClearML logger's function is incorrect so this attribute was dropped. ''')

    def finish(self):
        self._task.mark_completed()