from typing import Dict

class ElasticsearchRetriever:
    """Retriever for documents hosted on an ElasticSearch server."""

    def __init__(self, corpus_name: str, host: str, **kwargs: Dict[str, int]):
        """
        :param hosts: Full url:port to the Elasticsearch server.
        :param kwargs: Additional kwargs to pass to the Elasticsearch class.
        """
        from elasticsearch import Elasticsearch
        self.corpus_name = corpus_name
        self.hosts = host
        self.kwargs = kwargs
        self.es = Elasticsearch(hosts=host, **kwargs)

    def create_es_body(self, limit, query):
        """
        :param limit: Max number of documents to retrieve.
        :param query: Query string for retrieving documents.
        """
        body = {'size': limit, 'query': {'bool': {'must': {'text_expansion': {'ml.tokens': {'model_id': '.elser_model_1', 'model_text': query}}}}}}
        return body

    def retrieve(self, query: str, top_k: int=5) -> list[dict]:
        import pyarrow as pa
        body = self.create_es_body(top_k, query)
        retriever_results = self.es.search(index=self.corpus_name, body=body)
        hits = retriever_results['hits']['hits']
        _documents = []
        for hit in hits:
            document = {'id': hit['_source']['id'], 'text': hit['_source']['text']}
            _documents.append(document)
        table = pa.Table.from_pylist(_documents)
        return table