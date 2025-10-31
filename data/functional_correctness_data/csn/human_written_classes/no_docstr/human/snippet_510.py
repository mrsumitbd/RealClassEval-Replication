from addok.helpers import keys

class RedisStore:

    def fetch(self, *keys):
        pipe = _DB.pipeline(transaction=False)
        for key in keys:
            pipe.get(key)
        for key, doc in zip(keys, pipe.execute()):
            if doc is not None:
                yield (key, doc)

    def upsert(self, *docs):
        pipe = _DB.pipeline(transaction=False)
        for key, blob in docs:
            pipe.set(key, blob)
        pipe.execute()

    def remove(self, *keys):
        pipe = _DB.pipeline(transaction=False)
        for key in keys:
            pipe.delete(key)
        pipe.execute()

    def flushdb(self):
        _DB.flushdb()