import numpy as np
from natix.validator.config import MODEL_NAMES

class MockSyntheticDataGenerator:

    def __init__(self, prompt_type, use_random_t2v_model, t2v_model_name):
        self.prompt_type = prompt_type
        self.t2v_model_name = t2v_model_name
        self.use_random_t2v_model = use_random_t2v_model

    def generate(self, k=1, real_images=None, modality='image'):
        if self.use_random_t2v_model:
            self.load_t2v_model('random')
        else:
            self.load_t2v_model(self.t2v_model_name)
        return [{'prompt': f'mock {self.prompt_type} prompt', 'image': create_random_image(), 'id': i} for i in range(k)]

    def load_diffuser(self, t2v_model_name) -> None:
        """
        loads a huggingface diffuser model.
        """
        if t2v_model_name == 'random':
            t2v_model_name = np.random.choice(MODEL_NAMES, 1)[0]
        self.t2v_model_name = t2v_model_name