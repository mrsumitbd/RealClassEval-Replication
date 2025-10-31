import torch

class AddGaussianNoise:

    def __init__(self, mean=0.0, std=0.0):
        self.mean = mean
        self.std = std

    def __call__(self, data):
        tensor = data['hidden_state_big']
        noise = torch.randn(tensor.size()) * self.std + self.mean
        noisy_tensor = tensor + noise
        data['hidden_state_big'] = noisy_tensor
        return data