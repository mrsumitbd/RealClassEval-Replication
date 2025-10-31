from gr00t.model.policy import BasePolicy, Gr00tPolicy
import numpy as np
from policy_runner.gr00tn1.utils import DATA_CONFIG_MAP
import torch

class GR00TN1PolicyRunner:
    """
    Policy runner for GR00T N1 policy.

    Args:
        ckpt_path: Path to the checkpoint file.
        data_config: Data configuration.
        embodiment_tag: Embodiment tag.
        task_description: Task description. Default is "Perform a liver ultrasound."
        device: Device to run the model on. Default is "cuda" if available, otherwise "cpu".
        action_key: Key to extract from the model output. Default is "action.panda_hand".
    """

    def __init__(self, ckpt_path, data_config, embodiment_tag, task_description='Perform a liver ultrasound.', device='cuda' if torch.cuda.is_available() else 'cpu', action_key='action.panda_hand'):
        print(f'Loading model from {ckpt_path}...')
        data_config = DATA_CONFIG_MAP[data_config]
        modality_config = data_config.modality_config()
        modality_transform = data_config.transform()
        self.model: BasePolicy = Gr00tPolicy(model_path=ckpt_path, modality_config=modality_config, modality_transform=modality_transform, embodiment_tag=embodiment_tag, device=device)
        self.task_description = task_description
        self.action_key = action_key

    def infer(self, room_img, wrist_img, current_state) -> torch.Tensor:
        data_point = {'video.room': np.expand_dims(room_img, axis=0), 'video.wrist': np.expand_dims(wrist_img, axis=0), 'state.panda_hand': np.expand_dims(np.array(current_state), axis=0), 'annotation.human.task_description': self.task_description}
        return self.model.get_action(data_point)[self.action_key]