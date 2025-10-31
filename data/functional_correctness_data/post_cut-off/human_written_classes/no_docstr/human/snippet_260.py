from diffsynth_engine.utils.memory.linear_regression import LinearRegression, r2_score
from typing import List
import torch

class MemoryPredictModel:

    def __init__(self, key_inputs=None):
        self.key_inputs = key_inputs
        self.model = LinearRegression()

    def predict(self, forward_kwargs):
        if self.model is None or self.key_inputs is None:
            raise ValueError('Model not initialized, please call from_pretrained first')
        input_args = _forward_kwargs_to_record(forward_kwargs, self.key_inputs)
        return self.model.predict(list(input_args.values()))[0].item()

    def train(self, records: List[dict]):
        if self.key_inputs is None:
            raise ValueError('Key inputs not set, please set key_inputs')
        X = []
        y = []
        for record in records:
            X.append(list({key: value for key, value in record.items() if key.startswith('input#')}.values()))
            y.append(record['total_memory'])
        self.model.fit(X, y)
        y_pred = self.model.predict(X)
        r2 = r2_score(y, y_pred)
        return r2

    def save_model(self, model_path):
        with open(model_path, 'wb') as f:
            torch.save({'key_inputs': self.key_inputs, 'model': self.model.serialize()}, f)

    @classmethod
    def from_pretrained(cls, model_path):
        with open(model_path, 'rb') as f:
            data = torch.load(f)
            model = cls(data['key_inputs'])
            model.model = LinearRegression.deserialize(data['model'])
            return model