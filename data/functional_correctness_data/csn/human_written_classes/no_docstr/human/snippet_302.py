import sqlite3
import json

class OEmbeds:

    def __init__(self, path='oembeds.db'):
        self.db = sqlite3.connect(path)
        self.db.execute('\n            CREATE table IF NOT EXISTS oembeds (\n              url text PRIMARY KEY,\n              oembed text NOT NULL\n            )\n            ')

    def put(self, url, metadata):
        s = json.dumps(metadata)
        self.db.execute('INSERT INTO oembeds VALUES(?, ?)', [url, s])
        self.db.commit()

    def get(self, url):
        cursor = self.db.execute('SELECT oembed FROM oembeds WHERE url=?', [url])
        result = cursor.fetchone()
        if result is not None:
            return (json.loads(result[0]), True)
        else:
            return (None, False)