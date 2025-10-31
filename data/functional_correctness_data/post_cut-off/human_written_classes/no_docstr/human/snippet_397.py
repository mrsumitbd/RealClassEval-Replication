from typing import Any
import torch

class DataCollatorWithPadding:

    def paddingtensor(self, intensors, dim):
        b, n, s = intensors.shape
        padding_tensor = torch.zeros(b, dim - n, s)
        return torch.cat((intensors, padding_tensor), dim=1)

    def paddingtensor2d(self, intensors, num):
        b, n = intensors.shape
        padding_tensor = torch.zeros(b, num - n, dtype=intensors.dtype)
        return torch.cat((intensors, padding_tensor), dim=1)

    def __call__(self, features: list[dict[str, Any]]) -> dict[str, Any]:
        max_length = max((item['hidden_state_big'].shape[1] for item in features))
        batch_input_ids = torch.cat([self.paddingtensor2d(item['input_ids'], max_length) for item in features])
        batch_hidden_states = torch.cat([self.paddingtensor(item['hidden_state_big'], max_length) for item in features])
        batch_target = torch.cat([self.paddingtensor(item['target'], max_length) for item in features])
        batch_loss_mask = torch.tensor([item['loss_mask'] + [0] * (max_length - len(item['loss_mask'])) for item in features])
        batch_attention_mask = torch.tensor([item['attention_mask'] + [0] * (max_length - len(item['attention_mask'])) for item in features])
        return {'input_ids': batch_input_ids, 'hidden_states': batch_hidden_states, 'target': batch_target, 'attention_mask': batch_attention_mask, 'loss_mask': batch_loss_mask}