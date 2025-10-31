from pathlib import Path
import dataclasses
from loguru import logger

@dataclasses.dataclass
class ValidationGenerationsLogger:

    def log(self, loggers, samples, step):
        if 'wandb' in loggers:
            self.log_generations_to_wandb(samples, step)
        if 'swanlab' in loggers:
            self.log_generations_to_swanlab(samples, step)
        if 'mlflow' in loggers:
            self.log_generations_to_mlflow(samples, step)

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