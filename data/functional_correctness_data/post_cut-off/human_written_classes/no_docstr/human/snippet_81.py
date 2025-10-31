import torch

class RandomRayJitter:

    def __init__(self, enabled=True, apply_every_n_iterations=1, device='cuda'):
        self.enabled = enabled
        self.apply_every_n_iterations = apply_every_n_iterations
        self.device = device
        self.num_iterations_not_jittered = 0

    def __call__(self, img_shape):
        should_apply_jitter = self.num_iterations_not_jittered == 0
        self.num_iterations_not_jittered = (self.num_iterations_not_jittered + 1) % self.apply_every_n_iterations
        if self.enabled and should_apply_jitter:
            return torch.rand((*img_shape, 2), device=self.device)
        else:
            return 0.5 * torch.ones((*img_shape, 2), device=self.device)