from magi_attention.common.enum import AttnMaskType
from dataclasses import dataclass
from magi_attention.common.range import AttnRange
from magi_attention.common.ranges import AttnRanges

@dataclass(repr=False)
class MultiKAttnSlice:
    q_range: AttnRange
    k_ranges: AttnRanges
    mask_types: list[AttnMaskType]
    slice_id: int | None = None
    _area: int | None = None

    @property
    def area(self) -> int:
        if self._area is None:
            self._area = 0
            for k_range, mask_type in zip(self.k_ranges._ranges, self.mask_types):
                if mask_type is AttnMaskType.FULL:
                    self._area += self.q_range.seqlen * k_range.seqlen
                elif mask_type is AttnMaskType.CAUSAL or mask_type is AttnMaskType.INVCAUSAL:
                    if k_range.seqlen > self.q_range.seqlen:
                        self._area += (2 * k_range.seqlen - self.q_range.seqlen + 1) * self.q_range.seqlen // 2
                    else:
                        self._area += (1 + k_range.seqlen) * k_range.seqlen // 2
                elif mask_type is AttnMaskType.BICAUSAL:
                    self._area = (k_range.seqlen - self.q_range.seqlen + 1) * self.q_range.seqlen
                else:
                    raise ValueError(f"Only support 'full', 'causal', 'inv_causal' and 'bi_causal' mask, but got {mask_type} in mask_types.")
        return self._area

    @area.setter
    def area(self, area: int):
        self._area = area

    def __post_init__(self):
        assert len(self.mask_types) == len(self.k_ranges), f'The length of mask_types and k_ranges should be the same, but got {len(self.mask_types)} and {len(self.k_ranges)}'

    def __repr__(self) -> str:
        return f'MultiKAttnSlice(slice_id={self.slice_id}, q_range={self.q_range}, k_ranges={self.k_ranges}, mask_types={self.mask_types}, area={self.area})'