import torch
from threedgrut_playground.utils.rng import rng_torch_low_discrepancy

class DepthOfField:
    RNG_MODE = 'low_discrepancy_seq'
    " Random number generator mode -\n        - independent random: straightforward torch's random, each number is IID\n        - low discrepancy sequences: uses Owen's scrambling of Sobol sequence, converges faster for accumulated spp \n    "

    def __init__(self, spp=64, aperture_size=0.1, focus_z=1.0):
        assert 0.0 <= aperture_size and 0.1 >= aperture_size
        assert self.RNG_MODE in ('independent_random', 'low_discrepancy_seq')
        self.aperture_size = aperture_size
        self.focus_z = focus_z
        self.spp = spp
        self.spp_accumulated_for_frame = 1

    def reset_accumulation(self):
        self.spp_accumulated_for_frame = 1

    def has_more_to_accumulate(self):
        return self.spp_accumulated_for_frame <= self.spp

    @staticmethod
    def pixel_to_disc_shirley(seed):
        """ seed is a point on the unit square [0, 1]"""
        a = 2.0 * seed[:, 0] - 1.0
        b = 2.0 * seed[:, 1] - 1.0
        mask = a * a > b * b
        pi = torch.pi
        r = torch.where(mask, a, b)
        phi = torch.where(mask, pi / 4.0 * (b / a), pi / 4.0 * (a / b) + pi / 2.0)
        disc_coords = (r * torch.cos(phi), r * torch.sin(phi))
        return torch.stack(disc_coords)

    @torch.cuda.nvtx.range('depth-of-field')
    def __call__(self, camera_R, rays):
        rays_ori, rays_dir = (rays.rays_ori, rays.rays_dir)
        pixel_x, pixel_y = (rays.pixel_x, rays.pixel_y)
        ray_count = rays_ori.shape[1] * rays_ori.shape[2]
        lookat = rays_ori + rays_dir * self.focus_z
        if DepthOfField.RNG_MODE == 'independent_random':
            seed = torch.rand([ray_count, 2], device=rays_ori.device)
        elif DepthOfField.RNG_MODE == 'low_discrepancy_seq':
            seed = (pixel_x.long() * 19349663 + pixel_y.long() * 96925573).reshape(ray_count) & 4294967295
            index = (seed.new_ones(ray_count) * self.spp_accumulated_for_frame).long()
            seed = rng_torch_low_discrepancy(index, seed)
            seed = torch.stack(seed, dim=1)
        else:
            raise ValueError(f'Unknown RNG mode: {DepthOfField.RNG_MODE}')
        blur = self.aperture_size * self.pixel_to_disc_shirley(seed)
        expanded_cam = camera_R[:3, :2][None].expand(ray_count, 3, 2)
        rays_ori = rays_ori + (expanded_cam @ blur.T[:, :, None]).reshape_as(rays_ori)
        rays_dir = (lookat - rays_ori) / self.focus_z
        self.spp_accumulated_for_frame += 1
        return (rays_ori, rays_dir)