from openai import OpenAI
import numpy as np
from tqdm.autonotebook import trange

class SentenceTransformerOpenAI:
    """Simple SentenceTransformer wrapper for OpenAI embedding models"""

    def __init__(self, model_name):
        self.client = OpenAI()
        self.model = model_name

    def __call__(self, features):
        return self.forward(features)

    def forward(self, features):
        embedding = get_openai_embedding(self.client, features, model=self.model)
        return {'sentence_embedding': embedding}

    def encode(self, sentences, batch_size: int=32, show_progress_bar: bool=None, output_value: str='sentence_embedding', convert_to_numpy: bool=True, convert_to_tensor: bool=False, device: str=None, normalize_embeddings: bool=False):
        input_was_string = False
        if isinstance(sentences, str) or not hasattr(sentences, '__len__'):
            sentences = [sentences]
            input_was_string = True
        all_embeddings = []
        for start_index in trange(0, len(sentences), batch_size, desc='Batches', disable=not show_progress_bar):
            sentences_batch = sentences[start_index:start_index + batch_size]
            embeddings = self.forward(sentences_batch)[output_value]
            all_embeddings.extend(embeddings)
        if convert_to_numpy:
            all_embeddings = np.asarray([np.array(emb) for emb in all_embeddings])
        if input_was_string:
            all_embeddings = all_embeddings[0]
        return all_embeddings