from pruna.data.pruna_datamodule import PrunaDataModule
import torch
from pruna.evaluation.metrics.metric_base import BaseMetric
from pruna.evaluation.metrics.metric_stateful import StatefulMetric
from typing import Any, List, cast
from pruna.engine.utils import set_to_best_available_device

class Task:
    """
    Processes user requests and converts them into a format that the evaluation module can handle.

    Parameters
    ----------
    request : str | List[str | BaseMetric | StatefulMetric]
        The user request.
    datamodule : PrunaDataModule
        The dataloader to use for the evaluation.
    device : str | torch.device | None, optional
        The device to be used, e.g., 'cuda' or 'cpu'. Default is None.
        If None, the best available device will be used.
    """

    def __init__(self, request: str | List[str | BaseMetric | StatefulMetric], datamodule: PrunaDataModule, device: str | torch.device | None=None) -> None:
        device = set_to_best_available_device(device)
        self.metrics = get_metrics(request, device)
        self.datamodule = datamodule
        self.dataloader = datamodule.test_dataloader()
        if device not in ['cpu', 'mps'] and (not device.startswith('cuda')):
            raise ValueError(f'Unsupported device: {device}. Must be one of: cuda, cpu, mps.')
        self.device = device

    def get_single_stateful_metrics(self) -> List[StatefulMetric]:
        """
        Get single stateful metrics.

        Returns
        -------
        List[StatefulMetric]
            The stateful metrics.
        """
        return [metric for metric in self.metrics if isinstance(metric, StatefulMetric) and (not metric.is_pairwise())]

    def get_pairwise_stateful_metrics(self) -> List[StatefulMetric]:
        """
        Get pairwise stateful metrics.

        Returns
        -------
        List[StatefulMetric]
            The pairwise metrics.
        """
        return [metric for metric in self.metrics if isinstance(metric, StatefulMetric) and metric.is_pairwise()]

    def get_stateless_metrics(self) -> List[Any]:
        """
        Get stateless metrics.

        Returns
        -------
        List[Any]
            The stateless metrics.
        """
        return [metric for metric in self.metrics if not isinstance(metric, StatefulMetric)]

    def is_pairwise_evaluation(self) -> bool:
        """
        Check if the evaluation task is pairwise.

        Returns
        -------
        bool
            True if the task is pairwise, False otherwise.
        """
        return any((metric.is_pairwise() for metric in self.metrics if isinstance(metric, StatefulMetric)))