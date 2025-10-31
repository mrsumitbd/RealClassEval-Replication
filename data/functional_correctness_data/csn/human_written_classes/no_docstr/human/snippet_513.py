class HousenumbersIndexer:

    @staticmethod
    def index(pipe, key, doc, tokens, **kwargs):
        housenumbers = doc.get('housenumbers', {})
        for number, data in housenumbers.items():
            index_geohash(pipe, key, data['lat'], data['lon'])

    @staticmethod
    def deindex(db, key, doc, tokens, **kwargs):
        housenumbers = doc.get('housenumbers', {})
        for token, data in housenumbers.items():
            deindex_geohash(key, data['lat'], data['lon'])