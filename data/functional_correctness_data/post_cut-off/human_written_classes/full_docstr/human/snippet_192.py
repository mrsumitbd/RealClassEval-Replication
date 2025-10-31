from collections import defaultdict
import torch
import torch.distributed as dist
from siirl.utils.extras.device import get_device_id, get_device_name, device_synchronize
from typing import Any, Dict, List, Optional, Tuple, Union

class DistributedMetricAggregator:
    """
    A helper class to encapsulate the logic for aggregating metrics
    in a distributed environment.
    """

    def __init__(self, local_metrics: Dict[str, Union[float, List[float], torch.Tensor]], group: Optional[dist.ProcessGroup]):
        """
        Initializes the aggregator and prepares metrics for reduction.

        Args:
            local_metrics: The dictionary of metrics on the local rank.
            group: The process group for distributed communication.
        """
        self.group = group
        device_name = get_device_name()
        if device_name in ['cuda', 'npu']:
            self.device = f'{device_name}:{get_device_id()}'
        else:
            self.device = 'cpu'
        self.op_buckets = self._bucket_local_metrics(local_metrics)

    def _bucket_local_metrics(self, metrics: Dict) -> defaultdict:
        """
        Parses local metrics and groups them by the required reduction operation.
        This step also performs local pre-aggregation on lists and tensors.
        This version correctly handles multi-element tensors as input.

        Returns:
            A defaultdict containing keys and pre-aggregated values,
            grouped by reduction operation type (_ReduceOp).
        """
        buckets = defaultdict(list)
        for key in sorted(metrics.keys()):
            value = metrics[key]
            is_list = isinstance(value, list)
            is_tensor = isinstance(value, torch.Tensor)
            if '_max' in key:
                op_type = _ReduceOp.MAX
                if is_tensor:
                    local_val = torch.max(value).item() if value.numel() > 0 else 0.0
                elif is_list:
                    local_val = max(value) if value else 0.0
                else:
                    local_val = value
                buckets[op_type].append((key, local_val))
            elif '_min' in key:
                op_type = _ReduceOp.MIN
                if is_tensor:
                    local_val = torch.min(value).item() if value.numel() > 0 else 0.0
                elif is_list:
                    local_val = min(value) if value else 0.0
                else:
                    local_val = value
                buckets[op_type].append((key, local_val))
            else:
                op_type = _ReduceOp.SUM
                if is_tensor:
                    local_sum = torch.sum(value).item()
                    local_count = value.numel()
                elif is_list:
                    local_sum = sum(value) if value else 0.0
                    local_count = len(value)
                else:
                    local_sum = value
                    local_count = 1
                buckets[op_type].append((key, (local_sum, local_count)))
        return buckets

    def aggregate_and_get_results(self) -> Dict[str, float]:
        """
        Performs the distributed all_reduce operations and composes the final
        metrics dictionary.

        Returns:
            A dictionary with the globally aggregated metrics.
        """
        final_metrics = {}
        for op_type, data in self.op_buckets.items():
            if not data:
                continue
            keys, values = zip(*data)
            if op_type == _ReduceOp.SUM:
                sums, counts = zip(*values)
                sum_tensor = torch.tensor(sums, dtype=torch.float32, device=self.device)
                count_tensor = torch.tensor(counts, dtype=torch.float32, device=self.device)
                if self.group is not None:
                    dist.all_reduce(sum_tensor, op=op_type.value, group=self.group)
                    dist.all_reduce(count_tensor, op=op_type.value, group=self.group)
                global_sums = sum_tensor.cpu().numpy()
                global_counts = count_tensor.cpu().numpy()
                for i, key in enumerate(keys):
                    final_metrics[key] = global_sums[i] / global_counts[i] if global_counts[i] > 0 else 0.0
            else:
                value_tensor = torch.tensor(values, dtype=torch.float32, device=self.device)
                if self.group is not None:
                    dist.all_reduce(value_tensor, op=op_type.value, group=self.group)
                global_values = value_tensor.cpu().numpy()
                for i, key in enumerate(keys):
                    final_metrics[key] = global_values[i]
        return final_metrics