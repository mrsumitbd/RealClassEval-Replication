import numpy as np
import torch

class InMemoryRetriever:
    """Simple retriever that keeps docs and embeddings in memory."""

    def __init__(self, data_file_or_table, embedding_model_name: str):
        """
        :param data_file_or_table: Parquet file of document snippets and embeddings,
         or an equivalent in-memory PyArrow Table object.
         Should have columns `id`, `begin`, `end`, `text`, and `embedding`.
        :param embedding_model_name: Name of Sentence Transformers model to use for
         embeddings. Must be the same model that was used to compute embeddings in the
         data file.
        """
        import pyarrow as pa
        import pyarrow.parquet as pq
        import sentence_transformers
        if isinstance(data_file_or_table, pa.Table):
            self._data_table = data_file_or_table
        else:
            self._data_table = pq.read_table(data_file_or_table)
        self._is_float16 = pa.types.is_float16(self._data_table.schema.field('embedding').type.value_type)
        self._embedding_model = sentence_transformers.SentenceTransformer(embedding_model_name, model_kwargs={'torch_dtype': 'float16' if self._is_float16 else 'float32'})
        embeddings_array = np.array(list(self._data_table.column('embedding').to_numpy()))
        self._embeddings = torch.tensor(embeddings_array)

    def retrieve(self, query: str, top_k: int=5) -> list[dict]:
        import pyarrow as pa
        import sentence_transformers
        query_embeddings = self._embedding_model.encode(query)
        raw_result = sentence_transformers.util.semantic_search(query_embeddings, self._embeddings, top_k=top_k)
        row_nums = [r['corpus_id'] for r in raw_result[0]]
        scores = [r['score'] for r in raw_result[0]]
        result = self._data_table.take(row_nums)
        result = result.append_column('score', pa.array(scores))
        return result.select(['id', 'title', 'url', 'begin', 'end', 'text', 'score'])