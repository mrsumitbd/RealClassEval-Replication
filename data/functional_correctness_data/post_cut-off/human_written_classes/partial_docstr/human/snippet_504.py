from torch import Tensor, nn
from typing import Optional
from dataclasses import dataclass
import torch

@dataclass
class T3Cond:
    """
    Dataclass container for most / all conditioning info.

    TODO: serialization methods aren't used, keeping them around for convenience
    """
    speaker_emb: Tensor
    clap_emb: Optional[Tensor] = None
    cond_prompt_speech_tokens: Optional[Tensor] = None
    cond_prompt_speech_emb: Optional[Tensor] = None
    emotion_adv: Optional[Tensor] = 0.5

    def to(self, *, device=None, dtype=None):
        """Cast to a device and dtype. Dtype casting is ignored for long/int tensors."""
        for k, v in self.__dict__.items():
            if torch.is_tensor(v):
                is_fp = type(v.view(-1)[0].item()) is not int
                setattr(self, k, v.to(device=device, dtype=dtype if is_fp else None))
        return self

    def save(self, fpath):
        torch.save(self.__dict__, fpath)

    @staticmethod
    def load(fpath, map_location='cpu'):
        kwargs = torch.load(fpath, map_location=map_location, weights_only=True)
        return T3Cond(**kwargs)