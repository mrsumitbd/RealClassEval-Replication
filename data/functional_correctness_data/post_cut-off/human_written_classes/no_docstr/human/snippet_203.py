import torch
import magi_attention
from dataclasses import dataclass
from magi_attention.common import AttnRanges

@dataclass(repr=False)
class AttnArg:
    q_ranges: AttnRanges
    k_ranges: AttnRanges
    attn_type_map: list[int]
    shard_seqlen_q: int
    total_area: int = -1

    def __post_init__(self):
        assert len(self.q_ranges) == len(self.k_ranges) == len(self.attn_type_map), f'len(self.q_ranges)={len(self.q_ranges)!r}, len(self.k_ranges)={len(self.k_ranges)!r}, len(self.attn_type_map)={len(self.attn_type_map)!r}'
        self._filter_out_empty_slice()
        self._init_ffa_fwd_args_dict()
        self._init_ffa_bwd_args_dict()

    def _filter_out_empty_slice(self) -> None:
        filtered_q_ranges = AttnRanges()
        filtered_k_ranges = AttnRanges()
        filtered_attn_type_map: list[int] = []
        for q_range, k_range, attn_type_map in zip(self.q_ranges, self.k_ranges, self.attn_type_map):
            if not k_range.is_empty():
                filtered_q_ranges.append(q_range)
                filtered_k_ranges.append(k_range)
                filtered_attn_type_map.append(attn_type_map)
        self.q_ranges, self.k_ranges, self.attn_type_map = (filtered_q_ranges, filtered_k_ranges, filtered_attn_type_map)
        if magi_attention.is_sanity_check_enable():
            assert len(self.q_ranges) == len(self.k_ranges) == len(self.attn_type_map)
            for k_range in self.k_ranges:
                assert not k_range.is_empty()

    def _init_ffa_fwd_args_dict(self) -> None:
        batch_size_fwd = len(self.q_ranges)
        self.skip_attn_fwd = batch_size_fwd == 0
        self.disable_fwd_atomic_reduction = self.q_ranges.is_non_overlap()
        q_ranges_tensor_fwd = self.q_ranges.to_tensor(device=torch.cuda.current_device())
        k_ranges_tensor_fwd = self.k_ranges.to_tensor(device=torch.cuda.current_device())
        mask_type_tensor_fwd = torch.tensor(self.attn_type_map, dtype=torch.int32, device=torch.cuda.current_device())
        if magi_attention.is_sanity_check_enable():
            if not self.skip_attn_fwd:
                assert q_ranges_tensor_fwd.shape == torch.Size([batch_size_fwd, 2])
                assert k_ranges_tensor_fwd.shape == torch.Size([batch_size_fwd, 2])
                assert mask_type_tensor_fwd.shape == torch.Size([batch_size_fwd])
        if self.skip_attn_fwd:
            max_seqlen_q_fwd = 0
            max_seqlen_k_fwd = 0
        else:
            max_seqlen_q_fwd = self.q_ranges.max_seqlen
            max_seqlen_k_fwd = self.k_ranges.max_seqlen
        self.ffa_fwd_args_dict = dict(q_ranges=q_ranges_tensor_fwd, k_ranges=k_ranges_tensor_fwd, attn_type_map=mask_type_tensor_fwd, max_seqlen_q=max_seqlen_q_fwd, max_seqlen_k=max_seqlen_k_fwd)

    def _init_ffa_bwd_args_dict(self) -> None:
        self.skip_attn_bwd = self.skip_attn_fwd
        self.q_ranges_bwd = self.q_ranges
        self.k_ranges_bwd = self.k_ranges
        self.attn_type_map_bwd = self.attn_type_map
        self.ffa_bwd_args_dict = self.ffa_fwd_args_dict
        self.disable_bwd_dkv_atomic_reduction = False

    def to_ffa_args(self, is_bwd: bool=False) -> dict:
        return self.ffa_bwd_args_dict if is_bwd else self.ffa_fwd_args_dict

    def can_skip(self, is_bwd: bool=False) -> bool:
        return self.skip_attn_bwd if is_bwd else self.skip_attn_fwd

    def __repr__(self) -> str:
        return f'AttnArg(q_ranges={self.q_ranges}, k_ranges={self.k_ranges}, attn_type_map={self.attn_type_map}, shard_seqlen_q={self.shard_seqlen_q}, total_area={self.total_area}'