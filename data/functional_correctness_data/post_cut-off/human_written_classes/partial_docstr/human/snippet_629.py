import numpy as np
import json
import torch.fx as fx
from typing import Dict, List, Optional, Tuple
import logging
from wave_lang.kernel.wave.tuner.utils import enum_to_str, format_latency_us, latency_to_us
from pathlib import Path

class TuningLogger:
    """Custom logger for the optimization process."""

    def __init__(self, logger: logging.Logger, schedules_dir: Path):
        self.logger = logger
        self.schedules_dir = schedules_dir
        self.best_latency = float('inf')
        self.best_iteration = -1
        self.history = []
        self.current_iteration = 0
        self.graph = None
        self.initiation_interval = None
        self.num_stages = None
        self.resource_reservations = None
        self.resource_names = None
        self.original_schedule_file = None

    def set_schedule_params(self, graph: fx.Graph, initiation_interval: int, num_stages: int, resource_reservations: Optional[np.ndarray]=None, resource_names: Optional[list[str]]=None, original_schedule_file: Optional[str]=None) -> None:
        """Set parameters needed for saving schedules in schedule file format.

        Args:
            graph: FX graph for schedule file format
            initiation_interval: Initiation interval for schedule file format
            num_stages: Number of stages for schedule file format
            resource_reservations: Optional resource reservations for schedule file format
            resource_names: Optional resource names for schedule file format
            original_schedule_file: Optional original schedule file to preserve structure
        """
        self.graph = graph
        self.initiation_interval = initiation_interval
        self.num_stages = num_stages
        self.resource_reservations = resource_reservations
        self.resource_names = resource_names
        self.original_schedule_file = original_schedule_file

    def log_iteration(self, iteration: int, schedule: Dict, latency: float, is_improvement: bool) -> None:
        """Log an optimization iteration and save the schedule.

        Args:
            iteration: Current iteration number
            schedule: Current schedule
            latency: Achieved latency
            is_improvement: Whether this is an improvement
        """
        schedule_filename = f'schedule_{iteration:04d}'
        save_schedule(schedule, latency, iteration, self.schedules_dir, self.logger, self.graph, self.initiation_interval, self.num_stages, self.resource_reservations, self.resource_names, self.original_schedule_file)
        self.history.append({'iteration': int(iteration), 'latency_us': float(latency_to_us(latency)), 'is_improvement': bool(is_improvement), 'schedule_file': str(f'{schedule_filename}.json'), 'schedule_txt_file': str(f'{schedule_filename}.txt')})
        if is_improvement:
            self.best_latency = latency
            self.best_iteration = iteration
            self.logger.info(f'Iteration {iteration}: Found improvement! Latency: {format_latency_us(latency)}')
        else:
            self.logger.debug(f'Iteration {iteration}: No improvement. Latency: {format_latency_us(latency)}')

    def log_summary(self) -> None:
        """Log a summary of the tuning process."""
        self.logger.info('\nTuning Summary:')
        self.logger.info(f'Best latency: {format_latency_us(self.best_latency)}')
        self.logger.info(f'Best iteration: {self.best_iteration}')
        self.logger.info(f'Total iterations: {len(self.history)}')
        history_file = self.schedules_dir.parent / 'tuning_history.json'
        with open(history_file, 'w') as f:
            json.dump(self.history, f, indent=2)
        self.logger.info(f'Tuning history saved to {history_file}')