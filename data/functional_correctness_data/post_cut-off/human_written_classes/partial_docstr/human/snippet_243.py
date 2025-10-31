from contextlib import nullcontext
import torch
import torch.nn as nn
import torch.nn.functional as F

class VAE:

    def __init__(self, z_dim=16, vae_pth='', load_mean_std=False, mean_std_path: str='', dtype=torch.float, device='cuda', is_amp=True, temporal_window: int=4):
        self.dtype = dtype
        self.device = device
        self.temporal_window = temporal_window
        mean = [-0.7571, -0.7089, -0.9113, 0.1075, -0.1745, 0.9653, -0.1517, 1.5508, 0.4134, -0.0715, 0.5517, -0.3632, -0.1922, -0.9497, 0.2503, -0.2921]
        std = [2.8184, 1.4541, 2.3275, 2.6558, 1.2196, 1.7708, 2.6052, 2.0743, 3.2687, 2.1526, 2.8652, 1.5579, 1.6382, 1.1253, 2.8251, 1.916]
        self.mean = torch.tensor(mean, dtype=dtype, device=device)
        self.std = torch.tensor(std, dtype=dtype, device=device)
        self.scale = [self.mean, 1.0 / self.std]
        self.model, self.img_mean, self.img_std, self.video_mean, self.video_std = _video_vae(pretrained_path=vae_pth, z_dim=z_dim, load_mean_std=load_mean_std, mean_std_path=mean_std_path, device=device, temporal_window=temporal_window)
        self.model = self.model.eval().requires_grad_(False)
        self.is_amp = is_amp
        if not is_amp:
            self.model = self.model.to(dtype=dtype)
            self.context = nullcontext()
        else:
            self.context = torch.amp.autocast('cuda', dtype=dtype)

    def count_param(self):
        return sum((p.numel() for p in self.model.parameters()))

    @torch.no_grad()
    def encode(self, videos):
        """
        videos: A list of videos each with shape [C, T, H, W].
        """
        in_dtype = videos.dtype
        with self.context:
            if not self.is_amp:
                videos = videos.to(self.dtype)
            latent = self.model.encode(videos, self.scale)
        latent = latent.to(in_dtype)
        return latent

    @torch.no_grad()
    def decode(self, zs):
        in_dtype = zs.dtype
        with self.context:
            if not self.is_amp:
                zs = zs.to(self.dtype)
            video_recon = self.model.decode(zs, self.scale)
        video_recon = video_recon.to(in_dtype)
        return video_recon