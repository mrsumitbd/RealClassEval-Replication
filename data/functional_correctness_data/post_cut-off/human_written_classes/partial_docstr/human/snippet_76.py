from typing import Optional

class MetricsWandBSink:
    """
    Training metrics via W&B.

    Args:
        output_dir (str): Directory where W&B logs will be written locally.
        project (str, optional): Associate this training run with a W&B project. If None, W&B will generate a name based on the git repo name.
        run (str, optional): W&B run name. If None, W&B will generate a random name.
        config (dict, optional): Input parameters, like hyperparameters or data preprocessing settings for the run for later comparison.
    """

    def __init__(self, output_dir: str, project: Optional[str]=None, run: Optional[str]=None, config: Optional[dict]=None):
        self.output_dir = output_dir
        if wandb:
            self.run = wandb.init(project=project, name=run, config=config, dir=output_dir)
            print(f'W&B logging initialized. To monitor logs, open {wandb.run.url}.')
        else:
            self.run = None
            print("Unable to initialize W&B. Logging is turned off for this session. Run 'pip install wandb' to enable logging.")

    def update(self, values: dict):
        if not wandb or not self.run:
            return
        epoch = values['epoch']
        log_dict = {'epoch': epoch}
        if 'train_loss' in values:
            log_dict['Loss/Train'] = values['train_loss']
        if 'test_loss' in values:
            log_dict['Loss/Test'] = values['test_loss']
        if 'test_coco_eval_bbox' in values:
            coco_eval = values['test_coco_eval_bbox']
            ap50_90 = safe_index(coco_eval, 0)
            ap50 = safe_index(coco_eval, 1)
            ar50_90 = safe_index(coco_eval, 8)
            if ap50_90 is not None:
                log_dict['Metrics/Base/AP50_90'] = ap50_90
            if ap50 is not None:
                log_dict['Metrics/Base/AP50'] = ap50
            if ar50_90 is not None:
                log_dict['Metrics/Base/AR50_90'] = ar50_90
        if 'ema_test_coco_eval_bbox' in values:
            ema_coco_eval = values['ema_test_coco_eval_bbox']
            ema_ap50_90 = safe_index(ema_coco_eval, 0)
            ema_ap50 = safe_index(ema_coco_eval, 1)
            ema_ar50_90 = safe_index(ema_coco_eval, 8)
            if ema_ap50_90 is not None:
                log_dict['Metrics/EMA/AP50_90'] = ema_ap50_90
            if ema_ap50 is not None:
                log_dict['Metrics/EMA/AP50'] = ema_ap50
            if ema_ar50_90 is not None:
                log_dict['Metrics/EMA/AR50_90'] = ema_ar50_90
        wandb.log(log_dict)

    def close(self):
        if not wandb or not self.run:
            return
        self.run.finish()