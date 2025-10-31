import torch

class TorchStreamWrapper:

    def __init__(self, pt_stream: torch.cuda.Stream):
        self.pt_stream = pt_stream
        self.handle = pt_stream.cuda_stream

    def __cuda_stream__(self):
        stream_id = self.pt_stream.cuda_stream
        return (0, stream_id)