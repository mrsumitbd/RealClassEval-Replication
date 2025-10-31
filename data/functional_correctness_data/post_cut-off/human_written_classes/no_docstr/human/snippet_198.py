import torch

class EDMScaling:

    def __init__(self, sigma_data: float=0.5):
        self.sigma_data = sigma_data

    def __call__(self, sigma: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
        c_skip = self.sigma_data ** 2 / (sigma ** 2 + self.sigma_data ** 2)
        c_out = sigma * self.sigma_data / (sigma ** 2 + self.sigma_data ** 2) ** 0.5
        c_in = 1 / (sigma ** 2 + self.sigma_data ** 2) ** 0.5
        c_noise = 0.25 * sigma.log()
        return (c_skip, c_out, c_in, c_noise)

    def sigma_loss_weights(self, sigma: torch.Tensor) -> torch.Tensor:
        return (sigma ** 2 + self.sigma_data ** 2) / (sigma * self.sigma_data) ** 2