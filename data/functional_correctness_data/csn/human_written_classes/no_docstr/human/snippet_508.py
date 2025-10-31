from addok.config import config
from addok.db import DB
from addok.helpers import keys as dbkeys

class EdgeNgramIndexer:

    @staticmethod
    def index(pipe, key, doc, tokens, **kwargs):
        if config.INDEX_EDGE_NGRAMS:
            for token in tokens.keys():
                index_edge_ngrams(pipe, token)

    @staticmethod
    def deindex(db, key, doc, tokens, **kwargs):
        if config.INDEX_EDGE_NGRAMS:
            for token in tokens:
                tkey = dbkeys.token_key(token)
                if not DB.exists(tkey):
                    deindex_edge_ngrams(token)