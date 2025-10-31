class GeohashIndexer:

    @staticmethod
    def index(pipe, key, doc, tokens, **kwargs):
        index_geohash(pipe, key, doc['lat'], doc['lon'])

    @staticmethod
    def deindex(db, key, doc, tokens, **kwargs):
        deindex_geohash(key, doc['lat'], doc['lon'])