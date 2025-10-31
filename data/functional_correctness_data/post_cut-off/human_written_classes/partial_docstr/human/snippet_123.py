from torch import nn
import torch

class GraphWrapper:
    """Wrapper for graph capture and replay (CUDA graphs on NVIDIA, regular on others)."""

    def __init__(self, model: nn.Module, batch_size: int, seq_length: int):
        self.model = model
        self.device = self._get_device()
        self.static_input = self._create_random_batch(batch_size, seq_length)
        self.static_attention_mask = torch.ones_like(self.static_input)
        self._warmup()
        if torch.cuda.is_available() and hasattr(torch.cuda, 'CUDAGraph'):
            self.graph = torch.cuda.CUDAGraph()
            with torch.cuda.graph(self.graph):
                self.static_output = self.model(input_ids=self.static_input, attention_mask=self.static_attention_mask)
            self.use_cuda_graph = True
        else:
            self.use_cuda_graph = False
            self.static_output = None

    def _get_device(self) -> str:
        if torch.cuda.is_available():
            return 'cuda'
        elif torch.backends.mps.is_available():
            return 'mps'
        else:
            return 'cpu'

    def _create_random_batch(self, batch_size: int, seq_length: int) -> torch.Tensor:
        return torch.randint(0, 1000, (batch_size, seq_length), device=self.device, dtype=torch.long)

    def _warmup(self, num_warmup: int=3):
        with torch.no_grad():
            for _ in range(num_warmup):
                self.model(input_ids=self.static_input, attention_mask=self.static_attention_mask)

    def __call__(self, input_ids: torch.Tensor, attention_mask: torch.Tensor) -> torch.Tensor:
        if self.use_cuda_graph:
            self.static_input.copy_(input_ids)
            self.static_attention_mask.copy_(attention_mask)
            self.graph.replay()
            return self.static_output
        else:
            return self.model(input_ids=input_ids, attention_mask=attention_mask)