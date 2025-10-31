from typing import Dict, List, Optional

class BaseRetriever:

    def __init__(self, config):
        self.config = config
        self.retrieval_method = config.retrieval_method
        self.topk = config.retrieval_topk
        self.index_path = config.index_path
        self.corpus_path = config.corpus_path

    def _search(self, query: str, num: int, return_score: bool):
        raise NotImplementedError

    def _batch_search(self, query_list: List[str], num: int, return_score: bool):
        raise NotImplementedError

    def search(self, query: str, num: int=None, return_score: bool=False):
        return self._search(query, num, return_score)

    def batch_search(self, query_list: List[str], num: int=None, return_score: bool=False):
        return self._batch_search(query_list, num, return_score)