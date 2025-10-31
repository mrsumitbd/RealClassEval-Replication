import torch
from voicehub.models.dia.config import DiaConfig
from dataclasses import dataclass

@dataclass
class DecoderOutput:
    generated_tokens: torch.Tensor
    prefill_steps: list[int]

    @classmethod
    def new(cls, batch_size: int, config: DiaConfig, device: torch.device) -> 'DecoderOutput':
        max_audio_len = config.data.audio_length
        return cls(generated_tokens=torch.full((batch_size, max_audio_len, config.data.channels), fill_value=-1, dtype=torch.int, device=device), prefill_steps=[])

    def get_tokens_at(self, step_from: int, step_to: int | None=None) -> torch.Tensor:
        if step_to is None:
            step_to = step_from + 1
        return self.generated_tokens[:, step_from:step_to, :]

    def update_one(self, dec_out: torch.Tensor, step: int, apply_mask: bool=False):
        dec_out = dec_out.to(self.generated_tokens.dtype)
        if apply_mask:
            mask = self.generated_tokens[:, step, :] == -1
            self.generated_tokens[:, step, :] = torch.where(mask, dec_out, self.generated_tokens[:, step, :])
        else:
            self.generated_tokens[:, step, :] = dec_out

    def prefill(self, dec_out: torch.Tensor, prefill_steps: list[int]):
        length = dec_out.shape[1]
        self.generated_tokens[:, :length, :] = dec_out
        self.prefill_steps = prefill_steps