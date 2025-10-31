class NBlockRegionPicker:
    """Choose nblock regions reasonably spaced across chromosomes.

    This avoids excessively large blocks and also large numbers of tiny blocks
    by splitting to a defined number of blocks.

    Assumes to be iterating over an ordered input file and needs re-initiation
    with each new file processed as it keeps track of previous blocks to
    maintain the splitting.
    """

    def __init__(self, ref_regions, config, min_n_size):
        self._end_buffer = 250 if min_n_size > 50 else 0
        self._chr_last_blocks = {}
        target_blocks = int(config['algorithm'].get('nomap_split_targets', 200))
        self._target_size = self._get_target_size(target_blocks, ref_regions)
        self._ref_sizes = {x.chrom: x.stop for x in ref_regions}

    def _get_target_size(self, target_blocks, ref_regions):
        size = 0
        for x in ref_regions:
            size += x.end - x.start
        return size // target_blocks

    def include_block(self, x):
        """Check for inclusion of block based on distance from previous.
        """
        last_pos = self._chr_last_blocks.get(x.chrom, 0)
        if last_pos <= self._end_buffer and x.stop >= self._ref_sizes.get(x.chrom, 0) - self._end_buffer:
            return True
        elif self._ref_sizes.get(x.chrom, 0) <= self._target_size:
            return False
        elif x.start - last_pos > self._target_size:
            self._chr_last_blocks[x.chrom] = x.stop
            return True
        else:
            return False

    def expand_block(self, feat):
        """Expand any blocks which are near the start or end of a contig.
        """
        chrom_end = self._ref_sizes.get(feat.chrom)
        if chrom_end:
            if feat.start < self._end_buffer:
                feat.start = 0
            if feat.stop >= chrom_end - self._end_buffer:
                feat.stop = chrom_end
        return feat