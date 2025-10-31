from exps.dist_attn.benchmark.utils import generate_seqlen_for_one_time, generate_seqlens, seqlens2cu_seqlens, varlen_long_seqlen_distribution, varlen_short_seqlen_distribution
from exps.dist_attn.benchmark.enums import FlashMaskType
import random

class MaskIterator:
    """This is a iterator for multiple flash masks, it can be used with
    several params in init and get an iterator,
    """

    def __init__(self, generate_times: int, generate_mask: FlashMaskType, total_seqlen: int, distribution: dict[tuple[int, int], float] | None=None, to_attn_ranges: bool=True, seed: int | None=None):
        self.generate_times = generate_times
        self.current_times = 0
        self.generate_mask = generate_mask
        self.total_seqlen = total_seqlen
        self.to_attn_ranges = to_attn_ranges
        if distribution is not None:
            self.seqlen_distribution = distribution
        elif self.total_seqlen > 128 * 1024:
            self.seqlen_distribution = varlen_long_seqlen_distribution()
        else:
            self.seqlen_distribution = varlen_short_seqlen_distribution()
        if seed is not None:
            self.random_number_generator = random.Random(seed)
        else:
            self.random_number_generator = None
        self.mask_generator = MaskGenerator()

    def __iter__(self):
        assert self.generate_times > 0, f'generate times must greater than 0, but got {self.generate_times}'
        return self

    def __next__(self):
        if self.current_times >= self.generate_times:
            raise StopIteration
        value = self.mask_generator.generate(flash_mask_type=self.generate_mask, seqlen_distribute=self.seqlen_distribution, total_seqlen=self.total_seqlen, to_attn_ranges=self.to_attn_ranges, rng=self.random_number_generator)
        self.current_times += 1
        return value