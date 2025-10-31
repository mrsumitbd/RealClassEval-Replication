from addok.helpers import keys, magenta, white

class PairsIndexer:

    @staticmethod
    def index(pipe, key, doc, tokens, **kwargs):
        for token in list(set(tokens.keys())):
            pairs = set((t for t in tokens if t != token))
            if pairs:
                pipe.sadd(pair_key(token), *pairs)

    @staticmethod
    def deindex(db, key, doc, tokens, **kwargs):
        tokens = list(set(tokens))
        for i, token in enumerate(tokens):
            for token2 in tokens[i:]:
                if token != token2:
                    tmp_key = '|'.join(['didx', token, token2])
                    commons = db.zinterstore(tmp_key, [keys.token_key(token), keys.token_key(token2)])
                    db.delete(tmp_key)
                    if not commons:
                        db.srem(pair_key(token), token2)
                        db.srem(pair_key(token2), token)