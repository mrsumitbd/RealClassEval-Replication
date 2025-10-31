from torch import nn

class GraphContainer:
    """Container for managing graphs for different batch sizes (CUDA graphs on NVIDIA, regular on others)."""

    def __init__(self, model: nn.Module, seq_length: int):
        self.model = model
        self.seq_length = seq_length
        self.graphs: dict[int, GraphWrapper] = {}

    def get_or_create(self, batch_size: int) -> 'GraphWrapper':
        if batch_size not in self.graphs:
            self.graphs[batch_size] = GraphWrapper(self.model, batch_size, self.seq_length)
        return self.graphs[batch_size]