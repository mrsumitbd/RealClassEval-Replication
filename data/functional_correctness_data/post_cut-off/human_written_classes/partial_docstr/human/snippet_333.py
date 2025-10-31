import numpy as np
from typing import List, Dict, Any
import wandb

class ValidationTableManager:
    """Manages the validation table for wandb logging."""

    def __init__(self):
        self.validation_table = None

    def log_generations_to_wandb(self, log_rst: List[Dict[str, Any]], generations_to_log: int, global_steps: int=0) -> None:
        """Log a table of validation samples."""
        if generations_to_log <= 0:
            return
        if wandb.run is None:
            logger.warning('`val_generations_to_log_to_wandb` is set, but wandb is not initialized')
            return
        inputs = []
        outputs = []
        scores = []
        images = []
        for item in log_rst:
            inputs.append(item['config_id'])
            outputs.append(item['output_str'])
            scores.append(item['metrics']['score'])
            images.append(item.get('image_data', None))
        has_images = any((img_list for img_list in images if img_list))
        if has_images:
            max_images_per_sample = max((len(img_list) if img_list else 0 for img_list in images))
        else:
            max_images_per_sample = 0
        if has_images:
            samples = list(zip(inputs, outputs, scores, images))
        else:
            samples = list(zip(inputs, outputs, scores))
        samples.sort(key=lambda x: x[0])
        rng = np.random.RandomState(42)
        rng.shuffle(samples)
        samples = samples[:generations_to_log]
        if has_images:
            columns = ['input', 'output', 'score'] + [f'image_{i + 1}' for i in range(max_images_per_sample)]
        else:
            columns = ['input', 'output', 'score']
        table = wandb.Table(columns=columns)
        for sample in samples:
            if has_images:
                input_text, output_text, score, sample_images = sample
                wandb_images = []
                if sample_images:
                    for img in sample_images:
                        if img is not None:
                            if not isinstance(img, wandb.Image):
                                img = wandb.Image(img)
                            wandb_images.append(img)
                while len(wandb_images) < max_images_per_sample:
                    wandb_images.append(None)
                table.add_data(input_text, output_text, score, *wandb_images)
            else:
                input_text, output_text, score = sample
                table.add_data(input_text, output_text, score)
        wandb.log({'table': table}, step=global_steps)