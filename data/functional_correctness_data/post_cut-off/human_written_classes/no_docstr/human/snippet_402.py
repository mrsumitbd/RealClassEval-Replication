import torch

class AddUniformNoise:

    def __init__(self, std=0.0):
        self.std = std

    def __call__(self, data):
        tensor = data['hidden_state_big']
        noise = (torch.rand_like(tensor) - 0.5) * self.std * 512 / tensor.shape[1]
        noisy_tensor = tensor + noise
        data['hidden_state_big'] = noisy_tensor
        return data