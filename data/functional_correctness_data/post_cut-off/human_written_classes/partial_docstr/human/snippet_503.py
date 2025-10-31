import torch
from types import MethodType

class AlignmentStreamAnalyzer:

    def __init__(self, tfmr, queue, text_tokens_slice, alignment_layer_idx=9, eos_idx=0):
        """
        Some transformer TTS models implicitly solve text-speech alignment in one or more of their self-
        attention activation maps. This module exploits this to perform online integrity checks which
        streaming. A hook is injected into the specified attention layer, and heuristics are used to determine
        alignment position, repetition, etc.

        NOTE: currently requires no queues.
        """
        self.text_tokens_slice = i, j = text_tokens_slice
        self.eos_idx = eos_idx
        self.alignment = torch.zeros(0, j - i)
        self.curr_frame_pos = 0
        self.text_position = 0
        self.started = False
        self.started_at = None
        self.complete = False
        self.completed_at = None
        self.last_aligned_attn = None
        self._add_attention_spy(tfmr, alignment_layer_idx)

    def _add_attention_spy(self, tfmr, alignment_layer_idx):
        """
        Adds a forward hook to a specific attention layer to collect outputs.

        Using `output_attentions=True` is incompatible with optimized attention kernels, so using it for all
        layers slows things down too much. (credit: jrm)
        """

        def attention_forward_hook(module, input, output):
            """
            See `LlamaAttention.forward`; the output is a 3-tuple: `attn_output, attn_weights,
            past_key_value`.

            NOTE:
            - When `output_attentions=True`, `LlamaSdpaAttention.forward` calls `LlamaAttention.forward`.
            - `attn_output` has shape [B, H, T0, T0] for the 0th entry, and [B, H, 1, T0+i] for the rest i-th.
            """
            step_attention = output[1].cpu()
            self.last_aligned_attn = step_attention[0].mean(0)
        target_layer = tfmr.layers[alignment_layer_idx].self_attn
        _ = target_layer.register_forward_hook(attention_forward_hook)
        original_forward = target_layer.forward

        def patched_forward(self, *args, **kwargs):
            kwargs['output_attentions'] = True
            return original_forward(*args, **kwargs)
        target_layer.forward = MethodType(patched_forward, target_layer)

    def step(self, logits):
        """Emits an AlignmentAnalysisResult into the output queue, and potentially modifies the logits to
        force an EOS.
        """
        aligned_attn = self.last_aligned_attn
        i, j = self.text_tokens_slice
        if self.curr_frame_pos == 0:
            A_chunk = aligned_attn[j:, i:j].clone().cpu()
        else:
            A_chunk = aligned_attn[:, i:j].clone().cpu()
        A_chunk[:, self.curr_frame_pos + 1:] = 0
        self.alignment = torch.cat((self.alignment, A_chunk), dim=0)
        A = self.alignment
        T, S = A.shape
        cur_text_posn = A_chunk[-1].argmax()
        discontinuity = not -4 < cur_text_posn - self.text_position < 7
        if not discontinuity:
            self.text_position = cur_text_posn
        false_start = not self.started and (A[-2:, -2:].max() > 0.1 or A[:, :4].max() < 0.5)
        self.started = not false_start
        if self.started and self.started_at is None:
            self.started_at = T
        self.complete = self.complete or self.text_position >= S - 3
        if self.complete and self.completed_at is None:
            self.completed_at = T
        _ = A[15:, -3:].sum()
        long_tail = self.complete and A[self.completed_at:, -3:].sum(dim=0).max() >= 10
        repetition = self.complete and A[self.completed_at:, :-5].max(dim=1).values.sum() > 5
        if long_tail or repetition:
            logger.warn(f'forcing EOS token, long_tail={long_tail!r}, repetition={repetition!r}')
            logits = -2 ** 15 * torch.ones_like(logits)
            logits[..., self.eos_idx] = 2 ** 15
        if cur_text_posn < S - 3:
            logits[..., self.eos_idx] = -2 ** 15
        self.curr_frame_pos += 1
        return logits