import torch

class AlignmentStreamAnalyzer:

    def __init__(self, tfmr, queue, text_tokens_slice, alignment_layer_idx=9, eos_idx=0):
        """
        Some transformer TTS models implicitly solve text-speech alignment in one or more of their self-attention
        activation maps. This module exploits this to perform online integrity checks which streaming.
        A hook is injected into the specified attention layer, and heuristics are used to determine alignment
        position, repetition, etc.

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
        self.generated_tokens = []
        self.last_aligned_attns = []
        for i, (layer_idx, head_idx) in enumerate(LLAMA_ALIGNED_HEADS):
            self.last_aligned_attns += [None]
            self._add_attention_spy(tfmr, i, layer_idx, head_idx)

    def _add_attention_spy(self, tfmr, buffer_idx, layer_idx, head_idx):
        """
        Adds a forward hook to a specific attention layer to collect outputs.
        """

        def attention_forward_hook(module, input, output):
            """
            See `LlamaAttention.forward`; the output is a 3-tuple: `attn_output, attn_weights, past_key_value`.
            NOTE:
            - When `output_attentions=True`, `LlamaSdpaAttention.forward` calls `LlamaAttention.forward`.
            - `attn_output` has shape [B, H, T0, T0] for the 0th entry, and [B, H, 1, T0+i] for the rest i-th.
            """
            if isinstance(output, tuple) and len(output) > 1 and (output[1] is not None):
                step_attention = output[1].cpu()
                self.last_aligned_attns[buffer_idx] = step_attention[0, head_idx]
        target_layer = tfmr.layers[layer_idx].self_attn
        target_layer.register_forward_hook(attention_forward_hook)
        if hasattr(tfmr, 'config') and hasattr(tfmr.config, 'output_attentions'):
            self.original_output_attentions = tfmr.config.output_attentions
            tfmr.config.output_attentions = True

    def step(self, logits, next_token=None):
        """
        Emits an AlignmentAnalysisResult into the output queue, and potentially modifies the logits to force an EOS.
        """
        aligned_attn = torch.stack(self.last_aligned_attns).mean(dim=0)
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
        last_text_token_duration = A[15:, -3:].sum()
        long_tail = self.complete and A[self.completed_at:, -3:].sum(dim=0).max() >= 5
        alignment_repetition = self.complete and A[self.completed_at:, :-5].max(dim=1).values.sum() > 5
        if next_token is not None:
            if isinstance(next_token, torch.Tensor):
                token_id = next_token.item() if next_token.numel() == 1 else next_token.view(-1)[0].item()
            else:
                token_id = next_token
            self.generated_tokens.append(token_id)
            if len(self.generated_tokens) > 8:
                self.generated_tokens = self.generated_tokens[-8:]
        token_repetition = len(self.generated_tokens) >= 3 and len(set(self.generated_tokens[-2:])) == 1
        if token_repetition:
            repeated_token = self.generated_tokens[-1]
            logger.warning(f'🚨 Detected 2x repetition of token {repeated_token}')
        if cur_text_posn < S - 3 and S > 5:
            logits[..., self.eos_idx] = -2 ** 15
        if long_tail or alignment_repetition or token_repetition:
            logger.warning(f'forcing EOS token, long_tail={long_tail!r}, alignment_repetition={alignment_repetition!r}, token_repetition={token_repetition!r}')
            logits = -2 ** 15 * torch.ones_like(logits)
            logits[..., self.eos_idx] = 2 ** 15
        self.curr_frame_pos += 1
        return logits