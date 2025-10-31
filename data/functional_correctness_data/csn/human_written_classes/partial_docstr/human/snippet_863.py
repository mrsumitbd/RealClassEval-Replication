class ISA:

    @staticmethod
    def get_isa(isa='x86'):
        if isa.lower() == 'x86':
            return x86
        elif isa.lower() == 'aarch64':
            return AArch64

    @staticmethod
    def compute_block_metric(block):
        """Compute sortable metric to rank blocks."""
        return NotImplementedError

    @classmethod
    def select_best_block(cls, blocks):
        """
        Return best block label selected based on simple heuristic.

        :param blocks: OrderedDict map of label to list of instructions
        """
        if not blocks:
            raise ValueError('No suitable blocks were found in assembly.')
        best_block_label = next(iter(blocks))
        best_metric = cls.compute_block_metric(blocks[best_block_label])
        for label, block in list(blocks.items())[1:]:
            metric = cls.compute_block_metric(block)
            if best_metric < metric:
                best_block_label = label
                best_metric = metric
        return best_block_label

    @staticmethod
    def get_pointer_increment(block):
        """Return pointer increment."""
        raise NotImplementedError