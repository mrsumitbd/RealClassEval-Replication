from itertools import chain
from magi_attention.common.ranges import AttnRanges
from magi_attention.meta.container.slice import AttnSlice, MultiKAttnSlice
from dataclasses import dataclass

@dataclass
class HostRankEntry:
    """
    HostRankEntry is a dataclass that contains the host q/k ranges and the remote k ranges,
    it is a key data structure for calculating the remote rank entry.

    Args:
        host_q_ranges_global: global q ranges for this rank, merged
        host_k_ranges_global: global k ranges for this rank, merged

        attn_calc_slice_global_list: contains all slices to be calculated on this rank,
            including all slices from both host_stage and remote_stage
        attn_calc_host_slice_local_list: slices that need to be calculated in the host_stage

        remote_k_ranges_global: global remote k ranges for this rank, merged
        remote_k_ranges_global_per_chunk: global remote k ranges for each chunk,
            these are the k ranges needed by the attn slices in this chunk.
            the remote_k_ranges_global for each chunk is merged
        attn_calc_remote_slice_list_per_chunk: contains slices that need to be calculated for each chunk
    """
    host_q_ranges_global: AttnRanges
    host_k_ranges_global: AttnRanges
    attn_calc_slice_global_list: list[AttnSlice]
    attn_calc_host_slice_local_list: list[AttnSlice]
    remote_k_ranges_global: AttnRanges
    remote_k_ranges_global_per_chunk: list[AttnRanges]
    attn_calc_remote_slice_list_per_chunk: list[list[MultiKAttnSlice]]

    def __post_init__(self):
        assert len(self.remote_k_ranges_global_per_chunk) == len(self.attn_calc_remote_slice_list_per_chunk), f'The number of chunks is inconsistent: len(self.remote_k_ranges_global_per_chunk)={len(self.remote_k_ranges_global_per_chunk)!r}, len(self.attn_calc_remote_slice_list_per_chunk)={len(self.attn_calc_remote_slice_list_per_chunk)!r}'

    def get_host_calc_area(self) -> int:
        """Get the host calc area"""
        return sum((attn_slice.area for attn_slice in self.attn_calc_host_slice_local_list))

    def get_remote_calc_area(self, chunk_idx: int | None=None) -> int:
        """Get the remote calc area (w.r.t. a specific chunk)"""
        if chunk_idx is None:
            return sum((attn_slice.area for attn_slice in chain(*self.attn_calc_remote_slice_list_per_chunk)))
        return sum((attn_slice.area for attn_slice in self.attn_calc_remote_slice_list_per_chunk[chunk_idx]))

    def get_remote_comm_size(self, chunk_idx: int | None=None) -> int:
        """Get the remote comm size (w.r.t. a specific chunk)"""
        if chunk_idx is None:
            return sum((remote_k_ranges.total_seqlen for remote_k_ranges in self.remote_k_ranges_global_per_chunk))
        return self.remote_k_ranges_global_per_chunk[chunk_idx].total_seqlen