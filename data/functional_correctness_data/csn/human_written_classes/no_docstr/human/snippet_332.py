class _SentenceTransformersModel:

    def __init__(self, model: str='sentence-transformers/paraphrase-multilingual-mpnet-base-v2', device: str='cpu'):
        from sentence_transformers import SentenceTransformer
        self.device = device
        self.model_name = model
        self.model = SentenceTransformer(self.model_name, device=self.device)

    def change_device(self, device: str):
        from sentence_transformers import SentenceTransformer
        self.device = device
        self.model = SentenceTransformer(self.model_name, device=self.device)

    def get_score(self, sentences1: str, sentences2: str) -> float:
        from sentence_transformers import util
        embedding_1 = self.model.encode(sentences1, convert_to_tensor=True)
        embedding_2 = self.model.encode(sentences2, convert_to_tensor=True)
        return 1 - util.pytorch_cos_sim(embedding_1, embedding_2)[0][0].item()