import torch

class StratifiedRayJitter:
    """ Uses informed stratified sampling which relies on perturbing a fixed anti-aliasing pattern"""

    def __init__(self, enabled=True, apply_every_n_iterations=1, num_samples=16, fixed_pattern=False, device='cuda'):
        self.enabled = enabled
        self.apply_every_n_iterations = apply_every_n_iterations
        self.device = device
        self.num_iterations_not_jittered = 0
        self.num_samples = num_samples
        subpixel_means = dict(s1=[[0.5, 0.5]], s2=[[0.25, 0.25], [0.75, 0.75]], s4=[[0.375, 0.125], [0.875, 0.375], [0.625, 0.875], [0.125, 0.625]], s8=[[0.5625, 0.6875], [0.4375, 0.3125], [0.8125, 0.4375], [0.3125, 0.8125], [0.1875, 0.1875], [0.0625, 0.5625], [0.6875, 0.0625], [0.9375, 0.9375]], s16=[[0.5625, 0.4375], [0.4375, 0.6875], [0.3125, 0.375], [0.75, 0.5625], [0.1875, 0.625], [0.625, 0.1875], [0.1875, 0.3125], [0.6875, 0.8125], [0.375, 0.125], [0.5, 0.9375], [0.25, 0.875], [0.125, 0.25], [0.0, 0.5], [0.9375, 0.75], [0.875, 0.0625], [0.0625, 0.0]])
        self.subpixel_means = {k: torch.tensor(v, device=self.device) for k, v in subpixel_means.items()}
        self.subpixel_offset_max = dict(s1=0.5, s2=0.3535533905932738, s4=0.2795084971874737, s8=0.13975424859373686, s16=0.04419417382415922)
        assert f's{num_samples}' in self.subpixel_means, f'num_samples={num_samples} not supported. Choose a value in: {list(self.subpixel_means.keys())}'
        self.pattern = self.subpixel_means[f's{num_samples}']
        self.relaxation = self.subpixel_offset_max[f's{num_samples}']
        self.fixed_pattern = fixed_pattern
        self.samples_generator = self._subsample_gen()

    def _shuffle(self, img_shape):
        """ Change the permuted order of samples """
        cyclic_order = torch.randperm(self.num_samples, device=self.device)
        pixel_indices = torch.randint(low=0, high=self.num_samples, size=img_shape, device=self.device)
        return (cyclic_order, pixel_indices)

    def _subsample_gen(self):
        cyclic_order, pixel_indices, prev_shape = (None, None, None)
        while True:
            img_shape = (yield)
            if prev_shape != img_shape:
                cyclic_order, pixel_indices = self._shuffle(img_shape)
            sample_indices = cyclic_order[pixel_indices]
            pixel_indices = (pixel_indices + 1) % self.num_samples
            jittered_pixels = self.pattern[sample_indices]
            perturb = 0.0
            if not self.fixed_pattern:
                perturb = self.relaxation * (torch.rand_like(jittered_pixels) * 2.0 - 1.0)
            jittered_pixels = (jittered_pixels + perturb) % 1.0
            prev_shape = img_shape
            yield jittered_pixels

    def __call__(self, img_shape):
        """ Given an image shape, returns a pattern of pixel values to sample """
        should_apply_jitter = self.num_iterations_not_jittered == 0
        self.num_iterations_not_jittered = (self.num_iterations_not_jittered + 1) % self.apply_every_n_iterations
        if self.enabled and should_apply_jitter:
            next(self.samples_generator)
            return self.samples_generator.send(img_shape)
        else:
            return 0.5 * torch.ones((*img_shape, 2), device=self.device)