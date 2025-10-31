
import sqlite3
import json


class TokenStoreBase:

    def __init__(self, token_collection='default'):
        self.token_collection = token_collection
        self.conn = sqlite3.connect(f'{token_collection}.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS token_pairs
            (music_service_id TEXT, household_id TEXT, token_pair TEXT, PRIMARY KEY (music_service_id, household_id))
        ''')
        self.conn.commit()

    def save_token_pair(self, music_service_id, household_id, token_pair):
        token_pair_json = json.dumps(token_pair)
        self.cursor.execute('''
            INSERT OR REPLACE INTO token_pairs (music_service_id, household_id, token_pair)
            VALUES (?, ?, ?)
        ''', (music_service_id, household_id, token_pair_json))
        self.conn.commit()

    def load_token_pair(self, music_service_id, household_id):
        self.cursor.execute('''
            SELECT token_pair FROM token_pairs
            WHERE music_service_id = ? AND household_id = ?
        ''', (music_service_id, household_id))
        result = self.cursor.fetchone()
        if result:
            return json.loads(result[0])
        else:
            return None

    def has_token(self, music_service_id, household_id):
        self.cursor.execute('''
            SELECT 1 FROM token_pairs
            WHERE music_service_id = ? AND household_id = ?
        ''', (music_service_id, household_id))
        return self.cursor.fetchone() is not None
