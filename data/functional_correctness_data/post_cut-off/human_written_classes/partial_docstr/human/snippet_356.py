from pathlib import Path
from loguru import logger
import dataclasses
import os

@dataclasses.dataclass
class ValidationGenerationsLogger:

    def log(self, loggers, samples, step):
        if 'wandb' in loggers:
            self.log_generations_to_wandb(samples, step)
        if 'swanlab' in loggers:
            self.log_generations_to_swanlab(samples, step)
        if 'mlflow' in loggers:
            self.log_generations_to_mlflow(samples, step)
        if 'clearml' in loggers:
            self.log_generations_to_clearml(samples, step)
        if 'tensorboard' in loggers:
            self.log_generations_to_tensorboard(samples, step)

    def log_generations_to_wandb(self, samples, step):
        """Log samples to wandb as a table"""
        import wandb
        columns = ['step'] + sum([[f'input_{i + 1}', f'output_{i + 1}', f'score_{i + 1}'] for i in range(len(samples))], [])
        if not hasattr(self, 'validation_table'):
            self.validation_table = wandb.Table(columns=columns)
        new_table = wandb.Table(columns=columns, data=self.validation_table.data)
        row_data = []
        row_data.append(step)
        for sample in samples:
            row_data.extend(sample)
        new_table.add_data(*row_data)
        wandb.log({'val/generations': new_table}, step=step)
        self.validation_table = new_table

    def log_generations_to_swanlab(self, samples, step):
        """Log samples to swanlab as text"""
        import swanlab
        swanlab_text_list = []
        for i, sample in enumerate(samples):
            row_text = f'\n            input: {sample[0]}\n            \n            ---\n            \n            output: {sample[1]}\n            \n            ---\n            \n            score: {sample[2]}\n            '
            swanlab_text_list.append(swanlab.Text(row_text, caption=f'sample {i + 1}'))
        swanlab.log({'val/generations': swanlab_text_list}, step=step)

    def log_generations_to_mlflow(self, samples, step):
        """Log validation generation to mlflow as artifacts"""
        import json
        import tempfile
        import mlflow
        try:
            with tempfile.TemporaryDirectory() as tmp_dir:
                validation_gen_step_file = Path(tmp_dir, f'val_step{step}.json')
                row_data = []
                for sample in samples:
                    data = {'input': sample[0], 'output': sample[1], 'score': sample[2]}
                    row_data.append(data)
                with open(validation_gen_step_file, 'w') as file:
                    json.dump(row_data, file)
                mlflow.log_artifact(validation_gen_step_file)
        except Exception as e:
            logger.warning(f'save validation generation file to mlflow failed with error {e}')

    def log_generations_to_clearml(self, samples, step):
        """Log validation generation to clearml as table"""
        import clearml
        import pandas as pd
        task: clearml.Task | None = clearml.Task.current_task()
        if task is None:
            return
        table = [{'step': step, 'input': sample[0], 'output': sample[1], 'score': sample[2]} for sample in samples]
        logger = task.get_logger()
        logger.report_table(series='Validation generations', title='Validation', table_plot=pd.DataFrame.from_records(table), iteration=step)

    def log_generations_to_tensorboard(self, samples, step):
        """Log samples to tensorboard as text"""
        if not hasattr(self, 'writer'):
            from torch.utils.tensorboard import SummaryWriter
            tensorboard_dir = os.environ.get('TENSORBOARD_DIR', 'tensorboard_log')
            os.makedirs(tensorboard_dir, exist_ok=True)
            self.writer = SummaryWriter(log_dir=tensorboard_dir)
        text_content = f'**Generation Results - Step {step}**\n\n'
        for i, sample in enumerate(samples):
            text_content += f'### Sample {i + 1}\n'
            if len(sample) >= 3:
                input_text, output_text, score = (sample[0], sample[1], sample[2])
                text_content += f'**Input:** {input_text}\n\n'
                text_content += f'**Output:** {output_text}\n\n'
                text_content += f'**Score:** {score}\n\n'
            else:
                text_content += f'**Data:** {sample}\n\n'
            text_content += '---\n\n'
        self.writer.add_text('val/generations', text_content, step)
        self.writer.flush()