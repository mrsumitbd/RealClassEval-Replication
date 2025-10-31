class MetricsTensorBoardSink:
    """
    Training metrics via TensorBoard.

    Args:
        output_dir (str): Directory where TensorBoard logs will be written.
    """

    def __init__(self, output_dir: str):
        if SummaryWriter:
            self.writer = SummaryWriter(log_dir=output_dir)
            print(f"TensorBoard logging initialized. To monitor logs, use 'tensorboard --logdir {output_dir}' and open http://localhost:6006/ in browser.")
        else:
            self.writer = None
            print("Unable to initialize TensorBoard. Logging is turned off for this session.  Run 'pip install tensorboard' to enable logging.")

    def update(self, values: dict):
        if not self.writer:
            return
        epoch = values['epoch']
        if 'train_loss' in values:
            self.writer.add_scalar('Loss/Train', values['train_loss'], epoch)
        if 'test_loss' in values:
            self.writer.add_scalar('Loss/Test', values['test_loss'], epoch)
        if 'test_coco_eval_bbox' in values:
            coco_eval = values['test_coco_eval_bbox']
            ap50_90 = safe_index(coco_eval, 0)
            ap50 = safe_index(coco_eval, 1)
            ar50_90 = safe_index(coco_eval, 8)
            if ap50_90 is not None:
                self.writer.add_scalar('Metrics/Base/AP50_90', ap50_90, epoch)
            if ap50 is not None:
                self.writer.add_scalar('Metrics/Base/AP50', ap50, epoch)
            if ar50_90 is not None:
                self.writer.add_scalar('Metrics/Base/AR50_90', ar50_90, epoch)
        if 'ema_test_coco_eval_bbox' in values:
            ema_coco_eval = values['ema_test_coco_eval_bbox']
            ema_ap50_90 = safe_index(ema_coco_eval, 0)
            ema_ap50 = safe_index(ema_coco_eval, 1)
            ema_ar50_90 = safe_index(ema_coco_eval, 8)
            if ema_ap50_90 is not None:
                self.writer.add_scalar('Metrics/EMA/AP50_90', ema_ap50_90, epoch)
            if ema_ap50 is not None:
                self.writer.add_scalar('Metrics/EMA/AP50', ema_ap50, epoch)
            if ema_ar50_90 is not None:
                self.writer.add_scalar('Metrics/EMA/AR50_90', ema_ar50_90, epoch)
        self.writer.flush()

    def close(self):
        if not self.writer:
            return
        self.writer.close()