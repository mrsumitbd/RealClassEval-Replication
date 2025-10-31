import torch
from torch.distributed.device_mesh import DeviceMesh
from dataclasses import dataclass

@dataclass
class GroupCollectiveArg:
    """The native args for group cast/reduce collective"""
    input_split_size_list: list[int]
    output_split_size_list: list[int]
    dst_indices_list: list[list[int]]
    src_index_list: list[int]
    rank: int
    world_size: int
    device_mesh: DeviceMesh | None = None
    deterministic: bool = False

    def __post_init__(self):
        self.device = torch.cuda.current_device()

    def to_group_cast_args(self) -> dict:
        return dict(input_split_size_list=self.input_split_size_list, output_split_size_list=self.output_split_size_list, dst_indices_list=self.dst_indices_list, src_index_list=self.src_index_list)

    def to_group_reduce_args(self) -> dict:
        return dict(input_split_size_list=self.output_split_size_list, output_split_size_list=self.input_split_size_list, dst_index_list=self.src_index_list, src_indices_list=self.dst_indices_list)