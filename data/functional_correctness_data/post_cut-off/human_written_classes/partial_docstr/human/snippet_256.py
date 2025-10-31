from magi_attention.common.ranges import AttnRanges
from magi_attention.common.enum import AttnMaskType, AttnRole, AttnType
from dataclasses import dataclass
from magi_attention.meta.container.bucket import AttnBucket
import torch

@dataclass
class DispatchMeta:
    """The meta info of sequence dispatch for distributed attention

    Args:
        TODO: finish docstring

        max_valid_ids(int): the maximum valid token ids in the seqlen dim.

    NOTE: global_bucket
    """
    attn_role: AttnRole
    attn_type: AttnType
    attn_mask_type: list[AttnMaskType]
    ranges: AttnRanges
    batch_size: int
    total_seqlen: int
    shard_seqlen: int
    max_valid_ids: int
    chunk_size: int
    num_chunks: int
    cp_rank: int
    cp_size: int
    partitions: list[list[int]]
    partitions_perm_idxs: list[int]
    partitions_unperm_idxs: list[int]
    global_bucket: AttnBucket
    buckets_per_rank: list[AttnBucket]

    @property
    def host_ranges_per_rank(self) -> list[AttnRanges]:
        return [AttnRanges.from_ranges([[chunk_id * self.chunk_size, (chunk_id + 1) * self.chunk_size] for chunk_id in partition]) for partition in self.partitions]

    @property
    def position_ids(self) -> torch.Tensor:
        chunk_size = self.chunk_size
        local_partition = self.partitions[self.cp_rank]
        position_ids = torch.tensor([i for n in local_partition for i in range(n * chunk_size, (n + 1) * chunk_size)], device=torch.cuda.current_device())
        position_ids = position_ids.clamp(max=self.max_valid_ids - 1)
        return position_ids

    def __post_init__(self) -> None:
        assert len(self.partitions) == self.cp_size
        assert len(self.partitions_perm_idxs) == len(self.partitions_unperm_idxs) == self.num_chunks
        assert len(self.buckets_per_rank) == self.cp_size
        assert len(self.host_ranges_per_rank) == self.cp_size

    def __repr__(self, width: int=30) -> str:
        """Customized __repr__ method for BaseConfig,
        displaying all fields with their values in alphabetical order.
        """
        class_name = self.__class__.__name__
        repr_str = f"{'*' * width}   {class_name}   {'*' * width}\n"
        title_len = len(repr_str) - 1
        field_names = sorted(self.__dataclass_fields__.keys())
        for field_name in field_names:
            field_value = getattr(self, field_name)
            if isinstance(field_value, str):
                field_value = repr(field_value)
            repr_str += f'{field_name}: {field_value}\n'
        repr_str += f"{'*' * title_len}\n"
        return repr_str